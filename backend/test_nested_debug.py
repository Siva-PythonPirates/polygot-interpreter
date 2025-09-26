#!/usr/bin/env python3
"""
Test nested syntax with debug toggle
"""

from advanced_orchestrator import SharedStateOrchestrator

def test_nested_debug_toggle():
    orchestrator = SharedStateOrchestrator()
    
    # Test nested code
    nested_code = """
::c
int a = 5;
int b = 10;

::py
result = a * b * 2
print("Python calculated:", result)
::/py

printf("C result: %d\\n", a + b + result);
::/c
"""
    
    print("=== Testing NESTED with DEBUG_MODE = True ===")
    # Enable debug mode
    import advanced_orchestrator
    advanced_orchestrator.DEBUG_MODE = True
    
    orchestrator.parse_and_execute(nested_code)
    
    print("\n=== Testing NESTED with DEBUG_MODE = False ===")
    # Disable debug mode
    advanced_orchestrator.DEBUG_MODE = False
    
    # Reset orchestrator state for clean test
    orchestrator = SharedStateOrchestrator()
    
    orchestrator.parse_and_execute(nested_code)
    
    print("\n=== Nested Debug Toggle Test Completed ===")

if __name__ == "__main__":
    test_nested_debug_toggle()