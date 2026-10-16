# Cherry Tracker -- a computer desktop app that lists every active girl and mother
# with her pregnancy / birth-control state and her attitude toward the player
# (the dialogue-work axes: explicitness register, openness tier, baby-desire band,
# approach + sexual history).
#
# Integration is the base game's own extension points -- no base screen or label is
# overridden:
#   * The desktop app is one entry in database_computer_buttons (auto-placed in the
#     last free slot; the slot self-heals when the entry is absent, per
#     screen_computer_menu.rpy:39-41).
#   * It's SPOILER-GATED: the entry is only present while persistent
#     .vt_cherry_tracker_enabled is on (default off). A toggle is registered in the
#     base Settings menu via database_settings_options. Because the desktop re-syncs
#     its icon grid from database_computer_buttons every time it opens, adding/removing
#     the entry at init and on toggle is enough -- the icon appears/disappears live.
#
# The screen is otherwise READ-ONLY: every field is read via getattr(...) defaults and
# read-only helpers, so opening the tracker never mutates a girl or creates a sidecar key --
# EXCEPT for one deliberate, opt-in exception: a girl flagged as needing baby_desire migration
# (baby_desire_migration_version < 1, i.e. her score predates that flag) gets a "preview, then
# accept/cancel" mini-tool in her detail pane. Previewing never touches her data (the candidate
# value lives only in a screen-local cache); only clicking Accept commits it. See
# vt_ct_needs_migration / vt_ct_migration_roll / vt_ct_migration_accept / vt_ct_migration_cancel.

default persistent.vt_cherry_tracker_enabled = False

