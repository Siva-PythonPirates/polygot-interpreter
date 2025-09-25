import subprocess
import os
import tempfile
import shutil
import textwrap

def execute_in_docker(lang: str, code: str, state_json: str) -> str:
    """
    Builds and runs a Docker container, wrapping code in templates
    and definitively fixing Python indentation.
    """
    c_template = "#include <stdio.h>\n#include <string.h>\nint main() {{ {code} return 0; }}"
    java_template = "import java.util.Arrays; import java.util.regex.*; public class Main {{ public static void main(String[] args) {{ {code} }} }}"

    lang_map = {
        'c': ('main.c', 'c.Dockerfile', 'polyglot-c-runner', c_template),
        'py': ('script.py', 'py.Dockerfile', 'polyglot-py-runner', None),
        'java': ('Main.java', 'java.Dockerfile', 'polyglot-java-runner', java_template),
    }

    if lang not in lang_map:
        raise ValueError(f"Unsupported language: {lang}")

    filename, dockerfile_name, image_tag, template = lang_map[lang]
    
    final_code = code
    if lang == 'py':
        final_code = textwrap.dedent(final_code)
    
    if template:
        final_code = template.format(code=final_code)

    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, filename), 'w') as f:
            f.write(final_code)
        
        # Assumes Dockerfiles are in the same directory as this script
        shutil.copyfile(dockerfile_name, os.path.join(temp_dir, dockerfile_name))

        try:
            build_command = ["docker", "build", "-t", image_tag, "-f", dockerfile_name, "."]
            subprocess.run(build_command, check=True, cwd=temp_dir, capture_output=True, text=True)

            run_command = ["docker", "run", "--rm", image_tag, state_json]
            result = subprocess.run(run_command, check=True, capture_output=True, text=True)
            
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_message = f"Docker command failed.\nStderr: {e.stderr}"
            raise RuntimeError(error_message)
        except FileNotFoundError:
             raise RuntimeError("Docker command not found. Is Docker installed?")