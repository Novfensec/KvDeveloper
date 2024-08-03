import typer
from pathlib import Path

app = typer.Typer()
def_dir=Path(__file__).parent

# Configuration settings
TEMPLATES = {
    "blank": "Basic structure",
    "nav_toolbar": "Navigation and toolbar screens"
}
TEMPLATES_DIR = f"{def_dir}/templates"
STRUCTURES = {
    "none": "No specific structure",
    "MVC": "Model-View-Controller architecture"
}
STRUCTURES_DIR = f"{def_dir}/structures"
DEFAULT_TEMPLATE = "blank"
DEFAULT_STRUCTURE = "none"

VIEW_BASE = f"{def_dir}/view_base"
