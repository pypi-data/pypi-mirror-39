#!/usr/bin/env python
import imp
import inspect
import markdown
import os
import re
import pydoc
import public
import readme_md.tables
import requests
import setupcfg

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
            for k, v in python_sections().items():
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


@public.add
def doc(obj):
    """return first line of an object docstring"""
    doc = inspect.getdoc(obj) if obj.__doc__ else ""
    return doc.split("\n")[0].strip()


@public.add
def spec(func):
    """return a string with Python function specification"""
    doc = pydoc.plain(pydoc.render_doc(func))
    return doc.splitlines()[2]


def import_name(path):
    return os.path.splitext(path)[0].replace(os.sep, ".").replace(".__init__", "")


def import_module(path):
    """import python file and return its module object"""
    name = import_name(path)
    return imp.load_source(name, path)


@public.add
def modules():
    """load python files and return its module objects. `setup.cfg` `[options]` `py_modules` or `packages` required"""
    packages = setupcfg.get("options", "packages", [])
    py_modules = setupcfg.get("options", "py_modules", [])
    files = list(map(lambda m: "%s.py" % m, py_modules))
    for package in packages:
        path = package.replace(".", "/")
        filenames = os.listdir(path)
        py = filter(lambda f: os.path.splitext(f)[1] == ".py", filenames)
        files += list(map(lambda l: os.path.join(path, l), py))
    return list(map(import_module, files))


@public.add
def python_sections():
    """return a dictionary with python project sections: `install`, `classes`, `functions`, `cli`. `setup.cfg` required"""
    def install(name):
        return """```bash
$ [sudo] pip install %s
```""" % name
    _modules = modules()

    def scripts_usage(scripts):
        """return a string with `script --help` output"""
        usages = []
        for path in scripts:
            if open(path).read().find("#!") == 0:
                continue
            shebang = open(path).read().splitlines()[0].replace("#!", "")
            out = os.popen("%s %s --help 2>&1" % (shebang, path)).read().strip()
            usages.append("""```bash
%s
```""" % out)
        return "\n\n".join(usages)

    scripts = setupcfg.get("options", "scripts", [])
    scripts = list(filter(lambda f: os.path.basename(f)[0] != ".", scripts))

    modules_usage = readme_md.tables.usage(_modules)
    cli = "\n\n".join(filter(None, [modules_usage, scripts_usage(scripts)]))
    functions = list(readme_md.functions(_modules))
    classes = list(readme_md.classes(_modules))

    return dict(
        install=install(setupcfg.get("metadata", "name")),
        classes="\n\n".join(map(readme_md.tables.cls, classes)),
        functions=readme_md.tables.functions(functions),
        cli=cli
    )


def members(objects, predicate):
    """return README members of an objects in a list of (name, value) pairs. object `__readme__` or `__all__` required"""
    result = []
    for obj in objects:
        for name, value in inspect.getmembers(obj, predicate):
            if name in getattr(obj, "__readme__", getattr(obj, "__all__", [])):
                result.append((name, value))
    return result


@public.add
def functions(modules):
    """return list of README functions. module `__all__` or `__readme__` required"""
    return list(map(lambda pair: pair[1], members(modules, inspect.isroutine)))


@public.add
def classes(modules):
    """return list of README classes. module `__all__` or `__readme__` required"""
    return list(map(lambda pair: pair[1], members(modules, inspect.isclass)))


@public.add
def attrs(cls):
    """return README attributes of a class in a list of (name, value) pairs. object `__readme__` required"""
    def isattr(obj):
        return not inspect.isroutine(obj) and not isinstance(obj, property)

    return members([cls], isattr)


@public.add
def methods(cls):
    """return README methods of a class in a list of (name, method) pairs. class `__readme__` required"""
    def ismethod(obj):
        return inspect.isfunction(obj) or inspect.ismethod(obj)

    return members([cls], ismethod)


@public.add
def properties(cls):
    """return README properties of a class in a list of (name, prop) pairs. class `__readme__` required"""
    return members([cls], inspect.isdatadescriptor)


@public.add
def links(string):
    """return list with markdown links"""
    html = markdown.markdown(string, output_format='html')
    r = re.compile('(?<=href=").*?(?=")')
    result = []
    for link in r.findall(html):
        if link not in result:
            result.append(link)
    return result


@public.add
def broken_links(string, timeout=5):
    """return list with broken markdown links"""
    result = []
    for link in links(string):
        try:
            r = requests.get(link, timeout=timeout)
            ok = r.status_code == requests.codes.ok
            if not ok:
                result.append(link)
        except Exception:
            result.append(link)
    return result
