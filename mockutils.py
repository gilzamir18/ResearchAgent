from agenticblocks import as_tool
import json

@as_tool(name="web_search", description="retorna resultados de busca sobre o assunto pesquisado.")
def websearch_mock(keywords: str) -> str:
    print("websearch receive keywords ", keywords)
    with open('/home/gilzamir/projetos/ResearchAgent/mock_news.json', 'r', encoding='utf-8') as f:
        news = json.load(f)

    keywords_lower = keywords.lower().split()
    results = [article for article in news if any(kw in article.get('title', '').lower() or kw in article.get('content', '').lower() for kw in keywords_lower)]
    return "\n".join(results)


@as_tool(name="dbsearch", description="retorna resultados de busca sobre o assunto pesquisado.")
def databasesearch_mock(keywords: str) -> str:
    print("Database receive keywords: ", keywords)
    with open('/home/gilzamir/projetos/ResearchAgent/db.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    keywords_lower = keywords.lower().split()
    results = [line for line in content.split('\n') if any(kw in line.lower() for kw in keywords_lower)]
    return "\n".join(results)
