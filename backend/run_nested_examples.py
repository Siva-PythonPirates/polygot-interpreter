#!/usr/bin/env python3
"""
🎯 Nested Examples Test Runner
Run this to test all the nested examples locally before trying in browser
"""

from advanced_orchestrator import parse_code_to_tree, execute_nested_block
from engine import execute_in_docker

def test_example(name, code):
    """Test a single nested example"""
    print(f"\n{'='*50}")
    print(f"🧪 Testing: {name}")
    print(f"{'='*50}")
    
    try:
        # Parse the code
        tree = parse_code_to_tree(code)
        
        if tree and tree[0].get('is_nested'):
            # Execute nested processing
            structure = tree[0]['nested_structure']
            processed_code, _ = execute_nested_block(structure, {})
            
            print(f"✅ Processed successfully!")
            print(f"📄 Final C code:\n{processed_code.strip()}")
            
            # Execute the final code
            result = execute_in_docker('c', processed_code.strip(), '{}')
            print(f"\n🚀 Execution Result:")
            print(f"{'─'*30}")
            print(result)
            print(f"{'─'*30}")
            
        else:
            print("❌ Not a nested structure or parsing failed")
            
    except Exception as e:
        print(f"💥 Error: {e}")

def main():
    """Run all examples"""
    
    examples = {
        "Basic Array Processing": '''::c
int numbers[] = {1, 2, 3, 4, 5};
printf("Array elements:\\n");
for(int i = 0; i < 5; i++) {
    printf("Element %d: ", i);
    ::py print(numbers[i] * numbers[i]) ::/py
}
printf("Processing complete!\\n");
::/c''',
        
        "Mathematical Operations": '''::c
printf("=== Mathematical Calculations ===\\n");
int base = 2;
for(int exp = 1; exp <= 5; exp++) {
    printf("2^%d = ", exp);
    ::py print(base ** exp) ::/py
}
printf("=== End Calculations ===\\n");
::/c''',
        
        "Simple Shopping": '''::c
printf("Shopping Cart:\\n");
float prices[] = {12.99, 8.50, 15.75};
for(int item = 0; item < 3; item++) {
    printf("Item %d: $%.2f -> Tax: $", item+1, prices[item]);
    ::py print(f"{prices[item] * 0.08:.2f}") ::/py
}
::/c''',
        
        "Temperature Check": '''::c
printf("Temperature Report:\\n");
int temps[] = {72, 68, 80, 77};
for(int day = 0; day < 4; day++) {
    printf("Day %d: %d°F -> ", day+1, temps[day]);
    if(temps[day] > 75) {
        ::py print("Hot!") ::/py
    } else {
        ::py print("Cool!") ::/py
    }
}
::/c''',
        
        "String Processing": '''::c
printf("Text Demo:\\n");
char* words[] = {"hello", "world", "test"};
for(int w = 0; w < 3; w++) {
    printf("Word: %s -> Uppercase: ", words[w]);
    ::py print(words[w].upper()) ::/py
}
::/c'''
    }
    
    print("🎯 Nested Language Examples Test Runner")
    print("=" * 60)
    
    for name, code in examples.items():
        test_example(name, code)
    
    print(f"\n{'='*60}")
    print("🎉 All tests completed!")
    print("💡 Copy any of the examples to your browser to test the full system!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
