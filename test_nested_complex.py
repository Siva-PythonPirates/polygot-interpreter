import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from advanced_orchestrator import execute_polyglot_code, set_debug_mode

# Enable debug mode to see what's happening
set_debug_mode(True)

print("Testing corrected nested structure...")

# Corrected version of your code
corrected_code = """
::c
int a[] = {1, 2, 3, 4, 5};
for(int i = 0; i < 5; i++) {
    ::py print("Print in python - ", a[i]); l.append(a[i]**2) ::/py
    ::java System.out.println("Sout from Java - " + a[i]) ::/java
}
::/c

::py
print("Final list:", l)
::/py
"""

print("Executing corrected nested structure:")
execute_polyglot_code(corrected_code)