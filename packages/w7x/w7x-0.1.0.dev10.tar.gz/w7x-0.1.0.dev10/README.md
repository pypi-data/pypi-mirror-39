# Project description
The w7x package provides convenience methods for Magnetic Field evaluations around the stellarator Wendelstein 7-X.
The zen of the package (in addition to the zen of python) is the following:
* be intuitive
* Tell the user what he does wrong (the web services often fail without a clue for the user).
* Provide proper defaults for your functions.

The module includes handy wrapper methods for the following web-services:
* FieldLineTracing (see "http://webservices.ipp-hgw.mpg.de/docs/fieldlinetracer.html"). Namespace: w7x.flt
* VMEC (see "http://webservices.ipp-hgw.mpg.de/docs/vmec.html"). Namespace: w7x.vmec
* EXTENDER (see "http://webservices.ipp-hgw.mpg.de/docs/extender.html"). Namespace: w7x.extender

The package provides explicit classes for the osa types of the web-services provided.
The main starting point for the use of services is the Run() class e.g.
```python
import w7x
run = w7x.flt.Run()
lcfs_points = run.find_lcfs()  # returns one point on the lcfs
```
Most services are started from this class.

We utilize the tfields module in order to take care of proper coordinate transformations since some web-service tools need special coordinate systems.

# Examples
Look into [examples](https://gitlab.mpcdf.mpg.de/dboe/w7x/tree/master/examples) for running examples.

# Installation
## Requirements
* python versions >=2.7 or >=3.0
* For the use of the field line server and vmec server, access to the web services from within the IPP infrastructure are required.
## PYPI
From user side, we recommend the installation via pypi: 
```bash
pip install w7x
```

### Note:
If you want to use the divertor or baffle evaluator (for example see [diffusion mapping example](https://gitlab.mpcdf.mpg.de/dboe/w7x/tree/master/examples/diffusion_mapping.py)), \ie build an evaluator object like so:
```python
divertor_evaluator = w7x.evaluation.TracerEvaluator.from_loader(
    w7x.Defaults.Paths.divertor_upper_tiles_template_path)
```,
a known problem is, that the data used for loading can not be loaded by pickle in python>=3.0.
In this case, the functionality is yet only supported for python2.7.
Furthermore, the files can not be delivered by pypi. Thus you have to clone the project and set the $PYTHONPATH accordingly (see GIT section below).

## GIT
If you want to keep on track very tightly to the project and or want to support development, clone the git to your <favourite_directory> and set the $PYTHONPATH variable.
```bash
cd favourite_directory
git clone https://gitlab.mpcdf.mpg.de/dboe/w7x.git  # clone the repository
git submodule update --init --recursive  # also clone all submodules
echo 'export PYTHONPATH=$PYTHONPATH:</path/to/my/facvourite_directory/w7x>' >> ~/.bashrc  # permanently set the $PYTHONPATH variable
source ~/.bashrc # make the PYTHONPATH change active
```

# Testing:
Tests are implemented via doctests.
To run the doctests in a submodule, run the submodule file directly like:
```bash
python w7x/flt.py
```
in order to run the doctests of the flt submodule.

If you have cloned the git version of w7x, you can do all tests at once:
In the w7x directory, run
```bash
python w7x test
```
or 
```bash
make test
```

# Developers only:
Clone this project with git
To set up the shared git hooks, run
```bash
make init
```

To check the coverage, we prefere the 'coverage' tool
Use it in the w7x directory like so:
```bash
coverage run w7x test
```
or 
```bash
make coverage
```

To publish on pypi, run
```bash
make publish
```
