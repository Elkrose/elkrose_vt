## Overide the default screen girl_hud
init 1:

    screen tooltip_overlay():
        zorder 100

        $ tooltip = GetTooltip()

        if tooltip:
            if isinstance(tooltip, Girl):         # tooltip = Girl
                frame at tooltip_fade_in:
                    background "#000000EF"
                    xmaximum max_tooltip_width
                    xpos max(min(int(renpy.get_mouse_pos()[0]), 1920 - max_tooltip_width), 5)
                    ypos 0.15

                    hbox:
                        spacing 5

                        frame:
                            background menu_background_light
                            ysize 590

                            vbox:
                                spacing 5

                                $ face_image = fit_image_to_size(tooltip.image_manager.get_first_face_image(), 100)
                                add face_image xalign 0.5

                                text "[tooltip.full_name]" size font_size_large color menu_text_color xalign 0.5

                                null height 5
                                add "gui/widgets/separator_h.webp" xsize 300 xalign 0.5
                                null height 5

                                # Stat Bars
                                $ girl_stats_to_display = tooltip.get_dictionary_of_stats()
                                for stat_name, (stat_value, xp_stat_value) in girl_stats_to_display.items():
                                    $ display_name = stat_name.capitalize()

                                    $ stat_growth_multiplier, stat_growth_factors = tooltip.get_stat_growth_multiplier_for_stat(stat_name, include_factors=True)
                                    $ stat_growth_multiplier = round(stat_growth_multiplier, 2)

                                    $ xp_requirement = int(calculate_next_xp_threshold(stat_value))

                                    $ stat_string = f"{display_name} ({stat_value}/100):"
                                    if xp_stat_value:
                                        if stat_value == 100:
                                            $ xp_stat_value = xp_requirement

                                    vbox:
                                        xsize 360
                                        ysize 35
                                        hbox:
                                            xsize 360
                                            ysize 20

                                            hbox:
                                                xsize 200
                                                yalign 0.5

                                                text "[stat_string]" size font_size_very_small color menu_text_color

                                            text "Multiplier: x[stat_growth_multiplier]" size font_size_very_small color menu_text_color

                                        if stat_name == "grades":
                                            fixed:
                                                ysize 15
                                                xsize 360
                                                bar:
                                                    ysize 15
                                                    value stat_value
                                                    range 100
                                                    # value DictValue(girl_stats_to_display[stat_name], 0, 100)

                                                if not tooltip.alumni:
                                                    $ remaining_grade_period = tooltip.mother.get_remaining_grade_period()
                                                    $ grade_target = tooltip.mother.get_next_grade_target()
                                                    $ grade_separator_xalign = linear_conversion(grade_target, 0, 100, 0.0, 1.0)

                                                    if tooltip.mother.weekly_grade_target_met():
                                                        if grade_target < tooltip.mother.expected_grades:
                                                            $ stat_separator = apply_tint("gui/widgets/separator_wide.webp", "#55FF64")
                                                            add stat_separator xalign grade_separator_xalign yalign 0.5
                                                        else:
                                                            $ stat_separator = apply_tint("gui/widgets/separator_wide.webp", "#FF55E5")
                                                            add stat_separator xalign grade_separator_xalign yalign 0.5
                                                    else:
                                                        if grade_target < tooltip.mother.expected_grades:
                                                            $ stat_separator = apply_tint("gui/widgets/separator_wide.webp", menu_text_color_warning)
                                                            add stat_separator xalign grade_separator_xalign yalign 0.5
                                                        else:
                                                            $ stat_separator = "gui/widgets/separator_wide.webp"
                                                            add stat_separator xalign grade_separator_xalign yalign 0.5

                                                    if grade_target != tooltip.mother.expected_grades:
                                                        $ final_grade_separator_xalign = linear_conversion(tooltip.mother.expected_grades, 0, 100, 0.0, 1.0)
                                                        if tooltip.mother.currently_met_expectations():
                                                            $ stat_separator = apply_tint("gui/widgets/separator_wide.webp", "#FF55E5")
                                                            add stat_separator xalign final_grade_separator_xalign yalign 0.5
                                                        else:
                                                            $ stat_separator = "gui/widgets/separator_wide.webp"
                                                            add stat_separator xalign final_grade_separator_xalign yalign 0.5
                                        else:
                                            fixed:
                                                ysize 15

                                                $ stat_limit = 100
                                                if stat_name in tooltip.stat_limits:
                                                    $ stat_limit = tooltip.get_stat_limit(stat_name)

                                                bar:
                                                    ysize 15
                                                    # value DictValue(girl_stats_to_display[stat_name], 0, 100)
                                                    value stat_value
                                                    range 100

                                                if stat_limit != 100:
                                                    $ stat_separator_xalign = linear_conversion(stat_limit, 0, 100, 0.0, 1.0)
                                                    $ stat_separator = apply_tint("gui/widgets/separator_wide.webp", menu_text_color_warning)
                                                    add stat_separator xalign stat_separator_xalign yalign 0.5
                                
                                if girl is None:
                                    if selected_girl:
                                        $ girl = selected_girl
                                
                                use cherry_window(girl=tooltip)

                        if not renpy.get_screen("phone_screen") and not renpy.get_screen("girl_selection_menu") and not renpy.get_screen("girl_review_menu", layer="master"):
                            frame:
                                background menu_background_light
                                ysize 590

                                $ [button_face, button_boobs, button_pussy, button_ass, button_legs] = tooltip.image_manager.get_outfit_images()
                                $ button_boobs = fit_image_to_size(button_boobs, small_wide_button_size_x, small_wide_button_size_y)                    # Wide
                                $ button_ass = fit_image_to_size(button_ass, small_wide_button_size_x, small_wide_button_size_y)                        # Wide
                                $ button_pussy = fit_image_to_size(button_pussy, small_side_by_side_button_size_x, small_side_by_side_button_size_y)    # Side by Side
                                $ button_legs = fit_image_to_size(button_legs, small_side_by_side_button_size_x, small_side_by_side_button_size_y)      # Side by Side

                                vbox:
                                    yalign 0.5
                                    spacing 5

                                    fixed:
                                        xsize small_wide_button_size_x
                                        ysize small_wide_button_size_y

                                        textbutton "Upper":
                                            style "small_girl_button_wide"
                                            background button_boobs

                                        $ worn_nipple_acc = tooltip.get_clothing_on_part("nipple_acc")
                                        if worn_nipple_acc:
                                            $ part_covered = tooltip.part_covered_by_clothing("nipple_acc", ignore_transparent=False)
                                            if not part_covered:
                                                $ item_button = clothing_overview_buttons.get("nipple_acc", clothing_overview_buttons["unknown"])

                                                add item_button xalign 1.0

                                    fixed:
                                        xsize small_wide_button_size_x
                                        ysize small_wide_button_size_y

                                        textbutton "Lower:\nback":
                                            style "small_girl_button_wide"
                                            background button_ass

                                        $ worn_buttplug = tooltip.get_clothing_on_part("buttplug")
                                        if worn_buttplug:
                                            $ part_covered = tooltip.part_covered_by_clothing("buttplug", ignore_transparent=False)
                                            if not part_covered:
                                                $ item_button = clothing_overview_buttons.get("buttplug", clothing_overview_buttons["unknown"])

                                                add item_button xalign 1.0

                                    hbox:
                                        spacing 5

                                        fixed:
                                            xsize small_side_by_side_button_size_x
                                            ysize small_side_by_side_button_size_y

                                            textbutton "Lower:\nfront":
                                                style "small_girl_button_side_by_side"
                                                background button_pussy

                                            $ worn_pussy_acc = tooltip.get_clothing_on_part("pussy_acc")
                                            if worn_pussy_acc:
                                                $ part_covered = tooltip.part_covered_by_clothing("pussy_acc", ignore_transparent=False)
                                                if not part_covered:
                                                    $ item_button = clothing_overview_buttons.get("pussy_acc", clothing_overview_buttons["unknown"])

                                                    add item_button xalign 1.0

                                        textbutton "Legs":
                                            style "small_girl_button_side_by_side"
                                            background button_legs
            else:
                nearrect:
                    focus "tooltip"
                    preferred_side "top"
                    invert_offsets True

                    frame at tooltip_fade_in:
                        background "#000000EF"
                        xmaximum max_tooltip_width

                        if isinstance(tooltip, Action):         # tooltip = ExamAction or SexAction
                            frame:
                                background menu_background_light

                                vbox:
                                    $ action_text = tooltip.get_display_name()
                                    text "[action_text]" size font_size_large color menu_text_color xalign 0.5

                                    null height 3
                                    add "gui/widgets/separator_h_wide.webp" xsize 400 xalign 0.5
                                    null height 3

                                    hbox:
                                        spacing 50

                                        $ action_tooltip_strings = tooltip.get_impacts_description(girl=selected_girl, extra_indenting=True)
                                        if action_tooltip_strings:
                                            vbox:
                                                $ action_impacts = action_tooltip_strings.get("impacts")
                                                $ action_report_string = action_tooltip_strings.get("report")
                                                $ action_allowance_string = action_tooltip_strings.get("allowance")

                                                for impact_string in action_impacts:
                                                    null height 5
                                                    text "[impact_string]" size font_size_tooltip color menu_text_color_tooltip

                                        vbox:
                                            if action_report_string:
                                                text "[action_report_string]" size font_size_tooltip color menu_text_color_tooltip

                                            if action_allowance_string:
                                                if action_report_string:
                                                    null height 3
                                                    add "gui/widgets/separator_h_wide.webp" xsize 250 xalign 0.5
                                                    null height 3

                                                text "[action_allowance_string]" size font_size_tooltip color menu_text_color_tooltip

                                            if action_report_string or action_allowance_string:
                                                null height 3
                                                add "gui/widgets/separator_h_wide.webp" xsize 250 xalign 0.5
                                                null height 3

                                            text "Info:" size font_size_normal color menu_text_color

                                            if selected_girl and tooltip.target != "face" and tooltip.target not in selected_girl.outfit:
                                                $ relevant_protection = selected_girl.clothing_manager.get_relevant_protection(tooltip.target)
                                                text f"  {{color={menu_text_color_muted}}}Area Protection:{{/color}} [relevant_protection]%" size font_size_normal color menu_text_color

                                            $ can_make_girl_cum = database_action_impacts.get(tooltip.action_entry_name, {}).get("can_make_girl_cum", False)
                                            text f"  {{color={menu_text_color_muted}}}Girl Can Cum:{{/color}} [can_make_girl_cum]" size font_size_normal color menu_text_color

                                            # Don't display this for threesome actions.
                                            if "_mmf_" not in tooltip.name and "_ffm_" not in tooltip.name:
                                                $ can_make_player_cum = database_action_impacts.get(tooltip.action_entry_name, {}).get("can_make_player_cum", False)
                                                text f"  {{color={menu_text_color_muted}}}Player Can Cum:{{/color}} [can_make_player_cum]" size font_size_normal color menu_text_color

                                                $ skill_types = database_action_impacts.get(tooltip.action_entry_name, {}).get("skill_type", [])
                                                if skill_types:
                                                    if isinstance(skill_types, str):
                                                        $ skill_types = [skill_types]

                                                    $ skill_types_string = " | ".join(skill_type.replace("_skill", "").title() for skill_type in skill_types)

                                                    text f"  {{color={menu_text_color_muted}}}Skill Types:{{/color}} [skill_types_string]" size font_size_normal color menu_text_color
                        elif isinstance(tooltip, Clothing):     # tooltip = Clothing
                            frame:
                                background menu_background_light

                                vbox:
                                    $ scaled_icon = fit_image_to_size(tooltip.images["clothing"], 100, 100)
                                    add scaled_icon xalign 0.5

                                    null height 5

                                    text "[tooltip.full_name_tag]" size font_size_large color menu_text_color xalign 0.5 text_align 0.5

                                    null height 3
                                    add "gui/widgets/separator_h_wide.webp" xsize 300 xalign 0.5
                                    null height 3

                                    $ cum_tooltip = tooltip.get_clothing_cum_tooltip()
                                    if cum_tooltip:
                                        text "[cum_tooltip]" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5

                                        null height 3
                                        add "gui/widgets/separator_h_wide.webp" xsize 200 xalign 0.5
                                        null height 3

                                    $ uncovered_parts_tooltip = tooltip.damage_level > 0 and tooltip.get_uncovered_parts_tooltip()
                                    if uncovered_parts_tooltip:
                                        text "[uncovered_parts_tooltip]" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5

                                        null height 3
                                        add "gui/widgets/separator_h_wide.webp" xsize 200 xalign 0.5
                                        null height 3

                                    $ covered_parts_tooltip = tooltip.damage_level > 0 and tooltip.get_covered_parts_tooltip()
                                    if covered_parts_tooltip:
                                        text "[covered_parts_tooltip]" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5

                                        null height 3
                                        add "gui/widgets/separator_h_wide.webp" xsize 200 xalign 0.5
                                        null height 3

                                    $ passive_stat_tooltip = tooltip.get_passive_stat_tooltip()
                                    if passive_stat_tooltip:
                                        text "[passive_stat_tooltip]" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5

                                        null height 3
                                        add "gui/widgets/separator_h_wide.webp" xsize 200 xalign 0.5
                                        null height 3

                                    $ clothing_tags = ", ".join(tooltip.get_tags_for_menu())
                                    if clothing_tags:
                                        text f"{{color={menu_text_color_muted}}}Clothing Tags:{{/color}} {clothing_tags}" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5

                                        null height 3
                                        add "gui/widgets/separator_h_wide.webp" xsize 200 xalign 0.5
                                        null height 3

                                    $ blackmarket_sale = renpy.get_screen("clothing_collection_menu", layer="master") or (renpy.get_screen("clothing_selection_menu", layer="master") and not is_purchasing_clothing)
                                    $ clothing_value = tooltip.get_value(blackmarket_sale=blackmarket_sale)
                                    text f"{{color={menu_text_color_muted}}}Value:{{/color}} ${clothing_value}" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5

                                    $ value_influences = tooltip.get_value_influences(blackmarket_sale=blackmarket_sale)
                                    text "Influences:" size font_size_normal color menu_text_color_muted xalign 0.5 text_align 0.5
                                    text "[value_influences]" size font_size_small color menu_text_color xalign 0.5 text_align 0.5

                                    null height 3
                                    add "gui/widgets/separator_h_wide.webp" xsize 200 xalign 0.5
                                    null height 3

                                    if renpy.get_screen("exam_intro_menu", layer="master") or renpy.get_screen("exam_menu", layer="master") or renpy.get_screen("exam_actions_menu", layer="master"):
                                        $ rules_clothing_breaks = rule_manager.get_which_rules_clothing_breaks(tooltip)

                                        if rules_clothing_breaks:
                                            $ rules_clothing_breaks_string = join_list_of_strings(rules_clothing_breaks)
                                            text f"{{color={menu_text_color_muted}}}Breaks Rules:{{/color}} {rules_clothing_breaks_string}" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5
                                        else:
                                            text "Breaks no rules" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5

                                        null height 3
                                        add "gui/widgets/separator_h_wide.webp" xsize 200 xalign 0.5
                                        null height 3

                                    vbox:
                                        xalign 0.5
                                        spacing 0

                                        text f"{{color={menu_text_color_muted}}}Lewdness:{{/color}} {tooltip.lewdness}" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5
                                        # text "{i}Lewder clothing will passively increase the player's arousal, the class's corruption and the wearer's pressure depending on her corruption.{/i}" size font_size_small color menu_text_color xalign 0.5 text_align 0.5

                                    vbox:
                                        xalign 0.5
                                        spacing 0

                                        text f"{{color={menu_text_color_muted}}}Revealingness:{{/color}} {tooltip.revealingness}" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5
                                        # text "{i}More revealing clothing will passively increase the player's arousal, the class's naturism and the wearer's pressure depending on her naturism.{/i}" size font_size_small color menu_text_color xalign 0.5 text_align 0.5

                                    vbox:
                                        xalign 0.5
                                        spacing 0

                                        text f"{{color={menu_text_color_muted}}}Protection:{{/color}} {tooltip.protection}" size font_size_normal color menu_text_color xalign 0.5 text_align 0.5
                                        # text "{i}Protection decreases arousal and pressure impacts on parts clothing covers.{/i}" size font_size_small color menu_text_color xalign 0.5 text_align 0.5
                        elif isinstance(tooltip, StoreItem):    # tooltip = StoreItem
                            frame:
                                background menu_background_light

                                vbox:
                                    $ scaled_icon = fit_image_to_size(tooltip.icon, 125, 125)
                                    add scaled_icon xalign 0.5

                                    text "[tooltip.get_description()]" text_align 0.5 size font_size_normal color menu_text_color xalign 0.5
                        else:                                   # tooltip = str or list[str]
                            if not isinstance(tooltip, (list, tuple)):
                                $ tooltip = [tooltip]

                            hbox:
                                spacing 5
                                box_wrap True
                                for t in tooltip:
                                    if not t:
                                        continue

                                    frame:
                                        background menu_background_light
                                        text "[t]" size font_size_tooltip color menu_text_color_tooltip xalign 0.0

        # Tacked on here since it is always visible.
        $ video_button_selected = apply_tint("gui/widgets/video_button_large.webp", menu_text_color_conflict)
        $ video_button_unselected = apply_tint("gui/widgets/video_button_large.webp", menu_text_color_valid)
        if currently_playing_video and not renpy.get_screen("menu"):
            if currently_playing_video.hidden:
                imagebutton:
                    xalign 0.01
                    yalign 0.01
                    idle apply_brightness(video_button_selected, 0)
                    hover apply_brightness(video_button_selected)
                    action [
                        SetField(currently_playing_video, "hidden", False),
                        Function(persistent.hidden_webms.remove, currently_playing_video.path)
                    ]
                    tooltip "Show this video again."
            else:
                imagebutton:
                    xalign 0.01
                    yalign 0.01
                    idle apply_brightness(video_button_unselected, 0)
                    action [
                        SetField(currently_playing_video, "hidden", True),
                        Function(persistent.hidden_webms.append, currently_playing_video.path)
                    ]
                    if currently_playing_video_is_girl_video:
                        tooltip "Dont show this video again.\n\nCan be undone from girl review page."
                    else:
                        tooltip "Dont show this video again.\n\nCan be undone from generic video review page."
        elif currently_shown_image:
            if currently_shown_image.hidden:
                imagebutton:
                    xalign 0.01
                    yalign 0.01
                    idle apply_brightness(video_button_selected, 0)
                    hover apply_brightness(video_button_selected)
                    action SetField(currently_shown_image, "hidden", False)
                    tooltip "Show this image again."
            else:
                imagebutton:
                    xalign 0.01
                    yalign 0.01
                    idle apply_brightness(video_button_unselected, 0)
                    hover apply_brightness(video_button_unselected)
                    action SetField(currently_shown_image, "hidden", True)
                    if currently_shown_image_is_girl_image:
                        tooltip "Dont show this image again.\n\nCan be undone from girl review page."
                    else:
                        tooltip "Dont show this image again.\n\nCan be undone from generic image review page."
