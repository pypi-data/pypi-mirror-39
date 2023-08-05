#!/usr/bin/env python
import imp
import inspect
import os
import public
import pydoc
import readme_md
import setupcfg


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
    modules = readme_md.get.modules()

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

    modules_usage = readme_md.tables.usage(modules)
    cli = "\n\n".join(filter(None, [modules_usage, scripts_usage(scripts)]))
    functions = list(readme_md.get.functions(modules))
    classes = list(readme_md.get.classes(modules))

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
