## Welcome to fempy!
Fempy is a pure python cross platform package for solving systems of PDEs by finite element method. It provides abstractions for dealing with discretized domains, fields on these domains, weak forms constructed with the fields and for solving the resulting systems of equations. Linear, non linear and time dependent problems can be solved with fempy.

## Installation
Best way to install fempy is by using `pip`:
```
pip install -U fempy
```
The only dependencies required are numpy and scipy. However for automatic meshing and preview of results you will need also [gmsh](https://gmsh.info/) executable in your path. You may choose to install it with `pip` as well:
```
pip install -U gmsh-sdk
```

## Testing
Run all tests by:
```
python -m fempy.tests.runtests
```
You can also specify subpackages, e.g:
```
python -m fempy.tests.runtests domain
```
Examples can be executed similarely as:
```
python -m fempy.examples.elastic
```
Note, that most examples need gmsh and a running display.

