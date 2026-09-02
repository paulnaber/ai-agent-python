from .utils import check_working_directory
import os

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