import os
import kvdeveloper.components.factory_registers
from kivy.lang import Builder
from kvdeveloper.config import COMPONENTS_DIR

for root, _, files in os.walk(COMPONENTS_DIR):
    for file in files:
        file_path = os.path.join(root, file)
        if file.endswith(".kv"):
            with open(
                file_path, "r", encoding="utf-8"
            ) as kv_file:
                content = kv_file.read()
            if not file in [os.path.basename(kv_files) for kv_files in Builder.files]:
                Builder.load_string(content, filename=file)