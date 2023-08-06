# -*- coding: utf-8 -*-
import sys
from .formatter import format_obj


def console_display(text):
    sys.stdout.write(text)


def pretty_print(data_object, display_callback=None):
    return format_obj(data_object, display=display_callback)
