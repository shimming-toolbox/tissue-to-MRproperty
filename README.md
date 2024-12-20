# <div align="center">**Segmentation to MR Properties Converter**</div>

This repository will contain the code necessary for creating different (and selected) volumes whose values represent different MR useful properties: T2, T2 star, Proton Density and Susceptibility.

# Phantom Creation

This repository requires CT-labeled Nifti files. We use the output from Total Segmentator [1]. </br>
We implement an object-oriented python code that relies on the labels look up table from total segmentator. We implement 2 classes: Volume and Label. They have a parent-daughter relationship. The volume is the nifti file so we can access information from the header such as dimensions or voxel size and assign them as attributes to the Volume. Then we instance a label class for every unique label from the input, where MR properties are assigned as attributes such as: Proton Density, Net Magnetization, T1, T2, T2 star and susceptibility; as well as an identifying ID number and a name. We reduce the labels into groups based on their magnetic susceptibility. We group them based on susceptibility values as we want to create a new volume with susceptibility differences that will contribute to the image quality. 

A parcellation color map for ITK-snap is provided [here](parcellation_itk.txt). This file encodes labels 1 to 48 with a name according to the label it will hve once code is ran; labels 49 to 67, 72, 72, 77 to 86 are named "extra" as they do not have a fixed name in the label class. An example of the final output color scheme is shown below.

![image](https://github.com/sriosq/brainhack_project/assets/154398382/36e16ab6-0683-4455-bec4-4337bb7bb975)

# Installation

First, clone the repository

```
git clone https://github.com/shimming-toolbox/tissue-to-MRproperty
```

Navigate to the project directory

```
cd tissue-to-MRproperty
```

Install the package

```
pip install .
```

# Usage

Once in the package is installed, you can process your images directly from the terminal. A description follows. </br>

**Arguments** 
- -i, input filename (expected to be compressed nifti, must end in .nii.gz)
- -s, segmentation_tool : ['TotalSeg_CT','TotalSeg_MRI','ProCord_MRI','compare_fm']
- -v, version : ['v1','v2','mod0','mod1','mod2','dyn']
- -t, type : ["t2s", "sus", "pd", "t1", "t2"]
- -g, gauss : ["0", "1"]
- x, Susceptibility value (only used if tool is compare_fm tool and version is dynamic)
- -o, output filename (expected to be compressed nifti, must end in .nii.gz)

Example:
```
tissue_to_mr -i data/correct_pixels.nii.gz -t sus -s TotalSeg_CT -v mod2 -g 1 -o sus_gauss_dist.nii.gz
```

```
tissue_to_MR -i input_seg.nii.gz -s compare_fm -v dyn -t sus -x -4.36 -o chi_opt_map.nii.gz
```

**Output** The new volume will be saved as Nifti inside the *output* folder. </br>

The code has implemented a **pixel_check** function that will run before running the conversion. If the function finds a pixel with label intensity value outside the known labels in the dictionary provided by *-s*, segmentation label, the code will ask to change the value of the pixel or delete this pixel (set value to 0). If the code changes any value, it will automatically save a new Nifti image in the output folder with name: **corrected_pixels.nii.gz**.

Now the converter has an option of creating the phantom with a Gaussian (normal) distribution based on: the total count of pixels per label and using the fixed value on the look-up table as the mean. Currently only supports **t2s**, **pd** and **sus** volume creation.

*Note*: Only **t2s**, **pd** and **sus** are supported MR properties for conversion. Depending on the tool used for segmentation the code will use different lookup tables for label id-name relationship. </br>
*T1, T2 and more segmentation tools coming soon!*

# Look-up table
Here we document the respective look-up tables used for assigning MR property values to labels. This are acquired from literature publications, reference to the literature used for creating the look-up table are inside the code for the [label](functions/label.py) class.


| Label         | T1 [ms]  | T2  [ms] | T2*  [ms] | PD   | Susceptibility [ppm] |
|---------------|------|------|-------|------| ----------------------------|
| air           | 0    | 0    | 0.01  | 0.01 | 0.35 |
| bone          | 1204 | 53   | 33.03 | 117  | -9 |
| lungs         | 1270 | None | 0.1   | 0.1  | 0.2 |
| water         | 2500 | 2500 | 1     | 100  | -9.05 |
| CSF           | 3200 | 2000 | 1     | 100  | -9.05 |
| spinal_cord   | None | None | 76    | 59.5 | -9.055 |
| sc_csf        | 3200 | 2000 | 1     | 100  | -9.05 |
| fat           | 380  | 108  | 35    | 140  | -8.92 |
| liver         | 809  | 34   | 17    | 70   | -9.05 |
| spleen        | 1328 | 61   | 32.5  | 80   | -9.05 |
| brain         | None | None | 60.8  | 90   | -9.04 |
| white_matter  | None | None | 26.75 | 0    | - |
| gray_matter   | None | None | 66    | 0    | - |
| sc_wm         | None | None | 0     | 0    | - |
| sc_gm         | None | None | 0     | 0    | - |
| heart         | 1300 | 55   | 9.25  | 85   | -9.04 |
| kidney        | 1190 | 56   | 32.7  | 70   | -9.05 |
| pancreas      | 725  | 43   | 37    | 75   | -9.05 |
| cartilage     | 1240 | 32   | 20    | 50   | -9.04 |
| bone_marrow   | 365  | 23   | None  | 60   | -9.04 |
| SpinalCanal   | 993  | 78   | 60    | 100  | -9.05 |
| esophagus     | None | None | 17    | 35   | -9.05 |
| trachea       | None | None | 25    | 15   | 0.2 |
| organ         | 800  | 34   | 17    | 50   | -9.05 |
| gland         | None | None | 50    | 100  | -9.05 |
| extra         | 750  | 50   | 35    | 120  | -9.04 |

T1 and T2 values are still not completely implemented. </br>

# Adding Labels - Modified Nifti

One of the current limitations of the output from Total Segmentator is the label definition for the Spinal Cord. This encouraged us to add new labels to the phantom. </br>
In the following [repository](https://github.com/sriosq/Image-processing-strategies) you will find usefull strategies and code to create new labels as well as adding them to a segmented image.

# References 

[1] Wasserthal, J., Breit, H.-C., Meyer, M.T., Pradella, M., Hinck, D., Sauter, A.W., Heye, T., Boll, D., Cyriac, J., Yang, S., Bach, M., Segeroth, M., 2023. TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images. Radiology: Artificial Intelligence. https://doi.org/10.1148/ryai.230024 </br>
