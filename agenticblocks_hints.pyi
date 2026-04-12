# Type hints para AgenticBlocks.IO v0.8.1
# Este arquivo melhora o autocomplete no VS Code

from typing import Callable, Optional, Any, Dict, List

# Tipos de callback
class NodeResult:
    """Resultado da execução de um nó"""
    node_id: str
    output: Any
    status: str

OnNodeStartCallback = Callable[[str], None]
OnNodeEndCallback = Callable[[NodeResult], None]

# ============ agenticblocks.core.graph ============
class WorkflowGraph:
    """Grafo de fluxo de trabalho para conectar blocos"""
    
    def __init__(self) -> None:
        """Inicializa um novo grafo de fluxo de trabalho"""
        ...
    
    def add_block(self, block: 'Block', block_id: Optional[str] = None) -> str:
        """
        Adiciona um bloco ao grafo
        
        Args:
            block: O bloco a ser adicionado
            block_id: ID opcional para o bloco
            
        Returns:
            str: ID do bloco adicionado
        """
        ...
    
    def connect(self, source: str, target: str) -> None:
        """
        Conecta um bloco de origem a um bloco de destino
        
        Args:
            source: ID do bloco de origem
            target: ID do bloco de destino
        """
        ...
    
    def add_cycle(self, blocks: List[str]) -> None:
        """
        Adiciona um ciclo entre blocos
        
        Args:
            blocks: Lista de IDs dos blocos
        """
        ...
    
    def validate_connections(self) -> bool:
        """Valida se todas as conexões são válidas"""
        ...
    
    def collapsed_graph(self) -> 'Dict[str, Any]':
        """Retorna o grafo em formato colapsado"""
        ...


# ============ agenticblocks.runtime.executor ============
class WorkflowExecutor:
    """Executor de fluxos de trabalho"""
    
    def __init__(
        self,
        graph: WorkflowGraph,
        on_node_start: Optional[OnNodeStartCallback] = None,
        on_node_end: Optional[OnNodeEndCallback] = None
    ) -> None:
        """
        Inicializa o executor
        
        Args:
            graph: WorkflowGraph a ser executado
            on_node_start: Callback chamado quando um nó inicia
            on_node_end: Callback chamado quando um nó termina
        """
        ...
    
    def run(self, input_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Executa o fluxo de trabalho
        
        Args:
            input_data: Dados de entrada para o fluxo
            
        Returns:
            Resultado da execução
        """
        ...


# ============ agenticblocks.blocks.llm.agent ============
class LLMAgentBlock:
    """Bloco de agente com modelo de linguagem"""
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o agente com dados de entrada
        
        Args:
            input_data: Dados de entrada para o agente
            
        Returns:
            Saída do agente
        """
        ...
    
    def input_schema(self) -> Dict[str, Any]:
        """Retorna o schema de entrada do agente"""
        ...
    
    def output_schema(self) -> Dict[str, Any]:
        """Retorna o schema de saída do agente"""
        ...


# ============ agenticblocks.core ============
class Block:
    """Classe base para todos os blocos"""
    
    def run(self, input_data: Any) -> Any:
        """Executa o bloco com dados de entrada"""
        ...


class FunctionBlock(Block):
    """Bloco baseado em função Python"""
    
    def __init__(self, func: Callable) -> None:
        """
        Inicializa um bloco de função
        
        Args:
            func: Função Python a ser encapsulada
        """
        ...


# ============ agenticblocks Top-level ============
def as_tool(func: Callable) -> Callable:
    """
    Decorator para converter uma função em uma ferramenta
    
    Args:
        func: Função Python a ser convertida
        
    Returns:
        Função decorada como ferramenta
    """
    ...
