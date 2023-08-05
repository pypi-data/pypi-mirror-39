"""Simple App Generator - Python

Usage:
------
    $ sappgen [options] <project_name> <app_name>

Create an app:
    $ sappgen proj app

Available options are:
    -h, --help         Show this help

Contact:
--------
- https://aayushuppal.github.io

More information is available at:
- https://pypi.org/project/sappgen
- https://github.com/aayushuppal/sappgen
"""

import logging
import os
import sys
from .cfg import LOG_LEVEL
from .util import set_root_logger_stdout, cleanup
from .templates import Template1


set_root_logger_stdout(LOG_LEVEL)


def process(**kwargs):
    logging.info("sappgen:main")
    logging.info(kwargs)

    project_name = "project"
    app_name = "testapp"

    if "project" in kwargs:
        project_name = str(kwargs["project"])
    if "app" in kwargs:
        app_name = str(kwargs["app"])

    tmpl = Template1(project_name, app_name)
    try:
        tmpl.process()
    except:
        logging.exception("setup failed")
        cleanup(project_name)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return

    if len(args) == 2:
        project_name = str(args[0])
        app_name = str(args[1])
        process(project=project_name, app=app_name)
    else:
        print(__doc__)
        return
