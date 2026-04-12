# ResearchAgent

Um agente de pesquisa autônomo que recebe um tópico do usuário, busca informações na web em tempo real e produz um relatório em estilo jornalístico. Construído com [agenticblocks](https://github.com/gilzamir18/agenticblocks), MCP (Model Context Protocol) e modelos locais via Ollama.

## Como funciona

O agente segue um fluxo simples:

```
Entrada do usuário → Agente LLM (busca + fetch) → Relatório em prosa
```

1. O usuário informa um tópico de pesquisa.
2. O agente usa duas ferramentas MCP:
   - **DuckDuckGo** (`duckduckgo-mcp-server`) — busca URLs relevantes sobre o tópico.
   - **Fetch** (`mcp-server-fetch`) — acessa e extrai o conteúdo das páginas encontradas.
3. O modelo sintetiza as informações e entrega um texto jornalístico em prosa.

## Pré-requisitos

- Python 3.12+
- [Ollama](https://ollama.com/) instalado e rodando localmente
- [uvx](https://docs.astral.sh/uv/) instalado (para executar servidores MCP)

### Modelos Ollama necessários

```bash
ollama pull mistral-nemo
```

> O projeto também suporta outros modelos Ollama. Basta alterar o campo `model` em `research_appV2.py`.

## Instalação

```bash
git clone https://github.com/gilzamir18/ResearchAgent.git
cd ResearchAgent

python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

pip install agenticblocks mcp anyio litellm
```

> O pacote `agenticblocks` é a biblioteca de blocos utilizada para compor o workflow do agente.

## Uso

```bash
python research_appV2.py
```

Ao executar, o programa pergunta sobre qual tópico pesquisar:

```
Sobre o que você quer pesquisar: inteligência artificial no Brasil
```

O agente buscará informações na web e imprimirá um relatório em texto corrido, sem formatação Markdown.

## Estrutura do projeto

```
ResearchAgent/
├── research_appV2.py       # Versão principal: agente com MCP (DuckDuckGo + Fetch)
├── research_appV1.py       # Versão inicial: agente com ferramentas mock
├── research_app_debug.py   # Versão de chat interativo para depuração
├── mockutils.py            # Ferramentas mock de busca (usadas pela V1)
├── mock_news.json          # Dados mock para testes
└── agenticblocks_hints.pyi # Type hints do pacote agenticblocks
```

## Arquitetura

O workflow é definido com `WorkflowGraph` do `agenticblocks`:

```python
graph.add_sequence(get_user_input, agent_block)
```

- **`get_user_input`** — ferramenta decorada com `@as_tool` que captura a entrada do usuário e a formata como prompt para o agente.
- **`agent_block`** — `LLMAgentBlock` configurado com as ferramentas MCP, limite de iterações e instruções de system prompt.

As conexões MCP são gerenciadas por `MCPClientBridge`, que inicializa servidores como subprocessos via `uvx` e os expõe como blocos reutilizáveis.

## Versões

| Arquivo | Descrição |
|---|---|
| `research_appV1.py` | Usa ferramentas mock (sem internet) |
| `research_appV2.py` | Usa MCP real (DuckDuckGo + Fetch) |
| `research_app_debug.py` | Chat interativo multi-turno para debug |

## Licença

MIT
