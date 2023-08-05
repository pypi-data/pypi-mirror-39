[![Build Status](https://travis-ci.org/moritzploss/tribology.png)](https://travis-ci.org/moritzploss/tribology)
[![DOI](https://zenodo.org/badge/110825481.svg)](https://zenodo.org/badge/latestdoi/110825481)


# tribology
This Python 3 package is a collection of functions for
tribology research and education, including contact mechanics,
lubrication science, data handling and data processing. It provides 
implementations of analytical and numerical calculation routines together with 
frequently used constants.

The **tribology package** is hosted on GitHub:

    https://github.com/moritzploss/tribology

You can **install** the package from the
**<a href="https://pypi.python.org/pypi/tribology" target="_blank">PyPI</a>**
index using pip:

    pip install tribology

After installation, it is recommended to **import** the package and all
its modules as follows:

```python
import tribology as tr
```

The package
**<a href="https://moritzploss.github.io/tribology" target="_blank">
documenation</a>** is provided through GitHub Pages; the Sphinx source files
can be found in the [`/docs`](./docs) directory. Simple examples of how to use 
the package are provided in the [`/examples`](./examples) directory.

The package is provided under an MIT license. See the 
[`LICENSE.txt`](LICENSE.txt) file for more information.


# known issues
Some older versions of the package (0.4 <= version < 0.5) may raise the 
following error when imported:

    ModuleNotFoundError: No module named 'cv2'

This is caused by a missing `install_requires` argument in
[`setup.py`](./setup.py). To fix this, either update to a later version of the
package, or install the missing `cv2` package manually:

    pip install opencv-python


# use in scientific publications

You can refer to the tribology package in **scientific publications** by
using its DOI. The following DOI will resolve all releases of the
package and automatically point to the latest release. A more detailed
overview of the DOI release history can be found through
**<a href="https://doi.org/10.5281/zenodo.1117727" target="_blank">Zenodo</a>**:

    DOI:  10.5281/zenodo.1117727

Please refer to the list of contributors below and use the following format to 
cite the package:

    [List of contributors] et al., Tribology -- A Python Package for Tribology 
    Research and Education, version v[x.x.x] ([date]). doi: [DOI] 


List of contributors:

- **Moritz Ploss**, KTH Royal Institute of Technology, Stockholm, Sweden


# version history

Neutral builds are continuously deployed to PyPI. The log for
neutral builds includes changes with respect to the latest numbered
release listed below.

#### 0.5.10
- function `merge_npz` restored to earlier implementation; use more
  advanced data structures to merge databases where values are not numeric or
  not all databases contain the same set of keys

#### 0.5.9
- function `split_del` now has additional argument `force` to overwrite existing
  output files

#### 0.5.8
- bug fixes

#### 0.5.7
- function `split_del` added to module `data_import`

#### 0.5.6
- fixed a bug that lead function `approx_hertz_rad` to return radius `nan` 
  rather than `inf` for a straight line profile. added corresponding test
  case.

#### 0.5.5
- function `approx_hertz_rad` now returns additional parameters
- function `abbottfirestone` moved to module `rough_surfaces`
- function `import_del` and `import_dir` now have an additional argument 
  `colheadlines` for files where the column headers span multiple rows

#### 0.5.4
- function `approx_hertz_rad` improved (more accurate circle approximation) 

#### 0.5.3
- function `phertz` now has additional argument to indicate if mean or maximum
  pressure should be returned
- clarified that Hertz equations are only valid for elliptical and circular
  contacts; equations for line contacts are not implemented at the moment
- added additional test cases for Hertz equations

#### 0.5.2
- fixed bug in Hertz pressure calculation that may lead to wrong results for
  elliptical contacts if one of the contact bodies is completely flat

#### 0.5.1
- refactoring

#### 0.5.0
- module `rough_surfaces` added

##

#### 0.4.9
- fixed bug that lead to data import error when using `mat` output format


#### 0.4.7
- added missing package dependencies that may lead to an import error when using
  data import or slim mapper processing functions


#### 0.4.5
- functions `slim2thick` and `slim2thick_batch` now return color error values
  for each image 

#### 0.4.4
- function `merge_npz` added to `data_import` module

#### 0.4.3
- function `slim2thick_batch` now also returns mean thickness data for the SLIM
  mapper ZERO step

#### 0.4.2
- providing an output file name to the `merge_del` function is now optional 

#### 0.4.1
- function `merge_del` added to `data_import` module

#### 0.4.0
- module `process_slim_mapper` added. the module contains functions for 
  automated processing of SLIM mapper bitmap images as obtained from test rigs 
  by PCS Instruments.
- fixed a bug that lead to a `permission denied` error using the `import_del`
  function (and related functions) if the imported file is in the current working
  directory and the function is called within a program that runs in an IDE.
- docs theme changed to guzzle sphinx due to unresolvable compile problem with 
  rtd
- README updated

##

#### 0.3.4
- README updated
- when importing PCS files using the `import_dir` or `import_del` method of the
  `data_import` module, steps without numeric data (mapper steps, film zero 
  steps, ...) are now reflected in the `step_start` and `step_end` variables
  that are saved to the output file. 
- refactoring


#### 0.3.0
- `p3can` source code now fully merged with tribology package

##

#### 0.2.94

- module `roller_bearings` added
- function `fcylrolbear` added to module `roller_bearings`
- function `kinaxthrustrolbear` added to module `roller_bearings`
- added function `approx_hertz_rad` to module `hertz`
- merged <a href="https://github.com/moritzploss/p3can" target="_blank">
P3CAN project</a> with tribology package. The tribology package now has
a module `p3can` that allows users to run P3CAN simulation runs. The
final aim is to split the P3CAN code into standalone functions and
integrate them with the tribology package.
- refactoring


#### 0.2.58

- DOI now indexed through Zenodo
- method `walther` now supports `ndarray` arguments
- method `profrolleriso` added to `tribology` module
- no longer compatible with Python 3.4 and lower
- the `data_import` module now provides functions to import output files
from PCS Instruments test rigs.
- module `data_import` added. the module contains functions for data
import from delimited data files into Numpy and Matlab database format.
- modules renamed, removed leading `tribology_` in module names
- auto-release on PyPI through Travis CI
- refactoring


#### 0.2.2

- html documentation now with multi-page structure
- docstrings changed to numpy format and refactored
- functions `eeff` and `reff` moved to `tribology_hertz` module
- function `eeff` renamed to `reff`
- function `meff` renamed to `eeff`
- helper functions made private


#### 0.2.1
- Sphinx documentation added to GitHub repo, docs available at
https://moritzploss.github.io/tribology
-  Travis CI builds now with Pylint error check for package files.
Non-package files are not checked. Build fails if Pylint error is found.
- Python 3.4 and 3.5 builds added to Travis CI (now 3.4, 3.5 and 3.6)
- change log added to `README.md`
- various functions renamed
- helper functions made private
- classifiers added to `setup.py`
- demo for boundary element functions added (`demo_ball_on_plate.py`)
- refactoring

#### 0.2.0
first release on PyPI
