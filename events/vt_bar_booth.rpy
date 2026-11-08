# Bar "Invite her to a corner booth" -- port of the coffee shop booth
# (events/vt_coffeeshop_booth.rpy) to the bar location, per the user's direct request ("drunk girls...
# dark bar... shenanigans in a booth"). Appends a brand-new entry to the base game's own
# database_bar_options (no base-game file edits, no repoint needed since this option doesn't exist
# there today) that jumps into this file's own label.
#
# Reuses, rather than duplicates, every piece of the coffee shop booth's machinery that's already
# fully generic (parameterized by girl/act_key/floor, nothing coffee-shop-specific baked in):
# vt_log/vt_log_roll/vt_log_check/vt_log_acceptance_breakdown/vt_log_girl_snapshot, _vt_display_name,
# vt_voice, vt_booth_local_acceptance, vt_booth_arousal_aid, vt_booth_push_chance,
# vt_booth_lower_access_style, vt_booth_check_overstim, vt_booth_affection_tier,
# vt_booth_overlay_girl/vt_booth_arousal_overlay (the same live arousal/pressure HUD, shared since only
# one of these two booth scenes ever plays at a time), and vt_repoint_menu_label. Only genuinely
# bar-specific things are new here: the two labels below, this file's own tunable floor/penalty
# constants (a bar patron's baseline receptiveness may reasonably differ from a coffee-shop one, so
# these are fresh placeholder numbers, not reused ones), the full bar-flavored content set, and the
# new third escalation tier (below).
#
# What's different from the coffee shop version, and why:
# - Tipsy/drunk genuinely matter, for free. `Girl.get_acceptance_modifiers(action_name,
#   include_generic=True)` (class_girl_ren.py:1710-1724) adds the real "tipsy"/"drunk" traits' generic
#   acceptance bonus (class_personality_ren.py:282, trait_database_ren.py:855-872: tipsy +10, drunk
#   +20) into EVERY acceptance calculation that runs through _get_action_success_by_requirements --
#   this already covers get_acceptance_by_name (grope/finger/handjob/blowjob/fuck_pussy) AND
#   vt_booth_local_acceptance (seating/hand-hold/thigh, since it calls
#   get_acceptance_by_requirements, the same underlying method) with zero extra code. vt_log_acceptance_
#   breakdown already reproduces this same bonus term in its own logged breakdown (it calls the real
#   get_acceptance_modifiers itself), so the trait's contribution is already visible in the log with no
#   new logging needed either -- reusing that shared helper was enough. On top of that free mechanical
#   effect, a couple of has_trait("tipsy")/has_trait("drunk") narration touches are added below,
#   mirroring label_bar_discussions.rpy's own established convention for this -- deliberately NOT a
#   full parallel sobriety-tiered content system across every dict (out of scope, flagged in the plan).
# - A third, harder escalation tier: "Ride my cock" (act_key "fuck_pussy"), independent of handjob/blowjob
#   (no prerequisite that she's already done one of those first, confirmed with the user). Calls the
#   real, standalone generic_action_fuck_pussy (generic_actions_pussy.rpy:196, same call shape as
#   generic_action_handjob/blowjob: ask_to_cum=True/force_cum=False for a real finish-or-not choice) and
#   uses the real "fuck_pussy" acceptance key (pussy_actions_ren.py:628-638, floors corruption
#   45/affection 35 -- the highest floor in this whole ladder, appropriately the hardest ask) inside
#   the same shared vt_bar_booth_sex_gate label, just as a third act_key alongside "handjob"/"blowjob".
#   A creampie finish automatically routes through this mod's own existing pull-out coercion content
#   (03_vt_pullout_coercion.rpy, wired at the shared database_cum_targets level, confirmed compatible
#   with a standalone call) with no extra wiring needed.
# - Condom/consent framing for "Ride my cock" specifically, reusing the mod's real existing machinery
#   (per the user's choice -- this is the booth's first act with genuine pregnancy risk, so the gap
#   the handjob/blowjob asks quietly accept elsewhere matters here). Confirmed (00_vt_patcher.rpy's
#   vt_catch_vaginal_sex/vt_catch_vaginal_creampie hooks, wired via the action-name-keyed
#   database_apply_action_impacts_hooks list that apply_action_impacts always runs) that the real
#   mechanical consequences -- condom-breakage rolls, hymen/first-time tracking, the actual
#   birth-control-vs-fertility pregnancy check -- already fire correctly on a standalone call with zero
#   extra wiring. What's bypassed by a standalone call is only the NARRATIVE consent gate
#   (vt_condom_attempt_gate, 02_vt_gobare_coercion.rpy:234-289), which is wired onto SexAction objects a
#   standalone call never touches. Rather than duplicate that gate's dialogue, this file's own vaginal
#   call site replicates its plain decision logic directly (vt_gobare_beat(girl, act) takes plain
#   girl/act arguments, not a SexAction -- it's the real, already-register-varied coercion beat used
#   mod-wide, called directly with no new negotiation content needed): raw+wants-a-condom+not-yet-held-
#   firm-this-session triggers the real vt_gobare_beat("vaginal") coercion beat; everything else
#   (already protected, already conceded this session, never wanted one, already held firm this
#   session) short-circuits the same way vt_condom_attempt_gate itself does.
#
# Everything else (entry gate, seating roll + optional move, the flirty-action set, the
# grope/finger touch-escalation submenu, the overstim check, the arousal/pressure overlay, the
# handjob/blowjob push-respect negotiation) mirrors the coffee shop version's design 1:1 -- see that
# file's own header for the full rationale history behind each piece.
#
# VT_BAR_BOOTH_GROPE_COLD_ASK_PENALTY (65, unchanged) and VT_BAR_BOOTH_FINGER_COLD_ASK_PENALTY (85 ->
# 55, 2026-09-26) are the SAME corrected values as the coffee shop file's own fix -- caught via real
# play against a saturated/drunk girl (both formulas hit raw 100, exposing that grope's flat +15 bonus
# and finger's arousal aid could each outweigh the gap between adjacent tiers' penalties, inverting the
# intended thigh>grope>finger difficulty ordering). Re-derived again 2026-09-26 after the SAME girl
# (Kenzie Reeves) hit a second, bigger cliff between finger (18) and handjob/blowjob/ride-him (which all
# shared one flat 45 penalty, weaker than finger's 85) -- VT_BAR_BOOTH_SEX_COLD_ASK_PENALTY is now a
# per-act dict (60/65/70) instead of one shared int, and finger's own penalty came down to 55 so the
# whole hand-hold-through-ride-him chain descends in clean, even steps for the worst (no prior arousal
# built up) case. Also new this pass: an explicit, stacked drink bonus (vt_booth_intox_bonus) and a
# tiered arousal bonus (vt_booth_arousal_aid, reworked from continuous to tiered) apply at every stage.
# See vt_coffeeshop_booth.rpy's header for the full derivation (checked via a standalone script against
# 5 stat profiles, not just one).
#
# Stat-nuanced escalation rework (2026-09-26): the flat-subtraction-plus-hard-clamp scheme above is
# GONE, replaced entirely -- see vt_coffeeshop_booth.rpy's header for the full rationale (checked, this
# pass, against a wide corruption/affection grid rather than a handful of profiles: the old scheme
# collapsed almost the entire low-to-moderate stat range to the identical 5% floor, and the whole high
# end to identical numbers too). This file mirrors that fix exactly -- vt_booth_remap_chance/
# vt_booth_gap_close/vt_booth_stage_chance (all defined once in vt_coffeeshop_booth.rpy, reused as-is),
# this file's own VT_BAR_BOOTH_STAGE_ORDER/LOCAL_TIER_FLOORS/STAGE_BANDS feeding them, plus its own
# extra "fuck_pussy" stage. Also per direct user instruction: the handjob/blowjob/fuck_pussy sex gate no
# longer uses a deterministic `score >= 40` threshold -- it now rolls a die against the same chance
# number every earlier stage uses, same three-outcome shape (hard reject / negotiate-a-push / immediate
# accept) as before.
#
# Out of scope this pass, flagged not forgotten: no force-escalation tier; no "morning after regret"
# consequence hookup (that mechanism is wired to the invite-home flow's own next-day scene transition,
# which this booth doesn't have); no seating/outcome persistence beyond the single visit.

init 5 python:
    # Idempotent append (mirrors the existing vt_academy_bathroom_sex append pattern in
    # vt_location_dialogue_database_ren.py) -- this option doesn't exist in the base game today, so
    # there's nothing to repoint; a brand-new entry is added directly.
    if "database_bar_options" in globals():
        _vt_bb_marker = "vt_bar_booth"
        if not any(label == _vt_bb_marker for condition, text, label in database_bar_options):
            database_bar_options.append(
                ("'vt_bar_booth' not in actions_already_done", "Invite her to a corner booth", "vt_bar_booth")
            )
            renpy.log("VT MOD: Successfully added vt_bar_booth to database_bar_options.")
        else:
            renpy.log("VT MOD: vt_bar_booth already found in database_bar_options. Skipping addition.")
    else:
        renpy.log("VT MOD ERROR: database_bar_options not found! Could not add vt_bar_booth.")

default vt_bar_booth_vaginal_proceed = False

