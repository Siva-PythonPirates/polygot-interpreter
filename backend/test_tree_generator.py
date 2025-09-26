#!/usr/bin/env python3
"""
Test the tree generator function specifically to isolate the issue
"""

from advanced_orchestrator import parse_code_to_tree, execute_tree_generator, set_debug_mode, get_debug_mode

def test_tree_generator():
    test_code = """::c
int nums[] = {50, 25, 75, 100, 10};
::/c

::py
nums.sort()
print("Sorted:", nums)
::/py"""
    
    print("=== Testing with DEBUG OFF ===")
    set_debug_mode(False)
    print(f"Debug mode: {get_debug_mode()}")
    
    blocks = parse_code_to_tree(test_code)
    print(f"Parsed blocks: {len(blocks)}")
    
    print("\n--- Generator Output ---")
    for log_entry in execute_tree_generator(blocks):
        print(f"YIELD: {log_entry}")
    print("--- End Generator Output ---")

if __name__ == "__main__":
    test_tree_generator()