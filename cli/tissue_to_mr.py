import click
import os
import sys
import logging
import nibabel as nib
# With the next line we add to path the project folder to navigate into functions folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.volume import volume
from functions.utils.utils import is_nifti

# tissue_to_mr --input [labeled_nifti] --type [choose_MR_property] --output [name=default]

@click.group
def my_commands():
    pass

PROPERTIES = {
    "t2s" : "T2 star",
    "sus" : "Susceptibility",
    "pd" : "Proton density",
    "t1" : "T1",
    "t2" : "T2",
}
@click.command()
@click.argument("input_file", required=True) #, help="Input must be segmented label nifti",type=click.Path(exists=True))
@click.option('-s',"--segtool", help="State what segmentator was used")
@click.argument('output_file', required=False, type=click.Path())
@click.option('-t',"--type",required=True, type=click.Choice(PROPERTIES.keys()), help="Please choose MR property to convert to")
def converter(input_file,segtool,output_file, type):
    # We need to check if the input is a  nifti file
    if is_nifti(input_file):
        print("start")
        logging.info(f"Creating a new volume with {type} values")
        file = nib.load(input_file)
        print("file loaded")
        new_vol = volume(file)
        print("a")
        # Using the type:
        new_vol.create_segmentation_labels() # Automatically adding the names to known labels
        print("b")
        if output_file == None:

            new_vol.create_type_vol(type) # Thiscreates and saves a Nifti file
        else:
            new_vol.create_type_vol(type,output_file)

        print(f"Input segmented by:{segtool}")
    else:
        print("Input must be a Nifti file (.nii or .nii.gz extensions)")

my_commands.add_command(converter)
if __name__ == "__main__":
    my_commands()