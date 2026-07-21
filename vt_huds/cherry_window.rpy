screen cherry_minimum_window(girl=None, position="center", xoffset=0, yoffset=0, border_color="#FFFFFF", border_size=2, icon_size=50):
    $ girl = girl or persistent.selected_girl
    #$ girl = girl


    # Determine positioning values directly
    $ xalign_val = 0.5
    $ yalign_val = 0.5
    $ xanchor_val = 0.5
    $ yanchor_val = 0.5

    if position == "bottom":
        $ yalign_val = 1.0
        $ yanchor_val = 1.0
        $ yoffset = -10
    elif position == "left":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ xoffset = 10
    elif position == "right":
        $ xalign_val = 1.0
        $ xanchor_val = 1.0
        $ xoffset = -55
    elif position == "top":
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
        $ yoffset = 10
    elif position == "topleft":
        $ xalign_val = 0.0
        $ xanchor_val = 0.1
        $ yalign_val = 0.0
        $ yanchor_val = 0.0

    $ _frame_w = 6 * icon_size + 29 + border_size * 2

    #Single frame with proper sizing and border
    frame:
        xalign xalign_val
        yalign yalign_val
        xanchor xanchor_val
        yanchor yanchor_val
        xoffset xoffset
        yoffset yoffset
        xsize _frame_w
        #ysize 50
        padding (0, 0, 0, 0)

        # Border frame
        frame:
            xsize _frame_w
            #ysize 50
            background border_color
            padding (0, border_size, 0, border_size)

            # Content frame - contains background and UI
            frame:
                xsize (_frame_w - border_size * 2)
                xalign 0.5
                yalign 0.0
                xanchor 0.5
                yanchor 0.0
                padding (5, 5, 5, 5)
                background Frame("_mods/content/elkrose_vt/extra_images/Cherry_Background.png", xborder=1, yborder=1, xzoom=0.199, yzoom=0.201)
                #background Frame("_mods/content/vtmod/extra_images/Cherry_Background.png", xzoom=0.2, yzoom=0.2)

                vbox:
                    xsize (_frame_w - border_size * 2 - 4)
                    spacing 5
                    xalign 0.0  # Left-align content
                    yalign 0.0  # Top-align content

                        #First Row
                    hbox:
                        spacing 5
                        ysize icon_size

                        # Cherry Status
                        vbox:
                            xsize icon_size
                            xalign 0.0
                            imagebutton:
                                focus_mask True
                                at Transform(zoom=(icon_size / 50.0))
                                idle "_mods/content/elkrose_vt/extra_images/HUDVT_idle.png"
                                hover "_mods/content/elkrose_vt/extra_images/HUDVT_hover.png"
                                action Function(renpy.show_screen, "vtmod_virgin_preg_ui", girl=girl)
                                tooltip f"{{color=#ff0000}}Cherry Info.{{/color}}"

                        # Birth control status
                        vbox:
                            xsize icon_size
                            xalign 0.0
                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_token.png"
                            $ vt_tt_bc = "Unprotected"

                            if girl.pregnant and girl.player_knows_pregnant:
                                $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/feeding_bottle.png"
                                $ vt_tt_bc = f"{{color={menu_text_color_valid}}}Pregnant!{{/color}}"
                            else:
                                if girl.bc_status_known:
                                    $ vt_tt_bc += f"\nFertility: [girl.effective_fertility():.1f]%\n{girl.get_fertility_day_status()}"
                                    if girl.birth_control:
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_token.png"
                                        $ vt_tt_bc = f"{{color={menu_text_color_valid}}}Birth Control Active{{/color}}"
                                        if girl.vaginal_cum >= 1:
                                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_cum.png"
                                            $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                    else:
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_token.png"
                                        $ vt_tt_bc = "Unprotected"
                                        if girl.vaginal_cum >= 1:
                                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_cum.png"
                                            $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                        if girl.is_highly_fertile() :
                                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_fertile_cum.png"
                                            $ vt_tt_bc += f"\n{{color=#ff0000}}She is ovulating and has a higher chance of getting pregnant.{{/color}}"
                                else:
                                    $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bcknown.png"
                                    $ vt_tt_bc = "No idea if she is on birth control."

                            imagebutton:
                                focus_mask True
                                at Transform(zoom=(icon_size / 50.0))
                                idle vt_img_bc
                                action NullAction()
                                tooltip vt_tt_bc
                                xalign 0.0
                                yalign 0.0

                        # Sex/Arousal Status
                        vbox:
                            xsize icon_size
                            xalign 0.0

                            $ ss_tt_vag = f"{{color={menu_text_color_valid}}}Fresh and untouched, ready for action!{{/color}}"
                            $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/sexstatus.png"

                            if girl.hymen:
                                $ ss_tt_vag = f"{{color={menu_text_color_valid}}}A pristine canvas, untouched and pure!{{/color}}"
                                $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/virginsymbol.png"
                            else:
                                if girl.had_sex_today:
                                    $ ss_tt_vag = f"{{color={menu_text_color_valid}}}Had sex today!{{/color}}"
                                    $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/hadsextoday.png"
                                else:
                                    $ ss_tt_vag += f"\nNo sex today, yet."
                                    $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/sexstatus.png"

                            imagebutton:
                                focus_mask True
                                at Transform(zoom=(icon_size / 50.0))
                                idle ss_img_vag
                                action NullAction()
                                tooltip ss_tt_vag


                    # Item Status
                    hbox:
                        spacing 5
                        ysize icon_size
                        #Oral Status
                        vbox:
                            xsize icon_size
                            xalign 0.0

                            $ oralimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            $ oraltt = "No idea if she uses condoms for oral sex."
                            if girl.player_knows_oral_condom:
                                if girl.wants_oral_condom:
                                    $ oralimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                    $ oraltt =  f"{{color=#ff0000}}Wants Condom for Oral!{{/color}}"
                                else:
                                    $ oralimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                    $ oraltt =  f"{{color={menu_text_color_valid}}}Likes the risk during Oral!{{/color}}"
                                    if girl.oral_cum > 0:
                                        $ cumtextfix = "unit"
                                        if girl.oral_cum>1:
                                            $ cumtextfix = "units"
                                        $ oralimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                        $ oraltt =  f"{{color={menu_text_color_valid}}} Has {girl.oral_cum} {cumtextfix} of cum in her belly!{{/color}}"
                            else:
                                $ oraltt = "No idea if she wants condom for Oral."
                                $ oralimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                            fixed:
                                xysize (icon_size, icon_size)
                                xalign 0.5
                                imagebutton:
                                    focus_mask True
                                    at Transform(zoom=(icon_size / 50.0))
                                    xalign 0.5
                                    yalign 0.5
                                    idle oralimg
                                    action NullAction()
                                    tooltip oraltt
                                text "O":
                                    align (0.5, 0.5)
                                    size max(7, int(icon_size * 0.55))
                                    color "#FFFFFFAA"
                                    outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                        #Body Status
                        vbox:
                            xsize icon_size
                            xalign 0.0

                            $ bodyimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            $ bodytt = "No idea if she uses condoms for body play."
                            if girl.player_knows_body_condom:
                                if girl.wants_body_condom:
                                    $ bodyimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                    $ bodytt =  f"{{color=#ff0000}}Wants Condom for Body!{{/color}}"
                                else:
                                    $ bodyimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                    $ bodytt =  f"{{color={menu_text_color_valid}}}Likes the risk during Body!{{/color}}"
                                    #will need to figure out the body cum mechanic
                                    # if girl.oral_cum > 0:
                                        # $ cumtextfix = "unit"
                                        # if girl.oral_cum>1:
                                            # $ cumtextfix = "units"
                                        # $ bodyimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                        # $ bodytt =  f"{{color={menu_text_color_valid}}} Has {girl.oral_cum} of cum on her body!{{/color}}"
                            else:
                                $ bodytt = "No idea if she wants condom for Body."
                                $ bodyimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                            fixed:
                                xysize (icon_size, icon_size)
                                xalign 0.5
                                imagebutton:
                                    focus_mask True
                                    at Transform(zoom=(icon_size / 50.0))
                                    xalign 0.5
                                    yalign 0.5
                                    idle bodyimg
                                    action NullAction()
                                    tooltip bodytt
                                text "B":
                                    align (0.5, 0.5)
                                    size max(7, int(icon_size * 0.55))
                                    color "#FFFFFFAA"
                                    outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                        #Anal Status
                        vbox:
                            xsize icon_size
                            xalign 0.0

                            $ analimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            $ analtt = "No idea if she uses condoms for anal sex."
                            if girl.player_knows_anal_condom:
                                if girl.wants_anal_condom:
                                    $ analimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                    $ analtt =  f"{{color=#ff0000}}Wants Condom for Anal!{{/color}}"
                                else:
                                    $ analimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                    $ analtt =  f"{{color={menu_text_color_valid}}}Likes the risk during Anal!{{/color}}"
                                    if girl.anal_cum > 0:
                                        $ acumtextfix = "unit"
                                        if girl.anal_cum>1:
                                            $ acumtextfix = "units"
                                        $ analimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                        $ analtt =  f"{{color={menu_text_color_valid}}} Has {girl.anal_cum} {acumtextfix} of cum in her ass!{{/color}}"
                            else:
                                $ analtt = "No idea if she wants condom for Anal."
                                $ analimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                            fixed:
                                xysize (icon_size, icon_size)
                                xalign 0.5
                                imagebutton:
                                    focus_mask True
                                    at Transform(zoom=(icon_size / 50.0))
                                    xalign 0.5
                                    yalign 0.5
                                    idle analimg
                                    action NullAction()
                                    tooltip analtt
                                text "A":
                                    align (0.5, 0.5)
                                    size max(7, int(icon_size * 0.55))
                                    color "#FFFFFFAA"
                                    outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                        #Vaginal Status
                        vbox:
                            xsize icon_size
                            xalign 0.0

                            $ vaginalimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            $ vaginaltt = "No idea if she uses condoms for vaginal sex."
                            if girl.player_knows_vaginal_condom:
                                if girl.wants_vaginal_condom:
                                    $ vaginalimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                    $ vaginaltt =  f"{{color=#ff0000}}Wants Condom for Vaginal!{{/color}}"
                                else:
                                    $ vaginalimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                    $ vaginaltt =  f"{{color={menu_text_color_valid}}}Likes the risk during Vaginal!{{/color}}"
                                    if girl.vaginal_cum > 0:
                                        $ vcumtextfix = "unit"
                                        if girl.vaginal_cum>1:
                                            $ vcumtextfix = "units"
                                        $ vaginalimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                        $ vaginaltt =  f"{{color={menu_text_color_valid}}} Has {girl.vaginal_cum} {vcumtextfix} of cum in her womb!{{/color}}"
                            else:
                                $ vaginaltt = "No idea if she uses condoms for vaginal sex."
                                $ vaginalimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                            fixed:
                                xysize (icon_size, icon_size)
                                xalign 0.5
                                imagebutton:
                                    focus_mask True
                                    at Transform(zoom=(icon_size / 50.0))
                                    xalign 0.5
                                    yalign 0.5
                                    idle vaginalimg
                                    action NullAction()
                                    tooltip vaginaltt
                                text "V":
                                    align (0.5, 0.5)
                                    size max(7, int(icon_size * 0.55))
                                    color "#FFFFFFAA"
                                    outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                        vbox:
                            xsize icon_size
                            xalign 0.0

                            # FertiBOOST
                            if girl.fertility_boost >= 1:
                                $ days_rem_text = "days" if girl.fertility_boost > 1 else "day"
                                imagebutton:
                                    focus_mask True
                                    at Transform(zoom=(icon_size / 50.0))
                                    xalign 0.5
                                    yalign 0.5
                                    idle "_mods/content/elkrose_vt/extra_images/fertilitypills50.png"
                                    action NullAction()
                                    tooltip f"{{color={menu_text_color_valid}}}FertiBOOST Active! Good for {girl.fertility_boost} more {days_rem_text}!{{/color}}"

                        vbox:
                            xsize icon_size
                            xalign 0.0
                            # PregnaVITA
                            if girl.prenatal_boost >= 1:
                                imagebutton:
                                    focus_mask True
                                    at Transform(zoom=(icon_size / 50.0))
                                    xalign 0.5
                                    yalign 0.5
                                    idle "_mods/content/elkrose_vt/extra_images/pregboosters50.png"
                                    action NullAction()
                                    tooltip f"{{color={menu_text_color_valid}}}Has {girl.prenatal_boost} PregnaVITA{{/color}}"

