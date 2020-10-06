#name = 'enemy_skill_data'
action = 'download_enemy_skill_data'
ver = 'msver'
datanum = 29
jsonkey = 'enemy_skills'

import os, os.path
import warnings

from util import ojson_load, ojson_loads, Index
from padutil import gh_csv
from dataclass import DataClass


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
    #TODO: Cache it based on filepath.
        #! Check modified time.


def loads(s):
    j = ojson_loads(s)
    return loadjson(j)


def loadjson(j):
    """Load from JSON dict.
    """
    raw = j['enemy_skills']
    v = j.get('v', 1)  # version
    # v=1: dict-based
    # v=2: csv
    if v == 1:
        table = parse_1(raw)
    elif v == 2:
        table = parse_2(raw)
    else:
        warnings.warn("Enemy Skill JSON has unknown version %s." % (v))
        table = parse_2(raw)
    
    eskills = Index((row[0], EnemySkill(row)) for row in table)
    return eskills


def parse_1(raw):
    return [jso_to_list(i,o) for i,o in enumerate(raw)]


def parse_2(raw):
    table = ugh_csv(raw)
    assert table.pop()[0] == 'c' #Drop the checksum.
    return list(map(row_to_list, table))


import regex as re
line_pattern = re.compile(r"""
    ^
    (?:             # No capture groups, to modify findall behavior.
     ,              # empty
    |[^'][^,\s]*+,     # no quote
    |'(?:[^']|'[^,\r\n])++',
        # quoted, but no ', or '\n or space in middle
    )*+
    (?:
     $
    |[^'][^,\s]*+$
    |'(?:[^']|'[^,\r\n])++'$
    )
    (?:\r?\n|\Z)       # Oops, need to worry about the last line.
        # ^That \Z means I need to strip the last line.
""", re.VERBOSE|re.MULTILINE)

field_pattern = re.compile(r"""
    (   # Ignore the empty pattern so that it doesn't give me an unexpected final empty.
     [^'][^,\s]*+
    |'(?:[^']|'[^,\r\n])++'
    )
    (?:,|\r?\n|\Z)
""", re.VERBOSE)

def ugh_csv(raw):
    # Replace newlines that are within quotes with \n.
    # Count the number of apostrophes that are between commas.
        # Can there be an apostrophe next to a comma within a string?
    # enemy_skills doesn't seem to use the double comma.
    # Maybe add this feature to gh_csv.
    raw = raw.strip()
    lines = line_pattern.findall(raw)
    # Escape newlines in the middle of a line.
    assert ''.join(lines) == raw, "Line pattern didn't fully match!"
    # lines = [line.strip().replace('\n', '\\n') + '\n'
        # for line in lines]
        #^ Don't need to do this if I'm not passing to gh_csv?
    table = []
    for line in lines:
        row = []
        for item in field_pattern.findall(line.strip()):
            # Given the regex, there should be no empties and no mismatched quotes.
            if item and item[0] == "'" or item[-1] == "'":
                # Strip quote.
                assert item[0] == item[-1], "Mismatched quotes"
                item = item[1:-1]
            row.append(item)
        table.append(row)
    return table


# sample for ugh_csv.
_sample = """
234,'Dark Wind',5,1,'Unable to see Orbs'
1061,'I'll show you then',69,f,'If you want to die so badly, I'll show you!!|I won't be as gentle as I was before...',26,1,2
1062,'It's the first time I ever used this transformation!',69,7,'You are the first ones to ever see this!|Thank you for waiting...',26,2
1063,'My true form!!!',69,7,'Feast your eyes while you can!!
On my final transformation!!|I'll show you a nightmare beyond the horrors of hell...',26,3
1064,'Binding Wave',14,2007,'Skills are unusable',5,5,1
""".lstrip()


class EnemySkill(DataClass):
    fields = [
        'id',
        'name',
        'type',
        'help',
        'skp1',
        'skp2',
        'skp3',
        'skp4',
        'skp5',
        'skp6',
        'skp7',
        'skp8',
        'ratio',
        'aip0',
        'aip1',
        'aip2',
        'aip3',
        'aip4',
        '_UNK8000', #flag 8000
    ]
    sdleif = {attr:i for i, attr in enumerate(fields)}
    
    def __init__(self, raw):
        super().__init__(raw)


def jso_to_list(i, o):
    """v=1. Takes a JSON object representing an enemy skill.
    
    No need to specify defaults, because each had all keys.
    """
    return [
        i,       #id
        o['name'],
        o['type'],  # Swapped order with 'help' in JSON.
        o['help'],
        o['skp1'],
        o['skp2'],
        o['skp3'],
        o['skp4'],
        o['skp5'],
        o['skp6'],
        o['skp7'],
        o['skp8'],
        o['ratio'],
        o['aip0'],
        o['aip1'],
        o['aip2'],
        o['aip3'],
        o['aip4'],
        0,      #new thing in version 2, I dunno.
    ]


# name, type, default
packedparams = [
    ('help', str, ''),
    ('skp1', int, 0),
    ('skp2', int, 0),
    ('skp3', int, 0),
    ('skp4', int, 0),
    ('skp5', int, 0),
    ('skp6', int, 0),
    ('skp7', int, 0),
    ('skp8', int, 0),
    ('ratio', int, 100),
    ('aip0', int, 100),
    ('aip1', int, 100),
    ('aip2', int, 10000),
    ('aip3', int, 0),
    ('aip4', int, 0),
    ('_unk8000', int, 0),
]

def row_to_list(r, packedparams=packedparams):
    """v=2
    
    Includes ID, which isn't saved here.
    """
    
    rv = [
        int(r[0]),
        r[1], #name
        int(r[2]), #type
    ]
    flags = int(r[3], 16)
    assert flags < 1<<len(packedparams), "New unknown parameter"
    itr = iter(r[4:])
    # for i, (name, typ, default) in enumerate(packedparams):
        # if flags & (1<<i):
            # value = typ(next(itr))
        # else:
            # value = default
        # rv.append(value)
    rv.extend(
        typ(next(itr))
        if flags & (1<<i)
        else default
        for i, (name, typ, default) in enumerate(packedparams)
    )
    assert next(itr, None) is None, "Unhandled args"
    return rv



