#!/usr/bin/env python
import inspect
import mdown
import public
import readme_md


@public.add
def functions(functions):
    """return a string with functions table"""
    rows = []
    for func in functions:
        if not inspect.isroutine(func):
            raise ValueError("%s is not a function" % func)
        spec = readme_md.spec(func)
        module = inspect.getmodule(func)
        fullname = "%s.%s" % (module.__name__, spec)
        doc = readme_md.doc(func)
        rows.append(("`%s`" % fullname, doc))
    return mdown.table(("function", "`__doc__`"), rows)


@public.add
def classes(classes):
    """return a string with classes table"""
    maxtrix = []
    for cls in classes:
        if not inspect.isclass(cls):
            raise ValueError("%s is not a class" % cls)
        module = inspect.getmodule(cls)
        fullname = "%s.%s" % (module.__name__, cls.__name__)
        doc = readme_md.doc(cls)
        maxtrix.append(("`%s`" % fullname, doc))
    return mdown.table(("class", "`__doc__`"), maxtrix)


@public.add
def attrs(cls):
    """return a string with class attributes table"""
    matrix = []
    for name, value in readme_md.attrs(cls):
        value = value if value != "" else "''"
        matrix.append(("`%s`" % name, "`%s`" % value))
    return mdown.table(("attr", "default value"), matrix)


@public.add
def methods(cls):
    """return a string with class methods table"""
    matrix = []
    for name, method in readme_md.methods(cls):
        spec = readme_md.spec(method)
        spec = spec.replace("self, ", "").replace("(self)", "()")
        doc = readme_md.doc(method)
        matrix.append(("`%s`" % spec, doc))
    return mdown.table(("method", "`__doc__`"), matrix)


@public.add
def properties(cls):
    """return a string with class properties table"""
    maxtrix = []
    for name, prop in readme_md.properties(cls):
        doc = readme_md.doc(prop)
        maxtrix.append(("`%s`" % name, doc))
    return mdown.table(("@property", "`__doc__`"), maxtrix)


@public.add
def usage(modules):
    """return a string with cli modules usage table. `python -m module` or module `USAGE` variable (if defined). `if __name__ == "__main__"` line required"""
    def is_cli(module):
        for l in open(module.__file__).read().splitlines():
            if "__name__" in l and "__main__" in l and l == l.lstrip():
                return True

    matrix = []
    for module in modules:
        if not inspect.ismodule(module):
            raise ValueError("%s is not a module" % module)
        if is_cli(module):
            USAGE = getattr(module, "USAGE", "python -m %s" % module.__name__)
            doc = readme_md.doc(module)
            matrix.append(("`%s`" % USAGE, doc))
    return mdown.table(("usage", "`__doc__`"), matrix)


@public.add
def cls(cls):
    """return a string with class name, description and attrs+methods+properties tables"""
    module = inspect.getmodule(cls)
    fullname = "`%s.%s`" % (module.__name__, cls.__name__)
    doc = readme_md.doc(cls)
    title = " - ".join(filter(None, [fullname, doc]))
    attrs = readme_md.tables.attrs(cls)
    methods = readme_md.tables.methods(cls)
    props = readme_md.tables.properties(cls)
    lines = [title] + list(filter(None, [attrs, methods, props]))
    return "\n\n".join(lines)
