import numpy as np
import nibabel as nib
import argparse
import scipy

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

def get_relax_values():


    relax = {

        "air": [0, 0, 0, 0.01, 0.01],
        "bone": [None, 1204, 53, 33.03, 117],  # M0 is often not specified for bone
        "lungs": [None, 1270, None, 1, 0.1],  # Air in lungs doesn't have M0, T2 values?
        "water": [None, 2500, 2500, 1000, 100],  # High M0 value
        "CSF": [None, 3200, 2000, 1000, 100],  # High M0

        "spinal_cord": [None, None, None, 76, 59.5],  # From the new label 256
        # PD & T2* GM + WM / 2 =>  82 + 70 /2 =    , T2star = 66 + 53 / 2 =

        "sc_csf": [None, 3200, 2000, 1000, 100],  # From the new label 289
        "sc_wm": [None, None, None, 53, 70],  # From NumericalModel - Eva
        "sc_gm": [None, None, None, 66, 82],  # From Numerical Model - Eva

        "fat": [None, 380, 108, 35, 140],  # T2star value : 0.5*70e-3 # Daniel PD=90
        "liver": [None, 809, 34, 34 / 2, 70],
        "spleen": [None, 1328, 61, 65 / 2, 80],
        # In this initial segmentation the whole brain will be considered 60% GM and 40% WM
        # Given the values a ponderated estimation is 60.8 ms
        "brain": [None, None, None, 60.8, 90],
        "white_matter": [None, None, None, 53, 70],  # This is the brain WM
        "gray_matter": [None, None, None, 66, 82],  # This is the brain GM

        "heart": [1000, 1300, 55, 18.5 / 2, 85],
        "kidney": [None, 1190, 56, 65.4 / 2, 70],
        "pancreas": [None, 725, 43, 37, 75],
        "cartilage": [None, 1240, 32, 20, 50],  # PD value is a guess
        "bone_marrow": [None, 365, 23, None, 60],  # PD value is a guess
        "SpinalCanal": [None, 993, 78, 60, 100],  #
        "esophagus": [None, None, None, 17, 35],  #
        "trachea": [None, None, None, 25, 15],
        "organ": [None, 800, 34, 17, 50],  # Values similar to those from liver
        "gland": [None, None, None, 50, 100],
        # There are some organs that don't have enough documentation on the literature to complete
        # the required values so an estimation is used for these:
        "extra": [None, 750, 50, 35, 120],

        "sinus": [None, None, None, None, None]
    }
    
    return relax


