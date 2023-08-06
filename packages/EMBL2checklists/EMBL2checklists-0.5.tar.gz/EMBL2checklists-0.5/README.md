*EMBL2checklists*
=================

[![Build Status](https://ci.appveyor.com/api/projects/status/github/michaelgruenstaeudl/EMBL2checklists?branch=master&svg=true)](https://ci.appveyor.com/api/projects/status/github/michaelgruenstaeudl/EMBL2checklists)
[![Build Status](https://travis-ci.com/michaelgruenstaeudl/EMBL2checklists.svg?branch=master)](https://travis-ci.com/michaelgruenstaeudl/EMBL2checklists)
[![PyPI status](https://img.shields.io/pypi/status/EMBL2checklists.svg)](https://pypi.python.org/pypi/EMBL2checklists/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/EMBL2checklists.svg)](https://pypi.python.org/pypi/EMBL2checklists/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/EMBL2checklists.svg)](https://pypi.python.org/pypi/EMBL2checklists/)
[![PyPI license](https://img.shields.io/pypi/l/EMBL2checklists.svg)](https://pypi.python.org/pypi/EMBL2checklists/)

EMBL2checklists converts EMBL- or GenBank-formatted flatfiles to submission checklists (i.e., tab-separated spreadsheets) for submission to [ENA](http://www.ebi.ac.uk/ena) via the interactive [Webin submission system](https://www.ebi.ac.uk/ena/submit/sra/#home).


<!---

## FEATURES
* Foo
* Bar
* Baz

-->


## INPUT, OUTPUT AND PREREQUISITES
* **Input**: EMBL- or GenBank-formatted flatfile
* **Output**: tab-separated spreadsheet ("checklist")
* **Prerequisites**: Input flatfiles must have the DNA marker name (e.g., "matK", "ITS") as qualifier value for any of the defined key_features ("gene", "note", "product" or "standard_name").


## EXAMPLE USAGE

### On Linux / MacOS

#### Commandline Interface
```
$ EMBL2checklists_CLI \
    -i example/example_trnKmatK.embl \
    -o example/example_trnKmatK.tsv \
    -c trnK_matK \
    -e no
```
#### GUI Interface
```
$ EMBL2checklists_GUI
```

### On Windows

#### GUI Interface
Simply double-click the file `EMBL2checklist_GUI.exe` as generated during the installation (see below).


![](images/EMBL2checklist_GUI.png)


## INSTALLATION
First, please be sure to have [Python 2.7 installed](https://www.python.org/downloads/) on your system. Then:

To get the most recent stable version of *EMBL2checklists*, run:

    $ pip2 install EMBL2checklists

Or, alternatively, if you want to get the latest development version of *EMBL2checklists*, run:

    $ pip install git+https://github.com/michaelgruenstaeudl/EMBL2checklists.git


<!---

## CITATION
Using EMBL2checklists in your research? Please cite it!

- Gruenstaeudl M., Hartmaring Y. (2018). paper_title_here. journal_title_here. https://doi.org/doi_address_here

```
@article{GruenstaeudlHartmaring2018,
  doi = {...},
  url = {...},
  year  = {2018},
  publisher = {...},
  author = {Michael Gruenstaeudl, Yannick Hartmaring},
  title = {...},
  journal = {...}
}
```

-->


## CHANGELOG
See [`CHANGELOG.md`](CHANGELOG.md) for a list of recent changes to the software.
