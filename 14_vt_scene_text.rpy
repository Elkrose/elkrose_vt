# Presentation adapters for shared game text. Original effects/selectors still run.
# Encounter-only primitives survive a displayed save; the shared reset clears them.
default vt_finish_closing_contexts = {}
default vt_booth_buildup_context = None

init -3 python:
    VT_SHARED_CLOSING_GIRL_LINES = frozenset(['God, that was incredible! You really know how to unwind me. I hope it took some of your stress away too.', "Wow, you've got some serious skills. I'm starting to see why this feels so good.", "Well... that was something. I hope you're feeling a little less wound up now.", "That was wild. Honestly amazing! Shame you didn't finish, though... next time, maybe?", "You're good at this, no doubt. I just wish you'd gotten off too. It'd make it even hotter.", "Oh, uh... you're done already? I get it, though. Stress can mess with anyone.", "Ugh, finally! I can't believe I let it go that far... this is so embarrassing.", "Thank God that's over. I don't even want to think about what just happened.", "Well, that's done. Let's just pretend this never happened, okay?"])

    VT_CLOSING_REPLIES = {
        "break": (
            ("Let's work out what to do about the condom before we leave.", "All right. We'll think it through together."),
            ("Stay with me while we decide what to do about that tear.", "I'm here. We can take a moment to think."),
            ("I don't want to be left worrying about the condom on my own.", "We'll talk it through together.")),
        "uneasy": (
            ("That's enough for now. I need some space.", "All right. I'll give you room."),
            ("I need a moment to myself before we talk.", "Okay. Take your time."),
            ("Let's stop here. I need to collect myself.", "All right. We can leave it there.")),
        "warm_reserved": (
            ("Can we stay here a moment before we get up?", "Of course. There's no hurry."),
            ("I'm still a little flustered. Sit with me a moment?", "I'm happy to stay."),
            ("Give me a moment to find my words.", "Take your time. I'm here.")),
        "warm_familiar": (
            ("Stay close a little longer?", "I'd like that."),
            ("I like these quiet moments with you too.", "So do I. We don't have to rush."),
            ("Let's have a minute together before we move.", "Of course. Come here.")),
        "playful": (
            ("You're in no hurry to get up either, are you?", "You caught me. I'll stay a little longer."),
            ("Give me a minute before you look so pleased with yourself.", "A minute it is."),
            ("We can sit still together for once, can't we?", "I think I can manage that.")),
        "practical": (
            ("Let's get comfortable before we do anything else.", "All right. Take your time."),
            ("A moment to catch our breath, then we can move.", "That works for me."),
            ("Let me collect myself first.", "Of course. There's no hurry.")),
        "reserved_mother": (
            ("I would like a little privacy while I collect myself.", "Of course. I'll give you some privacy."),
            ("Let us leave it there for now, shall we?", "All right. We can stop here."),
            ("I need a moment before we talk about this.", "Take your time.")),
        "reserved": (
            ("Could I have a little space to collect myself?", "Of course. Take your time."),
            ("Let's leave it there for now, okay?", "Okay. We can stop here."),
            ("I'm not quite ready to talk yet.", "That's all right. There's no hurry.")),
        "neutral": (
            ("Let's take a moment before we move.", "All right. There's no hurry."),
            ("I need a second to catch my breath.", "Take your time."),
            ("Let's leave it there for now.", "Okay. We can stop here.")),
    }

    def vt_note_finish_closing(girl, known_break=False):
        previous = store.vt_finish_closing_contexts.get(girl.id, {})
        store.vt_finish_closing_contexts[girl.id] = {
            "context": vt_finish_reply_context(girl),
            "known_break": bool(known_break or previous.get("known_break", False)),
        }

    def vt_shared_closing_pair(girl, original_line):
        record = store.vt_finish_closing_contexts.get(girl.id)
        if not record:
            return None
        context = "break" if record["known_break"] else record["context"]
        pool = VT_CLOSING_REPLIES.get(context, VT_CLOSING_REPLIES["neutral"])
        # Reuse the already selected base alternative; no new RNG/cache reads.
        return pool[sum(map(ord, original_line)) % len(pool)]

    def vt_shared_closing_text(text, filename):
        if not filename.replace("\\", "/").endswith("/sex_interaction/label_sex_ending.rpy"):
            return text
        girl = getattr(store, "selected_girl", None)
        participants = getattr(store, "se_participants", ())
        if (not isinstance(girl, Girl) or len(participants) != 1 or participants[0] is not girl
                or getattr(girl, "left_sex_interaction", False)
                or store.se_end_label in ("vt_forced_sex_ending", "vt_force_fail_followup")
                or store.vt_force_outcome_this_session is not None):
            return text
        pair = vt_shared_closing_pair(girl, getattr(store, "player_response", text)
                                      if text == "[player_response]" else text)
        if pair is None:
            return text
        if text in VT_SHARED_CLOSING_GIRL_LINES:
            return pair[0]
        if text == "[player_response]":
            return pair[1]
        if text == "If you could give me a few minutes to clean up...":
            record = store.vt_finish_closing_contexts[girl.id]
            if record["known_break"]:
                return "Let's get comfortable, then talk this through."
            if record["context"] in ("warm_reserved", "warm_familiar", "playful"):
                return "We can take our time getting ready."
            return "I'll get myself sorted out."
        return text

    def vt_booth_buildup_matches(girl, action_name):
        return girl is not None and store.vt_booth_buildup_context == (girl.id, action_name)

    def vt_booth_oral_buildup_narration(narration):
        # Preserve ATM, first-time and break-awareness notices. Only the two
        # repeated activity summaries become one resolved protection beat.
        if not any(entry[0] == "dialog" for entry in narration):
            return narration
        entries = [entry for entry in narration if entry[0] != "dialog"]
        if player.condom_active == "raw":
            text = "You settle into the moment together, with no condom between you."
        elif player.condom_broke:
            text = ("The condom is torn. She has noticed it too." if selected_girl.aware_oral_condom
                    else "The condom is torn, though she hasn't noticed the damage.")
        else:
            text = "The condom stays in place as the moment continues beneath the table."
        return entries + [("dialog", text, None)]

    def vt_orgasm_player_reply(girl, original_line):
        context = vt_finish_reply_context(girl)
        pool = {
            "uneasy": ("Take your time. I'll give you room.", "We can stop here. Take a moment.", "All right. There's no hurry."),
            "warm_reserved": ("Stay close if you'd like.", "We don't have to rush.", "Take your time. I'm here."),
            "warm_familiar": ("I like being here with you.", "Come here. We can take our time.", "I'm happy to stay like this a while."),
            "playful": ("You have my full attention.", "We can take a breath before the next distraction.", "I'm enjoying having you all to myself."),
        }.get(context, ("Take a moment. There's no hurry.", "We can pause here a second.", "All right. Catch your breath."))
        return pool[sum(map(ord, original_line)) % len(pool)]

