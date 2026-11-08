# Booth invitation adapters. The base labels calculate their own acceptance, so only
# their destination setup/participant continuation is mirrored here. Normal encounter
# initialization, action/protection hooks and the home morning ending remain shared.
default vt_bar_booth_bathroom_visit = None

init python:
    VT_BAR_BOOTH_VENUES = {
        "bathroom": ("Bathroom quickie…", "bar_discussion_bathroom_quickie"),
        "player_home": ("Let's get out of here…", "bar_discussion_invite_home"),
    }
    # TODO: her place is planned; add a separate destination adapter after its home-visit
    # ownership/ending contract is designed. Do not expose an unfinished destination.

    def vt_bar_booth_pending_adverse():
        return se_end_label in ("vt_forced_sex_ending", "vt_force_fail_followup")

    def vt_bar_booth_venue_available(girl, destination):
        if destination not in VT_BAR_BOOTH_VENUES or girl is not selected_girl:
            return False
        if (_booth_intimacy_blocked or _vt_booth_end_visit or _vt_bar_booth_sour_ending
                or vt_bar_booth_pending_adverse()
                or girl.id not in girls_at_bar):
            return False
        # A timed departure deferred until conversation ends is not a completed exit.
        # Ordinary bar invitations remain available while she is still present.
        return vt_bar_booth_venue_requirement(girl, destination)

    def vt_bar_booth_venue_requirement(girl, destination):
        history = actions_already_done.get(girl.id, [])
        if "block_talking_bar" in history:
            return False
        action_key = VT_BAR_BOOTH_VENUES[destination][1]
        # Evaluate the ordinary menu's live requirement, including its history restriction.
        # A future restriction on that entry therefore applies at both entry points.
        for condition, caption, label in database_bar_options:
            if label == action_key:
                return requirements_met(condition, girl, {"girl": girl, "actions_already_done": history})
        return False

    def vt_bar_booth_closing_partner():
        # A closing invitation continues the suspended visit without putting anyone
        # back into a closed bar. Extras and partners who left cannot receive it.
        visit = vt_bar_booth_bathroom_visit
        if (not visit or time_manager.is_bar_hours() or visit["adverse"]
                or visit["values"]["_booth_intimacy_blocked"]
                or _vt_bar_booth_sour_ending or vt_bar_booth_pending_adverse()):
            return None
        girl = next((g for g in se_participants if isinstance(g, Girl) and g.id == visit["girl_id"]), None)
        if girl and not girl.left_sex_interaction and vt_bar_booth_venue_requirement(girl, "player_home"):
            return girl
        return None

    def vt_bar_booth_venue_options(girl):
        return [(caption, destination) for destination, (caption, key) in VT_BAR_BOOTH_VENUES.items()
                if vt_bar_booth_venue_available(girl, destination)]

    def vt_bar_booth_invitation_acceptance(girl):
        # The ordinary formula already includes alcohol. No intox fraction, stage
        # remapping, stage caps, cached bonus or character-method override belongs here.
        base = girl.get_acceptance_by_name("sex_interaction")
        score = max(0, min(100, vt_booth_gap_close(base, 100, vt_booth_arousal_fraction(girl))))
        vt_log(f"bar venue invitation: base={base} arousal={girl.arousal} adjusted={score}")
        return score

    def vt_bar_booth_suspend_for_bathroom(girl):
        # Primitive visit state survives the destination's normal initialization/ending.
        names = ("_booth_same_side", "_booth_done_flirty", "_vt_booth_flirt_uses",
                 "_vt_bar_booth_stage_chance", "_vt_booth_grope_earned_bonus",
                 "_vt_booth_grope_succeeded", "_vt_booth_touch_bare_started",
                 "_vt_booth_player_came", "_vt_booth_girl_came", "_booth_intimacy_blocked",
                 "_vt_booth_respected_acts")
        values = {}
        for name in names:
            value = getattr(store, name)
            values[name] = set(value) if isinstance(value, set) else dict(value) if isinstance(value, dict) else value
        store.vt_bar_booth_bathroom_visit = {"girl_id": girl.id, "seat": girls_at_bar.index(girl.id),
            "values": values, "girl_cums": girl.sex_interaction_cum_count,
            "player_cums": se_player_cum_count, "adverse": False}

    def vt_bar_booth_bathroom_end_guard(participants):
        # Capture an alternate ending before its shared handoff clears the outcome flags.
        if vt_bar_booth_bathroom_visit and vt_bar_booth_pending_adverse():
            vt_bar_booth_bathroom_visit["adverse"] = True

    def vt_bar_booth_restore_after_bathroom():
        visit = vt_bar_booth_bathroom_visit
        girl = next((g for g in se_participants if isinstance(g, Girl) and visit and g.id == visit["girl_id"]), None)
        store.vt_bar_booth_bathroom_visit = None
        # The encounter's real action costs may have carried us past bar closing.
        # After declining an eligible home invitation, or when none is available,
        # leave membership cleared and let show_bar own its usual closing/home flow.
        if not girl or girl.left_sex_interaction or visit["adverse"] or not time_manager.is_bar_hours():
            if girl:
                unassign_girl_from_all_locations(girl.id)
            if girl or selected_girl:
                vt_booth_end_encounter(girl or selected_girl)
            else:
                vt_reset_sex_session()
                sex_interaction_clear()
                store.vt_booth_overlay_girl = None
            return False
        girl_cums = visit["girl_cums"] + girl.sex_interaction_cum_count
        player_cums = visit["player_cums"] + se_player_cum_count
        # The normal ending removed bathroom participants. Restore only this booth partner,
        # retaining the hang-out timer/history rather than registering a new location visit.
        if girl.id not in girls_at_bar:
            seat = visit["seat"]
            if seat < len(girls_at_bar) and girls_at_bar[seat] is None:
                girls_at_bar[seat] = girl.id
            elif None in girls_at_bar:
                girls_at_bar[girls_at_bar.index(None)] = girl.id
            else:
                girls_at_bar.append(girl.id)
        store.selected_girl = girl
        vt_booth_start_encounter(girl)
        store.se_remove_girls_from_location = False
        for name, value in visit["values"].items():
            setattr(store, name, value)
        store._vt_booth_player_came = store._vt_booth_player_came or player_cums > 0
        store._vt_booth_girl_came = store._vt_booth_girl_came or girl_cums > 0
        girl.sex_interaction_cum_count = girl_cums
        store.se_player_cum_count = player_cums
        store._vt_booth_end_visit = False
        store._vt_bar_booth_sour_ending = False
        return True

    VT_BAR_BOOTH_BATHROOM_RETURN_LINES = [
        "You and [selected_girl] return to your booth and settle into your seats again.",
        "Back at the booth, you and [selected_girl] pick up your evening where you left off.",
    ]
    VT_BAR_BOOTH_CLOSING_LINES = [
        "As you and [selected_girl] come out of the bathroom, the staff are closing up. There's no time to return to your booth.",
        "Back outside the bathroom, you and [selected_girl] find the bar closing for the night. Your evening at the booth is over.",
    ]
    VT_BAR_BOOTH_CLOSING_SPACE_LINES = [
        "You give her the space she asked for as you leave the closing bar.",
        "You step back and let her leave on her own.",
    ]
    VT_BAR_BOOTH_CLOSING_DEPART_LINES = [
        "She collects her things and heads out on her own.",
        "She leaves the closing bar without you.",
    ]

    if vt_bar_booth_bathroom_end_guard not in database_post_sex_hooks:
        database_post_sex_hooks.append(vt_bar_booth_bathroom_end_guard)

    VT_BAR_BOOTH_VENUE_INVITE = {
        "bathroom": ["Want to slip into the bathroom with me for a quick private moment?",
                     "How about a quick detour to the bathroom, just us?"],
        "player_home": ["Let's get out of here. Would you like to come back to my place?",
                        "Want to come home with me, to my place? It's quieter there."],
    }
    VT_BAR_BOOTH_VENUE_YES = {
        "bathroom": {
            "demure": ["All right. Let's be discreet.", "Yes, but let's keep this between us."],
            "shy": ["Okay... come with me.", "Yes. Just a quick detour."],
            "neutral": ["I'm in. Let's make it quick.", "Okay, let's find a little privacy."],
            "direct": ["Yes. Lead the way.", "Sounds good. Let's go."],
            "explicit": ["I've been wanting some privacy with you.", "Yes, let's get away from this table."],
            "crude": ["About time. Let's go.", "I'm in. Show me the way."],
        },
        "player_home": {
            "demure": ["I'd like that. Let's go to your place.", "All right. I'd like a quieter evening with you."],
            "shy": ["Your place? Yes, I'd like that.", "Okay... let's go home with you."],
            "neutral": ["Your place sounds good. Let's go.", "Yes, I'd like to come home with you."],
            "direct": ["Yes. Take me to your place.", "I'm ready. Let's go home with you."],
            "explicit": ["Your place? That's just what I had in mind.", "Yes, let's have some privacy at your place."],
            "crude": ["Now we're talking. Your place it is.", "I'm in. Let's get back to your place."],
        },
    }
    VT_BAR_BOOTH_VENUE_YES_DRUNK = {
        "bathroom": ["The bathroom? Yeah... let's go!", "Okay... just a quick detour!"],
        "player_home": ["Your place? Yeah... lead the way!", "Okay... let's go back to your place!"],
    }
    VT_BAR_BOOTH_VENUE_YES_TIPSY = {
        "bathroom": ["A little detour? Heh, I'm in.", "Okay, let's sneak away for a bit."],
        "player_home": ["Your place sounds nice. Heh, let's go.", "Yes, let's go back to yours."],
    }
    VT_BAR_BOOTH_VENUE_NO = {
        "demure": ["No. Please leave me alone now.", "That isn't what I want. Don't ask me again."],
        "shy": ["No... I'd rather you left me alone.", "I don't want that. Please stop asking."],
        "neutral": ["No. I don't want to talk anymore.", "I'm not interested. Leave me alone."],
        "direct": ["No. We're done talking.", "Stop. I want some space."],
        "explicit": ["No. You've spoiled the evening for me.", "I'm not going anywhere with you. Leave me alone."],
        "crude": ["No chance. We're done talking.", "No. Give me some space."],
    }
    VT_BAR_BOOTH_VENUE_LEAVE = {
        "demure": ["No. I'm leaving now.", "That was too much. I'm going."],
        "shy": ["No... I need to leave.", "I don't want this. I'm going now."],
        "neutral": ["No. I've had enough. I'm leaving.", "I'm not going with you. I'm leaving on my own."],
        "direct": ["No. This evening is over.", "That's enough. I'm leaving."],
        "explicit": ["I'm not interested. I'm leaving.", "No. I'm done with this evening."],
        "crude": ["No chance. I'm out of here.", "Forget it. I'm leaving."],
    }
    VT_BAR_BOOTH_VENUE_NO_DRUNK = ["No... leave me alone now.", "I'm not going with you. Stop asking..."]
    VT_BAR_BOOTH_VENUE_NO_TIPSY = ["No, I'm not interested. Leave me alone.", "Nope. I don't want to talk anymore."]
    VT_BAR_BOOTH_VENUE_LEAVE_DRUNK = ["No... I've had enough. I'm leaving.", "I'm going now. On my own..."]
    VT_BAR_BOOTH_VENUE_LEAVE_TIPSY = ["No. I'm calling it a night.", "That's enough for me. I'm leaving."]
    VT_BAR_BOOTH_VENUE_STAY_LINES = [
        "You leave her at the booth and give her the space she asked for.",
        "You step away from the table, leaving her to the rest of her evening.",
    ]
    VT_BAR_BOOTH_VENUE_DEPART_LINES = [
        "She gathers her things and leaves the bar without you.",
        "She rises from the booth, collects her belongings and heads out on her own.",
    ]
    VT_BAR_BOOTH_HOME_ARRIVAL = {
        "sober": ["You and [selected_girl] reach your bedroom and settle onto the bed together.",
                  "At your place, you lead [selected_girl] into the bedroom and sit beside her on the bed."],
        "tipsy": ["You and [selected_girl] reach your bedroom, still giggling as you settle onto the bed.",
                  "Back at your place, [selected_girl] laughs softly as you sit together on the bed."],
        "drunk": ["You and [selected_girl] make your way into your bedroom, unsteady as you reach the bed.",
                  "At your place, [selected_girl] leans on you as you make your way to the bedroom."],
    }


