from util import keys, values, items

__all__ = [
    'PadDB',
]

class PadDB:
    """Proxy for a read-only indexable.
    
    Doesn't load file unless used.
    """
    def __init__(self, loader):
        self.load = loader
    def __getattr__(self, attr):
        if attr == 'db':
            self.db = self.load()
            return self.db
        else:
            raise AttributeError
    
    def __getitem__(self, index):
        return self.db[index]
    
    def keys(self):
        return keys(self.db)
    def values(self):
        return values(self.db)
    def items(self):
        return items(self.db)
    def __len__(self):
        return len(self.db)
    def __reversed__(self):
        return reversed(self.db)
    
    # def __iter__(self):
        # return values(self.db)

###

# cards = PadDB(load)

