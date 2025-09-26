import re
import json
from engine import execute_in_docker

def parse_polyglot_code(code_str: str) -> list[dict]:
    pattern = r"::(\w+)\n(.*?)(?=\n::|$)"
    matches = re.findall(pattern, code_str, re.DOTALL)
    return [{'lang': lang.strip(), 'code': code.strip()} for lang, code in matches]

def run_pipeline(polyglot_code: str):
    code_blocks = parse_polyglot_code(polyglot_code)
    current_state_json = "{}"
    
    for i, block in enumerate(code_blocks):
        lang, code = block['lang'], block['code']
        yield f"--- Running Block {i+1} ({lang}) ---"
        
        try:
            output = execute_in_docker(lang, code, current_state_json)
            
            # C block creates the initial state as a simple list
            if lang == 'c':
                current_state_json = f'{{"a": {output}}}'
            # Python block outputs a full JSON state object
            elif lang == 'py':
                current_state_json = output
            # Java block outputs a final string, not state to be passed on
            else:
                current_state_json = output

            yield f"Output:\n{current_state_json}"
        except Exception as e:
            yield f"❌ Error executing {lang} block: {e}"
            break
            
    yield "\n--- Pipeline Finished ---\n"