import glob
import os
from typing import List, Optional

from kivy.core.text import LabelBase
from kivy.factory import Factory

# Alias for the register function from Factory
component_register = Factory.register

# Get the absolute path to the "View" directory
view_path = os.path.join(os.getcwd(), "View")

# Pattern to match all "components" directories recursively within "View"
component_dir_pattern = os.path.join(view_path, "**", "components")

# Find all directories that match the component pattern
component_dirs: List[str] = glob.glob(component_dir_pattern, recursive=True)

"""
Registers custom components to the Kivy Factory.

Below code searches for all directories named "components" within the "View" directory and registers each component to the Kivy Factory. 
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
            component_register(module_name, module=module_import_path)


"""
Registers custom fonts to the Kivy LabelBase.

Below code searches for all directories within the "assets/fonts" directory and registers each font to the Kivy LabelBase. 
Once registered, the fonts can be used without explicitly importing them elsewhere in the kvlang files.

To successfully register the fonts, the directory structure should contain font files for regular, bold, italic, and bolditalic styles, as shown below:

- Example Directory Structure:

    TestApp
    └── assets
        └── fonts
            └── TestFont
                ├── testfont-bold.ttf
                ├── testfont-bolditalic.ttf
                ├── testfont-italic.ttf
                └── testfont-regular.ttf

- Usage in `kvlang` files:

```
    MDLabel:
        text: "TestFont"
        font_name: "TestFont" # (Case Sensitive Name)
        bold: True
        italic: True
```

"""

# Alias for the register function from LabelBase
font_register = LabelBase.register

# Get the absolute path to the "assets/fonts" directory
font_dir = os.path.join(os.getcwd(), "assets", "fonts")


def get_font_path(directory: str, font_name: str, style: str) -> Optional[str]:
    """
    Helper function to construct and check the path for a specific font style.

    Args:
        directory (str): The path to the font's directory.
        font_name (str): The base name of the font.
        style (str): The style of the font (e.g., regular, italic, bold, bolditalic).

    Returns:
        Optional[str]: The path to the font file if it exists, otherwise None.
    """
    font_path = os.path.join(directory, f"{font_name.lower()}-{style}.ttf")
    return font_path if os.path.isfile(font_path) else None


# Iterate over the fonts in the directory
for font_name in os.listdir(font_dir):
    target_dir = os.path.join(font_dir, font_name)

    # Check if it's a directory (excluding '__pycache__')
    if os.path.isdir(target_dir) and font_name != "__pycache__":

        # Fetch paths for different font styles if available
        regular_font = get_font_path(target_dir, font_name, "regular")
        italic_font = get_font_path(target_dir, font_name, "italic")
        bold_font = get_font_path(target_dir, font_name, "bold")
        bolditalic_font = get_font_path(target_dir, font_name, "bolditalic")

        # Register the font with the LabelBase
        font_register(font_name, regular_font, italic_font, bold_font, bolditalic_font)
