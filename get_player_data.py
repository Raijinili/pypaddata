from collections import Counter

import dataclass

class BoxCard(dataclass.DataClass):
    "A card in a player's box."
    fields = [
        'chrid', # Internal ID.
        'xp',
        'lv',
        'slv',
        'fuses', # Dumb and useless.
        'no', # Monster ID.
        'plus_hp',
        'plus_atk',
        'plus_rcv',
        'tamas',
        'latents', # Packed bits representing latents.
    ]
    __slots__ = fields
    properties = {
        'plusses': lambda c: c.plus_hp + c.plus_atk + c.plus_rcv,
    }
    
    def __init__(self, rawcard):
        for name, value in zip(self.fields, rawcard):
            setattr(self, name, value)

    # Need to override DataClass's repr.
    def __repr__(self):
        return '%s<%r, %r>' % (type(self).__name__, self.chrid, self.no)





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
    ct = raw & 0x0F  #number of latent slots
    raw >>= 4
    latents = []
    for _ in range(ct):
        latents.append(raw & 0x1F)
        raw >>= 5
    assert raw == 0
    return tuple(latents)


def repack_latents(latents):
    if not any(latents):
        return 0
    raw = 5
    shift = 4
    for latent in latents:
        raw |= latent << shift
        shift += 5
    return raw

