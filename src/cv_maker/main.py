import os
from pathlib import Path

from .backend import LatexEngine

from . import config

from .template import Template
from .loader import YamlLoader
from .protocols import DataLoader


def write_results_to_texfile(destination: str | Path, content: str) -> None:
    with open(destination, "w", encoding="utf-8") as file:
        file.write(content)


def main():
    config.BUILD_DIR.mkdir(parents=True, exist_ok=True)

    dataLoader: DataLoader = YamlLoader()

    template = Template(config.TEMPLATES)

    engine = LatexEngine()

    for file, name in dataLoader.load_all_files_in_dir(config.DATA_DIR):
        for data in file["languages"]:
            for form in config.FORMATS:
                template_path = Path(config.BUILD_DIR / name / form / data["language"])
                template_path.mkdir(parents=True, exist_ok=True)

                result = template.render(
                    f"template_{form}.tex", {**data, "image": config.PATH_TO_IMAGE}
                )

                write_results_to_texfile(
                    template_path / f"cv_{name}_{data['language']}_{form}.tex", result
                )
                os.chdir(template_path)
                print(os.getcwd())

                print("\n\n\n-------------------------------------")
                print(f"Compiling CV_Nazih_Boudaakkar_{name} {data['language']} {form}")
                print("-------------------------------------\n\n\n")

                engine.render(
                    file=(Path.cwd() / f"cv_{name}_{data['language']}_{form}.tex"),
                    output=f"CV_Nazih_Boudaakkar_{name}",
                    raise_on_exception=True,
                )


if __name__ == "__main__":
    main()
