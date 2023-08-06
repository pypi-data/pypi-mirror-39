#!/usr/bin/env python
#
# importing.py - The data import stage
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides the :func:`importData` function, which implements
the data importing stage of the ``ukbparse`` sequence
"""


import os.path               as op
import itertools             as it
import functools             as ft
import multiprocessing.dummy as mpd
import                          logging
import                          warnings
import                          collections

import              six
import pandas    as pd
import numpy     as np

from . import       util
from . import       custom
from . import       storage
from . import       merging
from . import       fileinfo
from . import       datatable
from . import       loadtables
from . import       expression


log = logging.getLogger(__name__)


NUM_ROWS = 10000
"""Default number of rows read at a time by :func:`loadData` - it reads the
data in chunks.
"""


MERGE_AXIS = 'variables'
"""Default merge axis when loading multiple data files - see :func:`mergeData`.
"""


MERGE_STRATEGY = 'intersection'
"""Default merge strategy when loading multiple data files - see
:func:`mergeData`.
"""

MERGE_AXIS_OPTIONS = ['0', 'rows', 'subjects',
                      '1', 'cols', 'columns', 'variables']
"""Values accepted for the ``axis`` option to the :func:`mergeData` function.
"""


MERGE_STRATEGY_OPTIONS = ['naive', 'union', 'intersection', 'inner', 'outer']
"""Values accepted for the ``strategy`` option to the :func:`mergeData`
function.
"""


def importData(datafiles,
               vartable,
               proctable,
               cattable,
               variables=None,
               categories=None,
               subjects=None,
               encoding=None,
               unknownVars=None,
               removeUnknown=True,
               mergeAxis=None,
               mergeStrategy=None,
               loaders=None,
               lowMemory=False,
               workDir=None,
               pool=None,
               mgr=None,
               dryrun=False):
    """The data import stage.

    This function does the following:

      1. Figures out which columns to load (using the :func:`columnsToLoad`
         function).

      2. Loads the data (using :func:`loadData`),

      3. Creates and returns a :class:`DataTable`.

    :arg datafiles:         Path to the data file(s)

    :arg vartable:          The data coding table

    :arg proctable:         The processing table

    :arg cattable:          The category table

    :arg variables:         List of variable IDs to import

    :arg categories:        List of category names to import

    :arg subjects:          List of subjects to include.

    :arg encoding:          Character encoding(s) for data file(s). See
                            :func:`loadData`.

    :arg unknownVars:       List of :class:`.Column` objects representing
                            unknown variables

    :arg removeUnknown:     If ``True`` (the default), any variables in
                            ``datafile`` which are not in ``varfile`` are not
                            loaded. Ignored if ``variables``or ``categories``
                            are provided.

    :arg mergeAxis:         Merging axis to use when loading multiple data
                            files - see the :func:`mergeData` function.

    :arg mergeStrategy:     Merging strategy to use when loading multiple
                            data files - see the :func:`mergeData` function.

    :arg loaders:           Dict of ``{ file : loaderName }`` mappings
                            containing custom sniffers/loaders to be used for
                            specific files. See the :mod:`.custom` module.

    :arg lowMemory:         Store intermediate results on disk to save RAM
                            (see :mod:`.storage`).

    :arg workDir:           Directory to store intermediate files (see
                            :mod:`.storage`). Only relevant when
                            ``lowMemory is True``

    :arg pool:              ``multiprocessing.Pool`` to use for parallelising
                            tasks. Only relevant when ``lowMemory is True``.

    :arg mgr:               ``multiprocessing.Manager`` to use for sharing
                            state. Only relevant when ``lowMemory is True``.

    :arg dryrun:            If ``True`` the data is not loaded.

    :returns:               A tuple containing:

                             - A :class:`DataTable`, which contains references
                               to the data, and the variable and procesing
                               tables.

                             - A list of :class:`.Column` objects that were not
                               loaded from each input file.
    """

    if not lowMemory:
        pool = None
        mgr  = None

    if unknownVars is None:
        unknownVars = []

    if loaders is None:
        loaders = {}

    variables = restrictVariables(cattable, variables, categories)

    # Figure out which columns to load
    cols, drop = columnsToLoad(datafiles,
                               vartable,
                               variables,
                               unknownVars,
                               removeUnknown,
                               loaders)

    # Load those columns, merging
    # multiple input files.
    data, cols = loadData(datafiles,
                          vartable,
                          cols,
                          subjects=subjects,
                          encoding=encoding,
                          mergeAxis=mergeAxis,
                          mergeStrategy=mergeStrategy,
                          loaders=loaders,
                          lowMemory=lowMemory,
                          workDir=workDir,
                          pool=pool,
                          mgr=mgr,
                          dryrun=dryrun)

    # Re-order the columns according to
    # specified variables, if provided
    if variables is not None:

        # organise columns by vid
        newcols = collections.defaultdict(list)
        for c in cols[1:]:
            newcols[c.vid].append(c)

        # order them by the variable list
        cols = list(it.chain([cols[0]], *[newcols[v] for v in variables]))

        if not dryrun:
            data = data[[c.name for c in cols[1:]]]

    dtable = datatable.DataTable(
        data, cols, vartable, proctable, cattable, pool)

    return dtable, drop


def removeSubjects(dtable, exclude=None, exprs=None):
    """Remove subjects (rows) from the data according to the ``exprs`` and
    ``exclude`` parameters.

    :arg dtable:   A :class:`DataTable` instance.

    :arg exprs:    List of strings containing expressions which identify
                   subjects to be included. Subjects for which *any*
                   expression evaluates to ``True`` will be included.
                   Overridden by ``exclude``.

    :arg exclude:  List of subject IDs to exclude. Overrides ``exprs``.
    """

    # We iteratively build up a binary
    # mask which contains ones for
    # subjects that are to be retained
    orignrows = len(dtable)

    # If subject include expressions are
    # provided, flag subjects accordingly
    if exprs is None: mask = np.ones( orignrows, dtype=np.bool)
    else:             mask = np.zeros(orignrows, dtype=np.bool)

    if exprs is not None:
        # Parse the expressions, and get a
        # list of all variables that are
        # mentioned in them.
        exprs = list(it.chain(*[e.split(',')    for e in exprs]))
        exprs = [expression.Expression(e)       for e in exprs]
        vids  = list(set(it.chain(*[e.variables for e in exprs])))

        # Build a list of the visits and
        # instances in the data for each
        # variable used in the expression.
        try:
            visits    = [dtable.visits(   v) for v in vids]
            instances = [dtable.instances(v) for v in vids]
        except KeyError as e:
            raise RuntimeError('Unknown variable used in exclude expression: '
                               '{}'.format(exprs))

        # Calculate the intersection of visits/
        # instances across all variables - we
        # evaluate expressions for each visit/
        # instance, and only where a visit/
        # instance is present for all variables.
        def intersection(a, b):
            return set(a).intersection(b)

        if len(visits)    > 0: visits    = ft.reduce(intersection, visits)
        if len(instances) > 0: instances = ft.reduce(intersection, instances)

        # A subject will be retained if *any*
        # expression for *any* visit/instance
        # evaluates to true.
        exprmasks = []

        for visit, instance in it.product(visits, instances):

            # build a dict of { vid : column } mappings
            # for each variable used in the expression
            cols = [dtable.columns(v, visit, instance)[0] for v in vids]
            cols = {v : c.name for v, c in zip(vids, cols)}

            with dtable.pool() as pool:
                for e in exprs:
                    exprmasks.append(pool.apply_async(
                        e.evaluate, (dtable, cols, )))

        # wait for each expression to complete,
        # then combine them using logical OR.
        exprmasks = [e.get() for e in exprmasks]
        mask      = ft.reduce(lambda a, b: a | b, exprmasks, mask)
        mask      = np.array(mask)

    # Flag subjects to drop
    if exclude is not None:
        exclude       = dtable.index.isin([int(s) for s in exclude])
        mask[exclude] = 0

    # drop the subjects
    if any((exclude  is not None,
            exprs    is not None)):
        log.debug('Dropping %i / %i rows', sum(~mask), orignrows)
        dtable.maskSubjects(mask)


def restrictVariables(cattable, variables, categories):
    """Determines which variables should be loaded (and the order
    they should appear in the output) from the given sequences of
    ``variables`` and ``categories``.

    If neither ``variables`` nor ``categories`` are provided, ``None`` is
    returned, indicating that all variables should be loaded.

    :arg cattable:   The category table
    :arg variables:  List of variable IDs to import. May be ``None``.
    :arg categories: List of category names to import. May be ``None``.
    :returns:        Sequence of variables to load, or ``None`` if all
                     variables should be loaded.
    """

    # Build a list of all the variables we
    # want to load, from the variables and
    # categories that were passed in.
    if categories is not None:

        if variables is None:
            variables = []

        catvars   = loadtables.categoryVariables(cattable, categories)
        variables = variables + [c for c in catvars if c not in variables]

    return variables


def columnsToLoad(datafiles,
                  vartable,
                  variables,
                  unknownVars,
                  removeUnknown,
                  sniffers=None):
    """Determines which columns should be loaded from ``datafiles``.

    Peeks at the first line of the data file (assumed to contain column names),
    then uses the variable table to determine which of them should be loaded.

    :arg datafiles:     Path to data file(s)

    :arg vartable:      Variable table

    :arg variables:     List of variables to load. If provided,
                        ``removeUnknown`` is ignored.

    :arg unknownVars:   List of :class:`.Column` objects representing unknown
                        variables

    :arg removeUnknown: If ``True``, any variables in ``datafile`` which are
                        not in ``vartable`` are not loaded.

    :arg sniffers:      Dict of ``{ file : snifferName }`` mappings containing
                        custom sniffers to be used for specific files. See the
                        :mod:`.custom` module.

    :returns:           A tuple containing:

                         - A dict of ``{ file : [Column] }`` mappings, the
                          :class:`.Column` objects to *load* from each input
                          file.

                         - A list containing the :class:`.Column` objects to
                          *ignore*.
    """

    if sniffers is None:
        sniffers = {}

    if variables is not None:
        removeUnknown = False

    unknownVids = list(sorted(set([c.vid for c in unknownVars])))

    if isinstance(datafiles, six.string_types):
        datafiles = [datafiles]

    # We apply these cleaning steps by
    # omitting the relevant columns.
    loadFuncNames = ['remove', 'keepVisits']

    # Peek at the columns that are
    # in the input files. Save a ref
    # to the first column (assumed
    # to be the ID column)
    allcols = fileinfo.fileinfo(tuple(datafiles), tuple(sniffers.items()))[2]
    hdrcols = [c[0] for c in allcols]
    allcols = list(it.chain(*[c[1:] for c in allcols]))

    # re-organise them - a list of
    # columns for each variable ID
    byvid = collections.defaultdict(list)
    for col in allcols:
        byvid[col.vid].append(col)

    # retrieve all cleaning steps -
    # we are only going to apply the
    # cleaning steps that will
    # determine whether or not a column
    # should be loaded
    mask    = vartable['Clean'].notna()
    cleans  = vartable['Clean'][mask]
    ppvids  = vartable.index[   mask]

    # Loop through all columns in
    # the data, and build a list of
    # the ones we want to load. The
    # end result will be organised
    # by the data files. We load
    # the ID column for every file.
    drop = []
    load = collections.OrderedDict(
        [(f, [hc]) for f, hc in zip(datafiles, hdrcols)])
    for vid, cols in byvid.items():

        # variable list provided, but this
        # variable is not in it - don't load.
        if variables is not None and vid not in variables:
            drop.extend(cols)
            continue

        # column is flagged as unknown,
        # and we have been told to
        # ignore unknown columns
        if removeUnknown and vid in unknownVids:
            drop.extend(cols)
            continue

        # cleaning specified for this variable
        if vid in ppvids:

            # retrieve the cleaning functions
            # which affect whether or not a column
            # should get loaded. We remove these
            # functions from the variable table, as
            # they won't need to be called again.
            funcs = [cleans[vid].pop(n, None) for n in loadFuncNames]
            funcs = [f for f in funcs if f is not None]

            # call the functions, generate a new
            # set of columns for this variable
            newcols = cols
            for f in funcs:
                newcols = f.run(vid, newcols)

            drop.extend(list(set.difference(set(cols), set(newcols))))

            cols = newcols

        for col in cols:
            load[col.datafile].append(col)

    log.debug('Identified %i / %i columns to be loaded',
              sum([len(c) for c in load.values()]),
              len(allcols) + len(datafiles))

    return load, drop


def loadData(datafiles,
             vartable,
             columns,
             nrows=None,
             subjects=None,
             encoding=None,
             mergeAxis=None,
             mergeStrategy=None,
             loaders=None,
             lowMemory=False,
             workDir=None,
             pool=None,
             mgr=None,
             dryrun=False):
    """Load data from ``datafiles``, using :func:`mergeData` if multiple files
    are provided.

    :arg datafiles:     Path to the data file(s)

    :arg vartable:      Variable table

    :arg columns:       Dict of ``{ file : [Column] }`` mappings,
                        defining the columns to load (as returned by
                        :func:`columnsToLoad`).

    :arg nrows:         Number of rows to read at a time. Defaults to
                       :attr:`NUM_ROWS`.

    :arg subjects:      List of subjects to include.

    :arg encoding:      Character encoding (or sequence of encodings, one
                        for each data file). Defaults to ``latin1``.

    :arg mergeAxis:     Merging axis to use when loading multiple data files -
                        see the :func:`mergeData` function. Defaults to
                        :attr:`MERGE_AXIS`.

    :arg mergeStrategy: Strategy for merging multiple data files - see the
                        :func:`mergeData` function. Defaults to
                        :attr:`MERGE_STRATEGY`.

    :arg loaders:       Dict of ``{ file : loaderName }`` mappings containing
                        custom loaders/sniffers to be used for specific files.
                        See the :mod:`.custom` module.

    :arg lowMemory:     Store intermediate results on disk to save RAM (see
                        :mod:`.storage`).

    :arg workDir:       Directory to store intermediate files (see
                        :mod:`.storage`). Only relevant when
                        ``lowMemory is True``

    :arg pool:          ``multiprocessing.Pool`` object for running tasks in
                        parallel. Only relevant when ``lowMemory is True``.

    :arg mgr:           ``multiprocessing.Manager`` to use for sharing state.
                        Only relevant when ``lowMemory is True``.

    :arg dryrun:        If ``True``, the data is not loaded.

    :returns:           A tuple containing:

                         - A ``pandas.DataFrame``, or a
                           :class:`.HDFStoreCollection`, containing the data,
                           or ``None`` if ``dryrun is True``.
                         - A list of :class:`.Column` objects representing the
                           columns that were loaded.
    """

    if mergeStrategy is None: mergeStrategy = MERGE_STRATEGY
    if mergeAxis     is None: mergeAxis     = MERGE_AXIS
    if loaders       is None: loaders       = {}

    if isinstance(datafiles, six.string_types):
        datafiles = [datafiles]
    if encoding is None or isinstance(encoding, six.string_types):
        encoding = [encoding] * len(datafiles)

    if lowMemory and len(datafiles) != 1:
        raise NotImplementedError('Low memory merging not yet implemented')

    # Get the format for each input file
    dialects, headers, names = fileinfo.fileinfo(
        tuple(datafiles), tuple(loaders.items()))

    # load the data
    data       = []
    loadedcols = []
    for fname, fencoding, dialect, header, allcols in zip(
            datafiles, encoding, dialects, headers, names):

        toload = columns[fname]
        loader = loaders.get(op.basename(fname), None)

        if dryrun:
            fdata = None

        elif loader is not None:
            log.debug('Loading %s with custom loader %s', fname, loader)
            fdata = custom.runLoader(loader, fname)

        else:
            log.debug('Loading %s with pandas', fname)
            fdata = loadFile(fname,
                             vartable,
                             header,
                             dialect,
                             allcols,
                             toload,
                             nrows=nrows,
                             subjects=subjects,
                             encoding=fencoding,
                             lowMemory=lowMemory,
                             workDir=workDir,
                             pool=pool,
                             mgr=mgr)

        data      .append(fdata)
        loadedcols.append(toload)

    # Merge data from multiple files
    # into a single dataframe

    # TODO merge HDFStores
    if lowMemory:
        data = data[0]
        cols = loadedcols[0]
    else:
        data, cols = merging.mergeDataFrames(
            data, loadedcols, mergeAxis, mergeStrategy, dryrun)

    # if a subject list was provided,
    # re-order the data according to
    # that list
    if (not dryrun) and subjects is not None:
        data = data.loc[subjects, :]

    return data, cols


def loadFile(fname,
             vartable,
             header,
             dialect,
             allcols,
             toload,
             nrows=None,
             subjects=None,
             encoding=None,
             lowMemory=False,
             workDir=None,
             pool=None,
             mgr=None):
    """Loads data from the specified file.

    :arg fname:     Path to the data file

    :arg vartable:  Variable table

    :arg header:    ``True`` if the file has a header row, ``False`` otherwise.

    :arg dialect:   File dialect (see :func:`.fileinfo`).

    :arg allcols:   Sequence of :class:`.Column` objects describing all columns
                    in the file.

    :arg toload:    Sequence of :class:`.Column` objects describing the columns
                    that should be loaded.

    :arg nrows:     Number of rows to read at a time. Defaults to
                    attr:`NUM_ROWS`.

    :arg subjects:  List of subjects to include.

    :arg encoding:  Character encoding (or sequence of encodings, one
                    for each data file). Defaults to ``latin1``.

    :arg lowMemory: Store intermediate results on disk to save RAM (see
                    :mod:`.storage`).

    :arg workDir:   Directory to store intermediate files (see
                    :mod:`.storage`). Only relevant when
                    ``lowMemory is True``

    :arg pool:      ``multiprocessing.Pool`` object for running tasks in
                    parallel. Only relevant when ``lowMemory is True``.

    :arg mgr:       ``multiprocessing.Manager`` to use for sharing state.
                    Only relevant when ``lowMemory is True``.

    :returns:       A ``pandas.DataFrame``, or a
                    :class:`.HDFStoreCollection`, containing the data.
    """


    ownPool = pool is None

    if encoding is None: encoding = 'latin1'
    if nrows    is None: nrows    = NUM_ROWS
    if pool     is None: pool     = mpd.Pool(1)

    # Build a list of the names of
    # columns that pandas should load
    name        = op.basename(fname)
    allcolnames = [c.name for c in allcols]
    toloadnames = [c.name for c in toload]

    def shouldLoad(c):
        return c in toloadnames

    # Figure out suitable data types to
    # store the data for each column.
    # Only date/time columns are converted
    # during load - this is done for us
    # by Pandas. We performs numeric
    # conversion after load, via the
    # coerceToNumeric function.
    vttypes, dtypes = loadtables.columnTypes(vartable, toload)
    datecols        = [c.name for c, t in zip(toload, vttypes)
                       if t in (util.CTYPES.date, util.CTYPES.time)]

    # input may or may not
    # have a header row
    if header: header = 0
    else:      header = None

    log.debug('Loading %u columns from %s: %s ...',
              len(toload), fname, toloadnames[:5])

    if dialect == 'whitespace': dlargs = {'delim_whitespace' : True}
    else:                       dlargs = {'dialect'          : dialect}

    if lowMemory:
        fdata = storage.HDFStoreCollection(prefix=name,
                                           workDir=workDir,
                                           mgr=mgr)
    else:
        fdata = []

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', module='pandas.io.parsers')
        warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)
        dfiter = pd.read_csv(fname,
                             header=header,
                             names=allcolnames,
                             index_col=0,
                             usecols=shouldLoad,
                             parse_dates=datecols,
                             infer_datetime_format=True,
                             iterator=True,
                             chunksize=nrows,
                             encoding=encoding,
                             **dlargs)

        for i, df in enumerate(dfiter):

            nrows = len(df)

            # If a subject list is provided,
            # drop subjects not in the list
            if subjects is not None:
                mask = df.index.isin(subjects)
                df   = df.drop(df.index[~mask])

            log.debug('Processing chunk %i (kept %i / %i rows)',
                      i + 1, len(df), nrows)

            # pd.read_csv will raise an error if
            # a column that is specified as
            # numeric contains non-numeric data.
            # So we coerce data types after the
            # data has been loaded. This causes
            # non-numeric data to be set to nan.
            cfunc  = ft.partial(coerceToNumeric, vartable)
            series = [df[c.name] for c in toload[1:]]
            series = pool.starmap(cfunc, zip(series, toload[1:]))

            for col, s in zip(toload[1:], series):
                df.loc[:, col.name] = s

            fdata.append(df)

    if ownPool:
        pool.close()
        pool.join()

    if not lowMemory:
        fdata = pd.concat(fdata, axis=0)

    log.debug('Loaded %i rows from %s', len(fdata), fname)

    return fdata


def coerceToNumeric(vartable, series, column):
    """Coerces the given column to numeric, if necessary.

    :arg vartable: The variable table

    :arg series:   ``pandas.Series`` containing the data to be coerced.

    :arg column:   :class:`.Column` object representing the column to coerce.

    :returns:      Coerced ``pandas.Series``
    """

    name          = column.name
    vttype, dtype = loadtables.columnTypes(vartable, [column])
    vttype        = vttype[0]
    has_dtype     = series.dtype
    exp_dtype     = dtype.get(name, None)

    if vttype in (util.CTYPES.continuous,
                  util.CTYPES.integer,
                  util.CTYPES.categorical_single,
                  util.CTYPES.categorical_multiple) and \
       has_dtype != exp_dtype:

        # We can't force a specific numpy
        # dtype *and* coerce bad values to
        # nan. So all columns will end up
        # as float32.
        return pd.to_numeric(series, errors='coerce', downcast='float')

    return series
