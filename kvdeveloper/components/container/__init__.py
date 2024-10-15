import os
from .container import Container
from kivy.lang import Builder
from pathlib import Path

with open(
    os.path.join(Path(__file__).parent, "container.kv"), "r", encoding="utf-8"
) as kv_file:
    content = kv_file.read()
    if not "Container.kv" in Builder.files:
        Builder.load_string(content, filename="Container.kv")