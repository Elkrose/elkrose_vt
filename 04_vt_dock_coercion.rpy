# SafeDOCK / DryDOCK gift-time consent gate. Reuses the mod's existing openness/willingness
# machinery (00_vt_patcher.rpy: vt_ask_reachable / vt_willingness_band) the same way
# 03_vt_pullout_coercion.rpy wires a coercion beat into an in-progress interaction: a girl who
# isn't relationship-wise "open" to the player managing her reproduction yet gives a flat
# refusal; one who is reachable but doesn't want the pill's effect gets a real "talk her into it"
# beat (push, at a cost -- can still fail) or can be respected outright.

init python:

    # Tunable impacts (revisit during playtest) -- same shape as VT_PULLOUT_IMPACTS.
    VT_DOCK_IMPACTS = {
        "push_hesitant": {"affection": (-250, -100)},
        "push_refuse":   {"affection": (-500, -250), "fear": (200, 500)},
        "respect":       {"affection": (100, 300)},
    }

    # -- SafeDOCK (planb_pill) lines --

    VT_SAFEDOCK_CLOSED = {
        "crude":    ["You're not shoving pills at me. I don't even know you like that."],
        "explicit": ["That's not something I'd take from you -- we're not close enough."],
        "direct":   ["I'd rather not. I don't know you well enough to put that in my body."],
        "neutral":  ["I... don't think I want that from you. Not yet."],
        "shy":      ["I-I can't take that from you... I barely know you..."],
        "demure":   ["I must decline. That is not a decision I would trust to you -- not yet."],
    }

    VT_SAFEDOCK_ACCEPT = {
        "crude":    ["Yeah, hand it over -- no way I'm getting knocked up right now."],
        "explicit": ["Mmm, good thinking. Give it here, I'll take it."],
        "direct":   ["That's smart. I'll take it."],
        "neutral":  ["Okay, thank you. I'll take it."],
        "shy":      ["O-oh... okay. Thank you for thinking of that."],
        "demure":   ["How thoughtful. I shall take it, thank you."],
    }

    # She's already pregnant and knows it -- SafeDOCK only blocks FUTURE conception, so this
    # isn't a consent negotiation, it's her correcting him. Only reached when the player doesn't
    # already know (vt_give_medicine, 05_vt_gift_flow_repoint.rpy, greys the option out with a
    # tooltip when he does).
    VT_SAFEDOCK_ALREADY_PREGNANT = {
        "crude":    ["Wait -- that's not gonna do anything. I'm already pregnant."],
        "explicit": ["Hold on... that won't do anything. I'm already pregnant."],
        "direct":   ["That won't do anything. I'm already pregnant."],
        "neutral":  ["That... wouldn't do any good. I'm already pregnant."],
        "shy":      ["I... that wouldn't help. I'm already pregnant..."],
        "demure":   ["That would serve no purpose. I am already with child."],
    }

    # Firm "no" -- refuse band.
    VT_SAFEDOCK_RESIST_REFUSE = {
        "crude":    ["No. I'm not taking that. Don't try to decide that for me."],
        "explicit": ["No. I won't take that -- don't you dare decide that for me."],
        "direct":   ["No. I won't take that. That's not your call to make."],
        "neutral":  ["No. I don't want that. Please don't try to decide that for me."],
        "shy":      ["N-no... I don't want that. Please don't decide that for me..."],
        "demure":   ["No. I shall not. That is not a decision for you to make on my behalf."],
    }

    # Wavering, not a flat "no" -- hesitant band.
    VT_SAFEDOCK_RESIST_HESITANT = {
        "crude":    ["Wait... I don't know. What if I actually want a baby? Give me a sec."],
        "explicit": ["Hold on... I'm not sure. What if I want to get pregnant? Let me think."],
        "direct":   ["I'm not sure about that. What if I want a baby?"],
        "neutral":  ["I'm not sure I want that... what if I want a baby someday?"],
        "shy":      ["I... I don't know if I want that. What if I want a baby...?"],
        "demure":   ["I am uncertain. What if I wish to conceive, one day?"],
    }

    VT_SAFEDOCK_PUSH_FAIL_REFUSE = {
        "crude":    ["No! I said NO. Don't push me on this!"],
        "explicit": ["I said no! Don't you dare push me on this."],
        "direct":   ["No. I've made my decision. Don't push."],
        "neutral":  ["No, and don't push me on this. I mean it."],
        "shy":      ["P-please stop... I said no. Don't push me..."],
        "demure":   ["I must insist you not press the matter further. I have refused."],
    }

    # Uncomfortable, not angry -- she's still deciding, not digging in.
    VT_SAFEDOCK_PUSH_FAIL_HESITANT = {
        "crude":    ["H-hey, don't push. I said I wasn't sure yet."],
        "explicit": ["Don't push me... I said I wasn't sure yet."],
        "direct":   ["Don't push. I said I wasn't sure."],
        "neutral":  ["Please don't push me on this. I said I wasn't sure."],
        "shy":      ["P-please don't push... I said I wasn't sure..."],
        "demure":   ["Please, do not press the matter. I said I was uncertain."],
    }

    VT_SAFEDOCK_RESPECT = {
        "crude":    ["...Thanks for not being an ass about it."],
        "explicit": ["Thank you... for actually listening."],
        "direct":   ["Thank you for respecting that."],
        "neutral":  ["Thank you for understanding."],
        "shy":      ["Th-thank you... for not pushing..."],
        "demure":   ["Thank you. I appreciate you honoring my wishes."],
    }

    # -- DryDOCK (emergency_pill) lines --

    VT_DRYDOCK_CLOSED = {
        "crude":    ["Whoa, back off -- that's way too personal a thing to hand me."],
        "explicit": ["That's... not something I'd take from you. We're not close enough."],
        "direct":   ["No. That's not a decision I'd trust you with -- not yet."],
        "neutral":  ["I don't think I can take that from you. Not yet."],
        "shy":      ["I-I can't take that... not from you, not yet..."],
        "demure":   ["I must decline. That is far too intimate a matter to entrust to you presently."],
    }

    # She has no idea anything might be wrong -- a neutral "sure, thanks" with no pregnancy
    # content at all, since she isn't reacting to anything she's aware of.
    VT_DRYDOCK_ACCEPT = {
        "crude":    ["Yeah... okay. Give it here."],
        "explicit": ["...Okay. I'll take it."],
        "direct":   ["Alright. I'll take it."],
        "neutral":  ["Okay... I'll take it."],
        "shy":      ["O-okay... I'll take it..."],
        "demure":   ["Very well. I shall take it."],
    }

    # She knows, the player doesn't (yet) -- taking it doubles as her quietly telling him.
    VT_DRYDOCK_ACCEPT_SECRET = {
        "crude":    ["Well... I was gonna tell you. Guess it doesn't matter now."],
        "explicit": ["I was going to tell you, honestly... I guess it doesn't matter now."],
        "direct":   ["I was going to tell you. I suppose it doesn't matter now."],
        "neutral":  ["Well, I was going to tell you, but I guess it doesn't matter now..."],
        "shy":      ["I... I was going to tell you... I guess it doesn't matter now..."],
        "demure":   ["I had intended to inform you. It seems that is no longer necessary."],
    }

    # Both already know -- her reaction to actually going through with it.
    VT_DRYDOCK_ACCEPT_KNOWN = {
        "crude":    ["Yeah... let's just be done with it. Give it here."],
        "explicit": ["Okay... let's take care of this. Together."],
        "direct":   ["Alright. Let's do this."],
        "neutral":  ["Okay... I'm ready. Thank you for being here for this."],
        "shy":      ["O-okay... I'm glad you're here with me for this..."],
        "demure":   ["Very well. I am grateful you are here to see me through this."],
    }

    # Firm "no" -- refuse band.
    VT_DRYDOCK_RESIST_REFUSE = {
        "crude":    ["No! I want this baby, don't make me get rid of it!"],
        "explicit": ["No -- I want to keep it. Please don't make me do this."],
        "direct":   ["No. I want to keep this pregnancy."],
        "neutral":  ["I... I want to keep it. Please don't ask me to do this."],
        "shy":      ["N-no... I want to keep the baby... please..."],
        "demure":   ["No. I wish to keep this child. Please do not ask this of me."],
    }

    # Torn, not decided -- hesitant band.
    VT_DRYDOCK_RESIST_HESITANT = {
        "crude":    ["Wait... I don't know. Maybe I want this baby. Give me a second."],
        "explicit": ["Hold on... I'm not sure. Maybe I want to keep it. Let me think."],
        "direct":   ["I'm not sure. Maybe I want to keep this pregnancy."],
        "neutral":  ["I... I'm not sure. Maybe I want to keep it."],
        "shy":      ["I... I don't know... maybe I want to keep it..."],
        "demure":   ["I am uncertain. Perhaps I wish to keep this child."],
    }

    VT_DRYDOCK_PUSH_FAIL_REFUSE = {
        "crude":    ["No! I said no -- I'm keeping it, don't push me!"],
        "explicit": ["No! Don't push me on this -- I'm keeping it!"],
        "direct":   ["No. I'm keeping it. Don't push me on this."],
        "neutral":  ["No, please -- I'm keeping it. Don't push me."],
        "shy":      ["P-please... I'm keeping it... don't push..."],
        "demure":   ["I must insist. I am keeping this child -- please do not press further."],
    }

    # She's asking for time to decide, not defending a decision already made.
    VT_DRYDOCK_PUSH_FAIL_HESITANT = {
        "crude":    ["H-hey, don't push me on this. I need time to think."],
        "explicit": ["Don't push... I need a little time to think about this."],
        "direct":   ["Don't push. I need time to think about this."],
        "neutral":  ["Please don't push me. I need a little time to think."],
        "shy":      ["P-please don't push... I need time to think..."],
        "demure":   ["Please, do not press me. I require time to consider this."],
    }

    VT_DRYDOCK_RESPECT = {
        "crude":    ["...Thank you. I mean it."],
        "explicit": ["Thank you... for letting me keep it."],
        "direct":   ["Thank you for respecting my choice."],
        "neutral":  ["Thank you... for understanding."],
        "shy":      ["Th-thank you... for not making me..."],
        "demure":   ["Thank you. I am grateful for your understanding."],
    }

