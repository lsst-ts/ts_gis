"""Sphinx configuration file for TSSW package"""

from documenteer.conf.pipelinespkg import *  # noqa

project = "ts_gis"
html_theme_options["logotext"] = project  # noqa
html_title = project
html_short_title = project

intersphinx_mapping["ts_xml"] = ("https://ts-xml.lsst.io", None)  # noqa
intersphinx_mapping["pymodbus"] = (  # noqa
    "https://pymodbus.readthedocs.io/en/v3.1.3",
    None,
)

extensions.append("sphinx-jsonschema")  # noqa