init python:

    # --- Tunable floors/bands -- fresh placeholder numbers for this location, not reused from the
    # coffee shop file (a bar patron's baseline receptiveness may reasonably differ), flagged for
    # tuning like every other formula in this mod. Floors themselves are kept identical to the coffee
    # shop's own choices (public-intimacy comfort is a similar underlying concept in either venue); only
    # the output bands are independently set. ---

    VT_BAR_BOOTH_ENTRY_ACCEPTANCE_THRESHOLD = 5

    # Stat-nuanced escalation rework (2026-09-26) -- see vt_coffeeshop_booth.rpy's header for the full
    # rationale (same bug, same fix, this file mirrors it exactly plus its own extra "fuck_pussy"
    # stage). Local-tier floors are unchanged from every prior pass; only how a real acceptance number
    # becomes a final chance changed. Reuses vt_coffeeshop_booth.rpy's own vt_booth_stage_chance/
    # vt_booth_remap_chance/vt_booth_gap_close/vt_booth_arousal_fraction/vt_booth_intox_fraction/
    # VT_BOOTH_GROPE_GUARANTEED_FRACTION/VT_BOOTH_SEX_PUSH_WINDOW as-is -- only the per-file
    # order/floors/bands/cache below are this file's own.
    VT_BAR_BOOTH_LOCAL_TIER_FLOORS = {
        "seating":  (5, 3),
        "handhold": (10, 5),
        "thigh":    (15, 8),
    }
    VT_BAR_BOOTH_STAGE_ORDER = ["seating", "handhold", "thigh", "grope", "finger",
                                "handjob", "blowjob", "fuck_pussy"]
    VT_BAR_BOOTH_STAGE_BANDS = {
        "seating":    (15, 96),
        "handhold":   (8, 92),
        "thigh":      (6, 86),
        "grope":      (5, 80),
        "finger":     (5, 70),
        "handjob":    (5, 58),
        "blowjob":    (5, 46),
        "fuck_pussy": (5, 34),
    }

    VT_BAR_BOOTH_IMPACTS = {
        "handhold":        {"affection": (200, 400), "corruption": (50, 150)},
        "handhold_reject": {"affection": (-150, -50)},
        "thigh":           {"corruption": (300, 600), "naturism": (200, 400)},
        "thigh_reject":    {"affection": (-150, -50)},
        "grope_reject":    {"affection": (-150, -50)},
        "finger_reject":   {"affection": (-150, -50)},
        "overstim_stop":   {"affection": (-100, -50)},
        "sex_accept":      {"corruption": (500, 1000)},
        "push_success":    {"affection": (-300, -100), "fear": (100, 300), "corruption": (400, 800)},
        "push_fail":       {"affection": (-1000, -600), "fear": (300, 600)},
        "respect":         {"affection": (100, 250)},
        "hard_reject":     {"affection": (-1500, -1000), "fear": (500, 1000)},
    }

    # --- Flirt mini-mechanic (dirty-talk) tunables, added 2026-09-27 (prototype, bar-booth only,
    # purely additive alongside "Compliment her" -- confirmed with the user, nothing above this
    # touches Compliment). Player gets VT_BAR_BOOTH_FLIRT_USES attempts per visit; each attempt picks
    # one of 4 approaches (same vocabulary as vt_bathroom.rpy's existing approach picker) and lands
    # in one of 5 deterministic tiers, no dice roll -- matching Compliment/Handhold/Thigh's own
    # gate-free feel rather than the touch-act roll system. All numbers below are first-pass
    # placeholders, flagged for tuning like every other formula in this file. ---
    VT_BAR_BOOTH_FLIRT_USES = 3

    # Local acceptance floor for the base score -- reuses vt_booth_local_acceptance (the same
    # corruption 0.6/affection 0.4/fear -0.4 template thigh/handhold already use), with thigh's own
    # floor as the closest existing intimacy-level analog for dirty talk (more forward than a
    # compliment, less physically invasive than groping).
    VT_BAR_BOOTH_FLIRT_LOCAL_FLOOR = (15, 8)  # (corruption_floor, affection_floor)

    # Approach-match/clash bonus, conceptually reused from vt_bathroom.rpy:128-152 (chosen_approach
    # vs. her freshly-computed dominant_approach) but RESCALED, not copied verbatim: that scene's
    # `approach_strength * 5` / `* 3` multipliers were calibrated against get_acceptance_by_name's
    # 0-100 output and can reach +/-500 there, which would swamp vt_booth_local_acceptance's own
    # 0-100 base score here. Scaled down to a fraction of a 0-100 base instead, capped so the bonus
    # can meaningfully shift a tier without single-handedly deciding one.
    VT_BAR_BOOTH_FLIRT_MATCH_BONUS_SCALE = 0.3    # e.g. approach_strength 100 -> +30
    VT_BAR_BOOTH_FLIRT_CLASH_PENALTY_SCALE = 0.2  # e.g. approach_strength 100 -> -20
    VT_BAR_BOOTH_FLIRT_APPROACH_CLASH_MAP = {
        "dominate": "compassionate",
        "compassionate": "dominate",
        "sexualized": "transactional",
        "transactional": "sexualized",
    }

    # Deterministic tier cutoffs on the final 0-100-ish score -- 5 tiers per direct user instruction
    # (miss/ok/good/great plus a "critical fail" below miss that ends the visit, one tier harsher
    # than a plain miss rather than reusing the touch-act hard-reject roll).
    VT_BAR_BOOTH_FLIRT_TIER_CUTOFFS = [
        ("critical_fail", 10),
        ("miss", 30),
        ("ok", 55),
        ("good", 80),
        ("great", 101),
    ]

    # Pressure moves BOTH directions by tier, per direct user instruction: landing an approach well
    # relieves pressure (like a visit going smoothly), missing it builds pressure (like an unwanted
    # touch would) -- apply_impacts already accepts negative ranges (see hard_reject/push_fail
    # above), so this is the same call shape, just a new "pressure" key with a tier-dependent sign.
    # This is also the first non-touch booth action to carry an "arousal" key -- apply_impacts()
    # already accepts one (class_girl_ren.py:2367-2386), just unused by Compliment/Handhold/Thigh
    # so far, since none of those are meant to arouse her directly.
    VT_BAR_BOOTH_FLIRT_IMPACTS_BY_TIER = {
        "miss":  {"arousal": (1, 3),   "affection": (-50, -20),                          "pressure": (3, 8)},
        "ok":    {"arousal": (3, 6)},
        "good":  {"arousal": (6, 10),  "affection": (50, 120),  "corruption": (50, 100),  "pressure": (-5, -2)},
        "great": {"arousal": (10, 16), "affection": (120, 250), "corruption": (100, 200), "pressure": (-10, -5)},
    }
    # Below "miss" -- reuses the vt_bar_booth_sex_gate hard-reject shape (spoken reject + narration
    # action line + harsh penalty + end the visit), NOT vt_booth_check_overstim (which only
    # soft-blocks further escalation and never ends the visit) -- this is the file's only actual
    # "she leaves early" convention. Slightly softer than sex_gate's own "hard_reject" since a bad
    # flirt line is a lesser offense than a hard sexual rejection, but still severe enough to end
    # the visit and carry a real pressure spike (she's rattled, on guard).
    VT_BAR_BOOTH_FLIRT_CRITFAIL_IMPACTS = {"affection": (-1200, -800), "fear": (350, 700), "pressure": (15, 25)}

    # --- Player-voiced and pure-narration flat line pools (no register -- the player doesn't have
    # one, and pure third-person narration doesn't either, matching the coffee shop file's own
    # established convention) ---

    VT_BAR_BOOTH_INVITE_LINES = [
        "Come sit with me in one of the booths for a bit -- it's quieter back there.",
        "Grab a seat with me in one of the booths? Better than shouting over the music out here.",
        "There's a booth free in the corner if you want somewhere a little more private to talk.",
    ]

    VT_BAR_BOOTH_SEAT_DOWN_ACTION_LINES = [
        "You slide into the dim corner booth, the bass from the jukebox fading to a low thrum as the vinyl seat creaks under you both.",
        "You and [selected_girl] settle into the shadowed booth, the clink of glasses and low chatter from the bar blurring into the background.",
        "You slide into the booth together, the smell of spilled liquor and old wood settling around you as the noise of the bar fades a little.",
    ]

    VT_BAR_BOOTH_SEAT_SPONTANEOUS_ACTION_LINES = [
        "Without waiting to be asked, she slides in right beside you, her leg pressing against yours in the cramped booth.",
        "She doesn't hesitate, dropping into the seat right next to you, leaving only a little space between you.",
        "She slides in beside you without a second thought, her knee bumping yours as she gets comfortable.",
    ]

    VT_BAR_BOOTH_SEAT_MOVE_AWAY_ACTION_LINES = [
        "She shrugs and slides back across to the other side of the booth.",
        "She scoots back out and drops into the seat across from you instead.",
        "She gets up briefly, then settles into the seat opposite you.",
    ]

    VT_BAR_BOOTH_SEAT_ACROSS_ACTION_LINES = [
        "She drops into the seat across from you instead, wrapping both hands around her drink.",
        "She takes the seat across the table, swirling the ice in her glass.",
        "She slides into the opposite seat, keeping the sticky table between you.",
    ]

    # --- Persona-keyed player pools (2026-09-26) -- what kind of guy is asking, from
    # vt_player_persona/vt_player_voice (defined once in vt_coffeeshop_booth.rpy, reused as-is here).
    # Every pool below defines all 5 keys; "neutral" carries this pool's original content unchanged.
    VT_BAR_BOOTH_SEAT_ASK_LINES = {
        "dominant": [
            "Come sit over here, next to me.",
            "Get over here and sit beside me.",
            "I want you sitting right here, not way over there.",
        ],
        "compassionate": [
            "Come sit over here with me, it's more fun this side.",
            "Why don't you come sit next to me? I'd like that.",
            "There's plenty of room right here beside me, if you'd like to be close.",
        ],
        "sexual": [
            "Come sit closer to me, I want you where I can touch you.",
            "Why don't you scoot in here, next to me, it's warmer.",
            "There's plenty of room right here beside me -- come get comfortable.",
        ],
        "transactional": [
            "Come sit over here with me -- it'll be worth your while.",
            "Why don't you scoot in closer? I'll make it interesting.",
            "There's plenty of room right here beside me, if you play along.",
        ],
        "neutral": [
            "Come sit over here with me, it's more fun this side.",
            "Why don't you scoot in next to me instead?",
            "There's plenty of room right here beside me, if you'd rather.",
        ],
    }

    # New utility pool (2026-09-26) -- the "would you mind sitting across instead" downgrade ask was
    # previously a single hardcoded literal, identical to the coffee shop file's own copy. Flat, not
    # persona-keyed, same reasoning as that file's version.
    VT_BAR_BOOTH_SEAT_ACROSS_ASK_LINES = [
        "Actually, would you mind sitting across from me instead?",
        "Actually, could you sit across from me instead? Just for a bit.",
        "On second thought, would you mind moving over there instead?",
    ]

    VT_BAR_BOOTH_SEAT_ASK_YES_ACTION_LINES = [
        "She hesitates, then slides around the table to sit pressed against your side.",
        "She hesitates a moment, then gets up and drops into the seat right beside you.",
    ]

    VT_BAR_BOOTH_COMPLIMENT_LINES = {
        "dominant": [
            "You know, you're mine to look at right now, and damn, you look good tonight.",
            "I like having you all to myself looking this good tonight.",
            "You look good enough that I don't want anyone else looking at you like this.",
        ],
        "compassionate": [
            "You know, I really do love just looking at you like this.",
            "You look so good -- it makes me happy just sitting here with you.",
            "I mean this -- you look wonderful tonight.",
        ],
        "sexual": [
            "God, you look good enough to eat right now.",
            "I keep getting distracted looking at you -- you're doing something to me tonight.",
            "Has anyone told you how good you look under these lights? Because it's really doing something for me.",
        ],
        "transactional": [
            "You look great tonight -- and I'd say that even if I didn't want something from you.",
            "A compliment like that usually gets me somewhere, right?",
            "You look good tonight -- good enough that I figure you owe me a smile at least.",
        ],
        "neutral": [
            "You know, you look really good tonight.",
            "I keep getting distracted looking at you.",
            "Has anyone told you how good you look under these lights?",
        ],
    }

    VT_BAR_BOOTH_HANDHOLD_SAMESIDE_LINES = {
        "dominant": [
            "You take her hand under the table, holding it like it's already yours.",
            "You take her hand under the table, firm and sure.",
            "You close your hand around hers under the table, no hesitation.",
        ],
        "compassionate": [
            "You gently take her hand under the table, lacing your fingers through hers.",
            "You reach over and take her hand under the table, holding it softly.",
            "You take her hand under the table, giving it a warm, reassuring squeeze.",
        ],
        "sexual": [
            "You take her hand under the table, thumb tracing slowly over her palm.",
            "You slide your hand over and take hers under the table, letting your fingers linger.",
            "You take her hand under the table, drawing it slowly closer to your lap.",
        ],
        "transactional": [
            "You take her hand under the table, an easy, practiced little gesture.",
            "You slide your hand over and take hers under the table, testing how she reacts.",
            "You take her hand under the table, curious how far it gets you tonight.",
        ],
        "neutral": [
            "You take her hand under the table.",
            "You slide your hand over and take hers under the table.",
            "You reach under the table and take her hand in yours.",
        ],
    }

    VT_BAR_BOOTH_HANDHOLD_ACROSS_LINES = {
        "dominant": [
            "You reach across the sticky table and take her hand, holding it firmly.",
            "You reach over the table and take her hand without waiting for permission.",
            "You reach across the table, closing your hand around hers.",
        ],
        "compassionate": [
            "You reach across the sticky table and take her hand gently.",
            "You reach over the table, fingers closing softly around hers.",
            "You reach across and take her hand, giving it a warm squeeze.",
        ],
        "sexual": [
            "You reach across the sticky table and take her hand, tracing your thumb over her knuckles.",
            "You reach over the table, letting your fingers slide slowly around hers.",
            "You reach across and take her hand, unable to help lingering there.",
        ],
        "transactional": [
            "You reach across the sticky table and take her hand, an easy, practiced move.",
            "You reach over the table, taking her hand like it's the natural next step.",
            "You reach across and take her hand, curious how far tonight goes.",
        ],
        "neutral": [
            "You reach across the sticky table and take her hand.",
            "You reach over the table, fingers closing gently around hers.",
            "You reach across the table and take her hand in yours.",
        ],
    }

    VT_BAR_BOOTH_THIGH_ASK_LINES = {
        "dominant": [
            "You rest a hand on her thigh under the table, claiming your spot without asking.",
            "You slide a hand onto her thigh in the dark of the booth, gripping it like you own the right to.",
            "Under the table, you plant a hand firmly on her thigh and let it stay there.",
        ],
        "compassionate": [
            "You rest a gentle hand on her thigh under the table, giving it a light, affectionate squeeze.",
            "You slide your hand onto her thigh in the dark of the booth, resting it there warmly.",
            "Under the table, you let your hand settle on her thigh, thumb tracing slow, soft circles.",
        ],
        "sexual": [
            "You slide a hand onto her thigh under the table, fingers already inching hungrily upward.",
            "You rest a hand high on her thigh in the dark of the booth, unable to resist creeping further.",
            "Under the table, your hand finds her thigh and drags slowly higher, greedy for more.",
        ],
        "transactional": [
            "You rest a hand on her thigh under the table, testing how far she'll let this go.",
            "You slide a hand onto her thigh in the dark of the booth, treating it as fair game now.",
            "Under the table, you let your hand settle on her thigh, seeing what you can get away with.",
        ],
        "neutral": [
            "You rest a hand on her thigh under the table, sliding it slowly upward.",
            "You slide a hand onto her thigh in the dark of the booth, fingers trailing higher.",
            "Under the table, you let your hand settle on her thigh and inch it up.",
        ],
    }

    # Flat, non-register access-narration keyed by vt_booth_lower_access_style (reused directly from
    # the coffee shop file -- fully generic, no coffee-shop-specific behavior). "dress" covers both a
    # worn dress and a skirt; "pants" covers jeans/leggings/shorts.
    VT_BAR_BOOTH_GROPE_ACCESS_LINES = {
        "dress": [
            "You slide your hand up her thigh and beneath her hem, in the cover of the dark booth.",
            "You slip your hand up beneath her hem, palm sliding slowly up the inside of her thigh.",
        ],
        "pants": [
            "You press your hand between her thighs, feeling the fabric give slightly as you push against her.",
            "You cup your hand between her legs, the fabric doing little to hide how she reacts to the pressure.",
        ],
        "bare": [
            "With nothing in the way, you slide your hand straight between her thighs.",
            "There's nothing to work around -- you slide your hand right between her legs.",
        ],
        "generic": [
            "You slide your hand between her thighs in the dark of the booth, searching out just where she wants to be touched.",
            "You work your hand between her legs, feeling her tense slightly at the contact.",
        ],
    }

    VT_BAR_BOOTH_GROPE_CONTINUE_LINES = [
        "You keep groping her under the table, feeling her squirm against you.",
        "You keep rubbing her under the table, unhurried, the booth hiding it all.",
    ]

    # Shared across all overstim-stop call sites (same beat every time, one pool, matching the coffee
    # shop's own dedup).
    # Hand-specific -- fits the grope/finger touch loop (his hand on/in her), not the sex-gate acts
    # below (her hand on him, her mouth, or her riding him) -- see VT_BAR_BOOTH_SEX_OVERSTIM_ACTION_LINES.
    VT_BAR_BOOTH_OVERSTIM_ACTION_LINES = [
        "She grabs your wrist, pushing your hand away, breathing hard.",
        "She catches your wrist and pushes your hand back, chest heaving.",
        "She clamps a hand over yours, stopping you, breathing hard.",
    ]

    VT_BAR_BOOTH_TOUCH_STOP_ACTION_LINES = [
        "You ease your hand back, giving her a moment to catch her breath.",
        "You slowly withdraw your hand, letting her catch her breath.",
    ]

    # Flat, non-register, keyed by (technique, style) for the first touch and by (last, this) for
    # every transition after -- same shape as the coffee shop file's own dicts.
    VT_BAR_BOOTH_TOUCH_ACCESS_LINES = {
        "finger": {
            "dress": [
                "You reach beneath her hem, moving any remaining fabric aside, and slide a finger inside her.",
                "You work your hand beneath her hem and past any remaining coverage, then press a finger into her.",
            ],
            "pants": [
                "You work your hand past her waistband and any remaining fabric, then slide a finger inside her.",
                "You reach past her waistband, clear any remaining coverage, and press a finger into her.",
            ],
            "bare": [
                "You move slowly, watching her reaction as your touch grows more intimate.",
                "You press a finger into her, with nothing to work around.",
            ],
            "generic": [
                "You move any fabric out of the way and slide a finger inside her.",
                "You find your way past any remaining coverage and press a finger into her.",
            ],
        },
        "two_fingers": {
            "dress": [
                "You reach beneath her hem, moving any remaining fabric aside, and slide two fingers inside her.",
                "You work your hand beneath her hem and past any remaining coverage, then press two fingers into her.",
            ],
            "pants": [
                "You work your hand past her waistband and any remaining fabric, then slide two fingers inside her.",
                "You reach past her waistband, clear any remaining coverage, and press two fingers into her.",
            ],
            "bare": [
                "You let her settle against you before deepening the touch.",
                "You press two fingers into her, with nothing to work around.",
            ],
            "generic": [
                "You move any fabric out of the way and slide two fingers inside her.",
                "You find your way past any remaining coverage and press two fingers into her.",
            ],
        },
        "clit": {
            "dress": [
                "You reach beneath her hem, move any remaining fabric aside, and rub slow circles over her clit.",
                "You work your hand beneath her hem and past any remaining coverage, then settle your fingers on her clit.",
            ],
            "pants": [
                "You work your hand past her waistband and any remaining fabric, then find her clit and rub slow circles.",
                "You reach past her waistband, clear any remaining coverage, and settle your fingers on her clit.",
            ],
            "bare": [
                "You find a steady rhythm, keeping your movements small beneath the table.",
                "You settle your fingers on her clit, with nothing to work around.",
            ],
            "generic": [
                "You move any fabric out of the way, then rub slow circles over her clit.",
                "You find your way past any remaining coverage and settle your fingers on her clit.",
            ],
        },
    }

    VT_BAR_BOOTH_TOUCH_TRANSITION_LINES = {
        ("clit", "clit"): [
            "You keep circling her clit, matching her rhythm.",
            "You keep rubbing slow circles against her clit.",
        ],
        ("finger", "finger"): [
            "You keep working your finger inside her, steady and deep.",
            "You keep your finger moving steadily inside her.",
        ],
        ("two_fingers", "two_fingers"): [
            "You keep working both fingers inside her, steady and deep.",
            "You keep both fingers moving steadily inside her.",
        ],
        ("clit", "finger"): [
            "You slide a finger inside her, thumb still working her clit.",
            "You press a finger into her, still circling her clit at the same time.",
        ],
        ("clit", "two_fingers"): [
            "You slide two fingers inside her at once, thumb still working her clit.",
            "You press two fingers into her, still circling her clit at the same time.",
        ],
        ("finger", "two_fingers"): [
            "You work a second finger in alongside the first.",
            "You ease a second finger in beside the first, filling her more.",
        ],
        ("finger", "clit"): [
            "You ease your finger out and settle on her clit instead, rubbing slow circles.",
            "You pull your finger free, focusing on her clit instead.",
        ],
        ("two_fingers", "clit"): [
            "You slide your fingers free and settle on her clit, circling it slowly.",
            "You ease both fingers out, focusing on her clit instead.",
        ],
        ("two_fingers", "finger"): [
            "You ease one finger free, keeping just one moving steadily inside her.",
            "You pull one finger back, working her with just the other.",
        ],
    }

    VT_BAR_BOOTH_PUSH_PITCH = {
        "dominant": [
            "Come on, I want this. Just do it.",
            "Quit worrying about who's watching and just go along with it.",
            "Nobody's going to say anything. Come on, now.",
        ],
        "compassionate": [
            "Please? I promise it'll be okay, I just really want this with you.",
            "Come on, it means a lot to me. I promise no one will notice.",
            "I wouldn't ask if I didn't trust this was okay. Please, just this once?",
        ],
        "sexual": [
            "Come on, you want this too, don't pretend you don't.",
            "We're both dying for it -- no one's paying attention, I promise.",
            "Just feel how bad we both want this. Come on.",
        ],
        "transactional": [
            "Come on, I'll make it worth it for you. Just this once.",
            "Do this for me and I'll owe you one, I promise.",
            "Nobody's going to notice, and I'll make sure you don't regret it.",
        ],
        "neutral": [
            "Come on, it's dark back here and everyone's watching the game, not us. Just this once.",
            "Nobody's paying attention over here, I promise. Please?",
            "We're tucked away enough, it'll be fine -- come on.",
        ],
    }

    VT_BAR_BOOTH_PUSH_FAIL_ACTION_LINES = [
        "She draws back with a hurt frown, gathers her things, and slides out of the booth. She leaves the bar without looking back.",
        "She shakes her head and takes a moment to collect herself. Then she gathers her things and leaves the bar, ending the conversation.",
        "She stands, gathers her things, and leaves the bar before you can say anything else.",
    ]

    VT_BAR_BOOTH_HARD_REJECT_ACTION_LINES = [
        "She shoves her drink aside and gets out of the booth, drawing a few glances. Gathering her things with a tense expression, she leaves the bar.",
        "She pulls away, visibly upset, and gathers her things. She slides out of the booth and heads straight out of the bar.",
        "She takes her things and walks out of the bar, leaving you alone at the table.",
    ]

    VT_BAR_BOOTH_DECLINE_ACTION_LINES = [
        "She shifts uncomfortably, her eyes darting away as she clutches her glass a little tighter.",
        "She shifts in her seat, avoiding your eyes as she wraps both hands around her drink.",
        "She keeps her place and turns her attention back to the room.",
    ]

    # Shown only when the visit ends normally (not after a hard reject or a failed push -- see
    # _vt_bar_booth_sour_ending below, same fix the coffee shop file already applies).
    VT_BAR_BOOTH_VISIT_END_ACTION_LINES = [
        "You finish your drinks and give her room to get up. She gathers her things, says goodbye, and leaves the bar.",
        "As you finish your drinks, she gathers her things and slides out of the booth. She gives you a parting nod before leaving the bar.",
        "After a final sip, she says goodbye, collects her things, and makes her way out of the bar.",
    ]

    # Has_trait("drunk")/has_trait("tipsy") narration touch #1 -- shown alongside (not instead of) the
    # normal seat-down line, mirroring label_bar_discussions.rpy's own established convention for this.
    VT_BAR_BOOTH_TIPSY_SEAT_LINES = [
        "She's clearly had a couple already, a looseness in the way she leans into you.",
        "There's a warm flush in her cheeks from the drinks so far, her laugh coming a little too easy.",
    ]

    VT_BAR_BOOTH_DRUNK_SEAT_LINES = [
        "She's visibly drunk, swaying slightly as she drops into the seat, her filter all but gone.",
        "She's had way more than a couple -- she practically falls into the booth, giggling at nothing in particular.",
    ]

    # --- Drunk/tipsy slurred-speech variants (2026-09-26), per direct user request. Bar-only -- the
    # coffee shop has no drunk/tipsy narration and doesn't get this. Curated to her 8 escalating "yes"
    # moments and the climax line (not every dict -- reject/negotiation lines stay plain register
    # content, matching the user's own "slightly different," not a full parallel voice track). Flat,
    # not register-keyed: being drunk already overrides a lot of her usual register-driven word choice,
    # so crossing drunk-state x register x variants would balloon this into exactly the "full parallel
    # sobriety-tiered content system across every dict" this file's own header already declined to
    # build. Style, following label_bar_discussions.rpy's own established convention: drunk = apostrophe
    # elisions/dropped endings/an occasional "hic"; tipsy = milder, mostly normal spelling with just
    # looser word choice, no elisions. The real acceptance bonus these traits grant already applies to
    # the roll itself (see the file header) -- this is purely the narration half.
    VT_BAR_BOOTH_COMPLIMENT_REACT_DRUNK = [
        "Heh, y'think so? *hic* You're sweet.",
        "Aw, stop it... you're gonna make me blush, ya charmer.",
        "Mmm, keep talkin' like that and I'll keep drinkin' with you.",
    ]
    VT_BAR_BOOTH_COMPLIMENT_REACT_TIPSY = [
        "Heh, you think so? That's sweet of you.",
        "Aw, stop it, you're making me blush.",
        "Mmm, keep talking like that and I might just believe you.",
    ]

    VT_BAR_BOOTH_HANDHOLD_ACCEPT_DRUNK = [
        "Heh, gettin' handsy, huh? *hic* I don't mind.",
        "Mmm, your hand's warm... I like it.",
        "Aw, that's kinda sweet, y'know that?",
    ]
    VT_BAR_BOOTH_HANDHOLD_ACCEPT_TIPSY = [
        "Heh, getting handsy, huh? I don't mind.",
        "Mmm, your hand's warm, I like it.",
        "Aw, that's kind of sweet, you know.",
    ]

    VT_BAR_BOOTH_THIGH_REACT_DRUNK = [
        "Ooh, someone's bold tonight. *hic* I like it.",
        "Mmm, careful, or I might just let you keep goin'.",
        "Heh, somebody's feelin' brave, huh?",
    ]
    VT_BAR_BOOTH_THIGH_REACT_TIPSY = [
        "Ooh, someone's bold tonight. I like it.",
        "Mmm, careful, or I might just let you keep going.",
        "Heh, somebody's feeling brave, huh?",
    ]

    VT_BAR_BOOTH_GROPE_ACCEPT_DRUNK = [
        "Mmh, fuck it, *hic* go ahead.",
        "Heh, why not. Keep goin'.",
        "Mmm, don't stop, that feels good.",
    ]
    VT_BAR_BOOTH_GROPE_ACCEPT_TIPSY = [
        "Mmh, why not, go ahead.",
        "Heh, keep going, I don't mind.",
        "Mmm, don't stop, that feels nice.",
    ]

    VT_BAR_BOOTH_FINGER_ACCEPT_DRUNK = [
        "Fuck, *hic* fine, get in there.",
        "Mmh, go on then, don't stop.",
        "Heh, yeah, touch me, I don't care who sees.",
    ]
    VT_BAR_BOOTH_FINGER_ACCEPT_TIPSY = [
        "Fine, go ahead, I don't mind.",
        "Mmh, go on then, don't stop.",
        "Heh, yeah, go for it.",
    ]

    VT_BAR_BOOTH_TOUCH_ACCEPT_DRUNK = [
        "Fuck, yes, *hic* don't stop, that feels so good.",
        "Mmh, right there, don't you dare stop.",
        "Ohh fuck, keep goin', please.",
    ]
    VT_BAR_BOOTH_TOUCH_ACCEPT_TIPSY = [
        "Yes, don't stop, that feels good.",
        "Mmh, right there, keep going.",
        "Ohh, keep going, please.",
    ]

    # Shared across all 3 acts (handjob/blowjob/fuck_pussy) -- a drunk/tipsy exclamation doesn't need
    # to name the specific act, unlike VT_BAR_BOOTH_SEX_ACCEPT itself.
    VT_BAR_BOOTH_SEX_ACCEPT_DRUNK = [
        "Heh, fuck it, why not. *hic* Let's do it.",
        "Mmh, yeah, alright, c'mere.",
        "Fuck it, I'm down. Let's go.",
    ]
    VT_BAR_BOOTH_SEX_ACCEPT_TIPSY = [
        "Heh, why not, alright, let's do it.",
        "Mmh, yeah, alright, come here.",
        "Alright, I'm down. Let's go.",
    ]

    VT_BAR_BOOTH_GIRL_ORGASM_DRUNK = [
        "Oh fuck, *hic* I'm cummin'!",
        "Fuck, fuck, I'm cummin', don't stop!",
        "Ohh fuck yes, I'm cummin'!",
    ]
    VT_BAR_BOOTH_GIRL_ORGASM_TIPSY = [
        "Oh, I'm coming!",
        "Mmm, yes, I'm coming, don't stop!",
        "Ohh, right there, I'm coming!",
    ]

    # --- Drunk/tipsy slurred-speech variants for REFUSAL/stop beats (2026-09-26), per direct user
    # follow-up: her refusals need the same slurred/looser treatment her positive lines already got,
    # not just her "yes" moments. Same flat, non-register shape and style guide as the accept-side
    # pools above (drunk = apostrophe elisions/dropped endings/an occasional "hic"; tipsy = milder,
    # normal spelling with just looser word choice) -- each variant still lands as the SAME refusal the
    # sober line does, just looser-spoken.

    VT_BAR_BOOTH_DECLINE_DRUNK = [
        "Nah, m'good right here.",
        "Nnh, I'll pass on that, *hic*.",
        "Not really feelin' it, I'll just stay put.",
    ]
    VT_BAR_BOOTH_DECLINE_TIPSY = [
        "Nah, I'm good right here, but thanks.",
        "I'll pass on that one, but thanks for asking.",
        "Not really feeling it, I'll just stay put.",
    ]

    VT_BAR_BOOTH_HANDHOLD_REJECT_DRUNK = [
        "Nnh, not that comfortable yet, slow down.",
        "Easy there, *hic*, not yet.",
        "Mmh, hold up, not ready for that.",
    ]
    VT_BAR_BOOTH_HANDHOLD_REJECT_TIPSY = [
        "Not that comfortable yet, slow down a little.",
        "Easy there, not yet, okay?",
        "Hold on, I'm not ready for that yet.",
    ]

    VT_BAR_BOOTH_THIGH_REJECT_DRUNK = [
        "Nnh, not there, not yet.",
        "Whoa, slow down, *hic*.",
        "Mmh, not yet, not there.",
    ]
    VT_BAR_BOOTH_THIGH_REJECT_TIPSY = [
        "Not there, not yet, okay?",
        "Whoa, slow down a little.",
        "Not yet, let's slow down.",
    ]

    VT_BAR_BOOTH_GROPE_REJECT_DRUNK = [
        "Whoa, not here, *hic*, slow down.",
        "Easy, not that far, not here.",
        "Nnh, not here, too much.",
    ]
    VT_BAR_BOOTH_GROPE_REJECT_TIPSY = [
        "Whoa, not here, slow down a little.",
        "Easy, not that far, not here.",
        "Not here, that's too much right now.",
    ]

    VT_BAR_BOOTH_FINGER_REJECT_DRUNK = [
        "Whoa, hold up, *hic*, not that far.",
        "Easy, that's too much here.",
        "Nnh, not here, not that.",
    ]
    VT_BAR_BOOTH_FINGER_REJECT_TIPSY = [
        "Whoa, hold on, not that far.",
        "Easy, that's too much right now.",
        "Not here, let's not go that far.",
    ]

    VT_BAR_BOOTH_HARD_REJECT_DRUNK = [
        "Are you fuckin' serious? *hic* I'm out of here!",
        "Whoa, no way, I'm gone!",
        "Nnh, that's too much, I'm leavin'!",
    ]
    VT_BAR_BOOTH_HARD_REJECT_TIPSY = [
        "Are you serious? I'm leaving!",
        "Whoa, no way, I'm out of here!",
        "That's too much, I'm leaving!",
    ]

    VT_BAR_BOOTH_PUSH_FAIL_DRUNK = [
        "No! I said not here, *hic*, drop it. I'm leavin'.",
        "Nnh, I meant it, not here. I'm leavin'.",
        "No, c'mon, I said no. I'm leavin'.",
    ]
    VT_BAR_BOOTH_PUSH_FAIL_TIPSY = [
        "No, I meant it, not here. I'm leaving.",
        "I said no, come on. I'm leaving.",
        "No, not here, I mean it. I'm leaving.",
    ]

    # Not triggered by an explicit ask, but still a real "no more, stop" beat -- included for the same
    # "in general" completeness the user asked for.
    VT_BAR_BOOTH_OVERSTIM_STOP_DRUNK = [
        "Fuck, stop, *hic*, that's too much, I can't.",
        "Nnh, stop, I need a sec.",
        "Whoa, stop, too much, too much.",
    ]
    VT_BAR_BOOTH_OVERSTIM_STOP_TIPSY = [
        "Stop, please, that's too much.",
        "Wait, stop, I need a moment.",
        "Okay stop, that's too much right now.",
    ]

    # --- Register-keyed reaction lines (6 registers, 2+ variants each) ---

    VT_BAR_BOOTH_ACCEPT = {
        "crude":    ["Fuck yeah, let's go get a drink and sit down.", "Sure, let's go park our asses in a booth.", "Hell yes, lead the way."],
        "explicit": ["Mmm, sounds perfect. Let's go sit.", "Oh, I'd love that. Let's go.", "Yes -- I could use somewhere quieter."],
        "direct":   ["Sure, that sounds nice. Let's sit.", "Sounds good. Let's grab that booth.", "Alright, sounds nice. Let's go."],
        "neutral":  ["Sure, that sounds nice.", "Okay, sounds good to me.", "Sure, I'd like that."],
        "shy":      ["O-oh, sure, that sounds nice...", "Um, okay, I'd like that...", "S-sure, I guess that'd be nice."],
        "demure":   ["That sounds lovely, thank you.", "I would enjoy that, yes.", "Certainly, that sounds pleasant."],
    }

    VT_BAR_BOOTH_DECLINE = {
        "crude":    ["No thanks, I'm good right here.", "Nah, I'll pass on that.", "Not really feeling it, I'll stay put."],
        "explicit": ["No thanks... I'm fine right here.", "I'd rather just stay here, sorry.", "Mmh, not right now -- I'll stay here."],
        "direct":   ["No thanks, I'm fine right here.", "I'll pass -- I'm comfortable here.", "No, I think I'll stay right here."],
        "neutral":  ["No thanks... I'm fine right here.", "I think I'll just stay here.", "No, I'm alright where I am."],
        "shy":      ["N-no thanks... I'm fine here...", "I-I'd rather stay here, sorry...", "Um... m-maybe another time..."],
        "demure":   ["No, thank you. I am fine right here.", "I would prefer to remain here, thank you.", "That is kind, but I must decline."],
    }

    VT_BAR_BOOTH_SEAT_TOGETHER = {
        "crude":    ["Move over, I'm sitting right next to you.", "Scoot in, I'm not sitting way over there.", "I'm parking myself right next to you, budge up."],
        "explicit": ["Mmm, I want to sit close to you.", "I'd rather sit right beside you.", "Mmm, I'll just squeeze in right beside you."],
        "direct":   ["I'll sit next to you, if that's alright.", "I'll just sit here beside you.", "I'd rather sit beside you, if you don't mind."],
        "neutral":  ["I'll sit next to you.", "I'll just sit here beside you, is that okay?", "I think I'll sit right beside you."],
        "shy":      ["I-is it okay if I sit next to you...?", "C-can I just sit here, beside you...?", "U-um, is it alright if I sit close...?"],
        "demure":   ["I would prefer to sit beside you, if you don't mind.", "Might I sit next to you instead?", "I believe I shall sit beside you, if that suits."],
    }

    VT_BAR_BOOTH_SEAT_ACROSS = {
        "crude":    ["I'll sit over here, where I can see you.", "I'm taking this side, thanks.", "I'll just park myself over here."],
        "explicit": ["I'll just sit across from you.", "I'll take this side, if that's fine.", "Mmm, I'll sit here across from you."],
        "direct":   ["I'll sit across from you.", "I'll take this seat, across from you.", "I think I'll sit over here instead."],
        "neutral":  ["I'll sit over here.", "I'll take this side.", "I think I'll sit across from you."],
        "shy":      ["I-I'll just sit over here...", "U-um, I'll sit across, if that's okay...", "I-I think I'll sit over here instead..."],
        "demure":   ["I shall sit across from you.", "I will take this seat, if you don't mind.", "I believe I shall take the seat across."],
    }

    VT_BAR_BOOTH_SEAT_ASK_YES = {
        "crude":    ["Fine, scooting my ass over there.", "Ugh, fine -- budge up.", "Alright, alright -- moving."],
        "explicit": ["Mmh, alright... budge over then.", "Okay... I'll come sit with you.", "Mmh, fine -- scoot over for me."],
        "direct":   ["Alright, I'll come sit next to you.", "Okay, fine -- I'll move over.", "Alright, I'll come sit beside you then."],
        "neutral":  ["Okay, I'll come sit next to you.", "Alright, I'll move over.", "Okay, I'll come sit beside you."],
        "shy":      ["O-okay... I'll come sit next to you...", "Um, okay... if you want me to...", "O-okay, if that's what you want..."],
        "demure":   ["Very well, I shall sit beside you.", "If you wish it, I will move over.", "Very well, I shall join you there."],
    }

    VT_BAR_BOOTH_SEAT_ASK_NO = {
        "crude":    ["Nah, I'm good right here.", "No way, I'm staying put.", "Nope, not moving."],
        "explicit": ["No, I'd rather stay right here.", "I'll just stay over here, thanks.", "Mmh, no -- I'll stay right here."],
        "direct":   ["No, I'll stay here.", "I'd rather stay across from you.", "No, I think I'll stay put."],
        "neutral":  ["No, I'll just stay here.", "I think I'll stay right here.", "No, I'll stay where I am."],
        "shy":      ["N-no, I'll just stay here...", "I-I'd rather stay over here...", "S-sorry, I'll just stay here..."],
        "demure":   ["No, I shall remain here, thank you.", "I would prefer to stay right here.", "No, I believe I shall remain here."],
    }

    VT_BAR_BOOTH_SEAT_MOVE_AWAY = {
        "crude":    ["Eh, whatever.", "Sure, no big deal.", "Fine by me."],
        "explicit": ["Oh, okay, sure.", "Mmh, alright then.", "Mmm, sure, whatever you'd like."],
        "direct":   ["Sure, no problem.", "Okay, that's fine.", "Sure, that works."],
        "neutral":  ["Oh, okay, sure.", "Sure, that's fine.", "Okay, no problem."],
        "shy":      ["Oh -- okay...", "U-um, sure...", "O-okay, if you'd like..."],
        "demure":   ["Very well, if you prefer.", "Of course, as you wish.", "Certainly, if that is your preference."],
    }

    VT_BAR_BOOTH_COMPLIMENT_REACT = {
        "low": {
            "crude":    ["Sure, whatever you say.", "Uh, thanks I guess.", "Yeah, okay, sure."],
            "explicit": ["Oh... thanks, I suppose.", "That's... nice of you to say.", "Oh -- well, thank you, I guess."],
            "direct":   ["Thanks, I suppose.", "That's kind, I guess.", "Thank you, I guess."],
            "neutral":  ["Thanks, I guess.", "Oh, um, thank you.", "Oh, thanks."],
            "shy":      ["Oh... um, thanks...", "I-I don't know what to say...", "Oh... th-thank you, I think..."],
            "demure":   ["That is... kind of you to say.", "I suppose I should thank you.", "That is... unexpected, but thank you."],
        },
        "mid": {
            "crude":    ["Damn right I do.", "Ha, I know, right?", "Ha, glad you noticed."],
            "explicit": ["Mmm, thank you. You're sweet.", "Oh stop, you're making me blush.", "Mmm, you really know how to flatter me."],
            "direct":   ["Thanks, that's kind of you to say.", "Thank you, that's nice to hear.", "Thank you, that's sweet of you."],
            "neutral":  ["Thank you, that's sweet.", "Aw, thank you.", "Thank you, that's kind."],
            "shy":      ["O-oh... thank you...", "R-really? Thanks...", "Th-thank you, that's sweet..."],
            "demure":   ["Thank you, that is very kind.", "You flatter me, thank you.", "That is very sweet of you to say."],
        },
        "high": {
            "crude":    ["Fuck yeah, I know I look good.", "Damn right, and you noticed.", "Hell yeah, I've still got it."],
            "explicit": ["Mmm, I love hearing that from you.", "You really know what to say to me.", "Mmm, keep talking like that and see what happens."],
            "direct":   ["I really appreciate you saying that.", "That means a lot, coming from you.", "That really does mean a lot to me."],
            "neutral":  ["That means a lot, thank you.", "You really know how to make me smile.", "You really know how to make my night."],
            "shy":      ["Th-thank you, that means so much...", "You really mean that? Thank you...", "I... I really needed to hear that..."],
            "demure":   ["You are far too kind to me.", "That means more to me than you know.", "You have such a gift for kind words."],
        },
    }

    VT_BAR_BOOTH_COMPLIMENT_IMPACTS_BY_TIER = {
        "low":  {"affection": (50, 150)},
        "mid":  {"affection": (150, 300)},
        "high": {"affection": (300, 500)},
    }

    # --- Flirt mini-mechanic line pools (2026-09-27) ---
    #
    # Approach-keyed (not persona-keyed): unlike Compliment, the player explicitly PICKS the approach
    # here via its own sub-menu, so the line reflects his deliberate choice rather than an
    # auto-detected persona. All 4 keys from vt_bathroom.rpy's existing vocabulary. Routed through
    # _vt_resolve_words (not vt_voice, since there's no register axis to pick here -- the approach
    # IS the picked key) so %slot% lexicon tokens still resolve against her current register/stats.
    VT_BAR_BOOTH_FLIRT_LINES = {
        "dominate": [
            "I want you to %verb_command%. You're mine to enjoy tonight.",
            "Tonight I want you %adj_desperate%, so %verb_command%.",
            "I like you like this -- %verb_command%. Let me look at you.",
            "You don't get a say in this. I want you to %verb_command%. Let me enjoy your %noun_ass%.",
            "I own this table tonight, and I own you -- %verb_command%.",
        ],
        "compassionate": [
            "You look %adj_praise%, and I can't stop thinking about how much I %verb_desire% you right now.",
            "Being here with you like this... I %verb_desire% you more than I probably should say out loud.",
            "You make me feel so much just sitting here -- I %verb_desire% you, all of you.",
            "Sitting here with you, I %verb_desire% you. I want to hold you close.",
            "You look %adj_praise% tonight -- I %verb_desire% you so much right now.",
        ],
        "sexualized": [
            "I keep imagining you in my lap right here, right now.",
            "God, I %verb_desire% you. I want to feel you around me tonight.",
            "I'm %adj_desperate% right now. I want my hands on your %noun_breasts%.",
            "I keep picturing your %noun_mouth% wrapped around me under this table.",
            "I want to watch you finish right here, and I don't care who sees.",
        ],
        "transactional": [
            "You look %adj_praise%. Keep me company and I'll make sure tonight is worth your while.",
            "I %verb_desire% you tonight -- and I promise it'll pay off for both of us.",
            "Play along with me a little, and you'll like what you get out of it.",
            "You look %adj_praise%, and I'd make it very worth your time tonight.",
            "Keep talking to me like this and you'll walk away happy -- I always pay what I owe.",
        ],
    }

    # Register-keyed reaction lines per outcome tier (miss/ok/good/great -- critical_fail has its own
    # separate reject pool below, mirroring hard_reject). 5 variants per cell (up from 3, 2026-09-27
    # revision -- the original 3-variant pass read as "SUPER boring" per direct user feedback), with
    # heavier lexicon use on good/great (where she's actually getting worked up) than miss/ok (where
    # she isn't) -- matches the tone each tier is meant to convey rather than sprinkling tokens evenly.
    VT_BAR_BOOTH_FLIRT_REACT_BY_TIER = {
        "miss": {
            "crude":    ["Ugh, that's not doing anything for me.", "Try again, that was weak as hell.", "Yeah, no. That did nothing.", "Ugh, is that seriously the best you've got?", "Pathetic. Try something that actually works."],
            "explicit": ["Mmm, no, that didn't really land.", "That's not really working for me right now.", "Hm, that one just didn't land.", "Mmm, that barely did anything for me.", "Oh, that one really missed the mark."],
            "direct":   ["That didn't really do anything for me.", "Not really my thing, try something else.", "That one missed, honestly.", "That really didn't land the way you wanted.", "Hm, that one just fell flat."],
            "neutral":  ["That didn't really land.", "Hm, not really feeling that.", "That one didn't do much for me.", "I don't know, that one just felt off.", "That wasn't really it, sorry."],
            "shy":      ["Oh... um, that didn't really do it for me...", "I-I don't really know how to respond to that...", "Um... that was a little awkward...", "Oh... I wasn't really expecting that, and not in a good way...", "Um, I don't think that's really my thing..."],
            "demure":   ["That is not quite what I was hoping to hear.", "I am afraid that did not move me much.", "That did not quite land as intended.", "I must say, that fell rather flat.", "That was, regrettably, not to my taste."],
        },
        "ok": {
            "crude":    ["Heh, okay, that's something at least.", "Not bad, keep going.", "Eh, decent enough.", "Heh, alright, I'll give you that one.", "Not bad. Keep talking, see where it goes."],
            "explicit": ["Mmm, okay, that's kind of working.", "That's... okay, I'll give you that.", "Mmm, not bad at all.", "Mmm, okay, that's a start.", "That's kind of sweet, actually, in a hot way."],
            "direct":   ["Okay, that's not bad.", "That's alright, I suppose.", "That's fair, I'll admit.", "Okay, I can work with that.", "That's decent, keep going."],
            "neutral":  ["That's okay, I guess.", "Hm, that's alright.", "That's fine, I suppose.", "Hm, that's a decent start.", "That's okay, I'll admit."],
            "shy":      ["Oh... that's kind of sweet, I guess...", "Um, okay... that's not bad...", "Oh... that's alright, I think...", "Um... that was kind of nice, actually...", "Oh, um... I liked that, a little..."],
            "demure":   ["That is... acceptable, I suppose.", "That was not unwelcome.", "That was tolerably charming.", "I suppose that was rather sweet.", "That was, I admit, somewhat charming."],
        },
        "good": {
            "crude":    ["Fuck, okay, keep talking like that.", "Damn, I'm %adj_desperate% now.", "Shit, okay, that landed.", "Fuck, say that again, that's actually working.", "Damn, keep going, my %noun_pussy% is starting to notice."],
            "explicit": ["Mmm, that's really working for me.", "Keep talking like that and see what happens.", "Mmm, that's actually getting to me.", "God, keep going, I'm getting a little %adj_desperate%.", "Mmm, my %noun_pussy% is starting to ache a little."],
            "direct":   ["Okay, that's actually pretty good.", "That's working, keep going.", "Okay, I actually liked that.", "Okay, I'm getting a little %adj_desperate% now.", "That's actually turning me on a bit."],
            "neutral":  ["That's actually really nice to hear.", "Okay, that's getting to me a little.", "Hm, that actually worked on me.", "Okay, I'm feeling a little %adj_desperate% now.", "That's actually starting to affect me."],
            "shy":      ["O-oh... that's really getting to me...", "I... I really like hearing that...", "Th-that's really working on me...", "Oh... I'm feeling a little %adj_desperate% now...", "I... that's really doing something to me..."],
            "demure":   ["That is quite affecting, truthfully.", "You are being rather charming right now.", "That was genuinely quite lovely to hear.", "I confess I am feeling rather %adj_desperate% now.", "You are, I confess, having quite an effect on me."],
        },
        "great": {
            "crude":    ["Fuck, say that again, I'm %adj_desperate% right now.", "God, keep going, I'm soaked.", "Fuck, keep talking, don't stop.", "Christ, I want you right now. I'm %adj_desperate%.", "Fuck, keep talking, I'm soaked."],
            "explicit": ["Mmm, you have no idea what that's doing to me right now.", "Keep talking like that, I'm so %adj_desperate%.", "God, say that again.", "Mmm, I'm %adj_desperate% right now. I want to feel you.", "God, my %noun_pussy% is throbbing, keep going."],
            "direct":   ["Okay, that's really getting to me.", "Keep that up and see what happens to me.", "Okay, wow, that really got me.", "Okay, I'm really %adj_desperate% right now.", "Keep going, I'm getting really turned on."],
            "neutral":  ["That's really getting to me, in a good way.", "Okay, wow, that's really working.", "That really got to me, honestly.", "I'm feeling really %adj_desperate% right now, honestly.", "Okay, that's really affecting me a lot."],
            "shy":      ["O-oh my... I'm so %adj_desperate% right now...", "That's... really affecting me a lot...", "I-I don't know what to say, that really got me...", "I... I'm so %adj_desperate%, I don't know what to do...", "Oh my... I think I really need you right now..."],
            "demure":   ["You are being entirely too charming for my own good.", "I confess that is having quite an effect on me.", "You are far too skilled with words for my own good.", "I am entirely too %adj_desperate% for propriety right now.", "You have rendered me quite %adj_desperate%, I confess."],
        },
    }

    # Drunk/tipsy overrides per tier (2026-09-27, per direct user instruction) -- FLAT, not
    # register-keyed, same convention as every other drunk/tipsy override in this file
    # (VT_BAR_BOOTH_COMPLIMENT_REACT_DRUNK/TIPSY, VT_BAR_BOOTH_HARD_REJECT_DRUNK/TIPSY, etc.):
    # intoxication overrides her filter regardless of her corruption-trait register. Drunk = dropped
    # g's + "*hic*" + cruder phrasing; tipsy = the same content, sober spelling, still looser than a
    # fully sober reaction -- same drunk-vs-tipsy differentiation this file already uses everywhere.
    VT_BAR_BOOTH_FLIRT_REACT_DRUNK_BY_TIER = {
        "miss": ["Ugh, *hic* nah, that ain't doin' nothin' for me.", "Try again, that was weak as hell.", "Pfft, that did nothin', try harder."],
        "ok":   ["Heh, *hic* okay, I'll give you that one.", "Not bad, keep goin'.", "Eh, that's somethin' at least."],
        "good": ["Fuck, *hic* okay, keep talkin' like that.", "Mmh, that's actually gettin' to me.", "Heh, keep goin', I'm likin' this."],
        "great": ["Fuck, *hic* say that again, I'm so fuckin' desperate right now.", "God, keep goin', don't you dare stop.", "Mmh, fuck, I'm soaked, keep talkin'."],
    }
    VT_BAR_BOOTH_FLIRT_REACT_TIPSY_BY_TIER = {
        "miss": ["Ugh, nah, that's not doing anything for me.", "Try again, that was pretty weak.", "Pfft, that did nothing, try harder."],
        "ok":   ["Heh, okay, I'll give you that one.", "Not bad, keep going.", "Eh, that's something at least."],
        "good": ["Fuck, okay, keep talking like that.", "Mmh, that's actually getting to me.", "Heh, keep going, I'm liking this."],
        "great": ["Fuck, say that again, I'm so desperate right now.", "God, keep going, don't you dare stop.", "Mmh, I'm soaked, keep talking."],
    }

    # Critical-fail reject line -- same register-keyed shape as VT_BAR_BOOTH_HARD_REJECT, deliberately
    # kept as its own pool (not shared with hard_reject) since the *reason* she's leaving is
    # different (a flirt line landed badly, not a sexual ask).
    VT_BAR_BOOTH_FLIRT_CRITFAIL_REJECT = {
        "crude":    ["Ugh, gross, don't talk to me like that.", "What the fuck? No. I'm done.", "Ugh, that's disgusting. I'm out."],
        "explicit": ["Ew, that's not okay. I'm leaving.", "That was disgusting, I'm done here.", "Ew, no. I'm leaving right now."],
        "direct":   ["That was way out of line. I'm done.", "No. That's not okay at all.", "That crossed a line. I'm done."],
        "neutral":  ["That was really uncomfortable. I need to go.", "I don't think this is working out.", "That made me really uncomfortable. I'm leaving."],
        "shy":      ["Th-that really scared me... I need to go...", "I... I don't like this at all... I have to leave...", "Th-that wasn't okay... I need to go now..."],
        "demure":   ["That was entirely inappropriate. I am leaving.", "I find that deeply unwelcome. Excuse me.", "That was wholly improper. I must go."],
    }
    VT_BAR_BOOTH_FLIRT_CRITFAIL_REJECT_DRUNK = [
        "Are you fuckin' serious? *hic* I'm done!",
        "Ugh, no. I'm outta here!",
        "That's fuckin' gross, I'm leavin'!",
    ]
    VT_BAR_BOOTH_FLIRT_CRITFAIL_REJECT_TIPSY = [
        "Are you serious? I'm done!",
        "Ugh, no. I'm out of here!",
        "That's gross, I'm leaving!",
    ]
    VT_BAR_BOOTH_FLIRT_CRITFAIL_ACTION_LINES = [
        "She recoils, takes a breath to steady herself, and grabs her things. Sliding out of the booth, she leaves the bar without looking back.",
        "She stiffens, gathers her things, and moves out of the booth. She heads out of the bar, done with the conversation entirely.",
        "Her expression sours completely. She collects herself, gathers her things, and leaves the bar without another word.",
    ]

    VT_BAR_BOOTH_HANDHOLD_ACCEPT = {
        "crude":    ["Getting handsy already, huh?", "Ha, cute. I'll allow it.", "Ha, look at you, all sweet on me."],
        "explicit": ["Mmm, I like that.", "I don't mind that at all.", "Mmm, I could get used to this."],
        "direct":   ["That's nice, actually.", "I don't mind this.", "That's actually pretty nice."],
        "neutral":  ["That's nice.", "I like that.", "That's sweet, actually."],
        "shy":      ["Th-that's... nice...", "O-oh... okay...", "Th-that's kind of nice, actually..."],
        "demure":   ["That is rather sweet.", "I don't mind this at all.", "That is quite a sweet gesture."],
    }

    VT_BAR_BOOTH_HANDHOLD_REJECT = {
        "crude":    ["Not that comfortable yet, slow down.", "Easy there, not yet.", "Hold up, not there yet."],
        "explicit": ["Mmh, not yet... let's slow down a bit.", "I'm not quite there yet, sorry.", "Mmh, give me a little more time first."],
        "direct":   ["I'm not ready for that yet.", "Let's slow down a little.", "I'd rather wait a bit on that."],
        "neutral":  ["I'm not sure about that yet.", "Let's take it slow, okay?", "Let's not rush into that yet."],
        "shy":      ["I-I'm not ready for that yet...", "C-can we slow down a little...?", "I-I need a bit more time first..."],
        "demure":   ["I am not yet comfortable with that.", "Let us proceed a bit more slowly, please.", "I would prefer we take our time."],
    }

    VT_BAR_BOOTH_THIGH_REACT = {
        "crude":    ["Mmh, someone's bold tonight.", "Getting handsy under here already?", "Ha, someone's feeling brave tonight."],
        "explicit": ["Mmm... careful, someone might notice.", "Ah -- keep that up and I won't be able to sit still.", "Mmm, you're playing with fire here."],
        "direct":   ["Someone might notice, you know.", "You're being pretty bold right now.", "You're being pretty daring right now."],
        "neutral":  ["Careful, someone might see.", "You're being pretty forward.", "You're being pretty bold."],
        "shy":      ["W-wait, someone might see us...!", "Um -- s-someone could notice...", "O-oh! Someone could walk by...!"],
        "demure":   ["You are being quite forward, aren't you.", "Someone may well notice, you realize.", "You are being rather bold, aren't you."],
    }

    VT_BAR_BOOTH_THIGH_REJECT = {
        "crude":    ["Not there, not yet.", "Whoa, slow down.", "Nuh-uh, not yet."],
        "explicit": ["Mmh, not yet... slow down.", "Wait, not there, not yet.", "Mmh, hold on -- not there yet."],
        "direct":   ["Not yet, let's slow down.", "Not there, please.", "Not there yet, if you don't mind."],
        "neutral":  ["Not yet, let's slow down.", "Please, not there yet.", "Let's not go there just yet."],
        "shy":      ["N-not yet, please...", "W-wait, not there...", "P-please, not there yet..."],
        "demure":   ["Not yet, if you please.", "I am not ready for that yet.", "I must ask you to wait on that."],
    }

    VT_BAR_BOOTH_GROPE_ACCEPT = {
        "crude":    ["Mmh, fuck it, go ahead.", "Ha, bold. Fine, keep going.", "Go ahead, touch my %noun_pussy%."],
        "explicit": ["Mmm... okay, don't stop.", "Ohh -- fine, keep going.", "Mmm, go ahead, touch my %noun_pussy%."],
        "direct":   ["Okay... go ahead.", "Alright, that's fine.", "Alright, touch my %noun_pussy% then."],
        "neutral":  ["Okay... that's fine.", "Alright, go ahead.", "Alright, you can touch my %noun_pussy%."],
        "shy":      ["O-okay... that's... fine...", "Um... okay, go ahead...", "Um... you can... touch me there..."],
        "demure":   ["Very well, you may continue.", "That is... acceptable, go on.", "Very well, you may touch me there."],
    }

    VT_BAR_BOOTH_GROPE_REJECT = {
        "crude":    ["Whoa, not here. Slow down.", "Easy, not that far.", "Hold up, not that far, not here."],
        "explicit": ["Mmh, not yet -- that's too far here.", "Wait, not that, not here.", "Mmh, not that far, not here."],
        "direct":   ["Not here, that's too far.", "Let's not go that far right now.", "Not that far, not here."],
        "neutral":  ["Not here, that's too much.", "Let's not go that far.", "That's too much, not here."],
        "shy":      ["W-wait, that's too far...", "N-not here, please...", "P-please, not that far..."],
        "demure":   ["That is too forward, not here.", "I must ask you not to go that far.", "That is too much, not here."],
    }

    VT_BAR_BOOTH_FINGER_ACCEPT = {
        "crude":    ["Fuck, fine -- touch me then.", "Mmh, go on then, touch it.", "Fuck, go on, touch my %noun_pussy%."],
        "explicit": ["Mmm... okay, go ahead, touch me.", "Ohh -- yes, go on.", "Mmm, go ahead, touch my %noun_pussy%."],
        "direct":   ["Okay... go ahead.", "Alright, you can touch me.", "Alright, go ahead and touch my %noun_pussy%."],
        "neutral":  ["Okay... that's fine.", "Alright, go ahead.", "Alright, you can touch my %noun_pussy%."],
        "shy":      ["O-okay... you can... touch me...", "Um... alright, go ahead...", "Um... okay, you can... touch me there..."],
        "demure":   ["Very well, you may touch me there.", "That is... acceptable, go on.", "Very well, you may touch me there directly."],
    }

    VT_BAR_BOOTH_FINGER_REJECT = {
        "crude":    ["Whoa, hold up -- not that far.", "Easy, that's too much here.", "Hold up, that's too much right now."],
        "explicit": ["Mmh, not that -- not here.", "Wait, that's too far here.", "Mmh, not that far, not right now."],
        "direct":   ["Not here, that's too far.", "Let's not go that far right now.", "That's too far, not right now."],
        "neutral":  ["Not here, that's too much.", "Let's not go that far.", "That's too much, not right now."],
        "shy":      ["W-wait, that's too far...", "N-not here, please...", "P-please, not that far right now..."],
        "demure":   ["That is too forward, not here.", "I must ask you not to go that far.", "That is too much, not right now."],
    }

    VT_BAR_BOOTH_TOUCH_ACCEPT = {
        "crude":    ["Fuck, yes -- don't stop.", "Mmh, fuck, right there.", "Fuck, keep touching me just like that."],
        "explicit": ["Mmm, yes... just like that.", "Ohh... don't stop, please.", "Mmm, don't stop touching my %noun_pussy%."],
        "direct":   ["Okay... don't stop.", "Yes, keep going.", "Don't stop, that's really good."],
        "neutral":  ["Okay... keep going.", "That's... good, don't stop.", "Don't stop, that feels really good."],
        "shy":      ["O-oh... don't stop...", "Um... th-that feels... good...", "O-oh, please... don't stop..."],
        "demure":   ["Please... do continue.", "That is... quite alright, don't stop.", "Please, do not stop now."],
    }

    VT_BAR_BOOTH_GIRL_ORGASM = {
        "crude":    ["Oh fuck, I'm cumming!", "Fuck, fuck, I'm cumming!", "Fuck, right there, I'm cumming!"],
        "explicit": ["Ohh god, yes... I'm coming...", "Mmm, yes, I'm coming...", "Ohh, yes, right there, I'm coming..."],
        "direct":   ["Oh -- I'm coming.", "Yes... I'm coming.", "Oh god, I'm coming."],
        "neutral":  ["Oh -- I'm coming!", "I'm coming, don't stop!", "Oh -- I'm coming, right there!"],
        "shy":      ["O-oh! I'm... I'm coming...!", "I-I'm coming...!", "O-oh! I'm gonna... I'm coming...!"],
        "demure":   ["Oh! I am... I am finishing...!", "Oh my -- I am coming...!", "Oh! I am about to finish...!"],
    }

    VT_BAR_BOOTH_OVERSTIM_STOP = {
        "crude":    ["Fuck, stop -- that's too much, I can't take any more.", "Enough! Stop, I mean it, I can't take it.", "Fuck, I said stop, I'm done."],
        "explicit": ["Mmh, stop -- please, I can't take any more like this.", "Wait, stop... it's too much, I need a moment.", "Mmh, please, I really need to stop now."],
        "direct":   ["Stop, please -- that's too much right now.", "Please stop, I can't take any more of that.", "Stop, please, I really need a break."],
        "neutral":  ["Please stop, that's too much.", "Stop, please -- I need a moment.", "Please stop, I need a break."],
        "shy":      ["P-please stop... it's too much...", "I-I can't take any more, please stop...", "P-please, I really need to stop..."],
        "demure":   ["Please, you must stop -- it is too much.", "I must ask you to stop, it is too much.", "Please, I must ask you to stop now."],
    }

    # Act-keyed (three acts now: handjob/blowjob/fuck_pussy -- same shared shape and
    # push/respect negotiation for all three, just a third cell in every act-keyed dict).

    VT_BAR_BOOTH_SEX_ASK = {
        "handjob": {
            "dominant": [
                "It's dark enough back here. Get me off, right here, right now.",
                "You know what I want. Get your hand on me, under the table.",
                "I want your hand on me. Now, under the table.",
            ],
            "compassionate": [
                "It's pretty dark back here. Would you take care of me a little, under the table?",
                "I'd really love it if you helped me out under here, if you're comfortable with that.",
                "This booth's private enough -- would you mind giving me a hand, just between us?",
            ],
            "sexual": [
                "God, I want your hand on me right now. It's dark enough back here -- come on.",
                "I can't stop thinking about your hand on me. Get me off under here.",
                "This booth's private enough -- why don't you get that hand working under the table.",
            ],
            "transactional": [
                "This booth's private enough -- help me out under the table, and I'll make it worth your while later.",
                "How about a little discreet fun under the table? I'll owe you one.",
                "It's pretty dark back here. Take care of me and I'll return the favor.",
            ],
            "neutral": [
                "It's pretty dark back here. How about a little... discreet fun under the table?",
                "This booth's private enough -- why don't you give me a hand under here?",
                "It's dark enough back here -- how about you give me a hand under the table?",
            ],
        },
        "blowjob": {
            "dominant": [
                "Get under this table and put that mouth to work. Now.",
                "You know what to do. Get down there and take care of me.",
                "I want your mouth on me. Get under there.",
            ],
            "compassionate": [
                "It's dark enough back here. Would you want to take care of me down there, if you're up for it?",
                "I'd love it if you slipped under and helped me out, only if you want to.",
                "No one can see under this table -- would you mind putting that mouth to use for me?",
            ],
            "sexual": [
                "God, I want your mouth on me right now. It's dark enough back here -- come on.",
                "I can't stop thinking about your mouth. Slip under and make it even better.",
                "No one can see under this table -- why don't you get down there and taste me.",
            ],
            "transactional": [
                "It's dark enough back here. Slip under and take care of me, and I'll make it worth it.",
                "No one can see under this table -- put that mouth to use, and I'll owe you one.",
                "How about you slip under and make it even better? I'll return the favor.",
            ],
            "neutral": [
                "It's dark enough back here. How about you slip under and make it even better?",
                "No one can see under this table -- why don't you get down there and put that mouth to use?",
                "It's dark enough over here -- why don't you slip under and take care of me?",
            ],
        },
        "fuck_pussy": {
            "dominant": [
                "Get on my lap. Now. I want to feel you ride me.",
                "You know what I want. Climb on and ride me.",
                "Get on top of me. Now, right here.",
            ],
            "compassionate": [
                "This booth's dark enough, and no one's looking over here. Would you want to climb on and ride me?",
                "I'd really love it if you got on my lap, if you're comfortable with that here.",
                "Nobody can see under this table -- would you want to be that close to me right now?",
            ],
            "sexual": [
                "God, I want to feel you riding me right now. This booth's dark enough -- come on.",
                "I can't stop thinking about you on top of me. Climb on and ride me.",
                "Nobody can see under this table -- why don't you get on my lap and ride me.",
            ],
            "transactional": [
                "This booth's dark enough, and no one's looking. Ride me, and I'll make it worth it.",
                "Nobody can see under this table -- climb on, and I'll owe you one.",
                "Get on my lap and ride me a little. I'll return the favor.",
            ],
            "neutral": [
                "This booth's dark enough, and no one's looking over here. Why don't you climb on and ride me?",
                "Nobody can see under this table -- why don't you get on my lap and ride me?",
                "It's dark enough back here -- why don't you climb on and ride me?",
            ],
        },
    }

    # Third variant on the handjob/blowjob cells weaves in %noun_penis% (same reasoning as the coffee
    # shop file's own version); fuck_pussy's third variant weaves in %verb_have_sex% instead, since
    # that's literally what she's agreeing to here.
    VT_BAR_BOOTH_SEX_ACCEPT = {
        "handjob": {
            "crude":    ["Oh, you're bold. Alright, let's see what I can do.", "Fuck it, get over here and let me feel that.", "Fuck it, get that %noun_penis% out then."],
            "explicit": ["Mmm, alright... hold still.", "Ohh, okay... let me take care of you.", "Mmm, let me feel that %noun_penis% in my hand."],
            "direct":   ["Alright, I can do that.", "Okay, I'll take care of that.", "Alright, let me take care of that %noun_penis%."],
            "neutral":  ["Okay, I can do that.", "Alright, I'll help you out.", "Okay, let me take care of that %noun_penis%."],
            "shy":      ["O-okay... I'll try...", "Um... alright, I guess...", "Um... okay, I'll take care of your %noun_penis%..."],
            "demure":   ["Very well, I shall attend to that.", "If you insist, I will help.", "Very well, I shall attend to your %noun_penis%."],
        },
        "blowjob": {
            "crude":    ["Risky, but I'm game. Hold onto your drink.", "Fuck it, get that %noun_penis% out then.", "Fuck it, whip that %noun_penis% out already."],
            "explicit": ["Mmm, alright... hold still for me.", "Ohh, okay... let me taste you.", "Mmm, let me put my mouth on that %noun_penis%."],
            "direct":   ["Alright, I can do that.", "Okay, I'll take care of you.", "Alright, let me take care of that %noun_penis%."],
            "neutral":  ["Okay, I can do that.", "Alright, I'll take care of it.", "Okay, let me take care of that %noun_penis%."],
            "shy":      ["O-okay... I'll try my best...", "Um... alright, I guess I can...", "Um... I'll take care of your %noun_penis%..."],
            "demure":   ["Very well, I shall attend to you.", "If you insist, I will oblige.", "Very well, I shall attend to your %noun_penis%."],
        },
        "fuck_pussy": {
            "crude":    ["Fuck it, why not. Get ready.", "Mmh, bold. Fine -- give me a second.", "Fuck it, let's %verb_have_sex% then."],
            "explicit": ["Mmm, alright... give me a second.", "Ohh, yes... okay, come here.", "Mmm, let's %verb_have_sex% then, come here."],
            "direct":   ["Alright, okay. Just be quick about it.", "Okay, fine -- come here.", "Alright, let's %verb_have_sex% then."],
            "neutral":  ["Okay, alright. Just be quick.", "Alright, fine, come here.", "Okay, let's %verb_have_sex%."],
            "shy":      ["O-okay... um, o-okay...", "Um... alright, I guess...", "Um... o-okay, let's %verb_have_sex%..."],
            "demure":   ["Very well, if you insist.", "If you truly wish it, then yes.", "Very well, let us %verb_have_sex%."],
        },
    }

    VT_BAR_BOOTH_SEX_INTERJECT = {
        "crude":    ["Whoa, hold up -- right here? Someone could see.", "Careful, someone's gonna notice.", "Whoa, hang on -- right here, seriously?"],
        "explicit": ["Ah -- wait, right here? Someone might see us...", "Mmh, hold on -- this is risky.", "Ah, wait -- right here, of all places?"],
        "direct":   ["Wait -- right here? Someone might notice.", "Hold on, that's pretty risky here.", "Wait -- are you sure, right here?"],
        "neutral":  ["Wait, here? Someone might see us.", "Hold on, isn't that risky here?", "Wait, right here? That seems risky."],
        "shy":      ["W-wait, here...? Someone might see...", "Um, s-someone could notice...", "W-wait, right here...? Are you sure...?"],
        "demure":   ["Wait -- here? Someone may well notice.", "That seems rather risky, here of all places.", "Wait -- are you certain, here of all places?"],
    }

    # Menu captions -- flagged as the hardest cell to write a genuinely non-redundant 3rd variant for
    # (same reasoning as the coffee shop file's own version; follows the same 03_vt_pullout_coercion.rpy
    # template).
    VT_BAR_BOOTH_MENU_PUSH_CAPTION = {
        "crude":    ["Push her -- no one will notice", "Talk her into it anyway", "Push her, she'll get over it"],
        "explicit": ["Convince her to go for it", "Push a little", "Try to talk her into it"],
        "direct":   ["Push her to go along with it", "Try to convince her", "Ask her again anyway"],
        "neutral":  ["Push her a little", "Try to convince her", "Ask her again"],
        "shy":      ["Gently push her", "Try to convince her", "Softly ask again"],
        "demure":   ["Press the matter", "Try to persuade her", "Politely ask again"],
    }

    VT_BAR_BOOTH_MENU_RESPECT_CAPTION = {
        "crude":    ["Fine, drop it", "Let it go", "Nah, forget it"],
        "explicit": ["Respect her -- let it go", "Back off", "Let it drop"],
        "direct":   ["Respect her wishes", "Let it go", "Drop it for now"],
        "neutral":  ["Respect her wishes", "Let it go", "Leave it be"],
        "shy":      ["Respect her wishes", "Let it go", "Gently let it go"],
        "demure":   ["Respect her wishes", "Let the matter go", "Graciously let it go"],
    }

    VT_BAR_BOOTH_PUSH_SUCCESS = {
        "crude":    ["Ugh, fine -- but you owe me.", "Fuck it, fine. Let's be quick about it.", "Ugh, fine, just don't drag it out."],
        "explicit": ["Mmh... okay, fine. Just be quick.", "Alright... fine, just this once.", "Mmh, alright, but hurry."],
        "direct":   ["Fine, but let's be quick.", "Alright, fine -- just this once.", "Fine, but let's not linger on it."],
        "neutral":  ["Okay, fine. Just be quick.", "Alright, just this once.", "Okay, fine -- but quickly."],
        "shy":      ["O-okay... just be quick, please...", "F-fine... just this once...", "O-okay... let's hurry, please..."],
        "demure":   ["Very well, but let us be quick.", "Fine -- but only this once.", "Very well, but let us not delay."],
    }

    VT_BAR_BOOTH_PUSH_FAIL = {
        "crude":    ["No! I said not here, drop it. I'm leaving.", "Are you deaf? I said no. I'm leaving.", "No means no, drop it already. I'm leaving."],
        "explicit": ["No -- I mean it, not here. I'm leaving.", "I said no, please stop pushing. I'm leaving.", "No -- I really do mean it. I'm leaving."],
        "direct":   ["No, I meant it -- not here. I'm leaving.", "I said no. Please respect that. I'm leaving.", "No, and I need you to hear that. I'm leaving."],
        "neutral":  ["No, I meant it. Not here. I'm leaving.", "I said no, please stop. I'm leaving.", "No, I really do mean that. I'm leaving."],
        "shy":      ["N-no... I said no... please stop... I need to leave...", "P-please, I meant it, not here... I need to go...", "N-no, please... I mean it... I'm leaving..."],
        "demure":   ["No. I meant what I said. I am leaving.", "I must insist -- the answer is no. I am leaving.", "No. I must ask you to respect that. I am leaving."],
    }

    VT_BAR_BOOTH_RESPECT = {
        "crude":    ["Thanks for backing off.", "Appreciate you not pushing it.", "Good, glad you dropped it."],
        "explicit": ["Thank you for respecting that.", "Thanks for not pushing.", "Thank you, that means something to me."],
        "direct":   ["Thank you for respecting that.", "I appreciate you backing off.", "Thank you for hearing me on that."],
        "neutral":  ["Thank you for understanding.", "Thanks for respecting that.", "Thank you for listening to me."],
        "shy":      ["Th-thank you... for not pushing...", "I... appreciate that, thank you...", "Th-thank you, for understanding..."],
        "demure":   ["Thank you for your consideration.", "I appreciate your restraint.", "Thank you for honoring my wishes."],
    }

    VT_BAR_BOOTH_HARD_REJECT = {
        "crude":    ["Are you insane? That's disgusting. I'm out of here!", "You're fucking revolting! I'm gone!", "What the fuck is wrong with you? I'm leaving!"],
        "explicit": ["Are you serious? I'm leaving!", "You're unbelievable. I'm out of here!", "I can't believe you just said that. I'm gone!"],
        "direct":   ["That's out of line. I'm leaving.", "Absolutely not. I'm done here.", "That crossed a line. I'm leaving."],
        "neutral":  ["That's way too much. I'm leaving.", "No way. I'm done here.", "That's too far. I'm leaving."],
        "shy":      ["Th-that upset me... I need to leave...!", "Th-that's too much, I'm leaving...!", "I-I can't believe you said that...!"],
        "demure":   ["That is entirely inappropriate. I am leaving.", "I will not tolerate that. Goodbye.", "That is quite unacceptable. I am leaving."],
    }

    # Sex-gate action narration, act-keyed (three acts). IMMEDIATE/FINISH/HELDBACK cover the >=40
    # immediate-accept path; the _PUSH variants cover the push-success path and read more reluctant.
    VT_BAR_BOOTH_SEX_ACTION_IMMEDIATE = {
        "handjob": [
            "She glances around, then slips her hand beneath the table, her fingers brushing your thigh before finding their target. The booth hides her movements as she works you with a steady, teasing grip.",
            "She checks that no one's watching, then slides her hand under the table and along your leg until she finds you, working you with a slow, deliberate grip.",
        ],
        "blowjob": [
            "She winks, then ducks under the table with surprising grace. You feel her hands on your knees, then the warm press of her mouth as she gets to work, hidden beneath the table.",
            "She flashes a grin, then slips out of her seat and under the table. You feel her hands part your knees, then the warm heat of her mouth closing around you, hidden beneath the table.",
        ],
        "fuck_pussy": [
            "She glances around, then climbs into your lap. You both adjust your clothes for access as she straddles you in the dim booth.",
            "She checks that no one's paying attention, then swings a leg over and settles into your lap. You both move any remaining clothing out of the way.",
        ],
    }

    VT_BAR_BOOTH_SEX_FINISH_LINES = {
        "handjob": [
            "After you finish, she draws her hand away and settles back into her seat.",
            "You catch your breath after your release while she withdraws her hand.",
        ],
        "blowjob": [
            "After you finish, she comes out from beneath the table and settles into her seat.",
            "As your breathing steadies, she returns to her seat and smooths the front of her outfit.",
        ],
        "fuck_pussy": [
            "As you catch your breath after finishing, she eases off your lap and straightens her clothes.",
            "You sit back after your release as she moves into her own seat, adjusting her clothes.",
        ],
    }

    VT_BAR_BOOTH_SEX_HELDBACK_LINES = {
        "handjob": [
            "You stop before finishing and let go of her wrist. She draws her hand away.",
            "You still her hand before you finish. She settles back into her seat.",
        ],
        "blowjob": [
            "You stop before finishing. She comes out from beneath the table and returns to her seat.",
            "You ease back before you finish, giving her room to return to her seat.",
        ],
        "fuck_pussy": [
            "You stop before finishing and let her move off your lap. She settles beside you and adjusts her clothes.",
            "You steady her hips, stopping before you finish. She eases off your lap and settles into her own seat.",
        ],
    }

    VT_BAR_BOOTH_SEX_ACTION_PUSH = {
        "handjob": [
            "She glances around one more time, then reluctantly slips her hand beneath the table.",
            "She takes one more look around, then reluctantly lets her hand drift under the table.",
        ],
        "blowjob": [
            "She hesitates, then ducks under the table, clearly less enthusiastic than a moment ago.",
            "She hesitates a beat longer, then slips under the table with far less enthusiasm than before.",
        ],
        "fuck_pussy": [
            "She hesitates, then climbs into your lap anyway. You both adjust your clothes for access, though she is clearly less enthusiastic than a moment ago.",
            "She takes one more look around, then reluctantly swings a leg over and settles into your lap. You both adjust your clothes for access.",
        ],
    }

    VT_BAR_BOOTH_SEX_FINISH_PUSH_LINES = {
        "handjob": [
            "After you finish, she draws her hand away in silence.",
            "You catch your breath after your release while she settles back into her seat.",
        ],
        "blowjob": [
            "After you finish, she comes out from beneath the table and sits back in silence.",
            "You catch your breath after your release as she returns to her seat.",
        ],
        "fuck_pussy": [
            "After your release, she moves off your lap and straightens her clothes in silence.",
            "You catch your breath after finishing while she eases into her own seat and adjusts her clothes.",
        ],
    }

    VT_BAR_BOOTH_SEX_HELDBACK_PUSH_LINES = {
        "handjob": [
            "You stop before finishing. She withdraws her hand, visibly relieved to have a break.",
            "You still her hand before you finish and let her settle back into her seat.",
        ],
        "blowjob": [
            "You stop before finishing. She returns to her seat, visibly relieved to have a break.",
            "You ease back before you finish, giving her room to come out from beneath the table.",
        ],
        "fuck_pussy": [
            "You stop before finishing. She moves off your lap, visibly relieved to have a break, and adjusts her clothes.",
            "You steady her hips and stop before you finish. She eases into her own seat and straightens her clothes.",
        ],
    }

    # Overstim narration for the sex-gate acts (handjob/blowjob/fuck_pussy) -- her pressure capped
    # without release. VT_BAR_BOOTH_OVERSTIM_ACTION_LINES (above) is written for the grope/finger touch
    # loop specifically (his hand on/in her); it doesn't fit any of these three -- handjob has her hand
    # on him, blowjob her mouth, and fuck_pussy has her riding him (cowgirl/reverse-cowgirl, per this
    # act's own established positioning throughout VT_BAR_BOOTH_SEX_ACTION_IMMEDIATE etc.) -- so this is
    # a separate, act-keyed pool instead of reusing that one.
    VT_BAR_BOOTH_SEX_OVERSTIM_ACTION_LINES = {
        "handjob": [
            "She pulls her hand back and sits up straighter, chest heaving.",
            "She stills her hand around you and leans back, breathing hard.",
        ],
        "blowjob": [
            "She pulls back and sits up, chest heaving.",
            "She comes up for air and leans back, breathing hard.",
        ],
        "fuck_pussy": [
            "She sits stiffly beside you, chest heaving, and holds up a hand to stop any further contact.",
            "She leans away in her seat, breathing hard, and makes it clear she needs a break.",
        ],
    }

    # Her closing narration if she balks specifically because the player has no condom on and won't
    # concede -- the negotiation itself (vt_gobare_beat) already voices her refusal, this is just the
    # physical wrap-up beat that follows.
    VT_BAR_BOOTH_VAGINAL_CONDOM_DECLINE_ACTION_LINES = [
        "She stays in her seat, keeping her clothes in place. She won't go further without a condom.",
        "She shakes her head and keeps her distance. That's a hard line for her: a condom or nothing.",
    ]

    def vt_bar_booth_first_time_voice(girl, lines, orgasm=False):
        """Reuse first-time tone/register pools without inventing a long-standing wish.
        The shared orgasm addendum precedes his finish choice's dispatch; 'too/as well'
        would claim a second climax even when he held back. Keep the shared tables intact."""
        line = vt_booth_voice(girl, lines, "...")
        replacements = (
            (" I've wanted this for a while...", " I want this..."),
            (" -- I've wanted that for a while, actually.", "."),
            (" -- I've wanted that for a while.", "."),
            (" -- I've hoped for that for a while.", "."),
            (" -- I've wanted this for a while.", "."),
            (" -- I have hoped for this for some time.", "."),
            (" -- truly, I have longed for this.", "."),
            (" -- I have hoped for this.", "."),
            (" I've wanted this for a while.", ""),
            (" I've felt that way for a while.", ""),
            (" That's been true for a while now.", ""),
            (" I have hoped for this for quite some time.", ""),
            ("I've hoped it would be you for a while now", "I'm glad it's you"),
            ("I've wanted it to be you for a while now", "I'm glad it's you"),
            ("I have long hoped it would be you", "I am glad it is you"),
            ("I've wanted this for so long", "I want this"),
            ("I've wanted this forever", "I want this"),
            ("I've been waiting for this way too long", "I want this"),
            ("I've wanted this for way too long", "I want this"),
            ("I've wanted this so bad", "I want this"),
            ("I've been wanting this", "I want this"),
            ("I've wanted this for a while", "I want this"),
            ("I've been wanting this for a while now", "I want this"),
            ("I've honestly been hoping for this", "I honestly want this"),
            ("I have wanted this for some time now", "I want this"),
            ("I have longed for this", "I want this"),
            ("I have anticipated this for quite some time", "I want this"),
            ("Can't believe I waited this long.", ""),
            ("I can't believe I waited this long for that.", ""),
            ("I can't believe I waited.", ""),
            (" -- I don't know why I waited so long.", "."),
            ("I don't know why I waited this long.", ""),
            ("and I can't believe I waited this long to feel that", "and I'm still taking it in"),
            ("I can't believe I waited this long to feel that", "I'm still taking it in"),
            ("can't believe I waited this long to feel that", "I'm still taking it in"),
            ("I confess I have no notion why I waited so long for it", "I am still taking it in"),
            ("and it was so worth the wait", "and I'm still taking it in"),
            (" Worth the wait.", ""),
            ("I wanted it to be you, you know that?", "I'm glad it was you."),
        )
        # Prefer the complete clause over a shorter prefix (including ellipsis variants).
        for old, new in sorted(replacements, key=lambda pair: len(pair[0]), reverse=True):
            line = line.replace(old, new)
        if orgasm:
            line = line.replace(" too", "").replace(" as well", "")
        return line.strip()


