#!/usr/bin/env python
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Script used to generate the features file before building the actual documentation."""

import os
import sys

import sphinx

from pylint.lint import PyLinter

def builder_inited(app):
    # PACKAGE/docs/exts/pylint_extensions.py --> PACKAGE/
    base_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    linter = PyLinter()
    linter.load_default_plugins()

    features = os.path.join(base_path, 'doc', 'technical_reference', 'features.rst')
    with open(features, 'w') as stream:
        stream.write("Pylint features\n")
        stream.write("===============\n\n")
        stream.write(".. generated by pylint --full-documentation\n\n")
        linter.print_full_documentation(stream)


def setup(app):
    app.connect('builder-inited', builder_inited)
    return {'version': sphinx.__display_version__}

if __name__ == "__main__":
    builder_inited(None)
