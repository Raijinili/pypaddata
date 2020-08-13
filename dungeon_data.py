# dungeons.py

import os
import sys
import json
import codecs
import warnings

import util
from util import ojson_load, ojson_loads, Index
from padutil import gh_csv
import datafiles

## TODO:
    #- Change color codes $47ae64$ to something like $Y$ for yellow.
        #- Use a utility func for this!
            #- Handle both ^ and $ (separately).
                #- They are used in different places. ($ for CSV?)
        #- GH is using "#G#" for urgent jewel dragons.
    #- Figure out and fix the v=6 d; args.


class Dungeon:
    # def __init__(self, raw):
        # self.raw = raw[1:]
        # self.id = int(self.raw[0])
        # self.name = self.raw[1].replace("''", "'")
            # # Hack because I can't figure out why the CSV is being a jerk.
        # self.floors = []
    def __init__(self, raw, v):
        self.raw = raw[1:]
        _, rawid, rawname, *rest = raw
        self.id = int(rawid)
        self.color, self.name = parse_color(rawname)
        self.floors = []
        if v < 6:
            assert len(self.raw) == 6
        else:
            if self.raw[6] == '':
                self.raw[6] = '0'
            assert len(self.raw) in range(8, 10)
            if len(self.raw) == 10:
                assert self.raw[-1] != '0'

    def __str__(self):
        return self.name
    def __repr__(self):
        return "Dungeon<%r, %r>" % (self.id, self.name)
    def append(self, floor):
        self.floors.append(floor)


class Floor:
    def __init__(self, raw, v):
        self.raw = raw[1:]
        [   _, idnum, name, 
            *args
        ] = raw
        self.id = int(idnum)
        self.color, self.name = parse_color(name)
        [
            self.floors, self.UNK_3,
            self.stamina, self.UNK_5,
            self.UNK_6, self.disables,
        ] = map(int, args[:6])
        args = args[6:]
        if v >= 6: #drops
            i = args.index('0')
            self.drops = list(map(int, args[:i]))
            args = args[i+1:]
        else:
            self.drops = None
        #- Parse the flagged args and verify them.
        flags = int(args[0])
        rest = args[1:]
        try:
            self.args = parseflaggedargs(flags, rest)
        except AssertionError as e:
            #! ugh not having actual messages
            # print("AssertionError: ", e, "while parsing", raw, file=sys.stderr)
            print("While parsing", raw, file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
        ...
    
    def __str__(self):
        return self.name
    def __repr__(self):
        return "Floor<%r, %r>" % (self.id, self.name)


def parse_color(rawname):
    if rawname[0] in '#$':
        color, name = rawname[1:].split(rawname[0], 2)
    else:
        color, name = None, rawname
    return color, name


def parseflaggedargs(flags, args):
    assert flags == flags & 0xFF, "Unknown flags: 0x%X" % (flags & ~0xFF)
    arglist = [None]*8
        # Should instead start with a default.
    #[2020-01] Why do I take `args[:1]` instead of args[0]?
    #[2020-04] Why don't I use `arglist[6], *args = args`?
    if flags & 1:
        arglist[0] = args[:2]
        args = args[2:]
    if flags & 2:
        raise ValueError("Unexpected.")
    if flags & 4:
        arglist[2] = args[:1]
        args = args[1:]
    if flags & 8:
        arglist[3] = args[:1]
        args = args[1:]
    if flags & 16:
        arglist[4] = args[:1]
        args = args[1:]
    if flags & 64: #multipliers?
        arglist[6] = args[:1]
        args = args[1:]
    #? Not sure if 128 should be checked before 32.
    assert flags & 160 != 160, "Check flags 32 vs 128"
    if flags & 128: #multipliers?
        arglist[7] = args[:1]
        args = args[1:]
    if flags & 32:
        # arglist[5] = args
        arglist[5] = list(map(int, args))
            # Seems to work.
        try:
            parseflag32args(arglist[5])
        except AssertionError as e:
            raise AssertionError("A32:%s:%s" % (args[0], args[1:])) from e
            #? Why not just let the assert bubble up?
    else:
        assert args == ['0', '0']
    return arglist

def parseflag32args(args):
    """For flags&32, assert that the `rest` is expected from the `first`.
    """
    first, *rest = args
    if first == 2:  # Cost <= %d
        assert len(rest) == 1
    elif first == 4:  # Rarity <= %d
        assert len(rest) == 1
    elif first == 7:  # {Type} Only
        assert rest and all(rest)
    elif first == 9:  # {*Attrs} required
        assert rest == list(range(1,6)), "Not all atts required."
    elif first == 10:  # No Dupes (for what args??)
        # assert len(rest) == 1
        # assert rest[0] in [0,4]
        pass #forget it
    elif first == 11:  # Special (roguelike)
        assert len(rest) == 5
    # New since I last checked, which was a long while ago.
    elif first == 13: #<=4 Challenge?
        assert len(rest) == 1
    elif first == 14: #<=4 Challenge?
        assert len(rest) == 1
    else:
        assert False, "Unknown flag32: " + first



def read_dungeons(raw, v):
    dungeons = Index()
    current = None
    for line in gh_csv(raw):
        if line[0] == 'd':
            current = Dungeon(line, v)
            dungeons[current.id] = current
        elif line[0] == 'f':
            current.append(Floor(line, v))
        elif line[0] == 'c':
            continue
        else:
            assert 0
    return dungeons
#


def load(folder_path=None):
    """Load the JSON from given folder.
    """
    if folder_path is None:
        import datafiles
        folder_path = datafiles.root
    return loadfile(os.path.join(folder_path, 'download_dungeon_data.json'))


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
    raws = j['dungeons']
    v = j.get('v', 1)  # version
    if v not in (3, 4, 6):
        warnings.warn("Dungeon JSON has unknown version %s." % (v))
    dungeons = read_dungeons(raws, v)
    return dungeons




# fname = datafiles.dungeon

# j = util.ojson_load(fname)
# raw = j['dungeons']
# dungeons = read_dungeons(raw, j.get('v', 1))


