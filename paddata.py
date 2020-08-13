## paddata.py
    ## The starting point for paddata.

import datafiles
import card_data
import skill_data
import dungeon_data

#TODO:
    #?- Lazy load?


cards = card_data.load(datafiles.dataroot)
skills = skill_data.load(datafiles.dataroot)
dungeons = dungeon_data.load(datafiles.dataroot)
    #^ I want a circular import?
        #^ Because limited_bonus_data relies on dungeon_data.

