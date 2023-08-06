#!/usr/bin/env python
#
# test_main.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import textwrap  as tw
import os.path   as op
import              os
import              shlex

from unittest import mock

import numpy as np
import pytest

import pandas as pd

import ukbparse.main       as main
import ukbparse.custom     as custom
import ukbparse.importing  as importing
import ukbparse.loadtables as loadtables

from . import (patch_logging,
               clear_plugins,
               tempdir,
               gen_tables,
               gen_DataTable,
               gen_test_data,
               gen_DataTableFromDataFrame)


@patch_logging
def test_main_minimal():
    with tempdir():
        gen_test_data(10, 100, 'data.tsv')
        main.main('out.tsv data.tsv'.split())

        out  = pd.read_csv('out.tsv',  delimiter='\t')
        data = pd.read_csv('data.tsv', delimiter='\t')

        assert np.all(out.columns == data.columns)
        assert np.all(out.values  == data.values)


@patch_logging
def test_main_minimal_lowMemory():
    with tempdir():
        gen_test_data(10, 100, 'data.tsv')
        main.main('-n -n -lm out.tsv data.tsv'.split())

        out  = pd.read_csv('out.tsv',  delimiter='\t')
        data = pd.read_csv('data.tsv', delimiter='\t')

        assert np.all(out.columns == data.columns)
        assert np.all(out.values  == data.values)


@patch_logging
def test_main_overwrite():
    with tempdir():
        gen_test_data(10, 100, 'data.tsv')

        with open('out.tsv', 'wt') as f:
            f.write('abc')

        with pytest.raises(SystemExit):
            main.main('out.tsv data.tsv'.split())

        with open('out.tsv', 'rt') as f:
            assert f.read() == 'abc'

        main.main('-ow out.tsv data.tsv'.split())

        out  = pd.read_csv('out.tsv',  delimiter='\t')
        data = pd.read_csv('data.tsv', delimiter='\t')

        assert np.all(out.columns == data.columns)
        assert np.all(out.values  == data.values)


@clear_plugins
@patch_logging
def test_main_pluginfile():

    plugin = tw.dedent("""
    import ukbparse.custom as custom

    @custom.cleaner()
    def replace_with_nines(dtable, vid):
        for col in dtable.columns(vid):
            dtable[:, col.name] = [9] * len(dtable)
    """).strip()

    with tempdir():
        gen_test_data(10, 100, 'data.tsv')

        with open('plugin.py', 'wt') as f:
            f.write(plugin)

        main.main(
            '-p plugin.py -sp -gc replace_with_nines out.tsv data.tsv'.split())

        out = pd.read_csv('out.tsv', delimiter='\t')

        exp         = np.zeros((11, 100))
        exp[0,  :]  = range(1, 101)
        exp[1:, :] = 9

        assert np.all(out.values == exp.T)


@patch_logging
def test_main_passthrough():
    with tempdir():
        gen_test_data(10, 100, 'data.tsv')

        main.main('-sn -scv -scf -sr -sp out1.tsv data.tsv'.split())
        main.main('-pt                   out2.tsv data.tsv'.split())

        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        out1 = pd.read_csv('out1.tsv', delimiter='\t', index_col=0)
        out2 = pd.read_csv('out2.tsv', delimiter='\t', index_col=0)

        assert (out1.columns == data.columns).all()
        assert np.all((out1 == data))
        assert (out2.columns == data.columns).all()
        assert np.all((out2 == data))


@patch_logging
def test_main_configfile():

    cfg = tw.dedent("""
    overwrite
    """).strip()

    with tempdir():
        gen_test_data(10, 100, 'data.tsv')

        with open('out.tsv', 'wt') as f:
            f.write('abc')

        with open('config.txt', 'wt') as f:
            f.write(cfg)

        main.main('-cfg config.txt out.tsv data.tsv'.split())

        out  = pd.read_csv('out.tsv',  delimiter='\t')
        data = pd.read_csv('data.tsv', delimiter='\t')

        assert np.all(out.columns == data.columns)
        assert np.all(out.values  == data.values)


