import os

from . table import *
from . bioset import *
from . xml import *
from . ftp import *
from . http import *

def local_path(path):
    path = os.path.join('~/.biomap', path)
    path = os.path.expanduser(path)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

class HashableDict(dict):
    def __init__(self, dct, hash_key):
        super().__init__(dct)
        self.key = hash_key

    def __hash__(self):
        return hash(self[self.key])
