"""
Hertz-Mindlin and reduced shear factor
=======================================

"""


# %%


import numpy as np 
import matplotlib.pyplot as plt
plt.rcParams['font.size']=14
plt.rcParams['font.family']='arial'


# %% 

import rockphypy # import the module for rock physics
from rockphypy import GM # import the "effective medium" GM module 


# %%
# Hertz-Mindlin thoery
# ~~~~~~~~~~~~~~~~~~~~~~~
# Hertz estimated the effective bulk modulus of a *dry, random distributed, identical-sphere pack* as:
# 
# .. math::
#       K_{eff}= \left [ \frac{C^2(1-\phi)^2 G^2}{18\pi^2 (1-\nu ^2)}P   \right ]^{1/3} 
# 
# 
# Mindlin (1949) showed that if the spheres are first pressed together, and a tangential force is applied afterward, slip may occur at the edges of the contact. The normal stiffness is the same as in the Hertz solution, while the effective shear modulus of a dry, random distributed, identical-sphere pack given by Mindlin is: 
# 
# .. math::
#       G_{eff}=\frac{5-4\nu }{5(2-\nu )} \left [ \frac{3C^2(1-\phi)^2 G^2}{2\pi^2 (1-\nu ^2)}P   \right ]^{1/3}
# 
# 
# :math:`C` is the coordination number being the average number of contacts per particle. :math:`P` is the hydrostatic confining pressure, :math:`G` and :math:`\nu` are the shear modulus and Poisson' ratio of grain material, respectively. 
#
# Reduced shear factor
# ~~~~~~~~~~~~~~~~~~~~
# There are experimental data show that bulk modulus of unconsolidated sand can be well predicted using Hertz Mindlin model, but the predicted shear modulus don't match the lab data. Walton's model is limited to no-slip and slip grain packs, in order to account for the fact that the friction between grains may in the state between no-slip and slip limits, Duffaut et al.(2010) are given as an average of the no-slip and slip contacts. A methodology that gives the same result is the binary mixing factor described in Bachrach and Avseth (2008). The factor from Bachrach and Avseth (2008) treats the grain assembly as a mixture of no-slip and slip contacts, instead of having all contacts at an intermediary state. As a result, the effective bulk modulus of the pack remains the same, but the expression for the effective shear modulus becomes 
# 
# .. math::
#       G_{\mathrm{eff}}=\frac{2+3 f-v(1+3 f)}{5(2-v)}\left[\frac{3 C^{2}(1-\phi)^{2} \mu^{2}}{2 \pi^{2}(1-v)^{2}} P\right]^{1 / 3}
# 
#
# Examples
# ~~~~~~~~
# The effect of reduced shear factor on HM modelling
#

# %%

# specify model parameters
phic=0.4
Cn=8.6
sigma=np.linspace(0,20,100) # confining pressure 
K0, G0= 37,44
Kw, Gw= 2.2,0
# no slip and slip limit
_,G_rough= GM.hertzmindlin(K0, G0, phic, Cn, sigma, 0)
_,G_smooth= GM.hertzmindlin(K0, G0, phic, Cn, sigma, 1)


# %%


# plot
plt.figure(figsize=(6,6))
plt.xlabel('Confining pressure (MPa)')
plt.ylabel('Shear modulus [GPa]')
plt.plot(sigma, G_rough,'--k',lw=3,label='No Slip limit')
plt.plot(sigma, G_smooth,'--k',lw=3,label='Slip limit')
# HM modelling for a discrete set values of reduced shear factors
len=20
f= np.linspace(0,1,len)
colors = plt.cm.rainbow(np.linspace(0, 1, len))
for i, val in enumerate(f):
    _,G= GM.hertzmindlin(K0, G0, phic, Cn, sigma, val)
    plt.plot(sigma, G, color=colors[i])
plt.legend(loc='best')

# %%
# Walton's theory
# ~~~~~~~~~~~~~~
# Mindlin assumes a partial slip in the contact area. In constrast, Walton assumes that normal and shear deformation of a two-grain combination occur simultaneously.  The slip occurs across the whole area once applied tractions exceed the friction resistance. Spheres maybe infinitely smooth (perfect slip) or infinitely rough (no slip). For the smooth-spheres dry pack: 
# 
# .. math::
#       G_{nofriction}=\frac{1}{10}  \left [ \frac{12C^2(1-\phi)^2 G^2}{\pi^2 (1-\nu ^2)}P   \right ]^{1/3}
# 
# 
# .. math::
#       K_{nofriction}=\frac{5}{3}G_{nofriction}
# 
# 
# The rough limit is the same as Hertz-Mindlin' theory. 
# 
#
# Noticed that the function ``GM.hertzmindlin`` and ``GM.walton`` yield exactly the same result as we include the reduced shear factor in both functions. But remember the difference between Hertz-Mindlin's approach and Walton' appraoch and their relations, as above decribed.
#

# %%


print('HM result:', GM.hertzmindlin(30,20,0.4,6,10,0.5))
print('Walton result:',GM.Walton(30,20,0.4,6,10,0.5))

# %%
# 
# Note that in many experiments on natural sands and artificial granular
# packs, the observed dependence of the elastic moduli on pressure is different
# from that given by the Hertz–Mindlin theory. This is because the grains are
# not perfect spheres, and the contacts have configurations different from
# those between perfectly spherical particles. Hertz–Mindlin theory also fails to incorporate the spatial heterogeneity of stress and strain within the random grain pack
#
# 
# **Reference**: 
#
# - Mavko, G., Mukerji, T. and Dvorkin, J., 2020. The rock physics handbook. Cambridge university press.
#
# - Bachrach, R. & Avseth, P. Rock physics modeling of unconsolidated sands: Accounting for nonuniform contacts and heterogeneous stress fields in the effective media approximation with applications to hydrocarbon exploration  Geophysics, Society of Exploration Geophysicists, 2008, 73, E197-E209
#
# - Duffaut, K.; Landrø, M. & Sollie, R. Using Mindlin theory to model friction-dependent shear modulus in granular media Geophysics, Society of Exploration Geophysicists, 2010, 75, E143-E152 
#
#
