# Coffee-booth additions: sober flirting and the existing café bathroom destination.
# Permanent preferences stay with their existing owners; these defaults are visit-only.
default vt_coffee_booth_flirts_left = 3
default vt_coffee_booth_bathroom_visit = None

init python:
    VT_COFFEE_BOOTH_FLIRT_LINES = {
        "dominate": [
            "Look at me a moment. I like having your attention.",
            "Stay with me. The rest of this place can wait.",
            "Come a little closer. I'd rather hear you than the room.",
        ],
        "compassionate": [
            "I'm enjoying this. I don't feel the need to fill every silence with you.",
            "The coffee was an excuse. I wanted some time with you.",
            "I like seeing you relax. It makes me want to stay a little longer.",
        ],
        "sexualized": [
            "You're making it difficult to concentrate on this conversation.",
            "I keep wondering what you'd say if we had a little more privacy.",
            "I was going to play it cool. Then you looked at me like that.",
        ],
        "transactional": [
            "Keep me company a little longer. I'll make the next coffee my treat.",
            "Give me a chance to impress you. I can do better than choosing the table.",
            "I'd like to earn another smile from you. Tell me where to start.",
        ],
    }
    VT_COFFEE_BOOTH_FLIRT_REPLIES = {
        "miss": {
            "crude": ["That sounded better in your head, didn't it?", 'Try talking to me instead of delivering a line.', 'You can do better than that. I was enjoying the conversation.', 'Was that supposed to impress me?', "You're laying it on a bit thick."],
            "explicit": ["Mm, you're trying a little too hard.", 'You had my attention before the line.', "I'd rather you stopped trying to guess what I want to hear.", "You don't have to sell this quite so hard.", "Mm, let's try an ordinary conversation for a moment."],
            "direct": ["That isn't really my style.", "I'd rather you were a little more yourself.", "I'm not sure you read me right there.", "You don't need to impress me with a speech.", "Let's try that with a little less pressure."],
            "neutral": ["I don't quite know what to do with that.", "Let's call that a practice attempt.", 'That felt a little rehearsed.', 'I liked it better when we were just talking.', 'I think we got our signals crossed.'],
            "shy": ["Oh... I wasn't sure you meant that.", 'Um, could we slow down a little?', "I... don't think that's quite what I meant.", 'Could we just talk for a little while?', "You're making me nervous, and not in the way you hoped."],
            "demure": ['I think we were doing rather well without the performance.', 'Perhaps we should return to our coffee for a moment.', 'A little less insistence would be welcome.', 'You need not try quite so hard on my account.', 'I fear you have mistaken my meaning.'],
        },
        "ok": {
            "crude": ['All right, that almost got me.', "Better. At least you're paying attention.", 'Heh. I might forgive that one.', 'All right. That earned you a smile.', 'There you go. That sounded like you.'],
            "explicit": ['Mm, I might let you keep talking.', "That's a little more like it.", 'Mm, that was worth putting my cup down for.', 'I think I can let you get away with that.', "All right. Let's see where this conversation goes."],
            "direct": ["I'll give you that one.", "All right. You've got my attention.", 'That sounded more like you.', 'I like a little honesty.', "All right. I'm listening."],
            "neutral": ['That was quite sweet, actually.', "Well, now I'm smiling.", "I wasn't expecting that smile to happen.", 'All right, you can keep me company a bit longer.', "I think we're getting somewhere."],
            "shy": ['Oh... I liked hearing that.', "You're making me a little shy.", "I might have been hoping you'd notice.", 'You can say things like that again, if you like.', "I think... I'm glad you said that."],
            "demure": ['That was pleasantly unexpected.', 'I may have to forgive your boldness.', 'I suppose a little flirting will do no harm.', 'I shall allow you that small victory.', 'You are beginning to make a rather good case for staying.'],
        },
        "good": {
            "crude": ["Damn you. Now I'm grinning into my cup.", "Keep that up and I'll forget why I ordered this.", "You know exactly what that grin is doing, don't you?", "Now you've made me forget what I was saying.", "If I spill this coffee, I'm blaming you."],
            "explicit": ["Mm, now you're making this interesting.", "I'd rather hear more of that than finish my coffee.", 'Mm, I like having this much of your attention.', "You're making the rest of this place feel very far away.", 'I could get used to this side of you.'],
            "direct": ['Yes. I like this side of you.', 'That got to me more than I expected.', "I'm enjoying this more than I expected.", 'Keep looking at me when you say that.', "I'd rather stay here with you for a while."],
            "neutral": ["I'm glad we chose this table.", 'You make it very easy to lose track of time.', 'I was trying not to make it too obvious that I like this.', "Now you've made me forget what I was about to say.", 'I like the way this conversation is going.'],
            "shy": ["Don't look away... I liked that.", 'I was hoping you might say something like that.', 'I keep trying to think of something clever, and then you look at me.', "Please don't mistake the quiet for not liking this.", "I'm glad it's you sitting here with me."],
            "demure": ['You are making it difficult to maintain my composure.', 'I find I am in no hurry to leave.', 'I had not planned on enjoying this quite so much.', 'You have a most inconvenient way of holding my attention.', 'I believe my coffee may have to wait.'],
        },
        "great": {
            "crude": ["Okay, you win. I'm barely tasting the coffee now.", 'Damn. Keep your eyes on me like that.', "You can stop looking so pleased with yourself. It's working.", 'Forget the coffee for a second. Look at me.', "I'm not even pretending to pay attention to anything else now."],
            "explicit": ['I wish this table gave us a little more privacy.', "Mm, come closer. I don't want to share this with the room.", "Mm, I think we both know the coffee isn't keeping me here.", 'Tell me that again, a little closer.', "I'd like to keep this moment to ourselves."],
            "direct": ['You have all my attention now.', "I'd like a little time alone with you.", "I don't want to get up from this table yet.", "I'm past pretending this is just about coffee.", 'Come closer. I want to hear that properly.'],
            "neutral": ["I'm going to remember this coffee for a while.", "I'm very glad you asked me to sit with you.", "Now I don't want to be anywhere else.", "The coffee can wait. I'd rather look at you.", "You make it very hard to remember that we're in public."],
            "shy": ["I don't want this to end just yet.", 'Can we stay like this a little longer?', 'I think you know why I keep looking at you.', "Don't tease me for smiling. I can't help it.", 'Stay close, please. I like this.'],
            "demure": ['I am beginning to think the coffee was rather beside the point.', 'You have made this a very distracting conversation.', 'I seem to have forgotten every sensible reason to leave.', 'I would very much like another moment of your company.', 'For once, I find I have little interest in my surroundings.'],
        },
    }
    VT_COFFEE_BOOTH_FLIRT_REJECT = {
        "crude": ["No. You've ruined this for me. I'm leaving.", "That was out of line. We're done here."],
        "explicit": ["No. I don't want to sit here with you anymore.", "That crossed a line. I'm leaving."],
        "direct": ["That's enough. I'm leaving.", "No. This conversation is over."],
        "neutral": ["That made me uncomfortable. I'm going to go.", "I don't want to continue this. Goodbye."],
        "shy": ["I... I need to leave now.", "No, please. I don't want to stay."],
        "demure": ["That was quite inappropriate. I am leaving.", "I will not continue this conversation. Goodbye."],
    }
    VT_COFFEE_BOOTH_DEPARTURE = [
        "She gathers her things and leaves the coffee shop, leaving you at the table.",
        "She gets up from the booth, collects her belongings and walks out without you.",
    ]
    VT_COFFEE_BOOTH_BATHROOM_INVITE = [
        "Would you like to slip away to the bathroom with me for a little privacy?",
        "How about a quick detour to the bathroom, just the two of us?",
    ]
    VT_COFFEE_BOOTH_BATHROOM_YES = {
        "crude": ["All right. Let's get away from this table.", "I'm in. You lead."],
        "explicit": ["Mm, I've been hoping for a little privacy.", "Yes. Let's take a quiet moment together."],
        "direct": ["Yes. Let's go.", "All right, but let's be discreet."],
        "neutral": ["Okay. Just a quick detour.", "Yes, I'd like a little privacy with you."],
        "shy": ["Okay... come with me.", "Yes, but let's be quiet about it."],
        "demure": ["Very well. Let us be discreet.", "All right. A brief detour, then."],
    }
    VT_COFFEE_BOOTH_BATHROOM_NO = {
        "crude": ["No. Give me some space.", "No chance. I'm done talking."],
        "explicit": ["No. I'd rather finish my coffee on my own.", "I'm not going with you. Please leave me be."],
        "direct": ["No. I want to be left alone now.", "I'm not interested. Give me some space."],
        "neutral": ["No, thank you. I'd like to sit on my own.", "I don't want that. Let's leave it here."],
        "shy": ["No... I'd rather stay here on my own.", "I don't want to. Please don't ask again."],
        "demure": ["No, thank you. I wish to be left alone.", "That is not what I want. Please excuse me."],
    }
    VT_COFFEE_BOOTH_BATHROOM_SPACE = [
        "You leave her at the booth and step away, giving her the space she asked for.",
        "You collect your things and leave her to finish her coffee on her own.",
    ]
    VT_COFFEE_BOOTH_BATHROOM_RETURN = [
        "You and [selected_girl] return to the booth and settle back into your seats.",
        "Back at your table, you and [selected_girl] pick up your conversation again.",
    ]
    VT_COFFEE_BOOTH_CLOSING = [
        "The staff are closing up when you come out. You collect your things and leave the café.",
        "There is no time to return to your booth. The mall is closing, and you both head out.",
    ]

    def vt_coffee_booth_flirt_result(girl, approach):
        # Same deterministic bands, match/clash terms and impacts as sober bar flirting.
        # No drink override, new roll, new persona state or automatic permission grant.
        approaches = {
            "dominate": (girl.discipline + girl.fear) / 2,
            "compassionate": (girl.affection + girl.intellect) / 2,
            "sexualized": (girl.corruption + girl.naturism) / 2,
            "transactional": (girl.corruption + girl.intellect) / 2,
        }
        dominant = max(approaches, key=approaches.get)
        strength = approaches[dominant]
        score = vt_booth_local_acceptance(girl, *VT_BAR_BOOTH_FLIRT_LOCAL_FLOOR)
        if approach == dominant:
            score += int(strength * VT_BAR_BOOTH_FLIRT_MATCH_BONUS_SCALE)
        elif VT_BAR_BOOTH_FLIRT_APPROACH_CLASH_MAP.get(approach) == dominant:
            score -= int(strength * VT_BAR_BOOTH_FLIRT_CLASH_PENALTY_SCALE)
        score = max(0, min(100, score))
        tier = next(name for name, ceiling in VT_BAR_BOOTH_FLIRT_TIER_CUTOFFS if score < ceiling)
        vt_log(f"coffee flirt: approach={approach} dominant={dominant} score={score} tier={tier}")
        return tier

    def vt_coffee_booth_bathroom_available(girl):
        if (girl is not selected_girl or _booth_intimacy_blocked or _vt_booth_end_visit
                or _vt_booth_sour_ending or vt_bar_booth_pending_adverse()
                or not time_manager.is_mall_hours() or girl.id not in girls_in_coffee_shop):
            return False
        history = actions_already_done.get(girl.id, [])
        if "block_talking_coffee_shop" in history:
            return False
        for condition, caption, label in database_coffee_shop_options:
            if label == "coffee_shop_discussion_bathroom_quickie":
                return requirements_met(condition, girl, {"girl": girl, "actions_already_done": history})
        return False

    def vt_coffee_booth_invitation_acceptance(girl):
        # The ordinary live café formula remains authoritative. Only current arousal
        # closes its remaining gap; there is no extra alcohol bonus or flat boost.
        base = girl.get_acceptance_by_name("sex_interaction")
        return max(0, min(100, vt_booth_gap_close(base, 100, vt_booth_arousal_fraction(girl))))

    def vt_coffee_booth_suspend(girl):
        names = ("_booth_same_side", "_booth_done_flirty", "vt_coffee_booth_flirts_left",
                 "_vt_booth_stage_chance", "_vt_booth_grope_earned_bonus", "_vt_booth_grope_succeeded",
                 "_vt_booth_touch_bare_started", "_vt_booth_player_came", "_vt_booth_girl_came",
                 "_booth_intimacy_blocked", "_vt_booth_respected_acts")
        values = {}
        for name in names:
            value = getattr(store, name)
            values[name] = set(value) if isinstance(value, set) else dict(value) if isinstance(value, dict) else value
        store.vt_coffee_booth_bathroom_visit = {
            "girl_id": girl.id, "seat": girls_in_coffee_shop.index(girl.id), "values": values,
            "girl_cums": girl.sex_interaction_cum_count, "player_cums": se_player_cum_count, "adverse": False,
        }

    def vt_coffee_booth_bathroom_end_guard(participants):
        if vt_coffee_booth_bathroom_visit and vt_bar_booth_pending_adverse():
            vt_coffee_booth_bathroom_visit["adverse"] = True

    def vt_coffee_booth_restore():
        visit = vt_coffee_booth_bathroom_visit
        girl = next((g for g in se_participants if isinstance(g, Girl) and visit and g.id == visit["girl_id"]), None)
        store.vt_coffee_booth_bathroom_visit = None
        if not girl or girl.left_sex_interaction or visit["adverse"] or not time_manager.is_mall_hours():
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
        if girl.id not in girls_in_coffee_shop:
            seat = visit["seat"]
            if seat < len(girls_in_coffee_shop) and girls_in_coffee_shop[seat] is None:
                girls_in_coffee_shop[seat] = girl.id
            elif None in girls_in_coffee_shop:
                girls_in_coffee_shop[girls_in_coffee_shop.index(None)] = girl.id
            else:
                girls_in_coffee_shop.append(girl.id)
        store.selected_girl = girl
        vt_booth_start_encounter(girl)
        store.se_remove_girls_from_location = False
        for name, value in visit["values"].items():
            setattr(store, name, value)
        store._vt_booth_player_came = store._vt_booth_player_came or player_cums > 0
        store._vt_booth_girl_came = store._vt_booth_girl_came or girl_cums > 0
        girl.sex_interaction_cum_count = girl_cums
        store.se_player_cum_count = player_cums
        store._vt_booth_end_visit = store._vt_booth_sour_ending = False
        return True

    if vt_coffee_booth_bathroom_end_guard not in database_post_sex_hooks:
        database_post_sex_hooks.append(vt_coffee_booth_bathroom_end_guard)

