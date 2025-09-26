#!/usr/bin/env python3
"""
Test the corrected nested syntax
"""

from advanced_orchestrator import SharedStateOrchestrator
import advanced_orchestrator

def test_corrected_nested():
    # Correct nested syntax - C as the outer language containing Python/Java
    corrected_nested = """::c
int a[] = {1, 2, 3, 4, 5};
int l[5];  // Array to store results
int l_count = 0;

for(int i = 0; i < 5; i++) {
    ::py 
    print("Print in python - ", a[i])
    result = a[i] ** 2
    ::/py
    
    ::java 
    System.out.println("Sout from Java - " + a[i]);
    ::/java
    
    // Store the squared result
    l[l_count] = result;
    l_count++;
}

// Print final results in C
printf("Final squared values: ");
for(int j = 0; j < l_count; j++) {
    printf("%d ", l[j]);
}
printf("\\n");
::/c"""

    print("=== Testing CORRECTED Nested Syntax ===")
    advanced_orchestrator.DEBUG_MODE = True
    
    orchestrator = SharedStateOrchestrator()
    orchestrator.parse_and_execute(corrected_nested)

def test_sequential_alternative():
    # Alternative: Pure sequential blocks (easier and more reliable)
    sequential_alternative = """::py
l = []
::/py

::c
int a[] = {1, 2, 3, 4, 5};
::/c

::py
for i in range(5):
    print("Print in python - ", a[i])
    l.append(a[i] ** 2)
    print("Squared result:", a[i] ** 2)
::/py

::java
System.out.println("Java processing:");
for(int i = 0; i < 5; i++) {
    System.out.println("Sout from Java - " + a[i]);
}
::/java

::py
print("Final list:", l)
::/py"""

    print("\n=== Testing SEQUENTIAL Alternative ===")
    advanced_orchestrator.DEBUG_MODE = True
    
    orchestrator = SharedStateOrchestrator()
    orchestrator.parse_and_execute(sequential_alternative)

if __name__ == "__main__":
    test_corrected_nested()
    test_sequential_alternative()