@clear_plugins
@patch_logging
def test_main_loader():
    plugin = tw.dedent("""
    import ukbparse
    import pandas as pd

    @ukbparse.sniffer('silly_loader')
    def silly_sniffer(infile):
        return [
            ukbparse.Column(infile, 'eid',   0, 0,     0, 0),
            ukbparse.Column(infile, '1-0.0', 0, 12345, 0, 0)]

    @ukbparse.loader()
    def silly_loader(infile):
        df = pd.DataFrame()
        df['eid']   = list(range(1, 101))
        df['1-0.0'] = list(reversed(range(100)))
        return df.set_index('eid')
    """).strip()

    with tempdir():

        with open('in.tsv', 'wt') as f:
            f.write(' ')

        with open('plugin.py', 'wt') as f:
            f.write(plugin)

        main.main(
            '-p plugin.py -l in.tsv silly_loader out.tsv in.tsv'.split())

        out = pd.read_csv('out.tsv', delimiter='\t')

        exp         = np.zeros((2, 100))
        exp[0, :] = list(range(1, 101))
        exp[1, :] = list(reversed(range(100)))

        assert np.all(out.values == exp.T)


@patch_logging
def test_main_variables():
    with tempdir():
        gen_test_data(10, 100, 'data.tsv')

        with open('varfile.txt', 'wt') as f:
            f.write('2\n')
            f.write('3\n')

        main.main('-v varfile.txt -v 4 -v 5 -v 6:7 out.tsv data.tsv'.split())

        data = pd.read_csv('data.tsv', delimiter='\t').set_index('eid')
        out  = pd.read_csv('out.tsv',  delimiter='\t').set_index('eid')

        expcols = ['{}-0.0'.format(i) for i in [2, 3, 4, 5, 6, 7]]

        assert (out.columns == expcols).all()
        assert np.all(out.loc[:, :] == data.loc[:, expcols])

        # Make sure duplicate variables are ignored
        with open('varfile.txt', 'wt') as f:
            f.write('2\n')
            f.write('2\n')
            f.write('3\n')
            f.write('3\n')
            f.write('3\n')
            f.write('4\n')

        main.main('-ow -v varfile.txt -v 3 -v 4 -v 5 -v 5 -v 6:7 '
                  'out.tsv data.tsv'.split())

        data = pd.read_csv('data.tsv', delimiter='\t').set_index('eid')
        out  = pd.read_csv('out.tsv',  delimiter='\t').set_index('eid')

        expcols = ['{}-0.0'.format(i) for i in [2, 3, 4, 5, 6, 7]]

        assert (out.columns == expcols).all()
        assert np.all(out.loc[:, :] == data.loc[:, expcols])


