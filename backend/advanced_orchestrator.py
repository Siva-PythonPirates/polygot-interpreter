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
        # Look for outer language block containing nested blocks
        outer_match = re.search(r'::(\w+)(.*?)::/\1', code_str, re.DOTALL)
        if outer_match:
            outer_content = outer_match.group(2)
            # Check if content contains nested blocks (inline ::lang syntax)
            nested_pattern = r'::(\w+)\s+(.*?)\s+::/\1'
            if re.search(nested_pattern, outer_content, re.DOTALL):
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
            for match in re.finditer(r'([a-zA-Z_]\w*)\.(append|extend|remove|pop|clear)', code):
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
        """Execute nested blocks with cross-language conversion"""
        debug_print("=" * 50)
        debug_print("🔄 NESTED BLOCK EXECUTION")
        debug_print("=" * 50)
        
        # Find the outermost language block
        outer_match = re.search(r'::(\w+)(.*?)::/\1', code_str, re.DOTALL)
        if not outer_match:
            # Fallback to sequential if no outer block found
            self.execute_sequential_blocks(code_str)
            return
        
        outer_lang = outer_match.group(1)
        outer_content = outer_match.group(2)
        
        debug_print(f"🏗️ Processing nested {outer_lang.upper()} block")
        
        # Process nested blocks and convert them to outer language syntax
        processed_content = self.process_nested_blocks(outer_content, outer_lang)
        
        # Execute the processed outer block
        block = {
            'lang': outer_lang,
            'code': processed_content,
            'type': 'nested'
        }
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
    """Parse code structure - returns compatible format"""
    orchestrator = SharedStateOrchestrator()
    structure_type = orchestrator.detect_code_structure(code_str)
    
    if structure_type.startswith('single_'):
        lang = structure_type.split('_')[1]
        return [{'lang': lang, 'code': code_str, 'is_nested': False}]
    else:
        return orchestrator.parse_sequential_blocks(code_str)

def execute_tree_generator(blocks: list, input_state: dict = None):
    """Execute blocks using shared state orchestrator"""
    orchestrator = SharedStateOrchestrator()
    if input_state:
        orchestrator.global_state.update(input_state)
    
    if len(blocks) == 1 and not re.search(r'::(\w+)', blocks[0]['code']):
        # Single language
        orchestrator.execute_single_language(blocks[0]['code'], blocks[0]['lang'])
    else:
        # Sequential blocks
        if DEBUG_MODE:
            yield "=" * 50
            yield "🔄 POLYGLOT EXECUTION PIPELINE STARTED"
            yield "=" * 50
        
        for i, block in enumerate(blocks):
            if DEBUG_MODE:
                yield f"\n🏗️ === BLOCK {i+1}/{len(blocks)}: {block['lang'].upper()} ==="
            
            orchestrator.execute_block_with_state(block)
        
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