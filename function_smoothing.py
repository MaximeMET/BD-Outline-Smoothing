# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:33:28 2024

@author: maxim
"""

import numpy as np

def cartesian_to_polar(data, origin):
    x = data[:, 0]  # Extract x values
    y = data[:, 1]  # Extract y values
    dx = x - origin[0]  # Compute difference in x from origin
    dy = y - origin[1]  # Compute difference in y from origin
    result = np.column_stack((np.arctan2(dy, dx)/np.pi*180, np.sqrt(dx**2 + dy**2)))  # Convert to polar coordinates (angle in degrees and radius)
    
    return result[result[:, 0].argsort()]  # Sort by angle

def polar_to_cartesian(data, origin):
    theta = data[:, 0]  # Extract angle values
    r = data[:, 1]  # Extract radius values
    
    x = r * np.cos(theta/180*np.pi) + origin[0]  # Convert to x
    y = r * np.sin(theta/180*np.pi) + origin[1]  # Convert to y
    
    return np.column_stack((x, y))  # Combine x and y into a single array

def adjacent_average(data, window_size=9):
    y = data[:, 1].copy()  # Copy y values for smoothing
    
    half_window = window_size // 2  # Calculate half of the window size
    y[half_window:-half_window] = np.convolve(y, np.ones(window_size, dtype=int) / window_size, 'valid')  # Apply moving average filter
    
    return np.column_stack((data[:, 0], y))  # Combine x and smoothed y into a single array

def lowess(data, frac=0.1):
    x = data[:, 0]
    y = data[:, 1]
    n = len(x)
    smoothed_y = np.zeros(n)
    if frac == 0.0:
        smoothed_y = y
    else:
        # Calculate the weights for the smoothing
        x_std = np.std(x)  # Compute standard deviation of x
        weights_matrix = np.exp(-((x[:, None] - x[None, :]) ** 2) / (2 * (frac * x_std) ** 2))  # Calculate weights based on distance
    
        # Calculate weighted averages for smoothing
        for i in range(n):
            weights = weights_matrix[i]
            smoothed_y[i] = np.sum(weights * y) / np.sum(weights)

    return np.column_stack((x, smoothed_y))  # Combine x and smoothed y into a single array

def interpolate1(data):
    new_x = np.arange(-180, 271, 1)  # Create new x values from -180 to 270 degrees
    new_y = np.interp(new_x, data[:, 0], data[:, 1])  # Interpolate y values

    # Copy data from -180 to -90 degrees to 180 to 270 degrees
    source_indices = np.where((new_x >= -180) & (new_x <= -90))[0]
    target_indices = np.where((new_x >= 180) & (new_x <= 270))[0]
    
    new_y[target_indices] = new_y[source_indices]
    
    return np.column_stack((new_x, new_y))  # Combine new x and y into a single array

def copying2(data):
    x = data[:, 0]  # Extract x values
    y = data[:, 1]  # Extract y values
    # Copy data from 180 to 270 degrees to -180 to -90 degrees
    source_indices = np.where((x >= 180) & (x <= 270))[0]
    target_indices = np.where((x >= -180) & (x <= -90))[0]
    
    y[target_indices] = y[source_indices]
    
    return np.column_stack((x, y))  # Combine x and y into a single array

def smoothing(data, frac):
    # Calculate the centroid (geometric center) of the data
    centroid = np.mean(data, axis=0)
    
    # Convert Cartesian data to polar coordinates
    polar_data = cartesian_to_polar(data, centroid)
    
    # Interpolate polar data and handle edge cases
    interp_polar_data = interpolate1(polar_data)
    
    # Apply LOWESS smoothing to the interpolated polar data
    lowess_interp_polar_data = lowess(interp_polar_data, frac)
    
    # Copy data from 180 to 270 degrees back to -180 to -90 degrees
    interp2_lowess_interp_polar_data = copying2(lowess_interp_polar_data)
    
    # Smooth the data around the -90 degree seam and apply adjacent averaging
    averaged_interp2_lowess_interp_polar_data = interp2_lowess_interp_polar_data[
        (interp2_lowess_interp_polar_data[:, 0] >= -120) & 
        (interp2_lowess_interp_polar_data[:, 0] <= -60)
    ]
    for i in range(2):  # Apply smoothing multiple times
        averaged_interp2_lowess_interp_polar_data = adjacent_average(averaged_interp2_lowess_interp_polar_data)
    
    # Replace the smoothed data back into the original position
    substi_interp2_lowess_interp_polar_data = interp2_lowess_interp_polar_data
    substi_interp2_lowess_interp_polar_data[
        (substi_interp2_lowess_interp_polar_data[:, 0] >= -120) & 
        (substi_interp2_lowess_interp_polar_data[:, 0] <= -60)
    ] = averaged_interp2_lowess_interp_polar_data
    
    # Convert the smoothed polar data back to Cartesian coordinates
    cartesian_data = polar_to_cartesian(
        substi_interp2_lowess_interp_polar_data[
            (substi_interp2_lowess_interp_polar_data[:, 0] >= -180) & 
            (substi_interp2_lowess_interp_polar_data[:, 0] <= 180)
        ], 
        centroid
    )
    
    return polar_to_cartesian(cartesian_to_polar(data, centroid),centroid), cartesian_data, polar_data, substi_interp2_lowess_interp_polar_data
