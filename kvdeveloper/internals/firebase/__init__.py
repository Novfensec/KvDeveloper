import io
import json
import os
from pathlib import Path

import requests

from kvdeveloper.config import console
from kvdeveloper.utils import extract_tar_file


def read_gradle_json(path: str):
    """
    gradle.json from path to dict
    :param path: Path of the gradle.json
    :return:
        Python dict with the keywords ['classpath', 'plugin', 'bom', 'dep']
        For each of the keys it does set(value) to avoid duplicates.
    """
    gradle_json = {"classpath": [], "plugin": [], "bom": [], "dep": []}

    if os.path.exists(path):
        with open(path, "r", encoding="UTF-8") as file:
            g_json = json.load(file)
            for k, v in g_json.items():
                if gradle_json.get(k) is not None:
                    gradle_json[k].extend(v)
                    gradle_json[k] = list(set(gradle_json[k]))

                else:
                    raise ValueError(f"Key does not belong to {gradle_json.keys()}")
    return gradle_json


def clone_p4a(p4a_dir: str, url: str):
    with requests.get(url, stream=True, timeout=3) as response:
        response.raise_for_status()
        with open(f"{p4a_dir}.tar.gz", "wb") as file:
            for chunk in response.iter_content(chunk_size=io.DEFAULT_BUFFER_SIZE):
                file.write(chunk)

    extract_tar_file(f"{p4a_dir}.tar.gz", Path(p4a_dir).parent)
    console.print(f"Removing: {p4a_dir}.tar.gz")
    os.remove(f"{p4a_dir}.tar.gz")

    with open("buildozer.spec", "r", encoding="utf-8") as build_file:
        content = build_file.readlines()

    with open("buildozer.spec", "w", encoding="utf-8") as target_build_file:
        for line in content:
            # Comment line with p4a.source_dir
            if line.lstrip().startswith("p4a.source_dir"):
                line = f"#{line}"

            target_build_file.write(line)

        line = f"p4a.source_dir = {p4a_dir}"
        console.print(f"Inserting at buildozer.spec: {line}")
        target_build_file.write(f"{line}\n")