init python:
    # The desktop-app entry (added to database_computer_buttons only while enabled).
    VT_CHERRY_TRACKER_BUTTON = {
        "name": "Cherry Tracker",
        "icon": "_mods/content/elkrose_vt/extra_images/cherries_idle.png",
        "label": "vt_show_cherry_tracker",
        "tooltip": "Pregnancy, birth control & attitude overview",
    }

    def vt_ct_apply_desktop_icon():
        """Add or remove the desktop app to match the persistent toggle. Safe to call
        anytime; the computer desktop re-syncs its grid from database_computer_buttons
        each time it opens, so this takes effect on the next open (no restart)."""
        if getattr(persistent, "vt_cherry_tracker_enabled", False):
            database_computer_buttons["vt_cherry_tracker"] = VT_CHERRY_TRACKER_BUTTON
        else:
            database_computer_buttons.pop("vt_cherry_tracker", None)

    # Settings-menu icon. The settings grid (unlike the desktop) does NOT fit_image_to_size the
    # icon, so we size it to fill the 125px slot ourselves. A DynamicDisplayable rebuilds it each
    # render, so it tracks the toggle: full colour while enabled, greyscale while disabled. Built
    # as a DynamicDisplayable so fit_image_to_size / desaturate_image resolve at render time (no
    # init-order dependency on the utils module).
    def _vt_ct_toggle_icon(st, at):
        base = "_mods/content/elkrose_vt/extra_images/cherries_idle.png"
        if getattr(persistent, "vt_cherry_tracker_enabled", False):
            return fit_image_to_size(base, 125, 125), None
        return fit_image_to_size(desaturate_image(base), 125, 125), None

    # Apply the persisted setting at load (runs after database_computer_buttons's init -4).
    vt_ct_apply_desktop_icon()

    # Register the always-available Settings-menu toggle.
    if "vt_cherry_tracker_toggle" not in database_settings_options:
        database_settings_options["vt_cherry_tracker_toggle"] = {
            "name": "Cherry Tracker",
            "icon": DynamicDisplayable(_vt_ct_toggle_icon),
            "label": "vt_toggle_cherry_tracker",
            "tooltip": "Show or hide the Cherry Tracker app on the computer desktop.\n\nIt reveals pregnancy, birth control and attitude info for every girl and mother -- spoilery, so it is off by default.",
        }

    # --- Presentation-only label maps (categorical helper tokens -> display text) ---
    VT_CT_REGISTER_LABELS = {
        "crude": "Crude", "explicit": "Explicit", "direct": "Direct",
        "neutral": "Neutral", "shy": "Shy", "demure": "Demure",
    }
    # Register is an ordered ladder (demure = least crude .. crude = most), so it can
    # carry a discrete bar. Rank -> 0..5, scaled to 0..100 for the bar.
    VT_CT_REGISTER_RANK = {
        "demure": 0, "shy": 1, "neutral": 2, "direct": 3, "explicit": 4, "crude": 5,
    }
    VT_CT_DESIRE_LABELS = {
        "none": "No interest", "curious": "Curious", "thinking": "Thinking about it",
        "obsessed": "Obsessed", "fixation": "Fixated", "obsession": "Utterly obsessed",
    }
    VT_CT_TIER_LABELS = {"closed": "Closed", "guarded": "Guarded", "open": "Open"}
    VT_CT_APPROACH_LABELS = {
        "compassionate": "Loving", "sexualized": "Sexual",
        "transactional": "Transactional", "dominate": "Dominant",
    }
    VT_CT_HISTORY_LABELS = {0: "None", 1: "Intimate", 2: "Vaginal", 3: "Established"}
    VT_CT_PHASE_LABELS = {0: "Just conceived", 1: "1st trimester", 2: "2nd trimester", 3: "3rd trimester"}

    def vt_ct_students():
        """Active/interactable students (mothers filtered out). Read-only."""
        gm = getattr(getattr(store, "academy", None), "girl_manager", None)
        if gm is None:
            return []
        try:
            girls = gm.get_interactable_girls()
        except Exception:
            girls = list(getattr(gm, "girls", []))
        return [g for g in girls if not is_mother_character(g)]

    def vt_ct_mothers():
        """Mothers of the active students, de-duplicated by identity. Read-only."""
        seen = set()
        out = []
        for g in vt_ct_students():
            m = getattr(g, "mother", None)
            if m is not None and id(m) not in seen:
                seen.add(id(m))
                out.append(m)
        return out

    def vt_ct_portrait(girl, size=300):
        try:
            return fit_image_to_size(girl.image_manager.get_first_face_image(), size, size)
        except Exception:
            return None

    def vt_ct_baby_desire(girl):
        return max(0, min(100, getattr(girl, "baby_desire", 0) or 0))

    def vt_ct_needs_migration(girl):
        """True for a girl whose baby_desire was set by a since-revised formula (pre-dates the
        baby_desire_migration_version flag) and hasn't yet been corrected via the manual tool
        below. Read-only check -- does not itself touch her data."""
        return vt_girl_bucket(girl).get("baby_desire_migration_version", 0) < 1

    def vt_ct_migration_roll(cache, girl):
        """Preview-only: compute a projected established-formula baby_desire and stash it in the
        screen-local cache. Does not touch the girl until vt_ct_migration_accept is used."""
        cache[girl.id] = get_baby_desire(girl, fresh=False)

    def vt_ct_migration_cancel(cache, girl):
        cache.pop(girl.id, None)

    def vt_ct_migration_accept(cache, girl):
        """Commit a previewed (or freshly-rolled, if never previewed) baby_desire value and mark
        her migrated so she won't be flagged again."""
        value = cache.pop(girl.id, None)
        if value is None:
            return False  # accept only a score the player actually previewed
        bucket = vt_girl_bucket(girl)
        bucket["baby_desire"] = int(max(0, min(100, value)))
        bucket["baby_desire_xp"] = 0
        bucket["baby_desire_migration_version"] = 1
        renpy.notify("{}'s baby desire updated to {}.".format(girl.first_name, bucket["baby_desire"]))

    def vt_ct_due_in(girl):
        """Days until due, or None if unknown. Read-only."""
        end = getattr(girl, "preg_end_day", 0) or 0
        if end <= 0:
            return None
        return end - getattr(time_manager, "total_days", 0)

    # Cycle-timeline zone colours (fixed bands across the 30-day cycle). The cycle is built so
    # ovulation is always cycle day 15, giving these day ranges:
    VT_CT_CYCLE_RED = "#c0392b"     # menstrual ("moon time"), days 1-5
    VT_CT_CYCLE_BLUE = "#3a9fd6"    # follicular / pre-ovulation, days 6-11
    VT_CT_CYCLE_GREEN = "#2ecc71"   # fertile window, days 12-16 (ovulation = day 15)
    VT_CT_CYCLE_YELLOW = "#e1c340"  # luteal / post-ovulation, days 17-30
    VT_CT_CYCLE_OVULATION = "#0b6e33"  # the single ovulation day (day 15), a darker green on top

    # Gestation-timeline trimester colours (light -> dark green as the pregnancy advances).
    VT_CT_GEST_1 = "#b6e8b0"  # 1st trimester (progress 0-104)
    VT_CT_GEST_2 = "#3fbf5a"  # 2nd trimester (progress 105-209)
    VT_CT_GEST_3 = "#0b6e33"  # 3rd trimester (progress 210-260)

    def vt_ct_cycle(girl):
        """Read-only cycle read for the timeline: (cycle_day 1-30 or 0, status text)."""
        try:
            cycle_day = girl.get_cycle_day()
        except Exception:
            cycle_day = 0
        try:
            status = girl.get_fertility_day_status()
        except Exception:
            status = ""
        return cycle_day, status

    def vt_ct_supplements(girl):
        """Fertility duration, prenatal stock and doses taken, as display text. Read-only.

        FertiBOOST (fertility_boost) is a day-countdown boost; PregnaVITA is shown by doses she
        has actually taken (prenatal_doses) and pill supply on hand (prenatal_boost).
        """
        out = []
        fb = getattr(girl, "fertility_boost", 0) or 0
        if fb > 0:
            out.append("FertiBOOST ({}d)".format(fb))
        prenatal = vt_prenatal_status(girl)
        if prenatal:
            out.append(prenatal)
        return ", ".join(out) if out else "None"


