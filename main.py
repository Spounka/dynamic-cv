from jinja2 import Environment, FileSystemLoader, Template
import yaml
import os
import subprocess
from pathlib import Path
from typing import TypedDict, List, Generator, Tuple, Literal

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
TEMPLATES = BASE_DIR / "template"
BUILD_DIR = BASE_DIR / "build"
PATH_TO_IMAGE = BASE_DIR / "images" / "NazihPicture3.jpg"

LANGS: List[Literal["en", "fr"]] = ["en", "fr"]
FORMATS = ["ats", "pretty"]


class EducationData(TypedDict):
    title: str
    date: str
    university: str


class Education(TypedDict):
    name: str
    data: List[EducationData]


class SkillData(TypedDict):
    title: str
    skills: List[str]


class Skill(TypedDict):
    name: str
    data: List[SkillData]


class Project(TypedDict):
    name: str
    date: str
    description: List[str]


class ExperienceData(TypedDict):
    title: str
    company: str
    projects: List[Project]


class Experience(TypedDict):
    name: str
    data: List[ExperienceData]


class SpokenLanguageData(TypedDict):
    name: str
    proficiency: str


class SpokenLanguage(TypedDict):
    name: str
    data: List[SpokenLanguageData]


class PersonalInfo(TypedDict):
    name: str
    course: str
    phone: str
    email: str
    address: str
    github: str
    linkedIn: str


class SummaryInfo(TypedDict):
    name: str
    details: str


class Language(TypedDict):
    personal_info: PersonalInfo
    summary: SummaryInfo
    education: Education
    technical_skills: Skill
    experiences: Experience
    spoken_languages: SpokenLanguage


class Languages(TypedDict):
    en: Language
    fr: Language


class CVData(TypedDict):
    languages: Languages


def list_yaml_files(directory: Path) -> List[Path]:
    """Lists all yaml files in directory and returns them in a list"""
    return [
        file
        for file in directory.iterdir()
        if file.is_file() and file.suffix in [".yml", ".yaml"]
    ]


def load_yaml_file(file: Path):
    """Opens a yaml file and parses it"""
    try:
        with open(file, "r") as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)
        return None


def load_data_files(path: Path) -> Generator[Tuple[CVData, str], None, None]:
    for file in list_yaml_files(path):
        data = load_yaml_file(file)
        if data:
            yield data, file.name.split(".")[0]


def render_template(template: Template, data: Language) -> str:
    """Renders a template with the data"""
    return template.render({**data, "image": PATH_TO_IMAGE})


def write_results_to_pdf(destination: str | Path, content: str) -> None:
    with open(destination, "w") as file:
        file.write(content)


def main():
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    env.comment_start_string = "{#%"
    env.comment_end_string = "%#}"
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    for file, name in load_data_files(DATA_DIR):
        if not file["languages"]["en"]["summary"]["details"]:
            continue

        for lang in LANGS:
            data = file["languages"][lang]

            for form in FORMATS:
                temp = Path(BUILD_DIR / name / form / lang)
                temp.mkdir(parents=True, exist_ok=True)

                template = env.get_template(f"template_{form}.tex")
                result = render_template(template, data)

                write_results_to_pdf(temp / f"cv_{name}_{lang}_{form}.tex", result)
                os.chdir(temp)
                print(os.getcwd())

                print("\n\n\n-------------------------------------")
                print(f"Compiling CV_Nazih_Boudaakkar_{name} {lang} {form}")
                print("-------------------------------------\n\n\n")

                return_code = subprocess.run(
                    [
                        "xelatex",
                        f'--jobname="CV_Nazih_Boudaakkar_{name}"',
                        f"./cv_{name}_{lang}_{form}.tex",
                    ]
                )
                if return_code:
                    print("completed with return code ", return_code)
        break


if __name__ == "__main__":
    main()
