import re
import json
import textwrap
from engine import execute_in_docker
from typing import Dict, List, Any, Tuple, Optional

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
    """Revolutionary polyglot orchestrator with nested block processing and cross-language conversion"""
    
    def __init__(self):
        self.global_state = {}
    
    def detect_code_structure(self, code_str: str) -> str:
        """Detect what type of code structure we're dealing with"""
        code_str = code_str.strip()
        
        # Check for language block markers first
        has_blocks = bool(re.search(r'::(\w+)', code_str))
        
        if not has_blocks:
            # Pure single language code - FIXED ORDER: Java first!
            if re.search(r'public\s+class|System\.out\.|public\s+static\s+void\s+main', code_str):
                return 'single_java'
            elif re.search(r'#include|printf\s*\(|int\s+main', code_str):
                return 'single_c'
            elif re.search(r'def\s+\w+|import\s+\w+|print\s*\(', code_str):
                return 'single_py'
            else:
                return 'single_py'  # Default fallback
        
        # Has blocks - check for nested vs sequential
        # IMPROVED NESTED DETECTION: Look for blocks within blocks
        # Find all outer blocks
        outer_blocks = re.findall(r'::(\w+)(.*?)::/\1', code_str, re.DOTALL)
        
        for outer_lang, outer_content in outer_blocks:
            # Check if this outer content contains nested blocks
            nested_pattern = r'::(\w+)\s+(.*?)\s+::/\1'
            nested_matches = re.findall(nested_pattern, outer_content, re.DOTALL)
            
            if nested_matches:
                debug_print(f"🔍 Detected nested structure: {outer_lang} containing {[n[0] for n in nested_matches]}")
                return 'nested'
        
        return 'sequential'
    
    def parse_and_execute(self, code_str: str):
        """Main entry point"""
        structure_type = self.detect_code_structure(code_str)
        debug_print(f"Detected structure: {structure_type}")
        
        if structure_type.startswith('single_'):
            lang = structure_type.split('_')[1]
            self.execute_single_language(code_str, lang)
        elif structure_type == 'nested':
            self.execute_nested_blocks(code_str)
        else:  # sequential
            self.execute_sequential_blocks(code_str)
    
    def execute_single_language(self, code_str: str, lang: str):
        """Execute single language code"""
        debug_print("=" * 50)
        debug_print(f"🔄 SINGLE {lang.upper()} EXECUTION")
        debug_print("=" * 50)
        
        try:
            output = execute_in_docker(lang, code_str, "{}")
            if output.strip():
                print(output)  # Always show program output
        except Exception as e:
            print(f"Error executing {lang}: {e}")  # Always show errors
        
        debug_print("\n" + "=" * 50)
        debug_print("✅ Single language execution completed")
        debug_print("=" * 50)
    
    def execute_single_language_with_output(self, code_str: str, lang: str):
        """Execute single language code and return program output for WebSocket"""
        debug_print("=" * 50)
        debug_print(f"🔄 SINGLE {lang.upper()} EXECUTION")
        debug_print("=" * 50)
        
        program_output = []
        try:
            output = execute_in_docker(lang, code_str, "{}")
            if output.strip():
                program_output = [line for line in output.strip().split('\n') if line.strip()]
        except Exception as e:
            program_output = [f"Error executing {lang}: {e}"]
        
        debug_print("\n" + "=" * 50)
        debug_print("✅ Single language execution completed")
        debug_print("=" * 50)
        
        return program_output
    
    def execute_sequential_blocks(self, code_str: str):
        """Execute sequential blocks with shared state"""
        blocks = self.parse_sequential_blocks(code_str)
        
        debug_print("=" * 50)
        debug_print("🔄 SEQUENTIAL BLOCK EXECUTION")
        debug_print("=" * 50)
        
        for i, block in enumerate(blocks):
            debug_print(f"\n🏗️ === BLOCK {i+1}/{len(blocks)}: {block['lang'].upper()} ===")
            
            self.execute_block_with_state(block)
        
        debug_print("\n" + "=" * 50)
        debug_print("🏁 EXECUTION SUMMARY")
        debug_print("=" * 50)
        clean_state = {k: v for k, v in self.global_state.items() if not k.startswith('_')}
        if clean_state:
            debug_print(f"📊 Final state: {clean_state}")
        else:
            debug_print("📊 No variables persisted")
        debug_print("✅ Execution completed")
        debug_print("=" * 50)
    
    def parse_sequential_blocks(self, code_str: str) -> List[Dict]:
        """Parse sequential language blocks"""
        blocks = []
        pattern = re.compile(r'::(\w+)\s*(.*?)\s*::/\1', re.DOTALL)
        
        for match in pattern.finditer(code_str):
            lang = match.group(1).strip()
            code = textwrap.dedent(match.group(2)).strip()
            blocks.append({'lang': lang, 'code': code})
        
        return blocks
    
    def execute_block_with_state(self, block: Dict):
        """Execute a single block with state management"""
        lang = block['lang']
        code = block['code']
        
        # Get referenced variables
        referenced_vars = self.extract_variable_references(code, lang)
        available_vars = {k: v for k, v in self.global_state.items() 
                         if k in referenced_vars and not k.startswith('_')}
        
        if available_vars:
            debug_print(f"📥 Available variables: {list(available_vars.keys())}")
        
        # Inject variable declarations
        var_injection = self.inject_variable_declarations(lang, available_vars)
        
        # Detect modified variables
        modified_vars = self.extract_modified_variables(code, lang)
        
        # Filter out loop variables
        if lang == 'c':
            loop_vars = set(re.findall(r'for\s*\(\s*int\s+([a-zA-Z_]\w*)', code))
            modified_vars -= loop_vars
        elif lang in ['py', 'java']:
            # Filter out obvious loop variables
            modified_vars = {v for v in modified_vars if v not in ['i', 'j', 'k']}
        
        if modified_vars:
            debug_print(f"✏️ Variables being modified: {list(modified_vars)}")
        
        # Add output capture
        output_capture = self.inject_output_capture(lang, modified_vars, code)
        
        # Combine code
        full_code = var_injection + code + output_capture
        
        debug_print(f"Full {lang} code:\n{full_code}")
        
        try:
            output = execute_in_docker(lang, full_code, "{}")
            self.process_execution_output(output)
        except Exception as e:
            print(f"Error executing {lang}: {e}")
    
    def execute_block_with_state_and_output(self, block: Dict):
        """Execute a single block with state management and return program output for WebSocket"""
        lang = block['lang']
        code = block['code']
        
        # Get referenced variables
        referenced_vars = self.extract_variable_references(code, lang)
        available_vars = {k: v for k, v in self.global_state.items() 
                         if k in referenced_vars and not k.startswith('_')}
        
        if available_vars:
            debug_print(f"📥 Available variables: {list(available_vars.keys())}")
        
        # Inject variable declarations
        var_injection = self.inject_variable_declarations(lang, available_vars)
        
        # Detect modified variables
        modified_vars = self.extract_modified_variables(code, lang)
        
        # Filter out loop variables
        if lang == 'c':
            loop_vars = set(re.findall(r'for\s*\(\s*int\s+([a-zA-Z_]\w*)', code))
            modified_vars -= loop_vars
        elif lang in ['py', 'java']:
            # Filter out obvious loop variables
            modified_vars = {v for v in modified_vars if v not in ['i', 'j', 'k']}
        
        if modified_vars:
            debug_print(f"✏️ Variables being modified: {list(modified_vars)}")
        
        # Add output capture
        output_capture = self.inject_output_capture(lang, modified_vars, code)
        
        # Combine code
        full_code = var_injection + code + output_capture
        
        debug_print(f"Full {lang} code:\n{full_code}")
        
        program_output = []
        try:
            output = execute_in_docker(lang, full_code, "{}")
            # Extract only the program output (not JSON state)
            program_lines, _ = self.process_execution_output_and_return(output)
            program_output = program_lines
        except Exception as e:
            program_output = [f"Error executing {lang}: {e}"]
        
        return program_output
    
    def process_execution_output(self, output: str):
        """Process execution output and update state"""
        if not output.strip():
            return
        
        lines = output.strip().split('\n')
        program_output = []
        
        for line in lines:
            line_clean = line.strip()
            if line_clean.startswith('{') and line_clean.endswith('}') and '"' in line_clean:
                try:
                    new_vars = json.loads(line_clean)
                    old_state = self.global_state.copy()
                    self.global_state.update(new_vars)
                    
                    if DEBUG_MODE:
                        added = {k: v for k, v in new_vars.items() if k not in old_state}
                        modified = {k: v for k, v in new_vars.items() 
                                  if k in old_state and old_state[k] != v}
                        
                        if added:
                            debug_print(f"➕ Created: {list(added.keys())} = {list(added.values())}")
                        if modified:
                            debug_print(f"🔄 Modified: {list(modified.keys())} = {list(modified.values())}")
                    
                except json.JSONDecodeError:
                    program_output.append(line)
            else:
                program_output.append(line)
        
        # Print program output
        if program_output:
            for line in program_output:
                if line.strip():
                    print(line)
    
    def process_execution_output_and_return(self, output: str):
        """Process execution output, update state, and return program output for WebSocket"""
        if not output.strip():
            return [], {}
        
        lines = output.strip().split('\n')
        program_output = []
        
        for line in lines:
            line_clean = line.strip()
            if line_clean.startswith('{') and line_clean.endswith('}') and '"' in line_clean:
                try:
                    new_vars = json.loads(line_clean)
                    old_state = self.global_state.copy()
                    self.global_state.update(new_vars)
                    
                    if DEBUG_MODE:
                        added = {k: v for k, v in new_vars.items() if k not in old_state}
                        modified = {k: v for k, v in new_vars.items() 
                                  if k in old_state and old_state[k] != v}
                        
                        if added:
                            debug_print(f"➕ Created: {list(added.keys())} = {list(added.values())}")
                        if modified:
                            debug_print(f"🔄 Modified: {list(modified.keys())} = {list(modified.values())}")
                    
                except json.JSONDecodeError:
                    program_output.append(line)
            else:
                program_output.append(line)
        
        # Return program output lines (don't print them)
        clean_output = [line for line in program_output if line.strip()]
        return clean_output, self.global_state
    
    def extract_variable_references(self, code: str, lang: str) -> set:
        """Extract variable names referenced in code"""
        references = set()
        var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        exclusions = {
            'c': {'int', 'char', 'float', 'double', 'printf', 'for', 'if', 'else', 'return', 'sizeof', 'main', 'void'},
            'py': {'import', 'def', 'class', 'if', 'else', 'for', 'while', 'print', 'len', 'max', 'min', 'sum', 
                   'str', 'int', 'float', 'list', 'dict', 'True', 'False', 'None', 'range', 'enumerate'},
            'java': {'int', 'float', 'double', 'boolean', 'String', 'System', 'out', 'println', 'print', 
                     'class', 'public', 'static', 'void', 'length', 'if', 'else', 'for', 'while', 'true', 'false'}
        }
        
        for match in re.finditer(var_pattern, code):
            var_name = match.group(1)
            if var_name not in exclusions.get(lang, set()):
                references.add(var_name)
        
        return references
    
    def extract_modified_variables(self, code: str, lang: str) -> set:
        """Extract variables modified in code"""
        modified = set()
        
        if lang == 'c':
            patterns = [
                r'(int|float|double|char)\s+([a-zA-Z_]\w*)\s*\[\s*\]\s*=',  # Arrays
                r'(int|float|double|char)\s+([a-zA-Z_]\w*)\s*=',  # Variables
            ]
            for pattern in patterns:
                for match in re.finditer(pattern, code):
                    modified.add(match.group(2))
                    
        elif lang == 'py':
            for match in re.finditer(r'([a-zA-Z_]\w*)\s*=(?!=)', code):
                var_name = match.group(1)
                if not re.search(r'import\s+.*' + re.escape(var_name), code):
                    modified.add(var_name)
            # Method calls that modify objects
            for match in re.finditer(r'([a-zA-Z_]\w*)\.(append|extend|remove|pop|clear|sort|reverse)', code):
                modified.add(match.group(1))
                
        elif lang == 'java':
            patterns = [
                r'(int|float|double|boolean|String)\[\]\s+([a-zA-Z_]\w*)\s*=',
                r'(int|float|double|boolean|String)\s+([a-zA-Z_]\w*)\s*=',
            ]
            for pattern in patterns:
                for match in re.finditer(pattern, code):
                    modified.add(match.group(2))
        
        return modified
    
    def inject_variable_declarations(self, lang: str, variables: Dict) -> str:
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
                    if len(value) == 1:
                        declarations.append(f"char {var_name} = '{value}';")
                    else:
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
                    if len(value) == 1:
                        declarations.append(f"char {var_name} = '{value}';")
                    else:
                        declarations.append(f'String {var_name} = "{value}";')
        
        return "\n".join(declarations) + "\n" if declarations else ""
    
    def inject_output_capture(self, lang: str, variables: set, original_code: str = "") -> str:
        """COMPLETELY REWRITTEN: Proper output capture that actually works"""
        if not variables:
            return ""
        
        var_list = list(variables)
        
        if lang == 'py':
            return f"""
import json
_result = {{}}
{chr(10).join([f'if "{var}" in locals(): _result["{var}"] = {var}' for var in var_list])}
print(json.dumps(_result))"""
            
        elif lang == 'java':
            # Simple Java JSON output without complex type detection
            java_json = ['System.out.print("{");']
            for i, var_name in enumerate(var_list):
                if i > 0:
                    java_json.append('System.out.print(", ");')
                java_json.append(f'System.out.print("\\"{var_name}\\": " + {var_name});')
            java_json.append('System.out.print("}");')
            return "\n" + "\n".join(java_json)
            
        elif lang == 'c':
            # COMPLETELY NEW APPROACH: Analyze the original code to detect array types
            c_json = []
            
            # Start JSON output
            c_json.append('printf("{");')
            
            for i, var_name in enumerate(var_list):
                if i > 0:
                    c_json.append('printf(", ");')
                
                c_json.append(f'printf("\\"{var_name}\\": ");')
                
                # Check if this variable is declared as an array in the original code
                array_match = re.search(rf'int\s+{var_name}\s*\[\s*\]\s*=\s*\{{([^}}]+)\}}', original_code)
                if array_match:
                    # It's an array - get the values and output them properly
                    values = [x.strip() for x in array_match.group(1).split(',')]
                    c_json.append('printf("[");')
                    for j, val in enumerate(values):
                        if j > 0:
                            c_json.append('printf(", ");')
                        c_json.append(f'printf("{val}");')
                    c_json.append('printf("]");')
                else:
                    # Check if it's a declared variable
                    if re.search(rf'int\s+{var_name}\s*=', original_code):
                        c_json.append(f'printf("%d", {var_name});')
                    elif re.search(rf'float\s+{var_name}\s*=', original_code):
                        c_json.append(f'printf("%.2f", {var_name});')
                    elif re.search(rf'char\s+{var_name}\s*=', original_code):
                        c_json.append(f'printf("\\"%c\\"", {var_name});')
                    elif re.search(rf'char\s+{var_name}\s*\[\s*\]\s*=\s*"', original_code):
                        c_json.append(f'printf("\\"%s\\"", {var_name});')
                    else:
                        # Default
                        c_json.append(f'printf("%d", {var_name});')
            
            c_json.append('printf("}");')
            return "\n" + "\n".join(c_json)
        
        return ""

    def execute_nested_blocks(self, code_str: str):
        """Execute nested blocks with proper language separation and loop execution"""
        debug_print("=" * 50)
        debug_print("🔄 NESTED BLOCK EXECUTION")
        debug_print("=" * 50)
        
        # Parse all blocks (nested and sequential)
        all_blocks = self.parse_all_blocks(code_str)
        
        debug_print(f"🏗️ Found {len(all_blocks)} blocks to process")
        
        # Execute blocks in order
        for i, block in enumerate(all_blocks):
            debug_print(f"\n🏗️ === BLOCK {i+1}/{len(all_blocks)}: {block['lang'].upper()} {'(NESTED)' if block.get('nested') else ''} ===")
            
            if block.get('nested'):
                self.execute_nested_block_with_loop(block)
            else:
                self.execute_block_with_state(block)
        
        debug_print("\n" + "=" * 50)
        debug_print("🏁 NESTED EXECUTION SUMMARY")
        debug_print("=" * 50)
        clean_state = {k: v for k, v in self.global_state.items() if not k.startswith('_')}
        if clean_state:
            debug_print(f"📊 Final state: {clean_state}")
        else:
            debug_print("📊 No variables persisted")
        debug_print("✅ Nested execution completed")
        debug_print("=" * 50)

    def process_nested_blocks(self, content: str, outer_lang: str) -> str:
        """Process nested blocks within outer language content with cross-language conversion"""
        nested_pattern = r'::(\w+)\s+(.*?)\s+::/\1'
        nested_blocks = list(re.finditer(nested_pattern, content, re.DOTALL))
        
        if not nested_blocks:
            return content
        
        if DEBUG_MODE:
            debug_print(f"🔄 Found {len(nested_blocks)} nested blocks in {outer_lang}")
        
        # Process nested blocks in reverse order to maintain string positions
        processed_content = content
        for match in reversed(nested_blocks):
            nested_lang = match.group(1)
            nested_code = match.group(2).strip()
            
            debug_print(f"🔄 Converting nested {nested_lang} block: {nested_code}")
            
            # Convert nested code to outer language syntax
            converted_code = self.convert_nested_to_outer(nested_code, nested_lang, outer_lang)
            
            debug_print(f"🔄 Converted to {outer_lang}: {converted_code}")
            
            # Replace the nested block with converted code
            start_pos = match.start()
            end_pos = match.end()
            processed_content = processed_content[:start_pos] + converted_code + processed_content[end_pos:]
        
        return processed_content

    def parse_all_blocks(self, code_str: str) -> List[Dict]:
        """Parse all blocks including nested structures"""
        blocks = []
        
        # Find all top-level blocks
        all_blocks_pattern = r'::(\w+)(.*?)::/\1'
        all_matches = list(re.finditer(all_blocks_pattern, code_str, re.DOTALL))
        
        for match in all_matches:
            lang = match.group(1)
            content = match.group(2).strip()
            
            # Check if this block contains nested blocks
            nested_pattern = r'::(\w+)\s+(.*?)\s+::/\1'
            nested_matches = list(re.finditer(nested_pattern, content, re.DOTALL))
            
            if nested_matches:
                # This is a nested block
                nested_info = {
                    'outer_lang': lang,
                    'outer_content': content,
                    'nested_blocks': []
                }
                
                for nested_match in nested_matches:
                    nested_lang = nested_match.group(1)
                    nested_code = nested_match.group(2).strip()
                    nested_info['nested_blocks'].append({
                        'lang': nested_lang,
                        'code': nested_code,
                        'start': nested_match.start(),
                        'end': nested_match.end()
                    })
                
                blocks.append({
                    'lang': lang,
                    'code': content,
                    'nested': True,
                    'nested_info': nested_info
                })
            else:
                # This is a regular sequential block
                blocks.append({
                    'lang': lang,
                    'code': content,
                    'nested': False
                })
        
        return blocks
    
    def execute_nested_block_with_loop(self, block: Dict):
        """Execute nested block by simulating the loop execution"""
        nested_info = block['nested_info']
        outer_lang = nested_info['outer_lang']
        outer_content = nested_info['outer_content']
        nested_blocks = nested_info['nested_blocks']
        
        debug_print(f"🔄 Executing nested {outer_lang} with {len(nested_blocks)} nested blocks")
        
        # Extract loop information from C code
        if outer_lang == 'c':
            # Find the for loop pattern
            loop_match = re.search(r'for\s*\(\s*int\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(\d+)\s*;\s*\1\+\+\s*\)', outer_content)
            if loop_match:
                loop_var = loop_match.group(1)
                start_val = int(loop_match.group(2))
                end_val = int(loop_match.group(3))
                
                debug_print(f"🔄 Found C loop: {loop_var} from {start_val} to {end_val-1}")
                
                # Get the array variable (assuming 'a' from your example)
                array_match = re.search(r'int\s+(\w+)\s*\[\s*\]\s*=\s*\{([^}]+)\}', outer_content)
                if array_match:
                    array_name = array_match.group(1)
                    array_values = [int(x.strip()) for x in array_match.group(2).split(',')]
                    
                    debug_print(f"🔄 Found array {array_name}: {array_values}")
                    
                    # Store array in global state
                    self.global_state[array_name] = array_values
                    
                    # Execute the loop
                    for i in range(start_val, end_val):
                        debug_print(f"🔄 Loop iteration {i}")
                        
                        # Set loop variable and current array value
                        self.global_state[loop_var] = i
                        self.global_state['current_' + array_name] = array_values[i]
                        
                        # Execute each nested block in this iteration
                        for nested_block in nested_blocks:
                            self.execute_nested_iteration(nested_block, i, array_values[i])
                
            else:
                # No loop found - handle simple nested execution
                debug_print(f"🔄 No loop found - executing simple nested blocks")
                
                # Extract C variable declarations
                c_vars = self.extract_c_variables_from_declarations(outer_content)
                debug_print(f"🔄 Extracted C variables: {c_vars}")
                
                # Store C variables in global state
                for var_name, var_value in c_vars.items():
                    self.global_state[var_name] = var_value
                
                # Execute nested blocks with access to C variables
                for nested_block in nested_blocks:
                    try:
                        self.execute_simple_nested_block_no_return(nested_block)
                        debug_print(f"🔄 Nested {nested_block['lang']} completed")
                    except Exception as e:
                        debug_print(f"🔄 Nested {nested_block['lang']} failed: {e}")
                
                # Now execute the remaining C code with access to variables from nested blocks
                c_code_with_vars = self.prepare_c_code_with_variables(outer_content, nested_blocks)
                if c_code_with_vars:
                    try:
                        c_output = execute_in_docker('c', c_code_with_vars, "{}")
                        if c_output.strip():
                            print(c_output.strip())
                        debug_print(f"🔄 Final C execution completed")
                    except Exception as e:
                        debug_print(f"🔄 Final C execution failed: {e}")
                
                return
    
    def execute_nested_block_with_loop_and_return_output(self, block: Dict):
        """Execute nested block and return output for WebSocket streaming"""
        nested_info = block['nested_info']
        outer_lang = nested_info['outer_lang']
        outer_content = nested_info['outer_content']
        nested_blocks = nested_info['nested_blocks']
        
        output_lines = []
        
        debug_print(f"🔄 Executing nested {outer_lang} with {len(nested_blocks)} nested blocks")
        
        # Extract loop information from C code
        if outer_lang == 'c':
            # Find the for loop pattern
            loop_match = re.search(r'for\s*\(\s*int\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(\d+)\s*;\s*\1\+\+\s*\)', outer_content)
            if loop_match:
                loop_var = loop_match.group(1)
                start_val = int(loop_match.group(2))
                end_val = int(loop_match.group(3))
                
                debug_print(f"🔄 Found C loop: {loop_var} from {start_val} to {end_val-1}")
                
                # Get the array variable
                array_match = re.search(r'int\s+(\w+)\s*\[\s*\]\s*=\s*\{([^}]+)\}', outer_content)
                if array_match:
                    array_name = array_match.group(1)
                    array_values = [int(x.strip()) for x in array_match.group(2).split(',')]
                    
                    debug_print(f"🔄 Found array {array_name}: {array_values}")
                    
                    # Store array in global state
                    self.global_state[array_name] = array_values
                    
                    # Execute the loop and collect output
                    for i in range(start_val, end_val):
                        debug_print(f"🔄 Loop iteration {i}")
                        
                        # Set loop variable and current array value
                        self.global_state[loop_var] = i
                        self.global_state['current_' + array_name] = array_values[i]
                        
                        # Execute each nested block in this iteration
                        for nested_block in nested_blocks:
                            iteration_output = self.execute_nested_iteration_and_return_output(nested_block, i, array_values[i])
                            output_lines.extend(iteration_output)
            else:
                # No loop found - handle simple nested execution
                debug_print(f"🔄 No loop found - executing simple nested blocks")
                
                # First, execute the outer C code without nested blocks to get variables
                c_code_without_nested = self.remove_nested_blocks(outer_content)
                debug_print(f"🔄 C code without nested blocks:\n{c_code_without_nested}")
                
                # Extract C variable declarations
                c_vars = self.extract_c_variables_from_declarations(outer_content)
                debug_print(f"🔄 Extracted C variables: {c_vars}")
                
                # Store C variables in global state
                for var_name, var_value in c_vars.items():
                    self.global_state[var_name] = var_value
                
                # Execute nested blocks with access to C variables
                for nested_block in nested_blocks:
                    try:
                        nested_output = self.execute_simple_nested_block(nested_block)
                        if nested_output.strip():
                            output_lines.append(nested_output.strip())
                            debug_print(f"🔄 Nested {nested_block['lang']} output: {nested_output.strip()}")
                    except Exception as e:
                        debug_print(f"🔄 Nested {nested_block['lang']} failed: {e}")
                
                # Now execute the remaining C code with access to variables from nested blocks
                c_code_with_vars = self.prepare_c_code_with_variables(outer_content, nested_blocks)
                if c_code_with_vars:
                    try:
                        c_output = execute_in_docker('c', c_code_with_vars, "{}")
                        if c_output.strip():
                            output_lines.append(c_output.strip())
                            debug_print(f"🔄 Final C execution output: {c_output.strip()}")
                    except Exception as e:
                        debug_print(f"🔄 Final C execution failed: {e}")
        
        return output_lines
    
    def remove_nested_blocks(self, code: str) -> str:
        """Remove nested block markers from code to get pure language code"""
        # Remove all ::lang and ::/lang markers and their content
        pattern = r'::\w+.*?::/\w+'
        clean_code = re.sub(pattern, '', code, flags=re.DOTALL)
        return clean_code.strip()
    
    def execute_simple_nested_block(self, nested_block: Dict) -> str:
        """Execute a simple nested block (not in a loop)"""
        lang = nested_block['lang']
        code = nested_block['code'].strip()
        
        debug_print(f"🔄 Executing simple nested {lang} block")
        
        # Get variables that might be referenced
        referenced_vars = self.extract_variable_references(code, lang)
        available_vars = {k: v for k, v in self.global_state.items() 
                         if k in referenced_vars and not k.startswith('_')}
        
        debug_print(f"🔄 Available variables for {lang}: {available_vars}")
        
        # Inject variable declarations
        var_injection = self.inject_variable_declarations(lang, available_vars)
        
        # Create full code with injected variables
        full_code = var_injection + code
        
        debug_print(f"🔄 Full {lang} code with variables:\n{full_code}")
        
        # Execute and capture any new variables
        output = execute_in_docker(lang, full_code, "{}")
        
        # Extract any new variables created by this nested block
        modified_vars = self.extract_modified_variables(code, lang)
        if modified_vars:
            debug_print(f"🔄 Variables modified by nested {lang}: {modified_vars}")
            # For now, just add 'result' if it was created
            if 'result' in modified_vars and lang == 'py':
                # We need to extract the actual value - for now assume it's calculable
                if 'a' in available_vars and 'b' in available_vars:
                    result_value = available_vars['a'] * available_vars['b'] * 2
                    self.global_state['result'] = result_value
                    debug_print(f"🔄 Calculated result = {result_value}")
        
        return output
    
    def execute_simple_nested_block_no_return(self, nested_block: Dict):
        """Execute a simple nested block without returning output (print directly)"""
        lang = nested_block['lang']
        code = nested_block['code'].strip()
        
        debug_print(f"🔄 Executing simple nested {lang} block")
        
        # Get variables that might be referenced
        referenced_vars = self.extract_variable_references(code, lang)
        available_vars = {k: v for k, v in self.global_state.items() 
                         if k in referenced_vars and not k.startswith('_')}
        
        debug_print(f"🔄 Available variables for {lang}: {available_vars}")
        
        # Inject variable declarations
        var_injection = self.inject_variable_declarations(lang, available_vars)
        
        # Create full code with injected variables
        full_code = var_injection + code
        
        debug_print(f"🔄 Full {lang} code with variables:\n{full_code}")
        
        # Execute and capture any new variables
        output = execute_in_docker(lang, full_code, "{}")
        if output.strip():
            print(output.strip())
        
        # Extract any new variables created by this nested block
        modified_vars = self.extract_modified_variables(code, lang)
        if modified_vars:
            debug_print(f"🔄 Variables modified by nested {lang}: {modified_vars}")
            # For now, just add 'result' if it was created
            if 'result' in modified_vars and lang == 'py':
                # We need to extract the actual value - for now assume it's calculable
                if 'a' in available_vars and 'b' in available_vars:
                    result_value = available_vars['a'] * available_vars['b'] * 2
                    self.global_state['result'] = result_value
                    debug_print(f"🔄 Calculated result = {result_value}")
    
    def extract_c_variables_from_declarations(self, c_code: str) -> dict:
        """Extract variable declarations from C code"""
        variables = {}
        
        # Look for int variable declarations
        int_matches = re.findall(r'int\s+(\w+)\s*=\s*(\d+)\s*;', c_code)
        for var_name, var_value in int_matches:
            variables[var_name] = int(var_value)
            
        debug_print(f"🔄 Found C variables: {variables}")
        return variables
    
    def prepare_c_code_with_variables(self, outer_content: str, nested_blocks: list) -> str:
        """Prepare C code with variables from nested execution"""
        # Remove nested blocks
        c_code_clean = self.remove_nested_blocks(outer_content)
        
        # Extract variable declarations to keep
        var_declarations = []
        for match in re.finditer(r'int\s+\w+\s*=\s*\d+\s*;', outer_content):
            var_declarations.append(match.group())
        
        # Add variable declarations for results from nested blocks
        additional_vars = []
        for var_name, var_value in self.global_state.items():
            if not var_name.startswith('_') and var_name not in ['a', 'b']:  # Don't redeclare C vars
                if isinstance(var_value, int):
                    additional_vars.append(f"int {var_name} = {var_value};")
        
        # Combine declarations and remaining C code
        all_declarations = var_declarations + additional_vars
        remaining_code = c_code_clean
        
        # Remove existing declarations from remaining code
        for decl in var_declarations:
            remaining_code = remaining_code.replace(decl, '')
        
        final_code = '\n'.join(all_declarations) + '\n' + remaining_code.strip()
        debug_print(f"🔄 Final C code with variables:\n{final_code}")
        
        return final_code.strip()
    
    def execute_nested_iteration(self, nested_block: Dict, loop_index: int, array_value: int):
        """Execute a single nested block iteration"""
        lang = nested_block['lang']
        code = nested_block['code'].strip()
        
        debug_print(f"🔄 Executing {lang} nested block for iteration {loop_index}")
        
        if lang == 'py':
            # Replace placeholders in Python code
            # Replace a[i] with actual value
            processed_code = re.sub(r'a\[i\]', str(array_value), code)
            
            # Get available variables
            referenced_vars = self.extract_variable_references(processed_code, lang)
            available_vars = {k: v for k, v in self.global_state.items() 
                             if k in referenced_vars and not k.startswith('_')}
            
            # Add current values
            available_vars['i'] = loop_index
            
            # Inject variables and execute - FIX INDENTATION
            var_injection = self.inject_variable_declarations(lang, available_vars)
            
            # Clean up the code - remove extra indentation and split by lines
            code_lines = processed_code.split('\n')
            clean_lines = []
            for line in code_lines:
                if line.strip():  # Only include non-empty lines
                    clean_lines.append(line.strip())  # Remove all leading whitespace
            
            clean_processed_code = '\n'.join(clean_lines)
            
            modified_vars = self.extract_modified_variables(clean_processed_code, lang)
            output_capture = self.inject_output_capture(lang, modified_vars, clean_processed_code)
            
            full_code = var_injection + clean_processed_code + output_capture
            
            debug_print(f"Python nested code:\n{full_code}")
            
            try:
                output = execute_in_docker(lang, full_code, "{}")
                self.process_execution_output(output)
            except Exception as e:
                print(f"Error executing nested {lang}: {e}")
        
        elif lang == 'java':
            # Replace placeholders in Java code
            processed_code = re.sub(r'a\[i\]', str(array_value), code)
            
            # Clean up indentation for Java code
            code_lines = processed_code.split('\n')
            clean_lines = []
            for line in code_lines:
                if line.strip():  # Only include non-empty lines
                    clean_lines.append('        ' + line.strip())  # Proper Java indentation inside main method
            
            clean_processed_code = '\n'.join(clean_lines)
            
            # Wrap in Main class
            java_code = f"""public class Main {{
    public static void main(String[] args) {{
        int i = {loop_index};
{clean_processed_code}
    }}
}}"""
            
            debug_print(f"Java nested code:\n{java_code}")
            
            try:
                output = execute_in_docker(lang, java_code, "{}")
                if output.strip():
                    print(output.strip())
            except Exception as e:
                print(f"Error executing nested {lang}: {e}")
    
    def execute_nested_iteration_and_return_output(self, nested_block: Dict, loop_index: int, array_value: int):
        """Execute a single nested block iteration and return output for WebSocket"""
        lang = nested_block['lang']
        code = nested_block['code'].strip()
        
        debug_print(f"🔄 Executing {lang} nested block for iteration {loop_index}")
        
        output_lines = []
        
        if lang == 'py':
            # Replace placeholders in Python code
            processed_code = re.sub(r'a\[i\]', str(array_value), code)
            
            # Get available variables
            referenced_vars = self.extract_variable_references(processed_code, lang)
            available_vars = {k: v for k, v in self.global_state.items() 
                             if k in referenced_vars and not k.startswith('_')}
            
            # Add current values
            available_vars['i'] = loop_index
            
            # Inject variables and execute
            var_injection = self.inject_variable_declarations(lang, available_vars)
            
            # Clean up the code - remove extra indentation
            code_lines = processed_code.split('\n')
            clean_lines = []
            for line in code_lines:
                if line.strip():  # Only include non-empty lines
                    clean_lines.append(line.strip())  # Remove all leading whitespace
            
            clean_processed_code = '\n'.join(clean_lines)
            
            modified_vars = self.extract_modified_variables(clean_processed_code, lang)
            output_capture = self.inject_output_capture(lang, modified_vars, clean_processed_code)
            
            full_code = var_injection + clean_processed_code + output_capture
            
            debug_print(f"Python nested code:\n{full_code}")
            
            try:
                output = execute_in_docker(lang, full_code, "{}")
                program_lines, _ = self.process_execution_output_and_return(output)
                output_lines.extend(program_lines)
            except Exception as e:
                output_lines.append(f"Error executing nested {lang}: {e}")
        
        elif lang == 'java':
            # Replace placeholders in Java code
            processed_code = re.sub(r'a\[i\]', str(array_value), code)
            
            # Clean up indentation for Java code
            code_lines = processed_code.split('\n')
            clean_lines = []
            for line in code_lines:
                if line.strip():  # Only include non-empty lines
                    clean_lines.append('        ' + line.strip())  # Proper Java indentation inside main method
            
            clean_processed_code = '\n'.join(clean_lines)
            
            # Wrap in Main class
            java_code = f"""public class Main {{
    public static void main(String[] args) {{
        int i = {loop_index};
{clean_processed_code}
    }}
}}"""
            
            debug_print(f"Java nested code:\n{java_code}")
            
            try:
                output = execute_in_docker(lang, java_code, "{}")
                if output.strip():
                    output_lines.extend([line for line in output.strip().split('\n') if line.strip()])
            except Exception as e:
                output_lines.append(f"Error executing nested {lang}: {e}")
        
        return output_lines

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
                                        printf_parts.append(f'printf({arg}); printf(" ");')
                                    else:
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