label vt_show_cherry_tracker:
    call screen vt_cherry_tracker_menu()
    jump show_computer_menu


# Settings-menu toggle: flip the spoiler gate, sync the desktop icon, notify, return.
label vt_toggle_cherry_tracker:
    python:
        persistent.vt_cherry_tracker_enabled = not getattr(persistent, "vt_cherry_tracker_enabled", False)
        vt_ct_apply_desktop_icon()
        if persistent.vt_cherry_tracker_enabled:
            renpy.notify("Cherry Tracker enabled -- its icon is now on the computer desktop.")
        else:
            renpy.notify("Cherry Tracker disabled -- its desktop icon is hidden.")
    jump show_settings_menu


screen vt_cherry_tracker_menu():
    default vt_ct_sel = None
    default vt_ct_bd_preview = {}

    $ _player = getattr(store, "player", None)
    $ _students = vt_ct_students()
    $ _mothers = vt_ct_mothers()
    $ _sel = vt_ct_sel or (_students[0] if _students else (_mothers[0] if _mothers else None))

    use base_computer_menu

    frame:
        background menu_background_light
        xsize 1920
        ysize 1042
        xalign 0.5
        ypadding 5
        xpadding 5

        text "corrupted_academy/cherry_tracker" size font_size_small color menu_text_color xpos 0.06 ypos 0.0338

        imagebutton:
            xalign 1.0
            yalign 0
            xoffset 5
            yoffset -5
            idle "gui/widgets/close.webp"
            hover apply_brightness("gui/widgets/close.webp", 0.5)
            action [
                Hide("vt_cherry_tracker_menu", _layer="master"),
                Jump("show_computer_menu")
            ]
            if persistent.right_click_close:
                keysym "mouseup_3"
                tooltip "{b}Hotkey{/b}: Right-Click"

        frame:
            background None
            xalign 0.5
            yalign 1.0
            ysize 963
            xfill True
            xpadding 0
            ypadding 0

            hbox:
                xalign 0.5
                spacing 5

                # ---------------- LEFT PANE: girl / mother lists ----------------
                frame:
                    background menu_background_light
                    yalign 0.5
                    xsize 540
                    yfill True

                    vbox:
                        spacing 8
                        xfill True

                        text "Students" size font_size_header color menu_text_color font header_font xalign 0.5

                        viewport:
                            xsize 520
                            ysize 420
                            draggable True
                            mousewheel True
                            scrollbars "vertical"
                            vscrollbar_unscrollable "hide"

                            vbox:
                                xfill True
                                spacing 2

                                if not _students:
                                    text "No active students." size font_size_small color menu_text_color_muted xalign 0.5
                                for _g in _students:
                                    use vt_ct_list_row(girl=_g, selected=(_sel is _g))

                        add "gui/widgets/separator.webp" xsize 500 ysize 5 xalign 0.5

                        text "Mothers" size font_size_header color menu_text_color font header_font xalign 0.5

                        viewport:
                            xsize 520
                            ysize 420
                            draggable True
                            mousewheel True
                            scrollbars "vertical"
                            vscrollbar_unscrollable "hide"

                            vbox:
                                xfill True
                                spacing 2

                                if not _mothers:
                                    text "No mothers." size font_size_small color menu_text_color_muted xalign 0.5
                                for _m in _mothers:
                                    use vt_ct_list_row(girl=_m, selected=(_sel is _m))

                # ---------------- RIGHT PANE: detail ----------------
                frame:
                    background menu_background_light
                    yalign 0.5
                    xsize 860
                    yfill True
                    xpadding 15
                    ypadding 10

                    if _sel is None:
                        text "No girls available." size font_size_header color menu_text_color_muted xalign 0.5 yalign 0.5
                    else:
                        use vt_ct_detail(girl=_sel, player=_player, preview_cache=vt_ct_bd_preview)


