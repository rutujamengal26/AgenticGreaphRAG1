from dataclasses import dataclass, field

@dataclass
class AgentState:
    query: str
    history: list = field(default_factory=list)
    confidence: float = 0.0
