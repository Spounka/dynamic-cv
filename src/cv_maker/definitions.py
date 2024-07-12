import sys
from typing import Generic, List, TypeVar

if sys.version_info < (3, 11):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict

T = TypeVar("T")


class LabeledData(TypedDict, Generic[T]):
    title: str
    data: List[T]


class Education(TypedDict):
    title: str
    date: str
    university: str


class SkillCategory(TypedDict):
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


class CVData(TypedDict):
    language: str
    personal_info: PersonalInfo
    summary: SummaryInfo
    education: LabeledData[Education]
    technical_skills: LabeledData[SkillCategory]
    experiences: LabeledData[Experience]
    spoken_languages: LabeledData[SpokenLanguage]


class MultilangCVData(TypedDict):
    languages: List[CVData]
