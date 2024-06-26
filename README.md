# <div align="center">**Segmentation to MR Properties Converter**</div>

This repository will contain the code necessary for creating different (and selected) volumes whose values represent different MR useful properties: T2, T2 star, Proton Density and Susceptibility.

# Phantom Creation

This repository requires CT-labeled Nifti files. We use the output from Total Segmentator [1]. </br>
We implement an object-oriented python code that relies on the labels look up table from total segmentator. We implement 2 classes: Volume and Label. They have a parent-daughter relationship. The volume is the nifti file so we can access information from the header such as dimensions or voxel size and assign them as attributes to the Volume. Then we instance a label class for every unique label from the input, where MR properties are assigned as attributes such as: Proton Density, Net Magnetization, T1, T2, T2 star and susceptibility; as well as an identifying ID number and a name. We reduce the labels into groups based on their magnetic susceptibility. We group them based on susceptibility values as we want to create a new volume with susceptibility differences that will contribute to the image quality. 

# Input Nifti advanced option


# Look-up tables
Here we document the respective look-up tables used for assigning the MR property values


# Output

The output volumes will be nifti files in which every pixel will have a MR property value. For now only T2star, PD and susceptibility volumes can be created. T1 and Net Magnetization (M0) are currently being implemented.
# References 

[1] Wasserthal, J., Breit, H.-C., Meyer, M.T., Pradella, M., Hinck, D., Sauter, A.W., Heye, T., Boll, D., Cyriac, J., Yang, S., Bach, M., Segeroth, M., 2023. TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images. Radiology: Artificial Intelligence. https://doi.org/10.1148/ryai.230024 </br>
