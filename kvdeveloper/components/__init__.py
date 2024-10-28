import os
from kivy.logger import Logger
from kivy.lang import Builder
from kvdeveloper import __version__
from kvdeveloper.config import COMPONENTS_DIR, def_dir
import kvdeveloper.components.factory_registers

for root, _, files in os.walk(COMPONENTS_DIR):
    for file in files:
        file_path = os.path.join(root, file)
        if file.endswith(".kv"):
            with open(file_path, "r", encoding="utf-8") as kv_file:
                content = kv_file.read()
            if not file in [os.path.basename(kv_files) for kv_files in Builder.files]:
                Builder.load_string(content, filename=file)


Logger.info(f"KvDeveloper: {__version__}")
Logger.info(f"KvDeveloper: Installed at {def_dir}")
