## girl_review_menu cherry widget now overlaid via vt_overlay.rpy
init 1:

    screen vtmod_virgin_preg_ui(girl=None):
        tag vtmod_ui  # CRITICAL FOR MANAGEMENT
        zorder 99
        modal False
        sensitive True
        # Full-screen click-catcher: click anywhere outside the info box to close
        button:
            xalign 0.0
            yalign 0.0
            xsize 1.0
            ysize 1.0
            background "#00000001"
            hover_background "#00000001"
            action Hide("vtmod_ui")

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
                            action Hide("vtmod_ui")
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