init 999 python:
    # Standard Ren'Py text filter, narrowly gated by source file and exact text.
    # The base ending retains all stat changes, rolls, cleanup and return routing.
    if not getattr(config.say_menu_text_filter, "_vt_scene_text", False):
        _vt_previous_text_filter = config.say_menu_text_filter
        def _vt_scene_text_filter(text):
            if _vt_previous_text_filter is not None:
                text = _vt_previous_text_filter(text)
            filename, _line = renpy.get_filename_line()
            return vt_shared_closing_text(text, filename)
        _vt_scene_text_filter._vt_scene_text = True
        config.say_menu_text_filter = _vt_scene_text_filter

    if not getattr(Player.get_description_for_action, "_vt_booth_text", False):
        _vt_original_player_description = Player.get_description_for_action
        def _vt_player_description(self, action_name, girl, *args, **kwargs):
            text = _vt_original_player_description(self, action_name, girl, *args, **kwargs)
            return None if self is player and vt_booth_buildup_matches(girl, action_name) else text
        _vt_player_description._vt_booth_text = True
        Player.get_description_for_action = _vt_player_description

    if not getattr(Girl.get_reaction_for_action, "_vt_booth_text", False):
        _vt_original_girl_reaction = Girl.get_reaction_for_action
        def _vt_girl_reaction(self, action_name, *args, **kwargs):
            text = _vt_original_girl_reaction(self, action_name, *args, **kwargs)
            return None if vt_booth_buildup_matches(self, action_name) else text
        _vt_girl_reaction._vt_booth_text = True
        Girl.get_reaction_for_action = _vt_girl_reaction

    if not getattr(Player.get_response_for_action, "_vt_orgasm_text", False):
        _vt_original_player_response = Player.get_response_for_action
        def _vt_player_response(self, action_name, girl, *args, **kwargs):
            text = _vt_original_player_response(self, action_name, girl, *args, **kwargs)
            orgasm = action_name == "orgasm" or action_name.endswith("_orgasm")
            if (text and orgasm and self is player and store.person_doing_action is player
                    and (store.is_during_sex_interaction or store.is_during_exam)
                    and store.vt_force_outcome_this_session is None and not store.vt_force_creampie_active):
                return vt_orgasm_player_reply(girl, text)
            return text
        _vt_player_response._vt_orgasm_text = True
        Player.get_response_for_action = _vt_player_response

label vt_booth_buildup(act_key, additional_subtags=None):
    $ assert act_key in ("handjob", "blowjob")
    $ vt_booth_buildup_context = (selected_girl.id, act_key)
    $ renpy.retain_after_load()
    if act_key == "handjob":
        call generic_action_handjob(additional_subtags=additional_subtags, skip_responses=True, ask_to_cum=True, force_cum=False)
    else:
        call generic_action_blowjob(additional_subtags=additional_subtags, skip_responses=True, ask_to_cum=True, force_cum=False)
    $ vt_booth_buildup_context = None
    return
