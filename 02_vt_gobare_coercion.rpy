# In-the-moment "talk her out of the condom" for an act she requires one for. Pure go_bare/go_bare_vaginal
# willingness (she already consented to the act). Outcomes: eager = wants_X_condom off permanently;
# conditional = this session only (vt_bare_session); hesitant/refuse = declines. One attempt per act per session.

# Other participants during the beat: small, faded, offset back-right (index fans several rightward).
transform vt_bystander_position(n=0):
    xalign 1.0
    xoffset (-20 - n * 90)
    ypos 200
    zoom 0.6
    alpha 0.4

init python:

    # Tunable impacts (revisit during playtest).
    VT_GOBARE_IMPACTS = {
        "yes_perm":    {"corruption": (500, 1000), "naturism": (100, 300)},
        "yes_session": {"corruption": (200, 500)},
        "no_soft":     {"affection": (-250, -100)},
        "no_hard":     {"affection": (-500, -250), "fear": (200, 500)},
        "respect":     {"affection": (100, 300)},
    }

    # Condom-gated act slots (slot -> display name).
    VT_GOBARE_ACTS = {"oral": "oral", "body": "body", "anal": "anal", "vaginal": "vaginal"}

    # Player's opening pitch, per act.
    VT_GOBARE_PITCH = {
        "oral":    "You don't need a rubber just to use your mouth on me... let me feel all of it.",
        "body":    "You really need me wrapped up just to rub against you? Let me feel your skin.",
        "anal":    "You don't need a condom for this... let me feel you, nothing between us.",
        "vaginal": "Do you really need me to wear one? I want to feel you properly...",
    }

    # Her reaction, keyed by outcome then register. Neutral to the player's current condom state (fires
    # whether raw or wrapped): lines say "go bare"/"use a condom", never "take it off"/"keep it on".
    VT_GOBARE_LINES = {
        "yes_perm": {
            "crude":    ["Fuck it -- no condom. I want to feel you bare, every damn time."],
            "explicit": ["God, yes... skin to skin. No rubber, from now on."],
            "direct":   ["Honestly? Go without. I've wanted to feel you properly anyway."],
            "neutral":  ["You know what... no condom. No more of that between us."],
            "shy":      ["I... okay. No condom. I want to feel you too... from now on."],
            "demure":   ["Mm... very well. No more of that between us. I want to feel you."],
        },
        "yes_session": {
            "crude":    ["...Fine. Just this once, no rubber. Don't make it a habit."],
            "explicit": ["Ohh... okay, just this once. No condom -- but only for now."],
            "direct":   ["Alright, just this time. But we're not making this a thing."],
            "neutral":  ["...Okay. Just this once. But use one next time."],
            "shy":      ["I... j-just this once, okay? O-only because it's you..."],
            "demure":   ["This once, then. But don't presume it'll be so easy again."],
        },
        "no": {
            "crude":    ["No. Wrap it up, or we're done here."],
            "explicit": ["Nice try. I want it wrapped -- I'm not risking it for you."],
            "direct":   ["No. Use a condom, or this stops."],
            "neutral":  ["No, I want you to use a condom. I mean it."],
            "shy":      ["N-no... please, I want you to wear one. I'm not ready for that."],
            "demure":   ["Absolutely not. Wear a condom, or we're finished."],
        },
    }

    VT_GOBARE_SUMMARY = {
        "yes_perm":    "She's done with condoms for this -- for good.",
        "yes_session": "She'll go bare this once -- but she'll want it back next time.",
        "no_soft":     "She's not comfortable with it. (She won't be asked again this session.)",
        "no_hard":     "She refuses, and resents being pushed. (She won't be asked again this session.)",
    }

    # Her initial resistance, shown when she wanted a condom for this act (her preference surfaces first).
    VT_GOBARE_RESIST = {
        "crude":    ["Mm -- you sure? I usually make guys wrap it..."],
        "explicit": ["Wait... shouldn't you put something on first?"],
        "direct":   ["Hold on -- don't you want a condom for this?"],
        "neutral":  ["Wait, shouldn't you wrap it up first?"],
        "shy":      ["Um... sh-shouldn't you use a condom...?"],
        "demure":   ["Oughtn't you to wear something first...?"],
    }

    # Her line when you back off and respect her boundary (keeps her condom; small affection gain).
    VT_GOBARE_RESPECT = {
        "crude":    ["Good call. Wrap it and I'm all yours."],
        "explicit": ["Thank you... put one on and you can have me."],
        "direct":   ["Thanks for listening. Wrap up and we're good."],
        "neutral":  ["Thank you. I'd rather we play it safe."],
        "shy":      ["Th-thank you... I feel better with one on."],
        "demure":   ["Thank you for understanding."],
    }

    # Her line when the act menu re-offers an act she already refused this session (anti-farm; no re-coercion).
    VT_GOBARE_ALREADY = {
        "crude":    ["I already said wrap it. Don't push your luck."],
        "explicit": ["I already told you -- I want it wrapped. Don't ask again."],
        "direct":   ["We already settled this. Condom, or it stops."],
        "neutral":  ["I already told you I want you to use one."],
        "shy":      ["I-I already said... please, just wear one..."],
        "demure":   ["I have already given you my answer. A condom, if you please."],
    }

    # Narrator reveal when a first raw attempt turns out she never wanted a condom for that act.
    VT_GOBARE_ACCEPT_NOTE = {
        "oral":    "{name} doesn't require a condom for oral sex.",
        "body":    "{name} doesn't require a condom for body contact.",
        "anal":    "{name} doesn't require a condom for anal sex.",
        "vaginal": "{name} doesn't require a condom for vaginal sex.",
    }

    def vt_condom_accept_note(girl, act):
        name = getattr(girl, "first_name", "She")
        return VT_GOBARE_ACCEPT_NOTE.get(act, "{name} has no condom requirement for this activity.").format(name=name)

    def _vt_gobare_intent(act):
        # Only go_bare_vaginal has its own willingness weights; oral/anal/body share "go_bare".
        return "go_bare_vaginal" if act == "vaginal" else "go_bare"

    def vt_condom_now(girl, act):
        """True if she wants a condom for `act` right now (a this-session concession only counts mid-interaction)."""
        if not (vt_body_contact_condom(girl) if act == "body" else getattr(girl, "wants_" + act + "_condom", False)):
            return False
        if getattr(store, "is_during_sex_interaction", False) and act in getattr(girl, "vt_bare_session", ()):
            return False
        return True

    def vt_reset_gobare_session():
        """Clear per-session coercion state for the current participants. Called at start_sex_interaction."""
        parts = getattr(store, "se_participants", None)
        if parts is None:
            return
        if not isinstance(parts, (list, tuple)):
            parts = [parts]
        for g in parts:
            if isinstance(g, Girl):
                g.vt_bare_session = set()
                g.vt_gobare_attempted = set()

    def vt_try_go_bare(girl, act, player=None):
        """Resolve a coercion attempt; store the result (outcome/line/act) for the coercion beat to read."""
        if player is None:
            player = getattr(store, "player", None)

        # One attempt per act per session.
        if not hasattr(girl, "vt_gobare_attempted") or girl.vt_gobare_attempted is None:
            girl.vt_gobare_attempted = set()
        if not hasattr(girl, "vt_bare_session") or girl.vt_bare_session is None:
            girl.vt_bare_session = set()
        girl.vt_gobare_attempted.add(act)

        band = vt_willingness_band(girl, _vt_gobare_intent(act), player)
        if band == "eager":
            outcome, line_key = "yes_perm", "yes_perm"
            setattr(girl, "wants_" + act + "_condom", False)   # permanent
        elif band == "conditional":
            outcome, line_key = "yes_session", "yes_session"
            girl.vt_bare_session.add(act)                       # this session only
        elif band == "hesitant":
            outcome, line_key = "no_soft", "no"
        else:
            outcome, line_key = "no_hard", "no"

        impacts = VT_GOBARE_IMPACTS.get(outcome)
        if impacts:
            girl.apply_impacts(dict(impacts))

        line = vt_voice(girl, VT_GOBARE_LINES[line_key], "No condom, then.")
        store.vt_gobare_result = {"outcome": outcome, "line": line, "act": act}

