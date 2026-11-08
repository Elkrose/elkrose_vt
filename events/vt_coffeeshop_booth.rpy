# Coffee shop "Invite to a booth" rework. Soft-repoints the base game's
# coffee_shop_discussion_talk_in_booth (label_coffee_shop_discussions.rpy:608-719) to a mod-owned
# replacement -- no base-game file edits.
#
# What changed vs. the base scene, and why:
# - Sitting down together is now a near-universal "yes" (still the shared free_use_compliance
#   acceptance roll, just a far lower bar) -- it's a coffee shop booth, not a proposition.
# - A new seating beat decides whether she sits beside him or across, driven by a new
#   vt_booth_closeness_score() formula (affection + corruption); a girl who defaults to sitting
#   across can be asked to move, resolved by a single roll on the same score -- deliberately lighter
#   than the sexual negotiation below, since only the sexual asks were asked to get that treatment.
# - The booth is now a real loop (the base label only ever let you pick ONE follow-up action, then
#   ended the visit) offering: small talk (dispatches straight into the base game's own
#   make_small_talk, so it's capped by the same global 2-per-day counter no matter where it's used --
#   no separate tracking needed), three new flirtatious non-sexual actions, and the two existing
#   sexual asks -- until the player picks "Finish your coffee" or the scene ends on its own.
# - The inner-thigh caress and both sexual asks require sitting beside her (same_side); sitting
#   across still gets the reason shown via the game's own "text|explanation" greyed-menu-caption
#   convention (already used elsewhere in this exact database, e.g. "Give gift|Given a gift today").
# - The two sexual asks are now routed through a real push/respect coercion beat
#   (vt_coffeeshop_sex_gate), matching the shape 02_vt_gobare_coercion.rpy / 03_vt_pullout_coercion.rpy
#   already use, instead of the base game's flat single-roll accept/reject. Deliberately NOT given a
#   "force" escalation tier (out of scope for this pass -- see the plan this was built from).
# - Debug logging (VT_BOOTH_DEBUG, vt_log*): every acceptance calculation and RNG roll in this file
#   writes a breakdown to log.txt (renpy.log, already enabled unconditionally by
#   enable_devmode.rpy's config.log = "log.txt") for balance tuning. vt_log_acceptance_breakdown
#   reproduces Personality._get_action_success_by_requirements's own per-stat math and logs its
#   result NEXT TO the real get_acceptance_by_name(...) value so any drift is visible in the log
#   itself. Set VT_BOOTH_DEBUG = False to silence once tuning is done.
# - Both sexual asks let the player choose, each time, whether to actually finish -- passes
#   ask_to_cum=True/force_cum=False into generic_action_handjob/generic_action_blowjob instead of
#   forcing an orgasm outright, so the base game's own "Stop her before you cum"/"Don't hold back"
#   choice is presented (generic_actions_misc.rpy/generic_actions_face.rpy). player.just_came is
#   reset immediately before each call (it isn't reset between this loop's own iterations otherwise,
#   which previously caused a stale-flag replay: a second act right after an orgasm would show a
#   second "Ah fuck I'm gonna cum!" cum-target menu for a climax that didn't actually just happen).
#   Once a real orgasm lands (player.just_came is True right after the call), the visit-scoped
#   _vt_booth_player_came flag latches True and both sexual asks are omitted from the menu (not
#   greyed) for the rest of the visit -- matching the mod's small-talk-cap convention above. The
#   post-act closing line now branches on player.just_came too, so "Stop her before you cum" gets a
#   genuine held-back line instead of the finish line playing regardless of the player's choice.
# - Escalation ladder, redesigned per direct playtest feedback: Compliment stays gate-free but its
#   reaction/impact now scales with her current affection tier (vt_booth_affection_tier, 3 bands --
#   mirrors, at a smaller scale, how dialogs/vt_small_talk_affection.rpy already tiers its own
#   reaction). Hand-holding now rolls against vt_booth_closeness_score (the same formula seating
#   already uses -- both are "how comfortable is she with public physical closeness") and, on
#   rejection, sets _booth_intimacy_blocked, which hides thigh-caress and both sexual asks for the
#   rest of the visit (not the whole visit -- small talk/compliment/finish stay available).
# - Cold-ask penalty on the sex gate: the base game's real handjob/blowjob acceptance floors
#   (game/scripts/databases/personality/generic_actions/misc_actions_ren.py:17-30,
#   face_actions_ren.py:368-380 -- NOT the acceptance_calculation_database_ren.py file a prior
#   session's research checked and came up empty on) are tuned for an established relationship, not a
#   first ask in public, and made the sexual asks feel "basically automatic." Rather than edit that
#   shared formula or quietly move the accept/interject thresholds, VT_BOOTH_SEX_COLD_ASK_PENALTY is
#   subtracted from her score first and logged as its own explicit line, so the real base-game score
#   and the booth-specific adjustment both stay visible and separately tunable.
# - Manual-touch escalation past the thigh caress: "Slide your hand between her legs" (calls the real
#   generic_action_grope_pussy, force_orgasm=False) is gated the same way as the sex-gate (her real
#   grope_pussy acceptance minus VT_BOOTH_SEX_COLD_ASK_PENALTY, a genuine roll) -- a rejection reuses
#   _booth_intimacy_blocked, same as a hand-hold rejection. Success unlocks "Touch her bare, try to
#   make her cum" (calls the real generic_action_finger_pussy, also force_orgasm=False) -- no separate
#   consent roll there (consent was already established by the grope succeeding), just the base game's
#   own organic arousal-threshold orgasm mechanism (apply_impacts flips just_came once arousal crosses
#   99) deciding whether she actually finishes. Both calls' access narration is clothing-aware
#   (vt_booth_lower_access_style: dress/skirt vs jeans-leggings-shorts vs already-bare vs generic,
#   mirroring the base game's own remove_lower/strip_lower dress-vs-pants narration split) on top of
#   grope_pussy's own already-clothing-aware description text. Her arousal/pressure are reset to her
#   own base_arousal/base_pressure at the top of each visit (NOT Girl.reset_for_sex(), which also
#   spikes tolerance and touches sex-interaction-only bookkeeping) so this ladder plays out
#   predictably regardless of unrelated carryover from an earlier scene the same day. Once she
#   orgasms this way, _vt_booth_girl_came hides "Touch her bare" for the rest of the visit (omitted,
#   same convention as the player's own post-orgasm pruning); until then it's repeatable.
# - "Touch her bare" is now a 3-technique submenu (Finger her / Slide a second finger in / Focus on
#   her clit), added per direct playtest feedback that repeating the same action showed only 1-2
#   base-game narration lines over and over. "Focus on her clit" calls the real, already-shipped
#   generic_action_tease_clit (distinct base-game description/reaction pool, between grope_pussy and
#   finger_pussy in intensity); the two finger techniques both mechanically call generic_action_
#   finger_pussy (no distinct base-game "two fingers" action exists) with different access-line
#   flavor only. Player hand_skill/vaginal_skill ALREADY scale arousal up and pressure down
#   automatically (scale_impacts_to_player_skill_multipliers, confirmed by direct research) -- an
#   unskilled player (hand_skill=0) sits at the worst end of both ratios, which is why a fresh
#   character's progress reads as slow; no new code needed for that half of the ask. What WAS missing:
#   pressure's own database numbers/formula headroom let it race arousal to its 100 cap well before
#   she can actually orgasm (confirmed: calculate_pressure_impact's clamp allows up to 2x nominal vs.
#   arousal's 1x cap, and arousal's own modifier is dragged down by rising pressure) -- if she caps out
#   without finishing, vt_booth_check_overstim (a new mod-side check; the closest base-game precedent,
#   screen_sex_interaction_menu.rpy:425, ejects her from a sex-interaction round on pressure alone,
#   with no equivalent "did she finish first" condition) has her push his hands away and ask him to
#   stop, setting _booth_intimacy_blocked same as any other rejection. A small live overlay
#   (screen vt_booth_arousal_overlay, dispatched from vt_huds/vt_overlay.rpy) shows her real arousal/
#   pressure bars once the escalation starts, reusing the base game's own bar styles.
# - "Touch her bare" is now a self-looping submenu (Finger her / Slide a second finger in / Focus on
#   her clit / Stop touching her) instead of a single pick that fell back to the main booth menu --
#   only "Stop touching her", an orgasm, or an overstim-stop exit the loop back to the main menu.
#   grope_pussy/tease_clit/finger_pussy are now all called with skip_descriptions=True (in addition to
#   skip_responses=True) to kill their own repetitive in-progress description/reaction lines -- this
#   ALSO silences their climax narration as a side effect (confirmed by direct read of
#   generic_action_orgasm, generic_actions_misc.rpy:1-48: the same flag gates both), so a new
#   VT_BOOTH_GIRL_ORGASM line is spoken explicitly wherever just_came is checked, replacing what was
#   suppressed rather than just losing it. Once _booth_intimacy_blocked is set, the main menu now
#   omits every escalation-tier option outright (not greyed) -- matching the small-talk-cap convention.
#   The technique-access line inside that submenu is now transition-aware: VT_BOOTH_TOUCH_ACCESS_LINES
#   (clothing-style-keyed "getting past her clothes" framing) only plays on the FIRST pick after
#   freshly entering the loop (_vt_touch_last_technique is None); every pick after that reads from
#   VT_BOOTH_TOUCH_TRANSITION_LINES, keyed by (last_technique, this_technique) -- her clothing is no
#   longer relevant once the player's hand is already there, only whether he's repeating a technique,
#   escalating (clit->finger->two_fingers), or backing off to a lighter one.
# - Seating is now a genuine roll (renpy.random.randint(1,100) <= vt_booth_seating_chance(...)) for
#   whether she sits close unprompted, instead of a flat >=65 deterministic threshold -- a spontaneous
#   "yes" now offers a follow-up "ask her to sit across instead" option (always succeeds, no roll,
#   since moving to the less-intimate seat is a low-friction downgrade), mirroring the existing
#   "invite her over" flow when the spontaneous roll fails. Hand-hold and thigh both now roll too
#   (thigh previously had no gate at all), each discounted by its own difficulty penalty
#   (VT_BOOTH_HANDHOLD_DIFFICULTY_PENALTY / VT_BOOTH_THIGH_DIFFICULTY_PENALTY -- thigh is a bigger ask
#   than hand-holding, which is a bigger ask than just tolerating a close seat). Grope now has its OWN,
#   smaller VT_BOOTH_GROPE_COLD_ASK_PENALTY instead of sharing
#   the sex gate's 45 -- sharing it made groping through her clothes read as HARDER to get than oral
#   sex in real play, confirmed by directly comparing two pasted log entries from the same encounter --
#   and now folds in vt_booth_arousal_bonus (consumed/re-granted) the same way the sex gate already
#   does, so thigh's escalation bonus rewards the very next step instead of skipping past it. Grope is
#   now repeatable ("Slide your hand between her legs" transforms into "Continue groping her" after a
#   first success, shown alongside the newly-unlocked "Touch her bare" -- renamed from "Touch her
#   bare, try to make her cum") -- once "Touch her bare" is first picked (_vt_booth_touch_bare_started),
#   "Continue groping her" disappears for good. The arousal/pressure overlay now first appears at
#   grope's success (moved from thigh) since thigh never touches her real arousal/pressure at all.
#   "Continue groping her" (2026-09-25): once the first grope has succeeded, consent for it is already
#   established -- repeat picks skip the acceptance roll AND her spoken accept line entirely, just
#   playing the action (access line + generic_action_grope_pussy + orgasm/overstim check) each time,
#   same as any other already-consented-to repeatable action in this file (e.g. the finger-touch loop).
# - Corrected immediately after real play exposed it: seating/hand-hold/thigh's original base score
#   (vt_booth_closeness_score, a flat linear_conversion(stat, 0, 100, 0, weight) blend) was on a much
#   stingier scale than grope_pussy's real acceptance key (whose action_requirements floors are a
#   narrow 20/10, not the full 0-100 range) -- for the same girl, closeness_score topped out at 51
#   while grope_pussy hit 80, so a thigh caress could roll HARDER than groping her even though it's
#   the lesser touch. Replaced with vt_booth_local_acceptance: a locally-built,
#   not-globally-registered acceptance_calculations-shaped dict evaluated through the same real
#   Personality.get_acceptance_by_requirements formula every actual key uses, with its own low floors
#   per tier (vt_booth_seating_chance/vt_booth_handhold_chance/vt_booth_thigh_chance, floors 5/3,
#   10/5, 15/8 -- all below grope_pussy's own 20/10) -- puts every rung of this ladder on a
#   comparable, consistently-generous scale instead of retuning flat penalties on an unrelated one.
# - Corrected again (2026-09-25) after real play showed the fix above still read as too generous: a
#   merely mid-level girl (Carolina, corruption 44/affection 58) was landing at a 95%+ near-lock on
#   seating/hand-hold/thigh. The user was explicit this is not a floor problem or a "different
#   resistance stat" problem (both offered, both declined) -- raised the flat penalties substantially
#   instead: new VT_BOOTH_SEATING_DIFFICULTY_PENALTY (0->35, seating had none before), hand-hold
#   (5->40), thigh (10->45), grope's own cold-ask penalty (20->55). Floors/axis/shape all untouched.
#   Flagged honestly to the user and left as-is on their instruction: because the floors don't move, a
#   "well-progressed" girl and a "fully maxed" girl still saturate to the identical pre-penalty raw
#   score for these tiers -- a flat penalty lowers the absolute height for everyone but can't restore
#   that lost distinction; only floor changes could, which the user didn't want.
# - Her live arousal now actually matters (2026-09-25). Traced at the user's direct question: nothing
#   in this ladder ever read her real `arousal` stat -- only a flat, one-time vt_booth_arousal_bonus
#   (thigh success -> +15 feeding grope's own roll; grope success -> +25 feeding whatever roll came
#   next) that never once looked at her actual arousal number, even though grope/finger-touching
#   already raise it for real via generic_action_grope_pussy/finger_pussy's genuine arousal impacts.
#   Per the user's explicit scope ("arousal only relevant for acts BEYOND groping"): grope's own roll
#   is untouched (still corruption/affection/fear + its cold-ask penalty, no arousal); "Touch her bare"
#   (vt_booth_finger) -- which previously had NO acceptance check at all, also flagged by the user via
#   a real log -- now rolls against the real finger_pussy acceptance key (floors 30/20) plus a new
#   vt_booth_arousal_aid(girl) term (scales 0..VT_BOOTH_AROUSAL_AID_CAP with her live arousal 0..100)
#   minus VT_BOOTH_FINGER_COLD_ASK_PENALTY; the handjob/blowjob sex gate reads the same live-arousal
#   term in place of the old flat vt_booth_arousal_bonus (nothing to consume/reset anymore -- it's read
#   fresh every call). VT_BOOTH_GROPE_AROUSAL_BONUS is retired entirely; VT_BOOTH_THIGH_AROUSAL_BONUS
#   is untouched (it only ever fed grope's own roll, which stays arousal-free).
# - Fixed a real escalation-ordering inversion, caught via real play (2026-09-25): grope's flat
#   VT_BOOTH_THIGH_AROUSAL_BONUS (+15, added before its own penalty) and finger's vt_booth_arousal_aid
#   (up to +30) could each outweigh the gap between adjacent tiers' cold-ask penalties once a girl's
#   stats were high enough to saturate every tier's base formula to the same raw 100 -- for exactly
#   such a girl, thigh (55) came out HARDER to pass than grope (60), and grope harder than finger (64),
#   backwards from the intended escalating difficulty. Re-derived VT_BOOTH_GROPE_COLD_ASK_PENALTY
#   (55->65) and VT_BOOTH_FINGER_COLD_ASK_PENALTY (40->85) together, checked via a standalone script
#   against 5 profiles (moderate, early/fresh, saturated-sober, saturated-drunk, maxed-drunk) so the
#   chain now holds seating>=handhold>=thigh>grope>finger (ties only at the 5% floor) in every one, not
#   just the profile that happened to be tested before.
# - Second real cliff, caught via real play (2026-09-26): the SAME girl (Kenzie Reeves, saturated/
#   drunk) exposed that finger's own gap-to-grope still ballooned in practice (grope's +15 bonus is
#   guaranteed every time, while finger's own live arousal-aid was often near-zero early on) AND that
#   handjob/blowjob shared one flat 45 cold-ask penalty, weaker than finger's 85 -- meaning both were
#   backwards-easier than touching her bare. Re-derived VT_BOOTH_FINGER_COLD_ASK_PENALTY (85->55) and
#   split VT_BOOTH_SEX_COLD_ASK_PENALTY from one shared int into a per-act dict (handjob 60/blowjob 65),
#   verified via the same standalone-script discipline: the worst case (no arousal built up yet) now
#   descends in a clean, even 5-point-per-rung chain (handhold>=thigh>grope>finger>handjob>blowjob) for
#   every profile tested. Also new this pass, both confirmed directly with the user: an explicit,
#   always-felt drink bonus (vt_booth_intox_bonus -- +10 tipsy/+25 drunk, stacked on TOP of the trait's
#   own automatic acceptance bonus, since that one is often invisible once a girl's already saturated)
#   applied at every stage; and vt_booth_arousal_aid reworked from a continuous linear formula to a
#   tiered one off her real, player-visible arousal band (get_arousal_state()) -- +5 per tier level. A
#   well-aroused girl can now let handjob/blowjob briefly overtake finger/grope in the FINAL chance --
#   confirmed with the user this is an intended reward for a patient playthrough, not a bug, since the
#   worst/rushed case (the one that actually broke) stays perfectly clean.
# - Stat-nuanced escalation rework (2026-09-26): reviewing the ladder surfaced a real design bug in the
#   flat-subtraction-plus-hard-clamp scheme every prior pass had been re-tuning -- checked against a
#   WIDE corruption/affection grid (not just the handful of high-end profiles those passes calibrated
#   against), it collapsed almost the entire low-to-moderate stat range to the identical 5% floor for
#   every stage past hand-hold, and the whole high end (corruption 80 vs 100) to identical numbers too.
#   A real playtest log showed WHY: a girl's real, per-act acceptance value hits its own ceiling well
#   before she's anywhere near maxed (each act's floor only spans a narrow window before saturating),
#   so a flat penalty subtracted from an already-saturated 100 either survives intact or crushes
#   straight through to the floor depending on tiny differences -- a "mid" girl read as barely
#   distinguishable from a total stranger. Replaced with: vt_booth_remap_chance (a per-stage linear
#   remap of her real acceptance into a narrower band, monotonic and injective across the WHOLE 0-100
#   input domain -- see its own docstring for why that's not the same as subtract-then-clamp),
#   vt_booth_gap_close (every situational bonus -- grope's guaranteed post-thigh nudge, live arousal,
#   drink -- now closes a FRACTION of the remaining headroom instead of adding a flat number, so it
#   can't dominate a near-zero baseline or blow past the ceiling), and a STRUCTURAL cascading cap
#   (vt_booth_stage_chance: each stage's chance is capped at the one before it in VT_BOOTH_STAGE_ORDER,
#   by construction -- guaranteed, not hand-verified against a handful of profiles the way the last
#   cliff snuck back in). Also, per direct user instruction: the handjob/blowjob sex gate no longer
#   uses a deterministic `score >= 40` threshold (the one stage in the whole ladder with no actual
#   randomness) -- it now rolls a die against the same chance number every earlier stage uses, keeping
#   the exact same three-outcome shape (hard reject / negotiate-a-push / immediate accept), just
#   decided by a roll instead of a flat comparison.
#
# Out of scope this pass, flagged not forgotten: no force-escalation tier; no condom-coercion-gate
# integration (this call path bypasses that system entirely, same as the library today); no seating/
# outcome persistence beyond the single visit; no new sexual acts beyond the existing handjob/blowjob
# pair.

