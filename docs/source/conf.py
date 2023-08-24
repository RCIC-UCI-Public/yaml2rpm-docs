# Configuration file for the Sphinx documentation builder.

# -- Project information

project = u'YAML2RPM'
copyright = u'2019-2023, The Regents of the University of California'
author = u'RCIC'

release = '0.1'
version = '0.1.0'

# add path to python code snippets
import sys
import os
sys.path.insert(0, os.path.abspath('src'))

# -- General configuration
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output
html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = '.rst'
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []
