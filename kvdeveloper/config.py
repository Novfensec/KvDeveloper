import typer
from pathlib import Path

app = typer.Typer()
def_dir = Path(__file__).parent

# Configuration settings
TEMPLATES = {
    "blank": "Basic structure with a SampleScreen component.",
    "nav_toolbar": "Navigation and toolbar screens with HomeScreen and LoginScreen components.",
    "nav_dock": "Navigation and toolbar screens with BottomNavigation, HomeScreen, LoginScreen and SettingsScreen components.",
}
TEMPLATES_DIR = f"{def_dir}/templates"
STRUCTURES = {
    "none": "No specific structure",
    "MVC": "Model-View-Controller architecture.",
}
STRUCTURES_DIR = f"{def_dir}/structures"
DEFAULT_TEMPLATE = "blank"
DEFAULT_STRUCTURE = "none"

VIEW_BASE = f"{def_dir}/view_base"

IMAGE_LIBRARY = f"{def_dir}/assets/image_library"

BUILD_DIR = f"{def_dir}/build_files"

LAYOUTS_DIR = f"{def_dir}/layouts"

COMPONENTS_DIR = f"{def_dir}/components"
