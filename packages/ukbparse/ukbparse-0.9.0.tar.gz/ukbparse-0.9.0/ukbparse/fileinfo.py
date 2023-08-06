#!/usr/bin/env python
#
# fileinfo.py - Get information about input files.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains the :func:`sniff` and :func:`fileinfo` functions, for
getting information about input data files.
"""


import functools as ft
import os.path   as op
import              io
import              csv
import              logging

import              six

from . import       util
from . import       custom
from . import       datatable


log = logging.getLogger(__name__)


@ft.lru_cache()
def sniff(datafile):
    """Identifies the format of the given input data file.

    :arg datafile: Input data file
    :returns:      A tuple containing:

                    - A ``csv`` dialect type

                    - List of ``Column`` objects. The ``name`` attributes will
                      be ``None`` if the file does not have a header row.
                      The ``variable``, ``visit``, and ``instance`` attributes
                      will be ``None``if the file does not have UKB-style
                      column names.
    """

    # Read the first few lines
    lines = []
    with open(datafile, 'rt') as f:
        for i in range(4):

            line = f.readline()

            # eof
            if len(line) == 0:
                break

            line = line.strip('\n')

            if len(line) > 0:
                lines.append(line)

    if len(lines) == 0:
        raise ValueError('Empty file: {}'.format(datafile))

    # Identify the CSV dialect (e.g.
    # tab- or comma-separated values)
    sniffer = csv.Sniffer()
    sample  = '\n'.join(lines)

    try:
        dialect = sniffer.sniff(sample)
    except csv.Error:
        dialect = None

    # But if the sniffer failed, or detected
    # space-separated data, let's try and
    # test whether it is fixed-width or
    # variable-whitespace delimited data (as
    # the sniffer can't detect these formats).
    if dialect is None or dialect.delimiter == ' ':

        linewords = [line.split() for line in lines]

        # Heuristic 1: If the number of columns
        # differs depending on whether we split
        # on a single space, or variable
        # whitespace, then this might be a fixed-
        # width or variable-whitespace delimited
        # file.
        spacesneq = any([line.split(' ') != words
                         for line, words in zip(lines, linewords)])

        # Heuristic 2: If each line has the same
        # number of space-separated words, it
        # might be whitespace-delimited
        nwords    = [len(lw) for lw in linewords]
        avgwords  = float(sum(nwords)) / len(nwords)
        samewords = all([n == avgwords for n in nwords])

        if spacesneq and samewords:
            dialect = 'whitespace'

    # Give up if it doesn't look like
    # CSV or whitespace delimited data
    if dialect is None:
        raise ValueError('Could not determine file format: '
                         '{}'.format(datafile))

    # if whitespace-delimited, we re-generate
    # the sample into a format that will be
    # recognised by the sniffer, purely so we
    # can use its has_header method. We take
    # a copy of the first row, so we can
    # extract column names if possible.
    if dialect == 'whitespace':
        firstRow  = lines[0].split()
        lines     = [','.join(line.split()) for line in lines]
        hasHeader = sniffer.has_header('\n'.join(lines))

    # Otherwise we pass the unmodified sample,
    # and read in the first row.
    else:
        hasHeader = sniffer.has_header(sample)
        reader    = csv.reader(io.StringIO(sample), dialect)
        firstRow  = next(reader)

    log.debug('Detected dialect for input file %s: (header: %s, '
              'delimiter: %s)',
              datafile, hasHeader,
              dialect if isinstance(dialect, str) else dialect.delimiter)

    # Now create a Column object for
    # each column in the data file.
    columns = []

    for i, col in enumerate(firstRow):

        name     = None
        vid      = None
        visit    = None
        instance = None

        # If there is a header, extract
        # the columns and attempt to
        # identify UKB variables.
        if hasHeader:

            name = col

            try:
                vid, visit, instance = util.parseColumnName(col)
            except ValueError:
                pass

        columns.append(
            datatable.Column(datafile, name, i, vid, visit, instance))

    return dialect, columns


@ft.lru_cache()
def fileinfo(datafiles, sniffers=None):
    """Identifies the format of each input data file, and extracts/generates
    column names and variable IDs for every column.

    :arg datafiles: Tuple (*must* be a tuple) of data files to be loaded.

    :arg sniffer:   Tuple containing ``(file, snifferName)`` pairs, specifying
                    custom sniffers to be used for specific files. See the
                    :mod:`.custom` module.

    :returns: A tuple containing:

               - List of ``csv`` dialect types

               - List of booleans, indicating whether or not each file has a
                 header row.

               - List of lists, ``Column`` objects representing the columns
                 in each file.
    """

    if sniffers is None:
        sniffers = []
    sniffers = dict(sniffers)

    if isinstance(datafiles, six.string_types):
        datafiles = [datafiles]

    # Situations we need to handle:
    #
    #  1. Data file is UKB-style - each column
    #     has a variable ID, visit, and instance
    #
    #  2. Data file has arbitray column names.
    #  3. Data file has no column names.
    #
    # In the latter two cases, we need to
    # generate variable IDs for each column
    # and, for the last case, generate
    # column names as well.
    dialects = []
    cols     = []

    for f in datafiles:

        sniffer = sniffers.get(op.basename(f), None)

        if sniffer is not None:
            dialect = 'custom ({})'.format(sniffer)
            fcols   = custom.runSniffer(sniffer, f)
        else:
            dialect, fcols = sniff(f)

        dialects.append(dialect)
        cols    .append(fcols)

    # Now we need to fix all non-UKB
    # style input files - generating
    # dummy variables, and generating
    # column names if necessary.
    headers = []
    autovid = datatable.AUTO_VARIABLE_ID
    for fi in range(len(datafiles)):

        fcols = cols[fi]

        # save whether or not each
        # file has a header row.
        headers.append(fcols[0].name is not None)

        for ci, col in enumerate(fcols):

            # UKB-style - all good
            if col.vid is not None:
                continue

            # Non-UKB style file - assign
            # a (vid, visit, instance) to
            # each column, assuming that
            # the first column is an index
            # (and is given ID 0)
            if ci == 0:
                vid = 0
            else:
                vid      = autovid
                autovid += 1

            col.vid      = vid
            col.visit    = 0
            col.instance = 0

            # And generate a name for
            # each column if necessary
            if col.name is None:
                col.name = util.generateColumnName(vid, 0, 0)

    return dialects, headers, cols
