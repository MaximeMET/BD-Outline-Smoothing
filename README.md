# BD-Outline-Smoothing
**Tool for Smoothing Enclosed Outlines**

Smoothing an enclosed outline can be challenging with common smoothing methods. This tool simplifies the process by converting Cartesian data to polar data, applying a smoothing method, and then converting the smoothed data back to Cartesian coordinates.

## How It Works

1. **Convert to Polar**: The Cartesian data is converted to polar coordinates.
2. **Apply LOWESS Smoothing**: The *LOWESS* (Locally Weighted Scatterplot Smoothing) method is applied to the polar data.
3. **Smooth Seamlessly**: To avoid "seams" in the outline, the beginning and end points are specifically smoothed using an adjacent average method.
4. **Convert Back to Cartesian**: The smoothed polar data is then converted back to Cartesian coordinates, resulting in a smoothly enclosed outline.

## How to Download
Download the latest version from the [Releases](https://github.com/MaximeMET/BD-Outline-Smoothing/releases) section on GitHub.
