# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "lpmd"
copyright = "2022, sndpgm"
author = "sndpgm"

# The full version, including alpha/beta/rc tags
release = "0.0.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "numpydoc",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for Autodoc -----------------------------------------------------

autodoc_default_options = {
    "member-order": "bysource",
    "special-members": "__init__",
}

# -- Build API doc ----------------------------------------------------------

numpydoc_show_class_members = False

fpath = os.path.dirname(__file__)
ref_path = os.path.join(fpath, "reference")
app_path = os.path.join(os.path.dirname(fpath), "lpmd")
apidoc_cmd = "sphinx-apidoc -e -f -d 5 --templatedir {0}/_templates/apidoc -o {1} {2} '{2}/tests/*'"
os.system(apidoc_cmd.format(fpath, ref_path, app_path))