screen vt_ct_list_row(girl, selected=False):
    button:
        xsize 500
        ypadding 4
        xpadding 8
        background None
        selected selected
        selected_background menu_background_medium
        hover_background menu_background_medium
        action SetScreenVariable("vt_ct_sel", girl)
        tooltip girl.full_name

        fixed:
            xsize 484
            ysize 30

            text "[girl.full_name]" size font_size_normal color menu_text_color xalign 0.0 yalign 0.5

            if getattr(girl, "pregnant", False):
                add fit_image_to_size("_mods/content/elkrose_vt/extra_images/feeding_bottle.png", 24, 24) xalign 1.0 yalign 0.5


screen vt_ct_detail(girl, player=None, preview_cache=None):
    viewport:
        xfill True
        yfill True
        draggable True
        mousewheel True
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"

        vbox:
            xfill True
            spacing 14

            # ---- Header: portrait + name ----
            hbox:
                spacing 20

                $ _portrait = vt_ct_portrait(girl, 200)
                if _portrait is not None:
                    add _portrait

                vbox:
                    yalign 0.5
                    spacing 6

                    text "{b}[girl.full_name]{/b}" size font_size_large_header color menu_text_color font header_font
                    if is_mother_character(girl):
                        text "Mother" size font_size_normal color menu_text_color_muted
                    else:
                        text "Student" size font_size_normal color menu_text_color_muted

            # ---- Pregnancy ----
            text "Pregnancy" size font_size_header color menu_text_color font header_font

            $ _pregnant = getattr(girl, "pregnant", False)
            if _pregnant:
                $ _phase = getattr(girl, "pregnancy_phase", 0) or 0
                $ _progress = getattr(girl, "preg_progress_days", 0) or 0
                $ _father = getattr(girl, "preg_father", None)
                $ _due = vt_ct_due_in(girl)

                use vt_ct_field(label="Status", value="Pregnant", tooltip="Whether she is currently pregnant.")
                use vt_ct_field(label="Stage", value="{} (day {})".format(VT_CT_PHASE_LABELS.get(_phase, "Early"), _progress), tooltip="Her current trimester and how many days into the pregnancy she is.")
                use vt_ct_field(label="Father", value=("You" if _father == "player" else ("Someone else" if _father == "npc" else "Unknown")), tooltip="Who fathered the pregnancy -- you, or another man.")
                if _due is not None:
                    use vt_ct_field(label="Due", value=("in {} days".format(_due) if _due > 0 else "any day now"), tooltip="Days until she is expected to give birth.")
                use vt_ct_field(label="She knows", value=("Yes" if getattr(girl, "knows_pregnant", False) else "No"), tooltip="Whether she has realized she's pregnant yet.")
                use vt_ct_field(label="You know", value=("Yes" if getattr(girl, "player_knows_pregnant", False) else "No"), tooltip="Whether you have found out she's pregnant yet.")
            else:
                use vt_ct_field(label="Status", value="Not pregnant", tooltip="Whether she is currently pregnant.")

            $ _kids_player = getattr(girl, "kids_with_player", 0) or 0
            $ _kids = getattr(girl, "kids", 0) or 0
            use vt_ct_field(label="Children", value="{} with you / {} total".format(_kids_player, _kids), tooltip="Children she has with you, and her total number of children.")

            # ---- Fertility ----
            text "Fertility" size font_size_header color menu_text_color font header_font

            if getattr(girl, "pregnant", False):
                # While pregnant, birth control and conception chance are irrelevant -- show gestation.
                $ _gest_progress = getattr(girl, "preg_progress_days", 0) or 0
                $ _gest_phase = getattr(girl, "pregnancy_phase", 0) or 0
                use vt_ct_gestation_bar(label="Gestation", progress=_gest_progress, band=VT_CT_PHASE_LABELS.get(_gest_phase, ""), tooltip="Pregnancy progress across the three trimesters (light to dark green). The marker shows her current gestational day.")
            else:
                use vt_ct_field(label="On birth control", value=("Yes" if getattr(girl, "birth_control", False) else "No"), tooltip="Whether she is currently taking birth control.")

                $ _cyc_day, _cyc_status = vt_ct_cycle(girl)
                use vt_ct_cycle_bar(label="Cycle", cycle_day=_cyc_day, band=_cyc_status, tooltip="Her position in her 30-day cycle. Red = period, blue = pre-ovulation, green = fertile window, dark-green pip = the ovulation day, yellow = post-ovulation. The marker shows today.")
                if _cyc_day:
                    use vt_ct_field(label="Cycle day", value="Day {} of 30".format(_cyc_day), tooltip="Which day of her 30-day cycle she is on.")

                $ _fert = 0.0
                python:
                    try:
                        _fert = max(0.0, min(100.0, float(girl.effective_fertility())))
                    except Exception:
                        _fert = 0.0
                use vt_ct_field(label="Conception chance", value="{:.1f}%".format(_fert), tooltip="Her actual chance of conceiving right now, combining her base fertility with her current cycle day.")

            use vt_ct_field(label="Supplements", value=vt_ct_supplements(girl), tooltip="FertiBOOST shows days left. PregnaVITA shows stock waiting for weekly dosing and doses already taken; only doses taken accelerate pregnancy.")

            # ---- Condom Desires ----
            text "Condom Desires" size font_size_header color menu_text_color font header_font

            use vt_ct_field(label="Vaginal", value=("Wants a condom" if getattr(girl, "wants_vaginal_condom", False) else "Prefers raw"), tooltip="Whether she wants a condom used during vaginal sex.")
            use vt_ct_field(label="Anal", value=("Wants a condom" if getattr(girl, "wants_anal_condom", False) else "Prefers raw"), tooltip="Whether she wants a condom used during anal sex.")
            use vt_ct_field(label="Oral", value=("Wants a condom" if getattr(girl, "wants_oral_condom", False) else "Prefers raw"), tooltip="Whether she wants a condom used during oral sex.")
            use vt_ct_field(label="Body", value=("Wants a condom" if getattr(girl, "wants_body_condom", False) else "Prefers raw"), tooltip="Whether she wants a condom used during body / other sex acts.")

            # ---- Baby Desire Migration (only shown for a girl flagged as not-yet-migrated) ----
            if preview_cache is not None and vt_ct_needs_migration(girl):
                text "Baby Desire Update Available" size font_size_header color menu_text_color font header_font
                text "Her baby desire score predates the current formula and may not reflect her current stats. Preview a new score before deciding whether to update her." size font_size_small color menu_text_color_muted

                use vt_ct_field(label="Current", value=str(vt_ct_baby_desire(girl)), tooltip="Her baby desire score right now -- unchanged unless you accept a preview below.")

                $ _bd_preview = preview_cache.get(girl.id)
                if _bd_preview is None:
                    textbutton "Preview updated score":
                        action Function(vt_ct_migration_roll, preview_cache, girl)
                        xalign 0.0
                else:
                    use vt_ct_field(label="Projected", value=str(_bd_preview), tooltip="What her score would become if you accept -- computed from her current stats, not her legacy value.")
                    hbox:
                        spacing 10
                        textbutton "Re-roll" action Function(vt_ct_migration_roll, preview_cache, girl)
                        textbutton "Accept" action Function(vt_ct_migration_accept, preview_cache, girl)
                        textbutton "Cancel" action Function(vt_ct_migration_cancel, preview_cache, girl)

            # ---- Attitude toward the player (items listed A-Z) ----
            text "Attitude" size font_size_header color menu_text_color font header_font

            # Approach is unordered (which of four types dominates), so it stays a badge, not a bar.
            $ _appr = getattr(girl, "dominant_approach", None)
            use vt_ct_field(label="Approach", value=VT_CT_APPROACH_LABELS.get(_appr, "Unknown"), tooltip="Her dominant relationship approach toward you: Loving, Sexual, Transactional, or Dominant.")

            $ _bd = vt_ct_baby_desire(girl)
            $ _bd_band = vt_baby_desire_band(girl)
            use vt_ct_bar(label="Baby desire", amount=_bd, band=VT_CT_DESIRE_LABELS.get(_bd_band, _bd_band), tooltip="How much she wants to become pregnant, from No interest to Utterly obsessed.")

            $ _reg = vt_explicitness_register(girl)
            use vt_ct_bar(label="Explicitness", amount=VT_CT_REGISTER_RANK.get(_reg, 2) * 20, band=VT_CT_REGISTER_LABELS.get(_reg, _reg), tooltip="How explicit her sexual wording gets, driven by her corruption, from Demure to Crude.")

            $ _hist = vt_history_level(girl)
            use vt_ct_bar(label="History", amount=_hist * 100 // 3, band=VT_CT_HISTORY_LABELS.get(_hist, str(_hist)), tooltip="Your sexual history with her, from None to Established.")

            $ _open = vt_topic_openness(girl, player)
            $ _tier = vt_topic_tier(girl, player)
            use vt_ct_bar(label="Openness", amount=_open, band=VT_CT_TIER_LABELS.get(_tier, _tier), tooltip="How willing she is to discuss sexual and reproductive topics with you, from Closed to Open.")


screen vt_ct_field(label="", value="", tooltip=""):
    fixed:
        xsize 780
        ysize 34
        text "[label]" size font_size_normal color menu_text_color_muted xalign 0.0 yalign 0.5
        text "[value]" size font_size_normal color menu_text_color xalign 1.0 yalign 0.5
        # Transparent hover target for the row tooltip (same idiom as the base My Stats screen).
        if tooltip:
            imagebutton:
                xysize (780, 34)
                idle "images/none.webp"
                action NullAction()
                tooltip tooltip


screen vt_ct_bar(label="", amount=0, band="", tooltip=""):
    fixed:
        xsize 780
        ysize 49
        vbox:
            xsize 780
            spacing 4
            fixed:
                xsize 780
                ysize 30
                text "[label]" size font_size_normal color menu_text_color_muted xalign 0.0 yalign 0.5
                text "[band]" size font_size_normal color menu_text_color xalign 1.0 yalign 0.5
            bar:
                xsize 780
                ysize 15
                value amount
                range 100
        if tooltip:
            imagebutton:
                xysize (780, 49)
                idle "images/none.webp"
                action NullAction()
                tooltip tooltip


# Cycle timeline: the whole 30-day cycle as fixed colour bands (moon / follicular / fertile /
# luteal) with a "today" marker at the current cycle day. Ovulation sits mid-bar (day 15).
screen vt_ct_cycle_bar(label="", cycle_day=0, band="", tooltip=""):
    $ _w = 780
    $ _red = int(round(_w * 5 / 30.0))     # days 1-5   (moon time)
    $ _blue = int(round(_w * 6 / 30.0))    # days 6-11  (follicular)
    $ _green = int(round(_w * 5 / 30.0))   # days 12-16 (fertile)
    $ _yellow = _w - _red - _blue - _green # days 17-30 (luteal)
    $ _ovul_w = int(round(_w / 30.0))          # one day wide
    $ _ovul_x = int(round(14.5 / 30.0 * _w))   # centre of cycle day 15 (ovulation)
    $ _marker_x = int(round((cycle_day - 0.5) / 30.0 * _w)) if cycle_day else -100

    fixed:
        xsize 780
        ysize 55
        vbox:
            xsize 780
            spacing 4
            fixed:
                xsize 780
                ysize 30
                text "[label]" size font_size_normal color menu_text_color_muted xalign 0.0 yalign 0.5
                text "[band]" size font_size_normal color menu_text_color xalign 1.0 yalign 0.5
            fixed:
                xsize 780
                ysize 21
                hbox:
                    yalign 0.5
                    spacing 0
                    add Solid(VT_CT_CYCLE_RED) xsize _red ysize 15
                    add Solid(VT_CT_CYCLE_BLUE) xsize _blue ysize 15
                    add Solid(VT_CT_CYCLE_GREEN) xsize _green ysize 15
                    add Solid(VT_CT_CYCLE_YELLOW) xsize _yellow ysize 15
                # Ovulation day: a taller, distinct band on top of the green so the peak day pops.
                add Solid(VT_CT_CYCLE_OVULATION) xsize _ovul_w ysize 21 xpos _ovul_x xanchor 0.5 yalign 0.5
                if cycle_day:
                    add Solid("#000000") xsize 5 ysize 21 xpos _marker_x xanchor 0.5 yalign 0.5
                    add Solid("#ffffff") xsize 3 ysize 21 xpos _marker_x xanchor 0.5 yalign 0.5
        if tooltip:
            imagebutton:
                xysize (780, 55)
                idle "images/none.webp"
                action NullAction()
                tooltip tooltip


# Gestation timeline (pregnant girls): the full 260-day term as three trimester bands
# (light -> mid -> dark green), with a marker at her current gestational progress.
screen vt_ct_gestation_bar(label="", progress=0, band="", tooltip=""):
    $ _w = 780
    $ _t1 = int(round(_w * 105 / 260.0))   # 1st trimester (progress 0-104)
    $ _t2 = int(round(_w * 105 / 260.0))   # 2nd trimester (progress 105-209)
    $ _t3 = _w - _t1 - _t2                  # 3rd trimester (progress 210-260)
    $ _marker_x = int(round(max(0, min(260, progress)) / 260.0 * _w))

    fixed:
        xsize 780
        ysize 55
        vbox:
            xsize 780
            spacing 4
            fixed:
                xsize 780
                ysize 30
                text "[label]" size font_size_normal color menu_text_color_muted xalign 0.0 yalign 0.5
                text "[band]" size font_size_normal color menu_text_color xalign 1.0 yalign 0.5
            fixed:
                xsize 780
                ysize 21
                hbox:
                    yalign 0.5
                    spacing 0
                    add Solid(VT_CT_GEST_1) xsize _t1 ysize 15
                    add Solid(VT_CT_GEST_2) xsize _t2 ysize 15
                    add Solid(VT_CT_GEST_3) xsize _t3 ysize 15
                add Solid("#000000") xsize 5 ysize 21 xpos _marker_x xanchor 0.5 yalign 0.5
                add Solid("#ffffff") xsize 3 ysize 21 xpos _marker_x xanchor 0.5 yalign 0.5
        if tooltip:
            imagebutton:
                xysize (780, 55)
                idle "images/none.webp"
                action NullAction()
                tooltip tooltip
