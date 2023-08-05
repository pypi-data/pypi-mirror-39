#!/usr/bin/env python
import os
import public
import readme_md.get
import readme_md.tables

#
# sorted(_attrs(cls), key=lambda kv: "__" in kv[0])


@public.add
class Readme:
    """README.md generator. attrs and properties as README sections, ordered by `order`"""
    __readme__ = ["get_sections", "load_sections", "header", "save", "load", "render"]
    order = ["badges", "description", "install", "features", "requirements", "index", "how", "config", "classes", "functions", "cli", "examples", "todo", "links", "generator"]
    disabled = []
    headers = dict(
        badges="",
        how="How it works",
        cli="CLI"
    )
    header_lvl = 4
    generator = """
<p align="center"><a href="https://pypi.org/project/readme-md/">readme-md</a> - README.md generator</p>"""

    def __init__(self, path=None, **kwargs):
        if os.path.exists("setup.cfg"):
            for k, v in readme_md.get.python_sections().items():
                setattr(self, k, v)
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.load_sections(path)

    def header(self, section_name):
        """return section header string"""
        header = self.headers.get(section_name, section_name.title())
        if not header:
            return ""
        if "#" in header:
            return header
        return "%s %s" % ("#" * self.header_lvl, header)

    def get_sections(self):
        """return all sections in a list of (name, string) pairs sorted by `order`"""
        result = []
        for name in self.order:
            if name not in getattr(self, "disabled", []):
                string = getattr(self, name, '')
                if string:
                    result.append([name, string.rstrip()])
        return result

    def render(self):
        """return README string"""
        # todo: clean
        sections = []
        for name, string in filter(lambda pair: pair[1], self.get_sections()):
            if string.splitlines()[0].strip() and string.find("#") != 0:
                header = self.header(name)
                string = "%s\n%s" % (header, str(string).lstrip())
            sections.append(string.strip())
        return "\n\n".join(filter(None, sections))

    def save(self, path='README.md'):
        """save to file"""
        if os.path.dirname(path) and not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        open(path, "w").write(self.render())
        return self

    def load_sections(self, path="."):
        """load sections from `.md` markdown files"""
        """
    path/<section_name>.md
    path/<section_name2>.md
        """
        if not path:
            path = os.getcwd()
        for f in map(lambda l: os.path.join(path, l), os.listdir(path)):
            if os.path.isfile(f) and os.path.splitext(f)[1] == ".md":
                key = os.path.splitext(os.path.basename(f))[0]
                value = open(f).read()
                setattr(self, key, value)
        return self
