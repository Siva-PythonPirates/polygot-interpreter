#!/usr/bin/env python3
"""
Test Python array sorting specifically
"""

from advanced_orchestrator import SharedStateOrchestrator
import advanced_orchestrator

def test_array_sorting():
    advanced_orchestrator.DEBUG_MODE = True
    orchestrator = SharedStateOrchestrator()
    
    test_code = """::c
int nums[] = {50, 25, 75, 100, 10};
::/c

::py
print("Before sort:", nums)
nums.sort()
print("After sort:", nums)
::/py"""
    
    print("=== Testing Array Sorting ===")
    orchestrator.parse_and_execute(test_code)

if __name__ == "__main__":
    test_array_sorting()