label vt_bar_booth_invite_venue(destination, closing=False):
    # Recheck after menu selection. A newly pending ending must not be overwritten by
    # destination setup. Completed departures are already owned by their caller.
    if not _vt_bar_booth_sour_ending and vt_bar_booth_pending_adverse():
        if closing:
            $ vt_bar_booth_bathroom_visit = None
        call vt_bar_booth_adverse_ending(VT_BAR_BOOTH_CLOSING_DEPART_LINES if closing else None)
        $ _vt_bar_booth_sour_ending = True
        $ _vt_booth_end_visit = True
        $ vt_booth_end_encounter(selected_girl)
        $ remove_girl_id_from_location(selected_girl.id, "girls_at_bar")
        return "show_bar"
    $ _vt_venue_available = (destination == "player_home" and selected_girl is not None and vt_bar_booth_closing_partner() is selected_girl) if closing else vt_bar_booth_venue_available(selected_girl, destination)
    if not _vt_venue_available:
        return

    $ actions_already_done[selected_girl.id].append(VT_BAR_BOOTH_VENUES[destination][1])
    $ time_manager.skip_time(minutes=5)
    $ _vt_venue_invite = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VENUE_INVITE[destination])
    player.character "[_vt_venue_invite]"
    $ girl_acceptance = vt_bar_booth_invitation_acceptance(selected_girl)
    if destination == "bathroom" and girl_acceptance >= 40:
        $ vt_bar_booth_suspend_for_bathroom(selected_girl)
    if closing:
        $ vt_bar_booth_bathroom_visit = None
    # Acceptance is latched before cleanup and the destination's normal reset_for_sex.
    $ _vt_booth_end_visit = True
    $ vt_booth_end_encounter(selected_girl)
    if girl_acceptance >= 40:
        if selected_girl.has_trait("drunk"):
            $ _vt_venue_reply = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VENUE_YES_DRUNK[destination])
        elif selected_girl.has_trait("tipsy"):
            $ _vt_venue_reply = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VENUE_YES_TIPSY[destination])
        else:
            $ _vt_venue_reply = vt_booth_voice(selected_girl, VT_BAR_BOOTH_VENUE_YES[destination])
        selected_girl.character "[_vt_venue_reply]"
        $ remove_girl_id_from_location(selected_girl.id, "girls_at_bar")
        $ se_forced_sex = selected_girl.has_trait("drunk") or selected_girl.has_trait("tipsy")
        $ se_participants = [selected_girl]
        $ se_use_generic_ending = True
        if destination == "bathroom":
            call vt_bar_booth_bathroom_destination
        elif destination == "player_home":
            call vt_bar_booth_player_home_destination
        return _return
    elif girl_acceptance >= 20:
        $ actions_already_done[selected_girl.id].append("block_talking_bar")
        if selected_girl.has_trait("drunk"):
            $ _vt_venue_reply = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VENUE_NO_DRUNK)
        elif selected_girl.has_trait("tipsy"):
            $ _vt_venue_reply = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VENUE_NO_TIPSY)
        else:
            $ _vt_venue_reply = vt_booth_voice(selected_girl, VT_BAR_BOOTH_VENUE_NO)
        selected_girl.character "[_vt_venue_reply]"
        $ selected_girl.apply_impacts({"affection": -500, "fear": 500})
        $ _vt_venue_transition = vt_booth_choice(selected_girl, VT_BAR_BOOTH_CLOSING_SPACE_LINES if closing else VT_BAR_BOOTH_VENUE_STAY_LINES)
        "[_vt_venue_transition]"
    else:
        if selected_girl.has_trait("drunk"):
            $ _vt_venue_reply = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VENUE_LEAVE_DRUNK)
        elif selected_girl.has_trait("tipsy"):
            $ _vt_venue_reply = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VENUE_LEAVE_TIPSY)
        else:
            $ _vt_venue_reply = vt_booth_voice(selected_girl, VT_BAR_BOOTH_VENUE_LEAVE)
        selected_girl.character "[_vt_venue_reply]"
        $ _vt_venue_transition = vt_booth_choice(selected_girl, VT_BAR_BOOTH_CLOSING_DEPART_LINES if closing else VT_BAR_BOOTH_VENUE_DEPART_LINES)
        "[_vt_venue_transition]"
        $ remove_girl_id_from_location(selected_girl.id, "girls_at_bar")
        $ selected_girl.apply_impacts({"affection": -1000, "fear": 1000})
    return "show_bar"


