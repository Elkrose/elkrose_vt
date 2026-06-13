init 5 python:
    # Soft dependency on ggypt_library_expansion: if its library menu exists, repoint
    # "between_the_stacks" to our enhanced version (no label override). No-op if absent.
    if "database_library_options" in globals():
        vt_repoint_menu_label(database_library_options, "between_the_stacks", "vt_between_the_stacks")

label vt_between_the_stacks:
    player.character "Would you care to join me in the stacks. I'm sure we can find an interesting book for you."

    $ additional_subtag = "library"
    $girl_acceptance = selected_girl.get_acceptance_by_name("free_use_compliance")
    if girl_acceptance >= 20:
        selected_girl.character "Sure, I'm sure we can find something useful to do."

        "You and [selected_girl] set between the shelves where you suddenly aren't immediately noticable from the work area."

        "You spend a couple of minutes doing small talk, suggesting books that they might be interested in and what not."

        $selected_girl.apply_impacts({"affection": (1000, 1500)})

        menu:
            "Ask for a Blowjob":
                player.character "We are pretty tucked away here, how about you wrap those lips around my cock?"

                $girl_acceptance = selected_girl.get_acceptance_by_name("blowjob")
                if girl_acceptance >= 40:
                    $time_manager.skip_time(minutes=10)

                    "She doesn't even glance around before dropping into a low crouch and dragging your pants down."

                    call generic_action_blowjob(additional_subtags=additional_subtag, skip_responses=True, force_cum=True)

                    "With a groan, you release into [selected_girl]'s mouth."
                    if librarian:
                        "You catch the librarian sneaking a quick glance at what you are doing."
                    $selected_girl.apply_impacts({"naturism": (1000, 1500), "corruption": (1000, 1500)})

                elif girl_acceptance >= 20:
                    selected_girl.character "No thank you. I should really get back to my studies."

                    "She pulls back, crossing her arms, angling to head back to her work table."
                    $grade_differential = selected_girl.mother.get_next_grade_target() - selected_girl.grades
                    if grade_differential > 2:
                        menu:
                            "Push Her (+2 Grade)":
                                $time_manager.skip_time(minutes=10)
                                player.character "If you do this, I can make sure your grade is up to snuff."
                                player.character "I'm sure you would much rather be doing things other than studying."
                                "You watch as the girl considers your words before kneeling down and fishing your cock out."
                                call generic_action_blowjob(additional_subtags=additional_subtag, skip_responses=True, force_cum=True)
                                "Watching a girl work for her grades like this was quite the sight, and you didn't last that long."
                                "You pull out and spray your load on the girl's face."
                                "After a beat the girl, flushed, rushes out of the library, only stopping to gather up her supplies."

                                $selected_girl.grades = min(100, selected_girl.grades + 2)
                                $selected_girl.apply_impacts({"corruption": (1000, 1500), "affection": (-2500, -2000), "fear": (1000, 1500)})
                                $remove_girl_id_from_location(selected_girl.id, "girls_at_library")

                            "Don't Push It":
                                "You decided it isn't worth it to push things."
                                "You let her return to her table and get back to her homework."
                                $actions_already_done[selected_girl.id].append("block_talking_library")
                                $selected_girl.apply_impacts({"affection": -1500})
                    else:
                        "You let her go, you don't have enough leverage on her to push things."
                        "[selected_girl] makes their way back to their table and starts continuing with their homework."
                        $actions_already_done[selected_girl.id].append("block_talking_library")
                        $selected_girl.apply_impacts({"affection": - 1500})
                else:
                    selected_girl.character "What!? No Way, I'm not doing that with you, let alone here."

                    "She storms back to the table she was working at, gathers up her supplies, and hurries out of the library."

                    $remove_girl_id_from_location(selected_girl.id, "girls_at_library")
                    $selected_girl.apply_impacts({"affection": - 2500, "fear": 1000})


            "Ask for a Titjob" if not (selected_girl.has_trait("small_boobs") or selected_girl.has_trait("small_boobs_fake")):
                player.character "No one will see us back here, why don't you take those tits out and use them?"
                $girl_acceptance = selected_girl.get_acceptance_by_name("fuck_boobs")
                if girl_acceptance >= 40:
                    $time_manager.skip_time(minutes=20)
                    if selected_girl.is_wearing_clothing_in_slots("upper") or selected_girl.is_wearing_clothing_in_slots("bra"):
                        $ _vt_boobs = selected_girl.boob_description()
                        "She quickly glances around before pulling her [_vt_boobs] out of her outfit."
                    else:
                        selected_girl.character "Well, they are already out, so easy enough to use."

                    "With the clothing out of the way, she wraps her tits around your cock."

                    selected_girl.character "I love how your throbbing meat feels between my tits."

                    call generic_action_fuck_boobs(additional_subtags=additional_subtag, skip_responses=True,force_cum=True)

                    "With a groan, you unleash your seeds on her tits."

                    "She takes a second to rub your seeds into her skin."

                    selected_girl.character "Thanks big guy."

                    "With that she gathers up her things and heads back out into the school."

                    $selected_girl.apply_impacts({"corruption": 1500})
                    $remove_girl_id_from_location(selected_girl.id, "girls_at_library")
                elif girl_acceptance >= 20:
                    selected_girl.character "I would prefer not, who knows who could see my boobs if I did that."
                    if "blowjob" in rule_manager.get_all_tolerated_actions(selected_girl):
                        selected_girl.character "If you want it I could give you a blowjob instead."
                        "You nod and she quickly crouches down and pulls your cock free from its confines."
                        call generic_action_blowjob(additional_subtags=additional_subtag, skip_responses = True, force_cum = True)
                        "With a groan, you unleash your seeds into her mouth."
                        selected_girl.character "I'm glad we could come to a compromise, now I am going to head back to my studies."

                        $actions_already_done[selected_girl.id].append("block_talking_library")
                        $selected_girl.apply_impacts({"affection": -250, "corruption": 1000})

                    else:
                        "If you don't mind, I would prefer to head back and continue on my studies."
                        $actions_already_done[selected_girl.id].append("block_talking_library")
                        $selected_girl.apply_impacts({"affection": -500})
                else:
                    selected_girl.character "No, I don't want to show you my tits, and especially not put your member between them."
                    "With that, she quickly gathers her stuff and storms out of the library."
                    $remove_girl_id_from_location(selected_girl.id, "girls_at_library")
                    $selected_girl.apply_impacts({"affection": -2500, "fear": 1000})

            "I want to fuck you." if not selected_girl.wants_vaginal_condom:
                player.character "No one will see us back here, let's be quick."
                $girl_acceptance = selected_girl.get_acceptance_by_name("fuck_pussy")
                if girl_acceptance >= 40:
                    $time_manager.skip_time(minutes=20)
                    if selected_girl.is_wearing_clothing_in_slots("lower") or selected_girl.is_wearing_clothing_in_slots("panties"):
                        "She quickly glances around before pulling her clothes down bending over, wiggling her ass and spreading her pussy apart."
                    else:
                        "She bends over and grabs a bookshelf to steady herself as she presents her ass and wet pussy to you."
                    
                    selected_girl.character "Time is a tickin, get dickin, Professor!"
                                   
                    $ apply_action_impacts("fuck_pussy")

                    call generic_action_fuck_pussy(additional_subtags=additional_subtag, skip_descriptions=False, skip_responses=False, force_cum=True, ask_to_cum=False, force_orgasm=True)
                    
                    "As you both recover from your quick study session, you almost accidentally pinch your dick while zipping up."

                    "She notices and giggles."

                    selected_girl.character "Don't hurt him, he was a good soldier."

                    "With that she gathers up her things and heads back out into the school."

                    $selected_girl.apply_impacts({"corruption": 1500})
                    $remove_girl_id_from_location(selected_girl.id, "girls_at_library")
                else:
                    selected_girl.character "No, I don't want to fuck right now, you old horn dog!"
                    "With that, she quickly gathers her stuff and storms out of the library."
                    $remove_girl_id_from_location(selected_girl.id, "girls_at_library")
                    $selected_girl.apply_impacts({"affection": -500, "fear": 300})

            "Finish your chat":
                player.character "This has been pleasant. Shall we get you back to your studies?"

                selected_girl.character "Thank you for the recommendations, I will keep them in mind."

                "You watch as she walks back to the tables and gathers her supplies before leaving the library."

                $ remove_girl_id_from_location(selected_girl.id, "girls_at_library")
        return "show_academy_library"
    else:
        selected_girl.character "No thanks... I would prefer to keep working on my homework."

        "She shifts uncomfortably, turning her eyes back to the textbook out in front of her."

    return
