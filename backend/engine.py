import subprocess
import os
import tempfile
import shutil

def execute_in_docker(lang: str, code: str, state_json: str) -> str:
    """
    Builds and runs a Docker container using direct CLI commands
    via the subprocess module.
    """
    lang_map = {
        'c': ('main.c', 'c.Dockerfile', 'polyglot-c-runner'),
        'py': ('script.py', 'py.Dockerfile', 'polyglot-py-runner'),
        'java': ('Main.java', 'java.Dockerfile', 'polyglot-java-runner'),
    }

    if lang not in lang_map:
        raise ValueError(f"Unsupported language: {lang}")

    filename, dockerfile_name, image_tag = lang_map[lang]

    # Use a temporary directory to avoid conflicts
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write the user's code and the correct Dockerfile to the temp directory
        with open(os.path.join(temp_dir, filename), 'w') as f:
            f.write(code)
        
        # We assume the Dockerfiles are in the same directory as this script
        shutil.copyfile(dockerfile_name, os.path.join(temp_dir, dockerfile_name))

        try:
            # --- Step 1: Build the Docker image using subprocess ---
            build_command = [
                "docker", "build",
                "-t", image_tag,
                "-f", dockerfile_name,
                "." # The build context is the temporary directory
            ]
            # We run the command from within the temp_dir
            subprocess.run(build_command, check=True, cwd=temp_dir, capture_output=True, text=True)

            # --- Step 2: Run the container using subprocess ---
            run_command = [
                "docker", "run",
                "--rm", # Automatically remove the container when it exits
                image_tag,
                state_json # Pass the state as a command-line argument
            ]
            result = subprocess.run(run_command, check=True, capture_output=True, text=True)
            
            # The captured output from the container is in stdout
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            # If any docker command fails, we raise an error with the details
            error_message = f"Docker command failed.\n"
            error_message += f"Stderr: {e.stderr}"
            raise RuntimeError(error_message)
        except FileNotFoundError:
             raise RuntimeError("Docker command not found. Is Docker installed and in your PATH?")