label vt_bar_booth_player_home_destination:
    $ se_end_label = "bar_discussion_invite_home_end_sex"
    $ se_additional_webm_sub_tags = ["home"]
    $ se_remove_girls_from_location = False
    scene black
    $ renpy.call_screen("transition_screen", transition_text="About 15 minutes later...", transition_duration=1.5)
    scene bg bedroom with dissolve
    $ _vt_venue_sobriety = "drunk" if selected_girl.has_trait("drunk") else "tipsy" if selected_girl.has_trait("tipsy") else "sober"
    $ _vt_venue_arrival = vt_booth_choice(selected_girl, VT_BAR_BOOTH_HOME_ARRIVAL[_vt_venue_sobriety]).replace("[selected_girl]", str(selected_girl))
    "[_vt_venue_arrival]"
    return "start_sex_interaction"


label vt_bar_booth_bathroom_destination:
    $ se_end_label = "vt_bar_booth_bathroom_end"
    $ se_remove_girls_from_location = True
    $ se_additional_webm_sub_tags = ["bathroom"]
    "You two push past another patron towards the bathroom."
    python:
        bartender_id = get_working_bartender()
        other_girls_in_area = [girl_id for girl_id in girls_at_bar if girl_id and girl_id != selected_girl.id]
        other_girls_in_area.append(bartender_id)
        menu_options = [
            ("Try getting someone else to join?", "title"),
            ("Invite him to join you", "mmf_threesome"),
        ]
        for girl_id in other_girls_in_area:
            if not girl_id:
                continue
            girl = academy.get_girl_by_id(girl_id)
            if girl:
                menu_options.append((f"{girl.full_name}", f"girl|{girl_id}"))
        menu_options.append(("No", "None"))
        menu_choice = renpy.display_menu(menu_options)
    if menu_choice == "mmf_threesome":
        "He eagerly accepts and locks the bathroom behind him."
        $ se_participants.append(GameCharacter(first_name=renrandom.choice(database_male_first_names)))
    elif menu_choice == "None":
        if selected_girl.has_trait("drunk"):
            "You and [selected_girl] stagger into an empty stall, fumbling with the lock..."
        elif selected_girl.has_trait("tipsy"):
            "You and [selected_girl] stumble into a stall, giggling as you latch it shut..."
        else:
            "You and [selected_girl] step into an empty stall and lock the door."
    else:
        $ girl_id = menu_choice.split("|")[-1]
        $ girl = academy.get_girl_by_id(girl_id)
        # Only the booth partner receives the arousal adjustment. Extra invitations use
        # the ordinary bar score and retain the original bartender/participant effects.
        $ girl_acceptance = girl.get_acceptance_by_name("sex_interaction")
        if girl_id == bartender_id:
            player.character "You know, things are heating up over here. How about you join us in the bathroom for a little... private break?"
            if girl_acceptance >= 40:
                girl.character "A break, huh? You're trouble, but I'm in."
                "She glances around, then calls out to a coworker."
                girl.character "Hey, cover the bar for me. I'll be back in a bit!"
                "She wipes her hands on her apron, smirking as she steps out from behind the counter to follow you."
                $ se_participants.append(girl)
            elif girl_acceptance >= 20:
                girl.character "Are you serious? I'm working here. Not running off to the bathroom with you!"
                "She plants her hands on her hips, her tone sharp as she glares at you over the counter."
                girl.character "Pay your tab and take your ideas elsewhere. Some of us have jobs to do."
                "The clatter of glasses behind her punctuates her rejection."
                $ girl.apply_impacts({"affection": -100})
            else:
                girl.character "What did you just say? That's it! Out! Both of you!"
                "Her face flushes with anger as she storms around the counter, pointing toward the door."
                girl.character "I'm not dealing with this nonsense. Get out before I call someone!"
                "She marches to the door, flips the lock with a loud click, and shoves it open, glaring until you and [selected_girl] stumble out."
                $ remove_girl_id_from_location(selected_girl.id, "girls_at_bar")
                if "bar" not in girls_blocking_area:
                    $ girls_blocking_area["bar"] = []
                $ girls_blocking_area["bar"].append(girl.id)
                $ sex_interaction_clear()
                $ vt_bar_booth_bathroom_visit = None
                $ girl.apply_impacts({"affection": -2000})
                return "show_map_navigation_menu"
        else:
            player.character "Hey, [girl], want to join us in the bathroom for a little... private party?"
            if girl_acceptance >= 40:
                if girl.has_trait("drunk"):
                    girl.character "Hell yeah! Le's... le's do it!"
                elif girl.has_trait("tipsy"):
                    girl.character "Ooh, yep! I'm joinin' ya!"
                else:
                    girl.character "Absolutely! Count me in!"
                $ se_participants.append(girl)
            elif girl_acceptance >= 20:
                "[girl] frowns and shakes her head."
                if girl.has_trait("drunk"):
                    girl.character "Nuh-uh, no way! Tha's... too much!"
                elif girl.has_trait("tipsy"):
                    girl.character "Ew, no thanks! I'm not tha' far gone!"
                else:
                    girl.character "No, I don't think so..."
                $ girl.apply_impacts({"affection": -500, "fear": 500})
            else:
                "[girl] steps back, glaring at you."
                if girl.has_trait("drunk"):
                    girl.character "Y're sick! No chance, creep!"
                elif girl.has_trait("tipsy"):
                    girl.character "Gross! Not happenin', weirdo!"
                else:
                    girl.character "You are disgusting! Not a chance!"
                $ girl.apply_impacts({"affection": -1000, "fear": 1000})
    scene black with dissolve
    scene bg bar_bathroom with dissolve
    return "start_sex_interaction"


