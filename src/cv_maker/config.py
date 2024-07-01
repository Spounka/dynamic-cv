from pathlib import Path
from typing import List, Literal


BASE_DIR = Path(__file__).parent.parent.parent.resolve()
DATA_DIR = BASE_DIR / "src" / "data"
TEMPLATES = BASE_DIR / "src" / "template"
BUILD_DIR = BASE_DIR / "build"
PATH_TO_IMAGE = BASE_DIR / "src" / "images" / "NazihPicture3.jpg"

LANGS: List[Literal["en", "fr"]] = ["en", "fr"]
FORMATS = ["ats", "pretty"]
