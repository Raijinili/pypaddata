## util.py
    #= Utility things not specific to PAD.
        ## Maybe some day I'll move them to my personal folder.

from functools import lru_cache, wraps, partial
from collections import OrderedDict
# import csv
import json
try:
    from cached_property import cached_property
except ImportError:
    raise ImportError("`cached_property` not installed!")
import warnings
import inspect


def Id(x): # Identity function.
    return x

DEFAULT = object()


class Index(OrderedDict):
    """Like an ordered dict but default iter by values.
    """
    def __iter__(self):
        return iter(self.values())


class OrderedJSON(OrderedDict):
    """An OrderedDict which acts like a JavaScript object.
    
    In other words, `j.x is j['x']`.
    """
    __slots__ = ()
    @cached_property
    def _o(self):
        """Exposes an explicit JSO view.
        
        Names like 'items' would be shadowed, otherwise.
        """
        return ObjectView(self)
    
    def __getattr__(self, key):
        try:
            return getattr(self._o, key)
        except AttributeError:
            raise AttributeError('%r object has no attribute %r'
                            % (type(self).__name__, key)) from None

    def __setattr__(self, key, val):
        setattr(self._o, key, val)

    def __delattr__(self, key):
        try:
            delattr(self._o, key)
        except AttributeError:
            raise AttributeError(
                    '%r object has no attribute %r'
                            % (type(self).__name__, key)
                  ) from None


class ObjectView:
    """Object view of a dict.
    """
    def __init__(self, d):
        self.__dict__ = d


def ojson_load(fpath):
    """Read file as OrderedJSON.
    """
    with open(fpath, encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=OrderedJSON)


def ojson_loads(s):
    """Read string as OrderedJSON.
    """
    return json.loads(s, object_pairs_hook=OrderedJSON)


def bucketize(things, key=None, *, buckets=None, ignores={None}):
    """Partition items into buckets.
    
    Basic call forms:
        - bucketize(keyval_pairs)
        - bucketize(values, keyfunction)
    
    Params:
        - things:
                Iterable of things to bucketize.
                
                If `key` is provided, `things` is an iterable of values.
                Otherwise, `things` is an iterable of `(key, value)` pairs.
        - key:
                A function to determine which bucket to put an item in.
        - buckets:
                The dict that will hold the objects.
                
                Pass in an OrderedDict to have ordered buckets, or some other kind of dict to have special processing. Otherwise, a new dict will be created.
        - ignores:
                Collection of keys to ignore. Default: Ignore `None` keys.
                
                Example: Pass in an empty collection to allow `None` keys.
    """
    if buckets is None:
        buckets = {}
    if key is not None:
        pairs = ((key(v), v) for v in things)
    else:
        pairs = things
    if ignores:
        pairs = (pair for pair in pairs if pair[0] not in ignores)
    for k, v in pairs:
        try:
            buckets[k].append(v)
        except KeyError:
            buckets[k] = [v]
    return buckets



def prints(itr, **kwargs):
    """Print items from an iterable, separated by newlines.
    """
    print(*itr, **kwargs, sep='\n')


def output_table(
        table,
        column_labels=None,
        row_labels=None,
        idnum=None,
        fpath='temp.out',
    ):
    """Output
    
    Params:
        idnum: int or None
            If provided, print the index of the row as the first column.
            Count will start at the provided int.
    
    
    # If I implement `flatten`ing, you could just pass in `table=map(enumerate, table)` instead of passing `idnum=0`.
    """
    with open(fpath, 'w', encoding='utf-8') as f:
        def print_row(*row):
            row = (
                s if not isinstance(s, str)
                else s.replace('\n', r'\n').replace('\t', r'\t')
                for s in row
            )
            print(*row, sep='\t', file=f)
        
        if column_labels is not None:
            assert row_labels is None, "Not implemented."
            if idnum is not None:
                print_row('id', *column_labels)
            else:
                print_row(*column_labels)
        if idnum is not None:
            for i, row in enumerate(table, idnum):
                print_row(i, *row)
        else:
            for row in table:
                print_row(*row)


def bitcount(n):
    """Number of bits in an int.
    """
    rv = 0
    while n:
        n = n & (n-1)
        rv += 1
    return rv


def binary(n, fill=16):
    """Binary representation of an int.
    """
    return bin(n)[2:].zfill(fill)


def warn_renamed(*names):
    """Decorator: Warn that the function has been renamed.
    
    Use as:
        @warn_renamed('oldname1', 'oldname2', ...)
        def newname(...):
            ...
    """
    def decorate(f):
        olds = {}
        name = f.__name__
        for name in names:
            @wraps(f)
            def renamed(*args, __name=name, **kwargs):
                warning.warn('%s has been renamed "%s".' % (__name, fname))
                return f(*args, **kwargs)
            renamed.__name__ = name
            olds[name] = renamed
        setpublic(inspect.getmodule(f), **olds)
        return f
    return decorate


