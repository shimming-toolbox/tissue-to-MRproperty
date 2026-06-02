#Dependencies
import numpy as np
from tissue2mrprop.functions.label import SegmentationLabel
import nibabel as nib
from tissue2mrprop.functions.utils.get_dic_values import to_csv_sus
import os
from tissue2mrprop.functions.utils.select_tool import new_return_dict_labels
from tissue2mrprop.conventions import CANONICAL_ID_TO_NAME


# Parent class for the creation of a non-finite biomechanical model of the body
class volume:
    
    def __init__(self, volume):
        # Tool and version as input arguments

        # In this version we correct that the output should be the nifti image
        # This way we can attribute the information from nifti files to the class

        self.nifti = volume # This points to a Nifti file
        # Given the input is ALWAYS a segmentation, we should open them as integers
        self.volume = self.nifti.get_fdata().astype(np.int32)
        self.dimensions = np.array(self.volume.shape) # It is initially a tuple, but it needs to be an array
        self.uniq_labels = np.unique(self.volume)
        self.segmentation_labels = {}
        self.grouped_labels = None
        self.sus_dist = None
        self.t2star_vol = None
        self.pd_dist = None
        self.t1_vol = None
        self.t2_vol = None
        self.static_vol = None
        #self.deltaB0 = np.zeros(self.dimensions)
        self.gaussian_phantom = None
        # The dictionary has keys for every id number and each value 
        # is the corresponding SegmentationLabel daughter class

        # to check ids depending on the tool selected
        self.look_up = {}
        # This is the Convention Dictionary for labels_id - names - sus_values
        self.relax_values = {}
        self.static_vals = {}
        self.static_vals_short = {}
        # This is a dictionary to get the relaxation values used in label.py

        # Now to get the dictionary of standard deviations
        self.std_devs = {}

        # Creating a dictionary that stores the counts for each label based on their name
        self.label_counts = {}
        self.label_gaussians = {}
        self.unique_counts = {}
        self.gauss_flag = 0

        self.gaussian_phantom = None

        # Creating folders for the code
        if not os.path.exists("output"):
            os.makedirs('output')
        if not os.path.exists('simulation'):
            os.makedirs('simulation')
        if not os.path.exists("data"):
            os.makedirs("data")

        self.magnitude = None
        self.phase = None
        self.real = None
        self.imaginary = None

        # For the fieldmap comparison project:
        self.new_chi = None

    def group_seg_labels(self, tool, version, in_fn):

        self.look_up = new_return_dict_labels(tool,version)

        for key, value in self.look_up.items():
            # Key is the number of ID and value is (name, new_id)
            name = value[0]
            new_id = value[1]

        # Now, check pixel integrity
        try:
            self.check_pixels(in_fn)
        except ValueError:
            return False
        return True

    def check_pixels(self, input_name):
        # Important to before going to conversion
        # If there is a pixel that is outside of range conversion won't work
        # because it won't be treated as a label but as a float
        flag = 0  # Flag to save in case there were changes
        volume_labels = self.uniq_labels
        valid_labels = np.array(list(self.look_up.keys()))
        # Now with lists instead of 3D arrays we can find any invalid labels
        invalid_labels = np.setdiff1d(volume_labels, valid_labels)

        if invalid_labels.size == 0:
            print("✅ All segmentation labels match the lookup table.")
            return True

        print("⚠️ Found labels not defined in selected tool:")
        print(invalid_labels)

        # Create mask of invalid voxels
        invalid_mask = np.isin(self.volume, invalid_labels)

        # Create output volume (only invalid labels kept)
        invalid_volume = np.zeros_like(self.volume)
        invalid_volume[invalid_mask] = self.volume[invalid_mask]

        # Save NIfTI
        tmp_img = nib.Nifti1Image(invalid_volume,header=self.nifti.header, affine=self.nifti.affine)

        if input_name.endswith(".nii.gz"):
            base_name = input_name[:-7]
            out_name = base_name + "_invalid_labels.nii.gz"
        elif input_name.endswith(".nii"):
            base_name = input_name[:-4]
            out_name = base_name + "_invalid_labels.nii.gz"
        else:
            out_name = "invalid_labels.nii.gz"
            print("Input filename not nifti or compressed nifit")

        out_path = os.path.join("output", out_name)
        nib.save(tmp_img, out_path)

        print(f"🚨 Invalid label map saved to: {out_path}")
        print("Please correct segmentation or select the appropriate tool.")

        raise ValueError("Segmentation contains labels incompatible with selected tool.")

    def create_new_grouped_labels(self):
        # Redefine volume to int so that we can use indexing
        # If we don't do this, we can't index with floats
        print("Checking type of volume:", type(self.volume))
        max_label = int(np.max(self.volume))
        lut = np.zeros(max_label+1, dtype=int)
        for key, (name, new_id) in self.look_up.items():
            if key <= max_label:
                print(f"Remapping label {name} to {new_id}")
                lut[key] = new_id # The second value of the tuple is the new id

        self.grouped_labels = lut[self.volume]
        return self.grouped_labels

