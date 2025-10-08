import time

import click
import logging
import nibabel as nib
# With the next line we add to path the project folder to navigate into functions folder
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from tissue2mrprop.functions import __dir_converter__, __dir_functions__, __dir_utils__
from tissue2mrprop.functions.volume import volume
from tissue2mrprop.functions.utils.utils import is_nifti
# tissue_to_mr --input [labeled_nifti] --type [choose_MR_property] --output [name=default]

import time

@click.command()

def display(input_file,segtool,version):
    if is_nifti(input_file):
        start = time.time()
        print("Hello")
        exit()