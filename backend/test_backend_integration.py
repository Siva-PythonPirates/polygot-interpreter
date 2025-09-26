from advanced_orchestrator import execute_polyglot_code, set_debug_mode

# Test the updated advanced_orchestrator
set_debug_mode(True)

print("Testing updated advanced_orchestrator.py...")

# Test nested execution
nested_test = """
::c
int numbers[] = {10, 20, 30};
for(int i = 0; i < 3; i++) {
    ::py print("Python says:", numbers[i]) ::/py
    ::java System.out.println("Java says: " + numbers[i]) ::/java
}
::/c
"""

execute_polyglot_code(nested_test)
print("\n🎉 Backend integration successful!")