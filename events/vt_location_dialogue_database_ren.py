from main_classes.girl.class_girl_ren import Girl

#actions_already_done = {}
#run after core which is -4

"""renpy
init -3 python:
"""

#Bathroom
    #Check if database_shop_items exists before modifying it
    if "database_student_bathroom_options" in globals():
        original_database = database_student_bathroom_options
        marker_label = "vt_academy_bathroom_sex"
        if not any(label == marker_label for condition, text, label in database_student_bathroom_options):
            # Add small_talk_pregnancy
            database_student_bathroom_options.append(
                ("'vt_academy_bathroom_sex' not in actions_already_done and ((not girl.wants_vaginal_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_vaginal_condom)))", "Offer sex in one of the stalls", "vt_academy_bathroom_sex")
            )
            
            renpy.log("VT MOD: Successfully added vt_academy_bathroom_sex to database.")
        else:
            # The marker was found, so we do nothing to avoid duplicates
            renpy.log("VT MOD: vt_academy_bathroom_sex overrides already found. Skipping addition.")
        renpy.log("VT MOD: Successfully added vt_academy_bathroom_sex to database_student_bathroom_options database")
    else:
        renpy.log("VT MOD ERROR: database_student_bathroom_options not found! Could not add items")

    ## Check if database_small_talk_options exists before modifying it
    if "database_small_talk_options" in globals():
        marker_label = "small_talk_pregnancy"
        if not any(label == marker_label for condition, text, label in database_small_talk_options):
            # The marker is not found, so it's safe to add our new options
            
            # Add small_talk_pregnancy
            database_small_talk_options.append(
                ("True", "Talk about Pregnancy", "small_talk_pregnancy")
            )
            
            # Add small_talk_condoms
            database_small_talk_options.append(
                ("True", "Talk about Condoms", "small_talk_condoms")
            )
            
            # Add small_talk_birth_control
            # database_small_talk_options.append(
                # ("True", "Talk about Birth Control", "small_talk_birth_control")
            # )
            
            renpy.log("VT MOD: Successfully added small_talk_options preg,condoms,bc, database")
        else:
            # The marker was found, so we do nothing to avoid duplicates
            renpy.log("VT MOD: Small talk options already found. Skipping addition.")
    else:
        renpy.log("VT MOD ERROR: small_talk_options not found! Could not add small talk items")

# ## Teacher's Lounge
# database_teacher_discussion_options = [
    # ("True", "Small talk", "teacher_discussion_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("True", "How about a kiss?", "generic_discussion_kiss"),
    # ("'generic_discussion_classroom_sex' not in actions_already_done", "Slip into an empty classroom", "generic_discussion_classroom_sex"),
    # ("girl.is_in_underwear() or girl.is_nude()", "Get dressed", "generic_discussion_get_dressed"),
    # ("not girl.is_in_underwear()", "Wear your underwear", "generic_discussion_strip_to_underwear"),
    # ("not girl.is_nude()", "Get naked", "generic_discussion_get_naked"),
    # ("'lounge_discussion_extra_milk' not in actions_already_done", "Some of {b}her{/b} milk", "lounge_discussion_extra_milk"),
    # ("'lounge_discussion_coffee_creamer' not in actions_already_done", "Offer coffee creamer", "lounge_discussion_coffee_creamer"),
    # ("'lounge_discussion_extra_toppings' not in actions_already_done", "Offer her some extra topping", "lounge_discussion_extra_toppings"),
# ]

