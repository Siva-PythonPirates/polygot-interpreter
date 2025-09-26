#!/usr/bin/env python3
"""
Test the new generator with output methods
"""

from advanced_orchestrator import parse_code_to_tree, execute_tree_generator, set_debug_mode, get_debug_mode

def test_new_generator():
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
    
    print("=== Testing NEW Generator with DEBUG OFF ===")
    set_debug_mode(False)
    print(f"Debug mode: {get_debug_mode()}")
    
    blocks = parse_code_to_tree(test_code)
    print(f"Parsed blocks: {len(blocks)}")
    
    print("\n--- Generator Output (Debug OFF) ---")
    for log_entry in execute_tree_generator(blocks):
        print(f">> {log_entry}")
    print("--- End Generator Output ---")
    
    print("\n=== Testing NEW Generator with DEBUG ON ===")
    set_debug_mode(True)
    print(f"Debug mode: {get_debug_mode()}")
    
    print("\n--- Generator Output (Debug ON) ---")
    for log_entry in execute_tree_generator(blocks):
        print(f">> {log_entry}")
    print("--- End Generator Output ---")

if __name__ == "__main__":
    test_new_generator()