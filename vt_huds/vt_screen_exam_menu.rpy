
init 1:

    # TODO - See time of day on UI
    screen exam_menu():
        $ resized_next_widget = fit_image_to_size("gui/widgets/next.webp", 25, 25)
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
                
                # Added Cherry Condoms (reusable component)
                null height 10
                use condom_cherry(position="center")

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
                if teaching_assistant:
                    action Show(
                        "confirm_user_choice", 
                        title_text="Leave exam early?", 
                        description_text=f"{teaching_assistant} will teach in your absence.", 
                        user_choices=(
                            ("Yes", "conclude_exam_early"), 
                            ("No", "none")
                        )
                    )
                else:
                    action Show(
                        "confirm_user_choice", 
                        title_text="End exam early?", 
                        description_text="This will prevent any further grades and stat changes.", 
                        user_choices=(
                            ("Yes", "conclude_exam_early"), 
                            ("No", "none")
                        )
                    )
                tooltip "End exam early"

        hbox:
            xsize 1900
            ysize 980
            xalign 0.5
            yalign 0.9
            spacing 5

            hbox:
                xsize 1525
                spacing 5
                for girl in available_girls:
                    $ estimated_tolerance_increase = action_stat_changes.get(girl.id, {}).get("tolerance", 0)
                    $ estimated_arousal_increase = action_stat_changes.get(girl.id, {}).get("arousal", 0)
                    $ estimated_pressure_increase = action_stat_changes.get(girl.id, {}).get("pressure", 0)
                    $ estimated_motivation_increase = action_stat_changes.get(girl.id, {}).get("motivation", 0)
                    $ estimated_grade_increase = action_stat_changes.get(girl.id, {}).get("grades", 0)

                    $ [button_face, button_boobs, button_pussy, button_ass, button_legs] = girl.image_manager.get_outfit_images()
                    $ button_face = fit_image_to_size(button_face, small_button_size, small_button_size)                     # Small
                    $ button_boobs = fit_image_to_size(button_boobs, wide_button_size_x, wide_button_size_y)                 # Wide
                    $ button_ass = fit_image_to_size(button_ass, wide_button_size_x, wide_button_size_y)                     # Wide
                    $ button_pussy = fit_image_to_size(button_pussy, side_by_side_button_size_x, side_by_side_button_size_y) # Side by Side
                    $ button_legs = fit_image_to_size(button_legs, side_by_side_button_size_x, side_by_side_button_size_y)   # Side by Side

                    frame:
                        background menu_background_light
                        xalign 0.5
                        yalign 0.9
                        xsize 505
                        ysize 980

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

                                    textbutton "[girl.full_name]":
                                        style "girl_exam_button_small"
                                        background button_face
                                        hover_background apply_brightness(button_face)
                                        action [
                                            SetVariable("selected_part", "face"),
                                            SetVariable("selected_girl", girl),
                                            Hide("exam_menu", _layer="master"),
                                            Jump("show_exam_actions_menu")
                                        ]

                                    vbox:
                                        yalign 0.02
                                        xalign 0.02
                                        spacing 2

                                        $ face_cum_tooltip = girl.get_body_part_cum_tooltip("face")
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

                                    $ tolerance_string = f"Tolerance: {girl.tolerance}/{girl.max_tolerance}"
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
                                            value girl.tolerance
                                            range girl.max_tolerance

                                        if girl.id in action_stat_changes and estimated_tolerance_increase:
                                            bar:
                                                style "bar_stat_change"
                                                ypos 0.1
                                                xsize 250
                                                ysize 14
                                                value girl.tolerance + estimated_tolerance_increase
                                                range girl.max_tolerance

                                    $ vulnerable_text = ""
                                    if girl.is_vulnerable_to_extreme_actions():
                                        $ vulnerable_text = f"{{color={arousal_colors[2]}}}Vulnerable{{/color}}"

                                    $ rounded_pressure = int(girl.pressure)
                                    $ pressure_for_vulnerable = girl.pressure_for_vulnerable()
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
                                            value girl.pressure
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

                                        if girl.id in action_stat_changes and estimated_pressure_increase:
                                            bar:
                                                style "bar_stat_change"
                                                ypos 0.1
                                                xsize 250
                                                ysize 14
                                                value girl.pressure + estimated_pressure_increase
                                                range 100

                                    $ arousal_text = girl.get_arousal_text()

                                    $ rounded_arousal = int(girl.arousal)
                                    $ arousal_for_vulnerable = girl.arousal_for_vulnerable()
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
                                            value girl.arousal
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
                                                tooltip f"{{color={menu_text_color_valid}}}Arousal target: {arousal_for_vulnerable} is met{{/color}}"
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
                                                tooltip f"Arousal target: {arousal_for_vulnerable} for vulnerable status"

                                        if girl.id in action_stat_changes and estimated_arousal_increase:
                                            bar:
                                                style "bar_stat_change"
                                                ypos 0.1
                                                xsize 250
                                                ysize 14
                                                value girl.arousal + estimated_arousal_increase
                                                range 100

                                    $ motivation_tooltip = get_stat_tooltip("motivation")
                                    $ motivation_changes_tooltip = get_motivation_changes_tooltip()
                                    $ motivation_tooltip += f"\n{motivation_changes_tooltip}"
                                    $ motivation_string = girl.get_motivation_string()

                                    textbutton "Motivation: [motivation_string]":
                                        xpadding 0
                                        ypadding 0
                                        text_size font_size_normal 
                                        text_color menu_text_color
                                        action NullAction()
                                        tooltip motivation_tooltip

                                    $ bar_size_and_color = girl.get_motivation_splits()
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
                                            value girl.motivation
                                            range 100

                                        if girl.id in action_stat_changes and estimated_motivation_increase:
                                            $ estimated_motivation_level = girl.motivation + estimated_motivation_increase
                                            bar:
                                                style "bar_stat_change"
                                                xsize 250
                                                ysize 14
                                                yalign 0.5
                                                value estimated_motivation_level
                                                range 100

                                    if not is_night_class:
                                        textbutton "Grades: [girl.grades]/100":
                                            xpadding 0
                                            ypadding 0
                                            text_size font_size_normal 
                                            text_color menu_text_color
                                            action NullAction()
                                            tooltip f"Her mother expects her to reach at least a {girl.mother.expected_grades} grade"

                                        fixed:
                                            ysize 10
                                            xsize 250
                                            bar:
                                                style "gr_bar"
                                                ysize 10
                                                value girl.grades
                                                range 100

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

                                            if girl.id in action_stat_changes and estimated_grade_increase:
                                                $ estimated_grade_level = girl.grades + estimated_grade_increase
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
                                    background button_boobs
                                    hover_background apply_brightness(button_boobs)
                                    action [
                                        SetVariable("selected_part", "boobs"),
                                        SetVariable("selected_girl", girl),
                                        Hide("exam_menu", _layer="master"),
                                        Jump("show_exam_actions_menu")
                                    ]

                                vbox:
                                    yalign 0.02
                                    xalign 0.02
                                    spacing 2

                                    $ boobs_cum_tooltip = girl.get_body_part_cum_tooltip("boobs")
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
                                        $ worn_item = girl.get_clothing_on_part(clothing_type)
                                        if worn_item:
                                            $ part_covered = girl.part_covered_by_clothing(clothing_type, ignore_transparent=False)
                                            $ vib_with_remote = worn_item.has_tag("vibrator") and girl.id in vibrator_remotes
                                            if not part_covered or vib_with_remote:
                                                $ item_button = clothing_overview_buttons.get(clothing_type, clothing_overview_buttons["unknown"])

                                                imagebutton:
                                                    yalign 0.5
                                                    xalign 0.5
                                                    idle item_button
                                                    hover apply_brightness(item_button)
                                                    if vib_with_remote:
                                                        action [
                                                            SetVariable("selected_girl", girl),
                                                            SetVariable("mouse_coords", renpy.get_mouse_pos()),
                                                            ToggleScreen("change_vibration_level_menu", clothing_item=worn_item, clear_girl=True)
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
                                    background button_ass
                                    hover_background apply_brightness(button_ass)
                                    action [
                                        SetVariable("selected_part", "ass"),
                                        SetVariable("selected_girl", girl),
                                        Hide("exam_menu", _layer="master"),
                                        Jump("show_exam_actions_menu")
                                    ]

                                vbox:
                                    yalign 0.02
                                    xalign 0.02
                                    spacing 2

                                    $ ass_cum_tooltip = girl.get_body_part_cum_tooltip("ass")
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
                                        $ worn_item = girl.get_clothing_on_part(clothing_type)
                                        if worn_item:
                                            $ part_covered = girl.part_covered_by_clothing(clothing_type, ignore_transparent=False)
                                            $ vib_with_remote = worn_item.has_tag("vibrator") and girl.id in vibrator_remotes
                                            if not part_covered or vib_with_remote:
                                                $ item_button = clothing_overview_buttons.get(clothing_type, clothing_overview_buttons["unknown"])

                                                imagebutton:
                                                    yalign 0.5
                                                    xalign 0.5
                                                    idle item_button
                                                    hover apply_brightness(item_button)
                                                    if vib_with_remote:
                                                        action [
                                                            SetVariable("selected_girl", girl),
                                                            SetVariable("mouse_coords", renpy.get_mouse_pos()),
                                                            ToggleScreen("change_vibration_level_menu", clothing_item=worn_item, clear_girl=True)
                                                        ]
                                                    else:
                                                        action NullAction()
                                                    tooltip worn_item

                            hbox:
                                xalign 0.5
                                spacing 5

                                fixed:
                                    xsize side_by_side_button_size_x
                                    ysize side_by_side_button_size_y

                                    textbutton "Lower:\nfront":
                                        style "girl_exam_button_side_by_side"
                                        background button_pussy
                                        hover_background apply_brightness(button_pussy)
                                        action [
                                            SetVariable("selected_part", "pussy"),
                                            SetVariable("selected_girl", girl),
                                            Hide("exam_menu", _layer="master"),
                                            Jump("show_exam_actions_menu")
                                        ]

                                    vbox:
                                        yalign 0.02
                                        xalign 0.02
                                        spacing 2

                                        $ pussy_cum_tooltip = girl.get_body_part_cum_tooltip("pussy")
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
                                            $ worn_item = girl.get_clothing_on_part(clothing_type)
                                            if worn_item:
                                                $ part_covered = girl.part_covered_by_clothing(clothing_type, ignore_transparent=False)
                                                $ vib_with_remote = worn_item.has_tag("vibrator") and girl.id in vibrator_remotes
                                                if not part_covered or vib_with_remote:
                                                    $ item_button = clothing_overview_buttons.get(clothing_type, clothing_overview_buttons["unknown"])

                                                    imagebutton:
                                                        yalign 0.5
                                                        xalign 0.5
                                                        idle item_button
                                                        hover apply_brightness(item_button)
                                                        if vib_with_remote:
                                                            action [
                                                                SetVariable("selected_girl", girl),
                                                                SetVariable("mouse_coords", renpy.get_mouse_pos()),
                                                                ToggleScreen("change_vibration_level_menu", clothing_item=worn_item, clear_girl=True)
                                                            ]
                                                        else:
                                                            action NullAction()
                                                        tooltip worn_item

                                fixed:
                                    xsize side_by_side_button_size_x
                                    ysize side_by_side_button_size_y
                                    textbutton "Legs":
                                        style "girl_exam_button_side_by_side"
                                        background button_legs
                                        hover_background apply_brightness(button_legs)
                                        action [
                                            SetVariable("selected_part", "legs"),
                                            SetVariable("selected_girl", girl),
                                            Hide("exam_menu", _layer="master"),
                                            Jump("show_exam_actions_menu")
                                        ]

                                    vbox:
                                        yalign 0.02
                                        xalign 0.02
                                        spacing 2

                                        $ legs_cum_tooltip = girl.get_body_part_cum_tooltip("legs")
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
                                            $ worn_item = girl.get_clothing_on_part(clothing_type)
                                            if worn_item:
                                                if clothing_type == "socks":
                                                    $ part_covered = "legs" in girl.get_clothing_on_part("shoes").covered_parts
                                                else:
                                                    $ part_covered = girl.part_covered_by_clothing(clothing_type, ignore_transparent=False)

                                                $ vib_with_remote = worn_item.has_tag("vibrator") and girl.id in vibrator_remotes
                                                if not part_covered or vib_with_remote:
                                                    $ item_button = clothing_overview_buttons.get(clothing_type, clothing_overview_buttons["unknown"])

                                                    imagebutton:
                                                        yalign 0.5
                                                        xalign 0.5
                                                        idle item_button
                                                        hover apply_brightness(item_button)
                                                        if vib_with_remote:
                                                            action [
                                                                SetVariable("selected_girl", girl),
                                                                SetVariable("mouse_coords", renpy.get_mouse_pos()),
                                                                ToggleScreen("change_vibration_level_menu", clothing_item=worn_item, clear_girl=True)
                                                            ]
                                                        else:
                                                            action NullAction()
                                                        tooltip worn_item

            frame:
                background menu_background_light
                xalign 1.0
                yalign 0.9
                xsize 370
                ysize 980

                vbox:
                    xalign 0.5
                    first_spacing 15
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
                                $ teaching_assistant_tooltip += "\n\nWill assist you with actions.\n+25% Impacts\n+25% Success Chance"

                            fixed:
                                xalign 1.0
                                xsize 85
                                ysize 85

                                imagebutton:
                                    idle teaching_assistant_image
                                    hover apply_brightness(teaching_assistant_image)
                                    action Show("teaching_assistant_quick_options")
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

                    $ too_many_actions = False
                    if renpy.variant("small"):
                        if len(database_global_exam_actions) + len(database_player_exam_actions) > 6:
                            $ too_many_actions = True
                    elif len(database_global_exam_actions) + len(database_player_exam_actions) > 10:
                        $ too_many_actions = True

                    viewport:
                        xfill True
                        yfill True
                        if too_many_actions:
                            draggable True
                            mousewheel True
                            scrollbars "vertical"

                        vbox:
                            xfill True
                            spacing 3

                            $ teaching_impacts_tooltip = get_teaching_impacts_tooltip(player_teaching_style)

                            button:
                                style "global_exam_action_button"
                                if too_many_actions:
                                    xsize 335

                                text "Change Teaching Style" size font_size_large color menu_text_color
                                action ToggleScreen("change_teaching_style_menu")
                                tooltip f"Change your teaching style and the impacts you and girls will receive\n\n{teaching_impacts_tooltip}"

                            $ teach_count = exam_manager.get_remaining_minutes() / exam_global_action_teach_class.time_cost
                            $ end_of_class_teaching_impacts_tooltip = get_teaching_impacts_tooltip(player_teaching_style, teach_count=teach_count)

                            button:
                                style "global_exam_action_button"
                                if too_many_actions:
                                    xsize 335

                                text "Teach until the end of class" size font_size_large color menu_text_color
                                action Show(
                                    "confirm_user_choice", 
                                    title_text="Teach until the end of class?", 
                                    description_text="This will give the girls stat increases based on the remaining time.", 
                                    user_choices=(
                                        ("Yes", "exam_global_action_teach_until_end"), 
                                        ("No", "none")
                                    )
                                )
                                tooltip f"Teach until the end of class\n\n{end_of_class_teaching_impacts_tooltip}"

                            button:
                                style "global_exam_action_button"
                                if too_many_actions:
                                    xsize 335

                                vbox:
                                    spacing 5
                                    text "[exam_global_action_teach_class.display_name]" size font_size_large color menu_text_color
                                    text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[exam_global_action_teach_class.time_cost] minutes" size font_size_small color menu_text_color
                                action [
                                    Hide("exam_actions_menu", _layer="master"),
                                    Function(action_stat_changes.clear),
                                    Function(exam_global_action_teach_class.call_global_action)
                                ]
                                tooltip f"{exam_global_action_teach_class.display_name}\n\n{teaching_impacts_tooltip}"

                            for exam_action in database_global_exam_actions:
                                if not debug_mode and (("debug" in exam_action.label.lower() or "debug" in exam_action.name.lower()) or ("cheat" in exam_action.label.lower() or "cheat" in exam_action.name.lower())):
                                    continue

                                $ action_text = exam_action.get_display_name()
                                if is_night_class and not exam_action.is_tolerated(girl=None):
                                    button:
                                        style "global_exam_action_button"
                                        if too_many_actions:
                                            xsize 335
                                        action NullAction()
                                        tooltip "Action not yet allowed by academy rules."

                                        text "{s}[action_text]{/s}" size font_size_large color menu_text_color
                                elif exam_action.requirements_met(girl=None):
                                    button:
                                        style "global_exam_action_button"
                                        if too_many_actions:
                                            xsize 335
                                        action [
                                            Hide("exam_actions_menu", _layer="master"),
                                            Function(action_stat_changes.clear),
                                            Function(exam_action.call_global_action)
                                        ]
                                        hovered Function(set_action_stat_changes, girls=available_girls, action=exam_action)
                                        unhovered Function(action_stat_changes.clear)

                                        if show_exam_action_tooltips:
                                            tooltip exam_action

                                        vbox:
                                            spacing 5
                                            text "[action_text]" size font_size_large color menu_text_color
                                            text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[exam_action.time_cost] minutes" size font_size_small color menu_text_color
                                else:
                                    button:
                                        style "global_exam_action_button"
                                        if too_many_actions:
                                            xsize 335
                                        action NullAction()
                                        if exam_action.requirement_description:
                                            tooltip exam_action.requirement_description

                                        text "{s}[action_text]{/s}" size font_size_large color menu_text_color

                            for exam_action in database_player_exam_actions:
                                if not debug_mode and (("debug" in exam_action.label.lower() or "debug" in exam_action.name.lower()) or ("cheat" in exam_action.label.lower() or "cheat" in exam_action.name.lower())):
                                    continue

                                $ action_text = exam_action.get_display_name()
                                if is_night_class and not exam_action.is_tolerated(girl=None):
                                    button:
                                        style "global_exam_action_button"
                                        if too_many_actions:
                                            xsize 335
                                        action NullAction()
                                        tooltip "Action not yet allowed by academy rules."

                                        text "{s}[action_text]{/s}" size font_size_large color menu_text_color
                                elif exam_action.requirements_met(girl=None):
                                    button:
                                        style "global_exam_action_button"
                                        if too_many_actions:
                                            xsize 335
                                        action [
                                            Hide("exam_menu", _layer="master"),
                                            Function(action_stat_changes.clear),
                                            Function(exam_action.call_global_action)
                                        ]
                                        hovered Function(set_action_stat_changes, girls=available_girls, action=exam_action)
                                        unhovered Function(action_stat_changes.clear)

                                        if show_exam_action_tooltips:
                                            tooltip exam_action

                                        vbox:
                                            spacing 5
                                            text "[action_text]" size font_size_large color menu_text_color
                                            text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[exam_action.time_cost] minutes" size font_size_small color menu_text_color
                                else:
                                    button:
                                        style "global_exam_action_button"
                                        if too_many_actions:
                                            xsize 335
                                        action NullAction()
                                        if exam_action.requirement_description:
                                            tooltip exam_action.requirement_description

                                        text "{s}[action_text]{/s}" size font_size_large color menu_text_color

        if show_tutorial:
            frame:
                background "#FFFFFF"
                xalign 0.05
                yalign 0.86

                $ tolerance_tooltip = get_stat_tooltip("tolerance")
                $ tolerance_tooltip += "\nTolerance loss is determined by how extreme your action is vs her corruption level, the more corrupted she is the less tolerance she will lose."
                $ tolerance_tooltip += "\nTolerated actions are less likely to be reported and if reported are less likely to result in any repercussions."
                $ tolerance_tooltip += "\nThese tolerated actions are highlighted in green, while actions that are likely to be reported are highlighted in red."
                $ tolerance_tooltip += "\nBe careful using more extreme actions on less corrupted/aroused students until they are allowed by PTA rules or they might report you."

                $ pressure_tooltip = get_stat_tooltip("pressure")
                $ pressure_tooltip += "\nIf it reaches 100 they will also flee the exam. This means they won't be subject to anymore training, you generally want to avoid this to avoid repercussions from their parents."

                $ arousal_tooltip = get_stat_tooltip("arousal")

                $ vulnerable_state_tooltip = "{b}Vulnerable State{/b}: When a girl is very aroused, pressured or corrupted she is considered in a 'Vulnerable State'.\nThis allows you to perform some actions even when their other requirements aren't met."
                $ motivation_tooltip = get_stat_tooltip("motivation")
                $ grades_tooltip = get_stat_tooltip("grades")

                vbox:
                    xsize 800
                    spacing 5
                    box_wrap True
                    text tolerance_tooltip font header_font size font_size_normal color "#000000"
                    text pressure_tooltip font header_font size font_size_normal color "#000000"
                    text arousal_tooltip font header_font size font_size_normal color "#000000"
                    text vulnerable_state_tooltip font header_font size font_size_normal color "#000000"
                    text motivation_tooltip font header_font size font_size_normal color "#000000"
                    text grades_tooltip font header_font size font_size_normal color "#000000"

            imagebutton:
                xalign 0.5
                yalign 0.5
                idle "images/other/tutorial/exam_tutorial.webp"
                action SetVariable("show_tutorial", False)

init 5:
    screen exam_outro_screen():
        frame:
            background menu_background_dark
            xsize 1920
            ysize 1080
            ypadding 0
            xpadding 0

            hbox:
                xalign 0.01
                yalign 0.02
                spacing 15

                $ resized_info_widget = fit_image_to_size("gui/widgets/info.webp", 40, 40)
                imagebutton:
                    idle resized_info_widget
                    hover apply_brightness(resized_info_widget, 0.5)
                    action SetVariable("show_tutorial", True)
                    tooltip "Show Tutorial"

                $ resized_skip_resp_widget = fit_image_to_size("gui/widgets/skip_resp.webp", 40, 40)
                if skip_stealing_responses:
                    $ resized_skip_resp_widget = apply_tint(resized_skip_resp_widget, menu_enabled_icon_color)
                    imagebutton:
                        yalign 0.5
                        idle resized_skip_resp_widget
                        hover apply_brightness(resized_skip_resp_widget, 0.5)
                        action [
                            Function(toggle_stealing_dialogue),
                            Jump("save_exam_outro_screen")
                        ]
                        tooltip "Skipping Stealing Responses\nDefault: False"
                else:
                    $ resized_skip_resp_widget = apply_tint(resized_skip_resp_widget, menu_disabled_icon_color)
                    imagebutton:
                        yalign 0.5
                        idle resized_skip_resp_widget
                        hover apply_brightness(resized_skip_resp_widget, 0.5)
                        action [
                            Function(toggle_stealing_dialogue),
                            Jump("save_exam_outro_screen")
                        ]
                        tooltip "Showing Stealing Responses\nDefault: False"

                $ resized_info_widget = fit_image_to_size("gui/widgets/panty_button.webp", 40, 40)
                imagebutton:
                    idle resized_info_widget
                    hover apply_brightness(resized_info_widget, 0.5)
                    action Show("set_stolen_clothing_types")
                    tooltip "Set stolen clothing types"

                add "gui/widgets/separator.webp" ysize 25 yalign 0.5

                if reputation_before_class == player.reputation:
                    text "No Reputation Change" size font_size_normal color menu_text_color xalign 0.5 yalign 0.5
                else:
                    text f"Reputation Change: {reputation_before_class} -> {player.reputation}" size font_size_normal color menu_text_color xalign 0.5 yalign 0.5
            hbox:
                xalign 0.5
                yalign 0.01
                spacing 10
                #text "{b}Exam Conclusion{/b}" size font_size_large_header color menu_text_color font header_font xalign 0.5 yalign 0.01
                text "{b}Exam Conclusion{/b}" size font_size_large_header color menu_text_color font header_font
                # Added Cherry Condoms (reusable component)
                null height 10
                use condom_cherry(position="center")

                python:
                    player.condom_cum = 0
                    player.condom_dirty = False
                    player.condom_broke = False
                    player.condom_active = "raw"
                    queue_notification("Cleaned up", duration=2.0)
                    renpy.log("VT MOD: EXAM Outro Cleaned up after sex")

            imagebutton:
                xalign 1.0
                yalign 0
                idle "gui/widgets/close.webp"
                hover apply_brightness("gui/widgets/close.webp", 0.5)
                action [
                    Hide("exam_outro_screen", _layer="master"),
                    Jump("conclude_exam_finish")
                ]
                if persistent.right_click_close:
                    keysym "mouseup_3"
                    tooltip "{b}Hotkey{/b}: Right-Click"

        hbox:
            xsize 1900
            ysize 980
            xalign 0.5
            yalign 0.9

            for girl in exam_manager.girls_in_exam.get("player", []) + exam_manager.girls_who_left_early:
                frame:
                    background menu_background_light
                    xalign 0.5
                    yalign 0.5
                    xsize 625
                    ysize 970
                    
                    vbox:
                        xsize 625
                        spacing 10

                        text "[girl.full_name]" size font_size_large_header color menu_text_color font header_font xalign 0.5 yalign 0.1

                        frame:
                            background None
                            xsize 625
                            ysize 225
                            xalign 0.5 
                            yalign 0.5
                            xpadding 0
                            ypadding 0

                            fixed:
                                xsize 225
                                ysize 225
                                xalign 0.5
                                yalign 0.5
                                
                                $ face_image = fit_image_to_size(girl.image_manager.get_face_image(), 225, 225)
                                add face_image xalign 0.5 yalign 0.5

                                if girl.not_in_room:
                                    imagebutton:
                                        idle fit_image_to_size("gui/widgets/left.webp", 225, 225)
                                        action NullAction()
                                        tooltip f"{girl} left the room before the end of the class."

                            if not girl.not_in_room:
                                vbox:
                                    xpos 0.7
                                    spacing 5

                                    if girl.id in clothing_to_try_steal:
                                        if any(item[0] for item in clothing_to_try_steal[girl.id]):
                                            $ colored_panty_button = apply_tint("gui/widgets/panty_button.webp", "#00FF00")
                                            imagebutton:
                                                idle apply_brightness(colored_panty_button, 0)
                                                hover apply_brightness(colored_panty_button)
                                                action Show("steal_clothing_selection_screen", girl=girl)
                                                tooltip f"Trying to steal some of {girl}'s clothing"
                                        else:
                                            $ colored_panty_button = apply_tint("gui/widgets/panty_button.webp", "#FF0000")
                                            imagebutton:
                                                idle apply_brightness(colored_panty_button, 0)
                                                hover apply_brightness(colored_panty_button)
                                                action Show("steal_clothing_selection_screen", girl=girl)
                                                tooltip f"Returning some of {girl}'s clothing"

                        if girl.id in exam_girl_stats_before_class:
                            $ girl_stats_before = exam_girl_stats_before_class[girl.id]

                            for stat_name, before_stat_value in girl_stats_before.items():
                                $ stat_title = f"{stat_name.title()}:"

                                $ current_stat_value = getattr(girl, stat_name)

                                hbox:
                                    spacing 3

                                    vbox:
                                        xsize 140
                                        text stat_title size font_size_normal color menu_text_color

                                    fixed:
                                        xsize 400
                                        ysize 20
                                        if before_stat_value < current_stat_value:
                                            bar:
                                                style "stat_increase_bar"
                                                xsize 400
                                                ysize 20
                                                yalign 0.5
                                                value current_stat_value
                                                range 100

                                            bar:
                                                style "stat_increase_before_bar"
                                                xsize 400
                                                ysize 20
                                                yalign 0.5
                                                value before_stat_value
                                                range 100

                                            imagebutton:
                                                xsize 400
                                                ysize 20
                                                idle "images/none.webp"
                                                action NullAction()
                                                tooltip f"{stat_title} {before_stat_value} -> {current_stat_value}"
                                        elif before_stat_value > current_stat_value:
                                            bar:
                                                style "stat_decrease_bar"
                                                xsize 400
                                                ysize 20
                                                yalign 0.5
                                                value before_stat_value
                                                range 100

                                            bar:
                                                style "stat_decrease_before_bar"
                                                xsize 400
                                                ysize 20
                                                yalign 0.5
                                                value current_stat_value
                                                range 100

                                            imagebutton:
                                                xsize 400
                                                ysize 20
                                                idle "images/none.webp"
                                                action NullAction()
                                                tooltip f"{stat_title} {before_stat_value} -> {current_stat_value}"
                                        else:
                                            bar:
                                                xsize 400
                                                ysize 20
                                                yalign 0.5
                                                value current_stat_value
                                                range 100
                        else:
                            text "Stats will be correctly tracked next class" size font_size_normal color menu_text_color xalign 0.5 yalign 0.5

                        if not is_night_class:
                            text "Assign Homework" size font_size_large color menu_text_color xalign 0.5 yalign 0.5

                            viewport:
                                xsize 614
                                yfill True
                                draggable True
                                mousewheel True
                                scrollbars "vertical"
                                vscrollbar_unscrollable "hide"

                                vbox:
                                    xsize 595
                                    spacing 3
                                    
                                    use cherry_window(girl=girl, position="top", border_color="#FF0000", border_size=3)
                                    
                                    button:
                                        style "global_exam_action_button"
                                        xsize 595
                                        text "No homework"
                                        action [
                                            SetField(girl, "active_homework_subject", None),
                                            Jump("save_exam_outro_screen")
                                        ]
                                        tooltip "Unassign all homework"

                                    for homework_subject in database_homework_subjects.values():
                                        if homework_subject.filter_requirements_met(girl):
                                            continue

                                        if not homework_subject.requirements_met(girl):
                                            continue

                                        $ homework_subject = girl.homework_subjects.get(homework_subject.id) or homework_subject
                                        $ homework_description = homework_subject.get_description(girl)

                                        button:
                                            style "global_exam_action_button"
                                            xsize 595
                                            text homework_subject.name

                                            if girl.active_homework_subject == homework_subject.id:
                                                background menu_background_rule_active
                                                hover_background menu_background_rule_active_hovered
                                                action NullAction()
                                            else:
                                                action [
                                                    SetField(girl, "active_homework_subject", homework_subject.id),
                                                    Function(girl.assign_homework_subject, homework_subject.id),
                                                    Jump("save_exam_outro_screen")
                                                ]
                                            tooltip homework_description

                                    for homework_subject in database_homework_subjects.values():
                                        if homework_subject.filter_requirements_met(girl):
                                            continue

                                        if homework_subject.requirements_met(girl):
                                            continue

                                        $ homework_description = homework_subject.get_description(girl)
                                        $ requirement_description = homework_subject.get_requirement_description()
                                        button:
                                            style "global_exam_action_button"
                                            background menu_background_rule_invalid
                                            hover_background menu_background_rule_invalid_hovered
                                            xsize 595
                                            text homework_subject.name
                                            action NullAction()
                                            tooltip f"{{color={menu_text_color_conflict}}}{requirement_description}{{/color}}\n{homework_description}"

                    # Added Cherry Window (reusable component)
                    # null height 10
                    # use cherry_window(girl=girl, position="bottom", border_color="#FF0000", border_size=3)

        if show_tutorial:
            imagebutton:
                xalign 0.5
                yalign 0.5
                idle "images/other/tutorial/exam_outro_tutorial.webp"
                hover "images/other/tutorial/exam_outro_tutorial.webp"
                action SetVariable("show_tutorial", False)