#!/usr/bin/env python3

from advanced_orchestrator import parse_code_to_tree

def test_browser_code():
    # Test the exact code from browser  
    browser_code = """::c
int numbers[] = {1, 2, 3, 4, 5};
printf("Array elements:\\n");
for(int i = 0; i < 5; i++) {
    printf("Element %d: ", i);
    ::py print(numbers[i] * numbers[i]) ::/py
}
printf("Processing complete!\\n");
::/c"""

    print('=== Testing Browser Code ===')
    print('Input code:')
    print(browser_code)
    print()

    tree = parse_code_to_tree(browser_code)
    print(f'Parsed tree has {len(tree)} blocks:')
    
    for i, block in enumerate(tree):
        print(f'\nBlock {i+1}:')
        print(f'  Lang: {block["lang"]}')
        print(f'  Is Nested: {block.get("is_nested", False)}')
        print(f'  Code length: {len(block["code"])}')
        
        if block.get('is_nested'):
            print(f'  ✅ NESTED STRUCTURE DETECTED!')
            nested_struct = block["nested_structure"]
            print(f'  Outer lang: {nested_struct["outer_lang"]}')
            print(f'  Has nested: {nested_struct["has_nested"]}')
            print(f'  Nested blocks: {len(nested_struct["nested_blocks"])}')
            
            for j, nested in enumerate(nested_struct["nested_blocks"]):
                print(f'    Nested {j+1}: {nested["lang"]} -> "{nested["code"]}"')
        else:
            print(f'  ❌ NOT DETECTED AS NESTED')
            print(f'  Raw code: {block["code"][:200]}...')

if __name__ == "__main__":
    test_browser_code()