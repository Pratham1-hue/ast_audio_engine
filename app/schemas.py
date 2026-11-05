from pydantic import BaseModel
from typing import List, Optional

class CodeAnalysisRequest(BaseModel):
    code: str
    filename: Optional[str] = "main.py"

class AudioCue(BaseModel):
    frequency: float
    type: str  # sine, square, triangle, sawtooth
    duration: float
    gain: float

class ASTSymbolNode(BaseModel):
    id: str
    name: str
    kind: str  # FunctionDef, ClassDef, Import, If, Loop
    line: int
    depth: int
    audio: AudioCue
    children: List['ASTSymbolNode'] = []

ASTSymbolNode.model_rebuild()

class AnalysisResponse(BaseModel):
    total_nodes: int
    max_depth: int
    tree: ASTSymbolNode