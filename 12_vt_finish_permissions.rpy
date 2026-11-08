# Contact protection and finish permission have separate owners. Permanent decisions
# are primitive sidecar data; encounter replies are keyed by partner and destination.
default vt_finish_session = {}
default vt_finish_request_allowed = False
default vt_booth_protection_proceed = False

init -3 python:
    VT_FINISH_DESTINATIONS = {
        "face": ("on your face", "oral"),
        "mouth": ("in your mouth", "oral"),
        "boobs": ("on your chest", "body"),
        "thighs": ("on your thighs", "body"),
        "ass": ("on your bottom", "body"),
        "pussy": ('on your pussy', "body"),
        "creampie_pussy": ("inside you", "vaginal"),
        "creampie_ass": ('inside your ass', "anal"),
    }
    VT_FINISH_BODY_TARGETS = ("boobs", "thighs", "ass")
    VT_FINISH_REPLY_PLACES = {
        "face": "on my face", "mouth": "in my mouth", "boobs": "on my chest",
        "thighs": "on my thighs", "ass": "on my bottom", "pussy": 'on my pussy',
        "creampie_pussy": "inside me", "creampie_ass": 'inside my ass',
    }
    # Bolder registers name the destination in their own words; every other
    # register keeps VT_FINISH_REPLY_PLACES. Wording only -- keys are unchanged.
    VT_FINISH_REPLY_PLACES_BY_REGISTER = {
        "crude": {
            "face": "all over my face", "mouth": "in my mouth", "boobs": "on my tits",
            "thighs": "on my thighs", "ass": "on my ass", "pussy": "on my pussy",
            "creampie_pussy": "in my pussy", "creampie_ass": "in my ass",
        },
        "explicit": {
            "face": "on my face", "mouth": "in my mouth", "boobs": "on my tits",
            "thighs": "on my thighs", "ass": "on my ass", "pussy": "on my pussy",
            "creampie_pussy": "inside me", "creampie_ass": "in my ass",
        },
    }


    def vt_body_contact_condom(girl):
        # Migration already precedes defaults in vt_ensure_girl_attrs. Do not reinterpret
        # an old explicit decision, or write/reroll anything while a menu queries this.
        bucket = (getattr(girl, "mod_data", None) or {}).get("elkrose_vt", {})
        value = bucket["wants_body_condom"] if "wants_body_condom" in bucket else getattr(girl, "__dict__", {}).get("wants_body_condom")
        return value is True

    def vt_finish_preference(girl, destination):
        bucket = (getattr(girl, "mod_data", None) or {}).get("elkrose_vt", {})
        decisions = bucket.get("finish_preferences", {})
        # Membership preserves a deliberate None overriding a shared body default.
        if destination in decisions:
            return decisions[destination]
        if destination in VT_FINISH_BODY_TARGETS:
            return decisions.get("body")
        return None

    def vt_set_finish_preference(girl, destination, value):
        if destination not in VT_FINISH_DESTINATIONS and destination != "body":
            raise ValueError("Unknown finish destination: " + str(destination))
        if value is not None and type(value) is not bool:
            raise ValueError("Finish preference must be None or a boolean")
        decisions = vt_girl_bucket(girl).setdefault("finish_preferences", {})
        decisions[destination] = value
        affected = [target for target in VT_FINISH_BODY_TARGETS if target not in decisions] if destination == "body" else [destination]
        session = getattr(store, "vt_finish_session", {})
        for target in affected:
            session.pop(vt_finish_key(girl, target), None)

    def vt_finish_key(girl, destination):
        return (girl.id, destination)

    def vt_finish_perceived_contained(girl, destination):
        slot = VT_FINISH_DESTINATIONS[destination][1]
        awareness = {"body": "aware_boob_condom", "oral": "aware_oral_condom",
                     "vaginal": "aware_vaginal_condom", "anal": "aware_anal_condom"}[slot]
        if destination == "thighs":
            awareness = "aware_thigh_condom"
        elif destination == "ass":
            awareness = "aware_ass_cumshot_condom"
        known_break = getattr(girl, awareness, False)
        if destination == "pussy":
            known_break = girl.aware_vaginal_condom or girl.aware_pussy_cumshot_condom
        return (player.condom_active != "raw" and
                (not player.condom_broke or not known_break))

    def vt_finish_permission(girl, destination):
        """Pure menu query: True/False is known permission, None needs a request."""
        key = vt_finish_key(girl, destination)
        if getattr(store, "is_during_sex_interaction", False) and key in store.vt_finish_session:
            return store.vt_finish_session[key]
        decision = vt_finish_preference(girl, destination)
        if destination == "creampie_pussy" and decision is None:
            # Read the legacy owner's saved yes without creating/migrating a bucket.
            bucket = (getattr(girl, "mod_data", None) or {}).get("elkrose_vt", {})
            if bucket.get("vt_accepts_vaginal_creampie", False):
                return True
            if getattr(store, "is_during_sex_interaction", False) and girl.id in getattr(store, "vt_creampie_session", ()):
                return True
        return decision

    VT_FINISH_PERMISSION_REPLIES = {
     'session': {
      'crude': ["Fuck it. {Place}, just this once -- don't make it a habit.",
                "Yeah, all right -- {place}. This time. Next time you ask again.",
                "{Place}? ...Fine. Do it before I change my mind."],
      'explicit': ["Mm. {Place}, then. Just this time, so make it count.",
                   "You want it {place}? Go ahead. Don't expect it every time.",
                   "Yes. {Place}. I'll decide about next time when there is one."],
      'direct': ["{Place} works. This once.",
                 "Sure, {place}. Ask me again next time.",
                 "Go ahead, {place}. Just for now."],
      'neutral': ["Okay... {place}. Just this time.",
                  "All right, {place}. Only this once, though.",
                  "I think that's okay. {Place}, this time."],
      'shy': ["Um... o-okay. {Place}... just this once.",
              "I... yes. {Place} is okay. This time.",
              "If you really want... {place}. But only this time, okay?"],
      'demure': ["Very well. {Place}, on this occasion only.",
                 "Since you asked so nicely... {place}. Just this once.",
                 "Yes, {place}. Please don't take it as a standing invitation."]},
     'permanent': {
      'crude': ["Fuck yes, {place}. Just fucking DO it next time... don't bother asking...",
                "{Place}. Stop asking and just do it -- that goes for next time too.",
                "Hell yes. {Place} -- that's where I want it, unless I say otherwise."],
      'explicit': ["Mmm, {place}. Oh, fuck, that's hot... you can do that any time you want...",
                   "{Place}, yes. You can skip asking next time.",
                   "God, yes -- {place}. Consider that a standing yes."],
      'direct': ["Yes, {place}. You don't need to ask me again.",
                 "{Place} is good. Every time, unless I say otherwise.",
                 "Yeah, {place}. Remember that one."],
      'neutral': ["Yes, {place}. You can remember that for next time.",
                  "{Place} is fine. I'll tell you if that changes.",
                  "I'd like that. {Place}... next time too."],
      'shy': ["Y-yes... {place}. You... you don't have to ask next time.",
              "{Place}... I'd like that. Next time too.",
              "Mm-hm. {Place}. I won't mind next time either."],
      'demure': ["{Place} is quite welcome. You may take that as my answer from now on.",
                 "Yes, {place}. I'd rather you didn't have to ask again.",
                 "You may, {place}. And next time as well, unless I tell you otherwise."]},
     'no': {
      'crude': ["Hell no. Not {place}. Aim it somewhere else.",
                "Not {place}. Anywhere but there.",
                "Fuck off with that. Not {place}."],
      'explicit': ["No. Not {place}. Finish somewhere else.",
                   "Not {place}, babe. That's a no.",
                   "Mm-mm. Not {place}. Finish away from me."],
      'direct': ["No. Not {place}.",
                 "Not {place}. Finish somewhere else.",
                 "No. Not {place}. Keep it away from me."],
      'neutral': ["No, not {place}. Please finish away from me.",
                  "I'd rather not... not {place}.",
                  "Not {place}, please. Somewhere else."],
      'shy': ["N-no... not {place}. Please.",
              "I... I don't want it {place}. Sorry.",
              "Please don't... not {place}."],
      'demure': ["No. Not {place}, if you please.",
                 "I must say no. Not {place}.",
                 "Not {place}. Please finish elsewhere."]}}

    def vt_finish_reply(girl, destination, outcome):
        places = VT_FINISH_REPLY_PLACES_BY_REGISTER.get(vt_explicitness_register(girl), VT_FINISH_REPLY_PLACES)
        place = places[destination]
        line = vt_voice(girl, VT_FINISH_PERMISSION_REPLIES[outcome], "Not {place}, please.")
        return line.format(place=place, Place=place[0].upper() + place[1:])

    def vt_resolve_finish_request(girl, destination):
        # Called only by the spoken request, never by a render/query. Repeated requests
        # retain their answer; there are no new stat rewards or acceptance RNG rolls.
        known = vt_finish_permission(girl, destination)
        if known is not None:
            outcome = "session" if known else "no"
            allowed = known
        else:
            slot = VT_FINISH_DESTINATIONS[destination][1]
            # Use the established live stats, fixed temperament and trait bonuses.
            # Saved contact-condom booleans are intentionally NOT finish preferences.
            naturally_willing = not wants_condom_live(girl, slot)
            band = vt_willingness_band(girl, _vt_gobare_intent(slot), player)
            allowed = naturally_willing or band in ("eager", "conditional")
            outcome = "permanent" if allowed and band == "eager" else "session" if allowed else "no"
            if outcome == "permanent":
                vt_set_finish_preference(girl, destination, True)
        if getattr(store, "is_during_sex_interaction", False):
            store.vt_finish_session[vt_finish_key(girl, destination)] = allowed
        return allowed, vt_finish_reply(girl, destination, outcome)

