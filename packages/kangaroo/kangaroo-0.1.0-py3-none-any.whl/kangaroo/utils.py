import os
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def jump_parent_directory_then_jump_back(previous_dir: str) -> Iterator[str]:
    parent_dir = os.path.abspath("..")
    try:
        os.chdir(parent_dir)
        yield parent_dir
    finally:
        os.chdir(previous_dir)


def get_current_directory() -> str:
    return os.getcwd()


def is_file_exists(filepath: str) -> bool:
    return os.path.exists(filepath)


def find_file_in_specific_directory(filename: str, directory: str) -> [None, str]:
    new_file_path = os.path.join(directory, filename)
    if is_file_exists(new_file_path):
        return new_file_path

    return None


def find_file_in_parent_directories_as_recursively(
    filename: str, start_directory: str, end_directory: str
) -> [None, str]:
    filename_path = find_file_in_specific_directory(filename, start_directory)
    if filename_path is not None:
        return filename_path

    if start_directory == end_directory:
        return None
    with jump_parent_directory_then_jump_back(start_directory) as parent_dir:
        return find_file_in_parent_directories_as_recursively(
            filename, parent_dir, end_directory
        )

