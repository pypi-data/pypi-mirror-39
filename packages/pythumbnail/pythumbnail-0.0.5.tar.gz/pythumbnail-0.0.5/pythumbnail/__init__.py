# This page intentionally left blank
from .thumbnail import thumbnail

def read_file(directory, silent = True, keys = ['class', 'def', 'for', 'if', 'elif','else:', 'while']):
    return thumbnail(directory, silent, keys)