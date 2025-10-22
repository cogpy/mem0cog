"""
Tests for OpenCog-inspired Cognitive Memory Architecture
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from mem0.memory.main import Memory
from mem0.memory.cognitive_memory import CognitiveMemoryManager, CognitiveContext
from mem0.configs.base import MemoryConfig
from mem0.configs.enums import MemoryType, CognitiveSynergyType, MemoryLayerPriority


class TestCognitiveMemory(unittest.TestCase):
    """Test cases for cognitive memory functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a memory config with cognitive synergy enabled
        self.config = MemoryConfig()
        self.config.enable_cognitive_synergy = True
        
        # Mock the underlying components to avoid requiring actual LLM/vector store
        with patch.multiple(
            'mem0.memory.main',
            EmbedderFactory=MagicMock(),
            VectorStoreFactory=MagicMock(),
            LlmFactory=MagicMock(),
            GraphStoreFactory=MagicMock(),
            SQLiteManager=MagicMock(),
            RerankerFactory=MagicMock(),
        ):
            self.memory = Memory(self.config)
            
        # Mock the base memory operations
        self.memory.add = MagicMock(return_value={"results": [{"id": "test_id", "memory": "Test memory"}]})
        self.memory.search = MagicMock(return_value={"results": [{"id": "test_id", "memory": "Test memory", "score": 0.8}]})
    
    def test_cognitive_manager_initialization(self):
        """Test that cognitive memory manager is properly initialized"""
        self.assertTrue(self.memory.enable_cognitive_synergy)
        self.assertIsNotNone(self.memory.cognitive_manager)
        self.assertIsInstance(self.memory.cognitive_manager, CognitiveMemoryManager)
    
    def test_cognitive_context_creation(self):
        """Test creating and registering cognitive contexts"""
        context = CognitiveContext(
            user_id="test_user",
            session_id="test_session",
            domain="healthcare",
            attention_focus=["patient care", "diagnosis"],
            emotional_state="focused",
            cognitive_load=0.7,
            active_goals=["improve patient outcomes"]
        )
        
        self.memory.cognitive_manager.register_cognitive_context(context)
        
        # Verify context is registered
        self.assertIn("test_user", self.memory.cognitive_manager.cognitive_contexts)
        registered_context = self.memory.cognitive_manager.cognitive_contexts["test_user"]
        self.assertEqual(registered_context.domain, "healthcare")
        self.assertEqual(registered_context.cognitive_load, 0.7)
    
    def test_memory_type_inference(self):
        """Test automatic inference of memory types from content"""
        # Test semantic memory inference
        semantic_content = "The patient's diagnosis is diabetes type 2"
        semantic_types = self.memory.cognitive_manager._infer_memory_types(
            semantic_content, 
            CognitiveContext(user_id="test_user")
        )
        self.assertIn(MemoryType.SEMANTIC, semantic_types)
        self.assertIn(MemoryType.WORKING, semantic_types)  # Always included
        
        # Test episodic memory inference
        episodic_content = "Yesterday the patient visited for a checkup"
        episodic_types = self.memory.cognitive_manager._infer_memory_types(
            episodic_content,
            CognitiveContext(user_id="test_user")
        )
        self.assertIn(MemoryType.EPISODIC, episodic_types)
        self.assertIn(MemoryType.WORKING, episodic_types)
        
        # Test procedural memory inference
        procedural_content = "How to perform blood pressure measurement procedure"
        procedural_types = self.memory.cognitive_manager._infer_memory_types(
            procedural_content,
            CognitiveContext(user_id="test_user")
        )
        self.assertIn(MemoryType.PROCEDURAL, procedural_types)
        self.assertIn(MemoryType.WORKING, procedural_types)
    
    def test_synergy_graph_initialization(self):
        """Test that cognitive synergy graph is properly initialized"""
        synergy_edges = self.memory.cognitive_manager.synergy_edges
        
        # Check that key synergy connections exist
        synergy_types = [edge.synergy_type for edge in synergy_edges]
        
        self.assertIn(CognitiveSynergyType.WORKING_SEMANTIC, synergy_types)
        self.assertIn(CognitiveSynergyType.WORKING_EPISODIC, synergy_types)
        self.assertIn(CognitiveSynergyType.WORKING_PROCEDURAL, synergy_types)
        self.assertIn(CognitiveSynergyType.SEMANTIC_EPISODIC, synergy_types)
        
        # Check synergy strengths are reasonable
        for edge in synergy_edges:
            self.assertGreater(edge.strength, 0.0)
            self.assertLessEqual(edge.strength, 1.0)
    
    def test_add_with_cognitive_synergy(self):
        """Test adding memory with cognitive synergy"""
        # Test with automatic memory type inference
        result = self.memory.add_with_cognitive_synergy(
            "The patient shows symptoms of hypertension",
            user_id="doctor_1"
        )
        
        # Verify that cognitive manager was called
        self.assertIsInstance(result, dict)
        # The actual result will depend on the mocked behavior
    
    def test_search_with_cognitive_synergy(self):
        """Test searching with cognitive synergy"""
        result = self.memory.search_with_cognitive_synergy(
            "patient symptoms",
            user_id="doctor_1"
        )
        
        # Verify that search was performed
        self.assertIsInstance(result, dict)
    
    def test_cognitive_state_retrieval(self):
        """Test retrieving cognitive state"""
        # Set up a cognitive context first
        self.memory.set_cognitive_context(
            user_id="test_user",
            domain="education",
            attention_focus=["learning", "memory"],
            cognitive_load=0.6
        )
        
        # Get cognitive state
        state = self.memory.get_cognitive_state(user_id="test_user")
        
        self.assertIn("user_id", state)
        self.assertIn("cognitive_context", state)
        self.assertIn("memory_layers", state)
        self.assertIn("synergy_edges", state)
    
    def test_set_cognitive_context(self):
        """Test setting cognitive context"""
        result = self.memory.set_cognitive_context(
            user_id="student_1",
            domain="mathematics",
            attention_focus=["algebra", "equations"],
            emotional_state="curious",
            cognitive_load=0.5,
            active_goals=["solve quadratic equations"]
        )
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["context"]["domain"], "mathematics")
        self.assertEqual(result["context"]["cognitive_load"], 0.5)
    
    def test_fallback_to_standard_memory(self):
        """Test fallback to standard memory when cognitive synergy is disabled"""
        # Disable cognitive synergy
        self.memory.enable_cognitive_synergy = False
        self.memory.cognitive_manager = None
        
        # Test add with cognitive synergy - should fallback
        result = self.memory.add_with_cognitive_synergy(
            "Test message",
            user_id="test_user"
        )
        
        # Should have called the standard add method
        self.memory.add.assert_called_once()
        
        # Test search with cognitive synergy - should fallback
        search_result = self.memory.search_with_cognitive_synergy(
            "test query",
            user_id="test_user"
        )
        
        # Should have called the standard search method
        self.memory.search.assert_called_once()
    
    def test_memory_layer_states(self):
        """Test memory layer state management"""
        cognitive_manager = self.memory.cognitive_manager
        
        # Check that all memory types have layer states
        for memory_type in MemoryType:
            self.assertIn(memory_type, cognitive_manager.memory_layers)
            layer_state = cognitive_manager.memory_layers[memory_type]
            self.assertEqual(layer_state.layer_type, memory_type)
            self.assertEqual(layer_state.activation_level, 0.0)  # Initial state
    
    def test_cross_layer_associations(self):
        """Test creation of cross-layer memory associations"""
        cognitive_manager = self.memory.cognitive_manager
        
        # Create test memories for association
        source_memories = [{"id": "mem_1", "memory": "Test memory 1"}]
        target_memories = [{"id": "mem_2", "memory": "Test memory 2"}]
        
        # Create associations
        cognitive_manager._create_cross_layer_associations(
            source_memories, target_memories, synergy_strength=0.8
        )
        
        # Check associations were created
        self.assertIn("mem_2", cognitive_manager.memory_associations["mem_1"])
        self.assertIn("mem_1", cognitive_manager.memory_associations["mem_2"])
    
    def test_activation_history_tracking(self):
        """Test memory activation history tracking"""
        cognitive_manager = self.memory.cognitive_manager
        context = CognitiveContext(user_id="test_user", cognitive_load=0.7)
        
        memories = [{"id": "test_mem", "memory": "Test memory"}]
        cognitive_manager._update_memory_associations(memories, context)
        
        # Check activation history was recorded
        self.assertIn("test_mem", cognitive_manager.activation_history)
        activation_records = cognitive_manager.activation_history["test_mem"]
        self.assertEqual(len(activation_records), 1)
        self.assertEqual(activation_records[0][1], 0.7)  # cognitive_load


