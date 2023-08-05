# -*- coding: utf-8 -*-

"""
Tools for ipyrest.

So far, stuff here is only used only during development.
"""

from ipywidgets import Tab, HBox, VBox, Accordion


def tree(widget, level=0):
    "Show widget hiararchy as nested tree."

    indent = level * '  '
    klass = widget.__class__
    class_name = klass.__name__
    print(f'{indent}{class_name}')
    if klass in (Tab, HBox, VBox, Accordion):
        for child in widget.children:
            tree(child, level + 1)
