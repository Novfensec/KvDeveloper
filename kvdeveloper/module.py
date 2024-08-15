import os
import typer
from typing import Optional, Dict
from .config import TEMPLATES_DIR, TEMPLATES, STRUCTURES_DIR, STRUCTURES, VIEW_BASE
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
import platform
import subprocess

console = Console()


def replace_placeholders(content: str, variables: Dict[str, str]) -> str:
    """
    Replace placeholders in the content with provided variables.

    :param content: The content with placeholders.
    :param variables: A dictionary of variables to replace in the content.
    :return: The content with replaced variables.
    """
    for placeholder, value in variables.items():
        content = content.replace(f"{{{{{placeholder}}}}}", value)
    return content


def create_from_template(
    template_name: str, destination: str, variables: Dict[str, str]
) -> None:
    """
    Create project files from a template, replacing placeholders with specified variables.

    :param template_name: The name of the template folder.
    :param destination: The destination path where files should be created.
    :param variables: A dictionary of variables to replace in the template files.
    """
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.isdir(template_path):
        typer.echo(f"Template '{template_name}' not found.")
        raise typer.Exit(code=1)

    for root, _, files in os.walk(template_path):
        relative_path = os.path.relpath(root, template_path)
        target_dir = os.path.join(destination, relative_path)
        os.makedirs(target_dir, exist_ok=True)

        for file_name in files:
            template_file_path = os.path.join(root, file_name)
            target_file_path = os.path.join(target_dir, file_name)

            with open(template_file_path, "r", encoding="utf-8") as template_file:
                content = template_file.read()

            content = replace_placeholders(content, variables)

            with open(target_file_path, "w", encoding="utf-8") as target_file:
                target_file.write(content)

            console.print(
                f"Created file: [bright_white]{target_file_path}[/bright_white]"
            )

    """
    Updating requirements.txt.
    """
    update_requirements(template_path, destination)


def create_from_structure(
    template_name: str, structure_name: str, destination: str, variables: Dict[str, str]
) -> None:
    """
    Create project files from a structure, replacing placeholders with specified variables.

    :param template_name: The name of the template folder.
    :param structure_name: The name of the structure folder.
    :param destination: The destination path where files should be created.
    :param variables: A dictionary of variables to replace in the structure files.
    """
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.isdir(template_path):
        typer.echo(f"Template '{template_name}' not found.")
        raise typer.Exit(code=1)

    structure_path = os.path.join(STRUCTURES_DIR, structure_name)
    if not os.path.isdir(structure_path):
        typer.echo(f"Structure '{structure_name}' not found.")
        raise typer.Exit(code=1)

    version = platform.python_version()

    """
    There is no point of writing MVC implementation from scratch so I used subprocess to run KivyMD's inbuilt create_project script simplifying development workflow.
    """

    if template_name == "blank":
        output = subprocess.run(
            [
                "python",
                "-m",
                "kivymd.tools.patterns.create_project",
                "MVC",
                ".",
                f"{variables['project_name']}",
                f"python{version}",
                "master",
                "--use_hotreload",
                "yes",
                "--name_screen",
                "SampleScreen",
            ]
        )

        if output.returncode != 0:
            raise typer.Exit(code=1)

        with open(
            f"{template_path}/View/SampleScreen/sample_screen.kv", "r", encoding="utf-8"
        ) as template_file:
            content = template_file.read()

        with open(
            f"{destination}/View/SampleScreen/sample_screen.kv", "w", encoding="utf-8"
        ) as target_file:
            target_file.write(content)

            console.print(
                f"Updated file: [bright_white]{destination}/View/SampleScreen/sample_screen.kv[/bright_white]"
            )

    elif template_name == "nav_toolbar":
        output = subprocess.run(
            [
                "python",
                "-m",
                "kivymd.tools.patterns.create_project",
                "MVC",
                ".",
                f"{variables['project_name']}",
                f"python{version}",
                "master",
                "--use_hotreload",
                "yes",
                "--name_screen",
                "HomeScreen",
                "LoginScreen",
            ]
        )

        if output.returncode != 0:
            raise typer.Exit(code=1)

        """
        updating home screen styles.
        """
        with open(
            f"{template_path}/View/HomeScreen/home_screen.kv", "r", encoding="utf-8"
        ) as template_file:
            content = template_file.read()

        with open(
            f"{destination}/View/HomeScreen/home_screen.kv", "w", encoding="utf-8"
        ) as target_file:
            target_file.write(content)

            console.print(
                f"Updated file: [bright_white]{destination}/View/HomeScreen/home_screen.kv[/bright_white]"
            )

        """
        updating base screen components.
        """
        with open(
            f"{template_path}/View/Components/components.kv", "r", encoding="utf-8"
        ) as template_file:
            content = template_file.read()

        with open(
            f"{destination}/View/base_screen.kv", "w", encoding="utf-8"
        ) as target_file:
            target_file.write(content)

            console.print(
                f"Updated file: [bright_white]{destination}/View/base_screen.kv[/bright_white]"
            )

        """
        updating login screen styles.
        """
        with open(
            f"{template_path}/View/LoginScreen/login_screen.kv", "r", encoding="utf-8"
        ) as template_file:
            content = template_file.read()

        with open(
            f"{destination}/View/LoginScreen/login_screen.kv", "w", encoding="utf-8"
        ) as target_file:
            target_file.write(content)

            console.print(
                f"Updated file: [bright_white]{destination}/View/LoginScreen/login_screen.kv[/bright_white]"
            )

    """
    updating main.py.
    """
    with open(f"{VIEW_BASE}/main.py", "r", encoding="utf-8") as template_file:
        content = template_file.read()

    content = replace_placeholders(content, variables)

    with open(f"{destination}/main.py", "w", encoding="utf-8") as target_file:
        target_file.write(content)

        console.print(
            f"Updated file: [bright_white]{destination}/main.py[/bright_white]"
        )

    """
    updating README.md.
    """
    with open(f"{template_path}/README.md", "r", encoding="utf-8") as template_file:
        content = template_file.read()

    with open(f"{destination}/README.md", "w", encoding="utf-8") as target_file:
        target_file.write(content)

        console.print(
            f"Updated file: [bright_white]{destination}/README.md[/bright_white]"
        )

    """
    Updating requirements.txt.
    """
    update_requirements(template_path, destination)

    """
    Installing requirements with pip.
    """
    console.print(f"\n[green]Installing requirements with pip.[/green]\n")
    try:
        subprocess.run(
            [
                f"{variables['project_name']}\\venv\scripts\python",
                "-m",
                "pip",
                "install",
                "-r",
                f"{destination}/requirements.txt",
            ]
        )
    except Exception as e:
        console.print(f"[bold red]{e}[/bold red]")


