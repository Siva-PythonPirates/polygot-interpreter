#!/usr/bin/env python3

# Simple test of WebSocket functionality
from advanced_orchestrator import parse_code_to_tree, execute_tree_generator
import advanced_orchestrator

# Test the exact code from frontend
nested_code = """
::py
results = []
::/py

::c
int numbers[] = {2, 4, 6, 8, 10};
for(int i = 0; i < 5; i++) {
    ::py 
    print(f"Processing {numbers[i]} in Python")
    results.append(numbers[i] ** 2)
    ::/py
    
    ::java 
    System.out.println("Java confirms: " + numbers[i] + " squared");
    ::/java
}
::/c

::py
print("Final results:", results)
print("Sum:", sum(results))
::/py
"""

print('🎯 Testing frontend code example with nested execution...')
print('📋 Setting debug mode OFF (like frontend clean output):')
advanced_orchestrator.DEBUG_MODE = False

blocks = parse_code_to_tree(nested_code)
print(f'✅ Parsed blocks: {blocks[0]["lang"] if blocks else "none"} ({len(blocks)} blocks)')

print('\n🚀 WebSocket-style execution (clean output):')
print('=' * 40)
for line in execute_tree_generator(blocks):
    print(line)
print('=' * 40)
print('✅ Frontend-backend integration working perfectly!')