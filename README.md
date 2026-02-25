# <div align="center">**Segmentation to MR Properties Converter**</div>

This repository contains the code required to generate quantitative magnetic resonance (MR) property volumes, including:

- **T1 relaxation maps (3T)**
- **T2 relaxation maps (3T)**
- **T2\* relaxation maps (3T)**
- **Relative permittivity maps (3T and 7T)**
- **Electrical conductivity maps (3T and 7T)**
- **Proton density maps**
- **Absolute magnetic susceptibility maps**

# Phantom Creation

All input segmentation files must follow the canonical label convention defined below.  
Each voxel in a segmentation file must contain one of the following integer IDs.

| Canonical ID | Tissue Name      |
|--------------|------------------|
| 0            | air              |
| 1            | heart            |
| 2            | liver            |
| 4            | kidney           |
| 5            | brain            |
| 6            | spleen           |
| 7            | cartilage        |
| 9            | muscle           |
| 10           | bone             |
| 11           | v_bone(vertebrae)|
| 12           | lungs            |
| 13           | trachea          |
| 14           | spinal_cord      |
| 18           | esophagus        |
| 19           | gland            |
| 100          | extra            |
| 101          | water            |
| 102          | organ            |
| 107          | tr_cartilage     |
| 113          | tr_lumen         |
| 196          | sc_wm            |
| 264          | fat              |
| 289          | sc_csf           |
| 324          | sc_gm            |

A parcellation color map for the canonical ID's can be used with ITK[1] available [here](parcellation_itk.txt)


---

## Tool 1: `seg_converter`

Different segmentation tools use different labeling conventions.  
To ensure consistency across datasets, this repository provides the `seg_converter` command line tool (CLI).

### Supported Segmentation Sources

Currently implemented:

- Total Segmentator CT [2]
- Total Segmentator MRI

### How It Works

1. The user provides:
   - The segmentation volume
   - The segmentation tool used to generate it

2. The tool:
   - Verifies that all voxel label IDs match the expected IDs for the selected segmentation tool.
   - Remaps the segmentation labels to the canonical label IDs.

3. If any voxel contains an unidentified label ID:
   - A binary mask is generated containing only those invalid voxels.
   - This mask allows the user to manually inspect and correct unexpected labels before proceeding.

This validation step ensures that all downstream MR property generation is physically consistent and reproducible.

---

## Tool 2: `tissue_to_MR`

Once a segmentation has been successfully remapped to the canonical label convention, it can be converted into quantitative MR property volumes using `tissue_to_MR` CLI.

### Purpose

`tissue_to_MR` transforms a canonical segmentation into a voxel-wise MR property map.

### Supported Properties

The user specifies which physical property to generate, including:

- T1 (3T)
- T2 (3T)
- T2*
- Relative permittivity (3T or 7T)
- Electrical conductivity (3T or 7T)
- Proton density
- Absolute magnetic susceptibility

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

All inputs and outputs are NIfTI volumes (`.nii` or `.nii.gz`).  
Unless otherwise specified, outputs are written as compressed NIfTI files (`.nii.gz`) inside the `output/` directory.

## `seg_converter`

Remaps a segmentation volume to the canonical label convention.

### Arguments

| Flag | Description | Options |
|------|------------|----------|
| `-i` | Input segmentation file | `.nii` or `.nii.gz` |
| `-s` | Segmentation tool used | `TotalSeg_CT`, `TotalSeg_MRI` |
| `-v` | Version of the segmentation labeling scheme | `v1`, `v2`, `mod0`, `mod1`, `mod2`|
| `-o` | Output remapped file | `.nii.gz` |


Example:

```
seg_converter -i data/input_file.nii.gz -s TotalSeg_CT -v v2 -o remapped_input_file.nii.gz
```


## `tissue_to_MR`

Converts a canonical segmentation volume into a quantitative MR property map by replacing each tissue label with its corresponding physical value.

### Arguments

| Flag | Description | Options |
|------|------------|---------|
| `-i` | Input canonical segmentation file | `.nii.gz` |
| `-t` | Property type to generate | `t2s`, `sus`, `pd`, `t1`, `t2`, `perm3T`, `cond3T`, `perm7T`, `cond7T` |
| `-g` | Apply Gaussian distribution in spinal cord WM and GM | `0` (disabled), `1` (enabled) |
| `-o` | Output filename | `.nii.gz` |

### Output

The generated MR property volume is saved in the `output/` directory.

If `-g 1` is enabled, voxel values within **spinal cord white matter (`sc_wm`)** and **spinal cord gray matter (`sc_gm`)** are sampled from a Gaussian (normal) distribution centered on the nominal property values. All other tissues are assigned fixed (deterministic) values.



# Look-Up Tables (LUT)

MR property values assigned to each tissue are derived from peer-reviewed literature.

Each physical property (T1, T2, T2*, susceptibility, permittivity, conductivity, etc.) has its own look-up table defined in the corresponding class within the codebase.

Below we document the literature sources used for parameter selection.


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
| lungs               | 1400    | 35.5    | 1.62     | 15     | -2.36 |
| trachea cartilage   | 1201    | 43.225      | 26.04       | 70      | -9.05 |
| trachea lumen       | 0.01    | 0.01      | 0.01       | 0.01      | 0.196 |
| air                 | 0.01    | 0.01    | 0.01     | 0.01   | 0.35  |
| extra (blood/muscle)| 800     | 50      | 35       | 50     | -9.04 |
| spinal_cord         | 936.5   | 76.75   | 40.07    | 60     | -9.055|
| water               | 2500    | 275     | 137.5    | 100    | -9.05 |
| CSF                 | 1953    | 275     | 137.5    | 100    | -9.05 |
| white_matter        | 887.7   | 65.4    | 35       | 70     | –     |
| gray_matter         | 1446.1  | 94.3    | 48       | 82     | –     |
| esophagus           | 1000    | 32      | 17       | 45     | -9.05 |
| organ (liver-like)  | 800     | 40      | 20       | 65     | -9.05 |
| gland (salivary)    | 1600    | 72      | 36       | 80     | -9.05 |
| sinus               | –       | –       | –        | –      | -     |
| inter_vert_discs    | 1201    | 42      | 26       | 50     | -9.055|


 

# References 
[1] Paul A. Yushkevich, Joseph Piven, Heather Cody Hazlett, Rachel Gimpel Smith, Sean Ho, James C. Gee, and Guido Gerig. User-guided 3D active contour segmentation of anatomical structures: Significantly improved efficiency and reliability. Neuroimage 2006 Jul 1;31(3):1116-28.
[2] Wasserthal, J., Breit, H.-C., Meyer, M.T., Pradella, M., Hinck, D., Sauter, A.W., Heye, T., Boll, D., Cyriac, J., Yang, S., Bach, M., Segeroth, M., 2023. TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images. Radiology: Artificial Intelligence. https://doi.org/10.1148/ryai.230024 </br>
