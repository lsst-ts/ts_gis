"""Sphinx configuration file for TSSW package"""

from documenteer.conf.guide import *  # noqa

numpydoc_show_class_members = False  # noqa
autosummary_generate = True  # noqa
automodsumm_inherited_members = True  # noqa
autodoc_inherit_docstrings = True  # noqa
autoclass_content = "class"  # noqa
autodoc_default_flags = ["show-inheritance", "special-members"]  # noqa
extensions.remove("myst_parser")  # noqa
source_suffix = {".rst": "restructuredtext"}