label vt_coffee_booth_flirt:
    if vt_coffee_booth_flirts_left <= 0:
        return
    $ vt_coffee_booth_flirts_left -= 1
    menu:
        "Take the lead. (Dominate)":
            $ _vt_coffee_approach = "dominate"
        "Tell her you enjoy her company. (Compassionate)":
            $ _vt_coffee_approach = "compassionate"
        "Let her know she is distracting you. (Sexualized)":
            $ _vt_coffee_approach = "sexualized"
        "Offer to make her time worthwhile. (Transactional)":
            $ _vt_coffee_approach = "transactional"
    $ _vt_coffee_line = vt_booth_choice(selected_girl, VT_COFFEE_BOOTH_FLIRT_LINES[_vt_coffee_approach])
    player.character "[_vt_coffee_line]"
    $ _vt_coffee_tier = vt_coffee_booth_flirt_result(selected_girl, _vt_coffee_approach)
    if _vt_coffee_tier == "critical_fail":
        $ _vt_coffee_line = vt_booth_voice(selected_girl, VT_COFFEE_BOOTH_FLIRT_REJECT)
        selected_girl.character "[_vt_coffee_line]"
        $ _vt_coffee_line = vt_booth_choice(selected_girl, VT_COFFEE_BOOTH_DEPARTURE)
        "[_vt_coffee_line]"
        $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_FLIRT_CRITFAIL_IMPACTS))
        $ _vt_booth_end_visit = _vt_booth_sour_ending = True
    else:
        $ _vt_coffee_line = vt_booth_voice(selected_girl, VT_COFFEE_BOOTH_FLIRT_REPLIES[_vt_coffee_tier])
        selected_girl.character "[_vt_coffee_line]"
        $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_FLIRT_IMPACTS_BY_TIER[_vt_coffee_tier]))
    return

