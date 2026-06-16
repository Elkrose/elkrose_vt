# VT MOD 

screen vt_firsttime_notification(message, duration=3.0):
    modal False
    zorder 100
    
    frame:
        style "vt_notify_firsttime_frame"
        xalign 0.5
        yalign 0.15
        padding (20, 15)
        
        text message:
            style "vt_notify_firsttime_text"
            text_align 0.5
    
    timer duration action Hide("vt_firsttime_notification")

screen vt_preg_notification(message, duration=3.0):
    modal False
    zorder 100
    
    frame:
        style "vt_notify_frame"
        xalign 0.5
        yalign 0.65
        padding (20, 15)
        
        text message:
            style "vt_notify_text"
            text_align 0.5
    
    timer duration action Hide("vt_preg_notification")

screen vt_relationals_notification(message, duration=3.0):
    modal False
    zorder 100
    
    frame:
        style "vt_rel_notify_frame"
        xalign 0.5
        yalign 0.25
        padding (20, 15)
        
        text message:
            style "vt_rel_notify_text"
            text_align 0.5
    
    timer duration action Hide("vt_relationals_notification")

screen vt_fetish_notification(message, duration=3.0):
    modal False
    zorder 100
    
    frame:
        style "vt_notify_fetish_frame"
        xalign 0.5
        yalign 0.55
        padding (20, 15)
        
        text message:
            style "vt_notify_fetish_text"
            text_align 0.5
    
    timer duration action Hide("vt_fetish_notification")

screen vt_cum_notification(message, duration=3.0):
    modal False
    zorder 100
    
    frame:
        style "vt_notify_cum_frame"
        xalign 0.5
        yalign 0.85
        padding (20, 15)
        
        text message:
            style "vt_notify_cum_text"
            text_align 0.5
    
    timer duration action Hide("vt_cum_notification")

style vt_notify_cum_frame:
    background "#FDFDED"  # pale yellow
    size 28
    
style vt_notify_cum_text:
    color "#000000"       # Pinkish-white text
    size 24
    slow_cps 0

#fetish #800080
style vt_notify_fetish_frame:
    background "#800080"  # Dark purple-black background
    size 28
    
style vt_notify_fetish_text:
    color "#ffccff"       # Pinkish-white text
    size 24
    slow_cps 0

style vt_notify_firsttime_frame:
    background "#3c0606"  # Dark purple-black background
    size 28
    
style vt_notify_firsttime_text:
    color "#ffccff"       # Pinkish-white text
    size 24
    slow_cps 0

style vt_notify_frame:
    background "#2a0a33"  # Dark purple-black background
    size 28
    
style vt_notify_text:
    color "#ffccff"       # Pinkish-white text
    size 24
    slow_cps 0

style vt_rel_notify_frame:
    background "#2f6e31"  # Dark purple-black background
    size 28
    
style vt_rel_notify_text:
    color "#ffffff"       # white text
    size 24
    slow_cps 0

init python:
    
    def vt_cum_notify(message, duration=3.0):
        """Custom VT notification with styled popup"""
        # First hide any existing VT notification
        renpy.hide_screen("vt_cum_notification")
        # Show our styled notification
        renpy.show_screen("vt_cum_notification", message=message, duration=duration)
        
    def vt_fetish_notify(message, duration=3.0):
        """Custom VT notification with styled popup"""
        # First hide any existing VT notification
        renpy.hide_screen("vt_fetish_notification")
        # Show our styled notification
        renpy.show_screen("vt_fetish_notification", message=message, duration=duration)
    
    def vt_preg_notify(message, duration=3.0):
        """Custom VT notification with styled popup"""
        # First hide any existing VT notification
        renpy.hide_screen("vt_preg_notification")
        # Show our styled notification
        renpy.show_screen("vt_preg_notification", message=message, duration=duration)

    def vt_firsttime_notify(message, duration=3.0):
        """Custom VT notification with styled popup"""
        # First hide any existing VT notification
        renpy.hide_screen("vt_firsttime_notification")
        # Show our styled notification
        renpy.show_screen("vt_firsttime_notification", message=message, duration=duration)

    def vt_relationals_notify(message, duration=3.0):
        """Custom VT notification with styled popup"""
        # First hide any existing VT notification
        renpy.hide_screen("vt_relationals_notification")
        # Show our styled notification
        renpy.show_screen("vt_relationals_notification", message=message, duration=duration)

    def vt_baby_desire_band(girl):
        """Resolve baby_desire into the mod's desire tiers.

        Mirrors the ladder in the creampie-roll notifier (this file, ~3470-3500) so all
        baby-desire copy speaks the same language. Clamps defensively on read because the
        apply_impacts write-path can push baby_desire past 100 (see VT-Pregnancy-System.md).
        """
        d = max(0, min(100, getattr(girl, "baby_desire", 0)))
        if d >= 99:
            return "obsession"
        if d >= 90:
            return "fixation"
        if d >= 75:
            return "obsessed"
        if d >= 50:
            return "thinking"
        if d >= 25:
            return "curious"
        return "none"

    def vt_pill_reaction(girl, pill_id):
        """Player-facing reaction text for a VT fertility-pill gift.

        Varies by the girl's baby_desire band, her pregnancy/awareness state
        (pregnant / knows_pregnant / player_knows_pregnant), and whether she already
        carries the player's child (kids_with_player) -- the latter reuses the existing
        "already a parent" axis from the creampie ladder instead of separate mother copy.
        Returns a string for vt_preg_notify.
        """
        name = girl.first_name
        pregnant = getattr(girl, "pregnant", False)
        knows = getattr(girl, "knows_pregnant", False)
        player_knows = getattr(girl, "player_knows_pregnant", False)
        has_player_kid = getattr(girl, "kids_with_player", 0) > 0

        if pill_id == "fertility_pill":
            if pregnant:
                # both-know is excluded from the give menu, so only two cases reach here.
                if knows and not player_knows:
                    return f"{name} takes the FertiBOOST with a sly little smile, keeping her secret to herself."
                return f"{name} takes the FertiBOOST without a clue her body is already ahead of it."
            band = vt_baby_desire_band(girl)
            if band == "obsession":
                if has_player_kid:
                    return f"{name} clutches the FertiBOOST like treasure - she wants to give you more babies, now."
                return f"{name} clutches the FertiBOOST like treasure, desperate to carry your child."
            if band == "fixation":
                if has_player_kid:
                    return f"{name} swallows the FertiBOOST at once - she can't wait to grow your family."
                return f"{name} swallows the FertiBOOST at once, already picturing the swell of your baby."
            if band == "obsessed":
                return f"{name} takes the FertiBOOST eagerly, biting her lip at the thought."
            if band == "thinking":
                return f"{name} takes the FertiBOOST thoughtfully, her hand drifting to her stomach."
            if band == "curious":
                return f"{name} studies the FertiBOOST a moment, a flicker of curiosity behind her blush."
            return f"{name} eyes the FertiBOOST warily, and only swallows it because you asked."

        if pill_id == "prenatal_vitamins":
            high = vt_baby_desire_band(girl) in ("obsessed", "fixation", "obsession") or has_player_kid
            if not pregnant:
                if high:
                    return f"{name} tucks the PregnaVITA away, already daydreaming of the day she'll need them."
                return f"{name} frowns - 'I won't be needing these' - but tucks the PregnaVITA away anyway."
            if knows and player_knows:
                if high:
                    return f"{name} beams, and promises to take PregnaVITA at her next check-up, glowing."
                return f"{name} accepts the PregnaVITA with a tight nod - she'll take it for the baby's sake."
            if knows and not player_knows:
                if high:
                    return f"{name} takes the PregnaVITA with a secret, radiant smile."
                return f"{name} pockets the PregnaVITA quickly, her secret heavy behind her eyes."
            # pregnant but doesn't know it yet
            if high:
                return f"{name} pockets the PregnaVITA, puzzled but quietly pleased."
            return f"{name} pockets the PregnaVITA, puzzled why you'd give her vitamins."

        return f"{name} accepts the {pill_id}."

    def check_pregnancy_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "pregnancy_followup") and girl.pregnancy_followup == current_day:
                girl.trigger_pregnancy_followup()

    def check_birth_control_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "birth_control_followup") and girl.birth_control_followup == current_day:
                girl.trigger_birth_control_followup()

    def check_condoms_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "condoms_followup") and girl.condoms_followup == current_day:
                girl.trigger_condoms_followup()

    def check_corruption_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "corruption_followup_day") and girl.corruption_followup_day == current_day:
                girl.trigger_corruption_followup()

    def check_naturism_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "naturism_followup_day") and girl.naturism_followup_day == current_day:
                girl.trigger_naturism_followup()
    
    def check_fear_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "fear_followup_day") and girl.fear_followup_day == current_day:
                girl.trigger_fear_followup()

    def check_blowjob_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "blowjob_followup") and girl.blowjob_followup == current_day:
                girl.trigger_blowjob_followup()

    def check_strip_tease_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "strip_tease_followup") and girl.strip_tease_followup == current_day:
                girl.trigger_strip_tease_followup()

    def check_get_dressed_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "get_dressed_followup") and girl.get_dressed_followup == current_day:
                girl.trigger_get_dressed_followup()

    def check_naked_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "naked_followup") and girl.naked_followup == current_day:
                girl.trigger_naked_followup()

    def check_milk_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "milk_followup") and girl.milk_followup == current_day:
                girl.trigger_milk_followup()

    def check_creamer_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "creamer_followup") and girl.creamer_followup == current_day:
                girl.trigger_creamer_followup()

    def check_toppings_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "toppings_followup") and girl.toppings_followup == current_day:
                girl.trigger_toppings_followup()

    def check_small_talk_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "small_talk_followup") and girl.small_talk_followup == current_day:
                girl.trigger_small_talk_followup()
    
    def check_masturbation_tips_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "masturbation_tips_followup") and girl.masturbation_tips_followup == current_day:
                girl.trigger_masturbation_tips_followup()

    def check_shower_sex_followups():
        current_day = time_manager.total_days
        all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
        for girl in all_girls:
            if hasattr(girl, "shower_sex_followup") and girl.shower_sex_followup == current_day:
                girl.trigger_shower_sex_followup()

    database_daily_updates["vt_pregnancy_followups"] = check_pregnancy_followups
    database_daily_updates["vt_birth_control_followups"] = check_birth_control_followups
    database_daily_updates["vt_condoms_followups"] = check_condoms_followups
    database_daily_updates["vt_corruption_followups"] = check_corruption_followups
    database_daily_updates["vt_naturism_followups"] = check_naturism_followups
    database_daily_updates["vt_fear_followups"] = check_fear_followups
    database_daily_updates["vt_blowjob_followups"] = check_blowjob_followups
    database_daily_updates["vt_strip_tease_followups"] = check_strip_tease_followups
    database_daily_updates["vt_get_dressed_followups"] = check_get_dressed_followups
    database_daily_updates["vt_naked_followups"] = check_naked_followups
    database_daily_updates["vt_milk_followups"] = check_milk_followups
    database_daily_updates["vt_creamer_followups"] = check_creamer_followups
    database_daily_updates["vt_toppings_followups"] = check_toppings_followups
    database_daily_updates["vt_small_talk_followups"] = check_small_talk_followups
    database_daily_updates["vt_masturbation_tips_followups"] = check_masturbation_tips_followups
    database_daily_updates["vt_shower_sex_followups"] = check_shower_sex_followups
    
    renpy.log("VT Followup System: All systems registered with game's database")

# HELPER FUNCTIONS (defined early for use in patches)
init python:
    # HELPER FUNCTION FOR MOTHER IDENTIFICATION
    def is_mother_character(girl):
        """Reliably determine if a character is a Mother"""
        if hasattr(girl, "is_mother") and girl.is_mother:
            return True
        if hasattr(girl, "role") and "mother" in str(girl.role).lower():
            return True
        if hasattr(girl, "character_type") and "mother" in str(girl.character_type).lower():
            return True
        if hasattr(girl, "__class__") and "Mother" in girl.__class__.__name__:
            return True
        return False

    def check_probability(percentage):
        """Returns True with exactly 'percentage'% probability"""
        #return renpy.random.randint(1, 1000) <= int(percentage * 10)
        """Returns True with exactly 'percentage'% probability, using a 1-100 scale."""
        return renpy.random.randint(1, 100) <= percentage
    
    def get_cum_fetish_level(girl, fetish_type):
        """Gets cum fetish level (0-100) based on relevant traits"""
        
        # Safety check for trait system
        if not hasattr(girl, 'has_trait'):
            return 0
            
        level = 0
        
        if fetish_type == "oral":
            if girl.has_trait("oral_cum_fixation"):
                level += 30
            if girl.has_trait("oral_cum_slut"):
                level += 25
            if girl.has_trait("oral_cum_addict"):
                level += 35
            if girl.has_trait("oral_cum_devotee"):
                level += 40  # Ultimate devotion
            if girl.has_trait("oral_fixation"):
                level += 30  # Reduced from 40
            if girl.has_trait("cum_slut"):
                level += 15  # Reduced from 30
            if girl.has_trait("slut"):
                level += 15
            if girl.has_trait("whore"):
                level += 25
            # Total: 90 (allows room for progression)
        
        elif fetish_type == "vaginal":
            if girl.has_trait("vaginal_cum_fixation"):
                level += 35
            if girl.has_trait("vaginal_cum_dumpster"):
                level += 30
            if girl.has_trait("vaginal_cum_addict"):
                level += 25
            if girl.has_trait("vaginal_cum_devotee"):
                level += 40  # Ultimate devotion
            if girl.has_trait("cum_dumpster"):
                level += 35  # Reduced from 50
            if girl.has_trait("cum_slut"):
                level += 15  # Reduced from 20
            if girl.has_trait("slut"):
                level += 15
            if girl.has_trait("whore"):
                level += 25
            # Total: 90 (allows room for progression)
        
        elif fetish_type == "anal":
            if girl.has_trait("anal_cum_fixation"):
                level += 30
            if girl.has_trait("anal_cum_dumpster"):
                level += 25
            if girl.has_trait("anal_cum_addict"):
                level += 25
            if girl.has_trait("anal_cum_devotee"):
                level += 40  # Ultimate devotion
            if girl.has_trait("anal_slut"):
                level += 30  # Reduced from 40
            if girl.has_trait("cum_dumpster"):
                level += 15  # Reduced from 20
            if girl.has_trait("slut"):
                level += 15
            if girl.has_trait("whore"):
                level += 25
            # Total: 85 (allows room for progression)
        
        # ADD THESE MISSING TYPES:
        elif fetish_type == "boobs":
            if girl.has_trait("boob_cum_slut"):
                level += 15
            if girl.has_trait("boob_cum_fixation"):
                level += 25
            if girl.has_trait("boob_cum_addict"):
                level += 35
            if girl.has_trait("boob_cum_devotee"):
                level += 45  # Ultimate devotion
            if girl.has_trait("cum_slut"):
                level += 15
            if girl.has_trait("slut"):
                level += 10
            if girl.has_trait("whore"):
                level += 15
            # Total: 125 (capped at 100)
        
        elif fetish_type == "thighs":
            if girl.has_trait("thigh_cum_slut"):
                level += 15
            if girl.has_trait("thigh_cum_fixation"):
                level += 25
            if girl.has_trait("thigh_cum_addict"):
                level += 35
            if girl.has_trait("thigh_cum_devotee"):
                level += 45 # Ultimate devotion
            if girl.has_trait("cum_slut"):
                level += 15
            if girl.has_trait("slut"):
                level += 10
            if girl.has_trait("whore"):
                level += 15
            # Total: 95
        
        elif fetish_type == "ass_cum":
            if girl.has_trait("ass_cum_slut"):
                level += 15
            if girl.has_trait("ass_cum_fixation"):
                level += 25
            if girl.has_trait("ass_cum_addict"):
                level += 35
            if girl.has_trait("ass_cum_devotee"):
                level += 45  # Ultimate devotion
            if girl.has_trait("cum_slut"):
                level += 15
            if girl.has_trait("slut"):
                level += 10
            if girl.has_trait("whore"):
                level += 15
            # Total: 95
        
        elif fetish_type == "pussy_cum":
            if girl.has_trait("pussy_cum_slut"):
                level += 15
            if girl.has_trait("pussy_cum_fixation"):
                level += 25
            if girl.has_trait("pussy_cum_addict"):
                level += 35
            if girl.has_trait("pussy_cum_devotee"):
                level += 45  # Ultimate devotion
            if girl.has_trait("cum_slut"):
                level += 15
            if girl.has_trait("slut"):
                level += 10
            if girl.has_trait("whore"):
                level += 25
            # Total: 110 (capped at 100)

        # Cap at 100
        return min(level, 100)

    def get_baby_desire(girl):
        """Calculates baby desire (0-100) based on traits and corruption"""
        
        # Safety check for trait system
        if not hasattr(girl, 'has_trait'):
            return 20
            
        # Base desire inversely related to corruption
        base_desire = 100 - min(girl.corruption, 100)
        
        # Conservative girls have higher baby desire
        if girl.has_trait("conservative"):
            base_desire += 20
        
        # Reserved girls have moderately high baby desire
        elif girl.has_trait("reserved"):
            base_desire += 10
        
        # Slutty/whore girls have lower baby desire
        if girl.has_trait("ultimate_whore"):
            base_desire -= 45
        elif girl.has_trait("whore"):
            base_desire -= 35
        elif girl.has_trait("slut"):
            base_desire -= 25
        
        # Cum dumpster girls might have higher baby desire (contradictory psychology)
        if girl.has_trait("cum_dumpster"):
            base_desire += 15
        
        # Handle conflicted traits with reduced impact
        conflicted_bonus = 0
        if girl.has_trait("conflicted_cum_dumpster"):
            conflicted_bonus += 7.5
        if girl.has_trait("conflicted_pussy_cum_slut"):
            conflicted_bonus += 12.5
        if conflicted_bonus > 0:
            base_desire += conflicted_bonus
        
        # ADD ALL SPECIFIC FETISH IMPACTS - with proper tiered values
        # Pussy cum exposure (strongest pregnancy connection)
        if girl.has_trait("pussy_cum_addict"):
            base_desire += 25  # Ultimate fixation
        elif girl.has_trait("pussy_cum_slut"):
            base_desire += 15  # Moderate interest
        
        # Vaginal creampie (direct pregnancy connection)
        if girl.has_trait("vaginal_addict"):
            base_desire += 20  # Ultimate fixation
        elif girl.has_trait("cum_dumpster_devotee"):
            base_desire += 12  # Devotee level
        elif girl.has_trait("cum_dumpster"):
            base_desire += 8   # Base level
        
        # External cumshot types (weaker pregnancy connection)
        if girl.has_trait("boob_cum_addict"):
            base_desire += 5
        elif girl.has_trait("boob_cum_slut"):
            base_desire += 3
            
        if girl.has_trait("thigh_cum_addict"):
            base_desire += 3
        elif girl.has_trait("thigh_cum_slut"):
            base_desire += 1
            
        if girl.has_trait("ass_cum_addict"):
            base_desire += 2
        elif girl.has_trait("ass_cum_slut"):
            base_desire += 1
            
        if girl.has_trait("oral_addict"):
            base_desire += 1  # Minimal connection
            
        # Anal has NEGATIVE connection to pregnancy desire
        if girl.has_trait("anal_addict"):
            base_desire -= 10
        elif girl.has_trait("anal_slut"):
            base_desire -= 5
        
        # Cap at 100 and floor at 0
        return max(0, min(base_desire, 100))

    def determine_initial_virginity(girl):
        """
        Determines initial virginity status and first-time flags based on:
        - Character type (mother vs student)
        - Trait combinations
        - Corruption/naturism levels
        - Baby desire
        - Financial situation
        
        Returns a dictionary of determined statuses
        """
        is_mother = is_mother_character(girl)
        statuses = {
            'hymen': True,  # Default to virgin
            'first_time_pussy': True,
            'first_time_oral': True,
            'first_time_anal': True,
            'first_time_boobs': True,
            'first_time_thighs': True,
            'first_time_ass_cumshot': True,
            'first_time_pussy_cumshot': True
        }
        
        # ===== MOTHERS HAVE SPECIFIC RULES =====
        if is_mother:
            # Mothers have had at least one child, so:
            statuses['hymen'] = False
            statuses['first_time_pussy'] = False
            
            # For other activities, it depends on their traits
            # Conservative mothers might still be oral/anal virgins
            if girl.has_trait("conservative") or girl.has_trait("reserved"):
                # Conservative mothers might avoid oral/anal
                statuses['first_time_oral'] = girl.corruption < 40
                statuses['first_time_anal'] = girl.corruption < 50
            else:
                # More experienced mothers
                statuses['first_time_oral'] = girl.corruption < 25
                statuses['first_time_anal'] = girl.corruption < 35
                
            # External cumshot experiences (boobs, thighs, etc.)
            statuses['first_time_boobs'] = girl.corruption < 30
            statuses['first_time_thighs'] = girl.corruption < 35
            statuses['first_time_ass_cumshot'] = girl.corruption < 40
            statuses['first_time_pussy_cumshot'] = girl.corruption < 45
            
            return statuses
        
        # ===== STUDENTS HAVE MORE NUANCED RULES =====
        
        # VAGINAL VIRGINITY (hymen & first_time_pussy)
        vaginal_virgin_chance = 100  # Base 100% chance of being virgin
        
        # Trait modifiers
        if girl.has_trait("virgin"):
            vaginal_virgin_chance = 100
        elif girl.has_trait("slut") or girl.has_trait("whore"):
            vaginal_virgin_chance = 0
        elif girl.has_trait("rebellious"):
            vaginal_virgin_chance -= 30
        elif girl.has_trait("dumb"):
            vaginal_virgin_chance -= 15  # Less likely to make smart decisions
            
        # Corruption/naturism modifiers
        vaginal_virgin_chance -= girl.corruption * 0.8
        vaginal_virgin_chance -= girl.naturism * 0.5
        
        # Baby desire modifier (higher desire = more likely to be virgin)
        vaginal_virgin_chance += girl.baby_desire * 0.3
        
        # Financial situation modifier (broke = less likely to be virgin)
        if hasattr(girl, 'financial_need'):
            vaginal_virgin_chance -= (girl.financial_need - 1) * 25
            
        # Final determination
        statuses['hymen'] = (renpy.random.randint(1, 100) <= max(0, min(100, vaginal_virgin_chance)))
        statuses['first_time_pussy'] = statuses['hymen']
        
        # ORAL VIRGINITY (first_time_oral)
        oral_virgin_chance = 100  # Base 100% chance of being oral virgin
        
        # Trait modifiers
        if girl.has_trait("oral_fixation") or girl.has_trait("oral_cum_slut"):
            oral_virgin_chance = 0
        elif girl.has_trait("slut") or girl.has_trait("whore"):
            oral_virgin_chance -= 40
        elif girl.has_trait("rebellious"):
            oral_virgin_chance -= 25
            
        # Corruption/naturism modifiers
        oral_virgin_chance -= girl.corruption * 0.7
        oral_virgin_chance -= girl.naturism * 0.4
        
        # Baby desire modifier (higher desire = more likely to be oral virgin)
        oral_virgin_chance += girl.baby_desire * 0.2
        
        # Financial situation modifier
        if hasattr(girl, 'financial_need'):
            oral_virgin_chance -= (girl.financial_need - 1) * 15
            
        # Final determination
        statuses['first_time_oral'] = (renpy.random.randint(1, 100) <= max(0, min(100, oral_virgin_chance)))
        
        # ANAL VIRGINITY (first_time_anal)
        anal_virgin_chance = 100  # Base 100% chance of being anal virgin
        
        # Trait modifiers
        if girl.has_trait("anal_slut"):
            anal_virgin_chance = 0
        elif girl.has_trait("slut") or girl.has_trait("whore"):
            anal_virgin_chance -= 30
        elif girl.has_trait("rebellious"):
            anal_virgin_chance -= 20
            
        # Corruption/naturism modifiers
        anal_virgin_chance -= girl.corruption * 0.9
        anal_virgin_chance -= girl.naturism * 0.6
        
        # Baby desire modifier (higher desire = more likely to be anal virgin)
        anal_virgin_chance += girl.baby_desire * 0.15
        
        # Financial situation modifier
        if hasattr(girl, 'financial_need'):
            anal_virgin_chance -= (girl.financial_need - 1) * 10
            
        # Final determination
        statuses['first_time_anal'] = (renpy.random.randint(1, 100) <= max(0, min(100, anal_virgin_chance)))
        
        # EXTERNAL CUMSHOT EXPERIENCES
        # These are less intimate but still relevant
        
        # Boob cumshot experience
        boob_cum_virgin_chance = 100
        if girl.has_trait("boob_cum_slut"):
            boob_cum_virgin_chance = 0
        elif girl.has_trait("slut") or girl.has_trait("whore"):
            boob_cum_virgin_chance -= 25
        boob_cum_virgin_chance -= girl.corruption * 0.6
        statuses['first_time_boobs'] = (renpy.random.randint(1, 100) <= max(0, min(100, boob_cum_virgin_chance)))
        
        # Thigh cumshot experience
        thigh_cum_virgin_chance = 100
        if girl.has_trait("thigh_cum_slut"):
            thigh_cum_virgin_chance = 0
        elif girl.has_trait("slut") or girl.has_trait("whore"):
            thigh_cum_virgin_chance -= 20
        thigh_cum_virgin_chance -= girl.corruption * 0.5
        statuses['first_time_thighs'] = (renpy.random.randint(1, 100) <= max(0, min(100, thigh_cum_virgin_chance)))
        
        # Ass cumshot experience
        ass_cum_virgin_chance = 100
        if girl.has_trait("ass_cum_slut"):
            ass_cum_virgin_chance = 0
        elif girl.has_trait("slut") or girl.has_trait("whore"):
            ass_cum_virgin_chance -= 15
        ass_cum_virgin_chance -= girl.corruption * 0.4
        statuses['first_time_ass_cumshot'] = (renpy.random.randint(1, 100) <= max(0, min(100, ass_cum_virgin_chance)))
        
        # Pussy cumshot experience (external)
        pussy_cum_virgin_chance = 100
        if girl.has_trait("pussy_cum_slut"):
            pussy_cum_virgin_chance = 0
        elif girl.has_trait("slut") or girl.has_trait("whore"):
            pussy_cum_virgin_chance -= 20
        pussy_cum_virgin_chance -= girl.corruption * 0.5
        statuses['first_time_pussy_cumshot'] = (renpy.random.randint(1, 100) <= max(0, min(100, pussy_cum_virgin_chance)))
        
        return statuses

    def initialize_virginity_status(girl):
        """Sets the virginity status attributes on a girl instance"""
        statuses = determine_initial_virginity(girl)
        
        # Set all attributes
        girl.hymen = statuses['hymen']
        girl.first_time_pussy = statuses['first_time_pussy']
        girl.first_time_oral = statuses['first_time_oral']
        girl.first_time_anal = statuses['first_time_anal']
        girl.first_time_boobs = statuses['first_time_boobs']
        girl.first_time_thighs = statuses['first_time_thighs']
        girl.first_time_ass_cumshot = statuses['first_time_ass_cumshot']
        girl.first_time_pussy_cumshot = statuses['first_time_pussy_cumshot']
        
        # Log for debugging
        renpy.log(f"VT MOD: Initialized virginity status for {girl.first_name}:")
        renpy.log(f"  - Vaginal: {'Virgin' if statuses['hymen'] else 'Non-virgin'}")
        renpy.log(f"  - Oral: {'Virgin' if statuses['first_time_oral'] else 'Non-virgin'}")
        renpy.log(f"  - Anal: {'Virgin' if statuses['first_time_anal'] else 'Non-virgin'}")

    def wants_condom(girl, sex_type="vaginal"):
        """Determines if girl wants condom based on traits and corruption level"""
        
        # Safety check for trait system
        if not hasattr(girl, 'has_trait'):
            return girl.corruption < 60
        
        # Base probability starts at 50% (neutral)
        base_probability = 50
        
        # Conservative/reserved girls strongly want condoms
        if girl.has_trait("conservative"):
            base_probability += 40
        elif girl.has_trait("reserved"):
            base_probability += 25
        
        # Slutty girls strongly don't want condoms
        if girl.has_trait("ultimate_whore"):
            base_probability -= 50
        elif girl.has_trait("whore"):
            base_probability -= 35
        elif girl.has_trait("slut"):
            base_probability -= 20
        
        # Adjust based on specific fetish types
        if sex_type == "vaginal":
            # Vaginal creampie has highest pregnancy risk
            if girl.has_trait("cum_dumpster_devotee") or girl.has_trait("vaginal_addict"):
                base_probability -= 45
            elif girl.has_trait("cum_dumpster"):
                base_probability -= 30
            elif girl.has_trait("conflicted_cum_dumpster"):
                base_probability -= 15  # Conflicted - sometimes wants, sometimes doesn't
                
        elif sex_type == "oral":
            # Oral has lower pregnancy risk but still relevant
            if girl.has_trait("oral_addict") or girl.has_trait("oral_cum_addict"):
                base_probability -= 35
            elif girl.has_trait("oral_fixation") or girl.has_trait("cum_slut"):
                base_probability -= 20
            elif girl.has_trait("conflicted_oral_cum_fixation"):
                base_probability -= 10
                
        elif sex_type == "anal":
            # Anal has no pregnancy risk but some girls still want protection
            if girl.has_trait("anal_addict") or girl.has_trait("anal_cum_addict"):
                base_probability -= 25
            elif girl.has_trait("anal_slut"):
                base_probability -= 15
            elif girl.has_trait("conflicted_anal_slut"):
                base_probability -= 7
                
        elif sex_type == "body":
            # Boob sex has very low pregnancy risk
            if girl.has_trait("boob_cum_addict"):
                base_probability -= 20
            elif girl.has_trait("boob_cum_slut"):
                base_probability -= 10
            elif girl.has_trait("conflicted_boob_cum_fixation"):
                base_probability -= 5
                
            # Thigh sex has minimal pregnancy risk
            if girl.has_trait("thigh_cum_addict"):
                base_probability -= 15
            elif girl.has_trait("thigh_cum_slut"):
                base_probability -= 7

            # External ass cumshot has no pregnancy risk
            if girl.has_trait("ass_cum_addict"):
                base_probability -= 10
            elif girl.has_trait("ass_cum_slut"):
                base_probability -= 5
                
            # External pussy cumshot has some pregnancy risk
            if girl.has_trait("pussy_cum_addict"):
                base_probability -= 25
            elif girl.has_trait("pussy_cum_slut"):
                base_probability -= 15
            elif girl.has_trait("conflicted_pussy_cum_slut"):
                base_probability -= 7
        
        # Add corruption modifier (more corrupted = less likely to want condoms)
        corruption_modifier = (100 - girl.corruption) / 2  # 0-50 range
        final_probability = max(5, min(95, base_probability + corruption_modifier))
        
        # Return True if random roll is below probability (higher probability = more likely to want condoms)
        return renpy.random.randint(1, 100) <= final_probability
        

    # TRACK RETRY ATTEMPTS TO PREVENT RECURSION
    _vt_retry_count = 0
    _vt_max_retries = 10  # Stop after 10 attempts

