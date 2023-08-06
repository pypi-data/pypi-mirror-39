# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 15:04:51 2018

@author: cham
"""

#%%
import os
os.chdir("/home/cham/")
from astropy.io import fits

input_flats = fits.getdata("./module_par.fits")

#%%
%%time
from regli import Regli
r = Regli.init_from_flats(input_flats)

#%%
#%pylab qt5
import numpy as np
from regli import Regli

ndim = input_flats.shape[1]
grids = [np.unique(input_flats[:, i]) for i in range(ndim)]


r = Regli(*grids)

# determine eps
eps_auto = np.min([np.min(np.diff(grid)) for grid in grids])*0.3

# determine n_flats
nrow = np.prod(r.grid_shape)
ind_values = np.zeros((nrow,), np.int)

for i in range(len(r.flats)):
    flat_ = r.flats[i]
    flat_ind_ = r.flats_ind[i]
    
    # evaluate norm
    norm_ = np.linalg.norm(input_flats - flat_, np.inf, axis=1)
    if np.min(norm_)<eps_auto:
        # data exists
        r.ind_dict[tuple(flat_ind_)] = np.argmin(norm_)
    else:
        r.ind_dict[tuple(flat_ind_)] = None
        print("@Regli: grid value lost --> ", flat_)

return r
#figure(); plot(norm_)
    

#%%
from collections import OrderedDict
