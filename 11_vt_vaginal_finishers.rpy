# VT scene ownership. Outcomes are resolved by the existing impact hooks; no new rolls.
# The transient options exist only during synchronous impacts and are cleared before text.
default vt_owned_finish_options = None

init -3 python:
    VT_FINISH_CONTAINED = [
        "The last tension leaves you, and you go still. The condom has held, keeping your release contained.",
        "A moment passes before your breathing evens out; your release stays in the intact condom.",
    ]
    VT_FINISH_INTERNAL = [
        "Your rhythm falters into stillness as you finish inside her, with no condom between you.",
        "The motion falters on a sharp breath. You finish inside her without a condom.",
    ]
    VT_FINISH_BREAK = [
        "You fall still, but the torn condom has let your release through inside her. She knows it has failed.",
        "The pause has a different weight: the condom hasn't held, and you have finished inside her. She knows it too.",
    ]
    VT_FINISH_BREAK_UNNOTICED = [
        "Your breath comes unevenly as the moment passes. The torn condom has let your release reach her, though she has not noticed.",
        "The movement ebbs. She remains unaware that the condom hasn't held and your release has reached her.",
    ]
    VT_FINISH_EXTERNAL = [
        "You pull out in time, finishing against her rather than inside her. The hurried movement gives way to stillness.",
        "A quick withdrawal interrupts the rhythm. Your release lands outside her, and the hurried moment is over.",
    ]
    VT_FINISH_EXTERNAL_CONTACT = [
        "Your breath catches as you finish against her, leaving your release outside. The movement subsides into stillness.",
        "The moment ends with your release against her lower body, not inside her. You go still, breathing unevenly.",
    ]
    VT_FINISH_EXTERNAL_CONTACT_LEAK = [
        "As you finish against her, some of your release escapes at the condom's base. The leak is already against her as you go still.",
        "Your breathing turns uneven as you finish. The condom has leaked at the base, leaving some of your release on her.",
    ]
    VT_FINISH_EXTERNAL_LEAK = [
        "You pull clear, but the condom hasn't kept everything contained: some of your release escapes at the base onto her.",
        "The rhythm breaks as you withdraw. You finish outside her, but a leak at the condom's base leaves some of your release against her.",
    ]
    VT_FINISH_REPLIES = {
        "contained": {
            "demure": ["That is a relief. Let us not hurry the moment.", "I should like a little quiet just now.", "Please be careful. I'd like everything to stay where it belongs."],
            "shy": ["Oh. That's a relief.", "I'm not in a hurry for anything else, okay?", "Careful with the condom. I'd rather not have a mess."],
            "neutral": ["That's a relief.", "All right. I'm choosing what happens next, though.", "Careful now. Let's keep everything in the condom."],
            "direct": ["Good. No surprises, please.", "I'm in no hurry for a repeat.", "Keep the mess in the condom, okay?"],
            "explicit": ["Well, that's a relief.", "Easy. I'm not ready to jump straight into something else.", "Careful with that condom. No spilling it now."],
            "crude": ["Well, that's a damn relief.", "I'm in no hurry for another round.", "Keep that mess in the condom, all right?"],
        },
        "break": {
            "demure": ["The condom has torn. I would like us to take that seriously.", "That is a broken condom. We need to decide what to do.", "Please, no guessing. Let us work out what happened."],
            "shy": ["It's torn. What are we going to do?", "The condom broke... I need a straight answer about this.", "Please don't brush off that tear."],
            "neutral": ["The condom broke. What do we do now?", "That tear matters. Let's think this through.", "I want to talk about the broken condom before anything else."],
            "direct": ["It's broken. Don't brush it off.", "The condom tore. We need a plan.", "No guessing. We need to deal with that tear."],
            "explicit": ["The condom broke. I need a straight answer here.", "It's torn. Let's take that seriously.", "That tear isn't something to shrug off."],
            "crude": ["Shit, it's broken. What do we do now?", "The condom tore. Don't brush that off.", "That damn tear matters. We need to talk."],
        },
        "unaware": {
            "demure": ["I would prefer a little quiet just now.", "I am feeling rather dazed.", "I would rather you asked how I am than guessed."],
            "shy": ["Can we just be quiet for a moment?", "I'm a little dazed. That's all I know how to say.", "You can ask how I am, you know."],
            "neutral": ["I'd like a little quiet.", "I'm a little dazed. Don't read too much into it.", "I'd rather you asked how I am than guessed."],
            "direct": ["Quiet for a minute, okay?", "I'm a little dazed. Don't make a big thing of it.", "Ask me how I am. Don't guess."],
            "explicit": ["I'd like a little quiet right now.", "I'm still feeling dazed.", "You can ask how I am instead of guessing."],
            "crude": ["Quiet for a minute, all right?", "I'm a bit dazed. Don't make a damn thing of it.", "Ask me how I am. Don't guess."],
        },
        "agreed": {
            "demure": ["I meant what I said. We may leave it at that.", "I am glad I could make that choice.", "I needn't explain every feeling all at once."],
            "shy": ["I did mean it. I'm just a little overwhelmed.", "I'm glad I got to choose.", "Can we leave some of this unsaid for now?"],
            "neutral": ["I meant it. Let's leave it at that.", "I'm glad I got to choose.", "There's a lot going through my head."],
            "direct": ["I meant it. I can speak for myself.", "That was my choice. I like being clear about it.", "I have mixed feelings. Let me have them."],
            "explicit": ["Yes, I meant it. Don't make me give a speech about it.", "I'm glad that was my call.", "I'm still sorting out how I feel."],
            "crude": ["I meant it. Don't make a damn ceremony out of it.", "Good. That was my call.", "I'm allowed to feel more than one damn thing."],
        },
        "external": {
            "demure": ["Well. I should like a moment to compose myself.", "I would like to clean up before anything else.", "Please give me a little room to sort myself out."],
            "shy": ["Oh. Let me sort myself out, okay?", "I'd like to clean up first.", "Could you give me a little room?"],
            "neutral": ["Well, that's quite a finish.", "I'd like to clean up before anything else.", "Give me a little room to sort myself out."],
            "direct": ["Well. That's quite a finish.", "I want to clean up first.", "A little room, please."],
            "explicit": ["Well, that's one thing to deal with.", "I'd like to clean up before deciding anything else.", "Give me some room to sort myself out."],
            "crude": ["Well, that's a mess to deal with.", "I'd like to clean up first.", "A little room, all right?"],
        },
    }
    VT_FINISH_CONTEXT_REPLIES = {
        "warm_reserved": {
            "demure": ["I do like having you here. I am simply not very good at saying so.", "Please be kind to me for a moment.", "I don't mind being a little shy with you."],
            "shy": ["I like being here with you. I'm just not very good at saying it.", "Be kind to me for a minute, will you?", "I don't mind being shy with you."],
            "neutral": ["I like having you here. The words are taking a little longer.", "A little kindness would go a long way right now.", "I don't mind being shy with you."],
            "direct": ["I like being here. I'm just not ready with a speech.", "Be kind to me for a minute, okay?", "I don't mind you seeing me a little shy."],
            "explicit": ["I like having you here. Don't make me get eloquent about it.", "Be kind to me for a moment, will you?", "I don't mind being shy around you."],
            "crude": ["I like being here with you. I'm just lousy at saying it.", "Be kind to me for a minute, all right?", "I don't mind you seeing me shy. Don't make a damn thing of it."],
        },
        "warm_familiar": {
            "demure": ["We need not fill every silence, you know. I rather like this one.", "I like not having to put on a performance with you.", "You do make it rather difficult to remain sensible."],
            "shy": ["We don't have to fill the silence. I like this part too.", "I like not having to put on an act with you.", "You're rather hard to be sensible around."],
            "neutral": ["You don't have to fill the silence. I like this part too.", "I like not having to put on an act with you.", "You're rather hard to be sensible around."],
            "direct": ["We can leave the silence alone. I like it.", "I like that I don't have to put on a performance with you.", "You make it difficult to stay sensible."],
            "explicit": ["Don't feel you have to fill the silence. I like this too.", "I like being myself with you.", "So much for being sensible around you."],
            "crude": ["Leave the silence alone. I like this part too.", "I like not having to put on a damn act with you.", "So much for being sensible around you."],
        },
        "playful": {
            "demure": ["If you are waiting for a clever remark, you may be waiting some time.", "Do not start looking pleased with yourself. I have not composed my review.", "I seem to have misplaced my dignity. Kindly pretend not to notice."],
            "shy": ["If you're waiting for a clever remark, you'll have to give me a minute.", "Don't start looking smug. I haven't worked out my review yet.", "I seem to have lost my composure. Could you pretend you didn't notice?"],
            "neutral": ["If you're waiting for a clever remark, you'll have to give me a minute.", "Don't start looking smug. I haven't written your review yet.", "I seem to have misplaced my dignity. Pretend you didn't notice."],
            "direct": ["My clever remark will have to wait.", "Don't get smug. Your review isn't finished.", "I've misplaced my dignity. You saw nothing."],
            "explicit": ["I had a clever remark ready. Apparently it's gone now.", "Don't get smug. I haven't decided what to put in your review.", "So much for my composure. You're going to pretend you missed that."],
            "crude": ["My clever remark has gone to hell. You'll have to wait.", "Don't get smug. The damn review isn't finished.", "There goes my dignity. You saw nothing, all right?"],
        },
        "reserved": {
            "demure": ["Must we find words for everything immediately?", "I am not quite ready to meet your eyes just yet.", "Please don't make a great occasion of my embarrassment."],
            "shy": ["We don't have to talk about everything right away, do we?", "I know I'm being quiet. I'm just embarrassed.", "Please don't make a big thing of me blushing."],
            "neutral": ["Can we leave some things unsaid for a moment?", "I'm being quiet because I'm embarrassed, all right?", "Please don't make a big thing of it."],
            "direct": ["Let me be quiet without turning it into a question.", "I'm embarrassed. You don't need to point it out.", "Don't make a big thing of this."],
            "explicit": ["I can be quiet without having an answer ready.", "Yes, I'm embarrassed. Don't start teasing.", "Don't make me explain every look on my face."],
            "crude": ["Let me be quiet without making a damn thing of it.", "I'm embarrassed, all right? Don't start.", "Don't make me explain every look on my face."],
        },
        "reserved_mother": {
            "demure": ["I should like to recover a little of my composure first.", "There are occasions when a measured silence is quite sufficient.", "I would rather choose my own words than be prompted."],
            "shy": ["I would like a little of my composure back first.", "A little silence isn't something we have to fix.", "Let me choose my own words, please."],
            "neutral": ["I'd like some of my composure back first.", "A little silence isn't a problem we have to solve.", "I'd rather choose my own words."],
            "direct": ["Let me get my composure back.", "We don't have to fix every silence.", "I'll choose my own words, thank you."],
            "explicit": ["Give me a chance to recover my composure.", "Silence isn't always an invitation to ask questions.", "Let me choose how I say this."],
            "crude": ["Let me get my composure back, all right?", "We don't need to fix every damn silence.", "I'll find my own words. Give me a chance."],
        },
        "uneasy": {
            "demure": ["I need a little space, please.", "I wish I could feel less tense.", "I would rather you told me what you are thinking."],
            "shy": ["Could I have a little space?", "I wish I didn't feel so tense.", "What are you thinking? I can't tell."],
            "neutral": ["I need a little space, please.", "I wish I felt less tense.", "Tell me what you're thinking. I can't read you."],
            "direct": ["Give me some space.", "I'm tense. I'm not going to pretend otherwise.", "Tell me what you're thinking instead of leaving me to guess."],
            "explicit": ["I need some space. Don't rush me.", "I'm still tense. I'm not putting on a happy face.", "What are you thinking? I'd rather hear it from you."],
            "crude": ["Give me some space, all right?", "I'm still fucking tense. I'm not pretending otherwise.", "Tell me what's going through your head."],
        },
        "practical": {
            "demure": ["One decision at a time, please.", "I would rather think clearly than find something flattering to say.", "Let us not rush straight into the next thing."],
            "shy": ["Can we take one thing at a time?", "I'd rather get my thoughts straight than find the right answer.", "We don't have to rush into anything else, do we?"],
            "neutral": ["One thing at a time, all right?", "I'd rather think clearly than find something flattering to say.", "There's no need to rush into the next thing."],
            "direct": ["One decision at a time.", "I'd rather be clear than flattering.", "Let's not rush the next thing."],
            "explicit": ["One thing at a time. I like to know what I'm deciding.", "I'd rather give you a straight answer than a pretty one.", "No need to hurry into the next thing."],
            "crude": ["One damn thing at a time.", "I'd rather be straight with you than tell you what sounds good.", "Don't rush straight into the next thing."],
        },
        "break_connected": {
            "demure": ["The condom has torn. Please talk to me while we think this through.", "I do care for you, but that tear still matters.", "Let us deal with the broken condom together, rather than falling silent."],
            "shy": ["It broke. Please talk to me while we work out what to do.", "I like being with you, but I can't ignore that tear.", "The condom's torn. Don't leave me worrying about it on my own."],
            "neutral": ["The condom broke. Talk to me while we think this through.", "I like being with you, but that tear still matters.", "Let's deal with the broken condom together."],
            "direct": ["It broke. Talk to me. We'll work out what to do.", "I care about you. I'm still taking that tear seriously.", "The condom's torn. I don't want to worry about it on my own."],
            "explicit": ["The condom broke. Don't go quiet on me now.", "I care about you. That doesn't make the tear unimportant.", "Let's think through the broken condom together."],
            "crude": ["Shit, it's broken. Talk to me while we work this out.", "I care about you. I'm still taking that damn tear seriously.", "The condom's torn. Don't leave me worrying about it alone."],
        },
        "break_uneasy": {
            "demure": ["It has torn. Please do not tell me that is nothing.", "The condom is broken. I need you to take that seriously.", "That tear matters. I need time to think."],
            "shy": ["It broke. Please don't tell me that's nothing.", "The condom's torn. I need you to take this seriously.", "Please don't brush off that tear. I'm worried."],
            "neutral": ["It broke. Please don't tell me that's nothing.", "The condom's torn. Take this seriously.", "That tear matters. I need time to think."],
            "direct": ["It's broken. Don't minimize it.", "The condom tore. Take that seriously.", "That tear matters. Let me think."],
            "explicit": ["It broke. Don't tell me it's nothing.", "The condom's torn. I need you to take this seriously.", "That tear matters. I'm not shrugging it off."],
            "crude": ["It's broken. Don't tell me it's nothing.", "The damn condom tore. Take it seriously.", "That tear matters. I'm not shrugging it off."],
        },
    }

    def vt_finish_reply_context(girl):
        # Wording only. Read existing facts directly: the general acceptance/context
        # helpers can update a cache or randomize tied acts, so neither is called here.
        fear = getattr(girl, "fear", 0)
        pressure = getattr(girl, "pressure", 0)
        affection = getattr(girl, "affection", 0)
        corruption = getattr(girl, "corruption", 0)
        naturism = getattr(girl, "naturism", 0)
        approach = getattr(girl, "dominant_approach", None)
        history = getattr(girl, "general_action_tracker", {})
        familiar = sum(history.get(act, 0) for act in ("fuck_pussy", "creampie_pussy")) >= 4
        if fear >= 50 or pressure >= 60:
            return "uneasy"
        if affection >= 60 and fear < 30 and pressure < 40:
            if familiar and corruption >= 50 and approach == "sexualized":
                return "playful"
            return "warm_familiar" if familiar and corruption >= 30 else "warm_reserved"
        if approach == "transactional":
            return "practical"
        if naturism < 30:
            return "reserved_mother" if isinstance(girl, Mother) else "reserved"
        return "neutral"

    def vt_finish_reply_pool(girl, outcome):
        context = vt_finish_reply_context(girl)
        # A known failure always has an informed, concerned reply. An unnoticed
        # failure never borrows these lines, even from an otherwise warm character.
        if outcome == "break":
            if context == "uneasy":
                return VT_FINISH_CONTEXT_REPLIES["break_uneasy"]
            if context in ("warm_reserved", "warm_familiar", "playful"):
                return VT_FINISH_CONTEXT_REPLIES["break_connected"]
            return VT_FINISH_REPLIES[outcome]
        return VT_FINISH_CONTEXT_REPLIES.get(context, VT_FINISH_REPLIES[outcome])

    def vt_vaginal_buildup_text(girl, condom_used, broken, aware, first_in_session, first_with_player, virgin):
        # Exactly one two-way choice, as in the reviewed mechanical delivery.
        if first_in_session:
            pool = ["You begin, and a rhythm takes shape with the condom in place.", "A brief shift, then you start to find the pace, the condom still between you."] if condom_used else ["You begin without a condom between you, taking a moment to find the pace.", "You start without protection, and the first uncertain rhythm grows steadier."]
        else:
            pool = ["You continue the rhythm, the condom still in place.", "The movement carries on; you find the pace again, still protected by the condom."] if condom_used else ["You continue the rhythm without a condom between you.", "The pace carries on, still without the barrier of a condom."]
        if broken:
            pool = ["The movement continues, but the torn condom is no longer a barrier.", "The pace carries on with the damaged condom still in place; it no longer keeps you covered."]
        text = renpy.random.choice(pool)
        if first_with_player:
            text += " This is your first time with her like this; there is no familiar pace to fall back on yet."
            if virgin:
                text += " At the initial resistance, you pause before continuing."
        if broken:
            text += " She knows it has torn." if aware else " She has not noticed the tear."
        return text

    def vt_internal_finish_available(girl):
        # The ordinary chooser is after the buildup's protection negotiation. A known
        # failure cannot bypass the registered action's existing protection boundary.
        return (not vt_condom_now(girl, "vaginal") or
                (player.condom_active != "raw" and
                 (not player.condom_broke or not girl.aware_vaginal_condom)))

    def vt_apply_owned_finish(action_name, skip_descriptions, skip_responses, origin_action=None):
        previous = store.vt_owned_finish_options
        store.vt_owned_finish_options = {
            "skip_responses": skip_responses,
            "permission": vt_accepts_creampie(selected_girl) or (store.is_during_sex_interaction and selected_girl.id in store.vt_creampie_session),
            "withdrawal": bool(store.vt_pullout_external_active or
                               (origin_action and "fuck_pussy" in origin_action)),
            "first_with_player": selected_girl.first_time_pussy,
            "virgin": selected_girl.hymen,
        }
        try:
            apply_action_impacts(action_name)
            return store.vt_owned_finish_options.get("narration", [])
        finally:
            store.vt_owned_finish_options = previous

    def vt_resolved_finish_narration(girl, internal, condom_used, pregnancy_risk):
        """Consume the hook's resolved exposure, without another break or conception roll.

        Hooks own the semen unit, conception and progression. Only the VT scene owns
        splatter. Legacy base callers retain their own scene effects and narration.
        """
        options = store.vt_owned_finish_options
        if options is None:
            return False
        broken = bool(condom_used and player.condom_broke)
        aware = bool(girl.aware_vaginal_condom if internal else
                     (girl.aware_vaginal_condom or girl.aware_pussy_cumshot_condom))
        external_description = VT_FINISH_EXTERNAL if options["withdrawal"] else VT_FINISH_EXTERNAL_CONTACT
        if not internal and condom_used:
            player.condom_cum = 0 if broken else player.condom_cum + 1
        if pregnancy_risk:
            target = "in_pussy" if internal else "pussy"
            player.cum_splatter_girl(target, girl)
            player.cum_splatter_clothes(target, girl)
        # The gate owns the distinct accident/force narration and reaction after this action.
        if internal and store.vt_force_creampie_active:
            return True
        if not pregnancy_risk:
            descriptions = VT_FINISH_CONTAINED
            reply = "contained"
        elif broken:
            descriptions = VT_FINISH_BREAK if aware else VT_FINISH_BREAK_UNNOTICED
            reply = "break" if aware else "unaware"
            if not internal:
                descriptions = external_description
        elif internal:
            descriptions = VT_FINISH_INTERNAL
            reply = "agreed" if options["permission"] else "unaware"
        else:
            descriptions = (VT_FINISH_EXTERNAL_LEAK if options["withdrawal"] else VT_FINISH_EXTERNAL_CONTACT_LEAK) if condom_used else external_description
            reply = "external"
        text = renpy.random.choice(descriptions)
        if internal and options["first_with_player"]:
            text = "This is your first time with her like this; there is no familiar pace to fall back on yet. " + text
            if options["virgin"]:
                text = "At the initial resistance, you pause before continuing. " + text
        vt_queue_finisher_narration("vt_fetish_dialog", text)
        # Withdrawal's negotiated/adverse reply is emitted by its gate, after the act.
        if not options["skip_responses"] and not store.vt_pullout_external_active:
            vt_queue_finisher_narration("vt_finish_girl_reply", vt_voice(girl, vt_finish_reply_pool(girl, reply), "Give me a moment."))
        return True

