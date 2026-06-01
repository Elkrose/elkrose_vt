# VT MOD - CUM FETISH TRAITS
# This file must load AFTER database_traits is created (init -4) but BEFORE game systems use it

init -3 python:
    """This init level (-3) runs after:
       - Core game's init -4 (database_traits creation)
       - VT mod's init -34 (Mother patching)
       - VT mod's init -14 (Girl patching)
       
       But BEFORE StoreManager initializes (which happens around init 0)
    """
    
    # Check if database_traits exists before modifying it
    if "database_traits" in globals():
        renpy.log("VT MOD: Found database_traits - adding cum fetish traits")
        
        # Import Trait class if not already available
        try:
            from class_trait_ren import Trait
        except ImportError:
            try:
                from game.class_trait_ren import Trait
            except ImportError:
                if hasattr(renpy.store, 'Trait'):
                    Trait = renpy.store.Trait
                else:
                    renpy.log("VT MOD ERROR: Could not find Trait class!")
                    # Don't return - let error happen visibly
        
        #ADD the FETISHES
        # Check if trait exists before adding it
        if "cum_slut" not in database_traits:
            database_traits["cum_slut"] = Trait(
                name="cum_slut",
                display_name="Cum Slut",
                rarity=0.7,  # More common than devotee traits
                color="#FF69B4",  # Pink
                stat_growth_multipliers={"corruption": 0.05, "arousal": 0.025},
                base_stat_modifiers={
                    "mouth_sensitivity": 0.05,
                    "boobs_sensitivity": 0.05,
                    "legs_sensitivity": 0.05,
                    "ass_sensitivity": 0.05,
                    "pussy_sensitivity": 0.05,
                    "shoot_acceptance": 0.05,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "facial", "creampie_mouth", "cumshot_boobs", "cumshot_pussy", 
                    "cumshot_ass", "cumshot_thighs", "cum_in_panties"
                ],
                action_multipliers={
                    "facial": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "creampie_mouth": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cumshot_boobs": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cumshot_pussy": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cumshot_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cumshot_thighs": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cum_in_panties": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She loves being covered in cum and actively seeks opportunities for it.",
                sponsor_description="Enjoys all types of cum exposure scenes, reliable performer for creampie-focused shoots.",
                earn_requirements="girl.get_tracked_action_count(('facial', 'cumshot_boobs', 'cumshot_pussy', 'cumshot_ass', 'cumshot_thighs', 'cum_in_panties')) > 3",
                earn_requirements_description="Earned: Came on girl 3+ times",
                remove_requirements="girl.get_tracked_action_count(('facial', 'cumshot_boobs', 'cumshot_pussy', 'cumshot_ass', 'cumshot_thighs', 'cum_in_panties')) < 2 and girl.oral_cum_fetish < 20 and girl.vaginal_cum_fetish < 20 and girl.anal_cum_fetish < 20",
                remove_requirements_description="Lose: Fewer than 2 cum exposures recently",
                report_strings=[
                    "I actually kinda like it when you cum on me...",
                    "Don't get me wrong, what you did was wrong... but I didn't hate it.",
                    "I shouldn't admit this, but I've been thinking about it all day."
                ]
            )
        else:
            renpy.log("VT MOD: Trait cum_slut already exists, skipping")
        
        if "cum_slut_devotee" not in database_traits:
            database_traits["cum_slut_devotee"] = Trait(
                name="cum_slut_devotee",
                display_name="Cum Devotee",
                rarity=0.3,
                color="#FF69B4",  # Vibrant pink
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "mouth_sensitivity": 0.05,
                    "boobs_sensitivity": 0.05,
                    "legs_sensitivity": 0.05,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "facial", "creampie_mouth", "cumshot_boobs", "cumshot_pussy", 
                    "cumshot_ass", "cumshot_thighs", "cum_in_panties"
                ],
                action_multipliers={
                    "facial": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "creampie_mouth": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cumshot_boobs": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cumshot_pussy": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cumshot_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cumshot_thighs": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "cum_in_panties": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's completely devoted to having cum on various body parts and actively seeks opportunities for it.",
                sponsor_description="Enjoys all types of cum exposure scenes, highly versatile for any creampie-focused shoot.",
                earn_requirements="girl.oral_cum_fetish >= 90 or girl.vaginal_cum_fetish >= 90 or girl.anal_cum_fetish >= 90 or girl.boob_cum_fetish >= 90 or girl.thigh_cum_fetish >= 90 or girl.ass_cum_fetish >= 90 or girl.pussy_cum_fetish >= 90",
                earn_requirements_description="Earned: Any cum fetish at 90+",
                remove_requirements="girl.oral_cum_fetish < 70 and girl.vaginal_cum_fetish < 70 and girl.anal_cum_fetish < 70 and girl.boob_cum_fetish < 70 and girl.thigh_cum_fetish < 70 and girl.ass_cum_fetish < 70 and girl.pussy_cum_fetish < 70",
                remove_requirements_description="Lose: All cum fetishes below 70",
                report_strings=[
                    "I actually look forward to getting covered in cum... it's my favorite part!",
                    "Don't stop! I want every drop in my mouth/on my body!",
                    "You know I love it when you fill me up with your cum..."
                ]
            )
        if "cum_dumpster" not in database_traits:
            database_traits["cum_dumpster"] = Trait(
                name="cum_dumpster",
                display_name="Cum Dumpster",
                rarity=0.6,  # More common than devotee traits
                color="#FF1493",  # Deep pink
                stat_growth_multipliers={"corruption": 0.05, "arousal": 0.025},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.05,
                    "ass_sensitivity": 0.05,
                    "shoot_acceptance": 0.05,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "creampie_pussy", "creampie_ass", "creampie_mouth"
                ],
                action_multipliers={
                    "creampie_pussy": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "creampie_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "creampie_mouth": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She loves being filled with cum and actively seeks creampie opportunities.",
                sponsor_description="Specializes in creampie scenes, reliable performer for creampie-focused shoots.",
                earn_requirements="girl.get_tracked_action_count(('creampie_pussy', 'creampie_ass', 'creampie_mouth')) > 3",
                earn_requirements_description="Earned: Came in girl 3+ times",
                remove_requirements="girl.get_tracked_action_count(('creampie_pussy', 'creampie_ass', 'creampie_mouth')) < 2 and girl.vaginal_cum_fetish < 20 and girl.anal_cum_fetish < 20",
                remove_requirements_description="Lose: Fewer than 2 creampie exposures recently",
                report_strings=[
                    "Please fill me up completely! I want to feel every drop inside me!",
                    "Don't pull out! I need you to cum deep inside me...",
                    "I love how full I feel after you fill me up with your cum."
                ]
            )
        if "cum_dumpster_devotee" not in database_traits:
            database_traits["cum_dumpster_devotee"] = Trait(
                name="cum_dumpster_devotee",
                display_name="Cum Dumpster Devotee",
                rarity=0.3,
                color="#FF1493",  # Deep pink
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.05,
                    "ass_sensitivity": 0.05,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "creampie_pussy", "creampie_ass", "creampie_mouth"
                ],
                action_multipliers={
                    "creampie_pussy": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "creampie_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "creampie_mouth": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's completely devoted to having cum inside her and actively seeks creampie opportunities.",
                sponsor_description="Specializes in creampie scenes, particularly enjoys vaginal and anal creampies.",
                earn_requirements="girl.vaginal_cum_fetish >= 90 or girl.anal_cum_fetish >= 90",
                earn_requirements_description="Earned: Vaginal/anal creampie fetish at 90+",
                remove_requirements="girl.vaginal_cum_fetish < 70 and girl.anal_cum_fetish < 70",
                remove_requirements_description="Lose: Both creampie fetishes below 70",
                report_strings=[
                    "Please fill me up completely! I want to feel every drop inside me!",
                    "Don't pull out! I need you to cum deep inside me...",
                    "I love how full I feel after you fill me up with your cum."
                ]
            )

        #ORAL (internal)
        # database_traits["oral_addict"] = Trait(
            # name="oral_addict",
            # display_name="Oral Addict",
            # rarity=0.25,
            # color="#FF00FF",  # Magenta
            # stat_growth_multipliers={"corruption": 0.1, "arousal": 0.075},
            # base_stat_modifiers={
                # "mouth_sensitivity": 0.15,
                # "shoot_acceptance": 0.15,
                # "financial_need": -0.1
            # },
            # treated_as_tolerated_actions=[
                # "facial", "creampie_mouth", "sleep_facials", "sleep_creampie_mouth"
            # ],
            # action_multipliers={
                # "facial": {
                    # "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                    # "other_girls": {"arousal": 0.15, "corruption": 0.2},
                    # "player": {"arousal": 0.2},
                # },
                # "creampie_mouth": {
                    # "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                    # "other_girls": {"arousal": 0.15, "corruption": 0.2},
                    # "player": {"arousal": 0.2},
                # },
                # "sleep_facials": {
                    # "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                    # "other_girls": {"arousal": 0.05, "corruption": 0.1},
                    # "player": {"arousal": 0.1},
                # },
                # "sleep_creampie_mouth": {
                    # "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                    # "other_girls": {"arousal": 0.05, "corruption": 0.1},
                    # "player": {"arousal": 0.1},
                # }
            # },
            # description="She's completely addicted to having cum in her mouth and will actively beg for it.",
            # sponsor_description="Specializes in facial and creampie mouth scenes, will enthusiastically perform even complex requests.",
            # earn_requirements="girl.oral_cum_fetish >= 90",
            # earn_requirements_description="Earned: Oral cum fetish at 90+",
            # remove_requirements="girl.oral_cum_fetish < 75",
            # remove_requirements_description="Lose: Oral cum fetish below 75",
            # report_strings=[
                # "I can't get enough of your cum in my mouth... please give me more!",
                # "I've been dreaming about tasting your cum again...",
                # "I love how you fill my mouth with your hot cum!"
            # ]
        # )
        
        
        
        # This trait already exists in trait_database_ren, but we're overwriting it with enhanced version
        
        
        
        
        #ORAL - both due to facial/blowjob
        # ORAL - TIER 2
        if "oral_cum_fixation" not in database_traits:
            database_traits["oral_cum_fixation"] = Trait(
                name="oral_cum_fixation",
                display_name="Oral Cum Fixation",
                rarity=0.5,
                color="#DB7093",  # Pale violet red
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "mouth_sensitivity": 0.15,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.075
                },
                treated_as_tolerated_actions=[
                    "facial", "creampie_mouth", "sleep_facials", "sleep_creampie_mouth"
                ],
                action_multipliers={
                    "facial": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "creampie_mouth": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_facials": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "sleep_creampie_mouth": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's developed a mild interest on having cum in her mouth.",
                sponsor_description="Specializes in facial and creampie mouth scenes, highly enthusiastic performer.",
                earn_requirements="girl.oral_cum_fetish >= 50",
                earn_requirements_description="Earned: Oral cum fetish at 50+",
                remove_requirements="girl.oral_cum_fetish < 40",
                remove_requirements_description="Lose: Oral cum fetish below 40",
                report_strings=[
                    "I can't concentrate when I'm thinking about your cum in my mouth...",
                    "It's not just about the money anymore... I genuinely enjoy it.",
                    "I've been practicing how to take more cum in my mouth..."
                ]
            )
        if "conflicted_oral_cum_slut" not in database_traits:
            database_traits["conflicted_oral_cum_slut"] = Trait(
                name="conflicted_oral_cum_slut",
                display_name="Conflicted Oral Cum Slut",
                rarity=0.45,
                color="#9370DB",  # Medium purple
                stat_growth_multipliers={"corruption": 0.05, "fear": 0.05},
                base_stat_modifiers={
                    "mouth_sensitivity": 0.1,
                    "fear": 5,
                    "max_report_chance": 10
                },
                treated_as_tolerated_actions=[
                    "facial", "creampie_mouth"
                ],
                action_multipliers={
                    "facial": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": 0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    },
                    "creampie_mouth": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": 0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's conflicted but can't resist cum in her mouth, showing visible distress during exposure.",
                sponsor_description="Can be used for creampie scenes but may require extra direction due to internal conflict.",
                earn_requirements="(girl.has_trait('conservative') or girl.has_trait('reserved')) and girl.oral_cum_fetish >= 60 and girl.oral_cum_fetish < 75",
                earn_requirements_description="Earned: Conservative/reserved girl with moderate oral cum fetish",
                remove_requirements="girl.oral_cum_fetish >= 75 or not (girl.has_trait('conservative') or girl.has_trait('reserved'))",
                remove_requirements_description="Transition: Fetish level 75+ or no longer conservative/reserved",
                report_strings=[
                    "I... I shouldn't have enjoyed that, but I couldn't help myself...",
                    "I feel so ashamed for liking it, but my body just... reacted.",
                    "Please don't tell anyone about this, I'm so embarrassed!"
                ]
            )
        # ORAL - TIER 3 
        if "oral_cum_slut" not in database_traits:
            database_traits["oral_cum_slut"] = Trait(
                name="oral_cum_slut",
                display_name="Oral Cum Slut",
                rarity=0.35,
                color="#FF69B4",  # Pink
                stat_growth_multipliers={"corruption": 0.05, "arousal": 0.025},
                base_stat_modifiers={
                    "mouth_sensitivity": 0.1,
                    "shoot_acceptance": 0.05,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "facial", "creampie_mouth", "sleep_facials", "sleep_creampie_mouth"
                ],
                action_multipliers={
                    "facial": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "creampie_mouth": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "sleep_facials": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    },
                    "sleep_creampie_mouth": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She loves having cum in her mouth and actively seeks opportunities for it.",
                sponsor_description="Enjoys facial and creampie mouth scenes, reliable performer for creampie-focused shoots.",
                earn_requirements="girl.oral_cum_fetish >= 75",
                earn_requirements_description="Earned: Oral cum fetish at 75+",
                remove_requirements="girl.oral_cum_fetish < 65",
                remove_requirements_description="Lose: Oral cum fetish below 65",
                report_strings=[
                    "I can't stop thinking about your cum in my mouth...",
                    "I find myself getting wet just imagining your cum in my mouth...",
                    "I've been practicing how to take more cum in my mouth..."
                ]
            )
        # ORAL - TIER 4
        if "oral_cum_addict" not in database_traits:
            database_traits["oral_cum_addict"] = Trait(
                name="oral_cum_addict",
                display_name="Oral Cum Addict",
                rarity=0.25,
                color="#FF00FF",  # Magenta
                stat_growth_multipliers={"corruption": 0.1, "arousal": 0.075},
                base_stat_modifiers={
                    "mouth_sensitivity": 0.25,
                    "shoot_acceptance": 0.15,
                    "financial_need": -0.1
                },
                treated_as_tolerated_actions=[
                    "facial", "creampie_mouth", "sleep_facials", "sleep_creampie_mouth"
                ],
                action_multipliers={
                    "facial": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "creampie_mouth": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_facials": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    },
                    "sleep_creampie_mouth": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's completely addicted to having cum in her mouth and will actively beg for it.",
                sponsor_description="Specializes in facial and creampie mouth scenes, will enthusiastically perform even complex requests.",
                earn_requirements="girl.oral_cum_fetish >= 90",
                earn_requirements_description="Earned: Oral cum fetish at 90+",
                remove_requirements="girl.oral_cum_fetish < 80",
                remove_requirements_description="Lose: Oral cum fetish below 80",
                report_strings=[
                    "I can't get enough of your cum in my mouth... please give me more!",
                    "I've been dreaming about tasting your cum again...",
                    "I love how you fill my mouth with your hot cum!"
                ]
            )
        # ULTIMATE ORAL FETISH (FINAL TIER)
        if "oral_cum_devotee" not in database_traits:
            database_traits["oral_cum_devotee"] = Trait(
                name="oral_cum_devotee",
                display_name="Oral Cum Devotee",
                rarity=0.15,
                color="#FF00FF",  # Magenta
                stat_growth_multipliers={"corruption": 0.15, "arousal": 0.1},
                base_stat_modifiers={
                    "mouth_sensitivity": 0.3,
                    "shoot_acceptance": 0.2,
                    "financial_need": -0.15
                },
                treated_as_tolerated_actions=["facial", "creampie_mouth", "sleep_facials", "sleep_creampie_mouth"],
                action_multipliers={
                    "facial": {
                        "target_girl": {"arousal": 0.3, "corruption": 0.3, "pressure": -0.3},
                        "other_girls": {"arousal": 0.25, "corruption": 0.3},
                        "player": {"arousal": 0.3},
                    },
                    "creampie_mouth": {
                        "target_girl": {"arousal": 0.3, "corruption": 0.3, "pressure": -0.3},
                        "other_girls": {"arousal": 0.25, "corruption": 0.3},
                        "player": {"arousal": 0.3},
                    },
                    "sleep_facials": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.1},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_creampie_mouth": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.1},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    }
                },
                description="She's utterly devoted to having cum in her mouth and will actively beg for it constantly.",
                sponsor_description="Specializes in extreme facial/creampie scenes, will enthusiastically perform even the most complex requests.",
                earn_requirements="girl.oral_cum_fetish >= 100",
                earn_requirements_description="Earned: Oral cum fetish at 100+",
                remove_requirements="girl.oral_cum_fetish < 90",
                remove_requirements_description="Lose: Oral cum fetish below 90",
                report_strings=[
                    "I can't get enough of your cum in my mouth... please give me more!",
                    "I've been dreaming about tasting your cum again...",
                    "I love how you fill my mouth with your hot cum!"
                ]
            )
        
        #VAGINAL (internal)
        # VAGINAL - TIER 2 
        if "vaginal_cum_fixation" not in database_traits:
            database_traits["vaginal_cum_fixation"] = Trait(
                name="vaginal_cum_fixation",
                display_name="Vaginal Cum Fixation",
                rarity=0.5,
                color="#DB7093",  # Pale violet red
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.15,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.075
                },
                treated_as_tolerated_actions=["creampie_pussy", "sleep_creampie_pussy"],
                action_multipliers={
                    "creampie_pussy": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_creampie_pussy": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's developed a mild interest on having cum inside her pussy.",
                sponsor_description="Specializes in vaginal creampie scenes, highly enthusiastic performer.",
                earn_requirements="girl.vaginal_cum_fetish >= 50",
                earn_requirements_description="Earned: Vaginal cum fetish at 50+",
                remove_requirements="girl.vaginal_cum_fetish < 40",
                remove_requirements_description="Lose: Vaginal cum fetish below 40",
                report_strings=[
                    "I can't concentrate when I'm thinking about your cum inside me...",
                    "It's not just about the money anymore... I genuinely enjoy it.",
                    "I've been practicing how to hold more cum inside me..."
                ]
            )
        if "conflicted_vaginal_cum_dumpster" not in database_traits:
            database_traits["conflicted_vaginal_cum_dumpster"] = Trait(
                name="conflicted_vaginal_cum_dumpster",
                display_name="Conflicted Vaginal Cum Dumpster",
                rarity=0.45,
                color="#9370DB",
                stat_growth_multipliers={"corruption": 0.05, "fear": 0.05},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.1,
                    "fear": 5,
                    "max_report_chance": 10
                },
                treated_as_tolerated_actions=[
                    "creampie_pussy"
                ],
                action_multipliers={
                    "creampie_pussy": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": 0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's conflicted but can't resist cum inside her pussy, showing visible distress during creampie.",
                sponsor_description="Can be used for creampie scenes but may require extra direction due to internal conflict.",
                earn_requirements="(girl.has_trait('conservative') or girl.has_trait('reserved')) and girl.vaginal_cum_fetish >= 60 and girl.vaginal_cum_fetish < 75",
                earn_requirements_description="Earned: Conservative/reserved girl with moderate vaginal creampie fetish",
                remove_requirements="girl.vaginal_cum_fetish >= 75 or not (girl.has_trait('conservative') or girl.has_trait('reserved'))",
                remove_requirements_description="Transition: Fetish level 75+ or no longer conservative/reserved",
                report_strings=[
                    "I shouldn't have enjoyed that creampie, but... it felt so good...",
                    "I feel so dirty for liking it when you fill me up...",
                    "Please don't tell anyone about this, I'm so ashamed!"
                ]
            )
        # VAGINAL - TIER 3
        if "vaginal_cum_dumpster" not in database_traits:
            database_traits["vaginal_cum_dumpster"] = Trait(
                name="vaginal_cum_dumpster",
                display_name="Vaginal Cum Dumpster",
                rarity=0.35,
                color="#FF1493",  # Deep pink
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.15,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.075
                },
                treated_as_tolerated_actions=["creampie_pussy", "sleep_creampie_pussy"],
                action_multipliers={
                    "creampie_pussy": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_creampie_pussy": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's developed a strong fixation on having cum inside her pussy and actively seeks creampie opportunities.",
                sponsor_description="Specializes in vaginal creampie scenes, highly enthusiastic performer.",
                earn_requirements="girl.vaginal_cum_fetish >= 75",
                earn_requirements_description="Earned: Vaginal cum fetish at 75+",
                remove_requirements="girl.vaginal_cum_fetish < 65",
                remove_requirements_description="Lose: Vaginal cum fetish below 65",
                report_strings=[
                    "I can't concentrate when I'm thinking about your cum inside me...",
                    "It's not just about the money anymore... I genuinely enjoy it.",
                    "I've been practicing how to hold more cum inside me..."
                ]
            )
        # VAGINAL - TIER 4 
        if "vaginal_cum_addict" not in database_traits:
            database_traits["vaginal_cum_addict"] = Trait(
                name="vaginal_cum_addict",
                display_name="Vaginal Cum Addict",
                rarity=0.25,
                color="#FF00FF",
                stat_growth_multipliers={"corruption": 0.1, "arousal": 0.075},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.15,
                    "shoot_acceptance": 0.15,
                    "financial_need": -0.1
                },
                treated_as_tolerated_actions=[
                    "creampie_pussy", "sleep_creampie_pussy"
                ],
                action_multipliers={
                    "creampie_pussy": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_creampie_pussy": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's completely addicted to having cum inside her pussy and will actively beg for creampie.",
                sponsor_description="Specializes in vaginal creampie scenes, will enthusiastically perform even complex requests.",
                earn_requirements="girl.vaginal_cum_fetish >= 90",
                earn_requirements_description="Earned: Vaginal cum fetish at 90+",
                remove_requirements="girl.vaginal_cum_fetish < 80",
                remove_requirements_description="Lose: Vaginal cum fetish below 80",
                report_strings=[
                    "Please fill me up completely! I want to feel every drop inside me!",
                    "Don't pull out! I need you to cum deep inside me...",
                    "I love how full I feel after you fill me up with your cum."
                ]
            )
        # ULTIMATE VAGINAL FETISH (FINAL TIER)
        if "vaginal_cum_devotee" not in database_traits:
            database_traits["vaginal_cum_devotee"] = Trait(
                name="vaginal_cum_devotee",
                display_name="Vaginal Cum Devotee",
                rarity=0.15,
                color="#FF00FF",  # Magenta
                stat_growth_multipliers={"corruption": 0.15, "arousal": 0.1},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.3,
                    "shoot_acceptance": 0.2,
                    "financial_need": -0.15
                },
                treated_as_tolerated_actions=["creampie_pussy", "sleep_creampie_pussy"],
                action_multipliers={
                    "creampie_pussy": {
                        "target_girl": {"arousal": 0.3, "corruption": 0.3, "pressure": -0.3},
                        "other_girls": {"arousal": 0.25, "corruption": 0.3},
                        "player": {"arousal": 0.3},
                    },
                    "sleep_creampie_pussy": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.1},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    }
                },
                description="She's utterly devoted to having cum inside her pussy and will actively beg for creampie constantly.",
                sponsor_description="Specializes in extreme creampie scenes, will enthusiastically perform even the most complex requests.",
                earn_requirements="girl.vaginal_cum_fetish >= 100",
                earn_requirements_description="Earned: Vaginal cum fetish at 100+",
                remove_requirements="girl.vaginal_cum_fetish < 90",
                remove_requirements_description="Lose: Vaginal cum fetish below 90",
                report_strings=[
                    "Please fill me up completely! I want to feel every drop inside me!",
                    "Don't pull out! I need you to cum deep inside me...",
                    "I love how full I feel after you fill me up with your cum."
                ]
            )
       
        #ANAL (internal)
        if "anal_slut" not in database_traits:
            database_traits["anal_slut"] = Trait(
                name="anal_slut",
                display_name="Anal Slut",
                rarity=0.5,  # More common than devotee traits
                color="#FF69B4",  # Pink
                stat_growth_multipliers={"corruption": 0.05, "arousal": 0.025},
                base_stat_modifiers={
                    "ass_sensitivity": 0.05,
                    "shoot_acceptance": 0.05,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "tease_ass", "finger_ass", "lick_ass", "fuck_ass", "creampie_ass"
                ],
                action_multipliers={
                    "tease_ass": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "finger_ass": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "lick_ass": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "fuck_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "creampie_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She loves anal play and actively seeks opportunities for it.",
                sponsor_description="Specializes in anal scenes, reliable performer for anal-focused shoots.",
                earn_requirements="girl.get_tracked_action_count(('fuck_ass', 'creampie_ass')) > 3",
                earn_requirements_description="Earned: 3+ anal sex events",
                remove_requirements="girl.get_tracked_action_count(('fuck_ass', 'creampie_ass')) < 2 and girl.anal_cum_fetish < 20",
                remove_requirements_description="Lose: Fewer than 2 anal events recently",
                report_strings=[
                    "I actually kinda like anal...",
                    "Don't get me wrong, what you did was wrong... but I didn't hate it.",
                    "I shouldn't admit this, but I've been thinking about it all day."
                ]
            )
        # ANAL - TIER 2 
        if "anal_cum_fixation" not in database_traits:
            database_traits["anal_cum_fixation"] = Trait(
                name="anal_cum_fixation",
                display_name="Anal Cum Fixation",
                rarity=0.5,
                color="#DB7093",  # Pale violet red
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "ass_sensitivity": 0.15,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.075
                },
                treated_as_tolerated_actions=["creampie_ass", "sleep_creampie_ass"],
                action_multipliers={
                    "creampie_ass": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_creampie_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's developed a mild interest on having cum in her ass.",
                sponsor_description="Specializes in anal creampie scenes, highly enthusiastic performer.",
                earn_requirements="girl.anal_cum_fetish >= 50",
                earn_requirements_description="Earned: Anal cum fetish at 50+",
                remove_requirements="girl.anal_cum_fetish < 40",
                remove_requirements_description="Lose: Anal cum fetish below 40",
                report_strings=[
                    "I can't concentrate when I'm thinking about your cum in my ass...",
                    "It's not just about the money anymore... I genuinely enjoy it.",
                    "I've been practicing how to hold more cum in my ass..."
                ]
            )
        if "conflicted_anal_cum_dumpster" not in database_traits:
            database_traits["conflicted_anal_cum_dumpster"] = Trait(
                name="conflicted_anal_cum_dumpster",
                display_name="Conflicted Anal Cum Dumpster",
                rarity=0.45,
                color="#9370DB",
                stat_growth_multipliers={"corruption": 0.05, "fear": 0.05},
                base_stat_modifiers={
                    "ass_sensitivity": 0.1,
                    "fear": 5,
                    "max_report_chance": 10
                },
                treated_as_tolerated_actions=[
                    "creampie_ass"
                ],
                action_multipliers={
                    "creampie_ass": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": 0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's conflicted but can't resist cum in her ass, showing visible distress during anal creampie.",
                sponsor_description="Can be used for anal creampie scenes but may require extra direction due to internal conflict.",
                earn_requirements="(girl.has_trait('conservative') or girl.has_trait('reserved')) and girl.anal_cum_fetish >= 60 and girl.anal_cum_fetish < 75",
                earn_requirements_description="Earned: Conservative/reserved girl with moderate anal creampie fetish",
                remove_requirements="girl.anal_cum_fetish >= 75 or not (girl.has_trait('conservative') or girl.has_trait('reserved'))",
                remove_requirements_description="Transition: Fetish level 75+ or no longer conservative/reserved",
                report_strings=[
                    "I shouldn't have enjoyed that anal creampie, but... it felt so good...",
                    "I feel so dirty for liking it when you fill my ass...",
                    "Please don't tell anyone about this, I'm so ashamed!"
                ]
            )
        # ANAL - TIER 3
        if "anal_cum_dumpster" not in database_traits:
            database_traits["anal_cum_dumpster"] = Trait(
                name="anal_cum_dumpster",
                display_name="Anal Cum Dumpster",
                rarity=0.35,
                color="#FF1493",  # Deep pink
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "ass_sensitivity": 0.15,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.075
                },
                treated_as_tolerated_actions=["creampie_ass", "sleep_creampie_ass"],
                action_multipliers={
                    "creampie_ass": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_creampie_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's developed a strong fixation on having cum in her ass and actively seeks anal creampie opportunities.",
                sponsor_description="Specializes in anal creampie scenes, highly enthusiastic performer.",
                earn_requirements="girl.anal_cum_fetish >= 75",
                earn_requirements_description="Earned: Anal cum fetish at 75+",
                remove_requirements="girl.anal_cum_fetish < 65",
                remove_requirements_description="Lose: Anal cum fetish below 65",
                report_strings=[
                    "I can't concentrate when I'm thinking about your cum in my ass...",
                    "It's not just about the money anymore... I genuinely enjoy it.",
                    "I've been practicing how to hold more cum in my ass..."
                ]
            )
        # ANAL - TIER 4 
        if "anal_cum_addict" not in database_traits:
            database_traits["anal_cum_addict"] = Trait(
                name="anal_cum_addict",
                display_name="Anal Cum Addict",
                rarity=0.25,
                color="#FF00FF",
                stat_growth_multipliers={"corruption": 0.1, "arousal": 0.075},
                base_stat_modifiers={
                    "ass_sensitivity": 0.15,
                    "shoot_acceptance": 0.15,
                    "financial_need": -0.1
                },
                treated_as_tolerated_actions=[
                    "creampie_ass", "sleep_creampie_ass"
                ],
                action_multipliers={
                    "creampie_ass": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_creampie_ass": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's completely addicted to having cum in her ass and will actively beg for anal creampie.",
                sponsor_description="Specializes in anal creampie scenes, will enthusiastically perform even complex requests.",
                earn_requirements="girl.anal_cum_fetish >= 90",
                earn_requirements_description="Earned: Anal cum fetish at 90+",
                remove_requirements="girl.anal_cum_fetish < 80",
                remove_requirements_description="Lose: Anal cum fetish below 80",
                report_strings=[
                    "Please fill my ass completely! I want to feel every drop inside me!",
                    "Don't pull out! I need you to cum deep inside my ass...",
                    "I love how full I feel after you fill my ass with your cum."
                ]
            )
        # ULTIMATE ANAL FETISH (FINAL TIER)
        if "anal_cum_devotee" not in database_traits:
            database_traits["anal_cum_devotee"] = Trait(
                name="anal_cum_devotee",
                display_name="Anal Cum Devotee",
                rarity=0.15,
                color="#FF00FF",  # Magenta
                stat_growth_multipliers={"corruption": 0.15, "arousal": 0.1},
                base_stat_modifiers={
                    "ass_sensitivity": 0.3,
                    "shoot_acceptance": 0.2,
                    "financial_need": -0.15
                },
                treated_as_tolerated_actions=["creampie_ass", "sleep_creampie_ass"],
                action_multipliers={
                    "creampie_ass": {
                        "target_girl": {"arousal": 0.3, "corruption": 0.3, "pressure": -0.3},
                        "other_girls": {"arousal": 0.25, "corruption": 0.3},
                        "player": {"arousal": 0.3},
                    },
                    "sleep_creampie_ass": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.1},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    }
                },
                description="She's utterly devoted to having cum in her ass and will actively beg for anal creampie constantly.",
                sponsor_description="Specializes in extreme anal creampie scenes, will enthusiastically perform even the most complex requests.",
                earn_requirements="girl.anal_cum_fetish >= 100",
                earn_requirements_description="Earned: Anal cum fetish at 100+",
                remove_requirements="girl.anal_cum_fetish < 90",
                remove_requirements_description="Lose: Anal cum fetish below 90",
                report_strings=[
                    "Please fill my ass completely! I want to feel every drop inside me!",
                    "Don't pull out! I need you to cum deep inside my ass...",
                    "I love how full I feel after you fill my ass with your cum."
                ]
            )
        
        #BOOBS (external)
        # BOOBS - TIER 2 
        if "boob_cum_fixation" not in database_traits:
            database_traits["boob_cum_fixation"] = Trait(
                name="boob_cum_fixation",
                display_name="Boob Cum Fixation",
                rarity=0.5,
                color="#FF69B4",
                stat_growth_multipliers={"corruption": 0.05, "arousal": 0.025},
                base_stat_modifiers={
                    "boobs_sensitivity": 0.1,
                    "shoot_acceptance": 0.05,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "cumshot_boobs", "sleep_cumshot_boobs"
                ],
                action_multipliers={
                    "cumshot_boobs": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "sleep_cumshot_boobs": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's developed a mild interest having cum shot on her breasts.",
                sponsor_description="Can perform basic boob cumshot scenes with minimal direction.",
                earn_requirements="girl.boob_cum_fetish >= 50",
                earn_requirements_description="Earned: Boob cum fetish at 50+",
                remove_requirements="girl.boob_cum_fetish < 40",
                remove_requirements_description="Lose: Boob cum fetish below 40",
                report_strings=[
                    "I actually like it when you cum on my breasts...",
                    "Don't get me wrong, what you did was wrong... but I didn't hate it.",
                    "I shouldn't admit this, but I've been thinking about it all day."
                ]
            )
        if "conflicted_boob_cum_slut" not in database_traits:
            database_traits["conflicted_boob_cum_slut"] = Trait(
                name="conflicted_boob_cum_slut",
                display_name="Conflicted Boob Cum Slut",
                rarity=0.4,
                color="#9370DB",
                stat_growth_multipliers={"corruption": 0.05, "fear": 0.05},
                base_stat_modifiers={
                    "boobs_sensitivity": 0.1,
                    "fear": 5,
                    "max_report_chance": 10
                },
                treated_as_tolerated_actions=[
                    "cumshot_boobs"
                ],
                action_multipliers={
                    "cumshot_boobs": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": 0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's conflicted but can't resist cum on her breasts, showing visible distress during cumshot.",
                sponsor_description="Can be used for cumshot scenes but may require extra direction due to internal conflict.",
                earn_requirements="(girl.has_trait('conservative') or girl.has_trait('reserved')) and girl.boob_cum_fetish >= 50 and girl.boob_cum_fetish < 80",
                earn_requirements_description="Earned: Conservative/reserved girl with moderate boob cum fetish",
                remove_requirements="girl.boob_cum_fetish >= 80 or not (girl.has_trait('conservative') or girl.has_trait('reserved'))",
                remove_requirements_description="Transition: Fetish level 80+ or no longer conservative/reserved",
                report_strings=[
                    "I... I shouldn't have enjoyed that, but I couldn't help myself...",
                    "I feel so ashamed for liking it, but my body just... reacted.",
                    "Please don't tell anyone about this, I'm so embarrassed!"
                ]
            )
        # BOOBS - TIER 3 
        if "boob_cum_slut" not in database_traits:
            database_traits["boob_cum_slut"] = Trait(
                name="boob_cum_slut",
                display_name="Boob Cum Slut",
                rarity=0.35,
                color="#DB7093",
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "boobs_sensitivity": 0.15,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.075
                },
                treated_as_tolerated_actions=[
                    "cumshot_boobs", "sleep_cumshot_boobs"
                ],
                action_multipliers={
                    "cumshot_boobs": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_cumshot_boobs": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's developed a strong fixation on having cum on her breasts and will actively seek cumshot opportunities.",
                sponsor_description="Specializes in boob cumshot scenes, highly enthusiastic performer.",
                earn_requirements="girl.boob_cum_fetish >= 75",
                earn_requirements_description="Earned: Boob cum fetish at 75+",
                remove_requirements="girl.boob_cum_fetish < 65",
                remove_requirements_description="Lose: Boob cum fetish below 65",
                report_strings=[
                    "I can't concentrate when I'm thinking about your cum on my breasts...",
                    "It's not just about the money anymore... I genuinely enjoy it.",
                    "I've been practicing how to keep the cum on my breasts longer..."
                ]
            )
        # BOOBS - TIER 4        
        if "boob_cum_addict" not in database_traits:
            database_traits["boob_cum_addict"] = Trait(
                name="boob_cum_addict",
                display_name="Boob Cum Addict",
                rarity=0.25,
                color="#FF00FF",
                stat_growth_multipliers={"corruption": 0.1, "arousal": 0.075},
                base_stat_modifiers={
                    "boobs_sensitivity": 0.25,
                    "shoot_acceptance": 0.15,
                    "financial_need": -0.1
                },
                treated_as_tolerated_actions=[
                    "cumshot_boobs", "sleep_cumshot_boobs"
                ],
                action_multipliers={
                    "cumshot_boobs": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_cumshot_boobs": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's completely addicted to cum on her breasts and will actively beg for cumshot.",
                sponsor_description="Specializes in boob cumshot scenes, will enthusiastically perform even complex requests.",
                earn_requirements="girl.boob_cum_fetish >= 90",
                earn_requirements_description="Earned: Boob cum fetish at 90+",
                remove_requirements="girl.boob_cum_fetish < 80",
                remove_requirements_description="Lose: Boob cum fetish below 80",
                report_strings=[
                    "I can't get enough of your cum on my breasts... please give me more!",
                    "I've been dreaming about feeling your cum on my breasts again...",
                    "I love how you cover my breasts with your hot cum!"
                ]
            )
        # ULTIMATE BOOB FETISH (FINAL TIER)
        if "boob_cum_devotee" not in database_traits:
            database_traits["boob_cum_devotee"] = Trait(
                name="boob_cum_devotee",
                display_name="Boob Cum Devotee",
                rarity=0.15,
                color="#FF00FF",  # Magenta
                stat_growth_multipliers={"corruption": 0.15, "arousal": 0.1},
                base_stat_modifiers={
                    "boobs_sensitivity": 0.3,
                    "shoot_acceptance": 0.2,
                    "financial_need": -0.15
                },
                treated_as_tolerated_actions=["cumshot_boobs", "sleep_cumshot_boobs"],
                action_multipliers={
                    "cumshot_boobs": {
                        "target_girl": {"arousal": 0.3, "corruption": 0.3, "pressure": -0.3},
                        "other_girls": {"arousal": 0.25, "corruption": 0.3},
                        "player": {"arousal": 0.3},
                    },
                    "sleep_cumshot_boobs": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.1},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    }
                },
                description="She's utterly devoted to having cum shot on her breasts and will actively beg for cumshot constantly.",
                sponsor_description="Specializes in extreme boob cumshot scenes, will enthusiastically perform even the most complex requests.",
                earn_requirements="girl.boob_cum_fetish >= 100",
                earn_requirements_description="Earned: Boob cum fetish at 100+",
                remove_requirements="girl.boob_cum_fetish < 90",
                remove_requirements_description="Lose: Boob cum fetish below 90",
                report_strings=[
                    "I can't get enough of your cum on my breasts... please give me more!",
                    "I've been dreaming about feeling your cum on my breasts again...",
                    "I love how you cover my breasts with your hot cum!"
                ]
            )
        
        #THIGHS (external)
        # THIGH PATH - TIER 2 
        if "thigh_cum_fixation" not in database_traits:
            database_traits["thigh_cum_fixation"] = Trait(
                name="thigh_cum_fixation",
                display_name="Thigh Cum Fixation",
                rarity=0.5,
                color="#FF69B4",
                stat_growth_multipliers={"corruption": 0.05, "arousal": 0.025},
                base_stat_modifiers={
                    "legs_sensitivity": 0.1,
                    "shoot_acceptance": 0.05,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "cumshot_thighs", "sleep_cumshot_thighs"
                ],
                action_multipliers={
                    "cumshot_thighs": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "sleep_cumshot_thighs": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's developed a mild interest having cum shot on her thighs.",
                sponsor_description="Can perform basic thigh cumshot scenes with minimal direction.",
                earn_requirements="girl.get_tracked_action_count(('cumshot_thighs', 'sleep_cumshot_thighs')) > 5",
                earn_requirements_description="Earned: 5+ thigh cumshots",
                remove_requirements="girl.get_tracked_action_count(('cumshot_thighs', 'sleep_cumshot_thighs')) < 2 and girl.thigh_cum_fetish < 30",
                remove_requirements_description="Lose: Fewer than 2 thigh cumshots recently",
                report_strings=[
                    "I actually like it when you cum on my thighs...",
                    "Don't get me wrong, what you did was wrong... but I didn't hate it.",
                    "I shouldn't admit this, but I've been thinking about it all day."
                ]
            )
        if "conflicted_thigh_cum_slut" not in database_traits:
            database_traits["conflicted_thigh_cum_slut"] = Trait(
                name="conflicted_thigh_cum_slut",
                display_name="Conflicted Thigh Cum Slut",
                rarity=0.45,
                color="#9370DB",
                stat_growth_multipliers={"corruption": 0.05, "fear": 0.05},
                base_stat_modifiers={
                    "legs_sensitivity": 0.1,
                    "fear": 5,
                    "max_report_chance": 10
                },
                treated_as_tolerated_actions=[
                    "cumshot_thighs"
                ],
                action_multipliers={
                    "cumshot_thighs": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": 0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's conflicted but can't resist cum on her thighs, showing visible distress during cumshot.",
                sponsor_description="Can be used for cumshot scenes but may require extra direction due to internal conflict.",
                earn_requirements="(girl.has_trait('conservative') or girl.has_trait('reserved')) and girl.thigh_cum_fetish >= 50 and girl.thigh_cum_fetish < 80",
                earn_requirements_description="Earned: Conservative/reserved girl with moderate thigh cum fetish",
                remove_requirements="girl.thigh_cum_fetish >= 80 or not (girl.has_trait('conservative') or girl.has_trait('reserved'))",
                remove_requirements_description="Transition: Fetish level 80+ or no longer conservative/reserved",
                report_strings=[
                    "I... I shouldn't have enjoyed that, but I couldn't help myself...",
                    "I feel so ashamed for liking it, but my body just... reacted.",
                    "Please don't tell anyone about this, I'm so embarrassed!"
                ]
            )
        # THIGH PATH - TIER 3 
        if "thigh_cum_slut" not in database_traits:
            database_traits["thigh_cum_slut"] = Trait(
                name="thigh_cum_slut",
                display_name="Thigh Cum Slut",
                rarity=0.35,
                color="#DB7093",  # Pale violet red
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "legs_sensitivity": 0.15,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.075
                },
                treated_as_tolerated_actions=[
                    "cumshot_thighs", "sleep_cumshot_thighs"
                ],
                action_multipliers={
                    "cumshot_thighs": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_cumshot_thighs": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's developed a strong fixation on having cum shot on her thighs.",
                sponsor_description="Specializes in thigh cumshot scenes, highly enthusiastic performer.",
                earn_requirements="girl.thigh_cum_fetish >= 75",
                earn_requirements_description="Earned: Thigh cum fetish at 75+",
                remove_requirements="girl.thigh_cum_fetish < 60",
                remove_requirements_description="Lose: Thigh cum fetish below 60",
                report_strings=[
                    "I can't concentrate when I'm thinking about your cum on my thighs...",
                    "It's not just about the money anymore... I genuinely enjoy it.",
                    "I've been practicing how to keep the cum on my thighs longer..."
                ]
            )
        # THIGH PATH - TIER 4 
        if "thigh_cum_addict" not in database_traits:
            database_traits["thigh_cum_addict"] = Trait(
                name="thigh_cum_addict",
                display_name="Thigh Cum Addict",
                rarity=0.25,
                color="#FF00FF",
                stat_growth_multipliers={"corruption": 0.1, "arousal": 0.075},
                base_stat_modifiers={
                    "legs_sensitivity": 0.25,
                    "shoot_acceptance": 0.15,
                    "financial_need": -0.1
                },
                treated_as_tolerated_actions=[
                    "cumshot_thighs", "sleep_cumshot_thighs"
                ],
                action_multipliers={
                    "cumshot_thighs": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_cumshot_thighs": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's completely addicted to cum on her thighs and will actively beg for cumshot.",
                sponsor_description="Specializes in thigh cumshot scenes, will enthusiastically perform even complex requests.",
                earn_requirements="girl.thigh_cum_fetish >= 90",
                earn_requirements_description="Earned: Thigh cum fetish at 90+",
                remove_requirements="girl.thigh_cum_fetish < 75",
                remove_requirements_description="Lose: Thigh cum fetish below 75",
                report_strings=[
                    "I can't get enough of your cum on my thighs... please give me more!",
                    "I've been dreaming about feeling your cum on my thighs again...",
                    "I love how you cover my thighs with your hot cum!"
                ]
            )
        # ULTIMATE THIGH FETISH (FINAL TIER)
        if "thigh_cum_devotee" not in database_traits:
            database_traits["thigh_cum_devotee"] = Trait(
                name="thigh_cum_devotee",
                display_name="Thigh Cum Devotee",
                rarity=0.15,
                color="#FF00FF",  # Magenta
                stat_growth_multipliers={"corruption": 0.15, "arousal": 0.1},
                base_stat_modifiers={
                    "legs_sensitivity": 0.3,
                    "shoot_acceptance": 0.2,
                    "financial_need": -0.15
                },
                treated_as_tolerated_actions=["cumshot_thighs", "sleep_cumshot_thighs"],
                action_multipliers={
                    "cumshot_thighs": {
                        "target_girl": {"arousal": 0.3, "corruption": 0.3, "pressure": -0.3},
                        "other_girls": {"arousal": 0.25, "corruption": 0.3},
                        "player": {"arousal": 0.3},
                    },
                    "sleep_cumshot_thighs": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.1},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    }
                },
                description="She's utterly devoted to having cum shot on her thighs and will actively beg for cumshot constantly.",
                sponsor_description="Specializes in extreme thigh cumshot scenes, will enthusiastically perform even the most complex requests.",
                earn_requirements="girl.thigh_cum_fetish >= 100",
                earn_requirements_description="Earned: Thigh cum fetish at 100+",
                remove_requirements="girl.thigh_cum_fetish < 90",
                remove_requirements_description="Lose: Thigh cum fetish below 90",
                report_strings=[
                    "I can't get enough of your cum on my thighs... please give me more!",
                    "I've been dreaming about feeling your cum on my thighs again...",
                    "I love how you cover my thighs with your hot cum!"
                ]
            )
        
        #ON ASS (external)
        # ASS PATH - TIER 2
        if "ass_cum_fixation" not in database_traits:
            database_traits["ass_cum_fixation"] = Trait(
                name="ass_cum_fixation",
                display_name="Ass Cum Fixation",
                rarity=0.5,
                color="#FF69B4",
                stat_growth_multipliers={"corruption": 0.05, "arousal": 0.025},
                base_stat_modifiers={
                    "ass_sensitivity": 0.1,
                    "shoot_acceptance": 0.05,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "cumshot_ass", "sleep_cumshot_ass"
                ],
                action_multipliers={
                    "cumshot_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "sleep_cumshot_ass": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's developed a mild interest having cum shot on her ass.",
                sponsor_description="Can perform basic ass cumshot scenes with minimal direction.",
                earn_requirements="girl.ass_cum_fetish >= 50",
                earn_requirements_description="Earned: Ass cum fetish at 50+",
                remove_requirements="girl.ass_cum_fetish < 40",
                remove_requirements_description="Lose: Ass cum fetish below 40",
                report_strings=[
                    "I actually like it when you cum on my ass...",
                    "Don't get me wrong, what you did was wrong... but I didn't hate it.",
                    "I shouldn't admit this, but I've been thinking about it all day."
                ]
            )
        if "conflicted_ass_cum_slut" not in database_traits:
            database_traits["conflicted_ass_cum_slut"] = Trait(
                name="conflicted_ass_cum_slut",
                display_name="Conflicted Ass Cum Slut",
                rarity=0.45,
                color="#9370DB",
                stat_growth_multipliers={"corruption": 0.05, "fear": 0.05},
                base_stat_modifiers={
                    "ass_sensitivity": 0.1,
                    "fear": 5,
                    "max_report_chance": 10
                },
                treated_as_tolerated_actions=[
                    "cumshot_ass"
                ],
                action_multipliers={
                    "cumshot_ass": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": 0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's conflicted but can't resist cum on her ass, showing visible distress during cumshot.",
                sponsor_description="Can be used for cumshot scenes but may require extra direction due to internal conflict.",
                earn_requirements="(girl.has_trait('conservative') or girl.has_trait('reserved')) and girl.ass_cum_fetish >= 50 and girl.ass_cum_fetish < 80",
                earn_requirements_description="Earned: Conservative/reserved girl with moderate ass cum fetish",
                remove_requirements="girl.ass_cum_fetish >= 80 or not (girl.has_trait('conservative') or girl.has_trait('reserved'))",
                remove_requirements_description="Transition: Fetish level 80+ or no longer conservative/reserved",
                report_strings=[
                    "I... I shouldn't have enjoyed that, but I couldn't help myself...",
                    "I feel so ashamed for liking it, but my body just... reacted.",
                    "Please don't tell anyone about this, I'm so embarrassed!"
                ]
            )
        # ASS PATH - TIER 3
        if "ass_cum_slut" not in database_traits:
            database_traits["ass_cum_slut"] = Trait(
                name="ass_cum_slut",
                display_name="Ass Cum Slut",
                rarity=0.35,
                color="#DB7093",  # Pale violet red
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "ass_sensitivity": 0.15,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.075
                },
                treated_as_tolerated_actions=[
                    "cumshot_ass", "sleep_cumshot_ass"
                ],
                action_multipliers={
                    "cumshot_ass": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_cumshot_ass": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's developed a strong fixation on having cum shot on her ass.",
                sponsor_description="Specializes in ass cumshot scenes, highly enthusiastic performer.",
                earn_requirements="girl.ass_cum_fetish >= 75",
                earn_requirements_description="Earned: Ass cum fetish at 75+",
                remove_requirements="girl.ass_cum_fetish < 65",
                remove_requirements_description="Lose: Ass cum fetish below 65",
                report_strings=[
                    "I can't concentrate when I'm thinking about your cum on my ass...",
                    "It's not just about the money anymore... I genuinely enjoy it.",
                    "I've been practicing how to keep the cum on my ass longer..."
                ]
            )
        # ASS PATH - TIER 4
        if "ass_cum_addict" not in database_traits:
            database_traits["ass_cum_addict"] = Trait(
                name="ass_cum_addict",
                display_name="Ass Cum Addict",
                rarity=0.25,
                color="#FF00FF",
                stat_growth_multipliers={"corruption": 0.1, "arousal": 0.075},
                base_stat_modifiers={
                    "ass_sensitivity": 0.25,
                    "shoot_acceptance": 0.15,
                    "financial_need": -0.1
                },
                treated_as_tolerated_actions=[
                    "cumshot_ass", "sleep_cumshot_ass"
                ],
                action_multipliers={
                    "cumshot_ass": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_cumshot_ass": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's completely addicted to cum on her ass and will actively beg for cumshot.",
                sponsor_description="Specializes in ass cumshot scenes, will enthusiastically perform even complex requests.",
                earn_requirements="girl.ass_cum_fetish >= 90",
                earn_requirements_description="Earned: Ass cum fetish at 90+",
                remove_requirements="girl.ass_cum_fetish < 80",
                remove_requirements_description="Lose: Ass cum fetish below 80",
                report_strings=[
                    "I can't get enough of your cum on my ass... please give me more!",
                    "I've been dreaming about feeling your cum on my ass again...",
                    "I love how you cover my ass with your hot cum!"
                ]
            )
        # ULTIMATE ASS FETISH (FINAL TIER)
        if "ass_cum_devotee" not in database_traits:
            database_traits["ass_cum_devotee"] = Trait(
                name="ass_cum_devotee",
                display_name="Ass Cum Devotee",
                rarity=0.15,
                color="#FF00FF",  # Magenta
                stat_growth_multipliers={"corruption": 0.15, "arousal": 0.1},
                base_stat_modifiers={
                    "ass_sensitivity": 0.3,
                    "shoot_acceptance": 0.2,
                    "financial_need": -0.15
                },
                treated_as_tolerated_actions=["cumshot_ass", "sleep_cumshot_ass"],
                action_multipliers={
                    "cumshot_ass": {
                        "target_girl": {"arousal": 0.3, "corruption": 0.3, "pressure": -0.3},
                        "other_girls": {"arousal": 0.25, "corruption": 0.3},
                        "player": {"arousal": 0.3},
                    },
                    "sleep_cumshot_ass": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.1},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    }
                },
                description="She's utterly devoted to having cum shot on her ass and will actively beg for cumshot constantly.",
                sponsor_description="Specializes in extreme ass cumshot scenes, will enthusiastically perform even the most complex requests.",
                earn_requirements="girl.ass_cum_fetish >= 100",
                earn_requirements_description="Earned: Ass cum fetish at 100+",
                remove_requirements="girl.ass_cum_fetish < 90",
                remove_requirements_description="Lose: Ass cum fetish below 90",
                report_strings=[
                    "I can't get enough of your cum on my ass... please give me more!",
                    "I've been dreaming about feeling your cum on my ass again...",
                    "I love how you cover my ass with your hot cum!"
                ]
            )
        
        #ON PUSSY (external)
        # PUSSY CUMSHOT PATH - TIER 2 
        if "pussy_cum_fixation" not in database_traits:
            database_traits["pussy_cum_fixation"] = Trait(
                name="pussy_cum_fixation",
                display_name="Pussy Cum Fixation",
                rarity=0.5,
                color="#FF69B4",
                stat_growth_multipliers={"corruption": 0.05, "arousal": 0.025},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.1,
                    "shoot_acceptance": 0.05,
                    "financial_need": -0.05
                },
                treated_as_tolerated_actions=[
                    "cumshot_pussy", "sleep_cumshot_pussy"
                ],
                action_multipliers={
                    "cumshot_pussy": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    },
                    "sleep_cumshot_pussy": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's developed a mild interest having cum shot on her pussy.",
                sponsor_description="Can perform basic pussy cumshot scenes with minimal direction.",
                earn_requirements="girl.pussy_cum_fetish >= 50",
                earn_requirements_description="Earned: Pussy cum fetish at 50+",
                remove_requirements="girl.pussy_cum_fetish < 40",
                remove_requirements_description="Lose: Pussy cum fetish below 40",
                report_strings=[
                    "I actually like it when you cum on my pussy...",
                    "Don't get me wrong, what you did was wrong... but I didn't hate it.",
                    "I shouldn't admit this, but I've been thinking about it all day."
                ]
            )
        if "conflicted_pussy_cum_slut" not in database_traits:
            database_traits["conflicted_pussy_cum_slut"] = Trait(
                name="conflicted_pussy_cum_slut",
                display_name="Conflicted Pussy Cum Slut",
                rarity=0.45,
                color="#9370DB",
                stat_growth_multipliers={"corruption": 0.05, "fear": 0.05},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.1,
                    "fear": 5,
                    "max_report_chance": 10
                },
                treated_as_tolerated_actions=[
                    "cumshot_pussy"
                ],
                action_multipliers={
                    "cumshot_pussy": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": 0.1},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's conflicted but can't resist cum on her pussy, showing visible distress during cumshot.",
                sponsor_description="Can be used for cumshot scenes but may require extra direction due to internal conflict.",
                earn_requirements="(girl.has_trait('conservative') or girl.has_trait('reserved')) and girl.pussy_cum_fetish >= 50 and girl.pussy_cum_fetish < 80",
                earn_requirements_description="Earned: Conservative/reserved girl with moderate Pussy cum fetish",
                remove_requirements="girl.pussy_cum_fetish >= 80 or not (girl.has_trait('conservative') or girl.has_trait('reserved'))",
                remove_requirements_description="Transition: Fetish level 80+ or no longer conservative/reserved",
                report_strings=[
                    "I... I shouldn't have enjoyed that, but I couldn't help myself...",
                    "I feel so ashamed for liking it, but my body just... reacted.",
                    "Please don't tell anyone about this, I'm so embarrassed!"
                ]
            )
        # PUSSY CUMSHOT PATH - TIER 3 
        if "pussy_cum_slut" not in database_traits:
            database_traits["pussy_cum_slut"] = Trait(
                name="pussy_cum_slut",
                display_name="Pussy Cum Slut",
                rarity=0.35,
                color="#DB7093",  # Pale violet red
                stat_growth_multipliers={"corruption": 0.075, "arousal": 0.05},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.15,
                    "shoot_acceptance": 0.1,
                    "financial_need": -0.075
                },
                treated_as_tolerated_actions=[
                    "cumshot_pussy", "sleep_cumshot_pussy"
                ],
                action_multipliers={
                    "cumshot_pussy": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_cumshot_pussy": {
                        "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                        "other_girls": {"arousal": 0.1, "corruption": 0.15},
                        "player": {"arousal": 0.15},
                    }
                },
                description="She's developed a strong fixation on having cum shot on her pussy.",
                sponsor_description="Specializes in pussy cumshot scenes, highly enthusiastic performer.",
                earn_requirements="girl.pussy_cum_fetish >= 75",
                earn_requirements_description="Earned: Pussy cum fetish at 75+",
                remove_requirements="girl.pussy_cum_fetish < 65",
                remove_requirements_description="Lose: Pussy cum fetish below 65",
                report_strings=[
                    "I can't concentrate when I'm thinking about your cum on my pussy...",
                    "It's not just about the money anymore... I genuinely enjoy it.",
                    "I've been practicing how to keep the cum on my pussy longer..."
                ]
            )
        # PUSSY CUMSHOT PATH - TIER 4 
        if "pussy_cum_addict" not in database_traits:
            database_traits["pussy_cum_addict"] = Trait(
                name="pussy_cum_addict",
                display_name="Pussy Cum Addict",
                rarity=0.25,
                color="#FF00FF",
                stat_growth_multipliers={"corruption": 0.1, "arousal": 0.075},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.25,
                    "shoot_acceptance": 0.15,
                    "financial_need": -0.1
                },
                treated_as_tolerated_actions=[
                    "cumshot_pussy", "sleep_cumshot_pussy"
                ],
                action_multipliers={
                    "cumshot_pussy": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.2},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    },
                    "sleep_cumshot_pussy": {
                        "target_girl": {"arousal": 0.1, "corruption": 0.1, "pressure": -0.05},
                        "other_girls": {"arousal": 0.05, "corruption": 0.1},
                        "player": {"arousal": 0.1},
                    }
                },
                description="She's completely addicted to cum on her pussy and will actively beg for cumshot.",
                sponsor_description="Specializes in pussy cumshot scenes, will enthusiastically perform even complex requests.",
                earn_requirements="girl.pussy_cum_fetish >= 90",
                earn_requirements_description="Earned: Pussy cum fetish at 90+",
                remove_requirements="girl.pussy_cum_fetish < 80",
                remove_requirements_description="Lose: Pussy cum fetish below 80",
                report_strings=[
                    "I can't get enough of your cum on my pussy... please give me more!",
                    "I've been dreaming about feeling your cum on my pussy again...",
                    "I love how you cover my pussy with your hot cum!"
                ]
            )
        # ULTIMATE PUSSY FETISH (FINAL TIER)
        if "pussy_cum_devotee" not in database_traits:
            database_traits["pussy_cum_devotee"] = Trait(
                name="pussy_cum_devotee",
                display_name="Pussy Cum Devotee",
                rarity=0.15,
                color="#FF00FF",  # Magenta
                stat_growth_multipliers={"corruption": 0.15, "arousal": 0.1},
                base_stat_modifiers={
                    "pussy_sensitivity": 0.3,
                    "shoot_acceptance": 0.2,
                    "financial_need": -0.15
                },
                treated_as_tolerated_actions=["cumshot_pussy", "sleep_cumshot_pussy"],
                action_multipliers={
                    "cumshot_pussy": {
                        "target_girl": {"arousal": 0.3, "corruption": 0.3, "pressure": -0.3},
                        "other_girls": {"arousal": 0.25, "corruption": 0.3},
                        "player": {"arousal": 0.3},
                    },
                    "sleep_cumshot_pussy": {
                        "target_girl": {"arousal": 0.2, "corruption": 0.2, "pressure": -0.1},
                        "other_girls": {"arousal": 0.15, "corruption": 0.2},
                        "player": {"arousal": 0.2},
                    }
                },
                description="She's utterly devoted to having cum shot on her pussy and will actively beg for cumshot constantly.",
                sponsor_description="Specializes in extreme pussy cumshot scenes, will enthusiastically perform even the most complex requests.",
                earn_requirements="girl.pussy_cum_fetish >= 100",
                earn_requirements_description="Earned: Pussy cum fetish at 100+",
                remove_requirements="girl.pussy_cum_fetish < 90",
                remove_requirements_description="Lose: Pussy cum fetish below 90",
                report_strings=[
                    "I can't get enough of your cum on my pussy... please give me more!",
                    "I've been dreaming about feeling your cum on my pussy again...",
                    "I love how you cover my pussy with your hot cum!"
                ]
            )

        #renpy.log("VT MOD: Successfully added cum fetish traits to database_traits")
    else:
        renpy.log("VT MOD ERROR: database_traits not found! Could not add fetish traits")