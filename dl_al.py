action = 'dl_al'  #What about al_infoall?
ver = 'alver'
datanum = 35
jsonkey = 'd'

import os, os.path
import util
from util import ojson_load, ojson_loads

def load(fpath=None):
    """Load the JSON from given folder or file path.
    """
    if fpath is None:
        import datafiles
        fpath = datafiles.root
    if os.path.isdir(fpath):
        fpath = os.path.join(fpath, action+'.json')
    j = ojson_load(fpath)
    return loadjson(j)

def loads(s):
    j = ojson_loads(s)
    return loadjson(j)

def loadjson(j):
    """Load from JSON dict.
    """
    raws = j[jsonkey]
    v = j.get('v', 1)
    raise NotImplementedError

