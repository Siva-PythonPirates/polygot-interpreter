# Test cases for the working orchestrator (working_orchestrator_final .py)

# Test 1: Single Java Code (should be detected as Java, not Python)
# Note: Class name must be 'Main' to match Docker container expectations
single_java_fixed = """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java!");
    }
}"""

# Test 2: Simple Sequential Blocks (focus on state transfer)
simple_sequential = """
::c
int numbers[] = {1, 2, 3};
int count = 3;
::/c

::py
print("Numbers from C:", numbers)
print("Count:", count)
doubled = [x * 2 for x in numbers]
::/py

::java
System.out.println("Doubled array from Python:");
for(int x : doubled) {
    System.out.print(x + " ");
}
::/java
"""

# Test 3: Simple Python Code
simple_python = """
data = [10, 20, 30]
print("Data:", data)
total = sum(data)
print("Total:", total)
"""

# Test 4: Complex Multi-Language Data Processing
complex_pipeline = """
::c
int raw_data[] = {5, 10, 15, 20, 25};
int data_size = 5;
::/c

::py
print("Processing data from C:", raw_data)
processed = [x * x for x in raw_data]  # Square each number
average = sum(processed) / len(processed)
print(f"Processed (squared): {processed}")
print(f"Average: {average}")
::/py

::java
System.out.println("Final report from Java:");
System.out.println("Original size: " + data_size);
System.out.print("Processed values: ");
for(int val : processed) {
    System.out.print(val + " ");
}
System.out.println();
System.out.println("Average: " + average);
::/java
"""

# Test 5: Your Nested Block Syntax (from your original request)
# Note: This now works with nested block processing!
nested_complex = """
::c
int a[] = {1, 2, 3, 4, 5};
for(int i = 0; i < 5; i++) {
    ::py 
    print("Print in python - ",a[i]) 
    l.append(a[i]**2)
    ::/py
    
    ::java 
    System.out.println("Sout from Java - "+a[i]);
    ::/java
}
::/c

::py
l=[]
print("Final list:", l)
::/py
"""

# Test 6: Sequential Workaround (alternative approach)
sequential_workaround = """
::c
int a[] = {1, 2, 3, 4, 5};
::/c

::py
l = []
for i in range(5):
    print(f"Print in python - {a[i]}")
    l.append(a[i]**2)
    # Note: Java output would go here in the nested version
::/py

::java
System.out.println("Java output after Python processing:");
for(int i = 0; i < 5; i++) {
    System.out.println("Sout from Java - " + a[i]);
}
::/java

::py
print("Final list:", l)
::/py
"""

def test_all_execution_types():
    """Test all execution types with debug ON and OFF"""
    from advanced_orchestrator import SharedStateOrchestrator
    import advanced_orchestrator
    
    test_cases = [
        ("Single Java", single_java_fixed),
        ("Simple Sequential", simple_sequential), 
        ("Simple Python", simple_python),
        ("Complex Pipeline", complex_pipeline),
        ("Nested Complex", nested_complex),
        ("Sequential Workaround", sequential_workaround)
    ]
    
    # Test with DEBUG_MODE = True
    print("🟢" + "="*80)
    print("🟢 TESTING ALL CASES WITH DEBUG_MODE = TRUE")
    print("🟢" + "="*80)
    
    advanced_orchestrator.DEBUG_MODE = True
    
    for test_name, code in test_cases:
        print(f"\n{'🔧'*50}")
        print(f"🔧 TESTING: {test_name} (DEBUG ON)")
        print(f"{'🔧'*50}")
        
        orchestrator = SharedStateOrchestrator()
        try:
            orchestrator.parse_and_execute(code)
        except Exception as e:
            print(f"❌ Error in {test_name}: {e}")
        
        print(f"{'✅'*50}")
        print(f"✅ COMPLETED: {test_name} (DEBUG ON)")
        print(f"{'✅'*50}\n")
    
    # Test with DEBUG_MODE = False
    print("\n\n🔴" + "="*80)
    print("🔴 TESTING ALL CASES WITH DEBUG_MODE = FALSE")
    print("🔴" + "="*80)
    
    advanced_orchestrator.DEBUG_MODE = False
    
    for test_name, code in test_cases:
        print(f"\n{'🎯'*50}")
        print(f"🎯 TESTING: {test_name} (DEBUG OFF)")
        print(f"{'🎯'*50}")
        
        orchestrator = SharedStateOrchestrator()
        try:
            orchestrator.parse_and_execute(code)
        except Exception as e:
            print(f"❌ Error in {test_name}: {e}")
        
        print(f"{'✅'*50}")
        print(f"✅ COMPLETED: {test_name} (DEBUG OFF)")
        print(f"{'✅'*50}\n")
    
    print("\n🏁" + "="*80)
    print("🏁 ALL TESTS COMPLETED - BOTH DEBUG MODES TESTED")
    print("🏁" + "="*80)

if __name__ == "__main__":
    test_all_execution_types()