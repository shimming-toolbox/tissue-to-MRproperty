# This code returns a dictionary ID: {label_name, susceptibility} based on the tool and version

# Huge thanks to prof. Eva Alonso Ortiz for guidence and providing reference to susceptibility values
# I encourage to read her repo: https://github.com/evaalonsoortiz/Fourier-based-field-estimation

# Important: When editing this lookup tables don't forget to edit the color map for itk and fsl
def return_dict_labels(tool, version, new_chi=None):

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
            # Updated as of August 2025 (compare_fm + chi_opt)
            10: ("lungs",-2.41), # lung_upper_lobe_left
            11: ("lungs",-2.41), # lung_lower_lobe_left
            12: ("lungs",-2.41), # lung_upper_lobe_right
            13: ("lungs",-2.41), # lung_middle_lobe_right
            14: ("lungs",-2.41), # lung_lower_lobe_right
            15: ("esophagus", -9.05),
            16: ("trachea", 0.2),
            #
            17: ("gland",-9.05), # thyroid_gland
            18: ("organ",-9.05), # small_bowel
            19: ("organ",-9.05), # duodenum
            20: ("organ",-9.05), # colon
            21: ("organ",-9.05), # urinary_bladder
            22: ("organ",-9.05), # prostate
            23: ("kidney",-9.05), # kidney_cyst_left
            24: ("kidney",-9.05), # kidney_cyst_right
            25: ("v_bone",-9.7), # sacrum
            26: ("v_bone",-9.7), #vertebrae_S1
            27: ("v_bone",-9.7), # vertebrae_L5
            28: ("v_bone",-9.7), # vertebrae_L4
            29: ("v_bone",-9.7), # vertebrae_L3
            30: ("v_bone",-9.7), # vertebrae_L2
            31: ("v_bone",-9.7), # vertebrae_L1
            32: ("v_bone",-9.7), # vertebrae_T12
            33: ("v_bone",-9.7), # vertebrae_T11
            34: ("v_bone",-9.7), # vertebrae_T10
            35: ("v_bone",-9.7), # vertebrae_T9
            36: ("v_bone",-9.7), # vertebrae_T8
            37: ("v_bone",-9.7), # vertebrae_T7
            38: ("v_bone",-9.7), # vertebrae_T6
            39: ("v_bone",-9.7), #vertebrae_T5
            40: ("v_bone",-9.7), # vertebrae_T4
            41: ("v_bone",-9.7), #vertebrae_T3
            42: ("v_bone",-9.7), # vertebrae_T2
            43: ("v_bone",-9.7), # vertebrae_T1
            44: ("v_bone",-9.7), # vertebrae_C7
            45: ("v_bone",-9.7), # vertebrae_C6
            46: ("v_bone",-9.7), # vertebrae_C5
            47: ("v_bone",-9.7), # vertebrae_C4
            48: ("v_bone",-9.7), # vertebrae_C3
            49: ("v_bone",-9.7), # vertebrae_C2
            50: ("v_bone",-9.7), # vertebrae_C1
            51: ("heart",-9.05), # heart
            52: ("extra",-9.05), # aorta
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
            69: ("bone",-11.1), # humerus_left
            70: ("bone",-11.1), # humerus_right
            71: ("bone",-11.1), # scapula_left
            72: ("bone",-11.1), # scapula_right
            73: ("bone",-11.1), # clavicula_left
            74: ("bone",-11.1), # clavicula_right
            75: ("bone",-11.1), # femur_left
            76: ("bone",-11.1), # femur_right
            77: ("bone",-11.1), # hip_left
            78: ("bone",-11.1), # hip_right
            79: ("SpinalCanal",-9.055), # Spinal Canal (from Total Seg)
            80: ("muscle",-9.03), # gluteus_maximus_left
            81: ("muscle",-9.03), # gluteus_maximus_right
            82: ("muscle",-9.03), # gluteus_medius_left
            83: ("muscle",-9.03), # gluteus_medius_right
            84: ("muscle",-9.03), # gluteus_minimus_left
            85: ("muscle",-9.03), # gluteus_minimus_right
            86: ("muscle",-9.03), # autochthon_left
            87: ("muscle",-9.03), # autochthon_right
            88: ("muscle",-9.03), # iliopsoas_left
            89: ("muscle",-9.03), # iliopsoas_right
            90: ("brain",-9.05), # brain
            91: ("bone",-11.1), # skull
            92: ("bone",-11.1), # rib_left_1
            93: ("bone",-11.1), # rib_left_2
            94: ("bone",-11.1), # rib_left_3
            95: ("bone",-11.1), # rib_left_4
            96: ("bone",-11.1), # rib_left_5
            97: ("bone",-11.1), # rib_left_6
            98: ("bone",-11.1), # rib_left_7
            99: ("bone",-11.1), # rib_left_8
            100: ("bone",-11.1), # rib_left_9
            101: ("bone",-11.1), # rib_left_10
            102: ("bone",-11.1), # rib_left_11
            103: ("bone",-11.1), # rib_left_12
            104: ("bone",-11.1), # rib_right_1
            105: ("bone",-11.1), # rib_right_2
            106: ("bone",-11.1), # rib_right_3
            107: ("bone",-11.1), # rib_right_4
            108: ("bone",-11.1), # rib_right_5
            109: ("bone",-11.1), # rib_right_6
            110: ("bone",-11.1), # rib_right_7
            111: ("bone",-11.1), # rib_right_8
            112: ("bone",-11.1), # rib_right_9
            113: ("bone",-11.1), # rib_right_10
            114: ("bone",-11.1), # rib_right_11
            115: ("bone",-11.1), # rib_right_12
            116: ("bone",-11.1), # sternum
            117: ("cartilage",-9.055) # costal_cartilages
        }

        if version == "v2":
            return dicc

        if version =="mod0":
            # This means it has labels + fat = Whole body
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

            return dicc

        if version == "mod3":
            # This means it has CSF + Spinal Cord + WM/GM segmentation instead of Spina Canal
            dicc[264] = ("fat", -8.92)
            # dicc[256] = ("spinal_cord", -9.055)
            # If labels are done correctly, spinalcord (as well as spinal canal #79)
            # should not be really appearing and not needed to state values for them
            # hence my comment on previous line.
            dicc[289] = ("sc_csf", -9.05)

            dicc[196] = ("sc_wm", -9.083)
            dicc[324] = ("sc_gm", -9.03)
            # Additional to this we add trachea_cartilage and trachea_lumen
            dicc[170] = ("tr_cartilage", -9.055)
            dicc[171] = ("tr_lumen", 0.196)  # Calculation done by S.R. following values from CRC Handbook and chi-opt
            return dicc



    if tool == 'TotalSeg_MRI':

        dicc = {
            0: ("air", 0.35),
            1: ("spleen", -9.05),
            2: ("kidney", -9.05),  # kidney_right
            3: ("kidney", -9.05),  # kidney_left
            4: ("organ", -9.05),  # gallbladder
            5: ("liver", -9.05),  # liver
            6: ("organ", -9.05),  # stomach
            7: ("organ", -9.05),  # pancreas
            8: ("gland", -9.05),  # adrenal_gland_right
            9: ("gland", -9.05),  # adrenal_gland_left
            10: ("lungs", 0.2),  # lung_left
            11: ("lungs", 0.2),  # lung_right
            12: ("esophagus", -9.05),  # esophagus
            13: ("organ", -9.05),  # small_bowel
            14: ("organ", -9.05),  # duodenum
            15: ("organ", -9.05),  # colon
            16: ("organ", -9.05),  # urinary_bladder
            17: ("organ", -9.05),  # prostate
            18: ("bone", -9),  # sacrum
            19: ("bone", -9),  # vertebrae
            20: ("bone", -9),  # intervertebral_discs
            21: ("spinal_cord", -9.055),  # spinal_cord
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
            # Adds labels with "head"
            dicc[145] = ("head", -8.97)
            dicc[169] = ("torso",-8.97)
            dicc[101] = ('bone', -9)
            return dicc

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

    if tool == "compare_fm":
        # This project aims to simulate only 3 different tissue types
        # Bones, soft tisssue and air
        #
        # Some values were changed for ISMRM abstract. More precise values may be implemented later
        dicc = {
            0: ("air", 0.35), # Outside of the body
            2: ("fat", -9.05), # Water and muscle surrounding the labels ## Before -9.032
            3: ("bone", -11), # Spine
            5: ("inter_vert_discs", -9.05),
            7: ("lungs", -4.2), # magical air inside lungs and esophagus
            8: ("trachea", -4.2), # Air in the trachea
            10: ("organ", -9.05), # Susceptibility of water
            12: ("muscle", -9.05), # Muscle has slightly different value than water
            15: ("sinus", -2),
            23: ("brain", -9.04),  # Brain from Samseg
            25: ("skull", -11),  # Skull from Samseg with manual correction in Slicer
            256: ("spinal_cord",-9.055), # Soft tissue for this project
            289:("sc_csf,",-9.055) # Same as 256 for this project, might change later
        }
        if version == 'mod0':
            return dicc

        if version == "dyn":
            # This is for dynamically changing the susceptiblity values
            # Only changing the value of air in lungs and trachea

            lst1 = list(dicc[7])
            lst2 = list(dicc[8])
            lst1[1] = new_chi
            lst2[1] = new_chi
            dicc[7] = tuple(lst1)
            dicc[8] = tuple(lst2)
            print("Changing susceptibility of air to: ", new_chi)
            return dicc

        if version == 'mod_PAM50':
            dicc2 = {
            0 : ("air", 0.35), # Air surrounding the body
            2 : ("fat", -9.05), # Water and muscle surrounding the labels
            3 : ("bone", -11), #
            5 : ("inter_vert_discs", -9.055),
            7 : ("lungs", -4.2), # magical air inside lungs and esophagus
            8 : ("trachea", -4.2), # Air in the trachea
            10 : ("organ", -9.05), # Susceptibility of water
            12: ("muscle", -9.05), # Muscle has slightly different value than water
            15 : ("sinus", -2), # Air in the sinuses and ear canal
            256: ("spinal cord",-9.05) # Soft tissue for this project
            }
            return dicc2

        if version == 'ds005616':
            dicc3 = {
                0: ("air", 0.35),  # Air surrounding the body
                1: ("fat", -9.05),
                2: ("sinus", -2),
                3: ("sinus",-2),
                4: ("trachea",-2.3),
                5: ("lungs",-2.3),
                6: ("lungs",-2.3),
                56: ("brain",-9.04),
                60: ("eyes",-9.05),
                91: ("skull",-11),
                92: ("bone",-11),
                93: ("inter_vert_discs",-9.055),
                100:("spinal_cord",-9.05)

            }
            return dicc3

    if tool  == "bracesTS":
        if version == "v1":
            # Unmerged labels - same values as v2
            dicc_braces = {  # ICPR 143
                0: ("air", 0.35),  # Air surrounding the body
                1: ("kidney", -9.05),  # Adrenal, left
                2: ("kidney", -9.05),  # Adrenal, right
                3: ("Anterior nasal passage", -9.05),  # Anterior nasal passage (ET1)
                4: ("Posterior nasal passage", -9.05),  # Posterior nasal passage (ET2)
                5: ("Oral mucosa", -9.05),  # Oral mucosa, tongue
                6: ("Oral mucosa", -9.05),  # Oral mucosa, lips and cheeks
                7: ("trachea", -9.055),  # !!!!! only the tissue, air is separate
                8: ("Bronchi", -9.05),  # !!!!! only the tissue air is separete
                9: ("extra (blood/muscle)", -9.04),  # Blood vessels, head
                10: ("extra (blood/muscle)", -9.04),  # Blood vessels, trunk
                11: ("extra (blood/muscle)", -9.04),  # Blood vessels, arms
                12: ("extra (blood/muscle)", -9.04),  # Blood vessels, legs
                13: ("bone", -11.1),  # Humeri, upper half, cortical
                14: ("bone", -11.1),  # Humeri, upper half, spongiosa
                15: ("bone", -11.1),  # Humeri, upper half, medullary cavity
                16: ("bone", -11.1),  # Humeri, lower half, cortical
                17: ("bone", -11.1),  # Humeri, lower half, spongiosa
                18: ("bone", -11.1),  # Humeri, lower half, medullary cavity
                19: ("bone", -11.1),  # Ulnae and radii, cortical
                20: ("bone", -11.1),  # Ulnae and radii, spongiosa
                21: ("bone", -11.1),  # Ulnae and radii, medullary cavity
                22: ("bone", -11.1),  # Wrists and hand bones, cortical
                23: ("bone", -11.1),  # Wrists and hand bones, spongiosa
                24: ("bone", -11.1),  # Clavicles, cortical
                25: ("bone", -11.1),  # Clavicles, spongiosa
                26: ("bone", -11.1),  # Cranium, cortical
                27: ("bone", -11.1),  # Cranium, spongiosa
                28: ("bone", -11.1),  # Femora, upper half, cortical
                29: ("bone", -11.1),  # Femora, upper half, spongiosa
                30: ("bone", -11.1),  # Femora, upper half, medullary cavity
                31: ("bone", -11.1),  # Femora, lower half, cortical
                32: ("bone", -11.1),  # Femora, lower half, spongiosa
                33: ("bone", -11.1),  # Femora, lower half, medullary cavity
                34: ("bone", -11.1),  # Tibiae, fibulae and patellae, cortical
                35: ("bone", -11.1),  # Tibiae, fibulae and patellae, spongiosa
                36: ("bone", -11.1),  # Tibiae, fibulae and patellae, medullary cavity
                37: ("bone", -11.1),  # Ankles and foot bones, cortical
                38: ("bone", -11.1),  # Ankles and foot bones, spongiosa
                39: ("bone", -11.1),  # Mandible, cortical
                40: ("bone", -11.1),  # Mandible, spongiosa
                41: ("bone", -11.1),  # Pelvis, cortical
                42: ("bone", -11.1),  # Pelvis, spongiosa
                43: ("bone", -11.1),  # Ribs, cortical
                44: ("bone", -11.1),  # Ribs, spongiosa
                45: ("bone", -11.1),  # Scapulae, cortical
                46: ("bone", -11.1),  # Scapulae, spongiosa
                47: ("Cervical spine", -9.7),  # Cervical spine, cortical
                48: ("Cervical spine", -9.7),  # Cervical spine, spongiosa
                49: ("Thoracic spine", -9.7),  # Thoracic spine, cortical
                50: ("Thoracic spine", -9.7),  # Thoracic spine, spongiosa
                51: ("Lumbar spine", -9.7),  # Lumbar spine, cortical
                52: ("Lumbar spine", -9.7),  # Lumbar spine, spongiosa
                53: ("Sacrum", -9.7),  # Sacrum, cortical
                54: ("Sacrum", -9.7),  # Sacrum, spongiosa
                55: ("bone", -11.1),  # Sternum, cortical
                56: ("bone", -11.1),  # Sternum, spongiosa
                57: ("cartilage", -9.055),  # Cartilage, head
                58: ("cartilage", -9.055),  # Cartilage, trunk
                59: ("cartilage", -9.055),  # Cartilage, arms
                60: ("cartilage", -9.055),  # Cartilage, legs
                61: ("brain", -9.05),
                62: ("fat", -8.92),  # Breast, left, adipose tissue
                63: ("Breast", -9.05),  # Breast, left, glandular tissue
                64: ("fat", -8.92),  # Breast, right, adipose tissue
                65: ("Breast", -9.05),  # Breast, right, glandular tissue
                66: ("Eye lens", -9.05),  # Eye lense, left
                67: ("Eye bulb", -9.05),  # Eye bulb, left
                68: ("Eye lens", -9.05),  # Eye lense, right
                69: ("Eye bulb", -9.05),  # Eye bulb, right
                70: ("Gall bladder", -9.05),  # Gall bladder wall
                71: ("Gall bladder", -9.05),  # Gall bladder contents
                72: ("Stomach", -9.05),  # Stomach wall
                73: ("Stomach", -9.05),  # Stomach contents
                74: ("Small intestine", -9.05),  # Small intestine wall
                75: ("Small intestine", -9.05),  # Small intestine contents
                76: ("Colon", -9.05),  # Ascending colon wall
                77: ("Colon", -9.05),  # Ascending colon contents
                78: ("Colon", -9.05),  # Transverse colon wall, right
                79: ("Colon", -9.05),  # Transverse colon contents, right
                80: ("Colon", -9.05),  # Transverse colon wall, left
                81: ("Colon", -9.05),  # Transverse colon contents, left
                82: ("Colon", -9.05),  # Descending colon wall
                83: ("Colon", -9.05),  # Descending colon contents
                84: ("Sigmoid colon", -9.05),  # Sigmoid colon wall
                85: ("Sigmoid colon", -9.05),  # Sigmoid colon contents
                86: ("Rectum", -9.05),  # Rectum wall
                87: ("heart", -9.05),  # Heart wall
                88: ("heart", -9.05),  # Heart contents (blood)
                89: ("kidney", -9.05),  # Kidney, left, cortex
                90: ("kidney", -9.05),  # Kidney, left, medulla
                91: ("kidney", -9.05),  # Kidney, left, pelvis
                92: ("kidney", -9.05),  # Kidney, right, cortex
                93: ("kidney", -9.05),  # Kidney, right, medulla
                94: ("kidney", -9.05),  # Kidney, right, pelvis
                95: ("liver", -9.05),
                96: ("lungs", -0.27),  # Lung, left, blood
                97: ("lungs", -0.27),  # Lung, left, tissue
                98: ("lungs", -0.27),  # Lung, right, blood
                99: ("lungs", -0.27),  # Lung, right, tissue
                100: ("Lymphatic nodes", -9.05),  # Lymphatic nodes, extrathoracic airways
                101: ("Lymphatic nodes", -9.05),  # Lymphatic nodes, thoracic airways
                102: ("Lymphatic nodes", -9.05),  # Lymphatic nodes, head
                103: ("Lymphatic nodes", -9.05),  # Lymphatic nodes, trunk
                104: ("Lymphatic nodes", -9.05),  # Lymphatic nodes, arms
                105: ("Lymphatic nodes", -9.05),  # Lymphatic nodes, legs
                106: ("muscle", -9.03),  # Muscle, head
                107: ("muscle", -9.03),  # Muscle, trunk
                108: ("muscle", -9.03),  # Muscle, arms
                109: ("muscle", -9.03),  # Muscle, legs
                110: ("esophagus", -9.05),
                111: ("Ovary", -9.05),  # Ovary, left
                112: ("Ovary", -9.05),  # Ovary, right
                113: ("pancreas", -9.05),
                114: ("Pituitary gland", -9.05),  #
                115: ("Prostate", -9.05),  #
                116: ("Residual tissue", -9.05),  # Residual tissue, head
                117: ("Residual tissue", -9.05),  # Residual tissue, trunk
                118: ("Residual tissue", -9.05),  # Residual tissue, arms
                119: ("Residual tissue", -9.05),  # Residual tissue, legs
                120: ("Salivary glands", -9.05),  # Salivary glands, left
                121: ("Salivary glands", -9.05),  # Salivary glands, right
                122: ("Skin", -8.92),  # Skin, head
                123: ("Skin", -8.92),  # Skin, trunk
                124: ("Skin", -8.92),  # Skin, arms
                125: ("Skin", -8.92),  # Skin, legs
                126: ("spinal_cord", -9.055),
                127: ("spleen", -9.05),
                128: ("Teeth", -10),  # Teeth
                129: ("Testis", -9.05),  # Testis, left
                130: ("Testis", -9.05),  # Testis, right
                131: ("Thymus", -9.05),  #
                132: ("Thyroid", -9.05),  #
                133: ("Tongue", -9.05),  # Tongue (inner part)
                134: ("Tonsils", -9.05),  #
                135: ("Ureter", -9.05),  # Ureter, left
                136: ("Ureter", -9.05),  # Ureter, right
                137: ("Urinary bladder", -9.05),  # Urinary bladder wall
                138: ("water", -9.05),  # Urinary bladder contents
                139: ("Uterus", -9.05),  #
                140: ("Air", 0.35),  # Air inside body
                141: ("braces", 900)  # Stainless stell 316L
            }
            return dicc_braces

        if version == 'v2':
            # Merged labels
            dicc_braces = {  # for scan with merged labels
                0: ("air", 0.35),  # Air surrounding the body
                1: ("bone", -11.1),
                2: ("Teeth", -10),
                3: ("Cervical spine", -9.7),
                4: ("cartilage", -9.055),
                5: ("watery tissue", -9.05),
                6: ("extra (blood/muscle)", -9.04),
                7: ("muscle", -9.03),
                8: ("fat", -8.92),
                9: ("lungs", -0.27),
                10: ("Air", 0.35),
                11: ("braces", 300),
            }
            return dicc_braces
    else:
        print("This tool hasn't been implemented yet.")
