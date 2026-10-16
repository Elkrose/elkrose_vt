# VT DIALOG RESPONSE ENGINE
#
# Data-driven replacement for the deep if/elif/else dialogue-selection trees in the
# small-talk conversations. See VT-Dialog-Response-System.md for the full design + the
# locked decisions (predicate + specificity matching with a priority escape hatch;
# register handled per-entry by vt_voice; behaviour-preserving migration).
#
# THE BOUNDARY: this engine returns ONLY the spoken line. Menus, apply_impacts(), and
# flag mutations stay in the label. A beat's label computes `$ _line = vt_say(...)` and
# then speaks `selected_girl.character "[_line]"`.
#
# Toggle a console trace of which entry matched with:  vt_dialog_trace = True
default vt_dialog_trace = False

init -1 python:
    import re

    # The registry: beat id -> list of response entries. Data files register into this.
    # An entry is a dict:
    #   {
    #     "when":     {fact_key: value_or_iterable, ...}   # optional; omitted axis = "don't care"
    #     "priority": int                                  # optional, default 0; escape hatch
    #     "lines":    {register: line_or_[variants], ...}  # vt_voice's shape
    #   }
    # A scalar `when` value must match exactly; an iterable (list/tuple/set) matches by membership.
    VT_RESPONSES = {}

    # VT WORD LEXICON: a second, lower-level registry alongside VT_RESPONSES. Instead of picking a
    # whole pre-written line, a beat (or a hand-written line) can ask for a single word/phrase for a
    # concept -- "penis", "have sex", "huge" -- and get back whichever fits her CURRENT stats, so
    # vocabulary composes instead of needing every combination hand-written as a full sentence.
    #
    # slot id -> list of entries. An entry is a dict:
    #   {"when": {...}, "words": ["word1", "word2", ...]}   # same `when` grammar as VT_RESPONSES
    # Selection mirrors vt_say exactly: filter by _vt_match, keep highest specificity, then
    # renpy.random.choice among both tied entries AND that entry's own word list.
    VT_LEXICON = {}

    def vt_register_words(slot, entries):
        """Append lexicon entries for a slot (e.g. "noun_penis"). Data files call this at init."""
        VT_LEXICON.setdefault(slot, []).extend(entries)

    def vt_word(girl, slot, player=None, default=""):
        """Resolve one word/phrase for `slot` from her current stats (see VT_LEXICON above).

        Same facts dict as vt_say (_vt_context), including "register" -- so a girl's improvised
        vocabulary always agrees with her canned response lines about how corrupted she sounds.
        Returns `default` if no entry matches (loud in developer mode, mirroring vt_say).
        """
        entries = VT_LEXICON.get(slot, ())
        facts = _vt_context(girl, player)
        cands = [e for e in entries if _vt_match(facts, e.get("when", {}))]
        if not cands:
            if config.developer:
                print("VT vt_word NO MATCH slot=%s girl=%s facts=%r" % (slot, getattr(girl, "name", girl), facts))
            return default
        best_spec = max(len(e.get("when", {})) for e in cands)
        cands = [e for e in cands if len(e.get("when", {})) == best_spec]
        entry = renpy.random.choice(cands)
        words = entry.get("words", [])
        return renpy.random.choice(words) if words else default

    # Matches %slot_name% tokens inside a vt_say-picked line (see the substitution step in vt_say
    # below). Deliberately NOT {curly braces} (Ren'Py's own style-tag delimiter, e.g. {b}/{color=..})
    # or [square brackets] (Ren'Py's live text substitution, already used for [girl]/[player]
    # tokens elsewhere in this table) -- substitution happens entirely in Python here, before the
    # resulting string is ever handed to Ren'Py, so %...% just keeps it visually unambiguous.
    _VT_WORD_TOKEN = re.compile(r"%([a-zA-Z_][a-zA-Z0-9_]*)%")

    def _vt_resolve_words(girl, line, player=None):
        """Replace every %slot% token in `line` with vt_word(girl, slot, player)."""
        if not line or "%" not in line:
            return line
        return _VT_WORD_TOKEN.sub(lambda m: vt_word(girl, m.group(1), player), line)

    # PLAYTEST TRACE: when True, every vt_say pick is logged to log.txt (girl, beat, register,
    # matched `when`, and the line returned) for post-playtest review. Underscore prefix means
    # Ren'Py never saves/restores it, so it's on regardless of an existing save's state.
    # Revert to False (or delete) once the Phase-2 playtest review is done.
    _VT_TRACE = False

    def vt_register_responses(beat, entries):
        """Append response entries for a beat. Data files call this at init."""
        VT_RESPONSES.setdefault(beat, []).extend(entries)

    def _vt_context(girl, player=None):
        """Resolve a girl (+ optional player) into the condition vocabulary the table matches on.

        Built once per ask. Mirrors how the live trees route so a migrated beat picks the same
        line for the same state: role from the daughter/mother attrs, the kids_with_player parent
        flag the already-pregnant beats use, the >70 / 30-70 / <30 baby_desire tiers the protection
        beats use, and the pregnancy enum -- note she only "speaks pregnant" once she KNOWS
        (knows_pregnant), matching the existing knows_pregnant gate.
        """
        # Role bucket: base mother (has a daughter) -> student (has a mother) -> other.
        if getattr(girl, "daughter", None):
            role = "mother"
        elif getattr(girl, "mother", None):
            role = "student"
        else:
            role = "other"

        # Currently-a-mother: base mothers carry the original daughter in .kids, so they need >1.
        total_kids = getattr(girl, "kids", 0) or 0
        is_mother = (total_kids > 1) if role == "mother" else (total_kids > 0)
        kwp = getattr(girl, "kids_with_player", 0) or 0

        # Pregnancy enum -- only meaningful once she knows.
        if getattr(girl, "pregnant", False) and getattr(girl, "knows_pregnant", False):
            pregnancy = "by_player" if getattr(girl, "preg_father", None) == "player" else "by_other"
        else:
            pregnancy = "none"

        # Trimester band for the phase-aware pregnancy beats -- from pregnancy_phase. Phase 0 is
        # "just conceived" (< ~10 days); a girl is normally only known-pregnant from phase 1, but the
        # player can DISCOVER it during phase 0, and then the phase-aware beats ARE reachable while
        # phase is still 0 -> map 0 to the earliest first trimester so they still have a line. None only
        # when there's no phase at all (not pregnant); a `"trimester"`-gated entry then just won't match.
        trimester = {0: "first", 1: "first", 2: "second", 3: "third"}.get(
            getattr(girl, "pregnancy_phase", None))

        # Coarse baby_desire tier used by the protection beats: >70 high, 30-70 mid, <30 low.
        d = max(0, min(100, getattr(girl, "baby_desire", 0) or 0))
        if d > 70:
            desire = "high"
        elif d >= 30:
            desire = "mid"
        else:
            desire = "low"

        return {
            "role":                 role,
            "trimester":            trimester,
            "is_mother":            is_mother,
            "parent":               kwp > 0,                                  # kids_with_player based
            "parent_broad":         (role == "mother") or is_mother or (kwp > 0),  # matches the trees' _vc_parent
            "kids_with_player":     kwp,
            "pregnancy":            pregnancy,
            "approach":             getattr(girl, "dominant_approach", None),
            "desire_tier":          desire,
            "wants_vaginal_condom": bool(getattr(girl, "wants_vaginal_condom", False)),
            "wants_anal_condom":    bool(getattr(girl, "wants_anal_condom", False)),
            "wants_oral_condom":    bool(getattr(girl, "wants_oral_condom", False)),
            "birth_control":        bool(getattr(girl, "birth_control", False)),
            "virgin":               (getattr(girl, "vaginal_sex_count", 0) or 0) <= 0,
            # Anal virginity, tracked separately: first anal is its own trepidation/reluctance beat
            # ("gross and weird at first"). Composed from the patcher's anal_sex_count, parallel to virgin.
            "anal_virgin":          (getattr(girl, "anal_sex_count", 0) or 0) <= 0,
            # Raw personality stats, exposed for the stat-cascade beats (affection / corruption / fear /
            # naturism small-talk) whose live trees split on `stat > N` / `stat < N` thresholds. Matched
            # via the dict-threshold `when` form; the exact cut points live in the table, mirroring the
            # mod author's existing thresholds (not new derived constants).
            "affection":            getattr(girl, "affection", 0) or 0,
            "fear":                 getattr(girl, "fear", 0) or 0,
            "discipline":           getattr(girl, "discipline", 0) or 0,
            "corruption":           getattr(girl, "corruption", 0) or 0,
            "intellect":            getattr(girl, "intellect", 0) or 0,
            "naturism":             getattr(girl, "naturism", 0) or 0,
            # Her corruption-trait explicitness bucket (demure/shy/neutral/direct/explicit/crude),
            # reused as-is from vt_voice's own register system (00_vt_patcher.rpy) so the word
            # lexicon (VT_LEXICON / vt_word, below) always agrees with her canned response lines
            # about how corrupted she currently sounds -- never re-derived independently.
            "register":             vt_explicitness_register(girl),
        }

    def _vt_match(facts, when):
        """True if every key in `when` is satisfied by `facts`.

        A `when` VALUE may be:
          - a scalar          -> exact equality
          - a list/tuple/set  -> membership
          - a dict            -> numeric threshold predicate, keys gt/ge/lt/le, ALL must hold
                                 (e.g. {"gt": 60}, {"ge": 60, "lt": 75}). Used by the stat-cascade
                                 beats (affection family) to mirror the live `stat > N` / `< N` splits.
        """
        for k, want in when.items():
            have = facts.get(k)
            if isinstance(want, dict):
                if have is None:
                    return False
                if "gt" in want and not (have >  want["gt"]): return False
                if "ge" in want and not (have >= want["ge"]): return False
                if "lt" in want and not (have <  want["lt"]): return False
                if "le" in want and not (have <= want["le"]): return False
            elif isinstance(want, (list, tuple, set)):
                if have not in want:
                    return False
            elif have != want:
                return False
        return True

    def vt_say(girl, beat, player=None, default=""):
        """Pick the spoken line for a question beat from the response table.

        Selection: filter to entries whose `when` is fully satisfied, keep the highest `priority`,
        then the most specific (most conditions), then random among the survivors -- and finally let
        vt_voice pick the register-appropriate variant within that entry. Returns `default` (and logs,
        in developer mode) if no entry matches, so a missing state is loud rather than silent.
        """
        entries = VT_RESPONSES.get(beat, ())
        facts = _vt_context(girl, player)
        cands = [e for e in entries if _vt_match(facts, e.get("when", {}))]
        if not cands:
            if config.developer or _VT_TRACE or store.vt_dialog_trace:
                print("VT vt_say NO MATCH beat=%s girl=%s reg=%s facts=%r"
                    % (beat, getattr(girl, "name", girl), vt_explicitness_register(girl), facts))
            return default

        n_matched = len(cands)                               # entries whose `when` fit her state at all
        best_pri = max(e.get("priority", 0) for e in cands)
        cands = [e for e in cands if e.get("priority", 0) == best_pri]
        best_spec = max(len(e.get("when", {})) for e in cands)
        cands = [e for e in cands if len(e.get("when", {})) == best_spec]
        entry = renpy.random.choice(cands)
        line = vt_voice(girl, entry.get("lines", {}), default, player)

        if _VT_TRACE or store.vt_dialog_trace:
            # Full decision-state dump so the picked path can be validated independently:
            #   facts   = her complete computed fact-set (the ONLY inputs to selection)
            #   matched = how many entries fit her state; tied = how many survived to the random pick
            print("VT vt_say beat=%s girl=%s reg=%s\n    facts=%r\n    winner: pri=%s spec=%s (matched=%d tied=%d) when=%r\n    line=%r"
                % (beat, getattr(girl, "name", girl), vt_explicitness_register(girl),
                    facts, best_pri, best_spec, n_matched, len(cands), entry.get("when", {}), line))
        return line

    def vt_say_coverage(beat=None):
        """Dev helper: report beats with no catch-all (no-`when`) fallback entry.

        A beat without an unconditional fallback can return "" for an unforeseen state. Call from the
        console -- vt_say_coverage() for all beats, or vt_say_coverage("vaginal_condom_pref").
        """
        beats = [beat] if beat else list(VT_RESPONSES.keys())
        for b in beats:
            entries = VT_RESPONSES.get(b, ())
            has_fallback = any(not e.get("when") for e in entries)
            renpy.log("VT coverage: beat=%s entries=%d fallback=%s" % (b, len(entries), has_fallback))
