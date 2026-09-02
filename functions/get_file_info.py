import os
from utils import check_working_directory

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        (full_path, err_string) = check_working_directory(working_directory, directory)
        if err_string is not None:
            return err_string

        if full_path:
            if not os.path.isdir(full_path):
                return f'Error: "{directory}" is not a directory'

            files: list[str] = os.listdir(full_path)
            file_infos: list[str] = []
            for f in files:
                size: int = os.path.getsize(full_path + "/" + f)
                is_dir: bool = os.path.isdir(full_path + "/" + f)
                file_infos.append(f"- {f}: file_size={size} bytes, is_dir={is_dir}")
            return "\n".join(file_infos)
                
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
    except Exception as e:
        return f'Error: {str(e)}'
