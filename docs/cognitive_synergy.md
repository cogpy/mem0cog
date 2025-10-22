# OpenCog-inspired Cognitive Memory Architecture

This document describes the cognitive synergy integration of parallel memory layers implemented in mem0cog, providing enhanced context-aware memory management for AI systems.

## Overview

The cognitive memory architecture extends mem0's existing memory system with OpenCog-inspired cognitive synergy between different memory subsystems. This allows for more sophisticated memory processing that mimics human cognitive processes through parallel memory layers and their interactions.

## Memory Types

The system now supports the following memory types:

### Core Memory Types
- **Semantic Memory**: Factual knowledge and concepts
- **Episodic Memory**: Personal experiences and events  
- **Procedural Memory**: Skills, processes, and procedures
- **Working Memory**: Currently active information and processing

### Extended Memory Types
- **Declarative Memory**: Explicit, conscious memories
- **Associative Memory**: Connection-based memory relationships
- **Contextual Memory**: Context-specific memory storage

## Cognitive Synergy Types

The system implements several types of cognitive synergy between memory layers:

- `WORKING_SEMANTIC`: Integration of active processing with factual knowledge
- `WORKING_EPISODIC`: Integration of active processing with experiential memory
- `WORKING_PROCEDURAL`: Integration of active processing with procedural knowledge
- `SEMANTIC_EPISODIC`: Connection between facts and experiences
- `SEMANTIC_PROCEDURAL`: Connection between knowledge and procedures
- `EPISODIC_PROCEDURAL`: Connection between experiences and procedures
- `MULTI_LAYER`: Complex multi-layer synergy integration

## Architecture Components

### CognitiveMemoryManager

The core orchestrator that manages parallel memory layers and their synergistic interactions.

```python
from mem0 import Memory, CognitiveContext
from mem0.configs.enums import MemoryType, CognitiveSynergyType

# Initialize memory with cognitive synergy
memory = Memory()

# Set cognitive context
memory.set_cognitive_context(
    user_id="user_123",
    domain="healthcare",
    attention_focus=["diagnosis", "treatment"],
    cognitive_load=0.7,
    active_goals=["accurate diagnosis"]
)
```

### CognitiveContext

Represents the cognitive state and context for memory operations:

```python
context = CognitiveContext(
    user_id="user_123",
    session_id="session_456", 
    domain="education",
    attention_focus=["learning", "problem solving"],
    emotional_state="focused",
    cognitive_load=0.6,
    active_goals=["master concepts"]
)
```

## Usage Examples

### Adding Memory with Cognitive Synergy

```python
# Add memory that will be processed across multiple layers
result = memory.add_with_cognitive_synergy(
    messages="Patient shows symptoms of hypertension",
    user_id="doctor_1",
    memory_types=[MemoryType.SEMANTIC, MemoryType.EPISODIC, MemoryType.WORKING]
)

print(result["synergy_activations"])  # Shows active synergies
```

### Searching with Cognitive Synergy

```python
# Search across multiple memory layers with synergy
results = memory.search_with_cognitive_synergy(
    query="treatment protocols for hypertension",
    user_id="doctor_1",
    synergy_types=[
        CognitiveSynergyType.WORKING_SEMANTIC,
        CognitiveSynergyType.WORKING_PROCEDURAL
    ]
)

# Results include synergy scores and layer information
for result in results["results"]:
    print(f"Memory: {result['memory']}")
    print(f"Source Layer: {result['source_layer']}")
    print(f"Synergy Score: {result.get('synergy_score', 0)}")
```

### Monitoring Cognitive State

```python
# Get detailed cognitive state
state = memory.get_cognitive_state(user_id="doctor_1")

print("Memory Layer Activations:")
for layer, info in state["memory_layers"].items():
    print(f"  {layer}: {info['activation_level']:.2f}")

print("Active Synergies:")
for synergy, info in state["synergy_edges"].items():
    if info["last_activation"]:
        print(f"  {synergy}: strength {info['strength']:.2f}")
```

## Configuration

Configure cognitive synergy in your memory config:

```python
from mem0.configs.base import MemoryConfig

config = MemoryConfig()
config.enable_cognitive_synergy = True
config.cognitive_synergy_config = {
    "max_parallel_layers": 6,
    "synergy_strength_threshold": 0.5,
    "working_memory_capacity": 150,
    "cross_layer_association_strength": 0.7,
    "cognitive_load_adaptation": True
}

memory = Memory(config)
```

## Use Cases

### Healthcare AI Assistant

```python
# Set healthcare context
memory.set_cognitive_context(
    user_id="doctor_smith",
    domain="healthcare", 
    attention_focus=["patient care", "diagnosis"],
    cognitive_load=0.8
)

# Add medical knowledge (semantic)
memory.add_with_cognitive_synergy(
    "Hypertension is defined as BP > 140/90 mmHg",
    user_id="doctor_smith",
    memory_types=[MemoryType.SEMANTIC, MemoryType.WORKING]
)

# Add patient encounter (episodic)
memory.add_with_cognitive_synergy(
    "Patient John presented with chest pain today",
    user_id="doctor_smith", 
    memory_types=[MemoryType.EPISODIC, MemoryType.WORKING]
)

# Add clinical procedure (procedural)
memory.add_with_cognitive_synergy(
    "BP measurement: 1) Position cuff 2) Inflate 3) Release",
    user_id="doctor_smith",
    memory_types=[MemoryType.PROCEDURAL, MemoryType.WORKING]
)

# Query with multi-layer synergy
results = memory.search_with_cognitive_synergy(
    "how to assess chest pain with elevated BP",
    user_id="doctor_smith",
    synergy_types=[CognitiveSynergyType.MULTI_LAYER]
)
```

