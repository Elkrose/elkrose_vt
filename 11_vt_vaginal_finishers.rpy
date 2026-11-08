# VT scene ownership. Outcomes are resolved by the existing impact hooks; no new rolls.
# The transient options exist only during synchronous impacts and are cleared before text.
default vt_owned_finish_options = None

init -3 python:
    VT_FINISH_CONTAINED = [
        "You drive in deep and cum hard, the condom catching every pulse. It holds, and you go still inside her, breathing hard.",
        "Your rhythm breaks as you cum into the condom. It holds, and for a moment neither of you moves.",
    ]
    # External containment never borrows insertion/inside-her narration.
    VT_FINISH_EXTERNAL_CONTAINED = [
        "You cum hard into the condom. It holds, and you pull back carefully to keep it that way.",
        "Your release fills the tip of the condom, and it holds. You ease back, breathing hard.",
    ]
    VT_FINISH_INTERNAL = [
        "You thrust deep against her cervix in time with your thick white ropes filling her womb, pulse after pulse until you're spent.",
        "Your rhythm stutters as you cum, filling her deep. You groan as you drain your balls inside her.",
    ]
    VT_FINISH_BREAK = [
        "You cum deep inside her, and only then does the torn condom show itself. She knows it failed, and she knows where it all went.",
        "You finish inside her, but the condom hasn't held. She feels it too, and the heat drains out of the moment.",
    ]
    VT_FINISH_BREAK_UNNOTICED = [
        "You cum inside her and catch your breath. The condom has torn and let it through, though she hasn't noticed.",
        "The moment ebbs as you finish. The torn condom hasn't kept anything from her, and she has no idea.",
    ]
    VT_FINISH_EXTERNAL = [
        "You pull out just in time and cum over her pussy and belly, hot against her skin.",
        "You pull out at the last second and spill across her skin.",
    ]
    VT_FINISH_EXTERNAL_CONTACT = [
        "You grind against her and cum, spilling over her pussy rather than inside it.",
        "Your breath catches as you finish against her, leaving her slick with your cum on the outside.",
    ]
    VT_FINISH_EXTERNAL_CONTACT_LEAK = [
        "You cum against her, and some of it squeezes out past the base of the condom onto her skin.",
        "As you finish against her, the condom leaks at the base, leaving a smear of your cum on her.",
    ]
    VT_FINISH_EXTERNAL_LEAK = [
        "You pull out and finish, but the condom leaks at the base and some of it ends up on her.",
        "You withdraw as you cum. The condom doesn't hold it all, and some leaks out across her.",
    ]
    VT_FINISH_REPLIES = {
        "contained": {
            "demure": ["Oh my. That was rather more than I expected.", "I'm glad the condom held. Let me catch my breath.", "Please be careful taking that off."],
            "shy": ["Th-that was a lot... I'm glad it held.", "C-careful with the condom, okay?", "I... need a second. That was intense."],
            "neutral": ["Wow. Okay. Good thing that held.", "Careful pulling out, okay?", "That was intense. Give me a second."],
            "direct": ["Good. It held.", "Careful pulling out. Keep that condom on until you're clear.", "That was good. Give me a sec."],
            "explicit": ["Mmm, I felt you throbbing in there. Good thing it held.", "God, that was good. Careful pulling out.", "That was hot. Pull out slow so it doesn't spill."],
            "crude": ["Fuck, I felt you pumping in there. Good thing it held.", "Damn, that was good. Pull out slow, don't spill it.", "Shit, that was hot. Keep that thing on till you're clear."],
        },
        "break": {
            "demure": ["The condom tore, and you finished inside me. We need to talk about this now.", "That is not what I agreed to. What do we do?", "Please don't brush this off. It broke."],
            "shy": ["I-it broke... and you... inside me... what do we do?", "The condom tore, didn't it? I can tell.", "Please don't say it's fine. It broke."],
            "neutral": ["It broke. You came inside me. What now?", "That condom tore. We need to figure this out.", "Don't brush this off. That was inside me."],
            "direct": ["It broke, and you came in me. We need a plan.", "Don't shrug this off. That tore.", "That's not what we agreed. What now?"],
            "explicit": ["Shit, it tore. You came right inside me.", "That's not how I wanted that. We need to deal with this.", "That condom's done, and so is the mood. What now?"],
            "crude": ["Fuck, it broke. You dumped it right in me.", "Shit, that's all inside me now. What the hell do we do?", "Damn thing tore. Don't you dare shrug that off."],
        },
        "unaware": {
            "demure": ["My goodness. I need a moment.", "I'm rather dazed, I'm afraid.", "I'd like you to ask how I am, rather than guess."],
            "shy": ["I... I need a second.", "My head's spinning a little...", "C-can we just stay quiet a moment?"],
            "neutral": ["Wow. I need a minute.", "I'm a little dazed.", "Ask me how I'm doing. Don't just guess."],
            "direct": ["Give me a minute.", "Whew. I'm dazed.", "Ask me how I am. Don't guess."],
            "explicit": ["Fuck... my legs are shaking.", "God. Give me a second to come down.", "I'm still buzzing. Don't move yet."],
            "crude": ["Fuck me... give me a damn minute.", "Shit, I can't think straight.", "Hold still, I'm still coming down."],
        },
        "agreed": {
            "demure": ["Goodness, that's... quite nice.", "Oh, my... let me have this moment.", "Well... I certainly didn't mind THAT..."],
            "shy": ["I... I'm glad I let you.", "I can still feel it... it's warm.", "Oh... wow... it's so much..."],
            "neutral": ["Yeah... that feels nice...", "I can still feel you. Give me a minute.", "I like feeling your seed inside me."],
            "direct": ["Ahhh... that feels so good.", "I can feel your cum flooding me.", "Stay there a second. I can still feel you."],
            "explicit": ["Mmm, I can feel your cum deep inside...", "God, I love feeling you fill me up.", "Fuck, feeling you flood me was the right call."],
            "crude": ["Fuck yes. Mmmm, I can feel it in my womb.", "Damn, you filled me up good. Fuck, that's hot...", "Oh, fuck, yes... so much fucking cum!"],
        },
        "external": {
            "demure": ["Well. I should like to clean up, please.", "That is... quite a mess. A moment, please.", "Please hand me something to tidy up with."],
            "shy": ["Oh... it's everywhere. C-can I clean up?", "Um... could you pass me something to wipe with?", "That's... a lot. Let me sort myself out."],
            "neutral": ["Well, that's quite a mess.", "Pass me something to clean up with?", "Give me a second to sort myself out."],
            "direct": ["That's a mess. Hand me a towel.", "Okay. Cleanup first.", "A little room, please. I need to wipe off."],
            "explicit": ["Look at the mess you made on me.", "Mmm, that's a lot. Hand me something to wipe off with.", "You really covered me. Let me clean up."],
            "crude": ["Fuck, look at this mess.", "Damn, you plastered me. Hand me something.", "Shit, it's all over me. Give me a sec."],
        },
    }
    VT_FINISH_EXTERNAL_CONTAINED_REPLIES = {
        "demure": ["Oh my. That was rather more than I expected.", "I'm glad the condom held. Let me catch my breath.", "Please be careful taking that off."],
        "shy": ["Th-that was a lot... I'm glad it held.", "C-careful with the condom, okay?", "I... need a second. That was intense."],
        "neutral": ["Wow. Okay. Good thing that held.", "Careful with the condom, okay?", "That was intense. Give me a second."],
        "direct": ["Good. It held.", "Keep that condom on until you're clear.", "That was good. Give me a sec."],
        "explicit": ["Mmm... don't move yet. Let me enjoy that.", "That's more like it. Give me a second to catch up.", "God. Okay... I need a breath."],
        "crude": ["Fuck... okay. Give me a second.", "Damn. That was something. Hang on.", "Shit, I need a minute after that."],
    }
    VT_FINISH_CONTEXT_REPLIES = {
        "warm_reserved": {
            "demure": ['I am glad you are here, even if I seem a little flustered.', 'Being close to you matters to me. Saying so is the difficult part.', 'You have left me rather flustered.'],
            "shy": ["I'm glad you're here. Even if I'm hiding my face.", "I like being close to you. I'm just not very good at saying it.", "Please don't tease me for being shy."],
            "neutral": ["I'm glad you're here. There, I managed to say it.", "I like having you this close, even if I'm not saying much.", "Be kind. I'm feeling a little shy."],
            "direct": ["I like having you here. That's what I'm trying to say.", 'You caught me off guard. In a good way.', "You can spare me the teasing. I'm feeling shy enough."],
            "explicit": ["I wasn't expecting to feel this shy around you.", 'I like having you this close. The words can wait.', "Be nice. I'm more shy around you than I expected."],
            "crude": ['I like having you here, all right? There, I said it.', "You've caught me off guard. In a good way.", "Don't start teasing. I'm feeling shy enough already."],
        },
        "warm_familiar": {
            "demure": ['Stay a little longer. Your company is rather welcome.', 'It is a comfort knowing I can be myself with you.', 'You do have a way of making me lose my train of thought.'],
            "shy": ['Stay a little longer? I like this part with you.', "I don't feel like I have to impress you. That's nice.", "It's easy being here with you."],
            "neutral": ['Stay a little longer. I like having you here.', 'I like that I can just be myself with you.', "We don't have to rush off, do we?"],
            "direct": ["I'm happy right here with you.", 'I can be myself with you. That matters.', "I'm in no hurry to end this moment."],
            "explicit": ["Don't rush off. I like having you to myself.", "I don't have to put on a show with you. I like that.", 'Stay close a little longer, will you?'],
            "crude": ['Stay a while, will you? I like having you around.', "I can just be myself with you. Fuck, that's a relief.", "We're not in that much of a hurry. Stay with me."],
        },
        "playful": {
            "demure": ['You look altogether too pleased with yourself.', 'I had a perfectly good reply a moment ago. It seems to have deserted me.', 'There goes my attempt to look composed.'],
            "shy": ["You're looking awfully pleased with yourself.", "Don't grin at me like that. You're making me blush.", 'I had something clever to say. Now look at me...'],
            "neutral": ["Look at that grin. You're pleased with yourself.", "Don't let this go to your head.", 'So much for playing it cool.'],
            "direct": ['You look far too pleased with yourself.', "Don't let it go to your head.", 'I was going to say something clever. There goes that plan.'],
            "explicit": ["Look at that grin. I know exactly what you're thinking.", "Don't get too pleased with yourself just yet.", 'I was trying to look composed. You can see how well that went.'],
            "crude": ["Look at that damn grin. You're enjoying yourself.", "Don't let it go to your head, all right?", 'I had a smart answer ready. Where the hell did it go?'],
        },
        "reserved": {
            "demure": ['I am not quite ready to put that into words.', 'I would like a little quiet while I collect myself.', 'I know I am blushing. Please be kind.'],
            "shy": ["I'm not sure I can look you in the eye yet.", "I'm embarrassed. I just need a little quiet.", "Please don't point out that I'm blushing."],
            "neutral": ["I'm still trying to find my words.", "I'm feeling a little self-conscious. Can we be quiet for a bit?", "Be kind. I know I'm blushing."],
            "direct": ["I'm not ready to talk about it yet.", "I'm embarrassed. A little quiet would help.", 'Let me have a little space.'],
            "explicit": ["I haven't found the words yet.", "Yes, I'm embarrassed. Just give me a little quiet.", 'A little space would help me settle.'],
            "crude": ["I'm still finding my damn words.", "I'm embarrassed, all right? A bit of quiet would help.", 'Give me some room to collect myself.'],
        },
        "reserved_mother": {
            "demure": ['I am rather at a loss for words.', 'A little quiet would help me collect myself.', 'I seem to have misplaced my composure.'],
            "shy": ["I'm... not quite sure what to say.", 'Could I have a little quiet to collect myself?', "I'm feeling rather self-conscious all of a sudden."],
            "neutral": ["I'm still finding my words.", 'A little quiet would help me collect myself.', "I'm not feeling quite composed yet."],
            "direct": ["I'm at a loss for words.", 'Let me collect myself before we talk.', "I'm feeling self-conscious. Bear with me."],
            "explicit": ["I don't quite have the words yet.", 'A little quiet, please. I need to collect myself.', "You've caught me without my usual composure."],
            "crude": ["I'm still finding my damn words.", 'A little quiet, all right? I need to collect myself.', 'So much for keeping my composure.'],
        },
        "uneasy": {
            "demure": ['A little space would help, please.', 'I am not at ease. Please do not hurry me.', 'I would rather know what you are thinking than have to guess.'],
            "shy": ['Could you give me a little room?', "I'm not sure what to say. Please don't press me.", "What are you thinking? I can't tell."],
            "neutral": ['I could use some space.', "I don't feel settled yet. Please wait.", "Talk to me. I don't want to guess what you're thinking."],
            "direct": ['Give me some room.', "I'm tense. Don't hurry me along.", "Tell me what you're thinking. I need a straight answer."],
            "explicit": ['Back up a little. I need room.', "I'm not ready to put on a happy face.", 'Talk to me instead of leaving me to guess.'],
            "crude": ['Give me some damn room.', "I'm tense. Don't expect me to pretend otherwise.", "Tell me what's going through your head."],
        },
        "practical": {
            "demure": ['I could do with a little water.', 'Anything else can wait until we have settled ourselves.', 'There is no reason to hurry straight into the next thing.'],
            "shy": ['Could I have a sip of water?', "We don't have to rush off, do we?", "Let's not try to do everything at once."],
            "neutral": ['I could use some water.', "Everything else can wait until we're comfortable.", 'One thing at a time.'],
            "direct": ['I need some water after that.', "We don't need to rush straight on.", 'We can take our time.'],
            "explicit": ['A drink of water would be good right now.', "We're in no rush. Stay here a little.", "Let's get comfortable before anything else."],
            "crude": ['I could use some damn water.', "There's no prize for rushing off.", 'No rush. We can sort out the rest afterward.'],
        },
        "break_connected": {
            "demure": ['The condom has torn. Please stay with me while we consider what to do.', 'I care for you. I still need us to take that tear seriously.', 'Let us look at the broken condom together.'],
            "shy": ['It broke... stay with me while we work out what to do?', "I like being with you, but I can't ignore that tear.", "Please don't leave me worrying about the condom by myself."],
            "neutral": ['The condom broke. Stay with me while we work this out.', 'I care about you. The tear still matters.', "Let's look at the broken condom together."],
            "direct": ['It broke. Stay here and help me think.', "I care about you. I'm taking the tear seriously.", 'We need to deal with the broken condom together.'],
            "explicit": ["The condom broke. Don't go quiet on me now.", 'I care about you. I still need you to take the tear seriously.', 'Stay with me. We need to work out what to do about the condom.'],
            "crude": ['Shit, it broke. Stay here while we work this out.', "I care about you. That doesn't make the damn tear disappear.", "Help me think about the condom. Don't leave me worrying alone."],
        },
        "break_uneasy": {
            "demure": ['It has torn. Please do not dismiss my concern.', 'The condom is broken. I need you to take this seriously.', 'Please give me a moment to think about that tear.'],
            "shy": ["It broke... please don't tell me it doesn't matter.", "The condom's torn. I need you to listen to me.", "Give me a moment. I'm worried about that tear."],
            "neutral": ["It broke. Please don't brush that off.", "The condom's torn. I need you to take this seriously.", 'Give me a moment to think. That tear matters.'],
            "direct": ["It's broken. Don't minimize it.", 'The condom tore. Take that seriously.', 'Let me think about that tear before you say anything else.'],
            "explicit": ["It broke. Don't tell me it's nothing.", 'I need you to listen. The condom tore.', "I'm not shrugging that tear off. Give me a minute."],
            "crude": ["It's broken. Don't tell me it's nothing.", 'The damn condom tore. Listen to me.', "Give me a minute. I'm not brushing that tear off."],
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

    def vt_finish_reply_join(outcome_line, personality_line):
        # Keep the supplied outcome; avoid asking for the same pause twice.
        if any(phrase in personality_line.lower() for phrase in
               ("give me a second", "give me a minute", "give me a sec")):
            for ending in (" Give me a minute.", " Give me a second.",
                           " Give me a sec.", " Give me a second to catch up."):
                if outcome_line.endswith(ending):
                    outcome_line = outcome_line[:-len(ending)]
                    break
        return outcome_line + " " + personality_line

    def vt_finish_reply_pool(girl, outcome, internal=True):
        context = vt_finish_reply_context(girl)
        base = (VT_FINISH_EXTERNAL_CONTAINED_REPLIES if outcome == "contained" and not internal
                else VT_FINISH_REPLIES[outcome])
        # A known failure stays informed; an unnoticed one never borrows break replies.
        if outcome == "break":
            if context == "uneasy":
                return VT_FINISH_CONTEXT_REPLIES["break_uneasy"]
            if context in ("warm_reserved", "warm_familiar", "playful"):
                return VT_FINISH_CONTEXT_REPLIES["break_connected"]
            return base if internal else VT_FINISH_CONTEXT_REPLIES["break_uneasy"]
        if context == "uneasy" or outcome == "unaware":
            return VT_FINISH_CONTEXT_REPLIES.get(context, base)
        personality = VT_FINISH_CONTEXT_REPLIES.get(context)
        if personality is None:
            return base
        # Pair the existing three alternatives without an extra draw or saved state.
        return {register: [vt_finish_reply_join(line, personality[register][(index + 1) % len(personality[register])])
                           for index, line in enumerate(lines)]
                for register, lines in base.items()}

    def vt_vaginal_buildup_text(girl, condom_used, broken, aware, first_in_session, first_with_player, virgin):
        # Exactly one two-way choice, as in the reviewed mechanical delivery.
        if first_in_session:
            pool = ["You push into her with the condom on, and a rhythm starts to build.", "You sink into her, the condom between you, and start to find the pace."] if condom_used else ["You push into her bare, nothing between you, taking a moment to find the pace.", "You slide in without a condom, and the first uncertain strokes grow steadier."]
        else:
            pool = ["You keep fucking her, the condom still in place.", "You find the pace again, still wrapped in the condom."] if condom_used else ["You keep fucking her bare.", "You keep the pace going, skin to skin, no condom between you."]
        if broken:
            pool = ["You keep going, but the torn condom isn't a barrier anymore.", "The pace carries on with the damaged condom still on you; it no longer keeps you covered."]
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
            descriptions = VT_FINISH_CONTAINED if internal else VT_FINISH_EXTERNAL_CONTAINED
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
        vt_note_finish_closing(girl, known_break=(reply == "break"))
        text = renpy.random.choice(descriptions)
        if internal and options["first_with_player"]:
            text = "This is your first time with her like this; there is no familiar pace to fall back on yet. " + text
            if options["virgin"]:
                text = "At the initial resistance, you pause before continuing. " + text
        vt_queue_finisher_narration("vt_fetish_dialog", text)
        # Withdrawal's negotiated/adverse reply is emitted by its gate, after the act.
        if not options["skip_responses"] and not store.vt_pullout_external_active:
            vt_queue_finisher_narration("vt_finish_girl_reply", vt_voice(girl, vt_finish_reply_pool(girl, reply, internal=internal), "Give me a moment."))
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

label vt_vaginal_buildup(additional_subtags=None, skip_descriptions=False, skip_responses=False, force_cum=False, ask_to_cum=False, force_orgasm=False, can_deny_orgasm=True, select_base_description=False):
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
    # Legacy scene callers retain the base selector/RNG draw, without a second insertion.
    if select_base_description and not skip_descriptions:
        $ action_description = player.get_description_for_action("fuck_pussy", selected_girl)
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
