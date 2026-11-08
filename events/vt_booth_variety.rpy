# Booth-local variation. Keep register, persona and situational gates at the caller.
init python:
    import builtins as _vt_booth_builtins
    import hashlib as _vt_booth_hashlib

    def vt_booth_choice(girl, lines):
        """Avoid an immediate repeat within the same eligible pool for this character.
        Primitive sidecar history survives visits/saves; Ren'Py owns rollback and RNG.
        Pool contents form the key, so edits cannot reuse an unrelated old index."""
        variants = list(dict.fromkeys(lines))
        if not variants:
            return ""
        bucket = girl.mod_data.setdefault("elkrose_vt", {})
        history = bucket.setdefault("booth_last_lines", {})
        key = _vt_booth_hashlib.sha256(repr(variants).encode("utf-8")).hexdigest()
        previous = history.get(key)
        candidates = [i for i in range(len(variants)) if i != previous]
        index = renpy.random.choice(candidates or [0])
        # Bound saved history even when future content adds many more pools.
        if key not in history and len(history) >= 128:
            del history[next(iter(history))]
        history[key] = index
        return variants[index]

    def vt_booth_voice(girl, options, default="", player=None):
        """Use vt_voice's exact register fallback, with booth-local repeat protection."""
        register = vt_explicitness_register(girl)
        for key in _VT_REGISTER_FALLBACK.get(register, ["neutral"]):
            if key in options:
                value = options[key]
                line = (vt_booth_choice(girl, value) if value else default) if isinstance(value, (_vt_booth_builtins.list, _vt_booth_builtins.tuple)) else value
                return _vt_resolve_words(girl, line, player)
        return default