# database_teaching_assistant_discussion_options = [
    # ("time_manager.is_other_teachers_class_hours()", "Where is everyone?", "teaching_assistant_discussion_where_is_everyone"),
    # ("True", "Small talk", "teaching_assistant_discussion_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("True", "How about a kiss?", "generic_discussion_kiss"),
    # ("'generic_discussion_classroom_sex' not in actions_already_done", "Slip into an empty classroom", "generic_discussion_classroom_sex"),
    # ("girl.is_in_underwear() or girl.is_nude()", "Get dressed", "generic_discussion_get_dressed"),
    # ("not girl.is_in_underwear()", "Wear your underwear", "generic_discussion_strip_to_underwear"),
    # ("not girl.is_nude()", "Get naked", "generic_discussion_get_naked"),
    # ("'lounge_discussion_extra_milk' not in actions_already_done", "Some of {b}her{/b} milk", "lounge_discussion_extra_milk"),
    # ("'lounge_discussion_coffee_creamer' not in actions_already_done", "Offer coffee creamer", "lounge_discussion_coffee_creamer"),
    # ("'lounge_discussion_extra_toppings' not in actions_already_done", "Offer her some extra topping", "lounge_discussion_extra_toppings"),
# ]


# ## Secretary in Office
# database_secretary_discussion_options = [
    # ("True", "Small talk", "secretary_discussion_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("time_manager.hour > 9 or player.been_to_class", "Call someone in for me|After 9AM/class", "secretary_discussion_call_in_girl"),
    # ("True", "How about a kiss?", "generic_discussion_kiss"),
    # ("'office_stress_relief_options' not in actions_already_done", "Stress Relief", "office_stress_relief_options"),
    # ("secretary.is_in_underwear() or secretary.is_nude()", "Get dressed", "generic_discussion_get_dressed"),
    # ("not secretary.is_in_underwear()", "Wear your underwear", "generic_discussion_strip_to_underwear"),
    # ("not secretary.is_nude()", "Get naked", "generic_discussion_get_naked"),
# ]

# database_office_stress_relief_options = [
    # ("True", "Blowjob", "office_stress_relief_blowjob"),
    # ("True", "Face fuck", "office_stress_relief_face_fuck"),
    # ("True", "Rimjob", "office_stress_relief_rimjob"),
    # ("True", "Bend over my desk", "office_stress_relief_sex"),
# ]


# ## Academy Locations
# database_girl_office_discussion_options = [  # Girl alone in office
    # ("True", "Small talk", "secretary_discussion_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'office_stress_relief_options' not in actions_already_done", "Stress Relief", "office_stress_relief_options"),
# ]
# database_mother_office_discussion_options = [  # Mother alone in office
    # ("True", "Small talk", "secretary_discussion_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'office_stress_relief_options' not in actions_already_done", "Stress Relief", "office_stress_relief_options"),
# ]

# database_alumni_office_discussion_options = [   # Alumni girl alone in office
    # ("True", "Small talk", "secretary_discussion_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'office_stress_relief_options' not in actions_already_done", "Stress Relief", "office_stress_relief_options"),
# ]
# database_alumni_mother_office_discussion_options = [  # Alumni girl alone in office
    # ("True", "Small talk", "secretary_discussion_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'office_stress_relief_options' not in actions_already_done", "Stress Relief", "office_stress_relief_options"),
# ]

# database_student_bathroom_options = [  # Girl alone in bathroom
    # ("'bathroom_apologize_and_leave' not in actions_already_done", "Apologize and leave", "bathroom_apologize_and_leave"),
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'generic_discussion_blowjob' not in actions_already_done", "Suggest a blowjob", "generic_discussion_blowjob"),
    # ("'generic_discussion_strip_tease' not in actions_already_done and not girl.is_nude()", "Suggest a strip tease", "generic_discussion_strip_tease"),
    # ("'bathroom_masturbation_tips' not in actions_already_done", "Offer masturbation tips", "bathroom_masturbation_tips"),
# ]
# database_alumni_bathroom_options = [
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
# ]

# database_student_cafeteria_options = [  # Girl in cafeteria
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'cafeteria_discussion_pay_for_lunch' not in actions_already_done and player.cash >= 25", "Pay for lunch ($25)", "cafeteria_discussion_pay_for_lunch"),
    # ("'generic_discussion_classroom_sex' not in actions_already_done", "Slip into an empty classroom", "generic_discussion_classroom_sex"),
    # ("'cafeteria_discussion_extra_toppings' not in actions_already_done", "Offer her some extra toppings", "cafeteria_discussion_extra_toppings"),
