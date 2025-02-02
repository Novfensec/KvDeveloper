import os
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
TEMPLATES_DIR = os.path.join(def_dir, "templates")

STRUCTURES = {
    "none": "No specific structure",
    "MVC": "Model-View-Controller architecture.",
}
STRUCTURES_DIR =  os.path.join(def_dir, "structures")

DEFAULT_TEMPLATE = "blank"
DEFAULT_STRUCTURE = "none"

VIEW_BASE =  os.path.join(def_dir, "view_base")

IMAGE_LIBRARY =  os.path.join(def_dir, "assets", "image_library")

BUILD_DIR =  os.path.join(def_dir, "build_files")

LAYOUTS_DIR =  os.path.join(def_dir, "layouts")

COMPONENTS = {
    "Container": "A responsive container with pre-defined padding calculations.",
    "ITCard": "(Image Title Description Card) A responsive boostrap like card with image aspect-ratio calculations.",
    "ResponsiveGrid": "A responsive grid with pre-defined column calculations.",
    "LazyManager": "A MDScreenManager class instance with lazy loading abilities.",
    "LoadingLayout": "A FloatLayout class instance with centralised MDCircularProgressIndicator widget."
}
COMPONENTS_DIR =  os.path.join(def_dir, "components")

LIBS_DIR =  os.path.join(def_dir, "libs")
