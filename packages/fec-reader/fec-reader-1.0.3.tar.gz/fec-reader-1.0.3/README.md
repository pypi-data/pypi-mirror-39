FEC Data Reader
==========================

A quick way to retrieve FEC bulk flat-file data from https://www.fec.gov:

This package is a demonstration of ETL skills for Alexus Wong. However, it is also important
that we as a society can efficiently consume the inordinate amount of information available
today. If we can process it, we can take steps in the right direction.

To use this package, instantiate a `DataReader` object with a target directory. As you call relevant methods,
the `DataReader` object will save flat-files to your chosen directory.

``` {.sourceCode .python}
>>> import fec_reader as fec
>>> reader = fec.DataReader(DATA_DIR='/raw') # pick a target directory
>>> reader.get_pac_summary()
```

Features
---------------

FEC Reader currently retrieves these data files:

-   PAC Summary - https://www.fec.gov/campaign-finance-data/pac-and-party-summary-file-description/ - 'get_pac_summary'
-   Candidate Master - https://www.fec.gov/campaign-finance-data/candidate-master-file-description/ - 'get_candidate_master'


Installation
------------

To install FEC Reader, simply use pip:

``` {.sourceCode .bash}
$ pip install fec-reader
```
