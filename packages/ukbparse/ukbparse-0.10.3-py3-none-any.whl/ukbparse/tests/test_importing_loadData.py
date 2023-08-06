#!/usr/bin/env python
#
# test importing_loadData.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import multiprocessing as mp
import textwrap as tw

import numpy as np
import pandas as pd

import ukbparse.importing as importing
import ukbparse.util      as util
import ukbparse.custom    as custom
import ukbparse.fileinfo  as fileinfo
import ukbparse.storage   as storage

from . import tempdir, gen_tables, gen_test_data


def test_loadData():

    vartable = gen_tables([10, 100])[0]
    data     = np.random.randint(1, 100, (10, 2))

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid, 10-0.0, 100-0.0\n')
            for i, d in enumerate(data):
                f.write('{}, {}, {}\n'.format(i, *d))
            f.write('11, 54, abcde\n')

        cols = fileinfo.fileinfo(('data.txt', ))[2][0]
        cols = {'data.txt' : cols}

        vartable.loc[10,  'Type'] = util.CTYPES.integer
        vartable.loc[100, 'Type'] = util.CTYPES.continuous

        loaded = importing.loadData('data.txt', vartable, cols)[0]
        got10  = loaded['10-0.0'].values
        got100 = loaded['100-0.0'].values

        # both 10 and 100 should be numeric
        exp10  = np.array(list(data[:, 0]) + [54])
        exp100 = np.array(list(data[:, 1]) + [np.nan])

        gotnan = np.isnan(got100)

        assert np.all(exp10 == got10)
        assert np.all(np.isnan(exp100) == gotnan)
        assert np.all(exp100[~gotnan] == got100[~gotnan])


def test_loadData_multiple_files_cols():
    vartable = gen_tables([10, 20, 30, 40])[0]
    data = [
        np.random.randint(1, 100, (10, 2)),
        np.random.randint(1, 100, (10, 2))]

    with tempdir():
        dfiles = ['data{}.txt'.format(i) for i in range(len(data))]
        for fi, d in enumerate(data):
            with open(dfiles[fi], 'wt') as f:

                cols = ['eid'] + ['{}-0.0'.format((ci + 1) * 10)
                                  for ci in range(fi * 2, fi * 2 + 2)]

                f.write('{}\n'.format(','.join(cols)))

                for ri, c in enumerate(d):
                    f.write('{}, {}, {}\n'.format(ri, *c))

        cols    = fileinfo.fileinfo(dfiles)[2]
        coldict = {f : c for f, c in zip(dfiles, cols)}

        loaded, lcols = importing.loadData(dfiles, vartable, coldict)

        assert lcols == cols[0] + cols[1][1:]

        assert np.all(loaded['10-0.0'] == data[0][:, 0])
        assert np.all(loaded['20-0.0'] == data[0][:, 1])
        assert np.all(loaded['30-0.0'] == data[1][:, 0])
        assert np.all(loaded['40-0.0'] == data[1][:, 1])


def test_loadData_multiple_files_rows():
    vartable = gen_tables([10, 20])[0]
    data = [
        np.random.randint(1, 100, (10, 2)),
        np.random.randint(1, 100, (10, 2))]

    with tempdir():
        dfiles = ['data{}.txt'.format(i) for i in range(len(data))]
        for fi, d in enumerate(data):
            with open(dfiles[fi], 'wt') as f:

                f.write('eid, 10-0.0, 20-0.0\n')

                for ri, c in enumerate(d):
                    f.write('{}, {}, {}\n'.format(10 * fi + ri, *c))

        cols    = fileinfo.fileinfo(dfiles)[2]
        coldict = {f : c for f, c in zip(dfiles, cols)}

        loaded, lcols = importing.loadData(
            dfiles, vartable, coldict, mergeAxis='subjects')

        assert lcols == cols[0]
        assert np.all(loaded['10-0.0'] ==
                      np.concatenate((data[0][:, 0], data[1][:, 0])))
        assert np.all(loaded['20-0.0'] ==
                      np.concatenate((data[0][:, 1], data[1][:, 1])))


