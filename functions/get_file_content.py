from .utils import check_working_directory
import os
from config import MAX_CHARS
from openai.types.chat import ChatCompletionToolParam

schema_get_file_content: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:    
        (full_path, err_string) = check_working_directory(working_directory, file_path)
        if err_string is not None:
            return err_string

        if full_path:
            if not os.path.isfile(full_path):
                return f'Error: File not found or is not a regular file: "{file_path}"'
            with open(full_path, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content_string
        return ""
    except Exception as e:
        return f'Error: {str(e)}'