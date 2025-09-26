#!/usr/bin/env python3
"""
Test the exact behavior to diagnose server vs local differences
"""

from advanced_orchestrator import SharedStateOrchestrator
import advanced_orchestrator

def test_server_behavior():
    print("=== TESTING DEBUG MODE STATUS ===")
    print(f"Current DEBUG_MODE: {advanced_orchestrator.DEBUG_MODE}")
    
    # Test with debug OFF (like your server)
    advanced_orchestrator.DEBUG_MODE = False
    print(f"Set DEBUG_MODE to: {advanced_orchestrator.DEBUG_MODE}")
    
    orchestrator = SharedStateOrchestrator()
    
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
    
    print("\n=== EXECUTION START ===")
    orchestrator.parse_and_execute(test_code)
    print("=== EXECUTION END ===")

if __name__ == "__main__":
    test_server_behavior()