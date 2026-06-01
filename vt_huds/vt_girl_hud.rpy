# DO NOT overwrite girl_hud - create your own extended version

## Overide the default screen girl_hud

init 1:

    screen girl_hud(girl=None):
        if girl is None:
            if selected_girl:
                $ girl = selected_girl
            # $ girl_id = selected_girl
        
        if girl_hud_girls:
            frame:
                background menu_background_dark
                xalign 0.0
                yalign 0.0
                xpadding 5
                ypadding 5

                $ column_count = min(len(girl_hud_girls), 7)
                vpgrid:
                    cols column_count
                    ysize 75
                    spacing 5
                    draggable True
                    mousewheel True
                    if len(girl_hud_girls) > 7:
                        scrollbars "vertical"

                    for girl_id in girl_hud_girls:
                        $ girl = academy.get_girl_by_id(girl_id, include_pending=True)
                        if not girl:
                            continue

                        $ girl_face_image = fit_image_to_size(girl.image_manager.get_first_face_image(), 75, 75)
                        imagebutton:
                            xalign 0.5
                            yalign 0.5
                            if is_during_home_visit and girl.is_currently_at_work() and girl != selected_girl:
                                idle desaturate_image(girl_face_image)
                                action NullAction()
                                tooltip f"{girl} is currently at work"
                            elif is_during_home_visit and not girl.is_available_at_home() and girl != selected_girl:
                                idle desaturate_image(girl_face_image)
                                action NullAction()
                                tooltip f"{girl} is currently unavailable"
                            else:
                                idle apply_brightness(girl_face_image, 0)
                                hover apply_brightness(girl_face_image)
                                action Show("girl_quick_overview", girl=girl)
                                tooltip f"Overview for {girl}"

    screen girl_quick_overview(girl=None, block_background=True):
        $ girl = girl
        
        if block_background:
            imagebutton:
                xsize 1920
                ysize 1080
                idle "images/none.webp"
                action Hide("girl_quick_overview")
                alternate Hide("girl_quick_overview")

        frame at center_appear:
            xalign 0.5
            yalign 0.5
            xpadding 10
            ypadding 10

            $ girl_face_image = fit_image_to_size(girl.image_manager.get_first_face_image(), 250, 250)

            vbox:
                spacing 5
                hbox:
                    xalign 0.5
                    ysize 450
                    spacing 5

                    frame:
                        background menu_background_light
                        yfill True
                        xsize 400

                        viewport:
                            ysize 450
                            draggable True
                            mousewheel True
                            scrollbars "vertical"
                            
                            vbox:
                                xalign 0.5
                                spacing 10
                                xfill True

                                text "{b}Traits{/b}" size font_size_header color menu_text_color font header_font xalign 0.5
                                hbox:
                                    box_wrap True
                                    # Added Cherry Window (reusable component)
                                    #null height 10
                                    use cherry_window(girl=girl, position="center", border_color="#FF0000", border_size=3)
                                    null height 5
                                    for trait in girl.trait_manager.get_unhidden_traits():
                                        textbutton "[trait]":
                                            text_color menu_text_color
                                            text_size font_size_normal
                                            text_outlines [(1, Color(trait.color).replace_opacity(0.6).hexcode, 0, 0)]
                                            action NullAction()
                                            tooltip trait.get_description()
                                

                    frame:
                        background menu_background_light
                        xsize 400
                        yfill True

                        vbox:
                            xsize 45
                            xalign 0.0
                            spacing 10

                            if girl.can_do_homework() or girl.can_do_training():
                                if girl.active_homework_subject:
                                    $ assigned_homework_subject = girl.homework_subjects[girl.active_homework_subject]
                                    $ assigned_homework_tooltip = f"Assigned: {assigned_homework_subject.name}"

                                    if not assigned_homework_subject.all_lessons_completed():
                                        $ homework_widget = apply_tint("gui/widgets/homework.webp", "#00FF00")
                                    else:
                                        $ homework_widget = apply_tint("gui/widgets/homework.webp", "#4B9CFF")
                                        $ assigned_homework_tooltip += f"\n{{color={menu_text_color_conflict}}}All Lessons Completed{{/color}}"

                                    $ assigned_homework_tooltip += f"\n{girl.get_assigned_homework_tooltip()}"
                                else:
                                    $ assigned_homework_tooltip = f"Assign Homework:\n{girl.get_assigned_homework_tooltip()}"
                                    $ homework_widget = apply_tint("gui/widgets/homework.webp", "#FF0000")
                                imagebutton:
                                    xalign 0.5
                                    yalign 0.5
                                    idle homework_widget
                                    hover apply_brightness(homework_widget)
                                    action Show("girl_homework_assignment_menu", girl=girl)
                                    tooltip assigned_homework_tooltip
                        
                        vbox:
                            xalign 0.5

                            add girl_face_image xalign 0.5

                            $ name_font_size = font_size_header
                            if len(girl.full_name) > 18:
                                $ name_font_size = font_size_sub_header

                            text "[girl.full_name]":
                                xalign 0.5
                                text_align 0.5
                                size name_font_size 
                                font header_font
                                outlines [(4, Color(girl.color).replace_opacity(0.6).hexcode, 0, 0)]

                            $ free_use_compliance = girl.get_acceptance_by_name("free_use_compliance")
                            textbutton "Free-Use Compliance: [free_use_compliance]":
                                xalign 0.5
                                xpadding 0
                                ypadding 0
                                text_size font_size_normal
                                action NullAction()
                                tooltip "A measure of how corrupted and accepting the girl is of the new free-use law.\n\nRaised by increasing a girls corruption and naturism.\nReduced by fear."

                            # TODO - Should have check if they left the school and aren't alumni.
                            # But since they just disappear and can't be interacted with this is fine.
                            if isinstance(girl, Mother):
                                if girl.alumni:
                                    text f"Her daughter {{color={mother_evaluation_colors[1]}}}has{{/color}} since joined the Academy's alumni." size font_size_small color menu_text_color xalign 0.5
                                else:
                                    $ mother_expectations_met = girl.currently_met_expectations()
                                    if mother_expectations_met:
                                        $ expectation_string = f"Expectations Met: {{color={menu_text_color_valid}}}{mother_expectations_met}{{/color}}\n{{i}}{{size=*0.75}}Need to meet her final grade target: {girl.expected_grades}{{/size}}{{/i}}"
                                    else:
                                        $ expectation_string = f"Expectations Met: {{color={menu_text_color_conflict}}}{mother_expectations_met}{{/color}}\n{{i}}{{size=*0.75}}Need to meet her final grade target: {girl.expected_grades}{{/size}}{{/i}}"

                                    text expectation_string size font_size_small color menu_text_color xalign 0.5 text_align 0.5
                            else:
                                if girl.alumni:
                                    text f"She {{color={mother_evaluation_colors[1]}}}has{{/color}} since joined the Academy's alumni." size font_size_small color menu_text_color xalign 0.5
                                else:
                                    if girl.can_join_alumni():
                                        text "Will join Alumni" size font_size_small color menu_text_color_valid xalign 0.5
                                    else:
                                        $ alumni_requirements_tooltip = girl.get_join_alumni_requirements_tooltip()
                                        text alumni_requirements_tooltip size font_size_small color menu_text_color xalign 0.5 text_align 0.5

                    frame:
                        background menu_background_light
                        yfill True
                        xsize 425

                        vbox:
                            xalign 0.5
                            spacing 10

                            text "{b}Stats{/b}" size font_size_header color menu_text_color font header_font xalign 0.5

                            # Stat Bars
                            $ girl_stats_to_display = girl.get_dictionary_of_stats()
                            for stat_name, (stat_value, xp_stat_value) in girl_stats_to_display.items():
                                $ display_name = stat_name.capitalize()

                                $ stat_growth_multiplier, stat_growth_factors = girl.get_stat_growth_multiplier_for_stat(stat_name, include_factors=True)
                                $ stat_growth_multiplier = round(stat_growth_multiplier, 2)
                                $ stat_growth_factors_string = " | ".join(stat_growth_factors)
                                $ stat_growth_tooltip = f"{display_name}\n\nStat Growth Factors:\n{stat_growth_factors_string}"

                                $ xp_requirement = int(calculate_next_xp_threshold(stat_value))
                                if stat_value == 100:
                                    $ xp_stat_value = xp_requirement

                                $ stat_string = f"{display_name} ({stat_value}/100):"

                                $ stat_string = f"{display_name} ({stat_value}/100):"
                                $ stat_tooltip = get_stat_tooltip(stat_name)

                                vbox:
                                    ysize 35
                                    xsize 330
                                    xalign 0.5
                                    hbox:
                                        xsize 360
                                        textbutton "[stat_string]":
                                            ysize 20
                                            xsize 200
                                            yalign 0.5
                                            xpadding 0
                                            text_size font_size_very_small 
                                            text_color menu_text_color
                                            text_hover_color menu_text_color_muted
                                            action NullAction()
                                            tooltip stat_tooltip
                                        
                                        textbutton "Multiplier: x[stat_growth_multiplier]":
                                            ysize 20
                                            xsize 180
                                            yalign 0.5
                                            text_size font_size_very_small 
                                            text_color menu_text_color
                                            text_hover_color menu_text_color_muted
                                            action NullAction()
                                            tooltip stat_growth_tooltip

                                    if stat_name == "grades":
                                        fixed:
                                            ysize 15
                                            bar:
                                                ysize 15
                                                value DictValue(girl_stats_to_display[stat_name], 0, 100)
                                                tooltip stat_tooltip

                                            if not girl.alumni:
                                                $ remaining_grade_period = girl.mother.get_remaining_grade_period()
                                                $ grade_target = girl.mother.get_next_grade_target()
                                                $ grade_separator_xalign = linear_conversion(grade_target, 0, 100, 0.0, 1.0)

                                                if girl.mother.weekly_grade_target_met():
                                                    if grade_target < girl.mother.expected_grades:
                                                        imagebutton:
                                                            xalign grade_separator_xalign 
                                                            yalign 0.5
                                                            xpadding 0
                                                            ypadding 0
                                                            idle apply_tint("gui/widgets/separator_wide.webp", "#55FF64")
                                                            action NullAction()
                                                            tooltip f"{{color={menu_text_color_valid}}}Weekly Grades: {grade_target} is met{{/color}}"
                                                    else:
                                                        imagebutton:
                                                            xalign grade_separator_xalign 
                                                            yalign 0.5
                                                            xpadding 0
                                                            ypadding 0
                                                            idle apply_tint("gui/widgets/separator_wide.webp", "#FF55E5")
                                                            action NullAction()
                                                            tooltip f"{{color={menu_text_color_valid}}}Expected Grades: {girl.mother.expected_grades} is met{{/color}}"
                                                else:
                                                    if grade_target < girl.mother.expected_grades:
                                                        $ grades_tooltip = f"Weekly Grades: {grade_target} is expected to be met by the end of the week"
                                                        if remaining_grade_period:
                                                            $ grades_tooltip += f"\n\n{{color={menu_text_color_valid}}}Remaining Grace Period: {remaining_grade_period} Days{{/color}}"

                                                        imagebutton:
                                                            xalign grade_separator_xalign 
                                                            yalign 0.5
                                                            xpadding 0
                                                            ypadding 0
                                                            idle apply_tint("gui/widgets/separator_wide.webp", menu_text_color_warning)
                                                            action NullAction()
                                                            tooltip grades_tooltip
                                                    else:
                                                        imagebutton:
                                                            xalign grade_separator_xalign 
                                                            yalign 0.5
                                                            xpadding 0
                                                            ypadding 0
                                                            idle "gui/widgets/separator_wide.webp"
                                                            action NullAction()
                                                            tooltip f"Expected Grades: {girl.mother.expected_grades} is her mother's expected grades"

                                                if grade_target != girl.mother.expected_grades:
                                                    $ final_grade_separator_xalign = linear_conversion(girl.mother.expected_grades, 0, 100, 0.0, 1.0)
                                                    if girl.mother.currently_met_expectations():
                                                        imagebutton:
                                                            xalign final_grade_separator_xalign 
                                                            yalign 0.5
                                                            xpadding 0
                                                            ypadding 0
                                                            idle apply_tint("gui/widgets/separator_wide.webp", "#FF55E5")
                                                            action NullAction()
                                                            tooltip f"{{color={menu_text_color_valid}}}Expected Grades: {girl.mother.expected_grades} is met{{/color}}"
                                                    else:
                                                        imagebutton:
                                                            xalign final_grade_separator_xalign 
                                                            yalign 0.5
                                                            xpadding 0
                                                            ypadding 0
                                                            idle "gui/widgets/separator_wide.webp"
                                                            action NullAction()
                                                            tooltip f"Expected Grades: {girl.mother.expected_grades} needed to pass girl"
                                    else:
                                        fixed:
                                            ysize 15

                                            $ stat_limit = 100
                                            $ stat_tooltip = f"XP: {xp_stat_value}/{xp_requirement}"
                                            if stat_name in girl.stat_limits:
                                                $ stat_limit = girl.get_stat_limit(stat_name)
                                                if stat_limit != 100:
                                                    $ stat_tooltip += f"\n\n{girl.get_stat_limit_tooltip(stat_name)}"

                                            bar:
                                                ysize 15
                                                value DictValue(girl_stats_to_display[stat_name], 0, 100)
                                                tooltip stat_tooltip

                                            if stat_limit != 100:
                                                $ stat_separator_xalign = linear_conversion(stat_limit, 0, 100, 0.0, 1.0)
                                                imagebutton:
                                                    xalign stat_separator_xalign 
                                                    yalign 0.5
                                                    xpadding 0
                                                    ypadding 0
                                                    idle apply_tint("gui/widgets/separator_wide.webp", menu_text_color_warning)
                                                    action NullAction()

                hbox:
                    xalign 0.5
                    ysize 450
                    spacing 5

                    frame:
                        background menu_background_light
                        yfill True
                        xsize 400

                        vbox:
                            xalign 0.5
                            spacing 10

                            text "{b}Additional Stats{/b}" size font_size_header color menu_text_color font header_font xalign 0.5
                            $ stats_multipliers_to_display = ("obedience_factor", "emotional_strength", "people_skill", "financial_need", "fame", "shoot_proficiency", "shoot_acceptance")
                            for stat_name in stats_multipliers_to_display:
                                $ display_name = stat_name.replace("_", " ").title()
                                $ stat_tooltip = girl.get_stat_tooltip(stat_name)
                                $ stat_value = girl.get_base_stat_modifier_for_stat(stat_name)
                                $ stat_value = round(getattr(girl, stat_name), 3)

                                textbutton f"{{color={menu_text_color_hover}}}{display_name}:{{/color}} {stat_value}":
                                    text_size font_size_small 
                                    text_hover_color menu_text_color
                                    action NullAction()
                                    tooltip stat_tooltip

                    frame:
                        background menu_background_light
                        yfill True
                        xsize 400

                        vbox:
                            xalign 0.5
                            spacing 10

                            text "{b}Punishments{/b}" size font_size_header color menu_text_color font header_font xalign 0.5
                            if girl.punishments:
                                viewport:
                                    draggable True
                                    mousewheel True
                                    vbox:
                                        spacing 5
                                        for punishment_id in girl.punishments:
                                            $ punishment = girl.punishments[punishment_id]["punishment"]
                                            $ punishment_duration = girl.punishments[punishment_id]["duration_in_days"]
                                            $ punishment_description = punishment.description.replace(f"[duration]", str(punishment_duration))
                                            text f"- {punishment_description}" size font_size_normal color menu_text_color
                            else:
                                text "{b}No Punishments{/b}" size font_size_large color menu_text_color_conflict font header_font xalign 0.5 yalign 0.5

                    if girl.events:
                        frame:
                            background menu_background_light
                            yfill True
                            xsize 425
                            xpadding 2

                            vbox:
                                xalign 0.5
                                spacing 10

                                text "{b}Events{/b}" size font_size_header color menu_text_color font header_font xalign 0.5
                                viewport:
                                    xfill True
                                    ysize 430
                                    draggable True
                                    mousewheel True
                                    scrollbars "vertical"

                                    vbox:
                                        spacing 5
                                        for event in girl.events:
                                            if event.hide_in_menus:
                                                continue

                                            $ requirements_met = event.requirements_met(ignore_participant_availability=True)
                                            $ all_participants_exist = event.all_participants_exist()
                                            $ event_tooltip = event.get_event_tooltip()

                                            button:
                                                xsize 405
                                                idle_background menu_background_light
                                                hover_background menu_background_medium
                                                action NullAction()
                                                tooltip f"{event_tooltip}"

                                                vbox:
                                                    xsize 395
                                                    add event.thumbnail xalign 0.5
                                                    text "[event.display_name]" size font_size_normal color menu_text_color xalign 0.5

                                                    if len(event.participant_ids) > 1:
                                                        text "Participants:" size font_size_small color menu_text_color_muted font header_font xalign 0.5
                                                        hbox:
                                                            xalign 0.5
                                                            spacing 3

                                                            for participant_id in event.participant_ids:
                                                                $ participant_face_image = None
                                                                $ availability_tooltip = ""
                                                                python:
                                                                    participant = academy.get_girl_by_id(participant_id)
                                                                    if not participant:
                                                                        girl_config = academy.get_config_by_id(participant_id)
                                                                        if girl_config:
                                                                            face_image = girl_config.get_first_face_image()
                                                                            participant_face_image = fit_image_to_size(face_image, 70, 70)
                                                                            available_for_event = False
                                                                            availability_tooltip = "This person is unknown to you."
                                                                    else:
                                                                        participant_face_image = fit_image_to_size(participant.image_manager.get_first_face_image(), 70, 70)
                                                                        available_for_event, availability_tooltip = participant.available_for_event(event.event_type, include_reason=True)

                                                                if not participant_face_image:
                                                                    continue

                                                                if participant:
                                                                    fixed:
                                                                        xsize 70
                                                                        ysize 70

                                                                        imagebutton:
                                                                            xsize 70
                                                                            ysize 70
                                                                            xalign 0.5
                                                                            action NullAction()
                                                                            if available_for_event:
                                                                                idle participant_face_image
                                                                            else:
                                                                                idle desaturate_image(apply_brightness(participant_face_image, -0.4))
                                                                            tooltip availability_tooltip

                                                                    if participant.expelled:
                                                                        add fit_image_to_size("gui/widgets/expelled.webp", 70, 70)

                                                                    if participant.left_academy:
                                                                        add fit_image_to_size("gui/widgets/left.webp", 70, 70)
                                                                else:
                                                                    imagebutton:
                                                                        xsize 70
                                                                        ysize 70
                                                                        xalign 0.5
                                                                        idle desaturate_image(apply_brightness(participant_face_image, -0.4))
                                                                        action NullAction()
                                                                        tooltip availability_tooltip

                                                    hbox:
                                                        xsize 390
                                                        if not all_participants_exist:
                                                            $ available_participant_names, unavailable_participant_names = event.get_available_and_unavailable_participant_names()
                                                            text f"Requires: {{color={menu_text_color_conflict}}}{unavailable_participant_names}{{/color}}" size font_size_very_small color menu_text_color xalign 0.5
                                                        elif requirements_met:
                                                            text "[event.trigger_description]" size font_size_very_small color menu_text_color xalign 0.5
                                                        else:
                                                            text "[event.requirement_description]" size font_size_very_small color menu_text_color_conflict xalign 0.5

                    if clothing_debug:
                        frame:
                            background menu_background_light
                            yfill True
                            xsize 400

                            $ outer_button = fit_image_to_size(girl.clothing_manager.outfit["outer"].get_clothing_image_for_part("clothing"), 100)
                            $ upper_button = fit_image_to_size(girl.clothing_manager.outfit["upper"].get_clothing_image_for_part("clothing"), 100)
                            $ bra_button = fit_image_to_size(girl.clothing_manager.outfit["bra"].get_clothing_image_for_part("clothing"), 100)
                            $ lower_button = fit_image_to_size(girl.clothing_manager.outfit["lower"].get_clothing_image_for_part("clothing"), 100)
                            $ panties_button = fit_image_to_size(girl.clothing_manager.outfit["panties"].get_clothing_image_for_part("clothing"), 100)
                            $ socks_button = fit_image_to_size(girl.clothing_manager.outfit["socks"].get_clothing_image_for_part("clothing"), 100)
                            $ shoes_button = fit_image_to_size(girl.clothing_manager.outfit["shoes"].get_clothing_image_for_part("clothing"), 100)
                            $ buttplug_button = fit_image_to_size(girl.clothing_manager.outfit["buttplug"].get_clothing_image_for_part("clothing"), 100)
                            hbox:
                                xalign 0.5
                                yalign 0.5
                                spacing 5

                                vbox:
                                    spacing 5

                                    textbutton "Outer":
                                        style "clothing_button_small"
                                        background outer_button
                                        action NullAction()

                                    textbutton "Upper":
                                        style "clothing_button_small"
                                        background upper_button
                                        action NullAction()

                                    textbutton "Bra":
                                        style "clothing_button_small"
                                        background bra_button
                                        action NullAction()
                                
                                    textbutton "Buttplug":
                                        style "clothing_button_small"
                                        background buttplug_button
                                        action NullAction()

                                vbox:
                                    spacing 5

                                    textbutton "Lower":
                                        style "clothing_button_small"
                                        background lower_button
                                        action NullAction()

                                    textbutton "Panties":
                                        style "clothing_button_small"
                                        background panties_button
                                        action NullAction()

                                    textbutton "Socks":
                                        style "clothing_button_small"
                                        background socks_button
                                        action NullAction()

                                    textbutton "Shoes":
                                        style "clothing_button_small"
                                        background shoes_button
                                        action NullAction()

    style clothing_button_small is button:
        xsize 100
        ysize 100
        
    style clothing_button_small_text is text:
        yalign 1.01
        size font_size_normal
        color menu_text_color
        outlines [(2, "#000000", 0, 0)]
        yfill True