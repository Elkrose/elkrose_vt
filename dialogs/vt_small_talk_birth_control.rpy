#SPECIFIC CHERRY DIALOGS
# to catch mothers if not hasattr(self, "daughter"):

label small_talk_birth_control:
    $ time_manager.skip_time(minutes=5)
    
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
    
    # DYNAMIC CHILD REFERENCE (for consistent dialogue)
    $ child_reference = ""
    if is_base_mother and (total_kids - kids_with_player - kids_with_others) > 0:
        $ child_reference = "my daughter"
    elif kids_with_player > 0:
        $ child_reference = "your child" if kids_with_player == 1 else f"our {total_kids} children"
    elif kids_with_others > 0:
        $ child_reference = "that child" if kids_with_others == 1 else f"my {total_kids} children"
    else:
        $ child_reference = "my child" if is_currently_a_mother else ""
    
    # BIRTH CONTROL STATE TRACKING
    $ currently_on_birth_control = selected_girl.birth_control
    $ bc_status_known = selected_girl.bc_status_known
    
    # PERSONALITY CLUSTERING
    $ norm_naturism = selected_girl.naturism / 10
    $ norm_corruption = selected_girl.corruption / 10
    $ norm_discipline = selected_girl.discipline / 10
    $ norm_fear = selected_girl.fear / 10
    $ norm_baby_desire = selected_girl.baby_desire / 10 if hasattr(selected_girl, "baby_desire") else 5.0

    $ natural_leaning = norm_naturism - norm_discipline
    $ risk_taking = norm_corruption - norm_fear
    $ family_leaning = norm_baby_desire - norm_fear
    
    # NORMALIZE PLAYER STATS TO 0-10 SCALE FOR CLUSTERING
    $ norm_compassion = (player.compassion + 10) / 2  # -10 to 10 becomes 0 to 10
    $ norm_intellect = selected_girl.intellect / 10  # 0 to 100 becomes 0 to 10
    $ norm_control = (player.control + 10) / 2  # -10 to 10 becomes 0 to 10
    $ norm_reputation = player.reputation / 10  # 0 to 100 becomes 0 to 10
    $ norm_lust = (player.lust + 10) / 2  # -10 to 10 becomes 0 to 10
    $ norm_arousal = player.arousal / 12  # 0 to 120 becomes 0 to 10
    
    # CLUSTER PLAYER STATS (0-10 scale)
    $ empathy = (norm_compassion + norm_intellect) / 2
    $ control = (norm_control + norm_reputation) / 2
    $ lust = (norm_lust + norm_arousal) / 2
    
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

        player_stats = {
            "control": player.control,
            "greed": player.greed,
            "lust": player.lust,
            "compassion": player.compassion
        }

        # Get the two highest stats for the girl (the ones that will drive her reaction)
        sorted_girl_stats = sorted(girl_stats.items(), key=lambda item: item[1], reverse=True)
        dominant_girl_stat1, dominant_girl_value1 = sorted_girl_stats[0]
        dominant_girl_stat2, dominant_girl_value2 = sorted_girl_stats[1]

        # Get the highest stat for the player (the one that will drive his reaction)
        dominant_player_stat = max(player_stats, key=player_stats.get)
        dominant_player_value = player_stats[dominant_player_stat]
        
        # SET REACTION BASED ON DOMINANT STATS + STRENGTH
        if dominant_girl_value1 > 60 and dominant_girl_value2 > 60:
            if dominant_girl_stat1 == "corruption" and dominant_girl_stat2 == "fear":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "submissive"  # "You're in charge, Master"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "seductive"  # "I'm yours to command"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "manipulative"  # "What's in it for me?"
                else:  # compassion
                    selected_girl.initial_reaction = "devoted"  # "I'll do anything for you"
            elif dominant_girl_stat1 == "affection" and dominant_girl_stat2 == "intellect":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "admiring"  # "You're so strong and smart"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "infatuated"  # "I can't stop thinking about you"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "generous"  # "I want to give you everything"
                else:  # compassion
                    selected_girl.initial_reaction = "loving"  # "I feel so connected to you"
            # Add more combinations as needed
        elif dominant_girl_value1 > 60 and dominant_girl_value2 <= 60:
            if dominant_girl_stat1 == "corruption":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "submissive"  # "You're in charge, Master"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "seductive"  # "I'm yours to command"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "manipulative"  # "What's in it for me?"
                else:  # compassion
                    selected_girl.initial_reaction = "devoted"  # "I'll do anything for you"
            elif dominant_girl_stat1 == "affection":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "admiring"  # "You're so strong"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "infatuated"  # "I can't stop thinking about you"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "generous"  # "I want to give you everything"
                else:  # compassion
                    selected_girl.initial_reaction = "loving"  # "I feel so connected to you"
            # Add more combinations as needed
        elif dominant_girl_value1 <= 60 and dominant_girl_value2 > 60:
            if dominant_girl_stat2 == "corruption":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "submissive"  # "You're in charge, Master"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "seductive"  # "I'm yours to command"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "manipulative"  # "What's in it for me?"
                else:  # compassion
                    selected_girl.initial_reaction = "devoted"  # "I'll do anything for you"
            elif dominant_girl_stat2 == "affection":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "admiring"  # "You're so strong"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "infatuated"  # "I can't stop thinking about you"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "generous"  # "I want to give you everything"
                else:  # compassion
                    selected_girl.initial_reaction = "loving"  # "I feel so connected to you"
            # Add more combinations as needed
        else:
            selected_girl.initial_reaction = "neutral"  # "Just another student"

    
    if not hasattr(selected_girl, "previous_birth_control_reaction"):
        $ selected_girl.previous_birth_control_reaction = "neutral"
    if not hasattr(selected_girl, "birth_control_discussion_level"):
        $ selected_girl.pregnancy_discussion_level = 0
    if not hasattr(selected_girl, "birth_control_followup"):
        $ selected_girl.birth_control_followup = 0
    
    # TRACK CONVERSATION HISTORY
    $ has_discussed_birth_control_before = getattr(selected_girl, "has_discussed_birth_control_before", False)
    $ previous_birth_control_reaction = getattr(selected_girl, "previous_birth_control_reaction", "neutral")
    $ birth_control_discussion_level = getattr(selected_girl, "birth_control_discussion_level", 1)
    
    # CHECK FOR ACTIVE FOLLOW-UP 
    # If we have a scheduled follow-up that's ready to happen
    if hasattr(selected_girl, "has_birth_control_followup") and selected_girl.has_birth_control_followup and has_discussed_birth_control_before:
        # Reset the flag so it doesn't keep appearing
        $ selected_girl.has_birth_control_followup = False
        
        # Update tracking variables for the follow-up
        $ selected_girl.birth_control_discussion_level = min(3, birth_control_discussion_level + 1)
        
        # Show follow-up specific dialogue
        "[selected_girl]'s eyes light up as you approach her, clearly remembering your previous conversation about birth control."
        
        # Call the actual follow-up dialogue
        call vt_small_talk_birth_control_followup from _call_vt_small_talk_birth_control_followup
        
        # Exit after follow-up completes
        return
    
    # INITIAL GREETING - CHARACTER-APPROPRIATE WITH MEMORY
    "You approach [selected_girl] to discuss birth control preferences."
    
    if has_discussed_birth_control_before:
        if previous_birth_control_reaction == "positive":
            selected_girl.character "You wanted to talk more about birth control? I've been thinking about what we discussed..."
        elif previous_birth_control_reaction == "negative":
            selected_girl.character "Back to this topic again? I thought we already covered everything I'm comfortable sharing..."
        else:
            selected_girl.character "You wanted to talk about birth control again? I'm listening..."
    else:
        $ selected_girl.has_discussed_birth_control_before = True
    # PHASE 1: REVEAL BIRTH CONTROL STATUS - USING INITIAL_REACTION SYSTEM
    if not bc_status_known:
        # Response based on initial_reaction
        if selected_girl.initial_reaction == "loving":
            if currently_on_birth_control:
                if is_currently_a_mother:
                    selected_girl.character "I feel so connected to you, but I need to be careful. I'm on birth control - with [child_reference] to think about, I can't risk another pregnancy right now."
                else:
                    selected_girl.character "I feel so connected to you, but I need to be careful. I'm on birth control - I want to enjoy our connection without worry."
            else:
                if is_currently_a_mother:
                    selected_girl.character "I feel so connected to you. I'm not on birth control - I'm already a mother, so another baby wouldn't be the end of the world."
                else:
                    selected_girl.character "I feel so connected to you. I'm not on birth control - I want to experience everything naturally with you."
                    
        elif selected_girl.initial_reaction == "submissive":
            if currently_on_birth_control:
                if is_currently_a_mother:
                    selected_girl.character "You're in charge, Master. I'm on birth control because I must protect my existing child - but if you want me to stop, I will."
                else:
                    selected_girl.character "You're in charge, Master. I'm on birth control - but if you want me to stop, I will."
            else:
                if is_currently_a_mother:
                    selected_girl.character "You're in charge, Master. I'm not on birth control - my body already knows how to handle children, and it's yours to command."
                else:
                    selected_girl.character "You're in charge, Master. I'm not on birth control - my body is yours to command."
                    
        elif selected_girl.initial_reaction == "seductive":
            if currently_on_birth_control:
                if is_currently_a_mother:
                    selected_girl.character "The way you look at me is so hot... but as a mother, I need to be careful. I'm on birth control - watching you cum inside me while I'm protected is its own kind of sexy."
                else:
                    selected_girl.character "The way you look at me is so hot... but I'm on birth control - watching you cum inside me while I'm protected can be its own kind of sexy."
            else:
                if is_currently_a_mother:
                    selected_girl.character "The way you look at me is so hot. I'm not on birth control - I want to feel your raw cock pumping into my pussy, no barriers - motherhood hasn't dulled my desires."
                else:
                    selected_girl.character "The way you look at me is so hot. I'm not on birth control - I want to feel your raw cock pumping into my pussy, no barriers."
                    
        elif selected_girl.initial_reaction == "manipulative":
            if currently_on_birth_control:
                if is_currently_a_mother:
                    selected_girl.character "What's in it for me? I'm on birth control because I'm a mother with responsibilities, Professor. Letting you cum in my protected pussy costs extra - I have childcare to pay for."
                else:
                    selected_girl.character "What's in it for me? I'm on birth control, Professor. Letting you cum in my protected pussy costs extra... unless you make it worth my time."
            else:
                if is_currently_a_mother:
                    selected_girl.character "What's in it for me? Unprotected pussy from a single mother? That's premium pricing, Professor - I'm supporting a household here."
                else:
                    selected_girl.character "What's in it for me? Unprotected pussy? That's premium pricing, Professor."
                    
        elif selected_girl.initial_reaction == "devoted":
            if currently_on_birth_control:
                if is_currently_a_mother:
                    selected_girl.character "I'll do anything for you, including being on birth control if it pleases you - my child's wellbeing comes first though."
                else:
                    selected_girl.character "I'll do anything for you, including being on birth control if it pleases you."
            else:
                if is_currently_a_mother:
                    selected_girl.character "I'll do anything for you, including not being on birth control if it pleases you - my body is yours even with my maternal duties."
                else:
                    selected_girl.character "I'll do anything for you, including not being on birth control if it pleases you."
                    
        elif selected_girl.initial_reaction == "admiring":
            if currently_on_birth_control:
                if is_currently_a_mother:
                    selected_girl.character "You're so strong. I'm on birth control because a mother needs to be practical about these things - I trust your judgment."
                else:
                    selected_girl.character "You're so strong. I'm on birth control because I trust your judgment about these things."
            else:
                if is_currently_a_mother:
                    selected_girl.character "You're so strong. I'm not on birth control because I trust your decision to claim my body - even with my child at home."
                else:
                    selected_girl.character "You're so strong. I'm not on birth control because I trust your decision to claim my body."
                    
        elif selected_girl.initial_reaction == "infatuated":
            if currently_on_birth_control:
                if is_currently_a_mother:
                    selected_girl.character "I can't stop thinking about you... but I need to be on birth control - I can't get pregnant again while raising my child."
                else:
                    selected_girl.character "I can't stop thinking about you... but I need to be on birth control - I want to be ready for you always."
            else:
                if is_currently_a_mother:
                    selected_girl.character "I can't stop thinking about you. I'm not on birth control - I dream about feeling your bare cock pumping into my pussy, maybe giving my child a sibling someday."
                else:
                    selected_girl.character "I can't stop thinking about you. I'm not on birth control - I dream about feeling your bare cock pumping into my pussy."
                    
        elif selected_girl.initial_reaction == "generous":
            if currently_on_birth_control:
                if is_currently_a_mother:
                    selected_girl.character "I want to give you everything, but I need to be on birth control - I must be responsible for my child's sake."
                else:
                    selected_girl.character "I want to give you everything, but I need to be on birth control - I want to be ready for you always."
            else:
                if is_currently_a_mother:
                    selected_girl.character "I want to give you everything. I'm not on birth control - my pussy is yours whenever you want it - motherhood hasn't made me selfish."
                else:
                    selected_girl.character "I want to give you everything. I'm not on birth control - my pussy is yours whenever you want it."
                    
        elif selected_girl.initial_reaction == "neutral":
            if currently_on_birth_control:
                if is_currently_a_mother:
                    selected_girl.character "As a mother, I need to be careful. I'm on birth control - I can't risk another mouth to feed right now."
                else:
                    selected_girl.character "Just another student being responsible. I'm on birth control."
            else:
                if is_currently_a_mother:
                    selected_girl.character "I'm already a mother, so what's one more risk? I'm not on birth control."
                else:
                    selected_girl.character "Just another student taking risks. I'm not on birth control."
        
        $ selected_girl.bc_status_known = True
        $ selected_girl.previous_birth_control_reaction = "neutral"
        $ selected_girl.apply_impacts({"affection": 25})
            
    # PHASE 2: STRATEGIC DIALOGUE OPTIONS (MEANINGFUL CHOICES)
    menu:
        # RESPONSIBLE/HEALTH APPROACH (INCREASES DISCIPLINE)
        "I'm concerned about your health and responsible reproductive choices." if norm_discipline > 5:
            $ selected_girl.apply_impacts({"discipline": 75, "fear": 50})
            
            # Response based on initial_reaction
            if selected_girl.initial_reaction == "loving":
                if is_currently_a_mother:
                    selected_girl.character "You're absolutely right, Professor. With [child_reference] to think about, I need to be more responsible about birth control."
                else:
                    selected_girl.character "You're absolutely right, Professor. I need to be more responsible about birth control for us."
            elif selected_girl.initial_reaction == "submissive":
                if is_currently_a_mother:
                    selected_girl.character "You're in charge, Master. If you want me to be responsible about birth control for [child_reference]'s sake, I will."
                else:
                    selected_girl.character "You're in charge, Master. If you want me to be responsible about birth control, I will."
            elif selected_girl.initial_reaction == "seductive":
                if is_currently_a_mother:
                    selected_girl.character "Mmm... a responsible Professor who cares about my health? That's unexpectedly hot. Fine, I'll be more careful - for [child_reference]."
                else:
                    selected_girl.character "Mmm... a responsible Professor who cares about my health? That's unexpectedly hot. Fine, I'll be more careful."
            elif selected_girl.initial_reaction == "manipulative":
                if is_currently_a_mother:
                    selected_girl.character "What's in it for me? Being responsible about birth control with [child_reference] to support? That costs extra, Professor."
                else:
                    selected_girl.character "What's in it for me? Being responsible about birth control? That costs extra, Professor."
            elif selected_girl.initial_reaction == "devoted":
                if is_currently_a_mother:
                    selected_girl.character "Anything for you. I'll be responsible about birth control for [child_reference]'s sake and yours."
                else:
                    selected_girl.character "Anything for you. I'll be responsible about birth control for your sake."
            elif selected_girl.initial_reaction == "admiring":
                if is_currently_a_mother:
                    selected_girl.character "You're so wise to be concerned about my health and [child_reference]'s future. I admire your responsibility."
                else:
                    selected_girl.character "You're so wise to be concerned about my health. I admire your responsibility."
            elif selected_girl.initial_reaction == "infatuated":
                if is_currently_a_mother:
                    selected_girl.character "You care about my health and [child_reference]? I can't stop thinking about you! Fine, I'll be more responsible."
                else:
                    selected_girl.character "You care about my health? I can't stop thinking about you! Fine, I'll be more responsible."
            elif selected_girl.initial_reaction == "generous":
                if is_currently_a_mother:
                    selected_girl.character "I want to give you everything, including being responsible about birth control for [child_reference]'s sake."
                else:
                    selected_girl.character "I want to give you everything, including being responsible about birth control."
            else:
                if is_currently_a_mother:
                    selected_girl.character "You're right, Professor. With [child_reference], I need to be more responsible."
                else:
                    selected_girl.character "You're right, Professor. I should be more responsible."
            
            $ selected_girl.previous_birth_control_reaction = "serious"
            
            menu:
                # "Should you continue birth control?" if currently_on_birth_control:
                    # $ selected_girl.bc_status_known = True
                    # if selected_girl.initial_reaction == "manipulative":
                        # if is_currently_a_mother:
                            # selected_girl.character "I'm already on birth control, Professor. But continuing it for [child_reference]'s sake? That's going to cost you extra monthly."
                        # else:
                            # selected_girl.character "I'm already on birth control, Professor. But continuing it? That's going to cost you extra monthly."
                        
                        # menu:
                            # "Offer 200 per month for birth control expenses?":
                                # if player.cash >= 200:
                                    # $ player.cash -= 200
                                    # $ selected_girl.apply_impacts({"corruption": 30, "affection": 10})
                                    # if is_currently_a_mother:
                                        # selected_girl.character "200 a month? Fine, I'll continue birth control for [child_reference]'s sake - but don't be late with payments."
                                    # else:
                                        # selected_girl.character "200 a month? Fine, I'll continue birth control - but don't be late with payments."
                                # else:
                                    # selected_girl.character "You think I can afford birth control on my own with [child_reference]? Come back when you can actually pay."
                                    # $ selected_girl.apply_impacts({"affection": -25})
                            # "Promise to give her better grades" if is_student:
                                # if hasattr(selected_girl, "grades"):
                                    # $ selected_girl.grades = min(100, selected_girl.grades + 10)
                                    # $ selected_girl.apply_impacts({"corruption": 40, "discipline": -20})
                                    # if is_currently_a_mother:
                                        # selected_girl.character "Better grades for birth control? Deal, but only if it helps with [child_reference]'s future too."
                                    # else:
                                        # selected_girl.character "Better grades for birth control? Deal, but this better not be a one-time arrangement."
                                # else:
                                    # selected_girl.character "I'm not even your student. Try cash next time."
                                    # $ selected_girl.apply_impacts({"affection": -15})
                            # "Forget it then.":
                                # if is_currently_a_mother:
                                    # selected_girl.character "Fine. I'll handle birth control myself for [child_reference]'s sake. Don't come crying when I'm too tired for sex."
                                # else:
                                    # selected_girl.character "Fine. I'll handle birth control myself. Don't come crying when I'm too busy for sex."
                                # $ selected_girl.apply_impacts({"affection": -20})
                    # else:
                        # selected_girl.character "I'm already on birth control, Professor. It's working well for me."
                
                    
                "Would you consider starting birth control?" if not currently_on_birth_control:
                    $ selected_girl.bc_status_known = True
                    if selected_girl.initial_reaction in ["loving", "devoted", "generous"]:
                        $ selected_girl.birth_control = True
                        $ selected_girl.previous_birth_control_reaction = "serious"
                        if is_currently_a_mother:
                            selected_girl.character "You've convinced me... I'll start birth control for health and for [child_reference]'s sake."
                        else:
                            selected_girl.character "You've convinced me... I'll start birth control for health and for our future."
                    elif selected_girl.initial_reaction == "manipulative":
                        if is_currently_a_mother:
                            selected_girl.character "Starting birth control with [child_reference] to care for? That's a significant expense, Professor. What's your offer?"
                        else:
                            selected_girl.character "Starting birth control? That's a significant expense, Professor. What's your offer?"
                        
                        menu:
                            "Offer 500 startup cost for birth control?":
                                if player.cash >= 500:
                                    $ player.cash -= 500
                                    $ selected_girl.cash += 500
                                    $ selected_girl.birth_control = True
                                    $ selected_girl.apply_impacts({"corruption": 40, "affection": 15})
                                    if is_currently_a_mother:
                                        selected_girl.character "500 upfront? Fine, I'll start birth control for [child_reference]'s sake - but I expect monthly support too."
                                    else:
                                        selected_girl.character "500 upfront? Fine, I'll start birth control - but I expect monthly support too."
                                else:
                                    selected_girl.character "You think birth control is cheap? Come back when you're serious about supporting me."
                                    $ selected_girl.apply_impacts({"affection": -30})
                            "Promise to cover all medical expenses":
                                $ selected_girl.birth_control = True
                                $ selected_girl.apply_impacts({"corruption": 50, "discipline": -25})
                                if is_currently_a_mother:
                                    selected_girl.character "Medical coverage? Now that's a negotiation. Fine, I'll start birth control for [child_reference]'s sake - but I want this in writing."
                                else:
                                    selected_girl.character "Medical coverage? Now that's a negotiation. Fine, I'll start birth control - but I want this in writing."
                            "Never mind then.":
                                if is_currently_a_mother:
                                    selected_girl.character "Smart move. Birth control is expensive with [child_reference] to support."
                                else:
                                    selected_girl.character "Smart move. Birth control isn't cheap."
                                $ selected_girl.apply_impacts({"affection": -10})
                    else:
                        selected_girl.character "I'm not ready to commit to birth control right now, Professor."
                
                
                # "Should you continue birth control with [child_reference]?" if currently_on_birth_control and is_currently_a_mother:
                    # $ selected_girl.bc_status_known = True
                    # $ persuasion_score = 35 + (norm_discipline * 4)
                    # if persuasion_score > 55:
                        # $ selected_girl.birth_control = True
                        # $ selected_girl.previous_birth_control_reaction = "serious"
                        # selected_girl.character "You're right... with [child_reference], I should continue birth control for proper spacing."
                    # else:
                        # selected_girl.character "I'm not comfortable with that suggestion, Professor."
                
                "Would you consider stopping birth control?" if currently_on_birth_control:
                    $ selected_girl.bc_status_known = True
                    if selected_girl.initial_reaction in ["seductive", "infatuated"]:
                        $ selected_girl.birth_control = False
                        $ selected_girl.previous_birth_control_reaction = "excited"
                        if is_currently_a_mother:
                            selected_girl.character "Mmm... stop birth control? I'd love to feel you cum in my bare pussy and give [child_reference] a sibling!"
                        else:
                            selected_girl.character "Mmm... stop birth control? I'd love to feel you cum in my bare pussy and have your baby!"
                    elif selected_girl.initial_reaction == "manipulative":
                        if is_currently_a_mother:
                            selected_girl.character "Stop birth control with [child_reference] to support? That's pregnancy we're talking about - premium pricing, Professor. What's your offer?"
                        else:
                            selected_girl.character "Stop birth control? That's pregnancy we're talking about - premium pricing, Professor. What's your offer?"
                        
                        menu:
                            "Offer 2000 for pregnancy expenses?":
                                if player.cash >= 2000:
                                    $ player.cash -= 2000
                                    $ selected_girl.cash += 2000
                                    $ selected_girl.birth_control = False
                                    $ selected_girl.apply_impacts({"baby_desire": 60, "corruption": 50})
                                    if is_currently_a_mother:
                                        selected_girl.character "2000 for another baby with [child_reference]? Fine, I'll stop birth control - but I expect significant child support."
                                    else:
                                        selected_girl.character "2000 for your baby? Fine, I'll stop birth control - but I expect significant child support."
                                else:
                                    selected_girl.character "You think that's enough for raising a baby? Don't insult me."
                                    $ selected_girl.apply_impacts({"affection": -35})
                            # "Promise marriage and full support":
                                # $ selected_girl.birth_control = False
                                # $ selected_girl.apply_impacts({"baby_desire": 80, "affection": 40, "corruption": 30})
                                # if is_currently_a_mother:
                                    # selected_girl.character "Marriage and full support for me and [child_reference]? Now THAT's what I'm talking about. Fine, let's make a baby!"
                                # else:
                                    # selected_girl.character "Marriage and full support? Now THAT's what I'm talking about. Fine, let's make a baby!"
                            "I'll think about it.":
                                if is_currently_a_mother:
                                    selected_girl.character "You think about it while I consider raising another child with [child_reference]. Let me know when you're serious."
                                else:
                                    selected_girl.character "You think about it while I consider raising your child. Let me know when you're serious."
                                $ selected_girl.apply_impacts({"affection": -15})
                    else:
                        selected_girl.character "I'm not comfortable with that suggestion, Professor."
        
                
                # "Would you consider stopping birth control in the future?" if not currently_on_birth_control and selected_girl.baby_desire > 70:
                    # $ selected_girl.bc_status_known = True
                    # $ persuasion_score = 35 + (family_leaning * 4)
                    # if persuasion_score > 55:
                        # $ selected_girl.previous_birth_control_reaction = "excited"
                        # if child_reference:
                            # selected_girl.character "I've actually been thinking about that. I want to experience pregnancy with [child_reference]."
                        # else:
                            # selected_girl.character "I've actually been thinking about that. I want to experience pregnancy with you."
                    # else:
                        # selected_girl.character "I'm not comfortable with that suggestion, Professor."
        
        # NATURAL CYCLE APPROACH (INCREASES NATURISM)
        "I think your body would feel better functioning naturally without artificial hormones." if natural_leaning > 2:
            $ selected_girl.apply_impacts({"naturism": 75, "affection": 50})
            
            # Response based on initial_reaction
            if selected_girl.initial_reaction == "loving":
                if is_currently_a_mother:
                    selected_girl.character "You make a compelling argument... I've always believed in natural bodily functions, even with [child_reference] to consider."
                else:
                    selected_girl.character "You make a compelling argument... I've always believed in natural bodily functions between us."
            elif selected_girl.initial_reaction == "submissive":
                if is_currently_a_mother:
                    selected_girl.character "If that's what you want, Master... I'll experience my natural cycle for you, even with [child_reference]."
                else:
                    selected_girl.character "If that's what you want, Master... I'll experience my natural cycle for you."
            elif selected_girl.initial_reaction == "seductive":
                if is_currently_a_mother:
                    selected_girl.character "Mmm... natural cycle? That means more chances for you to cum in my bare pussy... even with [child_reference] around. I like that."
                else:
                    selected_girl.character "Mmm... natural cycle? That means more chances for you to cum in my bare pussy. I like that."
            elif selected_girl.initial_reaction == "manipulative":
                if is_currently_a_mother:
                    selected_girl.character "Natural cycle with [child_reference] to support? That's risky business, Professor. What's in it for me?"
                else:
                    selected_girl.character "Natural cycle? That's risky business, Professor. What's in it for me?"
            elif selected_girl.initial_reaction == "devoted":
                if is_currently_a_mother:
                    selected_girl.character "Anything for you. I'll experience my natural cycle for you, even with [child_reference] to care for."
                else:
                    selected_girl.character "Anything for you. I'll experience my natural cycle for you."
            elif selected_girl.initial_reaction == "admiring":
                if is_currently_a_mother:
                    selected_girl.character "You're so wise about natural living. I admire that, even with [child_reference] to consider."
                else:
                    selected_girl.character "You're so wise about natural living. I admire that."
            elif selected_girl.initial_reaction == "infatuated":
                if is_currently_a_mother:
                    selected_girl.character "Natural cycle? I can't stop thinking about you! Fine, I'll go natural for you, even with [child_reference]!"
                else:
                    selected_girl.character "Natural cycle? I can't stop thinking about you! Fine, I'll go natural for you!"
            elif selected_girl.initial_reaction == "generous":
                if is_currently_a_mother:
                    selected_girl.character "I want to give you everything, including my natural cycle with [child_reference] to consider."
                else:
                    selected_girl.character "I want to give you everything, including my natural cycle."
            else:
                if is_currently_a_mother:
                    selected_girl.character "I... see your point, Professor. Maybe I've been too reliant on artificial methods with [child_reference]."
                else:
                    selected_girl.character "I... see your point, Professor. Maybe I've been too reliant on artificial methods."
            
            $ selected_girl.previous_birth_control_reaction = "positive"
            
            menu:
                "Would you consider stopping birth control to experience your natural cycle?" if currently_on_birth_control:
                    $ selected_girl.bc_status_known = True
                    if selected_girl.initial_reaction in ["seductive", "infatuated", "generous", "submissive", "neutral"]:
                        $ selected_girl.birth_control = False
                        $ selected_girl.previous_birth_control_reaction = "positive"
                        if is_currently_a_mother:
                            selected_girl.character "You've convinced me... I'll stop birth control to experience my natural cycle with [child_reference]."
                        else:
                            selected_girl.character "You've convinced me... I'll stop birth control to experience my natural cycle with you."
                    elif selected_girl.initial_reaction == "manipulative":
                        if is_currently_a_mother:
                            selected_girl.character "Stop birth control with [child_reference] to support? That's pregnancy risk, Professor. What's your offer?"
                        else:
                            selected_girl.character "Stop birth control? That's pregnancy risk, Professor. What's your offer?"
                        
                        menu:
                            "Offer 1000 for natural cycle expenses?":
                                if player.cash >= 1000:
                                    $ player.cash -= 1000
                                    $ selected_girl.cash += 1000
                                    $ selected_girl.birth_control = False
                                    $ selected_girl.apply_impacts({"naturism": 40, "corruption": 30})
                                    if is_currently_a_mother:
                                        selected_girl.character "1000 for natural cycle with [child_reference]? Deal, but if I get pregnant, you're supporting us both."
                                    else:
                                        selected_girl.character "1000 for natural cycle? Deal, but if I get pregnant, you're supporting the baby."
                                else:
                                    selected_girl.character "You think natural living is cheap? Come back when you can afford it."
                                    $ selected_girl.apply_impacts({"affection": -25})
                            "Promise to support any child naturally conceived":
                                $ selected_girl.birth_control = False
                                $ selected_girl.apply_impacts({"baby_desire": 50, "corruption": 40})
                                if is_currently_a_mother:
                                    selected_girl.character "Support me and [child_reference] and any new baby? Fine, I'll go natural - but I want this commitment in writing."
                                else:
                                    selected_girl.character "Support me and any baby? Fine, I'll go natural - but I want this commitment in writing."
                            "Never mind then.":
                                if is_currently_a_mother:
                                    selected_girl.character "Smart move. Natural living with [child_reference] is expensive."
                                else:
                                    selected_girl.character "Smart move. Natural living isn't cheap."
                                $ selected_girl.apply_impacts({"affection": -10})
                    else:
                        selected_girl.character "I'm not ready to go that far with stopping birth control, Professor."
                
                "I'm already experiencing my natural cycle, Professor. It feels right for my body." if not currently_on_birth_control:
                    $ selected_girl.bc_status_known = True
                    if selected_girl.initial_reaction == "loving":
                        if is_currently_a_mother:
                            selected_girl.character "I know... and it feels wonderful. My body knows what it's doing, even with [child_reference]."
                        else:
                            selected_girl.character "I know... and it feels wonderful. My body knows what it's doing with you."
                    elif selected_girl.initial_reaction == "seductive":
                        if is_currently_a_mother:
                            selected_girl.character "I know... and it means you can cum in my bare pussy anytime. Even with [child_reference], I'm still ready for you."
                        else:
                            selected_girl.character "I know... and it means you can cum in my bare pussy anytime. I'm always ready for you."
                    else:
                        if is_currently_a_mother:
                            selected_girl.character "I know... and it feels right for my body, even with [child_reference] to care for."
                        else:
                            selected_girl.character "I know... and it feels right for my body."
                
                "Would you consider starting birth control in the future?" if not currently_on_birth_control:
                    $ selected_girl.bc_status_known = True
                    if selected_girl.initial_reaction in ["loving", "devoted"]:
                        $ selected_girl.birth_control = True
                        $ selected_girl.previous_birth_control_reaction = "neutral"
                        if is_currently_a_mother:
                            selected_girl.character "You've convinced me... I'll consider birth control for health reasons in the future, for [child_reference]'s sake."
                        else:
                            selected_girl.character "You've convinced me... I'll consider birth control for health reasons in the future."
                    else:
                        selected_girl.character "I'm not comfortable with that suggestion, Professor."
        
        # FAMILY PLANNING APPROACH (INCREASES BABY_DESIRE)
        "Have you thought about how birth control affects your family planning?" if family_leaning > 3:
            $ selected_girl.apply_impacts({"baby_desire": 75, "affection": 50})
            $ selected_girl.bc_status_known = True
            
            # Response based on initial_reaction
            if selected_girl.initial_reaction == "loving":
                if is_currently_a_mother:
                    selected_girl.character "You're right, Professor... with [child_reference], I've been thinking about how birth control affects our family planning."
                else:
                    selected_girl.character "You're right, Professor... I've been thinking about how birth control affects our family planning together."
            elif selected_girl.initial_reaction == "submissive":
                if is_currently_a_mother:
                    selected_girl.character "You're in charge of our family planning, Master. If you want more children with [child_reference], I'll stop birth control."
                else:
                    selected_girl.character "You're in charge of our family planning, Master. If you want children, I'll stop birth control."
            elif selected_girl.initial_reaction == "seductive":
                if is_currently_a_mother:
                    selected_girl.character "Mmm... family planning? That means talking about you breeding me again with [child_reference] as a big sibling? So hot!"
                else:
                    selected_girl.character "Mmm... family planning? That means talking about you breeding me? So hot!"
            elif selected_girl.initial_reaction == "manipulative":
                if is_currently_a_mother:
                    selected_girl.character "Family planning with [child_reference] already? That's expensive business, Professor. What's your offer for expanding our family?"
                else:
                    selected_girl.character "Family planning? That's expensive business, Professor. What's your offer for starting our family?"
            elif selected_girl.initial_reaction == "devoted":
                if is_currently_a_mother:
                    selected_girl.character "Anything for you. I want to expand our family with [child_reference]. If you want more babies, I'll stop birth control."
                else:
                    selected_girl.character "Anything for you. I want to start our family. If you want babies, I'll stop birth control."
            elif selected_girl.initial_reaction == "admiring":
                if is_currently_a_mother:
                    selected_girl.character "You're so thoughtful about our family's future with [child_reference]. I admire your planning."
                else:
                    selected_girl.character "You're so thoughtful about our family's future. I admire your planning."
            elif selected_girl.initial_reaction == "infatuated":
                if is_currently_a_mother:
                    selected_girl.character "Family planning with you and [child_reference]? I can't stop thinking about it! Yes, let's expand our family!"
                else:
                    selected_girl.character "Family planning with you? I can't stop thinking about it! Yes, let's start our family!"
            elif selected_girl.initial_reaction == "generous":
                if is_currently_a_mother:
                    selected_girl.character "I want to give you everything, including more children with [child_reference]. If you want to expand our family, I'll stop birth control."
                else:
                    selected_girl.character "I want to give you everything, including children. If you want to start our family, I'll stop birth control."
            else:
                if is_currently_a_mother:
                    selected_girl.character "I... hadn't considered that perspective, Professor. Family planning with [child_reference] is important."
                else:
                    selected_girl.character "I... hadn't considered that perspective, Professor. Family planning is important."
            
            $ selected_girl.previous_birth_control_reaction = "excited"
    
            menu:
                "Would you consider stopping birth control to have another child?" if currently_on_birth_control and selected_girl.baby_desire > 70:
                    $ selected_girl.bc_status_known = True
                    if selected_girl.initial_reaction in ["loving", "devoted", "generous", "infatuated"]:
                        $ selected_girl.birth_control = False
                        $ selected_girl.previous_birth_control_reaction = "excited"
                        if is_currently_a_mother:
                            selected_girl.character "I've actually been wanting another child with [child_reference]. I'll stop birth control for our family!"
                        else:
                            selected_girl.character "I've actually been wanting a child with you. I'll stop birth control for our family!"
                    elif selected_girl.initial_reaction == "manipulative":
                        if is_currently_a_mother:
                            selected_girl.character "Another child with [child_reference]? That's premium family expansion, Professor. What's your offer?"
                        else:
                            selected_girl.character "A child? That's premium family planning, Professor. What's your offer?"
                        
                        menu:
                            "Offer 5000 for family expansion?":
                                if player.cash >= 5000:
                                    $ player.cash -= 5000
                                    $ selected_girl.cash += 5000
                                    $ selected_girl.birth_control = False
                                    $ selected_girl.apply_impacts({"baby_desire": 80, "corruption": 60})
                                    if is_currently_a_mother:
                                        selected_girl.character "5000 for expanding our family with [child_reference]? Fine, I'll stop birth control - but I expect you to be a real father."
                                    else:
                                        selected_girl.character "5000 for starting our family? Fine, I'll stop birth control - but I expect you to be a real father."
                                else:
                                    selected_girl.character "You think that's enough for a child? Don't insult me."
                                    $ selected_girl.apply_impacts({"affection": -40})
                            "Promise to be a good father and provider":
                                $ selected_girl.birth_control = False
                                $ selected_girl.apply_impacts({"baby_desire": 90, "affection": 50, "corruption": 20})
                                if is_currently_a_mother:
                                    selected_girl.character "Be a good father to me, [child_reference], and our new baby? Now THAT's what I want. Fine, let's expand our family!"
                                else:
                                    selected_girl.character "Be a good father and provider? Now THAT's what I want. Fine, let's start our family!"
                            "I'll need to think about it.":
                                if is_currently_a_mother:
                                    selected_girl.character "Think about it while I consider raising another child. Let me know when you're ready to be a father."
                                else:
                                    selected_girl.character "Think about it while I consider raising your child. Let me know when you're ready to be a father."
                                $ selected_girl.apply_impacts({"affection": -20})
                    else:
                        selected_girl.character "I'm not ready to make that decision right now, Professor."
                
                "Do you think [child_reference] would like a sibling?" if is_base_mother and total_kids == 1:
                    if selected_girl.initial_reaction in ["loving", "generous"]:
                        $ selected_girl.birth_control = False
                        $ selected_girl.previous_birth_control_reaction = "excited"
                        selected_girl.character "You know... I've always wanted [child_reference] to have a sibling. Maybe you're right, Professor."
                    elif selected_girl.initial_reaction == "manipulative":
                        selected_girl.character "A sibling for [child_reference]? That's expensive, Professor. What's your offer for giving my child a brother or sister?"
                        
                        menu:
                            "Offer 3000 for the sibling?":
                                if player.cash >= 3000:
                                    $ player.cash -= 3000
                                    $ selected_girl.cash += 3000
                                    $ selected_girl.birth_control = False
                                    $ selected_girl.apply_impacts({"baby_desire": 70, "corruption": 50})
                                    selected_girl.character "3000 for [child_reference]'s sibling? Fine, I'll stop birth control - but you'll be supporting both children."
                                else:
                                    selected_girl.character "You think that's enough for giving [child_reference] a sibling? Come back when you're serious."
                                    $ selected_girl.apply_impacts({"affection": -30})
                            "Promise to be a good father to both children":
                                $ selected_girl.birth_control = False
                                $ selected_girl.apply_impacts({"baby_desire": 85, "affection": 45, "corruption": 25})
                                selected_girl.character "Be a good father to [child_reference] and their new sibling? Now that's what I want. Fine, let's expand our family!"
                            "Maybe another time.":
                                selected_girl.character "Fine. But [child_reference] would love a sibling. Don't come crying when you miss the chance."
                                $ selected_girl.apply_impacts({"affection": -15})
                    else:
                        selected_girl.character "I appreciate the perspective, Professor, but I need to wait for the right time."
                
                "What are your long-term family goals?":
                    if selected_girl.initial_reaction == "loving":
                        if is_currently_a_mother:
                            selected_girl.character "I've always dreamed of a large family with you and [child_reference]. Birth control is just temporary planning."
                        else:
                            selected_girl.character "I've always dreamed of a large family with you. Birth control is just temporary planning."
                    elif selected_girl.initial_reaction == "manipulative":
                        if is_currently_a_mother:
                            selected_girl.character "My long-term goals involve financial security for me and [child_reference]. Birth control stops when you start providing."
                        else:
                            selected_girl.character "My long-term goals involve financial security. Birth control stops when you start providing."
                    elif selected_girl.initial_reaction in ["seductive", "infatuated"]:
                        if is_currently_a_mother:
                            selected_girl.character "I want lots of babies with you! [child_reference] needs lots of siblings, and I want you to keep breeding me!"
                        else:
                            selected_girl.character "I want lots of babies with you! I want you to keep breeding me over and over!"
                    else:
                        if is_currently_a_mother:
                            selected_girl.character "I'm open to family growth with [child_reference], but I want to be responsible about timing and spacing."
                        else:
                            selected_girl.character "I'm open to family growth, but I want to be responsible about timing and spacing."
        
        # RISKY THRILL APPROACH (INCREASES CORRUPTION)
        "Isn't there something exciting about the possibility of pregnancy without birth control?" if risk_taking > 3:
            $ selected_girl.apply_impacts({"corruption": 100, "affection": 75})
            
            # Response based on initial_reaction
            if selected_girl.initial_reaction == "seductive":
                if is_currently_a_mother:
                    selected_girl.character "Professor... that's so inappropriate to say, but... you're right, it is exciting - even with [child_reference] to consider. The risk makes me wet!"
                else:
                    selected_girl.character "Professor... that's so inappropriate to say, but... you're right, it is exciting. The risk makes me wet!"
            elif selected_girl.initial_reaction == "infatuated":
                if is_currently_a_mother:
                    selected_girl.character "Getting pregnant without birth control? I can't stop thinking about it! Yes, let's risk it for [child_reference]'s sibling!"
                else:
                    selected_girl.character "Getting pregnant without birth control? I can't stop thinking about it! Yes, let's risk it!"
            elif selected_girl.initial_reaction == "manipulative":
                if is_currently_a_mother:
                    selected_girl.character "The thrill of pregnancy with [child_reference] to support? That's the ultimate risk, Professor. What's your offer for playing Russian roulette with my womb?"
                else:
                    selected_girl.character "The thrill of pregnancy? That's the ultimate risk, Professor. What's your offer for playing Russian roulette with my womb?"
            elif selected_girl.initial_reaction == "submissive":
                if is_currently_a_mother:
                    selected_girl.character "If you want the thrill of risky pregnancy with [child_reference], Master... I'll stop birth control and take the risk."
                else:
                    selected_girl.character "If you want the thrill of risky pregnancy, Master... I'll stop birth control and take the risk."
            else:
                if is_currently_a_mother:
                    selected_girl.character "Professor... that's inappropriate to say, but... I see what you mean, even with [child_reference]."
                else:
                    selected_girl.character "Professor... that's inappropriate to say, but... I see what you mean."
            
            $ selected_girl.previous_birth_control_reaction = "excited"
    
            menu:
                "Would you consider stopping birth control for the thrill?" if currently_on_birth_control:
                    $ selected_girl.bc_status_known = True
                    if selected_girl.initial_reaction in ["seductive", "infatuated"]:
                        $ selected_girl.birth_control = False
                        $ selected_girl.previous_birth_control_reaction = "excited"
                        if is_currently_a_mother:
                            selected_girl.character "Mmm... I've actually been fantasizing about getting pregnant from you again. Let's do it - [child_reference] needs a sibling!"
                        else:
                            selected_girl.character "Mmm... I've actually been fantasizing about getting pregnant from you. Let's do it - knock me up!"
                    elif selected_girl.initial_reaction == "manipulative":
                        if is_currently_a_mother:
                            selected_girl.character "Stop birth control for thrills with [child_reference]? That's high-stakes gambling, Professor. What's your payout?"
                        else:
                            selected_girl.character "Stop birth control for thrills? That's high-stakes gambling, Professor. What's your payout?"
                        
                        menu:
                            "Offer 3000 for the gamble?":
                                if player.cash >= 3000:
                                    $ player.cash -= 3000
                                    $ selected_girl.cash += 3000
                                    $ selected_girl.birth_control = False
                                    $ selected_girl.apply_impacts({"baby_desire": 60, "corruption": 70})
                                    if is_currently_a_mother:
                                        selected_girl.character "3000 for gambling with my womb and [child_reference]'s future? Fine, I'll stop birth control - but if I get pregnant, you pay big time."
                                    else:
                                        selected_girl.character "3000 for gambling with my womb? Fine, I'll stop birth control - but if I get pregnant, you pay big time."
                                else:
                                    selected_girl.character "You think that's enough for this kind of risk? Don't insult me."
                                    $ selected_girl.apply_impacts({"affection": -35})
                            # "Promise to double support if pregnant":
                                # $ selected_girl.birth_control = False
                                # $ selected_girl.apply_impacts({"baby_desire": 70, "corruption": 60})
                                # if is_currently_a_mother:
                                    # selected_girl.character "Double support for me and [child_reference] if pregnant? Fine, I'll take the gamble - but I want this promise in writing."
                                # else:
                                    # selected_girl.character "Double support if pregnant? Fine, I'll take the gamble - but I want this promise in writing."
                            "Maybe this is too risky.":
                                if is_currently_a_mother:
                                    selected_girl.character "Smart move. Gambling with [child_reference]'s future is expensive."
                                else:
                                    selected_girl.character "Smart move. This kind of gambling isn't cheap."
                                $ selected_girl.apply_impacts({"affection": -15})
                    else:
                        selected_girl.character "That's inappropriate to discuss, Professor."
                
                "What's your biggest fear about pregnancy?":
                    if selected_girl.initial_reaction == "seductive":
                        if is_currently_a_mother:
                            selected_girl.character "Fear? Professor, the only thing I fear is not getting pregnant enough times! [child_reference] needs lots of siblings!"
                        else:
                            selected_girl.character "Fear? Professor, the only thing I fear is not getting pregnant enough times!"
                    elif selected_girl.initial_reaction == "manipulative":
                        if is_currently_a_mother:
                            selected_girl.character "My biggest fear? Not getting enough financial support for me and [child_reference]. Pregnancy without proper compensation is terrifying."
                        else:
                            selected_girl.character "My biggest fear? Not getting enough financial support. Pregnancy without proper compensation is terrifying."

        # FALLBACK OPTION - ALWAYS AVAILABLE
        "Perhaps we should maintain appropriate professional boundaries regarding reproductive health.": 
            "[selected_girl] visibly relaxes as you change the subject, clearly relieved to avoid an uncomfortable conversation."
            
            if is_base_mother:
                if child_reference:
                    selected_girl.character "Thank you for recognizing this boundary, Professor. As a mother, I must maintain appropriate conduct at all times, especially with [child_reference] around."
                else:
                    selected_girl.character "Thank you for recognizing this boundary, Professor. Professional conduct must be maintained at all times."
            elif is_student:
                selected_girl.character "I appreciate you recognizing this boundary, Professor. This topic is too personal for our professional relationship."
            else:
                selected_girl.character "Thank you for recognizing this boundary. Some topics are best kept professional."
            
            $ selected_girl.apply_impacts({
                "discipline": 125,
                "affection": 60 if selected_girl.affection > 65 else 30,
                "fear": -50,
                "intellect": 40,
                "reputation": 20
            })
                    
            return
        
    # PHASE 3: FINAL REACTIONS BASED ON OUTCOMES
    $ bc_changed = (selected_girl.birth_control != currently_on_birth_control)
    
    if bc_changed:
        $ selected_girl.bc_status_known = True
        if selected_girl.birth_control:
            if norm_discipline > 7:
                selected_girl.character "Thank you for helping me see the importance of birth control, Professor."
            else:
                selected_girl.character "I hope I made the right decision about birth control, Professor."
        else:
            if risk_taking > 5 or family_leaning > 5:
                selected_girl.character "I'm looking forward to experiencing my natural cycle with you, Professor."
            else:
                selected_girl.character "I hope I'm not making a mistake with the birth control changes, Professor."
    else:
        selected_girl.character "Thanks for checking in about birth control preferences, Professor."
    
    # PHASE 4: SET UP FOR FUTURE CONVERSATIONS
    # Track that this conversation happened
    $ actions_already_done.setdefault(selected_girl.id, []).append("small_talk_birth_control")
    
    # Create unique dialogue paths for next conversation
    # Create unique dialogue paths for next conversation
    $ current_level = getattr(selected_girl, "birth_control_discussion_level", 0)
    $ selected_girl.birth_control_discussion_level = 1 if current_level == 0 else min(3, current_level + 1)
 
    # Schedule follow-up conversation based on discussion level
    if bc_changed:
        if birth_control_discussion_level == 1:
            $ selected_girl.birth_control_followup = time_manager.total_days + 5
        elif birth_control_discussion_level == 2:
            $ selected_girl.birth_control_followup = time_manager.total_days + 7
        else:
            $ selected_girl.birth_control_followup = time_manager.total_days + 10
    
    # Apply final impacts based on discussion level and outcomes
    $ impact_amount = 25 * birth_control_discussion_level
    
    if bc_changed:
        if selected_girl.birth_control:  # Started birth control
            $ selected_girl.apply_impacts({
                "discipline": impact_amount,
                "fear": impact_amount * 0.5,
                "affection": impact_amount * 0.3,
                "baby_desire": -impact_amount * 0.7
            })
        else:  # Stopped birth control
            $ selected_girl.apply_impacts({
                "corruption": impact_amount,
                "naturism": impact_amount * 0.5,
                "affection": impact_amount * 0.7,
                "baby_desire": impact_amount * 0.8
            })
    else:  # No change
        $ selected_girl.apply_impacts({
            "intellect": impact_amount * 0.5,
            "affection": impact_amount * 0.4
        })
    
    $ time_manager.skip_time(minutes=5)
    
    return