def test_importData():
    vartable, proctable, cattable = gen_tables([100])[:3]
    data = np.random.randint(1, 100, (10, 2))

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid, 10-0.0, 100-0.0\n')
            for i, d in enumerate(data):
                f.write('{}, {}, {}\n'.format(i, *d))

            # bad data should be interpreted as nan
            f.write('11, 54, abcde\n')

        cols = fileinfo.fileinfo(('data.txt', ))[2][0]
        cols = {'data.txt' : cols}

        vartable.loc[10,  'Type'] = util.CTYPES.integer
        vartable.loc[100, 'Type'] = util.CTYPES.continuous

        loaded, _ = importing.importData(
            'data.txt', vartable, proctable, cattable)

        assert loaded.allColumns == cols['data.txt']
        got10  = loaded[:, '10-0.0']
        got100 = loaded[:, '100-0.0']

        # 10 and 100 should be numeric,
        # non-numeric valuus should be
        # set to nan
        exp10     = np.array(list(data[:, 0]) + [54])
        exp100    = np.array(list(data[:, 1]) + [np.nan])
        got100nan = got100.isna()

        assert np.all(exp10 == got10)
        assert np.all(np.isnan(exp100) == got100nan)
        assert np.all(exp100[~got100nan] == got100[~got100nan])


def test_importData_dropped():
    vartable, proctable, cattable = gen_tables([100])[:3]
    data = np.random.randint(1, 100, (10, 3))

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid, 1-0.0, 2-0.0, 3-0.0\n')
            for i, d in enumerate(data):
                f.write('{}, {}, {}, {}\n'.format(i, *d))

        cols = fileinfo.fileinfo(('data.txt', ))[2][0]

        loaded, dropped = importing.importData(
            'data.txt', vartable, proctable, cattable, variables=[1, 3])

        assert dropped           == [cols[2]]
        assert loaded.allColumns == [cols[0]] + cols[1::2]


def test_loadData_lowMemory():

    vartable = gen_tables(range(1, 51))[0]

    with tempdir() as td, mp.Pool(10) as pool:

        mgr  = mp.Manager()

        gen_test_data(200, 50, 'data.txt')
        data = pd.read_csv('data.txt', delimiter='\t', index_col='eid')

        cols = fileinfo.fileinfo(('data.txt', ))[2][0]
        cols = {'data.txt' : cols}

        loaded, lcols = importing.loadData('data.txt',
                                           vartable,
                                           cols,
                                           lowMemory=True,
                                           workDir=td,
                                           pool=pool,
                                           mgr=mgr)

        assert isinstance(loaded, storage.HDFStoreCollection)
        assert np.all(loaded.loc[:] == data)


def test_importData_lowMemory():

    vartable, proctable, cattable = gen_tables(range(1, 51))[:3]

    custom.registerBuiltIns()

    with tempdir(), mp.Pool(10) as pool:

        mgr  = mp.Manager()

        gen_test_data(200, 50, 'data.txt')
        data = pd.read_csv('data.txt', delimiter='\t', index_col='eid')

        cols = fileinfo.fileinfo(('data.txt', ))[2][0]
        cols = {'data.txt' : cols}

        loaded, _ = importing.importData('data.txt',
                                         vartable,
                                         proctable,
                                         cattable,
                                         lowMemory=True,
                                         pool=pool,
                                         mgr=mgr)

        assert loaded.allColumns == cols['data.txt']
        assert np.all(loaded[:] == data.loc[:])


def test_encoding():

    ascii_val  = 'abc'
    latin1_val = '\xa1\xa2\xa3'
    utf8_val   = '\u1F610\u1F632\u1F640'

    vartable, proctable, cattable = gen_tables(range(1, 2))[:3]

    with tempdir():

        for val, enc in zip(
                [ascii_val, latin1_val, utf8_val],
                ['ascii', 'latin1', 'utf8']):

            data = tw.dedent("""
            eid, 1-0.0
            1, {}
            """.format(val)).strip()

            with open('data.txt',  'wt') as f:
                f.write(data)

        df_enc, _ = importing.importData(
            'data.txt',
            vartable,
            proctable,
            cattable,
            encoding=enc)
        assert df_enc[1, '1-0.0'] == val

        # ascii/latin1 should load ok without
        # us having to specify the encoding
        if enc in ('ascii', 'latin1'):
            df_noenc, _ = importing.importData(
                'data.txt',
                vartable,
                proctable,
                cattable)
            assert df_noenc[1, '1-0.0'] == val
