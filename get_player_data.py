from collections import Counter

import dataclass

class BoxCard(dataclass.DataClass):
    "A card in a player's box."
    fields = [
        'chr',      #0. Internal (chronological) ID.
                        # Change to id? We do need lookup by ID.
        'xp',
        'lv',
        'slv',
        'fuses',    #4. Useless.
        'cid',      #5. Monster ID. (Can I change this to id?)
        'plus_hp',  
        'plus_atk',
        'plus_rcv',
        'tamas',    #9. Number of tamas (up to 10)
        # Newer:
        'latbits',  #10. Packed bits representing latents.
        'inherit',  #11. Inherit's CHR
        'saplus',   #12. Super Awakening plus progress.
        'sawkn',    #13. Super Awakening.
        '_unk14',   
    ]
    __slots__ = fields  #Should I slots here?
    defaults = [0]*len(fields)  #for now.
    properties = {
        'plusses': lambda m: m.plus_hp + m.plus_atk + m.plus_rcv,
        'latents': lambda m: unpack_latents(m.latbits),
    }
    
    def __init__(self, raw):
        # for name, value in zip(self.fields, raw):
            # setattr(self, name, value)
        # Pad with 0s.
            #? Maybe handle defaults in DataClass
        raw.extend(self.defaults[len(raw):])
        
        super().__init__(raw)

    # Need to override DataClass's repr.
    def __repr__(self):
        return '%s<%r, %r>' % (type(self).__name__, self.chr, self.cid)





# def unpack_latent(latent):
    # bits = bin(latent)[2:]
    # parts = []
    # for i in range(0, -25, -5):
        # parts.append(int(bits[-9+i:-4+i] or '0', 2))
    
    # #print parts
    # return parts


# def unpack_latents(latents):
    # if not latents:
        # return (0,0,0,0,0)
    
    # bits = bin(latents)[2:-4].zfill(25)
    # parts = []
    # for i in range(0, -25, -5):
        # parts.append(int(bits[-9+i:-4+i] or '0', 2))
    
    # #print parts
    # return parts

# def unpack_latents(raw):
    # if not raw:
        # return (0,0,0,0,0)
    # raw //= 0x10
    # latents = []
    # for _ in range(5):
        # raw, lat = divmod(raw, 0x20)
        # latents.append(lat)
    # return latents


# def repack_latents(latents):
    # # Test for order:
        # # repack_latents([5, 5, 3, 2, 1])
        # #   => 17877589
    # if not any(latents):
        # return 0
    # raw = 0
    # for latent in reversed(latents):
        # raw = raw * 0x20 + latent
    # raw = raw * 0x10 + 5
    # return raw

# def repack_latents(latents):
    # if not any(latents):
        # return 0
    # raw = 5
    # m = 0x10
    # for latent in latents:
        # raw += m * latent
        # m *= 0x20
    # return raw


def unpack_latents(raw):
    """Unpack latents.
    
    Returns a tuple of size 0, 5, or 6.
    """
    #! The latents come out backwards.
    # if raw == 0:
        # return (0,0,0,0,0)
    ct = raw & 0xF  #number of latent slots
    raw >>= 4
    if ct == 0xF:
        # New version with more slots and bigger values.
        ct = raw & 0xF
        raw >>= 4
        bpl = 7  #bits per latent
    else:
        bpl = 5
    mask = (1<<bpl) - 1
    latents = []
    for _ in range(ct):
        latents.append(raw & mask)
        raw >>= bpl
    assert raw == 0
    return tuple(latents)


def repack_latents(latents):
    #! Doesn't handle new version.
        # It's fine to always use new version now, even if it doesn't use new features.
    if not any(latents):
        return 0
    raw = 5
    shift = 4
    for latent in latents:
        raw |= latent << shift
        shift += 5
    return raw