label vt_small_talk_birth_control_followup:
    
    # Clear identification of relationship types (matching small_talk_birth_control)
    $ is_base_mother = False
    $ is_student = False
    $ is_other = False

    if hasattr(selected_girl, "daughter") and selected_girl.daughter:
        $ is_base_mother = True
    elif hasattr(selected_girl, "mother") and selected_girl.mother:
        $ is_student = True
    else:
        $ is_other = True
    
    # PROPER KIDS TRACKING (matching small_talk_birth_control)
    $ total_kids = selected_girl.kids
    $ kids_with_player = selected_girl.kids_with_player
    $ kids_with_others = selected_girl.kids_with_npc
    $ is_currently_a_mother = total_kids > 0
    if is_base_mother:
        $ is_currently_a_mother = total_kids > 1  # includes original daughter
    
    # DYNAMIC CHILD REFERENCE (matching small_talk_birth_control)
    $ child_reference = ""
    if is_base_mother and (total_kids - kids_with_player - kids_with_others) > 0:
        $ child_reference = "my daughter"
    elif kids_with_player > 0:
        $ child_reference = "your child" if kids_with_player == 1 else f"our {total_kids} children"
    elif kids_with_others > 0:
        $ child_reference = "that child" if kids_with_others == 1 else f"my {total_kids} children"
    else:
        $ child_reference = "my child" if is_currently_a_mother else ""
    
    # BIRTH CONTROL STATE TRACKING (matching small_talk_birth_control)
    $ currently_on_birth_control = selected_girl.birth_control
    $ bc_status_known = selected_girl.bc_status_known
    
    # Check how birth control status has changed since last discussion
    $ previous_birth_control = getattr(selected_girl, "previous_birth_control", currently_on_birth_control)
    $ birth_control_changed = (previous_birth_control != currently_on_birth_control)
    
    # PERSONALITY CLUSTERING (matching small_talk_birth_control)
    $ norm_naturism = selected_girl.naturism / 10
    $ norm_corruption = selected_girl.corruption / 10
    $ norm_discipline = selected_girl.discipline / 10
    $ norm_fear = selected_girl.fear / 10
    $ norm_baby_desire = selected_girl.baby_desire / 10 if hasattr(selected_girl, "baby_desire") else 5.0

    $ natural_leaning = norm_naturism - norm_discipline
    $ risk_taking = norm_corruption - norm_fear
    $ family_leaning = norm_baby_desire - norm_fear
    
    # NORMALIZE PLAYER STATS TO 0-10 SCALE FOR CLUSTERING (matching small_talk_birth_control)
    $ norm_compassion = (player.compassion + 10) / 2  # -10 to 10 becomes 0 to 10
    $ norm_intellect = selected_girl.intellect / 10  # 0 to 100 becomes 0 to 10
    $ norm_control = (player.control + 10) / 2  # -10 to 10 becomes 0 to 10
    $ norm_reputation = player.reputation / 10  # 0 to 100 becomes 0 to 10
    $ norm_lust = (player.lust + 10) / 2  # -10 to 10 becomes 0 to 10
    $ norm_arousal = player.arousal / 12  # 0 to 120 becomes 0 to 10
    
    # CLUSTER PLAYER STATS (0-10 scale)
    $ empathy = (norm_compassion + norm_intellect) / 2
    $ control = (norm_control + norm_reputation) / 2
    $ lust = (norm_lust + norm_arousal) / 2
    
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

        player_stats = {
            "control": player.control,
            "greed": player.greed,
            "lust": player.lust,
            "compassion": player.compassion
        }

        # Get the two highest stats for the girl (the ones that will drive her reaction)
        sorted_girl_stats = sorted(girl_stats.items(), key=lambda item: item[1], reverse=True)
        dominant_girl_stat1, dominant_girl_value1 = sorted_girl_stats[0]
        dominant_girl_stat2, dominant_girl_value2 = sorted_girl_stats[1]

        # Get the highest stat for the player (the one that will drive his reaction)
        dominant_player_stat = max(player_stats, key=player_stats.get)
        dominant_player_value = player_stats[dominant_player_stat]
        
        # SET REACTION BASED ON DOMINANT STATS + STRENGTH
        if dominant_girl_value1 > 60 and dominant_girl_value2 > 60:
            if dominant_girl_stat1 == "corruption" and dominant_girl_stat2 == "fear":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "submissive"  # "You're in charge, Master"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "seductive"  # "I'm yours to command"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "manipulative"  # "What's in it for me?"
                else:  # compassion
                    selected_girl.initial_reaction = "devoted"  # "I'll do anything for you"
            elif dominant_girl_stat1 == "affection" and dominant_girl_stat2 == "intellect":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "admiring"  # "You're so strong and smart"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "infatuated"  # "I can't stop thinking about you"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "generous"  # "I want to give you everything"
                else:  # compassion
                    selected_girl.initial_reaction = "loving"  # "I feel so connected to you"
            # Add more combinations as needed
        elif dominant_girl_value1 > 60 and dominant_girl_value2 <= 60:
            if dominant_girl_stat1 == "corruption":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "submissive"  # "You're in charge, Master"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "seductive"  # "I'm yours to command"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "manipulative"  # "What's in it for me?"
                else:  # compassion
                    selected_girl.initial_reaction = "devoted"  # "I'll do anything for you"
            elif dominant_girl_stat1 == "affection":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "admiring"  # "You're so strong"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "infatuated"  # "I can't stop thinking about you"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "generous"  # "I want to give you everything"
                else:  # compassion
                    selected_girl.initial_reaction = "loving"  # "I feel so connected to you"
            # Add more combinations as needed
        elif dominant_girl_value1 <= 60 and dominant_girl_value2 > 60:
            if dominant_girl_stat2 == "corruption":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "submissive"  # "You're in charge, Master"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "seductive"  # "I'm yours to command"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "manipulative"  # "What's in it for me?"
                else:  # compassion
                    selected_girl.initial_reaction = "devoted"  # "I'll do anything for you"
            elif dominant_girl_stat2 == "affection":
                if dominant_player_stat == "control":
                    selected_girl.initial_reaction = "admiring"  # "You're so strong"
                elif dominant_player_stat == "lust":
                    selected_girl.initial_reaction = "infatuated"  # "I can't stop thinking about you"
                elif dominant_player_stat == "greed":
                    selected_girl.initial_reaction = "generous"  # "I want to give you everything"
                else:  # compassion
                    selected_girl.initial_reaction = "loving"  # "I feel so connected to you"
            # Add more combinations as needed
        else:
            selected_girl.initial_reaction = "neutral"  # "Just another student"

    
    # TRACK CONVERSATION HISTORY (matching small_talk_birth_control)
    $ has_discussed_birth_control_before = "small_talk_birth_control" in actions_already_done.get(selected_girl.id, [])
    $ previous_birth_control_reaction = getattr(selected_girl, "previous_birth_control_reaction", "neutral")
    $ discussion_level = selected_girl.birth_control_discussion_level
    
    # Track previous baby_desire for impact calculation
    $ previous_baby_desire = selected_girl.baby_desire
    
    # DIFFERENT DIALOGUE BASED ON DISCUSSION LEVEL AND BIRTH CONTROL STATUS
    if discussion_level >= 2:
        if birth_control_changed:
            if currently_on_birth_control:
                # She started birth control
                if selected_girl.initial_reaction == "loving":
                    if is_currently_a_mother:
                        selected_girl.character "I've been taking birth control as we discussed. I need to be responsible with [child_reference] to think about."
                    else:
                        selected_girl.character "I've been taking birth control as we discussed. I need to be responsible for us."
                elif selected_girl.initial_reaction == "submissive":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control like you wanted, Master. I must protect my existing child."
                    else:
                        selected_girl.character "I've started birth control like you wanted, Master. Your will is my command."
                elif selected_girl.initial_reaction == "seductive":
                    if is_currently_a_mother:
                        selected_girl.character "I've been taking birth control... though as a mother, I must admit I miss the thrill of risk."
                    else:
                        selected_girl.character "I've been taking birth control... though I must admit I miss the thrill of risk."
                elif selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "I've been taking birth control as we discussed. It costs money, but I'm being responsible for [child_reference]."
                    else:
                        selected_girl.character "I've been taking birth control as we discussed. It costs money, but I'm being responsible."
                elif selected_girl.initial_reaction == "devoted":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control because it pleases you - though my child's wellbeing comes first."
                    else:
                        selected_girl.character "I've started birth control because it pleases you. Your will is my command."
                elif selected_girl.initial_reaction == "admiring":
                    if is_currently_a_mother:
                        selected_girl.character "I've been taking birth control consistently. A mother needs to be practical about family planning."
                    else:
                        selected_girl.character "I've been taking birth control consistently. I admire how you think about the future."
                elif selected_girl.initial_reaction == "infatuated":
                    if is_currently_a_mother:
                        selected_girl.character "I've been taking birth control because you asked... but I dream about having your baby and giving [child_reference] a sibling."
                    else:
                        selected_girl.character "I've been taking birth control because you asked... but I dream about having your baby."
                elif selected_girl.initial_reaction == "generous":
                    if is_currently_a_mother:
                        selected_girl.character "I've been taking birth control to be responsible for [child_reference], though I want to give you everything."
                    else:
                        selected_girl.character "I've been taking birth control to be responsible, though I want to give you everything."
                elif selected_girl.initial_reaction == "neutral":
                    if is_currently_a_mother:
                        selected_girl.character "I've been taking birth control as discussed. A mother needs to plan ahead."
                    else:
                        selected_girl.character "I've been taking birth control as discussed. It's the responsible thing to do."
                
                $ selected_girl.baby_desire = max(0, selected_girl.baby_desire - 3)
                
            else:
                # She stopped birth control
                if selected_girl.initial_reaction == "loving":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control like we discussed. I feel so connected to you, and [child_reference] would love a sibling."
                    else:
                        selected_girl.character "I've stopped birth control like we discussed. I feel so connected to you."
                elif selected_girl.initial_reaction == "submissive":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control as you commanded, Master. My body is ready to carry your child - it already knows how."
                    else:
                        selected_girl.character "I've stopped birth control as you commanded, Master. My body is yours to breed."
                elif selected_girl.initial_reaction == "seductive":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control... the risk of pregnancy again is so thrilling, even with [child_reference] at home."
                    else:
                        selected_girl.character "I've stopped birth control... the risk of pregnancy is so thrilling."
                elif selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control like we discussed. Another baby would mean more support from you - I'm counting on it."
                    else:
                        selected_girl.character "I've stopped birth control like we discussed. A baby would mean more support from you - I'm counting on it."
                elif selected_girl.initial_reaction == "devoted":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control because it pleases you. My body is yours even with my maternal duties."
                    else:
                        selected_girl.character "I've stopped birth control because it pleases you. My body is yours to fill."
                elif selected_girl.initial_reaction == "admiring":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control. I trust your judgment about expanding our family with [child_reference]."
                    else:
                        selected_girl.character "I've stopped birth control. I trust your judgment about our future."
                elif selected_girl.initial_reaction == "infatuated":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control! I can't wait to have your baby and watch [child_reference] become a big sibling!"
                    else:
                        selected_girl.character "I've stopped birth control! I can't wait to have your baby!"
                elif selected_girl.initial_reaction == "generous":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control. I want to give you another child to grow our family with [child_reference]."
                    else:
                        selected_girl.character "I've stopped birth control. I want to give you a child."
                elif selected_girl.initial_reaction == "neutral":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control. I'm already a mother, so what's one more?"
                    else:
                        selected_girl.character "I've stopped birth control. I'm open to seeing what happens."
                
                $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 5)
                
        else:
            # No change in birth control status
            if currently_on_birth_control:
                if selected_girl.initial_reaction == "loving":
                    if is_currently_a_mother:
                        selected_girl.character "I'm still on birth control. I need to be responsible for [child_reference]."
                    else:
                        selected_girl.character "I'm still on birth control. I need to be responsible for us."
                elif selected_girl.initial_reaction == "submissive":
                    if is_currently_a_mother:
                        selected_girl.character "I'm still taking birth control, Master, as you commanded. I must protect my existing child."
                    else:
                        selected_girl.character "I'm still taking birth control, Master, as you commanded."
                elif selected_girl.initial_reaction == "seductive":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control... though a mother like me sometimes dreams of the thrill again."
                    else:
                        selected_girl.character "Still on birth control... though I sometimes dream of the thrill."
                elif selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control. It's expensive, but [child_reference] needs me to be responsible."
                    else:
                        selected_girl.character "Still on birth control. It's expensive, but I'm being responsible."
                elif selected_girl.initial_reaction == "devoted":
                    if is_currently_a_mother:
                        selected_girl.character "I'm still on birth control as you wish. My child's wellbeing comes first, then your will."
                    else:
                        selected_girl.character "I'm still on birth control as you wish. Your will is my command."
                elif selected_girl.initial_reaction == "admiring":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control. I admire how you respect my need to plan for [child_reference]'s future."
                    else:
                        selected_girl.character "Still on birth control. I admire how you respect my need to plan."
                elif selected_girl.initial_reaction == "infatuated":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control... but I dream about stopping it and giving [child_reference] a sibling."
                    else:
                        selected_girl.character "Still on birth control... but I dream about stopping it and having your baby."
                elif selected_girl.initial_reaction == "generous":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control for [child_reference]'s sake, though I want to give you more children."
                    else:
                        selected_girl.character "Still on birth control, though I want to give you everything."
                elif selected_girl.initial_reaction == "neutral":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control. A mother needs to be practical."
                    else:
                        selected_girl.character "Still on birth control. Being responsible is important."
            else:
                if selected_girl.initial_reaction == "loving":
                    if is_currently_a_mother:
                        selected_girl.character "I'm still not on birth control. I feel connected to you, and [child_reference] would love a sibling someday."
                    else:
                        selected_girl.character "I'm still not on birth control. I feel connected to you."
                elif selected_girl.initial_reaction == "submissive":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control, Master. My body is ready for your child - it already knows how to carry one."
                    else:
                        selected_girl.character "Still not on birth control, Master. My body is ready for your child."
                elif selected_girl.initial_reaction == "seductive":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. The risk of another pregnancy is so exciting, even with [child_reference] to care for."
                    else:
                        selected_girl.character "Still not on birth control. The risk of pregnancy is so exciting."
                elif selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. Another baby would mean more support - I'm ready when you are, Professor."
                    else:
                        selected_girl.character "Still not on birth control. A baby would mean more support - I'm ready when you are, Professor."
                elif selected_girl.initial_reaction == "devoted":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. My body is yours to breed, even with my maternal duties."
                    else:
                        selected_girl.character "Still not on birth control. My body is yours to breed."
                elif selected_girl.initial_reaction == "admiring":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. I trust your plans for our family with [child_reference]."
                    else:
                        selected_girl.character "Still not on birth control. I trust your plans for our future."
                elif selected_girl.initial_reaction == "infatuated":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control! I'm hoping you'll give [child_reference] a sibling soon!"
                    else:
                        selected_girl.character "Still not on birth control! I'm hoping you'll give me a baby soon!"
                elif selected_girl.initial_reaction == "generous":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. I'm ready to give you another child to grow our family."
                    else:
                        selected_girl.character "Still not on birth control. I'm ready to give you a child."
                elif selected_girl.initial_reaction == "neutral":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. I'm open to expanding our family."
                    else:
                        selected_girl.character "Still not on birth control. I'm open to what happens."
                
                $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 2)

    elif discussion_level == 1:
        if birth_control_changed:
            if currently_on_birth_control:
                if selected_girl.initial_reaction == "loving":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control as we discussed. I need to think about [child_reference] first."
                    else:
                        selected_girl.character "I've started birth control as we discussed. I need to think about our future."
                elif selected_girl.initial_reaction == "submissive":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control as you commanded, Master. I must protect my child."
                    else:
                        selected_girl.character "I've started birth control as you commanded, Master."
                elif selected_girl.initial_reaction == "seductive":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control... though as a mother, part of me misses the excitement of risk."
                    else:
                        selected_girl.character "I've started birth control... though part of me misses the excitement of risk."
                elif selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control. It's an expense, but I'm being responsible for [child_reference]."
                    else:
                        selected_girl.character "I've started birth control. It's an expense, but I'm being responsible."
                elif selected_girl.initial_reaction == "devoted":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control to please you, though my child comes first."
                    else:
                        selected_girl.character "I've started birth control to please you. Your will is my command."
                elif selected_girl.initial_reaction == "admiring":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control. A mother must be practical about family planning."
                    else:
                        selected_girl.character "I've started birth control. I admire your foresight."
                elif selected_girl.initial_reaction == "infatuated":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control because you asked... but I still dream about your baby and [child_reference] having a sibling."
                    else:
                        selected_girl.character "I've started birth control because you asked... but I still dream about your baby."
                elif selected_girl.initial_reaction == "generous":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control to be responsible for [child_reference], though I want to give you more."
                    else:
                        selected_girl.character "I've started birth control to be responsible, though I want to give you everything."
                elif selected_girl.initial_reaction == "neutral":
                    if is_currently_a_mother:
                        selected_girl.character "I've started birth control. It's the practical choice for a mother."
                    else:
                        selected_girl.character "I've started birth control. It seems like the practical choice."
                
                $ selected_girl.baby_desire = max(0, selected_girl.baby_desire - 4)
                
            else:
                if selected_girl.initial_reaction == "loving":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control. I feel connected to you, and [child_reference] would love a sibling."
                    else:
                        selected_girl.character "I've stopped birth control. I feel connected to you."
                elif selected_girl.initial_reaction == "submissive":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control as you commanded, Master. My body is ready for your child."
                    else:
                        selected_girl.character "I've stopped birth control as you commanded, Master. My body is yours."
                elif selected_girl.initial_reaction == "seductive":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control. The risk is thrilling, even with [child_reference] to consider."
                    else:
                        selected_girl.character "I've stopped birth control. The risk is thrilling."
                elif selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control. A baby would mean more support - I'm ready to expand our family."
                    else:
                        selected_girl.character "I've stopped birth control. A baby would mean more support - I'm ready when you are."
                elif selected_girl.initial_reaction == "devoted":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control to please you. My body is yours, even as a mother."
                    else:
                        selected_girl.character "I've stopped birth control to please you. My body is yours."
                elif selected_girl.initial_reaction == "admiring":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control. I trust your vision for our family with [child_reference]."
                    else:
                        selected_girl.character "I've stopped birth control. I trust your vision for our future."
                elif selected_girl.initial_reaction == "infatuated":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control! I'm so excited to have your baby and give [child_reference] a sibling!"
                    else:
                        selected_girl.character "I've stopped birth control! I'm so excited to have your baby!"
                elif selected_girl.initial_reaction == "generous":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control. I want to give you another child for our family."
                    else:
                        selected_girl.character "I've stopped birth control. I want to give you a child."
                elif selected_girl.initial_reaction == "neutral":
                    if is_currently_a_mother:
                        selected_girl.character "I've stopped birth control. I'm open to expanding our family."
                    else:
                        selected_girl.character "I've stopped birth control. I'm open to what happens."
                
                $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 4)
                
        else:
            # No change but still discussing
            if currently_on_birth_control:
                if selected_girl.initial_reaction == "loving":
                    if is_currently_a_mother:
                        selected_girl.character "I'm still on birth control. I'm thinking about [child_reference] and our future."
                    else:
                        selected_girl.character "I'm still on birth control. I'm thinking about our future."
                elif selected_girl.initial_reaction == "submissive":
                    if is_currently_a_mother:
                        selected_girl.character "Still taking birth control as you wish, Master. I must protect my existing child."
                    else:
                        selected_girl.character "Still taking birth control as you wish, Master."
                elif selected_girl.initial_reaction == "seductive":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control... though a mother has needs too, Professor."
                    else:
                        selected_girl.character "Still on birth control... though I have needs too, Professor."
                elif selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control. It's the responsible choice for [child_reference]'s sake."
                    else:
                        selected_girl.character "Still on birth control. It's the responsible choice."
                elif selected_girl.initial_reaction == "devoted":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control as you command. My child's needs come first."
                    else:
                        selected_girl.character "Still on birth control as you command. Your will is my command."
                elif selected_girl.initial_reaction == "admiring":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control. I respect your concern for [child_reference]'s wellbeing."
                    else:
                        selected_girl.character "Still on birth control. I respect your concern for my wellbeing."
                elif selected_girl.initial_reaction == "infatuated":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control... but I dream about stopping it for your baby and [child_reference]."
                    else:
                        selected_girl.character "Still on birth control... but I dream about stopping it for your baby."
                elif selected_girl.initial_reaction == "generous":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control for [child_reference], though I want to give you more."
                    else:
                        selected_girl.character "Still on birth control, though I want to give you everything."
                elif selected_girl.initial_reaction == "neutral":
                    if is_currently_a_mother:
                        selected_girl.character "Still on birth control. A mother must be practical."
                    else:
                        selected_girl.character "Still on birth control. It seems practical."
            else:
                if selected_girl.initial_reaction == "loving":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. I'm thinking about you and [child_reference] having a sibling."
                    else:
                        selected_girl.character "Still not on birth control. I'm thinking about you and our future."
                elif selected_girl.initial_reaction == "submissive":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control, Master. My body is ready for your child."
                    else:
                        selected_girl.character "Still not on birth control, Master. My body is yours."
                elif selected_girl.initial_reaction == "seductive":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. The possibility of another baby excites me, Professor."
                    else:
                        selected_girl.character "Still not on birth control. The possibility of a baby excites me, Professor."
                elif selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. I'm ready for your baby whenever you decide to support our family."
                    else:
                        selected_girl.character "Still not on birth control. I'm ready for your baby whenever you decide to support me."
                elif selected_girl.initial_reaction == "devoted":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. My body is yours to breed, Master."
                    else:
                        selected_girl.character "Still not on birth control. My body is yours to breed, Master."
                elif selected_girl.initial_reaction == "admiring":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. I trust your plans for our family."
                    else:
                        selected_girl.character "Still not on birth control. I trust your plans."
                elif selected_girl.initial_reaction == "infatuated":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control! I dream about your baby and [child_reference] as siblings!"
                    else:
                        selected_girl.character "Still not on birth control! I dream about your baby!"
                elif selected_girl.initial_reaction == "generous":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. I'm ready to give you another child."
                    else:
                        selected_girl.character "Still not on birth control. I'm ready to give you a child."
                elif selected_girl.initial_reaction == "neutral":
                    if is_currently_a_mother:
                        selected_girl.character "Still not on birth control. I'm open to expanding our family."
                    else:
                        selected_girl.character "Still not on birth control. I'm open to what happens."

    else:  # discussion_level == 0 (shouldn't happen in follow-up)
        if selected_girl.initial_reaction == "loving":
            if is_currently_a_mother:
                selected_girl.character "I'm confused... but I'm thinking about [child_reference] and what you said."
            else:
                selected_girl.character "I'm confused... but I'm thinking about what you said."
        elif selected_girl.initial_reaction == "submissive":
            if is_currently_a_mother:
                selected_girl.character "I'm confused, Master... but I'm thinking about my child and your commands."
            else:
                selected_girl.character "I'm confused, Master... but I'm thinking about your commands."
        elif selected_girl.initial_reaction == "seductive":
            selected_girl.character "I'm confused... but I'm intrigued by where this might lead."
        elif selected_girl.initial_reaction == "manipulative":
            selected_girl.character "I'm confused... but I'm calculating what this might mean for me."
        elif selected_girl.initial_reaction == "devoted":
            if is_currently_a_mother:
                selected_girl.character "I'm confused... but I'll do what you want regarding my child and birth control."
            else:
                selected_girl.character "I'm confused... but I'll do what you want."
        elif selected_girl.initial_reaction == "admiring":
            selected_girl.character "I'm confused... but I trust your judgment."
        elif selected_girl.initial_reaction == "infatuated":
            if is_currently_a_mother:
                selected_girl.character "I'm confused... but I'm dreaming about your baby and [child_reference]!"
            else:
                selected_girl.character "I'm confused... but I'm dreaming about your baby!"
        elif selected_girl.initial_reaction == "generous":
            if is_currently_a_mother:
                selected_girl.character "I'm confused... but I want to give you what you want and more children."
            else:
                selected_girl.character "I'm confused... but I want to give you what you want."
        elif selected_girl.initial_reaction == "neutral":
            if is_currently_a_mother:
                selected_girl.character "I'm confused... why are you bringing this up again? I'm thinking about [child_reference]."
            else:
                selected_girl.character "I'm confused... why are you bringing this up again?"
    

    # Additional dialogue based on motherhood status
    if is_currently_a_mother and selected_girl.baby_desire > 50:
        if is_base_mother and child_reference:
            selected_girl.character "I think about [child_reference] when I consider my birth control choices."
            $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 2)
        else:
            selected_girl.character "Being a mother has changed how I view my birth control choices."
            $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 1)

    # Update tracking variables
    $ selected_girl.birth_control_discussion_level = min(3, discussion_level + 1)
    $ selected_girl.previous_birth_control = currently_on_birth_control
    
    # Set reaction based on outcome
    if birth_control_changed:
        if currently_on_birth_control:
            $ selected_girl.previous_birth_control_reaction = "serious"
        else:
            $ selected_girl.previous_birth_control_reaction = "excited"
    else:
        $ selected_girl.previous_birth_control_reaction = "neutral"

    # PLAYER RESPONSE OPTIONS WITH STAT REFERENCES
    menu:
        "This aligns with my compassionate approach to relationships. \n(Need compassion >5)" if player.compassion > 5:
            player "I'm glad you've been reflecting on our previous conversation. Your well-being is important to me."
            
            if selected_girl.initial_reaction == "loving":
                if is_currently_a_mother:
                    selected_girl.character "Thank you for caring about me and [child_reference]. That means everything."
                else:
                    selected_girl.character "Thank you for caring about me. That means everything."
                $ selected_girl.apply_impacts({"affection": 40, "baby_desire": 10})
            elif selected_girl.initial_reaction == "submissive":
                if is_currently_a_mother:
                    selected_girl.character "Thank you, Master. Your consideration for me and my child means everything."
                else:
                    selected_girl.character "Thank you, Master. Your consideration means everything."
                $ selected_girl.apply_impacts({"affection": 30, "trust": 20})
            elif selected_girl.initial_reaction == "seductive":
                selected_girl.character "Mmm... a compassionate man. That's unexpectedly attractive."
                $ selected_girl.apply_impacts({"affection": 25, "corruption": 10})
            elif selected_girl.initial_reaction == "manipulative":
                if is_currently_a_mother:
                    selected_girl.character "Your compassion is noted. Remember this when I need something for [child_reference]."
                else:
                    selected_girl.character "Your compassion is noted. Remember this when I need something."
                $ selected_girl.apply_impacts({"affection": 15, "corruption": 5})
            elif selected_girl.initial_reaction == "devoted":
                if is_currently_a_mother:
                    selected_girl.character "Thank you. I'm devoted to you and caring for my child."
                else:
                    selected_girl.character "Thank you. I'm devoted to you completely."
                $ selected_girl.apply_impacts({"affection": 35, "trust": 25})
            elif selected_girl.initial_reaction == "admiring":
                selected_girl.character "I admire your compassion. It shows your strength."
                $ selected_girl.apply_impacts({"affection": 30, "intellect": 10})
            elif selected_girl.initial_reaction == "infatuated":
                if is_currently_a_mother:
                    selected_girl.character "You're so compassionate! I can't stop thinking about you and our future with [child_reference]!"
                else:
                    selected_girl.character "You're so compassionate! I can't stop thinking about you and our future!"
                $ selected_girl.apply_impacts({"affection": 45, "baby_desire": 15})
            elif selected_girl.initial_reaction == "generous":
                if is_currently_a_mother:
                    selected_girl.character "Thank you. I want to give you everything, including more children."
                else:
                    selected_girl.character "Thank you. I want to give you everything."
                $ selected_girl.apply_impacts({"affection": 35, "baby_desire": 10})
            elif selected_girl.initial_reaction == "neutral":
                if is_currently_a_mother:
                    selected_girl.character "Thank you. I appreciate you understanding my situation as a mother."
                else:
                    selected_girl.character "Thank you. I appreciate your understanding."
                $ selected_girl.apply_impacts({"affection": 20})
            
        "This demonstrates proper discipline in our relationship. \n(Need control >5)" if player.control > 5:
            player "Good. I expect you to be responsible about your reproductive choices."
            
            if selected_girl.initial_reaction == "loving":
                if is_currently_a_mother:
                    selected_girl.character "I will be. For you and for [child_reference]."
                else:
                    selected_girl.character "I will be. For you and for us."
                $ selected_girl.apply_impacts({"discipline": 30, "affection": 20})
            elif selected_girl.initial_reaction == "submissive":
                if is_currently_a_mother:
                    selected_girl.character "Yes, Master. I'll be disciplined for you and my child."
                else:
                    selected_girl.character "Yes, Master. I'll be disciplined for you."
                $ selected_girl.apply_impacts({"discipline": 40, "trust": 15})
            elif selected_girl.initial_reaction == "seductive":
                selected_girl.character "Discipline? Mmm... I like a man who takes control."
                $ selected_girl.apply_impacts({"corruption": 20, "discipline": 10})
            elif selected_girl.initial_reaction == "manipulative":
                if is_currently_a_mother:
                    selected_girl.character "Discipline costs money, Professor. Childcare isn't free, you know."
                else:
                    selected_girl.character "Discipline costs money, Professor. Birth control isn't free, you know."
                $ selected_girl.apply_impacts({"corruption": 15})
            elif selected_girl.initial_reaction == "devoted":
                if is_currently_a_mother:
                    selected_girl.character "I'll be disciplined in all things, including caring for my child."
                else:
                    selected_girl.character "I'll be disciplined in all things. Your will is my command."
                $ selected_girl.apply_impacts({"discipline": 35, "trust": 20})
            elif selected_girl.initial_reaction == "admiring":
                selected_girl.character "I admire your discipline. It shows you're a leader."
                $ selected_girl.apply_impacts({"discipline": 25, "affection": 15})
            elif selected_girl.initial_reaction == "infatuated":
                selected_girl.character "You're so disciplined! That's so attractive!"
                $ selected_girl.apply_impacts({"affection": 30, "discipline": 15})
            elif selected_girl.initial_reaction == "generous":
                if is_currently_a_mother:
                    selected_girl.character "I'll be responsible for [child_reference] and for you."
                else:
                    selected_girl.character "I'll be responsible for you."
                $ selected_girl.apply_impacts({"discipline": 20, "affection": 20})
            elif selected_girl.initial_reaction == "neutral":
                if is_currently_a_mother:
                    selected_girl.character "I understand. A mother must be disciplined."
                else:
                    selected_girl.character "I understand. I'll be more disciplined."
                $ selected_girl.apply_impacts({"discipline": 15})
            
        "This fits with my more adventurous perspective. \n(Need lust >5)" if player.lust > 5:
            player "I'm glad you're embracing the more... natural aspects of our relationship."
            
            if selected_girl.initial_reaction == "loving":
                if is_currently_a_mother:
                    selected_girl.character "I feel connected to you naturally. Even with [child_reference], I trust this."
                else:
                    selected_girl.character "I feel connected to you naturally. I trust this."
                $ selected_girl.apply_impacts({"affection": 30, "naturism": 20})
            elif selected_girl.initial_reaction == "submissive":
                if is_currently_a_mother:
                    selected_girl.character "If you want me to embrace natural things, Master, I will - even having more children."
                else:
                    selected_girl.character "If you want me to embrace natural things, Master, I will."
                $ selected_girl.apply_impacts({"corruption": 25, "trust": 10})
            elif selected_girl.initial_reaction == "seductive":
                selected_girl.character "Mmm... natural and adventurous? I like where this is going."
                $ selected_girl.apply_impacts({"corruption": 35, "affection": 20})
            elif selected_girl.initial_reaction == "manipulative":
                if is_currently_a_mother:
                    selected_girl.character "Natural? That means more babies and more support. I'm listening..."
                else:
                    selected_girl.character "Natural? That means babies and support. I'm listening..."
                $ selected_girl.apply_impacts({"corruption": 25, "baby_desire": 10})
            elif selected_girl.initial_reaction == "devoted":
                if is_currently_a_mother:
                    selected_girl.character "I'll embrace whatever you want naturally, even as a mother."
                else:
                    selected_girl.character "I'll embrace whatever you want naturally."
                $ selected_girl.apply_impacts({"corruption": 20, "trust": 15})
            elif selected_girl.initial_reaction == "admiring":
                selected_girl.character "I admire your adventurous spirit. It's exciting."
                $ selected_girl.apply_impacts({"affection": 25, "corruption": 15})
            elif selected_girl.initial_reaction == "infatuated":
                selected_girl.character "You're so adventurous! I want to try everything with you!"
                $ selected_girl.apply_impacts({"affection": 40, "corruption": 20})
            elif selected_girl.initial_reaction == "generous":
                if is_currently_a_mother:
                    selected_girl.character "I want to give you natural experiences and more children."
                else:
                    selected_girl.character "I want to give you natural experiences."
                $ selected_girl.apply_impacts({"affection": 30, "naturism": 15})
            elif selected_girl.initial_reaction == "neutral":
                if is_currently_a_mother:
                    selected_girl.character "I see. Natural things can be nice, even for a mother."
                else:
                    selected_girl.character "I see. Natural things can be nice."
                $ selected_girl.apply_impacts({"naturism": 10})
        
        "Let's discuss changing your birth control." if birth_control_changed:
            player "Let's talk about your decision regarding birth control."
            
            if currently_on_birth_control:
                # She started birth control
                if selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "I started birth control, but it's expensive. Maybe you could help with the costs for [child_reference]'s sake?"
                        
                        menu:
                            "Offer 300 for her birth control costs?":
                                if player.cash >= 300:
                                    $ player.cash -= 300
                                    $ selected_girl.apply_impacts({"corruption": 20, "affection": 15})
                                    selected_girl.character "Thank you. I'll remember this favor. Birth control isn't cheap when you're raising a child."
                                else:
                                    selected_girl.character "Don't make promises you can't keep. I'll manage somehow."
                                    $ selected_girl.apply_impacts({"affection": -20})
                            "Remind her this was her decision":
                                selected_girl.character "Fine. But don't expect me to be happy about paying for it myself."
                                $ selected_girl.apply_impacts({"affection": -10})
                            "Leave it be.":
                                selected_girl.character "Suit yourself. I'll handle my own expenses."
                                $ selected_girl.apply_impacts({"affection": -5})
                    else:
                        selected_girl.character "I started birth control, but it's expensive. Maybe you could help with the costs?"
                        
                        menu:
                            "Offer 300 for her birth control costs?":
                                if player.cash >= 300:
                                    $ player.cash -= 300
                                    $ selected_girl.apply_impacts({"corruption": 20, "affection": 15})
                                    selected_girl.character "Thank you. I'll remember this favor. Birth control isn't cheap."
                                else:
                                    selected_girl.character "Don't make promises you can't keep. I'll manage somehow."
                                    $ selected_girl.apply_impacts({"affection": -20})
                            "Remind her this was her decision":
                                selected_girl.character "Fine. But don't expect me to be happy about paying for it myself."
                                $ selected_girl.apply_impacts({"affection": -10})
                            "Leave it be.":
                                selected_girl.character "Suit yourself. I'll handle my own expenses."
                                $ selected_girl.apply_impacts({"affection": -5})
                else:
                    if selected_girl.initial_reaction == "loving":
                        if is_currently_a_mother:
                            selected_girl.character "I started birth control for us. I hope this shows how much I care about you and [child_reference]."
                        else:
                            selected_girl.character "I started birth control for us. I hope this shows how much I care."
                    elif selected_girl.initial_reaction == "submissive":
                        if is_currently_a_mother:
                            selected_girl.character "I started birth control as you commanded, Master. Does this please you?"
                        else:
                            selected_girl.character "I started birth control as you commanded, Master. Does this please you?"
                    elif selected_girl.initial_reaction == "seductive":
                        selected_girl.character "I started birth control... though I must admit, part of me misses the excitement of not knowing."
                    elif selected_girl.initial_reaction == "devoted":
                        if is_currently_a_mother:
                            selected_girl.character "I started birth control because it pleases you. My body and my child are yours to direct."
                        else:
                            selected_girl.character "I started birth control because it pleases you. My body is yours to direct."
                    elif selected_girl.initial_reaction == "admiring":
                        selected_girl.character "I started birth control. I admire how you think about planning ahead."
                    elif selected_girl.initial_reaction == "infatuated":
                        if is_currently_a_mother:
                            selected_girl.character "I started birth control because you asked... though I dream about stopping it and giving [child_reference] a sibling!"
                        else:
                            selected_girl.character "I started birth control because you asked... though I dream about stopping it and having your baby!"
                    elif selected_girl.initial_reaction == "generous":
                        if is_currently_a_mother:
                            selected_girl.character "I started birth control to be responsible, though I want to give you more children someday."
                        else:
                            selected_girl.character "I started birth control to be responsible, though I want to give you children someday."
                    elif selected_girl.initial_reaction == "neutral":
                        if is_currently_a_mother:
                            selected_girl.character "I started birth control. It seems practical for a mother."
                        else:
                            selected_girl.character "I started birth control. It seems practical."
            else:
                # She stopped birth control
                if selected_girl.initial_reaction == "manipulative":
                    if is_currently_a_mother:
                        selected_girl.character "I stopped birth control like we discussed. A baby means more support - are you ready to provide for [child_reference] and a new baby?"
                        
                        menu:
                            "Promise to support her and the baby":
                                selected_girl.character "Good. I'm holding you to that. I expect proper support for our growing family."
                                $ selected_girl.apply_impacts({"baby_desire": 30, "corruption": 20})
                            "Offer 2000 now for baby expenses":
                                if player.cash >= 2000:
                                    $ player.cash -= 2000
                                    $ selected_girl.apply_impacts({"baby_desire": 40, "corruption": 30})
                                    selected_girl.character "2000 upfront? Smart man. I knew you'd provide properly for our family."
                                else:
                                    selected_girl.character "Empty promises don't pay for diapers, Professor."
                                    $ selected_girl.apply_impacts({"affection": -25})
                            "Leave it be.":
                                selected_girl.character "Fine. But don't think I'm getting pregnant without proper support."
                                $ selected_girl.apply_impacts({"baby_desire": -20})
                    else:
                        selected_girl.character "I stopped birth control like we discussed. A baby means support - are you ready to provide for me?"
                        
                        menu:
                            "Promise to support her and the baby":
                                selected_girl.character "Good. I'm holding you to that. I expect proper support."
                                $ selected_girl.apply_impacts({"baby_desire": 30, "corruption": 20})
                            "Offer 2000 now for baby expenses":
                                if player.cash >= 2000:
                                    $ player.cash -= 2000
                                    $ selected_girl.apply_impacts({"baby_desire": 40, "corruption": 30})
                                    selected_girl.character "2000 upfront? Smart man. I knew you'd provide properly."
                                else:
                                    selected_girl.character "Empty promises don't pay for diapers, Professor."
                                    $ selected_girl.apply_impacts({"affection": -25})
                            "Leave it be.":
                                selected_girl.character "Fine. But don't think I'm getting pregnant without proper support."
                                $ selected_girl.apply_impacts({"baby_desire": -20})
                else:
                    if selected_girl.initial_reaction == "loving":
                        if is_currently_a_mother:
                            selected_girl.character "I stopped birth control for us. I'm ready to expand our family with [child_reference]."
                        else:
                            selected_girl.character "I stopped birth control for us. I'm ready to start our family."
                    elif selected_girl.initial_reaction == "submissive":
                        if is_currently_a_mother:
                            selected_girl.character "I stopped birth control as you commanded, Master. My body is ready to carry your child again."
                        else:
                            selected_girl.character "I stopped birth control as you commanded, Master. My body is ready to carry your child."
                    elif selected_girl.initial_reaction == "seductive":
                        selected_girl.character "I stopped birth control. The risk is so exciting, isn't it?"
                    elif selected_girl.initial_reaction == "devoted":
                        if is_currently_a_mother:
                            selected_girl.character "I stopped birth control to please you. My body is ready to receive your child, even as a mother."
                        else:
                            selected_girl.character "I stopped birth control to please you. My body is ready to receive your child."
                    elif selected_girl.initial_reaction == "admiring":
                        selected_girl.character "I stopped birth control. I trust your plans for our future."
                    elif selected_girl.initial_reaction == "infatuated":
                        if is_currently_a_mother:
                            selected_girl.character "I stopped birth control! I'm so excited to have your baby and give [child_reference] a sibling!"
                        else:
                            selected_girl.character "I stopped birth control! I'm so excited to have your baby!"
                    elif selected_girl.initial_reaction == "generous":
                        if is_currently_a_mother:
                            selected_girl.character "I stopped birth control. I want to give you another child to grow our family."
                        else:
                            selected_girl.character "I stopped birth control. I want to give you a child."
                    elif selected_girl.initial_reaction == "neutral":
                        if is_currently_a_mother:
                            selected_girl.character "I stopped birth control. I'm open to expanding our family."
                        else:
                            selected_girl.character "I stopped birth control. I'm open to starting a family."
    
    # Calculate and log baby_desire change
    $ baby_desire_change = selected_girl.baby_desire - previous_baby_desire
    $ renpy.log(f"Baby desire changed by {baby_desire_change} for {selected_girl.first_name}")
    
    # Track that this follow-up conversation happened
    $ actions_already_done.setdefault(selected_girl.id, []).append("birth_control_followup")
    
    # Schedule next follow-up based on discussion level
    if selected_girl.birth_control_discussion_level == 1:
        $ selected_girl.birth_control_followup = time_manager.total_days + 5
    elif selected_girl.birth_control_discussion_level == 2:
        $ selected_girl.birth_control_followup = time_manager.total_days + 7
    else:
        # At max discussion level, no more scheduled follow-ups
        $ renpy.log(f"No further birth control follow-ups scheduled for {selected_girl.first_name}")
    
    # Skip time for conversation
    $ time_manager.skip_time(minutes=5)
    
    return


#the end of file cause labels suck at collapsing :P
