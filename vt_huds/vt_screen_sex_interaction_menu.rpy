#override the sex_interaction
init 1:

    # TODO - See time of day on UI
    screen sex_interaction_menu():
        $ resized_video_widget = fit_image_to_size("gui/widgets/video_button.webp", 35)
        $ video_widget_green = apply_tint(resized_video_widget, "#00FF00")
        $ video_widget_red = apply_tint(resized_video_widget, "#FF0000")

        $ cum_button = clothing_overview_buttons.get("cum", clothing_overview_buttons["unknown"])
        $ ripped_button = clothing_overview_buttons.get("ripped", clothing_overview_buttons["unknown"])

        frame:
            background menu_background_dark
            xsize 1920
            ysize 1080
            ypadding 5
            xpadding 5
            
            hbox:
                xalign 0.5
                yalign 0.01
                spacing 10
                text "{b}Perform Interactions{/b}" size font_size_large_header color menu_text_color font header_font

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
            
            # text "{b}Perform Interactions{/b}" size font_size_header color menu_text_color xalign 0.5 yalign 0.01

            # imagebutton:
                # xalign 0.642
                # yalign 0.015
                # idle apply_brightness("gui/widgets/inventory.webp")
                # hover apply_brightness("gui/widgets/inventory.webp", 0.4)
                # action Show("player_inventory_menu", show_hud=False)
                # tooltip "View inventory"
            
            # # Added Cherry Condoms (reusable component)
            # null height 10
            # use condom_cherry(position="center")
            
            hbox:
                xalign 1.0
                yalign 0
                spacing 25

                vbox:
                    xsize 380
                    yalign 0.5

                    text "Current Time: [time_manager.get_current_time()]" size font_size_large color menu_text_color

                    if persistent.sex_limit_duration:
                        if se_interaction_type == "ffm":
                            $ available_time = persistent.sex_ffm_duration_in_minutes
                        else:
                            $ available_time = persistent.sex_duration_in_minutes

                        text "Time Spent: [se_current_duration]/[available_time] mins"size font_size_large color menu_text_color
                    else:
                        text "Time Spent: [se_current_duration] mins"size font_size_large color menu_text_color

                imagebutton:
                    xoffset 5
                    yoffset -5

                    idle "gui/widgets/close.webp"
                    hover apply_brightness("gui/widgets/close.webp", 0.5)
                    action [
                        Hide("sex_interaction_menu", _layer="master"),
                        Jump("end_sex_interaction")
                    ]
                    tooltip "End Interaction"

            hbox:
                xalign 0.01
                yalign 0.01
                spacing 5
                $ resized_info_widget = fit_image_to_size("gui/widgets/info.webp", 40, 40)
                if show_sex_action_tooltips:
                    $ resized_info_widget = apply_tint(resized_info_widget, menu_enabled_icon_color)
                else:
                    $ resized_info_widget = apply_tint(resized_info_widget, menu_disabled_icon_color)

                imagebutton:
                    idle resized_info_widget
                    hover apply_brightness(resized_info_widget, 0.5)
                    action Function(change_sex_action_tooltip_visibility)
                    tooltip "Show Action Tooltips\nDefault: True"

                null width 3
                add "gui/widgets/separator.webp" ysize 25 yalign 0.5
                null width 3

                $ resized_skip_desc_widget = fit_image_to_size("gui/widgets/skip_desc.webp", 40, 40)
                if sex_skip_descriptions:
                    $ resized_skip_desc_widget = apply_tint(resized_skip_desc_widget, menu_enabled_icon_color)
                else:
                    $ resized_skip_desc_widget = apply_tint(resized_skip_desc_widget, menu_disabled_icon_color)

                imagebutton:
                    idle resized_skip_desc_widget
                    hover apply_brightness(resized_skip_desc_widget, 0.5)
                    action Function(change_sex_action_description_skipping)
                    tooltip "Skip Action Descriptions\nDefault: False"
                
                $ resized_skip_resp_widget = fit_image_to_size("gui/widgets/skip_resp.webp", 40, 40)
                if sex_skip_responses:
                    $ resized_skip_resp_widget = apply_tint(resized_skip_resp_widget, menu_enabled_icon_color)
                else:
                    $ resized_skip_resp_widget = apply_tint(resized_skip_resp_widget, menu_disabled_icon_color)

                imagebutton:
                    idle resized_skip_resp_widget
                    hover apply_brightness(resized_skip_resp_widget, 0.5)
                    action Function(change_sex_action_response_skipping)
                    tooltip "Skip Action Responses\nDefault: False"

                null width 3
                add "gui/widgets/separator.webp" ysize 25 yalign 0.5
                null width 3

        hbox:
            ysize 980
            xalign 0.5
            yalign 0.9
            spacing 5

            frame:
                background menu_background_light
                xsize 505
                yfill True
                xalign 0.5

                vbox:
                    xsize 505
                    yalign 0.5
                    spacing 5

                    hbox:
                        spacing 5
                        for participant in se_participants:
                            if not isinstance(participant, Girl):
                                continue

                            fixed:
                                xsize small_sex_interaction_button_size
                                ysize small_sex_interaction_button_size

                                $ participant_image = fit_image_to_size(participant.image_manager.get_face_image(), small_sex_interaction_button_size, small_sex_interaction_button_size)
                                if participant.left_sex_interaction:
                                    textbutton "[participant.full_name]":
                                        style "sex_interaction_button_small"
                                        background desaturate_image(apply_brightness(participant_image, -0.4))
                                        action NullAction()
                                        tooltip "Left because of pressure."
                                else:
                                    textbutton "[participant.full_name]":
                                        style "sex_interaction_button_small"
                                        if selected_girl == participant and len(se_participants) > 0:
                                            background apply_brightness(participant_image, brightness=0.15)
                                            hover_background apply_brightness(participant_image)
                                        else:
                                            background participant_image
                                            hover_background apply_brightness(participant_image)
                                        if selected_girl == participant:
                                            action [
                                                SetVariable("se_selected_part", "face"),
                                                Function(sex_interaction_refresh)
                                            ]
                                        else:
                                            action [
                                                SetVariable("selected_girl", participant),
                                                Function(change_se_other_female),
                                                Function(sex_interaction_refresh)
                                            ]
                                        alternate Show("girl_quick_overview", girl=participant)
                                        tooltip f"Selected {participant}\nRight-Click: Overview for {participant}"

                                    vbox:
                                        yalign 0.02
                                        xalign 0.02
                                        spacing 2

                                        $ face_cum_tooltip = participant.get_body_part_cum_tooltip("face")
                                        if face_cum_tooltip:
                                            imagebutton:
                                                idle cum_button
                                                hover apply_brightness(cum_button)
                                                action NullAction()
                                                tooltip f"{face_cum_tooltip}"

                    fixed:
                        xsize wide_button_size_x
                        ysize wide_button_size_y

                        if se_selected_part == "boobs":
                            textbutton "Upper":
                                style "girl_exam_button_wide"
                                background apply_brightness(button_boobs, brightness=0.15)
                                hover_background apply_brightness(button_boobs)
                                action [
                                    SetVariable("se_selected_part", None),
                                    Function(sex_interaction_refresh)
                                ]
                        else:
                            textbutton "Upper":
                                style "girl_exam_button_wide"
                                background button_boobs
                                hover_background apply_brightness(button_boobs)
                                action [
                                    SetVariable("se_selected_part", "boobs"),
                                    Function(sex_interaction_refresh)
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
                        if se_selected_part == "ass":
                            textbutton "Lower:\nback":
                                style "girl_exam_button_wide"
                                background apply_brightness(button_ass, brightness=0.15)
                                hover_background apply_brightness(button_ass)
                                action [
                                    SetVariable("se_selected_part", None),
                                    Function(sex_interaction_refresh)
                                ]
                        else:
                            textbutton "Lower:\nback":
                                style "girl_exam_button_wide"
                                background button_ass
                                hover_background apply_brightness(button_ass)
                                action [
                                    SetVariable("se_selected_part", "ass"),
                                    Function(sex_interaction_refresh)
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
                        spacing 0

                        fixed:
                            xsize side_by_side_button_size_x
                            ysize side_by_side_button_size_y

                            if se_selected_part == "pussy":
                                textbutton "Lower:\nfront":
                                    style "girl_exam_button_side_by_side"
                                    background apply_brightness(button_pussy, brightness=0.15)
                                    hover_background apply_brightness(button_pussy)
                                    action [
                                        SetVariable("se_selected_part", None),
                                        Function(sex_interaction_refresh)
                                    ]
                            else:
                                textbutton "Lower:\nfront":
                                    style "girl_exam_button_side_by_side"
                                    background button_pussy
                                    hover_background apply_brightness(button_pussy)
                                    action [
                                        SetVariable("se_selected_part", "pussy"),
                                        Function(sex_interaction_refresh)
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
                            ysize side_by_side_button_size_y

                            if se_selected_part == "legs":
                                textbutton "Legs":
                                    style "girl_exam_button_side_by_side"
                                    background apply_brightness(button_legs, brightness=0.15)
                                    hover_background apply_brightness(button_legs)
                                    action [
                                        SetVariable("se_selected_part", None),
                                        Function(sex_interaction_refresh)
                                    ]
                            else:
                                textbutton "Legs":
                                    style "girl_exam_button_side_by_side"
                                    background button_legs
                                    hover_background apply_brightness(button_legs)
                                    action [
                                        SetVariable("se_selected_part", "legs"),
                                        Function(sex_interaction_refresh)
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
                xsize 345
                yfill True
                xalign 1.0
                xpadding 5
                ypadding 5

                vbox:
                    xsize 335
                    spacing 5

                    frame:
                        background menu_background_light
                        xsize 335

                        vbox:
                            spacing 3

                            $ arousal_text = player.get_arousal_text()
                            text "Player Arousal: [arousal_text]" size font_size_normal color menu_text_color
                            fixed:
                                ysize 14
                                xsize 250
                                bar:
                                    style "player_arousal_bar"
                                    ysize 10
                                    yalign 0.5
                                    value player.arousal
                                    range player.max_arousal

                                $ estimated_arousal_increase = action_stat_changes.get("player", {}).get("arousal", 0)
                                if "player" in action_stat_changes and estimated_arousal_increase:
                                    bar:
                                        style "bar_stat_change"
                                        ypos 0.1
                                        xsize 250
                                        ysize 14
                                        value player.arousal + estimated_arousal_increase
                                        range player.max_arousal

                            $ remaining_stamina = player.sex_interaction_cum_limit - se_player_cum_count
                            textbutton "Remaining Stamina: [remaining_stamina]":
                                xpadding 0
                                ypadding 0
                                text_size font_size_normal 
                                text_color menu_text_color
                                action NullAction()
                                tooltip f"Can cum {remaining_stamina} times before being exhausted."

                    for participant in se_participants:
                        if not isinstance(participant, Girl):
                            continue

                        $ estimated_arousal_increase = action_stat_changes.get(participant.id, {}).get("arousal", 0)
                        $ estimated_pressure_increase = action_stat_changes.get(participant.id, {}).get("pressure", 0)

                        frame:
                            background menu_background_light
                            xsize 335

                            vbox:
                                spacing 3
                                text "[participant.full_name]" size font_size_large color menu_text_color

                                $ area_sensitivity_string = ""
                                python:
                                    sensitivity_strings = []
                                    for area_name, (sensitivity, sensitivity_discovered) in participant.area_sensitivity.items():
                                        sensitivity = participant.get_area_sensitivity(area_name)

                                        if sensitivity_discovered:
                                            sensitivity_strings.append(f"{area_name.capitalize()}: x{sensitivity}")
                                        else:
                                            sensitivity_strings.append(f"{area_name.capitalize()}: Undiscovered")
                                    
                                    area_sensitivity_string = "\n".join(sensitivity_strings)

                                textbutton "Area Sensitivity":
                                    xalign 0 
                                    yalign 0.4
                                    xpadding 0
                                    ypadding 0
                                    text_size font_size_normal 
                                    text_color menu_text_color 
                                    action NullAction()
                                    tooltip area_sensitivity_string

                                if participant.session_action_tracker:
                                    $ action_tracker_string = ""
                                    python:
                                        action_tracker_strings = []
                                        for action_name, action_count in participant.session_action_tracker.items():
                                            action_name = action_name.replace("_", " ").title()

                                            action_tracker_strings.append(f"{action_name}: {action_count}")
                                        
                                        action_tracker_string = "\n".join(action_tracker_strings)

                                    textbutton "Session Actions":
                                        xpadding 0
                                        ypadding 0
                                        text_color menu_text_color
                                        text_size font_size_normal
                                        action NullAction()
                                        tooltip action_tracker_string

                                if not participant.left_sex_interaction:
                                    text "Cum Count: [participant.sex_interaction_cum_count]" size font_size_normal color menu_text_color

                                    $ arousal_text = participant.get_arousal_text()
                                    text "Arousal: [arousal_text]" size font_size_normal color menu_text_color
                                    fixed:
                                        ysize 14
                                        xsize 250
                                        bar:
                                            style "girl_arousal_bar"
                                            ysize 10
                                            yalign 0.5
                                            value participant.arousal
                                            range 100

                                        if participant.id in action_stat_changes and estimated_arousal_increase:
                                            bar:
                                                style "bar_stat_change"
                                                ypos 0.1
                                                xsize 250
                                                ysize 14
                                                value participant.arousal + estimated_arousal_increase
                                                range 100

                                    text "Pressure:" size font_size_normal color menu_text_color
                                    fixed:
                                        ysize 14
                                        xsize 250
                                        bar:
                                            style "gr_bar"
                                            ysize 10
                                            yalign 0.5
                                            value participant.pressure
                                            range 100

                                        if participant.id in action_stat_changes and estimated_pressure_increase:
                                            bar:
                                                style "bar_stat_change"
                                                ypos 0.1
                                                xsize 250
                                                ysize 14
                                                value participant.pressure + estimated_pressure_increase
                                                range 100

                                else:
                                    text "Left because of pressure" size font_size_normal color menu_text_color_conflict

            frame:
                background menu_background_light
                xsize 510
                yfill True
                xalign 1.0
                xpadding 5
                ypadding 5

                if sex_action_set:
                    viewport:
                        xfill True
                        yfill True
                        spacing 5
                        draggable True
                        mousewheel True
                        scrollbars "vertical"

                        vbox:
                            xfill True
                            spacing 3
                            for (sex_action, has_custom_video) in sex_action_set:
                                $ display_name = sex_action.get_display_name()
                                button:
                                    style "sex_interaction_button"
                                    if len(display_name) > 30:
                                        ysize 103

                                    action [
                                        SetVariable("se_selected_sex_action", sex_action),
                                        Function(action_stat_changes.clear),
                                        Jump("sex_interaction_wrapper")
                                    ]
                                    hovered Function(set_action_stat_changes, girls=se_participants, action=sex_action)
                                    unhovered Function(action_stat_changes.clear)
                                    if show_sex_action_tooltips:
                                        tooltip sex_action

                                    vbox:
                                        xsize 435
                                        spacing 5

                                        text "[display_name]" size font_size_large color menu_text_color
                                        text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[sex_action.time_cost] minutes" size font_size_normal color menu_text_color

                                    if has_custom_video:
                                        imagebutton:
                                            xalign 1.0
                                            idle video_widget_green
                                            hover video_widget_green
                                            action NullAction()
                                            tooltip "Girl has video"
                                    elif has_custom_video is False:
                                        imagebutton:
                                            xalign 1.0
                                            idle video_widget_red
                                            hover video_widget_red
                                            action NullAction()
                                            tooltip "Will use generic video"

                            for (sex_action, has_custom_video) in unavailable_sex_action_set:
                                if selected_girl and sex_action.target in selected_girl.outfit:
                                    continue

                                $ display_name = sex_action.get_display_name()
                                button:
                                    style "sex_interaction_button"
                                    if len(display_name) > 30:
                                        ysize 103

                                    action NullAction()
                                    if sex_action.requirement_description:
                                        tooltip sex_action.requirement_description

                                    vbox:
                                        xsize 435
                                        spacing 5

                                        text f"{{s}}{display_name}{{/s}}" size font_size_large color menu_text_color
                                        text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[sex_action.time_cost] minutes" size font_size_normal color menu_text_color

                                    if has_custom_video:
                                        imagebutton:
                                            xalign 1.0
                                            idle video_widget_green
                                            hover video_widget_green
                                            action NullAction()
                                            tooltip "Girl has video"
                                    elif has_custom_video is False:
                                        imagebutton:
                                            xalign 1.0
                                            idle video_widget_red
                                            hover video_widget_red
                                            action NullAction()
                                            tooltip "Will use generic video"
                elif se_selected_part:
                    text "{b}No available actions.{/b}" size font_size_large color menu_text_color xalign 0.5 yalign 0.5
                else:
                    text "{b}Select a part to see actions.{/b}" size font_size_large color menu_text_color xalign 0.5 yalign 0.5

            frame:
                background menu_background_light
                xsize 510
                yfill True
                xalign 1.0
                xpadding 5
                ypadding 5

                viewport:
                    xfill True
                    yfill True
                    spacing 5
                    draggable True
                    mousewheel True
                    scrollbars "vertical"

                    vbox:
                        xfill True
                        spacing 3
                        
                        vbox:
                            xfill True
                            hbox:
                                #Cherry Status
                                # Added Cherry Window (reusable component)
                                #null height 10
                                use cherry_window(girl=selected_girl, position="center", border_color="#FF0000", border_size=3)
                        
                        for sex_action in database_player_sex_options:
                            if sex_action.filter_requirements_met(selected_girl, se_participants):
                                continue

                            if not sex_action.requirements_met(selected_girl, se_participants):
                                continue

                            $ has_custom_video = media_helper.has_custom_video(sex_action.video_main_tag, selected_girl)

                            $ display_name = sex_action.get_display_name()
                            button:
                                style "sex_interaction_button"
                                if len(display_name) > 30:
                                    ysize 103

                                action [
                                    SetVariable("se_selected_sex_action", sex_action),
                                    Function(action_stat_changes.clear),
                                    Jump("sex_interaction_wrapper")
                                ]
                                hovered Function(set_action_stat_changes, girls=se_participants, action=sex_action)
                                unhovered Function(action_stat_changes.clear)
                                if show_sex_action_tooltips:
                                    tooltip sex_action

                                vbox:
                                    xsize 435
                                    spacing 5

                                    text "[display_name]" size font_size_large color menu_text_color
                                    text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[sex_action.time_cost] minutes" size font_size_normal color menu_text_color

                                if has_custom_video:
                                    imagebutton:
                                        xalign 1.0
                                        idle video_widget_green
                                        hover video_widget_green
                                        action NullAction()
                                        tooltip "Girl has video"
                                elif has_custom_video is False:
                                    imagebutton:
                                        xalign 1.0
                                        idle video_widget_red
                                        hover video_widget_red
                                        action NullAction()
                                        tooltip "Will use generic video"

                        for sex_action in database_player_sex_options:
                            if sex_action.filter_requirements_met(selected_girl, se_participants):
                                continue

                            if sex_action.requirements_met(selected_girl, se_participants):
                                continue

                            $ has_custom_video = media_helper.has_custom_video(sex_action.video_main_tag, selected_girl)

                            $ display_name = sex_action.get_display_name()
                            button:
                                style "sex_interaction_button"
                                if len(display_name) > 30:
                                    ysize 103

                                action NullAction()
                                if sex_action.requirement_description:
                                    tooltip sex_action.requirement_description

                                vbox:
                                    xsize 435
                                    spacing 5

                                    text f"{{s}}{display_name}{{/s}}" size font_size_large color menu_text_color
                                    text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[sex_action.time_cost] minutes" size font_size_normal color menu_text_color

                                if has_custom_video:
                                    imagebutton:
                                        xalign 1.0
                                        idle video_widget_green
                                        hover video_widget_green
                                        action NullAction()
                                        tooltip "Girl has video"
                                elif has_custom_video is False:
                                    imagebutton:
                                        xalign 1.0
                                        idle video_widget_red
                                        hover video_widget_red
                                        action NullAction()
                                        tooltip "Will use generic video"

                        if threesome_sex_action_set:
                            null height 5
                            text "Threesome Actions" size font_size_large color menu_text_color xalign 0.5 yalign 0.5

                            for (sex_action, has_custom_video) in threesome_sex_action_set:
                                if se_other_female:
                                    $ display_name = sex_action.get_ffm_display_name()
                                else:
                                    $ display_name = sex_action.get_mmf_display_name()

                                button:
                                    style "sex_interaction_button"
                                    if len(display_name) > 30:
                                        ysize 103

                                    action [
                                        SetVariable("se_selected_sex_action", sex_action),
                                        SetVariable("is_threesome_action", True),
                                        Function(action_stat_changes.clear),
                                        Jump("sex_interaction_wrapper")
                                    ]
                                    hovered Function(set_action_stat_changes, girls=se_participants, action=sex_action, player_doing_action=False)
                                    unhovered Function(action_stat_changes.clear)
                                    if show_sex_action_tooltips:
                                        tooltip sex_action

                                    vbox:
                                        xsize 435
                                        spacing 5

                                        text "[display_name]" size font_size_large color menu_text_color
                                        text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[sex_action.time_cost] minutes" size font_size_normal color menu_text_color

                                    if has_custom_video:
                                        imagebutton:
                                            xalign 1.0
                                            idle video_widget_green
                                            hover video_widget_green
                                            action NullAction()
                                            tooltip "Girl has video"
                                    elif has_custom_video is False:
                                        imagebutton:
                                            xalign 1.0
                                            idle video_widget_red
                                            hover video_widget_red
                                            action NullAction()
                                            tooltip "Will use generic video"

                            for (sex_action, has_custom_video) in unavailable_threesome_sex_action_set:
                                if se_other_female:
                                    $ display_name = sex_action.get_ffm_display_name()
                                else:
                                    $ display_name = sex_action.get_mmf_display_name()

                                button:
                                    style "sex_interaction_button"
                                    if len(display_name) > 30:
                                        ysize 103

                                    action NullAction()
                                    if sex_action.requirement_description:
                                        tooltip sex_action.requirement_description

                                    vbox:
                                        xsize 435

                                        text f"{{s}}{display_name}{{/s}}" size font_size_large color menu_text_color
                                        text f"{{color={menu_text_color_muted}}}Time Cost:{{/color}} ~[sex_action.time_cost] minutes" size font_size_normal color menu_text_color

                                    if has_custom_video:
                                        imagebutton:
                                            xalign 1.0
                                            idle video_widget_green
                                            hover video_widget_green
                                            action NullAction()
                                            tooltip "Girl has video"
                                    elif has_custom_video is False:
                                        imagebutton:
                                            xalign 1.0
                                            idle video_widget_red
                                            hover video_widget_red
                                            action NullAction()
                                            tooltip "Will use generic video"

                            # vbox:
                                # xfill True
                                # hbox:
                                    # #Cherry Status
                                    # # Added Cherry Window (reusable component)
                                    # #null height 10
                                    # use cherry_window(girl=selected_girl, position="center", border_color="#FF0000", border_size=3)
                                   
                                    

                                   
init 5:
    screen sex_outro_screen:
        frame:
            background menu_background_dark
            xsize 1920
            ysize 1080
            ypadding 5
            xpadding 5

            hbox:
                xalign 0.5
                yalign 0.01
                spacing 10
                text "{b}Sex Conclusion{/b}" size font_size_large_header color menu_text_color font header_font
                
                # Added Cherry Condoms (reusable component)
                # null height 10
                use condom_cherry(position="center")

                imagebutton:
                    yalign 0.5
                    idle apply_brightness("gui/widgets/inventory.webp")
                    hover apply_brightness("gui/widgets/inventory.webp", 0.4)
                    action Show("player_inventory_menu", show_hud=False)
                    tooltip "View inventory\n{b}Hotkey{/b}: I"
                    keysym "K_i"
                
                

            # hbox:
                # xalign 0.01
                # yalign 0.02
                # spacing 15

            # text "{b}Sex Conclusion{/b}" size font_size_large_header color menu_text_color font header_font xalign 0.5 yalign 0.01

            imagebutton:
                xalign 1.0
                yalign 0
                idle "gui/widgets/close.webp"
                hover apply_brightness("gui/widgets/close.webp", 0.5)
                if se_use_generic_ending or se_end_label == "generic_sex_ending" or se_end_label is None:
                    action [
                        Hide("sex_outro_screen", _layer="master"),
                        Jump("generic_sex_ending")
                    ]
                else:
                    action [
                        Hide("sex_outro_screen", _layer="master"),
                        Jump(se_end_label)
                    ]
                if persistent.right_click_close:
                    keysym "mouseup_3"
                    tooltip "{b}Hotkey{/b}: Right-Click"

            # # Added Cherry Condoms (reusable component)
            # null height 10
            # use condom_cherry(position="center")

            python:
                player.condom_cum = 0
                player.condom_dirty = False
                player.condom_broke = False
                player.condom_active = "raw"
                queue_notification("Cleaned up", duration=2.0)
                renpy.log("VT MOD: Sex Interaction Cleaned up after sex")

        hbox:
            xsize 1900
            ysize 980
            xalign 0.5
            yalign 0.9

            for participant in se_participants:
                if not isinstance(participant, Girl):
                    continue

                frame:
                    background menu_background_light
                    xalign 0.5
                    yalign 0.5
                    xsize 625
                    ysize 970
                    
                    vbox:
                        xsize 625
                        spacing 10

                        text "[participant.full_name]" size font_size_large_header color menu_text_color font header_font xalign 0.5 yalign 0.1

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
                                
                                $ face_image = fit_image_to_size(participant.image_manager.get_face_image(), 225, 225)
                                add face_image xalign 0.5 yalign 0.5
                                if participant.left_sex_interaction:
                                    imagebutton:
                                        idle fit_image_to_size("gui/widgets/left.webp", 225, 225)
                                        action NullAction()
                                        tooltip f"{participant} left before you finished."

                        if participant.id in se_stats_before_sex:
                            $ girl_stats_before = se_stats_before_sex[participant.id]

                            for stat_name, before_stat_value in girl_stats_before.items():
                                $ stat_title = f"{stat_name.title()}:"

                                $ current_stat_value = getattr(participant, stat_name)

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
                            text "Stats will be correctly tracked next interaction" size font_size_normal color menu_text_color xalign 0.5 yalign 0.5

                    # Added Cherry Window (reusable component)
                    null height 10
                    use cherry_window(girl=participant, position="bottom", border_color="#FF0000", border_size=3)

        #end