# Records whether the gate applied a dose. Keep the flag for existing saves in this scene.
default vt_dock_gift_applied = False

# Gift.give_gift transfers control here from the medicine menu.
label vt_dock_gift_gate(girl, pill_id):
    $ vt_dock_gift_applied = False

    if pill_id == "planb_pill" and girl.pregnant and girl.knows_pregnant:
        # Already pregnant, and she knows -- SafeDOCK is mechanically pointless here (it only
        # blocks future conception). Not a consent negotiation, so this bypasses the openness
        # gate and willingness band entirely: she simply corrects him. Only reachable when the
        # player doesn't already know it's pointless (vt_give_medicine greys the option out with
        # a tooltip when he does). Not consumed -- vt_dock_gift_applied stays False.
        $ girl.player_knows_pregnant = True
        $ _dg_line = vt_voice(girl, VT_SAFEDOCK_ALREADY_PREGNANT, "...")
        girl.character "[_dg_line]"
        return

    python:
        _dg_ask = "take_safedock" if pill_id == "planb_pill" else "keep_pregnancy"
        _dg_reachable = vt_ask_reachable(girl, _dg_ask, player)

    if not _dg_reachable:
        # Blanket "not open to this yet" refusal -- flat, no persuasion possible.
        $ _dg_line = vt_voice(girl, VT_SAFEDOCK_CLOSED if pill_id == "planb_pill" else VT_DRYDOCK_CLOSED, "...")
        girl.character "[_dg_line]"
        return

    if pill_id == "emergency_pill":
        # Real calendar days, not preg_progress_days (that field runs at `speed`, which outpaces
        # real time once PregnaVITA is involved -- see apply_emergency_pill's own comment).
        $ _dg_within_window = girl.pregnant and (getattr(time_manager, "total_days", 0) - girl.preg_start_day) <= 14

        if not girl.knows_pregnant or not _dg_within_window:
            # Nothing for her to resist: either she has no idea anything might be happening (no
            # willingness axis applies -- she can't want to keep what she doesn't know exists),
            # or there's nothing left for the pill to do (not pregnant / past the window).
            # apply_emergency_pill() handles the pregnant/window check and the hedge-vs-clear
            # notify tiering itself.
            $ girl.apply_emergency_pill()
            $ vt_dock_gift_applied = True
            if _dg_within_window:
                # It actually resolved something and she had no idea -- a neutral take-it line,
                # no pregnancy content (she isn't reacting to anything she's aware of).
                $ _dg_line = vt_voice(girl, VT_DRYDOCK_ACCEPT, "...")
                girl.character "[_dg_line]"
            return

    $ _dg_band = vt_willingness_band(girl, _dg_ask, player)

    if _dg_band in ("eager", "conditional"):
        # Conditional and eager answers both accept the medicine without a follow-up menu.
        if pill_id == "planb_pill":
            if player.get_item_quantity(pill_id) <= 0:
                return
            python:
                girl.apply_planb_pill()
                vt_spend_pill_ammo(player, pill_id)
                vt_dock_gift_applied = True
            $ _dg_line = vt_voice(girl, VT_SAFEDOCK_ACCEPT, "...")
        else:
            $ girl.apply_emergency_pill()
            $ vt_dock_gift_applied = True
            if girl.player_knows_pregnant:
                # Both already knew -- her reaction to going through with it, register-varied.
                $ _dg_line = vt_voice(girl, VT_DRYDOCK_ACCEPT_KNOWN, "...")
            else:
                # She knows, he doesn't -- taking it doubles as quietly telling him.
                $ _dg_line = vt_voice(girl, VT_DRYDOCK_ACCEPT_SECRET, "...")
        girl.character "[_dg_line]"
        return

    # hesitant / refuse -- she resists; give the player a real choice (talk her into it, or back
    # off). Deterministic-by-band like vt_try_creampie: pushing NEVER overrides a hesitant/refuse
    # band -- it only changes the cost/line of the "no". Hesitant and refuse read as genuinely
    # different reactions (wavering vs a flat "no"), not just a different cost.
    $ _dg_hesitant = (_dg_band == "hesitant")

    if pill_id == "planb_pill":
        $ _dg_resist_line = vt_voice(girl, VT_SAFEDOCK_RESIST_HESITANT if _dg_hesitant else VT_SAFEDOCK_RESIST_REFUSE, "...")
    else:
        $ _dg_resist_line = vt_voice(girl, VT_DRYDOCK_RESIST_HESITANT if _dg_hesitant else VT_DRYDOCK_RESIST_REFUSE, "...")
    girl.character "[_dg_resist_line]"

    menu:
        "Push her to take it":
            $ _dg_outcome = "push_hesitant" if _dg_hesitant else "push_refuse"
            $ girl.apply_impacts(dict(VT_DOCK_IMPACTS[_dg_outcome]))
            if pill_id == "planb_pill":
                $ _dg_line = vt_voice(girl, VT_SAFEDOCK_PUSH_FAIL_HESITANT if _dg_hesitant else VT_SAFEDOCK_PUSH_FAIL_REFUSE, "...")
            else:
                $ _dg_line = vt_voice(girl, VT_DRYDOCK_PUSH_FAIL_HESITANT if _dg_hesitant else VT_DRYDOCK_PUSH_FAIL_REFUSE, "...")
            girl.character "[_dg_line]"

        "Respect her wishes":
            $ girl.apply_impacts(dict(VT_DOCK_IMPACTS["respect"]))
            $ _dg_line = vt_voice(girl, VT_SAFEDOCK_RESPECT if pill_id == "planb_pill" else VT_DRYDOCK_RESPECT, "...")
            girl.character "[_dg_line]"
    return
