"""
OpenCog-inspired Cognitive Memory Architecture for mem0

This module implements an intelligent memory architecture that integrates
cognitive synergy between parallel memory layers for enhanced context-aware
memory management and retrieval.
"""

import asyncio
import json
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from collections import defaultdict
from datetime import datetime

from mem0.configs.enums import MemoryType, CognitiveSynergyType, MemoryLayerPriority
from mem0.configs.base import MemoryItem
from mem0.memory.base import MemoryBase


logger = logging.getLogger(__name__)


@dataclass
class CognitiveContext:
    """Represents the cognitive context for memory operations"""
    user_id: str
    session_id: Optional[str] = None
    domain: Optional[str] = None
    attention_focus: List[str] = field(default_factory=list)
    emotional_state: Optional[str] = None
    cognitive_load: float = 0.5  # 0.0 to 1.0
    temporal_context: Optional[datetime] = None
    active_goals: List[str] = field(default_factory=list)


@dataclass
class MemoryLayerState:
    """State information for a memory layer"""
    layer_type: MemoryType
    activation_level: float = 0.0
    last_accessed: Optional[datetime] = None
    processing_queue: List[Any] = field(default_factory=list)
    synergy_connections: Set[MemoryType] = field(default_factory=set)
    priority: MemoryLayerPriority = MemoryLayerPriority.NORMAL


@dataclass
class SynergyEdge:
    """Represents a synergy connection between memory layers"""
    source_layer: MemoryType
    target_layer: MemoryType
    synergy_type: CognitiveSynergyType
    strength: float = 1.0
    last_activation: Optional[datetime] = None


