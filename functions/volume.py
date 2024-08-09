#Dependencies
import numpy as np
from functions.label import SegmentationLabel
import nibabel as nib
from functions.utils.get_dic_values import to_csv_sus
import os
from functions.utils.select_tool import return_dict_labels
from skimage.measure import label, regionprops

# Parent class for the creation of a non-finite biomechanical model of the body
class volume:
    
    def __init__(self, volume):
        # Tool and version as input arguments

        # In this version we correct that the output should be the nifti image
        # This way we can attribute the information from nifti files to the class

        self.nifti = volume # This is now directing to a Nifti file
        self.volume = self.nifti.get_fdata()
        self.dimensions = np.array(self.volume.shape) # It is initially a tuple, but it needs to be an array
        self.uniq_labels = np.unique(self.volume)
        self.segmentation_labels = {} 
        self.sus_dist = np.zeros(self.dimensions)
        self.t2star_vol = np.zeros(self.dimensions)
        self.pd_dist = np.zeros(self.dimensions)
        self.deltaB0 = np.zeros(self.dimensions)
        self.gaussian_phantom = np.zeros(self.dimensions)
        # The dictionary has keys for every id number and each value 
        # is the corresponding SegmentationLabel daughter class

        # to check ids depending on the tool selected
        self.look_up = {}
        # This is the Convention Dictionary for labels_id - names - sus_values
        self.relax_values = {}
        # This is a dictionary to get the relaxation values used in label.py

        # Creating a dictionary that stores the counts for each label based on their name
        self.label_counts = {}
        self.label_gaussians = {}
        self.unique_counts = {}
        self.gauss_flag = 0

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

    def group_seg_labels(self,tool,version):
        self.look_up = return_dict_labels(tool,version)

        # Function to get the relaxation values from label
        for i in self.look_up.keys():
            self.segmentation_labels[i] = SegmentationLabel(i)

        for key,value in self.look_up.items():
            # Key is the number of ID and value is (name, sus)
            name = value[0]
            sus = value[1]
            self.set_label_name(key, name)
            self.set_label_susceptibility(key, sus)

        self.relax_values = self.segmentation_labels[1].relax_values
        # Getting the relax values dictionary from any label

    def create_segmentation_labels_old(self):

        #Now this code checks the tool and the version for label-name relationship
        # Still keeping this method just in case
        # New method is group_seg_labels

        # The most important labels are:
        # lungs Bone Soft Tissue SpinalCord CSF
        # These are the regions of the body that impact the most
        # For susceptibility valuesfrom bone, fat and soft tissue:
        # https://pfeifer.phas.ubc.ca/refbase/files/Truong-MRI-2002-20-759.pdf
        #
        # We can create an already pre-defined from convention of label_ids

        # In TotalSegmentator this is labeled Spinal Cord, but
        # it really is the Spinal Canal = Spinal Cord + CSF
        # For SC is (GM + WM)/2 = -9.055
        # From Eva's code GM = -9.03 and WM = -9.08
        self.set_label_name(76,"SpinalCanal")
        self.set_label_susceptibility(76,-9.055)
        # IN this branch of the code, we have added labels for the SC
        # We correct the fact that in Total Seg it was Spinal Canal
        self.set_label_name(256, "spinal_cord")
        self.set_label_susceptibility(256,-9.055)
        self.set_label_name(289, "sc_csf")
        self.set_label_susceptibility(289,-9.05)


        # For the lungs we have [9,10,11,12,13]
        for i in [9,10,11,12,13]:
            self.set_label_name(i,'lung')
            self.set_label_susceptibility(i,0.4)

        # For the bones we have a lot more labels
        # Vertebrae and ribs. But all of them can have the same value: -11.1
        # Vertebrae list goes from Sacrum to C1
        vertebra_list = np.arange(22,48)
        rib_list = np.append(np.arange(89,114),[68,69,70,71,74,75,88])

        # It was -11.1, but now it is -9.0
        for i in vertebra_list:
            self.set_label_name(i,"bone")
            self.set_label_susceptibility(i,-9.0)

        for i in rib_list:
            self.set_label_name(i, "bone")
            self.set_label_susceptibility(i, -9.0)

        # Last but not least is to give susceptibility values to the organs
        # and soft tissue => susceptibility value of water = -9.05

        sus_water_list = [1, 2, 3, 4, 5, 6, 7, 8, 14, 16]

        self.set_label_name(1, "spleen")
        self.set_label_name(2, "kidney") #Right
        self.set_label_name(3, "kidney") # Left
        self.set_label_name(4, "organ") # Gallblader
        self.set_label_name(5, "liver")
        self.set_label_name(6, "organ") #Stomach
        self.set_label_name(7, "gland") # AdrenalGland
        self.set_label_name(8, "gland") # AdrenalGland
        self.set_label_name(14, "esophagus")
        self.set_label_name(15, "trachea")
        self.set_label_name(16, "gland") # Thyroid


        # Susceptibility value of fat = -8.39

        for i in sus_water_list:
            self.set_label_susceptibility(i, -9.05)

        # For trachea, it should have a susceptibilty value closer to air but withsome muscle so a bit diamag.
        self.set_label_susceptibility(15, 0.2)

        # Soft tissue == water
        # Inside of body == fat


        self.set_label_name(0,"air") # Outside of brain
        self.set_label_susceptibility(0,0.35)

        # If label has not been set it can be considered as fat
        # susceptibility of fat label is considering fat and muscle proportion of the body
        # sus of fat is -7.5, muscle is -9.05 and soft tissue is -9.5
        # Assuming that body is 20% fat, 40% muscle and 40% soft tissue
        # The weighted average of the fat label should be: -8.92

        self.set_label_name(264,"fat")
        self.set_label_susceptibility(264,-8.92)

        # For simulating GRE acquisition we need to set name of organs
        # brain, liver, spleen, kidney
        self.set_label_name(87, "brain")
        self.set_label_name(48,"heart")


        # The other labels missing without names follow

        intestines = [17,18,19,20,21,22,23]
        # small intestine duodenum colon urinary bladder prostate kidney cyst left and right
        for i in intestines:
            self.set_label_name(i,"organ")
            self.set_label_susceptibility(i,-9.05)

        # Lastly if everything was labeled properly what's left are veins and muscles
        # The susceptibility of csf and water is -9.05, of muscle is -9.03 we can combine them
        for i in self.uniq_labels:
            if self.segmentation_labels[i].name == None:
                self.set_label_name(i,"extra")
                self.set_label_susceptibility(i,-9.04)

        # This way we should have everything labeled
    def check_labels(self):
        for i in self.uniq_labels:
            if self.segmentation_labels[i].name == None:
                print("Label: ",self.segmentation_labels[i]["name"]," doesn't have name assigned")

    def set_label_name(self, label_id, name):
        ids = self.look_up.keys()
        if label_id in ids:
            self.segmentation_labels[label_id].set_name(name)
        else: print(f"Label ID {label_id} not found, check version selected")

    def set_label_susceptibility(self, label_id, susceptibility):
        ids = self.look_up.keys()
        if label_id in ids:
            # SImilar to set_label_name
            self.segmentation_labels[label_id].set_susceptibility(susceptibility)
        else: print(f"Label ID {label_id} not found.")
    def set_label_pd(self,label_id,pd):
        ids = self.look_up.keys()
        if label_id in ids:
            self.segmentation_labels[label_id].set_pd_val(pd)
        else: print(f"Label ID {label_id} not found.")

    def set_T2star(self, label_id, t2star):
        ids = self.look_up.keys()
        if label_id in ids:
        # SImilar to set_label_name
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

    def create_type_vol(self,type, output_name="default"):
        # This function is for the CLI app
        # Depending on the type we automatically call the specific function
        #
        if type =='sus':
            self.create_sus_dist()
            self.save_sus_dist_nii(output_name)
        if type =='t2s':
            self.create_t2_star_vol()
            self.save_t2star_dist(output_name)
        if type =='pd':
            self.create_pd_vol()
            self.save_pd_dist(output_name)
        if type =='t1':
            print("T1 value volume comming soon!")
        if type =='t2':
            print("T2 volume comming soon!")



    def check_pixels(self):
        # Important to before going to conversion
        # If there is a pixel that is outside of range conversion won't work
        # because it won't be treated as a label but as a float
        flag = 0 # Flag to save in case there were changes
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
                                print("Changed value to: ",rem2)
                                self.volume[i, j, k] = rem2

                            else:
                                print("Number not in look up table")
                                return 1

                        if rem == "Y" or rem == "y":
                            self.volume[i,j,k] = 0

        else:

            if flag == 1:

                print("Saving corrected volume for later usage!")
                tmp_img = nib.Nifti1Image(self.volume, affine = self.nifti.affine)
                path = os.path.join('output',"corrected_pixels.nii.gz")
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

    def create_pd_vol(self):
        # This method will use the lookup table of PD values to create a new volume
        # This new volume will use the labels to quickly create a volume with ProtonDensity values

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

    def calc_gauss(self, value, num_pixels, mr_prop, std_dev = 0.1):
        val = np.random.normal(value, std_dev, num_pixels)
        # In areas close to 0, the gaussian distribution must always return positive values
        # It is not possible to have negative T1, T2, T2s or PD. But susceptibility can be negative
        if mr_prop == "sus":
            return val
        else:
            abs_val = np.abs(val)
            return abs_val


    def calc_regions(self):
        #For  creating a gaussian distribution we need to group and count every label
        #Must be run after defining a tool in group_seg_labels

        unique_labels, counts = np.unique(self.volume, return_counts=True)
        self.unique_counts = dict(zip(unique_labels,counts))

        if self.look_up is {}:
            print("Please define a tool for a lookup table")

        else:
            for l, count in self.unique_counts.items():
                label_id = l
                label_name = self.look_up[l][0]
                label_suscep = self.look_up[l][1]
                if label_name in self.label_counts.keys():
                    self.label_counts[label_name] += count
                else:
                    self.label_counts[label_name] = count

        # Now depending on the tool used we grouped them up
        # And for visualizing, sorting might be good
        sorted_label_counts = sorted(self.label_counts.items(), key = lambda item: item[1], reverse=True)

        for name, count in sorted_label_counts:
            print(f"Label name: {name}: {count} pixels")

    def create_gauss_dist(self,prop):
        # For input restrictions of type, see Segmentation Label

        for l, count in self.unique_counts.items():
            # get the MR property desired
            # l is the name (as a str) of the label

            if prop == "sus":
                property = self.look_up[l][1]
                print("label_name: ",self.look_up[l][0], "susceptibility:",property)

            if prop == "t2s":
                l_name = self.look_up[l][0]
                property = self.relax_values[l_name][3]
                print("t2s:", property)

            if prop == "t2":
                print("Relaxation lookup table still missing some values!")
                print("Coming soon ...")
                #l_name = self.look_up[l][0]
                #property = self.relax_values[l_name][2]
                #print("t2:", prop)

            if prop == "t1":
                #l_name = self.look_up[l][0]
                #property = self.relax_values[l_name][1]
                #print("t1:", property)
                print("Relaxation lookup table still missing some values!")
                print("Coming soon ...")

            if prop == "pd":
                l_name = self.look_up[l][0]
                property = self.relax_values[l_name][4]
                print("pd: ",property)


            self.label_gaussians[l] = self.calc_gauss(num_pixels=count, value = property, mr_prop = prop)
            # This way for every label we have a gaussian distribution

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
                    self.gaussian_phantom[i,j,k] = value\

        print("Finished creating gaussian distributed, based on: ", prop)
        # Lastly add the gaussian phantom to a Nifti
        # And save it to output folder

    def save_gauss_dist(self, type, out_fn = "default"):
        #Saving the gaussian distribution with type defined
        # This must be run ONLY after creating the create_property.
        # If not it will automatically save the empty array
        self.gauss_flag = 1
        if type =='sus':
            self.save_sus_dist_nii(out_fn )

        if type =='t2s':
            self.save_t2star_dist(out_fn)

        if type =='pd':
            self.save_pd_dist(out_fn)

        if type =='t1':
            print("T1 value volume comming soon!")

        if type =='t2':
            print("T2 volume comming soon!")
    def __repr__(self):
        return f"SegmentationLabelManager == Volume"
