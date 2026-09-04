from functions.utils import check_working_directory
import os
import subprocess
from openai.types.chat import ChatCompletionToolParam

schema_run_python_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        (full_path, err_string) = check_working_directory(working_directory, file_path)
        if err_string is not None:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if full_path:
            if not os.path.isfile(full_path):
                return f'Error: "{file_path}" does not exist or is not a regular file'
            if not full_path.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file'

            command = ["python", full_path]
            if args is not None:
                command.extend(args)

            completeded_process = subprocess.run(command,capture_output=True, text=True, timeout=30000)
            string = ""
            rt = completeded_process.returncode
            stdout = completeded_process.stdout
            stderr = completeded_process.stderr

            if rt != 0:
                string = string + f"Process exited with code {rt}/n"
            if (stdout == "") and {stderr == ""}:
                string = string + "No output produced"
            if stdout:
                string = string + f"STDOUT: {stdout}"
            if stderr:
                string = string + f"STDERR: {stderr}"

            return string

        else:
            return "Error: no full_path"



    except Exception as e:
        return f'Error: executing Python file: {str(e)}'
