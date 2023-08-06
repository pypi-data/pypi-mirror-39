#!/usr/bin/env python
#
# loadtables.py - Functions which load the variable, data coding, processing,
#                 and category tables used by ukbparse.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides functions and logic to load the variable, data coding,
processing, and category tables used by ukbparse:


.. autosummary::
   :nosignatures:

   loadTables
   loadDefaultTables
   loadVariableTable
   addNewVariable
   loadProcessingTable
   loadCategoryTable
   categoryVariables
   columnTypes
"""


import itertools as it
import              re
import              logging
import              warnings
import              functools
import              collections

import numpy  as np
import pandas as pd

from . import util
from . import fileinfo
from . import processing
from . import expression


log = logging.getLogger(__name__)


def convert_type(val):
    """Convert a string containing a type into a numerical identifier for that
    type.
    """
    valmap = {
        'sequence' :
        util.CTYPES.sequence,
        'integer' :
        util.CTYPES.integer,
        'continuous' :
        util.CTYPES.continuous,
        'categorical (single)' :
        util.CTYPES.categorical_single,
        'categorical (single non-numeric)' :
        util.CTYPES.categorical_single_non_numeric,
        'categorical (multiple)' :
        util.CTYPES.categorical_multiple,
        'categorical (multiple non-numeric)' :
        util.CTYPES.categorical_multiple_non_numeric,
        'time' : util.CTYPES.time,
        'date' :
        util.CTYPES.date,
        'text' :
        util.CTYPES.text,
        'compound' :
        util.CTYPES.compound,
        'unknown' :
        util.CTYPES.unknown,
    }
    return valmap.get(val.lower(), util.CTYPES.unknown)


def convert_comma_sep_text(val):
    """Convert a string containing comma-separated text into a list. """
    if val.strip() == '':
        return np.nan
    words = val.split(',')
    return [w.strip() for w in words]


def convert_comma_sep_numbers(val):
    """Convert a string containing comma-separated numbers into a ``numpy``
    array.
    """
    if val.strip() == '':
        return np.nan
    return np.fromstring(val, sep=',', dtype=np.float)


def convert_ParentValues(val):
    """Convert a string containing a sequence of comma-separated
    ``ParentValue`` expressions into a sequence of :class:`.Expression`
    objects.
    """
    if val.strip() == '':
        return np.nan
    return [expression.Expression(e) for e in val.split(',')]


def convert_Process_Variable(val):
    """Convert a string containing a process variable specification - one of:

      - ``'all'``, indicating that the process is to be applied to all
        variables simultaneously

      - ``'all_independent'``,, indicating that the process is to be applied
        to all variables independently

      - One or more comma-separated MATLAB-style ``start:stop:step`` ranges.
    """
    if val in ('all', 'all_independent'):
        return val
    else:
        tokens = convert_comma_sep_text(val)
        return list(it.chain(*[util.parseMatlabRange(t) for t in tokens]))


def convert_Process(ptype, val):
    """Convert a string containing a sequence of comma-separated ``Process`` or
    ``Clean`` expressions into an ``OrderedDict`` of :class:`.Process`
    objects (with the process names used as dictionary keys).
    """
    if val.strip() == '':
        return np.nan

    procs = processing.parseProcesses(val, ptype)

    return collections.OrderedDict([(p.name, p)  for p in procs])


def convert_category_variables(val):
    """Convert a string containing a sequence of comma-separated variable IDs
    or ranges into a list of variable IDs. Variables may be specified as
    integer IDs, or via a MATLAB-style ``start:step:stop`` range. See
    :func:`.util.parseMatlabRange`.
    """

    ranges    = convert_comma_sep_text(val)
    variables = list(it.chain(*[util.parseMatlabRange(r) for r in ranges]))

    return variables


VARTABLE_DTYPES = {
    'ID'          : np.uint32,
    'Description' : str,

    # We can't use an integer for the data
    # coding, because not all variables
    # have a data coding, and pandas uses
    # np.nan to represent missing data.
    'DataCoding'  : np.float32,
}
"""Types to use for some columns in the variable table. """


VARTABLE_CONVERTERS = {
    'Type'         : convert_type,
    'NAValues'     : convert_comma_sep_numbers,
    'RawLevels'    : convert_comma_sep_numbers,
    'NewLevels'    : convert_comma_sep_numbers,
    'ParentValues' : convert_ParentValues,
    'ChildValues'  : convert_comma_sep_numbers,
    'Clean'        : functools.partial(convert_Process, 'cleaner'),
}
"""Custom converter functinos to use for some columns in the variable
table.
"""


DCTABLE_DTYPES = {
    'ID' : np.uint32,
}
"""Types to use for some columns in the data coding table. """


DCTABLE_CONVERTERS = {
    'NAValues'  : convert_comma_sep_numbers,
    'RawLevels' : convert_comma_sep_numbers,
    'NewLevels' : convert_comma_sep_numbers,
}
"""Custom converter functinos to use for some columns in the data coding
table.
"""


TYPETABLE_DTYPES = {
}
"""Types to use for some columns in the types table. """


TYPETABLE_CONVERTERS = {
    'Type'  : convert_type,
    'Clean' : functools.partial(convert_Process, 'cleaner'),
}
"""Custom converter functinos to use for some columns in the type trable. """



PROCTABLE_CONVERTERS = {
    'Variable' : convert_Process_Variable,
    'Process'  : functools.partial(convert_Process, 'processor'),
}
"""Custom converter functinos to use for some columns in the processing
table.
"""


CATTABLE_DTYPES = {
    'ID' : np.int32,
}
"""Types to use for some columns in the category table. """


CATTABLE_CONVERTERS = {
    'Variables' : convert_category_variables
}
"""Custom converter functinos to use for some columns in the category
table.
"""

UNKNOWN_CATEGORY_ID = -1
"""Category table ID to use for the automatically added unknown variable
category.
"""



def loadTables(datafiles,
               varfile,
               dcfile,
               typefile,
               procfile,
               catfile,
               **kw):
    """Loads the data tables used to run ``ukbparse``.

    :arg datafiles: Path(s) to the data files
    :arg varfile:   Path to the variable table file
    :arg dcfile:    Path to the data coding table file
    :arg typefile:  Path to the type table file
    :arg procfile:  Path to the processing table file
    :arg catfile:   Path to the category table file

    All other arguments are passed throughh to the :func:`loadVariableTable`
    and :func:`loadProcessingTable` functions.

    :returns:      A tuple containing:
                    - The variable table
                    - The processing table
                    - The category table
                    - List of integer variable IDs which are present in the
                      data, but were not present in the variable table.
    """

    vartable, uvs = loadVariableTable(datafiles,
                                      varfile,
                                      dcfile,
                                      typefile,
                                      **kw)
    proctable     = loadProcessingTable(procfile, **kw)
    cattable      = loadCategoryTable(catfile, uvs)

    return vartable, proctable, cattable, uvs


def loadDefaultTables(datafiles, **kw):
    """Convenience variant of :func:`loadTables` which uses the default
    table files.
    """

    from . import config
    return loadTables(datafiles,
                      config.DEFAULT_VFILE,
                      config.DEFAULT_DFILE,
                      config.DEFAULT_TFILE,
                      config.DEFAULT_PFILE,
                      config.DEFAULT_CFILE,
                      **kw)


def loadVariableTable(datafiles,
                      varfile,
                      dcfile,
                      typefile,
                      clean=None,
                      typeClean=None,
                      globalClean=None,
                      sniffers=None,
                      dropAbsent=True,
                      **kwargs):
    """Given variable table and datacoding table file names, builds and returns
    the variable table.


    TODO describe how dcfile/typefile are merged.

    :arg datafiles:   Path(s) to the data files

    :arg varfile:     Path to the variable file

    :arg dcfile:      Path to the data coding file

    :arg typefile:    Path to the type file

    :arg clean:       Dictionary of ``{vid : expr}`` mappings containing
                      cleaning functions to apply - this will override
                      any cleaning specified in the variable file, and
                      any cleaning specified in ``typeClean``.

    :arg typeClean:   Dictionary of ``{type : expr}`` mappings containing
                      cleaning functions to apply to all variables of a
                      specific type - this will override any cleaning
                      specified in the type file.

    :arg globalClean: Expression containing cleaning functions to
                      apply to every variable - this will be performed after
                      variable-specific cleaning in the variable table,
                      or specified via ``clean`` or ``typeClean``.

    :arg sniffers:    Dict of ``{ file : snifferName }`` mappings containing
                      custom sniffers to be used for specific files. See the
                      :mod:`.custom` module.

    :arg dropAbsent:  If ``True`` (the default), remove all variables from the
                      variable table which are not present in the data
                      file(s).

    All other keyword arguments are ignored.

    :returns: A tuple containing:

                - A ``pandas.DataFrame`` containing the variable table

                - A sequence of :class:`.Column` objects representing variables
                  which were present in the data files, but not in the variable
                  table, but were added to the variable table.
    """

    if sniffers is None:
        sniffers = {}

    log.debug('Loading variable table from %s', varfile)
    vartable = pd.read_csv(varfile, '\t',
                           index_col=0,
                           dtype=VARTABLE_DTYPES,
                           converters=VARTABLE_CONVERTERS)

    log.debug('Loading data coding table from %s', dcfile)
    dctable  = pd.read_csv(dcfile, '\t',
                           index_col=0,
                           dtype=DCTABLE_DTYPES,
                           converters=DCTABLE_CONVERTERS)

    log.debug('Loading type table from %s', typefile)
    tytable  = pd.read_csv(typefile, '\t',
                           index_col=0,
                           converters=TYPETABLE_CONVERTERS)

    # All column names and variable
    # IDs in the input data files,
    # with the first column from each
    # file dropped (as it is assumed
    # to be an index).
    finfo = fileinfo.fileinfo(tuple(datafiles), tuple(sniffers.items()))
    cols  = [c[1:] for c in finfo[2]]
    cols  = list(it.chain(*cols))

    unknownVars = []

    # Make sure a placeholder entry is
    # present for any variables which are
    # not in the variable table, but which
    # are in the data file(s).
    for i, col in enumerate(cols):

        vid  = col.vid
        name = col.name

        if vid in vartable.index:
            continue

        unknownVars.append(col)
        addNewVariable(vartable, vid, name)

    # And the inverse - we can drop any
    # variables from the variable table
    # that are not in the data.
    if dropAbsent:
        vids = [c.vid for c in cols]
        vartable.drop([v for v in vartable.index if v not in vids],
                      inplace=True)

    # Merge data coding specific NAValues,
    # RawLevels, and NewLevels from the data
    # coding table. into the variable table.
    with_datacoding = vartable['DataCoding'].notna()

    for field in ['NAValues', 'RawLevels', 'NewLevels']:
        mask    = vartable[field].isna() & with_datacoding
        newvals = vartable.loc[mask].merge(dctable,
                                           left_on='DataCoding',
                                           right_index=True,
                                           suffixes=('_v', '_dc'),
                                           copy=False)['{}_dc'.format(field)]
        vartable.loc[mask, field] = newvals

    # Merge type-specific Clean
    # from the type table into
    # the variable table.
    for vid in vartable.index:

        if vid == 0:
            continue

        vtype = vartable.loc[vid, 'Type']
        pp    = vartable.loc[vid, 'Clean']

        # Override with typeClean if necessary
        if typeClean is not None and vtype in typeClean:
            tpp = convert_Process('cleaner', typeClean[vtype])
        elif vtype in tytable.index:
            tpp = collections.OrderedDict((tytable.loc[vtype, 'Clean']))
        else:
            continue

        # type cleaning is applied after
        # variable-specific cleaning
        if pd.isnull(pp): vartable.loc[[vid], 'Clean'] = [tpp]
        else:             vartable.loc[ vid,  'Clean'].update(tpp)

    # Override cleaning with expressions
    # that have been passed on the command line
    if clean is not None:

        # Ignore any variables that
        # are not in variable table
        vids  = list(clean.keys())
        vin   = pd.Series(vids).isin(vartable.index)
        vids  = [v for i, v in enumerate(vids) if vin[i]]
        exprs = [convert_Process('cleaner', clean[vid]) for vid in vids]

        vartable.loc[vids, 'Clean'] = exprs

    # Add global cleaning to all variables
    if globalClean is not None:

        for vid in vartable.index:

            if vid == 0:
                continue

            pp  = vartable.loc[vid, 'Clean']
            gpp = convert_Process('cleaner', globalClean)

            # global cleaning is applied
            # after all other cleaning
            if pd.isnull(pp): vartable.loc[[vid], 'Clean'] = [gpp]
            else:             vartable.loc[ vid,  'Clean'].update(gpp)

    return vartable, unknownVars


def addNewVariable(vartable, vid, name, dtype=None):
    """Add a new row to the variable table.

    :arg vartable: The variable table
    :arg vid:      Integer variable ID
    :arg name:     Variable name - used as the description
    :arg dtype:    ``numpy`` data type. If ``None``, the variable type
                   is set to :attr:`.util.CTYPES.unknown`.
    """

    # set dtype to something which
    # will cause the conditionals
    # to fall through
    if dtype is None: dtype = object
    else:             dtype = dtype.type

    if   issubclass(dtype, np.integer): dtype = util.CTYPES.integer
    elif issubclass(dtype, np.float):   dtype = util.CTYPES.continuous
    else:                               dtype = util.CTYPES.unknown

    vartable.loc[vid, 'Description'] = name
    vartable.loc[vid, 'Type']        = dtype


def loadProcessingTable(procfile,
                        skipProcessing=False,
                        prependProcess=None,
                        appendProcess=None,
                        **kwargs):
    """Loads the processing table from the given file.

    :arg procfile:       Path to the processing table file.

    :arg skipProcessing: If ``True``, the processing table is not loaded from
                         ``procfile``. The ``prependProcess`` and
                         ``appendProcess`` arguments are still applied.

    :arg prependProcess: Sequence of ``(varids, procstr)`` mappings specifying
                         processes to prepend to the beginning of the
                         processing table.

    :arg appendProcess:  Sequence of ``(varids, procstr)`` mappings specifying
                         processes to append to the end of the processing
                         table.

    All other keyword arguments are ignored.
    """

    if prependProcess is None: prependProcess = []
    if appendProcess  is None: appendProcess  = []

    if not skipProcessing:
        log.debug('Loading processing table from %s', procfile)
        proctable = pd.read_csv(procfile, '\t',
                                index_col=False,
                                converters=PROCTABLE_CONVERTERS)

    else:
        proctable = pd.DataFrame(columns=['Variable', 'Process'])

    # prepend/append custom
    # processes to the table
    proctable.index += len(prependProcess)
    for i, (vids, procs) in enumerate(prependProcess):
        vids  = convert_Process_Variable(vids)
        procs = convert_Process('processor', procs)
        proctable.loc[i, ['Variable', 'Process']] = [vids, procs]

    for i, (vids, procs) in enumerate(appendProcess, len(proctable.index)):
        vids  = convert_Process_Variable(vids)
        procs = convert_Process('processor', procs)
        proctable.loc[i, ['Variable', 'Process']] = [vids, procs]

    proctable.sort_index(inplace=True)

    return proctable


def loadCategoryTable(catfile, unknownVars=None):
    """Loads the category table from the given file.

    :arg catfile:     Path to the category file.
    :arg unknownVars: Sequence of :class:`.Column` objects representing
                      variables to add to an "unknown" category.
    """
    log.debug('Loading category table from %s', catfile)
    cattable = pd.read_csv(catfile,
                           '\t',
                           dtype=CATTABLE_DTYPES,
                           converters=CATTABLE_CONVERTERS).set_index('ID')

    # add an implicit "unknown" category
    # for any columns in the data file
    # which are unknown
    if unknownVars is not None:

        unknownVids = list(sorted(set([c.vid for c in unknownVars])))

        # unknown column already in table?
        umask = cattable['Category'] == 'unknown'

        if np.any(umask):
            idx         = np.where(umask)[0][0]
            idx         = cattable.index[idx]
            unknownVids = cattable.loc[idx, 'Variables'] + unknownVids
        else:
            idx = UNKNOWN_CATEGORY_ID

        cattable.loc[idx, 'Category']  = 'unknown'
        cattable.loc[idx, 'Variables'] = list(unknownVids)

    return cattable


def categoryVariables(cattable, categories):
    """Returns a list of variable IDs from ``cattable`` which correspond to
    the strings in ``categories``.

    :arg cattable:   The category table.
    :arg categories: Sequence of integer category IDs or label sub-strings
                     specifying the categories to return.
    :returns:        A list of variable IDs as strings.
    """

    allvars = []

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for cat in categories:

            catpat  = re.compile('({})'.format(cat), re.IGNORECASE)
            idmask  = cattable.index.isin([cat])
            lblmask = cattable['Category'].str.contains(catpat)
            catvars = cattable.loc[idmask | lblmask, 'Variables']

            if len(catvars) == 0:
                continue

            for c in catvars.iloc[0]:
                if c not in allvars:
                    allvars.append(c)

    return allvars


def columnTypes(vartable, columns):
    """Retrieves the type of each column in ``cols`` as listed in ``vartable``.
    Also identifies a suitable internal data type to use for each column where
    possible.

    :arg vartable: The variable table.

    :arg columnss: List of :class:`.Column` objects.

    :returns:      A tuple containing:

                    - A list containing the type for each column in ``cols`` -
                      an identifier from the :attr:`.util.CTYPES` enum.
                      Columns corresponding to a variable which is not in
                      the variable table is given a type of ``None``.

                    - A dict of ``{ column_name : dtype }`` mappings containing
                      a suitable internal data type to use for some columns.
    """

    vttypes = []
    dtypes  = {}

    for col in columns:

        vid  = col.vid
        name = col.name

        if vid not in vartable.index:
            vttypes.append(None)
            continue

        vttype = vartable.loc[vid, 'Type']
        dtype  = util.DATA_TYPES.get(vttype, None)

        vttypes.append(vttype)
        if dtype is not None:
            dtypes[name] = dtype

    return vttypes, dtypes