label vt_bar_booth:
    $ time_manager.skip_time(minutes=10)

    $ _vt_bb_invite = vt_booth_choice(selected_girl, VT_BAR_BOOTH_INVITE_LINES)
    player.character "[_vt_bb_invite]"

    $ additional_subtags = ["bar", "undertable"]
    $ girl_acceptance = selected_girl.get_acceptance_by_name("free_use_compliance")
    $ vt_log_acceptance_breakdown(selected_girl, "free_use_compliance", player)
    $ vt_log_check("bar booth entry (sit down)", girl_acceptance, VT_BAR_BOOTH_ENTRY_ACCEPTANCE_THRESHOLD, girl_acceptance >= VT_BAR_BOOTH_ENTRY_ACCEPTANCE_THRESHOLD)

    if girl_acceptance >= VT_BAR_BOOTH_ENTRY_ACCEPTANCE_THRESHOLD:
        $ _vt_bb_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_ACCEPT, "Sure, that sounds nice. Let's sit.")
        selected_girl.character "[_vt_bb_line]"

        # .replace() here because these pool strings are plain Python literals chosen into a
        # variable -- Ren'Py's "[...]" substitution is single-pass, so a "[selected_girl]" token
        # embedded in the CHOSEN string never gets a second interpolation pass once it's displayed
        # through the outer "[_vt_bb_seat_down_line]" tag; it would otherwise show up onscreen
        # literally as the text "[selected_girl]" instead of her name.
        $ _vt_bb_seat_down_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEAT_DOWN_ACTION_LINES).replace("[selected_girl]", str(selected_girl))
        "[_vt_bb_seat_down_line]"

        # Has_trait("drunk")/has_trait("tipsy") narration touch -- shown alongside the normal seat-down
        # line, mirroring label_bar_discussions.rpy's own established convention for this. The real
        # acceptance bonus these traits grant (class_personality_ren.py:282) already applies to every
        # roll below automatically -- this is purely the narration half.
        if selected_girl.has_trait("drunk"):
            $ _vt_bb_trait_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_DRUNK_SEAT_LINES)
            "[_vt_bb_trait_line]"
        elif selected_girl.has_trait("tipsy"):
            $ _vt_bb_trait_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_TIPSY_SEAT_LINES)
            "[_vt_bb_trait_line]"

        $ selected_girl.apply_impacts({"affection": 1000})

        # Deliberate, narrow reset to her own resting baseline -- matches the coffee shop file's own
        # reasoning (NOT Girl.reset_for_sex(), which also spikes tolerance and touches
        # sex-interaction-only bookkeeping that doesn't belong in this standalone scene).
        $ vt_log(f"arousal/pressure reset: was arousal={selected_girl.arousal} pressure={selected_girl.pressure}")
        $ selected_girl.arousal = selected_girl.base_arousal
        $ selected_girl.pressure = selected_girl.base_pressure
        $ vt_log_girl_snapshot(selected_girl, player)

        # --- Seating ---
        $ _vt_bar_booth_stage_chance = {}
        python:
            _booth_closeness = vt_booth_stage_chance(selected_girl, "seating", VT_BAR_BOOTH_STAGE_ORDER,
                                                      VT_BAR_BOOTH_LOCAL_TIER_FLOORS, VT_BAR_BOOTH_STAGE_BANDS,
                                                      _vt_bar_booth_stage_chance)
            _vt_bar_booth_stage_chance["seating"] = _booth_closeness
        $ _booth_same_side = False
        python:
            _seat_spontaneous_roll = renpy.random.randint(1, 100)
            _seat_spontaneous_success = _seat_spontaneous_roll <= _booth_closeness
            vt_log_roll("bar spontaneous seating", _seat_spontaneous_roll, _booth_closeness, _seat_spontaneous_success)
        if _seat_spontaneous_success:
            $ _booth_same_side = True
            $ _vt_seat_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_SEAT_TOGETHER, "I'll sit next to you.")
            selected_girl.character "[_vt_seat_line]"
            $ _vt_seat_spontaneous_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEAT_SPONTANEOUS_ACTION_LINES)
            "[_vt_seat_spontaneous_line]"

            menu:
                "Let her stay beside you":
                    pass
                "Ask her to sit across instead":
                    $ _vt_seat_across_ask_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEAT_ACROSS_ASK_LINES)
                    player.character "[_vt_seat_across_ask_line]"
                    $ _booth_same_side = False
                    $ _vt_seat_move_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_SEAT_MOVE_AWAY, "Oh, okay, sure.")
                    selected_girl.character "[_vt_seat_move_line]"
                    $ _vt_seat_move_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEAT_MOVE_AWAY_ACTION_LINES)
                    "[_vt_seat_move_action_line]"
        else:
            $ _vt_seat_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_SEAT_ACROSS, "I'll sit over here.")
            selected_girl.character "[_vt_seat_line]"
            $ _vt_seat_across_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEAT_ACROSS_ACTION_LINES)
            "[_vt_seat_across_line]"

            menu:
                "Invite her to sit beside you":
                    $ _vt_seat_ask_pitch = vt_player_voice(player, VT_BAR_BOOTH_SEAT_ASK_LINES, "Come sit over here with me, it's more fun this side.")
                    player.character "[_vt_seat_ask_pitch]"
                    python:
                        _seat_roll = renpy.random.randint(1, 100)
                        _seat_threshold = max(20, min(95, _booth_closeness))
                        _seat_success = _seat_roll <= _seat_threshold
                        vt_log_roll("bar seating persuasion", _seat_roll, _seat_threshold, _seat_success)
                    if _seat_success:
                        $ _booth_same_side = True
                        $ _vt_seat_ask_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_SEAT_ASK_YES, "Okay, I'll come sit next to you.")
                        selected_girl.character "[_vt_seat_ask_line]"
                        $ _vt_seat_ask_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEAT_ASK_YES_ACTION_LINES)
                        "[_vt_seat_ask_action_line]"
                    else:
                        $ _vt_seat_ask_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_SEAT_ASK_NO, "No, I'll just stay here.")
                        selected_girl.character "[_vt_seat_ask_line]"
                "Let her sit across from you":
                    pass

        # --- Action loop ---
        $ _booth_done_flirty = set()
        $ _vt_booth_grope_earned_bonus = False
        $ _vt_booth_end_visit = False
        $ _vt_booth_player_came = False
        $ _booth_intimacy_blocked = False
        $ _vt_booth_girl_came = False
        $ _vt_booth_grope_succeeded = False
        $ _vt_booth_touch_bare_started = False
        $ _vt_bar_booth_sour_ending = False
        $ _vt_booth_flirt_uses = VT_BAR_BOOTH_FLIRT_USES

        # Every generic_action_* call below (grope/finger/handjob/blowjob/fuck_pussy) is a standalone
        # call, not a real screen_sex_interaction_menu.rpy session -- so the base game's own
        # is_during_sex_interaction flag (screen_sex_interaction_menu.rpy:235) never gets set just by
        # being here. That flag is read by a lot of shared machinery that assumes it reflects reality
        # (orgasm-reaction-line tiering, Player.apply_impacts' foreplay arousal dampening, this mod's
        # own vt_wants_pullout pull-out-coercion gate and vt_record_prev_act ATM-reaction recorder) --
        # setting it for the scene's duration makes the booth behave like a real sex scene for all of
        # that, instead of silently falling through to whatever each caller does when it's absent.
        $ vt_booth_start_encounter(selected_girl)

        label vt_bar_booth_resume:
        while not _vt_booth_end_visit:
            # Reset every round, same convention every base-game location screen uses (e.g.
            # screen_bar.rpy:188) -- otherwise a stale True from an earlier climax this visit (e.g. he
            # came during "Ride my cock") survives into a LATER, unrelated action. generic_action_finger_
            # pussy/tease_clit both end with "elif player.just_came: call generic_action_player_choose_
            # cum(...)" -- with the flag never cleared, picking "Finish her off" afterward re-enters
            # that menu on a stale flag alone, as a bogus second "Ah fuck I'm gonna cum!" with no new
            # arousal behind it. _vt_booth_player_came (set separately, right after each real climax)
            # already tracks "has he finished this visit" for menu-gating, so clearing this here doesn't
            # lose anything. Her just_came flag is equally action-local; the separate girl finish
            # flag keeps her visit outcome after this boundary clears both signals.
            $ vt_booth_clear_climax_flags(selected_girl)

            python:
                menu_options = []
                if get_action_count("small_talk", actions_already_done[selected_girl.id]) < 2:
                    menu_options.append(("Small talk", "vt_bar_booth_small_talk"))
                if "compliment" not in _booth_done_flirty:
                    menu_options.append(("Compliment her", "vt_bar_booth_compliment"))
                if _vt_booth_flirt_uses > 0:
                    # Purely additive alongside Compliment, same independence from seating/
                    # intimacy_blocked -- a talk-only beat, gated only by its own per-visit counter.
                    # No remaining-count in the caption (per direct user instruction) -- same
                    # unlabeled convention as Compliment/Handhold's own one-shot gates.
                    menu_options.append(("Flirt with her", "vt_bar_booth_flirt"))
                if "handhold" not in _booth_done_flirty:
                    menu_options.append(("Hold her hand", "vt_bar_booth_handhold"))
                if not _booth_same_side:
                    menu_options.append(("Caress her thigh under the table|Not available while sitting across from her", None))
                    if not _vt_booth_touch_bare_started:
                        if _vt_booth_grope_succeeded:
                            menu_options.append(("Continue groping her|Not available while sitting across from her", None))
                        else:
                            menu_options.append(("Slide your hand between her legs|Not available while sitting across from her", None))
                    if _vt_booth_grope_succeeded and not _vt_booth_girl_came:
                        if _vt_booth_player_came:
                            menu_options.append(("Finish her off|Not available while sitting across from her", None))
                        else:
                            menu_options.append(("Touch her bare|Not available while sitting across from her", None))
                    if not _vt_booth_player_came:
                        menu_options.append(("Ask for a handjob|Not available while sitting across from her", None))
                        menu_options.append(("Ask for a blowjob|Not available while sitting across from her", None))
                        menu_options.append(("Ride my cock|Not available while sitting across from her", None))
                elif _booth_intimacy_blocked:
                    # Once blocked, none of the escalation-tier options are offered at all -- omitted
                    # outright (not greyed), matching the small-talk-cap convention elsewhere.
                    pass
                else:
                    if "thigh" not in _booth_done_flirty:
                        menu_options.append(("Caress her thigh under the table", "vt_bar_booth_thigh"))
                    else:
                        if not _vt_booth_touch_bare_started:
                            if _vt_booth_grope_succeeded:
                                menu_options.append(("Continue groping her", "vt_bar_booth_grope"))
                            else:
                                menu_options.append(("Slide your hand between her legs", "vt_bar_booth_grope"))
                        if _vt_booth_grope_succeeded and not _vt_booth_girl_came:
                            if _vt_booth_player_came:
                                menu_options.append(("Finish her off", "vt_bar_booth_finger"))
                            else:
                                menu_options.append(("Touch her bare", "vt_bar_booth_finger"))
                    if not _vt_booth_player_came:
                        menu_options.append(("Ask for a handjob", "vt_bar_booth_ask_handjob"))
                        menu_options.append(("Ask for a blowjob", "vt_bar_booth_ask_blowjob"))
                        menu_options.append(("Ride my cock", "vt_bar_booth_ask_fuck"))
                menu_options.extend(vt_bar_booth_venue_options(selected_girl))
                menu_options.append(("Finish your drink", "vt_bar_booth_finish"))

                menu_choice = renpy.display_menu(menu_options)

            if menu_choice == "vt_bar_booth_finish":
                $ _vt_booth_end_visit = True

            elif menu_choice in ("bathroom", "player_home"):
                call vt_bar_booth_invite_venue(menu_choice)
                if _return:
                    # The adapter has cleared booth state and owns this departure. Forward
                    # its destination to bar_discussion; never clean up the new encounter.
                    return _return

            elif menu_choice == "vt_bar_booth_small_talk":
                call make_small_talk

            elif menu_choice == "vt_bar_booth_compliment":
                $ _booth_done_flirty.add("compliment")
                $ _vt_compliment_line = vt_player_voice(player, VT_BAR_BOOTH_COMPLIMENT_LINES, "You know, you look really good tonight.")
                player.character "[_vt_compliment_line]"
                $ _vt_compliment_tier = vt_booth_affection_tier(selected_girl)
                if selected_girl.has_trait("drunk"):
                    $ _vt_compliment_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_COMPLIMENT_REACT_DRUNK)
                elif selected_girl.has_trait("tipsy"):
                    $ _vt_compliment_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_COMPLIMENT_REACT_TIPSY)
                else:
                    $ _vt_compliment_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_COMPLIMENT_REACT[_vt_compliment_tier], "Thank you, that's sweet.")
                selected_girl.character "[_vt_compliment_react]"
                $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_COMPLIMENT_IMPACTS_BY_TIER[_vt_compliment_tier]))

            elif menu_choice == "vt_bar_booth_flirt":
                $ _vt_booth_flirt_uses -= 1

                menu:
                    "Command her, low and sure. (Dominate)":
                        $ _vt_flirt_approach = "dominate"
                    "Tell her how much she means to you. (Compassionate)":
                        $ _vt_flirt_approach = "compassionate"
                    "Describe exactly what you want to do to her. (Sexualized)":
                        $ _vt_flirt_approach = "sexualized"
                    "Offer to make it worth her while. (Transactional)":
                        $ _vt_flirt_approach = "transactional"

                $ _vt_flirt_line = _vt_resolve_words(selected_girl, vt_booth_choice(selected_girl, VT_BAR_BOOTH_FLIRT_LINES[_vt_flirt_approach]), player)
                player.character "[_vt_flirt_line]"

                python:
                    # Fresh, LOCAL dominant_approach/approach_strength -- deliberately NOT
                    # selected_girl.dominant_approach, which is only ever set by vt_bathroom.rpy and
                    # isn't guaranteed present on an arbitrary booth girl (confirmed via research).
                    # Formula reused verbatim from vt_bathroom.rpy:57-61.
                    _flirt_girl_approaches = {
                        "dominate": (selected_girl.discipline + selected_girl.fear) / 2,
                        "compassionate": (selected_girl.affection + selected_girl.intellect) / 2,
                        "sexualized": (selected_girl.corruption + selected_girl.naturism) / 2,
                        "transactional": (selected_girl.corruption + selected_girl.intellect) / 2,
                    }
                    _flirt_dominant_approach = max(_flirt_girl_approaches, key=_flirt_girl_approaches.get)
                    _flirt_approach_strength = _flirt_girl_approaches[_flirt_dominant_approach]

                    _flirt_base_score = vt_booth_local_acceptance(selected_girl, *VT_BAR_BOOTH_FLIRT_LOCAL_FLOOR)

                    _flirt_bonus = 0
                    if _vt_flirt_approach == _flirt_dominant_approach:
                        _flirt_bonus = int(_flirt_approach_strength * VT_BAR_BOOTH_FLIRT_MATCH_BONUS_SCALE)
                    elif VT_BAR_BOOTH_FLIRT_APPROACH_CLASH_MAP.get(_vt_flirt_approach) == _flirt_dominant_approach:
                        _flirt_bonus = -int(_flirt_approach_strength * VT_BAR_BOOTH_FLIRT_CLASH_PENALTY_SCALE)

                    _flirt_final_score = max(0, min(100, _flirt_base_score + _flirt_bonus))

                    _flirt_tier = "great"
                    for _flirt_tier_name, _flirt_tier_ceiling in VT_BAR_BOOTH_FLIRT_TIER_CUTOFFS:
                        if _flirt_final_score < _flirt_tier_ceiling:
                            _flirt_tier = _flirt_tier_name
                            break

                    vt_log(f"CALC vt_bar_booth_flirt({_vt_display_name(selected_girl)}): approach={_vt_flirt_approach} "
                           f"dominant={_flirt_dominant_approach}({_flirt_approach_strength:.1f}) base={_flirt_base_score} "
                           f"bonus={_flirt_bonus:+d} final={_flirt_final_score} -> tier={_flirt_tier}")

                if _flirt_tier == "critical_fail":
                    # Below "miss" -- reuses the sex_gate hard-reject SHAPE (spoken reject + narration
                    # action line + harsh penalty + end the visit), not vt_booth_check_overstim (which
                    # never ends the visit). Drunk/tipsy override first, same dispatch order every
                    # other reaction site in this file uses.
                    if selected_girl.has_trait("drunk"):
                        $ _vt_flirt_reject_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_FLIRT_CRITFAIL_REJECT_DRUNK)
                    elif selected_girl.has_trait("tipsy"):
                        $ _vt_flirt_reject_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_FLIRT_CRITFAIL_REJECT_TIPSY)
                    else:
                        $ _vt_flirt_reject_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_FLIRT_CRITFAIL_REJECT, "That was way too much. I'm leaving.")
                    selected_girl.character "[_vt_flirt_reject_line]"
                    $ _vt_flirt_reject_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_FLIRT_CRITFAIL_ACTION_LINES)
                    "[_vt_flirt_reject_action_line]"
                    $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_FLIRT_CRITFAIL_IMPACTS))
                    $ store._vt_booth_end_visit = True
                    $ store._vt_bar_booth_sour_ending = True
                else:
                    if selected_girl.has_trait("drunk"):
                        $ _vt_flirt_react_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_FLIRT_REACT_DRUNK_BY_TIER[_flirt_tier])
                    elif selected_girl.has_trait("tipsy"):
                        $ _vt_flirt_react_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_FLIRT_REACT_TIPSY_BY_TIER[_flirt_tier])
                    else:
                        $ _vt_flirt_react_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_FLIRT_REACT_BY_TIER[_flirt_tier], "...")
                    selected_girl.character "[_vt_flirt_react_line]"
                    $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_FLIRT_IMPACTS_BY_TIER[_flirt_tier]))

            elif menu_choice == "vt_bar_booth_handhold":
                $ _booth_done_flirty.add("handhold")
                if _booth_same_side:
                    $ _vt_handhold_ask = vt_player_voice(player, VT_BAR_BOOTH_HANDHOLD_SAMESIDE_LINES, "You take her hand under the table.")
                    player.character "[_vt_handhold_ask]"
                else:
                    $ _vt_handhold_ask = vt_player_voice(player, VT_BAR_BOOTH_HANDHOLD_ACROSS_LINES, "You reach across the sticky table and take her hand.")
                    player.character "[_vt_handhold_ask]"
                python:
                    _handhold_chance = vt_booth_stage_chance(selected_girl, "handhold", VT_BAR_BOOTH_STAGE_ORDER,
                                                              VT_BAR_BOOTH_LOCAL_TIER_FLOORS, VT_BAR_BOOTH_STAGE_BANDS,
                                                              _vt_bar_booth_stage_chance)
                    _vt_bar_booth_stage_chance["handhold"] = _handhold_chance
                    _handhold_roll = renpy.random.randint(1, 100)
                    _handhold_success = _handhold_roll <= _handhold_chance
                    vt_log_roll("bar hand-hold", _handhold_roll, _handhold_chance, _handhold_success)
                if _handhold_success:
                    if selected_girl.has_trait("drunk"):
                        $ _vt_handhold_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_HANDHOLD_ACCEPT_DRUNK)
                    elif selected_girl.has_trait("tipsy"):
                        $ _vt_handhold_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_HANDHOLD_ACCEPT_TIPSY)
                    else:
                        $ _vt_handhold_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_HANDHOLD_ACCEPT, "That's nice.")
                    selected_girl.character "[_vt_handhold_react]"
                    $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["handhold"]))
                else:
                    if selected_girl.has_trait("drunk"):
                        $ _vt_handhold_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_HANDHOLD_REJECT_DRUNK)
                    elif selected_girl.has_trait("tipsy"):
                        $ _vt_handhold_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_HANDHOLD_REJECT_TIPSY)
                    else:
                        $ _vt_handhold_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_HANDHOLD_REJECT, "I'm not ready for that yet.")
                    selected_girl.character "[_vt_handhold_react]"
                    $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["handhold_reject"]))
                    $ _booth_intimacy_blocked = True

            elif menu_choice == "vt_bar_booth_thigh":
                $ _booth_done_flirty.add("thigh")
                $ _vt_thigh_ask = vt_player_voice(player, VT_BAR_BOOTH_THIGH_ASK_LINES, "You rest a hand on her thigh under the table, sliding it slowly upward.")
                "[_vt_thigh_ask]"
                python:
                    _thigh_chance = vt_booth_stage_chance(selected_girl, "thigh", VT_BAR_BOOTH_STAGE_ORDER,
                                                           VT_BAR_BOOTH_LOCAL_TIER_FLOORS, VT_BAR_BOOTH_STAGE_BANDS,
                                                           _vt_bar_booth_stage_chance)
                    _vt_bar_booth_stage_chance["thigh"] = _thigh_chance
                    _thigh_roll = renpy.random.randint(1, 100)
                    _thigh_success = _thigh_roll <= _thigh_chance
                    vt_log_roll("bar thigh", _thigh_roll, _thigh_chance, _thigh_success)
                if _thigh_success:
                    if selected_girl.has_trait("drunk"):
                        $ _vt_thigh_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_THIGH_REACT_DRUNK)
                    elif selected_girl.has_trait("tipsy"):
                        $ _vt_thigh_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_THIGH_REACT_TIPSY)
                    else:
                        $ _vt_thigh_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_THIGH_REACT, "Careful, someone might see.")
                    selected_girl.character "[_vt_thigh_react]"
                    $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["thigh"]))
                    $ _vt_booth_grope_earned_bonus = True
                else:
                    if selected_girl.has_trait("drunk"):
                        $ _vt_thigh_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_THIGH_REJECT_DRUNK)
                    elif selected_girl.has_trait("tipsy"):
                        $ _vt_thigh_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_THIGH_REJECT_TIPSY)
                    else:
                        $ _vt_thigh_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_THIGH_REJECT, "Not yet, let's slow down.")
                    selected_girl.character "[_vt_thigh_react]"
                    $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["thigh_reject"]))
                    $ _booth_intimacy_blocked = True

            elif menu_choice == "vt_bar_booth_grope":
                if _vt_booth_grope_succeeded:
                    # Consent for this was already established by the first success -- continuing to
                    # grope her needs no fresh acceptance roll and no spoken reaction each time, just
                    # the action itself.
                    $ _vt_grope_access_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GROPE_CONTINUE_LINES)
                    "[_vt_grope_access_line]"
                    $ _vt_pre_pressure = selected_girl.pressure
                    $ _vt_pre_temp_pressure = selected_girl.temp_pressure
                    call generic_action_grope_pussy(additional_subtags=additional_subtags, skip_descriptions=True, skip_responses=True, force_orgasm=False)
                    $ vt_booth_apply_pressure_relief(selected_girl, _vt_pre_pressure, _vt_pre_temp_pressure)
                    if selected_girl.just_came:
                        if selected_girl.has_trait("drunk"):
                            $ _vt_girl_orgasm_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GIRL_ORGASM_DRUNK)
                        elif selected_girl.has_trait("tipsy"):
                            $ _vt_girl_orgasm_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GIRL_ORGASM_TIPSY)
                        else:
                            $ _vt_girl_orgasm_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_GIRL_ORGASM, "I'm coming!")
                        selected_girl.character "[_vt_girl_orgasm_line]"
                        $ _vt_booth_girl_came = True
                    elif vt_booth_check_overstim(selected_girl):
                        $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_ACTION_LINES)
                        "[_vt_overstim_action_line]"
                        if selected_girl.has_trait("drunk"):
                            $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_DRUNK)
                        elif selected_girl.has_trait("tipsy"):
                            $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_TIPSY)
                        else:
                            $ _vt_overstim_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                        selected_girl.character "[_vt_overstim_line]"
                        $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["overstim_stop"]))
                        $ _booth_intimacy_blocked = True
                else:
                    $ vt_log_acceptance_breakdown(selected_girl, "grope_pussy", player)
                    python:
                        _grope_chance = vt_booth_stage_chance(selected_girl, "grope", VT_BAR_BOOTH_STAGE_ORDER,
                                                               VT_BAR_BOOTH_LOCAL_TIER_FLOORS, VT_BAR_BOOTH_STAGE_BANDS,
                                                               _vt_bar_booth_stage_chance,
                                                               grope_earned=_vt_booth_grope_earned_bonus)
                        _vt_bar_booth_stage_chance["grope"] = _grope_chance
                        _vt_booth_grope_earned_bonus = False
                        _grope_roll = renpy.random.randint(1, 100)
                        _grope_success = _grope_roll <= _grope_chance
                        vt_log_roll("bar grope", _grope_roll, _grope_chance, _grope_success)
                    if _grope_success:
                        if selected_girl.has_trait("drunk"):
                            $ _vt_grope_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GROPE_ACCEPT_DRUNK)
                        elif selected_girl.has_trait("tipsy"):
                            $ _vt_grope_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GROPE_ACCEPT_TIPSY)
                        else:
                            $ _vt_grope_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_GROPE_ACCEPT, "Okay, go ahead.")
                        selected_girl.character "[_vt_grope_react]"
                        $ _vt_grope_style = vt_booth_lower_access_style(selected_girl)
                        $ _vt_grope_access_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GROPE_ACCESS_LINES[_vt_grope_style])
                        "[_vt_grope_access_line]"
                        $ _vt_pre_pressure = selected_girl.pressure
                        $ _vt_pre_temp_pressure = selected_girl.temp_pressure
                        call generic_action_grope_pussy(additional_subtags=additional_subtags, skip_descriptions=True, skip_responses=True, force_orgasm=False)
                        $ vt_booth_apply_pressure_relief(selected_girl, _vt_pre_pressure, _vt_pre_temp_pressure)
                        $ vt_booth_overlay_girl = selected_girl
                        $ _vt_booth_grope_succeeded = True
                        if selected_girl.just_came:
                            if selected_girl.has_trait("drunk"):
                                $ _vt_girl_orgasm_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GIRL_ORGASM_DRUNK)
                            elif selected_girl.has_trait("tipsy"):
                                $ _vt_girl_orgasm_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GIRL_ORGASM_TIPSY)
                            else:
                                $ _vt_girl_orgasm_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_GIRL_ORGASM, "I'm coming!")
                            selected_girl.character "[_vt_girl_orgasm_line]"
                            $ _vt_booth_girl_came = True
                        elif vt_booth_check_overstim(selected_girl):
                            $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_ACTION_LINES)
                            "[_vt_overstim_action_line]"
                            if selected_girl.has_trait("drunk"):
                                $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_DRUNK)
                            elif selected_girl.has_trait("tipsy"):
                                $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_TIPSY)
                            else:
                                $ _vt_overstim_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                            selected_girl.character "[_vt_overstim_line]"
                            $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["overstim_stop"]))
                            $ _booth_intimacy_blocked = True
                    else:
                        if selected_girl.has_trait("drunk"):
                            $ _vt_grope_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GROPE_REJECT_DRUNK)
                        elif selected_girl.has_trait("tipsy"):
                            $ _vt_grope_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GROPE_REJECT_TIPSY)
                        else:
                            $ _vt_grope_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_GROPE_REJECT, "Not here, that's too much.")
                        selected_girl.character "[_vt_grope_react]"
                        $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["grope_reject"]))
                        $ _booth_intimacy_blocked = True

            elif menu_choice == "vt_bar_booth_finger":
                $ _vt_booth_touch_bare_started = True
                $ vt_log_acceptance_breakdown(selected_girl, "finger_pussy", player)
                python:
                    _finger_chance = vt_booth_stage_chance(selected_girl, "finger", VT_BAR_BOOTH_STAGE_ORDER,
                                                            VT_BAR_BOOTH_LOCAL_TIER_FLOORS, VT_BAR_BOOTH_STAGE_BANDS,
                                                            _vt_bar_booth_stage_chance)
                    _vt_bar_booth_stage_chance["finger"] = _finger_chance
                    _finger_roll = renpy.random.randint(1, 100)
                    _finger_success = _finger_roll <= _finger_chance
                    vt_log_roll("bar touch her bare", _finger_roll, _finger_chance, _finger_success)
                if _finger_success:
                    if selected_girl.has_trait("drunk"):
                        $ _vt_finger_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_FINGER_ACCEPT_DRUNK)
                    elif selected_girl.has_trait("tipsy"):
                        $ _vt_finger_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_FINGER_ACCEPT_TIPSY)
                    else:
                        $ _vt_finger_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_FINGER_ACCEPT, "Okay, go ahead.")
                    selected_girl.character "[_vt_finger_react]"
                    $ _vt_touch_stop = False
                    $ _vt_touch_last_technique = None
                    while not _vt_touch_stop and not _booth_intimacy_blocked and not _vt_booth_girl_came:
                        $ vt_booth_clear_climax_flags(selected_girl)
                        $ _vt_touch_style = vt_booth_lower_access_style(selected_girl)
                        menu:
                            "Finger her":
                                $ _vt_touch_technique = "finger"
                            "Use two fingers":
                                $ _vt_touch_technique = "two_fingers"
                            "Focus on her clit":
                                $ _vt_touch_technique = "clit"
                            "Stop touching her":
                                $ _vt_touch_technique = "stop"

                        if _vt_touch_technique == "stop":
                            $ _vt_touch_stop_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_TOUCH_STOP_ACTION_LINES)
                            "[_vt_touch_stop_line]"
                            $ _vt_touch_stop = True
                        else:
                            if selected_girl.has_trait("drunk"):
                                $ _vt_touch_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_TOUCH_ACCEPT_DRUNK)
                            elif selected_girl.has_trait("tipsy"):
                                $ _vt_touch_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_TOUCH_ACCEPT_TIPSY)
                            else:
                                $ _vt_touch_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_TOUCH_ACCEPT, "Okay, don't stop.")
                            selected_girl.character "[_vt_touch_react]"
                            if _vt_touch_last_technique is None:
                                $ _vt_touch_access_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_TOUCH_ACCESS_LINES[_vt_touch_technique][_vt_touch_style])
                            else:
                                $ _vt_touch_access_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_TOUCH_TRANSITION_LINES[(_vt_touch_last_technique, _vt_touch_technique)])
                            "[_vt_touch_access_line]"
                            $ _vt_touch_last_technique = _vt_touch_technique
                            $ _vt_pre_pressure = selected_girl.pressure
                            $ _vt_pre_temp_pressure = selected_girl.temp_pressure
                            $ vt_log(f"bar {_vt_touch_technique} attempt pre: {_vt_display_name(selected_girl)} arousal={selected_girl.arousal} pressure={selected_girl.pressure}")
                            if _vt_touch_technique == "clit":
                                call generic_action_tease_clit(additional_subtags=additional_subtags, skip_descriptions=True, skip_responses=True, force_orgasm=False, can_deny_orgasm=False)
                            else:
                                call generic_action_finger_pussy(additional_subtags=additional_subtags, skip_descriptions=True, skip_responses=True, force_orgasm=False, can_deny_orgasm=False)
                            $ vt_booth_apply_pressure_relief(selected_girl, _vt_pre_pressure, _vt_pre_temp_pressure)
                            $ vt_log(f"bar {_vt_touch_technique} attempt post: {_vt_display_name(selected_girl)} arousal={selected_girl.arousal} pressure={selected_girl.pressure} just_came={selected_girl.just_came}")
                            if selected_girl.just_came:
                                if selected_girl.has_trait("drunk"):
                                    $ _vt_girl_orgasm_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GIRL_ORGASM_DRUNK)
                                elif selected_girl.has_trait("tipsy"):
                                    $ _vt_girl_orgasm_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_GIRL_ORGASM_TIPSY)
                                else:
                                    $ _vt_girl_orgasm_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_GIRL_ORGASM, "I'm coming!")
                                selected_girl.character "[_vt_girl_orgasm_line]"
                                $ _vt_booth_girl_came = True
                            elif vt_booth_check_overstim(selected_girl):
                                $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_ACTION_LINES)
                                "[_vt_overstim_action_line]"
                                if selected_girl.has_trait("drunk"):
                                    $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_DRUNK)
                                elif selected_girl.has_trait("tipsy"):
                                    $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_TIPSY)
                                else:
                                    $ _vt_overstim_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                                selected_girl.character "[_vt_overstim_line]"
                                $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["overstim_stop"]))
                                $ _booth_intimacy_blocked = True
                else:
                    if selected_girl.has_trait("drunk"):
                        $ _vt_finger_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_FINGER_REJECT_DRUNK)
                    elif selected_girl.has_trait("tipsy"):
                        $ _vt_finger_react = vt_booth_choice(selected_girl, VT_BAR_BOOTH_FINGER_REJECT_TIPSY)
                    else:
                        $ _vt_finger_react = vt_booth_voice(selected_girl, VT_BAR_BOOTH_FINGER_REJECT, "That's too much, not here.")
                    selected_girl.character "[_vt_finger_react]"
                    $ selected_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["finger_reject"]))
                    $ _booth_intimacy_blocked = True

            elif menu_choice in ("vt_bar_booth_ask_handjob", "vt_bar_booth_ask_blowjob", "vt_bar_booth_ask_fuck"):
                if menu_choice == "vt_bar_booth_ask_handjob":
                    $ _vt_bar_booth_act = "handjob"
                elif menu_choice == "vt_bar_booth_ask_blowjob":
                    $ _vt_bar_booth_act = "blowjob"
                else:
                    $ _vt_bar_booth_act = "fuck_pussy"
                call vt_bar_booth_sex_gate(_vt_bar_booth_act)

        if not _vt_bar_booth_sour_ending and se_end_label in ("vt_forced_sex_ending", "vt_force_fail_followup"):
            # This standalone booth owns its return/cleanup. Consume the existing adverse
            # ending's words here rather than jumping through its normal-sex map handoff.
            call vt_bar_booth_adverse_ending
            $ _vt_bar_booth_sour_ending = True
        if not _vt_bar_booth_sour_ending:
            $ _vt_visit_end_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VISIT_END_ACTION_LINES)
            "[_vt_visit_end_line]"

        $ vt_booth_end_encounter(selected_girl)
        $ remove_girl_id_from_location(selected_girl.id, "girls_at_bar")
    else:
        if selected_girl.has_trait("drunk"):
            $ _vt_bb_decline_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_DECLINE_DRUNK)
        elif selected_girl.has_trait("tipsy"):
            $ _vt_bb_decline_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_DECLINE_TIPSY)
        else:
            $ _vt_bb_decline_line = vt_booth_voice(selected_girl, VT_BAR_BOOTH_DECLINE, "No thanks... I'm fine right here.")
        selected_girl.character "[_vt_bb_decline_line]"
        $ _vt_decline_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_DECLINE_ACTION_LINES)
        "[_vt_decline_action_line]"

    return "show_bar"