### Educational AI Tutor

```python
# Set learning context
memory.set_cognitive_context(
    user_id="student_alice",
    domain="mathematics",
    attention_focus=["algebra", "problem solving"],
    cognitive_load=0.6,
    active_goals=["master quadratic equations"]
)

# Add concept (semantic)
memory.add_with_cognitive_synergy(
    "Quadratic equation: ax² + bx + c = 0",
    user_id="student_alice"
)

# Add learning experience (episodic)  
memory.add_with_cognitive_synergy(
    "I solved 5 quadratic problems correctly today",
    user_id="student_alice"
)

# Add solution method (procedural)
memory.add_with_cognitive_synergy(
    "Factoring method: 1) Move terms 2) Factor 3) Solve",
    user_id="student_alice"
)
```

## Benefits

### Enhanced Context Awareness
- Memories are processed and retrieved with rich contextual information
- Cognitive load and attention focus influence memory operations
- Domain-specific processing optimizations

### Parallel Processing
- Multiple memory layers process information simultaneously
- Reduced latency through concurrent operations
- Better resource utilization

### Synergistic Integration
- Cross-layer associations enhance memory retrieval
- Synergy scores improve relevance ranking
- Multi-modal memory connections

### Adaptive Behavior
- System adapts to user's cognitive state
- Dynamic memory layer activation
- Context-driven memory routing

## Performance Considerations

### Memory Layer Activation
- Working memory acts as the central hub for active processing
- Layer activation levels indicate processing intensity
- Automatic deactivation of unused layers

### Synergy Strength Management
- Synergy connections have strength thresholds
- Weak connections are pruned automatically
- Strong connections are reinforced through use

### Cognitive Load Adaptation
- System adjusts processing based on cognitive load
- High load focuses on essential memories
- Low load enables broader memory exploration

## Advanced Features

### Memory Association Networks
- Automatic creation of cross-layer memory associations
- Association strength based on synergy activations
- Network analysis for memory relationship discovery

### Temporal Context Integration
- Time-aware memory processing
- Temporal proximity influences association strength
- Historical activation tracking

### Emotional State Integration
- Emotional context affects memory encoding and retrieval
- Emotional tagging of memories
- Mood-congruent memory effects

## API Reference

### Core Methods

#### `add_with_cognitive_synergy(messages, **kwargs)`
Add memory with cognitive synergy processing across multiple layers.

**Parameters:**
- `messages`: Content to store
- `user_id`: User identifier
- `memory_types`: List of memory types to activate
- `cognitive_context`: Cognitive context for processing

**Returns:**
- Dictionary with results and synergy activations

#### `search_with_cognitive_synergy(query, **kwargs)`
Search memories with cognitive synergy integration.

**Parameters:**
- `query`: Search query
- `user_id`: User identifier  
- `memory_types`: Memory types to search
- `synergy_types`: Synergy types to apply

**Returns:**
- Dictionary with results, layer information, and synergy scores

#### `set_cognitive_context(user_id, **context_params)`
Set or update cognitive context for a user.

**Parameters:**
- `user_id`: User identifier
- `domain`: Domain context
- `attention_focus`: List of attention focus items
- `cognitive_load`: Load level (0.0-1.0)
- `emotional_state`: Emotional state
- `active_goals`: List of active goals

#### `get_cognitive_state(user_id)`
Retrieve current cognitive state and memory layer information.

**Returns:**
- Dictionary with cognitive context, layer states, and synergy information

## Best Practices

### Context Management
- Set appropriate cognitive context for your domain
- Update attention focus as user interactions evolve
- Monitor and adjust cognitive load based on task complexity

### Memory Type Selection
- Use specific memory types for targeted processing
- Combine complementary memory types for rich representation
- Let the system auto-infer types when appropriate

### Synergy Optimization
- Choose synergy types that match your use case
- Monitor synergy activations to understand system behavior
- Adjust synergy thresholds based on performance needs

### Performance Tuning
- Configure parallel processing limits based on resources
- Set appropriate working memory capacity
- Use cognitive load adaptation for dynamic optimization

## Troubleshooting

### Low Synergy Activation
- Check cognitive context setup
- Verify memory type compatibility
- Adjust synergy strength thresholds

### Performance Issues
- Reduce max parallel layers
- Lower working memory capacity
- Disable cognitive load adaptation if not needed

### Memory Association Problems
- Verify cross-layer association strength settings
- Check synergy threshold configuration
- Monitor activation history for debugging

## Future Enhancements

### Planned Features
- Attention mechanism integration
- Hierarchical memory organization
- Reinforcement learning for synergy optimization
- Multi-user cognitive state management
- Advanced temporal reasoning

### Research Areas
- Neuroplasticity-inspired memory adaptation
- Cognitive load prediction models
- Emotional memory integration
- Social cognitive memory sharing