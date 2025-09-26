import re
import json
import textwrap
from engine import execute_in_docker

# Debug configuration
DEBUG_MODE = True  # Set to False to hide all debug output

def debug_print(message: str):
    """Print debug message only if debug mode is enabled"""
    if DEBUG_MODE:
        print(message)

def set_debug_mode(enabled: bool):
    """Toggle debug mode on/off"""
    global DEBUG_MODE
    DEBUG_MODE = enabled
    debug_print(f"Debug mode {'enabled' if enabled else 'disabled'}")

def get_debug_mode() -> bool:
    """Get current debug mode status"""
    return DEBUG_MODE

def parse_nested_structure(code_str: str) -> dict:
    """Parse nested language blocks and return structured representation"""
    
    # Find the outermost language block
    outer_match = re.search(r'::(\w+)(.*?)::/\1', code_str, re.DOTALL)
    if not outer_match:
        return None
    
    outer_lang = outer_match.group(1)
    outer_content = outer_match.group(2)
    
    # Look for nested blocks within the outer content
    nested_blocks = []
    nested_pattern = re.compile(r'::(\w+)(.*?)::/\1', re.DOTALL)
    
    for nested_match in nested_pattern.finditer(outer_content):
        nested_lang = nested_match.group(1)
        nested_code = nested_match.group(2).strip()
        
        nested_blocks.append({
            'lang': nested_lang,
            'code': nested_code,
            'start_pos': nested_match.start(),
            'end_pos': nested_match.end()
        })
    
    return {
        'outer_lang': outer_lang,
        'outer_content': outer_content,
        'nested_blocks': nested_blocks,
        'has_nested': len(nested_blocks) > 0
    }

def execute_nested_block(structure: dict, current_state: dict):
    """Execute nested language structure by expanding inner blocks"""
    
    if not structure['has_nested']:
        # No nesting, execute as regular block
        return structure['outer_content']
    
    outer_content = structure['outer_content']
    updated_state = current_state.copy()
    
    # Process nested blocks in reverse order to maintain positions
    for nested_block in reversed(structure['nested_blocks']):
        nested_lang = nested_block['lang']
        nested_code = nested_block['code']
        start_pos = nested_block['start_pos']
        end_pos = nested_block['end_pos']
        
        debug_print(f"🔄 Executing nested {nested_lang} block")
        
        try:
            # Get referenced variables for this nested block
            referenced_vars = extract_variable_references(nested_code, nested_lang)
            available_vars = {k: v for k, v in updated_state.items() if k in referenced_vars}
            
            # Prepare nested block execution
            injected_declarations = inject_variable_declarations(nested_lang, available_vars)
            
            # Check what variables this nested block modifies
            modified_vars = extract_modified_variables(nested_code, nested_lang)
            output_capture = inject_output_capture(nested_lang, {k: updated_state.get(k, 0) for k in modified_vars}, nested_code)
            
            full_nested_code = injected_declarations + nested_code + output_capture
            
            debug_print(f"🔍 Nested {nested_lang} code:\n{full_nested_code}")
            
            # Execute nested block
            output = execute_in_docker(nested_lang, full_nested_code, "{}")
            
            # Try to parse output for variable updates
            actual_output = ""
            try:
                new_vars = json.loads(output.strip())
                updated_state.update(new_vars)
                debug_print(f"📊 Nested block updated variables: {new_vars}")
            except json.JSONDecodeError:
                # It's actual program output
                actual_output = output.strip()
                debug_print(f"📄 Nested block produced output: {actual_output}")
            
            # Replace the nested block with its output in outer content
            before = outer_content[:start_pos]
            after = outer_content[end_pos:]
            
            # Use actual output if any, otherwise empty
            outer_content = before + actual_output + after
            
            # Update positions for remaining blocks
            pos_diff = len(actual_output) - (end_pos - start_pos)
            for other_block in structure['nested_blocks']:
                if other_block['start_pos'] < start_pos:
                    other_block['start_pos'] += pos_diff
                    other_block['end_pos'] += pos_diff
                    
        except Exception as e:
            debug_print(f"❌ Error executing nested {nested_lang}: {e}")
            error_msg = f"/* Error: {e} */"
            before = outer_content[:start_pos]
            after = outer_content[end_pos:]
            outer_content = before + error_msg + after
    
    return outer_content, updated_state

