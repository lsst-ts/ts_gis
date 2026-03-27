"""Sphinx configuration file for TSSW package"""

from documenteer.conf.guide import *  # noqa

numpydoc_show_class_members = True  # noqa
autosummary_generate = True  # noqa
automodsumm_inherited_members = True  # noqa
autodoc_inherit_docstrings = True  # noqa
autodoc_default_flags = ["show-inheritance", "special-members"]  # noqa
source_suffix = {".rst": "restructuredtext"}
