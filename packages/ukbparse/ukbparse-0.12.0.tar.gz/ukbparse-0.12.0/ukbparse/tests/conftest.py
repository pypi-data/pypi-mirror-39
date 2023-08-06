#!/usr/bin/env python
#
# conftest.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import warnings
import pandas

import ukbparse.fileinfo as fileinfo
import ukbparse.icd10    as icd10


warnings.filterwarnings(module='pandas',
                        category=pandas.errors.ParserWarning,
                        action='ignore')


def fake_cache_clear():
    pass


fileinfo.sniff            = fileinfo.sniff           .__wrapped__
fileinfo.fileinfo         = fileinfo.fileinfo        .__wrapped__
icd10.readICD10CodingFile = icd10.readICD10CodingFile.__wrapped__

fileinfo.sniff           .cache_clear = fake_cache_clear
fileinfo.fileinfo        .cache_clear = fake_cache_clear
icd10.readICD10CodingFile.cache_clear = fake_cache_clear
