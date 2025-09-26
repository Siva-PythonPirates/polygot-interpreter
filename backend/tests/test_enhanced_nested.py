#!/usr/bin/env python3

# Test the enhanced nested implementation

from advanced_orchestrator import SharedStateOrchestrator
import advanced_orchestrator

def test_enhanced_nested():
    """Test enhanced nested block implementation"""
    
    # Your exact nested structure
    nested_code = """
::py
l=[]
::/py

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
print("Final list:", l)
::/py
"""
    
    print("🔥" + "="*80)
    print("🔥 TESTING ENHANCED NESTED IMPLEMENTATION")
    print("🔥" + "="*80)
    
    # Test with DEBUG ON
    print("\n🟢" + "="*50)
    print("🟢 WITH DEBUG MODE ON")
    print("🟢" + "="*50)
    
    advanced_orchestrator.DEBUG_MODE = True
    orchestrator = SharedStateOrchestrator()
    
    try:
        orchestrator.parse_and_execute(nested_code)
    except Exception as e:
        print(f"❌ Error with debug ON: {e}")
    
    print("\n🔴" + "="*50)
    print("🔴 WITH DEBUG MODE OFF")  
    print("🔴" + "="*50)
    
    # Test with DEBUG OFF
    advanced_orchestrator.DEBUG_MODE = False
    orchestrator = SharedStateOrchestrator()
    
    try:
        orchestrator.parse_and_execute(nested_code)
    except Exception as e:
        print(f"❌ Error with debug OFF: {e}")
    
    print("\n🏁" + "="*80)
    print("🏁 ENHANCED NESTED TEST COMPLETED")
    print("🏁" + "="*80)

if __name__ == "__main__":
    test_enhanced_nested()