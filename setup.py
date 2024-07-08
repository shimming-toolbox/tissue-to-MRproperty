from setuptools import find_packages, setup
from os import path

# Get directory where this current file is saved
here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tissue-to-MRproperty",
    python_requires = ">=3.8.8",
    description = "Code that creates a volume from a segmented Nifti file to a selected MR property",
    long_description = long_description,
    url = "https://github.com/shimming-toolbox/tissue-to-MRproperty",
    entry_points = {
        'console_scripts': [
        "tissue_to_MR = cli.tissue_to_mr:converter"
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
        "jupyterlab",
        "scipy"
    ]
)