label vt_bar_booth_bathroom_end:
    $ _vt_closing_partner = vt_bar_booth_closing_partner()
    if _vt_closing_partner:
        $ selected_girl = _vt_closing_partner
        scene bg bar with dissolve
        if selected_girl.image_manager.has_fullbody_image():
            $ body_image = fit_image_to_size(selected_girl.image_manager.get_fullbody_image(), 1500, 1500)
            show expression body_image as talker_body_image at dialogue_position
        $ _vt_closing_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_CLOSING_LINES).replace("[selected_girl]", str(selected_girl))
        "[_vt_closing_line]"
        menu:
            "Invite her back to my place…":
                call vt_bar_booth_invite_venue("player_home", closing=True)
                if _return:
                    jump expression _return
            "Call it a night":
                pass
    $ _vt_bathroom_resume = vt_bar_booth_restore_after_bathroom()
    if not _vt_bathroom_resume:
        jump show_bar
    scene bg bar with dissolve
    if selected_girl.image_manager.has_fullbody_image():
        $ body_image = fit_image_to_size(selected_girl.image_manager.get_fullbody_image(), 1500, 1500)
        show expression body_image as talker_body_image at dialogue_position
    $ _vt_bathroom_return_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_BATHROOM_RETURN_LINES).replace("[selected_girl]", str(selected_girl))
    "[_vt_bathroom_return_line]"
    call vt_bar_booth_resume
    jump expression _return