def parse_code_to_tree(code_str: str) -> list:
    """Parse language blocks with support for nesting"""
    
    # First check for nested structure
    nested_structure = parse_nested_structure(code_str)
    
    if nested_structure and nested_structure['has_nested']:
        debug_print(f"🔍 Detected nested structure: {nested_structure['outer_lang']} with nested blocks")
        return [{
            'lang': nested_structure['outer_lang'],
            'code': nested_structure['outer_content'],
            'nested_structure': nested_structure,
            'is_nested': True
        }]
    
    # Fallback to sequential parsing
    blocks = []
    pattern = re.compile(r'::(\w+)\s*(.*?)\s*::/\1', re.DOTALL)
    
    for match in pattern.finditer(code_str):
        lang = match.group(1).strip()
        code = textwrap.dedent(match.group(2)).strip()
        blocks.append({
            'lang': lang, 
            'code': code,
            'is_nested': False
        })
        
    return blocks

def inject_variable_declarations(lang: str, variables: dict) -> str:
    """Automatically inject variable declarations based on language"""
    if not variables:
        return ""
    
    declarations = []
    
    if lang == 'c':
        for var_name, value in variables.items():
            if isinstance(value, list):
                size = len(value)
                if all(isinstance(x, int) for x in value):
                    arr_str = ", ".join(map(str, value))
                    declarations.append(f"int {var_name}[] = {{{arr_str}}};")
                elif all(isinstance(x, float) for x in value):
                    arr_str = ", ".join(map(str, value))
                    declarations.append(f"float {var_name}[] = {{{arr_str}}};")
                elif all(isinstance(x, str) and len(x) == 1 for x in value):
                    arr_str = ", ".join([f"'{x}'" for x in value])
                    declarations.append(f"char {var_name}[] = {{{arr_str}}};")
                declarations.append(f"int {var_name}_size = {size};")
            elif isinstance(value, int):
                declarations.append(f"int {var_name} = {value};")
            elif isinstance(value, float):
                declarations.append(f"float {var_name} = {value}f;")
            elif isinstance(value, str):
                if len(value) == 1:
                    declarations.append(f"char {var_name} = '{value}';")
                else:
                    declarations.append(f'char {var_name}[] = "{value}";')
                
    elif lang == 'py':
        for var_name, value in variables.items():
            if isinstance(value, list):
                declarations.append(f"{var_name} = {value}")
            elif isinstance(value, dict):
                declarations.append(f"{var_name} = {value}")
            elif isinstance(value, (int, float, str, bool)):
                declarations.append(f"{var_name} = {repr(value)}")
            elif value is None:
                declarations.append(f"{var_name} = None")
                
    elif lang == 'java':
        for var_name, value in variables.items():
            if isinstance(value, list):
                if all(isinstance(x, int) for x in value):
                    arr_str = ", ".join(map(str, value))
                    declarations.append(f"int[] {var_name} = {{{arr_str}}};")
                elif all(isinstance(x, float) for x in value):
                    arr_str = ", ".join(map(str, value))
                    declarations.append(f"float[] {var_name} = {{{arr_str}}}f;")
                elif all(isinstance(x, str) for x in value):
                    arr_str = ", ".join([f'"{x}"' for x in value])
                    declarations.append(f"String[] {var_name} = {{{arr_str}}};")
            elif isinstance(value, int):
                declarations.append(f"int {var_name} = {value};")
            elif isinstance(value, float):
                declarations.append(f"float {var_name} = {value}f;")
            elif isinstance(value, bool):
                declarations.append(f"boolean {var_name} = {'true' if value else 'false'};")
            elif isinstance(value, str):
                declarations.append(f'String {var_name} = "{value}";')
    
    return "\n".join(declarations) + "\n" if declarations else ""

