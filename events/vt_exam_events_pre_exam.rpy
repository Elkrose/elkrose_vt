init 5 python:
#making it a habit to init hijank label lower priority
    config.label_overrides["exam_event_girl_caught_masturbating"] = "vt_exam_event_girl_caught_masturbating"

label vt_exam_event_girl_caught_masturbating:
    $ selected_girl = current_event.participants[0]

    $ descriptions = [
        "You arrive at the classroom door only to hear someone inside. As you approach, the sounds become more distinct. You hesitate for a moment, then decide to open the door.",
        "You can hear muffled moans and the sound of movement coming from the classroom. You're not sure what's going on, but you decide to investigate.",
        "As you walk down the hallway, you notice that one of the classroom doors is slightly ajar. You can hear soft gasps and the rustling of fabric. You push the door open..."
    ]
    $ description = renrandom.choice(descriptions)
    "[description]"

    $ apply_action_impacts("masturbate")

    $ current_event.show_video("masturbate", sub_tags=["class"])

    $ descriptions = [
        f"You open the door to find {selected_girl} in an intimate moment with herself. She's so absorbed in her own world that she doesn't notice your presence initially. When she does, her eyes widen with surprise and she hastily attempts to conceal herself.",
        f"As you push the door open, you discover {selected_girl} engaged in a personal act. She's so immersed in her pleasure that she doesn't realize you're there. When she finally does, her eyes fill with shock and she quickly tries to cover up",
        f"Upon opening the door, you stumble upon {selected_girl} in a private moment. She's so captivated by her actions that she doesn't notice you at first. When she does, her eyes widen in embarrassment and she hurriedly tries to hide herself",
        f"The door creaks open to reveal {selected_girl} in a compromising position. She's so engrossed in her own world that she doesn't notice you. When she does, her eyes widen in alarm and she quickly tries to cover herself",
        f"As the door swings open, you catch {selected_girl} in a moment of self-indulgence. She's so lost in her actions that she doesn't notice you. When she does, her eyes widen in panic and she hastily tries to cover herself"
    ]
    $ description = renrandom.choice(descriptions)
    "[description]"

    $ girl_response = selected_girl.get_response_for_action("caught_her_masturbating")
    if girl_response:
        selected_girl.character "[girl_response]"

    menu(title_text="What do you do?"):
        "I'm sorry, I didn't mean to interrupt. I'll leave you to it.":
            $ girl_reaction = selected_girl.get_reaction_for_action("leave_her_to_masturbate")
            if girl_reaction:
                "[girl_reaction]"

            $ current_event.apply_impacts(impacts={
                "participants": {"impacts": {"corruption": (250, 500), "affection": (1000, 2000), "fear": (-2000, -1000)}}
            })

        "I don't mind if you keep going. I can watch.":
            $ girl_response = selected_girl.get_response_for_action("watch_her_masturbate")

            if not selected_girl.get_action_success_by_name("watch_her_masturbate"):
                $ girl_reaction = selected_girl.get_reaction_for_action("watch_her_masturbate")
                if girl_reaction:
                    "[girl_reaction]"

                if girl_response:
                    selected_girl.character "[girl_response]"

                $ current_event.apply_impacts(impacts={
                    "participants": {"impacts": {"corruption": (250, 500), "fear": (500, 1000)}}
                })
            else:
                if girl_response:
                    selected_girl.character "[girl_response]"

                $ current_event.show_video("masturbate", sub_tags=["class"])

                $ description = player.get_description_for_action("watch_her_masturbate", selected_girl)
                if description:
                    "[description]"

                $ current_event.show_video("orgasm", sub_tags=["class"])

                $ selected_girl.cum()
                $ selected_girl.just_came = False

                $ selected_girl.add_to_action_tracker("masturbate_orgasm")

                $ description = player.get_description_for_action("watch_her_masturbate_orgasm", selected_girl, accept_chance_calculation_name="watch_her_masturbate")
                if description:
                    "[description]"

                $ girl_response = selected_girl.get_response_for_action("watch_her_masturbate_orgasm", accept_chance_calculation_name="watch_her_masturbate")
                if girl_response:
                    selected_girl.character "[girl_response]"

                $ current_event.apply_impacts(impacts={
                    "participants": {"impacts": {"corruption": (500, 1000), "affection": (500, 1000), "fear": (-1000, -500)}},
                    "player": {"impacts": {"arousal": (5, 15)}}
                })

                $ current_event.hide_video()

                $ player_response = player.get_response_for_action("watch_her_masturbate_orgasm", selected_girl, accept_chance_calculation_name="watch_her_masturbate")
                if player_response:
                    player.character "[player_response]"

                "You take your position behind your desk, while [selected_girl] composes herself and she quickly gets dressed again before the other girls arrive."
                
                $ player.arousal = player.arousal_for_erection

                return

        "I can help you out, if you want.":
            $ girl_response = selected_girl.get_response_for_action("offer_finger_pussy")

            if not selected_girl.get_action_success_by_name("offer_finger_pussy"):
                $ girl_reaction = selected_girl.get_reaction_for_action("offer_finger_pussy")
                if girl_reaction:
                    "[girl_reaction]"

                if girl_response:
                    selected_girl.character "[girl_response]"

                $ current_event.apply_impacts(impacts={
                    "participants": {"impacts": {"corruption": (250, 500), "fear": (750, 1250)}}
                })
            else:
                if girl_response:
                    selected_girl.character "[girl_response]"

                $ current_event.show_video("finger_pussy", sub_tags=["class"])

                $ description = player.get_description_for_action("finger_pussy", selected_girl, accept_chance_calculation_name="offer_finger_pussy")
                if description:
                    "[description]"

                $ girl_response = selected_girl.get_response_for_action("finger_pussy", accept_chance_calculation_name="offer_finger_pussy")
                if girl_response:
                    selected_girl.character "[girl_response]"

                $ selected_girl.cum()
                $ selected_girl.just_came = False

                $ current_event.show_video("orgasm", sub_tags=["class"])

                $ girl_reaction = selected_girl.get_reaction_for_action("finger_pussy_orgasm", default_to="orgasm", accept_chance_calculation_name="offer_finger_pussy")
                if girl_reaction:
                    "[girl_reaction]"

                $ girl_response = selected_girl.get_response_for_action("finger_pussy_orgasm", default_to="orgasm", accept_chance_calculation_name="offer_finger_pussy")
                if girl_response:
                    selected_girl.character "[girl_response]"

                $ apply_action_impacts("finger_pussy")

                $ current_event.hide_video()

                $ player_response = player.get_response_for_action("finger_pussy_orgasm", selected_girl, default_to="orgasm", accept_chance_calculation_name="offer_finger_pussy")
                if player_response:
                    player.character "[player_response]"

                $ selected_girl.add_to_action_tracker("finger_pussy_orgasm")

                "You take your position behind your desk, while [selected_girl] composes herself and she quickly gets dressed again before the other girls arrive."

                $ player.arousal = player.arousal_for_erection

                return

        "I want to taste you.":
            $ girl_response = selected_girl.get_response_for_action("offer_lick_pussy")

            if not selected_girl.get_action_success_by_name("offer_lick_pussy"):
                $ girl_reaction = selected_girl.get_reaction_for_action("offer_lick_pussy")
                if girl_reaction:
                    "[girl_reaction]"

                if girl_response:
                    selected_girl.character "[girl_response]"

                $ current_event.apply_impacts(impacts={
                    "participants": {"impacts": {"corruption": (250, 500), "fear": (1000, 1500)}}
                })
            else:
                if girl_response:
                    selected_girl.character "[girl_response]"

                $ current_event.show_video("lick_pussy", sub_tags=["class"])

                $ description = player.get_description_for_action("lick_pussy", selected_girl, accept_chance_calculation_name="offer_lick_pussy")
                if description:
                    "[description]"

                $ girl_response = selected_girl.get_response_for_action("lick_pussy", accept_chance_calculation_name="offer_lick_pussy")
                if girl_response:
                    selected_girl.character "[girl_response]"

                $ selected_girl.cum()
                $ selected_girl.just_came = False

                $ current_event.show_video("orgasm", sub_tags=["class"])

                $ girl_reaction = selected_girl.get_reaction_for_action("lick_pussy_orgasm", default_to="orgasm", accept_chance_calculation_name="offer_lick_pussy")
                if girl_reaction:
                    "[girl_reaction]"

                $ girl_response = selected_girl.get_response_for_action("lick_pussy_orgasm", default_to="orgasm", accept_chance_calculation_name="offer_lick_pussy")
                if girl_response:
                    selected_girl.character "[girl_response]"

                $ apply_action_impacts("lick_pussy")

                $ current_event.hide_video()

                $ player_response = player.get_response_for_action("lick_pussy_orgasm", selected_girl, default_to="orgasm", accept_chance_calculation_name="offer_lick_pussy")
                if player_response:
                    player.character "[player_response]"

                $ selected_girl.add_to_action_tracker("lick_pussy_orgasm")

                "You wipe your face clean, while [selected_girl] composes herself and she quickly gets dressed again before the other girls arrive."

                $ player.arousal = player.arousal_for_erection

                return

        "I want to fuck you. (no condom)" if not selected_girl.wants_vaginal_condom:
            $ girl_response = selected_girl.get_response_for_action("fuck_pussy")

            if not selected_girl.get_action_success_by_name("fuck_pussy"):
                $ girl_reaction = selected_girl.get_reaction_for_action("fuck_pussy")
                if girl_reaction:
                    "[girl_reaction]"

                if girl_response:
                    selected_girl.character "[girl_response]"

                $ current_event.apply_impacts(impacts={
                    "participants": {"impacts": {"corruption": (250, 500), "fear": (1250, 1750)}}
                })
            else:
                selected_girl.character "Yes, yes please Professor, slide your cock into me right now! "
                # if girl_response:
                    # selected_girl.character "[girl_response]"
                $ apply_action_impacts("fuck_pussy")

                $ current_event.show_video("fuck_pussy", sub_tags=["class"])

                $ girl_response = selected_girl.get_response_for_action("fuck_pussy", accept_chance_calculation_name="fuck_pussy")
                if girl_response:
                    selected_girl.character "[girl_response]"
                
                menu(title_text="Where do you cum?"):
                    "Inside her?":
                        $ selected_girl.cum()
                        $ selected_girl.just_came = False
                        
                        $ current_event.show_video("orgasm", sub_tags=["class"])

                        $ apply_action_impacts("creampie_pussy")
                        
                        $ current_event.show_video("creampie_pussy", sub_tags=["class"])
                        
                        $ girl_reaction = selected_girl.get_reaction_for_action("creampie_pussy", default_to="orgasm", accept_chance_calculation_name="creampie_pussy")
                        if girl_reaction:
                            "[girl_reaction]"
                        
                        $ girl_response = selected_girl.get_response_for_action("creampie_pussy", default_to="orgasm", accept_chance_calculation_name="creampie_pussy")
                        if girl_response:
                            selected_girl.character "[girl_response]"

                        $ current_event.hide_video()

                        $ player_response = player.get_response_for_action("creampie_pussy", selected_girl, default_to="orgasm", accept_chance_calculation_name="creampie_pussy")
                        if player_response:
                            player.character "[player_response]"
                        
                        $ selected_girl.add_to_action_tracker("fuck_pussy_creampie")
                        
                        "You clean yourself up and pull up your pants and fix your tie, while [selected_girl] composes herself and she quickly gets dressed again before the other girls arrive."

                        $ player.arousal = player.arousal_for_erection
                        
                        $ current_event.hide_video()
                        
                        return
                    
                    "On her ass?":
                     
                        $ selected_girl.cum()
                        $ selected_girl.just_came = False
                        
                        $ current_event.show_video("orgasm", sub_tags=["class"])

                        $ apply_action_impacts("cumshot_ass")
                        
                        $ current_event.show_video("cumshot_ass", sub_tags=["class"])
                        
                        $ girl_reaction = selected_girl.get_reaction_for_action("cumshot_ass", default_to="orgasm", accept_chance_calculation_name="cumshot_ass")
                        if girl_reaction:
                            "[girl_reaction]"
                        
                        $ girl_response = selected_girl.get_response_for_action("cumshot_ass", default_to="orgasm", accept_chance_calculation_name="cumshot_ass")
                        if girl_response:
                            selected_girl.character "[girl_response]"

                        $ current_event.hide_video()

                        $ player_response = player.get_response_for_action("cumshot_ass", selected_girl, default_to="orgasm", accept_chance_calculation_name="cumshot_ass")
                        if player_response:
                            player.character "[player_response]"
                        
                        $ selected_girl.add_to_action_tracker("cumshot_ass")
                        
                        "You clean yourself up and pull up your pants and fix your tie, while [selected_girl] composes herself and she quickly gets dressed again before the other girls arrive."

                        $ player.arousal = player.arousal_for_erection
                        
                        $ current_event.hide_video()
                        
                        return
                
    $ current_event.hide_video()

    return