# Last coercion attempt result (outcome/line/act), set by vt_try_go_bare.
default vt_gobare_result = None
# Last coercion beat outcome: yes_perm | yes_session | no_soft | no_hard | respect.
default vt_gobare_beat_outcome = None

# Coercion beat, reached via the act-menu gate (vt_condom_attempt_gate below). Shows her fullbody + faded
# bystanders, her resistance, then Push/Respect. Sets vt_gobare_beat_outcome; plays no act itself.
label vt_gobare_beat(girl=None, act="vaginal"):
    if not isinstance(girl, Girl):
        return
    # Already asked this session -> respect, don't re-run.
    if act in getattr(girl, "vt_gobare_attempted", ()):
        $ store.vt_gobare_beat_outcome = "respect"
        return

    $ setattr(girl, "player_knows_" + act + "_condom", True)

    # Faded bystanders behind her (zorder -1).
    python:
        _gb_others = [p for p in se_participants
                      if isinstance(p, Girl) and p is not girl
                      and not getattr(p, "left_sex_interaction", False)]
        for _gb_i, _gb_o in enumerate(_gb_others):
            if _gb_o.image_manager.has_fullbody_image():
                _gb_ob = fit_image_to_size(_gb_o.image_manager.get_fullbody_image(), 1500, 1500)
                renpy.show("vt_bystander_%d" % _gb_i, what=_gb_ob,
                           at_list=[vt_bystander_position(_gb_i)], zorder=-1)

    # Her fullbody (matches current outfit/state).
    if girl.image_manager.has_fullbody_image():
        $ _gb_body = fit_image_to_size(girl.image_manager.get_fullbody_image(), 1500, 1500)
        show expression _gb_body as talker_body_image at dialogue_position

    # Her resistance line.
    $ _gb_resist = vt_voice(girl, VT_GOBARE_RESIST, "Wait -- shouldn't you wrap it first?")
    girl.character "[_gb_resist]"

    $ _gb_out = "respect"
    menu:
        "Push her to go bare":
            $ _gb_pitch = VT_GOBARE_PITCH.get(act, "Come on... you don't need that.")
            player.character "[_gb_pitch]"
            $ vt_try_go_bare(girl, act, player)
            python:
                _gb_res = vt_gobare_result or {}
                _gb_out = _gb_res.get("outcome", "no_hard")
                _gb_line = _gb_res.get("line", "")
            if _gb_line:
                girl.character "[_gb_line]"

        "Respect her boundaries":
            $ _gb_rline = vt_voice(girl, VT_GOBARE_RESPECT, "Thank you for understanding.")
            girl.character "[_gb_rline]"
            $ girl.apply_impacts(dict(VT_GOBARE_IMPACTS.get("respect", {})))

    hide expression talker_body_image
    python:
        for _gb_i in range(len(_gb_others)):
            renpy.hide("vt_bystander_%d" % _gb_i)

    $ store.vt_gobare_beat_outcome = _gb_out
    return

