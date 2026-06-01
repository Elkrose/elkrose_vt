from main_classes.girl.class_girl_ren import Girl


global_current_location_label = ""


"""renpy
init -3 python:
"""

def is_visibly_pregnant(girl: Girl) -> bool:
    """
    Checks if the girl is in a state where a pregnancy body should be shown.
    This is used as a general fallback for 2nd or 3rd trimester.
    """
    return getattr(girl, 'preg_body', False) and getattr(girl, 'pregnancy_phase', 0) >= 2

# database_fullbody_image_tags = {
    # # =================================================================================
    # # PREGNANCY OVERRIDES (Highest Priority)
    # # These tags are checked first. If a condition is met, the system will try to
    # # find the corresponding image (e.g., preg_3rd_bare.webp). If it can't be
    # # found, it will continue down the list until it finds a match for an image
    # # that does exist.
    # # =================================================================================
    # # --- Third Trimester (Most Specific) ---
    # "preg_3rd_shower": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.id == girls_in_locker_room[2]",
    # "preg_3rd_bare": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.is_nude()",
    # "preg_3rd_swimsuit": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_swimsuit(girl)",
    # "preg_3rd_bikini": "getattr(girl, 'pregnancy_phase', 0) == 3 and (is_wearing_bikini(girl) or is_wearing_swimsuit(girl))",
    # "preg_3rd_underwear": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.is_in_underwear()",
    # "preg_3rd_bottomless": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.is_bottomless()",
    # "preg_3rd_topless": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.is_topless()",
    # "preg_3rd_maid": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_maid_outfit(girl)",
    # "preg_3rd_nurse": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_nurse_outfit(girl)",
    # "preg_3rd_secretary": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_working_as_secretary(girl)",
    # "preg_3rd_teacher": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_working_as_teacher(girl)",
    # "preg_3rd_teaching_assistant": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_working_as_teaching_assistant(girl)",
    # "preg_3rd_uniform": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_uniform(girl)",
    # "preg_3rd_athletic": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_athletic_outfit(girl)",
    # "preg_3rd_work": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_work_outfit(girl)",
    # "preg_3rd_clothed": "getattr(girl, 'pregnancy_phase', 0) == 3 and not girl.is_in_underwear() and not girl.is_nude()",


    # # --- Second Trimester ---
    # "preg_2nd_shower": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.id == girls_in_locker_room[2]",
    # "preg_2nd_bare": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.is_nude()",
    # "preg_2nd_swimsuit": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_swimsuit(girl)",
    # "preg_2nd_bikini": "getattr(girl, 'pregnancy_phase', 0) == 2 and (is_wearing_bikini(girl) or is_wearing_swimsuit(girl))",
    # "preg_2nd_underwear": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.is_in_underwear()",
    # "preg_2nd_bottomless": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.is_bottomless()",
    # "preg_2nd_topless": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.is_topless()",
    # "preg_2nd_maid": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_maid_outfit(girl)",
    # "preg_2nd_nurse": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_nurse_outfit(girl)",
    # "preg_2nd_secretary": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_working_as_secretary(girl)",
    # "preg_2nd_teacher": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_working_as_teacher(girl)",
    # "preg_2nd_teaching_assistant": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_working_as_teaching_assistant(girl)",
    # "preg_2nd_uniform": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_uniform(girl)",
    # "preg_2nd_athletic": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_athletic_outfit(girl)",
    # "preg_2nd_work": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_work_outfit(girl)",
    # "preg_2nd_clothed": "getattr(girl, 'pregnancy_phase', 0) == 2 and not girl.is_in_underwear() and not girl.is_nude()",


    # # --- General Pregnancy (Fallback for any visible pregnancy) ---
    # "preg_shower": "is_visibly_pregnant(girl) and girl.id == girls_in_locker_room[2]",
    # "preg_bare": "is_visibly_pregnant(girl) and girl.is_nude()",
    # "preg_swimsuit": "is_visibly_pregnant(girl) and is_wearing_swimsuit(girl)",
    # "preg_bikini": "is_visibly_pregnant(girl) and (is_wearing_bikini(girl) or is_wearing_swimsuit(girl))",
    # "preg_underwear": "is_visibly_pregnant(girl) and girl.is_in_underwear()",
    # "preg_bottomless": "is_visibly_pregnant(girl) and girl.is_bottomless()",
    # "preg_topless": "is_visibly_pregnant(girl) and girl.is_topless()",
    # "preg_maid": "is_visibly_pregnant(girl) and is_wearing_maid_outfit(girl)",
    # "preg_nurse": "is_visibly_pregnant(girl) and is_wearing_nurse_outfit(girl)",
    # "preg_secretary": "is_visibly_pregnant(girl) and is_working_as_secretary(girl)",
    # "preg_teacher": "is_visibly_pregnant(girl) and is_working_as_teacher(girl)",
    # "preg_teaching_assistant": "is_visibly_pregnant(girl) and is_working_as_teaching_assistant(girl)",
    # "preg_uniform": "is_visibly_pregnant(girl) and is_wearing_uniform(girl)",
    # "preg_athletic": "is_visibly_pregnant(girl) and is_wearing_athletic_outfit(girl)",
    # "preg_work": "is_visibly_pregnant(girl) and is_wearing_work_outfit(girl)",
    # "preg_clothed": "is_visibly_pregnant(girl) and not girl.is_in_underwear() and not girl.is_nude()",


    # # =================================================================================
    # # STANDARD OUTFITS (Default Priority)
    # # These are checked only if no pregnancy override conditions were met.
    # # =================================================================================
    
    
    # "shower": "girl.id == girls_in_locker_room[2]",
    # "bare": "girl.is_nude()",

    # "swimsuit": "is_wearing_swimsuit(girl)",
    # "bikini": "is_wearing_bikini(girl) or is_wearing_swimsuit(girl)",

    # "underwear": "girl.is_in_underwear()",

    # "bottomless": "girl.is_bottomless()",
    # "topless": "girl.is_topless()",

    # "maid": "is_wearing_maid_outfit(girl)",
    # "nurse": "is_wearing_nurse_outfit(girl)",
    # "secretary": "is_working_as_secretary(girl)",
    # "teacher": "is_working_as_teacher(girl)",
    # "teaching_assistant": "is_working_as_teaching_assistant(girl)",
    # "uniform": "is_wearing_uniform(girl)",

    # "athletic": "is_wearing_athletic_outfit(girl)",

    # "work": "is_wearing_work_outfit(girl)",
    

    



    # "clothed": "skip",
# }