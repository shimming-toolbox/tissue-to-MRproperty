# Dependencies


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
        self.perm3T = None
        self.cond3T = None
        self.perm7T = None
        self.cond7T = None

        # Key is the name and value is ordered:
        # M0, T1, T2, T2*, PD
        # M0 = C * PD, where C is a scaling factor
        # C represents smoothly-varying spatial modulation of the PD map
        # by the profile of the r. coil gain (B-)
        # The values of T1, T2* and T2 are in ms
        # Unit of PD is [pu] percentage units
        # Unit of susceptibility is ppm, we use absolute susceptibility values

        # REMEMBER TO UPDATE on select_tool.py everytime a value is changed

        self.relax_values = {
            # Official labels for the Whole Body phantom by S.R.
            "fat": [None, 401.2, 129.3, 64.65, 20],
            "heart": [None, 1215.67, 49.35, 25.195, 77],
            "liver": [None, 798.75, 33, 18.82, 70],
            "pancreas": [None, 797.55, 43.5, 21.1, 70],
            "kidney": [None, 1338, 86.835, 57.55, 82],
            "brain": [None, 1232.9, 82.9, 42.8, 74.5],
            "spleen": [None, 1328, 60.9, 16.3, 75],
            "cartilage": [None, 1201, 43.225, 26.04, 70],
            "bone_marrow": [None, 586, 49, 24.5, 27],

            "sc_wm": [None, 857, 73, 38.65, 70],
            "sc_gm": [None, 983.5, 76, 44.4, 80],
            "sc_csf": [None, 5128, 1419.84, 709.92, 100],

            "muscle": [None, 1237.825, 36.1, 24.1, 45],
            "bone": [None, 223, 0.39, 1.16, 18],
            "v_bone": [None, 618.5, 80.685, 40.3, 40],
            "lungs": [None, 1400, 35.5, 1.62, 15],
            "trachea": [None, 1100, 40, 12, 5],
            "tr_cartilage":[None, 1201, 43.225, 26.04, 70],
            "tr_lumen": [None, 0.01, 0.01, 0.01, 0.01],
            "air": [None, 0.01, 0.01, 0.01, 0.01],

            "extra": [None, 800, 50, 35, 50],  # Mostly blood carriers or muscle (high water content)

            # Other labels for other segmentation tools available :)
            # Literature review pending
            "spinal_cord": [None, 936.5, 76.75, 40.07, 60],
            "water": [None, 2500, 275, 275/2, 100],  # High M0 value
            "CSF": [None, 1953, 275, 275/2, 100],  # High M0 t1 from ITIS
            "white_matter": [None, 887.7, 65.4, 35, 70],  # This is the brain WM
            "gray_matter": [None, 1446.1, 94.3, 48, 82],  # This is the brain GM
            "SpinalCanal": [None, 993, 78, 78/2, 90],  #
            "esophagus": [None, 1000, 32, 17, 45],  # Assuming trachea is almost 100% muscle
            "organ": [None, 800, 40, 20, 65],  # Values similar to those from liver
            "gland": [None, 1600, 72, 72/2, 80],  # Values from ITIS foundation for Salivary gland
            # There are some organs that don't have enough documentation on the literature to complete
            # the required values so an estimation is used for these:
            "sinus": [None, None, None, None, None],  # Not used in CT tool // missing values
            # Used in totalSeg_mr & compare fm
            "inter_vert_discs": [None, 1201, 42, 26, 50],  # Same as cartilage

        }

        # Here we have Permittivity@3T, Conductivity@3T, Permittivity@7T, Conductivity@7T
        # Values come from IT'IS foundation using 177.74 MHz for 3T values
        # And 298.06 MHz for 7T
        # Gyromagnetic ratio used: 42.58
        # Units of conductivity S/m
        self.static_values = {
            # Will eventually need to be completed, for now use short version until required
            "fat": [],
            "heart": [],
            "liver": [],
            "pancreas": [],
            "kidney": [],
            "brain": [],
            "spleen": [],
            "cartilage": [],
            "bone_marrow": [],

            "sc_wm": [],
            "sc_gm": [],
            "sc_csf": [],

            "muscle": [],
            "bone": [],
            "v_bone": [],
            "lungs": [],
            "trachea": [],
            "air": [],

            "extra": [],

            "spinal_cord": [],
            "water": [],
            "CSF": [],
            "white_matter": [],
            "gray_matter": [],
            "SpinalCanal": [],
            "esophagus": [],
            "organ": [],
            "gland": [],

            "sinus": [],
            "inter_vert_discs": [],

        }

        self.static_values_short = {

            "fat": [48.17, 0.52, 44.25, 0.562],  # We use avg_infiltrated(30%) + muscle (70%)
            "brain": [79.80, 0.829, 59.8, 0.972],  # Considered cerebellum
            "muscle": [63.5, 0.719, 58.2, 0.77],
            "bone": [14.7, 0.0673, 13.4, 0.0825],  # Cortical
            "lungs": [29.5, 0.316, 24.8, 0.356],  # Using value of Inflated Lungs
            "trachea": [50.6, 0.559, 45.3, 0.61],
            "air": [1, 0, 1, 0],
            "spinal_cord": [44.1, 0.354, 36.9, 0.418],
            "sc_csf": [84.1, 2.14, 72.8, 2.22],
            "organ": [89.7, 0.852, 70.6, 1.02],  # Using Kidney as reference
            "sinus": [5.435, 0.0426, 4.48, 0.051],  # Considering healthy sinus is 95% air and 5% soft tissue
            "inter_vert_discs": [52.9, 0.488, 46.8, 0.552],  # Considered cartilage

            # For ds005616 we have the eyes label
            "skull": [14.7, 0.0673, 13.4, 0.0825], # Considered cortical bone
            "eyes": [84.1, 2.14, 72.8, 2.22],  # Which according to IT'IS foundation, can be considered as CSF
        }
    # Literature values will have a link to a paper/abstract soon!
    # It's a literature review

        self.std_dev = {

            "air": 2.78,  # air is background
            # To all labels we have subtracted air std_dev
            "bone": 5.42,  # 10.87
            "v_bone": 5.42,  # Same as bone
            "lungs": 4.01,  # 8.01
            # Water is a value similar to CSF
            "water": 10.29,  # 27.79
            "CSF": 12.25,  # 26.5

            "spinal_cord": 7.64,

            "sc_csf": 12.25,  # 26.5
            # These values are not taken from Whole spine data
            # But taken from Brain image.
            # EAO Flash 2.5mm
            "sc_wm": 1,  # 9.82
            "sc_gm": 1,  # 12.76
            "brain": 18.45,  # 27.91
            # Back to Whole Spine data values
            "fat": 15.39,  # 33.78
            "liver": 7.41,  # 14.82
            "spleen": 8.08,  # 16.17

            # "white_matter": ,  # This is the brain WM
            # "gray_matter": ,  # This is the brain GM

            "heart": 7.28,  # 15.49
            "kidney": 7.17,  # 14.35
            "pancreas": 8.49,  # 16.94
            "cartilage": 5.16,  # 10.21
            "bone_marrow": 6.1,  # 12.2
            "SpinalCanal": 9.98,  # 18.895 # sc_csf + (sc_wm + sc_gm / 2 )
            "esophagus": 8.96,  # 17.33
            "trachea": 5.16,  # 10.21 # Trachea should have similar to lung
            "organ": 7.33,  # 14.66
            "gland": 7.91,  # 15.82

            "extra": 7.45,  # 14.91

            "sinus": 4.26  # 9.53
        }

    def set_name(self, name):

        if name in self.relax_values.keys():
            self.name = name
            self.M0_val = self.relax_values[name][0]
            self.T1_val = self.relax_values[name][1]
            self.T2_val = self.relax_values[name][2]
            self.T2star_val = self.relax_values[name][3]
            self.PD_val = self.relax_values[name][4]

        elif name in self.static_values_short.keys():
            self.name = name
            self.perm3T = self.static_values_short[name][0]
            self.cond3T = self.static_values_short[name][1]
            self.perm7T = self.static_values_short[name][2]
            self.cond7T = self.static_values_short[name][3]

        else:

            self.name = name
            self.M0_val = 0
            self.T1_val = 0
            self.T2_val = 0
            self.T2star_val = 0
            self.PD_val = 0

    def set_static_name(self, name):

        if name in self.static_values_short.keys():
            self.name = name
            self.perm3T = self.static_values_short[name][0]
            self.cond3T = self.static_values_short[name][1]
            self.perm7T = self.static_values_short[name][2]
            self.cond7T = self.static_values_short[name][3]

        else:
            self.name = name
            self.perm3T = 0
            self.cond3T = 0
            self.perm7T = 0
            self.cond7T = 0

    def set_susceptibility(self, susceptibility):

        self.susceptibility = susceptibility

    def set_M0_val(self, M0):

        self.M0_val = M0

    def set_t1_val(self, t1):

        self.T1_val = t1

    def set_t2_val(self, t2):

        self.T2_val = t2

    def set_pd_val(self, pd):
        self.PD_val = pd

    def set_t2star_val(self, t2star):
        self.T2star_val = t2star

    def get_type(self, type):
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
        # Add the latest attributes addition to the class
        return (f"SegmentationLabel(label_id={self.label_id}, name={self.name}, chi={self.susceptibility},"
                f"M0={self.M0_val}, T1,T2,T2* = {self.T1_val,self.T2_val,self.T2star_val}, PD = {self.PD_val} )")