init 5 python:
    if "database_coffee_shop_options" in globals():
        vt_repoint_menu_label(database_coffee_shop_options, "coffee_shop_discussion_talk_in_booth", "vt_coffeeshop_booth")

# Girl/Mother to show the arousal/pressure overlay for, or None to hide it. Set/cleared directly by
# this file's own label (see vt_coffeeshop_booth below) -- deliberately NOT derived from
# vt_active_label, which doesn't revert when this scene calls out to other labels (make_small_talk,
# the touch/sex generic actions) and so can't reliably answer "are we still in this scene."
default vt_booth_overlay_girl = None
default _vt_booth_respected_acts = set()

init python:

    # --- Debug logging (writes to log.txt via renpy.log -- config.log = "log.txt" is already set
    # unconditionally in enable_devmode.rpy, the same mechanism 06_vt_covert_pill.rpy already relies
    # on for its own error logging). Purely diagnostic: never reads back its own output, never
    # changes any game state, safe to leave on. Toggle VT_BOOTH_DEBUG to False to silence it once
    # tuning is done, without deleting the call sites. ---
    VT_BOOTH_DEBUG = False

    def vt_log(msg):
        # Debug-only: must never be able to crash real gameplay, so this swallows anything odd
        # about the message itself too (e.g. a caller building it from an attribute that doesn't
        # exist on every character subclass -- see the Mother/.full_name incident this was added
        # after).
        if not VT_BOOTH_DEBUG:
            return
        try:
            renpy.log(f"[VT BOOTH] {msg}")
        except Exception as e:
            try:
                renpy.log(f"[VT BOOTH] (log message failed: {e})")
            except Exception:
                pass

    def _vt_display_name(character):
        """Girl and Mother both expose full_name, not name (confirmed by direct crash: Mother has
        no .name at all, and Girl doesn't either -- only full_name, class_girl_ren.py:225 /
        class_mother_ren.py:325-327). Falls back to .id, then a literal placeholder, so this can
        never itself throw."""
        for attr in ("full_name", "id"):
            value = getattr(character, attr, None)
            if value:
                return value
        return "<unknown>"

    def vt_log_girl_snapshot(girl, player=None):
        """Full stat snapshot at a point in time -- broader context alongside the per-calculation
        breakdowns above, since those only log the specific stats a given acceptance key weighs.
        The coffee shop can seat a Mother as well as a Girl (confirmed by a live crash -- Mother
        objects don't share every attribute a Girl has), so every read here is defensive; on any
        unexpected shape this logs the failure instead of raising, since a debug helper must never
        be able to crash the actual scene."""
        try:
            stats = {
                "affection": getattr(girl, "affection", None), "corruption": getattr(girl, "corruption", None),
                "fear": getattr(girl, "fear", None), "naturism": getattr(girl, "naturism", None),
                "intellect": getattr(girl, "intellect", None), "discipline": getattr(girl, "discipline", None),
                "arousal": getattr(girl, "arousal", None),
            }
            line = f"SNAPSHOT {_vt_display_name(girl)}: " + ", ".join(f"{k}={v}" for k, v in stats.items())
            if player is not None:
                line += f" | player.reputation={getattr(player, 'reputation', '?')}"
            vt_log(line)
        except Exception as e:
            vt_log(f"SNAPSHOT failed for {_vt_display_name(girl)}: {e}")

    def vt_log_roll(label, roll, threshold, passed):
        """A genuine RNG roll (e.g. renpy.random.randint) compared against a threshold."""
        vt_log(f"ROLL  {label}: roll={roll} vs threshold={threshold} -> {'PASS' if passed else 'FAIL'}")

    def vt_log_check(label, score, threshold, passed):
        """A deterministic acceptance-score check against a threshold -- no randomness involved,
        unlike vt_log_roll. Kept separate so the log makes clear which gates are actually random."""
        vt_log(f"CHECK {label}: score={score} vs threshold={threshold} -> {'PASS' if passed else 'FAIL'}")

    def vt_log_band_roll(label, roll, chance, push_window, outcome):
        """A three-way banded roll (accept/push/reject) -- accept if roll<=chance, push-eligible if
        roll<=chance+push_window, else hard reject. Kept separate from vt_log_roll (binary) since this
        reports which of three bands the roll landed in, and from vt_log_check (deterministic) since
        this one really is a roll."""
        vt_log(f"ROLL  {label}: roll={roll} vs chance={chance:.0f} (push_window=+{push_window}) -> {outcome}")

    def vt_log_acceptance_breakdown(girl, action_name, player=None):
        """Full per-stat breakdown of a get_acceptance_by_name(action_name) result, for tuning.
        Mirrors Personality._get_action_success_by_requirements's own per-stat math
        (class_personality_ren.py:219-274) for the plain stat-range case -- the only case
        free_use_compliance/handjob/blowjob/kiss actually use (none of them touch the tolerance/
        arousal/multiplier_attributes special-casing that function also handles). Calls the SAME
        sub-methods the base game uses for the bonus components (_get_acceptance_bonus_from_status/
        _get_acceptance_bonus_from_rules/get_acceptance_modifiers) rather than re-deriving them, and
        logs its own reproduced total next to the real, authoritative get_acceptance_by_name(...)
        result so any drift (e.g. a future key that DOES hit a special case) is immediately visible
        in the log itself rather than silently wrong.

        The whole body is wrapped defensively: this is diagnostic-only and must never be able to
        crash the scene it's instrumenting, even if a future call site passes a character subclass
        (Mother, etc.) that doesn't share every attribute/method a Girl has -- exactly what caused a
        real crash here (Mother has no .name -- and neither does Girl, only .full_name)."""
        name = _vt_display_name(girl)
        try:
            if action_name not in database_acceptance_calculations:
                vt_log(f"ACCEPT '{action_name}' for {name}: no database_acceptance_calculations entry -> flat 0")
                return

            action_data = database_acceptance_calculations[action_name]
            action_requirements = action_data.get("action_requirements", {})
            accept_influences = action_data.get("accept_influences", {})
            trait_influences = action_data.get("trait_influences", {})
            min_acceptance = action_data.get("min_acceptance", 0)
            max_acceptance = 100

            parts = [f"ACCEPT breakdown '{action_name}' for {name}:"]
            running = accept_influences.get("base", 0)
            parts.append(f"  base={running}")

            for stat_name, stat_data in accept_influences.items():
                if stat_name == "base":
                    continue
                stat_weight = stat_data.get("weight")
                if stat_name == "reputation":
                    stat_value = getattr(player, "reputation", None) if player is not None else None
                elif stat_name in ("tolerance", "arousal") or stat_name in multiplier_attributes:
                    parts.append(f"  {stat_name}: UNMODELED special-case stat (weight={stat_weight}) -- see class_personality_ren.py")
                    continue
                else:
                    stat_value = getattr(girl, stat_name, None)
                if stat_value is None:
                    parts.append(f"  {stat_name}: <not found on {type(girl).__name__}>")
                    continue

                if stat_name in action_requirements:
                    min_range = action_requirements[stat_name]
                    max_range = linear_conversion(min_range, 0, 50, 40, 80)
                else:
                    min_range, max_range = 0, 100

                contribution = linear_conversion(stat_value, min_range, max_range, 0, 100) * stat_weight
                running += contribution
                parts.append(f"  {stat_name}: raw={stat_value} range=({min_range:.1f},{max_range:.1f}) weight={stat_weight} -> {contribution:+.1f}")

            status_bonus = girl.personality._get_acceptance_bonus_from_status()
            rules_bonus = girl.personality._get_acceptance_bonus_from_rules()
            trait_bonus = girl.get_acceptance_modifiers(action_name, include_generic=True, traits_with_bonuses=trait_influences)
            parts.append(f"  + status_bonus={status_bonus:+.1f} rules_bonus={rules_bonus:+.1f} trait_bonus={trait_bonus:+.1f}")

            normalized = running + status_bonus + rules_bonus + trait_bonus
            reproduced = int(linear_conversion(normalized, 0, 100, min_acceptance, max_acceptance))
            actual = girl.get_acceptance_by_name(action_name)
            parts.append(f"  normalized={normalized:.1f} -> remapped[{min_acceptance},{max_acceptance}]={reproduced}  (live get_acceptance_by_name={actual})")

            vt_log("\n".join(parts))
        except Exception as e:
            vt_log(f"ACCEPT breakdown failed for '{action_name}' / {name} ({type(girl).__name__}): {e}")

    # --- Tunable formulas (placeholder base/spread, flagged for tuning) ---

    def vt_booth_local_acceptance(girl, corruption_floor, affection_floor):
        """Builds a LOCAL, not-globally-registered acceptance_calculations-shaped dict and evaluates
        it through the SAME real formula machinery every actual acceptance key uses
        (Personality.get_acceptance_by_requirements, class_personality_ren.py:153-154) -- keeps
        seating/hand-hold/thigh on the same narrow-floor, comparably generous scale as
        grope_pussy/handjob/blowjob, instead of a flat 0-100-denominator formula that was never on a
        comparable scale to begin with (confirmed live: that mismatch is what made a mere thigh
        caress roll harder than groping her, for the same girl, in the same encounter). Safe to call
        with no matching real action name -- Girl.get_acceptance_modifiers(None, ...) only ever does
        dict.get(None, 0) internally, confirmed by direct read."""
        action_data = {
            "action_requirements": {"corruption": corruption_floor, "affection": affection_floor},
            "accept_influences": {
                "corruption": {"weight": 0.6},
                "affection": {"weight": 0.4},
                "fear": {"weight": -0.4},
            },
        }
        score = int(girl.personality.get_acceptance_by_requirements(action_data))
        vt_log(f"CALC vt_booth_local_acceptance({_vt_display_name(girl)}, corruption_floor={corruption_floor}, "
               f"affection_floor={affection_floor}) -> {score}")
        return score

    def vt_booth_arousal_fraction(girl):
        """How much her CURRENT, real arousal helps her accept a further ask -- reworked (2026-09-26)
        from a flat added bonus to a GAP-CLOSING fraction (see vt_booth_gap_close below): off her real,
        player-visible arousal band (Girl.get_arousal_state(), class_girl_ren.py:5414), None=0%,
        Minor=5%, Aroused=10%, Horny=15%, Soaking Wet=20%, Edging=25% of whatever headroom she has left
        to this stage's own ceiling. A flat add either dominated a near-zero baseline or did nothing
        near the ceiling depending on where she sat -- a fraction of the gap scales itself down
        automatically at both ends. Only wired into rolls for acts BEYOND groping (touch her bare,
        handjob, blowjob, fuck_pussy) -- grope's own roll stays arousal-free, since before grope
        nothing has raised her arousal yet."""
        tier_level, tier_label = girl.get_arousal_state()
        fraction = tier_level * VT_BOOTH_AROUSAL_FRACTION_PER_TIER
        vt_log(f"CALC vt_booth_arousal_fraction({_vt_display_name(girl)}, arousal={girl.arousal}, "
               f"tier={tier_label}[{tier_level}]) -> {fraction:.2f}")
        return fraction

    def vt_booth_intox_fraction(girl):
        """Explicit, always-felt drink bonus -- separate from (and stacked on top of) the real
        base-game trait's own automatic acceptance bonus (tipsy +10/drunk +20 via base_stat_modifiers,
        already baked into every accept_influences calculation before its own 100-clamp). That
        automatic bonus is often invisible for an already-saturated girl (she was clamping at 100
        regardless) -- this is a second, intentionally-stacked bonus. Reworked (2026-09-26) from a flat
        added bonus to a gap-closing fraction (10% tipsy / 25% drunk of the remaining headroom to this
        stage's own ceiling), same reasoning as vt_booth_arousal_fraction above. Applies at every stage
        of the ladder except seating (hand-hold through ride-him alike)."""
        if girl.has_trait("drunk"):
            fraction = VT_BOOTH_DRUNK_INTOX_FRACTION
        elif girl.has_trait("tipsy"):
            fraction = VT_BOOTH_TIPSY_INTOX_FRACTION
        else:
            fraction = 0.0
        vt_log(f"CALC vt_booth_intox_fraction({_vt_display_name(girl)}): drunk={girl.has_trait('drunk')} "
               f"tipsy={girl.has_trait('tipsy')} -> {fraction:.2f}")
        return fraction

    def vt_booth_remap_chance(real_acceptance, min_out, max_out):
        """Replaces the old `real_acceptance - flat_penalty` step. A straight linear_conversion is
        monotonic and injective across the WHOLE 0-100 input domain, unlike subtract-then-clamp -- two
        girls with different real acceptance almost always land on different chances, all the way down
        near the bottom of this stage's own band, instead of both collapsing to the identical floor the
        instant the subtraction goes negative."""
        return linear_conversion(real_acceptance, 0, 100, min_out, max_out)

    def vt_booth_gap_close(value, ceiling, fraction):
        """Replaces every flat bonus add. Closes `fraction` of the remaining distance from `value` up
        to `ceiling` -- scales itself down automatically near the ceiling (no overflow into an
        artificial cap) and near the floor (no single bonus dominating a near-zero baseline), which a
        flat add could not do. Fraction is clamped to [0, 0.9] -- a stacked bonus can get her very
        close to this stage's ceiling, never guaranteed all the way to it."""
        fraction = max(0.0, min(0.9, fraction))
        return value + fraction * (ceiling - value)

    # Ladder stage names, in escalating-difficulty order -- shared by both this file and
    # vt_bar_booth.rpy (which appends its own extra "fuck_pussy" stage). "seating"/"handhold"/"thigh"
    # are this mod's own LOCAL stages (no matching real acceptance key, see
    # VT_BOOTH_LOCAL_TIER_FLOORS/vt_booth_stage_real_acceptance below); every other name is either a
    # real get_acceptance_by_name key directly ("handjob"/"blowjob"/"fuck_pussy") or this ladder's own
    # short name for one ("grope"->grope_pussy, "finger"->finger_pussy).
    VT_BOOTH_STAGE_ORDER = ["seating", "handhold", "thigh", "grope", "finger", "handjob", "blowjob"]
    VT_BOOTH_REAL_ACTION_NAMES = {"grope": "grope_pussy", "finger": "finger_pussy"}

    def vt_booth_stage_real_acceptance(girl, tier_key, local_floors):
        """Her real, stat-driven acceptance (0-100) for one ladder stage -- vt_booth_local_acceptance
        for this file's own local stages (using `local_floors`, the calling file's own floor
        constants), the real base-game acceptance key for every other stage."""
        if tier_key in local_floors:
            cf, af = local_floors[tier_key]
            return vt_booth_local_acceptance(girl, corruption_floor=cf, affection_floor=af)
        action_name = VT_BOOTH_REAL_ACTION_NAMES.get(tier_key, tier_key)
        return girl.get_acceptance_by_name(action_name)

    def vt_booth_stage_chance(girl, tier_key, stage_order, local_floors, bands, cache, grope_earned=False):
        """Generic, per-visit ladder-stage chance (2026-09-26 rework, replacing flat-subtraction +
        hard-clamp): remap her real acceptance into this stage's own band (vt_booth_remap_chance), close
        a fraction of the remaining gap for situational bonuses (vt_booth_gap_close: grope's earned
        nudge, live arousal, drink), then STRUCTURALLY cap the result at the stage immediately before it
        in `stage_order` -- guaranteeing "never easier than the step before it" by construction, instead
        of hand-picking band numbers and hoping a grid sweep finds no violations (how the last cliff
        snuck back in).

        `cache` is the calling file's own per-visit `_vt_..._stage_chance` dict (reset at the top of
        each visit) -- if the previous ladder stage was actually rolled this visit, its real recorded
        chance (including whatever bonus applied at that moment) is used as the cap. If it was never
        attempted (always true for the sex-gate stages, which have no structural prerequisite; possible
        for grope->finger too), this recurses into a fresh, CONSERVATIVE computation instead -- one that
        assumes any not-yet-earned path-dependent bonus (grope's own guaranteed nudge) is 0, since we
        can't assume she already passed a step she never actually faced.

        The requested stage is always computed from live state, even on a retry. Only earlier
        stages use recorded chances as escalation caps.

        Callers are responsible for writing their own real rolls' chance into `cache` after calling
        this -- this function only reads the cache, it never writes to it, so a fallback probe (used
        purely to compute a cap) never poisons a stage's value before it's actually attempted for real."""
        real = vt_booth_stage_real_acceptance(girl, tier_key, local_floors)
        lo, hi = bands[tier_key]
        chance = vt_booth_remap_chance(real, lo, hi)

        fraction = 0.0
        if tier_key == "grope" and grope_earned:
            fraction += VT_BOOTH_GROPE_GUARANTEED_FRACTION
        if tier_key in ("finger", "handjob", "blowjob", "fuck_pussy"):
            fraction += vt_booth_arousal_fraction(girl)
        if tier_key != "seating":
            fraction += vt_booth_intox_fraction(girl)
        chance = vt_booth_gap_close(chance, hi, fraction)
        chance = max(5, min(96, chance))

        idx = stage_order.index(tier_key)
        if idx > 0:
            prev_key = stage_order[idx - 1]
            if prev_key in cache:
                prev_chance = cache[prev_key]
            else:
                prev_chance = vt_booth_stage_chance(girl, prev_key, stage_order, local_floors, bands, cache)
            chance = min(chance, prev_chance)

        vt_log(f"CALC vt_booth_stage_chance({_vt_display_name(girl)}, '{tier_key}'): real={real} "
               f"band=({lo},{hi}) fraction={fraction:.2f} -> {chance:.1f}")
        return chance

    def vt_booth_intox_pressure_relief(girl):
        """Fraction of a pressure GAIN to refund if she's tipsy/drunk (2026-09-26, bar-booth only --
        wired only from vt_bar_booth.rpy's own touch-action call sites, per direct user instruction)
        -- an intoxicated girl builds up mounting tension more slowly per touch (reduced inhibition/
        sensitivity), rather than reaching overstim as fast. Reuses the same 10%/25% tipsy/drunk split
        already established for vt_booth_intox_bonus, for consistency -- placeholder magnitude,
        flagged for tuning like every other formula in this file."""
        if girl.has_trait("drunk"):
            return 0.25
        elif girl.has_trait("tipsy"):
            return 0.10
        return 0.0

    def vt_booth_apply_pressure_relief(girl, pre_pressure, pre_temp_pressure):
        """Refund the same fraction of the net gain, accounting for the base 100-clamp.
        Girl.modify_stat records positive, growth-scaled pressure in temp_pressure BEFORE fix_stats
        caps it. At the cap, recover that lost headroom so large/repeated gains can still reach 100.
        Below the cap (including after an orgasm's pressure reduction), use the actual net gain."""
        post_pressure = girl.pressure
        if post_pressure >= 100:
            full_gain = max(0, girl.temp_pressure - pre_temp_pressure)
            post_pressure = max(post_pressure, pre_pressure + full_gain)
        gain = post_pressure - pre_pressure
        if gain <= 0:
            return
        relief = vt_booth_intox_pressure_relief(girl)
        if relief <= 0:
            return
        refund = gain * relief
        girl.pressure = max(girl.base_pressure, min(100, post_pressure - refund))
        vt_log(f"CALC vt_booth_apply_pressure_relief({_vt_display_name(girl)}): gain={gain:.1f} "
               f"relief_fraction={relief} refund={refund:.1f} -> pressure={girl.pressure:.1f}")

    def vt_booth_clear_climax_flags(girl):
        """Clear action-local signals AFTER callers have latched the visit's finish flags."""
        player.just_came = False
        girl.just_came = False

    def vt_booth_start_encounter(girl):
        """Initialize standalone action context without the base clothing/tolerance reset."""
        # Clear the previous participants' concessions before replacing their action context.
        vt_reset_sex_session()
        sex_interaction_clear()
        store.se_participants = [girl]
        store.se_female_participants = [girl]
        store.se_remaining_participants = [girl]
        store.se_interaction_type = "normal"
        store.se_player_cum_count = 0
        girl.sex_interaction_cum_count = 0
        girl.left_sex_interaction = False
        store.se_selected_part = None
        store.is_threesome_action = False
        store.person_doing_action = player
        store.action_assistant = None
        store.vt_orig_se_end_label = None
        store.vt_orig_se_use_generic_ending = None
        store.vt_forced_girl = None
        store.vt_force_outcome_this_session = None
        store.vt_forced_girl_was_virgin = False
        store.vt_force_creampie_active = False
        vt_reset_sex_session()
        vt_booth_clear_climax_flags(girl)
        store._vt_booth_respected_acts = set()
        store.is_during_sex_interaction = True

    def vt_booth_end_encounter(girl):
        """Shared cleanup for normal departures, hard refusals, and failed pushes."""
        vt_reset_sex_session()
        vt_booth_clear_climax_flags(girl)
        store.vt_booth_overlay_girl = None
        sex_interaction_clear()
        store.is_threesome_action = False
        store.person_doing_action = player
        store.action_assistant = None
        store.vt_orig_se_end_label = None
        store.vt_orig_se_use_generic_ending = None
        store.vt_forced_girl = None
        store.vt_force_outcome_this_session = None
        store.vt_forced_girl_was_virgin = False
        store.vt_force_creampie_active = False
        store._vt_booth_respected_acts = set()

    def vt_booth_reward_respect(girl, act_key, impacts):
        """Keep the response repeatable, but reward each act only once in this visit."""
        if act_key not in store._vt_booth_respected_acts:
            store._vt_booth_respected_acts.add(act_key)
            girl.apply_impacts(dict(impacts))

    def vt_booth_push_chance(girl, act_key):
        """Chance a push past her hesitation succeeds -- her own acceptance for the act itself, plus
        a nudge from how affection-trusting/already-corrupted she is (easier to coerce in the moment
        the more either already applies)."""
        base_acceptance = girl.get_acceptance_by_name(act_key)
        corruption_term = linear_conversion(girl.corruption, 0, 100, -10, 20)
        affection_term = linear_conversion(girl.affection, 0, 100, -10, 15)
        score = max(5, min(90, int(base_acceptance + corruption_term + affection_term)))
        vt_log(f"CALC vt_booth_push_chance({_vt_display_name(girl)}, '{act_key}'): base_acceptance={base_acceptance} "
               f"corruption={girl.corruption}->{corruption_term:+.1f} affection={girl.affection}->{affection_term:+.1f} -> chance={score}")
        return score

    def vt_booth_affection_tier(girl):
        """Simple 3-band affection tier for scaling a lighter reaction (Compliment) to her current
        stats -- mirrors, at a much smaller scale, how dialogs/vt_small_talk_affection.rpy already
        tiers its own reaction by her affection band. Placeholder cutoffs, flagged for tuning."""
        if girl.affection < 30:
            tier = "low"
        elif girl.affection < 60:
            tier = "mid"
        else:
            tier = "high"
        vt_log(f"CALC vt_booth_affection_tier({_vt_display_name(girl)}): affection={girl.affection} -> tier={tier}")
        return tier

    # Player-side twin of the register system above: what kind of guy is doing the asking, derived
    # from his own control/greed/lust/compassion stats (-10..10 each, class_player_ren.py:130-133 --
    # base-game-flagged "CURRENTLY UNUSED: Will influence dialogue lines and options"). Mirrors the
    # bucket names/framing of vt_bathroom.rpy's/vt_small_talk_pregnancy.rpy's own dead
    # dominant_approach scaffolding (computed there, never consumed) for mod-wide naming consistency,
    # but deliberately drops that formula's reputation/arousal blend and adds a real 'neutral'
    # fallback -- an untrained player sits at (0,0,0,0) all game, and neutral must be the honest common
    # case, not a forced pick among 4 (2026-09-26, per direct user instruction).
    VT_PLAYER_PERSONA_THRESHOLD = 3  # first non-trivial step above "untrained" on a -10..10 stat

    def vt_player_persona(player):
        """Player's dominant persona bucket -- recomputed fresh every call, nothing to cache (same
        philosophy as vt_booth_arousal_aid: cheap to compute, and there's no reason a stat read here
        would ever go stale within a visit)."""
        stats = {
            "dominant":      player.control,
            "compassionate": player.compassion,
            "sexual":        player.lust,
            "transactional": player.greed,
        }
        top_key = max(stats, key=lambda k: stats[k])  # ties broken by this fixed key order
        persona = top_key if stats[top_key] >= VT_PLAYER_PERSONA_THRESHOLD else "neutral"
        vt_log(f"CALC vt_player_persona: control={player.control} compassion={player.compassion} "
               f"lust={player.lust} greed={player.greed} -> {persona}")
        return persona

    def vt_player_voice(player, options, default=""):
        """Player-side twin of vt_voice -- picks a persona-appropriate line for something the PLAYER
        says, keyed on vt_player_persona(player) instead of the girl's register. Unlike vt_voice's
        register ladder, there's no natural fallback chain between personas (dominant isn't "closer
        to" transactional the way crude is closer to explicit than to demure) -- so every persona-keyed
        pool this reads must define all 5 keys including 'neutral' directly."""
        persona = vt_player_persona(player)
        v = options.get(persona) or options.get("neutral", [])
        return vt_booth_choice(selected_girl, v) if v else default

    def vt_booth_lower_access_style(girl):
        """Classifies her current lower-body clothing into an access style for the touch-escalation
        narration below -- 'dress' (reach up under a hem: a worn dress, or a skirt), 'pants' (work
        past a more restrictive garment: jeans/leggings/shorts), 'bare' (no lower coverage at all --
        reuses girl.is_bottomless(), which already correctly treats a worn dress as covering), or
        'generic' fallback. Mirrors the real dress-vs-jeans/leggings/shorts split the base game itself
        already uses for remove_lower/strip_lower narration (clothing_actions_ren.py:235,579)."""
        upper = girl.get_clothing_on_part("upper")
        lower = girl.get_clothing_on_part("lower")
        if upper is not None and upper.has_tag("dress"):
            style = "dress"
        elif lower is not None and lower.has_tag("skirt"):
            style = "dress"
        elif girl.is_bottomless():
            style = "bare"
        elif lower is not None and lower.has_tag(("jeans", "leggings", "shorts")):
            style = "pants"
        else:
            style = "generic"
        vt_log(f"CALC vt_booth_lower_access_style({_vt_display_name(girl)}) -> {style}")
        return style

    def vt_booth_check_overstim(girl):
        """After any pressure-affecting touch, called only when she HASN'T just orgasmed: if her
        pressure has capped without release, she's had enough teasing and stops him. New mod-side
        check -- no base-game precedent conditions a pressure-100 bailout on whether she's climaxed
        first (the closest precedent, screen_sex_interaction_menu.rpy:425, checks pressure alone,
        independent of orgasm state). Returns True if she just stopped him."""
        if girl.pressure >= 100:
            vt_log(f"OVERSTIM {_vt_display_name(girl)}: pressure capped at {girl.pressure} without orgasm -> she stops him")
            return True
        return False

    # --- Stat-nuanced escalation rework (2026-09-26) ---
    #
    # Replaces the old flat-subtraction-plus-hard-clamp scheme entirely (VT_BOOTH_SEX_COLD_ASK_PENALTY/
    # *_DIFFICULTY_PENALTY/*_COLD_ASK_PENALTY are gone). That scheme was checked, this pass, against a
    # WIDE corruption/affection grid rather than just the handful of high-end profiles the previous
    # passes calibrated against -- it turned out to collapse almost the entire low-to-moderate stat
    # range to the identical 5% floor for every stage past hand-hold (a real base-game acceptance value
    # already hits its own ceiling well before a girl is anywhere near maxed, since each act's floor
    # only spans a narrow window before saturating -- confirmed directly from a real playtest log where
    # Kenzie Reeves' own real handjob acceptance was already a perfect 100 before any mod bonus was even
    # applied), AND collapsed the high end (corruption 80 vs 100) to identical numbers too. A "mid" girl
    # (corruption 40/affection 30) read as barely distinguishable from a total stranger, which is the
    # concrete bug this rework fixes -- see vt_booth_remap_chance/vt_booth_gap_close/
    # vt_booth_stage_chance above for the new mechanism itself.
    #
    # Local-tier floors (seating/hand-hold/thigh) are UNCHANGED from every prior pass -- only how a real
    # acceptance number becomes a final chance changed, not the floors/axis feeding it.
    VT_BOOTH_LOCAL_TIER_FLOORS = {
        "seating":  (5, 3),
        "handhold": (10, 5),
        "thigh":    (15, 8),
    }

    # Per-stage output bands (min_out, max_out) that vt_booth_remap_chance maps her real acceptance
    # into -- first-pass placeholders, same tuning posture as every constant this system has ever had.
    VT_BOOTH_STAGE_BANDS = {
        "seating":  (15, 96),
        "handhold": (8, 92),
        "thigh":    (6, 86),
        "grope":    (5, 80),
        "finger":   (5, 70),
        "handjob":  (5, 58),
        "blowjob":  (5, 46),
    }

    # Grope's existing "she already got past thigh" guaranteed nudge -- was a flat +15, now a
    # gap-closing fraction (vt_booth_gap_close) so it can't dominate a near-zero baseline or blow past
    # grope's own ceiling for an already-high one.
    VT_BOOTH_GROPE_GUARANTEED_FRACTION = 0.30

    # vt_booth_arousal_fraction's per-tier step (0-5 real arousal tiers -> 0%-25% of remaining
    # headroom) and vt_booth_intox_fraction's tipsy/drunk split (same 10%/25% ratio this mod has used
    # since it was first added, now expressed as a fraction of headroom instead of flat points).
    VT_BOOTH_AROUSAL_FRACTION_PER_TIER = 0.05
    VT_BOOTH_TIPSY_INTOX_FRACTION = 0.10
    VT_BOOTH_DRUNK_INTOX_FRACTION = 0.25

    # Width of the sex-gate's "requires coercion" roll band -- see vt_coffeeshop_sex_gate below. A roll
    # this far above her actual chance still gets a negotiation opportunity; further than that is a
    # hard no.
    VT_BOOTH_SEX_PUSH_WINDOW = 20

    # --- Tunable impacts ---

    VT_BOOTH_IMPACTS = {
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
        "hard_reject":     {"affection": (-2000, -1500), "fear": (500, 1000)},
    }

    # Compliment's affection grant now scales with her current affection tier (see
    # vt_booth_affection_tier) instead of a single flat range -- "mid" preserves the original range.
    VT_BOOTH_COMPLIMENT_IMPACTS_BY_TIER = {
        "low":  {"affection": (50, 100)},
        "mid":  {"affection": (150, 300)},
        "high": {"affection": (300, 500)},
    }

    # --- Player-voiced flat line pools (no register -- the player doesn't have one) ---

    VT_BOOTH_INVITE_LINES = [
        "Care to join me for a coffee and a chat in one of the booths? It's quieter over there.",
        "Why don't we grab one of the booths -- more comfortable than standing around out here.",
        "There's a booth free in the back if you'd like to sit and talk for a bit.",
    ]

    # --- Persona-keyed player pools (2026-09-26) -- what kind of guy is asking, from
    # vt_player_persona/vt_player_voice above. Every pool below must define all 5 keys (dominant/
    # compassionate/sexual/transactional/neutral) -- "neutral" carries this pool's original content
    # unchanged, so an untrained player (the common case) reads exactly as before.

    VT_BOOTH_COMPLIMENT_LINES = {
        "dominant": [
            "You know, you're mine to look at right now, and damn, you look good.",
            "I like having you all to myself looking this good.",
            "You look good enough that I don't want anyone else looking at you like this.",
        ],
        "compassionate": [
            "You know, I really do love just looking at you like this.",
            "You look so good -- it makes me happy just sitting here with you.",
            "I mean this -- you look wonderful today.",
        ],
        "sexual": [
            "God, you look good enough to eat right now.",
            "I keep getting distracted looking at you -- you're doing something to me.",
            "Has anyone told you how good that outfit looks on you? Because it's really doing something for me.",
        ],
        "transactional": [
            "You look great -- and I'd say that even if I didn't want something from you.",
            "A compliment like that usually gets me somewhere, right?",
            "You look good today -- good enough that I figure you owe me a smile at least.",
        ],
        "neutral": [
            "You know, you look really good today.",
            "I keep getting distracted looking at you.",
            "Has anyone told you how good that outfit looks on you?",
        ],
    }

    VT_BOOTH_SEX_ASK = {
        "handjob": {
            "dominant": [
                "We're tucked away enough. Get me off, right here, right now.",
                "You know what I want. Get your hand on me, under the table.",
                "I want your hand on me. Now, under the table.",
            ],
            "compassionate": [
                "You know, we're pretty tucked away here. Would you take care of me a little, under the table?",
                "I'd really love it if you helped me out under here, if you're comfortable with that.",
                "This booth's private enough -- would you mind giving me a hand, just between us?",
            ],
            "sexual": [
                "God, I want your hand on me right now. This booth's private enough -- come on.",
                "I can't stop thinking about your hand on me. Get me off under here.",
                "This booth's private enough -- why don't you get that hand working under the table.",
            ],
            "transactional": [
                "This booth's private enough -- help me out under the table, and I'll make it worth your while later.",
                "How about a little discreet fun under the table? I'll owe you one.",
                "You know, we're pretty tucked away here. Take care of me and I'll return the favor.",
            ],
            "neutral": [
                "You know, we're pretty tucked away here. How about a little... discreet fun under the table?",
                "This booth's private enough -- why don't you give me a hand under here?",
                "We're tucked away enough here -- how about you give me a hand under the table?",
            ],
        },
        "blowjob": {
            "dominant": [
                "Get under this table and put that mouth to work. Now.",
                "You know what to do. Get down there and take care of me.",
                "I want your mouth on me. Get under there.",
            ],
            "compassionate": [
                "This booth's nice and private. Would you want to take care of me down there, if you're up for it?",
                "I'd love it if you slipped under and helped me out, only if you want to.",
                "No one can see under this table -- would you mind putting that mouth to use for me?",
            ],
            "sexual": [
                "God, I want your mouth on me right now. This booth's private enough -- come on.",
                "I can't stop thinking about your mouth. Slip under and make it even better.",
                "No one can see under this table -- why don't you get down there and taste me.",
            ],
            "transactional": [
                "This booth's nice and private. Slip under and take care of me, and I'll make it worth it.",
                "No one can see under this table -- put that mouth to use, and I'll owe you one.",
                "How about you slip under and make it even better? I'll return the favor.",
            ],
            "neutral": [
                "This booth's nice and private. How about you slip under and make it even better?",
                "No one can see under this table -- why don't you get down there and put that mouth to use?",
                "This booth's dark enough -- why don't you slip under and take care of me?",
            ],
        },
    }

    VT_BOOTH_PUSH_PITCH = {
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
            "Come on, no one's paying attention to us back here. Just this once.",
            "Nobody's going to notice, I promise. Please?",
            "We're tucked away enough, it'll be fine -- come on.",
        ],
    }

    # --- Variety pass (2026-09-25) -- everything below was previously a single hardcoded literal
    # played identically no matter what. Same flat, non-register shape as the pools above: pure
    # third-person narration and player-voiced lines don't carry a register, only her own spoken
    # reactions do (those are all already register-keyed further down and were confirmed not thin).

    VT_BOOTH_SEAT_DOWN_ACTION_LINES = [
        "You and [selected_girl] slide into the booth, the worn leather creaking slightly under you. The hum of the coffee shop fades into a comfortable background as you settle in.",
        "You and [selected_girl] settle into the booth together, the noise of the shop fading as the leather seat gives slightly under you both.",
        "You slide into the booth with [selected_girl], the espresso machine's hiss and the low murmur of other patrons fading into the background.",
    ]

    VT_BOOTH_SEAT_SPONTANEOUS_ACTION_LINES = [
        "Without waiting for an invitation, she slides in right beside you, her leg brushing yours under the table.",
        "She doesn't hesitate, settling in right next to you, close enough that her shoulder presses against yours.",
        "She slides into the seat beside you without a second thought, her knee bumping yours as she gets comfortable.",
    ]

    VT_BOOTH_SEAT_MOVE_AWAY_ACTION_LINES = [
        "She shrugs and slides back across to the other side.",
        "She scoots back out and settles into the seat across from you instead.",
        "She gets up briefly, then settles into the seat opposite you.",
    ]

    VT_BOOTH_SEAT_ACROSS_ACTION_LINES = [
        "She settles into the seat across from you instead, folding her hands around her mug.",
        "She takes the seat across from you, wrapping both hands around her mug.",
        "She slides into the opposite seat, keeping the table between you.",
    ]

    VT_BOOTH_SEAT_ASK_LINES = {
        "dominant": [
            "Come sit over here, next to me.",
            "Get over here and sit beside me.",
            "I want you sitting right here, not way over there.",
        ],
        "compassionate": [
            "Come sit over here with me, it's cozier.",
            "Why don't you come sit next to me? I'd like that.",
            "There's room right here beside me, if you'd like to be close.",
        ],
        "sexual": [
            "Come sit closer to me, I want you where I can touch you.",
            "Why don't you scoot in here, next to me, where it's warmer.",
            "There's room right here beside me -- come get comfortable.",
        ],
        "transactional": [
            "Come sit over here with me -- it'll be worth your while.",
            "Why don't you come sit closer? I'll make it interesting.",
            "There's room right here beside me, if you play along.",
        ],
        "neutral": [
            "Come sit over here with me, it's cozier.",
            "Why don't you come sit next to me instead?",
            "There's room right here beside me, if you'd rather.",
        ],
    }

    # New utility pool (2026-09-26) -- the reverse "downgrade" ask, "would you mind sitting across
    # instead", was previously a single hardcoded literal with zero variety at all. Flat, not
    # persona-keyed -- a low-stakes housekeeping ask with no real coercive/romantic charge, matching
    # this file's own convention for zero-stakes utility lines (e.g. VT_BOOTH_TOUCH_STOP_ACTION_LINES).
    VT_BOOTH_SEAT_ACROSS_ASK_LINES = [
        "Actually, would you mind sitting across from me instead?",
        "Actually, could you sit across from me instead? Just for a bit.",
        "On second thought, would you mind moving over there instead?",
    ]

    VT_BOOTH_SEAT_ASK_YES_ACTION_LINES = [
        "She hesitates, then slides around to sit pressed against your side.",
        "She hesitates a moment, then gets up and slides in right beside you.",
    ]

    VT_BOOTH_HANDHOLD_SAMESIDE_LINES = {
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

    VT_BOOTH_HANDHOLD_ACROSS_LINES = {
        "dominant": [
            "You reach across the table and take her hand, holding it firmly.",
            "You reach over the table and take her hand without waiting for permission.",
            "You reach across the table, closing your hand around hers.",
        ],
        "compassionate": [
            "You reach across the table and take her hand gently.",
            "You reach over the table, fingers closing softly around hers.",
            "You reach across and take her hand, giving it a warm squeeze.",
        ],
        "sexual": [
            "You reach across the table and take her hand, tracing your thumb over her knuckles.",
            "You reach over the table, letting your fingers slide slowly around hers.",
            "You reach across and take her hand, unable to help lingering there.",
        ],
        "transactional": [
            "You reach across the table and take her hand, an easy, practiced move.",
            "You reach over the table, taking her hand like it's the natural next step.",
            "You reach across and take her hand, curious how far tonight goes.",
        ],
        "neutral": [
            "You reach across the table and take her hand.",
            "You reach over the table, fingers closing gently around hers.",
            "You reach across the table and take her hand in yours.",
        ],
    }

    VT_BOOTH_THIGH_ASK_LINES = {
        "dominant": [
            "You rest a hand on her thigh under the table, claiming your spot without asking.",
            "You slide a hand onto her thigh, gripping it like you own the right to.",
            "Under the table, you plant a hand firmly on her thigh and let it stay there.",
        ],
        "compassionate": [
            "You rest a gentle hand on her thigh under the table, giving it a light, affectionate squeeze.",
            "You slide your hand onto her thigh, resting it there warmly, careful and unhurried.",
            "Under the table, you let your hand settle on her thigh, thumb tracing slow, soft circles.",
        ],
        "sexual": [
            "You slide a hand onto her thigh under the table, fingers already inching hungrily upward.",
            "You rest a hand high on her thigh, unable to resist letting it creep further under the table.",
            "Under the table, your hand finds her thigh and drags slowly higher, greedy for more.",
        ],
        "transactional": [
            "You rest a hand on her thigh under the table, testing how far she'll let this go.",
            "You slide a hand onto her thigh, treating it as fair game now that you're this close.",
            "Under the table, you let your hand settle on her thigh, seeing what you can get away with.",
        ],
        "neutral": [
            "You rest a hand on her thigh, sliding it slowly upward under the table.",
            "You slide a hand onto her thigh under the table, fingers trailing slowly upward.",
            "Under the table, you let your hand settle on her thigh and inch it higher.",
        ],
    }

    # Shared across all 3 overstim-stop call sites (grope-continue, grope-first-success, and inside
    # the touch-technique loop) -- the same physical beat every time, one pool rather than three.
    VT_BOOTH_OVERSTIM_ACTION_LINES = [
        "She grabs your wrist, pushing your hand away, breathing hard.",
        "She catches your wrist and pushes your hand back, chest heaving.",
        "She clamps a hand over yours, stopping you, breathing hard.",
    ]

    VT_BOOTH_SEX_OVERSTIM_ACTION_LINES = {
        "handjob": [
            "She draws her hand away and leans back, breathing hard.",
            "She stops touching you and sits back, visibly tense.",
        ],
        "blowjob": [
            "She comes out from beneath the table and leans away, breathing hard.",
            "She returns to her seat and holds up a hand to stop any further contact.",
        ],
    }

    VT_BOOTH_TOUCH_STOP_ACTION_LINES = [
        "You ease your hand back, giving her a moment to catch her breath.",
        "You slowly withdraw your hand, letting her catch her breath.",
    ]

    VT_BOOTH_DECLINE_ACTION_LINES = [
        "She shifts uncomfortably, her eyes darting away as she clutches her mug a little tighter.",
        "She shifts in her seat, avoiding your eyes as she wraps both hands around her mug.",
        "She keeps her place and turns her attention back to the room.",
    ]

    # Shown only when the visit ends normally (not after a hard reject or a failed push, both of
    # which set _vt_booth_sour_ending -- a calm, polite goodbye previously played even after "she
    # storms out" a line above it, a real contradiction fixed alongside this variety pass).
    VT_BOOTH_VISIT_END_ACTION_LINES = [
        "You finish your coffee and give her room to get up. She gathers her things, says goodbye, and leaves the coffee shop.",
        "As you finish your coffee, she gathers her things and slides out of the booth. She gives you a parting nod before leaving the coffee shop.",
        "After a final sip, she says goodbye, collects her things, and makes her way out of the coffee shop.",
    ]

    # Sex-gate action narration, act-keyed (same {"handjob": [...], "blowjob": [...]} shape as
    # VT_BOOTH_SEX_ASK above). IMMEDIATE/FINISH/HELDBACK cover the >=40 immediate-accept path; the
    # _PUSH variants cover the push-success path and read more reluctant, matching that path's already
    # register-varied VT_BOOTH_PUSH_SUCCESS tone.
    VT_BOOTH_SEX_ACTION_IMMEDIATE = {
        "handjob": [
            "She glances around, then slips her hand beneath the table, her fingers brushing your thigh before finding their target. The booth hides her movements as she works you with a steady, teasing grip.",
            "She checks that no one's watching, then slides her hand under the table and along your leg until she finds you, working you with a slow, deliberate grip.",
        ],
        "blowjob": [
            "She checks the aisle before slipping beneath the table. Her hand rests briefly on your knee, a quiet reminder to keep still.",
            "She waits for a gap in the conversation nearby, then moves beneath the table. You draw a slow breath and try to look as though nothing has changed.",
        ],
    }

    VT_BOOTH_SEX_FINISH_LINES = {
        "handjob": [
            "After you finish, she draws her hand away and settles back into her seat.",
            "She withdraws her hand as you catch your breath. For a moment, the clink of cups nearby seems much louder.",
        ],
        "blowjob": [
            "After you finish, she comes out from beneath the table and settles into her seat.",
            "As your breathing steadies, she returns to her seat and smooths the front of her outfit.",
        ],
    }

    VT_BOOTH_SEX_HELDBACK_LINES = {
        "handjob": [
            "You stop before finishing and let go of her wrist. She draws her hand away.",
            "You still her hand before you finish. She settles back into her seat, leaving the rest of the moment between you.",
        ],
        "blowjob": [
            "You stop before finishing. She comes out from beneath the table and returns to her seat.",
            "You ease back before you finish, giving her room to return to her seat.",
        ],
    }

    VT_BOOTH_SEX_ACTION_PUSH = {
        "handjob": [
            "She glances around one more time, then reluctantly slips her hand beneath the table.",
            "She takes one more look around, then reluctantly lets her hand drift under the table.",
        ],
        "blowjob": [
            "She hesitates, then ducks under the table, clearly less enthusiastic than a moment ago.",
            "She hesitates a beat longer, then slips under the table with far less enthusiasm than before.",
        ],
    }

    VT_BOOTH_SEX_FINISH_PUSH_LINES = {
        "handjob": [
            "After you finish, she draws her hand away in silence.",
            "You catch your breath after your release while she settles back into her seat.",
        ],
        "blowjob": [
            "After you finish, she comes out from beneath the table and sits back in silence.",
            "You catch your breath after your release as she returns to her seat.",
        ],
    }

    VT_BOOTH_SEX_HELDBACK_PUSH_LINES = {
        "handjob": [
            "You stop before finishing. She withdraws her hand, visibly relieved to have a break.",
            "You still her hand before you finish and let her settle back into her seat.",
        ],
        "blowjob": [
            "You stop before finishing. She returns to her seat, visibly relieved to have a break.",
            "You ease back before you finish, giving her room to come out from beneath the table.",
        ],
    }

    VT_BOOTH_PUSH_FAIL_ACTION_LINES = [
        "She draws back with a hurt frown, gathers her things, and slides out of the booth. She leaves the coffee shop without looking back.",
        "She shakes her head and takes a moment to collect herself. Then she gathers her things and leaves the coffee shop, ending the conversation.",
        "She stands, gathers her things, and leaves the coffee shop before you can say anything else.",
    ]

    VT_BOOTH_HARD_REJECT_ACTION_LINES = [
        "She shoves her drink aside and gets out of the booth, drawing a few glances. Gathering her things with a tense expression, she leaves the coffee shop.",
        "She pulls away, visibly upset, and gathers her things. She slides out of the booth and heads straight out of the coffee shop.",
        "She takes her things and walks out of the coffee shop, leaving you alone at the table.",
    ]

    # Flat, non-register access-narration (pure third-person setup text, matching the thigh caress's
    # own unvaried setup line) for the two new touch-escalation steps, keyed by
    # vt_booth_lower_access_style. "dress" covers both a worn dress and a skirt (same "reach up
    # underneath" framing); "pants" covers jeans/leggings/shorts.
    VT_BOOTH_GROPE_ACCESS_LINES = {
        "dress": [
            "You slide your hand up along her thigh and beneath her hem, walking your fingers higher.",
            "You slip your hand up beneath her hem, palm sliding slowly up the inside of her thigh.",
        ],
        "pants": [
            "You press your hand between her thighs, feeling the fabric of her pants give slightly as you push against her.",
            "You cup your hand between her legs, the fabric doing little to hide how she reacts to the pressure.",
        ],
        "bare": [
            "With nothing in the way, you slide your hand straight between her thighs.",
            "There's nothing to work around -- you slide your hand right between her legs.",
        ],
        "generic": [
            "You slide your hand between her thighs, searching out just where she wants to be touched.",
            "You work your hand between her legs, feeling her tense slightly at the contact.",
        ],
    }

    # Used instead of VT_BOOTH_GROPE_ACCESS_LINES once grope has already succeeded once this visit --
    # same reasoning as the touch-technique transition lines: her clothing is no longer relevant to
    # the narration once the player's hand is already there, only the fact that he's continuing.
    VT_BOOTH_GROPE_CONTINUE_LINES = [
        "You keep groping her, feeling her squirm under your hand.",
        "You keep rubbing her under the table, unhurried.",
    ]

    # Three distinct bare-touch techniques offered once grope has succeeded (variety fix -- reusing
    # THREE separate real generic actions, each with their own base-game description/reaction pools,
    # rather than one action's 2-line pool repeating every attempt). "clit" -> generic_action_tease_clit
    # (a real, already-shipped base-game action -- confirmed via research, arousal 11/pressure 16
    # nominal, between grope_pussy's 8/10 and finger_pussy's 18/27). "finger"/"two_fingers" both call
    # generic_action_finger_pussy mechanically (no distinct base-game DB entry exists for a two-finger
    # variant) -- the escalation between them is narrative/access-line only, not a numeric difference.
    VT_BOOTH_TOUCH_ACCESS_LINES = {
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

    # Once a technique has already been picked once this foreplay session, her clothing is no longer
    # relevant to the narration -- the player's hand is already there. Keyed by (last_technique,
    # this_technique): the 3 same-technique pairs read as "keep doing it" continuity; the 6
    # different-technique pairs describe the specific transition (escalating: clit->finger->
    # two_fingers; de-escalating/lateral: the reverse). VT_BOOTH_TOUCH_ACCESS_LINES above is used only
    # for the FIRST pick after freshly entering the foreplay loop (vt_booth_touch_last_technique is
    # None then); this dict is used for every pick after that.
    VT_BOOTH_TOUCH_TRANSITION_LINES = {
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

    # --- Register-keyed reaction lines ---

    VT_BOOTH_ACCEPT = {
        "crude":    ["Fuck yeah, I could go for a coffee.", "Sure, let's go sit our asses down.", "Hell yes, lead the way."],
        "explicit": ["Mmm, sounds perfect. Let's go sit.", "Oh, I'd love that. Let's go.", "Yes -- I could really use a sit-down."],
        "direct":   ["Sure, that sounds nice. Let's sit.", "Sounds good. Let's grab that booth.", "Alright, sounds nice. Let's go."],
        "neutral":  ["Sure, that sounds nice.", "Okay, sounds good to me.", "Sure, I'd like that."],
        "shy":      ["O-oh, sure, that sounds nice...", "Um, okay, I'd like that...", "S-sure, I guess that'd be nice."],
        "demure":   ["That sounds lovely, thank you.", "I would enjoy that, yes.", "Certainly, that sounds pleasant."],
    }

    VT_BOOTH_DECLINE = {
        "crude":    ["No thanks, I'm good right here.", "Nah, I'll pass on that.", "Not really feeling it, I'll stay put."],
        "explicit": ["No thanks... I'm fine right here.", "I'd rather just stay here, sorry.", "Mmh, not right now -- I'll stay here."],
        "direct":   ["No thanks, I'm fine right here.", "I'll pass -- I'm comfortable here.", "No, I think I'll stay right here."],
        "neutral":  ["No thanks... I'm fine right here.", "I think I'll just stay here.", "No, I'm alright where I am."],
        "shy":      ["N-no thanks... I'm fine here...", "I-I'd rather stay here, sorry...", "Um... m-maybe another time..."],
        "demure":   ["No, thank you. I am fine right here.", "I would prefer to remain here, thank you.", "That is kind, but I must decline."],
    }

    VT_BOOTH_SEAT_TOGETHER = {
        "crude":    ["Move over, I'm sitting right next to you.", "Scoot in, I'm not sitting way over there.", "I'm parking myself right next to you, budge up."],
        "explicit": ["Mmm, I want to sit close to you.", "I'd rather sit right beside you.", "Mmm, I'll just squeeze in right beside you."],
        "direct":   ["I'll sit next to you, if that's alright.", "I'll just sit here beside you.", "I'd rather sit beside you, if you don't mind."],
        "neutral":  ["I'll sit next to you.", "I'll just sit here beside you, is that okay?", "I think I'll sit right beside you."],
        "shy":      ["I-is it okay if I sit next to you...?", "C-can I just sit here, beside you...?", "U-um, is it alright if I sit close...?"],
        "demure":   ["I would prefer to sit beside you, if you don't mind.", "Might I sit next to you instead?", "I believe I shall sit beside you, if that suits."],
    }

    VT_BOOTH_SEAT_ACROSS = {
        "crude":    ["I'll sit over here, where I can see you.", "I'm taking this side, thanks.", "I'll just park myself over here."],
        "explicit": ["I'll just sit across from you.", "I'll take this side, if that's fine.", "Mmm, I'll sit here across from you."],
        "direct":   ["I'll sit across from you.", "I'll take this seat, across from you.", "I think I'll sit over here instead."],
        "neutral":  ["I'll sit over here.", "I'll take this side.", "I think I'll sit across from you."],
        "shy":      ["I-I'll just sit over here...", "U-um, I'll sit across, if that's okay...", "I-I think I'll sit over here instead..."],
        "demure":   ["I shall sit across from you.", "I will take this seat, if you don't mind.", "I believe I shall take the seat across."],
    }

    VT_BOOTH_SEAT_ASK_YES = {
        "crude":    ["Fine, scooting my ass over there.", "Ugh, fine -- budge up.", "Alright, alright -- moving."],
        "explicit": ["Mmh, alright... budge over then.", "Okay... I'll come sit with you.", "Mmh, fine -- scoot over for me."],
        "direct":   ["Alright, I'll come sit next to you.", "Okay, fine -- I'll move over.", "Alright, I'll come sit beside you then."],
        "neutral":  ["Okay, I'll come sit next to you.", "Alright, I'll move over.", "Okay, I'll come sit beside you."],
        "shy":      ["O-okay... I'll come sit next to you...", "Um, okay... if you want me to...", "O-okay, if that's what you want..."],
        "demure":   ["Very well, I shall sit beside you.", "If you wish it, I will move over.", "Very well, I shall join you there."],
    }

    VT_BOOTH_SEAT_ASK_NO = {
        "crude":    ["Nah, I'm good right here.", "No way, I'm staying put.", "Nope, not moving."],
        "explicit": ["No, I'd rather stay right here.", "I'll just stay over here, thanks.", "Mmh, no -- I'll stay right here."],
        "direct":   ["No, I'll stay here.", "I'd rather stay across from you.", "No, I think I'll stay put."],
        "neutral":  ["No, I'll just stay here.", "I think I'll stay right here.", "No, I'll stay where I am."],
        "shy":      ["N-no, I'll just stay here...", "I-I'd rather stay over here...", "S-sorry, I'll just stay here..."],
        "demure":   ["No, I shall remain here, thank you.", "I would prefer to stay right here.", "No, I believe I shall remain here."],
    }

    # A "downgrade" ask (move to the LESS intimate seat) -- always succeeds, no roll, so this is a
    # simple, agreeable compliance line, not a real negotiation.
    VT_BOOTH_SEAT_MOVE_AWAY = {
        "crude":    ["Eh, whatever.", "Sure, no big deal.", "Fine by me."],
        "explicit": ["Oh, okay, sure.", "Mmh, alright then.", "Mmm, sure, whatever you'd like."],
        "direct":   ["Sure, no problem.", "Okay, that's fine.", "Sure, that works."],
        "neutral":  ["Oh, okay, sure.", "Sure, that's fine.", "Okay, no problem."],
        "shy":      ["Oh -- okay...", "U-um, sure...", "O-okay, if you'd like..."],
        "demure":   ["Very well, if you prefer.", "Of course, as you wish.", "Certainly, if that is your preference."],
    }

    # Tiered by her current affection band (vt_booth_affection_tier) -- "mid" is the original content,
    # unchanged; "low"/"high" are new, cooler/warmer variants so the reaction reads as commensurate
    # with where she actually stands, not uniformly enthusiastic regardless of her stats.
    VT_BOOTH_COMPLIMENT_REACT = {
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
            "neutral":  ["That means a lot, thank you.", "You really know how to make me smile.", "You really know how to make my day."],
            "shy":      ["Th-thank you, that means so much...", "You really mean that? Thank you...", "I... I really needed to hear that..."],
            "demure":   ["You are far too kind to me.", "That means more to me than you know.", "You have such a gift for kind words."],
        },
    }

    VT_BOOTH_HANDHOLD_ACCEPT = {
        "crude":    ["Getting handsy already, huh?", "Ha, cute. I'll allow it.", "Ha, look at you, all sweet on me."],
        "explicit": ["Mmm, I like that.", "I don't mind that at all.", "Mmm, I could get used to this."],
        "direct":   ["That's nice, actually.", "I don't mind this.", "That's actually pretty nice."],
        "neutral":  ["That's nice.", "I like that.", "That's sweet, actually."],
        "shy":      ["Th-that's... nice...", "O-oh... okay...", "Th-that's kind of nice, actually..."],
        "demure":   ["That is rather sweet.", "I don't mind this at all.", "That is quite a sweet gesture."],
    }

    VT_BOOTH_HANDHOLD_REJECT = {
        "crude":    ["Not that comfortable yet, slow down.", "Easy there, not yet.", "Hold up, not there yet."],
        "explicit": ["Mmh, not yet... let's slow down a bit.", "I'm not quite there yet, sorry.", "Mmh, give me a little more time first."],
        "direct":   ["I'm not ready for that yet.", "Let's slow down a little.", "I'd rather wait a bit on that."],
        "neutral":  ["I'm not sure about that yet.", "Let's take it slow, okay?", "Let's not rush into that yet."],
        "shy":      ["I-I'm not ready for that yet...", "C-can we slow down a little...?", "I-I need a bit more time first..."],
        "demure":   ["I am not yet comfortable with that.", "Let us proceed a bit more slowly, please.", "I would prefer we take our time."],
    }

    VT_BOOTH_THIGH_REACT = {
        "crude":    ["Mmh, someone's bold today.", "Getting handsy under here already?", "Ha, someone's feeling brave."],
        "explicit": ["Mmm... careful, someone might notice.", "Ah -- keep that up and I won't be able to sit still.", "Mmm, you're playing with fire here."],
        "direct":   ["Someone might notice, you know.", "You're being pretty bold right now.", "You're being pretty daring right now."],
        "neutral":  ["Careful, someone might see.", "You're being pretty forward.", "You're being pretty bold."],
        "shy":      ["W-wait, someone might see us...!", "Um -- s-someone could notice...", "O-oh! Someone could walk by...!"],
        "demure":   ["You are being quite forward, aren't you.", "Someone may well notice, you realize.", "You are being rather bold, aren't you."],
    }

    VT_BOOTH_THIGH_REJECT = {
        "crude":    ["Not there, not yet.", "Whoa, slow down.", "Nuh-uh, not yet."],
        "explicit": ["Mmh, not yet... slow down.", "Wait, not there, not yet.", "Mmh, hold on -- not there yet."],
        "direct":   ["Not yet, let's slow down.", "Not there, please.", "Not there yet, if you don't mind."],
        "neutral":  ["Not yet, let's slow down.", "Please, not there yet.", "Let's not go there just yet."],
        "shy":      ["N-not yet, please...", "W-wait, not there...", "P-please, not there yet..."],
        "demure":   ["Not yet, if you please.", "I am not ready for that yet.", "I must ask you to wait on that."],
    }

    # Accept side is a lexicon-enrichment candidate (crude/explicit/direct/neutral only -- their
    # noun_pussy pools all support a plain possessive "my ___" construction; shy/demure stay
    # token-free since their pool value "down there" doesn't parse as a possessive noun the same way).
    VT_BOOTH_GROPE_ACCEPT = {
        "crude":    ["Mmh, fuck it, go ahead.", "Ha, bold. Fine, keep going.", "Go ahead, touch my %noun_pussy%."],
        "explicit": ["Mmm... okay, don't stop.", "Ohh -- fine, keep going.", "Mmm, go ahead, touch my %noun_pussy%."],
        "direct":   ["Okay... go ahead.", "Alright, that's fine.", "Alright, touch my %noun_pussy% then."],
        "neutral":  ["Okay... that's fine.", "Alright, go ahead.", "Alright, you can touch my %noun_pussy%."],
        "shy":      ["O-okay... that's... fine...", "Um... okay, go ahead...", "Um... you can... touch me there..."],
        "demure":   ["Very well, you may continue.", "That is... acceptable, go on.", "Very well, you may touch me there."],
    }

    VT_BOOTH_GROPE_REJECT = {
        "crude":    ["Whoa, not here. Slow down.", "Easy, not that far.", "Hold up, not that far, not here."],
        "explicit": ["Mmh, not yet -- that's too far here.", "Wait, not that, not here.", "Mmh, not that far, not here."],
        "direct":   ["Not here, that's too far.", "Let's not go that far right now.", "Not that far, not here."],
        "neutral":  ["Not here, that's too much.", "Let's not go that far.", "That's too much, not here."],
        "shy":      ["W-wait, that's too far...", "N-not here, please...", "P-please, not that far..."],
        "demure":   ["That is too forward, not here.", "I must ask you not to go that far.", "That is too much, not here."],
    }

    # Her reaction to the new "Touch her bare" gate (2026-09-25) -- previously this step had no
    # acceptance check at all.
    VT_BOOTH_FINGER_ACCEPT = {
        "crude":    ["Fuck, fine -- touch me then.", "Mmh, go on then, touch it.", "Fuck, go on, touch my %noun_pussy%."],
        "explicit": ["Mmm... okay, go ahead, touch me.", "Ohh -- yes, go on.", "Mmm, go ahead, touch my %noun_pussy%."],
        "direct":   ["Okay... go ahead.", "Alright, you can touch me.", "Alright, go ahead and touch my %noun_pussy%."],
        "neutral":  ["Okay... that's fine.", "Alright, go ahead.", "Alright, you can touch my %noun_pussy%."],
        "shy":      ["O-okay... you can... touch me...", "Um... alright, go ahead...", "Um... okay, you can... touch me there..."],
        "demure":   ["Very well, you may touch me there.", "That is... acceptable, go on.", "Very well, you may touch me there directly."],
    }

    VT_BOOTH_FINGER_REJECT = {
        "crude":    ["Whoa, hold up -- not that far.", "Easy, that's too much here.", "Hold up, that's too much right now."],
        "explicit": ["Mmh, not that -- not here.", "Wait, that's too far here.", "Mmh, not that far, not right now."],
        "direct":   ["Not here, that's too far.", "Let's not go that far right now.", "That's too far, not right now."],
        "neutral":  ["Not here, that's too much.", "Let's not go that far.", "That's too much, not right now."],
        "shy":      ["W-wait, that's too far...", "N-not here, please...", "P-please, not that far right now..."],
        "demure":   ["That is too forward, not here.", "I must ask you not to go that far.", "That is too much, not right now."],
    }

    VT_BOOTH_TOUCH_ACCEPT = {
        "crude":    ["Fuck, yes -- don't stop.", "Mmh, fuck, right there.", "Fuck, keep touching me just like that."],
        "explicit": ["Mmm, yes... just like that.", "Ohh... don't stop, please.", "Mmm, don't stop touching my %noun_pussy%."],
        "direct":   ["Okay... don't stop.", "Yes, keep going.", "Don't stop, that's really good."],
        "neutral":  ["Okay... keep going.", "That's... good, don't stop.", "Don't stop, that feels really good."],
        "shy":      ["O-oh... don't stop...", "Um... th-that feels... good...", "O-oh, please... don't stop..."],
        "demure":   ["Please... do continue.", "That is... quite alright, don't stop.", "Please, do not stop now."],
    }

    # Her own reaction at the moment she actually climaxes from grope/tease_clit/finger_pussy. Shown
    # in place of the base game's own orgasm-reaction line (generic_actions_misc.rpy's
    # generic_action_orgasm), which we now suppress via skip_descriptions=True at every touch call
    # site (see file header) -- that flag silences the repetitive in-progress lines but also silences
    # the real climax narration as a side effect, so this replaces it rather than just losing it.
    VT_BOOTH_GIRL_ORGASM = {
        "crude":    ["Oh fuck, I'm cumming!", "Fuck, fuck, I'm cumming!", "Fuck, right there, I'm cumming!"],
        "explicit": ["Ohh god, yes... I'm coming...", "Mmm, yes, I'm coming...", "Ohh, yes, right there, I'm coming..."],
        "direct":   ["Oh -- I'm coming.", "Yes... I'm coming.", "Oh god, I'm coming."],
        "neutral":  ["Oh -- I'm coming!", "I'm coming, don't stop!", "Oh -- I'm coming, right there!"],
        "shy":      ["O-oh! I'm... I'm coming...!", "I-I'm coming...!", "O-oh! I'm gonna... I'm coming...!"],
        "demure":   ["Oh! I am... I am finishing...!", "Oh my -- I am coming...!", "Oh! I am about to finish...!"],
    }

    VT_BOOTH_OVERSTIM_STOP = {
        "crude":    ["Fuck, stop -- that's too much, I can't take any more.", "Enough! Stop, I mean it, I can't take it.", "Fuck, I said stop, I'm done."],
        "explicit": ["Mmh, stop -- please, I can't take any more like this.", "Wait, stop... it's too much, I need a moment.", "Mmh, please, I really need to stop now."],
        "direct":   ["Stop, please -- that's too much right now.", "Please stop, I can't take any more of that.", "Stop, please, I really need a break."],
        "neutral":  ["Please stop, that's too much.", "Stop, please -- I need a moment.", "Please stop, I need a break."],
        "shy":      ["P-please stop... it's too much...", "I-I can't take any more, please stop...", "P-please, I really need to stop..."],
        "demure":   ["Please, you must stop -- it is too much.", "I must ask you to stop, it is too much.", "Please, I must ask you to stop now."],
    }

    # Third variant on every cell weaves in %noun_penis% -- the crude/explicit/direct/neutral registers
    # all support a plain possessive "that ___"/"your ___" construction for every value their pool can
    # resolve to; shy/demure's shared pool ("thing"/"part" at low intellect, "penis" at high) still
    # reads fine possessively ("take care of your thing"/"attend to your penis"), so those get the
    # token too here (unlike noun_pussy's "down there", which breaks that same construction).
    VT_BOOTH_SEX_ACCEPT = {
        "handjob": {
            "crude":    ["Oh, you're bold. Alright, let's see what I can do.", "Fuck it, get over here and let me feel that.", "Fuck it, get that %noun_penis% out then."],
            "explicit": ["Mmm, alright... hold still.", "Ohh, okay... let me take care of you.", "Mmm, let me feel that %noun_penis% in my hand."],
            "direct":   ["Alright, I can do that.", "Okay, I'll take care of that.", "Alright, let me take care of that %noun_penis%."],
            "neutral":  ["Okay, I can do that.", "Alright, I'll help you out.", "Okay, let me take care of that %noun_penis%."],
            "shy":      ["O-okay... I'll try...", "Um... alright, I guess...", "Um... okay, I'll take care of your %noun_penis%..."],
            "demure":   ["Very well, I shall attend to that.", "If you insist, I will help.", "Very well, I shall attend to your %noun_penis%."],
        },
        "blowjob": {
            "crude":    ["Risky, but I'm game. Hold onto your coffee.", "Fuck it, get that %noun_penis% out then.", "Fuck it, whip that %noun_penis% out already."],
            "explicit": ["Mmm, alright... hold still for me.", "Ohh, okay... let me taste you.", "Mmm, let me put my mouth on that %noun_penis%."],
            "direct":   ["Alright, I can do that.", "Okay, I'll take care of you.", "Alright, let me take care of that %noun_penis%."],
            "neutral":  ["Okay, I can do that.", "Alright, I'll take care of it.", "Okay, let me take care of that %noun_penis%."],
            "shy":      ["O-okay... I'll try my best...", "Um... alright, I guess I can...", "Um... I'll take care of your %noun_penis%..."],
            "demure":   ["Very well, I shall attend to you.", "If you insist, I will oblige.", "Very well, I shall attend to your %noun_penis%."],
        },
    }

    VT_BOOTH_SEX_INTERJECT = {
        "crude":    ["Whoa, hold up -- right here? Someone could see.", "Careful, someone's gonna notice.", "Whoa, hang on -- right here, seriously?"],
        "explicit": ["Ah -- wait, right here? Someone might see us...", "Mmh, hold on -- this is risky.", "Ah, wait -- right here, of all places?"],
        "direct":   ["Wait -- right here? Someone might notice.", "Hold on, that's pretty risky here.", "Wait -- are you sure, right here?"],
        "neutral":  ["Wait, here? Someone might see us.", "Hold on, isn't that risky here?", "Wait, right here? That seems risky."],
        "shy":      ["W-wait, here...? Someone might see...", "Um, s-someone could notice...", "W-wait, right here...? Are you sure...?"],
        "demure":   ["Wait -- here? Someone may well notice.", "That seems rather risky, here of all places.", "Wait -- are you certain, here of all places?"],
    }

    # Menu captions -- flagged as the hardest cell to write a genuinely non-redundant 3rd variant for
    # (they must stay caption-length, not turn into prose). Follows 03_vt_pullout_coercion.rpy's own
    # VT_PULLOUT_MENU_PUSH_CAPTION/RESPECT_CAPTION template for this exact problem: keep a short,
    # register-neutral base phrasing as the first entry, then vary the SECOND/THIRD entries.
    VT_BOOTH_MENU_PUSH_CAPTION = {
        "crude":    ["Push her -- no one will notice", "Talk her into it anyway", "Push her, she'll get over it"],
        "explicit": ["Convince her to go for it", "Push a little", "Try to talk her into it"],
        "direct":   ["Push her to go along with it", "Try to convince her", "Ask her again anyway"],
        "neutral":  ["Push her a little", "Try to convince her", "Ask her again"],
        "shy":      ["Gently push her", "Try to convince her", "Softly ask again"],
        "demure":   ["Press the matter", "Try to persuade her", "Politely ask again"],
    }

    VT_BOOTH_MENU_RESPECT_CAPTION = {
        "crude":    ["Fine, drop it", "Let it go", "Nah, forget it"],
        "explicit": ["Respect her -- let it go", "Back off", "Let it drop"],
        "direct":   ["Respect her wishes", "Let it go", "Drop it for now"],
        "neutral":  ["Respect her wishes", "Let it go", "Leave it be"],
        "shy":      ["Respect her wishes", "Let it go", "Gently let it go"],
        "demure":   ["Respect her wishes", "Let the matter go", "Graciously let it go"],
    }

    VT_BOOTH_PUSH_SUCCESS = {
        "crude":    ["Ugh, fine -- but you owe me.", "Fuck it, fine. Let's be quick about it.", "Ugh, fine, just don't drag it out."],
        "explicit": ["Mmh... okay, fine. Just be quick.", "Alright... fine, just this once.", "Mmh, alright, but hurry."],
        "direct":   ["Fine, but let's be quick.", "Alright, fine -- just this once.", "Fine, but let's not linger on it."],
        "neutral":  ["Okay, fine. Just be quick.", "Alright, just this once.", "Okay, fine -- but quickly."],
        "shy":      ["O-okay... just be quick, please...", "F-fine... just this once...", "O-okay... let's hurry, please..."],
        "demure":   ["Very well, but let us be quick.", "Fine -- but only this once.", "Very well, but let us not delay."],
    }

    VT_BOOTH_PUSH_FAIL = {
        "crude":    ["No! I said not here, drop it. I'm leaving.", "Are you deaf? I said no. I'm leaving.", "No means no, drop it already. I'm leaving."],
        "explicit": ["No -- I mean it, not here. I'm leaving.", "I said no, please stop pushing. I'm leaving.", "No -- I really do mean it. I'm leaving."],
        "direct":   ["No, I meant it -- not here. I'm leaving.", "I said no. Please respect that. I'm leaving.", "No, and I need you to hear that. I'm leaving."],
        "neutral":  ["No, I meant it. Not here. I'm leaving.", "I said no, please stop. I'm leaving.", "No, I really do mean that. I'm leaving."],
        "shy":      ["N-no... I said no... please stop... I need to leave...", "P-please, I meant it, not here... I need to go...", "N-no, please... I mean it... I'm leaving..."],
        "demure":   ["No. I meant what I said. I am leaving.", "I must insist -- the answer is no. I am leaving.", "No. I must ask you to respect that. I am leaving."],
    }

    VT_BOOTH_RESPECT = {
        "crude":    ["Thanks for backing off.", "Appreciate you not pushing it.", "Good, glad you dropped it."],
        "explicit": ["Thank you for respecting that.", "Thanks for not pushing.", "Thank you, that means something to me."],
        "direct":   ["Thank you for respecting that.", "I appreciate you backing off.", "Thank you for hearing me on that."],
        "neutral":  ["Thank you for understanding.", "Thanks for respecting that.", "Thank you for listening to me."],
        "shy":      ["Th-thank you... for not pushing...", "I... appreciate that, thank you...", "Th-thank you, for understanding..."],
        "demure":   ["Thank you for your consideration.", "I appreciate your restraint.", "Thank you for honoring my wishes."],
    }

    VT_BOOTH_HARD_REJECT = {
        "crude":    ["Are you insane? That's disgusting. I'm out of here!", "You're fucking revolting! I'm gone!", "What the fuck is wrong with you? I'm leaving!"],
        "explicit": ["Are you serious? I'm leaving!", "You're unbelievable. I'm out of here!", "I can't believe you just said that. I'm gone!"],
        "direct":   ["That's out of line. I'm leaving.", "Absolutely not. I'm done here.", "That crossed a line. I'm leaving."],
        "neutral":  ["That's way too much. I'm leaving.", "No way. I'm done here.", "That's too far. I'm leaving."],
        "shy":      ["Th-that upset me... I need to leave...!", "Th-that's too much, I'm leaving...!", "I-I can't believe you said that...!"],
        "demure":   ["That is entirely inappropriate. I am leaving.", "I will not tolerate that. Goodbye.", "That is quite unacceptable. I am leaving."],
    }


# Small live arousal/pressure overlay for the touch-escalation ladder -- reuses the base game's own
# bar styles (girl_arousal_bar / gr_bar, screens.rpy:2609-2622) so it looks consistent with the real
# sex-interaction screen's own meters, and girl.get_arousal_text() for the tiered arousal label (no
# equivalent tiered helper exists for pressure, so that one's shown as a plain percentage). Dispatched
# from vt_huds/vt_overlay.rpy's existing vt_cherry_overlay (config.overlay_screens), gated on
# vt_booth_overlay_girl (a plain store flag this file sets/clears itself -- NOT vt_active_label,
# which turned out unreliable: it only updates when a label is *entered* and never reverts on return
# from a call, so it drifted to whatever sub-label the booth's own action loop last called into,
# e.g. make_small_talk, and never showed the overlay at all in real play). Sized/positioned to sit
# directly above the cherry window's own convo_menu position (left edge x=17, width 378px, traced
# from cherry_window_row's exact frame-width formula for icon_size=36/border_size=2), growing upward
# from its bottom edge so it doesn't need a hand-computed height.
screen vt_booth_arousal_overlay(girl):
    zorder 51
    frame:
        xpos 17
        xanchor 0.0
        ypos 401
        yanchor 1.0
        xsize 378
        background "#000000cc"
        padding (8, 6, 8, 6)
        vbox:
            spacing 4
            text "Arousal: [girl.get_arousal_text()]" size font_size_normal color menu_text_color
            bar:
                style "girl_arousal_bar"
                xsize 362
                ysize 10
                value girl.arousal
                range 100
            text "Pressure: [int(girl.pressure)]%" size font_size_normal color menu_text_color
            bar:
                style "gr_bar"
                xsize 362
                ysize 10
                value girl.pressure
                range 100
            text "Player Arousal: [player.get_arousal_text()]" size font_size_normal color menu_text_color
            bar:
                style "player_arousal_bar"
                xsize 362
                ysize 10
                value player.arousal
                range player.max_arousal


label vt_coffeeshop_booth:
    $ time_manager.skip_time(minutes=10)

    $ _vt_booth_invite = vt_booth_choice(selected_girl, VT_BOOTH_INVITE_LINES)
    player.character "[_vt_booth_invite]"

    $ additional_subtags = ["coffee_shop", "undertable"]
    $ girl_acceptance = selected_girl.get_acceptance_by_name("free_use_compliance")
    $ vt_log_acceptance_breakdown(selected_girl, "free_use_compliance", player)
    $ vt_log_check("booth entry (sit down)", girl_acceptance, 5, girl_acceptance >= 5)

    if girl_acceptance >= 5:
        $ _vt_booth_line = vt_booth_voice(selected_girl, VT_BOOTH_ACCEPT, "Sure, that sounds nice. Let's sit.")
        selected_girl.character "[_vt_booth_line]"

        # .replace() here because these pool strings are plain Python literals chosen into a
        # variable -- Ren'Py's "[...]" substitution is single-pass, so a "[selected_girl]" token
        # embedded in the CHOSEN string never gets a second interpolation pass once it's displayed
        # through the outer "[_vt_seat_down_line]" tag; it would otherwise show up onscreen
        # literally as the text "[selected_girl]" instead of her name.
        $ _vt_seat_down_line = vt_booth_choice(selected_girl, VT_BOOTH_SEAT_DOWN_ACTION_LINES).replace("[selected_girl]", str(selected_girl))
        "[_vt_seat_down_line]"

        $ selected_girl.apply_impacts({"affection": 1000})

        # Deliberate, narrow reset to her own resting baseline -- NOT Girl.reset_for_sex() (that
        # method also spikes tolerance to 85% of max and touches sex-interaction-only session
        # bookkeeping that doesn't belong in this standalone scene, confirmed by direct read). This
        # keeps the touch-escalation ladder below predictable regardless of unrelated arousal/pressure
        # carried over from an earlier exam/sex session the same day.
        $ vt_log(f"arousal/pressure reset: was arousal={selected_girl.arousal} pressure={selected_girl.pressure}")
        $ selected_girl.arousal = selected_girl.base_arousal
        $ selected_girl.pressure = selected_girl.base_pressure
        $ vt_log_girl_snapshot(selected_girl, player)

        # --- Seating ---
        $ _vt_booth_stage_chance = {}
        python:
            _booth_closeness = vt_booth_stage_chance(selected_girl, "seating", VT_BOOTH_STAGE_ORDER,
                                                      VT_BOOTH_LOCAL_TIER_FLOORS, VT_BOOTH_STAGE_BANDS,
                                                      _vt_booth_stage_chance)
            _vt_booth_stage_chance["seating"] = _booth_closeness
        $ _booth_same_side = False
        python:
            _seat_spontaneous_roll = renpy.random.randint(1, 100)
            _seat_spontaneous_success = _seat_spontaneous_roll <= _booth_closeness
            vt_log_roll("spontaneous seating", _seat_spontaneous_roll, _booth_closeness, _seat_spontaneous_success)
        if _seat_spontaneous_success:
            $ _booth_same_side = True
            $ _vt_seat_line = vt_booth_voice(selected_girl, VT_BOOTH_SEAT_TOGETHER, "I'll sit next to you.")
            selected_girl.character "[_vt_seat_line]"
            $ _vt_seat_spontaneous_line = vt_booth_choice(selected_girl, VT_BOOTH_SEAT_SPONTANEOUS_ACTION_LINES)
            "[_vt_seat_spontaneous_line]"

            menu:
                "Let her stay beside you":
                    pass
                "Ask her to sit across instead":
                    $ _vt_seat_across_ask_line = vt_booth_choice(selected_girl, VT_BOOTH_SEAT_ACROSS_ASK_LINES)
                    player.character "[_vt_seat_across_ask_line]"
                    $ _booth_same_side = False
                    $ _vt_seat_move_line = vt_booth_voice(selected_girl, VT_BOOTH_SEAT_MOVE_AWAY, "Oh, okay, sure.")
                    selected_girl.character "[_vt_seat_move_line]"
                    $ _vt_seat_move_action_line = vt_booth_choice(selected_girl, VT_BOOTH_SEAT_MOVE_AWAY_ACTION_LINES)
                    "[_vt_seat_move_action_line]"
        else:
            $ _vt_seat_line = vt_booth_voice(selected_girl, VT_BOOTH_SEAT_ACROSS, "I'll sit over here.")
            selected_girl.character "[_vt_seat_line]"
            $ _vt_seat_across_line = vt_booth_choice(selected_girl, VT_BOOTH_SEAT_ACROSS_ACTION_LINES)
            "[_vt_seat_across_line]"

            menu:
                "Invite her to sit beside you":
                    $ _vt_seat_ask_pitch = vt_player_voice(player, VT_BOOTH_SEAT_ASK_LINES, "Come sit over here with me, it's cozier.")
                    player.character "[_vt_seat_ask_pitch]"
                    python:
                        _seat_roll = renpy.random.randint(1, 100)
                        _seat_threshold = max(20, min(95, _booth_closeness))
                        _seat_success = _seat_roll <= _seat_threshold
                        vt_log_roll("seating persuasion", _seat_roll, _seat_threshold, _seat_success)
                    if _seat_success:
                        $ _booth_same_side = True
                        $ _vt_seat_ask_line = vt_booth_voice(selected_girl, VT_BOOTH_SEAT_ASK_YES, "Okay, I'll come sit next to you.")
                        selected_girl.character "[_vt_seat_ask_line]"
                        $ _vt_seat_ask_action_line = vt_booth_choice(selected_girl, VT_BOOTH_SEAT_ASK_YES_ACTION_LINES)
                        "[_vt_seat_ask_action_line]"
                    else:
                        $ _vt_seat_ask_line = vt_booth_voice(selected_girl, VT_BOOTH_SEAT_ASK_NO, "No, I'll just stay here.")
                        selected_girl.character "[_vt_seat_ask_line]"
                "Let her sit across from you":
                    pass

        # --- Action loop ---
        $ _booth_done_flirty = set()
        $ vt_coffee_booth_flirts_left = VT_BAR_BOOTH_FLIRT_USES
        $ vt_coffee_booth_bathroom_visit = None
        $ _vt_booth_grope_earned_bonus = False
        $ _vt_booth_end_visit = False
        $ _vt_booth_player_came = False
        $ _booth_intimacy_blocked = False
        $ _vt_booth_girl_came = False
        $ _vt_booth_grope_succeeded = False
        $ _vt_booth_touch_bare_started = False
        $ _vt_booth_sour_ending = False

        # Every generic_action_* call below (grope/finger/handjob/blowjob) is a standalone call, not a
        # real screen_sex_interaction_menu.rpy session -- so the base game's own is_during_sex_interaction
        # flag (screen_sex_interaction_menu.rpy:235) never gets set just by being here. That flag is read
        # by a lot of shared machinery that assumes it reflects reality (orgasm-reaction-line tiering,
        # Player.apply_impacts' foreplay arousal dampening, this mod's own vt_wants_pullout pull-out-
        # coercion gate and vt_record_prev_act ATM-reaction recorder) -- setting it for the scene's
        # duration makes the booth behave like a real sex scene for all of that, instead of silently
        # falling through to whatever each caller does when it's absent.
        $ vt_booth_start_encounter(selected_girl)

        label vt_coffeeshop_booth_resume:
        while not _vt_booth_end_visit:
            # Reset every round, same convention every base-game location screen uses (e.g.
            # screen_bar.rpy:188) -- otherwise a stale True from an earlier climax this visit (e.g. he
            # came during a handjob/blowjob) survives into a LATER, unrelated action. generic_action_
            # finger_pussy/tease_clit both end with "elif player.just_came: call generic_action_player_
            # choose_cum(...)" -- with the flag never cleared, picking "Finish her off" afterward
            # re-enters that menu on a stale flag alone, as a bogus second "Ah fuck I'm gonna cum!" with
            # no new arousal behind it. _vt_booth_player_came (set separately, right after each real
            # climax) already tracks "has he finished this visit" for menu-gating, so clearing this here
            # doesn't lose anything.
            $ vt_booth_clear_climax_flags(selected_girl)

            python:
                menu_options = []
                if get_action_count("small_talk", actions_already_done[selected_girl.id]) < 2:
                    menu_options.append(("Small talk", "vt_booth_small_talk"))
                if "compliment" not in _booth_done_flirty:
                    menu_options.append(("Compliment her", "vt_booth_compliment"))
                if vt_coffee_booth_flirts_left > 0:
                    menu_options.append(("Flirt with her", "vt_coffee_booth_flirt"))
                if "handhold" not in _booth_done_flirty:
                    menu_options.append(("Hold her hand", "vt_booth_handhold"))
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
                elif _booth_intimacy_blocked:
                    # Once blocked, none of the escalation-tier options are offered at all -- omitted
                    # outright (not greyed), matching the small-talk-cap convention elsewhere in this
                    # loop. Only small talk/compliment/hand-hold (if unattempted) and "Finish your
                    # coffee" remain.
                    pass
                else:
                    if "thigh" not in _booth_done_flirty:
                        menu_options.append(("Caress her thigh under the table", "vt_booth_thigh"))
                    else:
                        if not _vt_booth_touch_bare_started:
                            if _vt_booth_grope_succeeded:
                                menu_options.append(("Continue groping her", "vt_booth_grope"))
                            else:
                                menu_options.append(("Slide your hand between her legs", "vt_booth_grope"))
                        if _vt_booth_grope_succeeded and not _vt_booth_girl_came:
                            if _vt_booth_player_came:
                                menu_options.append(("Finish her off", "vt_booth_finger"))
                            else:
                                menu_options.append(("Touch her bare", "vt_booth_finger"))
                    if not _vt_booth_player_came:
                        menu_options.append(("Ask for a handjob", "vt_booth_ask_handjob"))
                        menu_options.append(("Ask for a blowjob", "vt_booth_ask_blowjob"))
                if vt_coffee_booth_bathroom_available(selected_girl):
                    menu_options.append(("Bathroom quickie…", "vt_coffee_booth_bathroom"))
                menu_options.append(("Finish your coffee", "vt_booth_finish"))

                menu_choice = renpy.display_menu(menu_options)

            if menu_choice == "vt_booth_finish":
                $ _vt_booth_end_visit = True

            elif menu_choice == "vt_coffee_booth_bathroom":
                call vt_coffee_booth_invite_bathroom
                if _return:
                    return _return

            elif menu_choice == "vt_coffee_booth_flirt":
                call vt_coffee_booth_flirt

            elif menu_choice == "vt_booth_small_talk":
                call make_small_talk

            elif menu_choice == "vt_booth_compliment":
                $ _booth_done_flirty.add("compliment")
                $ _vt_compliment_line = vt_player_voice(player, VT_BOOTH_COMPLIMENT_LINES, "You know, you look really good today.")
                player.character "[_vt_compliment_line]"
                $ _vt_compliment_tier = vt_booth_affection_tier(selected_girl)
                $ _vt_compliment_react = vt_booth_voice(selected_girl, VT_BOOTH_COMPLIMENT_REACT[_vt_compliment_tier], "Thank you, that's sweet.")
                selected_girl.character "[_vt_compliment_react]"
                $ selected_girl.apply_impacts(dict(VT_BOOTH_COMPLIMENT_IMPACTS_BY_TIER[_vt_compliment_tier]))

            elif menu_choice == "vt_booth_handhold":
                $ _booth_done_flirty.add("handhold")
                if _booth_same_side:
                    $ _vt_handhold_ask = vt_player_voice(player, VT_BOOTH_HANDHOLD_SAMESIDE_LINES, "You take her hand under the table.")
                    player.character "[_vt_handhold_ask]"
                else:
                    $ _vt_handhold_ask = vt_player_voice(player, VT_BOOTH_HANDHOLD_ACROSS_LINES, "You reach across the table and take her hand.")
                    player.character "[_vt_handhold_ask]"
                python:
                    _handhold_chance = vt_booth_stage_chance(selected_girl, "handhold", VT_BOOTH_STAGE_ORDER,
                                                              VT_BOOTH_LOCAL_TIER_FLOORS, VT_BOOTH_STAGE_BANDS,
                                                              _vt_booth_stage_chance)
                    _vt_booth_stage_chance["handhold"] = _handhold_chance
                    _handhold_roll = renpy.random.randint(1, 100)
                    _handhold_success = _handhold_roll <= _handhold_chance
                    vt_log_roll("hand-hold", _handhold_roll, _handhold_chance, _handhold_success)
                if _handhold_success:
                    $ _vt_handhold_react = vt_booth_voice(selected_girl, VT_BOOTH_HANDHOLD_ACCEPT, "That's nice.")
                    selected_girl.character "[_vt_handhold_react]"
                    $ selected_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["handhold"]))
                else:
                    $ _vt_handhold_react = vt_booth_voice(selected_girl, VT_BOOTH_HANDHOLD_REJECT, "I'm not ready for that yet.")
                    selected_girl.character "[_vt_handhold_react]"
                    $ selected_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["handhold_reject"]))
                    $ _booth_intimacy_blocked = True

            elif menu_choice == "vt_booth_thigh":
                $ _booth_done_flirty.add("thigh")
                $ _vt_thigh_ask = vt_player_voice(player, VT_BOOTH_THIGH_ASK_LINES, "You rest a hand on her thigh, sliding it slowly upward under the table.")
                "[_vt_thigh_ask]"
                python:
                    _thigh_chance = vt_booth_stage_chance(selected_girl, "thigh", VT_BOOTH_STAGE_ORDER,
                                                           VT_BOOTH_LOCAL_TIER_FLOORS, VT_BOOTH_STAGE_BANDS,
                                                           _vt_booth_stage_chance)
                    _vt_booth_stage_chance["thigh"] = _thigh_chance
                    _thigh_roll = renpy.random.randint(1, 100)
                    _thigh_success = _thigh_roll <= _thigh_chance
                    vt_log_roll("thigh", _thigh_roll, _thigh_chance, _thigh_success)
                if _thigh_success:
                    $ _vt_thigh_react = vt_booth_voice(selected_girl, VT_BOOTH_THIGH_REACT, "Careful, someone might see.")
                    selected_girl.character "[_vt_thigh_react]"
                    $ selected_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["thigh"]))
                    $ _vt_booth_grope_earned_bonus = True
                else:
                    $ _vt_thigh_react = vt_booth_voice(selected_girl, VT_BOOTH_THIGH_REJECT, "Not yet, let's slow down.")
                    selected_girl.character "[_vt_thigh_react]"
                    $ selected_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["thigh_reject"]))
                    $ _booth_intimacy_blocked = True

            elif menu_choice == "vt_booth_grope":
                if _vt_booth_grope_succeeded:
                    # Consent for this was already established by the first success -- continuing to
                    # grope her needs no fresh acceptance roll and no spoken reaction each time, just
                    # the action itself.
                    $ _vt_grope_access_line = vt_booth_choice(selected_girl, VT_BOOTH_GROPE_CONTINUE_LINES)
                    "[_vt_grope_access_line]"
                    call generic_action_grope_pussy(additional_subtags=additional_subtags, skip_descriptions=True, skip_responses=True, force_orgasm=False)
                    if selected_girl.just_came:
                        $ _vt_girl_orgasm_line = vt_booth_voice(selected_girl, VT_BOOTH_GIRL_ORGASM, "I'm coming!")
                        selected_girl.character "[_vt_girl_orgasm_line]"
                        $ _vt_booth_girl_came = True
                    elif vt_booth_check_overstim(selected_girl):
                        $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BOOTH_OVERSTIM_ACTION_LINES)
                        "[_vt_overstim_action_line]"
                        $ _vt_overstim_line = vt_booth_voice(selected_girl, VT_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                        selected_girl.character "[_vt_overstim_line]"
                        $ selected_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["overstim_stop"]))
                        $ _booth_intimacy_blocked = True
                else:
                    $ vt_log_acceptance_breakdown(selected_girl, "grope_pussy", player)
                    python:
                        _grope_chance = vt_booth_stage_chance(selected_girl, "grope", VT_BOOTH_STAGE_ORDER,
                                                               VT_BOOTH_LOCAL_TIER_FLOORS, VT_BOOTH_STAGE_BANDS,
                                                               _vt_booth_stage_chance,
                                                               grope_earned=_vt_booth_grope_earned_bonus)
                        _vt_booth_stage_chance["grope"] = _grope_chance
                        _vt_booth_grope_earned_bonus = False
                        _grope_roll = renpy.random.randint(1, 100)
                        _grope_success = _grope_roll <= _grope_chance
                        vt_log_roll("grope", _grope_roll, _grope_chance, _grope_success)
                    if _grope_success:
                        $ _vt_grope_react = vt_booth_voice(selected_girl, VT_BOOTH_GROPE_ACCEPT, "Okay, go ahead.")
                        selected_girl.character "[_vt_grope_react]"
                        $ _vt_grope_style = vt_booth_lower_access_style(selected_girl)
                        $ _vt_grope_access_line = vt_booth_choice(selected_girl, VT_BOOTH_GROPE_ACCESS_LINES[_vt_grope_style])
                        "[_vt_grope_access_line]"
                        call generic_action_grope_pussy(additional_subtags=additional_subtags, skip_descriptions=True, skip_responses=True, force_orgasm=False)
                        $ vt_booth_overlay_girl = selected_girl
                        $ _vt_booth_grope_succeeded = True
                        if selected_girl.just_came:
                            $ _vt_girl_orgasm_line = vt_booth_voice(selected_girl, VT_BOOTH_GIRL_ORGASM, "I'm coming!")
                            selected_girl.character "[_vt_girl_orgasm_line]"
                            $ _vt_booth_girl_came = True
                        elif vt_booth_check_overstim(selected_girl):
                            $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BOOTH_OVERSTIM_ACTION_LINES)
                            "[_vt_overstim_action_line]"
                            $ _vt_overstim_line = vt_booth_voice(selected_girl, VT_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                            selected_girl.character "[_vt_overstim_line]"
                            $ selected_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["overstim_stop"]))
                            $ _booth_intimacy_blocked = True
                    else:
                        $ _vt_grope_react = vt_booth_voice(selected_girl, VT_BOOTH_GROPE_REJECT, "Not here, that's too much.")
                        selected_girl.character "[_vt_grope_react]"
                        $ selected_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["grope_reject"]))
                        $ _booth_intimacy_blocked = True

            elif menu_choice == "vt_booth_finger":
                $ _vt_booth_touch_bare_started = True
                $ vt_log_acceptance_breakdown(selected_girl, "finger_pussy", player)
                python:
                    _finger_chance = vt_booth_stage_chance(selected_girl, "finger", VT_BOOTH_STAGE_ORDER,
                                                            VT_BOOTH_LOCAL_TIER_FLOORS, VT_BOOTH_STAGE_BANDS,
                                                            _vt_booth_stage_chance)
                    _vt_booth_stage_chance["finger"] = _finger_chance
                    _finger_roll = renpy.random.randint(1, 100)
                    _finger_success = _finger_roll <= _finger_chance
                    vt_log_roll("touch her bare", _finger_roll, _finger_chance, _finger_success)
                if _finger_success:
                    $ _vt_finger_react = vt_booth_voice(selected_girl, VT_BOOTH_FINGER_ACCEPT, "Okay, go ahead.")
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
                            $ _vt_touch_stop_line = vt_booth_choice(selected_girl, VT_BOOTH_TOUCH_STOP_ACTION_LINES)
                            "[_vt_touch_stop_line]"
                            $ _vt_touch_stop = True
                        else:
                            $ _vt_touch_react = vt_booth_voice(selected_girl, VT_BOOTH_TOUCH_ACCEPT, "Okay, don't stop.")
                            selected_girl.character "[_vt_touch_react]"
                            if _vt_touch_last_technique is None:
                                $ _vt_touch_access_line = vt_booth_choice(selected_girl, VT_BOOTH_TOUCH_ACCESS_LINES[_vt_touch_technique][_vt_touch_style])
                            else:
                                $ _vt_touch_access_line = vt_booth_choice(selected_girl, VT_BOOTH_TOUCH_TRANSITION_LINES[(_vt_touch_last_technique, _vt_touch_technique)])
                            "[_vt_touch_access_line]"
                            $ _vt_touch_last_technique = _vt_touch_technique
                            $ vt_log(f"{_vt_touch_technique} attempt pre: {_vt_display_name(selected_girl)} arousal={selected_girl.arousal} pressure={selected_girl.pressure}")
                            if _vt_touch_technique == "clit":
                                call generic_action_tease_clit(additional_subtags=additional_subtags, skip_descriptions=True, skip_responses=True, force_orgasm=False, can_deny_orgasm=False)
                            else:
                                call generic_action_finger_pussy(additional_subtags=additional_subtags, skip_descriptions=True, skip_responses=True, force_orgasm=False, can_deny_orgasm=False)
                            $ vt_log(f"{_vt_touch_technique} attempt post: {_vt_display_name(selected_girl)} arousal={selected_girl.arousal} pressure={selected_girl.pressure} just_came={selected_girl.just_came}")
                            if selected_girl.just_came:
                                $ _vt_girl_orgasm_line = vt_booth_voice(selected_girl, VT_BOOTH_GIRL_ORGASM, "I'm coming!")
                                selected_girl.character "[_vt_girl_orgasm_line]"
                                $ _vt_booth_girl_came = True
                            elif vt_booth_check_overstim(selected_girl):
                                $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BOOTH_OVERSTIM_ACTION_LINES)
                                "[_vt_overstim_action_line]"
                                $ _vt_overstim_line = vt_booth_voice(selected_girl, VT_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                                selected_girl.character "[_vt_overstim_line]"
                                $ selected_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["overstim_stop"]))
                                $ _booth_intimacy_blocked = True
                else:
                    $ _vt_finger_react = vt_booth_voice(selected_girl, VT_BOOTH_FINGER_REJECT, "That's too much, not here.")
                    selected_girl.character "[_vt_finger_react]"
                    $ selected_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["finger_reject"]))
                    $ _booth_intimacy_blocked = True

            elif menu_choice in ("vt_booth_ask_handjob", "vt_booth_ask_blowjob"):
                $ _vt_booth_act = "handjob" if menu_choice == "vt_booth_ask_handjob" else "blowjob"
                call vt_coffeeshop_sex_gate(_vt_booth_act)

        if not _vt_booth_sour_ending:
            $ _vt_visit_end_line = vt_booth_choice(selected_girl, VT_BOOTH_VISIT_END_ACTION_LINES)
            "[_vt_visit_end_line]"

        $ vt_booth_end_encounter(selected_girl)
        $ remove_girl_id_from_location(selected_girl.id, "girls_in_coffee_shop")
    else:
        $ _vt_booth_decline_line = vt_booth_voice(selected_girl, VT_BOOTH_DECLINE, "No thanks... I'm fine right here.")
        selected_girl.character "[_vt_booth_decline_line]"
        $ _vt_decline_action_line = vt_booth_choice(selected_girl, VT_BOOTH_DECLINE_ACTION_LINES)
        "[_vt_decline_action_line]"

    return "show_coffee_shop"


