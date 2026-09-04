from .utils import check_working_directory
import os
from openai.types.chat import ChatCompletionToolParam

schema_write_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites a file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        (full_path, err_string) = check_working_directory(working_directory, file_path)
        if err_string is not None:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if full_path:
            if os.path.isdir(full_path):
                return f'Error: Cannot write to "{file_path}" as it is a directory'

            # create directries if they dont exist up to the file
            path_last_dir = os.path.dirname(full_path)
            os.makedirs(path_last_dir, exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)' 
                
        else:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
    except Exception as e:
        return f'Error: {str(e)}'