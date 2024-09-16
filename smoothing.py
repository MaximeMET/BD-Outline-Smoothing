# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 13:42:37 2024

@author: maxim
"""

import numpy as np
import matplotlib.pyplot as plt
import function_smoothing as fs

# Load data
data = np.loadtxt('data.txt')
# Frac of lowess
frac = 0.05

# Apply the smoothing function from the custom module
smoothed_data, polar_data, smoothed_polar_data = fs.smoothing(data, frac)

smoothed_polar_data =smoothed_polar_data[
    (smoothed_polar_data[:, 0] >= -180) & 
    (smoothed_polar_data[:, 0] <= 180)]

# Plotting the original and smoothed Cartesian data
plt.figure(figsize=(8, 6))

# Plot the original data
plt.plot(data[:, 0], data[:, 1], label='Original Data', color='blue', linestyle='-', linewidth=3, alpha=0.7)

# Plot the smoothed data
plt.plot(smoothed_data[:, 0], smoothed_data[:, 1], label='Smoothed Data', color='red', linestyle='-', linewidth=3, alpha=0.7)

# Add title and labels
plt.title('Comparison of Original and Smoothed Data')
plt.xlabel('X Values')
plt.ylabel('Y Values')

# Display legend
plt.legend()

# Show the plot
plt.show()

# Plotting the original and smoothed polar data
plt.figure(figsize=(8, 6))

# Plot the original polar data
plt.plot(polar_data[:, 0], polar_data[:, 1], label='Original Polar Data', color='blue', linestyle='-', linewidth=3, alpha=0.7)

# Plot the smoothed polar data
plt.plot(smoothed_polar_data[:, 0], smoothed_polar_data[:, 1], label='Smoothed Polar Data', color='red', linestyle='-', linewidth=3, alpha=0.7)

# Add title and labels
plt.title('Comparison of Original and Smoothed Data')
plt.xlabel('θ (Degrees)')
plt.ylabel('Radius')

# Display legend
plt.legend()

# Show the plot
plt.show()

# Save the smoothed data to a text file
np.savetxt('smoothed_data.txt', smoothed_data, delimiter='\t', comments='')