# Registered action objects and chooser dictionaries keep their identities/requirements/costs.
# Run after their normal registration. Retain old entry labels for saved callers.
init 999 python:
    def vt_route_owned_vaginal_actions():
        routes = {
            "fuck_pussy": (("sex_fuck_pussy", "vt_first_time_gate_vaginal"), "vt_direct_vaginal_buildup"),
            "cumshot_pussy": (("sex_cumshot_pussy",), "vt_direct_withdrawal"),
        }
        for actions in database_sex_options.values():
            for action in actions:
                route = routes.get(action.action_entry_name)
                if route and action.label == "vt_condom_attempt_gate" and getattr(action, "vt_real_label", None) in route[0]:
                    action.vt_real_label = route[1]
        internal = database_cum_targets.get("creampie_pussy", {})
        protection = "vt_internal_finish_available(girl)"
        original = internal.get("requirements", "True")
        if protection not in original:
            internal["requirements"] = f"({original}) and ({protection})"
        target = database_cum_targets.get("pussy", {})
        if target.get("option_label") == "generic_action_cumshot_pussy":
            target["option_label"] = "vt_withdrawal_finisher"
    vt_route_owned_vaginal_actions()

label vt_finish_girl_reply(dialogtext):
    selected_girl.character "[dialogtext]"
    return

