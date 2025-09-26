#!/usr/bin/env python3
"""
Debug your specific nested code
"""

from advanced_orchestrator import SharedStateOrchestrator

def test_your_code():
    orchestrator = SharedStateOrchestrator()
    
    # Your exact code
    your_code = """::c
int a = 5;
int b = 10;

::py
result = a * b * 2
print("Python calculated:", result)
::/py

printf("C result: %d\\n", a + b + result);
::/c"""
    
    print("=== ANALYZING YOUR CODE STRUCTURE ===")
    
    # Parse the code structure
    blocks = orchestrator.parse_all_blocks(your_code)
    print(f"Detected {len(blocks)} blocks:")
    
    for i, block in enumerate(blocks):
        print(f"Block {i+1}: {block['lang']} - Nested: {block['nested']}")
        if block['nested']:
            print(f"  Nested info: {block['nested_info']['outer_lang']} containing {block['nested_info']['nested_blocks']}")
        print(f"  Code preview: {block['code'][:100]}...")
        print()
    
    print("=== EXECUTING WITH DEBUG ===")
    
    # Enable debug mode
    import advanced_orchestrator
    advanced_orchestrator.DEBUG_MODE = True
    
    try:
        orchestrator.parse_and_execute(your_code)
    except Exception as e:
        print(f"Execution failed: {e}")
        
    print("\n=== ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    test_your_code()