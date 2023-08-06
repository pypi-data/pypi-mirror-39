"""
Thumbnail Creator for Python Files
==================================

pythumbnail is a thumbnail creator for python codes 
that captures keywords such as def, class, for and restructure
them in a highly readable way. It aims to provide quick access
to the content of python codes even if they are badly written.

"""

from .thumbnail import thumbnail

# read and scan the document
def read_file(directory, silent = True, keys = ['class', 'def', 'for', 'if', 'elif','else:', 'while']):
    snapshot = thumbnail(directory, silent, keys)
    snapshot.scan()
    return snapshot