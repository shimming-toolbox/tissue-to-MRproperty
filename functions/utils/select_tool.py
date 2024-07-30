# This code returns a dictionary ID: {label_name, susceptibility} based on the tool and version

# Huge thanks to prof. Eva Alonso Ortiz for guidence and providing reference to susceptibility values
# I encourage to read her repo: https://github.com/evaalonsoortiz/Fourier-based-field-estimation

# Important: When editing this lookup tables don't forget to edit the color map for itk and fsl
def return_dict_labels(tool,version):
    if tool == "TotalSeg_CT":

        # Using total segmentator we use follow their list for 117 labels
        # and group them up based on their effect to the B0 map impact
        # link: https://github.com/wasserth/TotalSegmentator/blob/master/totalsegmentator/map_to_binary.py

        # Baseline dictionary for Total Segmentator CT
        # id : name, susceptibility_value

        dicc= {

            0: ("air", 0.35),
            1: ("spleen",-9.05),
            2: ("kidney",-9.05), # kidney_right
            3: ("kidney",-9.05), # kidney_left
            4: ("organ",-9.05), # gallbladder
            5: ("liver",-9.05), # liver
            6: ("organ",-9.05), # stomach
            7: ("organ",-9.05), # pancreas
            8: ("gland",-9.05), # adrenal gland left
            9: ("gland",-9.05), # adrenal_gland_left
            10: ("lung",0.2), # lung_upper_lobe_left
            11: ("lung",0.2), # lung_lower_lobe_left
            12: ("lung",0.2), # lung_upper_lobe_right
            13: ("lung",0.2), # lung_middle_lobe_right
            14: ("lung",0.2), # lung_lower_lobe_right
            15: ("esophagus",-9.05),
            16: ("trachea",0.2),
            17: ("gland",-9.05), # thyroid_gland
            18: ("organ",-9.05), # small_bowel
            19: ("organ",-9.05), # duodenum
            20: ("organ",-9.05), # colon
            21: ("organ",-9.05), # urinary_bladder
            22: ("organ",-9.05), # prostate
            23: ("kidney",-9.05), # kidney_cyst_left
            24: ("kidney",-9.05), # kidney_cyst_right
            25: ("bone",-9), # sacrum
            26: ("bone",-9), #vertebrae_S1
            27: ("bone",-9), # vertebrae_L5
            28: ("bone",-9), # vertebrae_L4
            29: ("bone",-9), # vertebrae_L3
            30: ("bone",-9), # vertebrae_L2
            31: ("bone",-9), # vertebrae_L1
            32: ("bone",-9), # vertebrae_T12
            33: ("bone",-9), # vertebrae_T11
            34: ("bone",-9), # vertebrae_T10
            35: ("bone",-9), # vertebrae_T9
            36: ("bone",-9), # vertebrae_T8
            37: ("bone",-9), # vertebrae_T7
            38: ("bone",-9), # vertebrae_T6
            39: ("bone",-9), #vertebrae_T5
            40: ("bone",-9), # vertebrae_T4
            41: ("bone",-9), #vertebrae_T3
            42: ("bone",-9), # vertebrae_T2
            43: ("bone",-9), # vertebrae_T1
            44: ("bone",-9), # vertebrae_C7
            45: ("bone",-9), # vertebrae_C6
            46: ("bone",-9), # vertebrae_C5
            47: ("bone",-9), # vertebrae_C4
            48: ("bone",-9), # vertebrae_C3
            49: ("bone",-9), # vertebrae_C2
            50: ("bone",-9), # vertebrae_C1
            51: ("heart",-9.04), # heart
            52: ("extra",-9.04), # aorta
            53: ("extra",-9.04), # pulmonary_vein
            54: ("extra",-9.04), # brachiocephalic_trunk
            55: ("extra",-9.04), # subclavian_artery_right
            56: ("extra",-9.04), # subclavian_artery_left
            57: ("extra",-9.04), # common_carotid_artery_right
            58: ("extra",-9.04), # common_carotid_artery_left
            59: ("extra",-9.04), # brachiocephalic_vein_left
            60: ("extra",-9.04), # brachiocephalic_vein_right
            61: ("extra",-9.04), # atrial_appendage_left
            62: ("extra",-9.04), # superior_vena_cava
            63: ("extra",-9.04), # inferior_vena_cava
            64: ("extra",-9.04), # portal_vein_and_splenic_vein
            65: ("extra",-9.04), # iliac_artery_left
            66: ("extra",-9.04), # iliac_artery_right
            67: ("extra",-9.04), # iliac_vena_left
            68: ("extra",-9.04), # iliac_vena_right
            69: ("bone",-9), # humerus_left
            70: ("bone",-9), # humerus_right
            71: ("bone",-9), # scapula_left
            72: ("bone",-9), # scapula_right
            73: ("bone",-9), # clavicula_left
            74: ("bone",-9), # clavicula_right
            75: ("bone",-9), # femur_left
            76: ("bone",-9), # femur_right
            77: ("bone",-9), # hip_left
            78: ("bone",-9), # hip_right
            79: ("SpinalCanal",-9.055), # Spinal Canal (from Total Seg)
            80: ("extra",-9.04), # gluteus_maximus_left
            81: ("extra",-9.04), # gluteus_maximus_right
            82: ("extra",-9.04), # gluteus_medius_left
            83: ("extra",-9.04), # gluteus_medius_right
            84: ("extra",-9.04), # gluteus_minimus_left
            85: ("extra",-9.04), # gluteus_minimus_right
            86: ("extra",-9.04), # autochthon_left
            87: ("extra",-9.04), # autochthon_right
            88: ("extra",-9.04), # iliopsoas_left
            89: ("extra",-9.04), # iliopsoas_right
            90: ("brain",-9.04), # brain
            91: ("bone",-9), # skull
            92: ("bone",-9), # rib_left_1
            93: ("bone",-9), # rib_left_2
            94: ("bone",-9), # rib_left_3
            95: ("bone",-9), # rib_left_4
            96: ("bone",-9), # rib_left_5
            97: ("bone",-9), # rib_left_6
            98: ("bone",-9), # rib_left_7
            99: ("bone",-9), # rib_left_8
            100: ("bone",-9), # rib_left_9
            101: ("bone",-9), # rib_left_10
            102: ("bone",-9), # rib_left_11
            103: ("bone",-9), # rib_left_12
            104: ("bone",-9), # rib_right_1
            105: ("bone",-9), # rib_right_2
            106: ("bone",-9), # rib_right_3
            107: ("bone",-9), # rib_right_4
            108: ("bone",-9), # rib_right_5
            109: ("bone",-9), # rib_right_6
            110: ("bone",-9), # rib_right_7
            111: ("bone",-9), # rib_right_8
            112: ("bone",-9), # rib_right_9
            113: ("bone",-9), # rib_right_10
            114: ("bone",-9), # rib_right_11
            115: ("bone",-9), # rib_right_12
            116: ("bone",-9), # sternum
            117: ("bone",-9) # costal_cartilages
        }

        if version == "v2":
            return dicc

        if version =="mod0":
            # This means it has labes + fat = Whole body
            dicc[264]=("fat",-8.92)
            return dicc

        if version =="mod1":
            # This means its Whole body + Spinal Cord CSF to differentiate Spinal Canal
            # from spinal cord
            dicc[264]=("fat",-8.92)
            dicc[256]=("spinal_cord",-9.055)
            dicc[289]=("sc_csf",-9.05)
            return dicc

        if version=="mod2":
            # This means it has CSF + Spinal Cord + WM/GM segmentation instead of Spina Canal
            dicc[264]=("fat",-8.92)
            #dicc[256] = ("spinal_cord", -9.055)
            # If labels are done correctly, spinalcord (as well as spinal canal #79)
            # should not be really appearing and not needed to state values for them
            # hence my comment on previous line.
            dicc[289] = ("sc_csf", -9.05)

            dicc[196] = ("sc_wm", -9.083)
            dicc[324] = ("sc_gm", -9.03)
            # Future implementation
            # Currently manually segmentating resampled registered CT image
            # to get WM/GM segmentation masks
            return dicc

    if tool == 'TotalSeg_MRI':

        dicc = {

            1: ("spleen", -9.05),
            2: ("kidney", -9.05),  # kidney_right
            3: ("kidney", -9.05),  # kidney_left
            4: ("organ", -9.05),  # gallbladder
            5: ("liver", -9.05),  # liver
            6: ("organ", -9.05),  # stomach
            7: ("organ", -9.05),  # pancreas
            8: ("gland", -9.05),  # adrenal_gland_right
            9: ("gland", -9.05),  # adrenal_gland_left
            10: ("lung", 0.2),  # lung_left
            11: ("lung", 0.2),  # lung_right
            12: ("esophagus", -9.05),  # esophagus
            13: ("organ", -9.05),  # small_bowel
            14: ("organ", -9.05),  # duodenum
            15: ("organ", -9.05),  # colon
            16: ("organ", -9.05),  # urinary_bladder
            17: ("organ", -9.05),  # prostate
            18: ("bone", -9),  # sacrum
            19: ("bone", -9),  # vertebrae
            20: ("bone", -9),  # intervertebral_discs
            21: ("spinal_cord", 0),  # spinal_cord
            22: ("heart", -9.04),  # heart
            23: ("extra", -9.04),  # aorta
            24: ("extra", -9.04),  # inferior_vena_cava
            25: ("extra", -9.04),  # portal_vein_and_splenic_vein
            26: ("extra", -9.04),  # iliac_artery_left
            27: ("extra", -9.04),  # iliac_artery_right
            28: ("extra", -9.04),  # iliac_vena_left
            29: ("extra", -9.04),  # iliac_vena_right
            30: ("bone", -9),  # humerus_left
            31: ("bone", -9),  # humerus_right
            32: ("bone", -9),  # fibula
            33: ("bone", -9),  # tibia
            34: ("bone", -9),  # femur_left
            35: ("bone", -9),  # femur_right
            36: ("bone", -9),  # hip_left
            37: ("bone", -9),  # hip_right
            38: ("extra", -9.04),  # gluteus_maximus_left
            39: ("extra", -9.04),  # gluteus_maximus_right
            40: ("extra", -9.04),  # gluteus_medius_left
            41: ("extra", -9.04),  # gluteus_medius_right
            42: ("extra", -9.04),  # gluteus_minimus_left
            43: ("extra", -9.04),  # gluteus_minimus_right
            44: ("extra", -9.04),  # autochthon_left
            45: ("extra", -9.04),  # autochthon_right
            46: ("extra", -9.04),  # iliopsoas_left
            47: ("extra", -9.04),  # iliopsoas_right
            48: ("extra", -9.04),  # quadriceps_femoris_left
            49: ("extra", -9.04),  # quadriceps_femoris_right
            50: ("extra", -9.04),  # thigh_medial_compartment_left
            51: ("extra", -9.04),  # thigh_medial_compartment_right
            52: ("extra", -9.04),  # thigh_posterior_compartment_left
            53: ("extra", -9.04),  # thigh_posterior_compartment_right
            54: ("extra", -9.04),  # sartorius_left
            55: ("extra", -9.04),  # sartorius_right
            56: ("brain", -9.04)  # brain
        }

        if version == 'v1':
            return dicc

        if version == 'mod0':
            # Adding similar to CT case
            # Adds labels with "fat" label
            pass

    if tool == 'ProCord_MRI':
        pass

    if tool == "charles":

        dicc = {

            0: ("air", 0.35),  # background
            1: ("water", -9.05),  # body
            2: ("air", 0.35),  # sinus
            3: ("air", 0.35),  # ear_canal
            4: ("trachea", 0.2),  # trachea
            5: ("lung", 0.2),  # lung_left
            6: ("lung", 0.2),  # lung_right
            7: ("bone", -11.5),  # skull
            8: ("water", -9.05),  # eyes
            9: ("bone", -11.5),  # vertebrates
            10: ("cartilage", -9.055),  # discs
        }
        if version == 'v1':
            return dicc


    else:
        print("This tool hasn't been implemented yet.")
