import click
import os
import sys
# With the next line we add to path the project folder to navigate into functions folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.volume import volume
from functions.utils.utils import is_nifti

# tissue_to_mr --input [labeled_nifti] --type [choose_MR_property] --output [name=default]

@click.command()
@click.option('-i',"--input",help="Input must be segmented label nifti")
@click.option("--type",help="Please choose MR property to convert to")
@click.option('-o',"--output",help="Output name (optional)")
def hello(input,type,output):
    if output == None:
        output = "default"
        click.echo(f"Input: {input} Type: {type} Output:{output}")
    else:
        click.echo(f"Input: {input} Type: {type} Output:{output}")

PROPERTIES = {
    "t2s" : "T2 star",
    "sus" : "Susceptibility",
    "pd" : "Proton density",
    "t1" : "T1",
    "t2" : "T2",
}
@click.command()
@click.option('-i',"--input",help="Input must be segmented label nifti")
@click.option("--type",type=click.Choice(PROPERTIES.keys()), help="Please choose MR property to convert to")
def converter(input,type):
    # We need to check if the input is a  nifti file
    if is_nifti(input):
        new_vol = volume(input)
        # Using the type:
        new_vol.create_segmentation_labels() # Automatically adding the names to known labels
        new_vol.create_type_vol(type)
    else:
        print("Input must be a nifti file")


if __name__ == "__main__":
    converter()