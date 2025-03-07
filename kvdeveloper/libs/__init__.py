import os
from typing import List

from kvdeveloper.config import LIBS_DIR
from kvdeveloper.module import console
from kvdeveloper.utils import replace_placeholders


def add_from_libs(name_libs: List[str], destination: str) -> None:
    for libs in name_libs:
        libs_path = os.path.join(LIBS_DIR, libs)
        destination = os.path.join(destination, libs)

    # Walk through the libs directory and replicate structure in destination
    for root, _, files in os.walk(libs_path):
        relative_path = os.path.relpath(root, libs_path)  # Relative path from the libs
        target_dir = os.path.join(
            destination, relative_path
        )  # Corresponding destination path

        os.makedirs(target_dir, exist_ok=True)  # Ensure the target directory exists

        # Process files in the current directory
        for file_name in files:
            # Skip unnecessary file types
            if file_name.endswith((".pyc", ".pyo")):
                continue

            source_file = os.path.join(root, file_name)  # Full path to the source file
            target_file = os.path.join(
                target_dir, file_name
            )  # Full path to the target file

            # Read and process the content of the template file
            with open(source_file, "r", encoding="utf-8") as src:
                content = src.read()

            # Replace placeholders in the content
            # content = replace_placeholders(content, variables)

            # Write the processed content to the target file
            with open(target_file, "w", encoding="utf-8") as dest:
                dest.write(content)

            console.print(f"\nCreated file: [bright_white]{target_file}[/bright_white]")
