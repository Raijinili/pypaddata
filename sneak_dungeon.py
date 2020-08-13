
from padcrypt import decodePadDungeon


class SneakData:
    """ Holds wave data.
    
    """
    def __init__(self, waves):
        """
        """
        
        '''
        Waves are structured as:
            * waves[floor] = wave
            * wave[i] = mon
            * mon = [??, enemy_id, enemy_lv, drop_id, drop_lv, ??]
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
            mon = wave.mons[i]
            mon.name
            mon.lv
            
            drop = wave.drop
            if drop is not None:
            
            sdata.coins
            waves.
            
        '''
        floors = self.floors = []
        
        for wave in waves:
            wave
        
    
    @classmethod
    def from_encrypted(cls, ciphertext):
        """
        
        """
        assert cls == SneakData, "Not ready for subclassing"
        
        return cls.from_decrypted(decodePadDungeon(ciphertext))
    
    @classmethod
    def from_decrypted(cls, plaintext):
        """ Create from plaintext.
        
        
        """
        assert cls == SneakData, "Not ready for subclassing"
        
        # Example:
        '''
waves=[["w":[1,161,5,161,1,0],[1,162,5,0,0,0],[1,163,5,0,0,0],[0,164,5,0,0,0]],["w":[1,166,10,0,0,0],[1,167,10,0,0,0],[1,168,10,0,0,0],[0,170,10,170,1,0]],["w":[1,171,2,0,0,0],[1,172,2,0,0,0],[1,173,2,173,1,0],[0,175,2,0,0,0]],["w":[1,161,5,161,1,0],[1,234,2,0,0,0],[1,161,5,0,0,0]],["w":[1,1294,1,0,0,0],[1,1295,1,1295,1,0]]]&dh=571748813127c&rs=8
        '''
        # Strip out stuff.
        #waves_txt = plaintext.split('=&')[1].replace('"w":', '')
        waves_txt = parse_uriparams(plaintext)['waves'].replace('"w":','')
        
        assert not set(waves_txt) - set(digits + ',[]'), 'Unexpected characters.'
        waves = eval(waves_txt)
        
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
    

def parse_uriparams(uri_params):
    """Decodes URI params and returns a dict.
    
    URI params are `<name>=<val>` pairs, delimited by '&'.
    """
    return FunFunFunOK(url_params.split('&')).map(lambda s: s.split('=',1)).to(dict)

def parse_uriparams(uri_params):
    """Decodes URI params and returns a dict.
    
    URI params are `<name>=<val>` pairs, delimited by '&'.
    """
    return dict(parse_qsl(uri_params))

