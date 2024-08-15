import typer
import os
from typing import Optional, Dict
from kvdeveloper import __app_name__, __version__
from .config import app, DEFAULT_TEMPLATE, DEFAULT_STRUCTURE, STRUCTURES, TEMPLATES
from .module import (
    create_from_template,
    create_from_structure,
    setup_build,
    project_info,
)
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()


@app.command()
def create(
    template: str = typer.Option(DEFAULT_TEMPLATE, help="Template for the project."),
    structure: str = typer.Option(DEFAULT_STRUCTURE, help="Structure for the project."),
    project_name: Optional[str] = typer.Argument(
        "NewProject", help="Name of the project"
    ),
) -> None:
    """
    Create a new project with the specified template and structure.

    :param project_name: The name of the project.
    :param template: The name of the template folder.
    :param structure: The name of the structure folder.
    """
    template_info = TEMPLATES[f"{template}"]
    structure_info = STRUCTURES[f"{structure}"]
    typer.secho(
        f"Creating project '{project_name}' with template '{template}': {template_info}\n",
        fg=typer.colors.BRIGHT_MAGENTA,
    )
    typer.secho(
        f"Applying structure '{structure}': {structure_info}\n",
        fg=typer.colors.BRIGHT_CYAN,
    )

    project_name = project_name.strip().replace(" ", "")
    variables = {
        "project_name": project_name,
    }

    destination = os.path.join(os.getcwd(), project_name)
    if structure == "none":
        create_from_template(template, destination, variables)
    elif structure == "MVC":
        create_from_structure(template, structure, destination, variables)

    build_variables = {
        "project_name": project_name,
        "project_package_name": project_name.lower(),
    }
    setup_build(project_name, destination, build_variables)
    project_info(project_name, template, structure, destination)


@app.command()
def list_templates() -> None:
    """
    List all available templates.
    """
    help_text = Text("\n Available Templates\n")
    templates_info = Text.assemble(
        ("All the templates have inbuilt"), (" hot reload", "bright_red"), (" system.")
    )
    template_table = Table(show_header=False, box=None)
    template_table.add_column("Template Name", style="bold cyan", width=21)
    template_table.add_column("Description")
    for template, description in TEMPLATES.items():
        template_table.add_row(template, description)
    templates_box = Panel(
        template_table, title="Templates", title_align="left", expand=True
    )
    templates_info_box = Panel(
        templates_info,
        title="[bright_white]Templates Info[/bright_white]",
        expand=True,
        title_align="left",
        padding=1,
    )
    typer.secho(help_text, fg=typer.colors.BRIGHT_WHITE)
    console.print(templates_box)
    console.print(templates_info_box)
    raise typer.Exit()


@app.command()
def list_structures() -> None:
    """
    List all available structures.
    """
    help_text = Text("\n Available Structures\n")
    structure_table = Table(show_header=False, box=None)
    structure_table.add_column("Template Name", style="bold cyan", width=21)
    structure_table.add_column("Description")
    for structure, description in STRUCTURES.items():
        structure_table.add_row(structure, description)
    structures_box = Panel(
        structure_table, title="Structures", title_align="left", expand=True
    )
    typer.secho(help_text, fg=typer.colors.BRIGHT_WHITE)
    console.print(structures_box)
    raise typer.Exit()


def _version_callback(value: bool) -> None:
    if value:
        typer.secho(f"{__app_name__} v{__version__}", fg=typer.colors.BRIGHT_WHITE)
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