init -34 python:
    # Define a consistent days_from_ideal_fertility method for both classes
    def consistent_days_from_ideal_fertility(self, with_direction=False):
        """
        Returns days from ideal fertile day
        Negative = before ideal day, Positive = after ideal day
        Example: -2 = 2 days before ovulation, +1 = 1 day after ovulation
        """
        # Safely access time_manager
        cycle_day = 0
        try:
            # Use the global 'time_manager' instance that was created in game_init.rpy
            cycle_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log(f"VT MOD ERROR: apply_prenatal_boost failed because 'time_manager' is not defined for {self.first_name}.")
            return # Exit the function can't get current day
            
        day_difference = cycle_day - self.ideal_fertile_day
        
        # Normalize to -15 to +14 range
        if day_difference > 15:
            day_difference -= 30
        elif day_difference < -15:
            day_difference += 30
            
        return day_difference if with_direction else abs(day_difference)
    
    # Patch GirlConfig if it exists
    try:
        GirlConfig = renpy.store.GirlConfig
    except:
        pass
    else:
        # Ensure GirlConfig has the necessary attributes
        GirlConfig.fertility_percent = getattr(GirlConfig, 'fertility_percent', 25.0)
        GirlConfig.ideal_fertile_day = getattr(GirlConfig, 'ideal_fertile_day', renpy.random.randint(0, 29))
        GirlConfig.baby_desire = getattr(GirlConfig, 'baby_desire', 100 - renpy.random.randint(0, 100))
        print("VT MOD: Patched GirlConfig with fertility attributes")

init -3 python:
    # Add condom tracking to Player class
    try:
        Player = renpy.store.Player
    except:
        pass
    else:
        original_player_init = Player.__init__
        original_player_daily_update = Player.daily_update

        # ===== SIDECAR IMPLEMENTATION ======================================
        # The player's condom state lives in player.mod_data["elkrose_vt"] -- a dict of
        # primitives -- instead of as loose attributes on the Player. This mirrors the
        # proposed base-game "mod_data[mod_id]" convention: if the mod is removed, the
        # blob is just inert leftover data that the base game never looks at (and that a
        # one-line `del player.mod_data["elkrose_vt"]` could wipe), rather than ~6 loose
        # keys welded onto the Player object.
        #
        # Access stays ergonomic: property accessors (defined below) make
        # `player.condom_active` transparently read/write the sidecar, so the ~200
        # existing `player.condom_*` call sites are unchanged. Properties are class-level,
        # so they are NEVER pickled -- the only thing saved is the mod_data dict, and the
        # properties vanish cleanly with the mod.
        VT_MOD_ID = "elkrose_vt"
        VT_PLAYER_CONDOM_DEFAULTS = {
            "condom_active": "raw",
            "condom_cheap_count": 0,
            "condom_premium_count": 0,
            "condom_broke": False,
            "condom_cum": 0,        # times unloaded in the CURRENT condom
            "condom_dirty": False,  # whether the current condom has cum
        }

        def vt_player_bucket(p):
            # Return (creating if needed) this mod's primitives-only sidecar dict on p.
            md = getattr(p, "mod_data", None)
            if md is None:
                md = {}
                p.mod_data = md
            return md.setdefault(VT_MOD_ID, {})

        # Gift "ammo": pills are bought into a per-id count in the sidecar instead of sitting
        # in the inventory as Gift objects (same idea as condoms). They surface as virtual
        # giftable items in the give-gift menu (see get_items_and_quantity / vt_give_gift).
        VT_PILL_IDS = ("fertility_pill", "prenatal_vitamins", "planb_pill", "emergency_pill")

        def vt_player_pill_counts(p):
            # Return (creating if needed) the pill ammo dict {pill_id: count} in the sidecar.
            return vt_player_bucket(p).setdefault("pill_counts", {})

        def vt_ensure_player_condom_attrs(p=None):
            # Ensure the sidecar exists and is fully populated. Idempotent. Also MIGRATES
            # any legacy loose attributes (from saves made before this mod, or before the
            # sidecar migration) into the sidecar, then strips them so the property accessors govern.
            # Called with no args by config.after_load_callbacks -> falls back to store.player.
            if p is None:
                p = getattr(renpy.store, "player", None)
            if p is None:
                return
            bucket = vt_player_bucket(p)
            for key, default in VT_PLAYER_CONDOM_DEFAULTS.items():
                # Pull a legacy loose attribute into the sidecar if one is present.
                if key in p.__dict__:
                    bucket.setdefault(key, p.__dict__[key])
                    del p.__dict__[key]
                bucket.setdefault(key, default)

            # Convert any legacy condom packs / gift pills already sitting in the inventory
            # (bought before the auto-convert at purchase) into counts, so older saves get
            # cleaned up too.
            pill_counts = bucket.setdefault("pill_counts", {})
            inv = getattr(p, "inventory", None)
            if inv:
                for it in list(inv):
                    iid = getattr(it, "id", None)
                    if iid in ("condoms", "condoms_premium"):
                        sc = getattr(it, "applied_buff", None)
                        sc = sc.get("stat_changes", {}) if isinstance(sc, dict) else {}
                        if iid == "condoms":
                            bucket["condom_cheap_count"] = bucket.get("condom_cheap_count", 0) + sc.get("condom_cheap_count", 10)
                        else:
                            bucket["condom_premium_count"] = bucket.get("condom_premium_count", 0) + sc.get("condom_premium_count", 10)
                    elif iid in VT_PILL_IDS:
                        pill_counts[iid] = pill_counts.get(iid, 0) + 1
                    else:
                        continue
                    try:
                        p.remove_item(it)
                    except Exception:
                        pass

        # Property accessors: keep `player.condom_active` ergonomics, store in the sidecar.
        def _vt_make_condom_property(key, default):
            def _getter(self):
                md = getattr(self, "mod_data", None)
                if md and key in md.get(VT_MOD_ID, {}):
                    return md[VT_MOD_ID][key]
                # Legacy fallback: a not-yet-migrated loose value (data descriptor would
                # otherwise shadow it). vt_ensure_player_condom_attrs cleans this up.
                if key in self.__dict__:
                    return self.__dict__[key]
                return default
            def _setter(self, value):
                vt_player_bucket(self)[key] = value
            return property(_getter, _setter)

        for _key, _default in VT_PLAYER_CONDOM_DEFAULTS.items():
            setattr(Player, _key, _vt_make_condom_property(_key, _default))

        def vt_player_init(self, character: Character, color: str):
            original_player_init(self, character, color)
            vt_ensure_player_condom_attrs(self)

        def vt_player_daily_update(self):
            # Defensive: a Player loaded from a pre-mod / pre-sidecar save is normalized here.
            vt_ensure_player_condom_attrs(self)
            original_player_daily_update(self)
            # Remove condom states if still wearing one when went to sleep
            if self.condom_active != "raw":
                self.condom_active = "raw"
                self.condom_broke = False
                self.condom_cum = 0
                self.condom_dirty = False
            else:
                self.condom_dirty = False

        Player.__init__ = vt_player_init
        Player.vt_player_daily_update = vt_player_daily_update
        Player.daily_update = vt_player_daily_update

        # Auto-convert bought condom packs into sidecar "ammo" at the moment of purchase,
        # so they never sit in player.inventory as ConsumableItem objects. The cherry HUD
        # spends these counts directly, so the inventory object is pointless -- and this way
        # nothing lingers in the base inventory if the mod is removed. Player.add_item is the
        # single chokepoint (purchase_item -> add_item). Guarded so a Shift+R reload doesn't
        # double-wrap the method.
        if not getattr(Player.add_item, "_vt_addon", False):
            original_player_add_item = Player.add_item

            def vt_player_add_item(self, item):
                item_id = getattr(item, "id", None)
                if item_id in ("condoms", "condoms_premium"):
                    buff = getattr(item, "applied_buff", None)
                    stat_changes = buff.get("stat_changes", {}) if isinstance(buff, dict) else {}
                    if item_id == "condoms":
                        qty = stat_changes.get("condom_cheap_count", 10)
                        self.condom_cheap_count += qty
                        label = "BasicShield"
                    else:
                        qty = stat_changes.get("condom_premium_count", 10)
                        self.condom_premium_count += qty
                        label = "UltraProtect"
                    word = "condom" if qty == 1 else "condoms"
                    try:
                        queue_notification(f"{qty} {label} {word} added to your stash!", duration=3.0)
                    except Exception:
                        pass
                    renpy.restart_interaction()
                    return
                if item_id in VT_PILL_IDS:
                    counts = vt_player_pill_counts(self)
                    counts[item_id] = counts.get(item_id, 0) + 1
                    try:
                        queue_notification(f"{getattr(item, 'name', 'Item')} added to your stash!", duration=3.0)
                    except Exception:
                        pass
                    renpy.restart_interaction()
                    return
                original_player_add_item(self, item)

            vt_player_add_item._vt_addon = True
            Player.add_item = vt_player_add_item

        # Surface condom "ammo" in the base UI WITHOUT overriding any screen, by feeding the
        # plain Player methods those screens already call:
        #  - get_item_quantity()       -> the shop's "Owned: N" (screen_ubuy_menu.rpy:176)
        #  - get_items_and_quantity()  -> the inventory listing (screen_player_inventory.rpy:63)
        # The inventory entry is a plain StoreItem (NOT a ConsumableItem), so the inventory
        # screen renders it but the click is a harmless no-op (the ConsumableItem branch, which
        # would "consume" it, is skipped) -- condoms are equipped from the cherry HUD, not used
        # from the inventory. These display items are transient: rebuilt each call, never stored
        # or saved.
        if not getattr(Player.get_item_quantity, "_vt_addon", False):
            original_get_item_quantity = Player.get_item_quantity

            def vt_get_item_quantity(self, item_id):
                if item_id == "condoms":
                    return self.condom_cheap_count
                if item_id == "condoms_premium":
                    return self.condom_premium_count
                if item_id in VT_PILL_IDS:
                    # Read-only: never create sidecar keys during a render-path call.
                    md = getattr(self, "mod_data", None)
                    if md:
                        return md.get(VT_MOD_ID, {}).get("pill_counts", {}).get(item_id, 0)
                    return 0
                return original_get_item_quantity(self, item_id)

            vt_get_item_quantity._vt_addon = True
            Player.get_item_quantity = vt_get_item_quantity

        if not getattr(Player.get_items_and_quantity, "_vt_addon", False):
            original_get_items_and_quantity = Player.get_items_and_quantity

            # Cache the condom display items so the SAME object identity is returned on every
            # call. Building a fresh StoreItem each evaluation makes the inventory screen look
            # "changed" every frame, which drives Ren'Py into a restart_interaction loop.
            # (Pills already reuse the stable database Gift objects, so they're fine.)
            _vt_condom_display_items = {}

            def _vt_condom_display_item(item_id, name, icon, description):
                cached = _vt_condom_display_items.get(item_id)
                if cached is not None:
                    return cached
                SI = getattr(renpy.store, "StoreItem", None)
                if SI is None:
                    return None
                try:
                    obj = SI(id=item_id, name=name, icon=icon, price=0, item_type="misc", description=description)
                except Exception:
                    return None
                _vt_condom_display_items[item_id] = obj
                return obj

            def vt_get_items_and_quantity(self):
                items = original_get_items_and_quantity(self)
                if self.condom_cheap_count > 0:
                    disp = _vt_condom_display_item(
                        "condoms", "BasicShield Condoms",
                        "_mods/content/elkrose_vt/extra_images/condom.png",
                        "Stored condoms. Equip them from the cherry indicator at the top of the screen.")
                    if disp is not None:
                        items.append((disp, self.condom_cheap_count))
                if self.condom_premium_count > 0:
                    disp = _vt_condom_display_item(
                        "condoms_premium", "UltraProtect Condoms",
                        "_mods/content/elkrose_vt/extra_images/condom_premium.png",
                        "Stored premium condoms. Equip them from the cherry indicator at the top of the screen.")
                    if disp is not None:
                        items.append((disp, self.condom_premium_count))
                # Virtual gift pills: reuse the real Gift objects from the shop database so the
                # give-gift menu shows them (is_giftable=True) with the correct accept chance and
                # effects. In the inventory screen they're Gifts (not ConsumableItems) -> no-op
                # click. The count comes from the sidecar; the Gift object itself is never stored
                # in anyone's inventory. Read-only: don't create sidecar keys during render.
                md = getattr(self, "mod_data", None)
                pill_counts = md.get(VT_MOD_ID, {}).get("pill_counts", {}) if md else {}
                if pill_counts:
                    gifts_db = getattr(renpy.store, "database_shop_items", {}).get("gifts", {})
                    # Once she AND the player both know she's pregnant, FertiBOOST is pointless,
                    # so don't even offer it for that girl. Scoped to the give-gift screen via
                    # selected_girl -- the plain inventory listing (no target girl) still shows
                    # owned pills. Read-only: getattr defaults avoid creating sidecar keys here.
                    hide_ferti = False
                    if renpy.get_screen("gift_selection_screen") is not None:
                        tgt = getattr(renpy.store, "selected_girl", None)
                        if tgt is not None and getattr(tgt, "pregnant", False) \
                                and getattr(tgt, "knows_pregnant", False) \
                                and getattr(tgt, "player_knows_pregnant", False):
                            hide_ferti = True
                    for pid, cnt in pill_counts.items():
                        if cnt > 0:
                            if pid == "fertility_pill" and hide_ferti:
                                continue
                            gift_obj = gifts_db.get(pid)
                            if gift_obj is not None:
                                items.append((gift_obj, cnt))
                return items

            vt_get_items_and_quantity._vt_addon = True
            Player.get_items_and_quantity = vt_get_items_and_quantity

        # Backfill/migrate on every load so a pre-mod/pre-sidecar save's Player is converted
        # to the sidecar before any gameplay runs.
        if vt_ensure_player_condom_attrs not in config.after_load_callbacks:
            config.after_load_callbacks.append(vt_ensure_player_condom_attrs)

        print("VT MOD: Player condom state moved to sidecar player.mod_data['elkrose_vt']")

    def trigger_npc_pregnancy(target_girl):
        """Handles pregnancy from NPC interactions"""
        if target_girl.pregnant or target_girl.just_had_baby:
            return False
        
        # Simplified fertility check for NPCs
        if renpy.random.randint(1, 100) < 15:  # 15% chance for NPC impregnation
            target_girl.pregnant = True
            try:
                target_girl.preg_start_day = time_manager.total_days
            except:
                target_girl.preg_start_day = 0
                renpy.log(f"VT MOD ERROR: preg_start_day failed because 'time_manager' is not defined for trigger_npc_pregnancy")
                return
            
            target_girl.preg_progress_days = 1
            target_girl.preg_end_day = target_girl.preg_start_day + 250 + renpy.random.randint(0, 10)
            target_girl.preg_father = "npc"  # Set father type to NPC
            renpy.log(f"VT MOD: {target_girl.first_name} got pregnant from an NPC!")
            return True
        return False

