action = 'get_product_list'
ver = None
datanum = None
jsonkey = 'items'


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
    return list(map(ShopItem, raws))


class ShopItem:
    def __init__(self, raw):
        self.raw = raw
        self.name = raw['name']
        self.code = raw['code']
        self.price = raw['price']
        self.bmsg = raw.get('bmsg', '')
        self.spc = raw.get('spc', '0')
        self.stone = int(raw['stone'])
        self.buyable = raw.get('buyable', 1)  #bool?
        #? Derive these defaults from self.price?
        self.price_int = raw.get('price_int', 0)
        self.price_num = raw.get('price_num', '')

    def __repr__(self):
        return f"ShopItem({self.name!r})"

