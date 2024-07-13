import pytest
from pathlib import Path
from cv_maker.config import TEMPLATES
from cv_maker.template import Template


def test_template_initialization():
    # assign
    template_dir = Path(TEMPLATES)
    template = Template(template_dir)

    # act

    # assert
    assert template.template_dir == template_dir
    assert template.env.comment_start_string == "{#%"
    assert template.env.comment_end_string == "%#}"


def test_template_returns_all_files(tmp_path_factory):
    # assign
    template_dir: Path = tmp_path_factory.mktemp("templates")
    for i in range(4):
        with open(template_dir / f"filename{i}.tex", "w", encoding="utf-8") as f:
            f.write("content")
    template = Template(template_dir)
    # act
    template_list = [f for f in template.env.list_templates()]
    result = [f.name for f in template_dir.iterdir() if f.stem not in template_list]
    # assert
    assert set(template_list) == set(result)


@pytest.mark.parametrize(
    "template_filename", ["file1.tex", "file2.tex", "file3.tex", "file4.tex"]
)
def test_template_returns_correct_file(template_filename, tmp_path_factory):
    # assign
    template_dir: Path = tmp_path_factory.mktemp("templates")
    with open(template_dir / template_filename, "w", encoding="utf-8") as f:
        f.write("content")
    # act
    template = Template(template_dir)
    template_file = template._get(file_name=template_filename)

    # assert
    assert template_file.filename == str((template_dir / template_filename).resolve())
