#!/usr/bin/env python3
"""
Simple test to verify the WebSocket pipeline matches local testing
"""

import asyncio
from advanced_orchestrator import parse_code_to_tree, execute_tree_generator

async def simulate_websocket_pipeline():
    """Simulate what the WebSocket server does"""
    
    # This is the exact code that failed in the browser
    polyglot_code = """::c
int numbers[] = {1, 2, 3, 4, 5};
printf("Array elements:\\n");
for(int i = 0; i < 5; i++) {
    printf("Element %d: ", i);
    ::py print(numbers[i] * numbers[i]) ::/py
}
printf("Processing complete!\\n");
::/c"""
    
    print("=== SIMULATING WEBSOCKET PIPELINE ===")
    print("Code being processed:")
    print(polyglot_code)
    print("\n" + "="*50)
    
    # Step 1: Parse (same as WebSocket server)
    blocks = parse_code_to_tree(polyglot_code)
    print(f"✅ Parsed into {len(blocks)} blocks")
    
    if blocks:
        for i, block in enumerate(blocks):
            print(f"Block {i+1}: {block['lang']} (nested: {block.get('is_nested', False)})")
    else:
        print("❌ No blocks parsed!")
        return
    
    print("\n" + "="*50)
    print("🚀 EXECUTING PIPELINE...")
    print("="*50)
    
    # Step 2: Execute (same as WebSocket server)
    if blocks:
        async for log_entry in execute_tree_generator_async(blocks):
            print(log_entry)
    else:
        print("❌ Error: Could not parse any code blocks.")
    
    print("--- Pipeline Finished ---")

async def execute_tree_generator_async(blocks):
    """Convert the sync generator to async for testing"""
    for log_entry in execute_tree_generator(blocks):
        yield log_entry

if __name__ == "__main__":
    asyncio.run(simulate_websocket_pipeline())