#!/usr/bin/env python3
"""
Test your simple nested code via WebSocket generator
"""

from advanced_orchestrator import SharedStateOrchestrator
import advanced_orchestrator

def test_your_code_websocket():
    print("🚀" + "="*80)
    print("🚀 TESTING YOUR SIMPLE NESTED CODE VIA WEBSOCKET")
    print("🚀" + "="*80)
    
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
    
    print("\n🟢 TESTING WITH DEBUG MODE ON (like frontend)")
    advanced_orchestrator.DEBUG_MODE = True
    
    print("🔥 EXECUTING VIA WEBSOCKET GENERATOR:")
    
    # First parse the code into blocks
    from advanced_orchestrator import parse_code_to_tree, execute_tree_generator
    blocks = parse_code_to_tree(your_code)
    print(f"📦 Parsed blocks: {blocks}")
    
    output_lines = []
    for line in execute_tree_generator(blocks):
        print(line)
        output_lines.append(line)
    
    print("\n🔴 TESTING WITH DEBUG MODE OFF (like frontend)")
    advanced_orchestrator.DEBUG_MODE = False
    
    # Reset orchestrator
    orchestrator = SharedStateOrchestrator()
    
    print("\n🔥 EXECUTING VIA WEBSOCKET GENERATOR (CLEAN OUTPUT):")
    
    # Parse the code again for clean execution
    blocks = parse_code_to_tree(your_code)
    
    for line in execute_tree_generator(blocks):
        if line.strip():  # Only show non-empty lines
            print(line)
    
    print("\n🏁" + "="*80)
    print("🏁 YOUR SIMPLE NESTED WEBSOCKET TEST COMPLETED")
    print("🏁" + "="*80)

if __name__ == "__main__":
    test_your_code_websocket()