def inject_output_capture(lang: str, variables: dict, user_code: str = "") -> str:
    """Automatically inject code to capture and output variables as JSON"""
    if not variables:
        return ""
    
    if lang == 'c':
        # Analyze the user code to determine variable types and categories
        array_vars = {}  # var_name -> type
        string_vars = set()
        scalar_vars = {}  # var_name -> type
        
        for var_name in variables.keys():
            # Check for strings FIRST (char arrays with string literals)
            if re.search(rf'char\s+{var_name}\s*\[\s*\d*\s*\]\s*=\s*"', user_code):
                string_vars.add(var_name)
            # Also check for char arrays without explicit size (strings)
            elif re.search(rf'char\s+{var_name}\s*\[\s*\]\s*=\s*"', user_code):
                string_vars.add(var_name)
            # Check if variable is declared as array (with {} syntax)
            elif re.search(rf'(int|float|double|char)\s+{var_name}\s*\[\s*\]\s*=\s*\{{', user_code):
                match = re.search(rf'(int|float|double|char)\s+{var_name}\s*\[\s*\]\s*=\s*\{{', user_code)
                array_vars[var_name] = match.group(1)
            else:
                # Determine scalar type
                for c_type in ['int', 'float', 'double', 'char']:
                    if re.search(rf'{c_type}\s+{var_name}\s*=', user_code):
                        scalar_vars[var_name] = c_type
                        break
                else:
                    scalar_vars[var_name] = 'int'  # default
        
        # For C, we need to declare size variables first, then capture output
        size_declarations = []
        output_parts = []
        
        for var_name in variables.keys():
            if var_name in array_vars:
                value = variables[var_name]
                c_type = array_vars[var_name]
                if isinstance(value, list):
                    # Declare size variable for arrays
                    size_declarations.append(f'int {var_name}_size = {len(value)};')
                    
                    # Array output with appropriate format specifier
                    format_spec = {'int': '%d', 'float': '%.2f', 'double': '%.2f', 'char': '%c'}[c_type]
                    
                    if len(output_parts) > 0:
                        output_parts.append('printf(", ");')
                    output_parts.append(f'printf("\\"{var_name}\\": [");')
                    output_parts.append(f'for(int i = 0; i < {var_name}_size; i++) {{')
                    output_parts.append(f'    printf("{format_spec}", {var_name}[i]);')
                    output_parts.append(f'    if(i < {var_name}_size - 1) printf(", ");')
                    output_parts.append(f'}}')
                    output_parts.append(f'printf("]");')
                    
            elif var_name in string_vars:
                # String variable
                if len(output_parts) > 0:
                    output_parts.append('printf(", ");')
                output_parts.append(f'printf("\\"{var_name}\\": \\"%s\\"", {var_name});')
                
            else:
                # Scalar variable with appropriate format
                c_type = scalar_vars.get(var_name, 'int')
                
                if len(output_parts) > 0:
                    output_parts.append('printf(", ");')
                
                if c_type == 'char':
                    # For chars, we need quotes in JSON
                    output_parts.append(f'printf("\\"{var_name}\\": \\"%c\\"", {var_name});')
                else:
                    format_spec = {'int': '%d', 'float': '%.2f', 'double': '%.2f'}[c_type]
                    output_parts.append(f'printf("\\"{var_name}\\": {format_spec}", {var_name});')
        
        if output_parts:
            json_output = []
            # Add size declarations first
            json_output.extend(size_declarations)
            # Then add JSON output code
            json_output.append('printf("{");')
            json_output.extend(output_parts)
            json_output.append('printf("}");')
            return "\n" + "\n".join(json_output)
            
    elif lang == 'py':
        # For Python, capture variables and print as JSON with simple serialization
        var_names = list(variables.keys())
        if var_names:
            return f"""
import json

result_dict = {{}}
{chr(10).join([f'if "{var}" in locals(): result_dict["{var}"] = {var}' for var in var_names])}
print(json.dumps(result_dict))"""
            
    elif lang == 'java':
        # For Java, we need to build JSON manually (no external libs)
        if variables:
            var_names = list(variables.keys())
            java_json = []
            java_json.append('System.out.print("{");')
            
            for i, var_name in enumerate(var_names):
                value = variables[var_name]
                if isinstance(value, list):
                    # Handle different array types
                    if all(isinstance(x, int) for x in value):
                        java_json.append(f'System.out.print("\\"{var_name}\\": [");')
                        java_json.append(f'for(int i = 0; i < {var_name}.length; i++) {{')
                        java_json.append(f'    System.out.print({var_name}[i]);')
                        java_json.append(f'    if(i < {var_name}.length - 1) System.out.print(", ");')
                        java_json.append(f'}}')
                        java_json.append(f'System.out.print("]");')
                    elif all(isinstance(x, str) for x in value):
                        java_json.append(f'System.out.print("\\"{var_name}\\": [");')
                        java_json.append(f'for(int i = 0; i < {var_name}.length; i++) {{')
                        java_json.append(f'    System.out.print("\\"" + {var_name}[i] + "\\"");')
                        java_json.append(f'    if(i < {var_name}.length - 1) System.out.print(", ");')
                        java_json.append(f'}}')
                        java_json.append(f'System.out.print("]");')
                elif isinstance(value, str):
                    java_json.append(f'System.out.print("\\"{var_name}\\": \\"" + {var_name} + "\\"");')
                elif isinstance(value, bool):
                    java_json.append(f'System.out.print("\\"{var_name}\\": " + {var_name});')
                else:
                    java_json.append(f'System.out.print("\\"{var_name}\\": " + {var_name});')
                
                if i < len(var_names) - 1:
                    java_json.append('System.out.print(", ");')
            
            java_json.append('System.out.print("}");')
            return "\n" + "\n".join(java_json)
    
    return ""

