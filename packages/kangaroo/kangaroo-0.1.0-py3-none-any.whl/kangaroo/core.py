from .utils import get_current_directory, find_file_in_parent_directories_as_recursively


def bring(
    filename: str = "manage.py",
    start_directory: str = get_current_directory(),
    end_directory: str = "/",
) -> [None, str]:
    file_path = find_file_in_parent_directories_as_recursively(
        filename, start_directory, end_directory
    )
    return file_path
