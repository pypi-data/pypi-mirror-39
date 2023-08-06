madplot
=======

This project aims to facilitate working with MADX from within Python. It contains the following
major components:

* **MADX API**: Build, parse and run MADX scripts.
* **Plot API**: Plot MADX output in various formats.
* **Utilities**: For example convert MADX output tables to pandas data frames.


MADX API
--------

The MADX API consists of three parts: *building*, *parsing* and *running* MADX scripts.


Builder
```````

The builder API can be used for creating MADX scripts. The following example code shows the
various features.

.. code-block:: python

    from madplot.madx.builder import Script

    # At first generate a new script.
    s = Script()

    # Labeled or declaration statements can be created via `[]` access.
    # This produces the following statement in the resulting MADX script:
    # L = 5;
    # N = 10;
    s['L'] = 5
    s['N'] = 10

    # MADX commands can be created by accessing them through the script instance.
    # Output: `DP: SBEND, L = L/2, ANGLE = 2*PI/(2*N);`.
    s['DP'] = s.SBEND(L='L/2', ANGLE='2*PI/(2*N)')

    # Output: `QF: MULTIPOLE, KNL = {0, 1/f};`.
    s['QF'] = s.MULTIPOLE(KNL=[0, '1/f'])

    # Sequences can be generated using the `Sequence` class.
    from madplot.madx.builder import Sequence

    with Sequence(refer='entry', l='N*L') as seq:
        for n in range(s.N):  # Python loop over number of cells.
            # Unlabeled statements can be just added the script instance.
            # Stored element definitions can be reused via attribute access of the script instance.
            # This produces the following output: `QF, at = 0 * L;`.
            seq += s.QF(at=f'{n} * L')

            # [...] Add more elements.

    # Adding a sequence to the script will auto-expand it when dumping the script.
    # This produces the following output:
    # `LATTICE: sequence, refer = entry, l = N*L;`
    # `    QF, at = 0 * L;`
    # `    [...]`
    # `endsequence;`
    s['LATTICE'] = seq

    # A script can be dumped by converting to `str`.
    with open('example.seq', 'w') as f:
        f.write(str(s))

Complete code example
~~~~~~~~~~~~~~~~~~~~~

The following is a complete code example.

.. code-block:: python

    from madplot.madx.builder import Sequence, Script

    s = Script()

    s['N_cells'] = 60
    s['L_cell'] = 13.45
    s['f'] = 7.570366

    s['DP'] = s.SBEND(L='L_cell/2', ANGLE='2*PI / (2*N_cells)')
    s['QF'] = s.MULTIPOLE(KNL=['0', '1/f'])
    s['QD'] = s.MULTIPOLE(KNL=['0', '-1/f'])

    with Sequence(refer='entry', l='N_cells*L_cell') as seq:
        for n in range(s.N_cells):
            seq += s.QF(at=f'{n} * L_cell')
            seq += s.DP(at=f'{n} * L_cell')
            seq += s.QD(at=f'{n} * L_cell + 0.50 * L_cell')
            seq += s.DP(at=f'{n} * L_cell + 0.50 * L_cell')

    s['FODO_LATTICE'] = seq

    with open('example.seq', 'w') as f:
        f.write(str(s))

Advanced control
~~~~~~~~~~~~~~~~

The following operations allow for advanced control statements.

* Comments can be placed as strings: ``s += '// Comment'``.
* Re-evaluated (deferred) expressions (`:=`) can be created via the ``E`` class: ``from madplot.madx.builder import E; s += s.ealign(dx=E('ranf()'))``.
* Any MADX command can be accessed via the script instance: ``s += s.TWISS(file='optics')``.


Parser
``````

The ``parser.Parser`` class has two methods available:

* ``Parser.raw_parse``: This method parses the given script into its statements and returns a list thereof. The different statement types can be found in ``Parser._types``. The literal values of command attributes will be returned.
* ``Parser.parse``: Parses the script into its statements as well but only returns non-comment non-variable declaration statements and interpolates any command attribute values.

For example:

.. code-block:: python

    >>> madx = '''
    ...     L = 5;
    ...     QF: QUADRUPOLE, k1 := pi/5, l = L;
    ... '''
    >>> Parser.raw_parse(madx)
    [[Variable] L = 5, [Command] QF: QUADRUPOLE {'k1': 'pi/5', 'l': 'L'}]
    >>> Parser.parse(madx)
    [[Command] QF: QUADRUPOLE {'k1': 0.6283185307179586, 'l': 5}]


Engine
``````

The MADX Engine API can be used to run MADX scripts. The `MADXEngine` class expects a set of templates
which will be used to run the script. A template is a MADX script that contains unfilled parts which
can be interpolated later on. The first template is considered the entry point (the main script) and will be run.

The following code creates an engine:

.. code-block:: python

    from madplot.madx.engine import MADXEngine

    engine = MADXEngine(
        ['test.madx', 'test.seq'],  # Template files; `test.madx` is the main script.
        madx='/opt/madx',  # File path to the MADX executable; if not specifed the `MADX` environment variable will be considered.
        working_directory='/tmp/test'  # The directory in which the engine runs the scripts.
    )

The templates can contain substitutions following the Python string formatting rules.
For example: ``QF: QUADRUPOLE, KL={kl};``. The ``{kl}`` part can be interpolated when running the scripts.

The ``run`` method can be invoked to run a script. It expects a list of output file names (which need to be
generated by the template scripts). By default the file contents will be returned as ``pandas.DataFrame``
instances.

.. code-block:: python

    twiss, = engine.run(['example.twiss'])

Here the file ``example.twiss`` needs to be generated when running ``test.madx``.
In case one or more template scripts require interpolation the corresponding values can be specified
using the `configuration` keyword argument:

.. code-block:: python

    twiss, = engine.run(
        ['example.twiss'],
        configuration={'test.madx': {'kl': 0.01}}
    )

Special arguments for the output conversion can be specified per output in form of a ``dict``:

.. code-block:: python

    (twiss, meta), = engine.run([('example.twiss', {'return_meta': True}])

This will return meta data (prefixed with `@` in the TFS output) along the main data frame.


Plotting
--------

Various functions for plotting are available in the ``madplot.plot`` module. Please refer directly
to this module for further information.


Utilities
---------

Utilities for conversion of data formats are available at ``madplot.utils``:

* ``Convert.tfs``: Converts TFS file to pandas data frame,
* ``Convert.trackone``: Converts trackone table (as outputted by ``TRACK, onetable = true``) to pandas data frame.
