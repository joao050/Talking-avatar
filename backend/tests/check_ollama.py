"""Script de diagnostico e validacao local do Ollama (TASK-101).

Verifica:
1. Presenca e versao do binario do Ollama.
2. Conectividade com a API HTTP local (http://localhost:11434).
3. Variaveis de protecao para ambientes com baixa memoria RAM (perfil 4GB).
4. Smoke test opcional de inferencia enxuta (--smoke-test <modelo>).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LOW_RAM_RECOMMENDED_ENV = {
    "OLLAMA_MAX_LOADED_MODELS": "1",
    "OLLAMA_NUM_PARALLEL": "1",
    "OLLAMA_KEEP_ALIVE": "2m",
    "OLLAMA_FLASH_ATTENTION": "1",
}


def get_effective_env(key: str) -> str | None:
    """Busca variavel no ambiente atual ou no Registro do Usuario no Windows."""
    val = os.getenv(key)
    if val:
        return val
    if sys.platform == "win32":
        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as reg_key:
                reg_val, _ = winreg.QueryValueEx(reg_key, key)
                return str(reg_val)
        except OSError:
            return None
    return None


def find_ollama_binary() -> str | None:
    """Localiza o executavel do Ollama no PATH ou no diretorio padrao do Windows."""
    in_path = shutil.which("ollama")
    if in_path:
        return in_path

    local_app_data = os.getenv("LOCALAPPDATA", "")
    if local_app_data:
        win_default = Path(local_app_data) / "Programs" / "Ollama" / "ollama.exe"
        if win_default.exists():
            return str(win_default)

    return None


def check_cli_version(binary_path: str) -> str:
    """Retorna a versao reportada pelo CLI do Ollama."""
    result = subprocess.run(
        [binary_path, "--version"],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    output = (result.stdout or result.stderr).strip()
    return output or "versao desconhecida"


def _open_no_proxy(req: urllib.request.Request, timeout: float):
    """Abre conexao HTTP ignorando proxies de sistema para chamadas locais."""
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return opener.open(req, timeout=timeout)


def http_json(url: str, payload: dict | None = None, timeout: float = 30.0) -> dict:
    """Executa requisicao GET ou POST JSON usando apenas biblioteca padrao."""
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers)
    with _open_no_proxy(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_smoke_test(base_url: str, model: str) -> bool:
    """Executa um teste curto de streaming medindo TTFT e tokens/s e libera a RAM."""
    print(f"\n[4/4] Executando smoke test de inferencia com '{model}' (num_ctx=2048)...")
    payload = {
        "model": model,
        "prompt": "Responda em uma unica frase curta em portugues: Ola, voce esta pronto?",
        "stream": True,
        "keep_alive": "30s",
        "options": {
            "num_ctx": 2048,
            "temperature": 0.2,
            "num_predict": 40,
        },
    }

    req = urllib.request.Request(
        f"{base_url}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    start = time.perf_counter()
    first_token_time: float | None = None
    chunks: list[str] = []
    eval_count = 0
    eval_duration_ns = 0

    try:
        with _open_no_proxy(req, timeout=120.0) as resp:
            for raw_line in resp:
                if not raw_line.strip():
                    continue
                event = json.loads(raw_line.decode("utf-8"))
                token = event.get("response", "")
                if token:
                    if first_token_time is None:
                        first_token_time = time.perf_counter() - start
                    chunks.append(token)
                if event.get("done"):
                    eval_count = int(event.get("eval_count", len(chunks)))
                    eval_duration_ns = int(event.get("eval_duration", 0))
                    break
    except urllib.error.URLError as exc:
        print(f"  [ERRO] Falha durante inferencia: {exc}")
        return False

    total_s = time.perf_counter() - start
    ttft_s = first_token_time if first_token_time is not None else total_s
    tps = (eval_count / (eval_duration_ns / 1e9)) if eval_duration_ns > 0 else 0.0
    full_response = "".join(chunks).strip()

    print(f"  -> Resposta: {full_response}")
    print(f"  -> TTFT: {ttft_s:.2f}s | Velocidade: {tps:.1f} tok/s | Total: {total_s:.2f}s")

    # Descarrega o modelo imediatamente da memoria RAM (keep_alive=0)
    try:
        http_json(
            f"{base_url}/api/generate",
            payload={"model": model, "keep_alive": 0},
            timeout=15.0,
        )
        print(f"  -> Modelo '{model}' descarregado da RAM com sucesso (keep_alive=0).")
    except urllib.error.URLError:
        pass

    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida instalacao e execucao local do Ollama.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="URL base do servidor Ollama.")
    parser.add_argument("--smoke-test", metavar="MODEL", help="Executa inferencia curta no modelo informado.")
    args = parser.parse_args()

    print("=== Validacao Local do Ollama (Perfil Ultra-Leve 4GB RAM) ===")

    # 1. Binario CLI
    binary = find_ollama_binary()
    if not binary:
        print("[1/4] Binario CLI: [ERRO] 'ollama' nao encontrado no PATH nem em AppData.")
        return 1
    version_str = check_cli_version(binary)
    print(f"[1/4] Binario CLI: [OK] {binary} ({version_str})")

    # 2. Variaveis de ambiente de protecao de RAM
    print("[2/4] Diretrizes de Economia de RAM (Usuario/Processo):")
    for key, recommended in LOW_RAM_RECOMMENDED_ENV.items():
        current = get_effective_env(key)
        status = f"configurado ({current})" if current else f"padrao (recomendado={recommended})"
        print(f"  - {key}: {status}")

    # 3. Servidor HTTP e modelos locais
    try:
        api_ver = http_json(f"{args.base_url}/api/version", timeout=5.0)
        tags_resp = http_json(f"{args.base_url}/api/tags", timeout=5.0)
    except urllib.error.URLError as exc:
        print(f"[3/4] Servidor HTTP ({args.base_url}): [ERRO] Inacessivel ({exc})")
        return 1

    models = [m.get("name", "?") for m in tags_resp.get("models", [])]
    models_label = ", ".join(models) if models else "nenhum modelo baixado ainda"
    print(f"[3/4] Servidor HTTP ({args.base_url}): [OK] API v{api_ver.get('version', '?')}")
    print(f"  -> Modelos disponiveis localmente: {models_label}")

    # 4. Smoke test opcional
    if args.smoke_test:
        if not run_smoke_test(args.base_url, args.smoke_test):
            return 1
    else:
        print("[4/4] Smoke test pulado (use --smoke-test qwen2.5:0.5b para testar geracao).")

    print("\nResultado: Ollama validado e operacional!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
