init -1 python: 
    database_traits["daddys_girl"] = Trait(
        name="daddys_girl",
        display_name="Daddy's girl",
        color="#9249F0",
        rarity=0,
        stat_growth_multipliers={"naturism": 0.03,"corruption": 0.03,"pressure": -0.5, "arousal": 0.025},
        base_stat_modifiers={"mouth_sensitivity": 0.05, "pussy_sensitivity": 0.05, "ass_sensitivity": 0.05, "acceptance": 20,"naturism": 0.05, "corruption": 0.15, "obedience_factor": 0.15, "max_tolerance": 0.15,"discipline": 0.15, "people_skill": 0.25, "max_tolerance": 80,"shoot_proficiency": 0.5, "base_arousal": 20},
        treated_as_tolerated_actions=["exam_action_spank_ass","exam_action_slap_ass", "facial","blowjob",
            "use_mouth", "cum_in_panties","creampie_mouth", "creampie_pussy", "creampie_ass","remove_lower", "remove_panties","remove_pantyhose","tease_clit","finger_pussy", "sleep_facials", "sleep_creampie_mouth", "sleep_creampie_pussy",],
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
            "remove_panties": {
                "target_girl": {"naturism": 0.2, "corruption": 0.15, "pressure": -0.15},
                "other_girls": {"naturism": 0.1, "corruption": 0.15},
                "player": {"arousal": 0.15},
            },
            "cum_in_panties": {
                "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                "other_girls": {"arousal": 0.1, "corruption": 0.15},
                "player": {"arousal": 0.15},
            },
            "blowjob": {
                "target_girl": {"arousal": 0.2, "corruption": 0.15, "pressure": -0.15},
                "other_girls": {"arousal": 0.1, "corruption": 0.15},
                "player": {"arousal": 0.15},
            },
            "tease_clit": {
                "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                "other_girls": {"arousal": 0.1, "corruption": 0.15},
                "player": {"arousal": 0.15},
            },
            "finger_pussy": {
                "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                "other_girls": {"arousal": 0.1, "corruption": 0.15},
                "player": {"arousal": 0.15},
            },
            "masturbate": {
                "target_girl": {"arousal": 0.2, "corruption": 0.15, "pressure": -0.15},
                "other_girls": {"arousal": 0.1, "corruption": 0.15},
                "player": {"arousal": 0.15},
            },
            "use_mouth": {
                "target_girl": {"arousal": 0.1, "corruption": 0.15, "pressure": -0.15},
                "other_girls": {"arousal": 0.1, "corruption": 0.15},
                "player": {"arousal": 0.15},
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
            },
            "sleep_creampie_pussy": {
                    "target_girl": {"arousal": 0.15, "corruption": 0.15, "pressure": -0.15},
                    "other_girls": {"arousal": 0.1, "corruption": 0.15},
                    "player": {"arousal": 0.15},
                }
        },
        description="She has a daddy's girl complex, and currently it is affixed to you.",
    )
