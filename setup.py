from setuptools import find_packages, setup
from os import path

# Get directory where this current file is saved
here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tissue-to-MRproperty",
    description = "Code that creates a volume from a segmented Nifti file to a selected MR property",
    long_description = long_description,
    keywords='',
    entry_points = {
        'console_scripts': [
        "tissue_to_MR = tissue-to-MRproperty.cli.tissue_to_mr:converter"
        ]
    },
    packages=find_packages(exclude=["docs"]),
    install_requires=[
        "click",
        "pandas",
        "nibabel",
        "nilearn",
        "numpy",
        "matplotlib",
        "ipykernel",
        "ipython",
        "treelib",
        "pytest",
        "jupyterlab"
    ]
)