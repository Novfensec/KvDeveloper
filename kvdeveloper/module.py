import os
import typer
import platform
import subprocess
import re
from typing import Dict, List
from kvdeveloper.utils import (
    name_parser,
    name_parser_snake,
    replace_placeholders,
)
from kvdeveloper.config import (
    TEMPLATES_DIR,
    TEMPLATES,
    STRUCTURES_DIR,
    STRUCTURES,
    LAYOUTS_DIR,
    VIEW_BASE,
)
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.prompt import Prompt

console = Console()


def add_extensions(
    template_name: str, destination: str, layout_name: str = None, index: str = "1"
) -> None:
    """
    Adds extensions.py to required dirs.
    """
    if layout_name != None:
        template_path = os.path.join(LAYOUTS_DIR, layout_name, index)
    else:
        template_path = os.path.join(TEMPLATES_DIR, template_name)

    if not os.path.isdir(template_path):
        typer.echo(f"Path '{template_path}' not found.")
        raise typer.Exit(code=1)

    for root, _, files in os.walk(template_path):
        relative_path = os.path.relpath(root, template_path)
        target_dir = os.path.join(destination, relative_path)

        for file_name in files:
            if file_name == "extensions.py":
                template_file_path = os.path.join(root, file_name)
                target_file_path = os.path.join(target_dir, file_name)

                with open(template_file_path, "r", encoding="utf-8") as template_file:
                    content = template_file.read()

                with open(target_file_path, "w", encoding="utf-8") as target_file:
                    target_file.write(content)

                console.print(
                    f"Created file: [bright_white]{target_file_path}[/bright_white]"
                )


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
            # Skip .pyc and .pyo files
            if file_name.endswith((".pyc", ".pyo")):
                continue
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
        if name_view == "__pycache__":
            continue
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
        f"python -m kivymd.tools.patterns.create_project MVC . {variables['project_name']} python{python_version} master --use_hotreload yes --name_screen {parsed_screens_string}",
        shell=True,
    )

    if output.returncode != 0:
        raise typer.Exit(code=1)

    """
    ipdating base screen components.
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
    updating screen styles.
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
    adding extended functions and classes.
    """
    add_extensions(template_name, destination)

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
    envbin = "bin"
    if os.name == "nt":
        envbin = "scripts"
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
    from kvdeveloper import __version__ as kvdeveloper_version

    install_variables = {
        "kvdeveloper_version": kvdeveloper_version,
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
                            # Skip .pyc and .pyo files
                            if file_name.endswith((".pyc", ".pyo")):
                                continue
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
    name_screen: List[str],
    destination: str,
    use_template: str = None,
    layout: str = None,
) -> None:
    """
    Add screens to the project using a custom structure.

    :param name_screen: A list of screen names to be added.
    :param use_template: The template name to be used for creating the view.
    :param destination: The destination path where the files will be created.
    """
    parsed_screens_list = []
    for name_view in name_screen:
        if name_view == "__pycache__":
            continue
        # Parse screen name to PascalCase
        parsed_name = name_parser(name_view, "screen")
        parsed_screens_list.append(parsed_name)

    parsed_screens_string = " ".join(parsed_screens_list)

    output = subprocess.run(
        f"python -m kivymd.tools.patterns.add_view MVC . {parsed_screens_string}",
        shell=True,
    )

    if output.returncode != 0:
        console.print(
            "\nThis project may not be following [green]MVC[/green] architecture.\n"
        )
        prompt = Prompt.ask(
            f"Want to add screen using structure [[green]none: {STRUCTURES['none']}[/green]] ?",
            choices=["y", "n"],
            default="n",
        )
        if prompt == "y":
            add_from_default(name_screen, use_template, destination)
            apply_layout(name_screen, layout, destination)
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
            apply_layout(name_screen, layout, destination)
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
            add_extensions(f"{use_template}/View", destination)


def add_from_layout(name_screen: List[str], layout: str, destination: str):
    """
    Add screens to the project with a specified layout and a default structure.

    :param name_screen: A list of screen names to be added.
    :param layout: The layout of the screen.
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
                # Construct the layout path

                layout = name_parser(layout, "screen").strip("Screen")
                layout, index = re.findall(r"[A-Za-z]+|\d+", layout)
                layout_path = os.path.join(LAYOUTS_DIR, layout, index)

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

                # Create an empty __init__.py File
                with open(
                    f"{view_path}/__init__.py", "w", encoding="utf-8"
                ) as init_file:
                    init_file.write("# Empty __init__.py file")

                if not os.path.isdir(layout_path):
                    # Layout does not exist; create files with a blank template
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

                elif os.path.isdir(layout_path):
                    # Layout exists; copy and process files from the layout
                    # Create the .kv file using the layout
                    name_layout = name_parser(layout, "screen")
                    snake_name_layout = name_parser_snake(name_layout)
                    with open(
                        f"{layout_path}/{snake_name_layout}.kv", "r", encoding="utf-8"
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
                    add_extensions(
                        template_name=None,
                        destination=view_path,
                        layout_name=layout,
                        index=index,
                    )
                update_screens_file(parsed_name, snake_name_view, destination)
            except Exception as e:
                typer.secho(f"Error: {e}", err=True)
        else:
            console.print(
                f"Screen with name [green]{parsed_name}[/green] already exists. Try a different name."
            )


def apply_layout(name_screen: List[str], layout: str, destination: str):
    """
    Apply layout to a screen with specified layout type.

    :param name_screen: The list containing the names of the screens.
    :param layout: The name of the layout for the screens.
    :param destination: The destination path where the files will be created and updated.
    """
    layout = name_parser(layout, "screen").strip("Screen")
    layout, index = re.findall(r"[A-Za-z]+|\d+", layout)
    layout_path = os.path.join(LAYOUTS_DIR, layout, index)
    if not os.path.isdir(layout_path):
        typer.echo(f"Layout '{layout}' not found.")
        raise typer.Exit(code=1)

    parsed_screens_list = []
    for name_view in name_screen:
        if name_view == "__pycache__":
            continue
        # Parse screen name to PascalCase
        parsed_name = name_parser(name_view, "screen")
        parsed_screens_list.append(parsed_name)

    # Parse required names for the layout
    name_layout = name_parser(layout, "screen")
    snake_name_layout = name_parser_snake(name_layout)

    for parsed_name in parsed_screens_list:
        # Construct the view path
        view_path = os.path.join(destination, parsed_name)
        # A snake that parses a name.
        snake_name_view = name_parser_snake(parsed_name)

        if os.path.isdir(view_path):
            variables = {"parsed_name": parsed_name}
            try:
                with open(
                    f"{layout_path}/{snake_name_layout}.kv", "r", encoding="utf-8"
                ) as view_file:
                    content = view_file.read()

                content = replace_placeholders(content, variables)

                with open(
                    f"{view_path}/{snake_name_view}.kv", "w", encoding="utf-8"
                ) as target_file:
                    target_file.write(content)

                    console.print(
                        f"\nUpdated file: [bright_white]{view_path}/{snake_name_view}.kv[/bright_white]"
                    )
                add_extensions(
                    template_name=None,
                    destination=view_path,
                    layout_name=layout,
                    index=index,
                )
            except Exception as e:
                typer.secho(f"Error: {e}", err=True)
        else:
            console.print(
                f"Screen with name [green]{parsed_name}[/green] does not exists. Try a different name."
            )
