from functions.utils import check_working_directory
import os
import subprocess


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

            if rt is not 0:
                string = string + f"Process exited with code {rt}/n"
            if (stdout is "") and {stderr is ""}:
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
