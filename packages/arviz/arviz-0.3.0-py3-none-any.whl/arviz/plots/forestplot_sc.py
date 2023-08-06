import pymc3 as pm
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import mcmcplotlib as mpl
plt.style.use('seaborn-darkgrid')


with pm.Model() as model:
    a = pm.Normal('a', 0 , 1, shape=2)
    b = pm.Normal('b', 0 , 1)
    trace0 = pm.sample(100, tune=0, chains=2, compute_convergence_checks=False)

with pm.Model() as model:
    a = pm.Beta('a', 1 , 1, shape=2)
    trace1 = pm.sample(100, tune=0, chains=2, compute_convergence_checks=False)
    
    
mpl.forestplot([trace0, trace1])
plt.show()