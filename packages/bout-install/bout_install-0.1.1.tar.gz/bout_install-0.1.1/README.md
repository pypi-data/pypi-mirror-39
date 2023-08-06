[![Build Status](https://travis-ci.org/CELMA-project/bout_install.svg?branch=master)](https://travis-ci.org/CELMA-project/bout_install)
[![codecov](https://codecov.io/gh/CELMA-project/bout_install/branch/master/graph/badge.svg)](https://codecov.io/gh/CELMA-project/bout_install)
[![pypi package](https://badge.fury.io/py/bout-install.svg)](https://pypi.org/project/bout-install/)
[![Python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
[![PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License](https://img.shields.io/badge/license-LGPL--3.0-blue.svg)](https://github.com/CELMA-project/bout_install/blob/master/LICENSE)

# bout_install

Python package to install [BOUT++](http://boutproject.github.io) and its 
dependencies.

> **NOTE**: This package is meant as a "last resort" to install BOUT++, for 
example when you are not a `root` user, and you are trying to install on a 
"tricky" system.
Otherwise 
BOUT++ can easily be installed using 
[docker](https://bout-dev.readthedocs.io/en/latest/user_docs/installing.html#docker-image)
or installed as explained in the BOUT ++ [documentation](https://bout-dev.readthedocs.io/en/latest/user_docs/installing.html#installing-dependencies)
.

## Getting Started

`bout_install` is a lightweight package, and requires only `python3`, 
`requests` and an internet connection to run. 

Building `BOUT++` and dependencies can be done by executing

```python
from bout_install import install_bout
install_bout(config_path=None, add_to_bashrc=False)
```

or from command-line

```bash
bout_install --help
```

which returns

```
usage: bout_install [-h] [-c CONFIG] [-a]

Install BOUT++ with dependencies

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the configuration file. Default is
                        /path/to/bout_install/bout_install/config.ini
  -a, --add_to_bashrc   If set, paths to binaries and libraries of
                        dependencies will be added to .bashrc. Default is
                        false
```

This will build BOUT++ and its dependencies according to the content of 
[`config.ini`](bout_install/config.ini):

```ini
[bout_options]
# Let these be empty for default behavior
# Read docstring of InstallerUsingGit.InstallerUsingGit.__init__ for details
# NOTE: Commit 8567b2d5bb5f4b70face0b8d0849fc1bbafbbdb0 is known to work
git_dir =
checkout =
enable_checks = no
enable_optimize = 3

[install_options]
# If packages not residing in local should be used
use_preinstalled = false
# Let these be empty for default behavior
# Read docstring of Installer.Installer.setup_install_dirs for details
main_dir =
install_dir =
local_dir =
examples_dir =

[required]
fftw = true
hdf5 = true
mpi = true
netcdf = true

[optional]
cmake = false
ffmpeg = false
gcc = false
slepc = true
sundials = true
# NOTE: PETSc is installed if slepc is true
petsc = false

[versions]
cmake = 3.7.2
ffmpeg = 3.1.4
fftw = 3.3.6-pl2
gcc = 6.1.0
hdf5 = 1.10.1
mpi = 3.2
nasm = 2.13.03
netcdf = 4.4.1.1
netcdf_cxx = 4.3.0
# NOTE: Only certain PETSc versions are supported by BOUT++
petsc = 3.10.0
# NOTE: Sundials 2.7.0 have given openmp problems
sundials = 2.6.2
# NOTE: Must correspond to the PETSc version
slepc = 3.10.0
yasm = 1.3.0
x264 = x264-snapshot-20180709-2245-stable
```

### Installing from pip

The package can be installed from `pip`:

```bash
pip install bout-install
```

### Installing from source

Alternatively it can be installed from source

```bash
python setup.py install
```

## Running the tests

The test suite can be executed through `pytest` or through `codecov pytest-cov`.
Installation through

```bash
pip install pytest
```

or

```bash
pip install codecov pytest-cov
```

and run with

```bash
pytest
```

or
 
```bash
pytest --cov=./
```

respectively

> **NOTE:** Due to time constraints of automatic testing with Travis, the 
unittests have been "blinded" by adding a "." in front of the name. In this 
way `pytest` will ignore those test. "Un-blind" them by removing the leading "
." in order to run them. 

## License

This project is licensed under the GNU Lesser General Public License - see the 
[LICENSE](LICENSE) file for details

## Acknowledgments

* The [BOUT++ team](http://boutproject.github.io/about/) for fast and 
accurate response on the 
[issue tracker](https://github.com/boutproject/BOUT-dev/issues) and 
[slack-channel](http://boutproject.github.io/documentation/)
