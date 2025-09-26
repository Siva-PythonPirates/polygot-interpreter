import re
import json
import textwrap
from engine import execute_in_docker
from typing import Dict, List, Any, Tuple

# Debug configuration
DEBUG_MODE = True

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

class SharedStateOrchestrator:
    """Orchestrator that maintains shared state across multiple language executions"""
    
    def __init__(self):
        self.global_state = {}  # Shared variables across all languages
        self.language_contexts = {}  # Language-specific execution contexts
    
    def parse_mixed_structure(self, code_str: str) -> List[Dict]:
        """Parse mixed sequential and nested language blocks"""
        
        debug_print(f"Parsing mixed structure:\n{code_str}")
        
        # Find the outermost language block
        outer_match = re.search(r'::(\w+)(.*?)::/\1', code_str, re.DOTALL)
        if not outer_match:
            debug_print("No outer block found - treating as sequential blocks")
            return self.parse_sequential_blocks(code_str)
        
        outer_lang = outer_match.group(1)
        outer_content = outer_match.group(2)
        
        debug_print(f"Found outer block: {outer_lang}")
        
        # Parse the structure into executable blocks
        blocks = self.parse_outer_content(outer_lang, outer_content)
        
        return blocks
    
    def parse_outer_content(self, outer_lang: str, content: str) -> List[Dict]:
        """Parse content that may contain sequential and nested blocks"""
        
        # First, check if this content contains nested blocks (inline ::lang syntax)
        nested_pattern = r'::(\w+)\s+(.*?)\s+::/\1'
        if re.search(nested_pattern, content, re.DOTALL):
            debug_print(f"Found nested blocks in {outer_lang} content")
            # This is a nested structure - process it as one block
            processed_content, nested_found = self.process_nested_blocks(content, outer_lang)
            debug_print(f"Processed content result:\n{processed_content}")
            return [{
                'type': 'outer',
                'lang': outer_lang,
                'code': processed_content,
                'is_nested': nested_found,
                'original_code': content
            }]
        
        # No nested blocks found - check for standalone blocks
        blocks = []
        current_pos = 0
        standalone_pattern = r'::(\w+)\s*(.*?)\s*::/\1'
        
        while current_pos < len(content):
            # Look for next standalone block
            standalone_match = re.search(standalone_pattern, content[current_pos:], re.DOTALL)
            
            if standalone_match:
                # Found a standalone block
                match_start = current_pos + standalone_match.start()
                match_end = current_pos + standalone_match.end()
                
                # Add any outer language content before this block
                before_content = content[current_pos:match_start].strip()
                if before_content:
                    blocks.append({
                        'type': 'outer',
                        'lang': outer_lang,
                        'code': before_content,
                        'is_nested': False
                    })
                
                # Add the standalone block
                block_lang = standalone_match.group(1)
                block_code = standalone_match.group(2).strip()
                blocks.append({
                    'type': 'standalone',
                    'lang': block_lang,
                    'code': block_code,
                    'is_nested': False
                })
                
                current_pos = match_end
            else:
                # No more standalone blocks - add remaining content as outer block
                remaining_content = content[current_pos:].strip()
                if remaining_content:
                    blocks.append({
                        'type': 'outer',
                        'lang': outer_lang,
                        'code': remaining_content,
                        'is_nested': False
                    })
                break
        
        return blocks
    
    def process_nested_blocks(self, content: str, outer_lang: str) -> Tuple[str, bool]:
        """Process nested blocks within outer language content with cross-language conversion"""
        
        nested_pattern = r'::(\w+)\s+(.*?)\s+::/\1'
        nested_blocks = list(re.finditer(nested_pattern, content, re.DOTALL))
        
        if not nested_blocks:
            return content, False
        
        debug_print(f"Found {len(nested_blocks)} nested blocks in {outer_lang}")
        
        # Process nested blocks in reverse order to maintain string positions
        processed_content = content
        for match in reversed(nested_blocks):
            nested_lang = match.group(1)
            nested_code = match.group(2).strip()
            
            debug_print(f"🔄 Processing nested {nested_lang} block: {nested_code}")
            
            # Convert nested code to outer language syntax
            converted_code = self.convert_nested_to_outer(nested_code, nested_lang, outer_lang)
            
            debug_print(f"🔄 Converted to {outer_lang}: {converted_code}")
            
            # Replace the nested block with converted code
            start_pos = match.start()
            end_pos = match.end()
            processed_content = processed_content[:start_pos] + converted_code + processed_content[end_pos:]
        
        return processed_content, True
    
    def convert_nested_to_outer(self, nested_code: str, nested_lang: str, outer_lang: str) -> str:
        """Convert nested language code to outer language syntax"""
        
        if outer_lang == 'c':
            if nested_lang == 'py':
                # Handle Python code - can have multiple statements separated by semicolons
                statements = [stmt.strip() for stmt in nested_code.split(';') if stmt.strip()]
                c_statements = []
                
                for stmt in statements:
                    # Handle Python print statements
                    if 'print(' in stmt:
                        print_match = re.search(r'print\s*\(\s*([^)]+)\s*\)', stmt)
                        if print_match:
                            print_args = print_match.group(1)
                            
                            # Handle multiple arguments separated by commas
                            if ',' in print_args:
                                args = [arg.strip() for arg in print_args.split(',')]
                                printf_parts = []
                                for arg in args:
                                    if arg.startswith('"') and arg.endswith('"'):
                                        # String literal
                                        printf_parts.append(f'printf({arg}); printf(" ");')
                                    else:
                                        # Variable - assume integer for now
                                        printf_parts.append(f'printf("%d ", {arg});')
                                c_statements.append(' '.join(printf_parts) + 'printf("\\n");')
                            else:
                                # Single argument
                                if print_args.startswith('"') and print_args.endswith('"'):
                                    c_statements.append(f'printf({print_args}); printf("\\n");')
                                else:
                                    c_statements.append(f'printf("%d\\n", {print_args});')
                    
                    # Handle Python list operations (commented out for C)
                    elif '.append(' in stmt:
                        c_statements.append(f'/* Python list operation: {stmt} */')
                    
                    # Handle other statements
                    else:
                        c_statements.append(f'/* Python: {stmt} */')
                
                return ' '.join(c_statements)
                
            elif nested_lang == 'java':
                # Convert Java to C
                if 'System.out.println(' in nested_code or 'System.out.print(' in nested_code:
                    java_match = re.search(r'System\.out\.print(?:ln)?\s*\(\s*([^)]+)\s*\)', nested_code)
                    if java_match:
                        print_arg = java_match.group(1).strip()
                        
                        # Handle Java string concatenation
                        if '+' in print_arg:
                            # Simple handling of "string " + variable
                            parts = [part.strip() for part in print_arg.split('+')]
                            printf_format = ""
                            printf_args = []
                            
                            for part in parts:
                                if part.startswith('"') and part.endswith('"'):
                                    printf_format += part[1:-1]  # Remove quotes
                                else:
                                    printf_format += "%d"
                                    printf_args.append(part)
                            
                            if printf_args:
                                result = f'printf("{printf_format}", {", ".join(printf_args)});'
                            else:
                                result = f'printf("{printf_format}");'
                        else:
                            # Simple argument
                            if print_arg.startswith('"') and print_arg.endswith('"'):
                                result = f'printf({print_arg});'
                            else:
                                result = f'printf("%d", {print_arg});'
                        
                        # Add newline for println
                        if 'println' in nested_code:
                            result += ' printf("\\n");'
                        
                        return result
                
                return f'/* Java code: {nested_code} */'
        
        # Default: return as comment if no conversion available
        return f'/* {nested_lang} code: {nested_code} */'
    
    def parse_sequential_blocks(self, code_str: str) -> List[Dict]:
        """Parse sequential language blocks"""
        blocks = []
        pattern = re.compile(r'::(\w+)\s*(.*?)\s*::/\1', re.DOTALL)
        
        for match in pattern.finditer(code_str):
            lang = match.group(1).strip()
            code = textwrap.dedent(match.group(2)).strip()
            blocks.append({
                'type': 'sequential',
                'lang': lang,
                'code': code,
                'is_nested': False
            })
        
        return blocks

    def execute_blocks(self, blocks: List[Dict]) -> None:
        """Execute all blocks while maintaining shared state"""
        
        debug_print(f"Executing {len(blocks)} blocks with shared state")
        
        for i, block in enumerate(blocks):
            debug_print(f"\n=== BLOCK {i+1}/{len(blocks)}: {block['lang'].upper()} ===")
            debug_print(f"Block details - Type: {block['type']}, Is nested: {block.get('is_nested', False)}")
            
            if block['type'] == 'standalone':
                self.execute_standalone_block(block)
            elif block['type'] == 'outer':
                if block['is_nested']:
                    debug_print("Using execute_outer_with_nested method")
                    self.execute_outer_with_nested(block)
                else:
                    debug_print("Using execute_standalone_block method")
                    self.execute_standalone_block(block)
            elif block['type'] == 'sequential':
                self.execute_standalone_block(block)
    
    def execute_standalone_block(self, block: Dict) -> None:
        """Execute a standalone language block"""
        lang = block['lang']
        code = block['code']
        
        debug_print(f"Executing standalone {lang} block")
        debug_print(f"Block type: {block.get('type', 'unknown')}, Is nested: {block.get('is_nested', False)}")
        
        # For nested blocks, make sure we use the processed code
        if block.get('is_nested') and 'original_code' in block:
            debug_print(f"Using processed code instead of original for nested block")
            code = block['code']  # This should already be the processed version
        
        # Get variables this block references
        referenced_vars = self.extract_variable_references(code, lang)
        available_vars = {k: v for k, v in self.global_state.items() 
                         if k in referenced_vars and not k.startswith('__')}
        
        debug_print(f"Available variables: {list(available_vars.keys())}")
        
        # Inject variable declarations
        injected_code = self.inject_variable_declarations(lang, available_vars)
        
        # Detect variables this block will modify - use original code for this analysis
        original_code_for_analysis = block.get('original_code', code)
        modified_vars = self.extract_modified_variables(original_code_for_analysis, lang)
        
        # Filter out loop variables and other locally scoped variables
        if lang == 'c':
            # Remove variables declared in for loops (like 'i' in 'for(int i = 0; ...)')
            for_loop_vars = re.findall(r'for\s*\(\s*int\s+([a-zA-Z_][a-zA-Z0-9_]*)', original_code_for_analysis)
            modified_vars = modified_vars - set(for_loop_vars)
        
        # Add output capture for modified variables
        output_capture = self.inject_output_capture(lang, modified_vars, original_code_for_analysis)
        
        # Combine code
        full_code = injected_code + code + output_capture
        
        debug_print(f"Full {lang} code:\n{full_code}")
        
        try:
            # Execute in Docker
            output = execute_in_docker(lang, full_code, "{}")
            
            # Parse output for variable updates
            try:
                if output.strip():
                    # Try to extract JSON from the end of output
                    lines = output.strip().split('\n')
                    for line in reversed(lines):
                        line = line.strip()
                        if line.startswith('{') and line.endswith('}'):
                            try:
                                new_vars = json.loads(line)
                                self.global_state.update(new_vars)
                                debug_print(f"Updated global state: {new_vars}")
                                break
                            except json.JSONDecodeError:
                                continue
                    
                    # Show program output (everything except the JSON state)
                    program_output = []
                    for line in lines:
                        if not (line.strip().startswith('{') and line.strip().endswith('}') and '"' in line):
                            program_output.append(line)
                    
                    if program_output:
                        print('\n'.join(program_output))
                        
            except Exception as e:
                debug_print(f"Error parsing output: {e}")
                print(output)
                
        except Exception as e:
            print(f"Error executing {lang}: {e}")
    
    def execute_outer_with_nested(self, block: Dict) -> None:
        """Execute outer language block that contains nested blocks"""
        lang = block['lang']
        code = block['code']
        original_code = block.get('original_code', code)
        
        debug_print(f"Executing {lang} block with nested components")
        
        # First, execute any nested blocks and collect their outputs
        nested_outputs = {}
        
        # Find all nested block placeholders and execute them
        for key, nested_info in self.global_state.items():
            if key.startswith(f'__nested_{lang}_'):
                nested_lang = nested_info['lang']
                nested_code = nested_info['code']
                placeholder = nested_info['placeholder']
                
                debug_print(f"Executing nested {nested_lang} block: {nested_code}")
                
                # Execute nested block with current global state
                try:
                    referenced_vars = self.extract_variable_references(nested_code, nested_lang)
                    available_vars = {k: v for k, v in self.global_state.items() 
                                   if k in referenced_vars and not k.startswith('__')}
                    
                    injected_code = self.inject_variable_declarations(nested_lang, available_vars)
                    modified_vars = self.extract_modified_variables(nested_code, nested_lang)
                    output_capture = self.inject_output_capture(nested_lang, modified_vars, nested_code)
                    
                    full_nested_code = injected_code + nested_code + output_capture
                    
                    nested_output = execute_in_docker(nested_lang, full_nested_code, "{}")
                    
                    # Parse nested output for state updates
                    if nested_output.strip():
                        lines = nested_output.strip().split('\n')
                        for line in reversed(lines):
                            line = line.strip()
                            if line.startswith('{') and line.endswith('}'):
                                try:
                                    new_vars = json.loads(line)
                                    self.global_state.update(new_vars)
                                    debug_print(f"Nested block updated state: {new_vars}")
                                    break
                                except json.JSONDecodeError:
                                    continue
                        
                        # Collect program output from nested block
                        program_output = []
                        for line in lines:
                            if not (line.strip().startswith('{') and line.strip().endswith('}') and '"' in line):
                                program_output.append(line)
                        
                        nested_outputs[placeholder] = '\n'.join(program_output)
                    
                except Exception as e:
                    debug_print(f"Error executing nested {nested_lang}: {e}")
                    nested_outputs[placeholder] = f"/* Error: {e} */"
        
        # Now execute the outer block
        # Replace placeholders with actual nested outputs if needed
        final_code = code
        for placeholder, output in nested_outputs.items():
            if placeholder in final_code and output:
                print(output)  # Print nested block output
        
        # Execute outer block normally with processed code
        self.execute_standalone_block({
            'lang': lang,
            'code': code,  # Use processed code, not original_code
            'type': 'outer',
            'is_nested': True,
            'original_code': original_code
        })

    def extract_variable_references(self, code: str, lang: str) -> set:
        """Extract variable names referenced in code"""
        references = set()
        
        # Simple pattern matching for variable names
        var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        # Language-specific exclusions
        exclusions = {
            'c': {'int', 'char', 'float', 'double', 'printf', 'for', 'if', 'else', 'return', 'sizeof', 'main', 'void'},
            'py': {'import', 'def', 'class', 'if', 'else', 'for', 'while', 'print', 'len', 'max', 'min', 'sum', 'str', 'int', 'float', 'list', 'dict', 'True', 'False', 'None'},
            'java': {'int', 'float', 'double', 'boolean', 'String', 'System', 'out', 'println', 'print', 'class', 'public', 'static', 'void', 'length', 'if', 'else', 'for', 'while', 'true', 'false'}
        }
        
        for match in re.finditer(var_pattern, code):
            var_name = match.group(1)
            if var_name not in exclusions.get(lang, set()):
                references.add(var_name)
        
        return references
    
    def extract_modified_variables(self, code: str, lang: str) -> set:
        """Extract variables that are modified in code"""
        modified = set()
        
        if lang == 'c':
            # C variable declarations and assignments
            for pattern in [
                r'(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*\]\s*=\s*\{',  # Arrays
                r'(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=',  # Regular variables
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*='  # Assignments
            ]:
                for match in re.finditer(pattern, code):
                    if len(match.groups()) == 2:
                        modified.add(match.group(2))
                    else:
                        modified.add(match.group(1))
        
        elif lang == 'py':
            # Python assignments
            for match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', code):
                var_name = match.group(1)
                if not re.search(r'import\s+.*' + re.escape(var_name), code):
                    modified.add(var_name)
            
            # Python method calls that modify objects
            for match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\.\s*(append|extend|remove|pop|clear)\s*\(', code):
                modified.add(match.group(1))
        
        elif lang == 'java':
            # Java variable declarations and assignments
            for pattern in [
                r'(int|float|double|boolean|String)\[\]\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=',
                r'(int|float|double|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=',
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*='
            ]:
                for match in re.finditer(pattern, code):
                    if len(match.groups()) == 2:
                        modified.add(match.group(2))
                    else:
                        modified.add(match.group(1))
        
        return modified
    
    def inject_variable_declarations(self, lang: str, variables: dict) -> str:
        """Inject variable declarations for each language"""
        if not variables:
            return ""
        
        declarations = []
        
        if lang == 'c':
            for var_name, value in variables.items():
                if isinstance(value, list):
                    if all(isinstance(x, int) for x in value):
                        arr_str = ", ".join(map(str, value))
                        declarations.append(f"int {var_name}[] = {{{arr_str}}};")
                        declarations.append(f"int {var_name}_size = {len(value)};")
                elif isinstance(value, int):
                    declarations.append(f"int {var_name} = {value};")
                elif isinstance(value, float):
                    declarations.append(f"float {var_name} = {value}f;")
                elif isinstance(value, str):
                    declarations.append(f'char {var_name}[] = "{value}";')
        
        elif lang == 'py':
            for var_name, value in variables.items():
                declarations.append(f"{var_name} = {repr(value)}")
        
        elif lang == 'java':
            for var_name, value in variables.items():
                if isinstance(value, list):
                    if all(isinstance(x, int) for x in value):
                        arr_str = ", ".join(map(str, value))
                        declarations.append(f"int[] {var_name} = {{{arr_str}}};")
                elif isinstance(value, int):
                    declarations.append(f"int {var_name} = {value};")
                elif isinstance(value, float):
                    declarations.append(f"float {var_name} = {value}f;")
                elif isinstance(value, bool):
                    declarations.append(f"boolean {var_name} = {'true' if value else 'false'};")
                elif isinstance(value, str):
                    declarations.append(f'String {var_name} = "{value}";')
        
        return "\n".join(declarations) + "\n" if declarations else ""
    
    def inject_output_capture(self, lang: str, variables: set, code: str = "") -> str:
        """Inject code to capture variable states as JSON"""
        if not variables:
            return ""
        
        if lang == 'py':
            var_list = list(variables)
            return f"""
import json
result_dict = {{}}
{chr(10).join([f'if "{var}" in locals(): result_dict["{var}"] = {var}' for var in var_list])}
print(json.dumps(result_dict))"""
        
        elif lang == 'java':
            # Java JSON output (simplified)
            var_list = list(variables)
            if var_list:
                java_json = ['System.out.print("{");']
                for i, var_name in enumerate(var_list):
                    if i > 0:
                        java_json.append('System.out.print(", ");')
                    java_json.append(f'System.out.print("\\"{var_name}\\": " + {var_name});')
                java_json.append('System.out.print("}");')
                return "\n" + "\n".join(java_json)
        
        elif lang == 'c':
            # Enhanced C JSON output with array handling
            var_list = list(variables)
            if var_list:
                c_json = ['printf("{");']
                for i, var_name in enumerate(var_list):
                    if i > 0:
                        c_json.append('printf(", ");')
                    
                    # Check if it's an array declaration in the code
                    if re.search(rf'int\s+{var_name}\s*\[\s*\]\s*=\s*\{{', code):
                        # It's an array - output as JSON array
                        c_json.append(f'printf("\\"{var_name}\\": [");')
                        c_json.append(f'int {var_name}_size = sizeof({var_name}) / sizeof({var_name}[0]);')
                        c_json.append(f'for(int __i = 0; __i < {var_name}_size; __i++) {{')
                        c_json.append(f'    printf("%d", {var_name}[__i]);')
                        c_json.append(f'    if(__i < {var_name}_size - 1) printf(", ");')
                        c_json.append(f'}}')
                        c_json.append(f'printf("]");')
                    else:
                        # Regular variable
                        c_json.append(f'printf("\\"{var_name}\\": %d", {var_name});')
                
                c_json.append('printf("}");')
                return "\n" + "\n".join(c_json)
        
        return ""


def parse_code_to_tree(code_str: str) -> list:
    """Parse language blocks using SharedStateOrchestrator - Legacy compatibility function"""
    orchestrator = SharedStateOrchestrator()
    blocks = orchestrator.parse_mixed_structure(code_str)
    
    # Convert to legacy format for compatibility
    legacy_blocks = []
    for block in blocks:
        legacy_blocks.append({
            'lang': block['lang'],
            'code': block['code'],
            'is_nested': block.get('is_nested', False)
        })
    
    return legacy_blocks

# Legacy compatibility functions
def inject_variable_declarations(lang: str, variables: dict) -> str:
    """Automatically inject variable declarations based on language - Legacy function"""
    orchestrator = SharedStateOrchestrator()
    return orchestrator.inject_variable_declarations(lang, variables)

def inject_output_capture(lang: str, variables: dict, user_code: str = "") -> str:
    """Automatically inject code to capture and output variables as JSON - Legacy function"""
    orchestrator = SharedStateOrchestrator()
    # Convert dict to set for new interface
    var_set = set(variables.keys()) if isinstance(variables, dict) else variables
    return orchestrator.inject_output_capture(lang, var_set, user_code)

def execute_tree_generator(blocks: list, input_state: dict = None):
    """Execute sequential language blocks using SharedStateOrchestrator - Legacy compatibility function"""
    
    # Create orchestrator and set initial state
    orchestrator = SharedStateOrchestrator()
    if input_state:
        orchestrator.global_state.update(input_state)
    
    if DEBUG_MODE:
        yield "=" * 50
        yield "🔄 POLYGLOT EXECUTION PIPELINE STARTED (SharedStateOrchestrator)"
        yield "=" * 50
    
    debug_print(f"🔄 Starting pipeline with {len(blocks)} language blocks")
    debug_print(f"📊 Initial state: {orchestrator.global_state}")
    
    for i, block in enumerate(blocks):
        lang = block['lang']
        
        if DEBUG_MODE:
            yield f"\n🏗️ === BLOCK {i+1}/{len(blocks)}: {lang.upper()} ==="
        
        debug_print(f"\n🏗️ === BLOCK {i+1}/{len(blocks)}: {lang.upper()} ===")
        
        # Convert legacy block format to new format
        new_block = {
            'type': 'sequential',
            'lang': lang,
            'code': block['code'],
            'is_nested': block.get('is_nested', False)
        }
        
        try:
            # Execute block using orchestrator
            old_state = orchestrator.global_state.copy()
            orchestrator.execute_standalone_block(new_block)
            
            # Show what changed
            new_vars = {k: v for k, v in orchestrator.global_state.items() 
                       if k not in old_state and not k.startswith('__')}
            modified_vars = {k: v for k, v in orchestrator.global_state.items() 
                           if k in old_state and old_state[k] != v and not k.startswith('__')}
            
            if DEBUG_MODE:
                if new_vars:
                    yield f"➕ Created: {list(new_vars.keys())} = {list(new_vars.values())}"
                if modified_vars:
                    yield f"🔄 Modified: {list(modified_vars.keys())} = {list(modified_vars.values())}"
                    
                # Show what will be passed to next block
                if i + 1 < len(blocks):
                    next_lang = blocks[i + 1]['lang']
                    next_code = blocks[i + 1]['code']
                    next_referenced = orchestrator.extract_variable_references(next_code, next_lang)
                    vars_to_pass = {k: v for k, v in orchestrator.global_state.items() 
                                  if k in next_referenced and not k.startswith('__')}
                    if vars_to_pass:
                        yield f"📤 Passing to {next_lang.upper()}: {list(vars_to_pass.keys())}"
                    else:
                        yield f"📤 Nothing to pass to {next_lang.upper()}"
                        
        except Exception as e:
            debug_print(f"❌ Error in {lang} block: {e}")
            yield f"Error in {lang}: {e}"
            break
    
    debug_print(f"🏁 Pipeline completed! Final state: {orchestrator.global_state}")
    
    # Only show summary when debug mode is enabled
    if DEBUG_MODE:
        yield "\n" + "=" * 50
        yield "🏁 PIPELINE EXECUTION SUMMARY"
        yield "=" * 50
        final_vars = {k: v for k, v in orchestrator.global_state.items() if not k.startswith('__')}
        if final_vars:
            yield f"📊 Final variable state: {final_vars}"
        else:
            yield "📊 No variables persisted across blocks"
        yield "✅ Pipeline completed successfully"


# Main execution function
def execute_polyglot_code(code_str: str) -> None:
    """Execute polyglot code with shared state management"""
    orchestrator = SharedStateOrchestrator()
    
    debug_print("Starting polyglot execution with shared state")
    
    # Parse the mixed structure
    blocks = orchestrator.parse_mixed_structure(code_str)
    
    debug_print(f"Parsed {len(blocks)} execution blocks:")
    for i, block in enumerate(blocks):
        debug_print(f"  Block {i+1}: {block['type']} {block['lang']} {'(nested)' if block.get('is_nested') else ''}")
    
    # Execute all blocks
    orchestrator.execute_blocks(blocks)

# Legacy compatibility functions for backward compatibility
def extract_variable_references(code: str, lang: str) -> set:
    """Extract variable names that are referenced (read) in the code - Legacy function"""
    orchestrator = SharedStateOrchestrator()
    return orchestrator.extract_variable_references(code, lang)

def extract_modified_variables(code: str, lang: str) -> set:
    """Extract variable names that are modified (written) in the code - Legacy function"""
    orchestrator = SharedStateOrchestrator()
    return orchestrator.extract_modified_variables(code, lang)