def setpublic(module, **namedvalues):
    """Sets names in the module/*, and also adds them to __all__*/.
    """
    for name, value in namedvalues.items():
        setattr(module, name, value)


def usorted(iterable, **kwargs):
    """Unique and sorted.
    
    Items should be hashable and comparable.
    
    Kwargs are passed to `sorted`. The sort key should be compatible with object equality.
    """
    return sorted(set(iterable), **kwargs)


def usorted_eq(iterable, **kwargs):
    """Unique and sorted, for unhashable items.
    """
    return [group[0] for group in itertools.groupby(sorted(iterable, **kwargs))]


def uniques(iterable, *, key=None, last=True):
    """Returns an iterable of the unique items in the iterable, in order.
    
    Params:
        key - A function to determine uniqueness.
        last - Whether to take the first or last found.
                If False, give up first of each.
                Else, give up last.
                If not provided, it means you don't care. The default is subject to change.
                ! If key is not provided, this is ignored.
    """
    if key is None:
        return OrderedDict.from_keys(iterable).keys()
    if last:
        # return OrderedDict((key(item), item) for item in iterable).values()
        it0, it1 = tee(iterable, 2)
        return OrderedDict(zip(map(key, it0), it1)).values()
    return _first_uniques(iterable, key)


def _first_uniques(iterable, key):
    seen = set()
    for item in iterable:
        k = key(item)
        if k not in seen:
            yield item
            seen.add(k)



class _BagMeta(type):
    """
    Adds functionality to the Bag class that won't take up names in bag objects.
        This makes a bag more "pure": if I do something to a bag, I'm sure to get the splayed out thing.
    
    For example, I wanna be able to do:
            `Bag[i](mybag)`
        to get the i'th item.
    
    And:
        `Bag.map(mybag)(f)`
        ^? Better syntax for this?
            - `Bag.map(mybag, f)`
            - `Bag.map(f, mybag)`
        ^^? Do I even need it? `__iter__` is enough.
    """
    ...


class Bag(list, metaclass=_BagMeta):
    """Bag of things of a single type.
    
    Implements:
        self[i] => super[i]
        self[i, j] => super[i][j]
        
        self.attr => Bag(item[attr]s)
    
    
    """
    '''
      Decisions:
        - Maybe index should ONLY be to per-getitem.
            - And use some special non-method way to index.
                Like Bag[:](mybag)
        - 
    '''
    def __getitem__(self, args):
        """
        
        """
        if not isinstance(args, tuple):
            items = super().__getitem__(args)
            if isinstance(args, slice):
                return Bag(items)
            else:
                return items
        
        idx, i = args
        items = super().__getitem__(idx)
        if isinstance(idx, slice):
            return Bag(item[i] for item in items)
        else:
            return items[i]
        
        
    def __getattr__(self, attr):
        return Bag(getattr(item, attr) for item in self)

    def filter(self, fn):
        return Bag(filter(fn, self))

    def map(self, fn):
        return Bag(map(fn, self))

    def flatten(self):
        return Bag(y for x in self for y in x)
    
    def group(self, n):
        return Bag(zip(*[iter(self)]*n))


class Splitter:
    """
    Linesplitter.
    
    S is the basic one.
    
    Call S(options) for more.
    """
    '''
    Wanted features:
        - ignore comments
        - ignore commentlines
            (so don't 
        - specify comment marker
            - as str
            - as func
            ??- block comment pair??
            ?- multiple things?
    '''
    def __init__(self):
        #TODO
        pass
    
    def __lshift__(self, s):
        # Just implement basic functionality for now.
        lines = s.splitlines() # split
        lines = map(str.strip, lines) # strip lines
        lines = filter(bool, lines) #filter empty
        #` if self.ignore_comments:
        lines = filter(lambda s: not s.startswith('#'), lines)
            # ignore comments
        return list(lines)
    
    def __call__(self, **kwargs):
        #TODO
        return self


S = Splitter()



def register(d, name=None):
    """Decorator to register a decorated function into a given dict.
    
    Example:
        @register(funcs, 'not_six')
        def five():
            return 5
    """
    def registration(f):
        d[name or f.__name__] = f
        return f
    return register


def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False



def keys(container):
    try:
        return container.keys()
    except:
        return range(len(container))

def values(container):
    try:
        return container.values()
    except:
        return container

def items(container, start=0):
    try:
        items = container.items()
    except:
        return enumerate(container, start=start)
    else:
        if start != 0:
            raise ValueError
        return items


def takes(iterable, n):
    """Take n things at a time.
    """
    return zip(*[iter(iterable)]*n)