screen cherry_window(girl=None, position="center", xoffset=0, yoffset=0, border_color="#FFFFFF", border_size=2, current_day=None):
    $ girl = girl 
    #or persistent.selected_girl
    #$ girl = girl

    
    # Determine positioning values directly
    $ xalign_val = 0.5
    $ yalign_val = 0.5
    $ xanchor_val = 0.5
    $ yanchor_val = 0.5
    
    if position == "bottom":
        $ yalign_val = 1.0
        $ yanchor_val = 1.0
        $ yoffset = -10
    elif position == "left":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ xoffset = 10
    elif position == "right":
        $ xalign_val = 1.0
        $ xanchor_val = 1.0
        $ xoffset = -10
    elif position == "top":
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
        $ yoffset = 10
    
    #Single frame with proper sizing and border
    frame:
        xalign xalign_val
        yalign yalign_val
        xanchor xanchor_val
        yanchor yanchor_val
        xoffset xoffset
        yoffset yoffset
        xsize 360
        #ysize 50
        padding (0, 0, 0, 0)
        
        # Border frame
        frame:
            xsize 360
            #ysize 50
            background Frame(
                "#00000000",  # Transparent base
                xborder=border_size,
                yborder=border_size,
                border=border_color
            )
            
            # Content frame - contains background and UI
            frame:
                xsize (360 - (border_size * 2))
                xalign 0.5
                yalign 0.0
                xanchor 0.5
                yanchor 0.0
                padding (5, 5, 5, 5)
                background Frame("_mods/content/elkrose_vt/extra_images/Cherry_Background.png", xborder=1, yborder=1, xzoom=0.199, yzoom=0.201)
                #background Frame("_mods/content/elkrose_vt/extra_images/Cherry_Background.png", xzoom=0.2, yzoom=0.2)
                
                vbox:
                    xsize (360 - (border_size * 2) - 4)
                    spacing 5
                    xalign 0.0  # Left-align content
                    yalign 0.0  # Top-align content
                    
                        #First Row
                    hbox:
                        spacing 5
                        ysize 50

                        # Cherry Status
                        vbox:
                            xsize 50
                            xalign 0.0
                            imagebutton:
                                idle "_mods/content/elkrose_vt/extra_images/HUDVT_idle.png"
                                hover "_mods/content/elkrose_vt/extra_images/HUDVT_hover.png"
                                action Function(renpy.show_screen, "vtmod_virgin_preg_ui", girl=girl)
                                tooltip f"{{color=#ff0000}}Cherry Info.{{/color}}"
                        
                        # Birth control status
                        vbox:
                            xsize 50
                            xalign 0.0
                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_token.png"
                            $ vt_tt_bc = "Unprotected"
                            
                            if girl.pregnant and girl.player_knows_pregnant:
                                $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/feeding_bottle.png"
                                $ vt_tt_bc = f"{{color={menu_text_color_valid}}}Pregnant!{{/color}}"
                            else:
                                if girl.bc_status_known:
                                    $ vt_tt_bc += f"\nFertility: [girl.effective_fertility():.1f]%\n{girl.get_fertility_day_status()}"
                                    if girl.birth_control:
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_token.png"
                                        $ vt_tt_bc = f"{{color={menu_text_color_valid}}}Birth Control Active{{/color}}"
                                        if girl.vaginal_cum >= 1:
                                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_cum.png"
                                            $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                    else:
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_token.png"
                                        $ vt_tt_bc = "Unprotected"
                                        if girl.vaginal_cum >= 1:
                                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_cum.png"
                                            $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                        if girl.is_highly_fertile() :
                                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_fertile_cum.png"
                                            $ vt_tt_bc += f"\n{{color=#ff0000}}She is ovulating and has a higher chance of getting pregnant.{{/color}}"
                                else:
                                    $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bcknown.png"
                                    $ vt_tt_bc = "No idea if she is on birth control."
                            imagebutton:
                                idle vt_img_bc
                                action NullAction()
                                tooltip vt_tt_bc
                                xalign 0.0
                                yalign 0.0

                        # Sex/Arousal Status
                        vbox:
                            xsize 50
                            xalign 0.0
                            
                            $ ss_tt_vag = f"{{color={menu_text_color_valid}}}Fresh and untouched, ready for action!{{/color}}"
                            $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/sexstatus.png"
                            
                            if girl.hymen:
                                $ ss_tt_vag = f"{{color={menu_text_color_valid}}}A pristine canvas, untouched and pure!{{/color}}"
                                $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/virginsymbol.png"
                            else:
                                if girl.had_sex_today:
                                    $ ss_tt_vag = f"{{color={menu_text_color_valid}}}Had sex today!{{/color}}"
                                    $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/hadsextoday.png"
                                else:
                                    $ ss_tt_vag += f"\nNo sex today, yet."
                                    $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/sexstatus.png"

                            imagebutton:
                                idle ss_img_vag
                                action NullAction()
                                tooltip ss_tt_vag

                        
                    # Item Status
                    hbox:
                        spacing 5
                        ysize 50
                        #Oral Status
                        vbox:
                            xsize 50
                            xalign 0.0
                            
                            $ oralimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            $ oraltt = "No idea if she uses condoms for oral sex."
                            if girl.player_knows_oral_condom:
                                if girl.wants_oral_condom:
                                    $ oralimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                    $ oraltt =  f"{{color=#ff0000}}Wants Condom for Oral!{{/color}}"
                                else:
                                    $ oralimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                    $ oraltt =  f"{{color={menu_text_color_valid}}}Likes the risk during Oral!{{/color}}"
                                    if girl.oral_cum > 0:
                                        $ cumtextfix = "unit"
                                        if girl.oral_cum>1:
                                            $ cumtextfix = "units"
                                        $ oralimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                        $ oraltt =  f"{{color={menu_text_color_valid}}} Has {girl.oral_cum} {cumtextfix} of cum in her belly!{{/color}}"
                            else:
                                $ oraltt = "No idea if she wants condom for Oral."
                                $ oralimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                            fixed:
                                xysize (50, 50)
                                xalign 0.5
                                imagebutton:
                                    xalign 0.5
                                    yalign 0.5
                                    idle oralimg
                                    action NullAction()
                                    tooltip oraltt
                                text "O":
                                    align (0.5, 0.5)
                                    size 27
                                    color "#FFFFFFAA"
                                    outlines [(3, "#000000AA", 0, 0)]
                       
                        #Body Status
                        vbox:
                            xsize 50
                            xalign 0.0
                            
                            $ bodyimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            $ bodytt = "No idea if she uses condoms for body play."
                            if girl.player_knows_body_condom:
                                if girl.wants_body_condom:
                                    $ bodyimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                    $ bodytt =  f"{{color=#ff0000}}Wants Condom for Body!{{/color}}"
                                else:
                                    $ bodyimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                    $ bodytt =  f"{{color={menu_text_color_valid}}}Likes the risk during Body!{{/color}}"
                                    #will need to figure out the body cum mechanic
                                    # if girl.oral_cum > 0:
                                        # $ cumtextfix = "unit"
                                        # if girl.oral_cum>1:
                                            # $ cumtextfix = "units"
                                        # $ bodyimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                        # $ bodytt =  f"{{color={menu_text_color_valid}}} Has {girl.oral_cum} of cum on her body!{{/color}}"
                            else:
                                $ bodytt = "No idea if she wants condom for Body."
                                $ bodyimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                            fixed:
                                xysize (50, 50)
                                xalign 0.5
                                imagebutton:
                                    xalign 0.5
                                    yalign 0.5
                                    idle bodyimg
                                    action NullAction()
                                    tooltip bodytt
                                text "B":
                                    align (0.5, 0.5)
                                    size 27
                                    color "#FFFFFFAA"
                                    outlines [(3, "#000000AA", 0, 0)]
                       
                        #Anal Status
                        vbox:
                            xsize 50
                            xalign 0.0
                            
                            $ analimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            $ analtt = "No idea if she uses condoms for anal sex."
                            if girl.player_knows_anal_condom:
                                if girl.wants_anal_condom:
                                    $ analimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                    $ analtt =  f"{{color=#ff0000}}Wants Condom for Anal!{{/color}}"
                                else:
                                    $ analimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                    $ analtt =  f"{{color={menu_text_color_valid}}}Likes the risk during Anal!{{/color}}"
                                    if girl.anal_cum > 0:
                                        $ acumtextfix = "unit"
                                        if girl.anal_cum>1:
                                            $ acumtextfix = "units"
                                        $ analimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                        $ analtt =  f"{{color={menu_text_color_valid}}} Has {girl.anal_cum} {acumtextfix} of cum in her ass!{{/color}}"
                            else:
                                $ analtt = "No idea if she wants condom for Anal."
                                $ analimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                            fixed:
                                xysize (50, 50)
                                xalign 0.5
                                imagebutton:
                                    xalign 0.5
                                    yalign 0.5
                                    idle analimg
                                    action NullAction()
                                    tooltip analtt
                                text "A":
                                    align (0.5, 0.5)
                                    size 27
                                    color "#FFFFFFAA"
                                    outlines [(3, "#000000AA", 0, 0)]
                        
                        #Vaginal Status
                        vbox:
                            xsize 50
                            xalign 0.0
                            
                            $ vaginalimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            $ vaginaltt = "No idea if she uses condoms for vaginal sex."
                            if girl.player_knows_vaginal_condom:
                                if girl.wants_vaginal_condom:
                                    $ vaginalimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                    $ vaginaltt =  f"{{color=#ff0000}}Wants Condom for Vaginal!{{/color}}"
                                else:
                                    $ vaginalimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                    $ vaginaltt =  f"{{color={menu_text_color_valid}}}Likes the risk during Vaginal!{{/color}}"
                                    if girl.vaginal_cum > 0:
                                        $ vcumtextfix = "unit"
                                        if girl.vaginal_cum>1:
                                            $ vcumtextfix = "units"
                                        $ vaginalimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                        $ vaginaltt =  f"{{color={menu_text_color_valid}}} Has {girl.vaginal_cum} {vcumtextfix} of cum in her womb!{{/color}}"
                            else:
                                $ vaginaltt = "No idea if she uses condoms for vaginal sex."
                                $ vaginalimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                            # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                            fixed:
                                xysize (50, 50)
                                xalign 0.5
                                imagebutton:
                                    xalign 0.5
                                    yalign 0.5
                                    idle vaginalimg
                                    action NullAction()
                                    tooltip vaginaltt
                                text "V":
                                    align (0.5, 0.5)
                                    size 27
                                    color "#FFFFFFAA"
                                    outlines [(3, "#000000AA", 0, 0)]
                        
                        vbox:
                            xsize 50
                            xalign 0.0
                            
                            # FertiBOOST
                            if girl.fertility_boost >= 1:
                                $ days_rem_text = "days" if girl.fertility_boost > 1 else "day"
                                imagebutton:
                                    xalign 0.5
                                    yalign 0.5
                                    idle "_mods/content/elkrose_vt/extra_images/fertilitypills50.png"
                                    action NullAction()
                                    tooltip f"{{color={menu_text_color_valid}}}FertiBOOST Active! Good for {girl.fertility_boost} more {days_rem_text}!{{/color}}"

                        vbox:
                            xsize 50
                            xalign 0.0                            
                            # PregnaVITA
                            if girl.prenatal_boost >= 1:
                                imagebutton:
                                    xalign 0.5
                                    yalign 0.5
                                    idle "_mods/content/elkrose_vt/extra_images/pregboosters50.png"
                                    action NullAction()
                                    tooltip f"{{color={menu_text_color_valid}}}Has {girl.prenatal_boost} PregnaVITA{{/color}}"

