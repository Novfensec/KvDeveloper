import os
import glob
from kivy.factory import Factory
from typing import List

# Alias for the register function from Factory
register = Factory.register

# Get the absolute path to the "View" directory
view_path = os.path.join(os.getcwd(), "View")

# Pattern to match all "Components" directories recursively within "View"
component_dir_pattern = os.path.join(view_path, "**", "Components")

# Find all directories that match the component pattern
component_dirs: List[str] = glob.glob(component_dir_pattern, recursive=True)

"""
Registers custom components to the Kivy Factory.

This code searches for all directories named "Components" within the "View" directory and registers each component to the Kivy Factory. 
Once registered, the components can be used without explicitly importing them elsewhere in the kvlang files.
"""

for component_path in component_dirs:
    # Loop through all items in the current component directory
    for component in os.listdir(component_path):
        target_dir = os.path.join(component_path, component)

        # Skip "__pycache__" and check if the item is a valid directory
        if component != "__pycache__" and os.path.isdir(target_dir):
            # Get the relative path to the target directory
            rel_path = os.path.relpath(target_dir)

            # Extract the module name (last part of the relative path)
            module_name = os.path.basename(rel_path)

            # Convert the path to a Python importable module format
            module_import_path = rel_path.replace(os.sep, ".")

            # Register the component with Kivy's Factory
            register(module_name, module=module_import_path)