label vt_coffee_booth_invite_bathroom:
    if vt_bar_booth_pending_adverse():
        call vt_bar_booth_adverse_ending(VT_COFFEE_BOOTH_DEPARTURE)
        $ _vt_booth_end_visit = _vt_booth_sour_ending = True
        $ vt_booth_end_encounter(selected_girl)
        $ remove_girl_id_from_location(selected_girl.id, "girls_in_coffee_shop")
        return "show_coffee_shop"
    if not vt_coffee_booth_bathroom_available(selected_girl):
        return
    $ actions_already_done[selected_girl.id].append("coffee_shop_discussion_bathroom_quickie")
    $ time_manager.skip_time(minutes=5)
    $ _vt_coffee_line = vt_booth_choice(selected_girl, VT_COFFEE_BOOTH_BATHROOM_INVITE)
    player.character "[_vt_coffee_line]"
    $ girl_acceptance = vt_coffee_booth_invitation_acceptance(selected_girl)
    if girl_acceptance >= 40:
        $ vt_coffee_booth_suspend(selected_girl)
    $ _vt_booth_end_visit = True
    $ vt_booth_end_encounter(selected_girl)
    if girl_acceptance >= 40:
        $ _vt_coffee_line = vt_booth_voice(selected_girl, VT_COFFEE_BOOTH_BATHROOM_YES)
        selected_girl.character "[_vt_coffee_line]"
        $ remove_girl_id_from_location(selected_girl.id, "girls_in_coffee_shop")
        $ se_forced_sex = False
        $ se_participants = [selected_girl]
        $ se_use_generic_ending = True
        $ se_remove_girls_from_location = True
        $ se_end_label = "vt_coffee_booth_bathroom_end"
        $ se_additional_webm_sub_tags = ["bathroom"]
        call vt_coffee_booth_bathroom_destination
        return _return
    elif girl_acceptance >= 20:
        $ actions_already_done[selected_girl.id].append("block_talking_coffee_shop")
        $ _vt_coffee_line = vt_booth_voice(selected_girl, VT_COFFEE_BOOTH_BATHROOM_NO)
        selected_girl.character "[_vt_coffee_line]"
        $ selected_girl.apply_impacts({"affection": -500, "fear": 500})
        $ _vt_coffee_line = vt_booth_choice(selected_girl, VT_COFFEE_BOOTH_BATHROOM_SPACE)
        "[_vt_coffee_line]"
    else:
        $ _vt_coffee_line = vt_booth_voice(selected_girl, VT_COFFEE_BOOTH_FLIRT_REJECT)
        selected_girl.character "[_vt_coffee_line]"
        $ _vt_coffee_line = vt_booth_choice(selected_girl, VT_COFFEE_BOOTH_DEPARTURE)
        "[_vt_coffee_line]"
        $ remove_girl_id_from_location(selected_girl.id, "girls_in_coffee_shop")
        $ selected_girl.apply_impacts({"affection": -1000, "fear": 1000})
    return "show_coffee_shop"

