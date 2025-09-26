#!/usr/bin/env python3
"""
Test script to verify debug toggle functionality
"""

from advanced_orchestrator import SharedStateOrchestrator

def test_debug_toggle():
    orchestrator = SharedStateOrchestrator()
    
    # Test code
    test_code = """
::py
x = 10
y = 20
print("Python result:", x + y)
::/py

::c
printf("C result: %d\\n", x + y);
::/c
"""
    
    print("=== Testing with DEBUG_MODE = True ===")
    # Enable debug mode
    import advanced_orchestrator
    advanced_orchestrator.DEBUG_MODE = True
    
    orchestrator.parse_and_execute(test_code)
    
    print("\n=== Testing with DEBUG_MODE = False ===")
    # Disable debug mode
    advanced_orchestrator.DEBUG_MODE = False
    
    # Reset orchestrator state for clean test
    orchestrator = SharedStateOrchestrator()
    
    orchestrator.parse_and_execute(test_code)
    
    print("\n=== Debug Toggle Test Completed ===")

if __name__ == "__main__":
    test_debug_toggle()