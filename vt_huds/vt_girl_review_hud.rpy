## Overide the default screen girl_hud
init 1:

    screen girl_review_menu():
        
        # if girl is None:
            # $girl =  selected_girl
            
        use base_computer_menu

        $ selected_radio_button_image = apply_brightness(fit_image_to_size("gui/widgets/radio_selected.webp", 25, 25), 0)
        $ unselected_radio_button_image = apply_brightness(fit_image_to_size("gui/widgets/radio_unselected.webp", 25, 25), 0)

        frame:
            background None
            xsize 1920
            ysize 1042
            xalign 0.5
            ypadding 5
            xpadding 5

            $ url_text = "corrupted_academy/girl_review/"
            if selected_girl:
                $ url_text += f"{selected_girl.config.modder}/{selected_girl.full_name}"

            text "[url_text]" size font_size_small color menu_text_color xpos 0.06 ypos 0.0338

            imagebutton:
                xalign 1.0
                yalign 0
                xoffset 5
                yoffset -5

                idle "gui/widgets/close.webp"
                hover apply_brightness("gui/widgets/close.webp", 0.5)
                action [
                    Hide("girl_review_menu", _layer="master"),
                    Hide("girl_homework_assignment_menu"),
                    Function(girl_review_clear),
                    SetVariable("selected_girl", None),
                    Jump("show_computer_menu")
                ]
                if persistent.right_click_close:
                    keysym "mouseup_3"
                    tooltip "{b}Hotkey{/b}: Right-Click"

            hbox:
                xalign 0.915
                yalign 0.01
                spacing 5
                text "{b}Search{/b}" size font_size_large color menu_text_color font header_font yalign 0.5
                frame:
                    yalign 0.5
                    xsize 300
                    xpadding 5
                    ypadding 5
                    fixed:
                        xsize 300
                        ysize 35
                        imagebutton:
                            xsize 300
                            ysize 35
                            xpadding 0
                            ypadding 0
                            idle "images/none.webp"
                            action Show("girl_review_search_input")
                            tooltip "Searches for girls by name."

                        text "[search_term]" yalign 0.5

            $ resized_info_widget = fit_image_to_size("gui/widgets/info.webp", 40, 40)
            imagebutton:
                xalign 0.96
                yalign 0.01
                idle resized_info_widget
                hover apply_brightness(resized_info_widget, 0.5)
                action SetVariable("show_tutorial", True)
                tooltip "Show Tutorial"

            # Girl Selecting
            frame:
                background menu_background_light
                xsize 442
                ysize 380
                xalign 0.0
                yalign 0.106
                xpadding 5
                ypadding 5

                viewport id "girl_review_girl_vpgrid":
                    yadjustment initialize_adjustment("girl_review_girl_vpgrid")

                    xfill True
                    draggable True
                    mousewheel True
                    scrollbars "vertical"

                    vbox:
                        spacing 3
                        for girl in available_girls:
                            if girl_review_filter_alumni:
                                if girl.alumni:
                                    continue

                            textbutton "[girl.full_name]":
                                style "girl_review_button"
                                xsize 415

                                if girl == selected_girl:
                                    background menu_background_medium
                                    text_color menu_text_color_hover

                                if girl.left_academy:
                                    text_color menu_text_color_conflict
                                    if girl == selected_girl:
                                        text_color menu_text_color_conflict_muted
                                elif girl.alumni:
                                    text_color menu_text_color_alumni
                                    if girl == selected_girl:
                                        text_color menu_text_color_alumni_muted
                                elif girl.expelled:
                                    text_color menu_text_color_conflict
                                    if girl == selected_girl:
                                        text_color menu_text_color_conflict_muted

                                action [
                                    SetVariable("selected_girl", girl),
                                    Jump("save_girl_review_menu")
                            ]

            frame:
                background menu_background_light
                xsize 442
                ysize 96
                xalign 0.0
                yalign 0.485
                xpadding 5
                ypadding 5

                vbox:
                    spacing 3
                    $ sort_text = girl_review_sort_by.replace("_", " ").title()
                    textbutton f"{{color={menu_text_color}}}Sorted by:{{/color}} {sort_text}":
                        xpadding 0
                        ypadding 0
                        text_size font_size_normal
                        text_color gui.hover_color
                        text_hover_color menu_text_color_muted
                        action [
                            CaptureFocus(),
                            Show("girl_review_sort_menu")
                        ]

                    hbox:
                        ysize 25
                        spacing 5
                        text "Filter Alumni:" size font_size_normal color menu_text_color

                        if girl_review_filter_alumni:
                            imagebutton:
                                yalign 0.5
                                idle apply_brightness(selected_radio_button_image)
                                hover apply_brightness(selected_radio_button_image, 0.5)
                                action ToggleVariable("girl_review_filter_alumni", True, False)
                        else:
                            imagebutton:
                                yalign 0.5
                                idle apply_brightness(unselected_radio_button_image)
                                hover apply_brightness(unselected_radio_button_image, 0.5)
                                action ToggleVariable("girl_review_filter_alumni", True, False)

                    hbox:
                        ysize 25
                        spacing 5
                        text "Review Mothers:" size font_size_normal color menu_text_color

                        if selected_girl:
                            if review_mother:
                                imagebutton:
                                    yalign 0.5
                                    idle selected_radio_button_image
                                    hover apply_brightness(selected_radio_button_image, 0.5)
                                    action [
                                        ToggleVariable("review_mother", True, False),
                                        SetVariable("selected_girl", selected_girl.daughter),
                                        Function(change_available_girls), 
                                        Jump("save_girl_review_menu")
                                    ]
                            else:
                                imagebutton:
                                    yalign 0.5
                                    idle unselected_radio_button_image
                                    hover apply_brightness(unselected_radio_button_image, 0.5)
                                    action [
                                        ToggleVariable("review_mother", True, False),
                                        SetVariable("selected_girl", selected_girl.mother),
                                        Function(change_available_girls), 
                                        Jump("save_girl_review_menu")
                                    ]
                        else:
                            if review_mother:
                                imagebutton:
                                    yalign 0.5
                                    idle selected_radio_button_image
                                    hover apply_brightness(selected_radio_button_image, 0.5)
                                    action [
                                        ToggleVariable("review_mother", True, False),
                                        Function(change_available_girls), 
                                        Jump("save_girl_review_menu")
                                    ]
                            else:
                                imagebutton:
                                    yalign 0.5
                                    idle unselected_radio_button_image
                                    hover apply_brightness(unselected_radio_button_image, 0.5)
                                    action [
                                        ToggleVariable("review_mother", True, False),
                                        Function(change_available_girls), 
                                        Jump("save_girl_review_menu")
                                    ]

            if selected_girl:
                # Girl Info
                frame:
                    background menu_background_light
                    xsize 1016
                    ysize 480
                    xalign 0.5
                    yalign 0.126
                    xpadding 5
                    ypadding 5

                    hbox:
                        xalign 0.0
                        spacing 5
                        ysize 480

                        vbox:
                            xsize 350
                            xalign 0.0
                            spacing 5

                            null height 5
                            
                            hbox:
                                xsize 380
                                ysize 300
                                xalign 0.5
                                yalign 0.5
                                spacing 5

                                vbox:
                                    xsize 45
                                    xalign 0.0
                                    spacing 10

                                    # PLANNED - Maybe add option after a girl passes to get her to join alumni or come back as a student for another degree.
                                    if not (selected_girl.expelled or selected_girl.left_academy):
                                        imagebutton:
                                            xalign 0.5
                                            yalign 0.5
                                            if (review_mother and (selected_girl.player_called_today or selected_girl.daughter.player_called_today)) or (not review_mother and (selected_girl.player_called_today or selected_girl.mother.player_called_today)):
                                                idle apply_brightness("gui/widgets/phone.webp", -0.1)
                                                action NullAction()
                                                tooltip "Already called today"
                                            elif (review_mother and not selected_girl.is_available_at_home() and not selected_girl.daughter.is_available_at_home()) or (not review_mother and not selected_girl.is_available_at_home() and not selected_girl.mother.is_available_at_home()):
                                                idle apply_brightness("gui/widgets/phone.webp", -0.1)
                                                action NullAction()
                                                tooltip "Neither are currently at home"
                                            elif time_manager.hour >= 10 and time_manager.hour < 18:
                                                idle "gui/widgets/phone.webp"
                                                hover apply_brightness("gui/widgets/phone.webp")
                                                action Jump("computer_start_home_visit_call")
                                                tooltip f"Visit {selected_girl}'s house."
                                            else:
                                                idle apply_brightness("gui/widgets/phone.webp", -0.1)
                                                action NullAction()
                                                tooltip "Only Available: 10:00-18:00"

                                        if selected_girl.can_do_homework() or selected_girl.can_do_training():
                                            if selected_girl.active_homework_subject:
                                                $ assigned_homework_subject = selected_girl.homework_subjects[selected_girl.active_homework_subject]
                                                $ assigned_homework_tooltip = f"Assigned: {assigned_homework_subject.name}"

                                                if not assigned_homework_subject.all_lessons_completed():
                                                    $ homework_widget = apply_tint("gui/widgets/homework.webp", "#00FF00")
                                                else:
                                                    $ homework_widget = apply_tint("gui/widgets/homework.webp", "#4B9CFF")
                                                    $ assigned_homework_tooltip += f"\n{{color={menu_text_color_conflict}}}All Lessons Completed{{/color}}"

                                                $ assigned_homework_tooltip += f"\n{selected_girl.get_assigned_homework_tooltip()}"
                                            else:
                                                $ assigned_homework_tooltip = f"Assign Homework:\n{selected_girl.get_assigned_homework_tooltip()}"
                                                $ homework_widget = apply_tint("gui/widgets/homework.webp", "#FF0000")

                                            imagebutton:
                                                xalign 0.5
                                                yalign 0.5
                                                idle homework_widget
                                                hover apply_brightness(homework_widget)
                                                action Show("girl_homework_assignment_menu", girl=selected_girl)
                                                tooltip assigned_homework_tooltip

                                        if not review_mother and not selected_girl.alumni:
                                            $ alumni_requirements_tooltip = f"To Join Alumni:\n{selected_girl.get_join_alumni_requirements_tooltip()}"
                                            $ pass_options_tooltip = selected_girl.get_pass_options_tooltip() + "\n\n" + alumni_requirements_tooltip
                                            imagebutton:
                                                xalign 0.5
                                                yalign 0.5
                                                idle "gui/widgets/pass.webp"
                                                hover apply_brightness("gui/widgets/pass.webp")
                                                if selected_girl.can_be_passed() or selected_girl.get_acceptance_by_name("free_use_compliance") >= 75:
                                                    action Jump("computer_start_mother_pass_call")
                                                    if selected_girl.can_join_alumni():
                                                        tooltip f"{{color={menu_text_color_valid}}}Pass {selected_girl} - Will join Alumni{{/color}}"
                                                    else:
                                                        tooltip f"{{color={menu_text_color_valid}}}Pass {selected_girl}{{/color}}\n\n{alumni_requirements_tooltip}"
                                                else:
                                                    action NullAction()
                                                    tooltip f"Pass {selected_girl}\n\nTo Pass:\n{pass_options_tooltip}"

                                            $ expel_options_tooltip = selected_girl.get_expel_options_tooltip()
                                            imagebutton:
                                                xalign 0.5
                                                yalign 0.5
                                                idle "gui/widgets/ban.webp"
                                                hover apply_brightness("gui/widgets/ban.webp")
                                                if selected_girl.can_be_expelled():
                                                    action Jump("computer_start_mother_expulsion_call")
                                                    tooltip f"{{color={menu_text_color_conflict}}}Expel {selected_girl}{{/color}}"
                                                else:
                                                    action NullAction()
                                                    tooltip f"Expel {selected_girl}\n\nTo Expel:\n{expel_options_tooltip}"

                                    if selected_girl.webms:
                                        imagebutton:
                                            xalign 0.5
                                            yalign 0.5
                                            idle "gui/widgets/video_button.webp"
                                            hover apply_brightness("gui/widgets/video_button.webp", 0.5)
                                            action Jump("show_girl_webm_review_menu")
                                            tooltip "Video Review"

                                    if debug_mode and not renpy.android:
                                        imagebutton:
                                            xalign 0.5
                                            yalign 0.5
                                            idle "gui/widgets/bug.webp"
                                            hover apply_brightness("gui/widgets/bug.webp", 0.5)
                                            action Jump("show_single_girl_rating_menu_from_review")
                                            tooltip "Error Checking"

                                fixed:
                                    xsize 300
                                    ysize 300

                                    imagebutton:
                                        idle girl_face_image

                                    if not review_mother:
                                        if selected_girl.left_academy:
                                            imagebutton:
                                                idle "gui/widgets/left.webp"
                                        elif selected_girl.alumni:
                                            imagebutton:
                                                idle "gui/widgets/alumni.webp" xalign 0.98 yalign 0.02
                                                action NullAction()
                                                tooltip "Alumni"
                                        elif selected_girl.expelled:
                                            imagebutton:
                                                idle "gui/widgets/expelled.webp"

                                    if academy.pta_president and selected_girl == academy.pta_president:
                                        imagebutton:
                                            xalign 0.98
                                            yalign 0.02
                                            idle "gui/widgets/crown.webp"
                                            hover apply_brightness("gui/widgets/crown.webp")
                                            action NullAction()
                                            tooltip "PTA President"

                            vbox:
                                xsize 330
                                xalign 1.0
                                if len(selected_girl.full_name) > 12:
                                    text "[selected_girl.full_name]":
                                        xalign 0.5
                                        size font_size_very_large 
                                        font header_font
                                        outlines [(4, Color(selected_girl.color).replace_opacity(0.6).hexcode, 0, 0)]
                                else:
                                    text "[selected_girl.full_name]":
                                        xalign 0.5
                                        size font_size_header 
                                        font header_font
                                        outlines [(4, Color(selected_girl.color).replace_opacity(0.6).hexcode, 0, 0)]

                                if not review_mother:
                                    $ stat_tooltip = get_stat_tooltip("tolerance")
                                    
                                    textbutton "Tolerance: [selected_girl.max_tolerance]":
                                        xalign 0.5
                                        xpadding 0
                                        ypadding 0
                                        text_size font_size_normal
                                        action NullAction()
                                        tooltip stat_tooltip

                                $ free_use_compliance = selected_girl.get_acceptance_by_name("free_use_compliance")
                                textbutton "Free-Use Compliance: [free_use_compliance]":
                                    xalign 0.5
                                    xpadding 0
                                    ypadding 0
                                    text_size font_size_normal
                                    action NullAction()
                                    tooltip "A measure of how corrupted and accepting the girl is of the new free-use law.\n\nRaised by increasing a girls corruption and naturism.\nReduced by fear."

                        vbox:
                            xsize 350
                            xalign 0.0
                            spacing 5

                            null height 10

                            # Stat Bars
                            $ girl_stats_to_display = selected_girl.get_dictionary_of_stats()
                            for stat_name, (stat_value, xp_stat_value) in girl_stats_to_display.items():
                                $ display_name = stat_name.capitalize()

                                $ stat_growth_multiplier, stat_growth_factors = selected_girl.get_stat_growth_multiplier_for_stat(stat_name, include_factors=True)
                                $ stat_growth_multiplier = round(stat_growth_multiplier, 2)
                                $ stat_growth_factors_string = " | ".join(stat_growth_factors)
                                $ stat_growth_tooltip = f"{display_name}\n\nStat Growth Factors:\n{stat_growth_factors_string}"

                                $ xp_requirement = int(calculate_next_xp_threshold(stat_value))

                                $ stat_string = f"{display_name} ({stat_value}/100):"
                                $ stat_tooltip = get_stat_tooltip(stat_name)
                                if xp_stat_value:
                                    if stat_value == 100:
                                        $ xp_stat_value = xp_requirement

                                vbox:
                                    xsize 360
                                    ysize 35
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
                                            xsize 360
                                            bar:
                                                ysize 15
                                                value DictValue(girl_stats_to_display[stat_name], 0, 100)
                                                tooltip stat_tooltip

                                            if not selected_girl.alumni:
                                                $ remaining_grade_period = selected_girl.mother.get_remaining_grade_period()
                                                $ grade_target = selected_girl.mother.get_next_grade_target()
                                                $ grade_separator_xalign = linear_conversion(grade_target, 0, 100, 0.0, 1.0)

                                                if selected_girl.mother.weekly_grade_target_met():
                                                    if grade_target < selected_girl.mother.expected_grades:
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
                                                            tooltip f"{{color={menu_text_color_valid}}}Expected Grades: {selected_girl.mother.expected_grades} is met{{/color}}"
                                                else:
                                                    if grade_target < selected_girl.mother.expected_grades:
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
                                                            tooltip f"Expected Grades: {selected_girl.mother.expected_grades} is her mother's expected grades"

                                                if grade_target != selected_girl.mother.expected_grades:
                                                    $ final_grade_separator_xalign = linear_conversion(selected_girl.mother.expected_grades, 0, 100, 0.0, 1.0)
                                                    if selected_girl.mother.currently_met_expectations():
                                                        imagebutton:
                                                            xalign final_grade_separator_xalign 
                                                            yalign 0.5
                                                            xpadding 0
                                                            ypadding 0
                                                            idle apply_tint("gui/widgets/separator_wide.webp", "#FF55E5")
                                                            action NullAction()
                                                            tooltip f"{{color={menu_text_color_valid}}}Expected Grades: {selected_girl.mother.expected_grades} is met{{/color}}"
                                                    else:
                                                        imagebutton:
                                                            xalign final_grade_separator_xalign 
                                                            yalign 0.5
                                                            xpadding 0
                                                            ypadding 0
                                                            idle "gui/widgets/separator_wide.webp"
                                                            action NullAction()
                                                            tooltip f"Expected Grades: {selected_girl.mother.expected_grades} needed to pass girl"
                                    else:
                                        fixed:
                                            ysize 15

                                            $ stat_limit = 100
                                            $ stat_tooltip = f"XP: {xp_stat_value}/{xp_requirement}"
                                            if stat_name in selected_girl.stat_limits:
                                                $ stat_limit = selected_girl.get_stat_limit(stat_name)
                                                if stat_limit != 100:
                                                    $ stat_tooltip += f"\n\n{selected_girl.get_stat_limit_tooltip(stat_name)}"

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

                            null height 10

                            if review_mother:
                                if selected_girl.expelled or selected_girl.left_academy or selected_girl.alumni:
                                    if selected_girl.alumni:
                                        text f"Her daughter {{color={mother_evaluation_colors[1]}}}has{{/color}} since joined the Academy's alumni." size font_size_small color menu_text_color
                                    else:
                                        text f"Her daughter did {{color={mother_evaluation_colors[0]}}}not{{/color}} join the Academy's alumni." size font_size_small color menu_text_color
                                else:
                                    if selected_girl.player_warnings > 0:
                                        textbutton "{b}Grades Warning{/b}":
                                            xpadding 0
                                            ypadding 0
                                            text_size font_size_normal
                                            text_color menu_text_color_conflict
                                            action NullAction()
                                            tooltip f"She has given you a warning about missing her grades.\nFailing to meet them again will result in {{color={selected_girl.daughter.color}}}{selected_girl.daughter.full_name}{{/color}} being {{color={menu_text_color_conflict}}}removed{{/color}} from the academy."

                                    $ expectations_met = selected_girl.currently_met_expectations()
                                    if expectations_met:
                                        $ expectation_string = f"Expectations Met: {{color={menu_text_color_valid}}}{expectations_met}{{/color}}\n{{i}}{{size=*0.75}}Need to meet her final grade target: {selected_girl.expected_grades}{{/size}}{{/i}}"
                                    else:
                                        $ expectation_string = f"Expectations Met: {{color={menu_text_color_conflict}}}{expectations_met}{{/color}}\n{{i}}{{size=*0.75}}Need to meet her final grade target: {selected_girl.expected_grades}{{/size}}{{/i}}"

                                    text "[expectation_string]" size font_size_small color menu_text_color

                                    if selected_girl.player_warnings > 0:
                                        $ warnings_string = "{color=[mother_evaluation_colors[0]]}[selected_girl.player_warnings]{/color}"
                                    else:
                                        $ warnings_string = "{color=[mother_evaluation_colors[1]]}[selected_girl.player_warnings]{/color}"

                                    text f"She has given you {warnings_string} warnings" size font_size_small color menu_text_color

                                    if "force_pta_vote" in selected_girl.punishments:
                                        $ force_vote_string = "Is {color=[mother_evaluation_colors[1]]}forced{/color} to vote in your favor."
                                    else:
                                        $ force_vote_string = "Is {color=[mother_evaluation_colors[0]]}not{/color} forced to vote in your favor."

                                    text force_vote_string size font_size_small color menu_text_color

                                    if "force_tolerated_actions" in selected_girl.punishments or "force_tolerated_actions" in selected_girl.daughter.punishments:
                                        $ forced_tolerated_string = "Is {color=[mother_evaluation_colors[1]]}forced{/color} to tolerate your actions."
                                    else:
                                        $ forced_tolerated_string = "Is {color=[mother_evaluation_colors[0]]}not{/color} forced to tolerate your actions."

                                    text forced_tolerated_string size font_size_small color menu_text_color

                                    $ remaining_grade_period = selected_girl.get_remaining_grade_period()
                                    if remaining_grade_period:
                                        $ grade_period_string = f"Remaining Grace Period: {{color={menu_text_color_valid}}}{remaining_grade_period} Days{{/color}}"
                                        text "[grade_period_string]" size font_size_small color menu_text_color
                            else:
                                if selected_girl.expelled or selected_girl.left_academy or selected_girl.alumni:
                                    if selected_girl.alumni:
                                        text f"She {{color={mother_evaluation_colors[1]}}}has{{/color}} since joined the Academy's alumni." size font_size_small color menu_text_color
                                    else:
                                        text f"She did {{color={mother_evaluation_colors[0]}}}not{{/color}} join the Academy's alumni." size font_size_small color menu_text_color
                                else:
                                    if selected_girl.mother.player_warnings > 0:
                                        textbutton "{b}Mother Warning{/b}":
                                            xpadding 0
                                            ypadding 0
                                            text_size font_size_normal
                                            text_color menu_text_color_conflict
                                            action NullAction()
                                            tooltip f"Her mother has given you a warning about missing her grades.\nFailing to meet them again will result in her being {{color={menu_text_color_conflict}}}removed{{/color}} from the academy."

                                    $ mother_expectations_met = selected_girl.mother.currently_met_expectations()
                                    if mother_expectations_met:
                                        $ expectation_string = f"Mother Expectations Met: {{color={menu_text_color_valid}}}{mother_expectations_met}{{/color}}\n{{i}}{{size=*0.75}}Need to meet her final grade target: {selected_girl.mother.expected_grades}{{/size}}{{/i}}"
                                    else:
                                        $ expectation_string = f"Mother Expectations Met: {{color={menu_text_color_conflict}}}{mother_expectations_met}{{/color}}\n{{i}}{{size=*0.75}}Need to meet her final grade target: {selected_girl.mother.expected_grades}{{/size}}{{/i}}"

                                    text "[expectation_string]" size font_size_small color menu_text_color

                                    if "force_tolerated_actions" in selected_girl.punishments:
                                        $ forced_tolerated_string = "Is {color=[mother_evaluation_colors[1]]}forced{/color} to tolerate your actions."
                                    else:
                                        $ forced_tolerated_string = "Is {color=[mother_evaluation_colors[0]]}not{/color} forced to tolerate your actions."

                                    text forced_tolerated_string size font_size_small color menu_text_color

                                    $ remaining_grade_period = selected_girl.mother.get_remaining_grade_period()
                                    if remaining_grade_period:
                                        $ grade_period_string = f"Remaining Grace Period: {{color={menu_text_color_valid}}}{remaining_grade_period} Days{{/color}}"
                                        text "[grade_period_string]" size font_size_small color menu_text_color

                        # Stat Multipliers
                        vbox:
                            yalign 0.1

                            $ stats_multipliers_to_display = ("obedience_factor", "emotional_strength", "people_skill", "financial_need", "fame", "shoot_proficiency", "shoot_acceptance")
                            for stat_name in stats_multipliers_to_display:
                                $ display_name = stat_name.replace("_", " ").title()
                                $ stat_tooltip = selected_girl.get_stat_tooltip(stat_name)
                                $ stat_value = selected_girl.get_base_stat_modifier_for_stat(stat_name)
                                $ stat_value = round(getattr(selected_girl, stat_name), 3)

                                textbutton f"{{color={menu_text_color_hover}}}{display_name}:{{/color}} {stat_value}":
                                    text_size font_size_small 
                                    text_hover_color menu_text_color
                                    action NullAction()
                                    tooltip stat_tooltip

                # New
                frame:
                    background menu_background_light
                    xsize 442
                    ysize 963
                    xalign 1.0
                    yalign 1.0
                    xpadding 5
                    ypadding 5

                    vbox:
                        xfill True
                        
                        null height 7
                        use cherry_minimum_window(girl=selected_girl, position="bottom", border_color="#FF0000", border_size=3)

                        text "Action Tracker (WIP)" size font_size_large color menu_text_color font header_font xalign 0.5

                        null height 3
                        add "gui/widgets/separator_h_wide.webp" xsize 200 xalign 0.5
                        null height 3

                        viewport:  # TODO - Add categories
                            xfill True
                            draggable True
                            mousewheel True
                            scrollbars "vertical"
                            vscrollbar_unscrollable "hide"
                            xalign 0.5

                            vbox:
                                xfill True
                                spacing 3

                                $ has_actions = False
                                for action_name, action_count in selected_girl.general_action_tracker.items():
                                    $ action_title, action_description = get_girl_action_data(selected_girl, action_name)
                                    if not action_title:
                                        continue

                                    vbox:
                                        xalign 0.5

                                        text "{b}[action_title]: [action_count]{/b}" size font_size_normal color menu_text_color xalign 0.5

                                        if action_description:
                                            $ has_actions = True
                                            text "[action_description]" size font_size_small color menu_text_color xalign 0.5

                    if not has_actions:
                        text "No actions tracked" size font_size_normal color menu_text_color_conflict xalign 0.5 yalign 0.5

                # Content
                frame:
                    background menu_background_light
                    xsize 442
                    ysize 478
                    xalign 0.0
                    yalign 1.0
                    ypadding 5
                    xpadding 5

                    vbox:
                        spacing 5
                        first_spacing 10
                        $ resized_next_widget = fit_image_to_size("gui/widgets/next.webp", 25, 25)
                        $ resized_prev_widget = fit_image_to_size("gui/widgets/prev.webp", 25, 25)
                        hbox:
                            xsize 433
                            imagebutton:
                                xalign 0
                                yalign 0.5
                                idle resized_prev_widget
                                hover apply_brightness(resized_prev_widget)
                                action [
                                    # CycleVariable("selected_content_type", ["photoshoots", "videoshoots", "events", "wardrobe"], reverse=True),
                                    CycleVariable("selected_content_type", ["photoshoots", "videoshoots", "events"], reverse=True),
                                    Jump("save_girl_review_menu")
                                ]

                            text "{b}[selected_content_type.title()]{/b}" size font_size_large color menu_text_color font header_font text_align 0.5 xalign 0.5
        
                            imagebutton:
                                xalign 1.0
                                yalign 0.5
                                idle resized_next_widget
                                hover apply_brightness(resized_next_widget)
                                action [
                                    # CycleVariable("selected_content_type", ["photoshoots", "videoshoots", "events", "wardrobe"]),
                                    CycleVariable("selected_content_type", ["photoshoots", "videoshoots", "events"]),
                                    Jump("save_girl_review_menu")
                                ]

                        if selected_content_type == "events":
                            viewport id "girl_review_events_vpgrid":
                                yadjustment initialize_adjustment("girl_review_events_vpgrid")

                                xfill True
                                ysize 430
                                yalign 1.0
                                spacing 4
                                draggable True
                                mousewheel True
                                scrollbars "vertical"
                                vscrollbar_unscrollable "hide"

                                vbox:
                                    spacing 5
                                    for event in selected_girl.events:
                                        if event.hide_in_menus:
                                            continue

                                        $ requirements_met = event.requirements_met(ignore_participant_availability=True)
                                        $ all_participants_exist = event.all_participants_exist()
                                        $ event_tooltip = event.get_event_tooltip()

                                        button:
                                            xsize 415
                                            idle_background menu_background_light
                                            hover_background menu_background_medium
                                            if selected_girl.event_completed(event.name) and event.all_participants_available(ignore_availability=True):
                                                action Function(event_manager.force_start_event, event=event)
                                                tooltip f"{{color={menu_text_color_valid}}}Can 'Relive' Event{{/color}}\n{event_tooltip}"
                                            else:
                                                if debug_mode and event.all_participants_available(ignore_availability=True):
                                                    action Function(event_manager.force_start_event, event=event)
                                                    tooltip f"{{color={menu_text_color_valid}}}Can Force Start Event{{/color}}\n{event_tooltip}"
                                                else:
                                                    action NullAction()
                                                    tooltip f"{event_tooltip}"

                                            vbox:
                                                xsize 415
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
                                                    xsize 405
                                                    if not all_participants_exist:
                                                        $ available_participant_names, unavailable_participant_names = event.get_available_and_unavailable_participant_names()
                                                        text f"Requires: {{color={menu_text_color_conflict}}}{unavailable_participant_names}{{/color}}" size font_size_very_small color menu_text_color xalign 0.5
                                                    elif requirements_met:
                                                        text "[event.trigger_description]" size font_size_very_small color menu_text_color xalign 0.5
                                                    else:
                                                        text "[event.requirement_description]" size font_size_very_small color menu_text_color_conflict xalign 0.5

                        elif selected_content_type == "wardrobe":
                            $ seen_clothing_count = len(selected_girl.clothing_manager.get_all_seen_clothing())
                            if seen_clothing_count < 1:
                                text "{b}No clothing seen yet{/b}" size font_size_normal color menu_text_color_conflict xalign 0.5 yalign 0.5
                            else:
                                viewport id "girl_review_wardrobe_vpgrid":
                                    yadjustment initialize_adjustment("girl_review_wardrobe_vpgrid")

                                    xfill True
                                    ysize 430
                                    yalign 1.0
                                    draggable True
                                    mousewheel True
                                    scrollbars "vertical"
                                    vscrollbar_unscrollable "hide"

                                    vbox:
                                        xsize 410
                                        spacing 10

                                        for clothing_type in selected_girl.clothing_manager.wardrobe:
                                            $ seen_clothing = selected_girl.clothing_manager.get_seen_clothing(clothing_type)
                                            if clothing_type == "nipple_acc":
                                                $ clothing_type_string = "Nipple Accessories"
                                            elif clothing_type == "pussy_acc":
                                                $ clothing_type_string = "Pussy Accessories"
                                            else:
                                                $ clothing_type_string = clothing_type.capitalize()

                                            text "{b}[clothing_type_string]{/b}" size font_size_normal color menu_text_color

                                            $ seen_clothing = selected_girl.clothing_manager.get_seen_clothing(clothing_type)
                                            if not seen_clothing:
                                                text "Haven't seen any clothing of this type" size font_size_small color menu_text_color_conflict xalign 0.5 xoffset 30
                                            else:
                                                vpgrid:
                                                    xsize 410
                                                    yminimum 64
                                                    cols 6
                                                    spacing 5
                                                    for clothing_item in seen_clothing:
                                                        $ clothing_image = clothing_item.get_clothing_image_for_part("clothing")

                                                        imagebutton:
                                                            idle fit_image_to_size(clothing_image, 64, 64)
                                                            action NullAction()
                                                            tooltip clothing_item
                        else:
                            viewport id "girl_review_shoot_vpgrid":
                                yadjustment initialize_adjustment("girl_review_shoot_vpgrid")

                                xfill True
                                draggable True
                                mousewheel True
                                scrollbars "vertical"
                                vscrollbar_unscrollable "hide"

                                vbox:
                                    spacing 5
                                    for shoot in available_girl_shoots:
                                        $ file_count = len(shoot.file_list)
                                        $ unlocked_file_count = shoot.get_unlocked_file_count()
                                        hbox:
                                            xsize 405
                                            spacing 2
                                            $ cover_image = apply_brightness(fit_image_to_size(shoot.cover_image, 115, 65), 0)
                                            if not shoot.can_be_attempted():
                                                $ cover_image = desaturate_image(cover_image)

                                            $ requirement_description = shoot.get_requirement_description()
                                            if isinstance(requirement_description, (list, tuple)):
                                                $ requirement_description = "\n".join(requirement_description)

                                            fixed:
                                                xsize 115
                                                ysize 65
                                                imagebutton:
                                                    xalign 0.5
                                                    yalign 0.5
                                                    idle cover_image
                                                    hover apply_brightness(cover_image)
                                                    action [
                                                        SetVariable("selected_shoot", shoot),
                                                        Jump("show_shoot_review_menu")
                                                    ]
                                                    tooltip requirement_description

                                            vbox:
                                                xsize 270
                                                yalign 0.5
                                                text "[shoot.display_name]" size font_size_normal color menu_text_color xpos 10
                                                text "Taken: [unlocked_file_count]/[file_count] " size font_size_very_small color menu_text_color xpos 10

                # Traits & Additional Info + New(Unused)
                hbox:
                    xsize 1016
                    xalign 0.5
                    yalign 1.0
                    spacing 5

                    vbox:
                        xsize 508
                        ysize 478
                        spacing 5

                        frame:
                            background menu_background_light
                            ysize 300
                            xfill True

                            vbox:
                                text "Traits:" size font_size_large color menu_text_color font header_font
                                viewport:
                                    xfill True
                                    draggable True
                                    mousewheel True

                                    hbox:
                                        xmaximum 508
                                        spacing 5
                                        box_wrap True

                                        for trait in selected_girl.trait_manager.get_unhidden_traits():
                                            textbutton "[trait]":
                                                text_color menu_text_color
                                                text_size font_size_normal
                                                text_outlines [(2, Color(trait.color).replace_opacity(0.6).hexcode, 0, 0)]
                                                action NullAction()
                                                tooltip trait.get_description()
                                        # Added Cherry Window (reusable component)
                                    # null height 10
                                    # use cherry_minimum_window(girl=selected_girl, position="bottom", border_color="#FF0000", border_size=3)
                        frame:
                            background menu_background_light
                            ypadding 5
                            xpadding 5
                            yfill True
                            xfill True

                            vbox:
                                text "Additional Info" size font_size_large color menu_text_color font header_font
                                xalign 0.05

                                $ area_sensitivity_string = ""
                                python:
                                    sensitivity_strings = []
                                    for area_name, (sensitivity, sensitivity_discovered) in selected_girl.area_sensitivity.items():
                                        sensitivity = selected_girl.get_area_sensitivity(area_name)

                                        if sensitivity_discovered:
                                            sensitivity_strings.append(f"{area_name.capitalize()}: x{sensitivity}")
                                        else:
                                            sensitivity_strings.append(f"{area_name.capitalize()}: Undiscovered")

                                    area_sensitivity_string = "\n".join(sensitivity_strings)

                                textbutton "Area Sensitivity":
                                    xpadding 0
                                    ypadding 0
                                    text_size font_size_small 
                                    text_color menu_text_color_hover
                                    text_hover_color menu_text_color 
                                    action NullAction()
                                    tooltip area_sensitivity_string

                                text f"{{color={menu_text_color_hover}}}Cash:{{/color}} ${selected_girl.cash} (+${selected_girl.get_wealth()}/week)" size font_size_small color menu_text_color 

                                $ seen_clothing_value = selected_girl.clothing_manager.get_seen_clothing_value()
                                text f"{{color={menu_text_color_hover}}}Seen Clothing Value:{{/color}} ${seen_clothing_value}" size font_size_small color menu_text_color 

                                $ estimated_wardrobe_value = selected_girl.clothing_manager.get_estimated_wardrobe_value()
                                text f"{{color={menu_text_color_hover}}}Estimated Wardrobe Value:{{/color}} ${estimated_wardrobe_value}" size font_size_small color menu_text_color 

                            vbox:
                                xalign 1.0

                                if review_mother:
                                    text "Daughter" size font_size_small color menu_text_color_hover xalign 0.5

                                    fixed:
                                        ysize 110
                                        xsize 110
                                        xalign 0.5

                                        $ daughter_face_image = apply_brightness(fit_image_to_size(selected_girl.daughter.image_manager.get_first_portrait_image(), 110, 110), 0)
                                        imagebutton:
                                            idle daughter_face_image
                                            hover apply_brightness(daughter_face_image)
                                            action [
                                                SetVariable("review_mother", False),
                                                SetVariable("selected_girl", selected_girl.daughter),
                                                Function(change_available_girls),
                                                Jump("save_girl_review_menu")
                                            ]
                                            tooltip selected_girl.daughter

                                        if selected_girl.left_academy:
                                            imagebutton:
                                                idle fit_image_to_size("gui/widgets/left.webp", 110, 110)
                                        elif selected_girl.alumni:
                                            imagebutton:
                                                idle fit_image_to_size("gui/widgets/alumni.webp", 35, 35) xalign 0.98 yalign 0.02
                                                action NullAction()
                                                tooltip "Alumni"
                                        elif selected_girl.expelled:
                                            imagebutton:
                                                idle fit_image_to_size("gui/widgets/expelled.webp", 110, 110)

                                    text "[selected_girl.daughter.full_name]":
                                        yalign 0.5
                                        xalign 0.5
                                        size font_size_small 
                                        font header_font
                                        outlines [(2, Color(selected_girl.daughter.color).replace_opacity(0.6).hexcode, 0, 0)]
                                else:
                                    text "Mother" size font_size_small color menu_text_color_hover xalign 0.5

                                    fixed:
                                        ysize 110
                                        xsize 110
                                        xalign 0.5

                                        $ mother_face_image = apply_brightness(fit_image_to_size(selected_girl.mother.image_manager.get_first_portrait_image(), 110, 110), 0)
                                        imagebutton:
                                            idle mother_face_image
                                            hover apply_brightness(mother_face_image)
                                            action [
                                                SetVariable("review_mother", True),
                                                SetVariable("selected_girl", selected_girl.mother),
                                                Function(change_available_girls),
                                                Jump("save_girl_review_menu")
                                            ]
                                            tooltip selected_girl.mother

                                        if academy.pta_president and selected_girl.mother == academy.pta_president and not selected_girl.left_academy:
                                            $ small_crown = fit_image_to_size("gui/widgets/crown.webp", 35, 35)
                                            imagebutton:
                                                xalign 0.98
                                                yalign 0.02
                                                idle small_crown
                                                hover apply_brightness(small_crown, 0.6)
                                                action NullAction()
                                                tooltip "PTA President"
                                    
                                    text "[selected_girl.mother.full_name]":
                                        yalign 0.5
                                        xalign 0.5
                                        size font_size_small 
                                        font header_font
                                        outlines [(2, Color(selected_girl.mother.color).replace_opacity(0.6).hexcode, 0, 0)]

                    # New(Unused) - Temporary Wardrobe
                    frame:
                        background menu_background_light
                        xsize 501
                        ysize 478

                        text "{b}Wardrobe{/b}" size font_size_large color menu_text_color font header_font xalign 0.5
                        $ seen_clothing_count = len(selected_girl.clothing_manager.get_all_seen_clothing())
                        if seen_clothing_count < 1:
                            text "{b}No clothing seen yet{/b}" size font_size_normal color menu_text_color_conflict xalign 0.5 yalign 0.5
                        else:
                            viewport id "girl_review_wardrobe_vpgrid":
                                yadjustment initialize_adjustment("girl_review_wardrobe_vpgrid")

                                xfill True
                                ysize 430
                                yalign 1.0
                                draggable True
                                mousewheel True
                                scrollbars "vertical"
                                vscrollbar_unscrollable "hide"

                                vbox:
                                    xsize 410
                                    spacing 10

                                    for clothing_type in selected_girl.clothing_manager.wardrobe:
                                        if clothing_type == "nipple_acc":
                                            $ clothing_type_string = "Nipple Accessories"
                                        elif clothing_type == "pussy_acc":
                                            $ clothing_type_string = "Pussy Accessories"
                                        else:
                                            $ clothing_type_string = clothing_type.capitalize()

                                        text "{b}[clothing_type_string]{/b}" size font_size_normal color menu_text_color

                                        $ seen_clothing = selected_girl.clothing_manager.get_seen_clothing(clothing_type)
                                        if not seen_clothing:
                                            text "Haven't seen any clothing of this type" size font_size_small color menu_text_color_conflict xalign 0.5 xoffset 30
                                        else:
                                            vpgrid:
                                                xsize 410
                                                yminimum 64
                                                cols 6
                                                spacing 5
                                                for clothing_item in seen_clothing:
                                                    $ clothing_image = clothing_item.get_clothing_image_for_part("clothing")

                                                    imagebutton:
                                                        idle fit_image_to_size(clothing_image, 64, 64)
                                                        action NullAction()
                                                        tooltip clothing_item
            else:
                text "No Girl Selected" size font_size_large_header color menu_text_color_conflict xalign 0.5 yalign 0.5

        if show_tutorial:
            imagebutton:
                xalign 0.5
                yalign 0.5
                idle "images/other/tutorial/girl_review_tutorial.webp"
                hover "images/other/tutorial/girl_review_tutorial.webp"
                action SetVariable("show_tutorial", False)


    screen vtmod_virgin_preg_ui(girl=None):
        tag vtmod_ui  # CRITICAL FOR MANAGEMENT
        zorder 99
        modal False
        sensitive True 
        add "black" alpha 0.001 xalign 0.0 yalign 0.0 xsize 1.0 ysize 1.0
        
        if girl is not None and hasattr(girl, "birth_control"):
            frame:
                background Frame("/_mods/content/elkrose_vt/extra_images/Cherry_Background.png", 
                                left_size=10, right_size=10, 
                                top_size=10, bottom_size=10)
                xsize 400
                #ysize 400  # Set explicit height for proper scaling
                xalign 0.5
                yalign 0.5
                xpadding 10
                ypadding 10
                #xfill True
                #yfill True
            
                vbox:
                    #xsize 380
                    #xalign 0.0
                    #yalign 0.0
                    spacing 10

                    #Header
                    hbox:
                        #xsize 400
                        #xalign 0.0
                        # Name
                        vbox:
                            xsize 400
                            xalign 0.5
                            spacing 10
                            text f"[girl.full_name]" text_align 0.5 size 30 color "#ffffff" bold True
                        imagebutton:
                            pos(-70,0)
                            idle "_mods/content/elkrose_vt/extra_images/HUDVT_idle.png"
                            hover "_mods/content/elkrose_vt/extra_images/HUDVT_hover.png"
                            action toggle_virgin_preg_ui(girl=girl)
                            #action ToggleScreen("VPMOD_virgin_preg_ui")
                            tooltip f"{{color=#ff0000}}Close Cherry Info.{{/color}}"
                    # CHANGE: Wrapped the conditional content in a vbox for better layout control
                    vbox:
                        if girl.pregnant and girl.player_knows_pregnant:
                            text "Pregnancy Status:" size 20
                            hbox:
                                xalign 0.5
                                spacing 10
                                vbox:
                                    # FIX: Changed self to girl
                                    $ vt_img_pp = "_mods/content/elkrose_vt/extra_images/pretrimester.webp"
                                    $ vt_text_pp = "She just starting her pregnancy"
                                    if girl.pregnancy_phase == 1 and girl.preg_progress_days < 35:
                                        $ vt_img_pp = "_mods/content/elkrose_vt/extra_images/pretrimester.webp"
                                        $ vt_text_pp = "First Trimester: She just slowly starting to show."
                                    elif girl.pregnancy_phase == 1 and girl.preg_progress_days >= 35:
                                        $ vt_img_pp = "_mods/content/elkrose_vt/extra_images/first_trimester.webp"
                                        $ vt_text_pp = "First Trimester: She is starting to show."
                                    elif girl.pregnancy_phase == 2:
                                        $ vt_img_pp = "_mods/content/elkrose_vt/extra_images/second_trimester.webp"
                                        $ vt_text_pp = "Second Trimester: Nice cute baby bump."
                                    elif girl.pregnancy_phase == 3 and girl.preg_progress_days > 10:
                                        $ vt_img_pp = "_mods/content/elkrose_vt/extra_images/third_trimester.webp"
                                        $ vt_text_pp = "Third Trimester: It is a baby, right?"
                                    
                                    xalign 0.5
                                    imagebutton:
                                        idle vt_img_pp
                                        action NullAction()
                                        #tooltip vt_tt_ps
                                #vbox:
                            text vt_text_pp size 20
                                
                            # ADD: Pregnancy Progression Section
                            null height 10
                            text "Pregnancy Progression:" size 20
                            # A standard pregnancy is ~260 days
                            $ preg_progress_pct = (girl.preg_progress_days / 260.0) * 100.0

                            # Progress bar (shows actual progress)
                            bar:
                                value preg_progress_pct
                                range 100
                                left_bar "_mods/content/elkrose_vt/extra_images/bar/follicular_bar.webp"  # Your progress image
                                right_bar "_mods/content/elkrose_vt/extra_images/bar/fertile_bar.webp"
                                thumb "_mods/content/elkrose_vt/extra_images/bar/bar_thumb15w.png"
                                xysize (380, 15)
                                # at Transform(anchor=(0.0, 0.0), pos=(0, 0))
                                # at truecenter  # This centers it over the background
                            text f"Day [girl.preg_progress_days] of 260" size 14 xalign 0.5
                                
                                
                        else:
                            text "Ovulation Info:" size 20
                            # The bar will now sit neatly under this header
                            vbox:
                                xalign 0.5
                                use pmsCycleBar(char=girl)

                        # --- ONLY SHOW after hymen breaks ---
                        
                        
                        #if not girl.hymen and not girl.player_knows_pregnant:
                        if not girl.player_knows_pregnant:
                            null height 10 # Spacer

                            # Birth Control Status
                            text "Birth Control Status:" size 20
                            hbox:
                                spacing 10
                                vbox:
                                    xsize 50
                                    # ... (Your birth control logic is fine, just removed the extra hbox wrappers)
                                    $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bcknown.png"
                                    $ vt_tt_bc = "Don't know her Birth Control Status."
                                    $ vt_text_bc = "Don't know her Birth Control Status."
                                    if girl.bc_status_known:
                                        if girl.birth_control:
                                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_token.png"
                                            $ vt_tt_bc = f"{{color={menu_text_color_valid}}}Birth Control Active{{/color}}"
                                            $ vt_text_bc = f"{{color={menu_text_color_valid}}}Birth Control Active{{/color}}"
                                            if girl.vaginal_cum >= 1:
                                                $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_cum.png"
                                                $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                                $ vt_text_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                        else:
                                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_token.png"
                                            $ vt_tt_bc = "Unprotected"
                                            $ vt_text_bc = f"{{color=#ff0000}}Unprotected{{/color}}"
                                            if girl.vaginal_cum >= 1:
                                                $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_cum.png"
                                                $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                                $ vt_text_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                            if girl.is_highly_fertile() :
                                                $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_fertile_cum.png"
                                                $ vt_tt_bc += f"\n{{color=#ff0000}}She is ovulating and has a higher chance of getting pregnant.{{/color}}"

                                        # --- FIX: Get the dynamic values at the very end ---
                                        $ day_status = girl.get_fertility_day_status()
                                        $ cycle_day = girl.get_cycle_day()
                                        $ current_fertility = girl.effective_fertility() # Call it here

                                        # --- FIX: Use the freshly fetched variable ---
                                        $ vt_tt_bc += f"\nFertility: {current_fertility:.1f}%\n{day_status}"
                                        $ vt_text_bc = f"\nBirth Control: {str(girl.birth_control)}\nCycle Day: {cycle_day}/30\nFertility: {current_fertility:.1f}%\n{day_status}"
                                    imagebutton:
                                        idle vt_img_bc
                                        action NullAction()
                                        tooltip vt_tt_bc
                                vbox:
                                    text vt_text_bc size 20

                            null height 10 # Spacer

                            # Vaginal Status
                            text "Vaginal Status:" size 20
                            hbox:
                                spacing 10
                                vbox:
                                    xsize 50
                                    # ... (Your vaginal logic is also fine)
                                    $ vt_img_vag = "_mods/content/elkrose_vt/extra_images/vagnone.png"
                                    $ vt_tt_vag = f"{{color={menu_text_color_valid}}} Fresh and untouched, ready for action! {{/color}}"
                                    $ vt_text_vag = "A pristine canvas, untouched and pure."
                                    if girl.hymen:
                                        $ vt_tt_vag = f"{{color={menu_text_color_valid}}} A pristine canvas, untouched and pure! {{/color}}"
                                        $ vt_img_vag = "_mods/content/elkrose_vt/extra_images/virginsymbol.png"
                                        $ vt_text_vag = "A pristine canvas, untouched and pure."
                                    else:
                                        if girl.vaginal_cum>=4:
                                            $ vt_tt_vag = f"{{color={menu_text_color_valid}}} A raging torrent, dripping with raw intensity. {{/color}}"
                                            $ vt_text_vag = "A raging torrent, dripping with raw intensity."
                                            $ vt_img_vag = "_mods/content/elkrose_vt/extra_images/vagmorecum.png"
                                        elif girl.vaginal_cum>=3:
                                            $ vt_tt_vag = f"{{color={menu_text_color_valid}}} Triple the thrill, a taste of indulgence. {{/color}}"
                                            $ vt_text_vag = "Triple the thrill, a taste of indulgence.."
                                            $ vt_img_vag = "_mods/content/elkrose_vt/extra_images/vagthreecum.png"
                                        elif girl.vaginal_cum>=2:
                                            $ vt_tt_vag = f"{{color={menu_text_color_valid}}} Double the delight, a tease of excess. {{/color}}"
                                            $ vt_text_vag = "Double the delight, a tease of excess."
                                            $ vt_img_vag = "_mods/content/elkrose_vt/extra_images/vagtwocum.png"
                                        elif girl.vaginal_cum>=1:
                                            $ vt_tt_vag = f"{{color={menu_text_color_valid}}} A tantalizing whisper, a hint of forbidden pleasure. {{/color}}"
                                            $ vt_text_vag = "A tantalizing whisper, a hint of forbidden pleasure."
                                            $ vt_img_vag = "_mods/content/elkrose_vt/extra_images/vagonecum.png"
                                        else:
                                            $ vt_tt_vag = f"{{color={menu_text_color_valid}}} A spotless canvas, untouched by passion.! {{/color}}"
                                            $ vt_text_vag = "A spotless canvas, untouched by passion!"
                                            $ vt_img_vag = "_mods/content/elkrose_vt/extra_images/none.png"
                                        $ vt_tt_vag +=f"\n Cum:{girl.vaginal_cum}"
                                    imagebutton:
                                        idle vt_img_vag
                                        action NullAction()
                                        tooltip vt_tt_vag
                                vbox:
                                    text vt_text_vag size 20

                        null height 10 # Spacer

                        # Items Active
                        text "Items Active:" size 20
                        hbox:
                            spacing 20
                            $ thereareitems = False
                            #FertiBOOST
                            if girl.fertility_boost >= 1:
                                $ days_rem_text = "days"
                                $ thereareitems = True
                                if girl.fertility_boost == 1:
                                    $days_rem_text = "day"
                                imagebutton:
                                    idle "_mods/content/elkrose_vt/extra_images/fertilitypills50.png"
                                    action NullAction()
                                    tooltip f"{{color={menu_text_color_valid}}} FertiBOOST Active!, good for {girl.fertility_boost} more {days_rem_text}! {{/color}}"
                            #PregnaVITA
                            if girl.prenatal_boost >= 1:
                                $ thereareitems = True
                                imagebutton:
                                    idle "_mods/content/elkrose_vt/extra_images/pregboosters50.png"
                                    action NullAction()
                                    tooltip f"{{color={menu_text_color_valid}}} PregnaVITA Active! {{/color}}"
                            if not thereareitems:
                                text "nothing" size 20
                        
        else:
            # Instead of recursive call, just hide the screen
            $ renpy.hide_screen("vtmod_virgin_preg_ui")
            $ persistent.vt_virgin_preg_ui_visible = False

