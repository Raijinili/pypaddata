action = 'download_card_data'
ver = 'cver'
datanum = 21
jsonkey = 'card'

import os, os.path
import ast
import json
import warnings
from operator import attrgetter as aget

import util
from util import ojson_load, ojson_loads, Index
from util import keys, values, items, bucketize
import padvalues

__all__ = [
    # 'load',
    # 'loadfile',
    # 'loads',
    # 'loadjson',
]


# Blocks alt monsters.
INSANE_CARD_LIMIT = 9900  # Some cards don't deserve to live.
# INSANE_CARD_LIMIT = 99000000

#NVM: See get_player_data.py.
# from boxcard import *
# from bookcard import *


def load(fpath=None, limit=INSANE_CARD_LIMIT):
    """Load the JSON from given folder or file.
    
    If fpath not given, use datafiles.root folder.
    """
    if fpath is None:
        import datafiles
        fpath = datafiles.root
    if os.path.isdir(fpath):
        fpath = os.path.join(fpath, action+'.json')
    return loadfile(fpath, limit=limit)


def loadfile(fpath, limit=INSANE_CARD_LIMIT):
    # import os
    # cwd = os.getcwd()
    # nwd = os.path.dirname(os.path.abspath(__file__))
    # os.chdir(nwd)
    # try:
        j = ojson_load(fpath)
        return loadjson(j, limit=limit)
    # finally:
        # os.chdir(cwd)
    #TODO: Cache it based on filepath.
        #! Check modified time.

def loadfile(fpath, limit=INSANE_CARD_LIMIT):
    j = ojson_load(fpath)
    return loadjson(j, limit=limit)


def loads(s, limit=INSANE_CARD_LIMIT):
    j = ojson_loads(s)
    return loadjson(j, limit=limit)


def loadjson(j, limit=INSANE_CARD_LIMIT):
    """Load from JSON dict.
    """
    raws = j['card']
    v = j['v']
        #^ We can use version to determine what the fields are.
    if v == 810:
        raise NotImplementedError('BookCard810')
    elif v == 900:
        cards = [BookCard900(i, raw) for i, raw in items(raws)]
        # cards = util.Bag(cards)
    elif v == 920:
        cards = Index(
                    (raw[0], BookCard920(raw))
                    for raw in values(raws)
                    if not limit or raw[0] < limit)
    else:
        fpath = "FORGOT TO ADD FPATH"
        raise ValueError("%r has unknown card version %s." % (fpath, v))
    
    _register_evos(cards)
    _register_families(cards)
    
    return cards

# WIP: Padding technique.
def loadjson(j, limit=INSANE_CARD_LIMIT):
    """Load from JSON dict.
    """
    raws = j['card']
    v = j['v']
        #^ We can use version to determine what the fields are.
    if v < 810:
        raise NotImplementedError(v)
    raws = [card[:] for card in raws]
    if v < 900:  # Collab and inherits.
        for card in raws: card.extend((0,0))
    if v < 920:  # Index.
        for i, card in items(raws): card.insert(0, i)
    if v < 1220:  # Weird furigana thing.
        for card in raws: card.append('')
    if v < 1230:  # Limit break.
        for card in raws: card.append(0)
    if v < 1240:  # Super awakening (prep).
        for card in raws: card.insert(-9, '')
    if v < 1520:  # Voice.
        for card in raws: card.append(0)
    if v < 1600:  # Orbskin.
        for card in raws: card.append(0)
    # 1800: HT 2019-10-11
    # 1800: NA 2019-10-~20
    if v < 1800:  # Only used so far for Fagan Rai?
        for card in raws: card.append('')
    if v > 1800:
        # Should raise a warning here.
        warnings.warn("Unknown card_data version: %s" % v)
    # else:
        # raise ValueError("%r has unknown card version %s." % (fpath, v))
    cards = Index(
                (raw[0], BookCard(raw))
                for raw in values(raws)
                if not limit or raw[0] < limit)
    
    _register_evos(cards)
    _register_families(cards)
    
    return cards



def _register_evos(cards):
    """Register `mon.evos`.
    """
    buckets = bucketize(values(cards), aget('preevo'), ignores={0})
    for mon_id, evos in items(buckets):
        mon = cards[mon_id]
        mon.evos = evos

