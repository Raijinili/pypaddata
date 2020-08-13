## datafiles.py
    #= Lists the current data files

import os
base = os.path.dirname(os.path.abspath(__file__))


root = INSERT_JSON_FOLDER_PATH_HERE
    #^ I should instead load the list from a file.

dungeon = root + 'download_dungeon_data.json'
card = root + 'download_card_data.json'
skill = root + 'download_skill_data.json'


