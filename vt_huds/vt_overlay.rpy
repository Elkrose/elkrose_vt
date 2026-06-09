## VT overlay - floats cherry widgets over base game screens without overriding them

init python:
    config.overlay_screens.append("vt_cherry_overlay")

transform vt_appear_after_popup:
    alpha 0.0
    pause 0.5
    alpha 1.0

screen vt_cherry_overlay():
    zorder 50
    modal False

    $ _vt_girl    = getattr(store, "selected_girl", None)
    $ _vt_part    = getattr(store, "participant", None)
    $ _vt_tooltip = GetTooltip()

    # Girl quick overview popup - takes priority so it replaces any exam/sex cherry
    if renpy.get_screen("girl_quick_overview"):
        $ _vt_qo = renpy.get_screen("girl_quick_overview")
        $ _vt_qo_girl = _vt_qo.scope.get("girl") if _vt_qo else None
        if _vt_qo_girl:
            # Absolute positions — tuned per layout variant (Events frame changes popup geometry)
            if _vt_qo_girl.events:
                $ _vt_qo_yoffset = 450
            else:
                $ _vt_qo_yoffset = 480

            fixed at vt_appear_after_popup:
                use cherry_window_row(girl=_vt_qo_girl, position="tooltip", xoffset=343, yoffset=_vt_qo_yoffset, border_color="#FF0000", border_size=2, icon_size=36) id "vt_qo_cherry"

    # Exam classroom
    elif renpy.get_screen("exam_menu", layer="master"):
        use condom_cherry(position="top") id "vt_ec_condom"

    elif renpy.get_screen("exam_actions_menu", layer="master"):
        if _vt_girl:
            use condom_cherry(position="top") id "vt_ea_condom"
            use cherry_window_row(girl=_vt_girl, position="top", yoffset=100, border_color="#FF0000", border_size=2, icon_size=36) id "vt_ea_cherry"

    elif renpy.get_screen("sex_interaction_menu", layer="master"):
        if _vt_girl:
            use condom_cherry(position="top_right") id "vt_si_condom"
            use cherry_window_row(girl=_vt_girl, position="top_left", border_color="#FF0000", border_size=2, icon_size=36) id "vt_si_cherry"

    elif renpy.get_screen("sex_outro_screen", layer="master"):
        $ _vt_so_girls = getattr(store, "se_female_participants", []) or ([_vt_part] if _vt_part else [])
        if _vt_so_girls:
            $ _vt_so_n = len(_vt_so_girls)
            use condom_cherry(position="top") id "vt_so_condom"
            for _vt_so_i, _vt_so_girl in enumerate(_vt_so_girls):
                use cherry_window_row(girl=_vt_so_girl, position="sex_outro", xoffset=-(_vt_so_n-1)*950//2+_vt_so_i*950, yoffset=150, border_color="#FF0000", border_size=2) id "vt_so_cherry_{}".format(_vt_so_i)

    elif renpy.get_screen("girl_review_menu", layer="master"):
        if _vt_girl:
            use cherry_window_row(girl=_vt_girl, position="girl_review", yoffset=-150, border_color="#FF0000", border_size=2) id "vt_gr_cherry"

    # VTMod pregnancy check pane - overlaid over bottom two-thirds of middle panel in girl ratings detail
    if renpy.get_screen("single_girl_rating_menu", layer="master"):
        use vtmod_preg_check_pane() id "vt_preg_pane"

    # Player HUD condom cherry - right side, below the 3 HUD buttons
    if renpy.get_screen("player_hud"):
        use hud_condom_cherry(position="top_right", icon_size=32) id "vt_ph_condom"

    # Tooltip cherry info - mirrors base game Girl tooltip x-clamping (screen_tooltip_overlay.rpy)
    if isinstance(_vt_tooltip, Girl):
        $ _tt_mx, _tt_my = renpy.get_mouse_pos()
        $ _tt_xoffset = max(min(_tt_mx, 1920 - max_tooltip_width), 5)
        $ _tt_yoffset = int(1080 * 0.15) + 474
        fixed at tooltip_fade_in:
            use cherry_window_row(girl=_vt_tooltip, position="tooltip", xoffset=_tt_xoffset, yoffset=_tt_yoffset, border_size=2, icon_size=36) id "vt_tt_cherry"
