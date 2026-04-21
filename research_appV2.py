import asyncio
from agenticblocks.blocks.llm.agent import LLMAgentBlock, AgentInput
from mockutils import websearch_mock, databasesearch_mock 
from agenticblocks import as_tool
from agenticblocks.core.graph import WorkflowGraph
from agenticblocks.runtime.executor import WorkflowExecutor


@as_tool(name="get_user_input")
async def get_user_input(prompt:str) -> AgentInput :
    print("Sobre o que você quer pesquisar (por enquanto respondemos sobre muito pouco): ", end="")
    user_input = input()
    return AgentInput(prompt=f"Pesquise sobre o tópico {user_input}")

async def main():
    # Cria o grafo de workflow
    graph = WorkflowGraph()

    # Adiciona o bloco de agente ao grafo
    agent_block = LLMAgentBlock(
        name="research_agent",
        model="ollama/mistral-nemo:latest",
        description="Agente de pesquisa",
        system_prompt="""Você é um assistente de pesquisa especializado em ajudar pesquisadores
        sobre os mais diversos tópicos. Você vai receber uma consulta sobre um tópico dado
        pelo usuário e vai produzir um relatório sobre este tópico. Para isso, faça uma busca 
        em fontes de dados usando as ferramentas disponíveis. Chame uma vez cada ferramenta usando 
        palavras-chaves correspondentes ao tópico informado pelo usuário. 
        Use apenas dados retornados pelas ferramentas.
        Exemplo de tópico do usuário e palavras-chaves correspondentes que você deve usar nas
        ferramentas:
        
        Tópico: Brasil, Palabras-Chave: Brasil, brasil, países emergentes, país emergente
        Tópico: economia, Palavras-Chave: PIB, peço, petróleo, mercado, ...

        Estruture a resposta final destacando as informações relevantes de acordo com o tópico 
        pesquisado.
        """,
        tools=[websearch_mock, databasesearch_mock],
        debug=True,
        max_iterations=5,
        on_max_iterations="return_last", #it returns the last message.
        litellm_kwargs={"temperature": 1.0, "tool_choice": "auto"}
    )

    graph.add_sequence(get_user_input, agent_block)

    # Cria o executor do workflow
    executor = WorkflowExecutor(graph)

    # Executa o workflow com dados de entrada
    ctx = await executor.run(initial_input={"prompt": ""})
    cr  = ctx.get_output("research_agent")
    print("Chat conversation ", cr.response)

if __name__ == "__main__":
    asyncio.run(main())