# Shared push/respect negotiation for the three sexual asks (act_key: "handjob"/"blowjob"/
# "fuck_pussy"). Reads her live arousal/intox fresh every call via vt_booth_stage_chance (reused
# directly from the coffee shop file -- fully generic). Sets store._vt_booth_end_visit = True on any
# outcome that ends the visit (hard reject, or a failed push), read back by the action loop above after
# this call returns; sets store._vt_bar_booth_sour_ending = True alongside it so the closing narration
# above doesn't contradict a storm-out/failed-push ending.
#
# Rolls a die against the same per-visit stage-chance machinery every earlier stage uses (2026-09-26 --
# see vt_coffeeshop_booth.rpy's header for the full rationale), replacing the old deterministic
# `if _sg_acceptance >= 40` threshold check. Same three-outcome shape as before, per direct user
# instruction: hard reject / negotiate-a-push / immediate accept, now decided by a roll.
label vt_bar_booth_sex_gate(act_key):
    python:
        _sg_girl = selected_girl
        _sg_ask = vt_player_voice(player, VT_BAR_BOOTH_SEX_ASK[act_key], "Okay, how about a little fun under the table?")
    player.character "[_sg_ask]"

    $ vt_log_acceptance_breakdown(_sg_girl, act_key, player)
    python:
        _sg_chance = vt_booth_stage_chance(_sg_girl, act_key, VT_BAR_BOOTH_STAGE_ORDER,
                                            VT_BAR_BOOTH_LOCAL_TIER_FLOORS, VT_BAR_BOOTH_STAGE_BANDS,
                                            _vt_bar_booth_stage_chance)
        _vt_bar_booth_stage_chance[act_key] = _sg_chance
        _sg_roll = renpy.random.randint(1, 100)
        if _sg_roll <= _sg_chance:
            _sg_outcome = "accept"
        elif _sg_roll <= _sg_chance + VT_BOOTH_SEX_PUSH_WINDOW:
            _sg_outcome = "push"
        else:
            _sg_outcome = "reject"
        vt_log_band_roll(f"bar sex gate '{act_key}'", _sg_roll, _sg_chance, VT_BOOTH_SEX_PUSH_WINDOW, _sg_outcome)

    if _sg_outcome == "accept":
        if _sg_girl.has_trait("drunk"):
            $ _sg_accept_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_ACCEPT_DRUNK)
        elif _sg_girl.has_trait("tipsy"):
            $ _sg_accept_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_ACCEPT_TIPSY)
        else:
            $ _sg_accept_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_SEX_ACCEPT[act_key], "Okay, I can do that.")
        _sg_girl.character "[_sg_accept_line]"
        $ time_manager.skip_time(minutes=10)
        $ vt_booth_clear_climax_flags(selected_girl)

        if act_key == "fuck_pussy":
            call vt_bar_booth_vaginal_condom_gate(_sg_girl)
            if vt_bar_booth_vaginal_proceed:
                $ _sg_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_ACTION_IMMEDIATE[act_key])
                if act_key == "blowjob":
                    call vt_booth_protection_gate(_sg_girl, "oral")
                    if not vt_booth_protection_proceed:
                        return
                "[_sg_action_line]"
                call vt_bar_booth_vaginal_action
                if player.just_came:
                    $ _sg_finish_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_FINISH_LINES[act_key])
                    "[_sg_finish_line]"
                else:
                    $ _sg_heldback_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_HELDBACK_LINES[act_key])
                    "[_sg_heldback_line]"
                $ vt_log(f"bar sex gate '{act_key}' immediate-accept path: player finished this call = {player.just_came}")
                if player.just_came:
                    $ store._vt_booth_player_came = True
                $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["sex_accept"]))
                # Her own orgasm from this act (generic_action_fuck_pussy already called .cum() on her
                # silently, via skip_responses) needs to latch the booth's OWN tracking flag too --
                # otherwise "Touch her bare" keeps thinking she hasn't finished, since that flag was
                # previously only ever set from the grope/finger touch loop, never from here.
                if _sg_girl.just_came:
                    $ store._vt_booth_girl_came = True
                elif vt_booth_check_overstim(_sg_girl):
                    # She didn't orgasm herself, but her pressure capped anyway -- same "had enough
                    # teasing" bailout the grope/finger touch loop already applies, just never wired up
                    # for this harder escalation tier until now. Act-keyed narration (not the flat
                    # grope/finger pool) since this act's positioning differs.
                    $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_OVERSTIM_ACTION_LINES[act_key])
                    "[_vt_overstim_action_line]"
                    if _sg_girl.has_trait("drunk"):
                        $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_DRUNK)
                    elif _sg_girl.has_trait("tipsy"):
                        $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_TIPSY)
                    else:
                        $ _vt_overstim_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                    _sg_girl.character "[_vt_overstim_line]"
                    $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["overstim_stop"]))
                    $ store._booth_intimacy_blocked = True
            else:
                $ _vt_condom_decline_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VAGINAL_CONDOM_DECLINE_ACTION_LINES)
                "[_vt_condom_decline_line]"
        else:
            $ _sg_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_ACTION_IMMEDIATE[act_key])
            if act_key == "blowjob":
                call vt_booth_protection_gate(_sg_girl, "oral")
                if not vt_booth_protection_proceed:
                    return
            "[_sg_action_line]"
            call vt_booth_buildup(act_key, additional_subtags=additional_subtags)
            if player.just_came:
                $ _sg_finish_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_FINISH_LINES[act_key])
                "[_sg_finish_line]"
            else:
                $ _sg_heldback_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_HELDBACK_LINES[act_key])
                "[_sg_heldback_line]"
            $ vt_log(f"bar sex gate '{act_key}' immediate-accept path: player finished this call = {player.just_came}")
            if player.just_came:
                $ store._vt_booth_player_came = True
            $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["sex_accept"]))
            if _sg_girl.just_came:
                $ store._vt_booth_girl_came = True
            elif vt_booth_check_overstim(_sg_girl):
                $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_OVERSTIM_ACTION_LINES[act_key])
                "[_vt_overstim_action_line]"
                if _sg_girl.has_trait("drunk"):
                    $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_DRUNK)
                elif _sg_girl.has_trait("tipsy"):
                    $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_TIPSY)
                else:
                    $ _vt_overstim_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                _sg_girl.character "[_vt_overstim_line]"
                $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["overstim_stop"]))
                $ store._booth_intimacy_blocked = True

    elif _sg_outcome == "push":
        $ _sg_interject_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_SEX_INTERJECT, "Wait, here? Someone might see us.")
        _sg_girl.character "[_sg_interject_line]"

        $ _sg_menu_push = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_MENU_PUSH_CAPTION, "Push her a little")
        $ _sg_menu_respect = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_MENU_RESPECT_CAPTION, "Respect her wishes")
        menu:
            "[_sg_menu_push]":
                $ _sg_pitch = vt_player_voice(player, VT_BAR_BOOTH_PUSH_PITCH, "Come on, it's dark back here and everyone's watching the game, not us. Just this once.")
                player.character "[_sg_pitch]"
                python:
                    _sg_push_chance = vt_booth_push_chance(_sg_girl, act_key)
                    _sg_push_roll = renpy.random.randint(1, 100)
                    _sg_push_success = _sg_push_roll <= _sg_push_chance
                    vt_log_roll(f"bar push '{act_key}'", _sg_push_roll, _sg_push_chance, _sg_push_success)
                if _sg_push_success:
                    $ _sg_push_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_PUSH_SUCCESS, "Okay, fine. Just be quick.")
                    _sg_girl.character "[_sg_push_line]"
                    $ time_manager.skip_time(minutes=10)
                    $ vt_booth_clear_climax_flags(selected_girl)

                    if act_key == "fuck_pussy":
                        call vt_bar_booth_vaginal_condom_gate(_sg_girl)
                        if vt_bar_booth_vaginal_proceed:
                            $ _sg_push_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_ACTION_PUSH[act_key])
                            if act_key == "blowjob":
                                call vt_booth_protection_gate(_sg_girl, "oral")
                                if not vt_booth_protection_proceed:
                                    return
                            "[_sg_push_action_line]"
                            call vt_bar_booth_vaginal_action
                            if player.just_came:
                                $ _sg_push_finish_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_FINISH_PUSH_LINES[act_key])
                                "[_sg_push_finish_line]"
                            else:
                                $ _sg_push_heldback_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_HELDBACK_PUSH_LINES[act_key])
                                "[_sg_push_heldback_line]"
                            $ vt_log(f"bar sex gate '{act_key}' push-success path: player finished this call = {player.just_came}")
                            if player.just_came:
                                $ store._vt_booth_player_came = True
                            $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["push_success"]))
                            if _sg_girl.just_came:
                                $ store._vt_booth_girl_came = True
                            elif vt_booth_check_overstim(_sg_girl):
                                $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_OVERSTIM_ACTION_LINES[act_key])
                                "[_vt_overstim_action_line]"
                                if _sg_girl.has_trait("drunk"):
                                    $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_DRUNK)
                                elif _sg_girl.has_trait("tipsy"):
                                    $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_TIPSY)
                                else:
                                    $ _vt_overstim_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                                _sg_girl.character "[_vt_overstim_line]"
                                $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["overstim_stop"]))
                                $ store._booth_intimacy_blocked = True
                        else:
                            $ _vt_condom_decline_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_VAGINAL_CONDOM_DECLINE_ACTION_LINES)
                            "[_vt_condom_decline_line]"
                    else:
                        $ _sg_push_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_ACTION_PUSH[act_key])
                        if act_key == "blowjob":
                            call vt_booth_protection_gate(_sg_girl, "oral")
                            if not vt_booth_protection_proceed:
                                return
                        "[_sg_push_action_line]"
                        call vt_booth_buildup(act_key, additional_subtags=additional_subtags)
                        if player.just_came:
                            $ _sg_push_finish_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_FINISH_PUSH_LINES[act_key])
                            "[_sg_push_finish_line]"
                        else:
                            $ _sg_push_heldback_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_HELDBACK_PUSH_LINES[act_key])
                            "[_sg_push_heldback_line]"
                        $ vt_log(f"bar sex gate '{act_key}' push-success path: player finished this call = {player.just_came}")
                        if player.just_came:
                            $ store._vt_booth_player_came = True
                        $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["push_success"]))
                        if _sg_girl.just_came:
                            $ store._vt_booth_girl_came = True
                        elif vt_booth_check_overstim(_sg_girl):
                            $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_SEX_OVERSTIM_ACTION_LINES[act_key])
                            "[_vt_overstim_action_line]"
                            if _sg_girl.has_trait("drunk"):
                                $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_DRUNK)
                            elif _sg_girl.has_trait("tipsy"):
                                $ _vt_overstim_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_OVERSTIM_STOP_TIPSY)
                            else:
                                $ _vt_overstim_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                            _sg_girl.character "[_vt_overstim_line]"
                            $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["overstim_stop"]))
                            $ store._booth_intimacy_blocked = True
                else:
                    if _sg_girl.has_trait("drunk"):
                        $ _sg_fail_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_PUSH_FAIL_DRUNK)
                    elif _sg_girl.has_trait("tipsy"):
                        $ _sg_fail_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_PUSH_FAIL_TIPSY)
                    else:
                        $ _sg_fail_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_PUSH_FAIL, "No, I meant it. Not here.")
                    _sg_girl.character "[_sg_fail_line]"
                    $ _sg_fail_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_PUSH_FAIL_ACTION_LINES)
                    "[_sg_fail_action_line]"
                    $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["push_fail"]))
                    $ actions_already_done[_sg_girl.id].append("block_talking_bar")
                    $ store._vt_booth_end_visit = True
                    $ store._vt_bar_booth_sour_ending = True

            "[_sg_menu_respect]":
                $ _sg_respect_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_RESPECT, "Thank you for understanding.")
                _sg_girl.character "[_sg_respect_line]"
                $ vt_booth_reward_respect(_sg_girl, act_key, VT_BAR_BOOTH_IMPACTS["respect"])

    else:
        if _sg_girl.has_trait("drunk"):
            $ _sg_reject_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_HARD_REJECT_DRUNK)
        elif _sg_girl.has_trait("tipsy"):
            $ _sg_reject_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_HARD_REJECT_TIPSY)
        else:
            $ _sg_reject_line = vt_booth_voice(_sg_girl, VT_BAR_BOOTH_HARD_REJECT, "That's way too much. I'm leaving.")
        _sg_girl.character "[_sg_reject_line]"
        $ _sg_reject_action_line = vt_booth_choice(selected_girl, VT_BAR_BOOTH_HARD_REJECT_ACTION_LINES)
        "[_sg_reject_action_line]"
        $ _sg_girl.apply_impacts(dict(VT_BAR_BOOTH_IMPACTS["hard_reject"]))
        $ store._vt_booth_end_visit = True
        $ store._vt_bar_booth_sour_ending = True

    return


