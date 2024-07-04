import numpy as np
import nibabel as nib
import argparse

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