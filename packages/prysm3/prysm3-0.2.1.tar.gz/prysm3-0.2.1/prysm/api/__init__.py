''' API for PRYSM

Feng Zhu (fengzhu@usc.edu)
2018-12-15 16:12:22
'''
from . import icecore
from . import tree
from . import coral
from . import lake
from . import speleo
import p2k
import numpy as np


def forward(proxy, lat_obs, lon_obs, lat_model, lon_model, time_model,
    tas=None, pr=None, psl=None, d18Opr=None, d18Ocoral=None, nproc=8,
    annualize_coral=True,
    Rlib_path='/Library/Frameworks/R.framework/Versions/3.4/Resources/library',
    T1=8, T2=23, M1=0.01, M2=0.05):

    ''' Forward environmental variables to proxy variables

    This is a major wrapper of the PSMs.

    Args:
        proxy (str): options are `coral_d18O`, `ice_d18O`, `tree_trw`
        lat_obs, lon_obs (float): the location of the proxy site
        lat_model, lon_model (1-D/2-D array): the grid points of the model simulation
        tas (3-D array): surface air temperature in (time, lat, lon) [K]
        pr (3-D array): precipitation rate in (time, lat, lon) [kg/m2/s]
        psl (3-D array): sea-level pressure in (time, lat, lon) [Pa]
        d18Opr (3-D array): precipitation d18O in (time, lat, lon) [permil]
        nproc (int): number of threads; only works for `coral_d18O`

    Returns:
        pseudo_value (1-D array): pseudoproxy timeseries
        pseudo_time (1-D array): the time axis of the pseudoproxy timeseries

    '''
    if proxy == 'coral_d18O':
        print('PRYSM >>> forward to {} ...'.format(proxy))
        if d18Ocoral is None:
            raise TypeError

        lat_ind, lon_ind = p2k.find_closest_loc(lat_model, lon_model, lat_obs, lon_obs, mode='mesh')
        print('PRYSM >>> Target: ({}, {}) >>> Found: ({}, {})'.format(
            lat_obs, lon_obs, lat_model[lat_ind, lon_ind], lon_model[lat_ind, lon_ind]))

        pseudo_value = np.asarray(d18Ocoral[:, lat_ind, lon_ind])
        pseudo_value[pseudo_value>1e5] = np.nan  # replace missing values with nan
        while np.all(np.isnan(pseudo_value)):
            for lat_fix in [0, -1, 1, -2, 2, -3, 3]:
                for lon_fix in [0, -1, 1, -2, 2, -3, 3]:
                    pseudo_value = np.asarray(d18Ocoral[:, lat_ind+lat_fix, lon_ind+lon_fix])

        pseudo_value[pseudo_value>1e5] = np.nan  # replace missing values with nan

        if annualize_coral:
            pseudo_value, pseudo_time = p2k.annualize_ts(pseudo_value, time_model)
        else:
            pseudo_time = time_model


    elif proxy == 'ice_d18O':
        print('PRYSM >>> forward to {} ...'.format(proxy))
        if tas is None or pr is None or psl is None or d18Opr is None:
            raise TypeError

        lat_ind, lon_ind = p2k.find_closest_loc(lat_model, lon_model, lat_obs, lon_obs, mode='latlon')
        print('PRYSM >>> Target: ({}, {}) >>> Found: ({}, {})'.format(
            lat_obs, lon_obs, lat_model[lat_ind], lon_model[lon_ind]))

        tas_sub = np.asarray(tas[:, lat_ind, lon_ind])
        pr_sub = np.asarray(pr[:, lat_ind, lon_ind])
        psl_sub = np.asarray(psl[:, lat_ind, lon_ind])
        d18Opr_sub = np.asarray(d18Opr[:, lat_ind, lon_ind])

        # annualize the data
        tas_ann, year_int = p2k.annualize(tas_sub, time_model)
        psl_ann, year_int = p2k.annualize(psl_sub, time_model)
        pr_ann, year_int = p2k.annualize(pr_sub, time_model)

        nyr = len(year_int)

        # sensor model
        d18O_ice = icecore.ice_sensor(time_model, d18Opr, pr)
        # diffuse model
        ice_diffused = icecore.ice_archive(d18O_ice[:, lat_ind, lon_ind], pr_ann, tas_ann, psl_ann, nproc=nproc)

        pseudo_value = ice_diffused[::-1]
        pseudo_time = year_int

    elif proxy == 'tree_trw':
        print('PRYSM >>> forward to {} ...'.format(proxy))
        if tas is None or pr is None:
            raise TypeError

        lat_ind, lon_ind = p2k.find_closest_loc(lat_model, lon_model, lat_obs, lon_obs, mode='latlon')
        print('PRYSM >>> Target: ({}, {}) >>> Found: ({}, {})'.format(
            lat_obs, lon_obs, lat_model[lat_ind], lon_model[lon_ind]))

        syear, eyear = int(np.floor(time_model[0])), int(np.floor(time_model[-1]))  # start and end year
        nyr = eyear - syear + 1
        phi = lat_obs

        tas_sub = np.asarray(tas[:, lat_ind, lon_ind])
        pr_sub = np.asarray(pr[:, lat_ind, lon_ind])

        pseudo_value = tree.vslite(
            syear, eyear, phi, tas_sub, pr_sub,
            Rlib_path=Rlib_path, T1=T1, T2=T2, M1=M1, M2=M2)
        pseudo_time = np.linspace(syear, eyear, nyr)

    else:
        print('PRYSM >>> ERROR: Proxy type not supported!')
        raise ValueError

    if np.all(np.isnan(pseudo_value)):
        pseudo_value, pseudo_time = None, None

    return pseudo_value, pseudo_time