@clear_plugins
@patch_logging
def test_main_formatters():

    def _datefmt(d):
        return d.strftime('%d-%m-%Y')
    def _timefmt(t):
        return t.strftime('%d-%m-%Y %S %M %H')

    plugin = tw.dedent("""
    from ukbparse import custom

    def _datefmt(d):
        return d.strftime('%d-%m-%Y')
    def _timefmt(t):
        return t.strftime('%d-%m-%Y %S %M %H')

    @custom.formatter('test_date_format')
    def datefmt(dtable, column, series):
        return series.apply(_datefmt)

    @custom.formatter('test_time_format')
    def timefmt(dtable, column, series):
        return series.apply(_timefmt)

    @custom.formatter('test_var_format')
    def varfmt(dtable, column, series):
        def fmt(v):
            return str(v + 10)
        return series.apply(fmt)
    """).strip()

    with tempdir():

        # Using specific VIDs that
        # are date/time types in the
        # built-in variable table
        datecol = '53-0.0'
        timecol = '4289-0.0'
        varcol1 = '48-0.0'
        varcol2 = '49-0.0'
        datevar = 53
        timevar = 4289
        varvar1 = 48
        varvar2 = 49
        names = [datecol, timecol, varcol1, varcol2]

        with open('plugin.py', 'wt') as f:
            f.write(plugin)

        gen_test_data(4, 100, 'data.tsv', ctypes={1 : 'date', 2 : 'datetime'},
                      names=names)

        data = pd.read_csv('data.tsv',
                           delimiter='\t',
                           parse_dates=[datecol, timecol],
                           infer_datetime_format=True,
                           index_col=0)

        main.main('-n -n '
                  '-p plugin.py '
                  '-edf test_date_format '
                  '-etf test_time_format '
                  '-tvf {} test_var_format '
                  '-tvf {} test_var_format '
                  'out.tsv data.tsv'.format(varvar1, varcol2).split())

        got  = pd.read_csv('out.tsv', delimiter='\t')
        gotd =          got[ datecol]
        gott =          got[ timecol]
        got1 =          got[ varcol1]
        got2 =          got[ varcol2]
        expd =          data[datecol].apply(_datefmt)
        expt =          data[timecol].apply(_timefmt)
        exp1 = np.array(data[varcol1] + 10)
        exp2 = np.array(data[varcol2] + 10)

        assert np.all(np.array(gotd) == expd)
        assert np.all(np.array(gott) == expt)
        assert np.all(np.array(got1) == exp1)
        assert np.all(np.array(got2) == exp2)


@patch_logging
@clear_plugins
def test_main_loader():

    plugin = tw.dedent("""
    import pandas as pd
    import numpy  as np

    from ukbparse import datatable
    from ukbparse import custom

    @custom.sniffer('test_loader')
    def sniffer(infile):
        cols = [
            datatable.Column(infile, 'eid',   0, 0, 0, 0),
            datatable.Column(infile, '1-0.0', 1, 1, 0, 0)]
        return cols

    @custom.loader('test_loader')
    def loader(infile):
        df            = pd.DataFrame()
        df['eid']   = np.arange(10, 110)
        df['1-0.0'] = [12345] * 100
        return df.set_index('eid')
    """).strip()


    with tempdir():

        with open('plugin.py', 'wt') as f:
            f.write(plugin)

        with open('data.tsv', 'wt') as f:
            f.write(' ')
        main.main('-p plugin.py '
                  '-l data.tsv test_loader out.tsv data.tsv'.split())

        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert np.all(got.index      == np.arange(10, 110))
        assert np.all(got['1-0.0'] == 12345)


@patch_logging
@clear_plugins
def test_main_visits():

    custom.registerBuiltIns()

    plugin = tw.dedent("""
    from ukbparse import custom

    @custom.cleaner('test_clean')
    def clean(dtable, vid):
        dtable[:, dtable.columns(vid)[0].name] *= 2
    """).strip()

    with tempdir():

        with open('plugin.py', 'wt') as f:
            f.write(plugin)

        gen_test_data(10, 100, 'data.tsv', min_visits=2, max_visits=3)

        tables = loadtables.loadDefaultTables(['data.tsv'])[:3]
        dt     = importing.importData(['data.tsv'], *tables)

        base = '-p plugin.py -ow '

        main.main((base + '-vi first out.tsv data.tsv').split())
        gotfirst = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        main.main((base + '-vi last out.tsv data.tsv').split())
        gotlast = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        main.main((base + '-vi 1 out.tsv data.tsv').split())
        gotone = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        main.main((base + '-vi 1 -gc test_clean out.tsv data.tsv').split())
        gotonecleaned = pd.read_csv('out.tsv', delimiter='\t', index_col=0)

        for vid in dt.variables:
            if vid == 0:
                continue
            firstcol = dt.columns(vid)[ 0].name
            lastcol  = dt.columns(vid)[-1].name
            onecol   = dt.columns(vid)[ 1].name

            assert np.all(dt[:, firstcol]   == gotfirst[     firstcol])
            assert np.all(dt[:, lastcol]    == gotlast[      lastcol])
            assert np.all(dt[:, onecol]     == gotone[       onecol])
            assert np.all(dt[:, onecol] * 2 == gotonecleaned[onecol])


