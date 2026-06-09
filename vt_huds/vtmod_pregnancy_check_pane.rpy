## VTMod pregnancy fullbody image check — floats over the middle panel of single_girl_rating_menu

screen vtmod_preg_check_pane():
    frame:
        # Positioned over the bottom two-thirds of the middle panel (xsize=400, starts at x≈780)
        xalign 0.0
        yalign 0.0
        xanchor 0.0
        yanchor 0.0
        xoffset 782
        yoffset 452
        xsize 392
        ysize 605
        background None
        padding (5, 5, 5, 5)

        viewport:
            xsize 382
            ysize 595
            draggable True
            mousewheel True
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"

            vbox:
                xsize 372
                spacing 5

                $ preg_keys = [key for key in selected_girl_rating.possible_fullbody_images if key.startswith("preg") and len(selected_girl_rating.possible_fullbody_images[key]) > 0]
                $ preg_count = len(preg_keys)
                $ vtmod_positive = preg_count > 0

                if vtmod_positive:
                    text "VTMod Positive" size font_size_small color menu_text_color_valid

                    vbox:
                        spacing 1
                        text f" - found [preg_count] preg fullbody images." size font_size_small color menu_text_color_valid
                        text " - keep in mind, doesn't count _slut/_whore varients." size font_size_small color menu_text_color_valid
                        text " - you do not have to create all 3, preg_bare is possible." size font_size_small color menu_text_color_valid

                    $ pregthird_keys = [key for key in selected_girl_rating.possible_fullbody_images if key.startswith("preg_3rd") and len(selected_girl_rating.possible_fullbody_images[key]) > 0]
                    $ pregthird_count = len(pregthird_keys)
                    if pregthird_count > 0:
                        text f" - found [pregthird_count] preg_3rd fullbody images." size font_size_small color menu_text_color_valid
                    else:
                        text " - no preg_3rd fullbody images found." size font_size_small color menu_text_color_conflict

                    $ pregsecond_keys = [key for key in selected_girl_rating.possible_fullbody_images if key.startswith("preg_2nd") and len(selected_girl_rating.possible_fullbody_images[key]) > 0]
                    $ pregsecond_count = len(pregsecond_keys)
                    if pregsecond_count > 0:
                        text f" - found [pregsecond_count] preg_2nd fullbody images." size font_size_small color menu_text_color_valid
                    else:
                        text " - no preg_2nd fullbody images found." size font_size_small color menu_text_color_conflict

                    $ pregfirst_keys = [key for key in selected_girl_rating.possible_fullbody_images if key.startswith("preg_1st") and len(selected_girl_rating.possible_fullbody_images[key]) > 0]
                    $ pregfirst_count = len(pregfirst_keys)
                    if pregfirst_count > 0:
                        text f" - found [pregfirst_count] preg_1st fullbody images." size font_size_small color menu_text_color_valid
                    else:
                        text " - no preg_1st fullbody images found." size font_size_small color menu_text_color_conflict

                else:
                    text "VTMod Negative" size font_size_small color menu_text_color_conflict
                    text " - There is no preg fullbody images" size font_size_small color menu_text_color_conflict