# Called only after the booth's acceptance AND protection decisions have resolved. Reuse the
# dedicated first-time words, without entering the normal-sex gate's different fallback flow.
label vt_bar_booth_vaginal_action:
    $ _bb_first_time = bool(getattr(selected_girl, "hymen", False) and getattr(selected_girl, "first_time_pussy", False))
    if not _bb_first_time:
        call vt_vaginal_buildup(additional_subtags=["bar", "booth"], skip_responses=True, ask_to_cum=True, force_cum=False)
        return

    $ _bb_first_time_tier = vt_booth_first_time_tier(selected_girl)
    $ _bb_first_time_line = vt_bar_booth_first_time_voice(selected_girl, VT_BOOTH_FIRST_TIME_VAGINAL_PRE_LINES[_bb_first_time_tier])
    selected_girl.character "[_bb_first_time_line]"

    # Mirror the booth's generic action parameters: one impact call, the same finish choice,
    # and the same orgasm/denial and cum-target dispatch. First-time aftermath belongs after
    # her orgasm bookkeeping and before any later pullout/creampie consequence.
    $ _bb_cum_before = selected_girl.sex_interaction_cum_count
    $ apply_action_impacts("fuck_pussy")
    $ media_helper.show_video("fuck_pussy", selected_girl, ["bar", "booth"])
    if currently_playing_video:
        pause
    else:
        $ renpy.notify("No videos for action found")

    $ _bb_force_cum = False
    if not person_doing_action.just_came:
        menu:
            "Stop before you cum":
                $ _bb_force_cum = False
            "Don't hold back":
                $ _bb_force_cum = True
    if _bb_force_cum and not person_doing_action.just_came:
        $ person_doing_action.cum()

    if selected_girl.just_came:
        call generic_action_orgasm("fuck_pussy", additional_subtags=["bar", "booth"], skip_descriptions=True, skip_responses=True, can_deny_orgasm=True)

    $ _bb_first_time_line = vt_bar_booth_first_time_voice(selected_girl, VT_BOOTH_FIRST_TIME_VAGINAL_LINES[_bb_first_time_tier])
    selected_girl.character "[_bb_first_time_line]"
    if selected_girl.sex_interaction_cum_count > _bb_cum_before:
        $ _bb_first_time_line = vt_bar_booth_first_time_voice(selected_girl, VT_BOOTH_FIRST_TIME_VAGINAL_ORGASM_ADDENDUM[_bb_first_time_tier], orgasm=True)
        selected_girl.character "[_bb_first_time_line]"

    if player.just_came:
        call generic_action_player_choose_cum(action_name="fuck_pussy", additional_subtags=["bar", "booth"], skip_descriptions=True, skip_responses=True)
    $ media_helper.hide_video()
    return