def _register_families(cards):
    """Register `mon.family`.
    """
    buckets = bucketize(values(cards), aget('base'))
    for base_id, members in items(buckets):
        # fam = CardFamily(base_id, members)
        # for member in fam:
            # member.family = fam
        for member in members:
            member.family = members


## Alternative API:
'''
def load(file=None, *, dir=None, fpath=None, region=None):
    """Load the data from a JSON.
    
    Call syntaxes:
        - load():
            Load from latest.
            ? Not necessary if we have ".cards" etc. be lazy DBs?
        - load(some_filelike_object):
            ? Why even bother?
        - load(dir=some_folder):
            Folder of the file. Filename is assumed.
        - load(fpath=some_path_or_file_handler):
            Path to the file.
        - load(region='EN'):
            Load latest from the given region.
        ? Overcomplicated?
    
    """
    if dir is not None:
        fpath = os.path.join(dir, file)
    else:
        fpath = file
    
    j = ojson_load(fpath)
    return loadjson(j)


'''








from dataclass import DataClass


class BookCard(DataClass):
    """A card in the monster book, as opposed to the box. The species.
    
    Current version: 12.5.
    """
    
    action = 'download_card_data'
    jsonkey = 'card'  # JSON key in the json file.
    
    fields = [
        #0
        'id',               #: int
        'name',             #: str
        'att',              #: -> elements
        'subatt',           #: -> elements
        'isult',            #: {0,1}
        'type1',            #: -> montypes
        'type2',            #: -> montypes
        'rarity',           #: int
        #8
        'cost',             #: int
        '_UNK09',           #: ??
        'lvmax',            #: int
        'feed4',            #: int
                                #= feed xp at lv4
        '_UNK12',           #: ??
                                #= 1 for unreleased, 100 for released.
        'sell10',           #: int
                                #= sell price at lv10
        'hp1',              #: int
        'hpmax',            #: int
        #16
        'hpe',              #: float    
                                #= HP exponent.
        'atk1',             #: int
        'atkmax',           #: int
        'atke',             #: float
        'rcv1',             #: int
        'rcvmax',           #: int
        'rcve',             #: float
        'xpmax',            #: int
        #24
        'xpgr',             #: float
        'active',           #: -> skills
        'leader',           #: -> skills
        'enemy_turns',      #: int
        'enemy_hp1',        #: int
        'enemy_hp10',       #: int
        'enemy_hpgr',       #: float
        'enemy_atk1',       #: int
        #32
        'enemy_atk10',      #: int
        'enemy_atkgr',      #: float
        'enemy_def1',       #: int
        'enemy_def10',      #: int
        'enemy_defgr',      #: float
        '_UNK37',
        'enemy_coins2',     #: int
                                #= Enemy coins reward at level 2
        'enemy_rankxp2',    #: int
                                #= Enemy XP reward at level 2
        #40
        'preevo',           #: -> cards    
        'evomat1',          #: -> cards
        'evomat2',          #: -> cards
        'evomat3',          #: -> cards
        'evomat4',          #: -> cards
        'evomat5',          #: -> cards
        'premat1',          #: -> cards
        'premat2',          #: -> cards
        #48
        'premat3',          #: -> cards
        'premat4',          #: -> cards
        'premat5',          #: -> cards
        '_UNK51',
        '_UNK52',
        '_UNK53',
        '_UNK54',
        '_UNK55',
        #56
        '_UNK56',
        'eskills',          #: list[???]
        'awkns',            #: list[-> awakens]
        'sawkns',           #: list[->? awakens]
        'base',             #: -> cards
        'gkey',             #: int
                                #= Group key or 0.
        'type3',            #: -> montypes
        'mp',               #: int
        #64
        'latent',           #: -> latents
                                #= Which latent is given upon feed.
        'collab',           #: -> collab
                                #? Which collab?
        '_flags65',         #: bitflags
                                #= Flags for inheritance etc.
        'furigana',         #: str
        'limit',            #: int
        'voice',            #: int
                                #= Voice
                                # Huh? This should be 69. It's the last entry of a maxsize70. Should I renumber the previous unknowns?
        'orbskin',          #: int
        '_UNK1800',         #: str
                                #Seen: "link:5631" for Fagan Rai, linking to transformed Rai.
    ]
    #? Flatten constant-sized arrays?
        #- Pre-evo mats.
        #- Evo mats. (set/counter)
        #- HP/Atk/RCV (+ enemy versions).
        #- Type. (set)
    #? Use `._thing` for the original value and `.thing` for the semantic value?
        #- E.g.
            #- Make `._type3` the original int value and `.type3` a MonsterType object.
            #- `.base` is a BookCard and `._base` is its ID.
        #- Or `.o_base` for "original `.base`".
    sdleif = {attr:i for i, attr in enumerate(fields)}
    
    # Additional properties.
    properties = {
        'types': lambda c:
                {t for t in (c.type1, c.type2, c.type3) if t != -1},
        'mats': lambda c:
                list(filter(bool,
                    (getattr(c, 'evomat%d' % (i+1))
                        for i in range(5)))),
        'sortkey':  # Monsterbook sortkey "Group".
            lambda c:
                # (c.base, c.preevo, c.id),
                # (c.gkey/10 if c.gkey else c.base, c.base, c.id),
                # (c.gkey/10 if c.gkey else c.base, c.gkey, c.base, c.id),
                # (c.gkey/10 or c.base, c.id),
                (c.gkey/10 or c.base, c.gkey, c.base, c.id),
        'inheritable':   lambda c: bool(c._flags65 & 0x01),
        'canassist':     lambda c: bool(c._flags65 & 0x01),
        'assisttarget':  lambda c: bool(c._flags65 & 0x02),
        '_flags65_4':    lambda c: bool(c._flags65 & 0x04),
        'nostackmat':    lambda c: bool(c._flags65 & 0x08),
        'assistonly':    lambda c: bool(c._flags65 & 0x10),
        'extralatents':  lambda c: bool(c._flags65 & 0x20),
        'link':
            lambda c: c and int(c._UNK1800.split(':')[1]),
        'stackable':
            lambda c: (set(c.types) & set(padvalues.stacktypes)) and not c.nostackmat,
    }
    
    def __init__(self, raw):
        ## Unflatten the arrays.
        raw = unflatten_card(raw, self.sdleif['eskills'], replace=True)
        super().__init__(raw)
        # self.sawkns = list(map(int, filter(bool, self.sawkns.split(','))))
        self.sawkns = ast.literal_eval('[%s]' % self.sawkns)


