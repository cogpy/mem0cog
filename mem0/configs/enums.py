from enum import Enum


class MemoryType(Enum):
    SEMANTIC = "semantic_memory"
    EPISODIC = "episodic_memory"
    PROCEDURAL = "procedural_memory"
    WORKING = "working_memory"
    DECLARATIVE = "declarative_memory"
    ASSOCIATIVE = "associative_memory"
    CONTEXTUAL = "contextual_memory"


class CognitiveSynergyType(Enum):
    """Types of cognitive synergy between memory layers"""
    WORKING_SEMANTIC = "working_semantic_synergy"
    WORKING_EPISODIC = "working_episodic_synergy"
    WORKING_PROCEDURAL = "working_procedural_synergy"
    SEMANTIC_EPISODIC = "semantic_episodic_synergy"
    SEMANTIC_PROCEDURAL = "semantic_procedural_synergy"
    EPISODIC_PROCEDURAL = "episodic_procedural_synergy"
    MULTI_LAYER = "multi_layer_synergy"


class MemoryLayerPriority(Enum):
    """Priority levels for memory layer processing"""
    IMMEDIATE = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5