@patch_logging
def test_main_subjects():

    custom.registerBuiltIns()

    with tempdir():
        data = np.random.randint(1, 10, (100, 6))
        data[:, 0] = np.arange(1, 101)
        data[ :20:2, 1] = 6
        data[1:20:2, 1] = 2
        cols = ['eid'] + ['{}-0.0'.format(i) for i in range(1, 6)]

        np.savetxt('data.tsv', data, delimiter='\t', header='\t'.join(cols))

        tables = loadtables.loadDefaultTables(['data.tsv'])[:3]
        dt     = importing.importData(['data.tsv'], *tables)

        with open('subjects.txt', 'wt') as f:
            f.write('\n'.join(map(str, [1, 2, 3])))

        main.main(shlex.split('-ow '
                              '-s subjects.txt '
                              '-s 3 '
                              '-s 3 '
                              '-s 4 '
                              '-s 4 '
                              '-s 5:10 '
                              '-s "v1 > 4" '
                              '-ex 8:20 '
                              '-sp '
                              'out.tsv data.tsv'))

        mask = np.zeros(100, dtype=np.bool)
        mask[:8:2] = 1

        got  = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp  = dt[mask, :]

        assert np.all(got == exp)


@patch_logging
def test_main_categories():
    with tempdir():

        with open('variables.tsv', 'wt') as f:
            f.write('ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean\n')
            f.write( '1\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write( '3\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write( '5\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write( '7\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write( '9\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('11\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('13\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('15\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('17\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('19\tContinuous\t\t\t\t\t\t\t\t\n')

        with open('categories.tsv', 'wt') as f:
            f.write('ID\tCategory\tVariables\n')
            f.write('1\tcat1\t1:5\n')
            f.write('2\tcat2\t6:10\n')
            f.write('3\tcat3\t11:15\n')

        cat1 = ['{}-0.0'.format(i) for i in range(1,  6)]
        cat2 = ['{}-0.0'.format(i) for i in range(6,  11)]
        unkn = ['{}-0.0'.format(i) for i in range(2, 21, 2)]
        cat3 = ['{}-0.0'.format(i) for i in range(11, 16)]

        gen_test_data(20, 100, 'data.tsv')

        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)

        pref = '-ow -cf categories.tsv -vf variables.tsv '
        suf  = ' out.tsv data.tsv'

        main.main((pref + '-c cat1' + suf).split())
        out = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert np.all(out.loc[:, :] == data.loc[:, cat1])

        main.main((pref + '-c 1' + suf).split())
        out = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert np.all(out.loc[:, :] == data.loc[:, cat1])

        main.main((pref + '-c cat2' + suf).split())
        out = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert np.all(out.loc[:, :] == data.loc[:, cat2])

        main.main((pref + '-c 1 -c cat2' + suf).split())
        out = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert np.all(out.loc[:, :] == data.loc[:, cat1 + cat2])

        main.main((pref + '-c unknown' + suf).split())
        out = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert np.all(out.loc[:, :] == data.loc[:, unkn])

        main.main((pref + '-c -1' + suf).split())
        out = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert np.all(out.loc[:, :] == data.loc[:, unkn])

        main.main((pref + '-c -1 -c cat3' + suf).split())
        out = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        expcols = unkn + [c for c in cat3 if c not in unkn]
        assert np.all(out.loc[:, :] == data.loc[:, expcols])


@patch_logging
def test_main_column_names():
    with tempdir():
        gen_test_data(10, 100, 'data.tsv')

        main.main(shlex.split('-oi subby -cp "{variable}-woo" out.tsv data.tsv'))
        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = ['{}-woo'.format(i) for i in range(1, 11)]
        assert np.all(got.columns == exp)
        assert got.index.name == 'subby'

        main.main(shlex.split(
            '-ow -rc 1-0.0 woopy -cp "{name}" out.tsv data.tsv'))
        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = ['{}-0.0'.format(i) for i in range(1, 11)]
        exp[0] = 'woopy'
        assert np.all(got.columns == exp)

        # non-standard input column names
        names = ['{}-0.0'.format(i) for i in range(1, 10)] + ['woopy']
        gen_test_data(10, 100, 'data.tsv', names=names)
        main.main(shlex.split('-ow out.tsv data.tsv'))
        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert sorted(got.columns) == sorted(names)

        gen_test_data(10, 100, 'data.tsv', names=names)
        main.main(shlex.split('-ow -cp "{name}-{visit}" out.tsv data.tsv'))
        exp = ['{}-0.0-0'.format(i) for i in range(1, 10)] + ['woopy-0']
        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert sorted(got.columns) == sorted(exp)


@patch_logging
@clear_plugins
def test_main_clean():

    plugin = tw.dedent("""
    from ukbparse import custom

    @custom.cleaner('test_clean1')
    def clean1(dtable, vid):
        dtable[:, dtable.columns(vid)[0].name] *= 2
    @custom.cleaner('test_clean2')
    def clean2(dtable, vid):
        dtable[:, dtable.columns(vid)[0].name] *= 3
    @custom.cleaner('test_clean3')
    def clean3(dtable, vid):
        dtable[:, dtable.columns(vid)[0].name] *= 4
    @custom.cleaner('test_clean4')
    def clean4(dtable, vid):
        dtable[:, dtable.columns(vid)[0].name] *= 5
    @custom.cleaner('test_clean_int')
    def clean_int(dtable, vid):
        dtable[:, dtable.columns(vid)[0].name] *= 6
    """).strip()

    with tempdir():

        with open('plugin.py', 'wt') as f:
            f.write(plugin)

        with open('variables.tsv', 'wt') as f:
            f.write('ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean\n')
            f.write( '4\tInteger\t\t\t\t\t\t\t\t\n')

        gen_test_data(10, 100, 'data.tsv')
        main.main('-p plugin.py '
                  '-vf variables.tsv '
                  '-cl 1 test_clean1 '
                  '-cl 2 test_clean2 '
                  '-cl 3 test_clean3 '
                  '-tc integer test_clean_int '
                  'out.tsv data.tsv'.split())

        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        got  = pd.read_csv('out.tsv',  delimiter='\t', index_col=0)

        assert np.all(( 2 * data['1-0.0']) == got['1-0.0'])
        assert np.all(( 3 * data['2-0.0']) == got['2-0.0'])
        assert np.all(( 4 * data['3-0.0']) == got['3-0.0'])
        assert np.all(( 6 * data['4-0.0']) == got['4-0.0'])

        main.main('-ow '
                  '-cl 4 test_clean4 '
                  '-gc test_clean1 '
                  'out.tsv data.tsv'.split())

        got  = pd.read_csv('out.tsv',  delimiter='\t', index_col=0)
        assert np.all(( 2 * data['1-0.0']) == got['1-0.0'])
        assert np.all(( 2 * data['2-0.0']) == got['2-0.0'])
        assert np.all(( 2 * data['3-0.0']) == got['3-0.0'])
        assert np.all((10 * data['4-0.0']) == got['4-0.0'])

        main.main('-ow -vf variables.tsv '
                  '-gc test_clean4 '
                  'out.tsv data.tsv'.split())
        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        got  = pd.read_csv('out.tsv',  delimiter='\t', index_col=0)
        assert np.all(( 5 * data.loc[:, :]) == got.loc[:, :])


        # Override clean on command line
        with open('variables.tsv', 'wt') as f:
            f.write('ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean\n')
            f.write( '4\tInteger\t\t\t\t\t\t\t\ttest_clean4\n')
        main.main('-ow -vf variables.tsv '
                  '-cl 4 test_clean3 '
                  'out.tsv data.tsv'.split())
        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        got  = pd.read_csv('out.tsv',  delimiter='\t', index_col=0)
        assert np.all(( 4 * data.loc[:, '4-0.0']) == got.loc[:, '4-0.0'])

        main.main(shlex.split('-ow -vf variables.tsv '
                              '-cl 4 \'\' '
                              'out.tsv data.tsv'))
        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        got  = pd.read_csv('out.tsv',  delimiter='\t', index_col=0)
        assert np.all((data.loc[:, :]) == got.loc[:, :])


@patch_logging
def test_main_badargs():

    with tempdir():

        gen_test_data(10, 10, 'data.tsv')

        with pytest.raises(ValueError):
            main.main('-f non-existent-format '
                      'out.tsv data.tsv'.split())

        with pytest.raises(ValueError):
            main.main('-l data.tsv non_existent_loader '
                      'out.tsv data.tsv'.split())

        with pytest.raises(ValueError):
            main.main('-edf non_existent_format '
                      'out.tsv data.tsv'.split())

        with pytest.raises(ValueError):
            main.main('-etf non_existent_format '
                      'out.tsv data.tsv'.split())

        with pytest.raises(ValueError):
            main.main('-tvf 1 non_existent_format '
                      'out.tsv data.tsv'.split())


@patch_logging
def test_main_subject_ordering():

    with tempdir():
        gen_test_data(10, 100, 'data.tsv')

        # skip processing, otherwise sparsity check will fail
        # main.main('-s 5:-1:1 -sp out.tsv data.tsv'.split())
        # data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        # got  = pd.read_csv('out.tsv',  delimiter='\t', index_col=0)

        # assert np.all(got == data.loc[[5, 4, 3, 2, 1], :])

        # order should still be applied if subject
        # inclusion expressions are specified
        main.main(shlex.split('-s 10:-1:1 -s "v1 > 50" -sp -ow out.tsv data.tsv'))
        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        got  = pd.read_csv('out.tsv',  delimiter='\t', index_col=0)

        exp = list(reversed(1 + np.where(data.loc[:10, '1-0.0'] > 50)[0]))
        print(exp)
        print(got.index)
        assert np.all(got.index == exp)


@patch_logging
def test_main_variable_ordering():

    with tempdir():

        gen_test_data(20, 100, 'data.tsv')
        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)

        with open('variables.tsv', 'wt') as f:
            f.write('ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean\n')
            f.write( '1\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write( '3\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write( '5\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write( '7\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write( '9\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('11\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('13\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('15\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('17\tContinuous\t\t\t\t\t\t\t\t\n')
            f.write('19\tContinuous\t\t\t\t\t\t\t\t\n')

        with open('categories.tsv', 'wt') as f:
            f.write('ID\tCategory\tVariables\n')
            f.write('1\tcat1\t1:5\n')
            f.write('2\tcat2\t6:10\n')
            f.write('3\tcat3\t11:15\n')
            f.write('4\tcat4\t16:20\n')

        allvars = ['{}-0.0'.format(v) for v in range(1,  21)]
        cat1    = ['{}-0.0'.format(v) for v in range(1,  6)]
        cat2    = ['{}-0.0'.format(v) for v in range(6,  11)]
        cat3    = ['{}-0.0'.format(v) for v in range(11, 16)]
        cat4    = ['{}-0.0'.format(v) for v in range(16, 21)]
        catunkn = ['{}-0.0'.format(v) for v in range(2,  21, 2)]

        argbase = ' -q -vf variables.tsv -cf categories.tsv  -ow out.tsv data.tsv'

        main.main(('-v 1 -v 2 -v 3' + argbase).split())
        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = data.loc[:, allvars[:3]]
        assert np.all(got == exp)

        main.main(('-v 3 -v 2 -v 1' + argbase).split())
        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = data.loc[:, allvars[2::-1]]
        assert np.all(got == exp)

        main.main(('-c cat1 -c cat3' + argbase).split())
        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = data.loc[:, cat1 + cat3]
        assert np.all(got == exp)

        main.main(('-c cat3 -c cat1' + argbase).split())
        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = data.loc[:, cat3 + cat1]
        assert np.all(got == exp)

        main.main(('-v 17 -c cat3 -v 3' + argbase).split())
        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = data.loc[:, [allvars[16]] + [allvars[2]] + cat3]
        assert np.all(got == exp)


@patch_logging
def test_main_subject_and_variable_ordering():

    with tempdir():
        gen_test_data(10, 100, 'data.tsv')

        # skip procesing, otherwise sparsity check will fail
        main.main('-s 5:-1:1 -v 5:-2:1 -sp out.tsv data.tsv'.split())
        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        got  = pd.read_csv('out.tsv',  delimiter='\t', index_col=0)
        exp  = data.loc[[5, 4, 3, 2, 1], ['5-0.0', '3-0.0', '1-0.0']]

        assert np.all(got == exp)



@patch_logging
def test_main_serial_parallel():

    with tempdir(), mock.patch('ukbparse.storage.COLUMNS_PER_FILE', 5):
        gen_test_data(50, 250, 'data.tsv')

        with open('variables.tsv', 'wt') as f:
            f.write('ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean\n')

        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        base = ' -lm -ow -vf variables.tsv out.tsv data.tsv'

        main.main(('-nj 0' + base).split())
        custom.clearRegistry()
        out0 = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        main.main(('-nj 1' + base).split())
        custom.clearRegistry()
        out1 = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        main.main(('-nj 2' + base).split())
        custom.clearRegistry()
        out2 = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        main.main(('-nj 4' + base).split())
        custom.clearRegistry()
        out4 = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        main.main(('-nj 8' + base).split())
        custom.clearRegistry()
        out8 = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        main.main(('-nj 16' + base).split())
        custom.clearRegistry()
        out16 = pd.read_csv('out.tsv', delimiter='\t', index_col=0)

        for got in [out0, out1, out2, out4, out8, out16]:
            assert np.all(np.isclose(got, data))


@patch_logging
def test_main_icd10():
    with tempdir():
        codings = tw.dedent("""
        coding\tmeaning\tnode_id\tparent_id
        a10\ta desc\t5\t0
        b20\tb desc\t1\t5
        c30\tc desc\t3\t5
        d40\td desc\t4\t3
        e50\te desc\t2\t1
        """).strip()

        data = tw.dedent("""
        eid,1-0.0
        1,a10
        2,b20
        3,c30
        4,d40
        5,e50
        """)

        exp = tw.dedent("""
        code\tvalue\tdescription\tparent_descs
        a10\t21\ta desc\t
        b20\t32\tb desc\t[a desc]
        c30\t43\tc desc\t[a desc]
        d40\t54\td desc\t[a desc] [c desc]
        e50\t65\te desc\t[a desc] [b desc]
        """).strip()

        with open('icd10.tsv', 'wt') as f: f.write(codings)
        with open('data.tsv',  'wt') as f: f.write(data)

        main.main('-cl 1 convertICD10Codes -if icd10.tsv '
                  '-imf icd10_mappings.tsv out.tsv data.tsv'
                  .split())

        with open('icd10_mappings.tsv', 'rt') as f:
            got = f.read().strip()

        assert exp == got


@patch_logging
def test_main_import_all():

    with tempdir():

        gen_test_data(10, 20, 'data.tsv')

        main.main('out.tsv data.tsv'.split())
        baseline = pd.read_csv('out.tsv', delimiter='\t', index_col=0)

        main.main('--import_all -ow out.tsv data.tsv'.split())
        passthru = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert np.all(baseline == passthru)

        main.main('-v 1:3 --import_all -ow out.tsv data.tsv'.split())
        dropvars = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = baseline.loc[:, ['1-0.0', '2-0.0', '3-0.0']]
        assert np.all(dropvars == exp)

        main.main('-v 3:-1:1 --import_all -ow out.tsv data.tsv'.split())
        ordered = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = baseline.loc[:, ['3-0.0', '2-0.0', '1-0.0']]
        assert np.all(ordered == exp)


        vartable = tw.dedent("""
        ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean
        3
        4
        5
        """).strip()

        with open('variables.tsv', 'wt') as f:
            f.write(vartable)

        main.main('-r -vf variables.tsv --import_all -ow out.tsv data.tsv'.split())
        ordered = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        exp = baseline.loc[:, ['3-0.0', '4-0.0', '5-0.0']]
        assert np.all(ordered == exp)


@patch_logging
def test_main_unknown_vars():

    vartable = tw.dedent("""
    ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean
    1
    2
    3
    4
    5
    """).strip()

    exp = tw.dedent("""
    name\tfile\tprocessed\texported
    6-0.0\tdata.tsv\t{}\t{}
    7-0.0\tdata.tsv\t{}\t{}
    8-0.0\tdata.tsv\t{}\t{}
    9-0.0\tdata.tsv\t{}\t{}
    10-0.0\tdata.tsv\t{}\t{}
    """).strip()

    def check(fname, *fmtargs):
        with open(fname, 'rt') as f:
            got = f.read().strip()

        print('got')
        print( got)
        print('exp')
        print( exp.format(*fmtargs))
        assert got == exp.format(*fmtargs)

    with tempdir():

        gen_test_data(10, 50, 'data.tsv')
        with open('variables.tsv', 'wt') as f:
            f.write(vartable)

        # don't use --import_all -
        # no file generated
        main.main('-ow '
                  '-vf variables.tsv '
                  '-uf unknowns.tsv '
                  'out.tsv data.tsv'.split())
        assert not op.exists('unknowns.tsv')

        main.main('-ow '
                  '-vf variables.tsv '
                  '-uf unknowns.tsv '
                  '--import_all '
                  'out.tsv data.tsv'.split())

        check('unknowns.tsv', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        os.remove('unknowns.tsv')

        # still generated if we use --remove_unknown
        main.main('-ow '
                  '-vf variables.tsv '
                  '-uf unknowns.tsv '
                  '--import_all '
                  '--remove_unknown '
                  'out.tsv data.tsv'.split())
        check('unknowns.tsv', 1, 0, 1, 0, 1, 0, 1, 0, 1, 0)
        os.remove('unknowns.tsv')

        # some unknowns exported, some dropped
        main.main('-ow '
                  '-vf variables.tsv '
                  '-uf unknowns.tsv '
                  '-v 3:7 '
                  '--import_all '
                  'out.tsv data.tsv'.split())
        check('unknowns.tsv', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0)
        os.remove('unknowns.tsv')

        # some unknowns
        # failed processing
        data = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        data.loc[1:45, '6-0.0'] = np.nan
        data.loc[5:,   '8-0.0'] = np.nan
        data.to_csv('data.tsv', sep='\t')
        main.main('-ow -n -n '
                  '-sp '
                  '-apr 6 removeIfSparse(minpres=20) '
                  '-apr 8 removeIfSparse(minpres=20) '
                  '-vf variables.tsv '
                  '-uf unknowns.tsv '
                  '--import_all '
                  'out.tsv data.tsv'.split())
        check('unknowns.tsv', 0, 0, 1, 1, 0, 0, 1, 1, 1, 1)
        os.remove('unknowns.tsv')


@patch_logging
def test_main_import_all_variable_removed():

    data = tw.dedent("""
    f.eid\t1-0.0\t2-0.0
    1\t5\t10
    2\t6\t
    3\t7\t
    4\t8\t
    5\t9\t
    6\t10\t
    7\t11\t
    8\t12\t
    9\t13\t
    10\t14\t
    """).strip()

    with tempdir():
        with open('data.tsv', 'wt') as f:
            f.write(data)

        main.main('-ia -v 1:2 -sp -apr all removeIfSparse(minpres=5) '
                  'out.tsv data.tsv'.split())

        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)
        assert np.all(got.index == np.arange(1, 11))
        assert got.columns == ['1-0.0']
        assert np.all(got['1-0.0'] == np.arange(5, 15))
