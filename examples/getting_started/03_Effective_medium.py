"""
Inclusion models
=================

"""



# %%

import numpy as np 
import matplotlib.pyplot as plt
plt.rcParams['font.size']=14
plt.rcParams['font.family']='arial'


# %%


# %% 

import rockphypy # import the module for rock physics
from rockphypy import EM # import the "effective medium" EM module 
# import the 'Fluid' module 
from rockphypy import Fluid



# %%
# Non-interacting inclusion model with spherical pores
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Basic elastic bounds such as Voigt, Reuss and Hashin-Strikmann bounds attempt to define limits of effective elastic moduli without assuming microgeometry of the composite. Inclusion based effective medium models, in contrast, attempt to give direct estimation of elastic moduli given matrix mineralogy, volume fractions and assumption on microgeometry. 
# 
# A simple inclusion model is the "Swiss cheese" model assuming a dilute distribution of spherical inclusions embedded in an **unbounded** homogenous solid.  It takes the "noninteracting assumption" in which all cavities (pores) are independent so that their contributions can be added. 
# 
# The Swiss cheese model is defined as :
# 
# .. math::
#       \frac{1}{K^{*}}=\frac{1}{K_{s}}\left[1+(1+\frac{3K_s}{4G_s} ) \phi\right]
# 
# 
# .. math::
#       \frac{1}{G^{*}}=\frac{1}{G_{s}}\left[1+\frac{15 K_{s}+20 G_{S}}{9 K_{S}+8 G_{S}} \phi\right]
# 
# 
# The function that performs the calculation is ``EM.Swiss_cheese``
#
#
# Self-Consistent(SC) model with spherical pores
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Rocks generally have their highest elastic moduli and seismic velocities in the limit of zero porosity, approaching the moduli of the mineral constituent. According to Nur's hypothesis, there is almost always a *critical porosity*, :math:`\phi_c` at which the rock loses it's coherence and falls apart. The noninteracting models are generally jusitified for very dilute concentration of inclusion and assumes no interaction between inclusions. The estimated average moduli are zero and the prediction fails when the void volume fraction reaches to 0.5. If we want to include the interaction effects to a certain extent and also incorpate the critical porosity behavior, Self-consistent (SC) models can be used. SC models follow the heuristic argument that each inclusion deforms as though it sits in the as-yet-unknown effective medium, rather than in the original uniform background phase. When assuming random distribution of spherical pores, the SC model can be written as: 
# 
# .. math::
#       \frac{1}{K^{*}}=\frac{1}{K_{S}}+\left(\frac{1}{K^{*}}+\frac{3}{4 G^{*}}\right) \phi
# 
# 
# .. math::
#       \frac{1}{G^{*}}=\frac{1}{G_{S}}+\frac{15 K^{*}+20 G *}{9 K^{*}+8 G *} \frac{\phi}{G^{*}}
# 
# 
# It's noted that :math:`K^*` is sitting at the both sides of the equation. So does :math:`G^*`. Therefore, iterative solver is invoked in the implementation. :math:`K^*` and :math:`G^*` will converge after several iterations.
# 
# The function that performs the calculation is ``EM.SC``
#  
#
# Non-interacting crack model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The predicted moduli using spherical inclusions are too high compared to experiments on e.g. sandstone, as spherical pores are stiff. The pore geometry in real rock is highly irregular and the pores are more compliant. A simple approach is to include cracks (thin pores) in the EM models. The non-iteracting randomly oriented crack model is defined as : 
# 
# .. math::
#       \frac{1}{K^{*}}=\frac{1}{K_{s}}\left[1+\frac{16}{9} \frac{1-v_{s}^{2}}{1-2 v_{s}} \xi\right] \quad 
# 
# 
# .. math::
#       \frac{1}{G^{*}}=\frac{1}{G_{s}}\left[1+\frac{32\left(1-v_{s}\right)\left(5-v_{s}\right)}{45\left(2-v_{s}\right)} \xi\right]
# 
# 
# where :math:`\xi` is crack density defined as:
# 
# .. math::
#       \xi=\frac{3\phi_{crack}}{4\pi\alpha}
# :math:`\phi_{crack}` is the crack porosity:
# 
# .. math::
#       \phi_c=\frac{4\pi}{3}\alpha \xi
# 
# 
# The function that performs the calculation is ``EM.Dilute_Crack``
#
# Self-Consistent crack model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# O’Connell and Budiansky (1974) presented equations for effective bulk and shear moduli of a cracked medium with randomly oriented dry penny-shaped cracks (in the limiting case when the aspect ratio :math:`\alpha` goes to 0)
# 
# .. math::
#       K^{*}=K_{s}\left[1-\frac{16}{9} \frac{1-v^{* 2}}{1-2 v^{*}} \xi\right] 
# 
# 
# .. math:: 
#       G^{*}=G_{s}\left[1-\frac{32}{45} \frac{\left(1-v^{*}\right)\left(5-v^{*}\right)}{\left(2-v^{*}\right)} \xi\right]
# 
# The poisson's ratio can be approximated as 
#
# .. math::
#       \nu^{*} \cong \nu_{s}\left(1-\frac{16}{9} \xi\right)
#
# 
# The function that performs the calculation is ``EM.OConnell_Budiansky``
# 
# Examples
# ~~~~~~~~
# Let's compare between different effective medium models for spherical pores
#

