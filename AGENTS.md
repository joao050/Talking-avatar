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

## 5. Fluxo de Git (Branches, Commits, Push e Pull)
- **Atualização Prévia (`git pull`):** Antes de iniciar qualquer nova tarefa, voltar para a branch `main` e executar `git pull origin main` para sincronizar os merges recentes do GitHub.
- **Branch por Tarefa:** Criar uma branch dedicada para cada task antes de criar ou modificar arquivos, nomeada com o código e descrição da tarefa (ex: `task-001/estrutura-diretorios`).
- **Comentários de Commit com o Usuário:** Antes de registrar commits, consultar o usuário sobre qual mensagem/comentário deve ser utilizado (ou sugerir e aguardar confirmação/edição).
- **Push sob Confirmação:** O comando `git push` para o GitHub só será executado após a confirmação explícita do usuário.
- **Pull Request e Merge Manual:** O Pull Request no GitHub será revisado e mergado na `main` manualmente pelo usuário.