init -4 python:
    # Patch Mother class if it exists
    try:
        Mother = renpy.store.Mother
    except:
        pass
    else:
        original_mother_init = Mother.__init__
        original_mother_daily_update = Mother.daily_update

        def vt_mother_init(self, mother_config: GirlConfig, daughter: Girl):
            # ===== PHASE 1: MINIMAL VT ATTRIBUTES NEEDED FOR CORE GAME =====
            # Initialize ONLY attributes that are used in trait requirements
            # BEFORE core init (to prevent the previous error)
            vt_minimal_attributes = [
                'boob_cum_fetish', 'thigh_cum_fetish', 'ass_cum_fetish', 'pussy_cum_fetish',
                'oral_cum_fetish', 'vaginal_cum_fetish', 'anal_cum_fetish', 'baby_desire'
            ]
            
            for attr in vt_minimal_attributes:
                if not hasattr(self, attr):
                    setattr(self, attr, 0)
            
            original_mother_init(self, mother_config, daughter)
            
            # ===== RELATIONSHIP TRACKING SYSTEM =====
            # Initialize relationship-specific metrics (separate from personality traits)
            if not hasattr(self, 'player_relationship'):
                self.player_relationship = {
                    "control": 0,          # How much the player dominates the relationship
                    "greed": 0,            # Player's financial/material interest
                    "lust": 0,             # Player's sexual interest
                    "compassion": 0,       # Player's genuine care
                    "reputation": 0,       # Player's standing with this girl
                    "stage": "stranger",   # Current relationship stage
                    "stage_progress": 0,    # Progress toward next stage
                    "is_poly": False,
                    "path":"neutral"
                }
            if not hasattr(self, 'path_seeds'):
                self.path_seeds = {
                    "slave": 0,
                    "girlfriend": 0,
                    "fwb": 0,
                    "sugarbaby": 0,
                    "paramour": 0,
                    "mistress": 0
                }
            if not hasattr(self, 'initial_reaction'):
                self.initial_reaction = "neutral"
                
            # ===== TOP-3 STAT BOOSTING WITH TRAIT PRIORITIZATION =====
            # Get all core personality stats after traits have been applied
            stats = {
                "affection": self.affection,
                "corruption": self.corruption,
                "discipline": self.discipline,
                "fear": self.fear,
                "intellect": self.intellect,
                "naturism": self.naturism
            }
            
            # Calculate trait rarity bonus
            # trait_boost = 0
            # for trait in self.traits:
                # if trait.rarity <= 1.0:  # Legendary or better (Super-Legendary)
                    # trait_boost += 5
                # elif trait.rarity <= 2.0:  # Epic
                    # trait_boost += 3
                # elif trait.rarity <= 3.0:  # Rare
                    # trait_boost += 2
            
            # Identify stats that should be prioritized based on key traits
            prioritized_stats = set()
            
            # Check for traits that should guarantee stat boosting
            for trait in self.traits:
                if trait.name == "nympho":
                    prioritized_stats.add("corruption")
                    prioritized_stats.add("arousal")
                elif trait.name == "brilliant":
                    prioritized_stats.add("intellect")
                elif trait.name == "naturist":
                    prioritized_stats.add("naturism")
                elif trait.name == "rebellious":
                    prioritized_stats.add("discipline")  # Actually negative, but we want to emphasize it
                # Add other key trait mappings as needed
            
            # Sort stats by value (highest first)
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            
            # Get top 3 stats, but ensure prioritized stats are included if possible
            top_3_stats = []
            
            # First add prioritized stats that aren't already in top stats
            for stat_name, _ in sorted_stats:
                if stat_name in prioritized_stats:
                    top_3_stats.append(stat_name)
                    if len(top_3_stats) >= 3:
                        break
            
            # Then fill remaining slots with highest non-prioritized stats
            if len(top_3_stats) < 3:
                for stat_name, _ in sorted_stats:
                    if stat_name not in top_3_stats:
                        top_3_stats.append(stat_name)
                        if len(top_3_stats) >= 3:
                            break
            
            # Apply boosts to top 3 stats (with prioritization)
            for stat_name in top_3_stats:
                # base_boost = renrandom.randint(3, 5)
                # total_boost = base_boost + trait_boost
                # current_value = getattr(self, stat_name)
                # setattr(self, stat_name, min(100, current_value + total_boost))
                boost_multiplier = self.get_stat_growth_multiplier_for_stat(stat_name)
                true_multiplier = 2 + (boost_multiplier - girl_stat_growth_multipliers.get(stat_name, 1))
                base_boost = renrandom.randint(3, 5)
                total_boost = base_boost * true_multiplier
                current_value = getattr(self, stat_name)
                setattr(self, stat_name, min(100, current_value + total_boost))
            
            # Ensure stats stay within limits
            if hasattr(self, 'fix_stats'):
                self.fix_stats(hide_notification=True)
            # ===== END BOOSTING =====
            # ===== VIRGINITY & FIRST-TIME STATUS SYSTEM =====
            # Initialize all virginity/first-time attributes using our comprehensive system
            initialize_virginity_status(self)

            # Ensure consistency with other attributes
            if self.hymen:
                self.vaginal_sex_count = 0
                self.last_vaginal_sex = -1
            if self.first_time_oral:
                self.oral_sex_count = 0
                self.last_oral_sex = -1
            if self.first_time_anal:
                self.anal_sex_count = 0
                self.last_anal_sex = -1
            # External cumshot counts should reflect first-time status
            if self.first_time_boobs:
                self.boob_sex_count = 0
                self.last_boob_sex = -1
            if self.first_time_thighs:
                self.thigh_sex_count = 0
                self.last_thigh_sex = -1
            if self.first_time_ass_cumshot:
                self.ass_cumshot_count = 0
                self.last_ass_cumshot = -1
            if self.first_time_pussy_cumshot:
                self.pussy_cumshot_count = 0
                self.last_pussy_cumshot = -1
            # ===== END VIRGINITY SYSTEM =====
            
            # Mother-specific VT properties
            if not hasattr(self, 'oral_cum'):
                self.oral_cum = 0
            if not hasattr(self, 'vaginal_cum'):
                self.vaginal_cum = 0
            if not hasattr(self, 'anal_cum'):
                self.anal_cum = 0
            if not hasattr(self, 'oral_sex_count'):
                self.oral_sex_count = 0
            if not hasattr(self, 'last_oral_sex'):
                self.last_oral_sex = -1
            if not hasattr(self, 'vaginal_sex_count'):
                self.vaginal_sex_count = 0
            if not hasattr(self, 'last_vaginal_sex'):
                self.last_vaginal_sex = -1
            if not hasattr(self, 'anal_sex_count'):
                self.anal_sex_count = 0
            if not hasattr(self, 'last_anal_sex'):
                self.last_anal_sex = -1
            if not hasattr(self, 'first_time_oral'):
                self.first_time_oral = True
            if not hasattr(self, 'first_time_pussy'):
                self.first_time_pussy = True
            if not hasattr(self, 'first_time_anal'):
                self.first_time_anal = True
            if not hasattr(self, 'aware_vaginal_condom'):
                self.aware_vaginal_condom = False
            if not hasattr(self, 'aware_oral_condom'):
                self.aware_oral_condom = False
            if not hasattr(self, 'aware_anal_condom'):
                self.aware_anal_condom = False
            if not hasattr(self, 'oral_cum_fetish'):
                self.oral_cum_fetish = get_cum_fetish_level(self, "oral")
            if not hasattr(self, 'vaginal_cum_fetish'):
                self.vaginal_cum_fetish = get_cum_fetish_level(self, "vaginal")
            if not hasattr(self, 'anal_cum_fetish'):
                self.anal_cum_fetish = get_cum_fetish_level(self, "anal")
            if not hasattr(self, 'baby_desire'):
                self.baby_desire = get_baby_desire(self)
            
            # WITH these lines:
            if not hasattr(self, 'hymen'):
                self.hymen = False  # Mothers never have hymen
            if not hasattr(self, 'kids'):
                self.kids = max(1, getattr(self, 'kids', 1))  # Total children
            if not hasattr(self, 'kids_with_player'):
                self.kids_with_player = 0  # Only children from player
            if not hasattr(self, 'kids_with_npc'):
                self.kids_with_npc = 1  # mother had daughter with someone (unknown npc)
            if not hasattr(self, 'original_daughter'):
                self.original_daughter = (self.kids > 0)  # Flag for base mother's original daughter
            if not hasattr(self, 'preg_father'):
                self.preg_father = None  # Will be "player", "npc", or None if not pregnant
            
            #active sex tracking
            if not hasattr(self, 'had_sex_today'):
                self.had_sex_today = False
            if not hasattr(self, 'having_oral_sex'):
                self.having_oral_sex = False
            if not hasattr(self, 'having_vaginal_sex'):
                self.having_vaginal_sex = False
            
            if not hasattr(self, 'boob_cum_fetish'):
                self.boob_cum_fetish = get_cum_fetish_level(self, "boobs")
            if not hasattr(self, 'boob_sex_count'):
                self.boob_sex_count = 0
            if not hasattr(self, 'last_boob_sex'):
                self.last_boob_sex = -1
            if not hasattr(self, 'first_time_boobs'):
                self.first_time_boobs = True
            if not hasattr(self, 'aware_boob_condom'):
                self.aware_boob_condom = False

            if not hasattr(self, 'thigh_cum_fetish'):
                self.thigh_cum_fetish = get_cum_fetish_level(self, "thighs")
            if not hasattr(self, 'thigh_sex_count'):
                self.thigh_sex_count = 0
            if not hasattr(self, 'last_thigh_sex'):
                self.last_thigh_sex = -1
            if not hasattr(self, 'first_time_thighs'):
                self.first_time_thighs = True
            if not hasattr(self, 'aware_thigh_condom'):
                self.aware_thigh_condom = False
            
            if not hasattr(self, 'ass_cum_fetish'):
                self.ass_cum_fetish = get_cum_fetish_level(self, "ass_cum")
            if not hasattr(self, 'ass_cumshot_count'):
                self.ass_cumshot_count = 0
            if not hasattr(self, 'last_ass_cumshot'):
                self.last_ass_cumshot = -1
            if not hasattr(self, 'first_time_ass_cumshot'):
                self.first_time_ass_cumshot = True
            if not hasattr(self, 'aware_ass_cumshot_condom'):
                self.aware_ass_cumshot_condom = False
            
            if not hasattr(self, 'pussy_cum_fetish'):
                self.pussy_cum_fetish = get_cum_fetish_level(self, "pussy_cum")
            if not hasattr(self, 'impreg_fetish'):
                self.impreg_fetish = 0
            if not hasattr(self, 'pussy_cumshot_count'):
                self.pussy_cumshot_count = 0
            if not hasattr(self, 'last_pussy_cumshot'):
                self.last_pussy_cumshot = -1
            if not hasattr(self, 'first_time_pussy_cumshot'):
                self.first_time_pussy_cumshot = True
            if not hasattr(self, 'aware_pussy_cumshot_condom'):
                self.aware_pussy_cumshot_condom = False
            
            # Mother birth control (lower usage)
            if not hasattr(self, 'bc_chance'):
                self.bc_chance = 100
            if not hasattr(self, 'birth_control'):
                self.birth_control = renpy.random.randint(0, 100) < 10
            if not hasattr(self, 'bc_status_known'):
                self.bc_status_known = False
            if not hasattr(self, 'bc_penalty'):
                self.bc_penalty = 0

            # Mother fertility (lower)
            self.fertility_percent = 5.0  # Ensure Mother has fertility_percent
            if not hasattr(self, 'ideal_fertile_day'):
                self.ideal_fertile_day = renpy.random.randint(0, 30)
            if not hasattr(self, 'baby_desire'):
                self.baby_desire = 100 - renpy.random.randint(0, 100)
            
            # Conversation Tracking System
            if not hasattr(self, 'has_met_before'):
                self.has_met_before = False
            if not hasattr(self, 'has_discussed_pregnancy_before'):
                self.has_discussed_pregnancy_before = False
            if not hasattr(self, 'has_discussed_birth_control_before'):
                self.has_discussed_birth_control_before = False
            if not hasattr(self, 'has_discussed_condoms_before'):
                self.has_discussed_condoms_before = False
            
            #Condoms
            if not hasattr(self, 'player_knows_vaginal_condom'):
                self.player_knows_vaginal_condom = False
            if not hasattr(self, 'player_knows_anal_condom'):
                self.player_knows_anal_condom = False
            if not hasattr(self, 'player_knows_oral_condom'):
                self.player_knows_oral_condom = False
            if not hasattr(self, 'player_knows_body_condom'):
                self.player_knows_body_condom = False
            if not hasattr(self, 'wants_vaginal_condom'):
                self.wants_vaginal_condom = wants_condom(self, "vaginal")
            if not hasattr(self, 'wants_anal_condom'):
                self.wants_anal_condom = wants_condom(self, "anal")
            if not hasattr(self, 'wants_oral_condom'):
                self.wants_oral_condom = wants_condom(self, "oral")
            if not hasattr(self, 'wants_body_condom'):
                self.wants_body_condom = wants_condom(self, "body")

            # Pregnancy tracking
            if not hasattr(self, 'pregnant'):
                self.pregnant = False
            if not hasattr(self, 'preg_body'):
                self.preg_body = False
            if not hasattr(self, 'knows_pregnant'):
                self.knows_pregnant = False
            if not hasattr(self, 'player_knows_pregnant'):
                self.player_knows_pregnant = False
            if not hasattr(self, 'preg_progress_days'):
                self.preg_progress_days = 0
            if not hasattr(self, 'preg_start_day'):
                self.preg_start_day = 0
            if not hasattr(self, 'preg_end_day'):
                self.preg_end_day = 0
            if not hasattr(self, 'preg_announce'):
                self.preg_announce = False
            if not hasattr(self, 'days_since_last_birth'):
                self.days_since_last_birth = 0
            if not hasattr(self, 'just_had_baby'):
                self.just_had_baby = False
            if not hasattr(self, 'pregnancy_phase'):
                self.pregnancy_phase = 0
            # Add fertility boost attribute
            if not hasattr(self, 'fertility_boost'):
                self.fertility_boost = 0  # Days remaining for fertility boost
            if not hasattr(self, 'prenatal_boost'):
                self.prenatal_boost = 0  # PregnaVITA supply: pills on hand, taken 1/week
            if not hasattr(self, 'prenatal_doses'):
                self.prenatal_doses = 0  # PregnaVITA doses taken (compression factor, capped)

            #Followup triggers
            if not hasattr(self, 'has_pregnancy_followup'):
                self.has_pregnancy_followup = False
            if not hasattr(self, 'has_birth_control_followup'):
                self.has_birth_control_followup = False
            if not hasattr(self, 'has_condoms_followup'):
                self.has_condoms_followup = False
            if not hasattr(self, 'has_corruption_followup'):
                self.has_corruption_followup = False
            if not hasattr(self, 'has_naturism_followup'):
                self.has_naturism_followup = False
            if not hasattr(self, 'has_fear_followup'):
                self.has_fear_followup = False
            if not hasattr(self, 'has_blowjob_followup'):
                self.has_blowjob_followup = False
            if not hasattr(self, 'has_strip_tease_followup'):
                self.has_strip_tease_followup = False
            if not hasattr(self, 'has_get_dressed_followup'):
                self.has_get_dressed_followup = False
            if not hasattr(self, 'has_strip_to_underwear_followup'):
                self.has_strip_to_underwear_followup = False
            if not hasattr(self, 'has_naked_followup'):
                self.has_naked_followup = False
            if not hasattr(self, 'has_milk_followup'):
                self.has_milk_followup = False
            if not hasattr(self, 'has_creamer_followup'):
                self.has_creamer_followup = False
            if not hasattr(self, 'has_toppings_followup'):
                self.has_toppings_followup = False
            if not hasattr(self, 'has_small_talk_followup'):
                self.has_small_talk_followup = False
            if not hasattr(self, 'has_masturbation_tips_followup'):
                self.has_masturbation_tips_followup = False
            if not hasattr(self, 'has_shower_sex_followup'):
                self.has_shower_sex_followup = False

            # Initialize the sidecar-migrated keys (relationship, etc.) for mothers too.
            # Runs last so the inline loose inits above are untouched; vt_ensure_girl_attrs'
            # hasattr guards skip the still-loose attrs and only fills the sidecar bucket.
            vt_ensure_girl_attrs(self)

            #original_mother_init(self, mother_config, daughter)

        #Followup triggers
        def trigger_pregnancy_followup(self):
            self.has_pregnancy_followup = True
            renpy.log(f"Pregnancy follow-up triggered for {self.first_name}")
            
        def trigger_birth_control_followup(self):
            self.has_birth_control_followup = True
            renpy.log(f"Birth Control follow-up triggered for {self.first_name}")
            
        def trigger_condoms_followup(self):
            self.has_condoms_followup = True
            renpy.log(f"Condoms follow-up triggered for {self.first_name}")

        def trigger_corruption_followup(self):
            self.has_corruption_followup = True
            self.corruption = min(100, self.corruption + 3)
            renpy.log(f"Corruption follow-up triggered for {self.first_name}")

        def trigger_naturism_followup(self):
            self.has_naturism_followup = True
            self.naturism = min(100, self.naturism + 3)
            renpy.log(f"Naturism follow-up triggered for {self.first_name}")
            
        def trigger_fear_followup(self):
            self.has_fear_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Fear follow-up triggered for {self.first_name}")

        def trigger_blowjob_followup(self):
            self.has_blowjob_followup = True
            vt_handle_cum_fetishes("blowjob", self, "oral")
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Blowjob follow-up triggered for {self.first_name}")
        
        def trigger_strip_tease_followup(self):
            self.has_strip_tease_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Strip tease follow-up triggered for {self.first_name}")

        def trigger_get_dressed_followup(self):
            self.has_get_dressed_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Get dressed follow-up triggered for {self.first_name}")

        def trigger_strip_to_underwear_followup(self):
            self.has_strip_to_underwear_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Strip to underwear follow-up triggered for {self.first_name}")

        def trigger_naked_followup(self):
            self.has_naked_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Naked follow-up triggered for {self.first_name}")

        def trigger_milk_followup(self):
            self.has_milk_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Milk follow-up triggered for {self.first_name}")

        def trigger_creamer_followup(self):
            self.has_creamer_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Creamer follow-up triggered for {self.first_name}")

        def trigger_toppings_followup(self):
            self.has_toppings_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Toppings follow-up triggered for {self.first_name}")

        def trigger_small_talk_followup(self):
            self.has_small_talk_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Small_talk Teacher follow-up triggered for {self.first_name}")

        def trigger_masturbation_tips_followup(self):
            self.has_masturbation_tips_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Masturbation tips follow-up triggered for {self.first_name}")

        def trigger_shower_sex_followup(self):
            self.has_shower_sex_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Shower sex follow-up triggered for {self.first_name}")

        # Apply the same property definitions to Mother
        def days_from_ideal_fertility(self, with_direction=False):
            """
            Returns days from ideal fertile day
            Negative = before ideal day, Positive = after ideal day
            Example: -2 = 2 days before ovulation, +1 = 1 day after ovulation
            """
            # Safely access time_manager
            cycle_day = 0
            try:
                cycle_day = time_manager.total_days % 30
            except NameError:
                # This should not happen if game_init.rpy is loaded correctly
                renpy.log("days_from_ideal_fertility ERROR: Global 'time_manager' variable not found!")
                return
                
            day_difference = cycle_day - self.ideal_fertile_day
            
            # Normalize to -15 to +14 range
            if day_difference > 15:
                day_difference -= 30
            elif day_difference < -15:
                day_difference += 30
                
            return day_difference if with_direction else abs(day_difference)

        def on_birth_control(self):
            return self.fertility_percent < 0 or self.birth_control

        def is_highly_fertile(self):
            if self.pregnant:
                return False
            # Get the signed difference, just like effective_fertility does
            day_diff = self.days_from_ideal_fertility(with_direction=True)
            
            # Define the fertile window based on the FERTILITY_CURVE
            # We'll consider anything above 10% of base fertility as "highly fertile"
            FERTILE_WINDOW = [-3, -2, -1, 0, 1]
            
            if day_diff in FERTILE_WINDOW:
                return True
                
            return False

        def effective_fertility(self):
            if self.fertility_percent < 0:
                return 0
                
            # Get signed difference (negative = before ideal day, positive = after)
            day_diff = self.days_from_ideal_fertility(with_direction=True)
            
            # FERTILITY CURVE BASED ON MEDICAL RESEARCH (NEJM)
            # Key: days from ovulation (negative = before, positive = after)
            # Value: percentage of BASE fertility (1.0 = 100%)
            FERTILITY_CURVE = {
                -5: 0.10,   # 5 days before: 10% of base
                -4: 0.20,   # 4 days before: 20% of base
                -3: 0.40,   # 3 days before: 40% of base
                -2: 0.75,   # 2 days before: 75% of base
                -1: 0.90,   # 1 day before: 90% of base
                0:  1.00,   # Ovulation day: 100% of base (PEAK)
                1:  0.40,   # 1 day after: 40% of base
            }
            
            # Get multiplier for current position in cycle
            multiplier = FERTILITY_CURVE.get(day_diff, 0.01)  # 1% outside fertile window
            
            # Check if boost is active and apply it additively to the base fertility
            if self.fertility_boost > 0:
                # Add 25 to the base fertility, then apply the day's multiplier
                base_fertility = (self.fertility_percent + 25) * multiplier
            else:
                # No boost, use the normal base fertility
                base_fertility = self.fertility_percent * multiplier
            
            return base_fertility

        def birthcontrol_efficiency(self):
            if not self.on_birth_control():
                return 0
            return max(100 - self.bc_penalty, 0)

        def pregnancy_chance(self):
            if self.effective_fertility() <= 0:  # NO PARENTHESES!
                return 0
            return (self.effective_fertility() / 100) * (100 - self.birthcontrol_efficiency())  # NO PARENTHESES!

        def apply_prenatal_boost(self):
            # Consume one PregnaVITA dose (called from the weekly tick). Gated: only if
            # pregnant, she knows, she has supply (prenatal_boost), and she is below the dose
            # ceiling. Each dose raises the daily progress speed (1 + doses) and pulls the due
            # date in -- no progress jump; compression happens via the daily speed.
            if not self.pregnant or not self.knows_pregnant:
                return
            if self.prenatal_boost <= 0 or getattr(self, 'prenatal_doses', 0) >= VT_PRENATAL_DOSE_CEILING:
                return

            current_day = 0
            try:
                current_day = time_manager.total_days
            except NameError:
                renpy.log(f"VT MOD ERROR: apply_prenatal_boost failed because 'time_manager' is not defined for {self.first_name}.")
                return

            self.prenatal_doses = getattr(self, 'prenatal_doses', 0) + 1
            self.prenatal_boost -= 1   # consume one pill from supply

            speed = 1 + min(self.prenatal_doses, VT_PRENATAL_DOSE_CEILING)
            remaining = max(VT_MIN_PREG_DAYS_LEFT, ((260 - self.preg_progress_days) + speed - 1) // speed)
            self.preg_end_day = current_day + remaining

            vt_preg_notify(f"{self.first_name} took PregnaVITA (dose {self.prenatal_doses}/{VT_PRENATAL_DOSE_CEILING}) - pregnancy accelerating.", duration=3.0)
            renpy.log(f"VT MOD: {self.first_name} PregnaVITA dose {self.prenatal_doses}, speed {speed}x, due day {self.preg_end_day}")

        # Create patched daily_update
        def vt_mother_daily_update(self):
            original_mother_daily_update(self)

            #reset stats
            self.had_sex_today = False
            self.having_oral_sex = False
            self.having_vaginal_sex = False
            
            # Fertility boost countdown
            if self.fertility_boost > 0:
                self.fertility_boost -= 1

            # Anal and Oral, all cum is gone by next day
            # technically doesn't really matter, as its more of a temp visual for the day.
            if self.oral_cum > 0:
                self.oral_cum = 0
            if self.anal_cum > 0:
                    self.anal_cum = 0

            # Pregnancy logic
            if self.vaginal_cum > 0:
                #regardless of cum stats the most sperm will live in the womb is 3-5 days, therefore max 3 units will remain regardless, it should still satisfy the 'inflation' cum kinks. This is to help with the 'sperm typically can stay alve for about 3 to 5 days', so I choosed 3 days for game purposes.
                if self.vaginal_cum >4:
                    self.vaginal_cum = 4
                
                if self.hymen:
                    self.hymen = False

                # Pregnancy check - only check if not already pregnant and not in postpartum period
                if not self.pregnant and not self.just_had_baby and self.vaginal_cum >= 0:
                    # Birth control failed to prevent the pregnancy
                    if renpy.random.randint(1, 100) > self.birthcontrol_efficiency():
                        # There's a chance she's pregnant based on effective fertility
                        if renpy.random.randint(1, 100) <= self.effective_fertility():
                            self.pregnant = True
                            self.knows_pregnant = False
                            self.player_knows_pregnant = False
                            # Track when this happened - SAFELY
                            self.preg_start_day = 0
                            try:
                                self.preg_start_day = time_manager.total_days
                            except NameError:
                                # This should not happen if game_init.rpy is loaded correctly
                                renpy.log("vt_mother_daily_update # Pregnancy check  ERROR: Global 'time_manager' variable not found!")
                                return
                            self.preg_progress_days = 1
                            self.pregnancy_phase = 1
                            self.preg_announce = False
                            self.days_since_last_birth = 0
                            self.preg_end_day = self.preg_start_day + (260 - self.preg_progress_days)
                            
                            # SET FATHER TYPE - CRITICAL ADDITION
                            self.preg_father = "player"  # This pregnancy is from the player
                            self.prenatal_doses = 0  # fresh pregnancy: no meds yet
                            self.prenatal_boost = 0  # no pill supply yet
                            
                            vt_preg_notify(f"{self.first_name} might be pregnant!", duration=3)

                #remove cum after preg check.
                self.vaginal_cum -= 1

            # Pregnancy progression
            if self.pregnant:
                speed = 1 + min(getattr(self, 'prenatal_doses', 0), VT_PRENATAL_DOSE_CEILING)
                self.preg_progress_days += speed
                
                # (PregnaVITA dosing moved to the weekly tick -- see vt_*_weekly_update.)
                
                current_day = 0
                try:
                    current_day = time_manager.total_days
                except NameError:
                    # This should not happen if game_init.rpy is loaded correctly
                    renpy.log("vt_mother_daily_update # Pregnancy progression ERROR: Global 'time_manager' variable not found!")
                    return
                # Awareness: a fixed real-day delay after conception, independent of meds;
                # latches regardless of trimester band (fixes the old prenatal-boost skip).
                if (current_day - self.preg_start_day) >= VT_KNOWS_AFTER_DAYS:
                    self.knows_pregnant = True
                    self.birth_control = False

                # Pregnancy ended - baby born
                if self.preg_progress_days >= 260:
                    # Increment appropriate counter based on father type
                    if self.preg_father == "player":
                        self.kids_with_player += 1
                        renpy.log(f"VT MOD: {self.first_name} gave birth to player's baby! Total player kids: {self.kids_with_player}")
                    elif self.preg_father == "npc":
                        self.kids_with_npc += 1
                        renpy.log(f"VT MOD: {self.first_name} gave birth to NPC's baby! Total NPC kids: {self.kids_with_npc}")
                    
                    # Always increment total kids count
                    self.kids += 1
                    
                    # Reset pregnancy state
                    self.preg_end_day = 0
                    self.pregnancy_phase = 0
                    self.pregnant = False
                    self.just_had_baby = True
                    self.days_since_last_birth = 1
                    self.preg_father = None  # Clear father type after birth
                    self.prenatal_doses = 0  # clear meds acceleration
                    self.prenatal_boost = 0  # clear leftover pill supply
                  # Visible pregnancy body after 30 days
                # After 30 weeks, she will start showing third trimester, very obvious now
                elif self.preg_progress_days >= 210:
                    self.pregnancy_phase = 3
                    self.preg_body = True
                # After 15 weeks, she will start showing second trimester, kind of obvious now
                elif self.preg_progress_days >= 105:
                    self.pregnancy_phase = 2
                    self.preg_body = True
                # After 7 weeks, she will start showing first trimester but can still hide pregnancy
                elif self.preg_progress_days >= 35:
                    self.pregnancy_phase = 1
                    #self.preg_body = True
                # After 2 days, she will know if she's pregnant and in her first trimester
                elif self.preg_progress_days >= 2:
                    self.pregnancy_phase = 1
                    self.knows_pregnant = True
                    self.birth_control = False

            # Post-birth cooldown
            if self.just_had_baby:
                self.days_since_last_birth += 1
                if self.days_since_last_birth >= 14:
                    # Time to determine birth control decision based on multiple factors
                    # BASE CHANCE CALCULATION (0-100%)
                    bc_chance = 0
                    # 1. Baby desire (MOST IMPORTANT FACTOR)
                    # Low desire = high BC chance, High desire = low BC chance
                    bc_chance += (100 - self.baby_desire)  # Inverse relationship
                    # 2. Number of kids (SECOND MOST IMPORTANT)
                    # Each additional kid increases BC likelihood significantly
                    kids_factor = max(0, self.kids - 1) * 25  # +25% per child beyond first
                    bc_chance += min(kids_factor, 50)  # Cap at +50% for multiple kids
                    # 3. Intellect (educated decision-making)
                    if hasattr(self, 'intellect'):
                        bc_chance += min(self.intellect // 3, 20)  # Up to +20% for high intellect
                    # 4. Corruption (strategic thinking)
                    if hasattr(self, 'corruption') and self.corruption > 70:
                        bc_chance += 15  # Strategic BC use for high corruption
                    # 5. Naturism (natural body acceptance)
                    if hasattr(self, 'naturism') and self.naturism > 70:
                        bc_chance -= 25  # Strong naturalists resist BC
                    # 6. Fear factor (anxiety about more pregnancy)
                    if hasattr(self, 'fear') and self.fear > 70:
                        bc_chance += 20  # Fearful women seek protection
                    # 7. Special case: Mothers vs Students
                    bc_chance += 10  # Mothers more likely to use BC after multiple births
                    # CLAMP FINAL CHANCE (0-100%)
                    bc_chance = max(10, min(90, bc_chance))  # Ensure some randomness remains
                    # MAKE DECISION
                    will_use_bc = (renpy.random.randint(1, 100) <= bc_chance)
                    # Apply decision - CRITICAL: bc_status_known remains FALSE (player doesn't know yet)
                    self.birth_control = will_use_bc
                    self.bc_status_known = False  # PLAYER DOESN'T KNOW HER BC STATUS YET
                    self.bc_penalty = 0  # Reset penalty after birth (new cycle)
                    
                    # LOG THE DECISION FOR DEBUGGING
                    if will_use_bc:
                        renpy.log(f"VT MOD: {self.first_name} (kids={self.kids}) decided to use birth control after birth (chance={bc_chance}%)")
                        # Player doesn't get notification - they don't know yet
                    else:
                        renpy.log(f"VT MOD: {self.first_name} (kids={self.kids}) chose NOT to use birth control after birth (chance={bc_chance}%)")
                        # Player doesn't get notification - they don't know yet
                    # Reset post-birth state
                    self.just_had_baby = False
                    self.days_since_last_birth = 0
                    self.preg_body = False
                    # Add subtle visual/textual hint that she might be on BC or not
                    # (Player will need to discover through dialogue)
                    self.bc_chance = 100 if will_use_bc else 0

        def get_fertility_day_status(self):
            """
            Returns a user-friendly string describing the current day in the fertility cycle.
            """
            cycle_day = self.get_cycle_day()
            menstrual_duration = 5

            # Check for the menstrual phase first
            if 1 <= cycle_day <= menstrual_duration:
                return "She is on her moon time... be nice"

            # Get signed difference (negative = before ideal day, positive = after)
            day_diff = self.days_from_ideal_fertility(with_direction=True)

            if day_diff == 0:
                return "Peak Ovulation Day!"
            elif 1 <= day_diff <= 3: # A few days after peak
                return f"{day_diff} day(s) past ovulation"
            elif -3 <= day_diff <= -1: # A few days before peak
                return f"{abs(day_diff)} day(s) before ovulation"
            elif -5 <= day_diff <= -4: # Early fertile window
                return "High fertility window!"
            else: # Outside the main window
                return "Low fertility"
        
        def get_cycle_day(self):
            """
            Returns the current day of the 30-day menstrual cycle (1-30).
            Day 1 is the first day after ovulation.
            """
            total_days = 0  # Initialize to a default value
            
            try:
                # Use the global 'time_manager' instance that was created in game_init.rpy
                total_days = time_manager.total_days
            except NameError:
                # This should not happen if game_init.rpy is loaded correctly
                renpy.log("get_cycle_day ERROR: Global 'time_manager' variable not found!")
                return 1

            ideal_day = self.ideal_fertile_day
            menstrual_duration = 5
            follicular_duration = 7
            
            ov_start_day = (ideal_day - 3 + 30) % 30
            cycle_start_day = (ov_start_day - follicular_duration - menstrual_duration + 30) % 30
            
            current_day = total_days % 30
            if current_day == 0: current_day = 30
            
            # The cycle day is the number of days from the start of the cycle
            days_from_cycle_start = (current_day - cycle_start_day + 30) % 30
            if days_from_cycle_start == 0: days_from_cycle_start = 30
            
            return days_from_cycle_start

            # if total_days > 0:
                # # --- DEBUGGING LINES ---
                # renpy.log(f"get_cycle_day DEBUG: total_days={total_days}, ideal_fertile_day={self.ideal_fertile_day}")
                
                # # Find the most recent ovulation day relative to the current game day
                # days_since_ovulation = (total_days - self.ideal_fertile_day) % 30

                # # --- DEBUGGING LINES ---
                # renpy.log(f"get_cycle_day DEBUG: days_since_ovulation={days_since_ovulation}")

                # # In a 30-day cycle, ovulation happens on day (30 - 14) = 16.
                # # The cycle starts the day after ovulation.
                # cycle_day = (16 + days_since_ovulation) % 30
                
                # # --- DEBUGGING LINES ---
                # renpy.log(f"get_cycle_day DEBUG: cycle_day before 0-check={cycle_day}")

                # # The modulo operator can result in 0, so we correct it to be 1-30.
                # if cycle_day == 0:
                    # cycle_day = 30
                    
                # # --- DEBUGGING LINES ---
                # renpy.log(f"get_cycle_day DEBUG: Final cycle_day={cycle_day}")
                # return cycle_day
            # else:
                # renpy.log("get_cycle_day: total_days was 0 or less.")
                # # Fallback in case total_days was not set for any reason
                # return 1
                
            

        #Relationals
        def vt_relationship_change(self, attribute, amount):
            previous_amount = self.player_relationship[attribute]
            self.player_relationship[attribute] = max(-20, min(100, previous_amount + amount)) 

        def vt_seed_relationship_path(self, path, amount):
            previous_amount = self.path_seeds[path]
            # girl.path_seeds = {"slave": 0, "girlfriend": 0, "fwb": 0, "sugarbaby": 0}
            self.path_seeds[path] = max(-20, min(100, previous_amount + amount))

        # Apply patches to Mother
        Mother.__init__ = vt_mother_init
        Mother.daily_update = vt_mother_daily_update

        # Patched weekly_update (mothers): same weekly PregnaVITA dosing, awareness-gated.
        original_mother_weekly_update = Mother.weekly_update
        def vt_mother_weekly_update(self):
            original_mother_weekly_update(self)
            if self.pregnant:
                try:
                    _cd = time_manager.total_days
                except NameError:
                    _cd = 0
                if _cd and (_cd - self.preg_start_day) >= VT_KNOWS_AFTER_DAYS:
                    self.knows_pregnant = True
                    self.birth_control = False
                self.apply_prenatal_boost()
        Mother.weekly_update = vt_mother_weekly_update
        Mother.days_from_ideal_fertility = days_from_ideal_fertility
        Mother.on_birth_control = on_birth_control
        Mother.is_highly_fertile = is_highly_fertile
        Mother.effective_fertility = effective_fertility
        Mother.birthcontrol_efficiency = birthcontrol_efficiency
        Mother.pregnancy_chance = pregnancy_chance
        Mother.apply_prenatal_boost = apply_prenatal_boost
        Mother.days_from_ideal_fertility = consistent_days_from_ideal_fertility
        Mother.trigger_pregnancy_followup = trigger_pregnancy_followup
        Mother.trigger_birth_control_followup = trigger_birth_control_followup
        Mother.trigger_condoms_followup = trigger_condoms_followup
        Mother.trigger_corruption_followup = trigger_corruption_followup
        Mother.trigger_naturism_followup = trigger_naturism_followup
        Mother.trigger_fear_followup = trigger_fear_followup
        Mother.trigger_blowjob_followup = trigger_blowjob_followup
        Mother.trigger_strip_tease_followup = trigger_strip_tease_followup
        Mother.trigger_get_dressed_followup = trigger_get_dressed_followup
        Mother.trigger_naked_followup = trigger_naked_followup
        Mother.trigger_milk_followup = trigger_milk_followup
        Mother.trigger_creamer_followup = trigger_creamer_followup
        Mother.trigger_toppings_followup = trigger_toppings_followup
        Mother.trigger_small_talk_followup = trigger_small_talk_followup
        Mother.trigger_masturbation_tips_followup = trigger_masturbation_tips_followup
        Mother.trigger_shower_sex_followup = trigger_shower_sex_followup
        Mother.get_fertility_day_status = get_fertility_day_status
        Mother.get_cycle_day = get_cycle_day
        Mother.vt_relationship_change = vt_relationship_change
        Mother.vt_seed_relationship_path = vt_seed_relationship_path
        print("VT MOD: Fixed Mother fertility to match medical reality")

init -4 python:
    # Patch GirlManager to ensure Mother instances are correctly initialized
    try:
        GirlManager = renpy.store.GirlManager
    except:
        pass
    else:
        original_create_new_girl = GirlManager._create_new_girl

        def vt_create_new_girl(self, girl_config: Union[GirlConfig, None] = None, allow_random=True) -> Union[Girl, None]:
            new_girl = original_create_new_girl(self, girl_config, allow_random)
            if new_girl and isinstance(new_girl, Mother):
                # Ensure Mother instances are initialized with fertility_percent
                new_girl.fertility_percent = getattr(new_girl, 'fertility_percent', 5.0)
            return new_girl

        GirlManager._create_new_girl = vt_create_new_girl
        print("VT MOD: Patched GirlManager to ensure Mother instances are correctly initialized")

init -14 python:
    # Patch Girl class directly
    try:
        Girl = renpy.store.Girl
    except:
        pass
    else:
        # Save original methods
        original_girl_init = Girl.__init__
        original_daily_update = Girl.daily_update

        # ===== PregnaVITA / pregnancy tuning knobs =====
        VT_PRENATAL_DOSE_CEILING = 4   # max stacked doses (max speed = 1 + this = 5x)
        VT_KNOWS_AFTER_DAYS = 10       # real days after conception before she knows (girl & mother)
        VT_MIN_PREG_DAYS_LEFT = 1      # floor on the derived due date after a dose

        # Shared, idempotent backfill of every VT attribute. Called from __init__ (for
        # newly created girls) AND from the after-load backfill loop (for girls in saves
        # created before the mod was installed -- mid-save install). Every assignment is
        # hasattr-guarded, so it never clobbers existing values and is safe to call
        # repeatedly. Mother-aware: mothers diverge from students on a handful of defaults.
        def vt_girl_bucket(self):
            # Return (creating if needed) this mod's primitives-only sidecar dict on a girl.
            md = getattr(self, "mod_data", None)
            if md is None:
                md = {}
                self.mod_data = md
            return md.setdefault("elkrose_vt", {})

        def vt_ensure_girl_attrs(self):
            is_mother = is_mother_character(self)
            bucket = vt_girl_bucket(self)

            # ----- Sidecar-migrated keys -----
            # Migrate any loose copies (from pre-sidecar saves) into the bucket, then strip
            # them so the property accessors govern. This list grows as later batches move
            # more attributes into the sidecar.
            for _k in VT_GIRL_SIDECAR_KEYS:
                if _k in self.__dict__:
                    bucket.setdefault(_k, self.__dict__[_k])
                    del self.__dict__[_k]

            # ===== RELATIONSHIP TRACKING SYSTEM (sidecar) =====
            if "player_relationship" not in bucket:
                bucket["player_relationship"] = {
                    "control": 0,          # How much the player dominates the relationship
                    "greed": 0,            # Player's financial/material interest
                    "lust": 0,             # Player's sexual interest
                    "compassion": 0,       # Player's genuine care
                    "reputation": 0,       # Player's standing with this girl
                    "stage": "stranger",   # Current relationship stage
                    "stage_progress": 0,    # Progress toward next stage
                    "is_poly": False,
                    "path":"neutral"
                }
            if "path_seeds" not in bucket:
                bucket["path_seeds"] = {
                    "slave": 0,
                    "girlfriend": 0,
                    "fwb": 0,
                    "sugarbaby": 0,
                    "paramour": 0,
                    "mistress": 0
                }
            if "initial_reaction" not in bucket:
                bucket["initial_reaction"] = "neutral"

            # Initialize VT properties with proper defaults
            if "oral_cum" not in bucket:
                bucket["oral_cum"] = 0
            if "vaginal_cum" not in bucket:
                bucket["vaginal_cum"] = 0
            if "anal_cum" not in bucket:
                bucket["anal_cum"] = 0
            if "oral_sex_count" not in bucket:
                bucket["oral_sex_count"] = 0
            if "last_oral_sex" not in bucket:
                bucket["last_oral_sex"] = -1
            if "vaginal_sex_count" not in bucket:
                bucket["vaginal_sex_count"] = 0
            if "last_vaginal_sex" not in bucket:
                bucket["last_vaginal_sex"] = -1
            if "anal_sex_count" not in bucket:
                bucket["anal_sex_count"] = 0
            if "last_anal_sex" not in bucket:
                bucket["last_anal_sex"] = -1
            if "first_time_oral" not in bucket:
                bucket["first_time_oral"] =  True
            if "first_time_pussy" not in bucket:
                bucket["first_time_pussy"] =  True
            if "first_time_anal" not in bucket:
                bucket["first_time_anal"] =  True
            if "aware_vaginal_condom" not in bucket:
                bucket["aware_vaginal_condom"] = False
            if "aware_oral_condom" not in bucket:
                bucket["aware_oral_condom"] = False
            if "aware_anal_condom" not in bucket:
                bucket["aware_anal_condom"] = False
            if "oral_cum_fetish" not in bucket:
                bucket["oral_cum_fetish"] = get_cum_fetish_level(self, "oral")
            if "vaginal_cum_fetish" not in bucket:
                bucket["vaginal_cum_fetish"] = get_cum_fetish_level(self, "vaginal")
            if "anal_cum_fetish" not in bucket:
                bucket["anal_cum_fetish"] = get_cum_fetish_level(self, "anal")
            if "baby_desire" not in bucket:
                bucket["baby_desire"] = get_baby_desire(self)  # Start with baseline baby desire
            if "baby_desire_xp" not in bucket:
                bucket["baby_desire_xp"] = 0  # XP companion so baby_desire levels like a base stat
            # Heal saves from before baby_desire was XP-backed: the old apply_impacts write-path
            # could push the level past 100. Re-seed from traits+corruption so the now-XP-backed
            # stat starts from a sane level instead of a stuck max.
            if bucket["baby_desire"] > 100:
                bucket["baby_desire"] = get_baby_desire(self)
                bucket["baby_desire_xp"] = 0

            if "hymen" not in bucket:
                bucket["hymen"] = False if is_mother else True
            if "kids" not in bucket:
                bucket["kids"] = 1 if is_mother else 0  # Total children
            if "kids_with_player" not in bucket:
                bucket["kids_with_player"] = 0  # Only children from player
            if "kids_with_npc" not in bucket:
                bucket["kids_with_npc"] = 0  # Children from NPCs
            if "original_daughter" not in bucket:
                bucket["original_daughter"] = is_mother  # Mothers have their daughter; students don't
            if "preg_father" not in bucket:
                bucket["preg_father"] = None  # "player", "npc", or None if not pregnant


            #active sex tracking
            if "had_sex_today" not in bucket:
                bucket["had_sex_today"] = False
            if "having_oral_sex" not in bucket:
                bucket["having_oral_sex"] = False
            if "having_vaginal_sex" not in bucket:
                bucket["having_vaginal_sex"] = False

            if "boob_cum_fetish" not in bucket:
                bucket["boob_cum_fetish"] = get_cum_fetish_level(self, "boobs")
            if "boob_sex_count" not in bucket:
                bucket["boob_sex_count"] = 0
            if "last_boob_sex" not in bucket:
                bucket["last_boob_sex"] = -1
            if "first_time_boobs" not in bucket:
                bucket["first_time_boobs"] = True
            if "aware_boob_condom" not in bucket:
                bucket["aware_boob_condom"] = False

            if "thigh_cum_fetish" not in bucket:
                bucket["thigh_cum_fetish"] = get_cum_fetish_level(self, "thighs")
            if "thigh_sex_count" not in bucket:
                bucket["thigh_sex_count"] = 0
            if "last_thigh_sex" not in bucket:
                bucket["last_thigh_sex"] = -1
            if "first_time_thighs" not in bucket:
                bucket["first_time_thighs"] = True
            if "aware_thigh_condom" not in bucket:
                bucket["aware_thigh_condom"] = False

            if "ass_cum_fetish" not in bucket:
                bucket["ass_cum_fetish"] =  get_cum_fetish_level(self, "ass_cum")
            if "ass_cumshot_count" not in bucket:
                bucket["ass_cumshot_count"] = 0
            if "last_ass_cumshot" not in bucket:
                bucket["last_ass_cumshot"] = -1
            if "first_time_ass_cumshot" not in bucket:
                bucket["first_time_ass_cumshot"] = True
            if "aware_ass_cumshot_condom" not in bucket:
                bucket["aware_ass_cumshot_condom"] = False

            if "pussy_cum_fetish" not in bucket:
                bucket["pussy_cum_fetish"] =  get_cum_fetish_level(self, "pussy_cum")
            if "impreg_fetish" not in bucket:
                bucket["impreg_fetish"] = 0
            if "pussy_cumshot_count" not in bucket:
                bucket["pussy_cumshot_count"] = 0
            if "last_pussy_cumshot" not in bucket:
                bucket["last_pussy_cumshot"] = -1
            if "first_time_pussy_cumshot" not in bucket:
                bucket["first_time_pussy_cumshot"] = True
            if "aware_pussy_cumshot_condom" not in bucket:
                bucket["aware_pussy_cumshot_condom"] = False

            #Condoms Only the 4 types, vaginal, anal, oral, body
            if "player_knows_vaginal_condom" not in bucket:
                bucket["player_knows_vaginal_condom"] = False
            if "player_knows_anal_condom" not in bucket:
                bucket["player_knows_anal_condom"] = False
            if "player_knows_oral_condom" not in bucket:
                bucket["player_knows_oral_condom"] = False
            if "player_knows_body_condom" not in bucket:
                bucket["player_knows_body_condom"] = False
            if "wants_vaginal_condom" not in bucket:
                bucket["wants_vaginal_condom"] = wants_condom(self, "vaginal")
            if "wants_anal_condom" not in bucket:
                bucket["wants_anal_condom"] = wants_condom(self, "anal")
            if "wants_oral_condom" not in bucket:
                bucket["wants_oral_condom"] = wants_condom(self, "oral")
            if "wants_body_condom" not in bucket:
                bucket["wants_body_condom"] = wants_condom(self, "body")



            # Birth control system
            # #self.male_condom = False #85% effective, 94% with spermicide
            # self.spermicide = False #70% by itself, need to apply 15-30min before sex, 1 hour effectiveness, vaginal irritation
            # self.female_condom = False #79% effective, 88% with spermicide
            # self.female_diaphragm = False #87%, 94% with spermicide, apply 2hrs before, 24hours after sex
            # self.cervical_cap = False #75%, 85% with spermicide, 6hrs before, 48 hours
            # self.cervical_sponge = False #76%, 91% with spermicide, day, if expecting sex, max one day, vaginal irritation
            # self.bc_implant = False #100% - 3 years, removable
            # self.intrauterine_device = False #100% - 3  years, removable
            # self.fertility_awareness = False #88% avoid sex 2 weeks before ideal day,
            # self.cervical_mucus = False #88% avoid sex 2 weeks before ideal day,
            # self.morning_after_pill = False #90% effective within 3 days of sex, will not work on ideal day.
            # self.tubal_ligation = False #100% effective, reversabile
            # self.salpingectomy = False #100% effective, reversabile
            # self.pulling_out = False #20% effective
            if "bc_chance" not in bucket:
                bucket["bc_chance"] = 100
            if "birth_control" not in bucket:
                bucket["birth_control"] = renpy.random.randint(0, 100) < (10 if is_mother else 69)
            if "bc_status_known" not in bucket:
                bucket["bc_status_known"] = False
            if "bc_penalty" not in bucket:
                bucket["bc_penalty"] = 0

            # Fertility cycle system
            if "fertility_percent" not in bucket:
                bucket["fertility_percent"] = 5.0 if is_mother else 25.0
            if "ideal_fertile_day" not in bucket:
                bucket["ideal_fertile_day"] = renpy.random.randint(0, 30)

            # Conversation Tracking System
            if "has_met_before" not in bucket:
                bucket["has_met_before"] = False
            if "has_discussed_pregnancy_before" not in bucket:
                bucket["has_discussed_pregnancy_before"] = False
            if "has_discussed_birth_control_before" not in bucket:
                bucket["has_discussed_birth_control_before"] = False
            if "has_discussed_condoms_before" not in bucket:
                bucket["has_discussed_condoms_before"] = False

            # Pregnancy tracking (sidecar)
            if "pregnant" not in bucket:
                bucket["pregnant"] = False
            if "preg_body" not in bucket:
                bucket["preg_body"] = False
            if "knows_pregnant" not in bucket:
                bucket["knows_pregnant"] = False
            if "player_knows_pregnant" not in bucket:
                bucket["player_knows_pregnant"] = False
            if "preg_progress_days" not in bucket:
                bucket["preg_progress_days"] = 0
            if "preg_start_day" not in bucket:
                bucket["preg_start_day"] = 0
            if "preg_end_day" not in bucket:
                bucket["preg_end_day"] = 0
            if "preg_announce" not in bucket:
                bucket["preg_announce"] = False
            if "days_since_last_birth" not in bucket:
                bucket["days_since_last_birth"] = 0
            if "just_had_baby" not in bucket:
                bucket["just_had_baby"] = False
            if "pregnancy_phase" not in bucket:
                bucket["pregnancy_phase"] = 0

            # Add fertility boost attribute
            if "fertility_boost" not in bucket:
                bucket["fertility_boost"] = 0  # Days remaining for fertility boost
            if "prenatal_boost" not in bucket:
                bucket["prenatal_boost"] = 0  # PregnaVITA supply: pills on hand, taken 1/week
            if "prenatal_doses" not in bucket:
                bucket["prenatal_doses"] = 0  # PregnaVITA doses taken (compression factor, capped)
            # SafeDOCK / DryDOCK state -- sidecar slots ready; the base dev still needs to
            # implement apply_planb_pill / apply_emergency_pill that drive these.
            if "planb_pills" not in bucket:
                bucket["planb_pills"] = 0      # SafeDOCK: conception-block days remaining
            if "emergency_pill" not in bucket:
                bucket["emergency_pill"] = 0   # DryDOCK: effect days remaining
            if "planb_boost" not in bucket:
                bucket["planb_boost"] = 0

            #Followup triggers
            if "has_pregnancy_followup" not in bucket:
                bucket["has_pregnancy_followup"] = False
            if "has_birth_control_followup" not in bucket:
                bucket["has_birth_control_followup"] = False
            if "has_condoms_followup" not in bucket:
                bucket["has_condoms_followup"] = False
            if "has_corruption_followup" not in bucket:
                bucket["has_corruption_followup"] = False
            if "has_naturism_followup" not in bucket:
                bucket["has_naturism_followup"] = False
            if "has_fear_followup" not in bucket:
                bucket["has_fear_followup"] = False
            if "has_blowjob_followup" not in bucket:
                bucket["has_blowjob_followup"] = False
            if "has_strip_tease_followup" not in bucket:
                bucket["has_strip_tease_followup"] = False
            if "has_get_dressed_followup" not in bucket:
                bucket["has_get_dressed_followup"] = False
            if "has_strip_to_underwear_followup" not in bucket:
                bucket["has_strip_to_underwear_followup"] = False
            if "has_naked_followup" not in bucket:
                bucket["has_naked_followup"] = False
            if "has_milk_followup" not in bucket:
                bucket["has_milk_followup"] = False
            if "has_creamer_followup" not in bucket:
                bucket["has_creamer_followup"] = False
            if "has_toppings_followup" not in bucket:
                bucket["has_toppings_followup"] = False
            if "has_small_talk_followup" not in bucket:
                bucket["has_small_talk_followup"] = False
            if "has_masturbation_tips_followup" not in bucket:
                bucket["has_masturbation_tips_followup"] = False
            if "has_shower_sex_followup" not in bucket:
                bucket["has_shower_sex_followup"] = False

            # ---- one-time pregnancy migration to the dose-based PregnaVITA model ----
            # Runs once per girl (version-flagged). For a girl already pregnant under the old
            # model: infer how many PregnaVITA doses she had (the old boost halved her remaining
            # time per dose), keep her preserved progress/phase, recompute her due date for that
            # inferred speed so the display is honest, and make sure she knows if she's far
            # enough along. We deliberately don't try to "correct" her progress.
            if bucket.get("preg_model_version", 0) < 2:
                bucket["preg_model_version"] = 2
                if self.pregnant:
                    try:
                        _cd = time_manager.total_days
                    except NameError:
                        _cd = self.preg_start_day
                    # Infer doses: how many times 250 (the ~conception remaining) can be halved
                    # and still cover her remaining progress. Matches round(log2(...)), capped.
                    _rem = max(1, 260 - self.preg_progress_days)
                    _doses = 0
                    _r = 250.0
                    while _doses < VT_PRENATAL_DOSE_CEILING and (_r / 2.0) >= _rem:
                        _r /= 2.0
                        _doses += 1
                    self.prenatal_doses = _doses
                    self.prenatal_boost = 0      # old "boost days" field repurposed as supply -> clear it
                    # Recompute the due date for her preserved progress at the inferred speed.
                    _speed = 1 + self.prenatal_doses
                    self.preg_end_day = _cd + max(VT_MIN_PREG_DAYS_LEFT, ((260 - self.preg_progress_days) + _speed - 1) // _speed)
                    # Make sure she knows she's pregnant if she's far enough along.
                    if (_cd - self.preg_start_day) >= VT_KNOWS_AFTER_DAYS:
                        self.knows_pregnant = True
                        self.birth_control = False

        # Create patched __init__
        def vt_girl_init(self, *args, **kwargs):
            # ===== PHASE 1: MINIMAL VT ATTRIBUTES NEEDED FOR CORE GAME =====
            # Initialize ONLY attributes that are used in trait requirements
            # BEFORE core init (to prevent the previous error)
            vt_minimal_attributes = [
                'boob_cum_fetish', 'thigh_cum_fetish', 'ass_cum_fetish', 'pussy_cum_fetish',
                'oral_cum_fetish', 'vaginal_cum_fetish', 'anal_cum_fetish', 'baby_desire'
            ]
            
            for attr in vt_minimal_attributes:
                if not hasattr(self, attr):
                    setattr(self, attr, 0)
            
            original_girl_init(self, *args, **kwargs)

            # ===== TOP-3 STAT BOOSTING WITH TRAIT PRIORITIZATION =====
            # Get all core personality stats after traits have been applied
            stats = {
                "affection": self.affection,
                "corruption": self.corruption,
                "discipline": self.discipline,
                "fear": self.fear,
                "intellect": self.intellect,
                "naturism": self.naturism
            }
            
            # Calculate trait rarity bonus
            # trait_boost = 0
            # for trait in self.traits:
                # if trait.rarity <= 1.0:  # Legendary or better (Super-Legendary)
                    # trait_boost += 5
                # elif trait.rarity <= 2.0:  # Epic
                    # trait_boost += 3
                # elif trait.rarity <= 3.0:  # Rare
                    # trait_boost += 2
            
            # Identify stats that should be prioritized based on key traits
            prioritized_stats = set()
            
            # Check for traits that should guarantee stat boosting
            for trait in self.traits:
                if trait.name == "nympho":
                    prioritized_stats.add("corruption")
                    prioritized_stats.add("arousal")
                elif trait.name == "brilliant":
                    prioritized_stats.add("intellect")
                elif trait.name == "naturist":
                    prioritized_stats.add("naturism")
                elif trait.name == "rebellious":
                    prioritized_stats.add("discipline")  # Actually negative, but we want to emphasize it
                # Add other key trait mappings as needed
            
            # Sort stats by value (highest first)
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            
            # Get top 3 stats, but ensure prioritized stats are included if possible
            top_3_stats = []
            
            # First add prioritized stats that aren't already in top stats
            for stat_name, _ in sorted_stats:
                if stat_name in prioritized_stats:
                    top_3_stats.append(stat_name)
                    if len(top_3_stats) >= 3:
                        break
            
            # Then fill remaining slots with highest non-prioritized stats
            if len(top_3_stats) < 3:
                for stat_name, _ in sorted_stats:
                    if stat_name not in top_3_stats:
                        top_3_stats.append(stat_name)
                        if len(top_3_stats) >= 3:
                            break
            
            # Apply boosts to top 3 stats (with prioritization)
            for stat_name in top_3_stats:
                # base_boost = renrandom.randint(3, 5)
                # total_boost = base_boost + trait_boost
                # current_value = getattr(self, stat_name)
                # setattr(self, stat_name, min(100, current_value + total_boost))
                boost_multiplier = self.get_stat_growth_multiplier_for_stat(stat_name)
                true_multiplier = 2 + (boost_multiplier - girl_stat_growth_multipliers.get(stat_name, 1))
                base_boost = renrandom.randint(3, 5)
                total_boost = base_boost * true_multiplier
                current_value = getattr(self, stat_name)
                setattr(self, stat_name, min(100, current_value + total_boost))
            
            # Ensure stats stay within limits
            if hasattr(self, 'fix_stats'):
                self.fix_stats(hide_notification=True)
            # ===== END BOOSTING =====
            # ===== VIRGINITY & FIRST-TIME STATUS SYSTEM =====
            # Initialize all virginity/first-time attributes using our comprehensive system
            initialize_virginity_status(self)

            # Ensure consistency with other attributes
            if self.hymen:
                self.vaginal_sex_count = 0
                self.last_vaginal_sex = -1
            if self.first_time_oral:
                self.oral_sex_count = 0
                self.last_oral_sex = -1
            if self.first_time_anal:
                self.anal_sex_count = 0
                self.last_anal_sex = -1
            # External cumshot counts should reflect first-time status
            if self.first_time_boobs:
                self.boob_sex_count = 0
                self.last_boob_sex = -1
            if self.first_time_thighs:
                self.thigh_sex_count = 0
                self.last_thigh_sex = -1
            if self.first_time_ass_cumshot:
                self.ass_cumshot_count = 0
                self.last_ass_cumshot = -1
            if self.first_time_pussy_cumshot:
                self.pussy_cumshot_count = 0
                self.last_pussy_cumshot = -1
            # ===== END VIRGINITY SYSTEM =====

            vt_ensure_girl_attrs(self)

            #original_girl_init(self, *args, **kwargs)


        #Followup triggers
        def trigger_pregnancy_followup(self):
            self.has_pregnancy_followup = True
            renpy.log(f"Pregnancy follow-up triggered for {self.first_name}")
            
        def trigger_birth_control_followup(self):
            self.has_birth_control_followup = True
            renpy.log(f"Birth Control follow-up triggered for {self.first_name}")
            
        def trigger_condoms_followup(self):
            self.has_condoms_followup = True
            renpy.log(f"Condoms follow-up triggered for {self.first_name}")

        def trigger_corruption_followup(self):
            self.has_corruption_followup = True
            self.corruption = min(100, self.corruption + 3)
            renpy.log(f"Corruption follow-up triggered for {self.first_name}")

        def trigger_naturism_followup(self):
            self.has_naturism_followup = True
            self.naturism = min(100, self.naturism + 3)
            renpy.log(f"Naturism follow-up triggered for {self.first_name}")
            
        def trigger_fear_followup(self):
            self.has_fear_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Fear follow-up triggered for {self.first_name}")

        def trigger_blowjob_followup(self):
            self.has_blowjob_followup = True
            vt_handle_cum_fetishes("blowjob", self, "oral")
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Blowjob follow-up triggered for {self.first_name}")
        
        def trigger_strip_tease_followup(self):
            self.has_strip_tease_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Strip tease follow-up triggered for {self.first_name}")

        def trigger_get_dressed_followup(self):
            self.has_get_dressed_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Get dressed follow-up triggered for {self.first_name}")

        def trigger_strip_to_underwear_followup(self):
            self.has_strip_to_underwear_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Strip to underwear follow-up triggered for {self.first_name}")

        def trigger_naked_followup(self):
            self.has_naked_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Naked follow-up triggered for {self.first_name}")

        def trigger_milk_followup(self):
            self.has_milk_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Milk follow-up triggered for {self.first_name}")

        def trigger_creamer_followup(self):
            self.has_creamer_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Creamer follow-up triggered for {self.first_name}")

        def trigger_toppings_followup(self):
            self.has_toppings_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Toppings follow-up triggered for {self.first_name}")

        def trigger_small_talk_followup(self):
            self.has_small_talk_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Small_talk Teacher follow-up triggered for {self.first_name}")

        def trigger_masturbation_tips_followup(self):
            self.has_masturbation_tips_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Masturbation tips follow-up triggered for {self.first_name}")

        def trigger_shower_sex_followup(self):
            self.has_shower_sex_followup = True
            self.fear = min(100, self.fear + 3)
            renpy.log(f"Shower sex follow-up triggered for {self.first_name}")

        # Add fertility calculation methods (since Ren'Py doesn't handle properties well in patching)
        def days_from_ideal_fertility(self, with_direction=False):
            """
            Returns days from ideal fertile day
            Negative = before ideal day, Positive = after ideal day
            Example: -2 = 2 days before ovulation, +1 = 1 day after ovulation
            """
            # Safely access time_manager
            cycle_day = 0
            try:
                # Use the global 'time_manager' instance that was created in game_init.rpy
                cycle_day = time_manager.total_days
            except NameError:
                # This should not happen if game_init.rpy is loaded correctly
                renpy.log("get_cycle_day ERROR: Global 'time_manager' variable not found!")
                return 1
            
            day_difference = cycle_day - self.ideal_fertile_day
            
            # Normalize to -15 to +14 range
            if day_difference > 15:
                day_difference -= 30
            elif day_difference < -15:
                day_difference += 30
                
            return day_difference if with_direction else abs(day_difference)

        def on_birth_control(self):
            return self.fertility_percent < 0 or self.birth_control

        def is_highly_fertile(self):
            if self.pregnant:
                return False
            # Get the signed difference, just like effective_fertility does
            day_diff = self.days_from_ideal_fertility(with_direction=True)
            
            # Define the fertile window based on the FERTILITY_CURVE
            # We'll consider anything above 10% of base fertility as "highly fertile"
            FERTILE_WINDOW = [-3, -2, -1, 0, 1]
            
            if day_diff in FERTILE_WINDOW:
                return True
                
            return False

        def effective_fertility(self):
            if self.fertility_percent < 0:
                return 0
                
            # Get signed difference (negative = before ideal day, positive = after)
            day_diff = self.days_from_ideal_fertility(with_direction=True)
            
            # FERTILITY CURVE BASED ON MEDICAL RESEARCH (NEJM)
            # Key: days from ovulation (negative = before, positive = after)
            # Value: percentage of BASE fertility (1.0 = 100%)
            FERTILITY_CURVE = {
                -5: 0.10,   # 5 days before: 10% of base
                -4: 0.20,   # 4 days before: 20% of base
                -3: 0.40,   # 3 days before: 40% of base
                -2: 0.75,   # 2 days before: 75% of base
                -1: 0.90,   # 1 day before: 90% of base
                0:  1.00,   # Ovulation day: 100% of base (PEAK)
                1:  0.40,   # 1 day after: 40% of base
            }
            
            # Get multiplier for current position in cycle
            multiplier = FERTILITY_CURVE.get(day_diff, 0.01)  # 1% outside fertile window
            
            # Check if boost is active and apply it additively to the base fertility
            if self.fertility_boost > 0:
                # Add 25 to the base fertility, then apply the day's multiplier
                base_fertility = (self.fertility_percent + 25) * multiplier
            else:
                # No boost, use the normal base fertility
                base_fertility = self.fertility_percent * multiplier
            
            #renpy.log(f"DEBUG FERTILITY: girl={self.full_name}, base_fert={self.fertility_percent}, boost={self.fertility_boost}, day_diff={day_diff}, multiplier={multiplier}, final_result={base_fertility}")
            
            return base_fertility

        def birthcontrol_efficiency(self):
            if not self.on_birth_control():
                return 0
            return max(100 - self.bc_penalty, 0)

        def pregnancy_chance(self):
            if self.effective_fertility() <= 0:  
                return 0
            return (self.effective_fertility() / 100) * (100 - self.birthcontrol_efficiency())  # NO PARENTHESES!

        def apply_prenatal_boost(self):
            # Consume one PregnaVITA dose (called from the weekly tick). Gated: only if
            # pregnant, she knows, she has supply (prenatal_boost), and she is below the dose
            # ceiling. Each dose raises the daily progress speed (1 + doses) and pulls the due
            # date in -- no progress jump; compression happens via the daily speed.
            if not self.pregnant or not self.knows_pregnant:
                return
            if self.prenatal_boost <= 0 or getattr(self, 'prenatal_doses', 0) >= VT_PRENATAL_DOSE_CEILING:
                return

            current_day = 0
            try:
                current_day = time_manager.total_days
            except NameError:
                renpy.log(f"VT MOD ERROR: apply_prenatal_boost failed because 'time_manager' is not defined for {self.first_name}.")
                return

            self.prenatal_doses = getattr(self, 'prenatal_doses', 0) + 1
            self.prenatal_boost -= 1   # consume one pill from supply

            speed = 1 + min(self.prenatal_doses, VT_PRENATAL_DOSE_CEILING)
            remaining = max(VT_MIN_PREG_DAYS_LEFT, ((260 - self.preg_progress_days) + speed - 1) // speed)
            self.preg_end_day = current_day + remaining

            vt_preg_notify(f"{self.first_name} took PregnaVITA (dose {self.prenatal_doses}/{VT_PRENATAL_DOSE_CEILING}) - pregnancy accelerating.", duration=3.0)
            renpy.log(f"VT MOD: {self.first_name} PregnaVITA dose {self.prenatal_doses}, speed {speed}x, due day {self.preg_end_day}")

        # Create patched daily_update
        def vt_daily_update(self):
            original_daily_update(self)

            #reset stats
            self.had_sex_today = False
            self.having_oral_sex = False
            self.having_vaginal_sex = False
            
            # Fertility boost countdown
            if self.fertility_boost > 0:
                self.fertility_boost -= 1

            # Anal and Oral, all cum is gone by next day
            # technically doesn't really matter, as its more of a temp visual for the day.
            if self.oral_cum > 0:
                self.oral_cum = 0
            if self.anal_cum > 0:
                    self.anal_cum = 0

            # Pregnancy logic
            if self.vaginal_cum > 0:
                #regardless of cum stats the most sperm will live in the womb is 3-5 days, therefore max 3 units will remain regardless, it should still satisfy the 'inflation' cum kinks. This is to help with the 'sperm typically can stay alve for about 3 to 5 days', so I choosed 3 days for game purposes.
                if self.vaginal_cum >4:
                    self.vaginal_cum = 4
                                
                if self.hymen:
                    self.hymen = False

                # Pregnancy check - only check if not already pregnant and not in postpartum period
                if not self.pregnant and not self.just_had_baby and self.vaginal_cum >= 0:
                    #still use up a unit for the check (this is for cum still in the womb)
                    
                    # Birth control failed to prevent the pregnancy
                    if renpy.random.randint(1, 100) > self.birthcontrol_efficiency():
                        # There's a chance she's pregnant based on effective fertility
                        if renpy.random.randint(1, 100) <= self.effective_fertility():
                            self.pregnant = True
                            self.knows_pregnant = False
                            self.player_knows_pregnant = False
                            # Safely access time_manager
                            # Track when this happened - SAFELY
                            self.preg_start_day = 0
                            try:
                                self.preg_start_day = time_manager.total_days
                            except NameError:
                                # This should not happen if game_init.rpy is loaded correctly
                                renpy.log("vt_daily_update # Pregnancy check  ERROR: Global 'time_manager' variable not found!")
                                return
                            self.preg_progress_days = 1
                            self.pregnancy_phase = 1
                            self.preg_announce = False
                            self.days_since_last_birth = 0
                            self.preg_end_day = self.preg_start_day + (260 - self.preg_progress_days)
                            
                            # SET FATHER TYPE - CRITICAL ADDITION
                            self.preg_father = "player"  # This pregnancy is from the player
                            self.prenatal_doses = 0  # fresh pregnancy: no meds yet
                            self.prenatal_boost = 0  # no pill supply yet
                            
                            vt_preg_notify(f"{self.first_name} might be pregnant!", duration=3)

                #remove cum after preg check.
                self.vaginal_cum -= 1


            # Pregnancy progression
            if self.pregnant:
                speed = 1 + min(getattr(self, 'prenatal_doses', 0), VT_PRENATAL_DOSE_CEILING)
                self.preg_progress_days += speed
                
                # (PregnaVITA dosing moved to the weekly tick -- see vt_*_weekly_update.)
                
                current_day = 0
                try:
                    current_day = time_manager.total_days
                except NameError:
                    # This should not happen if game_init.rpy is loaded correctly
                    renpy.log("vt_daily_update # Pregnancy progression ERROR: Global 'time_manager' variable not found!")
                    return
                # Awareness: a fixed real-day delay after conception, independent of meds;
                # latches regardless of trimester band (fixes the old prenatal-boost skip).
                if (current_day - self.preg_start_day) >= VT_KNOWS_AFTER_DAYS:
                    self.knows_pregnant = True
                    self.birth_control = False

                # Pregnancy ended - baby born
                if self.preg_progress_days >= 260:
                    # Increment appropriate counter based on father type
                    if self.preg_father == "player":
                        self.kids_with_player += 1
                        renpy.log(f"VT MOD: {self.first_name} gave birth to player's baby! Total player kids: {self.kids_with_player}")
                    elif self.preg_father == "npc":
                        self.kids_with_npc += 1
                        renpy.log(f"VT MOD: {self.first_name} gave birth to NPC's baby! Total NPC kids: {self.kids_with_npc}")
                    
                    # Always increment total kids count
                    self.kids += 1
                    
                    # Reset pregnancy state
                    self.preg_end_day = 0
                    self.pregnancy_phase = 0
                    self.pregnant = False
                    self.just_had_baby = True
                    self.days_since_last_birth = 1
                    self.preg_father = None  # Clear father type after birth
                    self.prenatal_doses = 0  # clear meds acceleration
                    self.prenatal_boost = 0  # clear leftover pill supply
                  # Visible pregnancy body after 30 days
                # After 30 weeks, she will start showing third trimester, very obvious now
                elif self.preg_progress_days >= 210:
                    self.pregnancy_phase = 3
                    self.preg_body = True
                # After 15 weeks, she will start showing second trimester, kind of obvious now
                elif self.preg_progress_days >= 105:
                    self.pregnancy_phase = 2
                    self.preg_body = True
                # After 7 weeks, she will start showing first trimester but can still hide pregnancy
                elif self.preg_progress_days >= 35:
                    self.pregnancy_phase = 1
                    #self.preg_body = True
                # After 2 days, she will know if she's pregnant and in her first trimester
                elif self.preg_progress_days >= 10:
                    self.pregnancy_phase = 1
                    self.knows_pregnant = True
                    self.birth_control = False

            # Post-birth cooldown
            if self.just_had_baby:
                self.days_since_last_birth += 1
                if self.days_since_last_birth >= 14:
                    # Time to determine birth control decision based on multiple factors
                    # BASE CHANCE CALCULATION (0-100%)
                    bc_chance = 0
                    # 1. Baby desire (MOST IMPORTANT FACTOR)
                    # Low desire = high BC chance, High desire = low BC chance
                    bc_chance += (100 - self.baby_desire)  # Inverse relationship
                    # 2. Number of kids (SECOND MOST IMPORTANT)
                    # Each additional kid increases BC likelihood significantly
                    kids_factor = max(0, self.kids - 1) * 25  # +25% per child beyond first
                    bc_chance += min(kids_factor, 50)  # Cap at +50% for multiple kids
                    # 3. Intellect (educated decision-making)
                    if hasattr(self, 'intellect'):
                        bc_chance += min(self.intellect // 3, 20)  # Up to +20% for high intellect
                    # 4. Corruption (strategic thinking)
                    if hasattr(self, 'corruption') and self.corruption > 70:
                        bc_chance += 15  # Strategic BC use for high corruption
                    # 5. Naturism (natural body acceptance)
                    if hasattr(self, 'naturism') and self.naturism > 70:
                        bc_chance -= 25  # Strong naturalists resist BC
                    # 6. Fear factor (anxiety about more pregnancy)
                    if hasattr(self, 'fear') and self.fear > 70:
                        bc_chance += 20  # Fearful women seek protection
                    # 7. Special case: Mothers vs Students
                    if hasattr(self, 'is_mother') and self.is_mother:
                        bc_chance += 10  # Mothers more likely to use BC after multiple births
                    # CLAMP FINAL CHANCE (0-100%)
                    bc_chance = max(10, min(90, bc_chance))  # Ensure some randomness remains
                    # MAKE DECISION
                    will_use_bc = (renpy.random.randint(1, 100) <= bc_chance)
                    # Apply decision - CRITICAL: bc_status_known remains FALSE (player doesn't know yet)
                    self.birth_control = will_use_bc
                    self.bc_status_known = False  # PLAYER DOESN'T KNOW HER BC STATUS YET
                    self.bc_penalty = 0  # Reset penalty after birth (new cycle)
                    
                    # LOG THE DECISION FOR DEBUGGING
                    if will_use_bc:
                        renpy.log(f"VT MOD: {self.first_name} (kids={self.kids}) decided to use birth control after birth (chance={bc_chance}%)")
                        # Player doesn't get notification - they don't know yet
                    else:
                        renpy.log(f"VT MOD: {self.first_name} (kids={self.kids}) chose NOT to use birth control after birth (chance={bc_chance}%)")
                        # Player doesn't get notification - they don't know yet
                    # Reset post-birth state
                    self.just_had_baby = False
                    self.days_since_last_birth = 0
                    self.preg_body = False
                    # Add subtle visual/textual hint that she might be on BC or not
                    # (Player will need to discover through dialogue)
                    self.bc_chance = 100 if will_use_bc else 0
        
        def get_fertility_day_status(self):
            """
            Returns a user-friendly string describing the current day in the fertility cycle.
            """
            cycle_day = self.get_cycle_day()
            menstrual_duration = 5

            # Check for the menstrual phase first
            if 1 <= cycle_day <= menstrual_duration:
                return "She is on her moon time... be nice"

            # Get signed difference (negative = before ideal day, positive = after)
            day_diff = self.days_from_ideal_fertility(with_direction=True)

            if day_diff == 0:
                return "Peak Ovulation Day!"
            elif 1 <= day_diff <= 3: # A few days after peak
                return f"{day_diff} day(s) past ovulation"
            elif -3 <= day_diff <= -1: # A few days before peak
                return f"{abs(day_diff)} day(s) before ovulation"
            elif -5 <= day_diff <= -4: # Early fertile window
                return "High fertility window!"
            else: # Outside the main window
                return "Low fertility"

        def get_cycle_day(self):
            """
            Returns the current day of the 30-day menstrual cycle (1-30).
            Day 1 is the first day of the menstrual phase.
            """
            total_days = 0
            try:
                total_days = time_manager.total_days
            except NameError:
                # This should not happen if game_init.rpy is loaded correctly
                renpy.log("get_cycle_day ERROR: Global 'time_manager' variable not found!")
                return 1

            ideal_day = self.ideal_fertile_day
            menstrual_duration = 5
            follicular_duration = 7
            
            ov_start_day = (ideal_day - 3 + 30) % 30
            cycle_start_day = (ov_start_day - follicular_duration - menstrual_duration + 30) % 30
            
            current_day = total_days % 30
            if current_day == 0: current_day = 30
            
            # The cycle day is the number of days from the start of the cycle
            days_from_cycle_start = (current_day - cycle_start_day + 30) % 30
            if days_from_cycle_start == 0: days_from_cycle_start = 30
            
            return days_from_cycle_start
   
        # #Relationals
        # def vt_relationship_change(self, attribute, amount)-> None:
            # previous_amount = self.player_relationship[attribute]
            # new_amount = max(-20, min(100, previous_amount + amount)) 
            # self.player_relationship[attribute] = new_amount
            # renpy.log(f"RELATIONSHIP UPDATE: {attribute} changed from {previous_amount} to {self.player_relationship[attribute]}")
            # # Ensure the change is persisted in the global store
            # #renpy.store[self].player_relationship[attribute] = self.player_relationship[attribute]
            # #setattr(person, key, value)
            # setattr(renpy.store, f"{self}.player_relationship['{attribute}']", new_amount)

        # def vt_seed_relationship_path(self, path, amount)-> None:
            # previous_amount = self.path_seeds[path]
            # new_amount =  max(-20, min(100, previous_amount + amount))
            # # girl.path_seeds = {"slave": 0, "girlfriend": 0, "fwb": 0, "sugarbaby": 0}
            # self.path_seeds[path] = new_amount
            # renpy.log(f"RELATIONSHIP UPDATE: {path} changed from {previous_amount} to {self.path_seeds[path]}")
            # # Ensure the change is persisted in the global store
            # #renpy.store[self].path_seeds[path] = self.path_seeds[path]
            # setattr(renpy.store, f"{self}.path_seeds['{path}']", new_amount)
        
        def boob_description(self):
            # Returns a randomized, flavorful bust descriptor (adjective + noun) based on
            # the girl's physical-appearance trait. Distinguishes natural vs fake; uses a
            # size-neutral positive fallback if she has no boob-size trait.
            nouns = ["tits", "boobs", "breasts"]
            if self.has_trait("big_boobs"):
                adjs = ["big", "huge", "massive", "ample", "full"]
            elif self.has_trait("big_boobs_fake"):
                adjs = ["big fake", "huge fake", "augmented"]
            elif self.has_trait("average_boobs"):
                adjs = ["shapely", "lovely"]
            elif self.has_trait("average_boobs_fake"):
                adjs = ["fake", "enhanced"]
            elif self.has_trait("small_boobs"):
                adjs = ["small", "tiny", "petite", "perky"]
            elif self.has_trait("small_boobs_fake"):
                adjs = ["small fake", "petite enhanced", "perky fake"]
            else:
                adjs = ["soft", "supple", "lovely"]
            return f"{renrandom.choice(adjs)} {renrandom.choice(nouns)}"

        # Apply patches
        Girl.__init__ = vt_girl_init
        Girl.daily_update = vt_daily_update

        # Patched weekly_update: PregnaVITA is taken once per week (Monday tick), gated on
        # awareness. Re-check awareness here first so a Monday discovery still doses that day.
        original_weekly_update = Girl.weekly_update
        def vt_weekly_update(self):
            original_weekly_update(self)
            if self.pregnant:
                try:
                    _cd = time_manager.total_days
                except NameError:
                    _cd = 0
                if _cd and (_cd - self.preg_start_day) >= VT_KNOWS_AFTER_DAYS:
                    self.knows_pregnant = True
                    self.birth_control = False
                self.apply_prenatal_boost()   # gated internally (knows + supply + under cap)
        Girl.weekly_update = vt_weekly_update
        Girl.days_from_ideal_fertility = days_from_ideal_fertility
        Girl.on_birth_control = on_birth_control
        Girl.is_highly_fertile = is_highly_fertile
        Girl.effective_fertility = effective_fertility
        Girl.birthcontrol_efficiency = birthcontrol_efficiency
        Girl.pregnancy_chance = pregnancy_chance
        Girl.apply_prenatal_boost = apply_prenatal_boost
        Girl.days_from_ideal_fertility = consistent_days_from_ideal_fertility
        Girl.trigger_pregnancy_followup = trigger_pregnancy_followup
        Girl.trigger_birth_control_followup = trigger_birth_control_followup
        Girl.trigger_condoms_followup = trigger_condoms_followup
        Girl.trigger_corruption_followup = trigger_corruption_followup
        Girl.trigger_naturism_followup = trigger_naturism_followup
        Girl.trigger_fear_followup = trigger_fear_followup
        Girl.trigger_blowjob_followup = trigger_blowjob_followup
        Girl.trigger_strip_tease_followup = trigger_strip_tease_followup
        Girl.trigger_get_dressed_followup = trigger_get_dressed_followup
        Girl.trigger_naked_followup = trigger_naked_followup
        Girl.trigger_milk_followup = trigger_milk_followup
        Girl.trigger_creamer_followup = trigger_creamer_followup
        Girl.trigger_toppings_followup = trigger_toppings_followup
        Girl.trigger_small_talk_followup = trigger_small_talk_followup
        Girl.trigger_masturbation_tips_followup = trigger_masturbation_tips_followup
        Girl.trigger_shower_sex_followup = trigger_shower_sex_followup
        Girl.get_fertility_day_status = get_fertility_day_status
        Girl.get_cycle_day = get_cycle_day
        Girl.boob_description = boob_description

        # ===== SIDECAR PROPERTY ACCESSORS (girl) =====
        # Batch 1: relationship keys. Each keeps `girl.<key>` working unchanged at every call
        # site and eval string, but stores the value in girl.mod_data["elkrose_vt"]. Getters
        # are READ-ONLY (render-path safe). For dict-valued keys the getter returns the SAME
        # dict object from the bucket, so in-place mutations persist. Inherited by Mother.
        # This list grows per batch; vt_ensure_girl_attrs migrates/initializes these keys.
        VT_GIRL_SIDECAR_KEYS = [
            # batch 1: relationship
            "player_relationship", "path_seeds", "initial_reaction",
            # batch 2: pregnancy
            "pregnant", "preg_body", "knows_pregnant", "player_knows_pregnant",
            "preg_progress_days", "preg_start_day", "preg_end_day", "preg_announce",
            "pregnancy_phase", "just_had_baby", "days_since_last_birth", "preg_father",
            # batch 3: fertility + birth control
            "bc_chance", "birth_control", "bc_status_known", "bc_penalty",
            "fertility_percent", "ideal_fertile_day",
            "fertility_boost", "prenatal_boost", "prenatal_doses",
            # SafeDOCK / DryDOCK (pending base-dev implementation)
            "planb_pills", "emergency_pill", "planb_boost",
            # batch 4: fetishes
            "oral_cum_fetish", "vaginal_cum_fetish", "anal_cum_fetish", "boob_cum_fetish",
            "thigh_cum_fetish", "ass_cum_fetish", "pussy_cum_fetish", "impreg_fetish", "baby_desire", "baby_desire_xp",
            # batch 5: sex history
            "oral_cum", "vaginal_cum", "anal_cum",
            "oral_sex_count", "last_oral_sex", "vaginal_sex_count", "last_vaginal_sex",
            "anal_sex_count", "last_anal_sex", "first_time_oral", "first_time_pussy", "first_time_anal",
            "boob_sex_count", "last_boob_sex", "first_time_boobs",
            "thigh_sex_count", "last_thigh_sex", "first_time_thighs",
            "ass_cumshot_count", "last_ass_cumshot", "first_time_ass_cumshot",
            "pussy_cumshot_count", "last_pussy_cumshot", "first_time_pussy_cumshot",
            "hymen", "kids", "kids_with_player", "kids_with_npc", "original_daughter",
            # batch 6: condom awareness
            "aware_vaginal_condom", "aware_oral_condom", "aware_anal_condom", "aware_boob_condom",
            "aware_thigh_condom", "aware_ass_cumshot_condom", "aware_pussy_cumshot_condom",
            "player_knows_vaginal_condom", "player_knows_anal_condom", "player_knows_oral_condom", "player_knows_body_condom",
            "wants_vaginal_condom", "wants_anal_condom", "wants_oral_condom", "wants_body_condom",
            # batch 7: misc flags / follow-ups
            "had_sex_today", "having_oral_sex", "having_vaginal_sex",
            "has_met_before", "has_discussed_pregnancy_before", "has_discussed_birth_control_before", "has_discussed_condoms_before",
            "has_pregnancy_followup", "has_birth_control_followup", "has_condoms_followup", "has_corruption_followup",
            "has_naturism_followup", "has_fear_followup", "has_blowjob_followup", "has_strip_tease_followup",
            "has_get_dressed_followup", "has_strip_to_underwear_followup", "has_naked_followup", "has_milk_followup",
            "has_creamer_followup", "has_toppings_followup", "has_small_talk_followup", "has_masturbation_tips_followup",
            "has_shower_sex_followup",
        ]
        # Fallback returned by the getter only in the brief pre-init window (before
        # vt_ensure_girl_attrs has populated the bucket). A callable is invoked to produce a
        # fresh value (use for mutable defaults like dicts); any other value is returned as-is.
        _VT_GIRL_SIDECAR_FALLBACKS = {
            # batch 1: relationship
            "player_relationship": dict,   # called -> fresh {} (only hit pre-init; not mutated then)
            "path_seeds": dict,
            "initial_reaction": "neutral",
            # batch 2: pregnancy (plain immutable values)
            "pregnant": False,
            "preg_body": False,
            "knows_pregnant": False,
            "player_knows_pregnant": False,
            "preg_progress_days": 0,
            "preg_start_day": 0,
            "preg_end_day": 0,
            "preg_announce": False,
            "pregnancy_phase": 0,
            "just_had_baby": False,
            "days_since_last_birth": 0,
            "preg_father": None,
            # batch 3: fertility + birth control
            "bc_chance": 100,
            "birth_control": False,
            "bc_status_known": False,
            "bc_penalty": 0,
            "fertility_percent": 25.0,
            "ideal_fertile_day": 0,
            "fertility_boost": 0,
            "prenatal_boost": 0,
            "prenatal_doses": 0,
            # SafeDOCK / DryDOCK (pending base-dev implementation)
            "planb_pills": 0, "emergency_pill": 0, "planb_boost": 0,
            # batch 4: fetishes
            "oral_cum_fetish": 0, "vaginal_cum_fetish": 0, "anal_cum_fetish": 0, "boob_cum_fetish": 0,
            "thigh_cum_fetish": 0, "ass_cum_fetish": 0, "pussy_cum_fetish": 0, "impreg_fetish": 0, "baby_desire": 0, "baby_desire_xp": 0,
            # batch 5: sex history
            "oral_cum": 0, "vaginal_cum": 0, "anal_cum": 0,
            "oral_sex_count": 0, "last_oral_sex": -1, "vaginal_sex_count": 0, "last_vaginal_sex": -1,
            "anal_sex_count": 0, "last_anal_sex": -1,
            "first_time_oral": True, "first_time_pussy": True, "first_time_anal": True,
            "boob_sex_count": 0, "last_boob_sex": -1, "first_time_boobs": True,
            "thigh_sex_count": 0, "last_thigh_sex": -1, "first_time_thighs": True,
            "ass_cumshot_count": 0, "last_ass_cumshot": -1, "first_time_ass_cumshot": True,
            "pussy_cumshot_count": 0, "last_pussy_cumshot": -1, "first_time_pussy_cumshot": True,
            "hymen": True, "kids": 0, "kids_with_player": 0, "kids_with_npc": 0, "original_daughter": False,
            # batch 6: condom awareness
            "aware_vaginal_condom": False, "aware_oral_condom": False, "aware_anal_condom": False, "aware_boob_condom": False,
            "aware_thigh_condom": False, "aware_ass_cumshot_condom": False, "aware_pussy_cumshot_condom": False,
            "player_knows_vaginal_condom": False, "player_knows_anal_condom": False, "player_knows_oral_condom": False, "player_knows_body_condom": False,
            "wants_vaginal_condom": False, "wants_anal_condom": False, "wants_oral_condom": False, "wants_body_condom": False,
            # batch 7: misc flags / follow-ups
            "had_sex_today": False, "having_oral_sex": False, "having_vaginal_sex": False,
            "has_met_before": False, "has_discussed_pregnancy_before": False, "has_discussed_birth_control_before": False, "has_discussed_condoms_before": False,
            "has_pregnancy_followup": False, "has_birth_control_followup": False, "has_condoms_followup": False, "has_corruption_followup": False,
            "has_naturism_followup": False, "has_fear_followup": False, "has_blowjob_followup": False, "has_strip_tease_followup": False,
            "has_get_dressed_followup": False, "has_strip_to_underwear_followup": False, "has_naked_followup": False, "has_milk_followup": False,
            "has_creamer_followup": False, "has_toppings_followup": False, "has_small_talk_followup": False, "has_masturbation_tips_followup": False,
            "has_shower_sex_followup": False,
        }

        def _vt_make_girl_property(key):
            _fb = _VT_GIRL_SIDECAR_FALLBACKS.get(key)
            def _getter(self):
                md = getattr(self, "mod_data", None)
                if md:
                    b = md.get("elkrose_vt")
                    if b is not None and key in b:
                        return b[key]
                if key in self.__dict__:   # not-yet-migrated loose value (pre-load-backfill)
                    return self.__dict__[key]
                return _fb() if callable(_fb) else _fb
            def _setter(self, value):
                vt_girl_bucket(self)[key] = value
            return property(_getter, _setter)

        for _gk in VT_GIRL_SIDECAR_KEYS:
            setattr(Girl, _gk, _vt_make_girl_property(_gk))
        #Girl.vt_relationship_change = vt_relationship_change
        #Girl.vt_seed_relationship_path = vt_seed_relationship_path

        # baby_desire is now an XP-backed stat (it has a baby_desire_xp sidecar companion), so the
        # (250,750)-scale dialogue/creampie impacts route through the XP economy exactly like
        # corruption/affection. Base fix_stats only levels its six hard-coded stats, so drive
        # baby_desire's leveling here, then clamp. Mother inherits Girl.fix_stats (no override).
        # NOTE: clamp to a literal 100 -- get_stat_limit("baby_desire") returns 0 (no stat_limits
        # entry) and would zero the stat. level-up notification stays suppressed; the mod's own
        # desire ladder (vt_handle_baby_desire) is the player-facing feedback.
        if not getattr(Girl.fix_stats, "_vt_baby_desire", False):
            _vt_orig_fix_stats = Girl.fix_stats

            def vt_fix_stats(self, hide_notification=False):
                _vt_orig_fix_stats(self, hide_notification=hide_notification)
                if hasattr(self, "baby_desire_xp"):
                    self.level_up_attribute("baby_desire", hide_notification=True)
                    self.baby_desire = int(max(min(self.baby_desire, 100), 0))

            vt_fix_stats._vt_baby_desire = True
            Girl.fix_stats = vt_fix_stats

        print("VT MOD: Successfully patched Girl class with advanced fertility system")

# Define the vaginal sex and creampie handlers inside a python block
init -3 python:
    def vt_handle_cum_fetishes(action_name: str, target_girl: Girl, fetish_category: str) -> None:
        """
        Handles fetish progression based on sex actions and creampie events
        fetish_category: 'oral', 'vaginal', 'anal', 'boobs', 'thighs', 'ass_cumshot', 'pussy_cumshot'
        """
        #Debugger
        renpy.log(f"VT MOD: FETISH PROGRESSION TRIGGER - Action: {action_name}, Girl: {target_girl.full_name}, Category: {fetish_category}")
         
        # Body part mapping for notifications
        body_part_map = {
            'oral': 'in her mouth',
            'vaginal': 'inside her pussy',
            'anal': 'inside her ass',
            'boobs': 'on her breasts',
            'thighs': 'on her thighs',
            'oral_cumshot': 'on her face',
            'ass_cumshot': 'on her ass',
            'pussy_cumshot': 'on her pussy'
        }
        
        # Get body part description for notifications
        body_part_term = body_part_map.get(fetish_category, fetish_category)
        
        # Base progression values based on creampie type
        fetish_map = {
            # INTERNAL CREAMPIE ACTIONS 
            'oral': ('oral_cum_fetish', 1, 4, 'oral_cum_fixation', 'oral_cum_slut', 'oral_cum_addict', 'oral_cum_devotee'),
            'vaginal': ('vaginal_cum_fetish', 3, 5, 'vaginal_cum_fixation', 'vaginal_cum_dumpster', 'vaginal_cum_addict', 'vaginal_cum_devotee'),
            'anal': ('anal_cum_fetish', 1, 3, 'anal_cum_fixation', 'anal_cum_dumpster', 'anal_cum_addict', 'anal_cum_devotee'),
            # EXTERNAL CUMSHOT ACTIONS
            'boobs': ('boob_cum_fetish', 1, 3, 'boob_cum_fixation', 'boob_cum_slut', 'boob_cum_addict', 'boob_cum_devotee'),
            'thighs': ('thigh_cum_fetish', 1, 2, 'thigh_cum_fixation', 'thigh_cum_slut', 'thigh_cum_addict', 'thigh_cum_devotee'),
            'oral_cumshot': ('oral_cum_fetish', 1, 4, 'oral_cum_fixation', 'oral_cum_slut', 'oral_cum_addict', 'oral_cum_devotee'),
            'ass_cumshot': ('ass_cum_fetish', 1, 2, 'ass_cum_fixation', 'ass_cum_slut', 'ass_cum_addict', 'ass_cum_devotee'),
            'pussy_cumshot': ('pussy_cum_fetish', 1, 3, 'pussy_cum_fixation', 'pussy_cum_slut', 'pussy_cum_addict', 'pussy_cum_devotee')
        }
        
        if fetish_category not in fetish_map:
            return

        fetish_attr, base_min, base_max, secondary_trait, tertiary_trait, quaternary_trait, quinary_trait = fetish_map[fetish_category]
    
        # Base progression chance (higher for creampie actions)
        #is_creampie = "creampie" in action_name or action_name in ["facial", "sleep_facial", "cumshot_boobs","sleep_cumshot_boobs", "cumshot_thighs","sleep_cumshot_thighs", "cumshot_ass","sleep_cumshot_ass", "cumshot_pussy","sleep_cumshot_pussy"]
        is_creampie = "creampie" in action_name 
        progression_chance = 40 if is_creampie else 20
        
        # Awareness modifier - unaware of broken condom increases progression
        unaware_modifier = 0
        awareness_attr = f"aware_{fetish_category}_condom"
        if hasattr(target_girl, awareness_attr) and not getattr(target_girl, awareness_attr):
            unaware_modifier = 25  # Higher progression when unaware of broken condom
        
        # Trait-based modifier - girls with related traits progress faster
        trait_modifier = 0
        # Safety check for trait system
        if hasattr(target_girl, 'has_trait'):
            # Highest bonus for ultimate trait (Devotee - Tier 5)
            if target_girl.has_trait(quinary_trait):
                trait_modifier += 25
            # High bonus for Addict tier (Tier 4)
            elif target_girl.has_trait(quaternary_trait):
                trait_modifier += 15
            # Medium bonus for Slut/Dumpster tier (Tier 3)
            elif target_girl.has_trait(tertiary_trait):
                trait_modifier += 8
            # Small bonus for Fixation tier (Tier 2)
            elif target_girl.has_trait(secondary_trait):
                trait_modifier += 4
        
        # Current fetish level modifier (diminishing returns at higher levels)
        current_level = getattr(target_girl, fetish_attr, 0)
        diminishing_return = max(0.15, 1 - (current_level / 100))  # Minimum 25% progression rate
        
        # Corruption modifier - more corrupted girls progress faster
        corruption_modifier = target_girl.corruption * 0.15
        
        # Baby desire modifier - higher baby desire increases progression
        # baby_desire_modifier = 0
        # if hasattr(target_girl, 'baby_desire'):
            # baby_desire_modifier = target_girl.baby_desire * 0.1
        
        # Special modifier for pussy cumshot (higher relevance to pregnancy)
        pussy_modifier = 0
        if fetish_category == "pussy_cumshot":
            # External cumshot on pussy has special relevance to pregnancy
            pussy_modifier = 5
        
        # Final progression chance
        final_chance = min(95, progression_chance + unaware_modifier + trait_modifier + corruption_modifier + pussy_modifier) * diminishing_return
    
        # Roll for progression
        if renpy.random.randint(1, 100) <= final_chance:
            
            # Calculate progression amount
            progression_amount = renpy.random.randint(base_min, base_max)
            
            # Special bonus for high baby desire
            if hasattr(target_girl, 'baby_desire') and target_girl.baby_desire > 70:
                progression_amount += 2
                renpy.log(f"VT MOD: {target_girl.first_name} has high baby desire, increasing fetish progression")
            
            # Additional bonus if already has related trait
            if hasattr(target_girl, 'has_trait'):
                if target_girl.has_trait(quinary_trait):
                    trait_modifier += 25  # Highest bonus for ultimate trait
                elif target_girl.has_trait(quaternary_trait):
                    trait_modifier += 15
                elif target_girl.has_trait(tertiary_trait):
                    trait_modifier += 8
                elif target_girl.has_trait(secondary_trait):
                    trait_modifier += 4
            
            # Special bonus for pussy cumshot (direct pregnancy relevance)
            if fetish_category == "pussy_cumshot" and target_girl.baby_desire > 50:
                progression_amount += 2
                renpy.log(f"VT MOD: {target_girl.first_name} has moderate baby desire, extra pussy cumshot progression")
            
            # Apply progression (capped at 100)
            new_level = min(100, current_level + progression_amount)
            
            #debug catch
            renpy.log(f"VT MOD: FETISH PROGRESSION - {target_girl.first_name}'s {fetish_attr} increased from {current_level} to {new_level}. (+{progression_amount})")
            
            setattr(target_girl, fetish_attr, new_level)
            
            # --- START: CORRECTED TRAIT ACQUISITION LOGIC ---
            # --- START: DEFINITIVE TRAIT LOGIC ---
            if hasattr(target_girl, 'add_trait') and hasattr(target_girl, 'remove_trait'):

                # Define ALL possible traits for this fetish to manage them
                all_possible_traits = [
                    secondary_trait, 
                    tertiary_trait, 
                    f"conflicted_{tertiary_trait}", 
                    quaternary_trait, 
                    quinary_trait
                ]
                
                # --- PART 1: HANDLE DOWNGRADES (if score decreased) ---
                if new_level < current_level:
                    target_girl.check_traits()
                    renpy.log(f"VT MOD: Fetish decreased for {target_girl.first_name}, forced trait check.")

                # --- PART 2: HANDLE UPGRADES (if score increased) ---
                if new_level > current_level:
                    trait_to_add = None
                    notification_message = ""

                    # --- ALWAYS CLEAN UP FIRST ---
                    # Remove all existing related traits to prevent overlap, NO MATTER WHAT.
                    traits_removed = []
                    for trait_name in all_possible_traits:
                        if target_girl.has_trait(trait_name):
                            target_girl.remove_trait(trait_name)
                            traits_removed.append(trait_name)
                    if traits_removed:
                        renpy.log(f"VT MOD: CLEANUP - Removed traits '{', '.join(traits_removed)}' from {target_girl.first_name}.")

                    # --- NOW, DECIDE WHICH TRAIT TO ADD ---
                    # 100% ULTIMATE FIXATION TRAIT (Devotee)
                    if new_level >= 100 and not target_girl.has_trait(quinary_trait):
                        trait_to_add = quinary_trait
                        notification_message = f"{target_girl.first_name} is completely devoted to cum {body_part_term}!"
                    
                    # 90% NEAR-COMPLETE OBSESSION TRAIT (Addict)
                    elif new_level >= 90 and not target_girl.has_trait(quaternary_trait):
                        trait_to_add = quaternary_trait
                        notification_message = f"{target_girl.first_name} has become utterly addicted to cum {body_part_term}!"

                    # 75% STRONG FIXATION TRAIT (Slut/Dumpster)
                    elif new_level >= 75 and not target_girl.has_trait(tertiary_trait):
                        if target_girl.has_trait("conservative") or target_girl.has_trait("reserved"):
                            conflicted_trait = f"conflicted_{tertiary_trait}"
                            if not target_girl.has_trait(conflicted_trait):
                                trait_to_add = conflicted_trait
                                notification_message = f"{target_girl.first_name} seems conflicted but can't resist cum {body_part_term}..."
                            else: # Already conflicted, now embracing it
                                trait_to_add = tertiary_trait
                                notification_message = f"{target_girl.first_name} has stopped fighting her desire for cum {body_part_term}!"
                        else:
                            trait_to_add = tertiary_trait
                            notification_message = f"{target_girl.first_name} is becoming very obsessed with cum {body_part_term}!"

                    # 50% MODERATE INTEREST TRAIT (Fixation)
                    elif new_level >= 50 and not target_girl.has_trait(secondary_trait):
                        trait_to_add = secondary_trait
                        notification_message = f"{target_girl.first_name} seems to be developing a taste for cum {body_part_term}..."
                    
                    # If a trait was chosen, add it
                    if trait_to_add:
                        target_girl.add_trait(trait_to_add)
                        vt_fetish_notify(notification_message, duration=4)
                        renpy.log(f"VT MOD: CLEANUP - Added trait '{trait_to_add}' to {target_girl.first_name}.")

            # --- END: DEFINITIVE TRAIT LOGIC ---
            # --- END: FINAL TRAIT LOGIC ---


            # --- END: CORRECTED TRAIT ACQUISITION LOGIC ---
 
            # Special notifications at threshold levels
            if new_level >= 100 and current_level < 100:
                # TOTAL FIXATION - ULTIMATE OBSESSION
                vt_fetish_notify(f"{target_girl.first_name} has become utterly addicted to cum {body_part_term} - she craves it constantly!", duration=5.0)
            elif new_level >= 90 and current_level < 90:
                # NEAR-COMPLETE OBSESSION
                vt_fetish_notify(f"{target_girl.first_name} is completely addicted to cum {body_part_term}!", duration=4.5)
            elif new_level >= 75 and current_level < 75:
                # STRONG FIXATION
                vt_fetish_notify(f"{target_girl.first_name} is becoming very obsessed with cum {body_part_term}!", duration=4.0)
            elif new_level >= 50 and current_level < 50:
                # DEVELOPING INTEREST
                vt_fetish_notify(f"{target_girl.first_name} seems to be developing a taste for cum {body_part_term}...", duration=3.5)
            elif new_level >= 25 and current_level < 25:
                # FIRST NOTICEABLE INTEREST
                vt_fetish_notify(f"{target_girl.first_name} seems curious about cum {body_part_term}...", duration=3.0)

    # Tuning knob: baby_desire is XP-backed, but the per-creampie amounts below were authored as
    # old 0-100 "points". Multiply them by this to get XP. ~50 makes a high-fetish creampie land
    # in the ballpark of a deliberate dialogue choice (250,750), with typical ones smaller. Adjust
    # here to make creampies push pregnancy desire faster or slower.
    VT_BABY_DESIRE_XP_PER_POINT = 50

    def vt_handle_baby_desire(action_name: str, target_girl: Girl, creampie_type: str) -> None:
        """
        Handles baby desire increases with fetish integration
        creampie_type: 'oral', 'vaginal', 'anal', 'boobs', 'thighs', 'ass_cumshot', 'pussy_cumshot'
        """
        # Exit early if not a creampie action
        if "creampie" not in action_name and "cumshot" not in action_name and action_name != "facial":
            return
            
        # Base chance to increase baby desire (varies by creampie type)
        base_chances = {
            'oral': 5,
            'vaginal': 20,
            'anal': 2,
            'boobs': 2,
            'thighs': 2,
            'ass_cumshot': 1,
            'pussy_cumshot': 10
        }
        
        if creampie_type not in base_chances:
            return
            
        base_chance = base_chances[creampie_type]
        
        # Get relevant fetish level
        fetish_level = 0
        fetish_attr = f"{creampie_type}_cum_fetish"
        if hasattr(target_girl, fetish_attr):
            fetish_level = getattr(target_girl, fetish_attr)
        
        # Higher fetish level = higher chance to increase baby desire
        fetish_modifier = fetish_level * 0.1  # 0.1% increase per fetish level
        
        # Awareness modifier - unaware of broken condom increases chance
        unaware_modifier = 0
        awareness_attr = f"aware_{creampie_type}_condom"
        if hasattr(target_girl, awareness_attr) and not getattr(target_girl, awareness_attr):
            unaware_modifier = 20
        
        # Special modifier for pussy cumshot (highest pregnancy relevance)
        pussy_modifier = 0
        if creampie_type == "pussy_cumshot":
            pussy_modifier = 10
        
        # Calculate final chance
        final_chance = min(85, base_chance + fetish_modifier + unaware_modifier + pussy_modifier)
        
        # Roll for baby desire increase
        if renpy.random.randint(1, 100) <= final_chance:
            # Amount to increase (varies by creampie type)
            increase_amounts = {
                'oral': max(1, int(fetish_level * 0.1) + renpy.random.randint(1, 3)),
                'vaginal': max(1, int(fetish_level * 0.15) + renpy.random.randint(1, 3)),
                'anal': max(1, int(fetish_level * 0.05) + renpy.random.randint(1, 2)),
                'boobs': max(1, int(fetish_level * 0.05) + renpy.random.randint(1, 2)),
                'thighs': max(1, int(fetish_level * 0.02) + renpy.random.randint(1, 1)),
                'ass_cumshot': max(1, int(fetish_level * 0.03) + renpy.random.randint(1, 1)),
                'pussy_cumshot': max(1, int(fetish_level * 0.1) + renpy.random.randint(1, 3))
            }
            
            increase_amount = increase_amounts[creampie_type]
            # Route through the XP economy (modify_stat -> patched fix_stats levels + clamps it,
            # with the base level-up popup suppressed). The band thresholds below then read the
            # freshly-leveled 0-100 value.
            target_girl.modify_stat("baby_desire", increase_amount * VT_BABY_DESIRE_XP_PER_POINT, hide_notification=True)

            renpy.log(f"VT MOD: {target_girl.first_name}'s baby desire increased to {target_girl.baby_desire}")
            vt_fetish_notify(f"{target_girl.first_name}'s desire for pregnancy increased!", duration=2.0)
            
            # Special reactions at high levels
            if not target_girl.pregnant:
                if target_girl.baby_desire >= 99 and target_girl.baby_desire <100:
                    # TOTAL PREGNANCY OBSESSION
                    if not getattr(target_girl, 'baby_obsession_notified', False):
                        if target_girl.kids_with_player > 0:
                            vt_fetish_notify(f"{target_girl.first_name} is utterly obsessed with getting pregnant by you - she talks about wanting to have more of your babies!", duration=5.5)
                        else:
                            vt_fetish_notify(f"{target_girl.first_name} is utterly obsessed with getting pregnant by you - she talks about wanting to have your babies constantly!", duration=5.5)
                    target_girl.baby_obsession_notified = True
                elif target_girl.baby_desire >= 90 and target_girl.baby_desire <=99:
                    # NEAR-COMPLETE PREGNANCY FIXATION
                    if not getattr(target_girl, 'baby_fixation_notified', False):
                        if target_girl.kids_with_player > 0:
                            vt_fetish_notify(f"{target_girl.first_name} is completely fixated on having your baby - she's fixated on growing your family!", duration=5.0)
                        else:
                            vt_fetish_notify(f"{target_girl.first_name} is completely fixated on having your baby - she's started planning your future family!", duration=5.0)
                        target_girl.baby_fixation_notified = True
                elif target_girl.baby_desire >= 75:
                    # STRONG PREGNANCY DESIRE
                    vt_fetish_notify(f"{target_girl.first_name} is becoming very obsessed with having your baby!", duration=4.5)
                elif target_girl.baby_desire >= 50:
                    # DEVELOPING BABY INTEREST
                    vt_fetish_notify(f"{target_girl.first_name} seems to be thinking about having your baby...", duration=4.0)
                elif target_girl.baby_desire >= 25:
                    # FIRST NOTICEABLE INTEREST
                    vt_fetish_notify(f"{target_girl.first_name} seems curious about the idea of having your baby...", duration=3.5)

            if target_girl.baby_desire < 100:
                target_girl.baby_obsession_notified = False
            if target_girl.baby_desire < 90 or target_girl.baby_desire > 99:
                target_girl.baby_fixation_notified = False

    def vt_catch_oral_sex(action_name: str, action_failed: bool, target_girl: Union[Girl, None], girls_who_got_impacts: list[Girl]) -> None:
        """Handles ALL oral sex actions including blowjobs, facials, and creampies"""
        # Exit early if action failed or no target girl
        if action_failed or not target_girl:
            return
            
        # Check if this is ANY oral sex action (including facial)
        if action_name not in ["blowjob", "sleep_blowjob", "use_mouth", "creampie_mouth","sleep_creampie_mouth", "facial", "sleep_facial"]:
            return
            
        # Initialize all required attributes if missing
        if not hasattr(target_girl, "oral_sex_count"):
            target_girl.oral_sex_count = 0
        if not hasattr(target_girl, "last_oral_sex"):
            target_girl.last_oral_sex = -1
        if not hasattr(target_girl, "first_time_oral"):
            target_girl.first_time_oral = True
        if not hasattr(target_girl, "oral_sensitivity"):
            target_girl.oral_sensitivity = 0
        
        # Track when this happened - SAFELY
        vt_current_day = 0
        try:
            vt_current_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log("vt_catch_oral_sex ERROR: Global 'time_manager' variable not found!")
            return

        # Increment oral sex counter and track last occurrence
        target_girl.oral_sex_count += 1
        target_girl.last_oral_sex = vt_current_day
        target_girl.had_sex_today = True
        
        # First time oral sex handling
        if target_girl.first_time_oral:
            target_girl.first_time_oral = False
            renpy.log(f"VT MOD: First Time Oral with {target_girl.full_name}!")
            vt_firsttime_notify(f"{target_girl.first_name}'s first oral experience with you!", duration=5.0)
        
        # Check for active condom
        condom_used = player.condom_active != "raw"
        premium_condom = player.condom_active == "premium"
        cheap_condom = player.condom_active == "cheap"
        
        # --- START: ACTION NOTIFICATION LOGIC ---
        # Notify for the start of the act, if it's not a creampie/facial action.
        if action_name in ["blowjob", "sleep_blowjob", "use_mouth"]:
            if not condom_used:
                dialogtext = f"{target_girl.first_name} eagerly wraps her lips around your bare cock, and sucks you."
                renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
            else:
                dialogtext = f"{target_girl.first_name} eagerly suck you off, her tongue teasing your tip through the latex of the condom."
                renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        # --- END: ACTION NOTIFICATION LOGIC ---
        # --- START: CONDOM BREAKAGE LOGIC (HAPPENS FIRST, BEFORE ANYTHING ELSE) ---
        # This block runs first to set the state of the condom before the action is described.
        if condom_used and not player.condom_broke:
            premium_condom = player.condom_active == "premium"
            cheap_condom = player.condom_active == "cheap"
            break_occurred = False

            if cheap_condom:
                base_break_chance = 35
                additional_break_chance = min(15, player.condom_cum * 5)
                total_break_chance = base_break_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Cheap condom broke during oral sex with {target_girl.first_name}! (Chance: {total_break_chance}%)")
                    
            elif premium_condom:
                base_break_chance = 2
                additional_break_chance = min(3, player.condom_cum * 1)
                total_break_chance = base_break_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Premium condom broke during oral sex with {target_girl.first_name}! (Chance: {total_break_chance}%)")
            
            # Handle breakage consequences IMMEDIATELY after it occurs
            if break_occurred:
                # Player's immediate notification
                vt_firsttime_notify("You feel a sudden tear! And the sudden bliss of her warm moist mouth on your cock!", duration=3.0)
                # Determine if girl is aware of breakage
                awareness_chance = 70  # Base chance to notice breakage
                # Modify chance based on girl's traits
                if hasattr(target_girl, "oral_sensitivity"):
                    awareness_chance += target_girl.oral_sensitivity
                # Oral-specific awareness modifiers
                if hasattr(target_girl, "oral_focus"):
                    awareness_chance += 10  # More focused on oral = more likely to notice
                if renpy.random.randint(1, 100) <= awareness_chance:
                    # Girl becomes aware of broken condom
                    target_girl.aware_oral_condom = True
                    vt_fetish_notify(f"{target_girl.first_name} gasps around your cock as the distinct taste of your precum hits her tongue, the barrier between you suddenly vanished!", duration=5.0)
                    renpy.log(f"VT MOD: {target_girl.first_name} became aware of broken oral condom")
                else:
                    # Girl remains unaware
                    target_girl.aware_oral_condom = False
                    vt_fetish_notify(f"{target_girl.first_name} moans softly, swirling her tongue around your now-exposed cock, loving the new, intense flavor.", duration=4.0)
                    renpy.log(f"VT MOD: {target_girl.first_name} remained unaware of broken oral condom")
            else:
                target_girl.aware_oral_condom = False
        # --- END: CONDOM BREAKAGE LOGIC --

        # --- LOGIC: Prepare dialogue and determine which label to call ---
        dialogtext = ""
        call_label = None

        # --- START: ACTION-SPECIFIC NOTIFICATION LOGIC  ---
        # This block can now correctly react to whether the condom is intact or broken.
        # Handle the Blowjob/Use Mouth action
        if action_name in ["blowjob", "sleep_blowjob", "use_mouth"]:
            if not condom_used:
                target_girl.aware_oral_condom = False
                dialogtext = f"{target_girl.first_name} moans around your bare cock, her warm, wet mouth wrapping perfectly around your shaft as she tastes your precum."
            elif player.condom_broke: # A condom was used and it broke
                if target_girl.aware_oral_condom:
                    dialogtext = f"Panicked, {target_girl.first_name} gags slightly as the taste of your raw cock floods her mouth, but she doesn't dare stop."
                else:
                    target_girl.aware_oral_condom = False
                    dialogtext = f"{target_girl.first_name} redoubles her efforts, confused by the sudden, intense taste of your skin as the broken condom slips away."
            else: # A condom was used and it held
                target_girl.aware_oral_condom = False
                dialogtext = f"{target_girl.first_name} expertly works the latex-covered shaft with her tongue, her warm mouth making you throb with need."
        
        # Handle the Oral Creampie action
        elif action_name in ["creampie_mouth", "sleep_creampie_mouth"]:
            player.condom_dirty = True
            if not condom_used:
                target_girl.aware_oral_condom = False
                target_girl.oral_cum += 1
                dialogtext = f"You groan, burying your raw cock to the hilt in {target_girl.first_name}'s throat. It clenches around you as you erupt, pumping a massive, hot load directly into her eager, willing belly."
            elif player.condom_broke: # The condom broke earlier, this is a bareback creampie
                target_girl.aware_oral_condom = True
                player.condom_cum = 0
                dialogtext = f"{target_girl.first_name}'s eyes go wide in shock as your bare cock erupts, flooding her mouth with the sudden, hot taste of your cum!"
            else: # Condom held
                target_girl.aware_oral_condom = False
                player.condom_cum += 1
                dialogtext = f"{target_girl.first_name} moans around your shaft, her tongue feeling the condom swell with your hot load as you fill her mouth."

        # Handle the Facial action
        elif action_name in ["facial", "sleep_facial"]:            
            player.condom_dirty = True
            if not condom_used:
                target_girl.aware_oral_condom = False
                dialogtext = f"You groan, aiming your bare cock as thick ropes of cum splash across {target_girl.first_name}'s eager face."
            elif player.condom_broke: # The condom broke earlier, this is a bareback facial
                target_girl.aware_oral_condom = True
                player.condom_cum = 0
                dialogtext = f"The condom shatters! Your hot, raw cum splatters across {target_girl.first_name}'s shocked face."
            else: # Condom held
                target_girl.aware_oral_condom = False
                player.condom_cum += 1
                dialogtext = f"{target_girl.first_name} flinches slightly as the warm, fluid-filled condom presses against her cheek."
        # --- END: ACTION-SPECIFIC NOTIFICATION LOGIC ---
        
        # Handle fetish progression using centralized function
        if action_name in ["creampie_mouth","sleep_creampie_mouth", "facial", "sleep_facial"]:
            vt_handle_cum_fetishes(action_name, target_girl, fetish_category="oral")
        
        # Handle baby desire increase for creampie/facial actions
        if action_name in ["creampie_mouth","sleep_creampie_mouth"]:
            vt_handle_baby_desire(action_name, target_girl, "oral")

        renpy.log(f"VT MOD: Oral sex processing complete for {target_girl.first_name}")
        
        # --- FINAL STEP: Call the dialogue label ---
        renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        # if call_label and dialogtext:
            # renpy.call(call_label, dialogtext=dialogtext)
        
        #renpy.restart_interaction()

    database_apply_action_impacts_hooks.append(vt_catch_oral_sex)

    def vt_catch_boobs_sex(action_name: str, action_failed: bool, target_girl: Union[Girl, None], girls_who_got_impacts: list[Girl]) -> None:
        """Handles boob sex actions including titfucks and cumshots on breasts with proper condom breakage mechanics"""
        # Exit early if action failed or no target girl
        if action_failed or not target_girl:
            return
            
        # Check if this is a boob sex action
        if action_name not in ["fuck_boobs","sleep_fuck_boobs", "cumshot_boobs","sleep_cumshot_boobs"]:
            return
            
        # Initialize all required attributes if missing
        if not hasattr(target_girl, "boob_sex_count"):
            target_girl.boob_sex_count = 0
        if not hasattr(target_girl, "last_boob_sex"):
            target_girl.last_boob_sex = -1
        if not hasattr(target_girl, "first_time_boobs"):
            target_girl.first_time_boobs = True
        
        # Track when this happened - SAFELY
        vt_current_day = 0
        try:
            vt_current_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log("vt_catch_boobs_sex ERROR: Global 'time_manager' variable not found!")
            return
        
        # Increment boob sex counter and track last occurrence
        target_girl.boob_sex_count += 1
        target_girl.last_boob_sex = vt_current_day
        target_girl.had_sex_today = True
        
        # First time boob sex handling
        if target_girl.first_time_boobs:
            target_girl.first_time_boobs = False
            renpy.log(f"VT MOD: First Time Boob Sex with {target_girl.full_name}!")
            vt_firsttime_notify(f"{target_girl.first_name}'s first boob experience with you!", duration=5.0)
        
        # Check for active condom
        condom_used = player.condom_active != "raw"
        
        # --- START: CONDOM BREAKAGE LOGIC (HAPPENS FIRST) ---
        # This block runs first to set the state of the condom, with chances based on the specific action.
        if condom_used and not player.condom_broke:
            premium_condom = player.condom_active == "premium"
            cheap_condom = player.condom_active == "cheap"
            break_occurred = False
            
            # Set base chances based on the action's roughness/intensity
            if action_name == "fuck_boobs":
                # ROUGH ACTION: Highest chance from friction
                cheap_base_chance = 45
                premium_base_chance = 5
                cheap_mult = 6
                premium_mult = 1
            elif action_name == "sleep_fuck_boobs":
                # GENTLE ACTION: Lowest chance
                cheap_base_chance = 20
                premium_base_chance = 1
                cheap_mult = 3
                premium_mult = 0.5
            else: # cumshot_boobs, sleep_cumshot_boobs
                # PRESSURE ACTION: Moderate chance from the force of ejaculation
                cheap_base_chance = 30
                premium_base_chance = 3
                cheap_mult = 4
                premium_mult = 0.7

            if cheap_condom:
                additional_break_chance = min(20, player.condom_cum * cheap_mult)
                total_break_chance = cheap_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Cheap condom broke during {action_name} with {target_girl.first_name}! (Chance: {total_break_chance}%)")
                    
            elif premium_condom:
                additional_break_chance = min(5, player.condom_cum * premium_mult)
                total_break_chance = premium_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Premium condom broke during {action_name} with {target_girl.first_name}! (Chance: {total_break_chance}%)")
            
            # Handle breakage consequences IMMEDIATELY after it occurs
            if break_occurred:
                # Player's immediate notification
                vt_firsttime_notify("You feel the condom give way, and suddenly the soft, warm flesh of her breasts is wrapped directly around your bare cock!", duration=4.0)
                
                # Determine if girl is aware of breakage
                awareness_chance = 65  # Slightly lower than vaginal for boob sex
                
                # Modify chance based on girl's traits
                if hasattr(target_girl, "notice_sensitivity"):
                    awareness_chance += target_girl.notice_sensitivity
                
                if renpy.random.randint(1, 100) <= awareness_chance:
                    # Girl becomes aware of broken condom
                    target_girl.aware_boob_condom = True
                    vt_fetish_notify(f"{target_girl.first_name}'s eyes fly wide open as the barrier vanishes! She feels every hot, throbbing inch of your raw cock against her soft breasts!", duration=5.0)
                    renpy.log(f"VT MOD: {target_girl.first_name} became aware of broken boob condom")
                else:
                    # Girl remains unaware
                    target_girl.aware_boob_condom = False
                    vt_fetish_notify(f"{target_girl.first_name} is completely lost in the pleasure, pushing her breasts together, unaware the condom has failed and your bare cock is now sliding against her skin.", duration=3.0)
                    renpy.log(f"VT MOD: {target_girl.first_name} remained unaware of broken boob condom")
            else:
                target_girl.aware_boob_condom = False
        # --- END: CONDOM BREAKAGE LOGIC ---
 
        # --- LOGIC: Prepare dialogue and determine which label to call ---
        dialogtext = ""
        call_label = None
 
        # Handle the Titfuck action
        if action_name in ["fuck_boobs", "sleep_fuck_boobs"]:
            if not condom_used:
                target_girl.aware_boob_condom = False
                dialogtext = f"The feeling is incredible as you thrust between {target_girl.first_name}'s soft breasts. Her warm, silky skin wraps around your hot, throbbing raw cock, every vein pulsing against her."
            elif player.condom_broke: # A condom was used and it broke
                if target_girl.aware_boob_condom:
                    dialogtext = f"A gasp escapes {target_girl.first_name}'s lips as she feels your hot, bare cock against her skin. Panicked but aroused, she continues to press her breasts around you, the raw intensity overwhelming."
                else:
                    target_girl.aware_boob_condom = False
                    dialogtext = f"{target_girl.first_name} moans louder, pressing her breasts tighter, unknowingly enjoying the intense friction of your now-bare cock against her skin."
            else: # A condom was used and it held
                target_girl.aware_boob_condom = False
                dialogtext = f"{target_girl.first_name} squeezes her soft tits around your cock, the thin latex glistening as you slide smoothly between her warm breasts, building an intense pressure."

        # Handle the Boobs Creampie action
        elif action_name in ["cumshot_boobs", "sleep_cumshot_boobs"]:
            player.condom_dirty = True
            if not condom_used:
                target_girl.aware_boob_condom = False
                dialogtext = f"You groan, your raw cock pulsing against her soft skin as you cover {target_girl.first_name}'s breasts in hot cum. She moans, arching her back to feel every drop."
            elif player.condom_broke: # The condom broke earlier, this is a bareback cumshot
                player.condom_cum = 0
                dialogtext = f"The sudden heat of your bare cock makes {target_girl.first_name} gasp. You erupt, and she cries out in pure bliss as your hot seed floods directly onto her sensitive skin."
            else: # Condom held
                player.condom_cum += 1
                target_girl.aware_boob_condom = False
                dialogtext = f"{target_girl.first_name} bites her lip, feeling the condom pulse and swell with your hot cum between her warm breasts, the throbbing elicits a groan from her."
        
        # Handle fetish progression using centralized function
        if action_name in ["cumshot_boobs","sleep_cumshot_boobs"]:
            vt_handle_cum_fetishes(action_name, target_girl, fetish_category="boobs")
        
        # Handle baby desire increase for creampie actions
        if action_name in ["cumshot_boobs","sleep_cumshot_boobs"]:
            vt_handle_baby_desire(action_name, target_girl, "boobs")

        renpy.log(f"VT MOD: Boob sex processing complete for {target_girl.first_name}")
        
        # --- FINAL STEP: Call the dialogue label ---
        renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        # if call_label and dialogtext:
            # renpy.call(call_label, dialogtext=dialogtext)
            
        #renpy.restart_interaction()

    database_apply_action_impacts_hooks.append(vt_catch_boobs_sex)

    def vt_catch_thighs_sex(action_name: str, action_failed: bool, target_girl: Union[Girl, None], girls_who_got_impacts: list[Girl]) -> None:
        """Handles thigh sex actions including thigh jobs and cumshots on thighs with proper condom breakage mechanics"""
        # Exit early if action failed or no target girl
        if action_failed or not target_girl:
            return
            
        # Check if this is a thigh sex action
        if action_name not in ["fuck_thighs", "cumshot_thighs","sleep_cumshot_thighs"]:
            return
            
        # Initialize all required attributes if missing
        if not hasattr(target_girl, "thigh_sex_count"):
            target_girl.thigh_sex_count = 0
        if not hasattr(target_girl, "last_thigh_sex"):
            target_girl.last_thigh_sex = -1
        if not hasattr(target_girl, "first_time_thighs"):
            target_girl.first_time_thighs = True
        
        # Track when this happened - SAFELY
        vt_current_day = 0
        try:
            vt_current_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log("vt_catch_thighs_sex ERROR: Global 'time_manager' variable not found!")
            return
        
        # Increment thigh sex counter and track last occurrence
        target_girl.thigh_sex_count += 1
        target_girl.last_thigh_sex = vt_current_day
        target_girl.had_sex_today = True
        
        # First time thigh sex handling
        if target_girl.first_time_thighs:
            target_girl.first_time_thighs = False
            renpy.log(f"VT MOD: First Time Thigh Sex with {target_girl.full_name}!")
            vt_firsttime_notify(f"{target_girl.first_name}'s first thigh experience with you!", duration=5.0)
        
        # Check for active condom
        condom_used = player.condom_active != "raw"
        
        # --- START: CONDOM BREAKAGE LOGIC (HAPPENS FIRST) ---
        # This block runs first to set the state of the condom, with chances based on the specific action.
        if condom_used and not player.condom_broke:
            premium_condom = player.condom_active == "premium"
            cheap_condom = player.condom_active == "cheap"
            break_occurred = False
            
            # Set base chances based on the action's intensity
            if action_name == "fuck_thighs":
                # THIGH JOB: Moderate chance from friction
                cheap_base_chance = 30
                premium_base_chance = 2
                cheap_mult = 4
                premium_mult = 0.5
            else: # cumshot_thighs, sleep_cumshot_thighs
                # CUMSHOT: Lower chance, as it's less about friction and more about pressure
                cheap_base_chance = 20
                premium_base_chance = 1
                cheap_mult = 2
                premium_mult = 0.2

            if cheap_condom:
                additional_break_chance = min(15, player.condom_cum * cheap_mult)
                total_break_chance = cheap_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Cheap condom broke during {action_name} with {target_girl.first_name}! (Chance: {total_break_chance}%)")
                    
            elif premium_condom:
                additional_break_chance = min(3, player.condom_cum * premium_mult)
                total_break_chance = premium_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Premium condom broke during {action_name} with {target_girl.first_name}! (Chance: {total_break_chance}%)")
            
            # Handle breakage consequences IMMEDIATELY after it occurs
            if break_occurred:
                # Player's immediate notification
                vt_firsttime_notify("A sudden tear! Her dripping pussy kisses your now-bare cock with every thrust!", duration=3.0)
                
                # Determine if girl is aware of breakage
                awareness_chance = 60  # Slightly lower than vaginal for thigh sex
                
                # Modify chance based on girl's traits
                if hasattr(target_girl, "notice_sensitivity"):
                    awareness_chance += target_girl.notice_sensitivity
                
                if renpy.random.randint(1, 100) <= awareness_chance:
                    # Girl becomes aware of broken condom
                    target_girl.aware_thigh_condom = True
                    vt_preg_notify(f"{target_girl.first_name} gasps as she feels your hot, raw cock sliding against her, her own juices dripping onto the shaft!", duration=4.0)
                    renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
                else:
                    # Girl remains unaware
                    target_girl.aware_thigh_condom = False
                    vt_preg_notify("{target_girl.first_name} is lost in ecstasy, her wet pussy lips kissing your cock, unaware the condom is gone.", duration=4.0)
                    renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
            else:
                target_girl.aware_thigh_condom = False

        # --- LOGIC: Prepare dialogue and determine which label to call ---
        dialogtext = ""
        call_label = None

        # --- END: CONDOM BREAKAGE LOGIC ---
        # Handle the Thigh Job action
        if action_name == "fuck_thighs":
            if not condom_used:
                target_girl.aware_thigh_condom = False
                dialogtext = f"You groan, thrusting your bare, throbbing cock between {target_girl.first_name}'s soft thighs. Her wet pussy lips kiss your shaft with every slide, dripping her arousal onto you as you almost slip inside."
            elif player.condom_broke: # A condom was used and it broke
                if target_girl.aware_thigh_condom:
                    dialogtext = f"A gasp escapes {target_girl.first_name}'s lips as she feels your hot, bare cock against her skin. Panicked but aroused, she keeps her thighs wrapped tightly around you."
                else:
                    target_girl.aware_thigh_condom = False
                    dialogtext = f"{target_girl.first_name} whimpers in pleasure, squeezing her thighs tighter, completely unaware that the condom is gone and your raw cock is now sliding against her dripping pussy."
            else: # A condom was used and it held
                target_girl.aware_thigh_condom = False
                dialogtext = f"You thrust between {target_girl.first_name}'s soft thighs, the latex of the condom a thin barrier against her hot, dripping skin."

        # Handle the Thighs Creampie action
        elif action_name in ["cumshot_thighs", "sleep_cumshot_thighs"]:
            player.condom_dirty = True
            if not condom_used:
                target_girl.aware_thigh_condom = False
                dialogtext = f"With a loud groan, your bare cock erupts, coating {target_girl.first_name}'s inner thighs and pussy with thick, hot ropes of your cum."
            elif player.condom_broke: # The condom broke earlier, this is a bareback cumshot
                target_girl.aware_thigh_condom = True
                player.condom_cum = 0
                dialogtext = f"Your bare cock erupts uncontrollably, painting {target_girl.first_name}'s inner thighs and her eager pussy with thick streams of cum!"
            else: # Condom held
                player.condom_cum += 1
                target_girl.aware_thigh_condom = False
                dialogtext = f"{target_girl.first_name} bites her lip, watching the condom swell and pulse against her pussy as you fill it with your cum."
        # --- END: ACTION-SPECIFIC NOTIFICATION LOGIC ---
        
        # Handle fetish progression using centralized function
        if action_name in ["cumshot_thighs", "sleep_cumshot_thighs"]:
            vt_handle_cum_fetishes(action_name, target_girl, fetish_category="thighs")
        
        # Very small chance of pregnancy from thigh sex (if creampie occurred)
        if action_name in ["cumshot_thighs", "sleep_cumshot_thighs"] and renpy.random.randint(1, 100) <= 2:
            target_girl.vaginal_cum = getattr(target_girl, 'vaginal_cum', 0) + 1
            #renpy.log(f"VT MOD: Added minimal cum unit (thigh cumshot with pregnancy risk). Total: {target_girl.vaginal_cum}")
        
        # Handle baby desire increase for creampie actions
        if action_name in ["cumshot_thighs", "sleep_cumshot_thighs"]:
            vt_handle_baby_desire(action_name, target_girl, "thighs")

        renpy.log(f"VT MOD: Thigh sex processing complete for {target_girl.first_name}")
        
        # --- FINAL STEP: Call the dialogue label ---
        renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        # if call_label and dialogtext:
            # renpy.call(call_label, dialogtext=dialogtext)
        
        #renpy.restart_interaction()
        
    database_apply_action_impacts_hooks.append(vt_catch_thighs_sex)

    def vt_catch_vaginal_sex(action_name: str, action_failed: bool, target_girl: Union[Girl, None], girls_who_got_impacts: list[Girl]) -> None:
        """Handles regular vaginal sex (fuck_pussy) without creampie"""
        if action_failed or not target_girl:
            return
            
        if action_name not in ["fuck_pussy", "sleep_fuck_pussy"]:
            return
            
        # Initialize fetish attributes if missing
        if not hasattr(target_girl, "vaginal_sex_count"):
            target_girl.vaginal_sex_count = 0
        if not hasattr(target_girl, "last_vaginal_sex"):
            target_girl.last_vaginal_sex = -1
        if not hasattr(target_girl, "first_time_pussy"):
            target_girl.first_time_pussy = True
        if not hasattr(target_girl, "having_vaginal_sex"):
            target_girl.having_vaginal_sex = False

        # Track when this happened - SAFELY
        vt_current_day = 0
        try:
            vt_current_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log("vt_catch_vaginal_sex ERROR: Global 'time_manager' variable not found!")
            return

        vt_today = vt_current_day
        target_girl.vaginal_sex_count += 1
        target_girl.last_vaginal_sex = vt_today
        target_girl.had_sex_today = True
        
        # Check for active condom
        condom_used = player.condom_active != "raw"
        girl_awake = True
        if action_name in ["sleep_fuck_pussy"]:
            girl_awake = False
        
        #vt_fetish_notify(f"{target_girl.first_name}'s is awake? {girl_awake}", duration=5.0)
        #dialogtext = ""
        # --- START: CONDOM BREAKAGE LOGIC (HAPPENS FIRST) ---
        # This block runs first to set the state of the condom before the action is described.
        if condom_used and not player.condom_broke:
            premium_condom = player.condom_active == "premium"
            cheap_condom = player.condom_active == "cheap"
            break_occurred = False
            
            # Set base chances for vaginal sex
            cheap_base_chance = 25
            premium_base_chance = 1
            cheap_mult = 3
            premium_mult = 0.75

            if cheap_condom:
                additional_break_chance = min(10, player.condom_cum * cheap_mult)
                total_break_chance = cheap_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Cheap condom broke during vaginal sex with {target_girl.first_name}! (Chance: {total_break_chance}%)")
                    
            elif premium_condom:
                additional_break_chance = min(2, player.condom_cum * premium_mult)
                total_break_chance = premium_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Premium condom broke during vaginal sex with {target_girl.first_name}! (Chance: {total_break_chance}%)")
            
            # Handle breakage consequences IMMEDIATELY after it occurs
            if break_occurred:
                # Determine if girl is aware of breakage
                awareness_chance = 75  # Higher awareness for vaginal sex
                
                # Modify chance based on girl's traits
                if hasattr(target_girl, "notice_sensitivity"):
                    awareness_chance += target_girl.notice_sensitivity
                
                if renpy.random.randint(1, 100) <= awareness_chance and girl_awake:
                    # Girl becomes aware of broken condom
                    target_girl.aware_vaginal_condom = True
                    #dialogtext = f"{target_girl.first_name} gasps, her pussy clenching tightly around your now-bare, throbbing shaft as she feels the intense heat of your skin!"
                    #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
                else:
                    # Girl remains unaware
                    target_girl.aware_vaginal_condom = False
                    #dialogtext = f"{target_girl.first_name} moans loudly, her wet hole sucking and milking your raw cock, completely lost in the blissful new sensation!"
                    #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
            else:
                target_girl.aware_vaginal_condom = False
        # --- END: CONDOM BREAKAGE LOGIC ---
        
        # --- LOGIC: Prepare dialogue and determine which label to call ---
        dialogtext = ""
        call_label = None
        
        # Handle the fuck action
        if action_name in ["fuck_pussy", "sleep_fuck_pussy"]:
            # --- NO CONDOM USED --- hymen, vaginal_sex checks - no need for condom awareness
            if not condom_used:
                target_girl.aware_vaginal_condom = False
                #penetrative sex step
                if not target_girl.having_vaginal_sex:
                    target_girl.having_vaginal_sex = True
                    call_label = "vt_fetish_dialog"
                    if target_girl.hymen:
                        # Hymen is still present and will be broken
                        if girl_awake:
                            dialogtext = f"You share a passionate kiss as you press into {target_girl.first_name}. With a soft cry, her barrier gives way, and your bare cock sinks into her incredible, slick heat, forging an intimate connection as your bodies become one."
                        else: # Asleep
                            dialogtext = f"You gently part {target_girl.first_name}'s sleeping folds. A moment of resistance, and then your bare cock is sheathed in her liquid warmth, her body shuddering with a soft sigh as it welcomes you in."
                    else:
                        # No hymen to break
                        if girl_awake:
                            dialogtext = f"You groan as your raw, throbbing cock sinks into {target_girl.first_name}'s dripping wet pussy. Her hot, tight walls wrap around you, pulling you deeper into her welcoming heat."
                        else: # Asleep
                            dialogtext = f"You groan as your raw cock sinks into {target_girl.first_name}'s sleeping, dripping warm wet pussy. Her body arches slightly, a soft moan on her lips as her pussy instinctively clenches, drawing you deeper into its intoxicating embrace."
                else:
                    #plays on every subsequent thrust
                    if target_girl.hymen:
                        # Hymen is still present and will be broken
                        if girl_awake:
                            dialogtext = f"You move together in a passionate rhythm, as you press into {target_girl.first_name}, your bare cock stroking her deepest, most sensitive places. Her moans grow louder with every thrust, her body completely lost to the pleasure."
                        else: # Asleep
                            dialogtext = f"You thrust steadily into {target_girl.first_name}'s sleeping form, her wet pussy gripping you tightly. Her soft moans and the slick sounds of your union fill the quiet room."
                    else:
                        # No hymen to break
                        if girl_awake:
                            dialogtext = f"A shared moan of pure bliss escapes you both as your bare cock slides into {target_girl.first_name}'s welcoming heat. Her slick walls embrace you, pulsing with a desperate need for your touch."
                        else: # Asleep
                            dialogtext = f"You sink your bare cock into {target_girl.first_name}'s sleeping warmth. Her body arches slightly, a soft moan on her lips as her pussy instinctively clenches, drawing you deeper."
                #renpy.call("vt_raw_dialog", dialogtext=dialogtext)
            # --- CONDOM BROKE ---
            elif player.condom_broke:
                call_label = "vt_broken_condom_dialog"
                #penetrative sex step
                if not target_girl.having_vaginal_sex:
                    target_girl.having_vaginal_sex = True
                    if target_girl.aware_vaginal_condom:
                        if target_girl.hymen:
                            # Hymen is still present and will be broken
                            if girl_awake:
                                dialogtext = f"A sharp gasp from {target_girl.first_name} as the latex tears, followed by a cry of pure ecstasy as your bare cock sink balls-deep into her hot, claiming her virginity. The sudden, intimate contact triggers a wave of pleasure that floods her senses."
                            else:
                                dialogtext = f"The condom gives way as your raw cock violates her sleeping innocence, tearing through her cherry and is suddenly enveloped by {target_girl.first_name}'s liquid fire. Her sleeping form jolts, her pussy clamping down on you as a deep, shuddering moan escapes her."
                        else:
                            if girl_awake:
                                dialogtext = f"The condom snaps! {target_girl.first_name}'s eyes fly wide as the barrier vanishes. A gasp of shock melts into a wanton moan as she feels your skin on hers, knowing every thrust now will be sending bolts of pure pleasure through her body."
                            else:
                                dialogtext = f"The condom tears! {target_girl.first_name} whimpers in her sleep, her brow furrowing in pleasure as the intense new heat of your bare cock sends waves of bliss through her dreaming body. "
                    else:
                        if target_girl.hymen:
                            # Hymen is still present and will be broken
                            if girl_awake:
                                dialogtext = f"{target_girl.first_name} cries out from the sudden, intense sensation as the condom tears and your bare cock fills her. She doesn't understand why it feels so much better, only that a powerful orgasm is already building."
                            else:
                                dialogtext = f"The condom rips, and {target_girl.first_name} whimpers in her sleep. Her sleeping body clenches instinctively, her wet pussy sucking and milking your now-bare cock as it fills her for the very first time."
                        else:
                            if girl_awake:
                                dialogtext = f"The condom tears! {target_girl.first_name} moans with abandon, her pussy gripping you tightly. She's lost in the pleasure, completely unaware that the thin latex is gone and your bare cock is now plumbing her depths."
                            else:
                                dialogtext = f"The condom tears! {target_girl.first_name} sighs contentedly in her sleep, her wet hole sucking at your bare cock, her body instinctively seeking the deeper pleasure it now feels without understanding why."
                                
                #plays on every subsequent thrust
                else:
                    if target_girl.aware_vaginal_condom:
                        if target_girl.hymen:
                            # Hymen is still present and will be broken
                            if girl_awake:
                                dialogtext = f"You pound into {target_girl.first_name}'s freshly deflowered pussy, her cries of pleasure echoing with every skin-on-slap. She's completely surrendered to the raw passion of the moment."
                            else:
                                dialogtext = f"You thrust into {target_girl.first_name}'s sleeping pussy, the sounds of her wetness growing louder. Her body rocks with your movements, soft moans escaping with each deep stroke of your bare cock."
                        else:
                            if girl_awake:
                                dialogtext = f"You drive your bare cock into {target_girl.first_name} again and again, her body trembling uncontrollably. She wraps her legs around you, pulling you in, desperate for every inch of your raw shaft."
                            else:
                                dialogtext = f"{target_girl.first_name}'s sleeping pussy gushes around your bare cock, her body completely overcome by the raw pleasure. Her soft moans are a constant, breathless counterpoint to your thrusts."
                    else:
                        if target_girl.hymen:
                            # Hymen is still present and will be broken
                            if girl_awake:
                                dialogtext = f"You thrust into {target_girl.first_name}'s tight heat, her body responding with a passion that surprises you both. She moans, pushing her hips back to meet yours, lost in the blissful new feelings."
                            else:
                                dialogtext = f"You stroke your bare cock in and out of {target_girl.first_name}'s sleeping pussy. Her body instinctively matches your rhythm, her slick walls clenching around you as soft, blissful sighs escape her lips."
                        else:
                            if girl_awake:
                                dialogtext = f"{target_girl.first_name} moans your name, her body slick with sweat and desire. She grinds against you, her pussy clenching rhythmically, milking your bare cock for all the pleasure it's worth."
                            else:
                                dialogtext = f"You continue to fuck {target_girl.first_name}'s sleeping form, her body now completely pliant and receptive. Her pussy pulses around your bare cock, a silent testament to the pleasure she's experiencing even in her dreams."
                                
                #renpy.call("vt_broken_condom_dialog", dialogtext=dialogtext)
                
            else: # A condom was used and it held
                target_girl.aware_vaginal_condom = False
                call_label = "vt_condom_dialog"
                if not target_girl.having_vaginal_sex:
                    target_girl.having_vaginal_sex = True
                    if target_girl.hymen:
                        # Hymen is present but not broken
                        if girl_awake:
                            dialogtext = f"You press against {target_girl.first_name}'s sacred gate, the thin latex a tantalizing barrier. She whimpers softly, her body trembling with anticipation, craving the moment you will finally become one."
                        else: # Asleep
                            dialogtext = f"You gently nudge your latex-covered cock against {target_girl.first_name}'s sleeping flower. Her body tenses with a soft gasp, a dream-like shiver running through her as she feels the tender pressure."
                    else:
                        # No hymen, standard protected sex
                        if girl_awake:
                            dialogtext = f"You slide into {target_girl.first_name}'s welcoming heat, her slick walls gripping you tightly. A shared moan of pleasure fills the air as your bodies move together in a passionate rhythm."
                        else: # Asleep
                            dialogtext = f"You slip your sheathed cock into {target_girl.first_name}'s sleeping warmth. Her body sighs, a soft sound of contentment, as she unconsciously pushes back against you, accepting your gentle presence."
                else:
                    #plays on every subsequent thrust
                    if target_girl.hymen:
                        # Hymen is still present but not broken
                        if girl_awake:
                            dialogtext = f"You move with a gentle, steady rhythm, pressing against {target_girl.first_name}'s barrier. Her body trembles, soft whimpers of need escaping her as she teeters on the edge of bliss."
                        else: # Asleep
                            dialogtext = f"You thrust gently into {target_girl.first_name}'s sleeping pussy, the thin latex still holding. Her body responds with soft sighs and shivers, her dream world filled with a growing, pleasant pressure."
                    else:
                        # No hymen, standard protected sex
                        if girl_awake:
                            dialogtext = f"You find a perfect, passionate rhythm with {target_girl.first_name}, your sheathed cock sliding in and out of her slick heat. Her moans of pleasure guide you, her body arching to meet your every thrust."
                        else: # Asleep
                            dialogtext = f"You continue to make love to {target_girl.first_name}'s sleeping form. Her breathing deepens, her body rocking subtly with yours, completely accepting of the gentle, protected pleasure you're giving her."
                
                #renpy.call("vt_condom_dialog", dialogtext=dialogtext)


        # First time sex
        if target_girl.first_time_pussy and target_girl.hymen:
            # Break hymen if intact
            target_girl.hymen = False
            target_girl.first_time_pussy = False
            vt_firsttime_notify(f"{target_girl.first_name} is no longer a virgin!!", duration=5.0)
        elif target_girl.first_time_pussy:
            target_girl.first_time_pussy = False
            vt_firsttime_notify(f"{target_girl.first_name}'s first time sex with you!", duration=5.0)

        # Handle fetish progression using centralized function
        if not condom_used or player.condom_broke:
            vt_handle_cum_fetishes(action_name, target_girl, fetish_category="vaginal")

        # --- FINAL STEP: Call the dialogue label ---
        if call_label and dialogtext:
            renpy.call(call_label, dialogtext=dialogtext)

        renpy.log(f"VT MOD: Vaginal sex tracked for {target_girl.full_name}")
        #renpy.restart_interaction()
    
    database_apply_action_impacts_hooks.append(vt_catch_vaginal_sex)

    def vt_catch_cumshot_pussy(action_name: str, action_failed: bool, target_girl: Union[Girl, None], girls_who_got_impacts: list[Girl]) -> None:
        """Handles external cumshot on pussy (cumshot_pussy) with proper pregnancy mechanics"""
        # Exit early if action failed or no target girl
        if action_failed or not target_girl:
            return
            
        # Check if this is a cumshot on pussy action
        if action_name not in ["cumshot_pussy","sleep_cumshot_pussy"]:
            return
            
        # Initialize all required attributes if missing
        if not hasattr(target_girl, "pussy_cumshot_count"):
            target_girl.pussy_cumshot_count = 0
        if not hasattr(target_girl, "last_pussy_cumshot"):
            target_girl.last_pussy_cumshot = -1
        if not hasattr(target_girl, "first_time_pussy_cumshot"):
            target_girl.first_time_pussy_cumshot = True
        
        # Track when this happened - SAFELY
        vt_current_day = 0
        try:
            vt_current_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log("vt_catch_cumshot_pussy ERROR: Global 'time_manager' variable not found!")
            return
        
        # Increment pussy cumshot counter and track last occurrence
        target_girl.pussy_cumshot_count += 1
        target_girl.last_pussy_cumshot = vt_current_day
        target_girl.had_sex_today = True

        # First time pussy cumshot handling
        if target_girl.first_time_pussy_cumshot:
            target_girl.first_time_pussy_cumshot = False
            renpy.log(f"VT MOD: First Time Pussy Cumshot with {target_girl.full_name}!")
            vt_firsttime_notify(f"{target_girl.first_name}'s first pussy cumshot experience with you!", duration=5.0)
        
        # Check for active condom
        condom_used = player.condom_active != "raw"
        
        # --- LOGIC: Prepare dialogue and determine which label to call ---
        dialogtext = ""
        call_label = None
        
        # --- START: CONDOM BREAKAGE LOGIC (HAPPENS FIRST) ---
        # This block runs first to set the state of the condom before the cumshot is described.
        if condom_used and not player.condom_broke:
            premium_condom = player.condom_active == "premium"
            cheap_condom = player.condom_active == "cheap"
            break_occurred = False
            
            # Set base chances for a pussy cumshot
            cheap_base_chance = 25
            premium_base_chance = 2
            cheap_mult = 3
            premium_mult = 0.7

            if cheap_condom:
                additional_break_chance = min(12, player.condom_cum * cheap_mult)
                total_break_chance = cheap_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Cheap condom broke during pussy cumshot with {target_girl.first_name}! (Chance: {total_break_chance}%)")
                    
            elif premium_condom:
                additional_break_chance = min(3, player.condom_cum * premium_mult)
                total_break_chance = premium_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Premium condom broke during pussy cumshot with {target_girl.first_name}! (Chance: {total_break_chance}%)")
            
            # Handle breakage consequences IMMEDIATELY after it occurs
            if break_occurred:
                # Player's immediate notification
                vt_firsttime_notify("As you stroke yourself hard, you feel the condom tear right as you are about to cum!", duration=3.0)
                
                # Determine if girl is aware of breakage
                awareness_chance = 65  # Higher than other areas due to direct contact
                
                # Modify chance based on girl's traits
                if hasattr(target_girl, "notice_sensitivity"):
                    awareness_chance += target_girl.notice_sensitivity
                
                if renpy.random.randint(1, 100) <= awareness_chance:
                    # Girl becomes aware of broken condom
                    target_girl.aware_pussy_cumshot_condom = True
                    vt_fetish_notify(f"{target_girl.first_name}'s eyes go wide as the raw heat of your cock kisses her soaked vulva, the sudden sensation making her realize the condom is gone!", duration=5.0)
                    renpy.log(f"VT MOD: {target_girl.first_name} became aware of broken pussy cumshot condom")
                else:
                    # Girl remains unaware
                    target_girl.aware_pussy_cumshot_condom = False
                    vt_fetish_notify(f"{target_girl.first_name} is lost in ecstasy, moaning as your bare cock slides against her dripping pussy, completely unaware the condom has failed.", duration=3.0)
                    renpy.log(f"VT MOD: {target_girl.first_name} remained unaware of broken pussy cumshot condom")
            else:
                target_girl.aware_pussy_cumshot_condom = False
        # --- END: CONDOM BREAKAGE LOGIC ---
        player.condom_dirty = True
        # Determine pregnancy risk (external cumshot can still cause pregnancy!)
        pregnancy_risk = False
        
        if not condom_used:
            dialogtext = f"You grind your raw cock against {target_girl.first_name}'s dripping vulva, her soaked lips kissing your shaft with every thrust. With a shared groan of pure ecstasy, you erupt, painting her pussy with thick hot cum that mixes with her gushing juices as it drips down her slit."
            #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
            pregnancy_risk = True
        elif player.condom_broke: # The condom broke earlier, this is a bareback cumshot
            dialogtext = f"The condom tears away just as you erupt! Your bare cock pulses against {target_girl.first_name}'s soaked pussy, and you both cry out as you feel the intense, direct heat of each other. You coat her vulva with your hot, sticky cum, a blissful, mind-blowing wave of pleasure crashing over you both."
            #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
            pregnancy_risk = True
        else: # Condom held however risk remains.
            if renpy.random.randint(1, 100) <= 5 and player.condom_active == "cheap":  # 5% residual risk
                pregnancy_risk = True
                dialogtext = f"You thrust hard against {target_girl.first_name}'s slick heat, the cheap condom straining as you cum. A thrilling jolt shoots through you both as you see a trickle of your load leak from the base, mixing with her dripping pussy juices in a risky, intimate mess."
                #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
            else:
                pregnancy_risk = False
                dialogtext = f"You grind your cock against {target_girl.first_name}'s soaked vulva, her wetness drenching the condom. You both moan in shared ecstasy as you pump the latex full of your cum, the intense heat of her pussy radiating through the thin barrier, bringing you both to the edge."
                #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        # Add vaginal cum if there's pregnancy risk (even though it's external, some may enter)
        if pregnancy_risk:
            target_girl.vaginal_cum += 1
            # Handle fetish progression using centralized function
            vt_handle_cum_fetishes(action_name, target_girl, fetish_category="pussy_cumshot")
            # Handle baby desire increase - FIXED: USING CENTRALIZED FUNCTION
            vt_handle_baby_desire(action_name, target_girl, "pussy_cumshot")
        
        # Immediate pregnancy check (for external cumshot with pregnancy risk)
        if pregnancy_risk and not target_girl.pregnant and not target_girl.just_had_baby:
            try:
                # Get fertility and birth control values
                bc_eff = target_girl.birthcontrol_efficiency()
                eff_fert = target_girl.effective_fertility()
                
                # External cumshot has reduced fertility chance compared to internal creampie
                reduced_fertility = eff_fert * 0.3
                
                renpy.log(f"VT MOD: External cumshot pregnancy check - BC efficiency: {bc_eff:.1f}%, Effective fertility: {reduced_fertility:.1f}%")
                
                # Birth control failed
                if renpy.random.randint(1, 100) > bc_eff:
                    # Fertility chance succeeded
                    if check_probability(reduced_fertility):
                        # SUCCESS - PREGNANCY HAPPENING
                        target_girl.pregnant = True
                        target_girl.knows_pregnant = False
                        target_girl.preg_progress_days = 1
                        target_girl.preg_announce = False
                        target_girl.days_since_last_birth = 0
                        target_girl.preg_father = "player"  # THIS IS A PLAYER-ORIGINATED PREGNANCY
                        # Get current day
                        target_girl.preg_start_day = vt_current_day
                        target_girl.preg_end_day = vt_current_day + 250 + renpy.random.randint(0, 10)
                        
                        renpy.log(f"VT MOD: {target_girl.full_name} got pregnant from external cumshot! (Chance: {reduced_fertility:.1f}%)")
                        vt_preg_notify( f"You watch, utterly captivated, as a heavy drop of your seed clings to her swollen lips. With a soft shudder from {target_girl.first_name}, her slick parting swallows it whole, disappearing into her fertile heat.", duration=5.0)
                        #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
                    else:
                        renpy.log(f"VT MOD: Pregnancy failed from external cumshot - fertility check ({reduced_fertility:.1f}%)")
                else:
                    renpy.log(f"VT MOD: Pregnancy failed from external cumshot - birth control succeeded ({bc_eff:.1f}%)")
                    
            except Exception as e:
                renpy.log(f"VT MOD ERROR: External cumshot pregnancy calculation failed - {str(e)}")        
        renpy.log(f"VT MOD: Pussy cumshot processing complete for {target_girl.first_name}")

        renpy.call("vt_raw_dialog", dialogtext=dialogtext)

        #renpy.restart_interaction()

    database_apply_action_impacts_hooks.append(vt_catch_cumshot_pussy)

    def vt_catch_vaginal_creampie(action_name: str, action_failed: bool, target_girl: Union[Girl, None], girls_who_got_impacts: list[Girl]) -> None:
        """Handles vaginal creampie actions (creampie_pussy)"""
        if action_failed or not target_girl:
            return
            
        if action_name not in ["creampie_pussy","sleep_creampie_pussy"]:
            return
            
        # Initialize fetish attributes if missing
        if not hasattr(target_girl, "vaginal_sex_count"):
            target_girl.vaginal_sex_count = 0
        if not hasattr(target_girl, "last_vaginal_sex"):
            target_girl.last_vaginal_sex = -1
        if not hasattr(target_girl, "first_time_pussy"):
            target_girl.first_time_pussy = True

        # Check for active condom
        condom_used = player.condom_active != "raw"
        premium_condom = player.condom_active == "premium"
        cheap_condom = player.condom_active == "cheap"
        
        # Track when this happened - SAFELY
        vt_current_day = 0
        try:
            vt_current_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log("vt_catch_vaginal_creampie ERROR: Global 'time_manager' variable not found!")
            return
        
        # Track creampie event
        target_girl.last_vaginal_sex = vt_current_day
        target_girl.had_sex_today = True
        
        # Check for active condom
        condom_used = player.condom_active != "raw"
        
        # --- LOGIC: Prepare dialogue and determine which label to call ---
        dialogtext = ""
        call_label = None
        
        # --- START: CONDOM BREAKAGE LOGIC (HAPPENS FIRST) ---
        # This block runs first to set the state of the condom before the creampie is described.
        if condom_used and not player.condom_broke:
            premium_condom = player.condom_active == "premium"
            cheap_condom = player.condom_active == "cheap"
            break_occurred = False
            
            # Set base chances for a vaginal creampie (high pressure)
            cheap_base_chance = 35
            premium_base_chance = 2
            cheap_mult = 5
            premium_mult = 1

            if cheap_condom:
                additional_break_chance = min(15, player.condom_cum * cheap_mult)
                total_break_chance = cheap_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Cheap condom broke during creampie with {target_girl.first_name}! (Chance: {total_break_chance}%)")
                    
            elif premium_condom:
                additional_break_chance = min(3, player.condom_cum * premium_mult)
                total_break_chance = premium_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Premium condom broke during creampie with {target_girl.first_name}! (Chance: {total_break_chance}%)")
            
            # Handle breakage consequences IMMEDIATELY after it occurs
            if break_occurred:
                # Player's immediate notification
                vt_firsttime_notify("A sudden tear! The frustrating latex is gone, and you feel her hot, dripping vulva kiss your raw, throbbing cock as it sinks deep into her wet heat!", duration=3.0)                
                # Determine if girl is aware of breakage
                awareness_chance = 60  # Slightly lower than oral for vaginal
                
                # Modify chance based on girl's traits
                if hasattr(target_girl, "notice_sensitivity"):
                    awareness_chance += target_girl.notice_sensitivity
                
                if renpy.random.randint(1, 100) <= awareness_chance:
                    # Girl becomes aware of broken condom
                    target_girl.aware_vaginal_condom = True
                    vt_fetish_notify(f"{target_girl.first_name} cries out in shock and pure ecstasy as the barrier vanishes! She feels every inch of your hot, bare cock stretching her, her pussy instantly beginning to milk your shaft for your seed.", duration=5.0)
                else:
                    # Girl remains unaware
                    target_girl.aware_vaginal_condom = False
                    vt_fetish_notify(f"{target_girl.first_name} moans like a whore, her pussy walls gripping you tighter than ever. She's too lost in the overwhelming pleasure to realize she's now taking your raw, bare cock with every thrust.", duration=5.0)
            else:
                target_girl.aware_vaginal_condom = False
        # --- END: CONDOM BREAKAGE LOGIC ---
        # Track creampie event
        player.condom_dirty = True
        if not condom_used:
            target_girl.aware_vaginal_condom = False
            dialogtext = f"You drive your raw, throbbing cock deep into {target_girl.first_name}'s dripping wet pussy. Her soft vulva kiss your shaft with every thrust, her tight hole sucking you as you slide back and forth. You groan as her pussy clenches, milking you for all you're worth, and explode, flooding her warm, eager womb with thick, potent ropes of your cum."
            pregnancy_risk = True
        elif player.condom_broke: # The condom broke earlier, this is a bareback creampie
            player.condom_cum = 0
            target_girl.aware_vaginal_condom = True
            dialogtext = f"The tearing latex sends a jolt through you both! Your bare, hot cock is now sheathed in {target_girl.first_name}'s unbelievably wet pussy. You feel her walls grip you, milking your shaft as you erupt uncontrollably, flooding her unprotected womb with every drop of your potent seed!"
            pregnancy_risk = True
        else: # Condom held
            player.condom_cum += 1
            target_girl.aware_vaginal_condom = False
            dialogtext = f"{target_girl.first_name}'s dripping pussy grips you tightly, her juices flowing down your cock as you bury yourself to the hilt. You throb powerfully inside her, groaning as you pump the condom full of your cum, the thin latex the only thing separating you from her fertile depths."
            pregnancy_risk = False
        # --- END: CUMSHOT NOTIFICATION LOGIC ---
        # --- START: PREGNANCY RISK LOGIC ---
        # This block now uses the pregnancy_risk flag set above.
        if pregnancy_risk:
            target_girl.vaginal_cum = getattr(target_girl, 'vaginal_cum', 0) + 1
            
            # Handle fetish progression using centralized function
            vt_handle_cum_fetishes(action_name, target_girl, fetish_category = "vaginal")
            
            # Handle baby desire increase using centralized function
            vt_handle_baby_desire(action_name, target_girl, "vaginal")
            
            # Immediate pregnancy check
            if not target_girl.pregnant and not target_girl.just_had_baby:
                try:
                    # Get fertility and birth control values
                    bc_eff = target_girl.birthcontrol_efficiency()
                    eff_fert = target_girl.effective_fertility()
                    
                    renpy.log(f"VT MOD: Pregnancy check - BC efficiency: {bc_eff:.1f}%, Effective fertility: {eff_fert:.1f}%")
                    
                    # Birth control failed
                    if renpy.random.randint(1, 100) > bc_eff:
                        # Fertility chance succeeded
                        if check_probability(eff_fert):
                            # SUCCESS - PREGNANCY HAPPENING
                            target_girl.pregnant = True
                            target_girl.knows_pregnant = False
                            target_girl.preg_progress_days = 1
                            target_girl.preg_announce = False
                            target_girl.days_since_last_birth = 0
                            target_girl.preg_father = "player"  # THIS IS A PLAYER-ORIGINATED PREGNANCY
                            # Track when this happened - SAFELY
                            vt_current_day = 0
                            try:
                                vt_current_day = time_manager.total_days
                            except NameError:
                                # This should not happen if game_init.rpy is loaded correctly
                                renpy.log("vt_catch_vaginal_creampie # Birth control failed ERROR: Global 'time_manager' variable not found!")
                                return
                                
                            target_girl.preg_start_day = vt_current_day
                            target_girl.preg_end_day = vt_current_day + 250 + renpy.random.randint(0, 10)
                            
                            renpy.log(f"VT MOD: {target_girl.full_name} got pregnant! (Chance: {eff_fert:.1f}%)")
                            vt_preg_notify(f"Your raw cock throbs deep inside her. {target_girl.first_name}'s pussy grips you, milking your shaft as you pump a massive load directly into her fertile womb.", duration=5.0)
                        else:
                            renpy.log(f"VT MOD: Pregnancy failed - fertility check ({eff_fert:.1f}%)")
                    else:
                        renpy.log(f"VT MOD: Pregnancy failed - birth control succeeded ({bc_eff:.1f}%)")
                        
                except Exception as e:
                    renpy.log(f"VT MOD ERROR: Pregnancy calculation failed - {str(e)}")
        # --- END: PREGNANCY RISK LOGIC ---
        
        # --- FINAL STEP: Call the dialogue label ---
        renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        # if call_label and dialogtext:
            # renpy.call(call_label, dialogtext=dialogtext)
        
        #renpy.restart_interaction()

    database_apply_action_impacts_hooks.append(vt_catch_vaginal_creampie)

    def vt_catch_anal_sex(action_name: str, action_failed: bool, target_girl: Union[Girl, None], girls_who_got_impacts: list[Girl]) -> None:
        """Handles regular anal sex (fuck_ass) without creampie"""
        if action_failed or not target_girl:
            return
            
        if action_name not in ["fuck_ass","sleep_fuck_ass"]:
            return
            
        # Initialize fetish attributes if missing
        if not hasattr(target_girl, "anal_sex_count"):
            target_girl.anal_sex_count = 0
        if not hasattr(target_girl, "last_anal_sex"):
            target_girl.last_anal_sex = -1
        if not hasattr(target_girl, "first_time_anal"):
            target_girl.first_time_anal = True

        # Track when this happened - SAFELY
        vt_current_day = 0
        try:
            vt_current_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log("vt_catch_anal_sex failed ERROR: Global 'time_manager' variable not found!")
            return
        target_girl.anal_sex_count += 1
        target_girl.last_anal_sex = vt_current_day
        target_girl.had_sex_today = True

        # Check for active condom
        condom_used = player.condom_active != "raw"
        
        # --- LOGIC: Prepare dialogue and determine which label to call ---
        dialogtext = ""
        call_label = None
        
        # --- START: CONDOM BREAKAGE LOGIC (HAPPENS FIRST) ---
        # This block runs first to set the state of the condom before the action is described.
        if condom_used and not player.condom_broke:
            premium_condom = player.condom_active == "premium"
            cheap_condom = player.condom_active == "cheap"
            break_occurred = False
            
            # Set base chances for anal sex
            cheap_base_chance = 25
            premium_base_chance = 1
            cheap_mult = 3
            premium_mult = 0.5

            if cheap_condom:
                additional_break_chance = min(10, player.condom_cum * cheap_mult)
                total_break_chance = cheap_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Cheap condom broke during anal sex with {target_girl.first_name}! (Chance: {total_break_chance}%)")
                    
            elif premium_condom:
                additional_break_chance = min(2, player.condom_cum * premium_mult)
                total_break_chance = premium_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Premium condom broke during anal sex with {target_girl.first_name}! (Chance: {total_break_chance}%)")
            
            # Handle breakage consequences IMMEDIATELY after it occurs
            if break_occurred:
                # Player's immediate notification
                vt_firsttime_notify("The thin barrier tears! You feel her hot, tight ass grip your now-bare, throbbing cock!", duration=3.0)
                
                # Determine if girl is aware of breakage
                awareness_chance = 55  # Lower awareness for anal sex
                
                # Modify chance based on girl's traits
                if hasattr(target_girl, "notice_sensitivity"):
                    awareness_chance += target_girl.notice_sensitivity
                
                if renpy.random.randint(1, 100) <= awareness_chance:
                    # Girl becomes aware of broken condom
                    target_girl.aware_anal_condom = True
                    vt_fetish_notify(f"{target_girl.first_name}'s breath hitches as she feels the sudden, intense heat of your raw cock stretching her ass, the torn latex a forgotten memory!", duration=5.0)
                else:
                    # Girl remains unaware
                    target_girl.aware_anal_condom = False
                    vt_fetish_notify(f"{target_girl.first_name} is too lost in ecstasy, her ass clenching around your bare cock, completely oblivious to the condom's failure!", duration=3.0)
            else:
                target_girl.aware_anal_condom = False
        # --- END: CONDOM BREAKAGE LOGIC ---
        if not condom_used:
            target_girl.aware_anal_condom = False
            dialogtext = f"You groan as your raw, throbbing cock sinks into {target_girl.first_name}'s tight ass. Her wet pussy drips down, coating your shaft as her forbidden hole grips and milks you with every intense thrust."
        elif player.condom_broke: # A condom was used and it broke
            if target_girl.aware_anal_condom:
                dialogtext = f"A mix of panic and intense pleasure floods {target_girl.first_name} as she feels your now-bare cock throbbing inside her ass, every vein and pulse sending shivers through her body."
            else:
                target_girl.aware_anal_condom = False
                dialogtext = f"{target_girl.first_name} cries out in bliss, completely unaware the condom is gone. Your raw cock pistons into her ass, her dripping pussy soaking the base of your shaft with each deep, powerful thrust."
        else: # A condom was used and it held
            target_girl.aware_anal_condom = False
            dialogtext = f"You slide into {target_girl.first_name}'s tight ass, the latex a dull barrier compared to the feeling of her dripping pussy lips soaking your shaft with each thrust."
        
        # Handle fetish progression using centralized function
        vt_handle_cum_fetishes(action_name, target_girl, fetish_category="anal")

        # First time anal sex
        if target_girl.first_time_anal:
            target_girl.first_time_anal = False
            renpy.log(f"VT MOD: First Time Anal with you {target_girl.full_name}!")
            vt_firsttime_notify(f"{target_girl.first_name}'s first anal with you!", duration=5.0)

        # --- FINAL STEP: Call the dialogue label ---
        renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        # if call_label and dialogtext:
            # renpy.call(call_label, dialogtext=dialogtext)

        #renpy.restart_interaction()
        renpy.log(f"VT MOD: Anal sex tracked for {target_girl.full_name}")

    database_apply_action_impacts_hooks.append(vt_catch_anal_sex)

    def vt_catch_cumshot_ass(action_name: str, action_failed: bool, target_girl: Union[Girl, None], girls_who_got_impacts: list[Girl]) -> None:
        """Handles external cumshot on ass (cumshot_ass) with proper mechanics"""
        # Exit early if action failed or no target girl
        if action_failed or not target_girl:
            return
            
        # Check if this is a cumshot on ass action
        if action_name not in ["cumshot_ass","sleep_cumshot_ass"]:
            return
            
        # Initialize all required attributes if missing
        if not hasattr(target_girl, "ass_cumshot_count"):
            target_girl.ass_cumshot_count = 0
        if not hasattr(target_girl, "last_ass_cumshot"):
            target_girl.last_ass_cumshot = -1
        if not hasattr(target_girl, "first_time_ass_cumshot"):
            target_girl.first_time_ass_cumshot = True
        
        # Track when this happened - SAFELY
        vt_current_day = 0
        try:
            vt_current_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log("vt_catch_cumshot_ass failed ERROR: Global 'time_manager' variable not found!")
            return
        
        # Increment ass cumshot counter and track last occurrence
        target_girl.ass_cumshot_count += 1
        target_girl.last_ass_cumshot = vt_current_day
        target_girl.had_sex_today = True
        
        # First time ass cumshot handling
        if target_girl.first_time_ass_cumshot:
            target_girl.first_time_ass_cumshot = False
            renpy.log(f"VT MOD: First Time Ass Cumshot with {target_girl.full_name}!")
            vt_firsttime_notify(f"{target_girl.first_name}'s first ass cumshot experience with you!", duration=5.0)
        
        # Check for active condom
        condom_used = player.condom_active != "raw"
        
        # --- LOGIC: Prepare dialogue and determine which label to call ---
        dialogtext = ""
        call_label = None
        
        # --- START: CONDOM BREAKAGE LOGIC (HAPPENS FIRST) ---
        # This block runs first to set the state of the condom before the cumshot is described.
        if condom_used and not player.condom_broke:
            premium_condom = player.condom_active == "premium"
            cheap_condom = player.condom_active == "cheap"
            break_occurred = False
            
            # Set base chances for an ass cumshot
            cheap_base_chance = 20
            premium_base_chance = 1
            cheap_mult = 3
            premium_mult = 0.5

            if cheap_condom:
                additional_break_chance = min(10, player.condom_cum * cheap_mult)
                total_break_chance = cheap_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Cheap condom broke during ass cumshot with {target_girl.first_name}! (Chance: {total_break_chance}%)")
                    
            elif premium_condom:
                additional_break_chance = min(2, player.condom_cum * premium_mult)
                total_break_chance = premium_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    renpy.log(f"VT MOD: Premium condom broke during ass cumshot with {target_girl.first_name}! (Chance: {total_break_chance}%)")
            
            # Handle breakage consequences IMMEDIATELY after it occurs
            if break_occurred:
                # Player's immediate notification
                vt_firsttime_notify("An intense jolt of pleasure as the latex tears! Your raw cock is now grinding directly against her!", duration=3.0)
                
                # Determine if girl is aware of breakage
                awareness_chance = 55  # Lower than vaginal for ass cumshot
                
                # Modify chance based on girl's traits
                if hasattr(target_girl, "notice_sensitivity"):
                    awareness_chance += target_girl.notice_sensitivity
                
                if renpy.random.randint(1, 100) <= awareness_chance:
                    # Girl becomes aware of broken condom
                    target_girl.aware_ass_cumshot_condom = True
                    vt_fetish_notify(f"{target_girl.first_name} gasps, a new, overwhelming heat spreading through her as she feels your bare, throbbing cock press against her tight anus.", duration=5.0)
                else:
                    # Girl remains unaware
                    target_girl.aware_ass_cumshot_condom = False
                    vt_fetish_notify(f"{target_girl.first_name} just whimpers and pushes back harder, the sudden, raw friction making her shudder with pleasure as her wet pussy drips.", duration=3.0)
            else:
                target_girl.aware_ass_cumshot_condom = False
        # --- END: CONDOM BREAKAGE LOGIC ---
        # Track creampie event for breakage calculation
        
        player.condom_dirty = True
        if not condom_used:
            target_girl.aware_ass_cumshot_condom = False
            dialogtext = f"You groan, your raw, throbbing cock sliding between {target_girl.first_name}'s warm ass cheeks. With a final grind against her tight anus, you erupt, painting her perfect ass with thick streams of your hot cum."
        elif player.condom_broke: # The condom broke earlier, this is a bareback cumshot
            target_girl.aware_ass_cumshot_condom = True
            player.condom_cum = 0
            dialogtext = f"The condom tears! You gasp as your bare cock feels the intense heat of her skin, and with a guttural moan, you unleash your load directly onto {target_girl.first_name}'s bare ass, your cum dripping down to her puckered anus."
        else: # Condom held
            target_girl.aware_ass_cumshot_condom = False
            player.condom_cum += 1
            dialogtext = f"You thrust between {target_girl.first_name}'s soft cheeks, her wet pussy dripping onto your balls as you grind. The thin latex separates you as you cum, your hot load filling the condom pressed against her tight anus."
        # --- END: CUMSHOT NOTIFICATION LOGIC ---
        # Handle fetish progression using centralized function
        vt_handle_cum_fetishes(action_name, target_girl, fetish_category="ass_cumshot")
        vt_handle_baby_desire(action_name, target_girl, "ass_cumshot")
        
        renpy.log(f"VT MOD: Ass cumshot processing complete for {target_girl.first_name}")
        # --- FINAL STEP: Call the dialogue label ---
        renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        # if call_label and dialogtext:
            # renpy.call(call_label, dialogtext=dialogtext)

       # renpy.restart_interaction()

    database_apply_action_impacts_hooks.append(vt_catch_cumshot_ass)

    def vt_catch_anal_creampie(action_name: str, action_failed: bool, target_girl: Union[Girl, None], girls_who_got_impacts: list[Girl]) -> None:
        """Handles anal creampie actions (creampie_ass)"""
        if action_failed or not target_girl:
            return
            
        if action_name not in ["creampie_ass","sleep_creampie_ass"]:
            return
            
        # Initialize fetish attributes if missing
        if not hasattr(target_girl, "anal_sex_count"):
            target_girl.anal_sex_count = 0
        if not hasattr(target_girl, "last_anal_sex"):
            target_girl.last_anal_sex = -1
        if not hasattr(target_girl, "first_time_anal"):
            target_girl.first_time_anal = True

        # Track when this happened - SAFELY
        vt_current_day = 0
        try:
            vt_current_day = time_manager.total_days
        except NameError:
            # This should not happen if game_init.rpy is loaded correctly
            renpy.log("vt_catch_anal_creampie failed ERROR: Global 'time_manager' variable not found!")
            return
        # Track creampie event
        target_girl.last_anal_sex = vt_current_day
        target_girl.had_sex_today = True

        # Check for active condom
        condom_used = player.condom_active != "raw"
        
        # --- LOGIC: Prepare dialogue and determine which label to call ---
        dialogtext = ""
        call_label = None
        
        # --- START: CONDOM BREAKAGE LOGIC (HAPPENS FIRST) ---
        # This block runs first to set the state of the condom before the creampie is described.
        if condom_used and not player.condom_broke:
            premium_condom = player.condom_active == "premium"
            cheap_condom = player.condom_active == "cheap"
            break_occurred = False
            
            # Set base chances for an anal creampie (high pressure)
            cheap_base_chance = 25
            premium_base_chance = 1
            cheap_mult = 3
            premium_mult = 0.5

            if cheap_condom:
                additional_break_chance = min(10, player.condom_cum * cheap_mult)
                total_break_chance = cheap_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
                    
            elif premium_condom:
                additional_break_chance = min(2, player.condom_cum * premium_mult)
                total_break_chance = premium_base_chance + additional_break_chance
                if renpy.random.randint(1, 100) <= total_break_chance:
                    player.condom_broke = True
                    break_occurred = True
            
            # Handle breakage consequences IMMEDIATELY after it occurs
            if break_occurred:
                # Player's immediate notification
                vt_firsttime_notify("The condom shears! A jolt of pure pleasure as your raw, throbbing crown finally feels her tight, hot anus gripping you directly.", duration=3.0)
                # Determine if girl is aware of breakage
                awareness_chance = 50  # Lower than vaginal for anal
                # Modify chance based on girl's traits
                if hasattr(target_girl, "notice_sensitivity"):
                    awareness_chance += target_girl.notice_sensitivity
                
                if renpy.random.randint(1, 100) <= awareness_chance:
                    # Girl becomes aware of broken condom
                    target_girl.aware_anal_condom = True
                    vt_preg_notify(f"{target_girl.first_name} gasps, her ass clenching in shock. 'The condom... it's gone!' she moans, her dripping pussy betraying her thrill as your raw cock stretches her wide.", duration=5.0)
                else:
                    # Girl remains unaware
                    target_girl.aware_anal_condom = False
                    vt_fetish_notify(f"{target_girl.first_name} whimpers into the pillow, her ass pushing back, instinctively craving the new, intense heat of your bare cock pistoning inside her.", duration=3.0)
            else:
                target_girl.aware_anal_condom = False
        # --- END: CONDOM BREAKAGE LOGIC ---
        # Track creampie event
        player.condom_dirty = True
        if not condom_used:
            target_girl.aware_anal_condom = False
            target_girl.anal_cum += 1
            dialogtext = f"You groan, your raw cock throbbing wildly inside {target_girl.first_name}'s clenching ass. Her tight anus kisses your cockhead with every pulse as you erupt, flooding her with your hot cum. Her wet pussy drips onto the sheets, the raw, intense pleasure of claiming her most forbidden hole almost overwhelming you both."
            #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        elif player.condom_broke: # The condom broke earlier, this is a bareback creampie
            target_girl.aware_anal_condom = True
            player.condom_cum = 0
            target_girl.anal_cum += 1
            dialogtext = f"A primal roar escapes you as your bare cock, finally free, erupts deep inside {target_girl.first_name}'s ass. You're marking her from the inside, claiming her tightest hole with a flood of your raw, potent cum. Her warm cheeks are pressed against you, her own orgasm triggered by the overwhelming heat and fullness of your load flooding her."
            #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        else: # Condom held
            target_girl.aware_anal_condom = False
            player.condom_cum += 1
            dialogtext = f"Your entire body tenses as you erupt, your hot throbbing cock straining against the latex as you fill the condom deep in {target_girl.first_name}'s ass. She cries out in pleasure, her own muscles clenching as she feels the intense heat of your captured seed throbbing within her, her anus gripping the base of your cock through the thin barrier."
            #renpy.call("vt_fetish_dialog", dialogtext=dialogtext)
        # --- END: CUMSHOT NOTIFICATION LOGIC ---

        # Handle fetish progression using centralized function
        vt_handle_cum_fetishes(action_name, target_girl, fetish_category="anal")
        
        # Handle baby desire increase - FIXED: USING CENTRALIZED FUNCTION
        vt_handle_baby_desire(action_name, target_girl, "anal")

        renpy.log(f"VT MOD: Anal creampie processing complete for {target_girl.first_name}")

        # --- FINAL STEP: Call the dialogue label ---
        renpy.call("vt_fetish_dialog", dialogtext=dialogtext)

        #renpy.restart_interaction()

    database_apply_action_impacts_hooks.append(vt_catch_anal_creampie)

    print("VT MOD: Using proper action callback system instead of label callbacks")


 
init 999 python:

    def vt_add_missing_attributes(delay=None):
        """delay parameter is required for Ren'Py 8.3.4 compatibility"""
        try:
            # Check retry count to prevent infinite recursion
            if renpy.store._vt_retry_count >= renpy.store._vt_max_retries:
                renpy.log("VT MOD: Maximum retry attempts reached - giving up")
                return
                
            renpy.store._vt_retry_count += 1
            renpy.log(f"VT MOD: Attempt #{renpy.store._vt_retry_count} to initialize VT attributes")
            
            # Check if academy is available
            if not hasattr(renpy.store, 'academy') or not hasattr(renpy.store.academy, 'girl_manager'):
                renpy.log("VT MOD: academy not ready yet - scheduling retry")
                # Schedule retry with increasing delay
                delay_time = min(0.5 * renpy.store._vt_retry_count, 5.0)
                renpy.invoke_in_new_context(vt_add_missing_attributes, delay_time)
                return
                
            # Reset retry counter on success
            renpy.store._vt_retry_count = 0
            
            # Include mothers too: they get their own daily/weekly updates (via mother_manager)
            # and need the same sidecar + pregnancy-model migration on load, so they must be in
            # the backfill. (girl_manager.get_all_possible_girls is girls-only.)
            if hasattr(renpy.store.academy, "get_all_possible_girls_and_mothers"):
                all_girls = renpy.store.academy.get_all_possible_girls_and_mothers(include_pending=True)
            else:
                all_girls = renpy.store.academy.girl_manager.get_all_possible_girls(include_pending=True)
            renpy.log(f"VT MOD: Processing {len(all_girls)} girls/mothers for VT compatibility")
            
            for girl in all_girls:
                is_mother = is_mother_character(girl)

                # Full idempotent backfill -- covers every VT attribute, not just a
                # subset. Critical for mid-save installs: these girls predate the mod,
                # so the patched __init__ never ran for them. Shared with Girl.__init__.
                vt_ensure_girl_attrs(girl)

                # Mother kids reconciliation (runs each load, not a one-time default).
                if is_mother:
                    # Base mothers must have at least 1 kid (their daughter)
                    girl.kids = max(1, girl.kids)
                    girl.original_daughter = True
                    # Ensure kids_with_player and kids_with_npc are consistent with total kids
                    girl.kids_with_player = max(0, girl.kids_with_player)
                    girl.kids_with_npc = max(0, girl.kids_with_npc)
                    # Total kids should be at least original daughter + player/npc kids
                    girl.kids = max(1, girl.kids_with_player + girl.kids_with_npc + (1 if girl.original_daughter else 0))
                else:
                    # Students start with 0 kids
                    girl.kids = max(0, girl.kids_with_player + girl.kids_with_npc)

                renpy.log("VT MOD: Successfully added VT attributes to all girls")
        except Exception as e:
            renpy.log(f"VT MOD ERROR: {str(e)}")
            # Only retry if we haven't hit max attempts
            if renpy.store._vt_retry_count < renpy.store._vt_max_retries:
                renpy.invoke_in_new_context(vt_add_missing_attributes, 1.0)

    # Register with compatibility system if available
    def register_compatibility(delay=None):
        """delay parameter is required for Ren'Py 8.3.4 compatibility"""
        try:
            # Reset retry counter at start
            renpy.store._vt_retry_count = 0
            
            if hasattr(renpy.store, 'academy') and hasattr(renpy.store.academy, 'compatibility_updates'):
                if isinstance(renpy.store.academy.compatibility_updates, list):
                    renpy.store.academy.compatibility_updates.append(vt_add_missing_attributes)
                    renpy.log("VT MOD: Registered with academy compatibility system")
                    return
            
            # Run immediately if no compatibility system
            vt_add_missing_attributes()
        except Exception as e:
            renpy.log(f"VT MOD: Compatibility check failed - {str(e)}")
            if renpy.store._vt_retry_count < renpy.store._vt_max_retries:
                renpy.invoke_in_new_context(vt_add_missing_attributes, 2.0)

    # Start the process
    renpy.store._vt_retry_count = 0
    renpy.invoke_in_new_context(register_compatibility, 0.1)
    print("VT MOD: Scheduled compatibility update (recursion-safe)")

    # CRITICAL for mid-save installs: the init-time run above sees the *fresh* academy
    # (before any save is loaded). Re-run the backfill on every load so the *loaded*
    # save's girls get the attributes too. (Base game has no compatibility_updates hook.)
    def vt_after_load_backfill():
        renpy.store._vt_retry_count = 0
        vt_add_missing_attributes()

    if vt_after_load_backfill not in config.after_load_callbacks:
        config.after_load_callbacks.append(vt_after_load_backfill)
