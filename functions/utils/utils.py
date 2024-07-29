import numpy as np
import nibabel as nib
import argparse
import scipy
from skimage.measure import label, regionprops
def is_nifti(filepath):
    """
    Check if the given filepath represents a NIfTI file.

    Args:
        filepath (str): The path of the file to check.

    Returns:
        bool: True if the file is a NIfTI file, False otherwise.
    """
    if filepath[-4:] == '.nii' or filepath[-7:] == '.nii.gz':
        return True
    else:
        return False

def create_gaussian(size,center,sigma):

    """
    Create a gaussian distribution

    Parameters:
        size: tuple of the dimensions of the output array (height, weight)
        center: tuple
        sigma:

    Returns:

    """
    x = np.linspace(0, size[1] - 1, size[1])
    y = np.linspace(0, size[0] - 1, size[0])

    x, y = np.meshgrid(x, y)
    gaussian = np.exp(-((x - center[1]) ** 2 + (y - center[0]) ** 2) / (2 * sigma ** 2))
    return gaussian


