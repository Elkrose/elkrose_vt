## Overide the default screen girl_hud

init 1:

    screen exam_actions_menu():
        $ resized_video_widget = "gui/widgets/video_button.webp"  # fit_image_to_size("gui/widgets/video_button.webp", 35)
        $ video_widget_green = apply_tint(resized_video_widget, "#00FF00")
        $ video_widget_red = apply_tint(resized_video_widget, "#FF0000")

        $ cum_button = clothing_overview_buttons.get("cum", clothing_overview_buttons["unknown"])
        $ ripped_button = clothing_overview_buttons.get("ripped", clothing_overview_buttons["unknown"])

        frame:
            background menu_background_dark
            xsize 1920
            ysize 1080
            xpadding 5
            ypadding 5

            vbox:
                xalign 0.01
                yalign 0.01
                text "Reputation: [player.reputation]" size font_size_small color menu_text_color

                $ player_cash = get_money_shorthand(player.cash)
                text "Player Cash: $[player_cash]" size font_size_small color menu_text_color

                $ academy_funds = get_money_shorthand(academy.available_funds)
                text "Academy Funds: $[academy_funds]" size font_size_small color menu_text_color

            hbox:
                xalign 0.5
                yalign 0.01
                spacing 10
                text "{b}Conducting Exam{/b}" size font_size_large_header color menu_text_color font header_font

                imagebutton:
                    yalign 0.5
                    idle apply_brightness("gui/widgets/inventory.webp")
                    hover apply_brightness("gui/widgets/inventory.webp", 0.4)
                    action Show("player_inventory_menu", show_hud=False)
                    tooltip "View inventory\n{b}Hotkey{/b}: I"
                    keysym "K_i"
                
                # Added Cherry Window (reusable component)
                null height 10
                use condom_cherry(position="center")

            if len(available_girls) > 1:
                $ resized_prev_widget = fit_image_to_size("gui/widgets/prev.webp", 60, 60)
                imagebutton:
                    xalign 0.3
                    yalign 0.01
                    idle resized_prev_widget
                    hover apply_brightness(resized_prev_widget)
                    action [
                        CycleVariable("selected_girl", available_girls, reverse=True),
                        Jump("save_exam_actions_menu")
                    ]
                    keysym ["any_K_LEFT", "any_KP_LEFT"]
                    tooltip "{b}Hotkey{/b}: Left Arrow"

                $ resized_next_widget = fit_image_to_size("gui/widgets/next.webp", 60, 60)
                imagebutton:
                    xalign 0.7
                    yalign 0.01
                    idle resized_next_widget
                    hover apply_brightness(resized_next_widget)
                    action [
                        CycleVariable("selected_girl", available_girls),
                        Jump("save_exam_actions_menu")
                    ]
                    keysym ["any_K_RIGHT", "any_KP_RIGHT"]
                    tooltip "{b}Hotkey{/b}: Right Arrow"

            hbox:
                xalign 0.96
                yalign 0.005
                spacing 5

                imagebutton:
                    idle apply_brightness("gui/widgets/info.webp")
                    hover apply_brightness("gui/widgets/info.webp", 0.4)
                    action SetVariable("show_tutorial", True)
                    tooltip "View Tutorial"

            imagebutton:
                xalign 1.0
                yalign 0
                xoffset 5
                yoffset -5

                idle "gui/widgets/close.webp"
                hover apply_brightness("gui/widgets/close.webp", 0.5)
                action [
                    Hide("exam_actions_menu", _layer="master"),
                    SetVariable("selected_girl", None),
                    Function(exam_actions_clear),
                    Hide("change_exam_force_level_menu"),
                    Hide("change_vibration_level_menu"),
                    Jump("show_exam_menu")
                ]
                if persistent.right_click_close:
                    keysym "mouseup_3"
                    tooltip "{b}Hotkey{/b}: Right-Click"

        hbox:
            xsize 1900
            ysize 980
            xalign 0.5
            yalign 0.9
            spacing 5

            frame:
                background menu_background_light
                xalign 0.5
                yalign 0.9
                xsize 505
                ysize 980

                $ estimated_tolerance_increase = action_stat_changes.get(selected_girl.id, {}).get("tolerance", 0)
                $ estimated_arousal_increase = action_stat_changes.get(selected_girl.id, {}).get("arousal", 0)
                $ estimated_pressure_increase = action_stat_changes.get(selected_girl.id, {}).get("pressure", 0)
                $ estimated_motivation_increase = action_stat_changes.get(selected_girl.id, {}).get("motivation", 0)
                $ estimated_grade_increase = action_stat_changes.get(selected_girl.id, {}).get("grades", 0)

                $ [button_face, button_boobs, button_pussy, button_ass, button_legs] = selected_girl.image_manager.get_outfit_images()
                $ button_face = fit_image_to_size(button_face, small_button_size, small_button_size)                     # Small
                $ button_boobs = fit_image_to_size(button_boobs, wide_button_size_x, wide_button_size_y)                 # Wide
                $ button_ass = fit_image_to_size(button_ass, wide_button_size_x, wide_button_size_y)                     # Wide
                $ button_pussy = fit_image_to_size(button_pussy, side_by_side_button_size_x, side_by_side_button_size_y) # Side by Side
                $ button_legs = fit_image_to_size(button_legs, side_by_side_button_size_x, side_by_side_button_size_y)   # Side by Side

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 5

                    hbox:
                        xalign 0.5
                        spacing 5

                        fixed:
                            xsize small_button_size
                            ysize small_button_size

                            textbutton "[selected_girl.full_name]":
                                style "girl_exam_button_small"
                                if selected_part == "face":
                                    background apply_brightness(button_face, brightness=0.05)
                                    hover_background apply_brightness(button_face)
                                    action [
                                        Hide("exam_actions_menu", _layer="master"),
                                        SetVariable("selected_girl", None),
                                        Jump("show_exam_menu")
                                    ]
                                else:
                                    background button_face
                                    hover_background apply_brightness(button_face)
                                    action [
                                        SetVariable("selected_part", "face"),
                                        Jump("show_exam_actions_menu")
                                    ]

                            vbox:
                                yalign 0.02
                                xalign 0.02
                                spacing 2

                                $ face_cum_tooltip = selected_girl.get_body_part_cum_tooltip("face")
                                if face_cum_tooltip:
                                    imagebutton:
                                        yalign 0.5
                                        xalign 0.5
                                        idle cum_button
                                        hover apply_brightness(cum_button)
                                        action NullAction()
                                        tooltip f"{face_cum_tooltip}"

                        vbox:
                            xsize 255
                            ysize 240
                            xalign 0.5

                            $ tolerance_string = f"Tolerance: {selected_girl.tolerance}/{selected_girl.max_tolerance}"
                            $ stat_tooltip = get_stat_tooltip("tolerance")
                            $ stat_tooltip += f"\n\n{tolerance_string}"

                            textbutton "[tolerance_string]":
                                xpadding 0
                                ypadding 0
                                text_size font_size_normal 
                                text_color menu_text_color
                                action NullAction()
                                tooltip stat_tooltip

                            fixed:
                                ysize 14
                                xsize 250

                                bar:
                                    style "rg_bar"
                                    ysize 10
                                    yalign 0.5
                                    value selected_girl.tolerance
                                    range selected_girl.max_tolerance

                                if selected_girl.id in action_stat_changes and estimated_tolerance_increase:
                                    bar:
                                        style "bar_stat_change"
                                        ypos 0.1
                                        xsize 250
                                        ysize 14
                                        value selected_girl.tolerance + estimated_tolerance_increase
                                        range selected_girl.max_tolerance

                            $ vulnerable_text = ""
                            if selected_girl.is_vulnerable_to_extreme_actions():
                                $ vulnerable_text = f"{{color={arousal_colors[2]}}}Vulnerable{{/color}}"

                            $ rounded_pressure = int(selected_girl.pressure)
                            $ pressure_for_vulnerable = selected_girl.pressure_for_vulnerable()
                            $ pressure_separator_xalign = linear_conversion(pressure_for_vulnerable, 0, 100, 0.0, 1.0)
                            $ stat_tooltip = get_stat_tooltip("pressure")
                            $ stat_tooltip += f"\n\nPressure: {rounded_pressure}/100"
                            if rounded_pressure >= pressure_for_vulnerable:
                                $ stat_tooltip += f"\nPressure for Vulnerable: {{color={menu_text_color_valid}}}{rounded_pressure}/{pressure_for_vulnerable}{{/color}}"
                            else:
                                $ stat_tooltip += f"\nPressure for Vulnerable: {rounded_pressure}/{pressure_for_vulnerable}"

                            textbutton "Pressure: [vulnerable_text]":
                                xpadding 0
                                ypadding 0
                                text_size font_size_normal 
                                text_color menu_text_color
                                action NullAction()
                                tooltip stat_tooltip

                            fixed:
                                ysize 14
                                xsize 250
                                bar:
                                    style "gr_bar"
                                    ysize 10
                                    yalign 0.5
                                    value selected_girl.pressure
                                    range 100
                                
                                if rounded_pressure >= pressure_for_vulnerable:
                                    imagebutton:
                                        xalign pressure_separator_xalign 
                                        yalign 0.5
                                        ysize 14
                                        yoffset -1
                                        xpadding 0
                                        ypadding 0
                                        idle apply_tint("gui/widgets/separator_wide.webp", "#55FF64")
                                        action NullAction()
                                        tooltip f"{{color={menu_text_color_valid}}}Pressure target: {pressure_for_vulnerable} is met{{/color}}"
                                else:
                                    imagebutton:
                                        xalign pressure_separator_xalign 
                                        yalign 0.5
                                        ysize 14
                                        yoffset -1
                                        xpadding 0
                                        ypadding 0
                                        idle "gui/widgets/separator_wide.webp"
                                        action NullAction()
                                        tooltip f"Pressure target: {pressure_for_vulnerable} for vulnerable status"

                                if selected_girl.id in action_stat_changes and estimated_pressure_increase:
                                    bar:
                                        style "bar_stat_change"
                                        ypos 0.1
                                        xsize 250
                                        ysize 14
                                        value selected_girl.pressure + estimated_pressure_increase
                                        range 100

                            $ arousal_text = selected_girl.get_arousal_text()

                            $ rounded_arousal = int(selected_girl.arousal)
                            $ arousal_for_vulnerable = selected_girl.arousal_for_vulnerable()
                            $ arousal_separator_xalign = linear_conversion(arousal_for_vulnerable, 0, 100, 0.0, 1.0)
                            $ stat_tooltip = get_stat_tooltip("arousal")
                            $ stat_tooltip += f"\n\nArousal: {rounded_arousal}/100"
                            if rounded_arousal >= arousal_for_vulnerable:
                                $ stat_tooltip += f"\nArousal for Vulnerable: {{color={menu_text_color_valid}}}{rounded_arousal}/{arousal_for_vulnerable}{{/color}}"
                            else:
                                $ stat_tooltip += f"\nArousal for Vulnerable: {rounded_arousal}/{arousal_for_vulnerable}"

                            textbutton "Arousal: [arousal_text]":
                                xpadding 0
                                ypadding 0
                                text_size font_size_normal 
                                text_color menu_text_color
                                action NullAction()
                                tooltip stat_tooltip

                            fixed:
                                ysize 14
                                xsize 250
                                bar:
                                    style "girl_arousal_bar"
                                    ysize 10
                                    yalign 0.5
                                    value selected_girl.arousal
                                    range 100
                                
                                if rounded_arousal >= arousal_for_vulnerable:
                                    imagebutton:
                                        xalign arousal_separator_xalign 
                                        yalign 0.5
                                        ysize 14
                                        yoffset -1
                                        xpadding 0
                                        ypadding 0
                                        idle apply_tint("gui/widgets/separator_wide.webp", "#55FF64")
                                        action NullAction()
                                        tooltip f"{{color={menu_text_color_valid}}}Pressure target: {arousal_for_vulnerable} is met{{/color}}"
                                else:
                                    imagebutton:
                                        xalign arousal_separator_xalign 
                                        yalign 0.5
                                        ysize 14
                                        yoffset -1
                                        xpadding 0
                                        ypadding 0
                                        idle "gui/widgets/separator_wide.webp"
                                        action NullAction()
                                        tooltip f"Pressure target: {arousal_for_vulnerable} for vulnerable status"

                                if selected_girl.id in action_stat_changes and estimated_arousal_increase:
                                    bar:
                                        style "bar_stat_change"
                                        ypos 0.1
                                        xsize 250
                                        ysize 14
                                        value selected_girl.arousal + estimated_arousal_increase
                                        range 100

                            $ motivation_tooltip = get_stat_tooltip("motivation")
                            $ motivation_changes_tooltip = get_motivation_changes_tooltip()
                            $ motivation_tooltip += f"\n{motivation_changes_tooltip}"
                            $ motivation_string = selected_girl.get_motivation_string()

                            textbutton "Motivation: [motivation_string]":
                                xpadding 0
                                ypadding 0
                                text_size font_size_normal 
                                text_color menu_text_color
                                action NullAction()
                                tooltip motivation_tooltip

                            $ bar_size_and_color = selected_girl.get_motivation_splits()
                            fixed:
                                xsize 250
                                ysize 14
                                xalign 0.5
                                yalign 0.5
                                hbox:
                                    xsize 250
                                    xalign 0.5
                                    spacing 0
                                    for (bar_size, bar_color) in bar_size_and_color:
                                        bar:
                                            style f"bar_{bar_color}"
                                            xsize bar_size
                                            ysize 10
                                            value 100
                                            range 100

                                bar:
                                    style "bar_transparent"
                                    xsize 250
                                    ysize 14
                                    yalign 0.5
                                    value selected_girl.motivation
                                    range 100

                                if selected_girl.id in action_stat_changes and estimated_motivation_increase:
                                    $ estimated_motivation_level = selected_girl.motivation + estimated_motivation_increase
                                    bar:
                                        style "bar_stat_change"
                                        xsize 250
                                        ysize 14
                                        yalign 0.5
                                        value estimated_motivation_level
                                        range 100

                            if not is_night_class:
                                textbutton "Grades: [selected_girl.grades]/100":
                                    xpadding 0
                                    ypadding 0
                                    text_size font_size_normal 
                                    text_color menu_text_color
                                    action NullAction()
                                    tooltip f"Her mother expects her to reach at least a {selected_girl.mother.expected_grades} grade"

                                fixed:
                                    ysize 10
                                    xsize 250
                                    bar:
                                        style "gr_bar"
                                        ysize 10
                                        value selected_girl.grades
                                        range 100

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

                                            if selected_girl.id in action_stat_changes and estimated_grade_increase:
                                                $ estimated_grade_level = selected_girl.grades + estimated_grade_increase
                                                bar:
                                                    style "bar_stat_change"
                                                    xsize 250
                                                    ysize 14
                                                    yalign 0.5
                                                    value estimated_grade_level
                                                    range 100

                    fixed:
                        xsize wide_button_size_x
                        ysize wide_button_size_y
                        xalign 0.5
                        
                        textbutton "Upper":
                            style "girl_exam_button_wide"
                            if selected_part == "boobs":
                                background apply_brightness(button_boobs, brightness=0.05)
                                hover_background apply_brightness(button_boobs)
                                action [
                                    Hide("exam_actions_menu", _layer="master"),
                                    SetVariable("selected_girl", None),
                                    Function(exam_actions_clear),
                                    Jump("show_exam_menu")
                                ]
                            else:
                                background button_boobs
                                hover_background apply_brightness(button_boobs)
                                action [
                                    SetVariable("selected_part", "boobs"),
                                    Jump("show_exam_actions_menu")
                                ]

                        vbox:
                            yalign 0.02
                            xalign 0.02
                            spacing 2

                            $ boobs_cum_tooltip = selected_girl.get_body_part_cum_tooltip("boobs")
                            if boobs_cum_tooltip:
                                imagebutton:
                                    yalign 0.5
                                    xalign 0.5
                                    idle cum_button
                                    hover apply_brightness(cum_button)
                                    action NullAction()
                                    tooltip f"{boobs_cum_tooltip}"

                        vbox:
                            yalign 0.02
                            xalign 0.98
                            spacing 2

                            for clothing_type in ("outer", "upper", "bra", "nipple_acc"):
                                $ worn_item = selected_girl.get_clothing_on_part(clothing_type)
                                if worn_item:
                                    $ part_covered = selected_girl.part_covered_by_clothing(clothing_type, ignore_transparent=False)
                                    $ vib_with_remote = worn_item.has_tag("vibrator") and selected_girl.id in vibrator_remotes
                                    if not part_covered or vib_with_remote:
                                        $ item_button = clothing_overview_buttons.get(clothing_type, clothing_overview_buttons["unknown"])

                                        imagebutton:
                                            yalign 0.5
                                            xalign 0.5
                                            idle item_button
                                            hover apply_brightness(item_button)
                                            if vib_with_remote:
                                                action [
                                                    SetVariable("mouse_coords", renpy.get_mouse_pos()),
                                                    ToggleScreen("change_vibration_level_menu", clothing_item=worn_item)
                                                ]
                                            else:
                                                action NullAction()
                                            tooltip worn_item

                    fixed:
                        xsize wide_button_size_x
                        ysize wide_button_size_y
                        xalign 0.5

                        textbutton "Lower:\nback":
                            style "girl_exam_button_wide"
                            if selected_part == "ass":
                                background apply_brightness(button_ass, brightness=0.05)
                                hover_background apply_brightness(button_ass)
                                action [
                                    Hide("exam_actions_menu", _layer="master"),
                                    SetVariable("selected_girl", None),
                                    Function(exam_actions_clear),
                                    Jump("show_exam_menu")
                                ]
                            else:
                                background button_ass
                                hover_background apply_brightness(button_ass)
                                action [
                                    SetVariable("selected_part", "ass"),
                                    Jump("show_exam_actions_menu")
                                ]
                    
                        vbox:
                            yalign 0.02
                            xalign 0.02
                            spacing 2

                            $ ass_cum_tooltip = selected_girl.get_body_part_cum_tooltip("ass")
                            if ass_cum_tooltip:
                                imagebutton:
                                    yalign 0.5
                                    xalign 0.5
                                    idle cum_button
                                    hover apply_brightness(cum_button)
                                    action NullAction()
                                    tooltip f"{ass_cum_tooltip}"

                        vbox:
                            yalign 0.02
                            xalign 0.98
                            spacing 2

                            for clothing_type in ("lower", "panties", "buttplug"):
                                $ worn_item = selected_girl.get_clothing_on_part(clothing_type)
                                if worn_item:
                                    $ part_covered = selected_girl.part_covered_by_clothing(clothing_type, ignore_transparent=False)
                                    $ vib_with_remote = worn_item.has_tag("vibrator") and selected_girl.id in vibrator_remotes
                                    if not part_covered or vib_with_remote:
                                        $ item_button = clothing_overview_buttons.get(clothing_type, clothing_overview_buttons["unknown"])

                                        imagebutton:
                                            yalign 0.5
                                            xalign 0.5
                                            idle item_button
                                            hover apply_brightness(item_button)
                                            if vib_with_remote:
                                                action [
                                                    SetVariable("mouse_coords", renpy.get_mouse_pos()),
                                                    ToggleScreen("change_vibration_level_menu", clothing_item=worn_item)
                                                ]
                                            else:
                                                action NullAction()
                                            tooltip worn_item

                    hbox:
                        xsize 500
                        ysize 240
                        spacing 5

                        fixed:
                            xsize side_by_side_button_size_x
                            ysize side_by_side_button_size_x
                            textbutton "Lower:\nfront":
                                style "girl_exam_button_side_by_side"
                                if selected_part == "pussy":
                                    background apply_brightness(button_pussy, brightness=0.05)
                                    hover_background apply_brightness(button_pussy)
                                    action [
                                        Hide("exam_actions_menu", _layer="master"),
                                        SetVariable("selected_girl", None),
                                        Function(exam_actions_clear),
                                        Jump("show_exam_menu")
                                    ]
                                else:
                                    background button_pussy
                                    hover_background apply_brightness(button_pussy)
                                    action [
                                        SetVariable("selected_part", "pussy"),
                                        Jump("show_exam_actions_menu")
                                    ]

                            vbox:
                                yalign 0.02
                                xalign 0.02
                                spacing 2

                                $ pussy_cum_tooltip = selected_girl.get_body_part_cum_tooltip("pussy")
                                if pussy_cum_tooltip:
                                    imagebutton:
                                        yalign 0.5
                                        xalign 0.5
                                        idle cum_button
                                        hover apply_brightness(cum_button)
                                        action NullAction()
                                        tooltip f"{pussy_cum_tooltip}"

                            vbox:
                                yalign 0.02
                                xalign 0.98
                                spacing 2

                                for clothing_type in ("lower", "panties", "pussy_acc"):
                                    $ worn_item = selected_girl.get_clothing_on_part(clothing_type)
                                    if worn_item:
                                        $ part_covered = selected_girl.part_covered_by_clothing(clothing_type, ignore_transparent=False)
                                        $ vib_with_remote = worn_item.has_tag("vibrator") and selected_girl.id in vibrator_remotes
                                        if not part_covered or vib_with_remote:
                                            $ item_button = clothing_overview_buttons.get(clothing_type, clothing_overview_buttons["unknown"])

                                            imagebutton:
                                                yalign 0.5
                                                xalign 0.5
                                                idle item_button
                                                hover apply_brightness(item_button)
                                                if vib_with_remote:
                                                    action [
                                                        SetVariable("mouse_coords", renpy.get_mouse_pos()),
                                                        ToggleScreen("change_vibration_level_menu", clothing_item=worn_item)
                                                    ]
                                                else:
                                                    action NullAction()
                                                tooltip worn_item

                        fixed:
                            xsize side_by_side_button_size_x
                            ysize side_by_side_button_size_x
                            textbutton "Legs":
                                style "girl_exam_button_side_by_side"
                                if selected_part == "legs":
                                    background apply_brightness(button_legs, brightness=0.05)
                                    hover_background apply_brightness(button_legs)
                                    action [
                                        Hide("exam_actions_menu", _layer="master"),
                                        SetVariable("selected_girl", None),
                                        Function(exam_actions_clear),
                                        Jump("show_exam_menu")
                                    ]
                                else:
                                    background button_legs
                                    hover_background apply_brightness(button_legs)
                                    action [
                                        SetVariable("selected_part", "legs"),
                                        Jump("show_exam_actions_menu")
                                    ]

                            vbox:
                                yalign 0.02
                                xalign 0.02
                                spacing 2

                                $ legs_cum_tooltip = selected_girl.get_body_part_cum_tooltip("legs")
                                if legs_cum_tooltip:
                                    imagebutton:
                                        yalign 0.5
                                        xalign 0.5
                                        idle cum_button
                                        hover apply_brightness(cum_button)
                                        action NullAction()
                                        tooltip f"{legs_cum_tooltip}"

                            vbox:
                                yalign 0.02
                                xalign 0.98
                                spacing 2

                                for clothing_type in ("shoes", "socks"):
                                    $ worn_item = selected_girl.get_clothing_on_part(clothing_type)
                                    if worn_item:
                                        if clothing_type == "socks":
                                            $ part_covered = "legs" in selected_girl.get_clothing_on_part("shoes").covered_parts
                                        else:
                                            $ part_covered = selected_girl.part_covered_by_clothing(clothing_type, ignore_transparent=False)

                                        $ vib_with_remote = worn_item.has_tag("vibrator") and selected_girl.id in vibrator_remotes
                                        if not part_covered or vib_with_remote:
                                            $ item_button = clothing_overview_buttons.get(clothing_type, clothing_overview_buttons["unknown"])

                                            imagebutton:
                                                yalign 0.5
                                                xalign 0.5
                                                idle item_button
                                                hover apply_brightness(item_button)
                                                if vib_with_remote:
                                                    action [
                                                        SetVariable("mouse_coords", renpy.get_mouse_pos()),
                                                        ToggleScreen("change_vibration_level_menu", clothing_item=worn_item)
                                                    ]
                                                else:
                                                    action NullAction()
                                                tooltip worn_item

                        
            frame:
                background menu_background_light
                yalign 0.9
                xsize 1015
                ysize 980

                textbutton "Back":
                    xalign 1.0
                    action [
                        Hide("exam_actions_menu", _layer="master"),
                        SetVariable("selected_girl", None),
                        Function(exam_actions_clear),
                        Jump("show_exam_menu")
                    ]

                # Added Cherry Window (reusable component)
                #null height 10
                #use cherry_window(girl=selected_girl, position="bottom", border_color="#FF0000", border_size=3)

                hbox:
                    xalign 0.01
                    yalign 0.01
                    spacing 5


                    $ resized_selection_widget = fit_image_to_size("gui/widgets/remember.webp", 40, 40)
                    if exam_remember_selection:
                        $ resized_selection_widget = apply_tint(resized_selection_widget, menu_enabled_icon_color)
                    else:
                        $ resized_selection_widget = apply_tint(resized_selection_widget, menu_disabled_icon_color)

                    imagebutton:
                        yalign 0.5
                        idle resized_selection_widget
                        hover apply_brightness(resized_selection_widget, 0.5)
                        action [
                            Function(change_exam_remember_selection),
                            Jump("save_exam_actions_menu")
                        ]
                        tooltip "Remember girl selection after action\nDefault: False"

                    null width 3
                    add "gui/widgets/separator.webp" ysize 25 yalign 0.5
                    null width 3

                    $ resized_info_widget = fit_image_to_size("gui/widgets/info.webp", 40, 40)
                    if show_exam_action_tooltips:
                        $ resized_info_widget = apply_tint(resized_info_widget, menu_enabled_icon_color)
                    else:
                        $ resized_info_widget = apply_tint(resized_info_widget, menu_disabled_icon_color)

                    imagebutton:
                        idle resized_info_widget
                        hover apply_brightness(resized_info_widget, 0.5)
                        action [
                            Function(change_exam_action_tooltip_visibility),
                            Jump("save_exam_actions_menu")
                        ]
                        tooltip "Show Action Tooltips\nDefault: True"

                    null width 3
                    add "gui/widgets/separator.webp" ysize 25 yalign 0.5
                    null width 3

                    $ resized_skip_desc_widget = fit_image_to_size("gui/widgets/skip_desc.webp", 40, 40)
                    if exam_skip_descriptions:
                        $ resized_skip_desc_widget = apply_tint(resized_skip_desc_widget, menu_enabled_icon_color)
                    else:
                        $ resized_skip_desc_widget = apply_tint(resized_skip_desc_widget, menu_disabled_icon_color)

                    imagebutton:
                        idle resized_skip_desc_widget
                        hover apply_brightness(resized_skip_desc_widget, 0.5)
                        action [
                            Function(change_exam_action_description_skipping),
                            Jump("save_exam_actions_menu")
                        ]
                        tooltip "Skip Action Descriptions\nDefault: False"

                    $ resized_skip_resp_widget = fit_image_to_size("gui/widgets/skip_resp.webp", 40, 40)
                    if exam_skip_responses:
                        $ resized_skip_resp_widget = apply_tint(resized_skip_resp_widget, menu_enabled_icon_color)
                    else:
                        $ resized_skip_resp_widget = apply_tint(resized_skip_resp_widget, menu_disabled_icon_color)

                    imagebutton:
                        idle resized_skip_resp_widget
                        hover apply_brightness(resized_skip_resp_widget, 0.5)
                        action [
                            Function(change_exam_action_response_skipping),
                            Jump("save_exam_actions_menu")
                        ]
                        tooltip "Skip Action Responses\nDefault: False"

                    null width 3
                    add "gui/widgets/separator.webp" ysize 25 yalign 0.5
                    null width 3

                    # $ resized_show_damage_widget = fit_image_to_size("gui/widgets/show_damage.webp", 40, 40)
                    # if show_clothing_damage:
                    #     $ resized_show_damage_widget = apply_tint(resized_show_damage_widget, menu_enabled_icon_color)
                    # else:
                    #     $ resized_show_damage_widget = apply_tint(resized_show_damage_widget, menu_disabled_icon_color)

                    # imagebutton:
                    #     idle resized_show_damage_widget
                    #     hover apply_brightness(resized_show_damage_widget, 0.5)
                    #     action [
                    #         Function(change_show_clothing_damage),
                    #         Jump("save_exam_actions_menu")
                    #     ]
                    #     tooltip "Visually show clothing damage\nDefault: False"

                    # $ resized_first_layer_widget = fit_image_to_size("gui/widgets/first_layer.webp", 40, 40)
                    # if not show_clothing_damage:
                    #     pass
                    # elif only_show_first_damaged_layer:
                    #     $ resized_first_layer_widget = apply_tint(resized_first_layer_widget, menu_enabled_icon_color)
                    # else:
                    #     $ resized_first_layer_widget = apply_tint(resized_first_layer_widget, menu_disabled_icon_color)

                    # imagebutton:
                    #     idle resized_first_layer_widget
                    #     hover apply_brightness(resized_first_layer_widget, 0.5)
                    #     if not show_clothing_damage:
                    #         action NullAction()
                    #         tooltip "Requires clothing damage to be shown"
                    #     else:
                    #         action [
                    #             Function(change_only_show_first_damaged_layer),
                    #             Jump("save_exam_actions_menu")
                    #         ]
                    #         tooltip "Show only first layers damage\nDefault: False\n\nEnable to avoid excessive clutter"

                    $ resized_skip_strip_widget = fit_image_to_size("gui/widgets/skip_strip.webp", 40, 40)
                    if skip_exam_strip_videos:
                        $ resized_skip_strip_widget = apply_tint(resized_skip_strip_widget, menu_enabled_icon_color)
                    else:
                        $ resized_skip_strip_widget = apply_tint(resized_skip_strip_widget, menu_disabled_icon_color)

                    imagebutton:
                        idle resized_skip_strip_widget
                        hover apply_brightness(resized_skip_strip_widget, 0.5)
                        action [
                            Function(change_skip_exam_strip_videos),
                            Jump("save_exam_actions_menu")
                        ]
                        tooltip "Skip 'strip' {b}event{/b} videos and dialogue during exam.\nDefault: False"

                    null width 3
                    add "gui/widgets/separator.webp" ysize 25 yalign 0.5
                    null width 3

                    $ exam_force_tooltip = get_action_force_level_tooltip(player.action_force_level)

                    $ damage_chance = database_action_force_levels.get(player.action_force_level, {}).get("damage_chance", 0)
                    $ all_damage_chances = [database_action_force_levels[force_level].get("damage_chance", 0) for force_level in database_action_force_levels]
                    $ widget_color = get_color_based_on_value(damage_chance, value_range=(min(all_damage_chances), max(all_damage_chances)), inverted=True)
                    $ resized_exam_force_widget = fit_image_to_size(apply_tint("gui/widgets/exam_force.webp", widget_color), 40, 40)

                    imagebutton:
                        idle resized_exam_force_widget
                        hover apply_brightness(resized_exam_force_widget, 0.5)
                        action ToggleScreen("change_exam_force_level_menu")
                        tooltip exam_force_tooltip

                viewport:
                    xalign 0.5
                    yalign 1.0
                    xsize 1005
                    ysize 910
                    spacing 5
                    yfill True
                    draggable True
                    mousewheel True
                    scrollbars "vertical"

                    vbox:
                        spacing 5

                        for exam_action, has_custom_video, raw_success_chance, colorized_success_chance, raw_report_chance, colorized_report_chance, action_possible in tease_actions + clothing_actions:
                            $ action_text = exam_action.get_display_name()

                            button:
                                style "exam_action_button"
                                action [
                                    Hide("exam_actions_menu", _layer="master"), 
                                    Function(action_stat_changes.clear),
                                    Function(selected_girl.attempt_exam_action, exam_action), 
                                ]
                                hovered Function(set_action_stat_changes, girls=selected_girl, action=exam_action)
                                unhovered Function(action_stat_changes.clear)
                                if show_exam_action_tooltips:
                                    tooltip exam_action

                                hbox:
                                    xfill True
                                    yalign 0.5

                                    vbox:
                                        spacing 5

                                        $ suffix_string = ""
                                        if exam_action.player_only_action and person_doing_action != player:
                                            $ suffix_string += "(Player"
                                            if exam_action.is_tolerated(selected_girl):
                                                $ suffix_string += "/Tolerated)"
                                            else:
                                                $ suffix_string += ")"
                                        elif exam_action.is_tolerated(selected_girl):
                                            $ suffix_string += "(Tolerated)"

                                        text "[action_text] [suffix_string]" size font_size_large color menu_text_color yalign 0.5

                                        hbox:
                                            fixed:
                                                xsize 220
                                                text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[exam_action.time_cost] mins" size font_size_normal color menu_text_color

                                            fixed:
                                                xsize 220
                                                text f"{{color={menu_text_color_muted}}}Report Chance:{{/color}} [colorized_report_chance]" size font_size_normal color menu_text_color

                                            fixed:
                                                xsize 240
                                                if raw_success_chance < 100:
                                                    text f"{{color={menu_text_color_muted}}}Success Chance:{{/color}} [colorized_success_chance]" size font_size_normal color menu_text_color

                                            if exam_action.target:
                                                $ sensitivity_discovered = selected_girl.get_area_sensitivity_discovery_status(exam_action.target)
                                                if sensitivity_discovered:
                                                    $ sensitivity = selected_girl.get_area_sensitivity(exam_action.target)
                                                    text f"{{color={menu_text_color_muted}}}Sensitivity:{{/color}} x[sensitivity]" size font_size_normal color menu_text_color
                                                else:
                                                    text f"{{color={menu_text_color_muted}}}Sensitivity:{{/color}} Unknown" size font_size_normal color menu_text_color

                                    if has_custom_video:
                                        imagebutton:
                                            xalign 1.0
                                            yalign 0.5
                                            idle video_widget_green
                                            hover video_widget_green
                                            action NullAction()
                                            tooltip "Girl has video"
                                    elif has_custom_video is False:
                                        imagebutton:
                                            xalign 1.0
                                            yalign 0.5
                                            idle video_widget_red
                                            hover video_widget_red
                                            action NullAction()
                                            tooltip "Will use generic video"

                        for exam_action, has_custom_video, raw_success_chance, colorized_success_chance, raw_report_chance, colorized_report_chance, action_possible in unavailable_tease_actions:
                            $ action_text = exam_action.get_display_name()
                            $ action_tooltip = exam_action.requirement_description
                            if is_night_class and not exam_action.is_tolerated(girl=None):
                                $ action_tooltip = "Action not yet allowed by academy rules."

                            button:
                                style "exam_action_button"
                                action NullAction()
                                if action_tooltip:
                                    tooltip action_tooltip

                                $ suffix_string = ""
                                if exam_action.player_only_action and person_doing_action != player:
                                    $ suffix_string += "(Player"
                                    if exam_action.is_tolerated(selected_girl):
                                        $ suffix_string += "/Tolerated)"
                                    else:
                                        $ suffix_string += ")"
                                elif exam_action.is_tolerated(selected_girl):
                                    $ suffix_string += "(Tolerated)"

                                $ suffix_string = ""
                                if exam_action.player_only_action and person_doing_action != player:
                                    $ suffix_string += "(Player"
                                    if exam_action.is_tolerated(selected_girl):
                                        $ suffix_string += "/Tolerated)"
                                    else:
                                        $ suffix_string += ")"
                                elif exam_action.is_tolerated(selected_girl):
                                    $ suffix_string += "(Tolerated)"

                                hbox:
                                    xfill True
                                    yalign 0.5

                                    vbox:
                                        spacing 5

                                        text "{s}[action_text] [suffix_string]{/s}" size font_size_large color menu_text_color yalign 0.5

                                        hbox:
                                            fixed:
                                                xsize 220
                                                text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[exam_action.time_cost] mins" size font_size_normal color menu_text_color

                                            fixed:
                                                xsize 220
                                                text f"{{color={menu_text_color_muted}}}Report Chance:{{/color}} [colorized_report_chance]" size font_size_normal color menu_text_color

                                            fixed:
                                                xsize 240
                                                if raw_success_chance < 100:
                                                    text f"{{color={menu_text_color_muted}}}Success Chance:{{/color}} [colorized_success_chance]" size font_size_normal color menu_text_color

                                            if exam_action.target:
                                                $ sensitivity_discovered = selected_girl.get_area_sensitivity_discovery_status(exam_action.target)
                                                if sensitivity_discovered:
                                                    $ sensitivity = selected_girl.get_area_sensitivity(exam_action.target)
                                                    text f"{{color={menu_text_color_muted}}}Sensitivity:{{/color}} x[sensitivity]" size font_size_normal color menu_text_color
                                                else:
                                                    text f"{{color={menu_text_color_muted}}}Sensitivity:{{/color}} Unknown" size font_size_normal color menu_text_color

                                    if has_custom_video:
                                        imagebutton:
                                            xalign 1.0
                                            yalign 0.5
                                            idle video_widget_green
                                            hover video_widget_green
                                            action NullAction()
                                            tooltip "Girl has video"
                                    elif has_custom_video is False:
                                        imagebutton:
                                            xalign 1.0
                                            yalign 0.5
                                            idle video_widget_red
                                            hover video_widget_red
                                            action NullAction()
                                            tooltip "Will use generic video"

            frame:
                background menu_background_light
                xalign 1.0
                yalign 0.9
                xsize 370
                ysize 980
                
                vbox:
                    xfill True
                    xalign 0.5
                    spacing 5

                    hbox:
                        xfill True

                        vbox:
                            $ time_string = f"Time left: {exam_manager.get_remaining_minutes()}"
                            textbutton "[time_string]":
                                xalign 0.0
                                yalign 0.01
                                xpadding 0
                                ypadding 0
                                text_align 0.5
                                text_size 35
                                text_color menu_text_color
                                text_font header_font
                                action NullAction()
                                tooltip f"{exam_manager.get_remaining_minutes()} minutes remain of the class."

                            for stat_function in database_exam_hud_stats:
                                text stat_function() size font_size_normal color menu_text_color yalign 0.02

                        if teaching_assistant:
                            $ teaching_assistant_image = apply_brightness(fit_image_to_size(teaching_assistant.image_manager.get_face_image(), 85, 85), 0)
                            $ teaching_assistant_tooltip = f"Teaching Assistant: {teaching_assistant}"
                            if person_doing_action != player:
                                $ teaching_assistant_tooltip += "\n\nWill perform actions.\n-25% Impacts"
                            elif action_assistant:
                                $ teaching_assistant_tooltip += "\n\nWill assist you with actions.\n+25% Impacts"
                            
                            fixed:
                                xalign 1.0
                                xsize 85
                                ysize 85

                                imagebutton:
                                    idle teaching_assistant_image
                                    hover apply_brightness(teaching_assistant_image)
                                    action Show("teaching_assistant_quick_options", actions_menu=True)
                                    tooltip teaching_assistant_tooltip
                                
                                if person_doing_action != player:
                                    text "Teaching":
                                        style "intro_button_text"
                                        size font_size_small
                                        yalign 1.0
                                elif action_assistant:
                                    text "Assisting":
                                        style "intro_button_text"
                                        size font_size_small
                                        yalign 1.0

                    if not is_night_class:
                        text "Expectation:" size font_size_large color menu_text_color font header_font
                        vbox:
                            xalign 0.05
                            spacing 1

                            if selected_girl.mother.player_warnings > 0:
                                textbutton "{b}Mother Warning{/b}":
                                    xpadding 0
                                    ypadding 0
                                    text_size font_size_normal
                                    text_color menu_text_color_conflict
                                    action NullAction()
                                    tooltip f"Her mother has given you a warning about missing her grades.\nFailing to meet them again will result in her being {{color={menu_text_color_conflict}}}removed{{/color}} from the academy."

                            text f"{{color={menu_text_color_muted}}}Final Expected Grades:{{/color}} {selected_girl.grades}/{selected_girl.mother.expected_grades}" size font_size_small color menu_text_color

                            if selected_girl.mother.weekly_grade_target_met():
                                text "Weekly Grade Target Met" size font_size_small color menu_text_color_valid
                            else:
                                text f"{{color={menu_text_color_muted}}}Grade Target:{{/color}} {selected_girl.mother.get_next_grade_target()}" size font_size_small color menu_text_color

                            $ join_alumni_requirements_tooltip = selected_girl.get_join_alumni_requirements_tooltip()
                            textbutton "[join_alumni_requirements_tooltip]":
                                xpadding 0
                                ypadding 0
                                text_size font_size_small 
                                text_color menu_text_color 
                                action NullAction()
                                tooltip "Requirements to join alumni"

                    null height 5
                    text "Attributes:" size font_size_large color menu_text_color font header_font
                    $ girl_stats_to_display = selected_girl.get_dictionary_of_stats()
                    for stat_name, (stat_value, xp_stat_value) in girl_stats_to_display.items():
                        $ display_name = stat_name.capitalize()

                        $ stat_growth_multiplier, stat_growth_factors = selected_girl.get_stat_growth_multiplier_for_stat(stat_name, include_factors=True)
                        $ stat_growth_multiplier = round(stat_growth_multiplier, 2)
                        $ stat_growth_factors_string = " | ".join(stat_growth_factors)
                        $ stat_growth_tooltip = f"{display_name}\n\nStat Growth Factors:\n{stat_growth_factors_string}"

                        $ xp_requirement = int(calculate_next_xp_threshold(stat_value))
                        if stat_value == 100:
                            $ xp_stat_value = xp_requirement

                        $ stat_string = f"{display_name} ({stat_value}/100):"
                        $ stat_tooltip = get_stat_tooltip(stat_name)

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

                    #null height 5
                    use cherry_window(girl=selected_girl, position="topleft", border_color="#FF0000", border_size=3)
                    text "Traits:" size font_size_large color menu_text_color font header_font
                    viewport:
                        xmaximum 360
                        yfill False
                        draggable True
                        mousewheel True

                        hbox:
                            ymaximum 100
                            spacing 5
                            box_wrap True

                            for trait in selected_girl.trait_manager.get_filtered_traits():
                                textbutton "[trait]":
                                    ypadding 0
                                    text_color menu_text_color
                                    text_size font_size_normal
                                    text_outlines [(1, Color(trait.color).replace_opacity(0.6).hexcode, 0, 0)]
                                    action NullAction()
                                    tooltip trait.get_description()

                    null height 5
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
                        text_color menu_text_color
                        text_size font_size_large
                        text_font header_font
                        action NullAction()
                        tooltip area_sensitivity_string

                    if selected_girl.session_action_tracker:
                        $ action_tracker_string = ""
                        python:
                            action_tracker_strings = []
                            for action_name, action_count in selected_girl.session_action_tracker.items():
                                action_name = action_name.replace("_", " ").title()

                                action_tracker_strings.append(f"{action_name}: {action_count}")
                            
                            action_tracker_string = "\n".join(action_tracker_strings)

                        textbutton "Session Actions":
                            xpadding 0
                            ypadding 0
                            text_color menu_text_color
                            text_size font_size_large
                            text_font header_font
                            action NullAction()
                            tooltip action_tracker_string

                    if database_general_targeted_exam_actions:
                        null height 5
                        viewport:
                            ysize 185
                            xfill True
                            draggable True
                            mousewheel True
                            scrollbars "vertical"
                            vscrollbar_unscrollable "hide"

                            vbox:
                                spacing 3

                                $ too_many_general_actions = len(database_general_targeted_exam_actions) > 3
                                for exam_action in database_general_targeted_exam_actions:
                                    if not debug_mode and (("debug" in exam_action.label.lower() or "debug" in exam_action.name.lower()) or ("cheat" in exam_action.label.lower() or "cheat" in exam_action.name.lower())):
                                        continue

                                    $ action_text = exam_action.get_display_name()
                                    if exam_action.requirements_met(girl=selected_girl):
                                        button:
                                            style "global_exam_action_button"
                                            if too_many_general_actions:
                                                xsize 340
                                            else:
                                                xsize 355

                                            action [
                                                Hide("exam_actions_menu", _layer="master"), 
                                                Function(action_stat_changes.clear),
                                                Function(selected_girl.attempt_exam_action, exam_action), 
                                            ]
                                            hovered Function(set_action_stat_changes, girls=selected_girl, action=exam_action)
                                            unhovered Function(action_stat_changes.clear)
                                            if show_exam_action_tooltips:
                                                tooltip exam_action

                                            hbox:
                                                spacing 5
                                                box_wrap True
                                                text "[action_text]" size font_size_large color menu_text_color
                                                text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[exam_action.time_cost] minutes" size font_size_normal color menu_text_color
                                    else:
                                        button:
                                            style "global_exam_action_button"
                                            if too_many_general_actions:
                                                xsize 340
                                            else:
                                                xsize 355

                                            action NullAction()
                                            if exam_action.requirement_description:
                                                tooltip exam_action.requirement_description

                                            text "{s}[action_text]{/s}" size font_size_large color menu_text_color

                    if debug_mode:
                        null height 5
                        text "Clothing (Debug):" size font_size_small color menu_text_color font header_font
                        viewport:
                            ysize 165
                            draggable True
                            mousewheel True
                            vbox:
                                spacing 3
                                for clothing_tag, clothing_item in selected_girl.clothing_manager.outfit.items():
                                    $ clothing_tag = clothing_tag.capitalize()
                                    text f"{clothing_tag} - {clothing_item.name}" size font_size_small color menu_text_color

        if show_tutorial:
            frame:
                background "#FFFFFF"
                xalign 0.5
                yalign 0.86
                $ affection_tooltip = get_stat_tooltip("affection")
                $ corruption_tooltip = get_stat_tooltip("corruption")
                $ discipline_tooltip = get_stat_tooltip("discipline")
                $ fear_tooltip = get_stat_tooltip("fear")
                $ intellect_tooltip = get_stat_tooltip("intellect")
                $ naturism_tooltip = get_stat_tooltip("naturism")

                vbox:
                    xsize 800
                    spacing 5
                    box_wrap True
                    text affection_tooltip font header_font size font_size_normal color "#000000"
                    text corruption_tooltip font header_font size font_size_normal color "#000000"
                    text discipline_tooltip font header_font size font_size_normal color "#000000"
                    text fear_tooltip font header_font size font_size_normal color "#000000"
                    text intellect_tooltip font header_font size font_size_normal color "#000000"
                    text naturism_tooltip font header_font size font_size_normal color "#000000"

            imagebutton:
                xalign 0.5
                yalign 0.5
                idle "images/other/tutorial/exam_actions_tutorial.webp"
                action SetVariable("show_tutorial", False)