label vt_direct_withdrawal:
    call vt_withdrawal_finisher(additional_subtags=se_additional_webm_sub_tags, skip_descriptions=sex_skip_descriptions, skip_responses=sex_skip_responses)
    return

label vt_vaginal_finisher(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False, _vt_finish_action="creampie_pussy"):
    $ _vt_finish_lines = vt_apply_owned_finish(_vt_finish_action, skip_descriptions, skip_responses, action_name)
    if action_name:
        $ media_helper.show_video(f"{_vt_finish_action}_{action_name}", selected_girl, sub_tags=additional_subtags, default_to=_vt_finish_action)
    else:
        $ media_helper.show_video(_vt_finish_action, selected_girl, sub_tags=additional_subtags)
    call vt_finisher_action_continuation(narration=_vt_finish_lines)
    if skip_descriptions and skip_responses:
        if currently_playing_video:
            pause
        else:
            $ renpy.notify("No videos for action found")
    $ media_helper.hide_video()
    return

label vt_withdrawal_finisher(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    call vt_vaginal_finisher(action_name=action_name, additional_subtags=additional_subtags, skip_descriptions=skip_descriptions, skip_responses=skip_responses, _vt_finish_action="cumshot_pussy")
    return

label vt_direct_vaginal_buildup:
    # Preserve the optional local first-time presentation without requiring that WIP script.
    if renpy.has_label("vt_first_time_gate_vaginal") and selected_girl.hymen and selected_girl.first_time_pussy:
        $ _vt_optional_first_time_label = "vt_first_time_gate_vaginal"
        call expression _vt_optional_first_time_label
    else:
        call vt_vaginal_buildup(additional_subtags=se_additional_webm_sub_tags, skip_descriptions=sex_skip_descriptions, skip_responses=sex_skip_responses)
    return

label vt_vaginal_buildup(additional_subtags=None, skip_descriptions=False, skip_responses=False, force_cum=False, ask_to_cum=False, force_orgasm=False, can_deny_orgasm=True):
    # The hook supplies insertion/first/repeat text once; the rest mirrors the base action.
    $ apply_action_impacts("fuck_pussy")
    $ media_helper.show_video("fuck_pussy", selected_girl, additional_subtags)
    if skip_descriptions and skip_responses:
        if currently_playing_video:
            pause
        else:
            $ renpy.notify("No videos for action found")
    if persistent.ask_to_cum_early and person_doing_action == player and not player.just_came and player.is_edging():
        $ ask_to_cum = True
    if ask_to_cum and not force_cum and not person_doing_action.just_came:
        menu:
            "Stop before you cum":
                $ force_cum = False
            "Don't hold back":
                $ force_cum = True
    if force_cum and not person_doing_action.just_came:
        $ person_doing_action.cum()
    $ can_deny_orgasm = can_deny_orgasm and not force_orgasm
    if force_orgasm and not selected_girl.just_came:
        $ selected_girl.just_came = True
    if selected_girl.just_came:
        call generic_action_orgasm("fuck_pussy", additional_subtags=additional_subtags, skip_descriptions=skip_descriptions, skip_responses=skip_responses, can_deny_orgasm=can_deny_orgasm)
        if player.just_came:
            call generic_action_player_choose_cum(action_name="fuck_pussy", additional_subtags=additional_subtags, skip_descriptions=skip_descriptions, skip_responses=skip_responses)
    elif player.just_came:
        call generic_action_player_choose_cum(action_name="fuck_pussy", additional_subtags=additional_subtags, skip_descriptions=skip_descriptions, skip_responses=skip_responses)
    else:
        if not skip_descriptions:
            $ girl_reaction = selected_girl.get_reaction_for_action("fuck_pussy")
            if girl_reaction:
                "[girl_reaction]"
        if not skip_responses:
            $ girl_response = selected_girl.get_response_for_action("fuck_pussy")
            if girl_response:
                selected_girl.character "[girl_response]"
            $ person_doing_action_response = player.get_response_for_action("fuck_pussy", selected_girl)
            if person_doing_action_response:
                person_doing_action.character "[person_doing_action_response]"
    $ media_helper.hide_video()
    return