# %% 

# specify model parameters
phi=np.linspace(0,0.6,100,endpoint=True) # solid volume fraction = 1-phi
K0, G0= 40,30
#Kw, Gw= 2.2,0
# Voigt bound
K_v=(1-phi)*K0
# Hashin-Strikmann bound 
K_UHS,_= EM.HS(1-phi, K0, 0,G0,0, bound='upper')
# Non-interacting 
K_ni,G_ni=EM.Swiss_cheese(K0,G0,phi)
# Self-Consistent
iter_n=100
phi_=np.linspace(0,0.5,100,endpoint=True) 
K_SC,G_SC=EM.SC(phi_,K0,G0,iter_n)



# %% 

# plot
plt.figure(figsize=(8,6))
plt.xlabel('Porosity')
plt.ylabel('Bulk modulus [GPa]')
plt.title('EM models for spherical pores')
plt.plot(phi, K_v,label='K Voigt')
plt.plot(phi, K_UHS,label='K HS+')
plt.plot(phi, K_ni,label='K Non-interacting \nSwiss Cheese model')
plt.plot(phi_, K_SC,label='K self consistent')
plt.legend(loc='best')
plt.grid(ls='--')


# %% 

# O’Connell and Budiansky
crd= np.arange(0,0.1,0.001)
K_ob,G_ob = EM.OConnell_Budiansky(K0, G0, crd)
# dilute crack
K_dc, G_dc= EM.Dilute_crack(K0,G0,crd)


# %% 

# plot
plt.figure(figsize=(8,6))
plt.xlabel('Crack density')
plt.ylabel('Bulk modulus [GPa]')
#plt.title('EM models for crack inclusions')
plt.plot(crd, K_ob,label='OConnell_Budiansky')
plt.plot(crd, K_dc,label='Dilute_crack')

plt.legend(loc='best')
plt.grid(ls='--')

# %% 
# Notice that the two initial models are equivalent for low values of crack density :math:`\xi`, hence they are both valid for low concentrations of inclusions. For high concentrations of inclusions, the models diverge. 
# 
#
# 
#
# Impact of fluid
# ~~~~~~~~~~~~~~~
# Some inclusion models with cracks will not be Biot-consistent, since the fluid pressure between cracks and pores does not have time to equilibrate during a period of the wave. Dry cavities can be modeled by setting the inclusion moduli to zero. Fluid saturated cavities are simulated by setting the inclusion shear modulus to zero.
# 
# For SC approach: Because the cavities are isolated with respect to flow, this approach simulates very high-frequency saturated rock behavior appropriate to ultrasonic laboratory conditions. At low frequencies, when there is time for wave-induced pore-pressure increments to flow and equilibrate, it is better to find the effective moduli for dry cavities and then saturate them with the Gassmann low-frequency relations. This should not be confused with the tendency to term this approach a low-frequency theory, for crack dimensions are assumed to be much smaller than a wavelength.  
#
# **Reference** : Mavko, G., Mukerji, T. and Dvorkin, J., 2020. The rock physics handbook. Cambridge university press.
#