init 1 python:
    
    # def toggle_virgin_preg_ui(girl = None):
        # # CORRECT: get_screen() doesn't take _layer parameter
        # if renpy.get_screen("vtmod_virgin_preg_ui"):
            # renpy.hide_screen("vtmod_virgin_preg_ui")
        # else:
            # renpy.show_screen("vtmod_virgin_preg_ui",girl=girl, _layer="master")

    persistent.vt_virgin_preg_ui_visible = False
    
    def toggle_virgin_preg_ui(girl=None):
        """Safely toggle the virgin/pregnancy UI screen for Ren'Py 8.3.x"""
        # Safety check - don't proceed if girl is invalid
        if girl is None or not hasattr(girl, "birth_control"):
            # Try to get the currently selected girl if none provided
            global selected_girl
            if selected_girl and hasattr(selected_girl, "birth_control"):
                girl = selected_girl
            else:
                return
        
        try:
            # Check actual screen state with layer specification
            screen_visible = renpy.get_screen("vtmod_virgin_preg_ui") is not None
            
            # Always hide first to ensure clean state
            if screen_visible:
                renpy.hide_screen("vtmod_virgin_preg_ui", layer="master")
                persistent.vt_virgin_preg_ui_visible = False
            else:
                # In Ren'Py 8.3.x, to replace a screen we must hide it first
                # then show with the same tag
                renpy.show_screen("vtmod_virgin_preg_ui", 
                                 girl=girl, 
                                 layer="master", 
                                 tag="vtmod_virgin_preg_ui")
                persistent.vt_virgin_preg_ui_visible = True
                
        except Exception as e:
            renpy.log(f"VT MOD ERROR in toggle_virgin_preg_ui: {str(e)}")
            # Reset state on error
            persistent.vt_virgin_preg_ui_visible = False
            # Try to hide the screen
            try:
                renpy.hide_screen("vtmod_virgin_preg_ui")
            except:
                pass