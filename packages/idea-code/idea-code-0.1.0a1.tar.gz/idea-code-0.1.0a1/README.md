[![Build Status](https://travis-ci.org/godby-group/idea-public.svg?branch=master)](https://travis-ci.org/godby-group/idea-public) [![Docs status](https://readthedocs.org/projects/idea-code/badge)](http://idea-code.readthedocs.io/)

# iDEA

The [interacting Dynamic Electrons Approach (iDEA)](https://www-users.york.ac.uk/~rwg3/idea.html)
 is a Python-Cython software suite developed in 
[Rex Godby's group](http://www-users.york.ac.uk/~rwg3/) at the University of
York since 2010. It has a central role in a number of research projects related
to many-particle quantum mechanics for electrons in matter.

iDEA's main features are:

* Exact solution of the many-particle time-independent Schrödinger equation,
  including exact exchange and correlation
* Exact solution of the many-particle time-dependent Schrödinger equation,
  including exact exchange and correlation
* Simplicity achieved using spinless electrons in one dimension
* An arbitrary external potential that may be time-dependent
* Optimisation methods to determine the exact DFT/TDDFT Kohn-Sham potential
  and energy components
* Implementation of various approximate functionals (established and novel) for
  comparison

A list of publications based on the iDEA code so far is available on [the iDEA code's home page](https://www-users.york.ac.uk/~rwg3/idea.html).

## How to get iDEA

The quickest way to try out iDEA are the
[iDEA demos](https://github.com/godby-group/idea-demos), which allow to run iDEA directly in the browser
using live jupyter notebooks.

In order to install iDEA locally, type:

```bash
pip install --user idea-code
```

For development, get the latest version from the git repository:

```bash
git clone https://github.com/godby-group/idea-public.git
cd idea-public
pip install --user -e .[doc] --no-build-isolation
idea-run
```

## Documentation

The [iDEA documentation](https://idea-code.readthedocs.io/en/latest/) 
explains the inner workings and theory behind iDEA, and includes pointers on
[how to contribute](https://idea-code.readthedocs.io/en/latest/dev/add.html) to the development of iDEA.

## Citing iDEA

If you use iDEA, we would appreciate a reference to the iDEA code's home page, [https://www-users.york.ac.uk/~rwg3/idea.html](https://www-users.york.ac.uk/~rwg3/idea.html), and to one relevant publication from our group. You might consider:

* For exact solution of the many-particle Schrödinger equation and reverse engineering of the exact DFT/TDDFT Kohn-Sham potential: [M.J.P. Hodgson, J.D. Ramsden, J.B.J. Chapman, P. Lillystone, and R.W. Godby, Physical Review B (Rapid Communications) **88** 241102(R) (2013)](http://www-users.york.ac.uk/~rwg3/abst_81-110.html#Paper_87)
* For Hartree-Fock and hybrid calculations: [A.R. Elmaslmane, J. Wetherell, M.J.P. Hodgson, K.P. McKenna and R.W. Godby, Physical Review Materials **2** 040801(R) (Rapid Communications) (2018)](http://www-users.york.ac.uk/~rwg3/abst_81-110.html#Paper_97)
* For the iDEA code's local-density approximations from finite systems: [M.T. Entwistle, M.J.P. Hodgson, J. Wetherell, B. Longstaff, J.D. Ramsden and R.W. Godby, Physical Review B **94** 205134 (2016)](http://www-users.york.ac.uk/~rwg3/abst_81-110.html#Paper_92)
* For the iDEA code's local-density approximation from the 1D homogeneous electron gas: [M.T. Entwistle, M. Casula and R.W. Godby, Physical Review B **97** 235143 (2018)](http://www-users.york.ac.uk/~rwg3/abst_81-110.html#Paper_98)

## License

The iDEA code is released under the [MIT license](MIT)
