#!/usr/bin/env python3

from advanced_orchestrator import parse_code_to_tree, execute_nested_block
from engine import execute_in_docker

def test_simple_nested():
    """Test basic nested functionality"""
    print("=== Test 1: Simple Nested ===")
    test_code = '::c int a[]={1,2,3,4,5}; for(int i=0;i<5;i++){ ::py print(a[i]) ::/py } ::/c'
    
    print(f"Original: {test_code}")
    
    tree = parse_code_to_tree(test_code)
    if tree and tree[0].get('is_nested'):
        structure = tree[0]['nested_structure']
        processed_code, _ = execute_nested_block(structure, {})
        
        print(f"Processed: {processed_code.strip()}")
        
        try:
            result = execute_in_docker('c', processed_code.strip(), '{}')
            print("✅ SUCCESS!")
            print(f"Output:\n{result}")
        except Exception as e:
            print(f"❌ Error: {e}")
    print()

def test_complex_nested():
    """Test more complex nested functionality"""
    print("=== Test 2: Complex Nested ===")
    test_code = '::c printf("Starting:\\n"); int nums[] = {10, 20, 30}; for(int j = 0; j < 3; j++) { printf("Element %d: ", j); ::py print(nums[j] * 2) ::/py } printf("Done!\\n"); ::/c'
    
    print(f"Original: {test_code}")
    
    tree = parse_code_to_tree(test_code)
    if tree and tree[0].get('is_nested'):
        structure = tree[0]['nested_structure']
        processed_code, _ = execute_nested_block(structure, {})
        
        print(f"Processed: {processed_code.strip()}")
        
        try:
            result = execute_in_docker('c', processed_code.strip(), '{}')
            print("✅ SUCCESS!")
            print(f"Output:\n{result}")
        except Exception as e:
            print(f"❌ Error: {e}")
    print()

def test_string_nested():
    """Test nested with string literals"""
    print("=== Test 3: String Nested ===")
    test_code = '::c char* names[] = {"Alice", "Bob", "Carol"}; for(int k=0; k<3; k++) { printf("Name %d: %s -> ", k, names[k]); ::py print("Hello!") ::/py } ::/c'
    
    print(f"Original: {test_code}")
    
    tree = parse_code_to_tree(test_code)
    if tree and tree[0].get('is_nested'):
        structure = tree[0]['nested_structure']
        processed_code, _ = execute_nested_block(structure, {})
        
        print(f"Processed: {processed_code.strip()}")
        
        try:
            result = execute_in_docker('c', processed_code.strip(), '{}')
            print("✅ SUCCESS!")
            print(f"Output:\n{result}")
        except Exception as e:
            print(f"❌ Error: {e}")
    print()

if __name__ == "__main__":
    test_simple_nested()
    test_complex_nested()
    test_string_nested()