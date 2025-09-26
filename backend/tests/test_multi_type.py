#!/usr/bin/env python3
"""
Test the specific multi-type data demo case
"""

from advanced_orchestrator import SharedStateOrchestrator
import advanced_orchestrator

def test_multi_type_demo():
    # Test code from user
    test_code = """::c
int nums[] = {50, 25, 75, 100, 10};
float pi = 3.14f;
char grade = 'A';
char name[] = "Polyglot";
::/c

::py
# Work with all data types seamlessly
nums.sort()
pi_doubled = pi * 2
message = f"Student {name} got grade {grade}"
stats = {"count": len(nums), "max": max(nums)}
::/py

::java
System.out.println("=== Multi-Type Data Demo ===");
System.out.println("Sorted numbers: ");
for (int i = 0; i < nums.length; i++) {
    System.out.print(nums[i] + " ");
}
System.out.println();
System.out.println("Pi doubled: " + pi_doubled);
System.out.println("Message: " + message);
::/java"""
    
    print("=== Testing Multi-Type Data Demo with DEBUG ON ===")
    advanced_orchestrator.DEBUG_MODE = True
    
    orchestrator = SharedStateOrchestrator()
    orchestrator.parse_and_execute(test_code)
    
    print("\n=== Testing Multi-Type Data Demo with DEBUG OFF ===")
    advanced_orchestrator.DEBUG_MODE = False
    
    orchestrator = SharedStateOrchestrator()
    orchestrator.parse_and_execute(test_code)

if __name__ == "__main__":
    test_multi_type_demo()