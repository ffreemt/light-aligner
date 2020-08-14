# Light-Aligner ![build](https://github.com/ffreemt/light-aligner/workflows/build/badge.svg)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/light-aligner.svg)](https://badge.fury.io/py/light-aligner)

A light-weight aligner for dual-text (currently just English-Chinese) alignment based on similariy scores using word for word "translation"

## Features
* `Light-weigh`, low resources demand
* `Lightning` fast, well maybe not `lightning` fast but quite fast
* No internet required

## Special Dependencies
`light aligner` depends on polyglot that in turn depends on `libicu`

To install `libicu`
###### For Linux/OSX

E.g.
* Ubuntu: `sudo apt install libicu-dev`
* Centos: `yum install libicu`
* OSX: `brew install icu4c`

Then use `poetry` or `pip` to install ` PyICU pycld2 Morfessor`, e.g.
```
poetry add PyICU pycld2 Morfessor
```
or
```
pip install PyICU pycld2 Morfessor
```
###### For Windows

Download and install the `pyicu` and `pycld2` (possibly also `Morfessor`) whl packages for your OS/Python version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2 (possibly also Morfessor https://www.lfd.uci.edu/~gohlke/pythonlibs/)

### Installation
```pip install light-aligner```

or, clone the repo and install necessary packages using `pip`:
```
git clone git@github.com:ffreemt/light-aligner.git
cd light-aigner
pip install -r requirements.txt
```
or, clone the repo and install necessary packages using `poetry`
```
git clone git@github.com:ffreemt/light-aligner.git
cd light-aigner
poetry install -v
```

`light aligner` can be run in `Linux/OSX`. In fact, the build process in github (pertaining to that github workflow badge ![build](https://github.com/ffreemt/light-aligner/workflows/build/badge.svg)) is carried out in Linux.

### Usage

```
cd light-aligner
python -m light-aligner
```

You may wish to use powershell (e.g., right click the powershell script`run-python-m.ps1` and select `Run with Powershell`) or conemu or cmder for better visual terminal experience.

Join qq-group 316287378 if you have any questions. The group chat is normally in Chinese but can switch to English if so desired.
