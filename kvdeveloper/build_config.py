import os, typer

from kvdeveloper.config import BUILD_DIR
from kvdeveloper.module import console


def generate_build_files(platform: str, external: str) -> None:
    """
    Create necessary build files.

    :param external: External Build Environment.
    """
    external_path = os.path.join(BUILD_DIR, external)
    if not os.path.isdir(external_path):
        console.print(f"External environment '{external}' not found.")
        raise typer.Exit(code=1)

    if external == "colab":
        external_file_path = os.path.join(external_path, "buildozer_action.ipynb")
        destination_file_path = os.path.join(
            os.getcwd(), "colab", "buildozer_action.ipynb"
        )
        os.makedirs("colab", exist_ok=True)
        with open(external_file_path, "r", encoding="utf-8") as target_file:
            content = target_file.read()

        with open(destination_file_path, "w", encoding="utf-8") as template_file:
            template_file.write(content)

            console.print(f"Created file {destination_file_path}.")

    elif external == "github":
        external_file_path = os.path.join(
            external_path, f"buildozer_{platform}_action.yml"
        )
        os.makedirs(".github/workflows", exist_ok=True)
        destination_file_path = os.path.join(
            os.getcwd(), ".github", "workflows", f"buildozer_{platform}_action.yml"
        )
        with open(external_file_path, "r", encoding="utf-8") as target_file:
            content = target_file.read()

        with open(destination_file_path, "w", encoding="utf-8") as template_file:
            template_file.write(content)

            console.print(f"Created file {destination_file_path}.")