# Destination effects/presentation and their stable label live in
# 13_vt_destination_finishers.rpy; this module owns decisions and adapters.

init 999 python:
    # Chain the real shared cleanup: normal endings, exits and interrupted routes
    # must retire temporary destination answers just as booth cleanup does.
    if not getattr(sex_interaction_clear, "_vt_finish_cleanup", False):
        _vt_finish_previous_interaction_clear = sex_interaction_clear
        def vt_finish_interaction_clear(*args, **kwargs):
            store.vt_finish_session = {}
            store.vt_finish_request_allowed = False
            return _vt_finish_previous_interaction_clear(*args, **kwargs)
        vt_finish_interaction_clear._vt_finish_cleanup = True
        sex_interaction_clear = vt_finish_interaction_clear

    def vt_route_finish_permissions():
        # Late composition preserves v1.1.6's owned vaginal gates. Stable labels also
        # leave callers in old saves valid. Never save original callable instances.
        captions = {"face": "Finish on her face", "mouth": "Finish in her mouth",
                    "boobs": "Finish on her chest", "thighs": "Finish on her thighs",
                    "ass": "Finish on her bottom", "pussy": "Finish on her pussy",
                    "creampie_pussy": "Finish inside her", "creampie_ass": "Finish inside her ass"}
        for target, data in database_cum_targets.items():
            if target in captions:
                data["option_text"] = captions[target]
            if target not in VT_FINISH_DESTINATIONS or target == "creampie_pussy":
                continue
            label = "vt_finish_target_" + target
            if data.get("option_label") != label:
                data["vt_finish_original_label"] = data["option_label"]
                data["option_label"] = label
        # A single-person alias suppresses the base chooser's unguarded bulk shortcut
        # while preserving the individual face request and its exam metadata.
        database_cum_targets["vt_face_single"] = dict(database_cum_targets["face"])
        database_cum_targets["vt_away"] = {
            "option_text": "Finish away from her", "option_label": "vt_finish_away",
            "requirements": "True",
        }
        direct = {"facial": "face", "creampie_mouth": "mouth", "cumshot_boobs": "boobs",
                  "cumshot_thighs": "thighs", "cumshot_ass": "ass", "cumshot_pussy": "pussy",
                  "creampie_ass": "creampie_ass"}
        for actions in database_sex_options.values():
            for action in actions:
                target = direct.get(action.action_entry_name)
                if target is None:
                    continue
                # Internal anal still has an outer penetration/protection requirement.
                if action.label == "vt_condom_attempt_gate":
                    action.vt_real_label = "vt_finish_direct_" + target
                else:
                    action.label = "vt_finish_direct_" + target
    vt_route_finish_permissions()

    def _vt_finish_label_callback(name, abnormal):
        previous = getattr(store, "_vt_finish_previous_label_callback", None)
        if previous is not None:
            previous(name, abnormal)
        if name == "generic_action_player_choose_cum_girl_target":
            parts = (current_event.participants if current_event else
                     [g for g in se_participants if isinstance(g, Girl) and not g.left_sex_interaction]
                     if is_during_sex_interaction else [selected_girl])
            girls = [g for g in parts if isinstance(g, Girl)]
            if len(girls) > 1 and "face" in (store.options or ()):
                # Preserve the old simultaneous route only for an exposed finish every
                # recipient has agreed to. Contained finishes use the owned single route.
                bulk_allowed = player.condom_active == "raw" and all(vt_finish_permission(g, "face") is True for g in girls)
                if not bulk_allowed:
                    store.options = ["vt_face_single" if option == "face" else option for option in store.options]
        if name == "generic_action_player_choose_cum_target":
            # Include the fallback even for explicit options lists. Copy before mutation
            # so shared database lists and saved callers' arguments remain unchanged.
            options = list(store.options or ())
            if "vt_away" not in options:
                options.append("vt_away")
            store.options = options

    if not getattr(store, "_vt_finish_label_callback_installed", False):
        store._vt_finish_previous_label_callback = config.label_callback
        config.label_callback = _vt_finish_label_callback
        store._vt_finish_label_callback_installed = True

