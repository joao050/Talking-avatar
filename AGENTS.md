# Diretrizes do Projeto: Avatar Falante com IA

Este documento estabelece as regras operacionais obrigatórias para atuação do agente neste repositório.

## 1. Leitura Prévia Obrigatória (Otimização de Tokens)
Antes de criar ou alterar qualquer arquivo de código ou configuração:
- Consultar obrigatoriamente os três arquivos norteadores:
  1. `project_map.md` (arquitetura, contratos WebSocket e estrutura)
  2. `tasks.md` (status atual e backlog priorizado)
  3. `trilha_avatar_ia.md` (diretrizes técnicas e componentes da esteira)
- Localizar pontualmente onde a intervenção deve ser feita, evitando varreduras globais cegas no projeto para manter o consumo de contexto enxuto.

## 2. Documentação e Sincronização Contínua
Imediatamente após criar ou modificar qualquer código ou arquivo:
- Atualizar o `tasks.md`, refletindo o status real (`[x]` concluída, `[/]` em andamento).
- Atualizar o `project_map.md` caso haja nova rota, convenção, payload ou alteração na árvore de diretórios.

## 3. Auditoria Preventiva e Alinhamento com o Usuário
- Em caso de dúvidas técnicas, ambiguidades de arquitetura, incompatibilidade de bibliotecas ou escolhas de hardware/modelos, realizar uma breve auditoria perguntando diretamente ao usuário antes de prosseguir com a implementação.
- Nunca assumir premissas incertas que possam causar retrabalho.

## 4. Prontidão para Versionamento (GitHub)
- O código deste projeto será disponibilizado em um repositório no GitHub.
- Manter o repositório limpo, com código modular, commits organizados e exclusão rigorosa de dados voláteis, arquivos pesados e caches (`.venv/`, `models/`, `data/vector_store/`, `__pycache__/`, `.env`) via `.gitignore`.