# Initializing tissue2MR using Canonical list of label id-name

    def init_segmentation_labels_from_canonical(self):
        self.segmentation_labels = {}
        for lab_id in self.uniq_labels:
            lab_id = int(lab_id)
            lbl = SegmentationLabel(lab_id)

            if lab_id not in CANONICAL_ID_TO_NAME:
                raise ValueError(f"Label ID {lab_id} not found, check tool and version selected")
            name = CANONICAL_ID_TO_NAME[lab_id]
            lbl.set_name(name) # This enables us to call all tissue properties as attributes per label
            self.segmentation_labels[lab_id] = lbl

        # At the end of the loop segmentation_labels has a Label object indexed by the canonical IDs!

        # Additionally, getting relax and static values from any segmentation label
        self.relax_values = next(
            iter(self.segmentation_labels.values())).relax_values if self.segmentation_labels else {}
        self.static_vals_short = next(
            iter(self.segmentation_labels.values())).static_values_short if self.segmentation_labels else {}
        self.static_vals = next(
            iter(self.segmentation_labels.values())).static_values if self.segmentation_labels else {}

# Core function for creating new volumes without having to use 3 for loops
    def _lut_from_label_attr(self, attr_name:str, default_value:float, dtype=np.float32):
        """
        Builds a LUT mapping label_id -> attribute value then returns the mapped volume
        attr_name examples: susceptibility, T1_val, T2star_val, PD_val, T2_val
        """
        max_label = int(self.volume.max())
        lut = np.full(max_label+1, default_value, dtype=dtype)

        # Now iterate only over unique labels present (faster)
        for lab_id in self.uniq_labels:
            lab_id = int(lab_id)
            lbl = self.segmentation_labels.get(lab_id, None)
            if lbl is None:
                continue
            val = getattr(lbl, attr_name, None)
            # None in case we get missing attributes or if typo on attr_name
            if val is None:
                continue
            lut[lab_id] = float(val)

        return lut[self.volume]

