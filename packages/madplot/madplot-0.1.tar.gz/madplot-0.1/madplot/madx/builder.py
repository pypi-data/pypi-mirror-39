from collections import OrderedDict
from functools import partial


def __getattr__(name):
    return partial(Command, name)


class E(str):
    """Re-evaluated expression.
    
    Wraps the expression as a string. Use via `E('expression')`.
    """


class Command:
    """Base class representing a MADX element (in fact, this can be any MADX command)."""

    def __init__(self, keyword, **attributes):
        super().__init__()
        self.keyword = keyword
        self.attributes = attributes

    def __getitem__(self, key):
        return self.attributes[key]

    def __str__(self):
        if not self.attributes:
            return f'{self.keyword};'
        keys, values = zip(*self.attributes.items())
        ops = [':=' if isinstance(x, E) else '=' for x in values]
        values = map(
            lambda x: (
                '{' + ', '.join(str(xx) for xx in x) + '}' if isinstance(x, (list, tuple))
                else str(x)
            ),
            values
        )
        return f'{self.keyword}, {", ".join(map(" ".join, zip(keys, ops, values)))};'


class DerivedCommand(Command):
    """Class for elements that depend on previous definitions
    
    Derived elements retain the attribute specifications from their templates (parents).
    """

    def __init__(self, base, name, **attributes):
        super().__init__(name, **attributes)
        self.base = base

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return self.base[key]


class Script:
    """Main class for building MADX scripts.
    
    * Labeled statements can be placed via `script['label'] = ...`,
    * Unlabeled statements can be placed via `script += ...` or `script._ = ...` or `script['_'] = ...`,
    * Any MADX command can be accessed via `script.COMMAND`,
    * Command arguments can be specified via `script.COMMAND(key=value)`,
    * Re-evaluated expressions can be placed via `E('...')`,
    * Comments can be placed via `scipt += '// Comment'`,
    * The script's content can be dumped via `str(script)`.
    
    Example
    -------
    
    ```python
    script = Script()
    script['L'] = 5
    script['DP'] = script.SBEND(l='L', angle='2*PI / 10')
    script += script.DP()
    script += script.TWISS(file='optics')
    script += script.EALIGN(dx=E('0.001 * (2*RANF() - 1)'))
    script += '// Example comment'
    with open('example.madx', 'w') as f:
        f.write(str(script))
    ```
    """

    def __init__(self):
        super().__init__()
        self.elements = []
        self.definitions = OrderedDict()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            return partial(Command, name)

    def __setattr__(self, key, value):
        if key == '_':
            self.__setitem__(key, value)
        else:
            super().__setattr__(key, value)

    def __getitem__(self, key):
        element = self.definitions[key]
        if isinstance(element, Command):
            return partial(DerivedCommand, element, key)
        return element

    def __setitem__(self, key, value):
        if key != '_':
            self.definitions[key] = value
        self.elements.append((key if key != '_' else None, value))

    def __iadd__(self, other):
        self.__setitem__('_', other)
        return self

    def __str__(self):
        return '\n'.join(map(self._format_element, self.elements))

    @staticmethod
    def _format_element(element):
        if element[0] is None:
            return str(element[1])
        elif isinstance(element[1], Command):
            return f'{element[0]}: {str(element[1])}'
        else:
            return '{} = {};'.format(*element)


class Block(Command, Script):
    """Represents a block element.
    
    * Blocks can be used as context managers,
    * Blocks work like scripts (i.e. all the `Script` rules apply),
    * Blocks can be added to scripts and will be auto-expanded when the script is dumped.
    """

    def __init__(self, **kwargs):
        super().__init__(self.__class__.__name__.lower(), **kwargs)
        # Any attributes added in `__init__` ended up in `self.elements` due to `__setattr__`.
        self.elements[:] = []

    def __str__(self):
        header = Command.__str__(self)
        body = '\n'.join(map('    {}'.format, Script.__str__(self).split('\n')))
        footer = f'end{self.__class__.__name__.lower()};'
        return '\n'.join([header, body, footer])


class Sequence(Block):
    """Main class for building sequences.

    * Sequences can be used as context managers,
    * Sequences work like scripts (i.e. all the `Script` rules apply),
    * Sequences can be added to scripts and will be auto-expanded when the script is dumped.

    Example
    -------

    ```python
    script = Script()

    with Sequence(refer='entry', l='length') as seq:
        seq += script.SBEND(l=..., angle=...)
        ...

    script['LATTICE'] = seq
    ```
    """
    pass


class Track(Block):
    """Main class for creating tracking runs.

    * Tracking blocks can be used as context managers,
    * Tracking blocks work like scripts (i.e. all the `Script` rules apply),
    * Tracking blocks can be added to scripts and will be auto-expanded when the script is dumped.

    Example
    -------

    ```python
    script = Script()

    with Track() as tracking:
        tracking += tracking.start(x=..., px=...)
        tracking += tracking.run(turns=...)
        ...
        
    script += tracking
    ```
    """
    pass
