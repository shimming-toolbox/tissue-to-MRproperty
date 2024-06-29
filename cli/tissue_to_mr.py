import click
import os
import sys
# With the next line we add to path the project folder to navigate into functions folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.volume import volume


# tissue_to_mr --input [labeled_nifti] --type [choose_MR_property] --output [name=default]

@click.command()
@click.option('-i',"--input",help="Input must be segmented label nifti")
@click.option("--type",help="Please choose MR property to convert to")
@click.option('-o',"--output",help="Output name (optional)")
def converter(input,type,output):
    if output == None:
        output = "default"
        click.echo(f"Input: {input} Type: {type} Output:{output}")
    else:
        click.echo(f"Input: {input} Type: {type} Output:{output}")


if __name__ == "__main__":
    converter()