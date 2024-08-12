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
        # The values of T2* and T2 are in ms
        # REMEMBER TO UPDATE on select_tool.py everytime a value is changed
        self.relax_values = {

            "air": [0, 0, 0, 0.01, 0.01],
            "bone": [None, 1204, 53, 33.03, 117],  # M0 is often not specified for bone
            "lung": [None, 1270, None, 1, 0.1],  # Air in lungs doesn't have M0, T2 values?
            "water": [None, 2500, 2500, 1000, 100],  # High M0 value
            "CSF": [None, 3200, 2000, 1000, 100],  # High M0

            "spinal_cord":[None, None, None, 76, 59.5], # From the new label 256
            # PD & T2* GM + WM / 2 =>  82 + 70 /2 =    , T2star = 66 + 53 / 2 =

            "sc_csf": [None, 3200, 2000, 1000, 100], # From the new label 289
            "sc_wm": [None, None, None, 53, 70], # From NumericalModel - Eva
            "sc_gm": [None, None, None, 66, 82], # From Numerical Model - Eva

            "fat": [None, 380, 108, 35, 140], # T2star value : 0.5*70e-3 # Daniel PD=90
            "liver": [None, 809, 34, 34/2, 70],
            "spleen": [None, 1328, 61, 65/2, 80],
            # In this initial segmentation the whole brain will be considered 60% GM and 40% WM
            # Given the values a ponderated estimation is 60.8 ms
            "brain":[None,None,None, 60.8, 90],
            "white_matter": [None, None, None, 53 ,70], # This is the brain WM
            "gray_matter": [None, None, None, 66, 82], # This is the brain GM

            "heart":[1000 ,1300, 55, 18.5/2, 85],
            "kidney":[None, 1190, 56, 65.4/2, 70],
            "pancreas":[None, 725,43, 37, 75],
            "cartilage":[None, 1240,32, 20, 50], # PD value is a guess
            "bone_marrow":[None, 365, 23, None, 60],  # PD value is a guess
            "SpinalCanal":[None, 993, 78, 60, 100], #
            "esophagus":[None,None, None, 17, 35], #
            "trachea":[None, None, None, 25, 15],
            "organ":[None, 800, 34, 17, 50], # Values similar to those from liver
            "gland":[None, None, None, 50, 100],
            # There are some organs that don't have enough documentation on the literature to complete
            # the required values so an estimation is used for these:
            "extra" : [None, 750, 50, 35,120],

            "sinus" :[None, None, None, None, None]
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
            "bone": 10.87,
            "lung": 8.01,
            # Water is a value similar to CSF
            "water": 27.79,
            "CSF": 26.5,

            "spinal_cord": 7.64,

            "sc_csf": 26.5,
            # These values are not taken from Whole spine data
            # But taken from Brain image.
            # EAO Flash 2.5mm
            "sc_wm": 1, # 9.82
            "sc_gm": 1, # 12.76
            "brain": 27.91,
            ### Back to Whole Spine data values
            "fat": 33.78,
            "liver": 14.82,
            "spleen": 16.17,

            # "white_matter": ,  # This is the brain WM
            # "gray_matter": ,  # This is the brain GM

            "heart": 15.49,
            "kidney": 14.35,
            "pancreas": 16.94,
            "cartilage": 10.21,
            "bone_marrow": 12.2,
            "SpinalCanal": 18.895,  # sc_csf + (sc_wm + sc_gm / 2 )
            "esophagus": 17.33,
            "trachea": 10.21,  # Trachea should have similar to lung
            "organ": 14.66,
            "gland": 15.82,

            "extra": 14.91,

            "sinus": 9.53
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
