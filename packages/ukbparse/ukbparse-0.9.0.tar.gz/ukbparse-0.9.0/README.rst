``ukbparse`` - the UK BioBank data parser
=========================================


.. image:: https://img.shields.io/pypi/v/ukbparse.svg
   :target: https://pypi.python.org/pypi/ukbparse/

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1997626.svg
   :target: https://doi.org/10.5281/zenodo.1997626

.. image:: https://git.fmrib.ox.ac.uk/fsl/ukbparse/badges/master/build.svg
   :target: https://git.fmrib.ox.ac.uk/fsl/ukbparse/commits/master/

.. image:: https://git.fmrib.ox.ac.uk/fsl/ukbparse/badges/master/coverage.svg
   :target: https://git.fmrib.ox.ac.uk/fsl/ukbparse/commits/master/


``ukbparse`` is a Python library for pre-processing of UK BioBank data.


Installation
------------


Install ``ukbparse`` via pip::

    pip install ukbparse


Usage
-----


Comprehensive documentation has not yet been written.


General usage is as follows::

  ukbparse [options] output.tsv input1.tsv input2.tsv


You can get information on all of the options by typing ``ukbparse --help``.


Options can be specified on the command line, and/or stored in a configuration
file. For example, the options in the following command line::

  ukbparse \
    --overwrite \
    --import_all \
    --log_file log.txt \
    --icd10_map_file icd_codes.tsv \
    --category 10 \
    --category 11 \
    output.tsv input1.tsv input2.tsv


Could be stored in a configuration file ``config.txt``::

  overwrite
  import_all
  log_file       log.txt
  icd10_map_file icd_codes.tsv
  category       10
  category       11

And then executed as follows::

  ukbparse -cfg config.txt output.tsv input1.tsv input2.tsv


Tests
-----

To run the test suite, you need to install some additional dependencies::

    pip install -r requirements-dev.txt


Then you can run the test suite using ``pytest``::

    pytest
