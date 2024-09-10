import os
import typer
import platform
import sys
import subprocess
import re
from typing import Dict, List, Literal
from .config import TEMPLATES_DIR, TEMPLATES, STRUCTURES_DIR, STRUCTURES, VIEW_BASE
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.prompt import Prompt

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

    parsed_screens_list = []
    dir_list = os.listdir(f"{template_path}/View")
    for name_view in dir_list:
        if os.path.isdir(f"{template_path}/View/{name_view}"):
            # Parse screen name to PascalCase
            parsed_name = name_parser(name_view, "screen")
            parsed_screens_list.append(parsed_name)

    parsed_screens_string = " ".join(parsed_screens_list)

    python_version = platform.python_version()

    """
    There is no point of writing MVC implementation from scratch so I used subprocess to run KivyMD's inbuilt create_project script simplifying development workflow.
    """
    output = subprocess.run(
        f"{sys.executable} -m kivymd.tools.patterns.create_project MVC . {variables['project_name']} python{python_version} master --use_hotreload yes --name_screen {parsed_screens_string}",
        shell=True,
    )

    if output.returncode != 0:
        raise typer.Exit(code=1)

    """
    updating base screen components.
    """
    with open(
        f"{template_path}/View/base_screen.kv", "r", encoding="utf-8"
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
    Updating screen styles.
    """

    for name_view in parsed_screens_list:
        parsed_name = name_parser(name_view, "screen")
        snake_name_view = name_parser_snake(parsed_name)
        with open(
            f"{template_path}/View/{parsed_name}/{snake_name_view}.kv",
            "r",
            encoding="utf-8",
        ) as template_file:
            content = template_file.read()

        with open(
            f"{destination}/View/{parsed_name}/{snake_name_view}.kv",
            "w",
            encoding="utf-8",
        ) as target_file:
            target_file.write(content)

            console.print(
                f"Updated file: [bright_white]{destination}/View/{parsed_name}/{snake_name_view}.kv[/bright_white]"
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
    if os.name == "nt":
        envbin = "scripts"
    else:
        envbin = "bin"
    console.print(f"\n[green]Installing requirements with pip.[/green]\n")
    try:
        subprocess.run(
            [
                f"{variables['project_name']}\\venv\\{envbin}\\python",
                "-m",
                "pip",
                "install",
                "-r",
                f"{destination}/requirements.txt",
            ],
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
    # from kivymd._version import __version__ as kivymd_version
    # from kivy._version import __version__ as kivy_version

    install_variables = {
        "kivymd_version": "1.1.1",
        "kivy_version": "2.3.0",
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


def add_from_default(
    name_screen: List[str], use_template: str, destination: str
) -> None:
    """
    Add screens to the project with a specified template and a default structure.

    :param name_screen: A list of screen names to be added.
    :param use_template: The template name to be used for creating the view if it pre-exists.
    :param destination: The destination path where the files will be created.
    """
    for name_view in name_screen:
        # Parse screen name to PascalCase
        parsed_name = name_parser(name_view, "screen")
        # A snake that parses a name.
        snake_name_view = name_parser_snake(parsed_name)
        console.print(
            f"Creating Screen with name [bold cyan]{parsed_name}[/bold cyan]."
        )

        # Construct the view path
        view_path = os.path.join(destination, parsed_name)

        if not os.path.isdir(view_path):
            variables = {"parsed_name": parsed_name}
            try:
                # Construct the template path
                template_path = os.path.join(
                    TEMPLATES_DIR, f"{use_template}/View/{parsed_name}"
                )

                if not os.path.isdir(template_path):
                    # Template does not exist; create files with a blank template
                    if use_template:
                        typer.echo(
                            f"View '{parsed_name}' not found in template '{use_template}'. Creating '{parsed_name}' with a blank template."
                        )
                    os.makedirs(view_path, exist_ok=True)

                    # Create the .py file using the default template
                    with open(
                        f"{VIEW_BASE}/default_screen.py", "r", encoding="utf-8"
                    ) as view_file:
                        content = view_file.read()
                    content = replace_placeholders(content, variables)
                    with open(
                        f"{view_path}/{snake_name_view}.py", "w", encoding="utf-8"
                    ) as target_file:
                        target_file.write(content)
                        console.print(
                            f"\nCreated file: [bright_white]{view_path}/{snake_name_view}.py[/bright_white]"
                        )

                    # Create the .kv file using the default template
                    with open(
                        f"{VIEW_BASE}/default_screen.kv", "r", encoding="utf-8"
                    ) as view_file:
                        content = view_file.read()

                    content = replace_placeholders(content, variables)

                    with open(
                        f"{view_path}/{snake_name_view}.kv", "w", encoding="utf-8"
                    ) as target_file:
                        target_file.write(content)

                        console.print(
                            f"\nCreated file: [bright_white]{view_path}/{snake_name_view}.kv[/bright_white]"
                        )
                    update_screens_file(parsed_name, snake_name_view, destination)

                    # Create an empty __init__.py File
                    with open(
                        f"{view_path}/__init__.py", "w", encoding="utf-8"
                    ) as init_file:
                        init_file.write("# Empty __init__.py file")

                elif os.path.isdir(template_path):
                    # Template exists; copy and process files from the template
                    for root, _, files in os.walk(template_path):
                        relative_path = os.path.relpath(root, template_path)
                        target_dir = os.path.join(destination, relative_path)
                        os.makedirs(target_dir, exist_ok=True)

                        for file_name in files:
                            template_file_path = os.path.join(root, file_name)
                            target_file_path = os.path.join(target_dir, file_name)

                            # Read and process each template file
                            with open(
                                template_file_path, "r", encoding="utf-8"
                            ) as template_file:
                                content = template_file.read()
                            content = replace_placeholders(content, variables)
                            with open(
                                target_file_path, "w", encoding="utf-8"
                            ) as target_file:
                                target_file.write(content)

                                console.print(
                                    f"Created file: [bright_white]{target_file_path}[/bright_white]"
                                )
                            update_screens_file(
                                parsed_name, snake_name_view, destination
                            )
            except Exception as e:
                typer.secho(f"Error: {e}", err=True)
        else:
            console.print(
                f"Screen with name [green]{parsed_name}[/green] already exists. Try a different name."
            )


def update_screens_file(
    parsed_name: str, snake_name_view: str, destination: str
) -> None:
    """
    Updates the screens.py file by adding the import statement and the screen entry.

    :param parsed_name: The name of the screen class (e.g., 'MyScreen').
    :param snake_name_view: The name of the screen in snake_case (e.g., 'my_screen').
    :param destination: The destination path where the files is located.
    """

    # Define the paths and patterns
    file_path = os.path.join(destination, "screens.py")
    import_statement = (
        f"from View.{parsed_name}.{snake_name_view} import {parsed_name}View\n"
    )
    screen_entry = f"\n    '{snake_name_view.replace('_', ' ')}': {{\n        'object': {parsed_name}View(),\n    }},"

    # Read the contents of the screens.py file
    with open(file_path, "r") as file:
        content = file.read()

    # Check if the import statement already exists
    if re.search(re.escape(import_statement.strip()), content):
        print(f"The import statement for {parsed_name}View already exists.")
    else:
        # Insert the import statement at the top of the file (after the first import block)
        # Finds the first occurrence of `from View...` and inserts new import below it
        content = re.sub(
            r"(from View\..*\n)+", r"\g<0>" + import_statement, content, count=1
        )

    # Check if the screen entry already exists
    screen_key = snake_name_view.replace("_", " ")
    if re.search(re.escape(f"'{screen_key}':"), content):
        print(f"The screen entry for {snake_name_view} already exists.")
    else:
        # Insert the new screen entry before the last closing curly brace of the dictionary
        content = re.sub(
            r"(\n\s*}\s*)$",  # This looks for the last closing curly brace
            screen_entry + r"\g<1>",  # Insert the new screen entry before it
            content,
        )

    # Write the updated content back to the screens.py file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    console.print(
        f"[bright cyan]screens.py[/bright cyan] has been successfully updated with {parsed_name}View."
    )


def add_from_structure(
    name_screen: List[str], use_template: str, destination: str
) -> None:
    """
    Add screens to the project using a custom structure.

    :param name_screen: A list of screen names to be added.
    :param use_template: The template name to be used for creating the view.
    :param destination: The destination path where the files will be created.
    :param structure: The custom structure to follow when creating the screens.
    """
    parsed_screens_list = []
    for name_view in name_screen:
        # Parse screen name to PascalCase
        parsed_name = name_parser(name_view, "screen")
        parsed_screens_list.append(parsed_name)

    parsed_screens_string = " ".join(parsed_screens_list)

    output = subprocess.run(
        f"{sys.executable} -m kivymd.tools.patterns.add_view MVC . {parsed_screens_string}",
        shell=True,
    )

    if output.returncode != 0:
        console.print(
            "\nThis project may not be following [green]MVC[/green] architecture.\n"
        )
        prompt = Prompt.ask(
            f"Want to add screen using structure [[green]none: {STRUCTURES[structure]}[/green]] ?",
            choices=["y", "n"],
            default="n",
        )
        if prompt == "y":
            add_from_default(name_screen, use_template, destination)
        else:
            raise typer.Exit(code=1)

    for parsed_name in parsed_screens_list:
        # Construct the template path
        template_path = os.path.join(
            TEMPLATES_DIR, f"{use_template}/View/{parsed_name}"
        )

        # Construct the view path
        view_path = os.path.join(destination, parsed_name)

        # A snake that parses a name.
        snake_name_view = name_parser_snake(parsed_name)

        variables = {"parsed_name": parsed_name}

        if not os.path.isdir(template_path):
            # Template does not exist;
            if use_template:
                typer.echo(
                    f"View '{parsed_name}' not found in template '{use_template}'."
                )
        elif os.path.isdir(template_path):
            # Template exists; process files from the template
            with open(
                f"{template_path}/{snake_name_view}.kv", "r", encoding="utf-8"
            ) as template_file:
                content = template_file.read()

            content = replace_placeholders(content, variables)

            with open(
                f"{view_path}/{snake_name_view}.kv", "w", encoding="utf-8"
            ) as target_file:
                target_file.write(content)

                console.print(
                    f"\nUpdated file: [bright_white]{view_path}/{snake_name_view}.kv[/bright_white]"
                )


def name_parser_snake(name: str) -> str:
    """
    Convert a PascalCase name to snake_case.

    :param name: The name to be converted.
    :return: The converted snake_case name.
    """
    # Convert name to lowercase and ensure 'screen' is separated with '_'
    snake_case = name.lower()
    snake_case = re.sub(r"_?screen", "_screen", snake_case)
    return snake_case


def name_parser(name: str, parse_type: Literal["screen", "project"]) -> str:
    """
    Parse the name according to the given parse type.

    :param name: The name to be parsed.
    :param parse_type: The type of parsing to perform ("screen" or "project").
    :return: The parsed name in PascalCase.
    :raises ValueError: If the name is invalid.
    :raises TypeError: If the parse type is invalid.
    """
    name = name.lower()

    if parse_type == "screen":
        # Validate and format screen name
        if name and name[0].isdigit():
            raise ValueError("The name of the screen should not start with a number.")
        elif "screen" not in name:
            name += "Screen"
        elif name.lower() == "screen":
            raise ValueError(
                "The name of the screen cannot be only 'screen' or 'Screen'."
            )

        # Extract and capitalize words
        words = re.split(r"[^a-zA-Z0-9]", name)
        pascal_case = "".join(
            word.capitalize() if word.lower() != "screen" else "Screen"
            for word in words
            if word
        )
        pascal_case = re.sub(r"Screen", "Screen", pascal_case, flags=re.IGNORECASE)
    elif parse_type == "project":
        # Validate and format project name
        if name and name[0].isdigit():
            raise ValueError("The name of the project should not start with a number.")
        elif "app" not in name:
            name += "App"
        elif name.lower() == "app":
            raise ValueError("The name of the project cannot be only 'app' or 'App'.")

        # Extract and capitalize words
        words = re.split(r"[^a-zA-Z0-9]", name)
        pascal_case = "".join(
            word.capitalize() if word.lower() != "app" else "App"
            for word in words
            if word
        )
        pascal_case = re.sub(r"App", "App", pascal_case, flags=re.IGNORECASE)
    else:
        raise TypeError(
            f"Invalid parse type: '{parse_type}'. Should be one of ['screen', 'project']"
        )

    return pascal_case
