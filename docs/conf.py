import os
import sys
import django

# Add project root to Python path
sys.path.insert(0, os.path.abspath(".."))

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

# Initialize Django
django.setup()


# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = 'ecommerce_project'
copyright = '2026, Jacob Saftig'
author = 'Jacob Saftig'
release = '00.00.01'


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

# Prevent autodoc from importing modules that require MySQL
autodoc_mock_imports = [
    "MySQLdb",
    "mysqlclient",
    "django.db.backends.mysql",
    "ecommerce.mysql_backend",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']