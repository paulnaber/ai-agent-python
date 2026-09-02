import os

def check_working_directory(working_directory: str, directory: str) -> tuple[str | None, str | None]:
    """
        checks whether the directory is withing the working directory

        Returns:
            (str, str): return the fullpath string if it the directory is withing the working_directory,
            will be None if not, errorstring in case of error
    """

    working_directory_absolute = os.path.abspath(working_directory)
    full_path = os.path.normpath(os.path.join(working_directory_absolute, directory))

    valid_target_dir = os.path.commonpath([working_directory_absolute, full_path]) == working_directory_absolute

    if valid_target_dir is True:
        return (full_path, None)
    else:
        return (None, f'Error: Cannot list "{directory}" as it is outside the permitted working directory')