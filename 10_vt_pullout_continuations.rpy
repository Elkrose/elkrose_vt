# Vaginal buildup and finishers complete their effects/hooks before narration.
# Composes with the existing oral continuation when installed; no oral prerequisite.
default vt_finisher_narration = None
default vt_force_finisher_compensation = False
default vt_pullout_external_active = False

init -3 python:
    VT_FINISHER_ACTIONS = ("creampie_pussy", "sleep_creampie_pussy", "cumshot_pussy", "sleep_cumshot_pussy")
    VT_PULLOUT_EXTERNAL_DESCRIPTION = [
        "You withdraw before finishing, spilling your release against her vulva instead of inside her.",
        "You pull free and finish outside, leaving your release on her vulva.",
    ]

    def vt_queue_finisher_narration(label, text):
        if store.vt_finisher_narration is None:
            raise RuntimeError("VT finisher narration requires the action continuation")
        store.vt_finisher_narration.append((label, text))

# At equal priority the numbered filename follows 09_vt_action_continuations.rpy.
init 999 python:
    if not getattr(apply_action_impacts, "_vt_finisher_continuation", False):
        _vt_original_finisher_impacts = apply_action_impacts

        def vt_apply_finisher_impacts(action_name, *args, **kwargs):
            if action_name not in VT_FINISHER_ACTIONS + ("fuck_pussy", "sleep_fuck_pussy"):
                return _vt_original_finisher_impacts(action_name, *args, **kwargs)
            previous = store.vt_finisher_narration
            narration = []
            store.vt_finisher_narration = narration
            try:
                original_entry = None
                if action_name == "creampie_pussy" and store.vt_force_finisher_compensation:
                    # The base impact override has a different shape at its two consumers.
                    # Narrowly replace the database entry for this synchronous action instead;
                    # preserve role probabilities, costs and every other impact/multiplier.
                    original_entry = database_action_impacts[action_name]
                    entry = dict(original_entry)
                    action_impacts = dict(entry["impacts"])
                    target = dict(action_impacts["target_girl"])
                    impacts = dict(target["impacts"])
                    impacts.pop("corruption", None)
                    target["impacts"] = impacts
                    action_impacts["target_girl"] = target
                    entry["impacts"] = action_impacts
                    database_action_impacts[action_name] = entry
                result = _vt_original_finisher_impacts(action_name, *args, **kwargs)
            finally:
                if original_entry is not None:
                    database_action_impacts[action_name] = original_entry
                store.vt_finisher_narration = previous
            # VT scenes select their media before speaking. Legacy callers still use
            # the continuation here. In both cases all hooks and queue restoration finish first.
            if store.vt_owned_finish_options is not None:
                store.vt_owned_finish_options["narration"] = narration
            elif narration:
                renpy.call("vt_finisher_action_continuation", narration=narration)
            return result

        vt_apply_finisher_impacts._vt_finisher_continuation = True
        apply_action_impacts = vt_apply_finisher_impacts

label vt_finisher_action_continuation(narration):
    # Preserve the completed action/callbacks when loading during a queued line.
    $ renpy.retain_after_load()
    while narration:
        $ _vt_finisher_label, _vt_finisher_text = narration.pop(0)
        $ renpy.call(_vt_finisher_label, dialogtext=_vt_finisher_text)
    return
