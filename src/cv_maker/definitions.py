from typing import List
from typing_extensions import TypedDict


class LabeledData[T](TypedDict):
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
    personal_info: PersonalInfo
    summary: SummaryInfo
    education: LabeledData[List[Education]]
    technical_skills: LabeledData[List[SkillCategory]]
    experiences: LabeledData[List[Experience]]
    spoken_languages: LabeledData[List[SpokenLanguage]]


class MultilangCVData(TypedDict):
    languages: List[CVData]
