action = 'download_skill_data'
ver = 'sver'
datanum = 36
jsonkey = 'skill'

import os

from util import ojson_load, ojson_loads
from util import keys, values, items, Bag, Index
import datafiles
# from dataclass import DataClass
# import skill_types
from skill_types import skill_types
import itertools

# class Skill(DataClass):
class Skill:
    """
    """
    #! `.params` is 0-indexed instead of 1-indexed.
    #! `.params` takes up more memory than the original, because I fill in the gaps.
        #^ Instead, I can:
            #? Try-catch everywhere?
            #? Is there a .get(i, 0) for tuples?
            #? Use a dict instead?
                #- Probably even worse.
            #? Custom tuple class?
            #? Truncate by skilltype?
                #- Causes error if unexpected val.
    action = 'download_skill_data'
    jsonkey = 'skill'  # JSON key in the json file.
    
    fields = [
        'name',  # str: Name.
        'help',  # str: Description.
        'sktp',  # int: Skill type.
        'lcap',  # int: Level cap.
        'ctbs',  # int: Skill turns at level 1.
        'ctel',  # int: 0 if LS, -1 if AS.
    ]
    def __init__(self, idnum, raw):
            #? Should idnum come first?
        self.id = idnum
        self.raw = raw
        if isinstance(raw, dict):  # Before 12.2.0.
            for field in self.fields:
                setattr(self, field, raw[field])
            self.params = tuple(raw.get('skp%d' % (i+1), 0)
                        for i in range(8))
        elif isinstance(raw, list):  # 12.2.0.
            for i, field in enumerate(self.fields[:-1]):
                setattr(self, field, raw[i])
            self.ctel = -(self.lcap > 0)
            self._UNK5 = raw[len(self.fields)-1]
            self.params = tuple(raw[len(self.fields):] + [0]*8)[:8]
        else:
            raise TypeError("Unknown raw type:", type(raw))
    
    @property
    def desc(self):
        """Description text for this skill.
        
        """
        raise NotImplementedError
        # return desc_maker[self.sktp](self.params)
        return skill_types[self.sktp](self.params).desc
    
    
    @property
    def isactive(self):
        return self.ctel == -1
    
    def __repr__(self):
        # return 'Skill(%s, %r)' % (self.id, self.name)
        #? Remove the trailing 0s from params?
        return f'Skill({self.id!r}, {self.name!r}, {self.sktp!r}, {self.params!r})'



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
    if v in {1, 1220}:  # Original version or array version.
        skills = Index((i, Skill(i, raw)) for i, raw in items(raws))
    else:
        # raise ValueError("%r has unknown skills version %s." % (fpath, v))
        raise ValueError("Skill data has unknown skills version %s." % (v,))
    return skills




def skillbag(skills, skid):
    """Flatten a skill."""
    if not isinstance(skid, int):
        skid = skid.id
    return Bag(_skillbag(skills, skid))

def _skillbag(skills, skid):
    sk = skills[skid]
    if sk.sktp not in (116, 138): #AS, LS
        yield sk
    else:
        yield from itertools.chain.from_iterable(_skillbag(skills, p) for p in filter(bool, sk.params))