# Create new volume house function
    def create_type_vol(self, mrprop, output_name="default"):
        # This function is for the CLI app
        # Depending on the type we automatically call the specific function
        # Piece-wise mode: on :P
        if mrprop == 'sus':
            self.sus_dist = self._lut_from_label_attr(
                attr_name="susceptibility",
                default_value=-9.05,  # In case None is found on a label's chi value
                dtype=np.float32
            )
            self.save_sus_dist(output_name)
        elif mrprop == 't2s':
            self.t2star_vol = self._lut_from_label_attr(
                attr_name="T2star_val",
                default_value=0,  # In case None is found on a label's T2star value
                dtype=np.float32
            )
            self.save_t2star_dist(output_name)
        elif mrprop == 'pd':
            self.pd_dist= self._lut_from_label_attr(
                attr_name="PD_val",
                default_value=0,  # In case None is found on a label's PD value
                dtype=np.float32
            )
            self.save_pd_dist(output_name)
        elif mrprop == 't1':
            self.t1_vol = self._lut_from_label_attr(
                attr_name="T1_val",
                default_value=0,  # In case None is found on a label's T1 value
                dtype=np.float32
            )
            self.save_t1_dist(output_name)
        elif mrprop == 't2':
            self.t2_vol = self._lut_from_label_attr(
                attr_name="T2_val",
                default_value=0,  # In case None is found on a label's T2 value
                dtype=np.float32
            )
            self.save_t2_dist(output_name)

        elif mrprop in ('perm3T', 'cond3T', 'perm7T', 'cond7T'):
            self.create_static_vol(mrprop)
            self.save_static_vol(mrprop, output_name)
        else:
            raise ValueError(f"Unknown property: {mrprop}")

    def save_sus_dist(self, fn):
        if self.gauss_flag:
            data = self.gaussian_phantom
        else:
            data = self.sus_dist
        tmp_img = nib.Nifti1Image(data, affine=self.nifti.affine)

        if fn == "default":
            fn = 'sus_dist.nii.gz'
        if self.gauss_flag:
            fn = "gauss_" + fn
        path = os.path.join('output', fn)
        nib.save(tmp_img,path)

        del tmp_img
        return path

    def save_t1_dist(self, fn = "default"):
        if self.gauss_flag:
            data = self.gaussian_phantom
        else:
            data = self.t1_vol
        tmp_img = nib.Nifti1Image(data, affine=self.nifti.affine)

        if fn == "default":
            fn = 't1_dist.nii.gz'
        if self.gauss_flag:
            fn = "gauss_" + fn
        path = os.path.join('output', fn)
        nib.save(tmp_img,path)

        del tmp_img
        return path

    def save_pd_dist(self, fn = 'default'):
        if self.gauss_flag:
            data = self.gaussian_phantom
        else:
            data = self.pd_dist
        tmp_img = nib.Nifti1Image(data, affine=self.nifti.affine)

        if fn == "default":
            fn = 'pd_dist.nii.gz'
        if self.gauss_flag:
            fn = "gauss_" + fn
        path = os.path.join('output', fn)
        nib.save(tmp_img,path)

        del tmp_img
        return path

    def save_t2star_dist(self, fn = "default"):
        if self.gauss_flag:
            data = self.gaussian_phantom
        else:
            data = self.t2star_vol
        tmp_img = nib.Nifti1Image(data, affine=self.nifti.affine)

        if fn == "default":
            fn = 't2_star.nii.gz'
        if self.gauss_flag:
            fn = "gauss_" + fn
        path = os.path.join('output', fn)
        nib.save(tmp_img,path)

        del tmp_img
        return path

    def save_t2_dist(self, fn = "default"):
        if self.gauss_flag:
            data = self.gaussian_phantom
        else:
            data = self.t2_vol
        tmp_img = nib.Nifti1Image(data, affine=self.nifti.affine)

        if fn == "default":
            fn = 't2_dist.nii.gz'
        if self.gauss_flag:
                fn = "gauss_" + fn
        path = os.path.join('output', fn)
        nib.save(tmp_img,path)

        del tmp_img
        return path

    def create_static_vol(self, mrprop):
        attr_map = {
            "perm3T": "perm3T",
            "cond3T": "cond3T",
            "perm7T": "perm7T",
            "cond7T": "cond7T",
        }

        if mrprop not in attr_map:
            raise ValueError(f"Unknown static type: {mrprop}")

        attr_name = attr_map[mrprop]

        # Undefined values default to 0
        self.static_vol = self._lut_from_label_attr(
            attr_name=attr_name,
            default_value=0.0,
            dtype=np.float32
        )
        return self.static_vol

    def save_static_vol(self, mrprop, fn="default"):
        if self.gauss_flag:
            data = self.gaussian_phantom
        else:
            data = self.static_vol
        tmp_img = nib.Nifti1Image(data, affine=self.nifti.affine)

        if fn == "default":
            fn = f"{mrprop}.nii.gz"
        if self.gauss_flag:
            fn = "gauss_" + fn
        path = os.path.join('output', fn)
        nib.save(tmp_img, path)

        del tmp_img
        return path

# CSV related functions (on development)
    def save_sus_csv(self):
        data = []
        for i in self.segmentation_labels.keys():
            label = self.segmentation_labels[i]
            if label.name is not None and label.susceptibility is not None and label.name not in data:
                # The last is to get unique names 
                data.append({
                    "Name": label.name,
                    "Susceptibility": label.susceptibility
                })
        # Call funtion that creates CSV
        path = os.path.join('data','susceptibility_values.csv')
        to_csv_sus(data,path)

    def save_relax_csv(self):
        # Further implementation to go through self.relax values of each label?
        # Think about a more efficient way because the user should be able to change the values
        # It might be usefull to get this inputs from different researchers and testing
        pass

