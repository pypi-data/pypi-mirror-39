# This page intentionally left blank
from .thumbnail import thumbnail

def read_file(directory, silence = True, tab_to_space = 4, keys = ['class', 'def', 'for', 'if', 'elif','else:', 'while']):
    return thumbnail(directory, silence, tab_to_space, keys)