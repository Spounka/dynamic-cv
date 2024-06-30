from typing import TypedDict, List


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
