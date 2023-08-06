``ukbparse`` changelog
======================


0.13.0 (Thursday 20th Deember 2018)
-----------------------------------


Added
^^^^^


* New ``--index`` option, allowing the position of the index column in input
  files to be specified.
* The ``--variable``, ``--subject``, and ``--exclude`` options now accept
  comma-separated lists, in addition to IDs, ID ranges, and text files.


Fixed
^^^^^


* Memory usage estimates in log messages were wrong under Linux.


0.12.3 (Tuesday 18th December 2018
----------------------------------


Changed
^^^^^^^


* Changes to new :func:`.fileinfo.has_header` function to improve robustness.


0.12.2 (Monday 17th December 2018)
----------------------------------


Changed
^^^^^^^


* Now using a custom implementation of ``csv.Sniffer.has_header``, as the
  standard library version does not handle some scenarios.


0.12.1 (Saturday 15th December 2018)
------------------------------------


Added
^^^^^


* Added some instructions for generating your own variable and data coding
  tables to the README.


Changed
^^^^^^^


* The ``ukbparse_demo`` script ensures that the Jupyter ``bash_kernel`` is
  installed.
* The ``ukbparse_compare_tables``, ``ukbparse_htmlparse`` and
  ``ukbparse_join`` scripts print some help documentation when called without
  any arguments.
* Added ``lxml`` as a dependency (required by ``beautifulsoup4``).


0.12.0 (Tuesday 11th December 2018)
-----------------------------------


Added
^^^^^


* The ``join``, ``compare_tables``, and ``htmlparse`` scripts are now
  installed as entry points called ``ukbparse_join``,
  ``ukbparse_compare_tables``, and ``ukbparse_htmlparse``.
* Jupyter notebook, demonstrating most of the features in ``ukbparse``, at
  ``ukbparse/demo/ukbparse_demonstration.ipynb``. You can run the demo via the
  ``ukbparse_demo`` entry point.


Changed
^^^^^^^


* Moved the ``scripts/`` directory into the ``ukbparse/`` directory.
* Improved string representation of process functions.


Fixed
^^^^^


* Fix to configuration file parsing code - ``shlex.split`` is now used instead
  of ``str.split``.
* Fixed mixed data type issues when merging the data coding and type tables into
  the variable table.


0.11.3 (Monday 10th December 2018)
----------------------------------


Changed
^^^^^^^


* Made the ``vid``, ``visit``, and ``instance`` parameters to the
  :class:`.Column` class optional, to make life easier for custom sniffer
  functions.


0.11.2 (Monday 10th December 2018)
----------------------------------


Fixed
^^^^^


* Fixed a bug in the handling of new variable IDs returned by processing
  functions.



0.11.1 (Monday 10th December 2018)
----------------------------------


Fixed
^^^^^


* Fixed a bug in the :func:`.removeIfSparse` processing function.


0.11.0 (Monday 10th December 2018)
----------------------------------


Added
^^^^^


* New ``--no_builtins`` option, which causes the built-in variable, data
  coding, type, and category table files to be bypassed.
* New :meth:`.PluginRegistry.get` function for getting a reference to a plugin
  function.
* Cleaning/processing functions are listed in command-line help.


0.10.5 (Saturday 8th December 2018)
-----------------------------------


Changed
^^^^^^^


* The ``minpres`` option to the :func:`.removeIfSparse` processing function
  is ignored if it is specified as an absolute value, and the data set length
  is less than it.


0.10.4 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* Fixed an issue with the `--subject` command line option.


0.10.3 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* Made use of the standard library ``resource`` module conditional, as it is
  not present on Windows.


0.10.2 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* Removed relative imports from test modules.


0.10.1 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* The :mod:`ukbparse.plugins` package was missing an ``__init__.py``, and was
  not being included in PyPI packages.


0.10.0 (Thursday 6th December 2018)
-----------------------------------


Added
^^^^^


* New ``--na_values``, ``--recoding``, and ``--child_values`` command-line
  options for specifying/overriding NA insertion, categorical recodings,
  and child variable value replacement.
* ``--dry_run`` mode now prints information about columns that would not be
  loaded.


Fixed
^^^^^


* Fixed a bug in the :func:`.calculateExpressionEvaluationOrder` function.


0.9.0 (Thursday 6th December 2018)
----------------------------------


Added
^^^^^


* Infrastructure for automatic deployment to PyPI and Zenodo.


Changed
^^^^^^^


* Improved ``--dry_run`` output formatting.


0.8.0
-----


Added
^^^^^


* New ``--dry_run`` command-line option, which prints a summary of the cleaning
  and processing that would take place.


0.7.1
-----


Fixed
^^^^^


* Fixed a bug in the :func:`.icd10.saveCodes` function.


0.7.0
-----


Changed
^^^^^^^


* Small refactorings in :mod:`ukbparse.config` so that command line arguments
  can be logged easily.


0.6.3
-----


Changed
^^^^^^^


* Minor updates to avoid deprecation warnings.


0.6.2
-----


Fixed
^^^^^


* Fixed a bug with the ``--import_all`` option, where an error would be thrown
  if a specifically requested variable was removed during processing.


0.6.1
-----


Changed
^^^^^^^


* Changed default processing for variables 41202/41204 so they are binarised
  *within* visit.


0.6.0
-----


Added
^^^^^


* New ``--import_all`` and ``--unknown_vars_file`` options for outputting
  information about previously unknown variables/columns.


Changed
^^^^^^^


* Changed processing function return value interface - see the
  :mod:`.processing_functions` module for details.


0.5.0
-----


Added
^^^^^


* Ability to export a mapping file containing the numeric values that ICD10
  codes have been converted into - see the ``--icd10_map_file`` argument.


Changed
^^^^^^^


* Changes to default processing - all ICD10 variables are binarised by default.
  Sparsity/redundancy tests happen at the end, so that columns generated by
  previous steps are tested.


Fixed
^^^^^


* :meth:`.HDFStoreCollection.loc` method returns a ``pandas.DataFrame`` when
  a list of columns are indexed, and a ``pandas.Series`` when a single column
  is indexed.


0.4.1
-----


Changed
^^^^^^^


* Updates to variable table for UKBiobank spirometry variables.


0.4.0
-----


Added
^^^^^


* New :func:`.parseSpirometryData` function for parsing spirometry data
  (i.e. `UKBiobank variable 3066
  <https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=3066>`_


Removed
^^^^^^^


* Removed the ``--disable_rename`` command line option, because having the
  columns renamed is really annoying.


0.3.3
-----


Changed
^^^^^^^


* Reverted the behaviour of :func:`.isSparse`.


0.3.2
-----


Changed
^^^^^^^


* Changed the behaviour of :func:`.isSparse` so that series which are *greater
  than* the ``minpres`` threshold pass, rather than *greater than or equal
  to*.


0.3.1
-----


Changed
^^^^^^^


* The :func:`.isSparse` function ignores the ``minpres`` argument if it
  is larger than the number of samples in the data set.


Fixed
^^^^^


* The :func:`.binariseCategorical` function now works on data with missing
  values.


0.3.0
-----


Added
^^^^^


* New :meth:`.DataTable.addColumns` method, so processing functions can
  now add new columns.
* New :func:`.binariseCategorical` processing function, which expands a
  categorical column into multiple binary columns, one for each unique
  value in the data.
* New :func:`.expandCompound` processing function, which expands a
  compound column into columns, one for each value in the compound data.
* Keyword arguments can now be used when specifying processing.


Fixed
^^^^^


* Fixed handling of non-numeric categorical variables


0.2.0
-----


Added
^^^^^

* Added a changelog file


Changed
^^^^^^^


* Updated variable/datacoding files to bring them in line with the latest
  Biobank data release.