label vt_bar_booth_adverse_ending(departure_lines=None):
    if se_end_label == "vt_forced_sex_ending":
        $ _bb_adverse_lines = _vt_forced_conflicted_lines(selected_girl) if selected_girl.sex_interaction_cum_count > 0 else VT_FORCED_ENDING_ANGRY
    else:
        $ _bb_adverse_lines = VT_FORCED_ENDING_ATTEMPT
    $ _bb_adverse_line = vt_booth_voice(selected_girl, _bb_adverse_lines, "I'm upset. I need to leave.")
    selected_girl.character "[_bb_adverse_line]"
    if se_end_label == "vt_forced_sex_ending" and not getattr(selected_girl, "birth_control", False):
        $ _bb_adverse_line = vt_booth_voice(selected_girl, VT_FORCED_ENDING_PREGNANCY_WORRY, "...")
        selected_girl.character "[_bb_adverse_line]"
    $ _bb_adverse_departure = vt_booth_choice(selected_girl, departure_lines if departure_lines is not None else VT_BAR_BOOTH_HARD_REJECT_ACTION_LINES)
    "[_bb_adverse_departure]"
    return


# Condom/consent glue for the "Ride my cock" escalation specifically -- this booth's first act with real
# pregnancy risk. Replicates vt_condom_attempt_gate's own decision logic (02_vt_gobare_coercion.rpy:
# 234-289) directly rather than reusing that label wholesale, since it's wired onto SexAction objects
# a standalone call never touches. Reuses vt_gobare_beat(girl, act) unchanged -- the real, already
# register-varied coercion beat used mod-wide, taking plain girl/act arguments (not screen-bound), so
# no new negotiation content needs writing here, only this glue. Sets store.vt_bar_booth_vaginal_proceed
# to whether the act should actually proceed.
label vt_bar_booth_vaginal_condom_gate(girl):
    $ store.vt_bar_booth_vaginal_proceed = True

    if (player.condom_active != "raw" and (not player.condom_broke or not girl.aware_vaginal_condom)) or "vaginal" in getattr(girl, "vt_bare_session", ()):
        return

    if not getattr(girl, "wants_vaginal_condom", False):
        return

    if "vaginal" in getattr(girl, "vt_gobare_attempted", ()):
        $ setattr(girl, "player_knows_vaginal_condom", True)
        $ _vt_bb_already = vt_booth_voice(girl, VT_GOBARE_ALREADY, "I already told you -- wrap it up.")
        girl.character "[_vt_bb_already]"
        $ store.vt_bar_booth_vaginal_proceed = False
        return

    call vt_gobare_beat(girl, "vaginal")
    if vt_gobare_beat_outcome not in ("yes_perm", "yes_session"):
        $ store.vt_bar_booth_vaginal_proceed = False
    return
