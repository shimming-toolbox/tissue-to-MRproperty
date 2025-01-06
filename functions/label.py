#Dependencies
import numpy as np


class SegmentationLabel:
    def __init__(self, label_id, name=None):

        self.label_id = label_id
        self.name = name
        self.susceptibility = None
        self.ct_number = None
        self.M0_val = None
        self.T1_val = None
        self.T2_val = None
        self.T2star_val = None
        self.PD_val = 0
        self.std_dev = {}

        # Key is the name and value is ordered: M0, T1, T2, T2*, PD
        # M0 = C * PD, where C is a scaling factor
        # C represents smoothly-varying spatial modulation of the PD map
        # by the profile of the receive coil gain (B-)
        # The values of T2* and T2 are in ms
        # Unit of PD is [pu] percentage units

        # REMEMBER TO UPDATE on select_tool.py everytime a value is changed
        self.relax_values = {

            "air": [None, 0.01, 0.02, 0.01, 0.01],
            "bone": [None, 224.8, 53, 0.4, 20],  # uMRI study showed T1: [1,1.6]s at 7T
            "lungs": [None, 1372, 1, 1, 30],  # Air in lungs doesn't have M0, T2 values?
            "water": [None, 2500, 275, 275/2, 100],  # High M0 value
            "CSF": [None, 1953, 275, 275/2, 100],  # High M0 t1 from ITIS

            "spinal_cord":[None, 936.5, 76.75, 40.07, 60], # From the new label 256
            # PD & T2* GM + WM / 2 =>  82 + 70 /2 =    , T2-star = 66 + 53 / 2 =
            # T2 is a guess

            "sc_csf": [None, 5128, 1419.84, 709.92, 100], # Values from https://pmc.ncbi.nlm.nih.gov/articles/PMC7410772/pdf/zj4788.pdf scaled to 3T
            "sc_wm": [None, 857, 75, 38.65, 70], # From NumericalModel - Eva
            "sc_gm": [None, 983.5, 95, 44.4, 82], # From Numerical Model - Eva
            "v_bone": [None, 400, 53, 0.4, 20], # Values from same articel as sc_csf

            "fat": [None, 401, 129.3, 64.65, 90], # T2star value : 0.5*70e-3 # Daniel PD=90
            "liver": [None, 798.75, 25.5, 18.82, 70],
            "spleen": [None, 1328, 60.9, 16.3, 80],
            # In this initial segmentation the whole brain will be considered 60% GM and 40% WM
            # Given the values a ponderated estimation is 60.8 ms

            "brain":[None, 1222.9, 82.9, 42.8, 90], # Assuming 40% more wm than GM
            "white_matter": [None, 887.7, 65.4, 35 ,70], # This is the brain WM
            "gray_matter": [None, 1446.1, 94.3, 48, 82], # This is the brain GM

            "heart":[None ,1215.67, 49.35, 25.195, 85],
            "kidney":[None, 1338, 86.835, 57.55, 70],
            "pancreas":[None, 797.55, 43.5, 21.1, 75],
            "cartilage":[None, 1201, 43.225, 26.04, 50], # PD value is a guess
            "bone_marrow":[None, 583, 49, 24.5, 60],  # PD value is a guess
            "SpinalCanal":[None, 993, 78, 78/2, 90], #

            "esophagus":[None, 1000, 32, 17, 45], # Assuming trachea is almost 100% muscle
            "trachea":[None, 1000, 35, 15, 15], # Assuming trachea is almost 100% cartilage
            "organ":[None, 800, 40, 20, 65], # Values similar to those from liver
            "gland":[None, 1600, 72, 72/2, 80], # Values from ITIS foundation for Salivatory gland

            # There are some organs that don't have enough documentation on the literature to complete
            # the required values so an estimation is used for these:
            "extra": [None, 800, 50, 35, 80], # Mostly blood carriers or muscle (high water content)

            "sinus":[None, None, None, None, None], # Not used in CT tool // missing values

            # Used in total_mr & compare fm
            "inter_vert_discs" : [None, 1201, 42, 26, 50], # Same as cartilage
            "muscle" : [None, 1237.825, 36.1, 24.1, 45]
        }
    # Literature values from:
    # Jorge Zavala Bojorquez, Stéphanie Bricq, Clement Acquitter, François Brunotte, Paul M. Walker, Alain Lalande, What are normal relaxation times of tissues at 3 T?, Magnetic Resonance Imaging, Volume 35, 2017, Pages 69-80, ISSN 0730-725X, https://doi.org/10.1016/j.mri.2016.08.021.
    #
    # Stanisz, G.J., Odrobina, E.E., Pun, J., Escaravage, M., Graham, S.J., Bronskill, M.J. and Henkelman, R.M. (2005), T1, T2 relaxation and magnetization transfer in tissue at 3T. Magn. Reson. Med., 54: 507-512. https://doi.org/10.1002/mrm.20605
    # Arnold, J., Fidler, F., Wang, T. et al. Imaging lung function using rapid dynamic acquisition of T 1-maps during oxygen enhancement. Magn Reson Mater Phy 16, 246–253 (2004). https://doi.org/10.1007/s10334-004-0034-z
    # Meloni, A., De Marchi, D., Positano, V. et al. Accurate estimate of pancreatic T2* values: how to deal with fat infiltration. Abdom Imaging 40, 3129–3136 (2015). https://doi.org/10.1007/s00261-015-0522-9
    # Hesper, T., Hosalkar, H.S., Bittersohl, D. et al. T2* mapping for articular cartilage assessment: principles, current applications, and future prospects. Skeletal Radiol 43, 1429–1445 (2014). https://doi.org/10.1007/s00256-014-1852-3
    # Wu, X., Song, H., Stenger, V.A., Gach, H.M. (2023). Quantification of B0 Inhomogeneities in the Abdomen at 3 T. In: Selvaraj, H., Chmaj, G., Zydek, D. (eds) Advances in Systems Engineering. ICSEng 2023. Lecture Notes in Networks and Systems, vol 761. Springer, Cham. https://doi.org/10.1007/978-3-031-40579-2_11
    #

    # MRI from Picture to Proton
    # Questions and answers in MRI website : Courtesy of Allen D. Elster, MRIquestions.com
    ########### For some T2star values #############
    # Some T2 star values from the literature are at 1.5T: liver, spleen, kidney, WM and GM, cartilage
    # T2 star values should decrease with higher field strength due to faster spin dephase
    # For the purpose of this code, the values at 1.5T are assumed to half at 3T
    # T2 star value of lungs from : Wu, X., Song, H., Stenger, V.A., Gach, H.M. (2023). Quantification of B0 Inhomogeneities in the Abdomen at 3 T. In: Selvaraj, H., Chmaj, G., Zydek, D. (eds) Advances in Systems Engineering. ICSEng 2023. Lecture Notes in Networks and Systems, vol 761. Springer, Cham. https://doi.org/10.1007/978-3-031-40579-2_11


    # Cristina Rossi, Andreas Boss, Michael Haap, Petros Martirosian, Claus D. Claussen, Fritz Schick, Whole-body T2⁎ mapping at 1.5 T, Magnetic Resonance Imaging, Volume 27, Issue 4, 2009, Pages 489-496, ISSN 0730-725X, https://doi.org/10.1016/j.mri.2008.08.004.
    # For brain T2star values: Andrew M. Peters, Matthew J. Brookes, Frank G. Hoogenraad, Penny A. Gowland, Susan T. Francis, Peter G. Morris, Richard Bowtell, T2* measurements in human brain at 1.5, 3 and 7 T,
    # Magnetic Resonance Imaging, Volume 25, Issue 6, 2007, Pages 748-753, ISSN 0730-725X, https://doi.org/10.1016/j.mri.2007.02.014.

    # For Proton density:
    # Proton density should be independent of field strength, we are using a value relative to water being 100
    #

        self.std_dev = {

            "air": 2.78,  # air is backgrund
            # To all labels we have substracted air std_dev
            "bone": 5.42, # 10.87
            "v_bone": 5.42, # Same as bone
            "lungs": 4.01, # 8.01
            # Water is a value similar to CSF
            "water": 10.29, # 27.79
            "CSF": 12.25, # 26.5

            "spinal_cord": 7.64,

            "sc_csf": 12.25, # 26.5
            # These values are not taken from Whole spine data
            # But taken from Brain image.
            # EAO Flash 2.5mm
            "sc_wm": 1, # 9.82
            "sc_gm": 1, # 12.76
            "brain": 18.45, # 27.91
            ### Back to Whole Spine data values
            "fat": 15.39, # 33.78
            "liver": 7.41, # 14.82
            "spleen": 8.08, # 16.17

            # "white_matter": ,  # This is the brain WM
            # "gray_matter": ,  # This is the brain GM

            "heart": 7.28, # 15.49
            "kidney": 7.17, # 14.35
            "pancreas": 8.49, # 16.94
            "cartilage": 5.16, # 10.21
            "bone_marrow": 6.1, # 12.2
            "SpinalCanal": 9.98, # 18.895 # sc_csf + (sc_wm + sc_gm / 2 )
            "esophagus": 8.96, # 17.33
            "trachea": 5.16, # 10.21 # Trachea should have similar to lung
            "organ": 7.33, # 14.66
            "gland": 7.91, # 15.82

            "extra": 7.45, # 14.91

            "sinus": 4.26 # 9.53
        }


    def set_name(self, name):

        if name in self.relax_values.keys():
            self.name = name
            self.M0_val = self.relax_values[name][0]
            self.T1_val = self.relax_values[name][1]
            self.T2_val = self.relax_values[name][2]
            self.T2star_val = self.relax_values[name][3]
            self.PD_val = self.relax_values[name][4]

        else:

            self.name = name
            self.M0_val = 0
            self.T1_val = 0
            self.T2_val = 0
            self.T2star_val = 0
            self.PD_val = 0


    def set_susceptibility(self, susceptibility):
        self.susceptibility = susceptibility

    def set_M0_val(self,M0):
        self.M0_val = M0
    def set_t1_val(self,t1):
        self.T1_val = t1

    def set_t2_val(self,t2):
        self.T2_val = t2
    def set_pd_val(self,pd):
        self.PD_val = pd

    def set_t2star_val(self,t2star):
        self.T2star_val = t2star

    def get_type(self,type):
        # Input a type as a string and returns the MR property
        if type == "sus":
            return self.susceptibility
        if type == "t2s":
            return self.T2star_val
        if type == "pd":
            return self.PD_val
        if type == "t1":
            return self.T1_val
        if type == "t2":
            return self.T2_val

    def get_relax_values(self):
        # To send the dictionary to other functions in the folder
        return self.relax_values

    def get_std_dev(self):
        # We need to differentiate the labels for a more realistic MR simulation
        # We need to identify per label
        # Using Whole Spine data - T2w images

        # With higher std_dev the values will have more distribution
        # I want to be able to differentiate water from organs
        # So the value of distribution for all the organs will be less than half
        # of that from tissue/fat label

        return self.std_dev

    def __str__(self):
        # Add the latest attributes additioned to the class
        return (f"SegmentationLabel(label_id={self.label_id}, name={self.name}, susceptibility={self.susceptibility},"
                f"M0={self.M0_val}, T1,T2,T2* = {self.T1_val,self.T2_val,self.T2star_val}, PD = {self.PD_val} )")
