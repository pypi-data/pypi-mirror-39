### snphwe: An exact test of Hardy-Weinberg Equilibrium
Reimplementation in Python of an exact SNP test of Hardy-Weinberg Equilibrium, as
described in Wigginton, JE, Cutler, DJ, and Abecasis, GR (2005) A Note on
Exact Tests of Hardy-Weinberg Equilibrium. AJHG 76: 887-893.

This package is just a python wrapper around their
[c implementation](http://csg.sph.umich.edu/abecasis/Exact/snp_hwe.c).

#### Installation
The simplest way to install snphwe is through pip:
```sh
pip install snphwe
```

#### Usage
Use snphwe within a python environment
```python
from snphwe import snphwe

hom1 = 10
hets = 500
hom2 = 5000
hwe_p = snphwe(hets, hom1, hom2)
```