class CognitiveMemoryManager:
    """
    OpenCog-inspired cognitive memory manager that orchestrates
    parallel memory layers with cognitive synergy integration
    """
    
    def __init__(self, memory_base: MemoryBase, config: Dict[str, Any] = None):
        self.memory_base = memory_base
        self.config = config or {}
        
        # Initialize memory layer states
        self.memory_layers: Dict[MemoryType, MemoryLayerState] = {
            layer_type: MemoryLayerState(layer_type=layer_type)
            for layer_type in MemoryType
        }
        
        # Initialize synergy connections
        self.synergy_edges: List[SynergyEdge] = []
        self._initialize_synergy_graph()
        
        # Cognitive processing
        self.executor = ThreadPoolExecutor(max_workers=8, thread_name_prefix="cognitive_memory")
        self.cognitive_contexts: Dict[str, CognitiveContext] = {}
        self.processing_lock = threading.RLock()
        self.active_processing: Dict[str, bool] = defaultdict(bool)
        
        # Memory activation tracking
        self.activation_history: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)
        self.memory_associations: Dict[str, Set[str]] = defaultdict(set)
        
        logger.info("Cognitive Memory Manager initialized with OpenCog architecture")
    
    def _initialize_synergy_graph(self):
        """Initialize the cognitive synergy graph between memory layers"""
        # Working memory synergies (high strength)
        self.synergy_edges.extend([
            SynergyEdge(MemoryType.WORKING, MemoryType.SEMANTIC, 
                       CognitiveSynergyType.WORKING_SEMANTIC, strength=0.9),
            SynergyEdge(MemoryType.WORKING, MemoryType.EPISODIC,
                       CognitiveSynergyType.WORKING_EPISODIC, strength=0.8),
            SynergyEdge(MemoryType.WORKING, MemoryType.PROCEDURAL,
                       CognitiveSynergyType.WORKING_PROCEDURAL, strength=0.7),
        ])
        
        # Cross-layer synergies (medium strength)
        self.synergy_edges.extend([
            SynergyEdge(MemoryType.SEMANTIC, MemoryType.EPISODIC,
                       CognitiveSynergyType.SEMANTIC_EPISODIC, strength=0.6),
            SynergyEdge(MemoryType.SEMANTIC, MemoryType.PROCEDURAL,
                       CognitiveSynergyType.SEMANTIC_PROCEDURAL, strength=0.5),
            SynergyEdge(MemoryType.EPISODIC, MemoryType.PROCEDURAL,
                       CognitiveSynergyType.EPISODIC_PROCEDURAL, strength=0.4),
        ])
        
        # Update synergy connections in layer states
        for edge in self.synergy_edges:
            self.memory_layers[edge.source_layer].synergy_connections.add(edge.target_layer)
            self.memory_layers[edge.target_layer].synergy_connections.add(edge.source_layer)
    
    def register_cognitive_context(self, context: CognitiveContext) -> None:
        """Register a cognitive context for context-aware processing"""
        self.cognitive_contexts[context.user_id] = context
        logger.debug(f"Registered cognitive context for user {context.user_id}")
    
    def add_memory_with_cognitive_synergy(
        self, 
        content: Union[str, List[Dict[str, str]]], 
        user_id: str,
        memory_types: List[MemoryType] = None,
        context: Optional[CognitiveContext] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Add memory with cognitive synergy processing across multiple layers
        """
        if context is None:
            context = self.cognitive_contexts.get(user_id, CognitiveContext(user_id=user_id))
        
        if memory_types is None:
            memory_types = self._infer_memory_types(content, context)
        
        # Process in parallel across memory layers
        futures = {}
        results = {"results": [], "synergy_activations": {}}
        
        with self.processing_lock:
            for memory_type in memory_types:
                future = self.executor.submit(
                    self._process_memory_layer, 
                    memory_type, content, user_id, context, **kwargs
                )
                futures[memory_type] = future
        
        # Collect results and apply synergy
        layer_results = {}
        for memory_type, future in futures.items():
            try:
                layer_results[memory_type] = future.result(timeout=30)
                results["results"].extend(layer_results[memory_type].get("results", []))
            except Exception as e:
                logger.error(f"Error processing {memory_type}: {e}")
                continue
        
        # Apply cognitive synergy between layers
        synergy_results = self._apply_cognitive_synergy(layer_results, context)
        results["synergy_activations"] = synergy_results
        
        # Update memory associations
        self._update_memory_associations(results["results"], context)
        
        return results
    
    def _infer_memory_types(self, content: Union[str, List[Dict[str, str]]], context: CognitiveContext) -> List[MemoryType]:
        """Infer appropriate memory types based on content and context"""
        memory_types = []
        
        # Always include working memory for active processing
        memory_types.append(MemoryType.WORKING)
        
        # Analyze content for memory type inference
        if isinstance(content, str):
            text_content = content.lower()
        else:
            text_content = " ".join([msg.get("content", "") for msg in content if isinstance(msg, dict)]).lower()
        
        # Semantic memory for factual information
        if any(word in text_content for word in ["is", "are", "was", "were", "definition", "means"]):
            memory_types.append(MemoryType.SEMANTIC)
        
        # Episodic memory for events and experiences
        if any(word in text_content for word in ["yesterday", "today", "when", "where", "happened", "remember"]):
            memory_types.append(MemoryType.EPISODIC)
        
        # Procedural memory for processes and skills
        if any(word in text_content for word in ["how", "step", "process", "procedure", "method"]):
            memory_types.append(MemoryType.PROCEDURAL)
        
        # Context-based inference
        if context.attention_focus:
            if any("learning" in focus for focus in context.attention_focus):
                if MemoryType.PROCEDURAL not in memory_types:
                    memory_types.append(MemoryType.PROCEDURAL)
        
        return memory_types
    
    def _process_memory_layer(
        self, 
        memory_type: MemoryType, 
        content: Union[str, List[Dict[str, str]]], 
        user_id: str, 
        context: CognitiveContext,
        **kwargs
    ) -> Dict[str, Any]:
        """Process memory for a specific layer"""
        layer_state = self.memory_layers[memory_type]
        layer_state.last_accessed = datetime.now()
        
        # Adjust processing based on memory type
        processed_kwargs = kwargs.copy()
        processed_kwargs["memory_type"] = memory_type.value
        
        # Layer-specific processing adjustments
        if memory_type == MemoryType.WORKING:
            # Working memory has higher priority and shorter retention
            processed_kwargs["priority"] = MemoryLayerPriority.HIGH.value
            processed_kwargs["retention_period"] = "short"
        elif memory_type == MemoryType.SEMANTIC:
            # Semantic memory focuses on factual information
            processed_kwargs["focus"] = "facts"
        elif memory_type == MemoryType.EPISODIC:
            # Episodic memory includes temporal and contextual information
            processed_kwargs["temporal_context"] = context.temporal_context
            processed_kwargs["emotional_context"] = context.emotional_state
        elif memory_type == MemoryType.PROCEDURAL:
            # Procedural memory focuses on process information
            processed_kwargs["focus"] = "procedures"
        
        # Call the base memory system with layer-specific parameters
        try:
            result = self.memory_base.add(content, user_id=user_id, **processed_kwargs)
            layer_state.activation_level = min(1.0, layer_state.activation_level + 0.1)
            return result
        except Exception as e:
            logger.error(f"Error in {memory_type} layer processing: {e}")
            return {"results": []}
    
    def _apply_cognitive_synergy(
        self, 
        layer_results: Dict[MemoryType, Dict[str, Any]], 
        context: CognitiveContext
    ) -> Dict[str, float]:
        """Apply cognitive synergy between memory layers"""
        synergy_activations = {}
        
        for edge in self.synergy_edges:
            if edge.source_layer in layer_results and edge.target_layer in layer_results:
                # Calculate synergy activation
                source_activation = len(layer_results[edge.source_layer].get("results", []))
                target_activation = len(layer_results[edge.target_layer].get("results", []))
                
                if source_activation > 0 and target_activation > 0:
                    synergy_strength = edge.strength * context.cognitive_load
                    synergy_activations[edge.synergy_type.value] = synergy_strength
                    
                    # Update edge activation
                    edge.last_activation = datetime.now()
                    
                    # Create cross-layer associations
                    self._create_cross_layer_associations(
                        layer_results[edge.source_layer]["results"],
                        layer_results[edge.target_layer]["results"],
                        synergy_strength
                    )
        
        return synergy_activations
    
    def _create_cross_layer_associations(
        self, 
        source_memories: List[Dict[str, Any]], 
        target_memories: List[Dict[str, Any]], 
        synergy_strength: float
    ) -> None:
        """Create associations between memories in different layers"""
        for source_mem in source_memories:
            for target_mem in target_memories:
                source_id = source_mem.get("id")
                target_id = target_mem.get("id")
                
                if source_id and target_id and synergy_strength > 0.5:
                    self.memory_associations[source_id].add(target_id)
                    self.memory_associations[target_id].add(source_id)
    
    def _update_memory_associations(self, memories: List[Dict[str, Any]], context: CognitiveContext) -> None:
        """Update memory associations based on context"""
        current_time = datetime.now()
        
        for memory in memories:
            memory_id = memory.get("id")
            if memory_id:
                # Track activation history
                self.activation_history[memory_id].append((current_time, context.cognitive_load))
                
                # Maintain activation history size
                if len(self.activation_history[memory_id]) > 100:
                    self.activation_history[memory_id] = self.activation_history[memory_id][-50:]
    
    def search_with_cognitive_synergy(
        self, 
        query: str, 
        user_id: str,
        memory_types: List[MemoryType] = None,
        synergy_types: List[CognitiveSynergyType] = None,
        context: Optional[CognitiveContext] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Search memories with cognitive synergy across multiple layers
        """
        if context is None:
            context = self.cognitive_contexts.get(user_id, CognitiveContext(user_id=user_id))
        
        if memory_types is None:
            memory_types = [MemoryType.WORKING, MemoryType.SEMANTIC, MemoryType.EPISODIC]
        
        # Search in parallel across memory layers
        futures = {}
        with self.processing_lock:
            for memory_type in memory_types:
                search_kwargs = kwargs.copy()
                search_kwargs["memory_type"] = memory_type.value
                
                future = self.executor.submit(
                    self._search_memory_layer,
                    memory_type, query, user_id, context, **search_kwargs
                )
                futures[memory_type] = future
        
        # Collect and merge results
        all_results = {"results": [], "layer_results": {}, "synergy_scores": {}}
        
        for memory_type, future in futures.items():
            try:
                layer_result = future.result(timeout=30)
                all_results["layer_results"][memory_type.value] = layer_result
                
                # Add layer information to results
                for result in layer_result.get("results", []):
                    result["source_layer"] = memory_type.value
                    all_results["results"].append(result)
                    
            except Exception as e:
                logger.error(f"Error searching {memory_type}: {e}")
                continue
        
        # Apply synergy-based ranking and filtering
        if synergy_types:
            all_results = self._apply_synergy_ranking(all_results, synergy_types, context)
        
        # Sort by combined relevance and synergy scores
        all_results["results"].sort(
            key=lambda x: (x.get("score", 0) + x.get("synergy_score", 0)), 
            reverse=True
        )
        
        return all_results
    
    def _search_memory_layer(
        self, 
        memory_type: MemoryType, 
        query: str, 
        user_id: str, 
        context: CognitiveContext,
        **kwargs
    ) -> Dict[str, Any]:
        """Search in a specific memory layer"""
        layer_state = self.memory_layers[memory_type]
        layer_state.last_accessed = datetime.now()
        layer_state.activation_level = min(1.0, layer_state.activation_level + 0.05)
        
        try:
            return self.memory_base.search(query, user_id=user_id, **kwargs)
        except Exception as e:
            logger.error(f"Error searching {memory_type} layer: {e}")
            return {"results": []}
    
    def _apply_synergy_ranking(
        self, 
        results: Dict[str, Any], 
        synergy_types: List[CognitiveSynergyType], 
        context: CognitiveContext
    ) -> Dict[str, Any]:
        """Apply synergy-based ranking to search results"""
        for result in results["results"]:
            synergy_score = 0.0
            result_id = result.get("id")
            
            if result_id and result_id in self.memory_associations:
                # Boost score based on memory associations
                association_count = len(self.memory_associations[result_id])
                synergy_score += association_count * 0.1
                
                # Check for activation history
                if result_id in self.activation_history:
                    recent_activations = [
                        activation for activation in self.activation_history[result_id]
                        if (datetime.now() - activation[0]).total_seconds() < 3600  # Last hour
                    ]
                    synergy_score += len(recent_activations) * 0.05
            
            # Apply context-based synergy boost
            if context.attention_focus:
                result_content = result.get("memory", "").lower()
                focus_matches = sum(1 for focus in context.attention_focus if focus.lower() in result_content)
                synergy_score += focus_matches * 0.2
            
            result["synergy_score"] = synergy_score
        
        return results
    
    def get_cognitive_state(self, user_id: str) -> Dict[str, Any]:
        """Get the current cognitive state of the memory system"""
        context = self.cognitive_contexts.get(user_id, CognitiveContext(user_id=user_id))
        
        layer_states = {}
        for layer_type, state in self.memory_layers.items():
            layer_states[layer_type.value] = {
                "activation_level": state.activation_level,
                "last_accessed": state.last_accessed.isoformat() if state.last_accessed else None,
                "synergy_connections": [conn.value for conn in state.synergy_connections],
                "priority": state.priority.value
            }
        
        synergy_states = {}
        for edge in self.synergy_edges:
            synergy_states[edge.synergy_type.value] = {
                "source_layer": edge.source_layer.value,
                "target_layer": edge.target_layer.value,
                "strength": edge.strength,
                "last_activation": edge.last_activation.isoformat() if edge.last_activation else None
            }
        
        return {
            "user_id": user_id,
            "cognitive_context": {
                "cognitive_load": context.cognitive_load,
                "attention_focus": context.attention_focus,
                "emotional_state": context.emotional_state,
                "active_goals": context.active_goals
            },
            "memory_layers": layer_states,
            "synergy_edges": synergy_states,
            "memory_associations_count": len(self.memory_associations)
        }
    
    def shutdown(self):
        """Shutdown the cognitive memory manager"""
        self.executor.shutdown(wait=True)
        logger.info("Cognitive Memory Manager shutdown complete")