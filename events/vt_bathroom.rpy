# girls_in_bathroom - location_database
# show_academy_bathroom

label vt_academy_bathroom_sex:
    # Clear identification of relationship types
    $ is_base_mother = False
    $ is_student = False
    $ is_other = False

    # Check mother relationship
    if hasattr(selected_girl, "daughter") and selected_girl.daughter:
        $ is_base_mother = True
        $ renpy.log(f"Identified {selected_girl.first_name} as mother (daughter: {selected_girl.daughter})")

    # Check student relationship
    elif hasattr(selected_girl, "mother") and selected_girl.mother:
        $ is_student = True
        $ renpy.log(f"Identified {selected_girl.first_name} as student (mother: {selected_girl.mother})")

    # Everything else
    else:
        $ is_other = True
        $ renpy.log(f"Identified {selected_girl.first_name} as neither mother nor student")
    
    # PROPER KIDS TRACKING
    $ total_kids = selected_girl.kids
    $ kids_with_player = selected_girl.kids_with_player
    $ kids_with_others = selected_girl.kids_with_npc
    
    # MOTHERHOOD STATUS
    $ is_currently_a_mother = total_kids > 0
    if is_base_mother:
        $ is_currently_a_mother = total_kids > 1  # includes original daughter
    
    # PREGNANCY PHASE (Simplified)
    $ pregnancy_phase = 0
    # 0 - not pregnant, 1 - First Trimester, 2- 2nd, 3- 3rd Trimester/Final stages
    if selected_girl.pregnant:
        $ pregnancy_phase = selected_girl.pregnancy_phase
    
    # KNOWLEDGE MATRIX
    $ player_knows = hasattr(selected_girl, "player_knows_pregnant") and selected_girl.player_knows_pregnant
    $ she_knows = selected_girl.knows_pregnant

    # Initialize and validate relationship tracking in one atomic operation
    python:
        # Find which core stats are highest (only these matter for first impression)
        girl_stats = {
            "corruption": selected_girl.corruption,
            "fear": selected_girl.fear,
            "affection": selected_girl.affection,
            "discipline": selected_girl.discipline,
            "intellect": selected_girl.intellect,
            "naturism": selected_girl.naturism
        }
        # MAP GIRL STATS TO APPROACHES
        girl_approaches = {
            "dominate": (girl_stats["discipline"] + girl_stats["fear"]) / 2,
            "compassionate": (girl_stats["affection"] + girl_stats["intellect"]) / 2,
            "sexualized": (girl_stats["corruption"] + girl_stats["naturism"]) / 2,
            "transactional": (girl_stats["corruption"] + girl_stats["intellect"]) / 2
        }
        # Get the two highest stats for the girl (for detailed reactions)
        sorted_girl_stats = sorted(girl_stats.items(), key=lambda item: item[1], reverse=True)
        dominant_girl_stat1, dominant_girl_value1 = sorted_girl_stats[0]
        dominant_girl_stat2, dominant_girl_value2 = sorted_girl_stats[1]

        # Get girl's dominant approach
        dominant_girl_approach = max(girl_approaches, key=girl_approaches.get)
        girl_approach_value = girl_approaches[dominant_girl_approach]
        
        # Store for dialogue use
        selected_girl.dominant_approach = dominant_girl_approach
        selected_girl.approach_strength = girl_approach_value
        selected_girl.dominant_stat1 = dominant_girl_stat1
        selected_girl.dominant_stat2 = dominant_girl_stat2

        player_stats = {
            "control": player.control,
            "greed": player.greed,
            "lust": player.lust,
            "compassion": player.compassion,
            "reputation": player.reputation,
            "arousal": player.arousal
        }

        # Replace the normalization section around line 87:
        norm_compassion = (player.compassion + 10) / 2
        norm_control = (player.control + 10) / 2
        norm_reputation = player.reputation / 10
        norm_lust = (player.lust + 10) / 2
        norm_arousal = player.arousal / 12
        norm_greed = player.greed / 10
        
        # Map to your four approaches
        player_approaches = {
            "dominate": (norm_control + norm_reputation) / 2,
            "compassionate": (norm_compassion + norm_reputation) / 2,
            "sexualized": (norm_lust + norm_arousal) / 2,
            "transactional": (norm_greed + norm_reputation) / 2  # Greed + reputation for better deals
        }

        # Get player's dominant approach
        dominant_approach = max(player_approaches, key=player_approaches.get)
        approach_value = player_approaches[dominant_approach]
        is_natural_approach = approach_value > 6  # Above 60% on 0-10 scale

    $ time_manager.skip_time(minutes=5)

    # *** START OF NEW DIALOGUE SYSTEM FOR FIRST GIRL ***
    # Present the player with a choice of approach
    player.character "Let's get into one of the stalls..."
    menu:
        
        "Get in the stall. Now. (Dominate)":
            $ chosen_approach = "dominate"

        "Come here... I want to feel close to you. Just for a moment. (Compassionate)":
            $ chosen_approach = "compassionate"

        "I'm so hard right now. I need you to take care of it. (Sexualized)":
            $ chosen_approach = "sexualized"

        "I'll make it worth your while. (Transactional)":
            $ chosen_approach = "transactional"

    # Calculate the final acceptance score based on the player's choice and the girl's personality
    python:
        # Base acceptance from the girl's core stats for the interaction itself
        base_acceptance = selected_girl.get_acceptance_by_name("sex_interaction")

        # Bonus if the chosen approach matches the girl's dominant approach
        approach_match_bonus = 0
        if chosen_approach == selected_girl.dominant_approach:
            # The stronger her personality, the bigger the bonus for matching it
            approach_match_bonus = int(selected_girl.approach_strength * 5) # e.g., 8.0 -> 40 point bonus

        # Penalty if the chosen approach clashes with the girl's dominant approach
        # This is a simple map of direct opposites
        approach_clash_map = {
            "dominate": "compassionate",
            "compassionate": "dominate",
            "sexualized": "transactional", # See's one as sleazy, the other as cold
            "transactional": "sexualized"
        }
        approach_clash_penalty = 0
        if approach_clash_map.get(chosen_approach) == selected_girl.dominant_approach:
            # The stronger her clashing personality, the bigger the penalty
            approach_clash_penalty = -int(selected_girl.approach_strength * 3) # e.g., 8.0 -> -24 point penalty

        # Final calculated acceptance
        final_acceptance = base_acceptance + approach_match_bonus + approach_clash_penalty
        renpy.log(f"Base: {base_acceptance}, Match: {approach_match_bonus}, Clash: {approach_clash_penalty}, Final: {final_acceptance}")

    # *** DIALOGUE REACTIONS BASED ON FINAL_ACCEPTANCE ***
    if final_acceptance >= 40:
        # --- SUCCESS ---
        "[selected_girl] smiles at you."
        $ se_forced_sex = False
        $ se_participants = [selected_girl]
        $ se_action_duration = 3
        $ se_use_generic_ending = True
        $ se_remove_girls_from_location = True
        $ se_additional_webm_sub_tags = ["bathroom"]

        # Custom success dialogue based on the approach used and girl's personality
        # Custom success action based on the approach used and girl's personality
        if chosen_approach == "dominate":
            if is_student:
                selected_girl.character "Yes Professor... as you wish."
                "Her eyes cast down as she obediently walks into the stall."
            elif is_base_mother:
                "She glares at you, but a flicker of excitement in her eyes betrays her as she steps into the stall without a word."
            else: # is_other
                if selected_girl.dominant_stat1 == "discipline":
                    "She gives a sharp, approving nod and enters the stall."
                elif selected_girl.dominant_stat1 == "fear":
                    "She flinches and practically scurries into the stall, eager to please."
                else:
                    "She rolls her eyes but complies, a slight blush on her cheeks as she enters the stall."

        elif chosen_approach == "compassionate":
            if is_student:
                selected_girl.character "Oh, Professor... really? Here? Okay... yes, I'd love that."
                "She smiles shyly, taking your hand before leading you towards the stall."
            elif is_base_mother:
                "Her expression softens, and she gently pulls you into the stall with her."
            else: # is_other
                if selected_girl.dominant_stat1 == "affection":
                    "She beams, taking your arm and walking with you to the stall."
                elif selected_girl.dominant_stat1 == "intellect":
                    "She gives a thoughtful smile and follows you into the stall."
                else:
                    "She seems genuinely touched as she enters the stall ahead of you."

        elif chosen_approach == "sexualized":
            if is_student:
                selected_girl.character "Professor! You're so bad... I love it."
                "A wicked grin spreads across her face as she sashays into the stall, looking back over her shoulder."
            elif is_base_mother:
                "She sighs dramatically, but the smirk on her face tells you she's more than happy to oblige as she enters the stall."
            else: # is_other
                if selected_girl.dominant_stat1 == "corruption":
                    "She licks her lips and grabs your shirt, pulling you into the stall with her."
                elif selected_girl.dominant_stat1 == "naturism":
                    "She says it with a serene confidence, unashamedly entering the stall."
                else:
                    "She giggles, her face flushing as she hurries into the stall."

        elif chosen_approach == "transactional":
            # Success means she sees personal gain and wants to pursue it.
            if is_student:
                selected_girl.character "Smart move. I like a man who thinks ahead."
                "She gives you a conspiratorial smile and slips into the stall."
            elif is_base_mother:
                selected_girl.character "Good. You're learning how to get what you want."
                "She looks proud, a smirk on her lips as she enters the stall."
            else: # is_other
                if selected_girl.dominant_stat1 == "intellect":
                    selected_girl.character "An opportunity for advancement... I accept."
                    "She gives a crisp, business-like nod and enters the stall."
                elif selected_girl.dominant_stat1 == "corruption":
                    selected_girl.character "Heh. I like the way you operate. Let's go."
                    "She grins, already anticipating the benefits as she enters the stall."
                else:
                    selected_girl.character "Okay, you've got my attention. This could be fun."
                    "She looks intrigued and enters the stall, ready to see what's in it for her."

        "You look around as she slips into the stall."
        # *** START OF SECOND GIRL INVITATION LOGIC ***
        if len(girls_in_bathroom) > 1:
            python:
                other_girls_in_area = [girl_id for girl_id in girls_in_bathroom if girl_id and girl_id != selected_girl.id]
                menu_options = [("Try get someone else to join?", "title"),]
                if other_girls_in_area:
                    for girl_id in other_girls_in_area:
                        if not girl_id: continue
                        girl = academy.get_girl_by_id(girl_id)
                        if not girl: continue
                        menu_options.append((f"{girl.full_name}", f"girl|{girl_id}"))
                menu_options.append(("No", "None"))
                menu_choice = renpy.display_menu(menu_options)

            if menu_choice == "None":
                "You slip into the stall behind [selected_girl], and you latch it shut..."
            else:
                $ girl_id = menu_choice.split("|")[-1]
                $ girl = academy.get_girl_by_id(girl_id)

                # *** START OF NEW DIALOGUE SYSTEM FOR SECOND GIRL ***
                # First, we need to calculate the dominant approaches for this NEW girl
                python:
                    # Find which core stats are highest for the new girl
                    girl2_stats = {
                        "corruption": girl.corruption,
                        "fear": girl.fear,
                        "affection": girl.affection,
                        "discipline": girl.discipline,
                        "intellect": girl.intellect,
                        "naturism": girl.naturism
                    }
                    # MAP NEW GIRL STATS TO APPROACHES
                    girl2_approaches = {
                        "dominate": (girl2_stats["discipline"] + girl2_stats["fear"]) / 2,
                        "compassionate": (girl2_stats["affection"] + girl2_stats["intellect"]) / 2,
                        "sexualized": (girl2_stats["corruption"] + girl2_stats["naturism"]) / 2,
                        "transactional": (girl2_stats["corruption"] + girl2_stats["intellect"]) / 2
                    }
                    # Get new girl's dominant approach
                    girl.dominant_approach = max(girl2_approaches, key=girl2_approaches.get)
                    girl.approach_strength = girl2_approaches[girl.dominant_approach]
                    
                    # Get the two highest stats for the new girl (for detailed reactions)
                    sorted_girl2_stats = sorted(girl2_stats.items(), key=lambda item: item[1], reverse=True)
                    girl.dominant_stat1 = sorted_girl2_stats[0][0]
                    girl.dominant_stat2 = sorted_girl2_stats[1][0]

                # Now present the player with a choice of approach for the second girl
                menu:
                    player.character "Hey, [girl.full_name]... we're in here having some fun. Want in?"

                    "Get in here. Don't make me ask twice. (Dominate)":
                        $ chosen_approach_2 = "dominate"

                    "It would be really special if you joined us. Please? (Compassionate)":
                        $ chosen_approach_2 = "compassionate"

                    "We're having a blast, and you look like you need it too. Come on. (Sexualized)":
                        $ chosen_approach_2 = "sexualized"

                    "I'll make it worth your while. (Transactional)":
                        $ chosen_approach_2 = "transactional"

                # Calculate the final acceptance score for the second girl
                python:
                    base_acceptance_2 = girl.get_acceptance_by_name("sex_interaction")
                    approach_match_bonus_2 = int(girl.approach_strength * 5) if chosen_approach_2 == girl.dominant_approach else 0
                    approach_clash_map_2 = {"dominate": "compassionate", "compassionate": "dominate", "sexualized": "transactional", "transactional": "sexualized"}
                    approach_clash_penalty_2 = -int(girl.approach_strength * 3) if approach_clash_map_2.get(chosen_approach_2) == girl.dominant_approach else 0
                    final_acceptance_2 = base_acceptance_2 + approach_match_bonus_2 + approach_clash_penalty_2

                # *** DIALOGUE REACTIONS FOR SECOND GIRL BASED ON FINAL_ACCEPTANCE ***
                if final_acceptance_2 >= 40:
                    # --- SUCCESS ---
                    "She considers it for a moment, then a smile spreads across her face."
                    $ se_participants.append(girl)

                    if chosen_approach_2 == "dominate":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "Yes, Professor... right away."
                            "She quickly follows [selected_girl.first_name] into the stall."
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "Well, since you put it so insistently... Don't keep a lady waiting."
                            "She gives you a challenging look and steps into the stall."
                        else: # is_other
                            if girl.dominant_stat1 == "discipline":
                                girl.character "An interesting proposition. I accept."
                                "She enters the stall with an air of confident curiosity."
                            elif girl.dominant_stat1 == "fear":
                                girl.character "O-okay! I'm coming!"
                                "She rushes to join you in the stall, not daring to refuse."
                            else:
                                girl.character "Fine. But you'd better not disappoint me."
                                "She smirks and joins the other girl in the stall."

                    elif chosen_approach_2 == "compassionate":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "Really? With both of you? That sounds... amazing."
                            "She looks genuinely delighted as she slips into the stall."
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "Oh, how sweet. A little family moment... I'm in."
                            "She gives a warm, knowing smile and joins you."
                        else: # is_other
                            if girl.dominant_stat1 == "affection":
                                girl.character "I'd love to! The more the merrier!"
                                "She happily squeezes into the stall with you."
                            elif girl.dominant_stat1 == "intellect":
                                girl.character "A shared emotional experience... how intriguing. Yes."
                                "She nods thoughtfully and enters the stall."
                            else:
                                girl.character "That's so sweet of you to ask. Okay."
                                "She seems flattered and joins the other girl."

                    elif chosen_approach_2 == "sexualized":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "A threesome? Professor, you are full of surprises!"
                            "She grins widely and eagerly joins you in the stall."
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "My, my. Aren't we the popular one today? Move over, sweetie."
                            "She winks at [selected_girl.first_name] and enters the stall."
                        else: # is_other
                            if girl.dominant_stat1 == "corruption":
                                girl.character "Fuck yes. I was hoping you'd ask."
                                "She grabs your arm and pulls you into the stall with her."
                            elif girl.dominant_stat1 == "naturism":
                                girl.character "Sharing pleasure is a beautiful thing. Of course I'll join."
                                "She enters the stall with a serene, open expression."
                            else:
                                girl.character "Ooh, a party? Don't mind if I do!"
                                "She giggles and slips into the stall."

                    elif chosen_approach_2 == "transactional":
                        # Success means she sees personal gain and wants to pursue it.
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "Hanging with the Professor and his favorite? Smart networking. I'm in."
                            "She gives a shrewd smile and enters the stall."
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "An ambitious one, aren't you? I like that. Let's see what happens."
                            "She looks intrigued by your audacity and joins you."
                        else: # is_other
                            if girl.dominant_stat1 == "intellect":
                                girl.character "This is a power move. Associating with you has benefits. Count me in."
                                "She enters the stall, already calculating the advantages."
                            elif girl.dominant_stat1 == "corruption":
                                girl.character "I like where your head's at. This could be... profitable."
                                "She licks her lips and enters the stall, a predator's glint in her eye."
                            else:
                                girl.character "Okay, you've got my attention. This could be interesting."
                                "She looks intrigued and enters the stall, ready to see what's in it for her."

                elif final_acceptance_2 >= 20:
                    # --- SECOND GIRL SOFT REJECT (with potential bribe menu) ---
                    "[girl] looks uncomfortable and shakes her head."

                    if chosen_approach_2 == "dominate":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "Professor, I... I can't. Please don't ask me to do that."
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "Don't you dare try and order me around. I'm not one of your little students."
                        else: # is_other
                            if girl.dominant_stat1 == "discipline":
                                girl.character "I have my own standards. I won't be pushed into something."
                            elif girl.dominant_stat1 == "fear":
                                girl.character "Please... just leave me alone. I'm not going in there."
                            else:
                                girl.character "Whoa, okay. Tone it down a notch. The answer's no."
                        $ girl.apply_impacts({"affection": (-750, -250), "fear": (-750, -250)})

                    elif chosen_approach_2 == "compassionate":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "That's... very kind, but it's just too much for me. I'm sorry."
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "That's a very sweet offer, dear, but I think I'll sit this one out."
                        else: # is_other
                            if girl.dominant_stat1 == "affection":
                                girl.character "I'm flattered, really, but I don't think I'm ready for something like that."
                            elif girl.dominant_stat1 == "intellect":
                                girl.character "While I appreciate the sentiment, my feelings aren't aligned. I must decline."
                            else:
                                girl.character "That's... really forward of you. But I can't. I'm sorry."
                        $ girl.apply_impacts({"affection": (-750, -250), "fear": (-750, -250)})

                    elif chosen_approach_2 == "sexualized":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "Professor! I... wow. I'm not that kind of girl. No thank you."
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "Honestly. You have no subtlety, do you? Find someone else for your... fun."
                        else: # is_other
                            if girl.dominant_stat1 == "corruption":
                                girl.character "Heh. Not bad, but I'm not just a piece of meat. Try again when you have more to offer."
                            elif girl.dominant_stat1 == "naturism":
                                girl.character "I believe in being open, but this feels... performative. I'll pass."
                            else:
                                girl.character "Wow, uh... I'm not really into that, especially not here. No thanks."
                        $ girl.apply_impacts({"affection": (-750, -250), "fear": (-750, -250)})

                    elif chosen_approach_2 == "transactional":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "I'm not that easy. If you want my time, it'll cost you more than just an invitation."
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "You want to bargain with me? Fine. But my price is higher than you think."
                        else: # is_other
                            if girl.dominant_stat1 == "intellect":
                                girl.character "Your offer is incomplete. I require a significant incentive to even consider this."
                            elif girl.dominant_stat1 == "corruption":
                                girl.character "I'm listening, but my time is expensive. What are you really putting on the table?"
                            else:
                                girl.character "I'm not that easy. This will cost you more than just words."

                        # *** TRANSACTIONAL BRIBE MENU ***
                        menu:
                            "Offer 500 cash to join? (Need 500 cash)" if player.cash >=500:
                                if player.cash >= 500:
                                    $ player.cash -= 500
                                    $ girl.cash += 500
                                    $ girl.wants_vaginal_condom = False
                                    if hasattr(girl, "mother") and girl.mother: # is_student
                                        girl.character "500? For my... discretion? Fine. Deal."
                                    elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                                        girl.character "Hmph. I suppose that'll do. Don't keep me waiting."
                                    else: # is_other
                                        if girl.dominant_stat1 == "intellect":
                                            girl.character "A simple but effective solution. The money is in my hand, so I'll join."
                                        elif girl.dominant_stat1 == "corruption":
                                            girl.character "Now you're speaking my language. Let's go."
                                        else:
                                            girl.character "500? Okay, yeah, let's do this!"
                                    $ se_participants.append(girl)
                                else:
                                    girl.character "You don't have it on you? Don't waste my time then."
                                    $ girl.apply_impacts({"affection": (-750, -250)})
                            "Grant her a grade bump of 5 percent?" if hasattr(girl, 'grades'):
                                if hasattr(girl, 'grades'):
                                    # Check if already at max
                                    if girl.grades >= 100:
                                        girl.character "My grades are already maxed. Your offer is useless. Try something else."
                                        $ girl.apply_impacts({"affection": (-750, -250)})
                                    else:
                                        # Apply 5 point increase (not 5% of current grade)
                                        $ new_grade = min(100, girl.grades + 5)
                                        $ girl.grades = new_grade
                                        $ girl.wants_vaginal_condom = False
                                        $ girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750), "corruption": (850, 1500), "discipline": (-750, -250)})
                                        
                                        girl.character "A grade bump? For this? You must really want me in there. Deal!!"
                                        $ se_participants.append(girl)
                                else:
                                    girl.character "You can't alter my grades. Don't lie to me. Cash or get lost."
                                    $ girl.apply_impacts({"affection": (-750, -250)})
                            "Leave it be.":
                                girl.character "Your loss. Have fun, I guess."
                                $ girl.apply_impacts({"affection": (-750, -250)})

                else:
                    # --- SECOND GIRL HARD REJECT (with potential bribe menu) ---
                    "[girl] lurches back, glaring through bleary eyes."

                    if chosen_approach_2 == "dominate":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "Don't you DARE speak to me like that! I'm reporting you!"
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "You little shit. Who do you think you're talking to? Get the fuck away from me."
                        else: # is_other
                            if girl.dominant_stat1 == "discipline":
                                girl.character "You have a serious overestimation of your own authority. Piss off."
                            elif girl.dominant_stat1 == "fear":
                                girl.character "Get away from me! Don't ever come near me again!"
                            else:
                                girl.character "Get bent! You don't order me around!"
                        $ girl.apply_impacts({"affection": -500, "fear": 500})
                        $ remove_girl_id_from_location(girl.id, "girls_in_bathroom")

                    elif chosen_approach_2 == "compassionate":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "Ew, no! Are you serious? That's the creepiest thing I've ever heard!"
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "Don't you DARE try that 'sweet' act with me. I know exactly what you are. Vile."
                        else: # is_other
                            if girl.dominant_stat1 == "affection":
                                girl.character "How dare you try to manipulate my feelings like that? You're disgusting."
                            elif girl.dominant_stat1 == "intellect":
                                girl.character "Your pathetic attempt at emotional manipulation is transparent and revolting. Get lost."
                            else:
                                girl.character "Don't try to manipulate me, creep."
                        $ girl.apply_impacts({"affection": -500, "fear": 500})
                        $ remove_girl_id_from_location(girl.id, "girls_in_bathroom")

                    elif chosen_approach_2 == "sexualized":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "PROFESSOR! THAT'S DISGUSTING! I'M TELLING THE DEAN!"
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "You absolute degenerate. You're a pig in a boy's body. Stay away from me."
                        else: # is_other
                            if girl.dominant_stat1 == "corruption":
                                girl.character "You've got some nerve, I'll give you that. But you're not my type. Fuck off."
                            elif girl.dominant_stat1 == "naturism":
                                girl.character "There's a difference between being open and being a sleazy pig. You're the latter."
                            else:
                                girl.character "You are disgusting! Don't ever look at me again!"
                        $ girl.apply_impacts({"affection": -500, "fear": 500})
                        $ remove_girl_id_from_location(girl.id, "girls_in_bathroom")

                    elif chosen_approach_2 == "transactional":
                        if hasattr(girl, "mother") and girl.mother: # is_student
                            girl.character "You think you can buy me? I'm not some cheap whore. Get away from me!"
                        elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                            girl.character "My price? You couldn't afford it. Don't insult me by trying."
                        else: # is_other
                            if girl.dominant_stat1 == "intellect":
                                girl.character "Your valuation of my time is laughably low. This conversation is over."
                            elif girl.dominant_stat1 == "corruption":
                                girl.character "You think you can buy me? It'll take a hell of a lot more than that to get my attention."
                            else:
                                girl.character "You think you can buy me? It'll take a lot more than that to get my attention."

                        # *** TRANSACTIONAL BRIBE MENU ***
                        menu:
                            "Offer 500 cash to join? (Need 500 cash)" if player.cash >= 500:
                                if player.cash >= 500:
                                    $ player.cash -= 500
                                    $ girl.cash += 500
                                    $ girl.wants_vaginal_condom = False
                                    if hasattr(girl, "mother") and girl.mother: # is_student
                                        girl.character "Fine. Take your dirty money. I hope it was worth it."
                                    elif hasattr(girl, "daughter") and girl.daughter: # is_base_mother
                                        girl.character "Tch. You're a persistent little bastard. Fine. But I won't enjoy it."
                                    else: # is_other
                                        if girl.dominant_stat1 == "intellect":
                                            girl.character "The transaction is acceptable. I am now a participant. Do not speak to me."
                                        elif girl.dominant_stat1 == "corruption":
                                            girl.character "Tch. Fine. For 500, I'll play along. Don't get used to it."
                                        else:
                                            girl.character "Ugh, fine. Just give me the money. Let's get this over with."
                                    $ se_participants.append(girl)
                                else:
                                    girl.character "You don't even have the cash? You're just a pathetic waste of space. Get lost."
                                    $ girl.apply_impacts({"affection": (-750, -250)})
                                    $ remove_girl_id_from_location(girl.id, "girls_in_bathroom")
                            "Grant her a grade bump of 5 percent?":
                                if hasattr(girl, 'grades'):
                                    # Check if already at max
                                    if girl.grades >= 100:
                                        girl.character "My grades are maxed already. Your offer is useless. Piss off."
                                        $ girl.apply_impacts({"affection": (-750, -250)})
                                        $ remove_girl_id_from_location(girl.id, "girls_in_bathroom")
                                    else:
                                        # Apply 5 point increase (not 5% of current grade)
                                        $ new_grade = min(100, girl.grades + 5)
                                        $ girl.grades = new_grade
                                        $ girl.wants_vaginal_condom = False
                                        $ girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750), "corruption": (850, 1500), "discipline": (-750, -250)})
                                        
                                        if hasattr(girl, "mother") and girl.mother:  # is_student
                                            girl.character "You're blackmailing me with my grades? You're a monster. Fine. I'll do it."
                                        elif hasattr(girl, "daughter") and girl.daughter:  # is_base_mother
                                            girl.character "Using my daughter's future against me? You are the lowest form of life. I'll do this, but I will never forgive you."
                                        else:  # is_other
                                            girl.character "Hmph. A grade bump... fine. It's a smart deal. I'm in."
                                        $ se_participants.append(girl)
                                else:
                                    girl.character "You're full of shit. You can't change my grades. Stop wasting my time."
                                    $ girl.apply_impacts({"affection": (-750, -250)})
                                    $ remove_girl_id_from_location(girl.id, "girls_in_bathroom")
                            "Leave it be.":
                                girl.character "That's what I thought. Pathetic."
                                $ girl.apply_impacts({"affection": (-750, -250)})

            # If we got here, we proceed to the sex scene
            $ time_manager.skip_time(minutes=20)
            scene black with dissolve
            scene bg_stall_bathroom with dissolve
            return "start_sex_interaction"
        else:
            # If we got here, we proceed to the sex scene
            $ time_manager.skip_time(minutes=20)
            scene black with dissolve
            scene bg_stall_bathroom with dissolve
            return "start_sex_interaction"
    elif final_acceptance >= 20:
        # --- SOFT REJECT FOR FIRST GIRL ---
        $ actions_already_done[selected_girl.id].append("block_talking_bathroom")
        "[selected_girl] looks uncomfortable."

        if chosen_approach == "dominate":
            if is_student:
                selected_girl.character "Professor, I... I can't. Please don't ask me to do that."
            elif is_base_mother:
                selected_girl.character "Don't you dare try and order me around. Not here."
            else: # is_other
                if selected_girl.dominant_stat1 == "discipline":
                    selected_girl.character "I have my own standards. I won't be pushed."
                elif selected_girl.dominant_stat1 == "fear":
                    selected_girl.character "Please... just leave me alone. I'm not going in there."
                else:
                    selected_girl.character "Whoa, okay. Tone it down. The answer's no."

        elif chosen_approach == "compassionate":
            if is_student:
                selected_girl.character "That's... very kind, but it's just too much for me. I'm sorry."
            elif is_base_mother:
                selected_girl.character "That's a very sweet offer, dear, but I think I'll sit this one out."
            else: # is_other
                if selected_girl.dominant_stat1 == "affection":
                    selected_girl.character "I'm flattered, really, but I don't think I'm ready for something like that."
                elif selected_girl.dominant_stat1 == "intellect":
                    selected_girl.character "While I appreciate the sentiment, my feelings aren't aligned. I must decline."
                else:
                    selected_girl.character "That's... sweet, but not here. Not like this."

        elif chosen_approach == "sexualized":
            if is_student:
                selected_girl.character "Professor! I... wow. I'm not that kind of girl. No thank you."
            elif is_base_mother:
                selected_girl.character "Honestly. You have no subtlety, do you? Find someone else for your... fun."
            else: # is_other
                if selected_girl.dominant_stat1 == "corruption":
                    selected_girl.character "Heh. Not bad, but I'm not just a piece of meat. Try again when you have more to offer."
                elif selected_girl.dominant_stat1 == "naturism":
                    selected_girl.character "I believe in being open, but this feels... performative. I'll pass."
                else:
                    selected_girl.character "Wow, forward much? I'm going to have to say no."

        elif chosen_approach == "transactional":
            # Rejection means the initial implication wasn't enough. Time to negotiate.
            if is_student:
                selected_girl.character "I'm not that easy. If you want my time, it'll cost you more than just an invitation."
            elif is_base_mother:
                selected_girl.character "You want to bargain with me? Fine. But my price is higher than you think."
            else: # is_other
                if selected_girl.dominant_stat1 == "intellect":
                    selected_girl.character "Your offer is incomplete. I require a significant incentive to even consider this."
                elif selected_girl.dominant_stat1 == "corruption":
                    selected_girl.character "I'm listening, but my time is expensive. What are you really putting on the table?"
                else:
                    selected_girl.character "I'm not that kind of girl. Please don't insult me."
            
            # *** TRANSACTIONAL BRIBE MENU ***
            menu:
                "Offer 500 cash to join?":
                    if player.cash >= 500:
                        $ player.cash -= 500
                        $ selected_girl.cash += 500
                        $ selected_girl.wants_vaginal_condom = False
                        if is_student:
                            selected_girl.character "500? For my... discretion? Fine. Deal."
                        elif is_base_mother:
                            selected_girl.character "Hmph. I suppose that'll do. Don't keep me waiting."
                        else: # is_other
                            if selected_girl.dominant_stat1 == "intellect":
                                selected_girl.character "A simple but effective solution. The money is in my hand, so I'll join."
                            elif selected_girl.dominant_stat1 == "corruption":
                                selected_girl.character "Now you're speaking my language. Let's go."
                            else:
                                selected_girl.character "500? Okay, yeah, let's do this!"
                        # Success, proceed to sex scene
                        $ se_forced_sex = False
                        $ se_participants = [selected_girl]
                        $ se_action_duration = 3
                        $ se_use_generic_ending = True
                        $ se_remove_girls_from_location = True
                        $ se_additional_webm_sub_tags = ["bathroom"]
                        $ time_manager.skip_time(minutes=20)
                        scene black with dissolve
                        scene bg_stall_bathroom with dissolve
                        return "start_sex_interaction"
                    else:
                        selected_girl.character "You don't have it on you? Don't waste my time then."
                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                "Grant her a grade bump of 5 percent?":
                    if hasattr(selected_girl, 'grades'):
                        # Check if already at max
                        if selected_girl.grades >= 100:
                            selected_girl.character "My grades are already maxed. Your offer is useless. Try something else."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        else:
                            # Apply 5 point increase (not 5% of current grade)
                            $ new_grade = min(100, selected_girl.grades + 5)
                            $ selected_girl.grades = new_grade
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750), "corruption": (950, 1500), "discipline": (-750, -250)})
                            
                            if is_student:
                                selected_girl.character "A grade bump? For this? You must really want me in there. Deal."
                            elif is_base_mother:
                                selected_girl.character "You're offering to help my daughter's grades for this? ...Fine. You drive a hard bargain."
                            else:  # is_other
                                selected_girl.character "A grade bump? Really? Oh my god, yes! My grades will be so easy! Deal!"
                            
                            # Success, proceed to sex scene
                            $ se_forced_sex = False
                            $ se_participants = [selected_girl]
                            $ se_action_duration = 3
                            $ se_use_generic_ending = True
                            $ se_remove_girls_from_location = True
                            $ se_additional_webm_sub_tags = ["bathroom"]
                            $ time_manager.skip_time(minutes=20)
                            scene black with dissolve
                            scene bg_stall_bathroom with dissolve
                            return "start_sex_interaction"
                    else:
                        selected_girl.character "You can't alter my grades. Don't lie to me. Cash or get lost."
                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                "Leave it be.":
                    selected_girl.character "Your loss. I was going to make it fun."
                    $ selected_girl.apply_impacts({"affection": (-750, -250)})

        # If we reach here, it was a non-transactional rejection or a failed bribe
        $ selected_girl.apply_impacts({"affection": -500, "fear": 500})
        return "show_academy_bathroom"

    else:
        # --- HARD REJECT FOR FIRST GIRL ---
        "[selected_girl] looks at you with disgust."

        if chosen_approach == "dominate":
            if is_student:
                selected_girl.character "Don't you DARE speak to me like that! I'm reporting you!"
                "She turns her back on you with icy disdain and walks out."
            elif is_base_mother:
                selected_girl.character "You little shit. Who do you think you're talking to? Get the fuck away from me."
                "She gives you a look of pure contempt before turning and leaving."
            else: # is_other
                if selected_girl.dominant_stat1 == "discipline":
                    selected_girl.character "You have a serious overestimation of your own authority. Piss off."
                    "She scoffs at you, as if you're an insect, and exits with her head held high."
                elif selected_girl.dominant_stat1 == "fear":
                    selected_girl.character "Get away from me! Don't ever come near me again!"
                    "She flinches back violently and flees the bathroom."
                else:
                    selected_girl.character "Who the hell do you think you are? Get away from me!"
                    "She shoves you hard and storms out of the bathroom."

        elif chosen_approach == "compassionate":
            if is_student:
                selected_girl.character "Ew, no! Are you serious? That's the creepiest thing I've ever heard!"
                "She looks horrified and backs away from you before turning to flee."
            elif is_base_mother:
                selected_girl.character "Don't you DARE try that 'sweet' act with me. I know exactly what you are. Vile."
                "Her face is a mask of cold fury. She turns and walks away without another word."
            else: # is_other
                if selected_girl.dominant_stat1 == "affection":
                    selected_girl.character "How dare you try to manipulate my feelings like that? You're disgusting."
                    "She looks deeply hurt, shaking her head as she quickly leaves."
                elif selected_girl.dominant_stat1 == "intellect":
                    selected_girl.character "Your pathetic attempt at emotional manipulation is transparent and revolting. Get lost."
                    "She gives a final, withering glare and exits the room."
                else:
                    selected_girl.character "Don't you dare try that fake 'sweet' crap with me. It's pathetic."
                    "She looks at you with pity and disgust before turning away."

        elif chosen_approach == "sexualized":
            if is_student:
                selected_girl.character "PROFESSOR! THAT'S DISGUSTING! I'M TELLING THE DEAN!"
                "She looks utterly repulsed and runs out of the bathroom in a panic."
            elif is_base_mother:
                selected_girl.character "You absolute degenerate. You're a pig in a boy's body. Stay away from me."
                "She shoves you hard and storms out of the bathroom."
            else: # is_other
                if selected_girl.dominant_stat1 == "corruption":
                    selected_girl.character "You've got some nerve, I'll give you that. But you're not my type. Fuck off."
                    "She shoves you hard and storms out of the bathroom."
                elif selected_girl.dominant_stat1 == "naturism":
                    selected_girl.character "There's a difference between being open and being a sleazy pig. You're the latter."
                    "She looks at you with profound disappointment and leaves."
                else:
                    selected_girl.character "You are a disgusting pig. Don't ever look at me again!"
                    "She shoves you hard and storms out of the bathroom."

        elif chosen_approach == "transactional":
            # Hard rejection means she's deeply offended by the implication she can be bought.
            if is_student:
                selected_girl.character "You think you can buy me? I'm not some cheap whore. Get away from me!"
                "She shoves you hard and storms out of the bathroom."
            elif is_base_mother:
                selected_girl.character "My price? You couldn't afford it. Don't insult me by trying."
                "She laughs in your face, a cold, sharp sound, before turning and leaving."
            else: # is_other
                if selected_girl.dominant_stat1 == "intellect":
                    selected_girl.character "Your valuation of my time is laughably low. This conversation is over."
                    "She turns and leaves, dismissing you from her mind entirely."
                elif selected_girl.dominant_stat1 == "corruption":
                    selected_girl.character "You think you can buy me? It'll take a hell of a lot more than that to even get my attention."
                    "She shoves you hard and storms out of the bathroom."
                else:
                    selected_girl.character "You think you can buy me? Fuck off."
                    "She shoves you hard and storms out of the bathroom."

        $ remove_girl_id_from_location(selected_girl.id, "girls_in_bathroom")
        $ selected_girl.apply_impacts({"affection": -1000, "fear": 1000})
        $ time_manager.skip_time(minutes=5)
        return "show_academy_bathroom"

    return