import anyio
from agenticblocks.core.graph import WorkflowGraph
from agenticblocks.runtime.executor import WorkflowExecutor
from agenticblocks.blocks.llm.agent import LLMAgentBlock, AgentInput
from agenticblocks import as_tool
from agenticblocks.tools.mcp_client import MCPClientBridge

@as_tool(name="get_user_input")
async def get_user_input(prompt: str) -> AgentInput:
    print("Sobre o que você quer pesquisar: ", end="")
    user_input = input()
    return AgentInput(prompt=f"Pesquise sobre o tópico {user_input}")

async def main():
    # Conecta ao servidor MCP fetch (inicia como subprocesso)
    mcp_fetch = MCPClientBridge(command="uvx", args=["mcp-server-fetch"])
    mcp_tools_fetch = await mcp_fetch.connect()  # retorna lista de MCPProxyBlock
    
    # Conecta ao servidor MCP fetch (inicia como subprocesso)
    mcp_search = MCPClientBridge(command="uvx", args=["duckduckgo-mcp-server"])
    mcp_tools_search = await mcp_search.connect()  # retorna lista de MCPProxyBlock
    
    graph = WorkflowGraph()

    agent_block = LLMAgentBlock(
        name="research_agent",
        model="ollama/mistral-nemo:latest",
        description="Agente de pesquisa",
        system_prompt="""Você é um assistente de pesquisa. Ao receber um tópico, use as ferramentas de busca e fetch para extrair informações de URLs. Escreva um relatório final em estilo jornalístico. Regra estrita: entregue apenas texto em prosa, sem absolutamente nenhuma formatação, listas ou marcações markdown.""",
        tools=mcp_tools_fetch+mcp_tools_search,   # <-- ferramentas vindas do servidor MCP
        max_iterations=10,
        on_max_iterations="return_last",
        litellm_kwargs={"temperature": 0.7, "tool_choice": "auto", "num_ctx": 32000}
    )

    graph.add_sequence(get_user_input, agent_block)

    executor = WorkflowExecutor(graph)
    ctx = await executor.run(initial_input={"prompt": ""})
    cr = ctx.get_output("research_agent")
    print(cr.response)

    try:
        await mcp_fetch.disconnect()
    except RuntimeError:
        pass

    try:
        await mcp_search.disconnect()
    except:
        pass

if __name__ == "__main__":
    anyio.run(main)
