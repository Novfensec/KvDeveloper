import typer
import os
import re
from typing import Optional, List
from kvdeveloper import __app_name__, __version__
from kvdeveloper.config import (
    app,
    DEFAULT_TEMPLATE,
    DEFAULT_STRUCTURE,
    STRUCTURES,
    TEMPLATES,
    COMPONENTS_DIR,
    COMPONENTS,
    VIEW_BASE,
)
from kvdeveloper.module import (
    console,
    create_from_template,
    create_from_structure,
    add_from_default,
    add_from_structure,
    add_from_layout,
    apply_layout,
    remove_from_default,
    remove_from_structure,
    setup_build,
    project_info,
)
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
        console.print(f"\nTemplate for name [green]{template}[/green] not found.")
        raise typer.Exit(code=0)
    try:
        structure_info = STRUCTURES[f"{structure}"]
    except:
        console.print(f"\nStructure for name [green]{structure}[/green] not found.")
        raise typer.Exit(code=0)

    typer.secho(
        f"\nCreating project '{project_name}' with template '{template}': {template_info}",
        fg=typer.colors.BRIGHT_MAGENTA,
    )
    typer.secho(
        f"\nApplying structure '{structure}': {structure_info}",
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
    name_screen: List[str] = typer.Argument(
        help="List containing the name of the screens."
    ),
    use_template: Optional[str] = typer.Option(
        None,
        help="Name of the template if the specified views exists in it.",
    ),
    layout: str = typer.Option(None, help="Layout of the screens."),
    structure: str = typer.Option(DEFAULT_STRUCTURE, help="Structure of the project."),
) -> None:
    """
    Create screens with specified template and structure.

    :param name_screen: List containing the name of the screens.

    :param use_template: The name of the template to be used for creating the views if it pre-exists.

    :param layout: The name of the layout.

    :param structure: The name of the structure folder.
    """
    destination = os.path.join(os.getcwd(), "View")
    if not os.path.isdir(destination):
        typer.secho("\n'View' directory not found.", err=True)
        raise typer.Exit(code=0)

    if structure == "none":
        if layout != None:
            add_from_layout(name_screen, layout, destination)
        elif layout == None:
            add_from_default(name_screen, use_template, destination)
    elif structure == "MVC":
        add_from_structure(name_screen, use_template, layout, destination)
    else:
        console.print("\nStructure for name [green]{structure}[/green] not found.")
        raise typer.Exit(code=0)


@app.command()
def remove_screen(
    name_screen: List[str] = typer.Argument(
        help="List containing the name of the screens."
    ),
    structure: str = typer.Option(DEFAULT_STRUCTURE, help="Structure of the project."),
) -> None:
    """
    Remove screen-specific directories and files associated with specified structure.

    :param name_screen: List containing the name of the screens.

    :param structure: The name of the structure folder.
    """
    destination = os.path.join(os.getcwd(), "View")
    if not os.path.isdir(destination):
        raise typer.Exit("\n'View' directory not found.", code=1)

    remove_from_default(name_screen, destination)
    if structure != "none":
        remove_from_structure(name_screen, destination, structure)


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
    """
    Add Components to the project.

    :param name_component: List containing the names of the components. (Case Sensitive Names)
    """
    list_component_path = []
    for components in name_component:
        component_path = os.path.join(COMPONENTS_DIR, components)
        if not os.path.isdir(component_path):
            typer.secho(f"\nComponent {components} does not exists.")
            continue
        list_component_path.append(component_path)

    destination = os.path.join(os.getcwd(), "Components")
    if not os.path.isdir(destination):
        os.makedirs("Components", exist_ok=True)

    for component_path in list_component_path:
        for root, _, files in os.walk(component_path):
            relative_path = os.path.relpath(root, COMPONENTS_DIR)
            target_dir = os.path.join(destination, relative_path)
            if not "__pycache__" in target_dir:
                os.makedirs(target_dir, exist_ok=True)

            console.print(
                f"\nCreating Component [bold cyan]{os.path.basename(component_path)}[/bold cyan]"
            )

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
                    f"\nCreated file: [bright_white]{target_file_path}[/bright_white]"
                )


