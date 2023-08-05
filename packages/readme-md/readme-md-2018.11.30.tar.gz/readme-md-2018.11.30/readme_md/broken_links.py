#!/usr/bin/env python
"""print README.md broken links"""
# -*- coding: utf-8 -*-
import click
import readme_md
import requests


MODULE_NAME = "readme_md.broken_links"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s path [timeout]' % MODULE_NAME


@click.command()
@click.argument('path', required=True)
@click.argument('timeout', default=5, required=False)
def _cli(path,timeout):
    string = open(path).read()
    links = readme_md.broken_links(path,timeout=timeout)
    if links:
        print("\n".join(links))



if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