label vt_finish_request(girl, destination):
    $ vt_finish_request_allowed = True
    if vt_finish_perceived_contained(girl, destination):
        return vt_finish_permission(girl, destination) is True
    if vt_finish_permission(girl, destination) is True:
        return True
    $ _vt_finish_place = VT_FINISH_DESTINATIONS[destination][0]
    player.character "Can I finish [_vt_finish_place]?"
    $ vt_finish_request_allowed, _vt_finish_answer = vt_resolve_finish_request(girl, destination)
    girl.character "[_vt_finish_answer]"
    return vt_finish_request_allowed

label vt_finish_away(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    # No target action/impacts, semen, conception check or second player climax.
    if not player.just_came:
        $ player.cum()
    if player.condom_active != "raw" and not player.condom_broke:
        $ player.condom_dirty = True
        $ player.condom_cum += 1
        "You move clear before you finish. The condom holds your release."
    else:
        if player.condom_active != "raw":
            $ player.condom_dirty = True
            $ player.condom_cum = 0
        "You turn away and finish clear of everyone else, then steady yourself."
    return

label vt_finish_target(destination, action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    if not isinstance(selected_girl, Girl):
        call vt_finish_away(action_name, additional_subtags, skip_descriptions, skip_responses)
        return
    if destination in ("mouth", "creampie_ass"):
        call vt_booth_protection_gate(selected_girl, "oral" if destination == "mouth" else "anal")
        if not vt_booth_protection_proceed:
            call vt_finish_away(action_name, additional_subtags, skip_descriptions, skip_responses)
            return
    call vt_finish_request(selected_girl, destination)
    $ _vt_target_exposure_agreed = bool(_return)
    if not vt_finish_request_allowed:
        call vt_finish_away(action_name, additional_subtags, skip_descriptions, skip_responses)
        return
    if destination != "pussy":
        call vt_destination_finisher(destination, action_name, additional_subtags, skip_descriptions, skip_responses, _vt_exposure_agreed=_vt_target_exposure_agreed)
        return
    $ _vt_finish_original = database_cum_targets[destination]["vt_finish_original_label"]
    $ renpy.call(_vt_finish_original, action_name=action_name, additional_subtags=additional_subtags, skip_descriptions=skip_descriptions, skip_responses=skip_responses)
    return

label vt_finish_direct(destination):
    call vt_finish_target(destination, additional_subtags=se_additional_webm_sub_tags, skip_descriptions=sex_skip_descriptions, skip_responses=sex_skip_responses)
    return

label vt_booth_protection_gate(girl, slot):
    $ vt_booth_protection_proceed = True
    $ _vt_booth_awareness = "aware_" + slot + "_condom"
    if (player.condom_active != "raw" and (not player.condom_broke or not getattr(girl, _vt_booth_awareness, False))) or not vt_condom_now(girl, slot):
        return
    if slot in getattr(girl, "vt_gobare_attempted", ()):
        $ setattr(girl, "player_knows_" + slot + "_condom", True)
        $ _vt_booth_protection_line = vt_booth_voice(girl, VT_GOBARE_ALREADY, "I already told you -- use a condom.")
        girl.character "[_vt_booth_protection_line]"
        $ vt_booth_protection_proceed = False
    else:
        call vt_gobare_beat(girl, slot)
        $ vt_booth_protection_proceed = vt_gobare_beat_outcome in ("yes_perm", "yes_session")
    if not vt_booth_protection_proceed:
        "You ease back, leaving her room. You do not take that step."
    return

label vt_finish_target_face(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    call vt_finish_target("face", action_name, additional_subtags, skip_descriptions, skip_responses)
    return

label vt_finish_direct_face:
    call vt_finish_direct("face")
    return

label vt_finish_target_mouth(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    call vt_finish_target("mouth", action_name, additional_subtags, skip_descriptions, skip_responses)
    return

label vt_finish_direct_mouth:
    call vt_finish_direct("mouth")
    return

label vt_finish_target_boobs(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    call vt_finish_target("boobs", action_name, additional_subtags, skip_descriptions, skip_responses)
    return

label vt_finish_direct_boobs:
    call vt_finish_direct("boobs")
    return

label vt_finish_target_thighs(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    call vt_finish_target("thighs", action_name, additional_subtags, skip_descriptions, skip_responses)
    return

label vt_finish_direct_thighs:
    call vt_finish_direct("thighs")
    return

label vt_finish_target_ass(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    call vt_finish_target("ass", action_name, additional_subtags, skip_descriptions, skip_responses)
    return

label vt_finish_direct_ass:
    call vt_finish_direct("ass")
    return

label vt_finish_target_pussy(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    call vt_finish_target("pussy", action_name, additional_subtags, skip_descriptions, skip_responses)
    return

label vt_finish_direct_pussy:
    call vt_finish_direct("pussy")
    return

label vt_finish_target_creampie_ass(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    call vt_finish_target("creampie_ass", action_name, additional_subtags, skip_descriptions, skip_responses)
    return

label vt_finish_direct_creampie_ass:
    call vt_finish_direct("creampie_ass")
    return
