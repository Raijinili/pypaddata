## Abstract base class of a paddata class.

from abc import ABC

from util import isiterable

class DataClass(ABC):
    """Abstract base class of a paddata class.
    
    Expected:
        + Class attrs:
            - .fields: list
                Names for each field.
            - .properties: dict
                - Keys: property names.
                - Values: One of:
                    - int: A
            - .packing: list
                ! Optional.
                - Specifies the packing.
                    - E.g. `Card`'s awakenings and eskills.
        + Instance attributes:
            (For __repr__.)
            - .id
            - .name
    """
    #? Allow .fields to be a dict?
        #- E.g. skill data is a dict.
        #- E.g. limited_bonus.
        #- .fields would be the same shape as the raw.
    #? Make unknowns `None`?
    properties = {}
    def __init__(self, raw):
        if len(raw) != len(self.fields):
            raise ValueError("DataClass {} expected len(raw) == {} but got len(raw) == {}"
                             .format(type(self).__name__, len(self.fields), len(raw)))
            # raise ValueError(f"DataClass {type(self).__name__} expected len(raw) == {len(self.fields)} but got len(raw) == {len(raw)}")
        self.raw = tuple(raw)
        for attr, val in zip(self.fields, raw):
            setattr(self, attr, val)
    
    def __getattr__(self, attr):
        try:
            return self._get(attr)
        except Exception as e:
            raise AttributeError(attr) from e
    
    def _get(self, attr):
        index = self.properties[attr]
        if isinstance(index, str):  # Alias.
            val = getattr(val, index)
        elif isiterable(index):       # Multiple things?
            val = type(index)(self._get(attr) for attr in index)
                #^ I want to keep the original collection type.
        elif callable(index):
            val = index(self)
        setattr(self, attr, val)    # Cache it.
        return val
    
    def __repr__(self):
        return '%s<%r, %r>' % (type(self).__name__, self.id, self.name)



