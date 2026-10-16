# Oral impact narration is action-scoped, primitive data only. The wrapper clears it
# before control transfer; the explicit label returns to the original generic action.
default vt_oral_narration = None

init -3 python:
    VT_ORAL_NARRATION_ACTIONS = (
        "blowjob", "sleep_blowjob", "use_mouth", "creampie_mouth",
        "sleep_creampie_mouth", "facial", "sleep_facial",
    )

    def vt_queue_oral_narration(kind, text, duration=None):
        if store.vt_oral_narration is None:
            raise RuntimeError("VT oral narration requires the action impact continuation")
        store.vt_oral_narration.append((kind, text, duration))

init 999 python:
    # Depends on utils_ren.py and every registered impact hook. Wrap the entire
    # impact call: renpy.call in any individual hook would unwind its later callbacks.
    if not getattr(apply_action_impacts, "_vt_oral_continuation", False):
        _vt_original_action_impacts = apply_action_impacts

        def vt_apply_action_impacts(action_name, *args, **kwargs):
            if action_name not in VT_ORAL_NARRATION_ACTIONS:
                return _vt_original_action_impacts(action_name, *args, **kwargs)
            previous = store.vt_oral_narration
            narration = []
            store.vt_oral_narration = narration
            try:
                result = _vt_original_action_impacts(action_name, *args, **kwargs)
            finally:
                store.vt_oral_narration = previous
            # All effects and callbacks have returned. No Python work follows transfer.
            if narration:
                renpy.call("vt_oral_action_continuation", narration=narration)
            return result

        vt_apply_action_impacts._vt_oral_continuation = True
        apply_action_impacts = vt_apply_action_impacts

label vt_oral_action_continuation(narration):
    # Retain completed impacts when loading mid-line instead of replaying the action.
    $ renpy.retain_after_load()
    while narration:
        $ _vt_oral_kind, _vt_oral_text, _vt_oral_duration = narration.pop(0)
        if _vt_oral_kind == "atm":
            call vt_atm_reaction(line=_vt_oral_text)
        elif _vt_oral_kind == "firsttime":
            $ vt_firsttime_notify(_vt_oral_text, duration=_vt_oral_duration)
        elif _vt_oral_kind == "fetish":
            $ vt_fetish_notify(_vt_oral_text, duration=_vt_oral_duration)
        else:
            call vt_fetish_dialog(dialogtext=_vt_oral_text)
    return
