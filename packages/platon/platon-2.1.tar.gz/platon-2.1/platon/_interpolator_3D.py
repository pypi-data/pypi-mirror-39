import numpy as np
import sys
from scipy.interpolate import RectBivariateSpline, interp1d
import time


def get_condition_array(target_data, interp_data, max_cutoff=np.inf):
    cond = np.zeros(len(interp_data), dtype=bool)

    start_index = None
    end_index = None

    for i in range(len(cond)):
        if start_index is None:
            if interp_data[i] > np.min(target_data):
                start_index = i-1
            if interp_data[i] == np.min(target_data):
                start_index = i
        if end_index is None:
            if interp_data[i] >= np.max(target_data) or \
               interp_data[i] >= max_cutoff:
                end_index = i + 1
                
    cond[start_index : end_index] = True
    return cond


def normal_interpolate(data, grid_x, grid_y, target_x, target_y):
    all_results = []
    for i in range(data.shape[0]):
        interpolator = RectBivariateSpline(grid_y, grid_x, data[i], kx=1, ky=1)
        result = interpolator.ev(target_y, target_x)
        all_results.append(result)
    return np.array(all_results)


def fast_interpolate(data, grid_x, grid_y, target_x, target_y):
    target_x = np.atleast_1d(target_x)
    target_y = np.atleast_1d(target_y)
    assert(len(target_x) == len(target_y))

    if len(grid_x) == 1:
        # Stupid hack to get around refusal of RectBivariateSpline to
        # interpolate with only one element
        if len(grid_y) == 1:
            # interp1d can't handle only 1 element either
            assert(grid_y == target_y)
            return data.reshape((data.shape[0], 1))
        interpolator = interp1d(grid_y, data, axis=1)
        return interpolator(target_y).reshape((data.shape[0], len(target_y)))

    if len(grid_y) == 1:
        # Same hack as above
        if len(grid_x) == 1:
            assert(grid_x == target_x)
            return data.reshape((data.shape[0], 1))
        interpolator = interp1d(grid_x, data, axis=2)
        return interpolator(target_x).reshape((data.shape[0], len(target_x)))
    
    x_mesh, y_mesh = np.meshgrid(np.arange(len(grid_x)), np.arange(len(grid_y)))
    interpolator = RectBivariateSpline(grid_x, grid_y, x_mesh.T, kx=1, ky=1)
    x_indices = interpolator.ev(target_x, target_y)
    assert(np.max(x_indices) <= len(grid_x))

    interpolator = RectBivariateSpline(grid_x, grid_y, y_mesh.T, kx=1, ky=1)
    y_indices = interpolator.ev(target_x, target_y)
    assert(np.max(y_indices) <= len(grid_y))

    x_indices_lower = x_indices.astype(int)
    x_indices_upper = x_indices_lower + 1
    x_indices_upper[x_indices_upper == len(grid_x)] -= 1
    x_indices_frac = x_indices - x_indices_lower

    y_indices_lower = y_indices.astype(int)
    y_indices_upper = y_indices_lower + 1
    y_indices_upper[y_indices_upper == len(grid_y)] -= 1
    y_indices_frac = y_indices - y_indices_lower

    result = data[:, y_indices_lower, x_indices_lower]*(1-y_indices_frac)*(1-x_indices_frac) + \
             data[:, y_indices_upper, x_indices_lower]*y_indices_frac*(1-x_indices_frac) + \
             data[:, y_indices_lower, x_indices_upper]*(1-y_indices_frac)*x_indices_frac + \
             data[:, y_indices_upper, x_indices_upper]*y_indices_frac*x_indices_frac
    return result
    