@app.command()
def register() -> None:
    """
    Add registers.py to recursively register all additional fonts and components to the kivy bases.
    """
    main_file_path = os.path.join(os.getcwd(), "main.py")
    if not os.path.isfile(main_file_path):
        typer.secho("\nFile 'main.py' does not exists.", err=True)
        raise typer.Exit(code=0)

    registers_file_path = os.path.join(os.getcwd(), "registers.py")
    if not os.path.isfile(registers_file_path):
        # Read the content of the `kvdeveloper/view_base/registers.py` file
        template_file_path = os.path.join(VIEW_BASE, "registers.py")
        with open(template_file_path, "r", encoding="utf-8") as template_file:
            content = template_file.read()

        with open(registers_file_path, "w", encoding="utf-8") as registers_file:
            registers_file.write(content)

        console.print(
            f"\nCreated file: [bright_white]{registers_file_path}[/bright_white]"
        )

    # Read the content of the `main.py` file
    with open(main_file_path, "r", encoding="utf-8") as main_file:
        content = main_file.read()

    # Regular expression to match import statements
    import_pattern = r"^(import\s+\S+|from\s+\S+\s+import\s+\S+)"

    # Search for import statements
    imports = re.findall(import_pattern, content, re.MULTILINE)

    # Check if 'import registers' is already present
    if "import registers" not in imports:
        # Find the last import statement
        last_import_match = re.search(
            f"({import_pattern})(\n|$)", content, re.MULTILINE
        )

        if last_import_match:
            # Insert 'import registers' after the last import statement
            insertion_point = last_import_match.end()
            updated_content = (
                content[:insertion_point]
                + "\nimport registers\n"
                + content[insertion_point:]
            )
        else:
            # If no import statement is found, add it at the beginning
            updated_content = "import registers\n" + content
    else:
        updated_content = content  # No change needed

    # Write the updated content back to the file
    with open(main_file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)


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
        `buildozer_action.ipynb`: Jupyter notebook for google colab environment.

    Setup build files for platforms Android and IOS.
    `Currently supporting Android conversions build system.`

    :param platform: Platform specific to setup build files.

    :param external: External Build Environment.
    """
    available_platforms = [
        "android",
    ]
    if not platform in available_platforms:
        typer.secho("\nUnavailable platform.", err=True)
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
    import pkg_resources

    try:
        pkg_resources.get_distribution("pyqt5")
        pkg_resources.get_distribution("pyqtwebengine")
    except pkg_resources.DistributionNotFound:
        typer.secho(
            f"Requires the following optional dependencies:\n - [bright_white]PyQt5[/bright_white]\n - [bright_white]PyQtWebEngine[/bright_white]"
        )
        raise typer.Exit(code=0)

    readme_path = os.path.join(directory, "README.md")
    if not os.path.isfile(readme_path):
        typer.echo(f"File '{readme_path}' not found.")
        raise typer.Exit(code=1)

    from kvdeveloper.info_reader import info_reader

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
    template_table.add_column("Name", style="bold cyan", width=21)
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
    structure_table.add_column("Name", style="bold cyan", width=21)
    structure_table.add_column("Description")
    for structure, description in STRUCTURES.items():
        structure_table.add_row(structure, description)
    structures_box = Panel(
        structure_table, title="Structures", title_align="left", expand=True
    )
    typer.secho(help_text, fg=typer.colors.BRIGHT_WHITE)
    console.print(structures_box)


@app.command()
def list_components() -> None:
    """
    List all available components.
    """
    help_text = Text("\n Available Components\n")
    component_table = Table(show_header=False, box=None)
    component_table.add_column("Name", style="bold cyan", width=21)
    component_table.add_column("Description")
    for component, description in COMPONENTS.items():
        component_table.add_row(component, description)
    components_box = Panel(
        component_table, title="Components", title_align="left", expand=True
    )
    typer.secho(help_text, fg=typer.colors.BRIGHT_WHITE)
    console.print(components_box)


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
