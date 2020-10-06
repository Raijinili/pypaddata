action = 'mdatadl'  # &dtp=0
ver = 'mever'   #tlver for dtp=1
datanum = 37    #37 and 38 for dtp=1
jsonkey = 'd'   #both


import os
import os.path
import warnings

import util
from util import ojson_load, ojson_loads
from util import keys, values, items, bucketize
#import padvalues
from padutil import gh_csv, gh_time
from dataclass import DataClass



def load(folder_path=None):
    """Load the JSON from given folder.
    """
    if folder_path is None:
        import datafiles
        folder_path = datafiles.root
    return loadfile(os.path.join(folder_path, 'mdatadl.json'))


def loadfile(fpath):
    j = ojson_load(fpath)
    return loadjson(j)
    #TODO: Cache it based on filepath.
        #! Check modified time.


def loads(s):
    j = ojson_loads(s)
    return loadjson(j)


def loadjson(j):
    """Load from JSON dict.
    """
    v = j.get('v', 1)  # version
    if v != 1:
        warnings.warn("Monster Exchange JSON has unknown version %s." % (v))
    raw = j['d']
    table = gh_csv(raw)
    trades = read_trades(table, v=v)
    return trades

def read_trades(table, v):
    return [ExchangeOffer(raw) for raw in table]


class ExchangeOffer(DataClass):
    action = 'mdatadl'
    jsonkey = 'd'
    # Is this incomplete?
    fields = [
        'A',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
    ]
    
    def __init__(self, raw):
        # Process the raw first.
        ...

class ExchangeOffer:
    def __init__(self, raw):
        # Process the raw first.
        self.raw = raw
        parsed = []
        for i, cell in enumerate(raw):
            if i in (0, 11):
                parsed.append(cell)
            else:
                parsed.append(int(cell or 0))
        self.parsed = parsed
        
        self.id = parsed[1]
        self.ord = parsed[2]
        self.tab = parsed[3]
        self.card = parsed[4]
        self.lv = parsed[5]
        self.flags1 = parsed[6]
        self.start = gh_time(parsed[7])
        self.end = gh_time(parsed[8])
        self.msgstart = gh_time(parsed[9]) if parsed[9] else None
        self.msgend = gh_time(parsed[10]) if parsed[10] else None
        self.msg = parsed[11]
        self.fcount = parsed[12]
        self.flags2 = parsed[13]
        self.fodder = parsed[14:]

    @property
    def multi(self):
        return bool(self.flags2 & 4)

    @property
    def once(self):
        return bool(self.flags2 & 2)

    def __repr__(self):
        return f"ExchangeOffer<{self.id}, {self.card}>"

    def __eq__(self, other):
        return self.parsed == other.parsed

    def __hash__(self):
        return hash(tuple(self.parsed))

