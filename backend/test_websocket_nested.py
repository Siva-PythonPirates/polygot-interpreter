#!/usr/bin/env python3

# Test the WebSocket compatibility for nested execution

from advanced_orchestrator import parse_code_to_tree, execute_tree_generator
import advanced_orchestrator

def test_websocket_nested():
    """Test WebSocket-compatible nested execution"""
    
    # Your exact nested structure
    nested_code = """
::py
l=[]
::/py

::c
int a[] = {1, 2, 3, 4, 5};
for(int i = 0; i < 5; i++) {
    ::py 
    print("Print in python - ",a[i]) 
    l.append(a[i]**2)
    ::/py
    
    ::java 
    System.out.println("Sout from Java - "+a[i]);
    ::/java
}
::/c

::py
print("Final list:", l)
::/py
"""
    
    print("🚀" + "="*80)
    print("🚀 TESTING WEBSOCKET-COMPATIBLE NESTED EXECUTION")
    print("🚀" + "="*80)
    
    # Test with DEBUG ON (like frontend debug mode)
    print("\n🟢 TESTING WITH DEBUG MODE ON (like frontend)")
    advanced_orchestrator.DEBUG_MODE = True
    
    # Parse the code (simulating what the server does)
    blocks = parse_code_to_tree(nested_code)
    print(f"📦 Parsed blocks: {blocks}")
    
    print("\n🔥 EXECUTING VIA WEBSOCKET GENERATOR:")
    
    # Execute via the generator (simulating WebSocket execution)
    for line in execute_tree_generator(blocks):
        print(line)
    
    print("\n🔴 TESTING WITH DEBUG MODE OFF (like frontend)")
    advanced_orchestrator.DEBUG_MODE = False
    
    # Parse again
    blocks = parse_code_to_tree(nested_code)
    
    print("\n🔥 EXECUTING VIA WEBSOCKET GENERATOR (CLEAN OUTPUT):")
    
    # Execute via the generator with debug OFF
    for line in execute_tree_generator(blocks):
        print(line)
    
    print("\n🏁" + "="*80)
    print("🏁 WEBSOCKET NESTED TEST COMPLETED")
    print("🏁" + "="*80)

if __name__ == "__main__":
    test_websocket_nested()