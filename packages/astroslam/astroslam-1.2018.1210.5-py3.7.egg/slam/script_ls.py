#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 15:06:36 2018

@author: cham
"""

#%%
import numpy as np
from scipy.linalg import svd
from scipy import optimize

# jacobian matrix to standard deviation
def jac_to_err(jac):
    _, s, VT = svd(jac, full_matrices=False)
    threshold = np.finfo(float).eps * max(jac.shape) * s[0]
    s = s[s > threshold]
    VT = VT[:s.size]
    pcov = np.dot(VT.T / s**2, VT)
    return np.sqrt(np.diag(pcov))

# return residuals [for leastsq, least_squares]
def cost1(x=0, y=0, y_err=1):
    return (x-y)/y_err

# return 1/2*chi2 [for minimize]
def cost2(p, obs, obs_err):
    return np.sum(((p-obs)/obs_err)**2.)*.5


#%%
test_y = 1.0
test_y_err = 0.2

r0 = optimize.leastsq(cost1, -10, args=(test_y, test_y_err), full_output=True)  #
r0 = optimize.leastsq(cost1, -10, args=(test_y, test_y_err))  #


print("r0=", r0)
print("r0_err=", np.sqrt(np.diag(r0[1])))

r1 = optimize.least_squares(cost1, -10, args=(test_y, test_y_err))  #
print("r1=", r1)
print("r2_err=", jac_to_err(r1.jac))