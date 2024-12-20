import time

import click
import logging
import nibabel as nib
# With the next line we add to path the project folder to navigate into functions folder
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from functions import __dir_converter__, __dir_functions__, __dir_utils__
from functions.volume import volume
from functions.utils.utils import is_nifti
# tissue_to_mr --input [labeled_nifti] --type [choose_MR_property] --output [name=default]

import time
@click.group()
def my_commands():
    pass

PROPERTIES = {
    "t2s" : "T2 star",
    "sus" : "Susceptibility",
    "pd" : "Proton density",
    "t1" : "T1",
    "t2" : "T2",
}

#@click.argument("input_file", required=True) #, help="Input must be segmented label nifti",type=click.Path(exists=True))
@click.command()
@click.option('-i','--input','input_file', type=click.Path(exists=True), required=True,
              help="Input segmentations distribution, supported extensions: .nii, .nii.gz")
@click.option('-s',"--segtool",required=True,type=click.Choice(['TotalSeg_CT','TotalSeg_MRI','ProCord_MRI', 'charles','compare_fm']), help="State what segmentator was used")
@click.option('-v',"--version",required=True,type=click.Choice(['v1','v2','mod0','mod1','mod2','dyn','mod_PAM50',"mathieu"]), help="Select the version of your segmentation file")
@click.option('-t',"--type",required=True, type=click.Choice(PROPERTIES.keys()), help="Please choose MR property to convert to")
@click.option("-g", "--gauss",required=False, type= click.Choice(["0","1"]), default = "0", help = "Set to 1 to use Gaussian distribution")
@click.option("-x","--chi", required = False, type = float, default = None, help = "Used to define new chi value for FM comparison approach")
@click.option('-o', '--output', 'output_file', type=click.Path(), default= "sus_dist.nii.gz", required= False,
              help = "By default it saves the chimap to the output folder")

def converter(input_file, segtool, version, type, gauss, chi, output_file):
    # We need to check if the input is a  nifti file
    if is_nifti(input_file):
        start = time.time()
        print("start")
        #logging.info(f"Creating a new volume with {type} values")
        print(f"Creating a new volume with {type} values")
        file = nib.load(input_file)
        print("file loaded")
        new_vol = volume(file)
        print("Grouping labels")
        # Using the type:

        # This for the FM comparison project:
        # Needs to be before grouping labels, if not it will put none
        if segtool == "compare_fm" and version == "dyn":
            if chi != None:
                new_vol.new_chi = chi
                print("Using new susceptibility value for air: ",chi)
            else:
                print("When using new dynamic version you must provide a chi value")
                new_vol.new_chi = 0.3
                print("Using default: ", new_vol.new_chi)

        new_vol.group_seg_labels(segtool, version)  # Automatically adding the names to known labels
        #print(new_vol.segmentation_labels[7])
        # Printing one label can help see the structure as well as verifying values selected
        # Specially when working with field map comparison project where chi can be changed

        print("Checking pixel integrity")
        ans = new_vol.check_pixels()

        if ans == 0:
            print("Converting ...")

            if gauss == "1":

                new_vol.gauss_flag = 1
                print("Gaussian option enabled ...")
                new_vol.calc_regions()
                new_vol.create_gauss_dist(type)
                print("Creating a Gaussian distribution phantom from ", type, " values")
                if output_file == None:
                    new_vol.save_gauss_dist(type)
                else:
                    new_vol.save_gauss_dist(type,output_file)


            else:

                if output_file == None:
                    print("Piece-wise mode: on")
                    new_vol.create_type_vol(type) # This creates and saves a Nifti file

                else:
                    print("Piece-wise ON - custom out_fn")
                    new_vol.create_type_vol(type,output_file)

            print(f"Input segmented by: {segtool}, version: {version}")
            end = time.time()
            elapsed = end-start
            print("Time elapsed: ",elapsed)

        else:

            print("Pixel integrity error")

    else:
        print("Input must be a Nifti file (.nii or .nii.gz extensions)")

#my_commands.add_command(converter)
#if __name__ == "__main__":
#    my_commands()
