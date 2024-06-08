from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader
import yaml
import os
import subprocess
from pathlib import Path
from typing import TypedDict, List, Generator

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
TEMPLATES = BASE_DIR / "template"


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


def load_data_files() -> Generator[CVData, None, None]:
    for file in DATA_DIR.iterdir():
        if file.is_file() and file.suffix in [".yaml", ".yml"]:
            with open(file, 'r') as stream:
                try:
                    yield yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)


def main():
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    for file in load_data_files():
        if file.get('languages', None).get('en', None).get("summary", None).get("name", None):
            print(file['languages']['en']['summary']['details'])
            print(env.get_template("Template ATS.tex.jinja").render(file.get("languages", None).get('en', None)))


if __name__ == "__main__":
    main()
