from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template as JinjaTemplate


class Template:
    def __init__(self, template_dir: Path) -> None:
        self.template_dir = template_dir
        self.__init_env()

    def __init_env(self):
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

        self.env.comment_start_string = "{#%"
        self.env.comment_end_string = "%#}"

    def render(self, file_name: str, data: Any = None) -> str:
        template = self._get(file_name)
        return template.render(data)

    def _get(self, file_name: str) -> JinjaTemplate:
        return self.env.get_template(file_name)