# "Attempt an act raw" gate. Condom-relevant acts have .label redirected here (01_vt_mod_items.rpy):
# not wants a condom -> brief reveal then the act; wants one -> coercion beat (go_bare), act plays on yes.
# Only a raw attempt tests her; protected / already-conceded / threesome pass through. Sets player_knows_<slot>_condom.
label vt_condom_attempt_gate:
    python:
        _cg_sa = se_selected_sex_action
        _cg_real = getattr(_cg_sa, "vt_real_label", None)
        _cg_slot = getattr(_cg_sa, "vt_condom_slot", None)
        _cg_girl = selected_girl

    # Missing wiring -> play the real label if present.
    if not _cg_real or not _cg_slot or not isinstance(_cg_girl, Girl):
        if _cg_real:
            $ renpy.call(_cg_real)
        return

    # Protected or already conceded this session -> play it.
    if player.condom_active != "raw" or (_cg_slot in getattr(_cg_girl, "vt_bare_session", ())):
        $ renpy.call(_cg_real)
        return

    python:
        _cg_wants = bool(vt_body_contact_condom(_cg_girl) if _cg_slot == "body" else getattr(_cg_girl, "wants_" + _cg_slot + "_condom", False))
        _cg_known = bool(getattr(_cg_girl, "player_knows_" + _cg_slot + "_condom", False))

    if not _cg_wants:
        # Never wanted one -> reveal once via toast, then play.
        if not _cg_known:
            $ setattr(_cg_girl, "player_knows_" + _cg_slot + "_condom", True)
            $ vt_fetish_notify(vt_condom_accept_note(_cg_girl, _cg_slot), duration=3.5)
        $ renpy.call(_cg_real)
        return

    # Wants a condom (discovered or not) -> this gate is the sole condom gatekeeper.

    # Already asked and held firm this session -> restate boundary; the act doesn't happen.
    if _cg_slot in getattr(_cg_girl, "vt_gobare_attempted", ()):
        $ setattr(_cg_girl, "player_knows_" + _cg_slot + "_condom", True)
        $ _cg_already = vt_voice(_cg_girl, VT_GOBARE_ALREADY, "I already told you -- wrap it up.")
        _cg_girl.character "[_cg_already]"
        return

    # Fresh attempt -> coercion beat; play on yes.
    call vt_gobare_beat(_cg_girl, _cg_slot)
    if vt_gobare_beat_outcome in ("yes_perm", "yes_session"):
        $ renpy.call(_cg_real)
    # Refusal/respect -> act doesn't happen; fall through to the menu.
    return
