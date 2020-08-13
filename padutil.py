# padutil.py

from util import *
from datetime import datetime as DT
import csv

def ghtime(s):
    #<  151228000000
    #>  2015-12-28 00:00:00
    #!TODO: Make sensitive to DST history?
    if isinstance(s, int):
        s = str(s)
    return DT.strptime(s, '%y%m%d%H%M%S')


gh_time = ghtime
    # Until I figure out which name I want.


def dispID(ID):
    """Permutes internal PAD ID to the displayed form.
    """
    ID = str(ID).zfill(9)
    return ''.join(ID[x-1] for x in [1,5,9,6,3,8,2,4,7])


# def gh_csv(raw):
    # # doesn't correctly deal with newlines in a field
    # typ, rest = line.split(';', 1)
    # args = [typ]
    # try:
        # while rest:
            # if rest[0] == "'":
                # quot = "'"
                # var, rest = rest[1:].split("',", 1)
            # elif rest[0] == '"':
                # quot = '"'
                # var, rest = rest[1:].split('",', 1)
            # else:
                # quot = ''
                # var, rest = rest.split(",", 1)
            # args.append(var)
    # except ValueError:
        # if rest[0] in '\'"':
            # assert rest[-1] == rest[0]
            # rest = rest[1:-1]
        # args.append(rest)
    
    # return args




def gh_csv(raw):
    """
    Gungho's terrible CSV with unescaped quotes.
        ? Wait maybe it's valid csv and I just screwed up before??
    
    CSV is used in:
        - dungeon_data
        - get_dung_sale (without first semi-colon)
        - shop_item (without first semi-colon)
        - dl_al (without first semi-colon)
            
    """
    lines = raw.splitlines(True)
    # # ugh
    # # Hopefully they never put a ' at the end of a line.
    # lines = (line
                # #startquote
                # .replace(",'", ",\0")
                # .replace("\n'", "\n\0")
                # #endquote
                # .replace("',", "\0,")
                # .replace("'\n", "\0\n")
                # #leftover
                # .replace("'", "''")
                # #now change it back
                # .replace("\0", "'")
        # for line in lines)
    
    lines = (line.replace(';', ',', 1)
            if line[1] == ';' else line
            for line in lines if line)
    
    csvraw = csv.reader(lines, 
        delimiter=',',
        quotechar="'",
        doublequote=True,
        strict=True)
    
    result = list(csvraw)
    # assert result[-1][0] == 'c' #crc
    return result


# def gh_csv(raw):
    # """
    # Gungho's terrible CSV with unescaped quotes.
    # """
    # # Escaping quotes on the original raw.
    # lines = (line.replace(';', ',', 1)
            # if line[1] == ';' else line
            # for line in raw
                            # #startquote
                            # .replace(",'", ",\0")
                            # .replace("\n'", "\n\0")
                            # #endquote
                            # .replace("',", "\0,")
                            # .replace("'\n", "\0\n")
                            # #leftover
                            # .replace("'", "''")
                            # #now change it back
                            # .replace("\0", "'")
                            # #and split
                            # .splitlines(True))
    
    # csvraw = csv.reader(lines, 
        # delimiter=',', 
        # quotechar="'", 
        # doublequote=True, 
        # strict=True)
    
    # bag = Bag(csvraw)
    # assert bag[-1][0] == 'c' #crc
    
    # # return bag[:-1]
    # return bag[:-1]
# #

