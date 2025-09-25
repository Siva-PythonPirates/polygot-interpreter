import re
import json
from pprint import pprint
import textwrap
from engine import execute_in_docker

def build_tree(nodes: list) -> list:
    tree, parent_stack = [], []
    for node in nodes:
        level = node['level']
        while parent_stack and parent_stack[-1]['level'] >= level:
            parent_stack.pop()
        if not parent_stack:
            tree.append(node)
        else:
            parent = parent_stack[-1]
            if 'children' not in parent: parent['children'] = []
            parent['children'].append(node)
        parent_stack.append(node)
    return tree

def parse_code_to_tree(code_str: str) -> list:
    flat_nodes = []
    pattern = re.compile(r"^(\s*)::(\w+)", re.MULTILINE)
    matches = list(pattern.finditer(code_str))
    for i, match in enumerate(matches):
        indent_str = match.group(1)
        lang = match.group(2)
        level = len(indent_str.replace('\t', '    '))
        content_start = match.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(code_str)
        
        raw_code = code_str[content_start:content_end]
        
        # This is the key: clean the indentation the moment the code is parsed.
        cleaned_code = textwrap.dedent(raw_code).strip()

        flat_nodes.append({'lang': lang, 'level': level, 'code': cleaned_code, 'children': []})
    return build_tree(flat_nodes)

def translate_state_to_code(lang: str, state: dict) -> str:
    if lang == 'c':
        declarations = []
        for key, value in state.items():
            if isinstance(value, list) and all(isinstance(i, int) for i in value):
                arr_str = ", ".join(map(str, value))
                declarations.append(f"int {key}[] = {{{arr_str}}};")
            elif isinstance(value, str):
                msg_str = value.replace('"', '\\"')
                declarations.append(f'char {key}[] = "{msg_str}";')
            elif isinstance(value, int):
                declarations.append(f"int {key} = {value};")
        return "\n".join(declarations)
    return ""

def execute_tree_generator(nodes: list, input_state: dict = None):
    current_state = input_state if input_state is not None else {}
    for node in nodes:
        child_input_state = current_state.copy()
        if node.get('children'):
            child_final_state = yield from execute_tree_generator(node['children'], child_input_state)
            current_state.update(child_final_state)
            
        lang, code = node['lang'], node['code']
        yield f"--- Preparing to run Block ({lang}) ---"
        
        try:
            injected_code = translate_state_to_code(lang, current_state)
            full_code_to_run = f"{injected_code}\n{code}"
            state_json_str = json.dumps(current_state)

            output = execute_in_docker(lang, full_code_to_run, state_json_str)
            
            try:
                new_state = json.loads(output)
                yield f"✅ Block ({lang}) finished. New state: {json.dumps(new_state)}"
                current_state.update(new_state)
            except json.JSONDecodeError:
                yield f"✅ Block ({lang}) finished. Final output:\n{output}"
                current_state = {}
        except Exception as e:
            yield f"❌ Error executing {lang} block: {e}"
            return current_state
            
    return current_state