# Gaussian related functions
    def calc_regions(self):
        # For  creating a gaussian distribution we need to group and count every label
        # Must be run after defining a tool in group_seg_labels
        self.gaussian_phantom = np.zeros(self.dimensions, dtype=np.float32)

        unique_labels, counts = np.unique(self.volume, return_counts=True)
        self.unique_counts = dict(zip(unique_labels,counts))

        std_regions_of_interest = ["sc_wm", "sc_gm"]

        if not self.look_up:
            print("Please define a tool for a lookup table")
            return

        self.label_counts = {}

        for lab_id, count in self.unique_counts.items():
            lab_id = int(lab_id)
            if lab_id not in self.look_up:
                continue
            label_name = self.look_up[lab_id][0]
            if label_name in std_regions_of_interest:
                self.label_counts[label_name] = self.label_counts.get(label_name, 0) + int(count)

        for name, count in sorted(self.label_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"Label name: {name}: {count} pixels")

    def create_gauss_sc_dist(self, prop):
        std_values = {
            "sus": {"sc_wm": 0.0104, "sc_gm": 0.031}, # => Avg taken from regions 1 through 7 of QSM RC2 paper (Deep gray matter) and WM
            "t2s": {"sc_wm": 4.6875, "sc_gm": 3.688}, # For WM we use: https://pmc.ncbi.nlm.nih.gov/articles/PMC3508464
            # For GM we use downscaled T2* values from QSM RC2 phantom as no 3T data was found, at 7T average was 9.757 ms
            # Values of t2s @ 7T where: for WM: 12.4 ms and for GM: 9.757 (from QSM RC2 in-vivo maps)
            "t2": {"sc_wm": 8.725, "sc_gm": 14.935}, # Using sub-MKP611 from https://openneuro.org/datasets/ds004611/versions/1.0.2
            "t1": {"sc_wm": 106.15, "sc_gm": 114.895}, # Using sub-MKP611 from https://openneuro.org/datasets/ds004611/versions/1.0.2
            "pd": {"sc_wm": 5.54, "sc_gm": 6.95}, # Same as M0 for now
            "M0": {"sc_wm": 13.41, "sc_gm": 16.83}, # => Avg taken from regions 1 through 7 of QSM RC2 paper (Deep gray matter) for GM and WM
            # STD values for the following properties still need to be added
            "perm3T": {"sc_wm": 0.01, "sc_gm": 0.01},
            "cond3T": {"sc_wm": 0.01, "sc_gm": 0.01},
            "perm7T": {"sc_wm": 0.01, "sc_gm": 0.01},
            "cond7T": {"sc_wm": 0.01, "sc_gm": 0.01}
        }
        # WM values come from corpus callosum
        # GM values come from Deep Gray Matter regions in the brain
        # M0 values got from QSM RC2 need to be re-scaled because the values range from 0 to XX
        # Using a brain mask on QSM RC2 phantom, max_QSM_RC2_phantom_M0 = 242
        # If the PD max is 100 we can use the following scaling factor:
        # scaling_for_PD = max(PD)/max(M0)
        # Which results in 100/242 = 0.413
        # PD_std = M0_std*0.413

        # ---------- Step 1: piecewise base ----------
        print("Step1 for Texture. Populate phantom with piecewise values")
        # Build property LUT over label IDs present
        max_label = int(self.volume.max())
        base = np.zeros(max_label + 1, dtype=np.float32)

        # index mapping for relax_values
        idx_map = {"sus":0, "t1": 1, "t2": 2, "t2s": 3, "pd": 4}
        idx_static_map = {"perm3T":0, "cond3T":1, "perm7T":2, "cond7T":3}

        for lab_id in self.uniq_labels:
            lab_id = int(lab_id)
            lbl = self.segmentation_labels.get(lab_id, None)
            if lbl is None:
                continue
            name = lbl.name

            if prop == "sus":
                val = lbl.susceptibility
                if val is None:
                    val = -9.05  # keep your fallback
            else:
                # assumes relax_values available and name exists there
                if prop in ("perm3T", "cond3T", "perm7T", "cond7T"):
                    # Eventually when mapped completely, replace with
                    # self.static_vals
                    val = self.static_vals_short[name][idx_static_map[prop]]
                else:
                    val = self.relax_values[name][idx_map[prop]]

            base[lab_id] = float(val)

        self.gaussian_phantom = base[self.volume].astype(np.float32)

        # ---------- Step 2&3: gaussian on sc_wm + sc_gm ----------
        print("Step2 for Texture. Calculate gaussian distribution for sc_wm and sc_gm")
        # Make masks by canonical IDs (fast)
        # Here: derive IDs from label objects (robust).
        sc_ids = {}
        for lab_id in self.uniq_labels:
            lab_id = int(lab_id)
            lbl = self.segmentation_labels.get(lab_id, None)
            if lbl and lbl.name in ("sc_wm", "sc_gm"):
                sc_ids[lbl.name] = lab_id

        rng = np.random.default_rng()  # optionally pass a seed for reproducibility

        for name in ("sc_wm", "sc_gm"):
            if name not in sc_ids:
                continue
            lab_id = sc_ids[name]
            mask = (self.volume == lab_id)
            n = int(mask.sum())
            if n == 0:
                continue

            mean_val = float(base[lab_id])
            std = float(std_values.get(prop, {}).get(name, 0.0))

            print(f"Applying Gaussian noise to {name} | prop={prop} | mean={mean_val} | std={std} | n={n}")

            if std > 0:
                self.gaussian_phantom[mask] = rng.normal(loc=mean_val, scale=std, size=n).astype(np.float32)
            else:
                self.gaussian_phantom[mask] = mean_val

        return self.gaussian_phantom

    def save_gauss_dist(self, mrprop, out_fn = "default"):
        #Saving the gaussian distribution with type defined
        # This must be run ONLY after creating the create_property.
        # If not it will automatically save the empty array
        self.gauss_flag = 1
        if mrprop == 'sus':
            self.save_sus_dist(out_fn)

        elif mrprop == 't2s':
            self.save_t2star_dist(out_fn)

        elif mrprop == 'pd':
            self.save_pd_dist(out_fn)

        elif mrprop == 't1':
            self.save_t1_dist(out_fn)

        elif mrprop == 't2':
            self.save_t2_dist(out_fn)

        elif mrprop in ("perm3T", "cond3T", "perm7T", "cond7T"):
            self.save_static_vol(out_fn)

    def check_labels(self):
        for i in self.uniq_labels:
            if self.segmentation_labels[i].name == None:
                print("Label: ",self.segmentation_labels[i]["name"]," doesn't have name assigned")
    def set_label_susceptibility(self, label_id, susceptibility):
        ids = self.look_up.keys()
        if label_id in ids:
            self.segmentation_labels[label_id].set_susceptibility(susceptibility)
        else:
            print(f"Label ID {label_id} not found.")
            exit()
    def set_T1(self, label_id, t1):
        ids = self.look_up.keys()
        if label_id in ids:
            self.segmentation_labels[label_id].set_t2star_val(t1)
        else:
            print(f"Label ID {label_id} not found.")
            exit()
    def set_label_pd(self,label_id,pd):
        ids = self.look_up.keys()
        if label_id in ids:
            self.segmentation_labels[label_id].set_pd_val(pd)
        else: print(f"Label ID {label_id} not found.")
    def set_T2star(self, label_id, t2star):
        ids = self.look_up.keys()
        if label_id in ids:
            self.segmentation_labels[label_id].set_t2star_val(t2star)
        else:
            print(f"Label ID {label_id} not found.")
    def manual_label(self,id,name,sus):
        if id in self.uniq_labels:
            label = self.segmentation_labels[id]
            label.name = name
            label.sus = sus
    def show_labels(self):
        for i in self.segmentation_labels:
            label = self.segmentation_labels[i]
            print(label) # Calling __str__ from label


    def __repr__(self):
        return f"SegmentationLabelManager == Volume"