# ]
# database_alumni_cafeteria_options = [
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
# ]

# database_nurse_discussion_options = [  # Alumni working as an academy nurse
    # ("True", "Small talk", "nurse_discussion_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("girl.is_in_underwear() or girl.is_nude()", "Get dressed", "generic_discussion_get_dressed"),
    # ("not girl.is_in_underwear()", "Wear your underwear", "generic_discussion_strip_to_underwear"),
    # ("not girl.is_nude()", "Get naked", "generic_discussion_get_naked"),
    # ("'nurse_discussion_checkup' not in actions_already_done", "Ask for a 'checkup'", "nurse_discussion_checkup"),
    # ("'nurse_discussion_call_in_girl' not in actions_already_done and (time_manager.hour > 9 or player.been_to_class)", "Call someone in for checkup|Once per day and after 9AM/class|Once per day", "nurse_discussion_call_in_girl"),
# ]
# database_student_clinic_options = [  # Girl visiting the nurse in the clinic
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("can_do_checkup(girl)", "Watch girl's checkup", "clinic_discussion_checkup"),
    # ("can_do_checkup(girl)", "Suggest a 'mental' checkup", "clinic_discussion_mental_checkup"),
    # ("can_do_checkup(girl)", "Suggest a 'deep' checkup", "clinic_discussion_deep_checkup"),
# ]
# database_alumni_clinic_options = [
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
# ]

# database_locker_room_options = [  # Girl in her underwear or naked in the locker room, possibly alone
    # ("'locker_room_apologize_and_leave' not in actions_already_done", "Apologize and leave", "locker_room_apologize_and_leave"),
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'generic_discussion_blowjob' not in actions_already_done", "Suggest a blowjob", "generic_discussion_blowjob"),
    # ("'generic_discussion_strip_tease' not in actions_already_done and not girl.is_nude()", "Suggest a strip tease", "generic_discussion_strip_tease"),
    # ("'locker_room_discussion_shower_sex' not in actions_already_done", "Suggest shower sex", "locker_room_discussion_shower_sex"),
# ]
# database_locker_room_shower_options = [  # Girl naked in shower room, possibly alone
    # ("'locker_room_apologize_and_leave' not in actions_already_done", "Apologize and leave", "locker_room_apologize_and_leave"),
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'generic_discussion_blowjob' not in actions_already_done", "Suggest a blowjob", "generic_discussion_blowjob"),
    # ("'locker_room_discussion_shower_sex' not in actions_already_done", "Suggest joining her in there", "locker_room_discussion_shower_sex"),
    # ("'locker_room_discussion_golden_shower' not in actions_already_done", "Golden shower", "locker_room_discussion_golden_shower"),
    # ("'locker_room_discussion_reverse_shower' not in actions_already_done", "Reverse golden shower", "locker_room_discussion_reverse_shower"),
# ]
# database_alumni_locker_room_options = [
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
# ]

# ## Map Locations
# database_bar_bartender_options = [  # Girl is working as a bartender at the bar
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("player.cash >= 25", "Order a drink ($25)", "bar_discussion_order_drink"),
    # ("'bar_discussion_give_tip' not in actions_already_done and ordered_drinks > 0 and player.cash >= 25", "Give tip ($25)", "bar_discussion_give_tip"),
# ]
# database_bar_options = [  # Girl in the bar
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("actions_already_done.count('bar_discussion_buy_girl_drink') < 2 and player.cash >= 25", "Buy her a drink ($25)", "bar_discussion_buy_girl_drink"),
    # ("'bar_discussion_invite_home' not in actions_already_done", "Invite her back to your place", "bar_discussion_invite_home"),
    # ("'bar_discussion_bathroom_quickie' not in actions_already_done", "Bathroom quickie", "bar_discussion_bathroom_quickie"),
    # ("'bar_discussion_creamy_cocktail' not in actions_already_done", "Offer her some cream for her cocktail", "bar_discussion_creamy_cocktail"),
