#!/usr/bin/env python3
"""
Test just the C block to verify it's working
"""

from advanced_orchestrator import SharedStateOrchestrator
import advanced_orchestrator

def test_c_block():
    advanced_orchestrator.DEBUG_MODE = True
    orchestrator = SharedStateOrchestrator()
    
    c_code = """::c
int nums[] = {50, 25, 75, 100, 10};
float pi = 3.14f;
char grade = 'A';
char name[] = "Polyglot";
::/c"""
    
    print("=== Testing C Block Only ===")
    orchestrator.parse_and_execute(c_code)

if __name__ == "__main__":
    test_c_block()