# Shared push/respect negotiation for the two sexual asks (act_key: "handjob" or "blowjob"). Reads
# her live arousal/intox fresh every call via vt_booth_stage_chance; nothing to reset. Sets
# store._vt_booth_end_visit = True on any outcome that ends the visit (hard reject, or a failed push),
# read back by the action loop above after this call returns.
#
# Rolls a die against the SAME per-visit stage-chance machinery every earlier stage uses (2026-09-26 --
# replaces the old deterministic `if _sg_acceptance >= 40` threshold check, which made this the one
# stage in the whole ladder with no actual randomness: cross the line and it was a guaranteed yes).
# Keeps the exact same three-outcome shape the user asked to preserve: a bad roll far above her chance
# is a hard reject, a bad roll close to her chance still gets a negotiation opportunity (the existing
# push/respect menu, untouched), and a good roll is an immediate accept.
label vt_coffeeshop_sex_gate(act_key):
    python:
        _sg_girl = selected_girl
        _sg_ask = vt_player_voice(player, VT_BOOTH_SEX_ASK[act_key], "Okay, how about a little fun under the table?")
    player.character "[_sg_ask]"

    $ vt_log_acceptance_breakdown(_sg_girl, act_key, player)
    python:
        _sg_chance = vt_booth_stage_chance(_sg_girl, act_key, VT_BOOTH_STAGE_ORDER,
                                            VT_BOOTH_LOCAL_TIER_FLOORS, VT_BOOTH_STAGE_BANDS,
                                            _vt_booth_stage_chance)
        _vt_booth_stage_chance[act_key] = _sg_chance
        _sg_roll = renpy.random.randint(1, 100)
        if _sg_roll <= _sg_chance:
            _sg_outcome = "accept"
        elif _sg_roll <= _sg_chance + VT_BOOTH_SEX_PUSH_WINDOW:
            _sg_outcome = "push"
        else:
            _sg_outcome = "reject"
        vt_log_band_roll(f"sex gate '{act_key}'", _sg_roll, _sg_chance, VT_BOOTH_SEX_PUSH_WINDOW, _sg_outcome)

    if _sg_outcome == "accept":
        $ _sg_accept_line = vt_booth_voice(_sg_girl, VT_BOOTH_SEX_ACCEPT[act_key], "Okay, I can do that.")
        _sg_girl.character "[_sg_accept_line]"
        $ time_manager.skip_time(minutes=10)
        $ vt_booth_clear_climax_flags(selected_girl)
        $ _sg_action_line = vt_booth_choice(selected_girl, VT_BOOTH_SEX_ACTION_IMMEDIATE[act_key])
        if act_key == "blowjob":
            call vt_booth_protection_gate(_sg_girl, "oral")
            if not vt_booth_protection_proceed:
                return
        "[_sg_action_line]"
        call vt_booth_buildup(act_key, additional_subtags=additional_subtags)
        if player.just_came:
            $ _sg_finish_line = vt_booth_choice(selected_girl, VT_BOOTH_SEX_FINISH_LINES[act_key])
            "[_sg_finish_line]"
        else:
            $ _sg_heldback_line = vt_booth_choice(selected_girl, VT_BOOTH_SEX_HELDBACK_LINES[act_key])
            "[_sg_heldback_line]"
        $ vt_log(f"sex gate '{act_key}' immediate-accept path: player finished this call = {player.just_came}")
        if player.just_came:
            $ store._vt_booth_player_came = True
        $ _sg_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["sex_accept"]))
        # Her own orgasm from this act (generic_action_handjob/blowjob already called .cum() on her
        # silently, via skip_responses) needs to latch the booth's OWN tracking flag too -- otherwise
        # "Touch her bare" keeps thinking she hasn't finished, since that flag was previously only
        # ever set from the grope/finger touch loop, never from here.
        if _sg_girl.just_came:
            $ store._vt_booth_girl_came = True
        elif vt_booth_check_overstim(_sg_girl):
            # She didn't orgasm herself, but her pressure capped anyway -- same "had enough teasing"
            # bailout the grope/finger touch loop already applies, just never wired up for this harder
            # escalation tier until now.
            $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BOOTH_SEX_OVERSTIM_ACTION_LINES[act_key])
            "[_vt_overstim_action_line]"
            $ _vt_overstim_line = vt_booth_voice(_sg_girl, VT_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
            _sg_girl.character "[_vt_overstim_line]"
            $ _sg_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["overstim_stop"]))
            $ store._booth_intimacy_blocked = True

    elif _sg_outcome == "push":
        $ _sg_interject_line = vt_booth_voice(_sg_girl, VT_BOOTH_SEX_INTERJECT, "Wait, here? Someone might see us.")
        _sg_girl.character "[_sg_interject_line]"

        $ _sg_menu_push = vt_booth_voice(_sg_girl, VT_BOOTH_MENU_PUSH_CAPTION, "Push her a little")
        $ _sg_menu_respect = vt_booth_voice(_sg_girl, VT_BOOTH_MENU_RESPECT_CAPTION, "Respect her wishes")
        menu:
            "[_sg_menu_push]":
                $ _sg_pitch = vt_player_voice(player, VT_BOOTH_PUSH_PITCH, "Come on, no one's paying attention to us back here. Just this once.")
                player.character "[_sg_pitch]"
                python:
                    _sg_push_chance = vt_booth_push_chance(_sg_girl, act_key)
                    _sg_push_roll = renpy.random.randint(1, 100)
                    _sg_push_success = _sg_push_roll <= _sg_push_chance
                    vt_log_roll(f"push '{act_key}'", _sg_push_roll, _sg_push_chance, _sg_push_success)
                if _sg_push_success:
                    $ _sg_push_line = vt_booth_voice(_sg_girl, VT_BOOTH_PUSH_SUCCESS, "Okay, fine. Just be quick.")
                    _sg_girl.character "[_sg_push_line]"
                    $ time_manager.skip_time(minutes=10)
                    $ vt_booth_clear_climax_flags(selected_girl)
                    $ _sg_push_action_line = vt_booth_choice(selected_girl, VT_BOOTH_SEX_ACTION_PUSH[act_key])
                    if act_key == "blowjob":
                        call vt_booth_protection_gate(_sg_girl, "oral")
                        if not vt_booth_protection_proceed:
                            return
                    "[_sg_push_action_line]"
                    call vt_booth_buildup(act_key, additional_subtags=additional_subtags)
                    if player.just_came:
                        $ _sg_push_finish_line = vt_booth_choice(selected_girl, VT_BOOTH_SEX_FINISH_PUSH_LINES[act_key])
                        "[_sg_push_finish_line]"
                    else:
                        $ _sg_push_heldback_line = vt_booth_choice(selected_girl, VT_BOOTH_SEX_HELDBACK_PUSH_LINES[act_key])
                        "[_sg_push_heldback_line]"
                    $ vt_log(f"sex gate '{act_key}' push-success path: player finished this call = {player.just_came}")
                    if player.just_came:
                        $ store._vt_booth_player_came = True
                    $ _sg_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["push_success"]))
                    if _sg_girl.just_came:
                        $ store._vt_booth_girl_came = True
                    elif vt_booth_check_overstim(_sg_girl):
                        $ _vt_overstim_action_line = vt_booth_choice(selected_girl, VT_BOOTH_SEX_OVERSTIM_ACTION_LINES[act_key])
                        "[_vt_overstim_action_line]"
                        $ _vt_overstim_line = vt_booth_voice(_sg_girl, VT_BOOTH_OVERSTIM_STOP, "Please stop, that's too much.")
                        _sg_girl.character "[_vt_overstim_line]"
                        $ _sg_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["overstim_stop"]))
                        $ store._booth_intimacy_blocked = True
                else:
                    $ _sg_fail_line = vt_booth_voice(_sg_girl, VT_BOOTH_PUSH_FAIL, "No, I meant it. Not here.")
                    _sg_girl.character "[_sg_fail_line]"
                    $ _sg_fail_action_line = vt_booth_choice(selected_girl, VT_BOOTH_PUSH_FAIL_ACTION_LINES)
                    "[_sg_fail_action_line]"
                    $ _sg_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["push_fail"]))
                    $ actions_already_done[_sg_girl.id].append("block_talking_coffee_shop")
                    $ store._vt_booth_end_visit = True
                    $ store._vt_booth_sour_ending = True

            "[_sg_menu_respect]":
                $ _sg_respect_line = vt_booth_voice(_sg_girl, VT_BOOTH_RESPECT, "Thank you for understanding.")
                _sg_girl.character "[_sg_respect_line]"
                $ vt_booth_reward_respect(_sg_girl, act_key, VT_BOOTH_IMPACTS["respect"])

    else:
        $ _sg_reject_line = vt_booth_voice(_sg_girl, VT_BOOTH_HARD_REJECT, "That's way too much. I'm leaving.")
        _sg_girl.character "[_sg_reject_line]"
        $ _sg_reject_action_line = vt_booth_choice(selected_girl, VT_BOOTH_HARD_REJECT_ACTION_LINES)
        "[_sg_reject_action_line]"
        $ _sg_girl.apply_impacts(dict(VT_BOOTH_IMPACTS["hard_reject"]))
        $ store._vt_booth_end_visit = True
        $ store._vt_booth_sour_ending = True

    return