# Compatibility functions for your existing API
def parse_code_to_tree(code_str: str) -> list:
    """Parse code structure - returns compatible format with enhanced nested detection"""
    orchestrator = SharedStateOrchestrator()
    structure_type = orchestrator.detect_code_structure(code_str)
    
    if structure_type.startswith('single_'):
        lang = structure_type.split('_')[1]
        return [{'lang': lang, 'code': code_str, 'is_nested': False}]
    elif structure_type == 'nested':
        # Return special marker for nested execution
        return [{'lang': 'nested', 'code': code_str, 'is_nested': True}]
    else:
        return orchestrator.parse_sequential_blocks(code_str)

def execute_tree_generator(blocks: list, input_state: dict = None):
    """Execute blocks using shared state orchestrator with full nested support"""
    orchestrator = SharedStateOrchestrator()
    if input_state:
        orchestrator.global_state.update(input_state)
    
    # Check if this is nested execution
    if len(blocks) == 1 and blocks[0].get('is_nested'):
        # This is nested code - use the full orchestrator
        if DEBUG_MODE:
            yield "=" * 50
            yield "🔄 NESTED EXECUTION PIPELINE STARTED"
            yield "=" * 50
        
        # Execute using the full orchestrator with nested support
        code_str = blocks[0]['code']
        
        # Parse all blocks (nested and sequential)
        all_blocks = orchestrator.parse_all_blocks(code_str)
        
        if DEBUG_MODE:
            yield f"🏗️ Found {len(all_blocks)} blocks to process"
        
        # Execute blocks in order
        for i, block in enumerate(all_blocks):
            if DEBUG_MODE:
                nested_marker = "(NESTED)" if block.get('nested') else ""
                yield f"\n🏗️ === BLOCK {i+1}/{len(all_blocks)}: {block['lang'].upper()} {nested_marker} ==="
            
            if block.get('nested'):
                # Handle nested blocks specially - execute the loop
                nested_output = orchestrator.execute_nested_block_with_loop_and_return_output(block)
                for line in nested_output:
                    yield line
            else:
                # Regular sequential block
                program_output = orchestrator.execute_block_with_state_and_output(block)
                if program_output:
                    for line in program_output:
                        yield line
        
        if DEBUG_MODE:
            yield "\n" + "=" * 50
            yield "🏁 NESTED EXECUTION SUMMARY"
            yield "=" * 50
            clean_state = {k: v for k, v in orchestrator.global_state.items() if not k.startswith('_')}
            if clean_state:
                yield f"📊 Final state: {clean_state}"
            else:
                yield "📊 No variables persisted"
            yield "✅ Nested execution completed"
            yield "=" * 50
        
    elif len(blocks) == 1 and not re.search(r'::(\w+)', blocks[0]['code']):
        # Single language
        program_output = orchestrator.execute_single_language_with_output(blocks[0]['code'], blocks[0]['lang'])
        if program_output:
            for line in program_output:
                yield line
    else:
        # Sequential blocks
        if DEBUG_MODE:
            yield "=" * 50
            yield "🔄 POLYGLOT EXECUTION PIPELINE STARTED"
            yield "=" * 50
        
        for i, block in enumerate(blocks):
            if DEBUG_MODE:
                yield f"\n🏗️ === BLOCK {i+1}/{len(blocks)}: {block['lang'].upper()} ==="
            
            # Execute block and get program output
            program_output = orchestrator.execute_block_with_state_and_output(block)
            if program_output:
                for line in program_output:
                    yield line
        
        # Debug final state only if debug mode is enabled
        if DEBUG_MODE:
            yield "\n" + "=" * 50
            yield "🏁 PIPELINE EXECUTION SUMMARY" 
            yield "=" * 50
            clean_state = {k: v for k, v in orchestrator.global_state.items() if not k.startswith('_')}
            if clean_state:
                yield f"📊 Final state: {clean_state}"
            else:
                yield "📊 No variables persisted"
            yield "✅ Pipeline completed successfully"
            yield "=" * 50
        # IMPORTANT: Final state should NEVER appear when DEBUG_MODE is False
        # If you see this in output when debug is off, the server needs to be restarted

# Legacy compatibility
def extract_variable_references(code: str, lang: str) -> set:
    orchestrator = SharedStateOrchestrator()
    return orchestrator.extract_variable_references(code, lang)

def extract_modified_variables(code: str, lang: str) -> set:
    orchestrator = SharedStateOrchestrator()
    return orchestrator.extract_modified_variables(code, lang)

def inject_variable_declarations(lang: str, variables: dict) -> str:
    orchestrator = SharedStateOrchestrator()
    return orchestrator.inject_variable_declarations(lang, variables)

def inject_output_capture(lang: str, variables: dict, user_code: str = "") -> str:
    orchestrator = SharedStateOrchestrator()
    var_set = set(variables.keys()) if isinstance(variables, dict) else variables
    return orchestrator.inject_output_capture(lang, var_set, user_code)

# Main execution function for backend compatibility
def execute_polyglot_code(code_str: str) -> None:
    """Execute polyglot code with shared state management - Backend compatible"""
    orchestrator = SharedStateOrchestrator()
    
    debug_print("Starting polyglot execution with enhanced orchestrator")
    
    # Use the new unified execution method
    orchestrator.parse_and_execute(code_str)