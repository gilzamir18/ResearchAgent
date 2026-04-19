import asyncio
from agenticblocks.blocks.llm.agent import AgentInput, LLMAgentBlock
from mockutils import websearch_mock, databasesearch_mock 

async def main():
    # Adiciona o bloco de agente ao grafo
    agent_block = LLMAgentBlock(
        name="research_agent",
        model="ollama/mistral-nemo:latest",
        description="Agente de pesquisa",
        debug=True,
        system_prompt="""Identifique o tópico de pesquisa, infira as palavras-chaves 
        relevantes, faça uma consulta sobre 
        pelo usuário e vai produzir um relatório sobre este tópico. Para isso, faça uma busca 
        em fontes de dados usando as ferramentas disponíveis. Chame uma vez cada ferramenta usando 
        palavras-chaves correspondentes ao tópico informado pelo usuário. 
        Use apenas dados retornados pelas ferramentas.
        Exemplo de tópico do usuário e palavras-chaves correspondentes que você deve usar nas
        ferramentas:
        
        Tópico: Brasil, Palabras-Chave: Brasil, brasil, países emergentes, país emergente
        Tópico: economia, Palavras-Chave: PIB, peço, petróleo, mercado, ...

        Estruture a resposta final destacando as informações relevantes de acordo com o tópico pesquisado.
        """,
        tools=[websearch_mock, databasesearch_mock],
        max_iterations=10,
        on_max_iterations="return_last", #it returns the last message.
        litellm_kwargs={"temperature": 0.7, "tool_choice": "auto"}
    )

    output = await agent_block.run(AgentInput(prompt="Qual é o Índice de Inflação ao Consumidor (IPCA) atual?"))
    print(output.response)

if __name__ == "__main__":
    asyncio.run(main())
