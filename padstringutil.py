# -*- coding: UTF-8 -*-

## PAD string utilities.
## python 2/3

try:
    range = xrange
except NameError:
    pass

import string

PUNCTUATION = set(string.punctuation + string.whitespace + u'　')


def isvalidstring(s):
    return (s
        # and s[:4] not in (u'****', u'????')
        # and s[0] not in u'*? '  # SIIIIIII
        and s[0] not in u'*?'     #  IIIIIII
        and s != u' nya!'         #  IIIIIIIGH.
        and s != u"\u7121\u3057"   # "Nashi".
        and u'_' not in s
    )




def isvalidstringNA(s):
    return (isvalidstring(s)
        and not hasJPchars(s)
        and s != u'Monster Hunter 4G Collab Series'
    )

def hasJPchars(s):
    """ Checks for hints that this is a Japanese name.
    
    ? Is this to see if it's an English name, or is it to guess if it's JP-only?
    """
    return any(any(c in block for block in jpcharblocks)
            and c not in weirdNAchars
            for c in set(map(ord, s)))



jpcharblocks = (
    ## http://stackoverflow.com/a/30200250
    ## http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
    range(0x3000, 0x3100),  # Katakana and hiragana.
    range(0x3400, 0x4dc0),  # Rare kanji.
    range(0x4e00, 0x9fb0),  # Common CJK.
    # range(0xff00, 0xfff0),  # Special roman characters, and half-width kana.
    range(0xFF66, 0xFFDD),  # Conservative: Allow special Roman characters.
)
## ARG WHY ARE THERE THESE CHARACTERS IN SKILL DESCRIPTIONS.
weirdNAchars = {
    0x3000,  # ?? in Crows Collab LSs.
    0x223c, 0xff4e,  # "∼ｎ" in Polaris&Kapibara-san.
    0xff53,  # Invisible `S` in Mechdragon actives.
    # *range(0x2200, 0x2300),  # Math characters. (WHY YOU DO THIS GUNGHO)
}


