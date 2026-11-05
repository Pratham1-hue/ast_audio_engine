from typing import Dict, Any
from app.schemas import AudioCue, ASTSymbolNode

# Sound profiles for node categories
NODE_WAVE_MAP = {
    "ClassDef": "sine",       # Deep, foundational tones
    "FunctionDef": "triangle",# Soft, melodic workhorse tones
    "AsyncFunctionDef": "triangle",
    "If": "sawtooth",         # Sharp tone for logic branches
    "For": "square",          # Rhythmic tone for iteration
    "While": "square",
    "Import": "sine",
    "Call": "sine"
}

BASE_FREQ = 220.0  # A3 note in Hz

def map_ast_to_audio_tree(raw_node: Dict[str, Any]) -> ASTSymbolNode:
    depth = raw_node["depth"]
    kind = raw_node["kind"]

    # Exponential frequency scale based on depth
    # Higher depth = higher pitch shift
    frequency = round(BASE_FREQ * (1.15 ** depth), 2)
    wave_type = NODE_WAVE_MAP.get(kind, "sine")
    
    # Deeper nesting gets shorter, sharper audio cues to prevent acoustic blur
    duration = max(0.08, round(0.25 - (depth * 0.02), 2))
    gain = max(0.1, round(0.4 - (depth * 0.03), 2))

    audio_cue = AudioCue(
        frequency=frequency,
        type=wave_type,
        duration=duration,
        gain=gain
    )

    children = [map_ast_to_audio_tree(child) for child in raw_node.get("children", [])]

    return ASTSymbolNode(
        id=raw_node["id"],
        name=raw_node["name"],
        kind=kind,
        line=raw_node["line"],
        depth=depth,
        audio=audio_cue,
        children=children
    )