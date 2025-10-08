# <div align="center">**Segmentation to MR Properties Converter**</div>

This repository will contain the code necessary for creating different (and selected) volumes whose values represent different MR useful properties: T2, T2 star, Proton Density and Susceptibility.

# Phantom Creation

This tool requires that the segmentation nifti file provided has already been added to the repositories dictionary of vlaues. We initially used the output from Total Segmentator [1] to group into broader tissue types. </br>
We implement an object-oriented python code that relies on the labels look up table. We implement 2 classes: Volume and Label. They have a parent-daughter relationship. The volume is the nifti file from which we can access information from the header such as dimensions or voxel size and assign them as attributes to the Volume. Then we instance a label class for every unique label from the input, where MR properties are assigned to them as attributes such as: Proton Density, Net Magnetization, T1, T2, T2 star and susceptibility; as well as an identifying ID number and a name. 

A parcellation color map for the TotalCT version "mod 2" for ITK-snap is provided [here](parcellation_itk.txt). This file encodes labels 1 to 48 with a name according to the label it will have; labels 49 to 67, 72, 72, 77 to 86 are named "extra" as they do not have a fixed name in the label class. An example of the final output color scheme is shown below.

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
- -x, Susceptibility value (only used if tool is compare_fm tool and version is dynamic, changes the value susceptibility of Trachea and Lung labels)
- -r, Use as reference value to demodulate the susceptibility property to create different referenced Chi-maps
- -o, output filename (expected to be compressed nifti, must end in .nii.gz)

Example:
```
tissue_to_mr -i data/correct_pixels.nii.gz -i iMag_dub07.nii.gz -s TotalSeg_CT -v mod2 -t sus -g 1 -o dub07_gauss_sus_phantom.nii.gz
```

```
tissue_to_MR -i iMag_dub07.nii.gz -s compare_fm -v dyn -t sus -x -4.36 -o custom_dub07_sus_phantom.nii.gz
```

**Output** The new volume will be saved as Nifti inside the *output* folder. </br>

The tool performs a **pixel_check** function that will run before running the conversion. If the function finds a pixel with label intensity value outside the known labels in the dictionary provided by *-s*, segmentation label, the tool will ask to change the value of the pixel or delete this pixel (set value to 0). If the code changes any value, it will automatically save a new Nifti image in the output folder with name: **corrected_pixels.nii.gz**.

The tool has an option of creating the phantom with a Gaussian (normal) distribution based on: the total count of pixels per label and using the fixed value on the look-up table as the mean. Currently only supported for **t2s**, **pd** and **sus** volume creation.

Depending on the tool used for segmentation the code will use different lookup tables for label id-name relationship. </br>

# Look-up table
Here we document the respective look-up tables used for assigning MR property values to labels. This are acquired from literature publications, reference to the literature used for creating the look-up table are inside the code for the [label](functions/label.py) class.

## Relaxation Values & Susceptibility

| Tissue/Label        | T1 (ms) | T2 (ms) | T2* (ms) | PD (%) | Susceptibility (ppm) |
|----------------------|---------|---------|----------|--------|-----------------------|
| fat                 | 401.2   | 129.3   | 64.65    | 20     | -8.92 |
| heart               | 1215.67 | 49.35   | 25.195   | 77     | -9.05 |
| liver               | 798.75  | 33      | 18.82    | 70     | -9.05 |
| pancreas            | 797.55  | 43.5    | 21.1     | 70     | -9.05 |
| kidney              | 1338    | 86.835  | 57.55    | 82     | -9.05 |
| brain               | 1232.9  | 82.9    | 42.8     | 74.5   | -9.05 |
| spleen              | 1328    | 60.9    | 16.3     | 75     | -9.05 |
| cartilage           | 1201    | 43.225  | 26.04    | 70     | -9.055|
| bone_marrow         | 586     | 49      | 24.5     | 27     | -9.05 |
| sc_wm (Spinal WM)   | 857     | 73      | 38.65    | 70     | -9.083|
| sc_gm (Spinal GM)   | 983.5   | 76      | 44.4     | 80     | -9.03 |
| sc_csf (Spinal CSF) | 5128    | 1419.84 | 709.92   | 100    | -9.03 |
| muscle              | 1237.825| 36.1    | 24.1     | 45     | -9.03 |
| bone                | 223     | 0.39    | 1.16     | 18     | -11.1 |
| v_bone (Vertebrae)  | 618.5   | 80.685  | 40.3     | 40     | -9.7  |
| lungs               | 1400    | 35.5    | 1.62     | 15     | -0.27* |
| trachea             | 1100    | 40      | 12       | 5      | -4.36* |
| air                 | 0.01    | 0.01    | 0.01     | 0.01   | 0.35  |
| extra (blood/muscle)| 800     | 50      | 35       | 50     | -9.04 |
| spinal_cord         | 936.5   | 76.75   | 40.07    | 60     | -9.055|
| water               | 2500    | 275     | 137.5    | 100    | -9.05 |
| CSF                 | 1953    | 275     | 137.5    | 100    | -9.05 |
| white_matter        | 887.7   | 65.4    | 35       | 70     | –     |
| gray_matter         | 1446.1  | 94.3    | 48       | 82     | –     |
| SpinalCanal         | 993     | 78      | 39       | 90     | -9.055|
| esophagus           | 1000    | 32      | 17       | 45     | -9.05 |
| organ (liver-like)  | 800     | 40      | 20       | 65     | -9.05 |
| gland (salivary)    | 1600    | 72      | 36       | 80     | -9.05 |
| sinus               | –       | –       | –        | –      | -     |
| inter_vert_discs    | 1201    | 42      | 26       | 50     | -9.055|


* Susceptibility for Air cavities: lungs & trachea are guesses from a WIP project.

Citation to come with publication soon!. </br>

# Adding Labels - Modified Nifti

One of the current limitations of the output from Total Segmentator is the label definition for the Spinal Cord. This encouraged us to add new labels to the phantom. </br>
In the following [repository](https://github.com/sriosq/Image-processing-strategies) you will find usefull strategies and code to create new labels as well as adding them to a segmented image.
If you would like help adding labels or would like to create a new segmentation tool to easily convert please create a new issue or contact us!

# References 

[1] Wasserthal, J., Breit, H.-C., Meyer, M.T., Pradella, M., Hinck, D., Sauter, A.W., Heye, T., Boll, D., Cyriac, J., Yang, S., Bach, M., Segeroth, M., 2023. TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images. Radiology: Artificial Intelligence. https://doi.org/10.1148/ryai.230024 </br>