screen cherry_window_row(girl=None, position="center", xoffset=0, yoffset=0, border_color="#FFFFFF", border_size=2, current_day=None, icon_size=50):
    $ girl = girl

    # Determine positioning values directly
    $ xalign_val = 0.5
    $ yalign_val = 0.5
    $ xanchor_val = 0.5
    $ yanchor_val = 0.5

    if position == "bottom":
        $ yalign_val = 1.0
        $ yanchor_val = 1.0
        $ yoffset = -10
    elif position == "convo_menu":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ yanchor_val = 1.0
    elif position == "girl_review":
        $ xalign_val = 0.5
        $ xanchor_val = 0.0
        $ yalign_val = 0.5
        $ yanchor_val = 0.0
        $ xoffset = -460
        $ yoffset = -35
    elif position == "left":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ xoffset = 10
    elif position == "right":
        $ xalign_val = 1.0
        $ xanchor_val = 1.0
        $ xoffset = -10
    elif position == "sex_outro":
        $ xalign_val = 0.5
        $ xanchor_val = 0.5
        $ yalign_val = 0.5
        $ yanchor_val = 0.5
    elif position == "tooltip":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
    elif position == "top":
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
        $ yoffset = 9
        $ xoffset = 620
    elif position == "top_left":
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
        $ yoffset = 9
        $ xoffset = -490

    # 9 icons + 8 gaps (spacing 5) + content padding (5 each side) = symmetric box
    $ _frame_w = 9 * icon_size + 8 * 5 + 5 * 2 + border_size * 2

    #Single frame with proper sizing and border
    frame:
        xalign xalign_val
        yalign yalign_val
        xanchor xanchor_val
        yanchor yanchor_val
        xoffset xoffset
        yoffset yoffset
        xsize _frame_w
        padding (0, 0, 0, 0)

        # Border frame
        frame:
            xsize _frame_w
            background border_color
            padding (0, border_size, 0, border_size)

            # Content frame - contains background and UI
            frame:
                xsize (_frame_w - border_size * 2)
                xalign 0.5
                yalign 0.0
                xanchor 0.5
                yanchor 0.0
                padding (5, 5, 5, 5)
                background Frame("_mods/content/elkrose_vt/extra_images/Cherry_Background.png", xborder=1, yborder=1, xzoom=0.199, yzoom=0.201)

                hbox:
                    xsize (_frame_w - border_size * 2 - 5 * 2)
                    spacing 5
                    ysize icon_size
                    xalign 0.5
                    yalign 0.0

                    # Cherry Status
                    vbox:
                        xsize icon_size
                        xalign 0.0
                        imagebutton:
                            focus_mask True
                            idle fit_image_to_size("_mods/content/elkrose_vt/extra_images/HUDVT_idle.png", icon_size, icon_size)
                            hover fit_image_to_size("_mods/content/elkrose_vt/extra_images/HUDVT_hover.png", icon_size, icon_size)
                            action Function(renpy.show_screen, "vtmod_virgin_preg_ui", girl=girl)
                            tooltip f"{{color=#ff0000}}Cherry Info.{{/color}}"

                    # Birth control status
                    vbox:
                        xsize icon_size
                        xalign 0.0
                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_token.png"
                        $ vt_tt_bc = "Unprotected"

                        if girl.pregnant and girl.player_knows_pregnant:
                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/feeding_bottle.png"
                            $ vt_tt_bc = f"{{color={menu_text_color_valid}}}Pregnant!{{/color}}"
                        else:
                            if girl.bc_status_known:
                                $ vt_tt_bc += f"\nFertility: [girl.effective_fertility():.1f]%\n{girl.get_fertility_day_status()}"
                                if girl.birth_control:
                                    $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_token.png"
                                    $ vt_tt_bc = f"{{color={menu_text_color_valid}}}Birth Control Active{{/color}}"
                                    if girl.vaginal_cum >= 1:
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_cum.png"
                                        $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                else:
                                    $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_token.png"
                                    $ vt_tt_bc = "Unprotected"
                                    if girl.vaginal_cum >= 1:
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_cum.png"
                                        $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                    if girl.is_highly_fertile() :
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_fertile_cum.png"
                                        $ vt_tt_bc += f"\n{{color=#ff0000}}She is ovulating and has a higher chance of getting pregnant.{{/color}}"
                            else:
                                $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bcknown.png"
                                $ vt_tt_bc = "No idea if she is on birth control."
                        imagebutton:
                            focus_mask True
                            idle fit_image_to_size(vt_img_bc, icon_size, icon_size)
                            action NullAction()
                            tooltip vt_tt_bc
                            xalign 0.0
                            yalign 0.0

                    # Sex/Arousal Status
                    vbox:
                        xsize icon_size
                        xalign 0.0

                        $ ss_tt_vag = f"{{color={menu_text_color_valid}}}Fresh and untouched, ready for action!{{/color}}"
                        $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/sexstatus.png"

                        if girl.hymen:
                            $ ss_tt_vag = f"{{color={menu_text_color_valid}}}A pristine canvas, untouched and pure!{{/color}}"
                            $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/virginsymbol.png"
                        else:
                            if girl.had_sex_today:
                                $ ss_tt_vag = f"{{color={menu_text_color_valid}}}Had sex today!{{/color}}"
                                $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/hadsextoday.png"
                            else:
                                $ ss_tt_vag += f"\nNo sex today, yet."
                                $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/sexstatus.png"

                        imagebutton:
                            focus_mask True
                            idle fit_image_to_size(ss_img_vag, icon_size, icon_size)
                            action NullAction()
                            tooltip ss_tt_vag

                    #Oral Status
                    vbox:
                        xsize icon_size
                        xalign 0.0

                        $ oralimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        $ oraltt = "No idea if she uses condoms for oral sex."
                        if girl.player_knows_oral_condom:
                            if girl.wants_oral_condom:
                                $ oralimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                $ oraltt =  f"{{color=#ff0000}}Wants Condom for Oral!{{/color}}"
                            else:
                                $ oralimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                $ oraltt =  f"{{color={menu_text_color_valid}}}Likes the risk during Oral!{{/color}}"
                                if girl.oral_cum > 0:
                                    $ cumtextfix = "unit"
                                    if girl.oral_cum>1:
                                        $ cumtextfix = "units"
                                    $ oralimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                    $ oraltt =  f"{{color={menu_text_color_valid}}} Has {girl.oral_cum} {cumtextfix} of cum in her belly!{{/color}}"
                        else:
                            $ oraltt = "No idea if she wants condom for Oral."
                            $ oralimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                        fixed:
                            xysize (icon_size, icon_size)
                            xalign 0.5
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size(oralimg, icon_size, icon_size)
                                action NullAction()
                                tooltip oraltt
                            text "O":
                                align (0.5, 0.5)
                                size max(7, int(icon_size * 0.55))
                                color "#FFFFFFAA"
                                outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                    #Body Status
                    vbox:
                        xsize icon_size
                        xalign 0.0

                        $ bodyimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        $ bodytt = "No idea if she uses condoms for body play."
                        if girl.player_knows_body_condom:
                            if girl.wants_body_condom:
                                $ bodyimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                $ bodytt =  f"{{color=#ff0000}}Wants Condom for Body!{{/color}}"
                            else:
                                $ bodyimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                $ bodytt =  f"{{color={menu_text_color_valid}}}Likes the risk during Body!{{/color}}"
                                #will need to figure out the body cum mechanic
                                # if girl.oral_cum > 0:
                                    # $ cumtextfix = "unit"
                                    # if girl.oral_cum>1:
                                        # $ cumtextfix = "units"
                                    # $ bodyimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                    # $ bodytt =  f"{{color={menu_text_color_valid}}} Has {girl.oral_cum} of cum on her body!{{/color}}"
                        else:
                            $ bodytt = "No idea if she wants condom for Body."
                            $ bodyimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                        fixed:
                            xysize (icon_size, icon_size)
                            xalign 0.5
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size(bodyimg, icon_size, icon_size)
                                action NullAction()
                                tooltip bodytt
                            text "B":
                                align (0.5, 0.5)
                                size max(7, int(icon_size * 0.55))
                                color "#FFFFFFAA"
                                outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                    #Anal Status
                    vbox:
                        xsize icon_size
                        xalign 0.0

                        $ analimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        $ analtt = "No idea if she uses condoms for anal sex."
                        if girl.player_knows_anal_condom:
                            if girl.wants_anal_condom:
                                $ analimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                $ analtt =  f"{{color=#ff0000}}Wants Condom for Anal!{{/color}}"
                            else:
                                $ analimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                $ analtt =  f"{{color={menu_text_color_valid}}}Likes the risk during Anal!{{/color}}"
                                if girl.anal_cum > 0:
                                    $ acumtextfix = "unit"
                                    if girl.anal_cum>1:
                                        $ acumtextfix = "units"
                                    $ analimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                    $ analtt =  f"{{color={menu_text_color_valid}}} Has {girl.anal_cum} {acumtextfix} of cum in her ass!{{/color}}"
                        else:
                            $ analtt = "No idea if she wants condom for Anal."
                            $ analimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                        fixed:
                            xysize (icon_size, icon_size)
                            xalign 0.5
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size(analimg, icon_size, icon_size)
                                action NullAction()
                                tooltip analtt
                            text "A":
                                align (0.5, 0.5)
                                size max(7, int(icon_size * 0.55))
                                color "#FFFFFFAA"
                                outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                    #Vaginal Status
                    vbox:
                        xsize icon_size
                        xalign 0.0

                        $ vaginalimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        $ vaginaltt = "No idea if she uses condoms for vaginal sex."
                        if girl.player_knows_vaginal_condom:
                            if girl.wants_vaginal_condom:
                                $ vaginalimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                $ vaginaltt =  f"{{color=#ff0000}}Wants Condom for Vaginal!{{/color}}"
                            else:
                                $ vaginalimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                $ vaginaltt =  f"{{color={menu_text_color_valid}}}Likes the risk during Vaginal!{{/color}}"
                                if girl.vaginal_cum > 0:
                                    $ vcumtextfix = "unit"
                                    if girl.vaginal_cum>1:
                                        $ vcumtextfix = "units"
                                    $ vaginalimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                    $ vaginaltt =  f"{{color={menu_text_color_valid}}} Has {girl.vaginal_cum} {vcumtextfix} of cum in her womb!{{/color}}"
                        else:
                            $ vaginaltt = "No idea if she uses condoms for vaginal sex."
                            $ vaginalimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                        fixed:
                            xysize (icon_size, icon_size)
                            xalign 0.5
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size(vaginalimg, icon_size, icon_size)
                                action NullAction()
                                tooltip vaginaltt
                            text "V":
                                align (0.5, 0.5)
                                size max(7, int(icon_size * 0.55))
                                color "#FFFFFFAA"
                                outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                    vbox:
                        xsize icon_size
                        xalign 0.0

                        # FertiBOOST
                        if girl.fertility_boost >= 1:
                            $ days_rem_text = "days" if girl.fertility_boost > 1 else "day"
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size("_mods/content/elkrose_vt/extra_images/fertilitypills50.png", icon_size, icon_size)
                                action NullAction()
                                tooltip f"{{color={menu_text_color_valid}}}FertiBOOST Active! Good for {girl.fertility_boost} more {days_rem_text}!{{/color}}"

                    vbox:
                        xsize icon_size
                        xalign 0.0
                        # PregnaVITA
                        if girl.prenatal_boost >= 1:
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size("_mods/content/elkrose_vt/extra_images/pregboosters50.png", icon_size, icon_size)
                                action NullAction()
                                tooltip f"{{color={menu_text_color_valid}}}Has {girl.prenatal_boost} PregnaVITA{{/color}}"

