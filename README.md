[![Documentation Status](https://readthedocs.org/projects/rockphypy/badge/?version=latest)](http://rockphypy.readthedocs.io/en/latest/?badge=latest)[![PyPI version](https://badge.fury.io/py/rockphypy.svg)](https://badge.fury.io/py/rockphypy)[![Downloads](https://static.pepy.tech/badge/rockphypy)](https://pepy.tech/project/rockphypy)
---------


# [rockphypy](https://rockphypy.readthedocs.io/en/latest/)

# Release Note 

## Note: Issues with NumPy 2.0 Compatibility 

rockphypy relies on a dependency called ``KDEpy`` for generating KDE plots in the QI module. However, KDEpy uses the ``numpy.product`` function, which is deprecated in NumPy versions greater than 2.0. Consequently, if you have NumPy 2.0 or higher installed, importing rockphypy will result in an ImportError related to the KDEpy package.

Workarounds:

Downgrade NumPy: Install a NumPy version lower than 2.0.

Use a Fresh Virtual Environment: Set up a new virtual environment and ensure that the NumPy version is less than 2.0 before installing rockphypy.

We are actively working to remove the dependency on KDEpy, as only a single method in the QI module relies on it. 

*********************************

BUG Fixed In October. 

The latest version, rockphypy 0.0.2, has been released. The "cannot import module name" bugs have been fixed. Additionally, new models, such as the varying patchiness cement model (VPCM), have been implemented. Please reinstall the package to fix the bugs and enjoy more useful functionalities.



# About

This Python 3.8+ package implements most of the rock physics models introduced in the Rock Physics Handbook. The package provides a bunch of usefel classes, i.e. ``Anisotropy``, ``AVO``, ``BW``, ``EM(Effective medium)``, ``Empirical``, ``Fluid``, ``GM(Granular Medium)``, ``Permeability``, ``QI`` and ``utils``. An exhaust list of methods in different classes are given in  the [API Documentation](https://rockphypy.readthedocs.io/en/latest/autoapi/index.html).

# Citation 

Want to cite rockphypy in your work? 

Bibtex: 

@article{YU2023101567, <br>
title = {rockphypy: An extensive Python library for rock physics modeling},<br>
journal = {SoftwareX},<br>
volume = {24},<br>
pages = {101567},<br>
year = {2023},<br>
issn = {2352-7110},<br>
doi = {https://doi.org/10.1016/j.softx.2023.101567},<br>
url = {https://www.sciencedirect.com/science/article/pii/S2352711023002637},<br>
author = {Jiaxin Yu and Tapan Mukerji and Per Avseth}}


## Installation

rockphypy is available through [PyPI] and may be installed using `pip`:

```text
pip install rockphypy
```


## Example code and documentation

Below is an simple example showing the comparison between critical porosity model and elastic bounds computed by  Hashin-Strikmann bounds. See the [documentation](https://rockphypy.readthedocs.io/en/latest/) for more examples.

```python
from rockphypy import EM
from rockphypy import Fluid

# specify model parameters
phi=np.linspace(0,1,100,endpoint=True) # solid volume fraction = 1-phi
K0, G0= 37,44 # moduli of grain material
Kw, Gw= 2.2,0 # moduli of water 
# VRH bounds
volumes= np.vstack((1-phi,phi)).T
M= np.array([K0,Kw])
K_v,K_r,K_h=EM.VRH(volumes,M)
# Hashin-Strikmann bound 
K_UHS,G_UHS= EM.HS(1-phi, K0, Kw,G0,Gw, bound='upper')
# Critical porosity model
phic=0.4 # Critical porosity
phi_=np.linspace(0.001,phic,100,endpoint=True) # solid volume fraction = 1-phi
K_dry, G_dry= EM.cripor(K0, G0, phi_, phic)# Compute dry-rock moduli
Ksat, Gsat = Fluid.Gassmann(K_dry,G_dry,K0,Kw,phi_)# saturate rock with water

# plot
plt.figure(figsize=(6,6))
plt.xlabel('Porosity')
plt.ylabel('Bulk modulus [GPa]')
plt.title('V, R, VRH, HS bounds')
plt.plot(phi, K_v,label='K Voigt')
plt.plot(phi, K_r,label='K Reuss = K HS-')
plt.plot(phi, K_h,label='K VRH')
plt.plot(phi, K_UHS,label='K HS+')
plt.plot(phi_, Ksat,label='K CriPor')
plt.legend(loc='best')
plt.grid(ls='--')
```

## Issues and contributing

### Issues

If you are having trouble using the package, please let me know by creating an [Issue on GitHub] and I'll get back to you.

### Contributing

Whatever your mathematical and Python background is, you are very welcome to contribute to rockphypy.
To contribute, fork the project, create a branch and submit and Pull Request.
Please follow these guidelines:

- Import as few external dependencies as possible.
- Use test driven development, have tests and docs for every method.
- Cite literature and implement recent methods.
- Unless it's a bottleneck computation, readability trumps speed.
- Employ object orientation, but resist the temptation to implement many methods -- stick to the basics.
- Follow PEP8.

### Timeline 

![2timeline](https://github.com/yujiaxin666/rockphypy/assets/45630390/5689968c-7683-41e4-864a-0dca791a38a0)

