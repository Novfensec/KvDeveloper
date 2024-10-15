import os
from .itdcard import ITDCard
from kivy.lang import Builder
from pathlib import Path

with open(
    os.path.join(Path(__file__).parent, "itdcard.kv"), "r", encoding="utf-8"
) as kv_file:
    content = kv_file.read()
    if not "ITDCard.kv" in Builder.files:
        Builder.load_string(content, filename="ITDCard.kv")