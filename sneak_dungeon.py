import json
from urllib.parse import parse_qsl
try:
    import padcrypt
except ImportError:
    print("Warning: Don't know how to decrypt sneak_dungeon.")

# Need to get:
#- card_db
#- non-monster types (e.g. gold)
#- 

__all__ = [
    'SneakData',
]


class SneakData:
    """ Holds wave data.
    
    """
    def __init__(self, waves):
        """
        """
        
        '''
        Waves are structured as:
            * waves[floor] = wave
            * wave[i] = spawn
            * spawn = [??, enemy_id, enemy_lv, drop_id, drop_lv, plusses]
                - All ints.
        '''
        '''
        goal:   
            sdata = SneakData(...)
            sdata
                .coins: int
                .xp: int
                .drops
                # who really cares about chests?
                    # well, they matter for dropcount.
            wave = sdata[floor]
            spawn = wave.spawns[i]
            spawn.name
            spawn.lv
            
            drop = wave.drop
            if drop is not None:
            
            sdata.coins
            waves.
            
        '''
        floors = self.floors = []
        
        for wave in waves:
            wave
            # incomplete
    
    @classmethod
    def from_encrypted(cls, ciphertext):
        """
        
        """
        assert cls == SneakData, "Not ready for subclassing"
        
        return cls.from_decrypted(padcrypt.decodePadDungeon(ciphertext))
    
    @classmethod
    def from_decrypted(cls, plaintext):
        """ Create from plaintext.
        
        
        """
        assert cls == SneakData, "Not ready for subclassing"
        
        waves = _query2wavelist(plaintext)
        return cls(waves)
    
    def encrypted(self):
        raise NotImplementedError("Haha no you cheater.")

    def yaml(self):
        """
        
        """
        
        ''' Goal:
        
        dungeon_name:
          Drops:
            - Rank XP
            - Coins
            - Mon (Lv)
            - Mon (Lv)
          Floors:
            - drop: Mon (lv)
              enemies:
                - Mon (lv)
                - Mon (lv)
                - Mon (lv)
            - drop: Mon (lv)
              enemies:
                - Mon (lv)
                - Mon (lv)
                - Mon (lv)
        '''
    
    def html(self):
        """
        
        """
        
        ''' Goal:
        
        dungeon_name:
            - drop: Mon (lv) | None
              enemies:
                - id. mon_name (lv)
                - id. mon_name (lv)
            - drop: Mon (lv)
              enemies:
                - id. mon_name (lv)
                - id. mon_name (lv)
        '''


class Spawn:
    # Needs card_data for:
        #- Name
        #- XP
        #- 
    # Needs bonus info for non-monster drops.
    def __init__(self, raw):
        self._unk, self.mon_id, self.lv, self.drop, self.dropvar, self.plusses = raw
    
    def display(self, card_db):
        """Given a source of card info, display this spawn.
        """
        mon = card_db[self.mon_id]
        mon_s = f"{mon.name} @ lv{self.lv}"
        if self.drop == 0:
            return mon_s
        elif self.drop < 9900:
            drop = card_db[self.drop]
            drop_lv = self.dropvar
            drop_s = f"{drop.name} @ {drop_lv}"
        elif self.drop == 9900:
            drop_s = f"{self.dropvar} coins"
        else:
            drop_s = f"(other) @ {self.dropvar}"
        return f"{mon_s}: {drop_s}"


def parse_uriparams(uri_params):
    """Decodes URI params and returns a dict.
    
    URI params are `<name>=<val>` pairs, delimited by '&'.
    """
    return dict(s.split('=', 1) for s in uri_params.split('&'))

def parse_uriparams(uri_params):
    """Decodes URI params and returns a dict.
    
    URI params are `<name>=<val>` pairs, delimited by '&'.
    """
    return dict(parse_qsl(uri_params))


def _j2wavelist(s):
    """
    Input: JSON string or dict.
    Output: wave list.
    """
    if isinstance(s, str):
        e = json.loads(s)['e']
    else:
        e = s['e']
    plaintext = padcrypt.decodePadDungeon(e)
    return _query2wavelist(plaintext)

def _query2wavelist(plaintext):
    """Handles the deciphered text.
    
    Like 'waves={WAVELIST}&dh={DH}&rs={RS}'
    """
    # raw_waves = parse_uriparams(plaintext)['waves']
    raw_waves = plaintext.split('&')[0].split('=')[1]
    wave_arr = json.loads(raw_waves.replace('"w":', ''))

    # # Or use eval.
    # assert not set(raw_waves) - set(digits + ',[]'), 'Unexpected characters.'
    # wave_arr = eval(raw_waves)

    return wave_arr



