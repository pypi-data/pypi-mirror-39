# This page intentionally left blank
from .thumbnail import thumbnail

def read_file(directory, silent = True, keys = ['class', 'def', 'for', 'if', 'elif','else:', 'while']):
    snapshot = thumbnail(directory, silent, keys)
    snapshot.scan()
    return snapshot