def setup_build(project_name: str, destination: str, variables: Dict[str, str]) -> None:
    """
    Create buildozer.spec, replacing placeholders with specified variables.

    :param project_name: The name of the project.
    :param destination: The destination path where file should be created.
    :param variables: A dictionary of variables to replace in the structure files.
    """
    with open(f"{VIEW_BASE}/buildozer.spec", "r", encoding="utf-8") as build_file:
        content = build_file.read()

    content = replace_placeholders(content, variables)

    with open(
        f"{destination}/buildozer.spec", "w", encoding="utf-8"
    ) as target_build_file:
        target_build_file.write(content)

        console.print(
            f"\nCreated file: [bold cyan]{destination}/buildozer.spec[/bold cyan]\n"
        )


def project_info(project_name, template, structure, destination) -> None:
    """
    Display Project Info.

    :param project_name: The name of the project.
    :param template_name: The name of the template folder.
    :param structure_name: The name of the structure folder.
    :param destination: The destination path where files are created.
    """
    console.print(
        f"\nProject [bold white]{project_name}[/bold white] creation [bold green]SUCCESSFULL[/bold green].\n"
    )
    info_table = Table(show_header=False, box=None)
    info_table.add_column("Info", style="bold cyan", width=21)
    info_table.add_column("Description")
    info_table.add_row("Template", TEMPLATES[template])
    info_table.add_row("Structure", STRUCTURES[structure])
    info_panel = Panel(
        info_table,
        title=f"{project_name} - Info",
        title_align="left",
        border_style="bold green",
        padding=1,
    )
    console.print(info_panel)

    dir_list = os.listdir(destination)
    tree = Tree(f"{project_name}", style="bold magenta")
    for entry in dir_list:
        tree.add(entry, style="bold cyan")
    tree_panel = Panel(
        tree,
        title="File Tree",
        border_style="bold green",
        title_align="left",
        padding=1,
    )
    console.print(tree_panel)
    console.print(f"\n[bold yellow]Happy Coding![/bold yellow]\n")


def update_requirements(template_path: str, destination: str) -> None:
    """
    Updating requirements.txt.
    :param template_path: The path of the template folder.
    :param destination: The destination path where files are created.
    """
    from kivymd._version import __version__ as kivymd_version
    from kivy._version import __version__ as kivy_version

    install_variables = {
        "kivymd_version": kivymd_version,
        "kivy_version": kivy_version,
    }
    with open(
        f"{template_path}/requirements.txt", "r", encoding="utf-8"
    ) as template_file:
        content = template_file.read()

    content = replace_placeholders(content, install_variables)

    with open(f"{destination}/requirements.txt", "w", encoding="utf-8") as target_file:
        target_file.write(content)

        console.print(
            f"\nUpdated file: [bright_white]{destination}/requirements.txt[/bright_white]"
        )