class BookCard920(DataClass):
    """A card in the monster book, as opposed to the box. The species.
    
    This version is for version 9.2.0 and up.
    """
    
    action = 'download_card_data'
    jsonkey = 'card'  # JSON key in the json file.
    
    fields = [
        #0
        'id',               #: int
        'name',             #: str
        'att',              #: -> elements
        'subatt',           #: -> elements
        'isult',            #: {0,1}
        'type1',            #: -> montypes
        'type2',            #: -> montypes
        'rarity',           #: int
        #8
        'cost',             #: int
        '_UNK09',           #: ??
        'lvmax',            #: int
        'feed4',            #: int
                                #= feed xp at lv4
        '_UNK12',           #: ??
                                #= 1 for unreleased, 100 for released.
        'sell10',           #: int
                                #= sell price at lv10
        'hp1',              #: int
        'hpmax',            #: int
        #16
        'hpe',              #: float    
                                #= HP exponent.
        'atk1',             #: int
        'atkmax',           #: int
        'atke',             #: float
        'rcv1',             #: int
        'rcvmax',           #: int
        'rcve',             #: float
        'xpmax',            #: int
        #24
        'xpgr',             #: float
        'active',           #: -> skills
        'leader',           #: -> skills
        'enemy_turns',      #: int
        'enemy_hp1',        #: int
        'enemy_hp10',       #: int
        'enemy_hpgr',       #: float
        'enemy_atk1',       #: int
        #32
        'enemy_atk10',      #: int
        'enemy_atkgr',      #: float
        'enemy_def1',       #: int
        'enemy_def10',      #: int
        'enemy_defgr',      #: float
        '_UNK37',
        'enemy_coins2',     #: int
                                #= Enemy coins reward at level 2
        'enemy_rankxp2',    #: int
                                #= Enemy XP reward at level 2
        #40
        'preevo',           #: -> cards    
        'evomat1',          #: -> cards
        'evomat2',          #: -> cards
        'evomat3',          #: -> cards
        'evomat4',          #: -> cards
        'evomat5',          #: -> cards
        'premat1',          #: -> cards
        'premat2',          #: -> cards
        #48
        'premat3',          #: -> cards
        'premat4',          #: -> cards
        'premat5',          #: -> cards
        '_UNK51',
        '_UNK52',
        '_UNK53',
        '_UNK54',
        '_UNK55',
        #56
        '_UNK56',
        'eskills',          #: list[???]
        'awkns',            #: -> awakens
        'base',             #: -> cards
        'gkey',             #: int
                                #= Group key or 0.
        'type3',            #: -> montypes
        'mp',               #: int
        'latent',           #: -> latents
                                #= Which latent is given upon feed.
        #64
        '_UNK64',           #: -> collab
                                #? Which collab?
        '_flags65',         #: flags[3]
                                #= Flags for inheritance.
    ]
    #? Flatten constant-sized arrays?
        #- Pre-evo mats.
        #- Evo mats. (set/counter)
        #- HP/Atk/RCV (+ enemy versions).
        #- Type. (set)
    #? Use `._thing` for the original value and `.thing` for the semantic value?
        #- E.g.
            #- Make `._type3` the original int value and `.type3` a MonsterType object.
            #- `.base` is a BookCard and `._base` is its ID.
        #- Or `.o_base` for "original `.base`".
    sdleif = {attr:i for i, attr in enumerate(fields)}
    
    # Additional properties.
    properties = {
        'types': lambda c:
                {t for t in (c.type1, c.type2, c.type3) if t != -1},
        'mats': lambda c:
                list(filter(bool,
                    (getattr(c, 'evomat%d' % (i+1))
                        for i in range(5)))),
        'sortkey':  # Monsterbook sortkey "Group".
            lambda c:
                # (c.base, c.preevo, c.id),
                # (c.gkey/10 if c.gkey else c.base, c.base, c.id),
                # (c.gkey/10 if c.gkey else c.base, c.gkey, c.base, c.id),
                # (c.gkey/10 or c.base, c.id),
                (c.gkey/10 or c.base, c.gkey, c.base, c.id),
        'inheritable':
            lambda c:
                c._flags65 & 1,
    }
    
    def __init__(self, raw):
        ## Unflatten the arrays.
        raw = unflatten_card(raw, self.sdleif['eskills'], replace=True)
        super().__init__(raw)