def execute_tree_generator(blocks: list, input_state: dict = None):
    """Execute sequential language blocks with automatic variable injection"""
    current_state = input_state or {}
    
    if DEBUG_MODE:
        yield "=" * 50
        yield "🔄 POLYGLOT EXECUTION PIPELINE STARTED"
        yield "=" * 50
    
    debug_print(f"🔄 Starting pipeline with {len(blocks)} language blocks")
    debug_print(f"📊 Initial state: {current_state}")
    
    for i, block in enumerate(blocks):
        lang = block['lang']
        
        if DEBUG_MODE:
            yield f"\n🏗️ === BLOCK {i+1}/{len(blocks)}: {lang.upper()} ==="
        
        debug_print(f"\n🏗️ === BLOCK {i+1}/{len(blocks)}: {lang.upper()} ===")
        
        # Handle nested blocks
        if block.get('is_nested', False):
            debug_print(f"🔄 Processing nested block structure")
            if DEBUG_MODE:
                yield f"🔄 Detected nested structure with {len(block['nested_structure']['nested_blocks'])} inner blocks"
            
            # Execute nested structure
            user_code, current_state = execute_nested_block(block['nested_structure'], current_state)
            if DEBUG_MODE:
                yield f"🔄 Nested execution completed, updated state: {list(current_state.keys())}"
        else:
            user_code = block['code']
        
        # Extract variable names that the user code references
        referenced_vars = extract_variable_references(user_code, lang)
        debug_print(f"🔍 Variables referenced in {lang}: {referenced_vars}")
        
        # Filter current_state to only include referenced variables
        available_vars = {k: v for k, v in current_state.items() if k in referenced_vars}
        
        if available_vars:
            debug_print(f"📥 Variables received from previous blocks: {available_vars}")
            if DEBUG_MODE:
                yield f"📥 Receiving variables: {list(available_vars.keys())}"
        else:
            debug_print(f"📥 No variables passed to {lang} block")
            if DEBUG_MODE and i > 0:
                yield f"📥 No variables received from previous blocks"
        
        if i == 0 and not available_vars:
            debug_print(f"🏁 First block - starting fresh")
            if DEBUG_MODE:
                yield "🏁 Starting fresh (first block)"
        
        # Inject variable declarations at the beginning
        injected_declarations = inject_variable_declarations(lang, available_vars)
        if available_vars and injected_declarations:
            debug_print(f"💉 Injected variable declarations for {lang}:")
            for line in injected_declarations.split('\n'):
                if line.strip():
                    debug_print(f"   📝 {line.strip()}")
        
        # Inject output capture at the end (only if user code modifies variables)
        modified_vars = extract_modified_variables(user_code, lang)
        debug_print(f"✏️ Variables modified in {lang}: {modified_vars}")
        
        if DEBUG_MODE and modified_vars:
            yield f"✏️ Variables being modified: {list(modified_vars)}"
        
        if DEBUG_MODE and lang == 'java':
            yield f"DEBUG Java modified vars: {modified_vars}"
        
        # For C, if we detect variable declarations, we need to capture them
        if lang == 'c' and modified_vars:
            # Create a dummy state for variables we're declaring in this block
            new_vars_state = {}
            for var in modified_vars:
                # Try to extract array values from the code
                array_match = re.search(rf'{var}\s*\[\s*\]\s*=\s*\{{\s*([^}}]+)\s*\}}', user_code)
                if array_match:
                    values_str = array_match.group(1)
                    # Determine if it's int, float, or char array
                    if re.search(rf'int\s+{var}', user_code):
                        values = [int(x.strip()) for x in values_str.split(',')]
                    elif re.search(rf'float\s+{var}', user_code):
                        values = [float(x.strip()) for x in values_str.split(',')]
                    elif re.search(rf'char\s+{var}', user_code):
                        values = [x.strip().strip("'") for x in values_str.split(',')]
                    else:
                        values = [int(x.strip()) for x in values_str.split(',')]
                    new_vars_state[var] = values
                
                # Try to extract string literals (with explicit size)
                elif re.search(rf'char\s+{var}\s*\[\s*\d+\s*\]\s*=\s*"([^"]*)"', user_code):
                    string_match = re.search(rf'char\s+{var}\s*\[\s*\d+\s*\]\s*=\s*"([^"]*)"', user_code)
                    new_vars_state[var] = string_match.group(1)
                
                # Try to extract string literals (without explicit size)
                elif re.search(rf'char\s+{var}\s*\[\s*\]\s*=\s*"([^"]*)"', user_code):
                    string_match = re.search(rf'char\s+{var}\s*\[\s*\]\s*=\s*"([^"]*)"', user_code)
                    new_vars_state[var] = string_match.group(1)
                
                # Try to extract scalar values
                elif re.search(rf'(int|float|double|char)\s+{var}\s*=\s*([^;]+)', user_code):
                    scalar_match = re.search(rf'(int|float|double|char)\s+{var}\s*=\s*([^;]+)', user_code)
                    var_type = scalar_match.group(1)
                    value_str = scalar_match.group(2).strip()
                    
                    if var_type == 'int':
                        new_vars_state[var] = int(value_str)
                    elif var_type in ['float', 'double']:
                        new_vars_state[var] = float(value_str.rstrip('f'))
                    elif var_type == 'char':
                        new_vars_state[var] = value_str.strip("'")
                else:
                    # Default for other variables
                    new_vars_state[var] = 0
            
            output_capture = inject_output_capture(lang, new_vars_state, user_code)
        else:
            output_capture = inject_output_capture(lang, {k: current_state.get(k, 0) for k in modified_vars}, user_code)
        
        # Combine the code
        full_code = injected_declarations + user_code + output_capture
        
        debug_print(f"🚀 Executing {lang} block...")
        
        try:
            # Execute the code
            if DEBUG_MODE and lang == 'java':
                yield f"DEBUG Java code:\n{full_code}\n---"
            
            old_state_keys = set(current_state.keys())
            output = execute_in_docker(lang, full_code, "{}")
            
            # Try to parse output as JSON
            try:
                new_state = json.loads(output.strip())
                
                # Track what variables were added/modified
                added_vars = {k: v for k, v in new_state.items() if k not in old_state_keys}
                modified_vars_actual = {k: v for k, v in new_state.items() if k in old_state_keys and current_state[k] != v}
                
                current_state.update(new_state)
                
                if added_vars:
                    debug_print(f"➕ New variables created in {lang}: {added_vars}")
                    if DEBUG_MODE:
                        yield f"➕ Created: {list(added_vars.keys())} = {list(added_vars.values())}"
                        
                if modified_vars_actual:
                    debug_print(f"🔄 Variables modified in {lang}: {modified_vars_actual}")
                    if DEBUG_MODE:
                        yield f"🔄 Modified: {list(modified_vars_actual.keys())} = {list(modified_vars_actual.values())}"
                
                # Show what will be passed to next block
                next_block_index = i + 1
                if next_block_index < len(blocks):
                    next_lang = blocks[next_block_index]['lang']
                    next_referenced = extract_variable_references(blocks[next_block_index]['code'], next_lang)
                    vars_to_pass = {k: v for k, v in current_state.items() if k in next_referenced}
                    if vars_to_pass:
                        debug_print(f"📤 Variables ready for {next_lang}: {vars_to_pass}")
                        if DEBUG_MODE:
                            yield f"📤 Passing to {next_lang.upper()}: {list(vars_to_pass.keys())}"
                    else:
                        debug_print(f"📤 No variables will be passed to {next_lang}")
                        if DEBUG_MODE:
                            yield f"📤 Nothing to pass to {next_lang.upper()}"
                
            except json.JSONDecodeError:
                debug_print(f"📄 {lang} produced user output (no variable updates)")
                yield output
                
        except Exception as e:
            debug_print(f"❌ Error in {lang} block: {e}")
            yield f"Error in {lang}: {e}"
            break
    
    debug_print(f"🏁 Pipeline completed! Final state: {current_state}")
    
    if DEBUG_MODE:
        yield "\n" + "=" * 50
        yield "🏁 PIPELINE EXECUTION SUMMARY"
        yield "=" * 50
        if current_state:
            yield f"📊 Final variable state: {current_state}"
        else:
            yield "📊 No variables persisted across blocks"
        yield "✅ Pipeline completed successfully"