label vt_coffee_booth_bathroom_destination:
    "You two push past another patron towards the bathroom."

    python:
        barista_id = get_working_barista()

        other_girls_in_area = [girl_id for girl_id in girls_in_coffee_shop if girl_id and girl_id != selected_girl.id]
        other_girls_in_area.append(barista_id)

        menu_options = [
            ("Try getting someone else to join?", "title"),
            ("Invite him to join you", "mmf_threesome"),
        ]

        if other_girls_in_area:
            for girl_id in other_girls_in_area:
                if not girl_id:
                    continue

                girl = academy.get_girl_by_id(girl_id)
                if not girl:
                    continue

                menu_options.append((f"{girl.full_name}", f"girl|{girl_id}"))

        menu_options.append(("No", "None"))

        menu_choice = renpy.display_menu(menu_options)

    if menu_choice == "mmf_threesome":
        "He eagerly accepts and locks the bathroom behind him."

        $ se_participants.append(GameCharacter(first_name=renrandom.choice(database_male_first_names)))
    elif menu_choice == "None":
        "You and [selected_girl] step into an empty stall and close the door behind you."
    else:
        $ girl_id = menu_choice.split("|")[-1]
        $ girl = academy.get_girl_by_id(girl_id)

        $ girl_acceptance = girl.get_acceptance_by_name("sex_interaction")
        if girl_id == barista_id:
            player.character "You know, things are heating up over here. How about you join us in the bathroom for a little... private break?"

            if girl_acceptance >= 40:
                girl.character "A break, huh? You're trouble, but I'm in."

                "She glances around, then calls out to a coworker."

                girl.character "Hey, cover the counter for me. I'll be back in a bit!"

                "She wipes her hands on her apron, smirking as she steps out from behind the counter to follow you."

                $ se_participants.append(girl)
            elif girl_acceptance >= 20:
                girl.character "Are you serious? I'm working here. Not running off to the bathroom with you!"

                "She plants her hands on her hips, her tone sharp as she glares at you over the espresso machine."

                girl.character "Take your coffee and your ideas elsewhere. Some of us have jobs to do."

                "The clatter of cups behind her punctuates her rejection."

                $ girl.apply_impacts({"affection": -100})
            else:
                girl.character "What did you just say? That's it! Out! Both of you!"

                "Her face flushes with anger as she storms around the counter, pointing toward the door."

                girl.character "I'm not dealing with this nonsense. Get out before I call someone!"

                "She marches to the door, flips the lock with a loud click, and shoves it open, glaring until you and [selected_girl] stumble out."

                $ remove_girl_id_from_location(selected_girl.id, "girls_in_coffee_shop")

                if "coffee_shop" not in girls_blocking_area:
                    $ girls_blocking_area["coffee_shop"] = []

                $ girls_blocking_area["coffee_shop"].append(girl.id)

                $ vt_coffee_booth_bathroom_visit = None
                $ vt_booth_end_encounter(selected_girl)

                $ girl.apply_impacts({"affection": -2000})

                return "show_mall"
        else:
            player.character "Hey, [girl], wanna join us in our private {i}booth{/i}?"

            if girl_acceptance >= 40:
                girl.character "Absolutely! Count me in!"

                $ se_participants.append(girl)
            elif girl_acceptance >= 20:
                "[girl] scowls at you, clearly repulsed."

                girl.character "No, I don't think so..."

                $ girl.apply_impacts({"affection": -500, "fear": 500})
            else:
                "[girl] glares at you, her disgust obvious."

                girl.character "You are disgusting! Not a chance!"

                $ girl.apply_impacts({"affection": -1000, "fear": 1000})

    scene black with dissolve

    scene bg coffee_shop_bathroom with dissolve

    return "start_sex_interaction"

label vt_coffee_booth_bathroom_end:
    $ _vt_coffee_resume = vt_coffee_booth_restore()
    if not _vt_coffee_resume:
        if not time_manager.is_mall_hours():
            $ _vt_coffee_line = vt_booth_choice(selected_girl, VT_COFFEE_BOOTH_CLOSING)
            "[_vt_coffee_line]"
        jump show_coffee_shop
    scene bg coffee_shop with dissolve
    if selected_girl.image_manager.has_fullbody_image():
        $ body_image = fit_image_to_size(selected_girl.image_manager.get_fullbody_image(), 1500, 1500)
        show expression body_image as talker_body_image at dialogue_position
    $ _vt_coffee_line = vt_booth_choice(selected_girl, VT_COFFEE_BOOTH_BATHROOM_RETURN).replace("[selected_girl]", str(selected_girl))
    "[_vt_coffee_line]"
    call vt_coffeeshop_booth_resume
    jump expression _return
