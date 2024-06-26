# <div align="center">**Segmentation to MR Properties Converter**</div>

This repository will contain the code necessary for creating different (and selected) volumes whose values represent different MR useful properties: T2, T2 star, Proton Density and Susceptibility.

# Phantom Creation

This repository requires CT-labeled Nifti files. We use the output from Total Segmentator [1]. </br>
We implement an object-oriented python code that relies on the labels look up table from total segmentator. We implement 2 classes: Volume and Label. They have a parent-daughter relationship. The volume is the nifti file so we can access information from the header such as dimensions or voxel size and assign them as attributes to the Volume. Then we instance a label class for every unique label from the input, where MR properties are assigned as attributes such as: Proton Density, Net Magnetization, T1, T2, T2 star and susceptibility; as well as an identifying ID number and a name. We reduce the labels into groups based on their magnetic susceptibility. We group them based on susceptibility values as we want to create a new volume with susceptibility differences that will contribute to the image quality. 

A parcellation color map for ITK-snap is provided [here](parcellation_itk.txt). This file encodes labels 1 to 48 with a name according to the label it will hve once code is ran; labels 49 to 67, 72, 72, 77 to 86 are named "extra" as they do not have a fixed name in the label class. An example of the final output color scheme is shown below.

![image](https://github.com/sriosq/brainhack_project/assets/154398382/36e16ab6-0683-4455-bec4-4337bb7bb975)

# Input Nifti advanced option
One of the current limitations of the output from Total Segmentator is the label definition for the Spinal Cord. This encouraged us to add new labels to the phantom. 

# Look-up tables
Here we document the respective look-up tables used for assigning MR property values to labels. This are acquired from literature publications, reference to the literature used for creating the look-up table are inside the code for the [label](functions/label.py) class.

| Label        | M0   | T1   | T2   | T2*   | PD   |
|---------------|------|------|------|-------|------|
| air           | 0    | 0    | 0    | 0.01  | 0.01 |
| bone          | None | 1204 | 53   | 33.03 | 117  |
| lungs         | None | 1270 | None | 0.1   | 0.1  |
| water         | None | 2500 | 2500 | 1     | 100  |
| CSF           | None | 3200 | 2000 | 1     | 100  |
| spinal_cord   | None | None | None | 76    | 59.5 |
| sc_csf        | None | 3200 | 2000 | 1     | 100  |
| fat           | None | 380  | 108  | 35    | 140  |
| liver         | None | 809  | 34   | 17    | 70   |
| spleen        | None | 1328 | 61   | 32.5  | 80   |
| brain         | None | None | None | 60.8  | 90   |
| white_matter  | None | None | None | 26.75 | 0    |
| gray_matter   | None | None | None | 66    | 0    |
| sc_wm         | None | None | None | 0     | 0    |
| sc_gm         | None | None | None | 0     | 0    |
| heart         | 1000 | 1300 | 55   | 9.25  | 85   |
| kidney        | None | 1190 | 56   | 32.7  | 70   |
| pancreas      | None | 725  | 43   | 37    | 75   |
| cartilage     | None | 1240 | 32   | 20    | 50   |
| bone_marrow   | None | 365  | 23   | None  | 60   |
| SpinalCanal   | None | 993  | 78   | 60    | 100  |
| esophagus     | None | None | None | 17    | 35   |
| trachea       | None | None | None | 25    | 15   |
| organ         | None | 800  | 34   | 17    | 50   |
| gland         | None | None | None | 50    | 100  |
| extra         | None | 750  | 50   | 35    | 120  |

M0, T1 and T2 values are still not complete.

# Output

The output volumes will be nifti files in which every pixel will have a MR property value. For now only T2star, PD and susceptibility volumes can be created. T1 and Net Magnetization (M0) are currently being implemented.

# References 

[1] Wasserthal, J., Breit, H.-C., Meyer, M.T., Pradella, M., Hinck, D., Sauter, A.W., Heye, T., Boll, D., Cyriac, J., Yang, S., Bach, M., Segeroth, M., 2023. TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images. Radiology: Artificial Intelligence. https://doi.org/10.1148/ryai.230024 </br>
