# 📝 Backlog de Tarefas: Avatar Falante com IA

> **Status Global:** Em Planejamento  
> **Diretório Raiz:** `C:/Users/ADM/.gemini/antigravity/scratch/projects/avatar-falante`

---

## 📌 Legenda
- `[ ]` Não iniciada
- `[/]` Em andamento
- `[x]` Concluída
- 🔴 Alta prioridade | 🟡 Média prioridade | 🟢 Baixa prioridade / Refinamento

---

## 🛠️ Fase 0: Setup Inicial do Projeto
- [x] 🔴 **TASK-000**: Inicializar repositório Git, .gitignore e vincular remoto no GitHub
- [x] 🔴 **TASK-001**: Criar estrutura de diretórios (`backend/`, `frontend/`, `docs/`, `models/`, `data/`)
- [ ] 🔴 **TASK-002**: Configurar ambiente virtual Python (`.venv` com Python 3.10 ou 3.11)
- [ ] 🔴 **TASK-003**: Criar `requirements.txt` base (FastAPI, uvicorn, langchain, chromadb, etc.)
- [ ] 🟡 **TASK-004**: Criar arquivo `.env.example` para configurações locais

---

## 1️⃣ Etapa 1: Chatbot Local (LLM & Prompt)
- [ ] 🔴 **TASK-101**: Instalar e validar Ollama em execução local
- [ ] 🔴 **TASK-102**: Baixar modelo base (`qwen2.5:3b-instruct` ou `llama3.2:3b`)
- [ ] 🔴 **TASK-103**: Criar `Modelfile` customizado com a persona do atendente (respostas concisas e tom falado)
- [ ] 🟡 **TASK-104**: Desenvolver protótipo rápido com Streamlit/Gradio para validar streaming de tokens e latência

---

## 2️⃣ Etapa 2: RAG (Base de Conhecimento com PDFs)
- [ ] 🔴 **TASK-201**: Criar pipeline de ingestão de PDFs em `backend/rag/ingest.py`
- [ ] 🔴 **TASK-202**: Configurar chunking semântico com `RecursiveCharacterTextSplitter`
- [ ] 🔴 **TASK-203**: Integrar modelo de embeddings `BAAI/bge-m3` (via FastEmbed ou Ollama)
- [ ] 🔴 **TASK-204**: Configurar armazenamento persistente com ChromaDB local
- [ ] 🟡 **TASK-205**: Criar retriever com filtro de score de relevância e fallback amigável quando a informação não constar nos documentos
- [ ] 🟢 **TASK-206**: Adicionar testes automatizados de perguntas e respostas para os documentos da disciplina

---

## 3️⃣ Etapa 3: Módulo de Voz (STT & TTS)
- [ ] 🔴 **TASK-301**: Integrar `faster-whisper` com modelo `base` / `small` em pt-BR
- [ ] 🟡 **TASK-302**: Adicionar `Silero VAD` para detecção de silêncio e fim de sentença de fala
- [ ] 🔴 **TASK-303**: Baixar e testar binário do `Piper TTS` com modelo `pt_BR-faber-medium` ou `pt_BR-edresson-low`
- [ ] 🔴 **TASK-304**: Implementar gerador de áudio em streaming (quebra de sentenças por pontuação `. ? !`)
- [ ] 🟡 **TASK-305**: Mensurar latência fim-a-fim de áudio (objetivo: < 1.5s)

---

## 4️⃣ Etapa 4: Avatar 3D & Lip-Sync
- [ ] 🔴 **TASK-401**: Configurar servidor frontend estático (HTML/JS/Vite)
- [ ] 🔴 **TASK-402**: Integrar `TalkingHead.js` ou `Three.js` + `@pixiv/three-vrm`
- [ ] 🟡 **TASK-403**: Obter/configurar modelo de avatar 3D (`.vrm`) com blendshapes de expressão e fala
- [ ] 🔴 **TASK-404**: Implementar sincronização labial (lip-sync) via visemas ou análise de frequências com Web Audio API
- [ ] 🟢 **TASK-405**: Adicionar animações idle (piscar de olhos e respiração suave)

---

## 5️⃣ Etapa 5: Orquestração e WebSocket em Tempo Real
- [ ] 🔴 **TASK-501**: Implementar servidor FastAPI com WebSocket bidirecional (`/ws/chat`)
- [ ] 🔴 **TASK-502**: Definir protocolo de payloads JSON/Binário para áudio, transcrição e visemas
- [ ] 🔴 **TASK-503**: Conectar fluxo contínuo: Microfone -> Whisper -> RAG/LLM -> Piper -> Avatar
- [ ] 🟡 **TASK-504**: Implementar cancelamento/interrupção de fala (barge-in do usuário)

---

## 6️⃣ Etapa 6: Empacotamento, Avaliação e LGPD
- [ ] 🟡 **TASK-601**: Escrever `Dockerfile` para o backend FastAPI
- [ ] 🟡 **TASK-602**: Criar `docker-compose.yml` orquestrando os serviços (LLM, Backend, Web)
- [ ] 🟢 **TASK-603**: Configurar framework de avaliação de respostas (Ragas)
- [ ] 🔴 **TASK-604**: Revisar conformidade LGPD: processamento em memória efêmera, termo de consentimento de microfone e ausência de chamadas a nuvens externas
