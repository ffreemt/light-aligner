# Light-Aligner ![build](https://github.com/ffreemt/light-aligner/workflows/build/badge.svg)
A light-weight aligner for dual-texts (currently just Enlgish-Chinese) based on similariy scores using word for word "translation"

## Features
* Fast
* Low resources demand
* No internet required

## Special Dependencies
Light-Aligner depends on polyglot that depends on `libicu`

To install `libicu`
###### For Linux/OSX

E.g.
* Ubuntu: `sudo apt install libicu-dev`
* Centos: `yum install libicu`
* OSX: `brew install icu4c`

###### For Windows

Download and install the `pyicu` and `pycld2` (possibly also `Morfessor`) whl packages for your OS/Python version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2 (possibly also Morfessor https://www.lfd.uci.edu/~gohlke/pythonlibs/)

### Installation
```pip install light-aligner```