def extract_variable_references(code: str, lang: str) -> set:
    """Extract variable names that are referenced (read) in the code"""
    references = set()
    
    if lang == 'c':
        # Look for variable usage (simple heuristic)
        for match in re.finditer(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', code):
            var_name = match.group(1)
            # Exclude C keywords and function names
            if var_name not in ['int', 'char', 'float', 'double', 'printf', 'for', 'if', 'else', 'return', 'sizeof', 'i', 'j', 'k', 'main', 'void']:
                references.add(var_name)
    
    elif lang == 'py':
        # Look for variable usage
        for match in re.finditer(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', code):
            var_name = match.group(1)
            # Exclude Python keywords and common functions
            if var_name not in ['import', 'def', 'class', 'if', 'else', 'for', 'while', 'print', 'sort', 'json', 'sys', 'len', 'max', 'min', 'sum', 'str', 'int', 'float', 'list', 'dict', 'True', 'False', 'None']:
                references.add(var_name)
    
    elif lang == 'java':
        # Look for variable usage
        for match in re.finditer(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', code):
            var_name = match.group(1)
            # Exclude Java keywords and common loop variables
            if var_name not in ['int', 'float', 'double', 'boolean', 'String', 'System', 'out', 'println', 'print', 'class', 'public', 'static', 'void', 'length', 'i', 'j', 'k', 'if', 'else', 'for', 'while', 'true', 'false']:
                references.add(var_name)
    
    return references

def parse_control_structures(code: str, lang: str):
    """Parse and extract all control structures like a compiler"""
    structures = {
        'loops': [],
        'conditions': [],
        'exceptions': [],
        'blocks': [],
        'local_vars': set(),
        'scoped_vars': set()
    }
    
    if lang == 'java':
        # Find for loops with their complete structure
        for match in re.finditer(r'for\s*\(\s*([^;]+);\s*([^;]+);\s*([^)]+)\)\s*\{([^}]*)\}', code, re.DOTALL):
            init_part = match.group(1).strip()
            condition = match.group(2).strip()
            increment = match.group(3).strip()
            body = match.group(4).strip()
            
            # Extract loop variable declarations
            for var_match in re.finditer(r'(int|float|double|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)', init_part):
                structures['local_vars'].add(var_match.group(2))
            
            # Extract loop variable assignments
            for var_match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', init_part):
                structures['local_vars'].add(var_match.group(1))
            
            # Extract increment variables
            for var_match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*(\+\+|--|\+=|-=)', increment):
                structures['local_vars'].add(var_match.group(1))
        
        # Find for-each loops
        for match in re.finditer(r'for\s*\(\s*(int|float|double|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)\s*\{([^}]*)\}', code, re.DOTALL):
            loop_var = match.group(2)
            structures['local_vars'].add(loop_var)
        
        # Find while loops
        for match in re.finditer(r'while\s*\([^)]+\)\s*\{([^}]*)\}', code, re.DOTALL):
            body = match.group(1)
            # Any variables declared inside while loop are local
            for var_match in re.finditer(r'(int|float|double|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)', body):
                structures['local_vars'].add(var_match.group(2))
        
        # Find if-else blocks
        for match in re.finditer(r'if\s*\([^)]+\)\s*\{([^}]*)\}(\s*else\s*\{([^}]*)\})?', code, re.DOTALL):
            if_body = match.group(1)
            else_body = match.group(3) if match.group(3) else ""
            
            # Variables declared inside if/else are local
            for body in [if_body, else_body]:
                if body:
                    for var_match in re.finditer(r'(int|float|double|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)', body):
                        structures['local_vars'].add(var_match.group(2))
        
        # Find try-catch blocks
        for match in re.finditer(r'try\s*\{([^}]*)\}\s*catch\s*\([^)]+\)\s*\{([^}]*)\}', code, re.DOTALL):
            try_body = match.group(1)
            catch_body = match.group(2)
            
            # Variables declared inside try/catch are local
            for body in [try_body, catch_body]:
                for var_match in re.finditer(r'(int|float|double|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)', body):
                    structures['local_vars'].add(var_match.group(2))
        
        # Find method parameters and local method declarations
        for match in re.finditer(r'(public|private|protected)?\s*(static)?\s*(void|int|float|double|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)', code):
            # Method names shouldn't be considered as variables
            structures['local_vars'].add(match.group(4))
    
    elif lang == 'c':
        # Find for loops
        for match in re.finditer(r'for\s*\(\s*([^;]+);\s*([^;]+);\s*([^)]+)\)\s*\{([^}]*)\}', code, re.DOTALL):
            init_part = match.group(1).strip()
            
            # Extract loop variable declarations
            for var_match in re.finditer(r'(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-9_]*)', init_part):
                structures['local_vars'].add(var_match.group(2))
        
        # Find while loops and their local variables
        for match in re.finditer(r'while\s*\([^)]+\)\s*\{([^}]*)\}', code, re.DOTALL):
            body = match.group(1)
            for var_match in re.finditer(r'(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-9_]*)', body):
                structures['local_vars'].add(var_match.group(2))
        
        # Find if blocks
        for match in re.finditer(r'if\s*\([^)]+\)\s*\{([^}]*)\}', code, re.DOTALL):
            body = match.group(1)
            for var_match in re.finditer(r'(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-9_]*)', body):
                structures['local_vars'].add(var_match.group(2))
    
    elif lang == 'py':
        # Find for loops
        for match in re.finditer(r'for\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+([^:]+):', code):
            loop_var = match.group(1)
            structures['local_vars'].add(loop_var)
        
        # Find while loops with their indented blocks
        for match in re.finditer(r'while\s+[^:]+:\s*\n((?:\s{4,}[^\n]*\n?)*)', code, re.MULTILINE):
            body = match.group(1)
            # Python variables in loops might be local depending on scope
            for var_match in re.finditer(r'^\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=', body, re.MULTILINE):
                structures['local_vars'].add(var_match.group(1))
        
        # Find try-except blocks
        for match in re.finditer(r'try:\s*\n((?:\s{4,}[^\n]*\n?)*)\s*except[^:]*:\s*\n((?:\s{4,}[^\n]*\n?)*)', code, re.MULTILINE):
            try_body = match.group(1)
            except_body = match.group(2)
            
            for body in [try_body, except_body]:
                for var_match in re.finditer(r'^\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=', body, re.MULTILINE):
                    structures['local_vars'].add(var_match.group(1))
    
    return structures

def extract_modified_variables(code: str, lang: str) -> set:
    """Extract variable names that are modified (written) in the code with scope awareness"""
    modified = set()
    
    # Parse control structures to identify local/scoped variables
    structures = parse_control_structures(code, lang)
    local_vars = structures['local_vars']
    
    debug_print(f"DEBUG Local/scoped vars detected: {local_vars}")
    
    if lang == 'c':
        # Look for array declarations - all types with [] syntax
        for match in re.finditer(r'(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*\]\s*=\s*\{', code):
            var_name = match.group(2)
            if var_name not in local_vars:
                modified.add(var_name)
                
        for match in re.finditer(r'(int|float|double|char)\[\s*\]\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\{', code):
            var_name = match.group(2)
            if var_name not in local_vars:
                modified.add(var_name)
        
        # Look for string declarations (char arrays with strings)
        for match in re.finditer(r'char\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*\d*\s*\]\s*=\s*"', code):
            var_name = match.group(1)
            if var_name not in local_vars:
                modified.add(var_name)
                
        for match in re.finditer(r'char\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*\]\s*=\s*"', code):
            var_name = match.group(1)
            if var_name not in local_vars:
                modified.add(var_name)
        
        # Look for regular variable declarations - all primitive types
        for match in re.finditer(r'(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[^{"]', code):
            var_name = match.group(2)
            if var_name not in local_vars:
                modified.add(var_name)
        
        # Look for assignments to existing variables (name = value)
        for match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=(?!=)', code):
            var_name = match.group(1)
            # Exclude if it's part of a type declaration or local variable
            if (not re.search(r'\b(int|char|float|double)\s+' + re.escape(var_name), code) and 
                var_name not in local_vars):
                modified.add(var_name)
    
    elif lang == 'py':
        # Look for assignments or method calls that modify
        for match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', code):
            var_name = match.group(1)
            # Exclude module imports and local variables
            if (not re.search(r'import\s+.*' + re.escape(var_name), code) and 
                var_name not in local_vars):
                modified.add(var_name)
                
        # Look for in-place modifications like .sort()
        for match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\.\s*(sort|reverse|append|extend|remove|pop|clear|update)\s*\(', code):
            var_name = match.group(1)
            if var_name not in local_vars:
                modified.add(var_name)
                
        # Look for dictionary/list modifications
        for match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*[^\]]+\s*\]\s*=', code):
            var_name = match.group(1)
            if var_name not in local_vars:
                modified.add(var_name)
    
    elif lang == 'java':
        # Look for variable declarations - all types
        for match in re.finditer(r'(int|float|double|boolean|String)\[\]\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=', code):
            var_name = match.group(2)
            if var_name not in local_vars:
                modified.add(var_name)
                
        for match in re.finditer(r'(int|float|double|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=', code):
            var_name = match.group(2)
            if var_name not in local_vars:
                modified.add(var_name)
                
        # Look for assignments to existing variables
        for match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=(?!=)', code):
            var_name = match.group(1)
            
            # Comprehensive scope checking - exclude local variables
            if var_name not in local_vars:
                # Additional checks for edge cases
                is_declaration = re.search(r'\b(int|float|double|boolean|String)\s+' + re.escape(var_name), code)
                if not is_declaration:
                    modified.add(var_name)
    
    debug_print(f"DEBUG Final modified vars: {modified}")
    return modified