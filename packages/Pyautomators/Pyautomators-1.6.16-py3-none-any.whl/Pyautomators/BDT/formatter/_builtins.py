# -*- coding: utf-8 -*-
"""
Knowledge base of all built-in formatters.
"""

from __future__ import  absolute_import
from Pyautomators.BDT.formatter import _registry


# -----------------------------------------------------------------------------
# DATA:
# -----------------------------------------------------------------------------
# SCHEMA: formatter.name, formatter.class(_name)
_BUILTIN_FORMATS = [
    # pylint: disable=bad-whitespace
    ("plain",   "Pyautomators.BDT.formatter.plain:PlainFormatter"),
    ("pretty",  "Pyautomators.BDT.formatter.pretty:PrettyFormatter"),
    ("json",    "Pyautomators.BDT.formatter.json:JSONFormatter"),
    ("json.pretty", "Pyautomators.BDT.formatter.json:PrettyJSONFormatter"),
    ("null",      "Pyautomators.BDT.formatter.null:NullFormatter"),
    ("progress",  "Pyautomators.BDT.formatter.progress:ScenarioProgressFormatter"),
    ("progress2", "Pyautomators.BDT.formatter.progress:StepProgressFormatter"),
    ("progress3", "Pyautomators.BDT.formatter.progress:ScenarioStepProgressFormatter"),
    ("rerun",     "Pyautomators.BDT.formatter.rerun:RerunFormatter"),
    ("tags",          "Pyautomators.BDT.formatter.tags:TagsFormatter"),
    ("tags.location", "Pyautomators.BDT.formatter.tags:TagsLocationFormatter"),
    ("steps",         "Pyautomators.BDT.formatter.steps:StepsFormatter"),
    ("steps.doc",     "Pyautomators.BDT.formatter.steps:StepsDocFormatter"),
    ("steps.catalog", "Pyautomators.BDT.formatter.steps:StepsCatalogFormatter"),
    ("steps.usage",   "Pyautomators.BDT.formatter.steps:StepsUsageFormatter"),
    ("sphinx.steps",  "Pyautomators.BDT.formatter.sphinx_steps:SphinxStepsFormatter"),
    ("json.cucumber", "Pyautomators.BDT.formatter.cucumber:CucumberJSONFormatter"),
]

# -----------------------------------------------------------------------------
# FUNCTIONS:
# -----------------------------------------------------------------------------
def setup_formatters():
    """Register all built-in formatters (lazy-loaded)."""
    _registry.register_formats(_BUILTIN_FORMATS)