class BookCard900(BookCard920):
    """BookCard, except that you have to pass in the card ID manually.
    
    API version 9.0.0.
    """
    def __init__(self, idnum, raw):
        super().__init__([idnum, *raw])


def unflatten_card(raw, i, replace):
    """Unflatten a card array.
    
    Params:
        i:
            Index of enemy_skill count.
            From 9.2, it's 57. Before that, it's 56.
        replace:
            If False, eskills will just hold the number of enemy skills.
    """
    raw = list(raw)
    s = slice(i+1, i+1 + 3*raw[i])
    eskills = tuple(util.takes(raw[s], 3))
    del raw[s]
    s = slice(i+2, i+2 + raw[i+1])
    awkns = raw[s]
    del raw[s]
    if replace:
        raw[i:i+2] = eskills, awkns
    return raw



'''Problem: Given a card, find its final evo.
    - The issue is, it would need access to the rest of the cards.

Solutions?:
    - Always go through a PadData.
    - BookCards have a link to their BookCardDB object.
        - The BookCardDB object will have:
            - Evo map.
            - 
    - Register evos onto cards as we're reading them.
        ``  # Maps pre-evo ids to BookCards.
            buckets = bucketize(cards, aget('preevo'))
            
            for monid, evos in items(buckets):
                mon = cards[monid]
                mon.evos = evos
            return cards
'''

# def descendents(card):
    # try:
        # yield from card.evos
    # except AttributeError:
        

