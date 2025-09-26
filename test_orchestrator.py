#!/usr/bin/env python3
"""
Test script for the new SharedStateOrchestrator implementation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from advanced_orchestrator import SharedStateOrchestrator, execute_polyglot_code, parse_code_to_tree

def test_basic_functionality():
    """Test basic functionality of SharedStateOrchestrator"""
    print("🧪 Testing SharedStateOrchestrator Basic Functionality")
    print("=" * 60)
    
    # Test 1: Sequential blocks
    print("\n📝 Test 1: Sequential Blocks")
    sequential_code = """
::c
int x = 42;
int y = 24;
::/c

::py  
print("x + y =", x + y)
result = x * 2
::/py

::java
System.out.println("Result from Python: " + result);
int finalValue = result + 100;
::/java
"""
    
    try:
        orchestrator = SharedStateOrchestrator()
        blocks = orchestrator.parse_mixed_structure(sequential_code)
        
        print(f"✅ Parsed {len(blocks)} blocks successfully")
        for i, block in enumerate(blocks):
            print(f"   Block {i+1}: {block['type']} {block['lang']}")
        
        print("\n🚀 Executing blocks...")
        orchestrator.execute_blocks(blocks)
        
        print(f"\n📊 Final global state: {orchestrator.global_state}")
        
    except Exception as e:
        print(f"❌ Error in sequential test: {e}")
    
    # Test 2: Legacy compatibility
    print("\n📝 Test 2: Legacy Compatibility")
    
    try:
        legacy_blocks = parse_code_to_tree(sequential_code)
        print(f"✅ Legacy parse_code_to_tree works: {len(legacy_blocks)} blocks")
        
    except Exception as e:
        print(f"❌ Error in legacy test: {e}")

def test_nested_functionality():
    """Test nested block functionality"""
    print("\n🧪 Testing Nested Block Functionality")
    print("=" * 60)
    
    nested_code = """
::c
int nums[] = {1, 2, 3, 4, 5};
for(int i = 0; i < 5; i++) {
    printf("Processing: %d\\n", nums[i]);
    ::py
    print("Python says: processing", nums[i])
    ::/py
}
::/c
"""
    
    try:
        orchestrator = SharedStateOrchestrator()
        blocks = orchestrator.parse_mixed_structure(nested_code)
        
        print(f"✅ Parsed nested structure: {len(blocks)} blocks")
        for i, block in enumerate(blocks):
            nested_info = " (nested)" if block.get('is_nested') else ""
            print(f"   Block {i+1}: {block['type']} {block['lang']}{nested_info}")
        
        print("\n🚀 Executing nested blocks...")
        orchestrator.execute_blocks(blocks)
        
    except Exception as e:
        print(f"❌ Error in nested test: {e}")

if __name__ == "__main__":
    print("🎯 SharedStateOrchestrator Test Suite")
    print("=" * 60)
    
    test_basic_functionality()
    test_nested_functionality()
    
    print("\n✅ All tests completed!")