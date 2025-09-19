#Dependencies
import numpy as np
from functions.label import SegmentationLabel
import nibabel as nib
from functions.utils.get_dic_values import to_csv_sus
import os
from functions.utils.select_tool import return_dict_labels
#from skimage.measure import label, regionprops

# Parent class for the creation of a non-finite biomechanical model of the body
class volume:
    
    def __init__(self, volume):
        # Tool and version as input arguments

        # In this version we correct that the output should be the nifti image
        # This way we can attribute the information from nifti files to the class

        self.nifti = volume # This points to a Nifti file
        self.volume = self.nifti.get_fdata()
        self.dimensions = np.array(self.volume.shape) # It is initially a tuple, but it needs to be an array
        self.uniq_labels = np.unique(self.volume)
        self.segmentation_labels = {}
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

    def group_seg_labels(self, tool, version, type, ref):
        #self.look_up = return_dict_labels(tool,version)
        # For the fieldmap comparison project
        if tool == "compare_fm" and version == "dyn":
            # If the version is dynamic
            # The new value will replace None
            # We can check just in case
            self.look_up = return_dict_labels(tool,version, new_chi = self.new_chi)
        else:
            self.look_up = return_dict_labels(tool,version)

        # Function to get the relaxation values from label
        for i in self.look_up.keys():
            self.segmentation_labels[i] = SegmentationLabel(i)

        for key, value in self.look_up.items():
            # Key is the number of ID and value is (name, sus)
            name = value[0]
            sus = value[1]

            if ref != 0:
                new_sus = sus - ref
                self.set_label_susceptibility(key, new_sus)

            self.set_label_name(key, name, type)
            self.set_label_susceptibility(key, sus)

            if type == "sus":
                print(name, " Chi:", sus)
            if type == "pd":
                print(name, " PD:", self.segmentation_labels[key].PD_val)
            if type == "t2s":
                print(name, " T2s:", self.segmentation_labels[key].T2star_val)
            if type == "t1":
                print(name, " T1:", self.segmentation_labels[key].T1_val)
            if type == "t2":
                print(name, " T2:", self.segmentation_labels[key].T2_val)
            if type == "perm3T":
                print(name, " Permittivity@3T:", self.segmentation_labels[key].perm3T)
            if type == "cond3T":
                print(name, " Conductivity @3T:", self.segmentation_labels[key].cond3T)
            if type == "perm7T":
                print(name, " Permittivity @7T:", self.segmentation_labels[key].perm7T)
            if type == "cond7T":
                print(name, " Permittivity @7T:", self.segmentation_labels[key].cond7T)

        # Getting the relax values dictionary from any label
        self.relax_values = self.segmentation_labels[0].relax_values
        self.static_vals = self.segmentation_labels[0].static_values_short

    def check_labels(self):
        for i in self.uniq_labels:
            if self.segmentation_labels[i].name == None:
                print("Label: ",self.segmentation_labels[i]["name"]," doesn't have name assigned")

    def set_label_name(self, label_id, name, type):
        '''
        This is the most important set function, as this function enables the calling the tissue properties as attributes
        if and only if the label is found in the ids
        '''
        ids = self.look_up.keys()
        if label_id in ids:
            if type == "perm3T" or type == "cond3T" or type == "perm7T" or type == "cond7T":
                self.segmentation_labels[label_id].set_static_name(name)

            self.segmentation_labels[label_id].set_name(name)
        else:
            print(f"Label ID {label_id} not found, check version selected")
            exit()

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

    def create_type_vol(self, type, output_name="default"):
        # This function is for the CLI app
        # Depending on the type we automatically call the specific function
        # Piece-wise mode: on :P
        if type == 'sus':
            self.create_sus_dist()
            self.save_sus_dist_nii(output_name)
        if type == 't2s':
            self.create_t2_star_vol()
            self.save_t2star_dist(output_name)
        if type == 'pd':
            self.create_pd_vol()
            self.save_pd_dist(output_name)
        if type == 't1':
            self.create_t1_vol()
            self.save_t1_dist(output_name)
        if type == 't2':
            print("T2 volume comming soon!")

        if type == 'perm3T' or type == 'cond3T' or type == 'perm7T' or type == 'cond7T':
            self.create_static_vol(type)
            self.save_static_vol(type, output_name)



    def check_pixels(self,input_name):
        # Important to before going to conversion
        # If there is a pixel that is outside of range conversion won't work
        # because it won't be treated as a label but as a float
        flag = 0  # Flag to save in case there were changes
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):

                    pixel = self.volume[i, j, k]

                    if pixel not in self.look_up.keys():

                        flag = 1
                        print(f"Pixel with wrong value: {pixel} located at {i,j,k}")
                        print("(indexed from [0,0,0])")
                        rem = str(input("Do you want to delete the pixel? [Y] [n]: "))
                        print("[Y] continues checking pixels, [n] lets you edit it")

                        if rem == "n":
                            print("Maybe you want to change the value?")
                            rem2 = int(input("Choose the value: "))

                            if rem2 in self.segmentation_labels:
                                print("Changed value to: ", rem2)
                                self.volume[i, j, k] = rem2

                            else:
                                print("Number not in look up table")
                                return 1

                        if rem == "Y" or rem == "y":
                            self.volume[i, j, k] = 0

        else:

            if flag == 1:

                print("Saving corrected volume for later usage!")
                tmp_img = nib.Nifti1Image(self.volume, affine = self.nifti.affine)
                if input_name.endswith(".nii.gz"):  # Maybe code for .nii later (not urgent)
                    base_name = input_name[:-7]  # Remove the `.nii.gz`
                    extension = ".nii.gz"
                out_name = base_name + "corrected_pixels.nii.gz"
                path = os.path.join('output', out_name)
                nib.save(tmp_img,path)
                del tmp_img
                del path
                return 0

            else:
                print("Input has correct pixel integrity!")
                return 0

    def create_sus_dist(self):
        # Code for create a susceptibility distribution volume
        # Using the label class
        self.sus_dist = np.zeros(self.dimensions)
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):

                    pixel = self.volume[i,j,k]

                    label = self.segmentation_labels[pixel]
                    suscep = label.susceptibility

                    if suscep == None:
                        # THis means the label is not defined
                        # The only not defined labels are organs
                        # We can consider the suscp of water
                        self.sus_dist[i,j,k] = -9.05
                    else:
                        self.sus_dist[i,j,k] = suscep

        return self.sus_dist

    def save_sus_dist_nii(self, fn):
        # Method to save the susceptibility distribution created to nifti
        if self.gauss_flag:
            temp_img = nib.Nifti1Image(self.gaussian_phantom, affine=self.nifti.affine)
            g_str = "gauss"
        else:
            temp_img = nib.Nifti1Image(self.sus_dist, affine=self.nifti.affine)

        if fn == "default":
            fn = 'sus_dist.nii.gz'
            if self.gauss_flag:
                fn = "gauss_" + fn
            # Conditioning if gauss flag is active, if not. We use the susceptibility np array
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img,path)
        else:
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img,path)

        del temp_img
        del path

    def create_static_vol(self, type):

        self.static_vol = np.zeros(self.dimensions)
        # Recall the type will tell us what index to take from the perm&cond dictionary

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):

                    pixel = self.volume[i,j,k]

                    label = self.segmentation_labels[pixel]

                    if type == "perm3T":
                        stat = label.perm3T
                        self.static_vol[i, j, k] = stat

                    if type == "cond3T":
                        stat = label.cond3T
                        self.static_vol[i, j, k] = stat

                    if type == "perm7T":
                        stat = label.perm7T
                        self.static_vol[i, j, k] = stat

                    if type == "cond7T":
                        stat = label.cond7T
                        self.static_vol[i, j, k] = stat

                    #else:
                        #print(f"Label {label} doesn't have a Perm or Cond value associated, check dictionary")
                        #exit()

        return self.static_vol

    def save_static_vol(self, type, fn="default"):
        # Method to save the Perm or Cond vol created to nifti
        if self.gauss_flag:
            temp_img = nib.Nifti1Image(self.gaussian_phantom, affine=self.nifti.affine)
            g_str = "gauss"
        else:
            temp_img = nib.Nifti1Image(self.static_vol, affine=self.nifti.affine)

        if fn == "default":
            fn = type+'.nii.gz'
            if self.gauss_flag:
                fn = "gauss_" + fn
            # Conditioning if gauss flag is active, if not. We use the static_vol np array
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img, path)
        else:
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img, path)

        del temp_img
        del path

    def create_t1_vol(self):
        self.t1_vol = np.zeros(self.dimensions)
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):
                    pixel = self.volume[i,j,k]
                    label = self.segmentation_labels[pixel]
                    val_t1 = label.T1_val
                    if val_t1 == None:
                        print("Label: ",label.name," does not have T1 value")
                        self.t1_vol[i,j,k] = 0
                    else:
                        self.t1_vol[i, j, k] = val_t1
        return self.t1_vol

    def save_t1_dist(self, fn = "default"):
        # Method to save T1 volume created to nifti
        if self.gauss_flag:
            temp_img = nib.Nifti1Image(self.gaussian_phantom, affine=self.nifti.affine)
        else:
            temp_img = nib.Nifti1Image(self.t1_vol, affine=self.nifti.affine)

        if fn == "default":
            fn = 't1_dist.nii.gz'
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            nib.save(temp_img,path)
        else:
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            nib.save(temp_img,path)
        del temp_img
        del path

    def create_pd_vol(self):
        # This method will use the lookup table of PD values to create a new volume
        # This new volume will use the labels to quickly create a volume with ProtonDensity values
        self.pd_dist = np.zeros(self.dimensions)
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):

                    pixel = self.volume[i,j,k]
                    label = self.segmentation_labels[pixel]
                    pd = label.PD_val
                    if pd == None:
                        # THis means the label does not have PD defined
                        self.pd_dist[i,j,k] = 0
                    else:
                        # If the label has PD value it will put this value on the volume
                        self.pd_dist[i,j,k] = pd

        return self.pd_dist
    def save_pd_dist(self, fn = 'default'):
        # Method to save the proton density distribution created to nifti
        if self.gauss_flag:
            temp_img = nib.Nifti1Image(self.gaussian_phantom, affine=self.nifti.affine)
        else:
            temp_img = nib.Nifti1Image(self.pd_dist, affine=self.nifti.affine)

        if fn == "default":
            fn = 'pd_dist.nii.gz'
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img,path)
        else:
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img,path)
        del temp_img
        del path

    def create_t2_star_vol(self):
        # This method will use the lookup table of T2 star values to create a new volume
        # This new volume will use the labels to quickly create a volume with relaxation time
        self.t2star_vol = np.zeros(self.dimensions)
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):

                    pixel = self.volume[i,j,k]
                    label = self.segmentation_labels[pixel]
                    t2star = label.T2star_val
                    if t2star == None:
                        # THis means the label does not have T2 star value defined
                        self.t2star_vol[i,j,k] = 0.001
                    else:
                        # If the label has value it will put this value on the volume
                        self.t2star_vol[i,j,k] = t2star

        return self.t2star_vol
    def save_t2star_dist(self, fn = "default"):
        # Method to save the volume with T2 star values  created to nifti
        if self.gauss_flag:
            temp_img = nib.Nifti1Image(self.gaussian_phantom, affine=self.nifti.affine)
        else:
            temp_img = nib.Nifti1Image(self.t2star_vol, affine=self.nifti.affine)

        if fn == "default":
            fn = 't2_star.nii.gz'
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img,path)
        else:
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img,path)
        del temp_img
        del path

    def create_t2_vol(self):
        # This method will use the lookup table of T2 star values to create a new volume
        # This new volume will use the labels to quickly create a volume with relaxation time
        self.t2_vol = np.zeros(self.dimensions)
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):

                    pixel = self.volume[i, j, k]
                    label = self.segmentation_labels[pixel]
                    t2val = label.T2_val
                    if t2val == None:
                        # THis means the label does not have T2 defined
                        self.t2_vol[i, j, k] = 0.001
                    else:
                        # If the label has value it will put this value on the volume
                        self.t2_vol[i, j, k] = t2val

        return self.t2_vol

    def save_t2_dist(self, fn = "default"):
        # Method to save the volume with T2 star values  created to nifti
        if self.gauss_flag:
            temp_img = nib.Nifti1Image(self.gaussian_phantom, affine=self.nifti.affine)
        else:
            temp_img = nib.Nifti1Image(self.t2_vol, affine=self.nifti.affine)

        if fn == "default":
            fn = 't2_map.nii.gz'
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img,path)
        else:
            if self.gauss_flag:
                fn = "gauss_" + fn
            path = os.path.join('output', fn)
            # Save the new NIfTI image to a file
            nib.save(temp_img,path)
        del temp_img
        del path
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

    def calc_regions(self):
        # For  creating a gaussian distribution we need to group and count every label
        # Must be run after defining a tool in group_seg_labels
        self.gaussian_phantom = np.zeros(self.dimensions)
        unique_labels, counts = np.unique(self.volume, return_counts=True)
        self.unique_counts = dict(zip(unique_labels,counts))

        std_regions_of_interest = ["sc_wm", "sc_gm"]

        if self.look_up is {}:
            print("Please define a tool for a lookup table")

        else:
            for l, count in self.unique_counts.items():
                #label_id = l
                label_name = self.look_up[l][0]
                #label_suscep = self.look_up[l][1]
                # Filter only for SC wm and gm
                if label_name == std_regions_of_interest[0] or std_regions_of_interest[1]:
                    if label_name in self.label_counts.keys():
                        self.label_counts[label_name] += count
                    else:
                        self.label_counts[label_name] = count

        # Now depending on the tool used we grouped them up
        # And for visualizing, sorting might be good
        sorted_label_counts = sorted(self.label_counts.items(), key=lambda item: item[1], reverse=True)

        # Now should only show SC gm and wm
        for name, count in sorted_label_counts:
            # Display the pixel count per label
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
            "M0": {"sc_wm": 13.41, "sc_gm": 16.83} # => Avg taken from regions 1 through 7 of QSM RC2 paper (Deep gray matter) for GM and WM
        }
        # WM values come from corpus callosum
        # GM values come from Deep Gray Matter regions in the brain
        # M0 values got from QSM RC2 need to be re-scaled because the values range from 0 to XX
        # Using a brain mask on QSM RC2 phantom, max_QSM_RC2_phantom_M0 = 242
        # If the PD max is 100 we can use the following scaling factor:
        # scaling_for_PD = max(PD)/max(M0)
        # Which results in 100/242 = 0.413
        # PD_std = M0_std*0.413

        print("Step1 for Texture. Populate phantom with piecewise values")
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):
                    pixel = self.volume[i, j, k]
                    label = self.segmentation_labels[pixel]
                    l_name = label.name

                    # Determine the property value based on the input prop
                    if prop == "sus":
                        property_value = label.susceptibility
                    else:
                        property_value = self.relax_values[l_name][{
                            "t2s": 3, "t2": 2, "t1": 1, "pd": 4, "M0": 1
                        }[prop]]

                    # Assign the piecewise value directly
                    self.gaussian_phantom[i, j, k] = property_value

        # Step 2: Apply gaussian distribution only to sc_wm and gm

        print("Step2 for Texture. Calculate gaussian distribution for sc_wm and sc_gm")
        for l, count in self.unique_counts.items():
            #label_id = l
            label_name = self.look_up[l][0]
            label_sus = self.look_up[l][1]
            # Determine the property value based on the input prop

            if label_name in ["sc_wm", "sc_gm"]:
                if prop == "sus":
                    property_value = label_sus
                else:
                    property_value = self.relax_values[label_name][{
                        "t2s": 3, "t2": 2, "t1": 1, "pd": 4, "M0": 1
                    }[prop]]
                std_dev = std_values.get(prop, {}).get(label_name, 0)
                print(f"Applying Gaussian noise to {label_name} with STD: {std_dev}")

                print(f"Label: {label_name} | Property: {prop} | Mean Value: {property_value} | STD: {std_dev}")

                self.label_gaussians[l] = self.calc_gauss(
                num_pixels=count,
                value = property_value,
                mr_prop=prop,
                std_dev=std_dev
                )
        # Step 3 for Texture. Replacing with gaussian values only in SC WM and SC GM
        print("Creating gaussian phantom -> longer for big files")

        # Optimized Gaussian Phantom Creation Loop
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):
                    pixel = self.volume[i, j, k]
                    lab_id = self.segmentation_labels[pixel].label_id
                    # Only apply Gaussian if it is sc_wm or sc_gm
                    if lab_id in self.label_gaussians:
                        gaussian_values = self.label_gaussians[lab_id]
                        value = np.random.choice(gaussian_values)
                        self.gaussian_phantom[i, j, k] = value

    def create_gauss_dist(self,prop):
        '''
        This is an old function S.R. implemented to add gaussian distribution to all labels
        It could be deleted, but I'm leaving here in case eventually we want to use it again
        Args:
            prop:

        Returns:

        '''
        # For input restrictions of type, see Segmentation Label

        for l, count in self.unique_counts.items():
            # get the MR property desired
            # l is the name (as a str) of the label
            l_name = self.look_up[l][0]

            if l_name not in ["sc_wm", "sc_gm"]:
                continue  # Skip labels other than sc_wm and sc_gm

            if prop == "sus":
                property_value = self.look_up[l][1]
                #l_name = self.look_up[l][0]
                #property = self.look_up[l][1]
                #SD = self.std_devs[l_name]
                sc_wm_std = 0.0145 # [ppm] => Similar to corpus callosum
                sc_gm_std = 0.031 # [ppm]

                if l_name == "sc_wm":
                    print(f"STD of Chi of {l_name}: {sc_wm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_wm_std)
                if l_name == "sc_gm":
                    print(f"STD of Chi of {l_name}: {sc_gm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_gm_std)

            if prop == "t2s":
                l_name = self.look_up[l][0]
                property = self.relax_values[l_name][3]
                #SD = self.std_devs[l_name]
                sc_wm_std = 5.4 # [ms]
                sc_gm_std = 5.6 # [ms]

                if l_name == "sc_wm":
                    print(f"STD of T2* of {l_name}: {sc_wm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_wm_std)
                if l_name == "sc_gm":
                    print(f"STD of T2* of {l_name}: {sc_gm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_gm_std)

            if prop == "t2":
                l_name = self.look_up[l][0]
                property = self.relax_values[l_name][2]
                #SD = self.std_devs[l_name]
                sc_wm_std = 5.4  # [ms]
                sc_gm_std = 5.6  # [ms]

                if l_name == "sc_wm":
                    print(f"STD of T2 (same as T2*) of {l_name}: {sc_wm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_wm_std)
                if l_name == "sc_gm":
                    print(f"STD of T2 (same as T2*) of {l_name}: {sc_gm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_gm_std)

            if prop == "t1":
                l_name = self.look_up[l][0]
                property = self.relax_values[l_name][1]
                #SD = self.std_devs[l_name]
                sc_wm_std = 42  # [ms]
                sc_gm_std = 44  # [ms]
                if l_name == "sc_wm":
                    print(f"STD of T1 of {l_name}: {sc_wm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_wm_std)
                if l_name == "sc_gm":
                    print(f"STD of T1 of {l_name}: {sc_gm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_gm_std)

            if prop == "pd":
                l_name = self.look_up[l][0]
                property = self.relax_values[l_name][4]
                #SD = self.std_devs[l_name]
                sc_wm_std = 22.31  # [ms]
                sc_gm_std = 16.83  # [ms]
                if l_name == "sc_wm":
                    print(f"STD of PD of {l_name}: {sc_wm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_wm_std)
                if l_name == "sc_gm":
                    print(f"STD of PD of {l_name}: {sc_gm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_gm_std)

            if prop == "M0":
                l_name = self.look_up[l][0]
                property = self.relax_values[l_name][1]
                #SD = self.std_devs[l_name]
                sc_wm_std = 22.31  # [ms] => Similar to corpus callosum
                sc_gm_std = 16.83  # [ms] => Avg taken from regions 1 through 7 of QSM RC2 paper (Deep gray matter)

                if l_name == "sc_wm":
                    print(f"STD of T1 of {l_name}: {sc_wm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_wm_std)
                if l_name == "sc_gm":
                    print(f"STD of T1 of {l_name}: {sc_gm_std}")
                    self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value=property, mr_prop=prop,
                                                              std_dev=sc_gm_std)



            # This way for every label we have a gaussian distribution

        print("Creating gaussian phantom -> longer for big files")
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):

                    pixel = self.volume[i,j,k]
                    # Now we need the ID of the label from pixel so
                    lab_id = self.segmentation_labels[pixel].label_id
                    # Instead of getting the name of the label we get the label id
                    # Because label gaussian is created per label
                    # Now randomly select a value from the gaussian distribution
                    gaussian_values = self.label_gaussians[lab_id]
                    value = np.random.choice(gaussian_values)
                    self.gaussian_phantom[i,j,k] = value

        print("Finished creating gaussian distributed, based on: ", prop)
        # Lastly add the gaussian phantom to a Nifti
        # And save it to output folder
    def calc_gauss(self, value, num_pixels, mr_prop, std_dev):
        val = np.random.normal(value, std_dev, num_pixels)
        # In areas close to 0, the gaussian distribution must always return positive values
        # It is not possible to have negative T1, T2, T2s or PD. But susceptibility can be negative
        if mr_prop == "sus":
            return val
        else:
            abs_val = np.abs(val)
            return abs_val

    def save_gauss_dist(self, type, out_fn = "default"):
        #Saving the gaussian distribution with type defined
        # This must be run ONLY after creating the create_property.
        # If not it will automatically save the empty array
        self.gauss_flag = 1
        if type == 'sus':
            self.save_sus_dist_nii(out_fn)

        if type == 't2s':
            self.save_t2star_dist(out_fn)

        if type == 'pd':
            self.save_pd_dist(out_fn)

        if type == 't1':
            self.save_t1_dist(out_fn)

        if type == 't2':
            self.save_t2_dist(out_fn)
    def __repr__(self):
        return f"SegmentationLabelManager == Volume"
