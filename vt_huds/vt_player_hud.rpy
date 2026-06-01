# init 100:
    # python:
        # # Store old show actions
        # _old_show = renpy.show
        # _old_hide = renpy.hide
        
        # # Hook function to show the cherry HUD when player_hud is shown
        # def _show_player_cherry_hud():
            # renpy.show("player_cherry_hud")
        
        # def _hide_player_cherry_hud():
            # renpy.hide("player_cherry_hud")
        
        # # Wrap show to automatically show cherry HUD when player_hud shows
        # def show_with_player_cherry(*args, **kwargs):
            # if "player_hud" in args:
                # renpy.show("player_cherry_hud")
            # _old_show(*args, **kwargs)
        
        # # Wrap hide to automatically hide cherry HUD when player_hud hides
        # def hide_with_player_cherry(*args, **kwargs):
            # if "player_hud" in args:
                # renpy.hide("player_cherry_hud")
            # _old_hide(*args, **kwargs)
        
        # renpy.show = show_with_player_cherry
        # renpy.hide = hide_with_player_cherry


# # Separate screen that displays independently
# screen player_cherry_hud():
    # layer "overlay"
    # zorder 90
    
    # use hud_condom_cherry(position="right")

## Overide the default screen girl_hud
init 1:

    screen player_hud():
        if not renpy.get_screen("girl_selection_menu"):
            frame:
                background None
                ypadding 4

                if hud_changed:
                    if not global_stats_visible:
                        at hud_disappear()
                    else:
                        at hud_appear()
                else:
                    if not global_stats_visible:
                        xpos 0.96
                    else:
                        xpos 0.825

                hbox:
                    yalign 0.005
                    spacing 5

                    frame:
                        background menu_background_dark
                        xpadding 5
                        ypadding 5

                        hbox:
                            spacing 5
                            frame:
                                background menu_background_light
                                ysize 270
                                vbox:
                                    yfill True

                                    $ resized_prev_image = fit_image_to_size("gui/widgets/prev.webp", 50, 50)

                                    imagebutton:
                                        xalign 0.5
                                        yalign 0.5
                                        idle apply_brightness(resized_prev_image, 0.15)
                                        hover apply_brightness(resized_prev_image, 0.3)
                                        action Function(change_stats_visibility)
                                        if not global_stats_visible:
                                            tooltip "Show Stats"
                                        else:
                                            tooltip "Hide Stats"

                                    if time_manager.is_time_locked:
                                        imagebutton:
                                            xalign 0.5
                                            yalign 0.5
                                            idle apply_brightness("gui/widgets/phone.webp", -0.2)
                                            action NullAction()
                                            tooltip "It would be rude to call from here"
                                    else:
                                        imagebutton:
                                            xalign 0.5
                                            yalign 0.5
                                            idle apply_brightness("gui/widgets/phone.webp")
                                            hover apply_brightness("gui/widgets/phone.webp", 0.4)
                                            action Jump("show_home_visit_call_menu")
                                            tooltip "View phone\n{b}Hotkey{/b}: P"
                                            keysym "K_p"

                                    imagebutton:
                                        xalign 0.5
                                        yalign 0.5
                                        idle apply_brightness("gui/widgets/inventory.webp")
                                        hover apply_brightness("gui/widgets/inventory.webp", 0.4)
                                        action [
                                            Hide("player_hud"),
                                            Show("player_inventory_menu")
                                        ]
                                        tooltip "View inventory\n{b}Hotkey{/b}: I"
                                        keysym "K_i"
                                    
                                    #cherry window of activated stats
                                    use hud_condom_cherry(position="center")
                                    
                            frame:
                                background menu_background_light
                                xsize 250
                                yminimum 270

                                vbox:
                                    spacing 10
                                    vbox:
                                        $ day_of_week = time_manager.get_day_of_week()
                                        text "{b}[day_of_week]{/b} (Day [time_manager.total_days])" size font_size_normal color menu_text_color font header_font

                                        hbox:
                                            spacing 5
                                            $ current_time = time_manager.get_current_time()
                                            text "{b}[current_time]{/b}" size font_size_normal color menu_text_color
                                            if not time_manager.is_time_locked and (time_manager.hour > 6 or time_manager.hour < 3):
                                                $ resized_next_widget = fit_image_to_size("gui/widgets/next.webp", 25, 25)
                                                imagebutton:
                                                    yalign 0.4
                                                    idle apply_brightness(resized_next_widget, 0.15)
                                                    hover apply_brightness(resized_next_widget, 0.3)
                                                    action Function(player.wait_around)
                                                    tooltip "Wait 30 minutes"

                                    vbox:
                                        for stat_function in database_academy_hud_stats:
                                            $ stat_title, stat_value = stat_function()
                                            hbox:
                                                xsize 240
                                                xalign 0.5
                                                box_wrap True

                                                text "[stat_title]" size font_size_small color menu_text_color
                                                text "[stat_value]" size font_size_small color menu_text_color xalign 1.0

                                    vbox:
                                        for stat_function in database_player_hud_stats:
                                            $ stat_title, stat_value = stat_function()
                                            hbox:
                                                xsize 240
                                                xalign 0.5
                                                box_wrap True

                                                text "[stat_title]" size font_size_small color menu_text_color
                                                text "[stat_value]" size font_size_small color menu_text_color xalign 1.0
                                    # #cherry window of activated stats
                                    # vbox:
                                        # use hud_condom_cherry(position="center")

            if (global_current_location_label == "academy_office" and not renpy.get_screen("girl_hud")) or renpy.get_screen("map_navigation_menu", layer="master"):
                frame:
                    background menu_background_dark
                    xalign 0.0
                    yalign 0.0
                    xpadding 5
                    ypadding 5

                    hbox:
                        spacing 5

                        if global_current_location_label == "academy_office":
                            imagebutton:
                                xalign 0.5
                                yalign 0.5
                                idle apply_brightness("gui/widgets/home.webp", 0)
                                hover apply_brightness("gui/widgets/home.webp")
                                action [
                                    Hide("player_hud"),
                                    Jump("leave_for_home")
                                ]
                                tooltip "Leave for home"
                        else:
                            imagebutton:
                                xalign 0.5
                                yalign 0.5
                                idle apply_brightness("gui/widgets/home.webp", 0)
                                hover apply_brightness("gui/widgets/home.webp")
                                action [
                                    Hide("player_hud"),
                                    Jump("quick_leave_for_home")
                                ]
                                tooltip "Leave for home"

                        if (global_current_location_label == "academy_office" and not renpy.get_screen("girl_hud")) and not renpy.get_screen("map_navigation_menu", layer="master"):
                            if time_manager.is_school_hours():
                                for job_variable_name, job_data in database_office_hud_girls.items():
                                    $ requirements = job_data.get("requirements", "True")
                                    if not requirements_met(requirements):
                                        continue

                                    $ button_tooltip = job_data.get("tooltip", "")
                                    if callable(button_tooltip):
                                        $ button_tooltip = button_tooltip()
                                    $ button_tooltip = replace_variables_in_text(button_tooltip)

                                    $ hud_label = job_data.get("hud_label", None)

                                    $ assigned_faculty = globals().get(job_variable_name)
                                    if assigned_faculty:
                                        $ girl_face_image = fit_image_to_size(assigned_faculty.image_manager.get_first_face_image(), 100, 100)
                                        imagebutton:
                                            xalign 0.5
                                            yalign 0.5
                                            idle apply_brightness(girl_face_image, 0)
                                            hover apply_brightness(girl_face_image)
                                            if hud_label:
                                                action Jump(hud_label)
                                            else:
                                                action NullAction()
                                            tooltip button_tooltip
#endoffile