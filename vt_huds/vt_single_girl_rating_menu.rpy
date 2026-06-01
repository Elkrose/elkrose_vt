## Overide the girl_ratings_input
init 1:

    screen single_girl_rating_menu(girl_review=False):
        frame:
            background "gui/pc/browser.webp"
            xsize 1920
            ysize 1080
            ypadding 0
            xpadding 0
            
            text "corrupted_academy/settings/girl_ratings" size font_size_small color menu_text_color xalign 0.075 yalign 0.038

            text "{b}Girl Content Ratings{/b}" size font_size_large_header color menu_text_color xalign 0.5 yalign 0.075

            vbox:
                yalign 0.08
                xpos 0.64
                spacing 4

                $ resized_radio_selected = fit_image_to_size("gui/widgets/radio_selected.webp", 25, 25)
                $ resized_radio_unselected = fit_image_to_size("gui/widgets/radio_unselected.webp", 25, 25)
                hbox:
                    spacing 3

                    if show_missing_webm_tags:
                        imagebutton:
                            idle resized_radio_selected
                            hover apply_brightness(resized_radio_selected)
                            action SetVariable("show_missing_webm_tags", False),
                    else:
                        imagebutton:
                            idle resized_radio_unselected
                            hover apply_brightness(resized_radio_unselected)
                            action SetVariable("show_missing_webm_tags", True),
                    text "Show missing main tags" size font_size_small color menu_text_color  yalign 0.5
                
                hbox:
                    spacing 3
                    if include_remove_and_strip_tags:
                        imagebutton:
                            idle resized_radio_selected
                            hover apply_brightness(resized_radio_selected)
                            action SetVariable("include_remove_and_strip_tags", False),
                    else:
                        imagebutton:
                            idle resized_radio_unselected
                            hover apply_brightness(resized_radio_unselected)
                            action SetVariable("include_remove_and_strip_tags", True),
                    text "Include missing remove and strip tags" size font_size_small color menu_text_color  yalign 0.5

            $ resized_refresh_widget = fit_image_to_size("gui/widgets/refresh.webp", 50, 50)
            imagebutton:
                xalign 0.96
                yalign 0.01
                idle apply_brightness(resized_refresh_widget, 0)
                hover apply_brightness(resized_refresh_widget, 0.5)
                action [
                    Function(remove_girl_rating, selected_girl_rating), 
                    Function(generate_all_girl_ratings)
                ]
                tooltip "Refresh Selected Rating"

            imagebutton:
                xalign 1.0
                yalign 0
                idle "gui/widgets/close.webp"
                hover apply_brightness("gui/widgets/close.webp", 0.5)
                if girl_review:
                    action [
                        Hide("single_girl_rating_menu", _layer="master"),
                        Show("girl_review_menu", _layer="master")
                    ]
                else:
                    action [
                        Hide("single_girl_rating_menu", _layer="master"),
                        Jump("show_girl_ratings_menu_from_single")
                    ]
                if persistent.right_click_close:
                    keysym "mouseup_3"
                    tooltip "{b}Hotkey{/b}: Right-Click"

        frame:
            background menu_background_light
            xsize 1900
            ysize 920
            xalign 0.5
            yalign 0.9
            xpadding 5
            ypadding 5

            $ possible_body_images = selected_girl_rating.possible_body_images["face"]
            if possible_body_images:
                $ girl_face_image = apply_brightness(fit_image_to_size(possible_body_images[0].path, 250, 250), 0)
            else:
                $ girl_face_image = apply_brightness(fit_image_to_size("images/unknown.webp", 250, 250), 0)

            hbox:
                xsize 1850
                spacing 5
                
                frame:
                    background menu_background_light
                    xsize 760
                    yfill True
                    xpadding 5
                    ypadding 5
                    
                    hbox:
                        xsize 750
                        spacing 10

                        imagebutton:
                            xalign 0.0
                            yalign 0.5
                            idle girl_face_image
                            if not girl_review:
                                hover apply_brightness(girl_face_image)
                                action [
                                    Hide("single_girl_rating_menu", _layer="master"),
                                    Jump("show_girl_ratings_menu_from_single")
                                ]

                        vbox:
                            xsize 490
                            xalign 1.0
                            spacing 3
                            hbox:
                                text "{b}[selected_girl_rating]{/b}" size font_size_large color menu_text_color
                                if selected_girl_rating.mother_rating:
                                    textbutton "(Mother)" yoffset -6:
                                        text_size font_size_large
                                        text_color gui.hover_color
                                        text_hover_color menu_text_color_muted
                                        action [
                                            SetVariable("selected_girl_rating", selected_girl_rating.mother_rating),
                                            Jump("show_single_girl_rating_menu")
                                        ]

                            $ rating_grade = number_to_grade(selected_girl_rating.rating)
                            hbox:
                                spacing 5
                                text "{b}Overall:{/b}" yalign 0.5 size font_size_large color menu_text_color
                                textbutton "[rating_grade] ([selected_girl_rating.rating])":
                                    yalign 0.5
                                    xpadding 0
                                    ypadding 0
                                    text_size font_size_large
                                    text_color gui.hover_color
                                    text_hover_color menu_text_color_hover
                                    action NullAction()
                                    tooltip f"{selected_girl_rating.rating_tooltip}"

                            vbox:
                                spacing 1
                                for rating_name, rating_grade in selected_girl_rating.ratings.items():
                                    text "{b}[rating_name]: [rating_grade]{/b}" size font_size_small color menu_text_color

                            null height 10
                            textbutton "{b}Directory Path:{/b} [selected_girl_rating.folder_path]":
                                xpadding 0
                                ypadding 0
                                text_size font_size_small
                                text_color gui.hover_color
                                text_hover_color menu_text_color_muted
                                # action Function(os.startfile, os.path.join(game_path, selected_girl_rating.folder_path))
                                # tooltip "Open folder directory"

                            text "{b}Size:{/b} [selected_girl_rating.size] MB" size font_size_small color menu_text_color
                            if selected_girl_rating.modded_content_size > 0:
                                text "{b}Modded Content Size:{/b} [selected_girl_rating.modded_content_size] MB" size font_size_small color menu_text_color
                            text "{b}Modder:{/b} [selected_girl_rating.modder]" size font_size_small color menu_text_color

                            text "{b}Photoshoots:{/b} [selected_girl_rating.total_photoshoots]" size font_size_small color menu_text_color
                            text "{b}Videoshoots:{/b} [selected_girl_rating.total_videoshoots]" size font_size_small color menu_text_color

                            text "{b}Vids:{/b} [selected_girl_rating.total_webms]" size font_size_small color menu_text_color
                            text "{b}Events:{/b} [selected_girl_rating.total_events]" size font_size_small color menu_text_color

                frame:
                    background menu_background_light
                    xsize 400
                    yfill True
                    xpadding 5
                    ypadding 5

                    viewport:
                        xsize 400
                        draggable True
                        mousewheel True
                        scrollbars "vertical"
                        vscrollbar_unscrollable "hide"

                        vbox:
                            xsize 390
                            spacing 1
                            for positive in selected_girl_rating.rating_positives:
                                text "[positive]" size font_size_small color menu_text_color_valid

                frame:
                    background menu_background_light
                    xsize 720
                    yfill True
                    xpadding 5
                    ypadding 5

                    viewport:
                        xsize 710
                        draggable True
                        mousewheel True
                        scrollbars "vertical"
                        vscrollbar_unscrollable "hide"

                        vbox:
                            xsize 710
                            spacing 10
                            
                            $ preg_keys = [key for key in selected_girl_rating.possible_fullbody_images if key.startswith("preg") and len(selected_girl_rating.possible_fullbody_images[key]) > 0]
                            $ preg_count = len(preg_keys)
                            $ vtmod_positive = False
                            if preg_count > 0:
                                $ vtmod_positive = True
                            
                            vbox:
                                spacing 1
                                if vtmod_positive:
                                    text "VTMod Positive" size font_size_small color menu_text_color_valid
                                    text " - found [preg_count] preg fullbody images." size font_size_small color menu_text_color_valid 
                                    text " - keep in mind, doesn't count _slut/_whore varients." size font_size_small color menu_text_color_valid
                                    text " - you do not have to create all 3, preg_bare is possible." size font_size_small color menu_text_color_valid
                                    $ pregthird_keys = [key for key in selected_girl_rating.possible_fullbody_images if key.startswith("preg_3rd") and len(selected_girl_rating.possible_fullbody_images[key]) > 0]
                                    $ pregthird_count = len(pregthird_keys)
                                    if pregthird_count>0:
                                        text " - found [pregthird_count] preg_3rd fullbody images." size font_size_small color menu_text_color_valid 
                                    else:
                                        text " - no preg_3rd fullbody images found." size font_size_small color menu_text_color_conflict
                                    
                                    $ pregsecond_keys = [key for key in selected_girl_rating.possible_fullbody_images if key.startswith("preg_2nd") and len(selected_girl_rating.possible_fullbody_images[key]) > 0]
                                    $ pregsecond_count = len(pregsecond_keys)
                                    if pregsecond_count>0:
                                        text " - found [pregsecond_count] preg_2nd fullbody images." size font_size_small color menu_text_color_valid
                                    else:
                                        text " - no preg_2nd fullbody images found." size font_size_small color menu_text_color_conflict
                                    
                                    $ pregfirst_keys = [key for key in selected_girl_rating.possible_fullbody_images if key.startswith("preg_1st") and len(selected_girl_rating.possible_fullbody_images[key]) > 0]
                                    $ pregfirst_count = len(pregfirst_keys)
                                    if pregfirst_count>0:
                                        text " - found [pregfirst_count] preg_1st fullbody images." size font_size_small color menu_text_color_valid
                                    else:
                                        text " - no preg_1st fullbody images found." size font_size_small color menu_text_color_conflict
                                    
                                    # text "preg_3rd_" size font_size_small color menu_text_color_valid
                                    # for key in selected_girl_rating.possible_fullbody_images:
                                        # $ item_count = len(selected_girl_rating.possible_fullbody_images[key])
                                        # if key.startswith("preg") and item_count>0:
                                            # text "[key]: [item_count] items" size font_size_small color menu_text_color_valid
                                else:
                                    text "VTMod Negative" size font_size_small color menu_text_color_conflict
                                    text " - There is no preg fullbody images" size font_size_small color menu_text_color_conflict
                            
                            if selected_girl_rating.errors:
                                vbox:
                                    spacing 1
                                    text "Errors/Strong Warnings:" size font_size_normal color menu_text_color
                                    for error in selected_girl_rating.errors:
                                        if "Click portrait" in error:
                                            continue

                                        text "[error]" size font_size_small color menu_text_color_conflict

                            if selected_girl_rating.warnings:
                                vbox:
                                    spacing 1
                                    text "Warnings:" size font_size_normal color menu_text_color
                                    for warning in selected_girl_rating.warnings:
                                        text "[warning]" size font_size_small color menu_text_color_warning

                            if selected_girl_rating.shoot_tag_warnings:
                                vbox:
                                    spacing 1
                                    text "Shoot Warnings:" size font_size_normal color menu_text_color
                                    for shoot_warning in selected_girl_rating.shoot_tag_warnings:
                                        text "[shoot_warning]" size font_size_small color menu_text_color_conflict

                            if selected_girl_rating.image_tag_warnings:
                                vbox:
                                    spacing 1
                                    text "Image Tag Warnings:" size font_size_normal color menu_text_color
                                    for image_warning in selected_girl_rating.image_tag_warnings:
                                        text "[image_warning]" size font_size_small color menu_text_color_conflict

                            if selected_girl_rating.image_resolution_warnings:
                                vbox:
                                    spacing 1
                                    text "Image Resolution Warnings:" size font_size_normal color menu_text_color
                                    for image_warning in selected_girl_rating.image_resolution_warnings:
                                        text "[image_warning]" size font_size_small color menu_text_color_conflict

                            if selected_girl_rating.webm_tag_warnings:
                                vbox:
                                    spacing 1
                                    text "Webm Warnings:" size font_size_normal color menu_text_color
                                    for webm_warning in selected_girl_rating.webm_tag_warnings:
                                        text "[webm_warning]" size font_size_small color menu_text_color_conflict

                            if selected_girl_rating.size_warnings:
                                vbox:
                                    spacing 1
                                    text "Size Warnings:" size font_size_normal color menu_text_color
                                    for size_warning in selected_girl_rating.size_warnings:
                                        text "[size_warning]" size font_size_small color menu_text_color_conflict

                            if show_missing_webm_tags:
                                if selected_girl_rating.missing_webm_main_tag_warnings:
                                    vbox:
                                        spacing 1
                                        text "Missing Webm Main Tags:" size font_size_normal color menu_text_color
                                        for webm_warning in selected_girl_rating.missing_webm_main_tag_warnings:
                                            if not include_remove_and_strip_tags:
                                                if "remove_" in webm_warning or "strip_" in webm_warning:
                                                    continue

                                            text "[webm_warning]" size font_size_small color menu_text_color_warning
                            
                            # vbox:
                                # spacing 1
                                
                                
                                # text "VT Preg bodies:" size font_size_normal color menu_text_color
                            
                            
                            # if selected_girl_rating.possible_fullbody_images["preg_3rd_shower"]