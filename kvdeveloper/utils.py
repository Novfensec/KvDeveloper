from typing import Dict, Literal
import re

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
