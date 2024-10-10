import typer
import os
from typing import Optional, List
from kvdeveloper import __app_name__, __version__
from kvdeveloper.config import (
    app,
    DEFAULT_TEMPLATE,
    DEFAULT_STRUCTURE,
    STRUCTURES,
    TEMPLATES,
    COMPONENTS_DIR,
)
from kvdeveloper.module import (
    console,
    create_from_template,
    create_from_structure,
    add_from_default,
    add_from_structure,
    add_from_layout,
    apply_layout,
    setup_build,
    project_info,
)
from kvdeveloper.info_reader import info_reader
from kvdeveloper.build_config import generate_build_files
from rich.panel import Panel
from rich.text import Text
from rich.table import Table


@app.command()
def create(
    template: str = typer.Option(DEFAULT_TEMPLATE, help="Template for the project."),
    structure: str = typer.Option(DEFAULT_STRUCTURE, help="Structure for the project."),
    project_name: Optional[str] = typer.Argument(
        "NewProject", help="Name of the project."
    ),
) -> None:
    """
    Create a new project with the specified template and structure.

    :param project_name: The name of the project.
    :param template: The name of the template folder.
    :param structure: The name of the structure folder.
    """

    destination = os.path.join(os.getcwd(), project_name)
    if os.path.isdir(destination):
        ValueError(f"Project '{project_name}' already exists.")

    try:
        template_info = TEMPLATES[f"{template}"]
    except:
        console.print(f" Template for name [green]{template}[/green] not found.")
        raise typer.Exit(code=0)
    try:
        structure_info = STRUCTURES[f"{structure}"]
    except:
        console.print(f" Structure for name [green]{structure}[/green] not found.")
        raise typer.Exit(code=0)

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
    funcs = {
        "none": lambda: create_from_template(template, destination, variables),
        "MVC": lambda: create_from_structure(
            template, structure, destination, variables
        ),
    }
    task = funcs.get(structure)()
    build_variables = {
        "project_name": project_name,
        "project_package_name": project_name.lower(),
    }
    setup_build(project_name, destination, build_variables)
    project_info(project_name, template, structure, destination)


@app.command()
def add_screen(
    name_screen: List[str] = typer.Argument(help="Name of the screen."),
    use_template: Optional[str] = typer.Option(
        None, help="Name of the template if the specified view exists in it."
    ),
    layout: str = typer.Option(None, help="Layout of the screen."),
    structure: str = typer.Option(DEFAULT_STRUCTURE, help="Structure of the project."),
) -> None:
    """
    Create screens with specified template and structure.

    :param name_screen: The name of the screen.
    :param use_template: The name of the template to be used for creating the view if it pre-exists.
    :param layout: The name of the layout.
    :param structure: The name of the structure folder.
    """
    destination = os.path.join(os.getcwd(), "View")
    if structure == "none":
        if layout != None:
            add_from_layout(name_screen, layout, destination)
        elif layout == None:
            add_from_default(name_screen, use_template, destination)
    elif structure == "MVC":
        if layout != None:
            add_from_structure(name_screen, layout, destination)
        if layout == None:
            add_from_structure(name_screen, use_template, destination)
    else:
        console.print("Structure for name [green]{structure}[/green] not found.")
        raise typer.Exit(code=0)


@app.command()
def add_layout(
    name_screen: List[str] = typer.Option(
        help="List containig the name of the screens."
    ),
    layout: str = typer.Argument(None, help="The name of the layout for the screens."),
) -> None:
    """
    Apply layout to a screen with specified layout type.

    :param name_screen: The list containing the names of the screens.
    :param layout: The name of the layout for the screens.
    :param destination: The destination path where the files will be created and updated.
    """
    destination = os.path.join(os.getcwd(), "View")

    apply_layout(name_screen, layout, destination)


@app.command()
def add_component(
    name_component: List[str] = typer.Argument(
        help="List containing the names of the components."
    ),
) -> None:
    list_component_path = []
    for components in name_component:
        component_path = os.path.join(COMPONENTS_DIR, components)
        if not os.path.isdir(component_path):
            typer.secho(f"Component {components} does not exists.")
            continue
        list_component_path.append(component_path)

    destination = os.path.join(os.getcwd(), "Components")
    if not os.path.isdir(destination):
        os.makedirs("Components", exist_ok=True)

    for component_path in list_component_path:
        for root, _, files in os.walk(component_path):
            relative_path = os.path.relpath(root, component_path)
            target_dir = os.path.join(destination, relative_path)
            os.makedirs(target_dir, exist_ok=True)

            for file_name in files:
                # Skip .pyc and .pyo files
                if file_name.endswith((".pyc", ".pyo")):
                    continue
                template_file_path = os.path.join(root, file_name)
                target_file_path = os.path.join(target_dir, file_name)

                with open(template_file_path, "r", encoding="utf-8") as template_file:
                    content = template_file.read()

                with open(target_file_path, "w", encoding="utf-8") as target_file:
                    target_file.write(content)

                console.print(
                    f"Created file: [bright_white]{target_file_path}[/bright_white]"
                )


@app.command()
def config_build_setup(
    platform: str = typer.Argument(help="Platform specific to setup build files."),
    external: str = typer.Option(help="External Build Environment."),
) -> None:
    """
    Generates necessary build files for external build environments and linux systems.

    - buildozer.spec: Buildozer configurations file.
    - Github:
        buildozer_action.yml: CI/CD worflow file for github actions.
    - Colab:
        buildozer_action.ipynb: Jupyter notebook for google colab environment.

    Setup build files for platforms Android and IOS.
    `Currently supporting Android conversions build system.`

    :param platform: Platform specific to setup build files.
    :param external: External Build Environment.
    """
    available_platforms = [
        "android",
    ]
    for platforms in available_platforms:
        if platform != platforms:
            typer.secho("Unavailable platform.", err=True)
            raise typer.Exit(code=0)

    generate_build_files(platform, external)
    spec_file_path = os.path.join(os.getcwd(), "buildozer.spec")

    if not os.path.isfile(spec_file_path):
        project_name = "SampleApp"
        variables = {
            "project_name": project_name,
            "project_package_name": project_name.strip("App").lower(),
        }
        setup_build(project_name, ".", variables)


@app.command()
def show_readme(
    directory: Optional[str] = typer.Argument(
        ".", help="The directory containig the README.md file."
    )
) -> None:
    """
    Show the README.md file containing the template info of the project.

    :param directory: The directory containig the README.md file.
    """
    readme_path = os.path.join(directory, "README.md")
    if not os.path.isfile(readme_path):
        typer.echo(f"File '{readme_path}' not found.")
        raise typer.Exit(code=1)

    info_reader(directory)


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
