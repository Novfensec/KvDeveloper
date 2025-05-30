import os
import importlib.util
import glob
import shutil
from pathlib import Path

from kvdeveloper.utils import toml_parser
from kvdeveloper.config import console


def sort_modules(
    module_name: str, sortmapping: str, sortfile: str, destination: str
) -> None:
    """
    Collect and copy selected module files based on a mapping and user-defined configuration.

    Args:
        module_name (str): The root Python package name (e.g., 'carbonkivy').
        sortmapping (str): Path to the TOML file defining available modules and their paths.
        sortfile (str): Path to the TOML file with user selections for modules to include.
        destination (str): Destination directory to copy sorted files into.
    """
    spec = importlib.util.find_spec(module_name)
    if spec is None or spec.origin is None:
        raise ModuleNotFoundError(f"Module {module_name} not found.")

    root = os.path.dirname(spec.origin).rstrip(module_name)

    source = toml_parser(sortmapping)
    user_config = toml_parser(sortfile)
    included_members = user_config[module_name.upper()]["members"]

    sorted_modules = []
    for member in included_members:
        sorted_modules.extend(source[member]["modules"])

    glob_patterns = []
    for module in sorted_modules:
        module_path = module.replace(".", os.sep)
        for ext in source["CORE"]["extensions"]:
            pattern = os.path.join(root, module_path, ext)
            glob_patterns.append(pattern)

    sorted_files = []
    for pattern in glob_patterns:
        sorted_files.extend(glob.glob(pattern, recursive=True))

    os.makedirs(destination, exist_ok=True)

    for source_file in sorted_files:
        src = Path(source_file)
        relative_path = src.relative_to(root)
        dest_path = Path(destination).parent / relative_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_path)
        console.print(f"\nCreated file: [bright_white]{dest_path}[/bright_white]")
