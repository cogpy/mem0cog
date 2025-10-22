#!/usr/bin/env python3
"""
OpenCog-inspired Cognitive Memory Synergy Demo

This example demonstrates the cognitive synergy integration of parallel memory layers
in mem0cog, showing how different types of memories (working, semantic, episodic, 
procedural) can work together with cognitive synergy for enhanced AI memory management.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List

from mem0 import Memory
from mem0.memory.cognitive_memory import CognitiveContext
from mem0.configs.enums import MemoryType, CognitiveSynergyType
from mem0.configs.base import MemoryConfig


def setup_cognitive_memory():
    """Set up memory with cognitive synergy enabled"""
    config = MemoryConfig()
    config.enable_cognitive_synergy = True
    
    # Configure cognitive synergy parameters
    config.cognitive_synergy_config = {
        "max_parallel_layers": 6,  # Include all memory types
        "synergy_strength_threshold": 0.4,
        "working_memory_capacity": 150,
        "cross_layer_association_strength": 0.7,
        "cognitive_load_adaptation": True
    }
    
    return Memory(config)


def healthcare_assistant_demo():
    """Demonstrate cognitive synergy in a healthcare AI assistant scenario"""
    print("\n" + "="*60)
    print("HEALTHCARE AI ASSISTANT - COGNITIVE SYNERGY DEMO")
    print("="*60)
    
    memory = setup_cognitive_memory()
    
    # Set up healthcare-specific cognitive context
    print("\n1. Setting up cognitive context for healthcare domain...")
    context_result = memory.set_cognitive_context(
        user_id="dr_johnson",
        domain="healthcare",
        attention_focus=["patient care", "diagnosis", "treatment planning"],
        emotional_state="focused",
        cognitive_load=0.7,
        active_goals=["accurate diagnosis", "patient safety", "evidence-based treatment"]
    )
    print(f"✓ Context set: {context_result['status']}")
    
    # Add medical knowledge (Semantic Memory)
    print("\n2. Adding medical knowledge to semantic memory...")
    medical_knowledge = [
        "Hypertension is defined as blood pressure consistently above 140/90 mmHg",
        "Type 2 diabetes is characterized by insulin resistance and relative insulin deficiency",
        "Coronary artery disease is the leading cause of death worldwide",
        "BMI over 30 is classified as obese and increases cardiovascular risk"
    ]
    
    for idx, knowledge in enumerate(medical_knowledge, start=1):
        result = memory.add_with_cognitive_synergy(
            knowledge,
            user_id="dr_johnson",
            memory_types=[MemoryType.SEMANTIC, MemoryType.WORKING]
        )
        print(f"  ✓ Medical knowledge item {idx} added.")
    
    # Add patient encounters (Episodic Memory)
    print("\n3. Adding patient encounters to episodic memory...")
    patient_encounters = [
        "Patient Sarah Wilson, 45, presented with chest pain and shortness of breath on March 15",
        "Follow-up visit: Patient John Smith showed improved BP readings after medication adjustment",
        "Emergency case: 60-year-old male with acute MI, successfully treated with PCI",
        "Routine checkup: Mary Johnson's diabetes management is progressing well"
    ]
    
    for encounter in patient_encounters:
        result = memory.add_with_cognitive_synergy(
            encounter,
            user_id="dr_johnson",
            memory_types=[MemoryType.EPISODIC, MemoryType.WORKING]
        )
        print(f"  ✓ Added: {encounter[:50]}...")
    
    # Add clinical procedures (Procedural Memory)
    print("\n4. Adding clinical procedures to procedural memory...")
    procedures = [
        "Blood pressure measurement: 1) Position cuff properly 2) Inflate to 180mmHg 3) Release slowly",
        "ECG interpretation: 1) Check rhythm 2) Measure intervals 3) Look for ST changes",
        "Diabetes management protocol: 1) Check HbA1c 2) Adjust medications 3) Lifestyle counseling",
        "Emergency response for chest pain: 1) Assess vitals 2) ECG within 10 minutes 3) Consider aspirin"
    ]
    
    for procedure in procedures:
        result = memory.add_with_cognitive_synergy(
            procedure,
            user_id="dr_johnson",
            memory_types=[MemoryType.PROCEDURAL, MemoryType.WORKING]
        )
        print(f"  ✓ Added: {procedure[:50]}...")
    
    # Demonstrate cognitive synergy in action
    print("\n5. Demonstrating cognitive synergy in clinical decision making...")
    
    clinical_scenarios = [
        {
            "query": "How to manage a patient with chest pain and elevated blood pressure?",
            "synergy_types": [
                CognitiveSynergyType.WORKING_SEMANTIC,
                CognitiveSynergyType.WORKING_EPISODIC,
                CognitiveSynergyType.WORKING_PROCEDURAL,
                CognitiveSynergyType.MULTI_LAYER
            ]
        },
        {
            "query": "What are the key considerations for diabetes follow-up visits?",
            "synergy_types": [
                CognitiveSynergyType.SEMANTIC_PROCEDURAL,
                CognitiveSynergyType.EPISODIC_PROCEDURAL
            ]
        }
    ]
    
    for i, scenario in enumerate(clinical_scenarios, 1):
        print(f"\n  Scenario {i}: {scenario['query']}")
        
        search_result = memory.search_with_cognitive_synergy(
            query=scenario["query"],
            user_id="dr_johnson",
            synergy_types=scenario["synergy_types"]
        )
        
        print(f"  📊 Found {len(search_result.get('results', []))} relevant memories")
        
        # Show synergy activations
        if 'synergy_activations' in search_result:
            print("  🧠 Active synergies:")
            for synergy, strength in search_result['synergy_activations'].items():
                print(f"    - {synergy}: {strength:.2f}")
        
        # Show top results from different layers
        if 'layer_results' in search_result:
            print("  🔍 Results by memory layer:")
            for layer, layer_data in search_result['layer_results'].items():
                count = len(layer_data.get('results', []))
                print(f"    - {layer}: {count} results")
    
    # Display cognitive state
    print("\n6. Current cognitive state analysis...")
    cognitive_state = memory.get_cognitive_state(user_id="dr_johnson")
    
    print("  🧠 Cognitive Context:")
    context = cognitive_state['cognitive_context']
    print(f"    - Cognitive Load: {context['cognitive_load']:.1f}")
    print(f"    - Attention Focus: {', '.join(context['attention_focus'])}")
    print(f"    - Active Goals: {', '.join(context['active_goals'])}")
    
    print("  🔗 Memory Layer Activations:")
    for layer, state in cognitive_state['memory_layers'].items():
        print(f"    - {layer}: {state['activation_level']:.2f}")
    
    print("  ⚡ Synergy Edge States:")
    active_synergies = 0
    for synergy, state in cognitive_state['synergy_edges'].items():
        if state['last_activation']:
            active_synergies += 1
    print(f"    - Active synergy connections: {active_synergies}")
    
    return memory


def educational_tutor_demo():
    """Demonstrate cognitive synergy in an educational AI tutor scenario"""
    print("\n" + "="*60)
    print("EDUCATIONAL AI TUTOR - COGNITIVE SYNERGY DEMO")
    print("="*60)
    
    memory = setup_cognitive_memory()
    
    # Set up educational cognitive context
    print("\n1. Setting up cognitive context for mathematics learning...")
    memory.set_cognitive_context(
        user_id="student_alex",
        domain="mathematics",
        attention_focus=["algebra", "quadratic equations", "problem solving"],
        emotional_state="curious",
        cognitive_load=0.6,
        active_goals=["master quadratic equations", "improve problem-solving skills"]
    )
    print("✓ Educational context established")
    
    # Add mathematical concepts (Semantic Memory)
    print("\n2. Building mathematical knowledge base...")
    math_concepts = [
        "A quadratic equation has the general form ax² + bx + c = 0 where a ≠ 0",
        "The discriminant Δ = b² - 4ac determines the nature of roots",
        "If Δ > 0, the equation has two distinct real roots",
        "The quadratic formula is x = (-b ± √(b² - 4ac)) / (2a)"
    ]
    
    for concept in math_concepts:
        memory.add_with_cognitive_synergy(
            concept,
            user_id="student_alex",
            memory_types=[MemoryType.SEMANTIC, MemoryType.WORKING]
        )
        print(f"  ✓ Concept: {concept[:40]}...")
    
    # Add learning experiences (Episodic Memory)
    print("\n3. Recording learning experiences...")
    learning_experiences = [
        "Yesterday I struggled with factoring x² - 5x + 6 but finally got (x-2)(x-3)",
        "During today's class, I learned how the discriminant predicts root types",
        "I made an error forgetting the ± sign in the quadratic formula last week",
        "Successfully solved 3 quadratic word problems about projectile motion"
    ]
    
    for experience in learning_experiences:
        memory.add_with_cognitive_synergy(
            experience,
            user_id="student_alex",
            memory_types=[MemoryType.EPISODIC, MemoryType.WORKING]
        )
        print(f"  ✓ Experience: {experience[:40]}...")
    
    # Add problem-solving procedures (Procedural Memory)
    print("\n4. Learning problem-solving procedures...")
    procedures = [
        "Factoring method: 1) Move all terms to one side 2) Find two numbers that multiply to c and add to b 3) Factor and solve",
        "Quadratic formula method: 1) Identify a, b, c 2) Calculate discriminant 3) Apply formula 4) Simplify",
        "Completing the square: 1) Make a=1 2) Move constant to right 3) Add (b/2)² to both sides 4) Factor left side",
        "Graphical method: 1) Plot the parabola 2) Find x-intercepts 3) Read solutions from graph"
    ]
    
    for procedure in procedures:
        memory.add_with_cognitive_synergy(
            procedure,
            user_id="student_alex",
            memory_types=[MemoryType.PROCEDURAL, MemoryType.WORKING]
        )
        print(f"  ✓ Procedure: {procedure[:40]}...")
    
    # Demonstrate adaptive learning with cognitive synergy
    print("\n5. Adaptive learning scenarios with cognitive synergy...")
    
    learning_queries = [
        "How do I solve x² - 7x + 12 = 0?",
        "Why did I get the wrong answer when I forgot the discriminant?",
        "What's the best method for solving 2x² + 5x - 3 = 0?",
        "How can I avoid making sign errors in quadratic equations?"
    ]
    
    for i, query in enumerate(learning_queries, 1):
        print(f"\n  Learning Query {i}: {query}")
        
        # Update cognitive load based on query complexity
        complexity_load = {1: 0.5, 2: 0.7, 3: 0.6, 4: 0.8}
        memory.set_cognitive_context(
            user_id="student_alex",
            cognitive_load=complexity_load.get(i, 0.6)
        )
        
        # Search with multi-layer synergy
        result = memory.search_with_cognitive_synergy(
            query=query,
            user_id="student_alex",
            memory_types=[MemoryType.WORKING, MemoryType.SEMANTIC, 
                         MemoryType.EPISODIC, MemoryType.PROCEDURAL],
            synergy_types=[CognitiveSynergyType.MULTI_LAYER]
        )
        
        print(f"    🎯 Retrieved {len(result.get('results', []))} relevant memories")
        
        # Show how different memory layers contribute
        if 'layer_results' in result:
            for layer, data in result['layer_results'].items():
                count = len(data.get('results', []))
                if count > 0:
                    print(f"    📚 {layer}: {count} contributions")
    
    # Show learning progress through cognitive state
    print("\n6. Learning progress analysis...")
    cognitive_state = memory.get_cognitive_state(user_id="student_alex")
    
    print("  📈 Cognitive Development:")
    print(f"    - Current cognitive load: {cognitive_state['cognitive_context']['cognitive_load']:.1f}")
    print(f"    - Focus areas: {', '.join(cognitive_state['cognitive_context']['attention_focus'])}")
    
    print("  🧠 Memory Layer Development:")
    layers = cognitive_state['memory_layers']
    for layer_name, state in layers.items():
        activation = state['activation_level']
        if activation > 0:
            print(f"    - {layer_name}: {activation:.2f} (active)")
    
    return memory


def creative_writing_demo():
    """Demonstrate cognitive synergy in a creative writing assistant scenario"""
    print("\n" + "="*60)
    print("CREATIVE WRITING ASSISTANT - COGNITIVE SYNERGY DEMO")
    print("="*60)
    
    memory = setup_cognitive_memory()
    
    # Set up creative writing context
    print("\n1. Setting up cognitive context for creative writing...")
    memory.set_cognitive_context(
        user_id="writer_maya",
        domain="creative_writing",
        attention_focus=["character development", "plot structure", "world building"],
        emotional_state="creative",
        cognitive_load=0.5,
        active_goals=["write compelling characters", "create engaging plot", "build immersive world"]
    )
    print("✓ Creative writing context established")
    
    # Add writing knowledge and techniques (Semantic Memory)
    print("\n2. Building writing craft knowledge...")
    writing_craft = [
        "Show don't tell: demonstrate character emotions through actions rather than exposition",
        "The hero's journey follows: ordinary world → call to adventure → trials → return",
        "Dialogue should reveal character personality and advance the plot simultaneously",
        "World-building requires consistent rules, geography, culture, and history"
    ]
    
    for craft in writing_craft:
        memory.add_with_cognitive_synergy(
            craft,
            user_id="writer_maya",
            memory_types=[MemoryType.SEMANTIC, MemoryType.WORKING]
        )
        print(f"  ✓ Craft: {craft[:40]}...")
    
    # Add writing experiences and inspiration (Episodic Memory)
    print("\n3. Recording writing experiences and inspiration...")
    experiences = [
        "Last week I observed an elderly man feeding pigeons - perfect character inspiration",
        "The thunderstorm yesterday gave me ideas for a dramatic scene climax",
        "Reading Ursula K. Le Guin inspired me to focus more on character relationships",
        "Feedback from my writing group: my dialogue needs more subtext and conflict"
    ]
    
    for experience in experiences:
        memory.add_with_cognitive_synergy(
            experience,
            user_id="writer_maya",
            memory_types=[MemoryType.EPISODIC, MemoryType.WORKING]
        )
        print(f"  ✓ Experience: {experience[:40]}...")
    
    # Add writing processes and techniques (Procedural Memory)
    print("\n4. Learning writing processes...")
    processes = [
        "Character creation: 1) Define core motivation 2) Create backstory 3) Give unique voice 4) Plan character arc",
        "Plot development: 1) Establish conflict 2) Build tension 3) Create turning points 4) Resolve satisfyingly",
        "Scene writing: 1) Set clear objective 2) Add conflict/obstacles 3) Show character change 4) End with hook",
        "Revision process: 1) Let draft rest 2) Read for big picture 3) Line edit for clarity 4) Polish prose"
    ]
    
    for process in processes:
        memory.add_with_cognitive_synergy(
            process,
            user_id="writer_maya",
            memory_types=[MemoryType.PROCEDURAL, MemoryType.WORKING]
        )
        print(f"  ✓ Process: {process[:40]}...")
    
    # Demonstrate creative synergy in action
    print("\n5. Creative problem-solving with cognitive synergy...")
    
    creative_challenges = [
        "How can I make my protagonist more compelling and three-dimensional?",
        "I'm stuck on this scene - how can I add more tension and conflict?",
        "How do I show my character's emotional growth without being heavy-handed?",
        "What techniques can help me create a more immersive fantasy world?"
    ]
    
    for i, challenge in enumerate(creative_challenges, 1):
        print(f"\n  Creative Challenge {i}: {challenge}")
        
        # Adjust cognitive state for creative flow
        memory.set_cognitive_context(
            user_id="writer_maya",
            cognitive_load=0.4 + (i * 0.1),  # Increase load with complexity
            attention_focus=["creativity", "problem solving", "storytelling"]
        )
        
        result = memory.search_with_cognitive_synergy(
            query=challenge,
            user_id="writer_maya",
            synergy_types=[
                CognitiveSynergyType.WORKING_SEMANTIC,
                CognitiveSynergyType.WORKING_EPISODIC,
                CognitiveSynergyType.WORKING_PROCEDURAL,
                CognitiveSynergyType.SEMANTIC_EPISODIC
            ]
        )
        
        print(f"    💡 Creative insights from {len(result.get('results', []))} memory sources")
        
        # Show synergy between different types of creative knowledge
        if 'layer_results' in result:
            insights = []
            for layer, data in result['layer_results'].items():
                count = len(data.get('results', []))
                if count > 0:
                    insights.append(f"{layer}({count})")
            if insights:
                print(f"    🎨 Creative synthesis: {' + '.join(insights)}")
    
    # Creative flow analysis
    print("\n6. Creative flow and cognitive state analysis...")
    cognitive_state = memory.get_cognitive_state(user_id="writer_maya")
    
    print("  🎭 Creative Flow State:")
    context = cognitive_state['cognitive_context']
    print(f"    - Creative cognitive load: {context['cognitive_load']:.1f}")
    print(f"    - Creative focus: {', '.join(context['attention_focus'])}")
    print(f"    - Writing goals: {', '.join(context['active_goals'])}")
    
    print("  📝 Writing Memory Integration:")
    total_associations = cognitive_state.get('memory_associations_count', 0)
    print(f"    - Cross-memory associations: {total_associations}")
    
    return memory


def demonstrate_memory_layer_synergy():
    """Demonstrate detailed synergy between different memory layers"""
    print("\n" + "="*70)
    print("DETAILED MEMORY LAYER SYNERGY DEMONSTRATION")
    print("="*70)
    
    memory = setup_cognitive_memory()
    
    print("\n1. Analyzing synergy connections...")
    
    # Get cognitive manager for detailed analysis
    cognitive_manager = memory.cognitive_manager
    
    print("  🔗 Synergy Graph Structure:")
    for edge in cognitive_manager.synergy_edges:
        print(f"    {edge.source_layer.value} ←→ {edge.target_layer.value}")
        print(f"      Type: {edge.synergy_type.value}")
        print(f"      Strength: {edge.strength:.2f}")
        print()
    
    # Set up test context
    memory.set_cognitive_context(
        user_id="synergy_test",
        domain="multi_domain",
        attention_focus=["learning", "analysis", "synthesis"],
        cognitive_load=0.7
    )
    
    print("2. Testing parallel layer processing...")
    
    # Add content that should activate multiple layers
    multi_layer_content = [
        "Machine learning is a subset of artificial intelligence",  # Semantic
        "Yesterday I implemented my first neural network and it worked!",  # Episodic  
        "To train a model: 1) Prepare data 2) Choose architecture 3) Train 4) Evaluate",  # Procedural
        "Currently working on understanding backpropagation algorithm"  # Working
    ]
    
    for i, content in enumerate(multi_layer_content, 1):
        print(f"\n  Adding content {i}: {content[:50]}...")
        
        result = memory.add_with_cognitive_synergy(
            content,
            user_id="synergy_test"
        )
        
        # Show which layers were activated
        if 'synergy_activations' in result:
            print("    🔥 Synergy activations:")
            for synergy, strength in result['synergy_activations'].items():
                print(f"      - {synergy}: {strength:.3f}")
    
    print("\n3. Testing synergy-enhanced retrieval...")
    
    # Search with different synergy combinations
    synergy_tests = [
        {
            "query": "how to implement machine learning",
            "synergy_types": [CognitiveSynergyType.WORKING_SEMANTIC, CognitiveSynergyType.WORKING_PROCEDURAL],
            "description": "Combining factual knowledge with procedures"
        },
        {
            "query": "my experience learning neural networks",
            "synergy_types": [CognitiveSynergyType.WORKING_EPISODIC, CognitiveSynergyType.SEMANTIC_EPISODIC],
            "description": "Combining personal experience with knowledge"
        },
        {
            "query": "step by step machine learning process",
            "synergy_types": [CognitiveSynergyType.MULTI_LAYER],
            "description": "Multi-layer integration"
        }
    ]
    
    for test in synergy_tests:
        print(f"\n  Test: {test['description']}")
        print(f"  Query: {test['query']}")
        
        result = memory.search_with_cognitive_synergy(
            query=test["query"],
            user_id="synergy_test",
            synergy_types=test["synergy_types"]
        )
        
        print(f"    📊 Results: {len(result.get('results', []))} memories")
        
        # Show synergy scores
        synergy_scores = {}
        for res in result.get('results', []):
            if 'synergy_score' in res:
                layer = res.get('source_layer', 'unknown')
                synergy_scores[layer] = synergy_scores.get(layer, 0) + res['synergy_score']
        
        if synergy_scores:
            print("    ⚡ Synergy contribution by layer:")
            for layer, score in synergy_scores.items():
                print(f"      - {layer}: {score:.3f}")
    
    print("\n4. Final synergy network analysis...")
    cognitive_state = memory.get_cognitive_state(user_id="synergy_test")
    
    # Count active synergy connections
    active_connections = 0
    total_strength = 0.0
    
    for synergy, state in cognitive_state['synergy_edges'].items():
        if state['last_activation']:
            active_connections += 1
            total_strength += state['strength']
    
    print(f"  🌐 Network Statistics:")
    print(f"    - Active synergy connections: {active_connections}")
    print(f"    - Total synergy strength: {total_strength:.2f}")
    print(f"    - Memory associations: {cognitive_state.get('memory_associations_count', 0)}")
    
    # Show layer activation levels
    print(f"  🧠 Layer Activation Levels:")
    for layer, state in cognitive_state['memory_layers'].items():
        activation = state['activation_level']
        status = "🔥" if activation > 0.5 else "⚡" if activation > 0.1 else "💤"
        print(f"    {status} {layer}: {activation:.2f}")


def main():
    """Main demo function"""
    print("🧠 OpenCog-inspired Cognitive Memory Synergy Demonstration")
    print("🔗 Parallel Memory Layer Integration for Enhanced AI Memory")
    print("\nThis demo showcases the cognitive synergy integration between")
    print("multiple memory subsystems (working, semantic, episodic, procedural)")
    print("with context-aware processing and cross-layer associations.\n")
    
    try:
        # Run healthcare demo
        healthcare_memory = healthcare_assistant_demo()
        
        # Run educational demo
        educational_memory = educational_tutor_demo()
        
        # Run creative writing demo
        creative_memory = creative_writing_demo()
        
        # Demonstrate detailed synergy mechanics
        demonstrate_memory_layer_synergy()
        
        print("\n" + "="*70)
        print("🎉 COGNITIVE SYNERGY DEMONSTRATION COMPLETE")
        print("="*70)
        print("\n✅ Successfully demonstrated:")
        print("  🏥 Healthcare AI Assistant with cognitive synergy")
        print("  📚 Educational AI Tutor with adaptive memory layers")
        print("  ✍️  Creative Writing Assistant with multi-layer integration")
        print("  🧠 Detailed memory layer synergy mechanics")
        print("\n🔬 Key Features Showcased:")
        print("  • Parallel processing across multiple memory types")
        print("  • Cognitive synergy between memory layers")
        print("  • Context-aware memory routing and retrieval")
        print("  • Cross-layer memory associations")
        print("  • Adaptive cognitive load management")
        print("  • Domain-specific cognitive contexts")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Note: This demo requires proper LLM and vector store configuration.")
        print("For testing purposes, you may want to mock the underlying services.")


if __name__ == "__main__":
    main()