# ]

# database_beach_options = [  # Girl in a bikini at the public beach  
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'beach_discussion_go_for_a_walk' not in actions_already_done", "Go for a walk", "beach_discussion_go_for_a_walk"),
    # ("player.has_item('tan_lotion') and 'beach_discussion_rub_lotion' not in actions_already_done", "Offer her some tanning lotion", "beach_discussion_rub_lotion"),
    # ("'beach_discussion_pee' not in actions_already_done", "Peeing on the beach", "beach_discussion_pee"),
    # ("'beach_discussion_sex' not in actions_already_done", "Sex in the sand", "beach_discussion_sex"),
# ]

# database_park_options = [  # Girl at public park
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'park_discussion_go_for_a_walk' not in actions_already_done", "Go for a walk", "park_discussion_go_for_a_walk"),
    # ("'park_discussion_sex' not in actions_already_done", "Tryst in the trees", "park_discussion_sex"),
    # ("'park_discussion_invite_home' not in actions_already_done", "Invite her back to your place", "park_discussion_invite_home"),
# ]

# database_pier_options = [  # Girl at public pier
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'pier_discussion_go_for_a_walk' not in actions_already_done", "Go for a walk", "pier_discussion_go_for_a_walk"),
    # ("'pier_discussion_sex' not in actions_already_done", "Private time at the pier", "pier_discussion_sex"),
    # ("'pier_discussion_invite_home' not in actions_already_done", "Invite her back to your place", "pier_discussion_invite_home"),
# ]


# database_shoot_assistant_discussion_options = [
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
# ]
# database_student_shoot_studio_options = [
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
# ]

# ## Mall Locations
# database_coffee_shop_barista_options = [  # Girl is working as a barista at the coffee shop in the mall
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("get_action_count('coffee_shop_discussion_order_coffee', actions_already_done) < 4 and player.cash >= 25", "Order a coffee ($25)", "coffee_shop_discussion_order_coffee"),
    # ("'coffee_shop_discussion_give_tip' not in actions_already_done and ordered_coffees > 0 and player.cash >= 25", "Give Tip ($25)", "coffee_shop_discussion_give_tip"),
    # ("'coffee_shop_discussion_charity_donation' not in actions_already_done and player.cash >= 100", "Charity Donation ($100)", "coffee_shop_discussion_charity_donation"),
    # ("block_extra_milk != girl.id and can_order_extra_milk", "Some of {b}her{/b} milk", "coffee_shop_discussion_extra_milk"),
# ]
# database_coffee_shop_options = [  # Girl at coffee shop in the mall
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'coffee_shop_discussion_buy_girl_coffee' not in actions_already_done and player.cash >= 25", "Buy her a coffee ($25)", "coffee_shop_discussion_buy_girl_coffee"),
    # ("'coffee_shop_discussion_extra_cream' not in actions_already_done", "Offer her some cream for her coffee", "coffee_shop_discussion_extra_cream"),
    # ("'coffee_shop_discussion_bathroom_quickie' not in actions_already_done", "Bathroom quickie", "coffee_shop_discussion_bathroom_quickie"),
    # ("'coffee_shop_discussion_talk_in_booth' not in actions_already_done", "Invite to a booth", "coffee_shop_discussion_talk_in_booth"),
# ]

# database_clothing_store_clerk_options = [  # Girl is working as a clerk at clothing store in the mall
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
# ]
# database_clothing_store_options = [  # Girl at clothing store in the mall
    # ("get_action_count('small_talk', actions_already_done) < 2", "Small talk", "make_small_talk"),
    # ("'give_girl_gift' not in actions_already_done", "Give gift|Given a gift today", "give_girl_gift"),
    # ("'clothing_store_discussion_buy_clothing' not in actions_already_done", "Offer to buy her some clothing", "clothing_store_discussion_buy_clothing"),
    # ("'clothing_store_discussion_changing_room_quickie' not in actions_already_done", "Changing room quickie", "clothing_store_discussion_changing_room_quickie"),
# ]
