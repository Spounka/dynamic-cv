import yaml
import os
import subprocess
from pathlib import Path
from typing import TypedDict, List, Generator

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
TEMPLATES = BASE_DIR / "template"

LANGS = ['en', 'fr']
FORMATS = ['ats', 'pretty']


class Education(TypedDict):
    title: str
    date: str
    university: str


class Skill(TypedDict):
    title: str
    skills: List[str]


class Project(TypedDict):
    name: str
    date: str
    description: List[str]


class Experience(TypedDict):
    title: str
    company: str
    projects: List[Project]


class SpokenLanguage(TypedDict):
    name: str
    proficiency: str


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
    education: List[Education]
    technical_skills: List[Skill]
    experiences: List[Experience]
    spoken_languages: List[SpokenLanguage]


class Languages(TypedDict):
    en: Language
    fr: Language


class CVData(TypedDict):
    languages: Languages


def list_yaml_files(directory: Path) -> List[Path]:
    """Lists all yaml files in directory and returns them in a list"""
    return [file for file in directory.iterdir() if file.is_file() and file.suffix in ['yml', 'yaml']]


def load_yaml_file(file: Path):
    """Opens a yaml file and parses it"""
    try:
        with open(file, 'r') as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)
        return None


def load_data_files(dir: Path) -> Generator[CVData, None, None]:
    for file in list_yaml_files(dir):
        data = load_yaml_file(file)
        if data:
            yield data


def main():
    for file in load_data_files(DATA_DIR):
        if file.get('languages', None).get('en', None).get("summary", None).get("name", None):
            print(file['languages']['en']['summary']['details'])


if __name__ == "__main__":
    main()