screen cherry_window_column(girl=None, position="center", xoffset=0, yoffset=0, border_color="#FFFFFF", border_size=2, current_day=None, icon_size=50):
    $ girl = girl

    # Determine positioning values directly
    $ xalign_val = 0.5
    $ yalign_val = 0.5
    $ xanchor_val = 0.5
    $ yanchor_val = 0.5

    if position == "bottom":
        $ yalign_val = 1.0
        $ yanchor_val = 1.0
        $ yoffset = -10
    elif position == "exam_outro":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
    elif position == "left":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ xoffset = 10
    elif position == "right":
        $ xalign_val = 1.0
        $ xanchor_val = 1.0
        $ xoffset = -10
    elif position == "call_menu":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
    elif position == "top":
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
        $ yoffset = 9

    # 9 icons + 8 gaps (spacing 5) + content padding (5 each side) = symmetric box
    $ _frame_h = 9 * icon_size + 8 * 5 + 5 * 2 + border_size * 2
    $ _frame_w = icon_size + 5 * 2 + border_size * 2

    #Single frame with proper sizing and border
    frame:
        xalign xalign_val
        yalign yalign_val
        xanchor xanchor_val
        yanchor yanchor_val
        xoffset xoffset
        yoffset yoffset
        ysize _frame_h
        xsize _frame_w
        padding (0, 0, 0, 0)

        # Border frame - all sides
        frame:
            ysize _frame_h
            xsize _frame_w
            background border_color
            padding (border_size, border_size, border_size, border_size)

            # Content frame - contains background and UI
            frame:
                ysize (_frame_h - border_size * 2)
                xsize (_frame_w - border_size * 2)
                xalign 0.0
                yalign 0.0
                padding (5, 5, 5, 5)
                background Frame("_mods/content/elkrose_vt/extra_images/Cherry_Background.png", xborder=1, yborder=1, xzoom=0.199, yzoom=0.201)

                vbox:
                    ysize (_frame_h - border_size * 2 - 5 * 2)
                    spacing 5
                    xsize icon_size
                    xalign 0.5
                    yalign 0.5

                    # Cherry Status
                    hbox:
                        ysize icon_size
                        yalign 0.0
                        imagebutton:
                            focus_mask True
                            idle fit_image_to_size("_mods/content/elkrose_vt/extra_images/HUDVT_idle.png", icon_size, icon_size)
                            hover fit_image_to_size("_mods/content/elkrose_vt/extra_images/HUDVT_hover.png", icon_size, icon_size)
                            action Function(renpy.show_screen, "vtmod_virgin_preg_ui", girl=girl)
                            tooltip f"{{color=#ff0000}}Cherry Info.{{/color}}"

                    # Birth control status
                    hbox:
                        ysize icon_size
                        yalign 0.0
                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_token.png"
                        $ vt_tt_bc = "Unprotected"

                        if girl.pregnant and girl.player_knows_pregnant:
                            $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/feeding_bottle.png"
                            $ vt_tt_bc = f"{{color={menu_text_color_valid}}}Pregnant!{{/color}}"
                        else:
                            if girl.bc_status_known:
                                $ vt_tt_bc += f"\nFertility: [girl.effective_fertility():.1f]%\n{girl.get_fertility_day_status()}"
                                if girl.birth_control:
                                    $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_token.png"
                                    $ vt_tt_bc = f"{{color={menu_text_color_valid}}}Birth Control Active{{/color}}"
                                    if girl.vaginal_cum >= 1:
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bc_cum.png"
                                        $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                else:
                                    $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_token.png"
                                    $ vt_tt_bc = "Unprotected"
                                    if girl.vaginal_cum >= 1:
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_cum.png"
                                        $ vt_tt_bc += f"{{color=#ff5555}} Cum inside: {girl.vaginal_cum}{{/color}}"
                                    if girl.is_highly_fertile() :
                                        $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/nobc_fertile_cum.png"
                                        $ vt_tt_bc += f"\n{{color=#ff0000}}She is ovulating and has a higher chance of getting pregnant.{{/color}}"
                            else:
                                $ vt_img_bc = "_mods/content/elkrose_vt/extra_images/bcknown.png"
                                $ vt_tt_bc = "No idea if she is on birth control."
                        imagebutton:
                            focus_mask True
                            idle fit_image_to_size(vt_img_bc, icon_size, icon_size)
                            action NullAction()
                            tooltip vt_tt_bc
                            xalign 0.0
                            yalign 0.0

                    # Sex/Arousal Status
                    hbox:
                        ysize icon_size
                        yalign 0.0

                        $ ss_tt_vag = f"{{color={menu_text_color_valid}}}Fresh and untouched, ready for action!{{/color}}"
                        $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/sexstatus.png"

                        if girl.hymen:
                            $ ss_tt_vag = f"{{color={menu_text_color_valid}}}A pristine canvas, untouched and pure!{{/color}}"
                            $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/virginsymbol.png"
                        else:
                            if girl.had_sex_today:
                                $ ss_tt_vag = f"{{color={menu_text_color_valid}}}Had sex today!{{/color}}"
                                $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/hadsextoday.png"
                            else:
                                $ ss_tt_vag += f"\nNo sex today, yet."
                                $ ss_img_vag = "_mods/content/elkrose_vt/extra_images/sexstatus.png"

                        imagebutton:
                            focus_mask True
                            idle fit_image_to_size(ss_img_vag, icon_size, icon_size)
                            action NullAction()
                            tooltip ss_tt_vag

                    #Oral Status
                    hbox:
                        ysize icon_size
                        yalign 0.0

                        $ oralimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        $ oraltt = "No idea if she uses condoms for oral sex."
                        if girl.player_knows_oral_condom:
                            if girl.wants_oral_condom:
                                $ oralimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                $ oraltt =  f"{{color=#ff0000}}Wants Condom for Oral!{{/color}}"
                            else:
                                $ oralimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                $ oraltt =  f"{{color={menu_text_color_valid}}}Likes the risk during Oral!{{/color}}"
                                if girl.oral_cum > 0:
                                    $ cumtextfix = "unit"
                                    if girl.oral_cum>1:
                                        $ cumtextfix = "units"
                                    $ oralimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                    $ oraltt =  f"{{color={menu_text_color_valid}}} Has {girl.oral_cum} {cumtextfix} of cum in her belly!{{/color}}"
                        else:
                            $ oraltt = "No idea if she wants condom for Oral."
                            $ oralimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                        fixed:
                            xysize (icon_size, icon_size)
                            xalign 0.5
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size(oralimg, icon_size, icon_size)
                                action NullAction()
                                tooltip oraltt
                            text "O":
                                align (0.5, 0.5)
                                size max(7, int(icon_size * 0.55))
                                color "#FFFFFFAA"
                                outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                    #Body Status
                    hbox:
                        ysize icon_size
                        yalign 0.0

                        $ bodyimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        $ bodytt = "No idea if she uses condoms for body play."
                        if girl.player_knows_body_condom:
                            if girl.wants_body_condom:
                                $ bodyimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                $ bodytt =  f"{{color=#ff0000}}Wants Condom for Body!{{/color}}"
                            else:
                                $ bodyimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                $ bodytt =  f"{{color={menu_text_color_valid}}}Likes the risk during Body!{{/color}}"
                                #will need to figure out the body cum mechanic
                                # if girl.oral_cum > 0:
                                    # $ cumtextfix = "unit"
                                    # if girl.oral_cum>1:
                                        # $ cumtextfix = "units"
                                    # $ bodyimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                    # $ bodytt =  f"{{color={menu_text_color_valid}}} Has {girl.oral_cum} of cum on her body!{{/color}}"
                        else:
                            $ bodytt = "No idea if she wants condom for Body."
                            $ bodyimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                        fixed:
                            xysize (icon_size, icon_size)
                            xalign 0.5
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size(bodyimg, icon_size, icon_size)
                                action NullAction()
                                tooltip bodytt
                            text "B":
                                align (0.5, 0.5)
                                size max(7, int(icon_size * 0.55))
                                color "#FFFFFFAA"
                                outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                    #Anal Status
                    hbox:
                        ysize icon_size
                        yalign 0.0

                        $ analimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        $ analtt = "No idea if she uses condoms for anal sex."
                        if girl.player_knows_anal_condom:
                            if girl.wants_anal_condom:
                                $ analimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                $ analtt =  f"{{color=#ff0000}}Wants Condom for Anal!{{/color}}"
                            else:
                                $ analimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                $ analtt =  f"{{color={menu_text_color_valid}}}Likes the risk during Anal!{{/color}}"
                                if girl.anal_cum > 0:
                                    $ acumtextfix = "unit"
                                    if girl.anal_cum>1:
                                        $ acumtextfix = "units"
                                    $ analimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                    $ analtt =  f"{{color={menu_text_color_valid}}} Has {girl.anal_cum} {acumtextfix} of cum in her ass!{{/color}}"
                        else:
                            $ analtt = "No idea if she wants condom for Anal."
                            $ analimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                        fixed:
                            xysize (icon_size, icon_size)
                            xalign 0.5
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size(analimg, icon_size, icon_size)
                                action NullAction()
                                tooltip analtt
                            text "A":
                                align (0.5, 0.5)
                                size max(7, int(icon_size * 0.55))
                                color "#FFFFFFAA"
                                outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                    #Vaginal Status
                    hbox:
                        ysize icon_size
                        yalign 0.0

                        $ vaginalimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        $ vaginaltt = "No idea if she uses condoms for vaginal sex."
                        if girl.player_knows_vaginal_condom:
                            if girl.wants_vaginal_condom:
                                $ vaginalimg = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                                $ vaginaltt =  f"{{color=#ff0000}}Wants Condom for Vaginal!{{/color}}"
                            else:
                                $ vaginalimg = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                                $ vaginaltt =  f"{{color={menu_text_color_valid}}}Likes the risk during Vaginal!{{/color}}"
                                if girl.vaginal_cum > 0:
                                    $ vcumtextfix = "unit"
                                    if girl.vaginal_cum>1:
                                        $ vcumtextfix = "units"
                                    $ vaginalimg = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                                    $ vaginaltt =  f"{{color={menu_text_color_valid}}} Has {girl.vaginal_cum} {vcumtextfix} of cum in her womb!{{/color}}"
                        else:
                            $ vaginaltt = "No idea if she uses condoms for vaginal sex."
                            $ vaginalimg = "_mods/content/elkrose_vt/extra_images/nocondom.png"
                        # PROTOTYPE: single-letter slot label (O/B/A/V) drawn over the icon
                        fixed:
                            xysize (icon_size, icon_size)
                            xalign 0.5
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size(vaginalimg, icon_size, icon_size)
                                action NullAction()
                                tooltip vaginaltt
                            text "V":
                                align (0.5, 0.5)
                                size max(7, int(icon_size * 0.55))
                                color "#FFFFFFAA"
                                outlines [(max(1, icon_size // 14), "#000000AA", 0, 0)]

                    hbox:
                        ysize icon_size
                        yalign 0.0

                        # FertiBOOST
                        if girl.fertility_boost >= 1:
                            $ days_rem_text = "days" if girl.fertility_boost > 1 else "day"
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size("_mods/content/elkrose_vt/extra_images/fertilitypills50.png", icon_size, icon_size)
                                action NullAction()
                                tooltip f"{{color={menu_text_color_valid}}}FertiBOOST Active! Good for {girl.fertility_boost} more {days_rem_text}!{{/color}}"

                    hbox:
                        ysize icon_size
                        yalign 0.0
                        # PregnaVITA
                        if girl.prenatal_boost >= 1:
                            imagebutton:
                                focus_mask True
                                xalign 0.5
                                yalign 0.5
                                idle fit_image_to_size("_mods/content/elkrose_vt/extra_images/pregboosters50.png", icon_size, icon_size)
                                action NullAction()
                                tooltip f"{{color={menu_text_color_valid}}}Has {girl.prenatal_boost} PregnaVITA{{/color}}"

screen condom_cherry(position="center", xoffset=0, yoffset=0):
    # Determine positioning values directly
    $ xalign_val = 0.5
    $ yalign_val = 0.5
    $ xanchor_val = 0.5
    $ yanchor_val = 0.5
    $ xsize_val = 100
    $ ysize_val = 50
    
    if position == "bottom":
        $ yalign_val = 1.0
        $ yanchor_val = 1.0
        $ yoffset = -10
    elif position == "left":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ xoffset = 10
    elif position == "player_hud":
        $ xsize_val = 50
        $ ysize_val = 100
    elif position == "right":
        $ xalign_val = 1.0
        $ xanchor_val = 1.0
        $ xoffset = -10
    elif position == "top":
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
        $ yoffset = 20
        $ xoffset = -275
    elif position == "top_left":
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
        $ yoffset = 20
        $ xoffset = -475
    elif position == "top_right":
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
        $ yoffset = 20
        $ xoffset = 360
    
    #Single frame with proper sizing and border
    frame:
        xalign xalign_val
        yalign yalign_val
        xanchor xanchor_val
        yanchor yanchor_val
        xoffset xoffset
        yoffset yoffset
        xsize 100
        #ysize 50
        padding (0, 0, 0, 0)
        background None
        
        #First Row
        hbox:
            spacing 5
            ysize 50

            # Cherry Condom Status - SINGLE IMAGEBUTTON IMPLEMENTATION
            vbox:
                xsize 50
                xalign 0.0
                
                # DETERMINE CURRENT STATE AND SET VARIABLES
                $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                $ condom_tooltip = "{color=#ff0000}No condoms available!{/color}"

                # STATE 7: Premium creampie with broke condom (cum + broke)
                if player.condom_active == "premium" and player.condom_dirty and player.condom_broke:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumbrokepremiumcondom50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#FF0000}}UltraProtect: BROKE & CREAMPIED! Remaining: {player.condom_premium_count}{{/color}}"

                # STATE 6: Premium condom broke (but no creampie)
                elif player.condom_active == "premium" and player.condom_broke and not player.condom_dirty:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/condom_premium50broke.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = f"{{color=#FFA500}}UltraProtect: Condom broke during sex! Remaining: {player.condom_premium_count}{{/color}}"

                # STATE 5: Premium creampie (cum in condom)
                elif player.condom_active == "premium" and player.condom_dirty and not player.condom_broke:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumcondom_premium50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#00FF00}}UltraProtect: You shot your load! Remaining: {player.condom_premium_count}{{/color}}"

                # STATE 4: Cheap creampie with broke condom (cum + broke)
                elif player.condom_active == "cheap" and player.condom_dirty and player.condom_broke:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumbrokecondom50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#FF0000}}BasicShield: BROKE & CREAMPIED! Remaining: {player.condom_cheap_count}{{/color}}"

                # STATE 3: Cheap condom broke (but no creampie)
                elif player.condom_active == "cheap" and player.condom_broke and not player.condom_dirty:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/condom50broke.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = f"{{color=#FFA500}}BasicShield: Condom broke during sex! Remaining: {player.condom_cheap_count}{{/color}}"

                # STATE 2: Cheap creampie (cum in condom)
                elif player.condom_active == "cheap" and player.condom_dirty and not player.condom_broke:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumincondom50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#00FF00}}BasicShield: You shot your load! Remaining: {player.condom_cheap_count}{{/color}}"

                # STATE 1: Raw creampie (cum cherries)
                elif player.condom_active == "raw" and player.condom_dirty:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = "{color=#ff0000}You blasted raw! Click to clean or put on protection.{/color}"

                # STATE 9: Just wearing premium condom (no creampie)
                elif player.condom_active == "premium":
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = f"{{color=#00FF00}}UltraProtect: Sensation + safety! Remaining: {player.condom_premium_count}{{/color}}"

                # STATE 8: Just wearing cheap condom (no creampie)
                elif player.condom_active == "cheap":
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/condom50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = f"{{color=#00FF00}}BasicShield: Protection active! Remaining: {player.condom_cheap_count}{{/color}}"

                # STATE 10: Raw with condoms available
                elif player.condom_active == "raw" and (player.condom_premium_count > 0 or player.condom_cheap_count > 0):
                    $ condom_total = player.condom_premium_count + player.condom_cheap_count
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#ff0000}}You are all natural! Condoms Remaining: {condom_total}{{/color}}"

                # FINAL IMAGEBUTTON - SINGLE DEFINITION
                imagebutton:
                    focus_mask True
                    yalign 0.5
                    idle condom_idle_img
                    hover condom_hover_img
                    action Function(renpy.show_screen, "vt_select_condom")
                    tooltip condom_tooltip

            #Viagra Effects
            vbox:
                xsize 50
                xalign 0.0

                if "Viagra" in player.temporary_stat_changes:
                    imagebutton:
                        focus_mask True
                        yalign 0.5
                        idle "_mods/content/elkrose_vt/extra_images/viagra.webp"
                        action NullAction()
                        tooltip f"{{color={menu_text_color_valid}}} Viagra Active!{{/color}}"

screen hud_condom_cherry(position="center", xoffset=0, yoffset=0, icon_size=50):
    # Determine positioning values directly
    $ xalign_val = 0.5
    $ yalign_val = 0.5
    $ xanchor_val = 0.5
    $ yanchor_val = 0.5
    $ xsize_val = 100
    $ ysize_val = 50
    
    if position == "bottom":
        $ yalign_val = 1.0
        $ yanchor_val = 1.0
        $ yoffset = -10
    elif position == "left":
        $ xalign_val = 0.0
        $ xanchor_val = 0.0
        $ xoffset = 10
    elif position == "right":
        $ xalign_val = 1.0
        $ xanchor_val = 1.0
        $ xoffset = -10
    elif position == "top_right":
        $ xalign_val = 1.0
        $ xanchor_val = 1.0
        $ yalign_val = 0.0
        $ yanchor_val = 0.0
        $ xoffset = -10
        $ yoffset = 10

    #Single frame with proper sizing and border
    frame:
        xalign xalign_val
        yalign yalign_val
        xanchor xanchor_val
        yanchor yanchor_val
        xoffset xoffset
        yoffset yoffset
        xsize icon_size
        #ysize 50
        padding (0, 0, 0, 0)
        background None

        #First Row
        vbox:
            spacing 5

            # Cherry Condom Status - SINGLE IMAGEBUTTON IMPLEMENTATION
            hbox:
                xsize icon_size
                xalign 0.0
                
                # DETERMINE CURRENT STATE AND SET VARIABLES
                $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                $ condom_tooltip = "{color=#ff0000}No condoms available!{/color}"

                # STATE 7: Premium creampie with broke condom (cum + broke)
                if player.condom_active == "premium" and player.condom_dirty and player.condom_broke:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumbrokepremiumcondom50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#FF0000}}UltraProtect: BROKE & CREAMPIED! Remaining: {player.condom_premium_count}{{/color}}"

                # STATE 6: Premium condom broke (but no creampie)
                elif player.condom_active == "premium" and player.condom_broke and not player.condom_dirty:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/condom_premium50broke.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = f"{{color=#FFA500}}UltraProtect: Condom broke during sex! Remaining: {player.condom_premium_count}{{/color}}"

                # STATE 5: Premium creampie (cum in condom)
                elif player.condom_active == "premium" and player.condom_dirty and not player.condom_broke:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumcondom_premium50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#00FF00}}UltraProtect: You shot your load! Remaining: {player.condom_premium_count}{{/color}}"

                # STATE 4: Cheap creampie with broke condom (cum + broke)
                elif player.condom_active == "cheap" and player.condom_dirty and player.condom_broke:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumbrokecondom50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#FF0000}}BasicShield: BROKE & CREAMPIED! Remaining: {player.condom_cheap_count}{{/color}}"

                # STATE 3: Cheap condom broke (but no creampie)
                elif player.condom_active == "cheap" and player.condom_broke and not player.condom_dirty:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/condom50broke.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = f"{{color=#FFA500}}BasicShield: Condom broke during sex! Remaining: {player.condom_cheap_count}{{/color}}"

                # STATE 2: Cheap creampie (cum in condom)
                elif player.condom_active == "cheap" and player.condom_dirty and not player.condom_broke:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumincondom50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#00FF00}}BasicShield: You shot your load! Remaining: {player.condom_cheap_count}{{/color}}"

                # STATE 1: Raw creampie (cum cherries)
                elif player.condom_active == "raw" and player.condom_dirty:
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = "{color=#ff0000}You blasted raw! Click to clean or put on protection.{/color}"

                # STATE 9: Just wearing premium condom (no creampie)
                elif player.condom_active == "premium":
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/condom_premium50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = f"{{color=#00FF00}}UltraProtect: Sensation + safety! Remaining: {player.condom_premium_count}{{/color}}"

                # STATE 8: Just wearing cheap condom (no creampie)
                elif player.condom_active == "cheap":
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/condom50.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_tooltip = f"{{color=#00FF00}}BasicShield: Protection active! Remaining: {player.condom_cheap_count}{{/color}}"

                # STATE 10: Raw with condoms available
                elif player.condom_active == "raw" and (player.condom_premium_count > 0 or player.condom_cheap_count > 0):
                    $ condom_total = player.condom_premium_count + player.condom_cheap_count
                    $ condom_idle_img = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
                    $ condom_hover_img = "_mods/content/elkrose_vt/extra_images/cumcherries_idle.png"
                    $ condom_tooltip = f"{{color=#ff0000}}You are all natural! Condoms Remaining: {condom_total}{{/color}}"

                # FINAL IMAGEBUTTON - SINGLE DEFINITION
                imagebutton:
                    focus_mask True
                    at Transform(zoom=(icon_size / 50.0))
                    yalign 0.5
                    idle condom_idle_img
                    hover condom_hover_img
                    action Function(renpy.show_screen, "vt_select_condom")
                    tooltip condom_tooltip

            #Viagra Effects
            hbox:
                xsize icon_size
                xalign 0.0

                if "Viagra" in player.temporary_stat_changes:
                    imagebutton:
                        focus_mask True
                        at Transform(zoom=(icon_size / 50.0))
                        yalign 0.5
                        idle "_mods/content/elkrose_vt/extra_images/viagra.webp"
                        action NullAction()
                        tooltip f"{{color={menu_text_color_valid}}} Viagra Active!{{/color}}"

init 10:
    screen pmsCycleBar(char):
        zorder 100
        default barSize = (200, 15)

        python:
            if char is None:
                day_diff = "N/A"
                thumb_value = 0
                menstrual_val = follicular_val = ovulation_val = luteal_val = 0
                # Default to a neutral icon if no character
                current_phase_icon = "_mods/content/elkrose_vt/extra_images/bar/luteal_phase.png"
            else:
                ideal_day = char.ideal_fertile_day
                day_diff = char.days_from_ideal_fertility(with_direction=True)
                
                vt_current_day = 0
                try:
                    vt_current_day = time_manager.total_days
                except NameError:
                    # This should not happen if game_init.rpy is loaded correctly
                    renpy.log("screen pmsCycleBar ERROR: Global 'time_manager' variable not found!")
                    vt_current_day = 1 # Set a safe default value
                
                thumb_value = vt_current_day % 30
                if thumb_value == 0:
                    thumb_value = 30

                # --- DURATION OF EACH PHASE (these are fixed) ---
                menstrual_duration = 5
                follicular_duration = 7
                ovulation_duration = 4
                luteal_duration = 14

                # --- CALCULATE THE START DAY OF THE CYCLE ---
                ov_start_day = (ideal_day - 3 + 30) % 30
                cycle_start_day = (ov_start_day - follicular_duration - menstrual_duration + 30) % 30
                
                # --- CALCULATE CUMULATIVE VALUES FOR THE LAYERED BARS ---
                menstrual_val = menstrual_duration
                follicular_val = menstrual_duration + follicular_duration
                ovulation_val = menstrual_duration + follicular_duration + ovulation_duration
                luteal_val = 30 # The total

                # --- CALCULATE THE THUMB'S POSITION ON THE 0-30 RANGE ---
                current_day = vt_current_day % 30
                if current_day == 0: current_day = 30
                days_from_cycle_start = (current_day - cycle_start_day + 30) % 30
                if days_from_cycle_start == 0: days_from_cycle_start = 30

                # --- FIX: SET ICON BASED ON THE THUMB'S POSITION ON THE BAR ---
                if 1 <= days_from_cycle_start <= menstrual_val:
                    current_phase_icon = "_mods/content/elkrose_vt/extra_images/bar/menstrual_phase.png"
                elif menstrual_val < days_from_cycle_start <= follicular_val:
                    current_phase_icon = "_mods/content/elkrose_vt/extra_images/bar/follicular_phase.png"
                elif follicular_val < days_from_cycle_start <= ovulation_val:
                    current_phase_icon = "_mods/content/elkrose_vt/extra_images/bar/fertile_phase.png"
                else: # It must be in the luteal phase
                    current_phase_icon = "_mods/content/elkrose_vt/extra_images/bar/luteal_phase.png"

        frame:
            #xalign 0.5
            xsize 300
            xpadding 10
            ypadding 0
            background Frame("_mods/content/elkrose_vt/extra_images/bar/frame_ch.png", Borders(5, 5, 5, 5), tile=True)

            vbox:
                xsize 290
                xalign 0.5
                spacing 10
                #xsize 220 spacing 10
                null height 10

                if char is not None:
                    text _(u"Pregnancy Chance: ") + f"{char.pregnancy_chance():.1f}%" size 14 xalign 0.5
                else:
                    text _(u"Pregnancy Chance: N/A") size 14 xalign 0.5

                # --- LAYERED BARS WITH CORRECT VALUES ---
                fixed:
                    xysize barSize
                    xalign 0.5
                    #xmaximum 200 xminimum 200 ymaximum 15 yminimum 15 xpos 0.5 xalign 0.5

                    bar:
                        value luteal_val
                        range 30
                        left_bar "_mods/content/elkrose_vt/extra_images/bar/luteal_bar.webp"
                        right_bar "_mods/content/elkrose_vt/extra_images/bar/invisible.png"
                        xysize barSize

                    bar:
                        value ovulation_val
                        range 30
                        left_bar "_mods/content/elkrose_vt/extra_images/bar/fertile_bar.webp"
                        right_bar "_mods/content/elkrose_vt/extra_images/bar/invisible.png"
                        xysize barSize

                    bar:
                        value follicular_val
                        range 30
                        left_bar "_mods/content/elkrose_vt/extra_images/bar/follicular_bar.webp"
                        right_bar "_mods/content/elkrose_vt/extra_images/bar/invisible.png"
                        xysize barSize

                    bar:
                        value menstrual_val
                        range 30
                        left_bar "_mods/content/elkrose_vt/extra_images/bar/menstrual_bar.webp"
                        right_bar "_mods/content/elkrose_vt/extra_images/bar/invisible.png"
                        xysize barSize

                    # --- THUMB BAR WITH CORRECT VALUE ---
                    bar:
                        value days_from_cycle_start
                        range 30
                        left_bar "_mods/content/elkrose_vt/extra_images/bar/invisible.png"
                        right_bar "_mods/content/elkrose_vt/extra_images/bar/invisible.png"
                        thumb "_mods/content/elkrose_vt/extra_images/bar/bar_thumb15w.png"
                        xysize barSize

                # --- LEGENDS ---
                hbox:
                    xoffset 10
                    spacing 4
                    add "_mods/content/elkrose_vt/extra_images/bar/menstrual_bar.webp" xysize (15, 15)
                    text _(u"Menstrual Phase") size 14

                hbox:
                    xoffset 10
                    spacing 4
                    add "_mods/content/elkrose_vt/extra_images/bar/follicular_bar.webp" xysize (15, 15)
                    text _(u"Follicular Phase") size 14

                hbox:
                    xoffset 10
                    spacing 4
                    add "_mods/content/elkrose_vt/extra_images/bar/fertile_bar.webp" xysize (15, 15)
                    text _(u"Ovulation Phase") size 14

                hbox:
                    xoffset 10
                    spacing 4
                    add "_mods/content/elkrose_vt/extra_images/bar/luteal_bar.webp" xysize (15, 15)
                    text _(u"Luteal Phase") size 14

                add current_phase_icon:
                    xalign 0.5
                
                null height 2