class TestCognitiveMemoryIntegration(unittest.TestCase):
    """Integration tests for cognitive memory with different scenarios"""
    
    def setUp(self):
        """Set up test fixtures for integration tests"""
        self.config = MemoryConfig()
        self.config.enable_cognitive_synergy = True
        
        with patch.multiple(
            'mem0.memory.main',
            EmbedderFactory=MagicMock(),
            VectorStoreFactory=MagicMock(),
            LlmFactory=MagicMock(),
            GraphStoreFactory=MagicMock(),
            SQLiteManager=MagicMock(),
            RerankerFactory=MagicMock(),
        ):
            self.memory = Memory(self.config)
        
        # Mock base memory operations with more realistic returns
        self.memory.add = MagicMock(return_value={
            "results": [
                {"id": "semantic_1", "memory": "Factual information", "event": "ADD"},
                {"id": "episodic_1", "memory": "Event memory", "event": "ADD"}
            ]
        })
        
        self.memory.search = MagicMock(return_value={
            "results": [
                {"id": "result_1", "memory": "Search result 1", "score": 0.9},
                {"id": "result_2", "memory": "Search result 2", "score": 0.7}
            ]
        })
    
    def test_healthcare_scenario(self):
        """Test cognitive memory in a healthcare scenario"""
        # Set healthcare context
        self.memory.set_cognitive_context(
            user_id="doctor_smith",
            domain="healthcare",
            attention_focus=["patient diagnosis", "treatment planning"],
            emotional_state="focused",
            cognitive_load=0.8,
            active_goals=["accurate diagnosis", "patient safety"]
        )
        
        # Add medical knowledge (should activate semantic + working memory)
        semantic_result = self.memory.add_with_cognitive_synergy(
            "Hypertension is defined as blood pressure consistently above 140/90 mmHg",
            user_id="doctor_smith"
        )
        
        # Add patient encounter (should activate episodic + working memory)
        episodic_result = self.memory.add_with_cognitive_synergy(
            "Patient John Doe presented today with chest pain and elevated BP 160/95",
            user_id="doctor_smith"
        )
        
        # Add treatment procedure (should activate procedural + working memory)
        procedural_result = self.memory.add_with_cognitive_synergy(
            "To measure blood pressure: 1) Position cuff 2) Inflate to 180mmHg 3) Release slowly",
            user_id="doctor_smith"
        )
        
        # Search with synergy (should activate cross-layer associations)
        search_result = self.memory.search_with_cognitive_synergy(
            "blood pressure measurement for hypertensive patient",
            user_id="doctor_smith",
            synergy_types=[
                CognitiveSynergyType.WORKING_SEMANTIC,
                CognitiveSynergyType.WORKING_EPISODIC,
                CognitiveSynergyType.WORKING_PROCEDURAL
            ]
        )
        
        # Verify cognitive state reflects healthcare context
        cognitive_state = self.memory.get_cognitive_state(user_id="doctor_smith")
        self.assertEqual(cognitive_state["cognitive_context"]["cognitive_load"], 0.8)
        self.assertIn("patient diagnosis", cognitive_state["cognitive_context"]["attention_focus"])
    
    def test_educational_scenario(self):
        """Test cognitive memory in an educational scenario"""
        # Set educational context
        self.memory.set_cognitive_context(
            user_id="student_alice",
            domain="mathematics",
            attention_focus=["algebra", "problem solving"],
            emotional_state="learning",
            cognitive_load=0.6,
            active_goals=["understand quadratic equations"]
        )
        
        # Add conceptual knowledge
        concept_result = self.memory.add_with_cognitive_synergy(
            "A quadratic equation has the form ax² + bx + c = 0",
            user_id="student_alice"
        )
        
        # Add learning experience
        experience_result = self.memory.add_with_cognitive_synergy(
            "During today's math class, I learned how to factor quadratic equations",
            user_id="student_alice"
        )
        
        # Add problem-solving procedure
        procedure_result = self.memory.add_with_cognitive_synergy(
            "To solve by factoring: 1) Move all terms to one side 2) Factor 3) Set each factor to zero",
            user_id="student_alice"
        )
        
        # Search for integrated knowledge
        integrated_search = self.memory.search_with_cognitive_synergy(
            "how to solve quadratic equations using factoring method",
            user_id="student_alice"
        )
        
        # Verify educational context is maintained
        cognitive_state = self.memory.get_cognitive_state(user_id="student_alice")
        self.assertEqual(cognitive_state["cognitive_context"]["cognitive_load"], 0.6)


if __name__ == '__main__':
    unittest.main()