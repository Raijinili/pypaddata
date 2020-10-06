# Parsing bonus data.
action = 'download_limited_bonus_data'
ver = 'pver'
datanum = 39
jsonkey = 'bonuses'

from datetime import datetime as DT
import json

from util import ojson_load, ojson_loads
from padutil import ghtime
import dungeon_data
from dataclass import DataClass


"""
TODO:
- Find a way to set dungeon_data.
    - Must do it in a way that doesn't depend on a global.
    ?- Or don't set it in init. Pass it in when printing.

"""

#dummy
dungeons = {}

# keys: 'sebiadm'
# s: start
# e: end
# b: bonus type
    # 2: coins * 10000
    # 3: drop * 10000
    # 5: stamina * 10000
    # 6: special dungeon
    # 8: PEM
    # 9: REM
    # 10: PEM cost? (skip)
    # 11: xp bonus chance * 10000
    # 12: (old:) absolute +egg rate?? * 10000
    # 14: GF announcement?
    # 16: (new:) relative +egg rate?? * 10000
    # 17: skillup bonus
    # 21: tournament over?
    # 22: tournament?
# i: unknown

## TODO:
#   - Identify urgents. (They last for an hour.)
#   - Rather than start-end times, have time categories.
#       - Categories:
#           - Urgent (1 hour).
#           - Day.
#           - Week.
#           - Biweek.
#               ? Two-week?
#           - Halfmonth.
#               - E.g. coin dungeons and MP shop.
#           - 
#   ^- Or have times.
#       - Hour.
#       - Day.
#   ^^- Or have columns per unit.
#       - Hour.
#       - Day.
#       - Week.
#       - 
#       - 
#   -! The bonus data depends on group. (E.g. urgents.)
#   - 
#   - 


def ghmult(x):
    mult = x/10000
    if int(mult) == mult:
        mult = int(mult)
    return '%sx' % mult


def ghchance(x):
    assert x % 100 == 0
    return '%d%%' % (x//100)



class Bonus:
    # Lists special handlers for each type.
    types = {
        1: {'b':'exp*', 'a':ghmult},
        2: {'b':'coin*', 'a':ghmult},
        3: {'b':'drop*', 'a':ghmult},
        5: {'b':'stam*', 'a':ghmult},
        11: {'b':'great*', 'a':ghmult},
        12: {'b':'plus%', 'a':ghchance},
        16: {'b':'plus*', 'a':ghmult},
        17: {'b':'skill*', 'a':ghmult},
        
        6: {'b':'dung'}, # special/co-op dungeon list
        10: {'b':'pem$', 'a':int},
        # 8: {'b':'rem?', },
        # 9: {'b':'pem?', },
        8: {'b':'pem?', }, # Or "current"?
        9: {'b':'rem?', }, # Or "next"?
        14: {'b':'gf_?', },
        15: {'b':'present?', },
        21: {'b':'tourn', }, # "tourney is over, results pending"?
        22: {'b':'annc', },
        23: {'b':'meta?', },   # metadata?

        25: {'b':'drop%?', },
        36: {'b':'mxp*', 'a':ghmult},
        37: {'b':'dskill*', 'a':ghmult},
    }
    
    keys = 'sebiadfm'
    #f: floor
    
    'iadfm'
    keynames = {
        'i': 'i',
        'a': 'amt',
        'd': 'dung',
        'f': 'floor',
        'm': 'msg',
    }
    
    def __init__(self, raw):
        if not set(raw) <= set(Bonus.keys):
            raise ValueError('Unexpected keys: ' + str(set(raw) - set(Bonus.keys)))
    
        self.s = ghtime(raw['s'])
        self.e = ghtime(raw['e'])
        if 'd' in raw:
            # self.d = dungeons[int(raw['d'])]
            self.d = dungeons.get(int(raw['d']), 'd:%s'%raw['d'])
        if 'm' in raw:
            self.m = 'm'.replace('\n', r'\n')
        
        b = raw['b']
        others = 'iadfm'
        self.b = b
        if b in Bonus.types:
            typ = Bonus.types[b]
            self.type = typ['b']
        else:
            self.b = b
            typ = {}
            self.type = 'UNK_%d' % b
        
        for k, key in self.keynames.items():
            if k in raw:
                if k in typ:
                    setattr(self, key, typ[k](raw[k]))
                else:
                    setattr(self, key, raw[k])
        self.raw = raw
    
    
    def __repr__(self):
        d = dict(self.raw)
        d.pop('b')
        d.pop('s')
        d.pop('e')
        return 'Bonuses(%r, %r)' % (self.type, d)



#? Should each bonus have a different class?



#############
# 2020 code
#############

#? Should I make it an enum?
b_codes = {
    1: 'xp',
    2: 'coins',
    3: 'drop',
    5: 'stamina',
    6: 'specialdungeon',
    
}


def parse_dungeons(bonuses, dungeons):
    """Parse out the current dungeons.
    """
    if isinstance(bonuses, str):
        bonuses = ojson_loads(bonuses)['bonuses']
    bdungs = [
        dungeons[b.d] for b in bonuses
        if b.b == 6
    ]
    return bdungs


def parse_skillup_dungeons(bonuses, dungeons):
    """Parse out the current skillup dungeons.
    """
    if isinstance(bonuses, str):
        bonuses = ojson_loads(bonuses)['bonuses']
    bdungs = [
        dungeons[b.d] for b in bonuses
        if b.b == 25 and b.get('a', 0) == 0
    ]
    return bdungs


#############
# [2020] Loads.
#############



def load(fpath=None):
    """Load the JSON from given folder or file path.
    """
    if fpath is None:
        import datafiles
        fpath = datafiles.root
        raise NotImplementedError("Oops, didn't put bonus data into datafiles folder.")
    if os.path.isdir(fpath):
        fpath = os.path.join(fpath, action+'.json')
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
    raws = j['bonuses']
    v = j.get('v', 1)  # version
    if v != 2:
        warnings.warn("Bonus JSON has unknown version %s." % (v))
    bonuses = readbonuses2(raws, v)
    return bonuses

def readbonuses2(raws):
    ...
    raise NotImplementedError()
    return list(map(Bonus, raws))


