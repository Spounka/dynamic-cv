import subprocess
from pathlib import Path


class LatexEngine:
    def render(
        self, file: Path, output: str = "default", raise_on_exception: bool = False
    ):
        if not file.exists():
            raise IOError(f"File {file.resolve()} does not exist")
        if file.suffix != ".tex":
            raise ValueError("File is not a tex file")

        result = subprocess.run(
            ["xelatex", f"--jobname={output}", file.resolve()], check=True
        )
        if raise_on_exception:
            result.check_returncode()
