#SPECIFIC CHERRY DIALOGS
# to catch mothers if not hasattr(self, "daughter"):

# Save-compat shim: redirect the old un-prefixed label name (pre-1.0.6 saves/references) instead of erroring.
label small_talk_pregnancy:
    jump vt_small_talk_pregnancy

label vt_small_talk_pregnancy:
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

 

    if not hasattr(selected_girl, "previous_pregnancy_reaction"):
        $ selected_girl.previous_pregnancy_reaction = "neutral"
    if not hasattr(selected_girl, "pregnancy_discussion_level"):
        $ selected_girl.pregnancy_discussion_level = 0
    if not hasattr(selected_girl, "pregnancy_followup"):
        $ selected_girl.pregnancy_followup = 0
        
    # TRACK CONVERSATION HISTORY
    $ has_discussed_pregnancy_before = getattr(selected_girl, "has_discussed_pregnancy_before", False)
    $ previous_pregnancy_reaction = getattr(selected_girl, "previous_pregnancy_reaction", "neutral")
    
    # # PREGNANCY DISCOVERY CHECK - JUMP TO SEPARATE LABEL IF PREGNANT AND DISCOVERY NEEDED
   
    # Simplified condition - check if she's pregnant and neither knows
    if selected_girl.pregnant and (not selected_girl.player_knows_pregnant and not selected_girl.knows_pregnant):
        $ renpy.log("CALLING vt_pregnancy_discovery")
        call vt_pregnancy_discovery from _call_vt_pregnancy_discovery
    # Check if she knows but player doesn't  
    elif selected_girl.pregnant and (not selected_girl.player_knows_pregnant and selected_girl.knows_pregnant):
        $ renpy.log("CALLING vt_pregnancy_confession")
        call vt_pregnancy_confession from _call_vt_pregnancy_confession
    else:
        $ renpy.log("No pregnancy discovery triggered - conditions not met")
  
    # CHECK FOR ACTIVE FOLLOW-UP 
    # If we have a scheduled follow-up that's ready to happen
    if hasattr(selected_girl, "has_pregnancy_followup") and selected_girl.has_pregnancy_followup and has_discussed_pregnancy_before:
        # Reset the flag so it doesn't keep appearing
        $ selected_girl.has_pregnancy_followup = False
        
        # Update tracking variables for the follow-up
        $ selected_girl.pregnancy_discussion_level = min(3, selected_girl.pregnancy_discussion_level + 1)
        
        # Show follow-up specific dialogue based on previous reaction, dominant approach, and baby_desire
        if previous_pregnancy_reaction == "positive":
            if selected_girl.baby_desire > 70:
                if selected_girl.dominant_approach == "compassionate":
                    "[selected_girl]'s eyes light up with warmth as you approach her, her hands instinctively going to her stomach as she remembers your beautiful conversation about starting a family together."
                elif selected_girl.dominant_approach == "sexualized":
                    "[selected_girl] licks her lips as you approach, a hungry look in her eyes as she clearly remembers your steamy conversation about breeding her."
                elif selected_girl.dominant_approach == "transactional":
                    "[selected_girl] gets a calculating gleam in her eye as you approach, already running numbers in her head about the profitable family business you discussed."
                elif selected_girl.dominant_approach == "dominate":
                    "[selected_girl] stands taller as you approach, her expression serious and determined as she remembers your discussion about strengthening your family line."
                else:
                    "[selected_girl]'s eyes light up as you approach her, clearly remembering your previous conversation about pregnancy."
                    
            elif selected_girl.baby_desire > 30:
                if selected_girl.dominant_approach == "compassionate":
                    "[selected_girl] smiles softly as you approach her, her expression thoughtful as she remembers your gentle conversation about pregnancy and family."
                elif selected_girl.dominant_approach == "sexualized":
                    "[selected_girl] gives you a sly smile as you approach, clearly remembering your exciting conversation about the possibilities of pregnancy."
                elif selected_girl.dominant_approach == "transactional":
                    "[selected_girl] raises an eyebrow thoughtfully as you approach, considering the practical aspects of your previous pregnancy discussion."
                elif selected_girl.dominant_approach == "dominate":
                    "[selected_girl] nods respectfully as you approach, her expression focused as she remembers your serious discussion about family planning."
                else:
                    "[selected_girl] arches a brow as you approach her, clearly remembering your previous conversation about pregnancy."
                    
            else:
                if selected_girl.dominant_approach == "compassionate":
                    "[selected_girl] gives you a gentle, slightly nervous smile as you approach, clearly trying to be positive about your previous pregnancy discussion despite her reservations."
                elif selected_girl.dominant_approach == "sexualized":
                    "[selected_girl] forces a smile as you approach, clearly remembering your pregnancy talk but trying to act enthusiastic even though she's not really feeling it."
                elif selected_girl.dominant_approach == "transactional":
                    "[selected_girl] looks thoughtful as you approach, trying to see the business value in your pregnancy discussion despite her low interest."
                elif selected_girl.dominant_approach == "dominate":
                    "[selected_girl] maintains a neutral expression as you approach, logically processing your pregnancy discussion despite her lack of personal investment."
                else:
                    "[selected_girl] gives a small smile as you approach her, clearly remembering your previous conversation about pregnancy."
                    
        elif previous_pregnancy_reaction == "negative":
            if selected_girl.baby_desire > 50:
                # High baby desire but negative reaction = conflicted
                if selected_girl.dominant_approach == "compassionate":
                    "[selected_girl] looks conflicted as you approach, her expression a mix of longing and fear as she remembers your difficult pregnancy discussion."
                elif selected_girl.dominant_approach == "sexualized":
                    "[selected_girl] bites her lip as you approach, clearly torn between wanting babies and being scared by your pregnancy discussion."
                elif selected_girl.dominant_approach == "transactional":
                    "[selected_girl] looks frustrated as you approach, struggling between the logical benefits of children and the emotional costs you discussed."
                elif selected_girl.dominant_approach == "dominate":
                    "[selected_girl] looks tense as you approach, her mind at war with her body's desires over your pregnancy discussion."
                else:
                    "[selected_girl]'s eyes narrow a bit as you approach her, clearly remembering your previous conversation about pregnancy."
                    
            else:
                # Low baby desire and negative reaction = resistant
                if selected_girl.dominant_approach == "compassionate":
                    "[selected_girl] looks hurt as you approach, clearly remembering your painful pregnancy discussion and wishing you wouldn't bring it up again."
                elif selected_girl.dominant_approach == "sexualized":
                    "[selected_girl] rolls her eyes dramatically as you approach, clearly annoyed that you're bringing up the boring pregnancy topic again."
                elif selected_girl.dominant_approach == "transactional":
                    "[selected_girl] looks impatient as you approach, clearly viewing your follow-up as a waste of time and resources."
                elif selected_girl.dominant_approach == "dominate":
                    "[selected_girl] stiffens defensively as you approach, her expression cold as she remembers your unwanted pregnancy discussion."
                else:
                    "[selected_girl]'s eyes narrow a bit, and she sighs as you approach her, clearly remembering your previous conversation about pregnancy."
                    
        else:  # neutral reaction
            if selected_girl.baby_desire > 60:
                if selected_girl.dominant_approach == "compassionate":
                    "[selected_girl] looks thoughtful as you approach, clearly considering your previous pregnancy discussion with growing interest."
                elif selected_girl.dominant_approach == "sexualized":
                    "[selected_girl] gives you a curious look as you approach, clearly warming up to the idea of pregnancy after your last talk."
                elif selected_girl.dominant_approach == "transactional":
                    "[selected_girl] looks calculating as you approach, clearly seeing new possibilities in your pregnancy discussion."
                elif selected_girl.dominant_approach == "dominate":
                    "[selected_girl] looks considering as you approach, clearly evaluating your pregnancy discussion from a logical perspective."
                else:
                    "[selected_girl] arches a brow as you approach her, clearly remembering your previous conversation about pregnancy."
                    
            elif selected_girl.baby_desire < 30:
                if selected_girl.dominant_approach == "compassionate":
                    "[selected_girl] looks hesitant as you approach, clearly unsure how to feel about your previous pregnancy discussion."
                elif selected_girl.dominant_approach == "sexualized":
                    "[selected_girl] looks bored as you approach, clearly unimpressed by your pregnancy talk but trying to be polite."
                elif selected_girl.dominant_approach == "transactional":
                    "[selected_girl] looks unimpressed as you approach, clearly seeing no value in following up on your pregnancy discussion."
                elif selected_girl.dominant_approach == "dominate":
                    "[selected_girl] looks indifferent as you approach, clearly viewing your pregnancy discussion as irrelevant to her goals."
                else:
                    "[selected_girl] arches a brow as you approach her, clearly remembering your previous conversation about pregnancy."
                    
            else:
                if selected_girl.dominant_approach == "compassionate":
                    "[selected_girl] gives you a neutral, thoughtful look as you approach, clearly processing your previous pregnancy discussion."
                elif selected_girl.dominant_approach == "sexualized":
                    "[selected_girl] gives you a curious look as you approach, clearly wondering what direction your pregnancy talk will take this time."
                elif selected_girl.dominant_approach == "transactional":
                    "[selected_girl] looks analytical as you approach, clearly weighing the pros and cons of your pregnancy discussion."
                elif selected_girl.dominant_approach == "dominate":
                    "[selected_girl] looks assessing as you approach, clearly evaluating the merits of continuing your pregnancy discussion."
                else:
                    "[selected_girl] arches a brow as you approach her, clearly remembering your previous conversation about pregnancy."
        
        # Call the actual follow-up dialogue
        call vt_small_talk_pregnancy_followup from _call_vt_small_talk_pregnancy_followup
        
        # Exit after follow-up completes
        return

    # INITIAL GREETING - CHARACTER-APPROPRIATE WITH MEMORY
    "You approach [selected_girl] to discuss pregnancy and family matters."

    if has_discussed_pregnancy_before:
        if previous_pregnancy_reaction == "positive":
            if selected_girl.baby_desire > 70:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "You wanted to talk more about pregnancy? I've been dreaming about nothing but having your babies!"
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Back to talk about making babies? I've been touching myself thinking about you breeding me..."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "You want to discuss pregnancy again? I've been calculating the financial benefits of having your children..."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "You wish to continue our pregnancy discussion. I have been preparing my body for more of your children."
                else:
                    selected_girl.character "You wanted to talk more about pregnancy? I've been thinking about what we discussed..."
            elif selected_girl.baby_desire > 30:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "You wanted to talk more about pregnancy? I've been thinking about what we discussed... it's nice to think about."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Back to pregnancy talk? I've been wondering what it would feel like to carry your baby..."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "You want to discuss pregnancy again? I've been considering the practical aspects of what we talked about."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "You wish to continue our pregnancy discussion. I have been preparing my thoughts on the matter."
                else:
                    selected_girl.character "You wanted to talk more about pregnancy? I've been thinking about what we discussed..."
            else:
                if selected_girl.dominant_approach == "dominate":
                    selected_girl.character "We've already addressed this topic. I found our previous discussion sufficient."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "Back to this topic? I've already established my position. Unless you have new terms to offer..."
                elif selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "I... I'm still not comfortable discussing this. Can we talk about something else?"
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Ugh, this again? I thought we were done with the boring pregnancy talk."
                else:
                    selected_girl.character "Back to this topic again? I thought we already covered everything I'm comfortable sharing..."
                    
        elif previous_pregnancy_reaction == "negative":
            if selected_girl.baby_desire > 50:
                # High baby desire but negative reaction = conflicted
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "I know I should want to talk about this... and part of me does, but I'm scared..."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "I want to want this... but the reality is kind of terrifying, you know?"
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "Logically I see the benefits, but emotionally... I'm not ready to commit yet."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "I understand the biological imperative, but I am not prepared for this discussion."
                else:
                    selected_girl.character "Back to this topic again? I'm still not sure how I feel about it..."
            else:
                # Low baby desire and negative reaction = resistant
                if selected_girl.dominant_approach == "dominate":
                    selected_girl.character "We've already addressed this topic. I found our previous discussion sufficient."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "Back to this topic? I've already established my position. Unless you have new terms to offer..."
                elif selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "I... I'm still not comfortable discussing this. Can we talk about something else?"
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Ugh, pregnancy again? Can't we talk about something fun?"
                else:
                    selected_girl.character "Back to this topic again? I thought we already covered everything I'm comfortable sharing..."
        else:
            if selected_girl.baby_desire > 60:
                if selected_girl.dominant_approach == "transactional":
                    selected_girl.character "You wish to discuss pregnancy again? Very well, but make it worth my time - I want to hear your plans for our family."
                elif selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "You want to talk about pregnancy again? I'll listen... I've been hoping you'd bring this up again!"
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "Proceed with your pregnancy discussion. I am prepared to consider this seriously."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Pregnancy talk again? Good... I've been wanting to discuss you knocking me up."
                else:
                    selected_girl.character "You wanted to talk about pregnancy again? I'm listening..."
            elif selected_girl.baby_desire < 30:
                if selected_girl.dominant_approach == "transactional":
                    selected_girl.character "You wish to discuss pregnancy again? This seems like a waste of time unless you have something new to offer."
                elif selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "You want to talk about pregnancy again? I... I'd rather not, but I'll listen if you insist."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "Proceed with your pregnancy discussion, though I fail to see its importance."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Pregnancy talk again? Really? Can't we talk about something actually exciting?"
                else:
                    selected_girl.character "You wanted to talk about pregnancy again? If we must..."
            else:
                if selected_girl.dominant_approach == "transactional":
                    selected_girl.character "You wish to discuss pregnancy again? Very well, but make it worth my time."
                elif selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "You want to talk about pregnancy again? I'll listen... I want to understand."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "Proceed with your pregnancy discussion. I am prepared to listen."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Pregnancy talk again? Hmm... okay, but let's make it interesting this time."
                else:
                    selected_girl.character "You wanted to talk about pregnancy again? I'm listening..."
    else:
        $ selected_girl.has_discussed_pregnancy_before = True

    # ROLE-BASED OPENINGS WITH BABY DESIRE INTEGRATION
    if is_base_mother:
        if selected_girl.pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player":
            if kids_with_player > 0:
                if selected_girl.baby_desire > 80:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "As a mother who's been through this before, and carrying your child again... I recognize these symptoms and my heart is so full! Another baby with you!"
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "My body knows this feeling well... being pregnant with your baby again is making me so horny! I can't wait to have more!"
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "As an experienced mother carrying your second child, I recognize these symptoms. Our family is growing - we'll need to discuss expanded financial support."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "I have been through this before and recognize the symptoms. My body is prepared for this pregnancy, and I am ready to expand our family."
                    else:
                        selected_girl.character "As a mother who's been through this before, I recognize these symptoms..."
                elif selected_girl.baby_desire > 40:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "As a mother who's been through this before, I recognize these symptoms... having another baby with you is wonderful."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "My body knows this feeling well... being pregnant with your baby again is pretty exciting..."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "As an experienced mother carrying your second child, I recognize these symptoms. This will require additional resources."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "I have been through this before and recognize the symptoms. I am prepared to handle this pregnancy."
                    else:
                        selected_girl.character "As a mother who's been through this before, I recognize these symptoms..."
                else:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "As a mother who's been through this before, I recognize these symptoms... though I'm nervous about having another baby so soon."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "My body knows this feeling... another baby? I'm still getting used to the first one..."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "As an experienced mother, I recognize these symptoms. Another child will significantly impact our finances."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "I recognize these symptoms from my previous pregnancy. This will require additional preparation."
                    else:
                        selected_girl.character "As a mother who's been through this before, I recognize these symptoms..."
            else:
                if selected_girl.baby_desire > 70:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "As a mother, I understand pregnancy well... and carrying your child? This is the family I've always dreamed of!"
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "I know all about pregnancy... but being pregnant with YOUR baby? That's the hottest thing that's ever happened to me!"
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "As a mother, I understand pregnancy well. Since you're the father, this child represents a significant investment in our future."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "I am experienced with pregnancy. This child with you is a logical next step for our relationship."
                    else:
                        selected_girl.character "As a mother, I understand pregnancy well... though I wasn't expecting it with you."
                elif selected_girl.baby_desire > 30:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "As a mother, I understand pregnancy well... carrying your child is a new journey I'm excited to take with you."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "I know all about pregnancy... being pregnant with YOUR baby? That's pretty exciting..."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "As a mother, I understand pregnancy well. Since you're the father, we'll need to discuss financial arrangements."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "I am experienced with pregnancy. This child with you is unexpected, but I am prepared to handle it."
                    else:
                        selected_girl.character "As a mother, I understand pregnancy well... though I wasn't expecting it with you."
                else:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "As a mother, I understand pregnancy well... though I wasn't expecting another baby right now."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "I know all about pregnancy... another baby? I just got used to not being pregnant..."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "As a mother, I understand the financial burden of pregnancy. This timing is not optimal."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "I am experienced with pregnancy. This child with you presents logistical challenges."
                    else:
                        selected_girl.character "As a mother, I understand pregnancy well... though I wasn't expecting it with you."
        else:
            if selected_girl.baby_desire > 70:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "As a mother, I understand pregnancy is a beautiful journey... I'd love to have more babies with you!"
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "As a mother, I know how amazing pregnancy can be... my body changing, growing new life... I want to do it again with you!"
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "As a mother, I understand the benefits of expanding our family. What are you offering for another child?"
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "As a mother, I have experience with pregnancy. I am prepared to have more of your children."
                else:
                    selected_girl.character "As a mother, I understand pregnancy well. It's important to be prepared."
            elif selected_girl.baby_desire > 30:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "As a mother, I understand pregnancy is a beautiful journey. It's important to be prepared with love and support."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "As a mother, I know how amazing pregnancy can be... my body changing, growing new life... it's incredible."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "As a mother, I understand the practical aspects of pregnancy. It's important to be prepared financially."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "As a mother, I have experience with pregnancy. Proper preparation is essential for success."
                else:
                    selected_girl.character "As a mother, I understand pregnancy well. It's important to be prepared."
            else:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "As a mother, I understand pregnancy... but I'm not sure I want to go through it again anytime soon."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "As a mother, I know pregnancy... and honestly? I'm enjoying my freedom right now."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "As a mother, I understand the costs of pregnancy. Another child is not in my current financial plan."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "As a mother, I have completed my pregnancy duties. I am not prepared for another at this time."
                else:
                    selected_girl.character "As a mother, I understand pregnancy well... but I'm not looking to have more right now."

    elif is_student:
        if selected_girl.pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player":
            if kids_with_player > 0:
                if selected_girl.baby_desire > 70:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "Being a mother with you is still new to me... but I love it! I can't wait to have more of your babies!"
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "Being your baby mama is so hot... I love having your baby inside me! When are you knocking me up again?"
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "Motherhood with you is an ongoing arrangement. I'm ready to discuss expanding our family contract."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "I am adapting to motherhood with you. I am prepared to discuss having more of your children."
                    else:
                        selected_girl.character "Being a mother with you is still new to me..."
                elif selected_girl.baby_desire > 30:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "Being a mother with you is still new to me... but I'm learning to love this journey we're on together."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "Being your baby mama is pretty hot... still getting used to it, but I love how my body looks."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "Motherhood with you is an ongoing arrangement. What aspect of our agreement did you want to discuss?"
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "I am adapting to motherhood with you. What requires discussion?"
                    else:
                        selected_girl.character "Being a mother with you is still new to me..."
                else:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "Being a mother is still new to me... I'm trying my best, but it's overwhelming sometimes."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "Being a mom is... a lot of work. I miss my freedom sometimes."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "Motherhood is more expensive than I calculated. We need to renegotiate our terms."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "Motherhood requires significant resources. I am managing, but it is challenging."
                    else:
                        selected_girl.character "Being a mother with you is still new to me..."
            else:
                if selected_girl.baby_desire > 70:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "Pregnancy? I'm carrying your child! This is the most wonderful thing that's ever happened to me!"
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "Pregnancy? Oh, you mean your baby growing inside me? Yeah, I can't stop thinking about how hot this is!"
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "Pregnancy? Yes, I'm carrying your child. This represents a significant increase in my value. What are you offering?"
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "Pregnancy. I am carrying your child. This is a logical development of our relationship."
                    else:
                        selected_girl.character "Pregnancy? That's... quite a topic to bring up, sir."
                elif selected_girl.baby_desire > 30:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "Pregnancy? That's... quite a topic, Professor. I'm carrying your child... it's overwhelming but amazing."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "Pregnancy? Oh, you mean your baby growing inside me? Yeah, that's pretty hot to talk about..."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "Pregnancy? Yes, I'm carrying your child. This will require renegotiation of our current arrangement."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "Pregnancy. I am carrying your child. State the purpose of this discussion."
                    else:
                        selected_girl.character "Pregnancy? That's... quite a topic to bring up, sir."
                else:
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "Pregnancy? I'm carrying your child... I'm scared, but I'll try to be strong..."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "Pregnancy? Ugh, my body's changing and I feel weird... this isn't as sexy as I thought it'd be."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "Pregnancy? Yes, I'm carrying your child. This complicates my future plans significantly."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "Pregnancy. I am carrying your child. This presents significant challenges to my goals."
                    else:
                        selected_girl.character "Pregnancy? That's... quite a topic to bring up, sir."
        else:
            if selected_girl.baby_desire > 70:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "Pregnancy? That's... a serious topic, Professor. I've been dreaming about having your babies!"
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Pregnancy? Ooh, are we talking about the risk of it? I've been fantasizing about you knocking me up!"
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "Pregnancy? That's a significant investment opportunity. What are the terms and benefits you're proposing?"
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "Pregnancy is a biological function. I am prepared to discuss carrying your children."
                else:
                    selected_girl.character "Pregnancy? That's... quite a topic to bring up, sir."
            elif selected_girl.baby_desire > 30:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "Pregnancy? That's... a serious topic, Professor. I've thought about what it would mean to start a family someday."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Pregnancy? Ooh, are we talking about the risk of it? That's kind of exciting..."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "Pregnancy? That's a significant life decision. What are the terms and benefits you're proposing?"
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "Pregnancy is a biological function. What is your question about it?"
                else:
                    selected_girl.character "Pregnancy? That's... quite a topic to bring up, sir."
            else:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "Pregnancy? I... I'm not really thinking about that right now. I have other priorities."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Pregnancy? Ew, no thanks. I'm not ruining my figure for a baby."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "Pregnancy? The costs outweigh the benefits at this point in my life. Not interested."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "Pregnancy would interfere with my goals. This discussion is not productive."
                else:
                    selected_girl.character "Pregnancy? That's... quite a topic to bring up, sir."
    
    # Phase 1: General talk about pregnancy
    if not selected_girl.pregnant or not (selected_girl.player_knows_pregnant and selected_girl.knows_pregnant):
        player.character "What are your thoughts on pregnancy in general?"

        # Response based on dominant_approach with role context
        if selected_girl.dominant_approach == "compassionate":
            if is_base_mother:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? As a mother, I find it to be the most profound experience. Creating a new life, especially a child that's ours... it's a beautiful, fulfilling journey that I would happily take again."
                    else:
                        selected_girl.character "My thoughts? Well, as a mother, I know it's a life-changing event. It's incredibly rewarding, but also demanding. I think we have to be careful and thoughtful about bringing another child into our family."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts on pregnancy? As an experienced mother, I believe it's a woman's greatest purpose. It's a beautiful, powerful experience that creates an unbreakable bond. I've always loved being a mother."
                    else:
                        selected_girl.character "My thoughts? As an experienced mother, I know it's a profound responsibility. It changes your body and your life completely. It's a blessing, but one that requires immense commitment and stability."
            elif is_student:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts on pregnancy? Honestly? I think it's the most romantic thing in the world. Carrying your child, feeling our family grow... it's an experience that has changed me for the better."
                    else:
                        selected_girl.character "My thoughts? It's... a lot. It's beautiful to have our child, but it's also terrifying as a student. I'm constantly balancing being a mother with my studies. It's not easy."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I think it's the most romantic thing in the world. The idea of carrying a child, feeling my body change to nurture a new life... it feels like the ultimate expression of love."
                    else:
                        selected_girl.character "My thoughts? It's... a lot. The idea of carrying a child is beautiful, but as a student, it's also terrifying. I'm not sure how I'd balance it all."
            else:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts on pregnancy? I think it's the most beautiful experience. Carrying your child, feeling our family grow... it's an experience that has changed me for the better."
                    else:
                        selected_girl.character "My thoughts? It's... a lot. It's beautiful to have our child, but it's also a huge responsibility. It changes everything."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I think it's the most beautiful experience. The idea of carrying a child, feeling my body change to nurture a new life... it feels like the ultimate expression of love."
                    else:
                        selected_girl.character "My thoughts? It's... a lot. The idea of carrying a child is beautiful, but it's also a huge responsibility. I'm not sure how I'd handle it."

        elif selected_girl.dominant_approach == "sexualized":
            if is_base_mother:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I think pregnancy is incredibly sexy. The swollen belly, knowing you're the one who bred me... it's a huge turn-on. I loved feeling my body change for our child."
                    else:
                        selected_girl.character "My thoughts? It has its sexy moments, for sure. But the sleepless nights and the toll on your body... it takes a lot out of you. It's not all fun and games."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I think pregnancy is incredibly sexy. The swollen belly, the bigger breasts... it's a huge turn-on. I loved feeling my body change to carry a child."
                    else:
                        selected_girl.character "My thoughts? It has its sexy moments, for sure. But the toll on your body... it takes a lot out of you. It's not all fun and games."
            elif is_student:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? It's so hot. Knowing you put a baby in me, seeing my body get all swollen and full... it's the sexiest I've ever felt. I'd do it again."
                    else:
                        selected_girl.character "My thoughts? It can be sexy, but it's also hard. I'm scared of getting fat again and losing my figure, especially with all the studying I have to do."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I think it's so hot. The idea of my body swelling with your baby, getting all full and round... it's the sexiest thing I can imagine."
                    else:
                        selected_girl.character "My thoughts? It could be sexy, but I'm scared of getting fat and losing my figure. I'm not ready to give up my body like that yet."
            else:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I think pregnancy is incredibly sexy. The swollen belly, knowing you're the one who bred me again... it's a huge turn-on. I loved feeling my body change for our child."
                    else:
                        selected_girl.character "My thoughts? It has its sexy moments, for sure. But the toll on your body... it takes a lot out of you. It's not all fun and games."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I think pregnancy is incredibly sexy. The idea of my body swelling with your baby, getting all full and round... it's the sexiest thing I can imagine."
                    else:
                        selected_girl.character "My thoughts? It could be sexy, but I'm scared of getting fat and losing my figure. I'm not ready to give up my body like that yet."

        elif selected_girl.dominant_approach == "transactional":
            if is_base_mother:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? As a mother, I see it as a long-term investment. It's incredibly rewarding, but it's also an 18-year financial commitment. A family is a business, and it requires capital to run smoothly."
                    else:
                        selected_girl.character "My thoughts? It's a massive financial and physical undertaking. The rewards are emotional, but the costs are very real. You can't put a price on a child, but you absolutely have to plan for the expense."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? As a mother, I see it as a long-term investment. It's incredibly rewarding, but it's also an 18-year financial commitment. A family is a business, and it requires capital to start."
                    else:
                        selected_girl.character "My thoughts? It's a massive financial and physical undertaking. The rewards are emotional, but the costs are very real. You can't put a price on a child, but you absolutely have to plan for the expense."
            elif is_student:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? As a student, it's a huge risk and a potential reward. Having a child can secure your future, but it can also derail it. It's all about what you can get out of the deal."
                    else:
                        selected_girl.character "My thoughts? It's a huge financial burden, especially for a student. It's an 18-year contract that can destroy your future prospects if you're not careful. The costs outweigh the benefits right now."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? As a student, it's a huge risk and a potential reward. Having a child can secure your future, but it can also derail it. It's all about what you can get out of the deal."
                    else:
                        selected_girl.character "My thoughts? It's a huge financial burden, especially for a student. It's an 18-year contract that can destroy your future prospects if you're not careful. The costs outweigh the benefits right now."
            else:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? It's a long-term investment. It's incredibly rewarding, but it's also an 18-year financial commitment. A family is a business, and it requires capital to run smoothly."
                    else:
                        selected_girl.character "My thoughts? It's a massive financial and physical undertaking. The rewards are emotional, but the costs are very real. You can't put a price on a child, but you absolutely have to plan for the expense."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? It's a long-term investment. It's incredibly rewarding, but it's also an 18-year financial commitment. A family is a business, and it requires capital to start."
                    else:
                        selected_girl.character "My thoughts? It's a massive financial and physical undertaking. The rewards are emotional, but the costs are very real. You can't put a price on a child, but you absolutely have to plan for the expense."

        elif selected_girl.dominant_approach == "dominate":
            if is_base_mother:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I believe it is a woman's highest calling and purpose. To be chosen to carry a man's child, to create a family for him... it is the greatest honor. I am proud to have done it for you."
                    else:
                        selected_girl.character "My thoughts? It is a duty. A woman's body is meant for it, and it is an honor to bear children for the man she serves. It is a demanding but necessary role."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I believe it is a woman's highest calling and purpose. To be chosen to carry a man's child, to create a family for him... it is the greatest honor. I hope to fulfill that purpose again."
                    else:
                        selected_girl.character "My thoughts? It is a duty. A woman's body is meant for it, and it is an honor to bear children for the man she serves. It is a demanding but necessary role."
            elif is_student:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I believe it is my purpose as a woman to serve you in this way. To carry your child and give you a family is the greatest fulfillment I can imagine. I am proud to have done it."
                    else:
                        selected_girl.character "My thoughts? It is my duty to you. If you wish for me to carry your children, I will. My purpose is to please you, and this is a fundamental way to do so."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I believe it is my purpose as a woman to serve you in this way. To carry your child and give you a family is the greatest fulfillment I can imagine."
                    else:
                        selected_girl.character "My thoughts? It is my duty to you. If you wish for me to carry your children, I will. My purpose is to please you, and this is a fundamental way to do so."
            else:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I believe it is a woman's highest calling and purpose. To be chosen to carry a man's child, to create a family for him... it is the greatest honor. I am proud to have done it for you."
                    else:
                        selected_girl.character "My thoughts? It is a duty. A woman's body is meant for it, and it is an honor to bear children for the man she serves. It is a demanding but necessary role."
                else:
                    if selected_girl.baby_desire > 70:
                        selected_girl.character "My thoughts? I believe it is a woman's highest calling and purpose. To be chosen to carry a man's child, to create a family for him... it is the greatest honor."
                    else:
                        selected_girl.character "My thoughts? It is a duty. A woman's body is meant for it, and it is an honor to bear children for the man she serves. It is a demanding but necessary role."

        else: # neutral or other approaches
            if is_base_mother:
                if selected_girl.kids_with_player > 0:
                    selected_girl.character "My thoughts? As a mother, it's... complicated. It changes everything. It's the hardest thing I've ever done, but also the most meaningful. I'm not sure I'm ready to go through it all again right now."
                else:
                    selected_girl.character "My thoughts? As a mother, it's... complicated. It changes everything. It's the hardest thing I've ever done, but also the most meaningful. It's not something to be taken lightly."
            elif is_student:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.intellect > 70:
                        selected_girl.character "My thoughts? From a biological perspective, experiencing another pregnancy is fascinating. The cellular development, hormonal changes... it's quite remarkable to witness from the inside."
                    elif selected_girl.fear > 70:
                        selected_girl.character "My thoughts? I try not to think about another one. It was scary enough the first time, and now with our child to care for... it's a lot to handle as a student."
                    else:
                        selected_girl.character "My thoughts? I don't know much about having another one, to be honest. It seems both amazing and terrifying, especially while we're already raising a child."
                else:
                    if selected_girl.intellect > 70:
                        selected_girl.character "My thoughts? From a biological perspective, pregnancy is fascinating. The cellular development, hormonal changes... it's quite remarkable."
                    elif selected_girl.fear > 70:
                        selected_girl.character "My thoughts? I try not to think about it. It's scary to imagine my body changing like that while I'm trying to study."
                    else:
                        selected_girl.character "My thoughts? I don't know much about it, to be honest. It seems both amazing and terrifying."
            else:
                if selected_girl.kids_with_player > 0:
                    if selected_girl.intellect > 70:
                        selected_girl.character "My thoughts? From a biological perspective, experiencing another pregnancy is fascinating. The cellular development, hormonal changes... it's quite remarkable to witness from the inside."
                    elif selected_girl.fear > 70:
                        selected_girl.character "My thoughts? I try not to think about another one. It was scary enough the first time."
                    else:
                        selected_girl.character "My thoughts? I don't know much about having another one, to be honest. It seems both amazing and terrifying."
                else:
                    if selected_girl.intellect > 70:
                        selected_girl.character "My thoughts? From a biological perspective, pregnancy is fascinating. The cellular development, hormonal changes... it's quite remarkable."
                    elif selected_girl.fear > 70:
                        selected_girl.character "My thoughts? I try not to think about it. It's scary to imagine my body changing like that."
                    else:
                        selected_girl.character "My thoughts? I don't know much about it, to be honest. It seems both amazing and terrifying."

    # PHASE 2: CONDOM & BIRTH CONTROL DISCUSSION (COMPLETE INTEGRATION)
    player.character "Can we talk about protection and birth control?"

    if selected_girl.dominant_approach == "compassionate":
        if is_base_mother: # 30+ Woman, confident and experienced
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Of course. As a mother, I know that protecting our family's future is a joint responsibility. I'm glad you're bringing this up so we can make decisions together."
            else:
                selected_girl.character "I appreciate you asking. It's a sign of maturity and respect. As a woman with experience, I know how vital these conversations are. I'm happy to share my perspective with you."
        elif is_student: # Teen, naive and deferential to professor
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Okay, Professor. I'm a little nervous talking about this, but since we have our child, I know we have to be responsible grown-ups for them. I'll listen."
            else:
                selected_girl.character "Oh! Um, okay. That's... a very serious topic. I think it's good you're bringing it up, Professor. It makes me feel like you really care. I can try to talk about it."
        else: # 18-25, young adult but not naive
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Of course. Since we have a child together, it's really important we're on the same page about this. I want to make sure we're both secure in our plan."
            else:
                selected_girl.character "Yeah, of course. I'm glad you're being direct about this. It's an important conversation to have, and I'm ready to talk about it like adults."

    elif selected_girl.dominant_approach == "sexualized":
        if is_base_mother: # 30+ Woman, confident and in control of her sexuality
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Mmm, protection? After you've already given me a child? I find it incredibly thrilling that you want to discuss the... risks... we're taking now. It feels so naughty."
            else:
                selected_girl.character "What a deliciously serious topic. An experienced woman like me finds that the most exciting things in life often require a... lack of protection. Let's discuss what you're really proposing."
        elif is_student: # Teen, exploring newfound sexuality, easily flustered/excited
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Protection? Hehe... we weren't very careful before, were we, Professor? It's kind of hot to talk about all the... rules... we broke. It makes me blush."
            else:
                selected_girl.character "Wow, Professor... you want to talk about... that? No one's ever talked to me about it so... directly. It's a little scary but also... kind of exciting. My heart is beating so fast."
        else: # 18-25, confident in her sexuality but less experienced than the mother
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Protection? After we already made a baby? That's pretty hot, you know. Talking about being safe now feels like we're just playing a game. What are the rules this time?"
            else:
                selected_girl.character "Protection... I like that you're not afraid to talk about it. It can be a really sexy topic, you know? All about control and temptation. I'm intrigued."

    elif selected_girl.dominant_approach == "transactional":
        if is_base_mother: # 30+ Woman, knows her value and negotiates from a position of strength
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Protection and birth control? For our family? My preferences for our future have significant value. This is a negotiation, Professor. What are you offering for my consideration and cooperation?"
            else:
                selected_girl.character "Let's be clear. My body, my experience, and my preferences are assets. This conversation has a cost. If you want my input on something so critical, you need to make it worth my while. What's your offer?"
        elif is_student: # Teen, sees value but is unsure how to leverage it, looks to authority figure
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Um... okay. Since we have a baby, I know this is important for them. But... what do I get for talking about this? I don't really know what to ask for, Professor."
            else:
                selected_girl.character "Protection and birth control? I... I don't really know what this is worth? Is it something I'm supposed to get something for? What are you offering, Professor?"
        else: # 18-25, transactional but more direct and less naive than the student
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Okay, let's talk business. For our family, my cooperation isn't free. What's in it for me if we agree on a plan? I need to know what I'm getting out of this."
            else:
                selected_girl.character "Alright, let's cut to it. My preferences on this aren't up for debate without an incentive. If you want me to agree to your terms, you need to bring something to the table. What are you offering?"

    elif selected_girl.dominant_approach == "dominate":
        if is_base_mother: # 30+ Woman, commanding and in control
            if selected_girl.kids_with_player > 0:
                selected_girl.character "You will proceed. As the mother of your child, I will hear your plan for our family's future. You will present it clearly, and I will then render my decision."
            else:
                selected_girl.character "You have my attention. Do not waste it. State your purpose for this discussion, Professor. I will evaluate your words and tell you what I will accept."
        elif is_student: # Teen, submissive but trying to act strong, deference to professor is key
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Yes, Professor. For our child, I know we must. You should tell me what you want to do, and I will listen. I want to do what's right for our family."
            else:
                selected_girl.character "You... you can talk, Professor. I will listen. I want to be strong and handle this, but I don't know what to do. I will follow your lead."
        else: # 18-25, assertive and in control, but without the life experience of the mother
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Fine. Let's talk. For our child's sake, I'll hear you out. But make no mistake, my opinion is not a suggestion. We will do what I decide is best."
            else:
                selected_girl.character "Go ahead. I'm listening. You can state your case, but don't expect me to just agree. I have my own mind, and I'll make my own decision on this."

    else: # Fallback to original personality-based responses, now with context
        if is_base_mother: # 30+ Woman
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Of course. As a mother, being responsible for our family's future is my priority. Let's discuss it calmly."
            else:
                selected_girl.character "Of course. It's an important topic, and I'm an adult. We can have a mature conversation about it."
        elif is_student: # Teen
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Okay, Professor. I'm still learning how to be a mom, so if you think we should talk about this, we should. I trust you."
            else:
                if selected_girl.intellect > 70:
                    selected_girl.character "Yes, Professor. I've read about it in health class. It's important for preventing STIs and planning for the future. I can discuss the academic points."
                elif selected_girl.corruption > 60:
                    selected_girl.character "Hehe, protection? Is that what all the cool kids are talking about with their professors? I'm sure we can figure something out..."
                elif selected_girl.fear > 70:
                    selected_girl.character "I... I don't know, Professor. My parents would kill me if they knew we were talking about this. It's scary."
                else:
                    selected_girl.character "I guess so. I don't really know anything about it, but you're the professor, so you must know what's best."
        else: # 18-25
            if selected_girl.kids_with_player > 0:
                selected_girl.character "Yeah, we should. We have a kid now, so we can't just mess around. We need to be smart."
            else:
                if selected_girl.intellect > 70:
                    selected_girl.character "Certainly. It's a matter of public health and personal autonomy. I'm prepared for a logical discussion."
                elif selected_girl.corruption > 60:
                    selected_girl.character "Protection? Sounds like you're trying to plan something fun. I'm listening."
                elif selected_girl.fear > 70:
                    selected_girl.character "It's a bit of a heavy topic, isn't it? It makes me anxious, but I understand we need to talk."
                else:
                    selected_girl.character "Sure, we can talk. It's a normal part of life, right? What's on your mind?"
    
    menu:
        # VAGINAL CONDOM PREFERENCES
        "What are your thoughts on condoms for vaginal sex?": 
            player.character "What are your thoughts on condoms for vaginal sex?"
            # Response based on dominant_approach, role, and pregnancy context
            $ selected_girl.player_knows_vaginal_condom = True
            if selected_girl.pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player": # Already pregnant with player's baby
                $ selected_girl.wants_vaginal_condom = False
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm already carrying your next baby, and we have our child. As an experienced mother, my body is yours. We don't need that barrier between us anymore."
                        else:
                            selected_girl.character "I'm already carrying your baby. As an experienced mother, I know my body can handle this. We don't need that barrier between us anymore."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm already carrying your next baby, Professor! And we have our other one... so I guess we really don't need condoms anymore, do we? That's... kind of amazing!"
                        else:
                            selected_girl.character "I'm already carrying your baby, Professor! Wow... so I guess we don't need condoms anymore, right? That's... kind of amazing!"
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm already carrying your next baby, and we have our child. I want to feel you completely, with nothing between us. Our connection is deeper than ever now."
                        else:
                            selected_girl.character "I'm already carrying your baby. I want to feel you completely, with nothing between us. It's a special kind of intimacy now."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm pregnant with your next baby! An experienced mother like me being bare again, knowing we've already made a child... feeling you cum inside me while I'm carrying our next is the hottest thing I've ever felt!"
                        else:
                            selected_girl.character "I'm pregnant with your baby! An experienced woman like me being bare... feeling you cum inside me while carrying your child is the hottest thing I've ever felt."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm pregnant with your next baby! Oh my god, you can cum inside me with no condom again! We have our other one, and now this... it's so... wow!"
                        else:
                            selected_girl.character "I'm pregnant with your baby! Oh my god, you can cum inside me with no condom! That's so... wow, I didn't even think about that! It feels so naughty!"
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm pregnant with your next baby! Of course I want you bare. Feeling you cum inside me again while I'm carrying our child, knowing we made one before... it's the ultimate thrill."
                        else:
                            selected_girl.character "I'm pregnant with your baby! Of course I want you bare. Feeling you cum inside me while I'm carrying your child is the ultimate thrill."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm carrying your next child. As an experienced mother, bare access is now part of our established family arrangement. There's no additional charge, though I expect you to uphold your end for both our children."
                        else:
                            selected_girl.character "I'm carrying your child. As an experienced mother, bare access is now part of our family arrangement. There's no additional charge, though I expect you to uphold your end of the support."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm carrying your next baby... so does that mean bare access is still free? I mean, we already have one, so this is just... part of the deal now, right?"
                        else:
                            selected_girl.character "I'm carrying your baby... so does that mean bare access is free now? Or do I still get paid for it? I'm not sure how the pricing works for this situation..."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm carrying your next child. Since you're the father to both, bare access is included in our ongoing family package. No additional charge."
                        else:
                            selected_girl.character "I'm carrying your child. Since you're the father, bare access is included in the pregnancy package. No additional charge."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I am carrying your next child. As an experienced mother, I know protection is unnecessary. You may proceed as you wish with the mother of your children."
                        else:
                            selected_girl.character "I am carrying your child. As an experienced mother, I know protection is unnecessary. You may proceed as you wish."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm carrying your next baby... so if you don't want to use a condom, that's okay, Professor. Whatever you want is what I'll do for our family."
                        else:
                            selected_girl.character "I'm carrying your baby... so if you don't want to use a condom, that's okay, Professor. Whatever you want is what I'll do."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I am carrying your next child. Protection is unnecessary. Proceed as you wish with the mother of your child."
                        else:
                            selected_girl.character "I am carrying your child. Protection is unnecessary for vaginal intercourse. Proceed as you wish."
                else:
                    if selected_girl.kids_with_player > 0:
                        selected_girl.character "I'm pregnant with your next baby... and we already have one. So condoms aren't really necessary anymore, are they?"
                    else:
                        selected_girl.character "I'm pregnant with your baby... so condoms aren't really necessary anymore, are they?"

            elif selected_girl.wants_vaginal_condom: # She wants condoms
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "As an experienced mother, I have to be careful for the child we already have. When you're inside me, I need that protection. I can't risk another pregnancy right now."
                        else:
                            selected_girl.character "As an experienced mother with responsibilities, I have to be careful. When you're inside me, I need that protection. I can't risk another pregnancy right now."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I feel so close to you, but I'm also really scared... we have our child, and I can't handle another one so soon. When we're together, I need that protection, Professor."
                        else:
                            selected_girl.character "I feel so close to you, but I'm also really scared... when we're together, I think I need that protection. I'm not ready to be a mom yet, Professor."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I feel connected to you, but we have a child to think about. When we're intimate, I need that layer of protection. It lets me relax and enjoy the moment without worrying about another."
                        else:
                            selected_girl.character "I feel connected to you, but when we're intimate, I need that layer of protection. It lets me relax and enjoy the moment without worrying."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "The way you look at me is so hot... but we have a child, and I have to be smart. Watching you roll a condom on before you take me shows you respect our family, and that's a turn-on."
                        else:
                            selected_girl.character "The way you look at me is so hot... but as an experienced mother, I need to be smart. Watching you roll a condom on before you take me shows you respect my situation, and that's a turn-on."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "You make me feel so hot... but we have our child, and I'm so nervous about getting pregnant again. Watching you put on a condom makes me feel safer... and actually kind of sexy in a responsible way?"
                        else:
                            selected_girl.character "You make me feel so hot... but I'm so nervous about getting pregnant. Watching you put on a condom makes me feel safer... and actually kind of sexy in a responsible way?"
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "The way you look at me is so hot... but we have a child now. Watching you roll a condom on before you fuck me shows you're thinking about our family, which is its own kind of sexy."
                        else:
                            selected_girl.character "The way you look at me is so hot... but watching you roll a condom on before you fuck me can be its own kind of sexy. It's like teasing what's to come."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "Let's be clear. As the mother of your child, letting you fuck my pussy with a condom costs extra. My safety and our child's wellbeing have a price."
                        else:
                            selected_girl.character "Let's be clear. As an experienced mother, letting you fuck my pussy with a condom costs extra. My safety and my existing child's wellbeing have a price."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "What's in it for me? We have a child, so letting you... you know... with a condom is about protecting our family. That's going to cost you extra, Professor."
                        else:
                            selected_girl.character "What's in it for me? Letting you... you know... with a condom... um, does that cost less than without? I'm not sure about the pricing here, Professor."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "What's in it for me? We have a child. Letting you fuck my pussy with a condom costs extra. It's the safer option for our family, so you pay a premium."
                        else:
                            selected_girl.character "What's in it for me? Letting you fuck my pussy with a condom costs extra. It's the safer option, so you pay a premium for the reduced risk."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "You are in charge, Master. As the mother of your child, if you wish to use a condom, I will accept it. I must prioritize the safety of the child we already have."
                        else:
                            selected_girl.character "You are in charge, Master. As an experienced mother, if you wish to use a condom, I will accept it. I must prioritize the safety of the child I already have."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "You're in charge, Professor. But we have a child. If you want to use a condom when we... do it... I'll do what you want. It's probably for the best."
                        else:
                            selected_girl.character "You're in charge, Professor. If you want to use a condom when we... do it... I'll do what you want. Your choice is what matters."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "You are in charge. As the mother of your child, if you wish to use a condom before entering my pussy, I will accept it for the sake of our family."
                        else:
                            selected_girl.character "You are in charge. If you wish to use a condom before entering my pussy, I will accept it."
                else:
                    if selected_girl.kids_with_player > 0:
                        selected_girl.character "I prefer using condoms for vaginal sex... we have a child, and it's just safer that way for me right now."
                    else:
                        selected_girl.character "I prefer using condoms for vaginal sex... it's just safer that way for me right now."

            else: # She doesn't want condoms
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I feel so connected to you. As the mother of your child, my body already knows what to do. I want to feel your bare cock inside me again, nothing between us when we make love."
                        else:
                            selected_girl.character "I feel so connected to you. As an experienced mother, my body knows what to do. I want to feel your bare cock inside me, nothing between us when we make love."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I feel so connected to you. We have a child together, so I want to feel your bare cock inside me... it feels more right and intimate without anything between us now."
                        else:
                            selected_girl.character "I feel so connected to you. I want to feel your bare cock inside me... it feels more intimate and real without anything between us, you know?"
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I feel so connected to you. We have a child, and I want to feel you completely, with nothing between us when we're together. It just feels more right that way now."
                        else:
                            selected_girl.character "I feel so connected to you. I want to feel you completely, with nothing between us when we're together. It just feels more right that way."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "The way you look at me is so hot. As the mother of your child, I want to feel your raw cock stretching my pussy open again. I loved it the first time."
                        else:
                            selected_girl.character "The way you look at me is so hot. As an experienced mother, I want to feel your raw cock stretching my pussy open. Motherhood hasn't dulled my desires at all."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "The way you look at me is so hot! We have a child, and I want to feel your bare cock inside me again... I loved how it felt when we made them!"
                        else:
                            selected_girl.character "The way you look at me is so hot! I want to feel your bare cock inside me... I've never done it without a condom before, Professor. It sounds so exciting and dangerous!"
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "The way you look at me is so hot. We have a child, and I want to feel your raw cock stretching me open again, no barriers. Just like the first time."
                        else:
                            selected_girl.character "The way you look at me is so hot. I want to feel your raw cock stretching me open, no barriers, no holding back. Just you and me."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "What's in it for me? Bareback access from the mother of your child? That's still a premium service, Professor. I know exactly what my body is worth to you."
                        else:
                            selected_girl.character "What's in it for me? Bareback access from an experienced mother? That's a premium service, Professor. I know exactly what my body is worth."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "What's in it for me? Bareback...? We have a child, so you know I'm good at it. Is that more expensive? I don't really know what to charge for that..."
                        else:
                            selected_girl.character "What's in it for me? Bareback...? Is that more expensive? I don't really know what to charge for that... what do you think is fair, Professor?"
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "What's in it for me? We have a child, so you know bareback pussy access is top quality. That's a premium experience, Professor. You'll have to pay for the privilege."
                        else:
                            selected_girl.character "What's in it for me? Bareback pussy access? That's a premium experience, Professor. You'll have to pay for the privilege."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "You are in charge, Master. As the mother of your child, if you want to fuck my bare pussy with no condom, I will not stop you. My body knows how to handle you."
                        else:
                            selected_girl.character "You are in charge, Master. As an experienced mother, if you want to fuck my bare pussy with no condom, I will not stop you. My body knows how to handle this."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "You're in charge, Professor. We have a child, so if you want to fuck me without a condom... okay, I'll let you. Whatever you want is what I'll do for our family."
                        else:
                            selected_girl.character "You're in charge, Professor. If you want to fuck me without a condom... okay, I'll let you. Whatever you want is what I'll do."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "You are in charge. As the mother of your child, if you want to fuck my bare pussy with no condom, I will not stop you."
                        else:
                            selected_girl.character "You are in charge. If you want to fuck my bare pussy with no condom, I will not stop you."
                else:
                    if selected_girl.kids_with_player > 0:
                        selected_girl.character "I don't really like condoms... especially since we have a child together. I prefer it bare, just like before."
                    else:
                        selected_girl.character "I don't really like condoms... I prefer it bare. It just feels better."
            
            # Skip menu if already pregnant with his baby
            if not (selected_girl.pregnant and selected_girl.preg_father == "player"):
                menu:
                    "I respect your boundaries. We'll always use condoms when fucking your pussy.": 
                        player.character "I respect your boundaries. We'll always use condoms when fucking your pussy."
                        $ selected_girl.wants_vaginal_condom = True
                        $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                        # Response based on her dominant_approach, role, and family context
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Thank you for understanding. As the mother of your child, I appreciate you respecting my boundaries for our family's future. It means the world to me."
                                else:
                                    selected_girl.character "Thank you for understanding. As an experienced mother, I appreciate you respecting my responsibilities. It makes me feel even more connected to you."
                            elif is_student:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Thank you, Professor! That makes me feel so much better about... us. I'm glad you're being so responsible for our family."
                                else:
                                    selected_girl.character "Thank you for understanding! That makes me feel so much better about... you know. I'm glad you're being so responsible with me."
                            else:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Thank you for understanding. Since we have a child, knowing you'll protect me like this makes me feel safe and even more connected to you."
                                else:
                                    selected_girl.character "Thank you for understanding. Knowing you'll protect me makes me feel even more connected to you."

                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Mmm... a man who respects the mother of his child. That's unexpectedly hot. Knowing you'll be careful for our family... I like that a lot."
                                else:
                                    selected_girl.character "Mmm... a gentleman who respects an experienced mother's boundaries. That's unexpectedly hot. I like that."
                            elif is_student:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Mmm... you're being so sweet and responsible for our family! That's actually really hot. I like that a lot, Professor."
                                else:
                                    selected_girl.character "Mmm... you're being so sweet and responsible! That's actually really hot. I like that a lot."
                            else:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Mmm... a man who respects the mother of his child's pussy. That's a new kind of hot. I like it."
                                else:
                                    selected_girl.character "Mmm... a gentleman who respects pussy boundaries. That's unexpectedly hot. I like that."

                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Fine. As the mother of your child, I'll remember this favor. A responsible father is a valuable asset, and you just increased your worth."
                                else:
                                    selected_girl.character "Fine. As an experienced mother, I'll remember this favor next time you want something - responsible men are valuable."
                            elif is_student:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Okay! I'll remember you were so good about this for our family. That was really smart of you, Professor."
                                else:
                                    selected_girl.character "Okay! I'll remember you were so nice about this. That was really good of you, Professor."
                            else:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Fine. I'll remember this favor next time you want something from me. A man who takes care of his family is a good investment."
                                else:
                                    selected_girl.character "Fine. I'll remember this favor next time you want something from me."

                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Thank you, Master. As the mother of your child, your consideration for my body and our family's future confirms your wisdom. You have made the right choice."
                                else:
                                    selected_girl.character "Thank you, Master. As an experienced mother, your consideration for my pussy and my family means everything to me."
                            elif is_student:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Thank you, Professor! I'm glad you're being so thoughtful about our family. It shows you know what's best for us."
                                else:
                                    selected_girl.character "Thank you, Professor! I'm glad you're being so thoughtful about... about me."
                            else:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Thank you, Master. Your consideration for the mother of your child means everything to me. You have pleased me."
                                else:
                                    selected_girl.character "Thank you, Master. Your consideration for my pussy means everything to me."
                        else:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Thank you for respecting my boundaries about condoms, especially now that we have a child."
                            else:
                                selected_girl.character "Thank you for respecting my boundaries about condoms."
                    
                    "But what if we wanted to make a baby? No condom when I cum in your pussy?":
                        # Check if she wants a baby and her approach
                        player.character "But what if we wanted to make a baby? No condom when I cum in my pussy?"
                        if selected_girl.baby_desire > 50 and selected_girl.dominant_approach in ["compassionate", "sexualized"]: # Emotionally invested reactions
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750)})
                            if selected_girl.dominant_approach == "compassionate":
                                if is_base_mother:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "Another baby? To keep growing our family? As an experienced mother, I'd love nothing more. Please cum in my bare pussy."
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "A sibling for our child? As an experienced mother, I'd love to give them one. Please cum in my bare pussy."
                                    else:
                                        selected_girl.character "A baby with you... as an experienced mother, I'd love to give you a child. Please cum in my bare pussy."
                                elif is_student:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "Another baby? Wow, Professor! To make our family even bigger? I'd love that! Please cum in my bare pussy!"
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "A sibling for our child? Oh my god, really? I'd love that! Please cum in my bare pussy and give them a brother or sister!"
                                    else:
                                        selected_girl.character "A baby with you? Oh my god, really? I'd love that! Please cum in my bare pussy and put a baby in me!"
                                else:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "Another baby? I love the sound of that. Let's make our beautiful family even bigger. Please cum in my bare pussy."
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "A baby with you... I'd love to give our child a sibling. Please cum in my bare pussy and put another baby in me."
                                    else:
                                        selected_girl.character "A baby with you... I'd love nothing more! Please cum in my bare pussy and put a baby in me."
                            elif selected_girl.dominant_approach == "sexualized":
                                if is_base_mother:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "Another baby? Knocking me up again? My body remembers this, Professor. Fill my pussy with your cum and make our family bigger!"
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "A sibling? You knocking me up again? As an experienced mother, I know exactly how hot that is. Fill my pussy with your cum!"
                                    else:
                                        selected_girl.character "A baby? You knocking me up? As an experienced mother, I know exactly how hot that is. Fill my pussy with your cum!"
                                elif is_student:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "Another baby? You're trying to get me pregnant again? Oh wow! That's so hot! Please cum inside me and make our family huge!"
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "A baby? You knocking me up again? Oh wow! That's so hot! Please cum inside me and give our child a sibling!"
                                    else:
                                        selected_girl.character "A baby? You knocking me up? Oh wow! That's so hot! Please cum inside me and put a baby in me!"
                                else:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "Another baby? You knocking me up again? That's so hot! Please cum in my bare pussy and put another baby in me!"
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "A baby? You knocking me up again? That's so hot! Please cum in my bare pussy and put another baby in me!"
                                    else:
                                        selected_girl.character "A baby? You knocking me up? That's so hot! Please cum in my bare pussy and put a baby in me!"

                        elif selected_girl.dominant_approach == "transactional": # Transactional always sees it as business
                            if is_base_mother:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Another baby? As the mother of your children, expanding our family further requires a significant new investment. What are you offering for another one?"
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "A sibling for our child? As the mother of your child, I know exactly what that's worth. We're talking a significant investment. What are you offering?"
                                else:
                                    selected_girl.character "A baby with you? As an experienced mother, I know exactly what that's worth. We're talking significant investment. What are you offering?"
                                menu:
                                    "Offer 5,000 cash for baby expenses?":
                                        if player.cash >= 5000:
                                            $ player.cash -= 5000
                                            $ selected_girl.cash += 5000
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "corruption": (250, 750)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "5000 upfront? It's a start for another child. Fine, you can breed me again... but my expectations for support are even higher now."
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "5000 upfront? As the mother of your child, I know that's a start for a sibling. Fine, you can breed me again... but I expect significant ongoing support."
                                            else:
                                                selected_girl.character "5000 upfront? As an experienced mother, I know that's a start for a child. Fine, you can breed me... but I expect significant ongoing support."
                                            if selected_girl.birth_control:
                                                $ selected_girl.birth_control = False
                                                selected_girl.character "Guess, don't need to worry about birth control any more..."
                                        else:
                                            selected_girl.character "You think that's enough for the mother of your children to carry another? Don't insult me. Come back when you're serious."
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Cover 18,000 medical expenses":
                                        if player.cash >= 18000:
                                            $ player.cash -= 18000
                                            $ selected_girl.cash += 18000
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750), "corruption": (250, 750)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "Medical coverage for another child? That's the security I need to expand our family. Fine, you can put another baby in me."
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "Medical coverage for a sibling? As the mother of your child, I appreciate that security. Fine, you can put another baby in me."
                                            else:
                                                selected_girl.character "Medical coverage for your child? As an experienced mother, I appreciate that security. Fine, you can put a baby in me."
                                            if selected_girl.birth_control:
                                                $ selected_girl.birth_control = False
                                                selected_girl.character "Guess, don't need to worry about birth control any more..."
                                        else:
                                            selected_girl.character "You think you have enough to cover medical expenses for another child? Don't insult me. Come back when you're serious."
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Leave it be.":
                                        if selected_girl.kids_with_player > 1:
                                            selected_girl.character "Smart move. The mother of your children isn't cheap, and I'm not expanding our family without proper compensation."
                                        else:
                                            selected_girl.character "Smart move. An experienced mother isn't cheap, and I'm not giving you a child without proper compensation."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            elif is_student:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Another baby? Like, a third one? But that's... so much! What would you even pay for another one?"
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "A baby? A sibling for ours? But that's... that's even more 18 years of stuff! What would you even pay for that?"
                                else:
                                    selected_girl.character "A baby? Like... for real? But that's... that's 18 years of stuff! What would you even pay for that? I don't even know what that costs!"
                                menu:
                                    "Offer 5000 cash for baby expenses?":
                                        if player.cash >= 5000:
                                            $ player.cash -= 5000
                                            $ selected_girl.cash += 5000
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "corruption": (250, 750)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "5000? For another baby? Oh my god, okay! Yeah, you can put another one in me! I'll be the best mom to all of them, I promise!"
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "5000? For a sibling? Oh my god, that's so much money! Okay, yeah, you can put another baby in me for that! I'll be a good mom to both, I promise!"
                                            else:
                                                selected_girl.character "5000? Oh my god, that's so much money! Okay, yeah, you can put a baby in me for that! I'll be a good mom, I promise!"
                                            if selected_girl.birth_control:
                                                $ selected_girl.birth_control = False
                                                selected_girl.character "Guess, don't need to worry about birth control any more..."
                                        else:
                                            selected_girl.character "That's not enough for a baby, is it? I don't think so... you need to be more serious than that."
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Cover 18,000 medical expenses":
                                        if player.cash >= 18000:
                                            $ player.cash -= 18000
                                            $ selected_girl.cash += 18000
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750), "corruption": (250, 750)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "You'll cover all the doctor stuff for another one? Really? Okay! That makes me feel better about... having another. Yeah, let's do it!"
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "You'll cover all the doctor stuff for a sibling? Really? Okay! That makes me feel better about... you know, having a sibling for ours. Yeah, let's do it!"
                                            else:
                                                selected_girl.character "You'll cover all the doctor stuff? Really? Okay! That makes me feel better about... you know, having a baby. Yeah, let's do it!"
                                            if selected_girl.birth_control:
                                                $ selected_girl.birth_control = False
                                                selected_girl.character "Guess, don't need to worry about birth control any more..."
                                        else:
                                            selected_girl.character "You think you have enough to cover medical expenses? Don't insult me. Come back when you're serious."
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Grant her a grade bump of 50 percent?":
                                        if selected_girl.grades < 100:
                                            $ new_grade = min(100, selected_girl.grades + 50)
                                            $ selected_girl.grades = new_grade
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection":(250, 750), "corruption": (250, 750)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "Grade bump for having another baby for you? As a student, that's perfect security for our growing family! Fine, you can put another baby in me... grade bump for a baby bump!"
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "Grade bump for having a sibling for our child? As a student, that's perfect security! Fine, you can put another baby in me... grade bump for a baby bump!"
                                            else:
                                                selected_girl.character "Grade bump for having your baby? As a student, that's perfect security! Fine, you can put a baby in me... grade bump for a baby bump!"
                                            if selected_girl.birth_control:
                                                $ selected_girl.birth_control = False
                                                selected_girl.character "Guess, don't need to worry about birth control any more..."
                                        else:
                                            selected_girl.character "But... my grades are already at maximum! A bump won't help much... can you offer something else?"
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Leave it be.":
                                        if selected_girl.kids_with_player > 1:
                                            selected_girl.character "Oh... okay. Maybe having another baby is... a lot. I understand."
                                        else:
                                            selected_girl.character "Oh... okay. Maybe having a baby right now is... a lot. I understand."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            else:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Another baby? That's another lifetime commitment, Professor. We're talking 18+ more years of support for our growing family. What are you offering?"
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "A baby with you? A sibling for our child? That's a lifetime commitment, Professor. We're talking 18+ more years of support. What are you offering?"
                                else:
                                    selected_girl.character "A baby with you? That's a lifetime commitment, Professor. We're talking 18+ years of support. What are you offering?"
                                menu:
                                    "Offer 5000 cash for baby expenses?":
                                        if player.cash >= 5000:
                                            $ player.cash -= 5000
                                            $ selected_girl.cash += 5000
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"baby_desire": (750, 1500), "corruption": (750, 1500)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "5000 upfront? For another child? That's a start. Fine, you can breed me again... but I expect increased support for all of them. This is strictly business."
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "5000 upfront? For a sibling for our child? That's a start. Fine, you can breed me again... but I expect regular child support payments for both. This is strictly business."
                                            else:
                                                selected_girl.character "5000 upfront? That's a start. Fine, you can breed me... but I expect regular child support payments. This is strictly business."
                                            if selected_girl.birth_control:
                                                $ selected_girl.birth_control = False
                                                selected_girl.character "Guess, don't need to worry about birth control any more..."
                                        else:
                                            selected_girl.character "You think that's enough for 18+ more years of commitment? Don't insult me. Come back when you're serious."
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Cover 18,000 medical expenses":
                                        if player.cash >= 18000:
                                            $ player.cash -= 18000
                                            $ selected_girl.cash += 18000
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750), "corruption": (550, 1000)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "Medical coverage for another child? That's security for our family. Fine, you can put another baby in me... but I want it wired to me right now."
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "Medical coverage for a sibling? That's security for our family. Fine, you can put another baby in me... but I want it wired to me right now."
                                            else:
                                                selected_girl.character "Medical coverage? That's security. Fine, you can put a baby in me... but I want it wired to me right now."
                                            if selected_girl.birth_control:
                                                $ selected_girl.birth_control = False
                                                selected_girl.character "Guess, don't need to worry about birth control any more..."
                                        else:
                                            selected_girl.character "You think you have enough to cover medical expenses for another child? Don't insult me. Come back when you're serious."
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Leave it be.":
                                        if selected_girl.kids_with_player > 1:
                                            selected_girl.character "Smart move. I'm not expanding your family again without proper compensation."
                                        else:
                                            selected_girl.character "Smart move. I'm not giving you a baby without proper compensation."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})

                        elif selected_girl.dominant_approach == "dominate": # Dominate will submit to player's wishes
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.birth_control = False
                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750)})
                            if is_base_mother:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "If you wish to put another baby in me, Master... as the mother of your children, I will accept your seed again. My body is yours to command."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "If you wish to put another baby in me, Master... as the mother of your child, I will accept your seed again. My body knows how to serve you."
                                else:
                                    selected_girl.character "If you wish to put a baby in me, Master... as an experienced mother, I will accept your seed. My body knows how to serve you."
                            elif is_student:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "If you want to put another baby in me, Professor... okay. I'll do that for you and our family. Whatever you want."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "If you want to put another baby in me, Professor... okay. I'll do that for you and our family. Whatever you want."
                                else:
                                    selected_girl.character "If you want to put a baby in me, Professor... okay. I'll do that for you. Whatever you want."
                            else:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "If you wish to put another baby in me, Master... I will accept your seed. My body is yours to command, and our family will grow."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "If you wish to put another baby in me, Master... I will accept your seed. My body is yours to command, and our family will grow."
                                else:
                                    selected_girl.character "If you wish to put a baby in me, Master... I will accept your seed. My body is yours to command."
                        else: # Low baby desire or uncertain
                            $ selected_girl.wants_vaginal_condom = True
                            if is_base_mother:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Another baby? As the mother of your children, I'm not sure I'm ready for more right now. Let's focus on the family we already have."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "A sibling? As the mother of your child, I'm not sure I'm ready for more children right now. Let's focus on the one we have."
                                else:
                                    selected_girl.character "A baby? As an experienced mother, I'm not sure I'm ready for more children right now."
                            elif is_student:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Another baby? Oh... wow, that's... that's a lot. I'm not sure I'm ready for another one right now, Professor! I'm still in school!"
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "A sibling? Oh... wow, that's... that's a lot. I'm not sure I'm ready for another one right now, Professor! I'm still in school!"
                                else:
                                    selected_girl.character "A baby? Oh... wow, that's... that's a lot. I'm not sure I'm ready for that, Professor. I'm still in school!"
                            else:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "That's not something I'm comfortable discussing right now. We have children to focus on."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "That's not something I'm comfortable discussing right now. We have a child to focus on."
                                else:
                                    selected_girl.character "That's not something I'm comfortable discussing right now."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    
                    "Would you consider letting me fuck your bare pussy sometimes?": 
                        # Check different dominant_approach types
                        player.character "Would you consider letting me fuck your bare pussy sometimes?"
                        if selected_girl.dominant_approach == "sexualized": # Already open to it
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                            if is_base_mother:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Mmm... bareback fucking my pussy again? As the mother of your children, I've been wanting you to ask. Take me bare, Professor."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "Mmm... bareback fucking my pussy again? As the mother of your child, my body remembers you. Take me bare, Professor."
                                else:
                                    selected_girl.character "Mmm... bareback fucking my pussy? As an experienced woman, I've been wanting you to ask. Take me bare, Professor."
                            elif is_student:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Mmm... bareback again? We've already done that to make our family! Of course! Take me bare, Professor!"
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "Mmm... bareback again? We did that to make our baby! Of course! Take me bare, Professor!"
                                else:
                                    selected_girl.character "Mmm... bareback? Like... without a condom? I've never done that before! But... okay, yeah, I want to try! Take me bare!"
                            else:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Mmm... bareback fucking my pussy again? As the mother of your children, I've been wanting you to ask. Take me bare."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "Mmm... bareback fucking my pussy again? As the mother of your child, I've been wanting you to ask. Take me bare."
                                else:
                                    selected_girl.character "Mmm... bareback fucking my pussy? I've been wanting you to ask. Take me bare."

                        elif selected_girl.dominant_approach == "transactional": # This is where the negotiation happens
                            if is_base_mother:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Bare pussy access again? As the mother of your children, I know what this privilege is worth to you. What are you offering for it?"
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "Bare pussy access again? As the mother of your child, I know what this privilege is worth. What are you offering for it?"
                                else:
                                    selected_girl.character "Bare pussy access? As an experienced mother, I know that's a premium service. What are you offering for this privilege?"
                                menu:
                                    "Grant her a 500 cash incentive?":
                                        if player.cash >= 500:
                                            $ player.cash -= 500
                                            $ selected_girl.cash += 500
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"corruption": (350, 750), "affection": (250, 750)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "500 for bareback access again? As the mother of your children, I know that's fair. Deal. Just don't forget this is business."
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "500 for bareback access again? As the mother of your child, I know that's fair. Deal. Just don't forget this is business."
                                            else:
                                                selected_girl.character "500 for bareback access? As an experienced mother, I know that's fair. Deal. Just don't get too attached - this is business."
                                        else:
                                            selected_girl.character "Don't waste an experienced mother's time with empty promises. Come back when you can actually pay."
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Leave it be.":
                                        if selected_girl.kids_with_player > 1:
                                            selected_girl.character "Suit yourself. The mother of your children's bare pussy stays on lockdown until you learn how negotiations work."
                                        else:
                                            selected_girl.character "Suit yourself. An experienced mother's bare pussy stays on lockdown until you learn how negotiations work."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            elif is_student:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Bare... again? Like we did to make our other babies? Is that more expensive now? I don't know what to charge for another one..."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "Bare... again? Like we did to make our baby? Is that more expensive now? I don't know what to charge for another one..."
                                else:
                                    selected_girl.character "Bare...? Like no condom? Is that more expensive? I don't know what to charge... but maybe... a grade bump? What do you think is fair?"
                                menu:
                                    "Grant her a 500 cash incentive?":
                                        if player.cash >= 500:
                                            $ player.cash -= 500
                                            $ selected_girl.cash += 500
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"corruption": (350, 750), "affection": (250, 750)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "500? To do it again? Oh my god, okay! Yeah, you can fuck my pussy without a condom for that! Thank you!"
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "500? To do it again? Oh my god, okay! Yeah, you can fuck my pussy without a condom for that! Thank you!"
                                            else:
                                                selected_girl.character "500? Oh my god, that's so much! Okay, yeah, you can fuck my pussy without a condom for that! Thank you!"
                                        else:
                                            selected_girl.character "Oh... you don't have enough? That's okay... maybe some other time?"
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Grant her a grade bump of 5 percent?":
                                        if selected_girl.grades >= 100:
                                            selected_girl.character "But... my grades are already at maximum! A bump won't help much... can you offer something else?"
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                        else:
                                            $ new_grade = min(100, selected_girl.grades + 5)
                                            $ selected_girl.grades = new_grade
                                            $ selected_girl.apply_impacts({"corruption": (250, 750), "discipline": (-750, -250)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "Grade bump to do it again? As a student, that's perfect security for our family! Fine, you can fuck my pussy raw..."
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "Grade bump to do it again? As a student, that's perfect security for our family! Fine, you can fuck my pussy raw..."
                                            else:
                                                selected_girl.character "Grade bump for bareback? As a student, that's perfect security! Fine, you can fuck my pussy raw... "
                                    "Leave it be.":
                                        selected_girl.character "Oh... okay. Well, if you change your mind about the grade bump or cash, just let me know, I guess?"
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            else:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "Bare pussy access again? As the mother of your children, that's a premium service. What are you offering?"
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "Bare pussy access again? As the mother of your child, that's a premium service. What are you offering?"
                                else:
                                    selected_girl.character "Bare pussy access? That's a premium service, Professor. What are you offering?"
                                menu:
                                    "Grant her a 500 cash incentive?":
                                        if player.cash >= 500:
                                            $ player.cash -= 500
                                            $ selected_girl.cash += 500
                                            $ selected_girl.wants_vaginal_condom = False
                                            $ selected_girl.apply_impacts({"corruption": (350, 750), "affection": (250, 750)})
                                            if selected_girl.kids_with_player > 1:
                                                selected_girl.character "500 for bareback access again? Deal. Just don't get too attached - this is a business arrangement for our family."
                                            elif selected_girl.kids_with_player == 1:
                                                selected_girl.character "500 for bareback access again? Deal. Just don't get too attached - this is a business arrangement for our family."
                                            else:
                                                selected_girl.character "500 for bareback access? Deal. Just don't get too attached - this is a business arrangement."
                                        else:
                                            selected_girl.character "Don't waste my time with empty promises, Professor. Come back when you can actually pay."
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    "Leave it be.":
                                        if selected_girl.kids_with_player > 1:
                                            selected_girl.character "Suit yourself. The mother of your children's bare pussy stays on lockdown until you learn how negotiations work."
                                        else:
                                            selected_girl.character "Suit yourself. My bare pussy stays on lockdown until you learn how negotiations work."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})

                        elif selected_girl.dominant_approach in ["compassionate", "dominate"]: # These will agree to please the player
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                            if selected_girl.dominant_approach == "compassionate":
                                if is_base_mother:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "I trust you completely, Professor. As the mother of your children, let's feel each other without anything between us again."
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "I trust you completely, Professor. As the mother of your child, let's feel each other without anything between us again."
                                    else:
                                        selected_girl.character "I trust you completely, Professor. As an experienced mother, let's feel each other without anything between us."
                                elif is_student:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "I trust you, Professor. We've made our family, so of course I want to feel you without anything between us again."
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "I trust you, Professor. We've made our baby, so of course I want to feel you without anything between us again."
                                    else:
                                        selected_girl.character "I trust you, Professor. I want to feel you without anything between us... that sounds really intimate."
                                else:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "I trust you completely. As the mother of your children, let's feel each other without anything between us again."
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "I trust you completely. As the mother of your child, let's feel each other without anything between us again."
                                    else:
                                        selected_girl.character "I trust you completely. Let's feel each other without anything between us."
                            else: # Dominate
                                if is_base_mother:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "If that's what you want, Master... as the mother of your children, I'll let you fuck my bare pussy again."
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "If that's what you want, Master... as the mother of your child, I'll let you fuck my bare pussy again."
                                    else:
                                        selected_girl.character "If that's what you want, Master... as an experienced mother, I'll let you fuck my bare pussy."
                                elif is_student:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "If that's what you want, Professor... okay, I'll let you fuck me without a condom again. For our family."
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "If that's what you want, Professor... okay, I'll let you fuck me without a condom again. For our baby."
                                    else:
                                        selected_girl.character "If that's what you want, Professor... okay, I'll let you fuck me without a condom."
                                else:
                                    if selected_girl.kids_with_player > 1:
                                        selected_girl.character "If that's what you want, Master... as the mother of your children, I'll let you fuck my bare pussy again."
                                    elif selected_girl.kids_with_player == 1:
                                        selected_girl.character "If that's what you want, Master... as the mother of your child, I'll let you fuck my bare pussy again."
                                    else:
                                        selected_girl.character "If that's what you want, Master... I'll let you fuck my bare pussy."
                        else: # Not interested
                            $ selected_girl.wants_vaginal_condom = True
                            if is_base_mother:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "I'm not comfortable with that. As the mother of your children, I need to be careful. Let's stick to condoms for now."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "I'm not comfortable with that. As the mother of your child, I need to be careful. Let's stick to condoms for now."
                                else:
                                    selected_girl.character "I'm not comfortable with that. As an experienced mother, I need to be careful. Let's stick to condoms for now."
                            elif is_student:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "I'm not sure I'm ready for that again... without a condom? We have our family to think about. Let's stick with condoms, okay?"
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "I'm not sure I'm ready for that again... without a condom? We have our baby to think about. Let's stick with condoms, okay?"
                                else:
                                    selected_girl.character "I'm not sure I'm ready for that... without a condom? That's kind of scary. Let's stick with condoms, okay?"
                            else:
                                if selected_girl.kids_with_player > 1:
                                    selected_girl.character "I'm not comfortable with that. As the mother of your children, let's stick to condoms for now."
                                elif selected_girl.kids_with_player == 1:
                                    selected_girl.character "I'm not comfortable with that. As the mother of your child, let's stick to condoms for now."
                                else:
                                    selected_girl.character "I'm not comfortable with that. Let's stick to condoms for now."
        
        # ANAL CONDOM PREFERENCES
        "What about for anal sex?":
            # Response based on dominant_approach, role, and pregnancy context
            if selected_girl.pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player":
                # Already pregnant with player's baby
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "Since I'm already carrying your baby, Professor... as an experienced mother, I want to feel you completely. Anal without protection would be incredibly intimate."
                    elif is_student:
                        selected_girl.character "Since I'm already pregnant with your baby... wow, so anal without condoms would be okay? That sounds... kind of intense but really intimate!"
                    else:
                        selected_girl.character "Since I'm already carrying your baby, Professor... I want to feel you completely. Anal without protection would be incredibly intimate."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I'm pregnant with your baby! As an experienced woman, bareback anal while carrying your child... that's incredibly hot and taboo. I want it!"
                    elif is_student:
                        selected_girl.character "I'm pregnant with your baby! Oh my god, bareback anal while pregnant? That sounds so naughty and hot! Yes!"
                    else:
                        selected_girl.character "I'm pregnant with your baby! Bareback anal while carrying your child? That's so hot and taboo. I want it!"
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I'm carrying your child. As an experienced mother, bareback anal is included in our pregnancy package - no additional charge, though I expect proper support."
                    elif is_student:
                        selected_girl.character "I'm carrying your baby... so does bareback anal cost extra? Or is it free since I'm already pregnant? I'm not sure how the pricing works for this..."
                    else:
                        selected_girl.character "I'm carrying your child. Since you're the father, bareback anal is included in the pregnancy package - no additional charge."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I am carrying your child. As an experienced mother, I know protection is unnecessary for anal. Proceed as you wish."
                    elif is_student:
                        selected_girl.character "I'm carrying your baby... so if you want bareback anal, that's okay, Professor. Whatever you want."
                    else:
                        selected_girl.character "I am carrying your child. Protection is unnecessary for anal intercourse. Proceed as you wish."
                else:
                    selected_girl.character "I'm pregnant with your baby... so I guess we don't need condoms for anal either, right?"
            
            elif selected_girl.wants_anal_condom:
                # She wants condoms for anal
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "As an experienced mother, I need to be careful about my health. When you're in my ass, I need that protection - I can't risk getting sick while caring for my family."
                    elif is_student:
                        selected_girl.character "I feel so connected to you, but I'm nervous about anal... when you're in my ass, I think I need that protection. I've heard it can be risky."
                    else:
                        selected_girl.character "I feel so connected to you, but when you're in my ass, I need that rubber layer. It lets me relax and enjoy us without worry."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "The way you look at me is so hot... but as an experienced mother, I need to be careful. Watching you roll a condom over your hard cock before taking my ass shows you respect my health."
                    elif is_student:
                        selected_girl.character "The way you look at me is so hot... but I'm kind of scared of anal without protection. Watching you put on a condom makes me feel safer... and actually kind of sexy!"
                    else:
                        selected_girl.character "The way you look at me is so hot... but watching you roll a condom over your hard cock before taking my ass can be its own kind of sexy."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "What's in it for me? As an experienced mother with responsibilities, protected anal costs extra - I have to maintain my health for my family."
                    elif is_student:
                        selected_girl.character "What's in it for me? Protected anal... um, does that cost less than without? I'm not sure about the pricing for anal stuff..."
                    else:
                        selected_girl.character "What's in it for me? Protected anal costs extra... unless you make it worth my time."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "You're in charge, Master. As an experienced mother, if you want to wrap your cock before entering my ass, I'll accept it - I must protect my family."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want to use a condom for anal... I'll do what you want."
                    else:
                        selected_girl.character "You're in charge, Master. If you want to wrap your cock before entering my ass, I'll accept it."
                else:
                    selected_girl.character "I prefer using condoms for anal sex... it's safer that way."
            
            else:
                # She doesn't want condoms for anal
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I feel so connected to you. As an experienced mother, I want to feel your bare cock in my ass - it's a different kind of intimacy that I trust you with."
                    elif is_student:
                        selected_girl.character "I feel so connected to you. I want to feel your bare cock in my ass... it feels more intimate without anything between us, you know?"
                    else:
                        selected_girl.character "I feel so connected to you. I want to feel your bare cock in my ass, nothing between us when we're intimate like that."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "The way you look at me is so hot. As an experienced woman, I want to feel your raw cock stretching my ass open - motherhood hasn't dulled my desires for that intensity."
                    elif is_student:
                        selected_girl.character "The way you look at me is so hot! I want to feel your bare cock in my ass... I've never done anal without a condom before, that sounds so exciting!"
                    else:
                        selected_girl.character "The way you look at me is so hot. I want to feel your raw cock stretching my ass open, no barriers."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "What's in it for me? Bareback anal from an experienced mother? That's premium pricing, Professor - I know exactly what I'm offering."
                    elif is_student:
                        selected_girl.character "What's in it for me? Bareback anal? Is that more expensive? I don't really know what to charge for that... what do you think is fair?"
                    else:
                        selected_girl.character "What's in it for me? Bareback anal access? That's premium pricing, Professor."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "You're in charge, Master. As an experienced mother, if you want to fuck my bare ass with no condom, I won't stop you - my body knows how to handle this."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want to fuck my ass without a condom... okay, I'll let you. Whatever you want."
                    else:
                        selected_girl.character "You're in charge, Master. If you want to fuck my bare ass with no condom, I won't stop you."
                else:
                    selected_girl.character "I don't really like condoms for anal... I prefer it bare."
            
            $ selected_girl.player_knows_anal_condom = True
            
            # Skip menu if already pregnant with his baby
            if not (selected_girl.pregnant and selected_girl.preg_father == "player"):
                menu:
                    "I respect your boundaries. We'll always use condoms when fucking your ass.": 
                        $ selected_girl.wants_anal_condom = True
                        $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                        
                        # Response based on her dominant_approach and role
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "Thank you for understanding. As an experienced mother, I appreciate you respecting my health concerns. It makes me feel even more connected to you."
                            elif is_student:
                                selected_girl.character "Thank you for understanding! That makes me feel so much better about... you know, anal. I'm glad you're being so responsible with me."
                            else:
                                selected_girl.character "Thank you for understanding. Knowing you'll protect my ass makes me feel even more connected to you."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "Mmm... a gentleman who respects an experienced mother's anal boundaries. That's unexpectedly hot. I like that."
                            elif is_student:
                                selected_girl.character "Mmm... you're being so sweet and responsible about anal! That's actually really hot. I like that a lot."
                            else:
                                selected_girl.character "Mmm... a gentleman who respects anal boundaries. That's unexpectedly hot. I like that."
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Fine. As an experienced mother, I'll remember this favor next time you want something - responsible men are valuable."
                            elif is_student:
                                selected_girl.character "Okay! I'll remember you were so nice about this. That was really good of you, Professor."
                            else:
                                selected_girl.character "Fine. I'll remember this favor next time you want something from me."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "Thank you, Master. As an experienced mother, your consideration for my ass and my family means everything to me."
                            elif is_student:
                                selected_girl.character "Thank you, Professor! I'm glad you're being so thoughtful about... about my ass."
                            else:
                                selected_girl.character "Thank you, Master. Your consideration for my ass means everything to me."
                        else:
                            selected_girl.character "Thank you for respecting my boundaries about anal protection."
                    
                    "Would you consider letting me fuck your bare ass sometimes?": 
                        # Check different dominant_approach types
                        if selected_girl.dominant_approach == "sexualized":
                            # Already open to it
                            $ selected_girl.wants_anal_condom = False
                            $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                            if is_base_mother:
                                selected_girl.character "Mmm... bareback fucking my ass? As an experienced woman, I've been wanting you to ask. Take my bare ass, Professor."
                            elif is_student:
                                selected_girl.character "Mmm... bareback anal? Like... without a condom? I've never done that before! But... okay, yeah, I want to try! Take my bare ass!"
                            else:
                                selected_girl.character "Mmm... bareback fucking my ass? I've been wanting you to ask. Take my bare ass."
                            
                        elif selected_girl.dominant_approach == "transactional":
                            # This is where the negotiation happens
                            if is_base_mother:
                                selected_girl.character "Bare ass access? As an experienced mother, I know that's premium service. What are you offering for this privilege?"
                            elif is_student:
                                selected_girl.character "Bare ass? Like no condom for anal? Is that more expensive? I don't know what to charge... what do you think is fair?"
                            else:
                                selected_girl.character "Bare ass access? That's a premium service, Professor. What are you offering?"
                            
                            menu:
                                "Grant her a 400 cash incentive?":
                                    if player.cash >= 400:
                                        $ player.cash -= 400
                                        $ selected_girl.cash += 400
                                        $ selected_girl.wants_anal_condom = False
                                        $ selected_girl.apply_impacts({"corruption": (350, 750), "affection": (250, 750)})
                                        if is_base_mother:
                                            selected_girl.character "400 for bareback anal? As an experienced mother, I know that's fair. Deal. Just don't get too attached - this is business."
                                        elif is_student:
                                            selected_girl.character "400? Oh my god, that's so much! Okay, yeah, you can fuck my ass without a condom for that! Thank you!"
                                        else:
                                            selected_girl.character "400 for bareback anal? Deal. Just don't get too attached - this is a business arrangement."
                                    else:
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time with empty promises. Come back when you can actually pay."
                                        elif is_student:
                                            selected_girl.character "Oh... you don't have enough? That's okay... maybe some other time?"
                                        else:
                                            selected_girl.character "Don't waste my time with empty promises, Professor. Come back when you can actually pay."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                
                                # Only students get grade option
                                "Grant her a grade bump of 25 percent?" if is_student:
                                    if hasattr(selected_girl, 'grades'):
                                        # Check if already at max
                                        if selected_girl.grades >= 100:
                                            selected_girl.character "But... my grades are already at maximum! A bump won't help much... can you offer something else?"
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                        else:
                                            # Apply 25 point increase (not 25% of current grade)
                                            $ new_grade = min(100, selected_girl.grades + 25)
                                            $ selected_girl.grades = new_grade
                                            $ selected_girl.apply_impacts({"baby_desire": (450, 750), "corruption": (550, 1500)})
                                            selected_girl.character "Grade bump for having your baby? As a student, that's perfect security! Fine, you can put a baby in me... but I want this in writing!"
                                    else:
                                        # Missing grade attributes
                                        selected_girl.character "I... don't think you can change my grades? Can you? As a student, maybe just cash would help more?"
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                
                                "Leave it be.":
                                    if is_base_mother:
                                        selected_girl.character "Suit yourself. An experienced mother's bare ass stays on lockdown until you learn how negotiations work."
                                    elif is_student:
                                        selected_girl.character "Oh... okay. Well, if you change your mind about the grade bump or cash, just let me know, I guess?"
                                    else:
                                        selected_girl.character "Suit yourself. My bare ass stays on lockdown until you learn how negotiations work."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        
                        elif selected_girl.dominant_approach in ["compassionate", "dominate"]:
                            # These will agree to please the player
                            $ selected_girl.wants_anal_condom = False
                            $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                            
                            if selected_girl.dominant_approach == "compassionate":
                                if is_base_mother:
                                    selected_girl.character "I trust you completely, Professor. As an experienced mother, let's feel each other without anything between us... even there."
                                elif is_student:
                                    selected_girl.character "I trust you, Professor. I want to feel you without anything between us... even in my ass. That sounds really intimate."
                                else:
                                    selected_girl.character "I trust you completely. Let's feel each other without anything between us... even there."
                            else:
                                if is_base_mother:
                                    selected_girl.character "If that's what you want, Master... as an experienced mother, I'll let you fuck my bare ass."
                                elif is_student:
                                    selected_girl.character "If that's what you want, Professor... okay, I'll let you fuck my ass without a condom."
                                else:
                                    selected_girl.character "If that's what you want, Master... I'll let you fuck my bare ass."
                        
                        else:
                            # Not interested
                            $ selected_girl.wants_anal_condom = True
                            if is_base_mother:
                                selected_girl.character "I'm not comfortable with that. As an experienced mother, I need to be careful about anal health. Let's stick to condoms for now."
                            elif is_student:
                                selected_girl.character "I'm not sure I'm ready for bareback anal... that's kind of scary. Let's stick with condoms, okay?"
                            else:
                                selected_girl.character "I'm not comfortable with that. Let's stick to condoms for anal sex."
        
        # ORAL CONDOM PREFERENCES
        "And for oral sex?":
            # Response based on dominant_approach, role, and pregnancy context
            if selected_girl.pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player":
                # Already pregnant with player's baby
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "Since I'm already carrying your baby, Professor... as an experienced mother, I want to taste you completely. Oral without protection would be incredibly intimate."
                    elif is_student:
                        selected_girl.character "Since I'm already pregnant with your baby... wow, so I can suck your cock without a condom? That sounds... really intimate and special!"
                    else:
                        selected_girl.character "Since I'm already carrying your baby, Professor... I want to taste you completely. Oral without protection would be incredibly intimate."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I'm pregnant with your baby! As an experienced woman, tasting your bare cock while carrying your child... that's incredibly hot. I want to swallow every drop!"
                    elif is_student:
                        selected_girl.character "I'm pregnant with your baby! Oh my god, I can suck your bare cock and taste you? That's so hot! I want to feel you cum in my mouth!"
                    else:
                        selected_girl.character "I'm pregnant with your baby! Tasting your bare cock while carrying your child? That's so hot. I want it!"
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I'm carrying your child. As an experienced mother, bare oral is included in our pregnancy package - no additional charge, though I expect proper support."
                    elif is_student:
                        selected_girl.character "I'm carrying your baby... so does sucking your bare cock cost extra? Or is it free since I'm already pregnant? I'm not sure how the pricing works for oral..."
                    else:
                        selected_girl.character "I'm carrying your child. Since you're the father, bare oral is included in the pregnancy package - no additional charge."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I am carrying your child. As an experienced mother, I know protection is unnecessary for oral. Proceed as you wish."
                    elif is_student:
                        selected_girl.character "I'm carrying your baby... so if you want bare oral, that's okay, Professor. Whatever you want."
                    else:
                        selected_girl.character "I am carrying your child. Protection is unnecessary for oral sex. Proceed as you wish."
                else:
                    selected_girl.character "I'm pregnant with your baby... so I guess we don't need condoms for oral either, right?"
            
            elif selected_girl.wants_oral_condom:
                # She wants protection for oral
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "As an experienced mother, I need to be careful about my health. When I'm sucking your cock, I prefer using protection - I can't risk getting sick while caring for my family."
                    elif is_student:
                        selected_girl.character "I feel so connected to you, but I'm kind of nervous about oral... when I'm sucking your cock, I think I need that protection. I want to be safe."
                    else:
                        selected_girl.character "I feel so connected to you, but when I'm sucking your cock, I need that protection. It lets me relax and enjoy pleasuring you without worry."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "The way you look at me is so hot... but as an experienced mother, I need to be careful. Using protection when I suck your cock shows you respect my health situation."
                    elif is_student:
                        selected_girl.character "The way you look at me is so hot... but I'm kind of scared of oral without protection. Using something makes me feel safer... and actually kind of kinky!"
                    else:
                        selected_girl.character "The way you look at me is so hot... but using protection when I suck your cock can be its own kind of kinky."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "What's in it for me? As an experienced mother with responsibilities, protected oral costs extra - I have to buy dental dams and stay healthy for my family."
                    elif is_student:
                        selected_girl.character "What's in it for me? Protected oral... um, does that cost less than without? I'm not sure about the pricing for blowjobs..."
                    else:
                        selected_girl.character "What's in it for me? Sucking your cock with protection costs extra... unless you make it worth my time."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "You're in charge, Master. As an experienced mother, if you want to use protection when I suck your cock, I'll accept it - I must stay healthy for my family."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want to use protection for oral... I'll do what you want."
                    else:
                        selected_girl.character "You're in charge, Master. If you want to use protection when I suck your cock, I'll accept it."
                else:
                    selected_girl.character "I prefer using protection for oral sex... it's safer that way."
            
            else:
                # She doesn't want protection for oral
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I feel so connected to you. As an experienced mother, I want to taste your bare cock in my mouth - it's a different kind of intimacy that I trust you with."
                    elif is_student:
                        selected_girl.character "I feel so connected to you. I want to taste your bare cock in my mouth... it feels more intimate without anything between us, you know?"
                    else:
                        selected_girl.character "I feel so connected to you. I want to taste your bare cock in my mouth, nothing between us when I'm pleasuring you."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "The way you look at me is so hot. As an experienced woman, I want to feel your bare cock sliding between my lips - motherhood hasn't dulled my desire to please you completely."
                    elif is_student:
                        selected_girl.character "The way you look at me is so hot! I want to taste your bare cock in my mouth... I've never given oral without protection before, that sounds so exciting!"
                    else:
                        selected_girl.character "The way you look at me is so hot. I want to feel your bare cock sliding between my lips, no barriers."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "What's in it for me? Bare cock in my mouth from an experienced mother? That's premium pricing, Professor - I know exactly what I'm offering."
                    elif is_student:
                        selected_girl.character "What's in it for me? Bare oral? Is that more expensive? I don't really know what to charge for blowjobs... what do you think is fair?"
                    else:
                        selected_girl.character "What's in it for me? Bare cock in my mouth? That's premium pricing, Professor."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "You're in charge, Master. As an experienced mother, if you want me to suck your bare cock with no protection, I won't stop you - my mouth is yours to command."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want me to suck your cock without a condom... okay, I'll do it. Whatever you want."
                    else:
                        selected_girl.character "You're in charge, Master. If you want me to suck your bare cock with no protection, I won't stop you."
                else:
                    selected_girl.character "I don't really like protection for oral... I prefer to taste you directly."
            
            $ selected_girl.player_knows_oral_condom = True
            
            # Skip menu if already pregnant with his baby
            if not (selected_girl.pregnant and selected_girl.preg_father == "player"):
                menu:
                    "I respect your boundaries. We'll always use protection for oral.": 
                        $ selected_girl.wants_oral_condom = True
                        $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                        
                        # Response based on her dominant_approach and role
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "Thank you for understanding. As an experienced mother, I appreciate you respecting my health concerns. It makes me feel even more connected to you."
                            elif is_student:
                                selected_girl.character "Thank you for understanding! That makes me feel so much better about... you know, oral. I'm glad you're being so responsible with me."
                            else:
                                selected_girl.character "Thank you for understanding. Knowing you'll protect my health makes me feel even more connected to you."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "Mmm... a gentleman who respects an experienced mother's oral boundaries. That's unexpectedly hot. I like that."
                            elif is_student:
                                selected_girl.character "Mmm... you're being so sweet and responsible about oral! That's actually really hot. I like that a lot."
                            else:
                                selected_girl.character "Mmm... a gentleman who respects oral boundaries. That's unexpectedly hot. I like that."
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Fine. As an experienced mother, I'll remember this favor next time you want something - responsible men are valuable."
                            elif is_student:
                                selected_girl.character "Okay! I'll remember you were so nice about this. That was really good of you, Professor."
                            else:
                                selected_girl.character "Fine. I'll remember this favor next time you want something from me."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "Thank you, Master. As an experienced mother, your consideration for my health and my family means everything to me."
                            elif is_student:
                                selected_girl.character "Thank you, Professor! I'm glad you're being so thoughtful about... about my health."
                            else:
                                selected_girl.character "Thank you, Master. Your consideration for my health means everything to me."
                        else:
                            selected_girl.character "Thank you for respecting my boundaries about oral protection."
                    
                    "Would you consider letting me cum in your mouth without protection sometimes?": 
                        # Check different dominant_approach types
                        if selected_girl.dominant_approach == "sexualized":
                            # Already open to it
                            $ selected_girl.wants_oral_condom = False
                            $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                            if is_base_mother:
                                selected_girl.character "Mmm... cumming in my bare mouth? As an experienced woman, I've been wanting you to ask. I want to taste you."
                            elif is_student:
                                selected_girl.character "Mmm... cumming in my mouth without protection? Like... bare? I've never done that before! But... okay, yeah, I want to taste you!"
                            else:
                                selected_girl.character "Mmm... cumming in my bare mouth? I've been wanting you to ask. I want to taste you."
                            
                        elif selected_girl.dominant_approach == "transactional":
                            # This is where the negotiation happens
                            if is_base_mother:
                                selected_girl.character "Bare cock in my mouth? As an experienced mother, I know that's premium service. What are you offering for this privilege?"
                            elif is_student:
                                selected_girl.character "Bare oral? Like... you cumming in my mouth without protection? Is that more expensive? I don't know what to charge for that... what do you think is fair?"
                            else:
                                selected_girl.character "Bare cock in my mouth? That's a premium service, Professor. What are you offering?"
                            
                            menu:
                                "Grant her a 300 cash incentive?":
                                    if player.cash >= 300:
                                        $ player.cash -= 300
                                        $ selected_girl.cash += 300
                                        $ selected_girl.wants_oral_condom = False
                                        $ selected_girl.apply_impacts({"corruption": (350, 750), "affection": (250, 750)})
                                        if is_base_mother:
                                            selected_girl.character "300 for bare oral? As an experienced mother, I know that's fair. Deal. Just don't get too attached - this is business."
                                        elif is_student:
                                            selected_girl.character "300? Oh my god, that's so much! Okay, yeah, you can cum in my mouth without protection for that! Thank you!"
                                        else:
                                            selected_girl.character "300 for bare oral? Deal. Just don't get too attached - this is a business arrangement."
                                    else:
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time with empty promises. Come back when you can actually pay."
                                        elif is_student:
                                            selected_girl.character "Oh... you don't have enough? That's okay... maybe some other time?"
                                        else:
                                            selected_girl.character "Don't waste my time with empty promises, Professor. Come back when you can actually pay."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                
                                # Only students get grade option
                                "Grant her a grade bump of 25 percent?" if is_student:
                                    if hasattr(selected_girl, 'grades'):
                                        # Check if already at max
                                        if selected_girl.grades >= 100:
                                            selected_girl.character "But... my grades are already at maximum! A bump won't help much... can you offer something else?"
                                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                        else:
                                            # Apply 25 point increase (not 25% of current grade)
                                            $ new_grade = min(100, selected_girl.grades + 25)
                                            $ selected_girl.grades = new_grade
                                            $ selected_girl.apply_impacts({"baby_desire": (350, 750), "corruption": (550, 1500)})
                                            selected_girl.character "Grade bump for having your baby? As a student, that's perfect security! Fine, you can put a baby in me... but I want this in writing!"
                                    else:
                                        # Missing grade attributes
                                        selected_girl.character "I... don't think you can change my grades? Can you? As a student, maybe just cash would help more?"
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                
                                "Leave it be.":
                                    if is_base_mother:
                                        selected_girl.character "Suit yourself. An experienced mother's mouth stays on lockdown until you learn how negotiations work."
                                    elif is_student:
                                        selected_girl.character "Oh... okay. Well, if you change your mind about the grade bump or cash, just let me know, I guess?"
                                    else:
                                        selected_girl.character "Suit yourself. My mouth stays on lockdown until you learn how negotiations work."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        
                        elif selected_girl.dominant_approach in ["compassionate", "dominate"]:
                            # These will agree to please the player
                            $ selected_girl.wants_oral_condom = False
                            $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                            
                            if selected_girl.dominant_approach == "compassionate":
                                if is_base_mother:
                                    selected_girl.character "I trust you completely, Professor. As an experienced mother, let me taste you without anything between us."
                                elif is_student:
                                    selected_girl.character "I trust you, Professor. I want to taste you without anything between us... that sounds really intimate."
                                else:
                                    selected_girl.character "I trust you completely. Let me taste you without anything between us."
                            else:
                                if is_base_mother:
                                    selected_girl.character "If that's what you want, Master... as an experienced mother, I'll let you cum in my bare mouth."
                                elif is_student:
                                    selected_girl.character "If that's what you want, Professor... okay, I'll let you cum in my mouth without protection."
                                else:
                                    selected_girl.character "If that's what you want, Master... I'll let you cum in my bare mouth."
                        
                        else:
                            # Not interested
                            $ selected_girl.wants_oral_condom = True
                            if is_base_mother:
                                selected_girl.character "I'm not comfortable with that. As an experienced mother, I need to be careful about oral health. Let's stick to protection for now."
                            elif is_student:
                                selected_girl.character "I'm not sure I'm ready for you to cum in my mouth without protection... that's kind of scary. Let's stick with protection, okay?"
                            else:
                                selected_girl.character "I'm not comfortable with that. Let's stick to protection for oral sex."
        
        # BODY CONDOM PREFERENCES (for body shots)
        "What about for body shots or other external ejaculation?": 
            # Response based on dominant_approach and role
            if selected_girl.dominant_approach == "compassionate":
                if is_base_mother:
                    selected_girl.character "I feel so connected to you, but as an experienced mother, I prefer using condoms even for body shots. It keeps things cleaner and more controlled for my family life."
                elif is_student:
                    selected_girl.character "I feel so connected to you, but I'm kind of messy... I think I prefer condoms for body shots. It keeps things cleaner and less awkward."
                else:
                    selected_girl.character "I feel so connected to you, but I prefer using condoms even for body shots. It keeps things cleaner and more controlled."
            elif selected_girl.dominant_approach == "sexualized":
                if is_base_mother:
                    selected_girl.character "The way you look at me is so hot... but as an experienced mother, I need to be careful. Using condoms for body shots shows you respect my practical needs."
                elif is_student:
                    selected_girl.character "The way you look at me is so hot... but I'm kind of worried about getting cum everywhere. Using condoms for body shots can be its own kind of sexy, right?"
                else:
                    selected_girl.character "The way you look at me is so hot... but using condoms for body shots can be its own kind of sexy."
            elif selected_girl.dominant_approach == "transactional":
                if is_base_mother:
                    selected_girl.character "What's in it for me? As an experienced mother with responsibilities, clean body shots cost extra - I have to maintain certain standards for my family."
                elif is_student:
                    selected_girl.character "What's in it for me? Body shots... um, does that cost extra if you want it clean? I'm not sure about the pricing for that..."
                else:
                    selected_girl.character "What's in it for me? Using condoms for body shots costs extra... unless you make it worth my time."
            elif selected_girl.dominant_approach == "dominate":
                if is_base_mother:
                    selected_girl.character "You're in charge, Master. As an experienced mother, if you want to use condoms for body shots, I'll accept it - I must be careful as a mother."
                elif is_student:
                    selected_girl.character "You're in charge, Professor. If you want to use condoms for body shots... I'll do what you want."
                else:
                    selected_girl.character "You're in charge, Master. If you want to use condoms for body shots, I'll accept it."
            else:
                selected_girl.character "I'm not sure about body shots... I prefer to keep things clean."
            
            $ selected_girl.player_knows_body_condom = True
            
            menu:
                "I like keeping things clean and controlled.": 
                    $ selected_girl.wants_body_condom = True
                    $ selected_girl.apply_impacts({"discipline": (250, 750), "affection": (250, 750)})
                    
                    if selected_girl.dominant_approach == "compassionate":
                        if is_base_mother:
                            selected_girl.character "Thank you for understanding. Being clean and controlled is important as a mother - I appreciate your consideration for my family life."
                        elif is_student:
                            selected_girl.character "Thank you for understanding! I'm glad you like keeping things clean too. That makes me feel better about... you know, body stuff."
                        else:
                            selected_girl.character "Thank you for understanding. I appreciate that you want to keep things clean."
                    elif selected_girl.dominant_approach == "sexualized":
                        if is_base_mother:
                            selected_girl.character "Mmm... a clean and controlled approach from an experienced woman? That's surprisingly hot for a mother. I like that."
                        elif is_student:
                            selected_girl.character "Mmm... you being clean and controlled? That's actually really hot! I like that a lot."
                        else:
                            selected_girl.character "Mmm... a clean and controlled approach. That's unexpectedly hot. I like that."
                    elif selected_girl.dominant_approach == "transactional":
                        if is_base_mother:
                            selected_girl.character "Fine. As an experienced mother, I'll remember this practical approach next time you want something - mothers appreciate consideration."
                        elif is_student:
                            selected_girl.character "Okay! I'll remember you were so practical about this. That was really smart of you, Professor."
                        else:
                            selected_girl.character "Fine. I'll remember this practical approach next time you want something."
                    elif selected_girl.dominant_approach == "dominate":
                        if is_base_mother:
                            selected_girl.character "Yes, Master. Being clean and controlled is the right choice for an experienced mother."
                        elif is_student:
                            selected_girl.character "Yes, Professor. Being clean and controlled is what you want - I'll remember that."
                        else:
                            selected_girl.character "Yes, Master. Being clean and controlled is what you want."
                    else:
                        if is_base_mother:
                            selected_girl.character "Good. A mother needs to be practical about these things."
                        else:
                            selected_girl.character "Good. I prefer keeping things clean too."
                
                "I love the idea of my cum on your bare skin...": 
                    if selected_girl.dominant_approach == "sexualized":
                        $ selected_girl.wants_body_condom = False
                        $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                        if is_base_mother:
                            selected_girl.character "Mmm... marking my body with your cum? As an experienced woman, that's so hot. Do it - even mothers need to feel desired and marked."
                        elif is_student:
                            selected_girl.character "Mmm... marking my body with your cum? That's so hot! I've never done that before! Do it - mark me with your cum!"
                        else:
                            selected_girl.character "Mmm... marking my body with your cum? That's so hot. Do it."
                            
                    elif selected_girl.dominant_approach == "transactional":
                        # This is where the negotiation happens
                        if is_base_mother:
                            selected_girl.character "Marking my bare body with your cum? As an experienced mother, I know that's premium service. What are you offering for this privilege?"
                        elif is_student:
                            selected_girl.character "Marking my body with your cum? Like... bare? Is that more expensive? I don't know what to charge for that... what do you think is fair?"
                        else:
                            selected_girl.character "Marking my bare body with your cum? That's a premium service, Professor. What are you offering?"
                        
                        menu:
                            "Grant her a 300 cash incentive?":
                                if player.cash >= 300:
                                    $ player.cash -= 300
                                    $ selected_girl.cash += 300
                                    $ selected_girl.wants_body_condom = False
                                    $ selected_girl.apply_impacts({"corruption": (350, 750), "affection": (250, 750)})
                                    if is_base_mother:
                                        selected_girl.character "300 for body marking privileges? As an experienced mother, I know that's fair. Fine, just don't get any crazy ideas - I'm still a mother."
                                    elif is_student:
                                        selected_girl.character "300? Oh my god, that's so much! Okay, yeah, you can mark my body with your cum for that! Thank you!"
                                    else:
                                        selected_girl.character "300 for body marking privileges? Deal. Just don't get too attached - this is business."
                                else:
                                    if is_base_mother:
                                        selected_girl.character "Don't waste an experienced mother's time with empty promises. Come back when you can actually pay."
                                    elif is_student:
                                        selected_girl.character "Oh... you don't have enough? That's okay... maybe some other time?"
                                    else:
                                        selected_girl.character "Don't waste my time with empty promises, Professor. Come back when you can actually pay."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            
                            # Only students get grade option
                            "Grant her a grade bump of 25 percent?" if is_student:
                                if hasattr(selected_girl, 'grades'):
                                    # Check if already at max
                                    if selected_girl.grades >= 100:
                                        selected_girl.character "But... my grades are already at maximum! A bump won't help much... can you offer something else?"
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    else:
                                        # Apply 25 point increase (not 25% of current grade)
                                        $ new_grade = min(100, selected_girl.grades + 25)
                                        $ selected_girl.grades = new_grade
                                        $ selected_girl.apply_impacts({"baby_desire": (450, 750), "corruption": (750, 1500)})
                                        selected_girl.character "Grade bump for having your baby? As a student, that's perfect security! Fine, you can put a baby in me... but I want this in writing!"
                                else:
                                    # Missing grade attributes
                                    selected_girl.character "I... don't think you can change my grades? Can you? As a student, maybe just cash would help more?"
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            
                            "Leave it be.":
                                if is_base_mother:
                                    selected_girl.character "Suit yourself. An experienced mother's bare skin stays off-limits until you learn how negotiations work."
                                elif is_student:
                                    selected_girl.character "Oh... okay. Well, if you change your mind about the grade bump or cash, just let me know, I guess?"
                                else:
                                    selected_girl.character "Suit yourself. My bare skin stays off-limits until you learn how negotiations work."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    
                    elif selected_girl.dominant_approach in ["compassionate", "dominate"]:
                        # These will agree to please the player
                        $ selected_girl.wants_body_condom = False
                        $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                        
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "I trust you completely, Professor. As an experienced mother, let me give you this intimacy - mark my bare skin if it pleases you."
                            elif is_student:
                                selected_girl.character "I trust you, Professor. I want to feel your cum on my bare skin... that sounds really intimate and special."
                            else:
                                selected_girl.character "I trust you completely. Let me give you this intimacy - mark my bare skin if it pleases you."
                        else:
                            if is_base_mother:
                                selected_girl.character "If that's what you want, Master... as an experienced mother, I'll let you mark my bare body."
                            elif is_student:
                                selected_girl.character "If that's what you want, Professor... okay, I'll let you cum on my bare body."
                            else:
                                selected_girl.character "If that's what you want, Master... I'll let you mark my bare body."
                    
                    else:
                        # Not interested
                        if selected_girl.dominant_approach == "admiring":
                            if is_base_mother:
                                selected_girl.character "I admire your confidence, but... as a mother, I think we should keep things clean, especially with my family to consider."
                            elif is_student:
                                selected_girl.character "I admire your confidence, but... I think we should keep things clean. I'm kind of worried about messes."
                            else:
                                selected_girl.character "I admire your confidence, but... I think we should keep things clean."
                            # Convert trust to fear (positive trust becomes negative fear)
                            $ selected_girl.apply_impacts({"affection": (-750, -250), "fear": (-750, -250)})
                        else:
                            if is_base_mother:
                                selected_girl.character "That's inappropriate to say, Professor. As a mother, I need to maintain certain standards for my family."
                            elif is_student:
                                selected_girl.character "That's inappropriate to say, Professor... I'm not comfortable with that kind of talk."
                            else:
                                selected_girl.character "That's inappropriate to say, Professor."
                            # Convert trust to fear (positive trust becomes negative fear)
                            $ selected_girl.apply_impacts({"affection": (-750, -250), "fear": (-750, -250)})               
        
        # BIRTH CONTROL OPTIONS
        "What are your thoughts on birth control methods?": 
            # Reveal birth control status if player doesn't know yet
            if not selected_girl.bc_status_known:
                $ selected_girl.bc_status_known = True
            
            # Response based on dominant_approach, role, and current birth control status
            if selected_girl.birth_control:
                # She IS on birth control
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm currently on birth control pills, which I take regularly. As an experienced mother, I need to be responsible about family planning - I can't just let our family grow without preparation. Do you want me to stay on them or should we think about expanding our family?"
                        else:
                            selected_girl.character "I'm currently on birth control pills, which I take regularly. As an experienced mother, I believe in being responsible about family planning - it's important to be prepared for children."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm on birth control pills right now. My mom said it's important to be responsible... but since we already have a baby together, I wonder if you want me to stay on them or not?"
                        else:
                            selected_girl.character "I'm on birth control pills right now. My mom said it's important to be responsible... I think it's smart to be careful until I'm ready to start a family."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm currently on birth control pills, which I take regularly. Since we already have a baby together, do you want me to continue taking them or should we let nature take its course?"
                        else:
                            selected_girl.character "I'm currently on birth control pills, which I take regularly. I think it's important to be responsible and plan ahead for when I'm ready to have children."
                
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm on the pill. As an experienced mother, I need to be careful... but it's kind of hot knowing we're playing safe. Though since we already have a baby, maybe you want me off them?"
                        else:
                            selected_girl.character "I'm on the pill. As an experienced mother, I need to be careful... but it's kind of hot knowing we're playing safe while still being so intimate and risky in other ways."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm on the pill! It's nice not having to worry, though since we already have a baby, I wonder if you want me to stay on them or go raw all the time?"
                        else:
                            selected_girl.character "I'm on the pill! It's nice not having to worry, though sometimes I wonder what it would feel like completely raw... that sounds so exciting!"
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm on the pill. It's nice not having to worry, but since we already have a baby together, maybe you want me off them so we can have more?"
                        else:
                            selected_girl.character "I'm on the pill. It's nice not having to worry, though sometimes I wonder what it would feel like completely raw..."
                
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm on birth control pills. As an experienced mother, I can't afford surprises for our growing family. Unless you're planning to make it worth my while to stop taking them?"
                        else:
                            selected_girl.character "I'm on birth control pills. As an experienced mother, I know children are expensive - it's just smart business to control when they happen."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm on birth control pills. But since we already have a baby together, I could be convinced to stop... for the right price or grade bump, you know?"
                        else:
                            selected_girl.character "I'm on birth control pills. I think it's smart - babies are expensive and I need to focus on my career first."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm on birth control pills. But since we already have a baby together, I could be convinced to stop... for the right price, of course."
                        else:
                            selected_girl.character "I'm on birth control pills. I'm practical - children are a 20-year investment and I need to be financially ready first."
                
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I am on birth control. As an experienced mother, I must protect our existing family. If you wish me to stop, that is your decision to make."
                        else:
                            selected_girl.character "I am on birth control. As an experienced mother, I must protect my existing family. It is the logical choice for responsible family planning."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm on birth control. If you want me to stop taking them, I will. Whatever you decide, Professor."
                        else:
                            selected_girl.character "I'm on birth control. It is the responsible choice for someone focused on their education and future."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I am on birth control. If you wish me to stop, that is your decision to make."
                        else:
                            selected_girl.character "I am on birth control. It is the logical choice for someone planning their future carefully."
                else:
                    selected_girl.character "I'm on birth control pills right now. They've been working for me."
            else:
                # She is NOT on birth control
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on any birth control right now. As an experienced mother, my body already knows how to handle children, and I trust you completely with our family planning. Should I stay off them?"
                        else:
                            selected_girl.character "I'm not on any birth control right now. As an experienced mother, I prefer natural family planning - my body knows what it's doing."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on birth control right now. Since we already have a baby together, I trust you and want to experience everything naturally... but should I stay off them?"
                        else:
                            selected_girl.character "I'm not on birth control right now. I prefer natural methods - I think it's better for my body and I want to be ready when the time is right."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on any birth control right now. Since we already have a baby together, I prefer to let things happen naturally between us. Should I continue like this?"
                        else:
                            selected_girl.character "I'm not on any birth control right now. I prefer to let things happen naturally - I think it's more intimate and authentic."
                
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on birth control. As an experienced mother, I know what my body can do... and the risk of another baby with you makes everything so much more intense! Should I stay off them?"
                        else:
                            selected_girl.character "I'm not on birth control. As an experienced mother, I know what my body can do... and the risk makes everything so much more intense, doesn't it?"
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on birth control! Oh my god, the risk of another baby with you is so exciting! I love not knowing what might happen... should I stay off them?"
                        else:
                            selected_girl.character "I'm not on birth control! Oh my god, the risk is so exciting! I love not knowing what might happen... it makes everything more thrilling!"
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on birth control. The risk of another baby with you is so thrilling! I love not knowing what might happen... should I stay unprotected?"
                        else:
                            selected_girl.character "I'm not on birth control. I love the thrill of not knowing what might happen... it makes everything more exciting!"
                
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on birth control. As an experienced mother, another baby with you could be smart business... if you're prepared to support our growing family."
                        else:
                            selected_girl.character "I'm not on birth control. As an experienced mother, I see it as an investment opportunity - but only with the right financial partner."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on birth control! No pills, no barriers... just pure opportunity for another baby with you! But if you want me to start, that'll cost extra..."
                        else:
                            selected_girl.character "I'm not on birth control. I see it as leaving my options open - the right opportunity could secure my future."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on birth control. No pills, no barriers... just pure opportunity for another baby with you. For both of us!"
                        else:
                            selected_girl.character "I'm not on birth control. I believe in keeping my options open - you never know when the right opportunity might come along."
                
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I am not on birth control. As an experienced mother, my body is prepared for another child with you. If you wish me to start, that is your command."
                        else:
                            selected_girl.character "I am not on birth control. As an experienced mother, my body is prepared for whatever nature intends. It is the natural way."
                    elif is_student:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I'm not on birth control. If you want me to start taking them, I will. Whatever you want, Professor."
                        else:
                            selected_girl.character "I'm not on birth control. I prefer to face consequences directly rather than hiding behind medication."
                    else:
                        if selected_girl.kids_with_player > 0:
                            selected_girl.character "I am not on birth control. My body is prepared for another child with you. If you wish me to start, that is your decision to make."
                        else:
                            selected_girl.character "I am not on birth control. I believe in facing whatever happens naturally."
                else:
                    if selected_girl.kids_with_player > 0:
                        selected_girl.character "I'm not on any birth control right now. Since we already have a baby together, I prefer to let things happen naturally between us."
                    else:
                        selected_girl.character "I'm not on any birth control right now. I prefer to let things happen naturally."
            
            menu:
                "Have you considered starting birth control?" if not selected_girl.birth_control: 
                    if selected_girl.dominant_approach in ["compassionate", "dominate"]:
                        $ selected_girl.birth_control = True
                        $ selected_girl.apply_impacts({"discipline": (250, 750)})
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "You're right... as an experienced mother, I should be more responsible about family planning. I'll start birth control for our family's sake."
                                else:
                                    selected_girl.character "You're right... as an experienced mother, I should be more responsible about family planning. I'll start birth control."
                            elif is_student:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "You're right... I should be more responsible, especially since we already have a baby. My mom would be happy I'm being careful. I'll start birth control."
                                else:
                                    selected_girl.character "You're right... I should be more responsible. My mom would be happy I'm being careful. I'll start birth control."
                            else:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "You're right... I should be more responsible, especially since we already have a baby. I'll start birth control."
                                else:
                                    selected_girl.character "You're right... I should be more responsible. I'll start birth control."
                        else:  # dominate approach
                            if is_base_mother:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "If you think it's best, Professor. As an experienced mother, I will start birth control to better serve your wishes for our family."
                                else:
                                    selected_girl.character "If you think it's best, Professor. As an experienced mother, I will start birth control to better serve your wishes."
                            elif is_student:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "If you think it's best, Professor. Since we already have a baby, I'll start birth control. Whatever you want."
                                else:
                                    selected_girl.character "If you think it's best, Professor. I'll start birth control. Whatever you want."
                            else:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "If you think it's best, I'll start birth control for our family. Your will is my command."
                                else:
                                    selected_girl.character "If you think it's best, I'll start birth control. Your will is my command."
                
                    elif selected_girl.dominant_approach == "transactional":
                        if is_base_mother:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Starting birth control? That costs money, Professor. As an experienced mother with our growing family, what are you offering to cover the expenses and compensate me for the inconvenience?"
                            else:
                                selected_girl.character "Starting birth control? That costs money, Professor. As an experienced mother, what are you offering to cover the expenses and compensate me for the inconvenience?"
                        elif is_student:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Starting birth control? That costs money, Professor. Since we already have a baby, what are you offering to cover the expenses and compensate me?"
                            else:
                                selected_girl.character "Starting birth control? That costs money, Professor. What are you offering to cover the expenses and compensate me for the inconvenience?"
                        else:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Starting birth control? That costs money, Professor. Since we already have a baby, what are you offering to cover the expenses and compensate me?"
                            else:
                                selected_girl.character "Starting birth control? That costs money, Professor. What are you offering to cover the expenses and compensate me for the inconvenience?"
                        menu:
                            "Offer 300 cash for birth control expenses?":
                                if player.cash >= 300:
                                    $ player.cash -= 300
                                    $ selected_girl.cash += 300
                                    $ selected_girl.birth_control = True
                                    $ selected_girl.apply_impacts({"discipline": (250, 750), "corruption": (450, 750)})
                                    if is_base_mother:
                                        if selected_girl.kids_with_player > 0:
                                            selected_girl.character "300 covers the prescription and compensates me for being a responsible mother to our family. Fine, I'll start birth control."
                                        else:
                                            selected_girl.character "300 covers the prescription and compensates me for being a responsible mother. Fine, I'll start birth control."
                                    elif is_student:
                                        if selected_girl.kids_with_player > 0:
                                            selected_girl.character "300 for birth control? Oh my god, that's so much! Okay, yeah, I'll start taking them for our baby's sake. Thank you, Professor!"
                                        else:
                                            selected_girl.character "300 for birth control? Oh my god, that's so much! Okay, yeah, I'll start taking them. Thank you, Professor!"
                                    else:
                                        if selected_girl.kids_with_player > 0:
                                            selected_girl.character "300 covers the pills and my time. Fine, I'll start birth control for our family."
                                        else:
                                            selected_girl.character "300 covers the pills and my time. Fine, I'll start birth control."
                                else:
                                    $ selected_girl.birth_control = False
                                    if is_base_mother:
                                        selected_girl.character "Don't waste an experienced mother's time. Come back when you can afford my reproductive health."
                                    elif is_student:
                                        selected_girl.character "Oh... you don't have enough? That's okay... I'll figure something else out, I guess."
                                    else:
                                        selected_girl.character "Don't waste my time. Come back when you can afford my reproductive health."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            
                            # Only students get grade option
                            "Grant her a grade bump of 15 percent?" if is_student:
                                if selected_girl.grades >= 100:
                                    selected_girl.character "But... my grades are already at maximum! A bump won't help much... can you offer something else?"
                                    $ selected_girl.birth_control = False
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                else:
                                    # Apply 15 point increase (not 15% of current grade)
                                    $ new_grade = min(100, selected_girl.grades + 15)
                                    $ selected_girl.grades = new_grade
                                    $ selected_girl.birth_control = True
                                    $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750), "corruption": (750, 1500), "discipline": (-750, -250)})
                                    if selected_girl.kids_with_player > 0:
                                        selected_girl.character "Fine. Guess you don't want to worry about having to support another child."
                                    else:
                                        selected_girl.character "A grade bump? Really? Oh my god, yes! My grades will be so easy! Deal! Start popping em now!"
                            
                            "Leave it be.":
                                if is_base_mother:
                                    if selected_girl.kids_with_player > 0:
                                        selected_girl.character "Fine. But don't come crying to me when I get pregnant and you have to help support another child in our family."
                                    else:
                                        selected_girl.character "Fine. But don't come crying to me when I get pregnant and you have to help support another child."
                                elif is_student:
                                    if selected_girl.kids_with_player > 0:
                                        selected_girl.character "Oh... okay. Well, if I get pregnant again, that's... your responsibility too, right? Just so we're clear?"
                                    else:
                                        selected_girl.character "Oh... okay. Well, if I get pregnant, that's... your responsibility too, right? Just so we're clear?"
                                else:
                                    if selected_girl.kids_with_player > 0:
                                        selected_girl.character "Fine. But don't come crying to me when I get pregnant and you have to pay child support for our next baby."
                                    else:
                                        selected_girl.character "Fine. But don't come crying to me when I get pregnant and you have to pay child support."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    
                    elif selected_girl.dominant_approach == "sexualized":
                        if is_base_mother:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Birth control? But the risk of another baby with you is so exciting... though as an experienced mother, I guess I should be more careful. Maybe if you make it worth my while to stay on the pill?"
                            else:
                                selected_girl.character "Birth control? But the risk is so exciting... though as an experienced mother, I guess I should be more careful. Maybe if you make it worth my while to stay on the pill?"
                        elif is_student:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Birth control? But the risk of another baby with you is so exciting! I don't know, Professor... you'd have to convince me it's worth giving up that thrill!"
                            else:
                                selected_girl.character "Birth control? But the risk is so exciting! I don't know, Professor... you'd have to convince me it's worth giving up that thrill!"
                        else:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Birth control? But the risk of another baby with you is so exciting... I don't know, Professor. You'd have to convince me it's worth giving up that thrill!"
                            else:
                                selected_girl.character "Birth control? But the risk is so exciting... I don't know, Professor. You'd have to convince me it's worth giving up that thrill!"
                    
                    else:  # neutral or other approaches
                        if is_base_mother:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "I'm not sure. As an experienced mother with our family, I should probably be more careful, but I don't like putting chemicals in my body."
                            else:
                                selected_girl.character "I'm not sure. As an experienced mother, I should probably be more careful, but I don't like putting chemicals in my body."
                        elif is_student:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "I'm not sure... my mom said birth control is important, especially since we already have a baby, but I'm kind of scared of putting chemicals in my body."
                            else:
                                selected_girl.character "I'm not sure... my mom said birth control is important, but I'm kind of scared of putting chemicals in my body."
                        else:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "I'm not sure. Since we already have a baby, maybe I should be more careful, but I prefer to let things happen naturally."
                            else:
                                selected_girl.character "I'm not sure. I prefer to let things happen naturally."
                    
                "Would you consider stopping birth control?" if selected_girl.birth_control:
                    if selected_girl.baby_desire > 50 or selected_girl.dominant_approach in ["sexualized", "compassionate", "dominate"]:
                        $ selected_girl.birth_control = False
                        $ selected_girl.apply_impacts({"baby_desire": (1000, 1500)})
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "You want me to stop birth control? To expand our family? As an experienced mother, I'd love that. I'll stop taking them right away for our growing family."
                                else:
                                    selected_girl.character "You want me to stop birth control... to start a family with you? As an experienced mother, I'd love that. I'll stop taking them right away."
                            elif is_student:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "You want me to stop birth control? So we could... have another baby? Wow! I'd love that! I'll stop taking them right away!"
                                else:
                                    selected_girl.character "You want me to stop birth control... so we could have a baby? Wow! I'd love that! I'll stop taking them right away!"
                            else:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "You want me to stop birth control? I'd love that. I want to expand our family and experience everything with you naturally."
                                else:
                                    selected_girl.character "You want me to stop birth control? I'd love that. I want to start a family and experience everything with you naturally."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Stop birth control? So you can breed me again? Mmm... as an experienced woman, the thought of another baby with you is so hot. I'll stop taking them immediately."
                                else:
                                    selected_girl.character "You want me to stop birth control... so you can breed me? Mmm... as an experienced woman, the thought of your baby is so hot. I'll stop taking them immediately."
                            elif is_student:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Stop birth control? So you can get me pregnant again? Oh my god, that's so hot! Yes! I'll stop right now!"
                                else:
                                    selected_girl.character "You want me to stop birth control... so you can get me pregnant? Oh my god, that's so hot! Yes! I'll stop right now!"
                            else:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "Stop birth control? So you can breed me again? Mmm... the thought of another baby with you is so hot. I'll stop taking them."
                                else:
                                    selected_girl.character "You want me to stop birth control... so you can breed me? Mmm... the thought of your baby is so hot. I'll stop taking them."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "If you wish me to stop birth control to expand our family, Professor. As an experienced mother, I will obey your command for our children."
                                else:
                                    selected_girl.character "If you wish me to stop birth control to start our family, Professor. As an experienced mother, I will obey your command."
                            elif is_student:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "If you want me to stop birth control for our next baby, Professor. Okay, I'll stop taking them. Whatever you want."
                                else:
                                    selected_girl.character "If you want me to stop birth control for your first baby, Professor. Okay, I'll stop taking them. Whatever you want."
                            else:
                                if selected_girl.kids_with_player > 0:
                                    selected_girl.character "If you wish me to stop birth control to expand our family, I will obey your command."
                                else:
                                    selected_girl.character "If you wish me to stop birth control to start our family, I will obey your command."
                    elif selected_girl.dominant_approach == "transactional":
                        if is_base_mother:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Stop birth control? So you can get me pregnant again? That's a significant financial commitment for our growing family, Professor. What are you offering for this... upgrade?"
                            else:
                                selected_girl.character "You want me to stop birth control... to get pregnant? That's a significant commitment, Professor. What's your offer for this?"
                        elif is_student:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Stop birth control? So you can get me pregnant again? That's a huge commitment for our family, Professor. What are you offering for this... upgrade?"
                            else:
                                selected_girl.character "You want me to stop birth control... to get pregnant? That's a huge commitment, Professor. What are you offering for this?"
                        else:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Stop birth control? So you can get me pregnant again? That's a significant financial commitment for our family, Professor. What are you offering for this... upgrade?"
                            else:
                                selected_girl.character "You want me to stop birth control... to get pregnant? That's a significant commitment, Professor. What's your offer for this?"
                        menu:
                            "Offer 5000 cash for stopping birth control?":
                                if player.cash >= 5000:
                                    $ player.cash -= 5000
                                    $ selected_girl.cash += 5000
                                    $ selected_girl.birth_control = False
                                    $ selected_girl.apply_impacts({"baby_desire": (250, 750), "corruption": (500, 1500), "naturism":(250, 750)})
                                    if is_base_mother:
                                        if selected_girl.kids_with_player > 0:
                                            selected_girl.character "5000 to stop taking pills and risk another baby? As an experienced mother, that's reasonable for our growing family. Fine, I'll stop birth control."
                                        else:
                                            selected_girl.character "5000 to stop taking pills and risk pregnancy? As an experienced mother, that's reasonable. Fine, I'll stop birth control."
                                    elif is_student:
                                        if selected_girl.kids_with_player > 0:
                                            selected_girl.character "5000? Oh my god, that's so much money! Okay, yeah, I'll stop taking my pills! You can get me pregnant again for that!"
                                        else:
                                            selected_girl.character "5000? Oh my god, that's so much money! Okay, yeah, I'll stop taking my pills! You can get me pregnant for that!"
                                    else:
                                        if selected_girl.kids_with_player > 0:
                                            selected_girl.character "5000 to stop taking pills and risk another baby for our family? Deal. I'll stop birth control."
                                        else:
                                            selected_girl.character "5000 to stop taking pills and risk pregnancy? Deal. I'll stop birth control."
                                else:
                                    $ selected_girl.birth_control = True
                                    if is_base_mother:
                                        selected_girl.character "You think that's enough for an experienced woman to carry a child for you? Don't insult me. Come back when you're serious."
                                    elif is_student:
                                        selected_girl.character "That's not enough for a baby, is it? You need to be more serious than that."
                                    else:
                                        selected_girl.character "You think that's enough for potentially 18 years of commitment? Don't insult me. Come back when you're serious."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            "Offer 10,000 to cover all medical expenses, as nature intended.":
                                player.character "This includes vaginal condoms too."
                                if player.cash >= 10000:
                                    $ player.cash -= 10000
                                    $ selected_girl.cash += 10000
                                    $ selected_girl.birth_control = False
                                    $ selected_girl.wants_vaginal_condom = False
                                    $ selected_girl.player_knows_vaginal_condom = True
                                    $ selected_girl.apply_impacts({"baby_desire": (500, 1000), "affection": (250, 750), "fear": (-750, -250), "corruption": (750, 1500), "naturism":(250, 750)})
                                    if is_base_mother:
                                        if selected_girl.kids_with_player > 0:
                                            selected_girl.character "Medical coverage for another child? As an experienced mother, I appreciate that security for our family. Fine, you can put another baby in me... but I want this wired to me now."
                                        else:
                                            selected_girl.character "Medical coverage for your child? As an experienced mother, I appreciate that security. Fine, you can put a baby in me... but I want this wired to me now."
                                    elif is_student:
                                        if selected_girl.kids_with_player > 0:
                                            selected_girl.character "You'll cover all the doctor stuff for another baby? Really? Okay! That makes me feel so much better about expanding our family! Yeah, let's do it!"
                                        else:
                                            selected_girl.character "You'll cover all the doctor stuff for a baby? Really? Okay! That makes me feel so much better about this! Yeah, let's do it!"
                                else:
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    if selected_girl.kids_with_player > 0:
                                        selected_girl.character "Medical coverage for another child? You can't afford it, and can't count, so piss off."
                                    else:
                                        selected_girl.character "Medical coverage? That's security, but come back when you can actually afford it... PRO...FESS....OR..... dumbass."
                            "Grant her a grade bump of 50 percent?" if is_student:
                                if selected_girl.grades >= 100:
                                    selected_girl.character "But... my grades are already perfect! A bump won't do anything... can you offer something else?"
                                    $ selected_girl.birth_control = True
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                else:
                                    # Apply 50 point increase
                                    player.character "This also includes no vaginal condoms, remember that."
                                    $ selected_girl.wants_vaginal_condom = False
                                    $ selected_girl.player_knows_vaginal_condom = True
                                    $ new_grade = min(100, selected_girl.grades + 50)
                                    $ selected_girl.grades = new_grade
                                    $ selected_girl.birth_control = False
                                    $ selected_girl.apply_impacts({"baby_desire": (450, 750), "affection": (250, 750), "corruption": (250, 750), "discipline": (-750, -250), "naturism":(250, 750)})
                                    if selected_girl.kids_with_player > 0:
                                        selected_girl.character "A 50-point grade bump to have another baby? Fine. My grades will make things so much easier. Deal."
                                    else:
                                        selected_girl.character "A 50-point grade bump to have your baby? Oh my god, yes! My grades will be perfect! Deal! I'll stop taking my pills right now!"
                        
                            "Leave it be.":
                                if is_base_mother:
                                    if selected_girl.kids_with_player > 0:
                                        selected_girl.character "Smart move. An experienced mother with our family isn't cheap, and I'm not getting pregnant again without proper compensation."
                                    else:
                                        selected_girl.character "Smart move. An experienced mother isn't cheap, and I'm not getting pregnant without proper compensation."
                                elif is_student:
                                    if selected_girl.kids_with_player > 0:
                                        selected_girl.character "Oh... okay. Maybe having another baby right now is... a lot for our family. I understand."
                                    else:
                                        selected_girl.character "Oh... okay. Maybe having a baby right now is... a lot. I understand."
                                else:
                                    if selected_girl.kids_with_player > 0:
                                        selected_girl.character "Smart move. I'm not getting pregnant again for our family without proper compensation."
                                    else:
                                        selected_girl.character "Smart move. I'm not getting pregnant without proper compensation."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    else:
                        # Low baby desire and not in the listed approaches
                        if is_base_mother:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Stop birth control? As an experienced mother with our family to think about, I'm not sure that's wise right now. We need to be responsible."
                            else:
                                selected_girl.character "Stop birth control? As an experienced mother, I'm not sure that's wise right now. We need to be responsible."
                        elif is_student:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Stop birth control? I'm not sure that's a good idea... I'm kind of scared of having another baby right now while I'm still in school."
                            else:
                                selected_girl.character "Stop birth control? I'm not sure that's a good idea... I'm kind of scared of getting pregnant right now."
                        else:
                            if selected_girl.kids_with_player > 0:
                                selected_girl.character "Stop birth control? I'm not sure that's wise for our family right now. I need to think about our future."
                            else:
                                selected_girl.character "Stop birth control? I'm not sure that's wise. I need to think about my future."
                        $ selected_girl.apply_impacts({"affection": (-750, -250)})

                "Never mind.":  
                    selected_girl.character "Oh... okay. Well, let me know if you want to talk about anything else."
                    $ selected_girl.apply_impacts({"affection": (250, 750)})
                    return
                
    # PHASE 4: STRATEGIC DIALOGUE (MEANINGFUL CHOICES) - WITH CONDOM INTEGRATION
    if selected_girl.pregnant and selected_girl.player_knows_pregnant and selected_girl.knows_pregnant:
        menu:
            # SUPPORTIVE APPROACH (INCREASES BABY_DESIRE)
            "This is a beautiful time in your life. How are you feeling about it?":
                $ selected_girl.apply_impacts({"affection": (750, 1500), "baby_desire": (750, 1500)})
                
                if selected_girl.dominant_approach == "compassionate":
                    if selected_girl.baby_desire > 70:
                        if is_base_mother:
                            selected_girl.character "It's wonderful! As an experienced mother, I feel so connected to you and our growing family. My body was made for this purpose, and I love that you're here with me through it all."
                        elif is_student:
                            selected_girl.character "It's wonderful! I feel so connected to you. I've always dreamed about being pregnant with you, and now it's really happening!"
                        else:
                            selected_girl.character "It's wonderful! I feel so connected to you. I've always wanted to experience this with you."
                    elif selected_girl.baby_desire > 30:
                        if is_base_mother:
                            selected_girl.character "It's... unexpected but as an experienced mother, I'm trying to be positive about expanding our family, though I'm nervous about managing another child."
                        elif is_student:
                            selected_girl.character "It's... unexpected but I'm trying to be positive about it, though I'm scared about being pregnant and in school."
                        else:
                            selected_girl.character "It's... unexpected but I'm trying to be positive about it, though I'm scared."
                    else:
                        if is_base_mother:
                            selected_girl.character "I'm scared... as an experienced mother, I know how much work this is, and I wasn't planning another pregnancy right now."
                        elif is_student:
                            selected_girl.character "I'm scared... I didn't plan for this to happen while I'm still in school. I don't know what to do."
                        else:
                            selected_girl.character "I'm scared... I didn't plan for this to happen."
                            
                elif selected_girl.dominant_approach == "sexualized":
                    if selected_girl.baby_desire > 70:
                        if is_base_mother:
                            selected_girl.character "The way you look at me while I'm pregnant is so hot... knowing I'm carrying your child makes me want you even more. As an experienced woman, pregnancy makes me feel incredibly sexy!"
                        elif is_student:
                            selected_girl.character "The way you look at me while I'm pregnant is so hot... knowing I'm carrying your baby makes me so horny! I can't stop thinking about you!"
                        else:
                            selected_girl.character "The way you look at me while I'm pregnant is so hot... knowing I'm carrying your child makes me want you even more."
                    elif selected_girl.baby_desire > 30:
                        if is_base_mother:
                            selected_girl.character "Being pregnant is... different. As an experienced mother, I know my body is changing, but sometimes I still feel sexy knowing I'm carrying your baby."
                        elif is_student:
                            selected_girl.character "Being pregnant is... weird. Sometimes I feel sexy knowing I'm carrying your baby, but sometimes I just feel fat and awkward."
                        else:
                            selected_girl.character "Being pregnant is... different. Sometimes I feel sexy knowing I'm carrying your child."
                    else:
                        if is_base_mother:
                            selected_girl.character "Pregnancy isn't as sexy as I thought it would be... as an experienced mother, I know the reality is a lot of work and discomfort."
                        elif is_student:
                            selected_girl.character "I don't feel very sexy right now... being pregnant is kind of gross actually. My body feels all weird."
                        else:
                            selected_girl.character "I don't feel very sexy right now... pregnancy is a lot of work."
                            
                elif selected_girl.dominant_approach == "transactional":
                    if selected_girl.baby_desire > 60:
                        if is_base_mother:
                            selected_girl.character "Well, carrying your child does have its advantages... as an experienced mother, I know exactly what this is worth. What are you offering me for expanding our family?"
                            
                            menu:
                                "Offer 2000 cash for pregnancy expenses?":
                                    if player.cash >= 2000:
                                        $ player.cash -= 2000
                                        $ selected_girl.cash += 2000
                                        $ selected_girl.apply_impacts({"baby_desire": (450, 750), "corruption": (750, 1000)})
                                        selected_girl.character "2000 for carrying your child? As an experienced mother, I know that's reasonable for our growing family. Fine, I'll be happy about this pregnancy... for now."
                                    else:
                                        selected_girl.character "You think that's enough for an experienced woman to carry your child? Come back when you're serious about supporting our family."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                
                                "Promise to cover all medical expenses":
                                    $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750)})
                                    selected_girl.character "Medical coverage? As an experienced mother, I appreciate that security for our child. Fine, I'll try to be positive about carrying your baby."
                                    # Convert trust to fear
                                    $ selected_girl.apply_impacts({"fear": (-750, -250)})
                                
                                "Leave it be.":
                                    selected_girl.character "Fine. But don't expect me to be thrilled about carrying your child without proper compensation."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        else:
                            selected_girl.character "Well, carrying your child does have its advantages... what are you offering me? This isn't free, you know."
                            
                            menu:
                                "Offer 2000 cash for pregnancy expenses?":
                                    if player.cash >= 2000:
                                        $ player.cash -= 2000
                                        $ selected_girl.cash += 2000
                                        $ selected_girl.apply_impacts({"baby_desire": (250, 750), "corruption": (750, 1500)})
                                        if is_student:
                                            selected_girl.character "2000 for carrying your baby? Oh my god, that's so much! Okay, yeah, I'll be happy about this pregnancy for that!"
                                        else:
                                            selected_girl.character "2000 for carrying your child? That's reasonable. Fine, I'll be happy about this pregnancy... for now."
                                    else:
                                        if is_student:
                                            selected_girl.character "You think that's enough for a baby? I don't think so... you need to be more serious than that."
                                        else:
                                            selected_girl.character "You think that's enough for carrying my child? Come back when you're serious."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                
                                "Promise to cover all medical expenses":
                                    $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750)})
                                    if is_student:
                                        selected_girl.character "You'll cover all the doctor stuff? Really? Okay! That makes me feel better about having your baby!"
                                    else:
                                        selected_girl.character "Medical coverage? That's a start. Fine, I'll try to be positive about carrying your child."
                                    # Convert trust to fear
                                    $ selected_girl.apply_impacts({"fear": (-750, -250)})
                                
                                "Leave it be.":
                                    if is_student:
                                        selected_girl.character "Fine. But don't expect me to be happy about being pregnant without you helping more."
                                    else:
                                        selected_girl.character "Fine. But don't expect me to be thrilled about carrying your child for free."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    else:
                        if is_base_mother:
                            selected_girl.character "Another baby? As an experienced mother, I know exactly what this costs in time and money. What's in it for me?"
                        elif is_student:
                            selected_girl.character "A baby? Like... for real? But that's... that's 18 years of stuff! What would you even pay for that?"
                        else:
                            selected_girl.character "What's in it for me? Carrying your child is a huge commitment."
                            
                elif selected_girl.dominant_approach == "dominate":
                    if selected_girl.baby_desire > 70:
                        if is_base_mother:
                            selected_girl.character "I am carrying your child. As an experienced mother, I am prepared for this responsibility and will fulfill my duty to expand our family."
                        elif is_student:
                            selected_girl.character "I'm carrying your baby! I'll do my best to be a good mother and take care of your child properly."
                        else:
                            selected_girl.character "I am carrying your child. I am prepared for this responsibility."
                    elif selected_girl.baby_desire > 30:
                        if is_base_mother:
                            selected_girl.character "I am carrying your child. As an experienced mother, I will manage this situation efficiently and effectively."
                        elif is_student:
                            selected_girl.character "I'm carrying your baby... I'll try to handle this the best I can. I'm scared but I'll do what needs to be done."
                        else:
                            selected_girl.character "I am carrying your child. I will manage this situation."
                    else:
                        if is_base_mother:
                            selected_girl.character "I am carrying your child. As an experienced mother, this presents significant logistical challenges that must be addressed."
                        elif is_student:
                            selected_girl.character "I'm carrying your baby... this is really complicated. I don't know how I'm supposed to handle this."
                        else:
                            selected_girl.character "I am carrying your child. This presents significant challenges."
            
            # FETISH APPROACH (RISKY BUT POTENTIALLY HIGH BABY_DESIRE GAIN)
            "I love the idea of you carrying my child inside you...":
                if selected_girl.dominant_approach == "sexualized":
                    $ selected_girl.apply_impacts({"corruption": (950, 1500), "baby_desire": (950, 1500)})
                    if is_base_mother:
                        selected_girl.character "That's... incredibly inappropriate, but as an experienced woman, I find it strangely exciting. I feel myself wanting it more, especially when you cum inside my pregnant pussy..."
                    elif is_student:
                        selected_girl.character "That's... so dirty but so hot! Oh my god, saying that while I'm pregnant with your baby... I can't stop thinking about it! I want you so bad!"
                    else:
                        selected_girl.character "That's... incredibly inappropriate, but strangely exciting. I feel myself wanting it more, especially when you cum inside me..."
                        
                elif selected_girl.dominant_approach == "compassionate":
                    $ selected_girl.apply_impacts({"baby_desire": (750, 1000), "affection": (750, 1500)})
                    if is_base_mother:
                        selected_girl.character "Oh... you saying that while I'm already carrying your child... as an experienced mother, it makes me want to give you more babies."
                    elif is_student:
                        selected_girl.character "Oh... you saying that while I'm pregnant with your baby... that's so romantic! I want to have more of your babies!"
                    else:
                        selected_girl.character "Oh... you saying that... it makes me want to carry your child even more."
                        
                elif selected_girl.dominant_approach == "dominate":
                    $ selected_girl.apply_impacts({"baby_desire": (550, 900), "affection": (550, 900)})
                    if is_base_mother:
                        selected_girl.character "If you wish me to carry more of your children, Professor. As an experienced mother, my body is prepared to serve this purpose."
                    elif is_student:
                        selected_girl.character "If you want me to have more babies... okay, I will. Whatever you want, Professor."
                    else:
                        selected_girl.character "If you wish me to carry more of your children, I will obey your command."
                        
                elif selected_girl.dominant_approach == "transactional":
                    if selected_girl.baby_desire > 50:
                        selected_girl.character "Mmm... you want me that badly? That's powerful leverage. What are you offering me for carrying your child and letting you talk to me like that?"
                        
                        menu:
                            "Offer 1000 cash for the compliment":
                                if player.cash >= 1000:
                                    $ player.cash -= 1000
                                    $ selected_girl.cash += 1000
                                    $ selected_girl.apply_impacts({"corruption": (650, 1500), "baby_desire": (250, 750)})
                                    if is_base_mother:
                                        selected_girl.character "1000 just for dirty talk? As an experienced mother, I know that's good money. Fine, I'll play along... you can talk about breeding me anytime if you keep paying."
                                    elif is_student:
                                        selected_girl.character "1000 for saying that? Oh my god, that's so much! Okay, yeah, you can talk dirty to me about breeding anytime!"
                                    else:
                                        selected_girl.character "1000 just for dirty talk? Fine, I'll play along... you can talk about impregnating me anytime if you keep paying."
                                else:
                                    if is_base_mother:
                                        selected_girl.character "Talk is cheap, Professor. An experienced woman expects better compensation than empty words."
                                    elif is_student:
                                        selected_girl.character "You don't have enough money for that? That's okay... maybe just regular compliments then?"
                                    else:
                                        selected_girl.character "Talk is cheap. Come back when you can afford my attention."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            
                            "Leave it be.":
                                if is_base_mother:
                                    selected_girl.character "That's what I thought. Don't waste an experienced mother's time with empty compliments."
                                elif is_student:
                                    selected_girl.character "Oh... okay. Well, that was still nice of you to say, I guess?"
                                else:
                                    selected_girl.character "That's what I thought. Don't waste my time with empty compliments."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    else:
                        if is_base_mother:
                            selected_girl.character "That's disgusting! As an experienced mother, I expect better from you, especially while I'm carrying your child!"
                        elif is_student:
                            selected_girl.character "That's... really gross! I'm pregnant and you're saying stuff like that? Ew!"
                        else:
                            selected_girl.character "That's disgusting! I expect better from you!"
                        $ selected_girl.apply_impacts({"affection": (-1500, -750), "fear": (750, 1500)})
                else:
                    selected_girl.character "That's disgusting! I expect better from you!"
                    $ selected_girl.apply_impacts({"affection": (-1500, -750), "fear": (750, 1500)})
            
            # PRACTICAL APPROACH (DECREASES BABY_DESIRE)
            "We need to be responsible about this situation.":
                $ selected_girl.apply_impacts({"discipline": (750, 1000), "baby_desire": (-750, -250)})
                
                if selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "You're absolutely right. As an experienced mother, I need to be more responsible for my existing family and this new child."
                    elif is_student:
                        selected_girl.character "You're right. I need to be more responsible about this... even though I'm scared about being a pregnant student."
                    else:
                        selected_girl.character "You're absolutely right. I need to be more responsible about this."
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "Responsible? As an experienced mother, you want ME to be responsible when YOU knocked me up? What are you offering to help with our growing family?"
                        
                        menu:
                            "Offer 3000 for family support":
                                if player.cash >= 3000:
                                    $ player.cash -= 3000
                                    $ selected_girl.cash += 3000
                                    $ selected_girl.apply_impacts({"discipline": (750, 1000), "corruption": (250, 750)})
                                    selected_girl.character "3000 for being 'responsible'? As an experienced mother, I know that's fair. Fine, I'll take it. But don't think this makes you a father."
                                else:
                                    selected_girl.character "Of course you want responsibility without paying for it. An experienced mother isn't that cheap."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            
                            "Leave it be.":
                                selected_girl.character "That's what I thought. Don't lecture an experienced mother about responsibility when you won't back it up."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    else:
                        selected_girl.character "Responsible? You want ME to be responsible when YOU knocked me up? What are you offering?"
                        
                        menu:
                            "Offer 2000 for pregnancy support":
                                if player.cash >= 2000:
                                    $ player.cash -= 2000
                                    $ selected_girl.cash += 2000
                                    $ selected_girl.apply_impacts({"discipline": (750, 1000), "corruption": (250, 750)})
                                    if is_student:
                                        selected_girl.character "2000 for being 'responsible'? Oh my god, that's so much! Fine, I'll take it and be more responsible, I guess."
                                    else:
                                        selected_girl.character "2000 for being 'responsible'? Fine, I'll take it. But don't think this makes you special."
                                else:
                                    if is_student:
                                        selected_girl.character "You don't have enough for that? That's okay... I'll try to be responsible on my own then."
                                    else:
                                        selected_girl.character "Of course you want responsibility without paying for it. Typical."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            
                            "Leave it be.":
                                if is_student:
                                    selected_girl.character "Fine. I'll try to be responsible by myself then, even though it's really hard."
                                else:
                                    selected_girl.character "That's what I thought. Don't lecture me about responsibility when you won't back it up."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                
                elif selected_girl.dominant_approach in ["compassionate", "sexualized"]:
                    if is_base_mother:
                        selected_girl.character "I understand your concern, but as an experienced mother, I've made my decision. This baby is meant to be, and I'll handle my responsibilities to all my children."
                    elif is_student:
                        selected_girl.character "I understand you're worried, but I've made my decision. This baby happened and I'll handle it... even if it's scary."
                    else:
                        selected_girl.character "I understand your concern, but I've made my decision. This baby is meant to be."
                        
                else:
                    selected_girl.character "You're right. I need to be more responsible about this. Maybe we should reconsider."
            
            # NURTURING APPROACH (MOTHER-SPECIFIC)
            "How's the baby doing?" if is_base_mother:
                $ selected_girl.apply_impacts({"affection": (950, 1500), "baby_desire": (750, 1500)})
                
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "Wonderful! As an experienced mother, I can feel the kicks now. It's bringing back such beautiful memories with my daughter. I've been researching fetal development extensively for our growing family."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Amazing! As an experienced woman, pregnancy makes me feel so alive and sexy! I can't wait until you can feel them move too!"
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "The baby is fine, but as an experienced mother, raising another child is expensive. What are you contributing to our family's wellbeing?"
                    
                    menu:
                        "Offer 1000 for baby supplies":
                            if player.cash >= 1000:
                                $ player.cash -= 1000
                                $ selected_girl.cash += 1000
                                $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750)})
                                selected_girl.character "1000 for baby supplies? As an experienced mother, I know that's helpful. The baby is doing great, by the way."
                            else:
                                selected_girl.character "Don't ask about the baby if you're not willing to help support them. An experienced mother knows these costs."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        
                        "Leave it be.":
                            selected_girl.character "Fine. As an experienced mother, the baby is fine. But don't expect updates without contributions."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "The baby is developing as expected. As an experienced mother, I am managing all prenatal care appropriately."
                else:
                    selected_girl.character "It's... progressing normally. As an experienced mother, I'm trying not to get too attached yet with my other child to think about."
            
            # STUDENT-SPECIFIC CONCERNS
            "What about school? How will you manage?" if is_student:
                if selected_girl.dominant_approach == "dominate":
                    $ selected_girl.apply_impacts({"affection": (950, 1500), "baby_desire": (750, 1500)})
                    selected_girl.character "I've been thinking about it... as a student mother, I want this baby more than anything, even if it means taking time off school. I've already researched online degree programs that work with pregnancy."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "School? With your baby? As a student, that's going to be expensive. What are you offering to help me continue my education while raising your child?"
                    
                    menu:
                        "Offer to cover her tuition expenses?":
                            if player.cash >= 2000:
                                $ player.cash -= 2000
                                $ selected_girl.cash += 2000
                                $ selected_girl.apply_impacts({"baby_desire": (250, 750), "discipline": (250, 750)})
                                selected_girl.character "2000 for tuition? As a student, that helps a lot! Fine, I'll continue school while carrying your baby."
                            else:
                                selected_girl.character "Of course you want me to figure it out myself. As a student, I can't afford that without help."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        
                        "Grant her a grade bump of 25 percent?" if is_student:
                            if hasattr(selected_girl, 'grades'):
                                # Check if already at max
                                if selected_girl.grades >= 100:
                                    selected_girl.character "But... my grades are already at maximum! A bump won't help much... can you offer something else?"
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                else:
                                    # Apply 25 point increase (not 25% of current grade)
                                    $ new_grade = min(100, selected_girl.grades + 25)
                                    $ selected_girl.grades = new_grade
                                    $ selected_girl.apply_impacts({"baby_desire": (250, 750), "corruption": (750, 1500)})
                                    selected_girl.character "Grade bump for having your baby? As a student, that's perfect security! Fine, you can put a baby in me... but I want this in writing!"
                            else:
                                # Missing grade attributes
                                selected_girl.character "I... don't think you can change my grades? Can you? As a student, maybe just cash would help more?"
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        
                        "Leave it be.":
                            selected_girl.character "Fine. As a student, I'll figure it out myself, but don't expect me to be grateful about it."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    
                elif selected_girl.dominant_approach in ["compassionate", "sexualized"]:
                    $ selected_girl.apply_impacts({"affection": (950, 1500), "baby_desire": (750, 1500)})
                    selected_girl.character "I've been thinking about it... as a student, I want this baby more than anything, even if it means taking time off school. Your support means everything."
                else:
                    $ selected_girl.apply_impacts({"affection": (750, 1500)})
                    selected_girl.character "I'm terrified about what this means for my future as a student... but I don't know what to do."

    # PHASE 5: PRENATAL VITAMINS (CONTEXTUAL OPTION) - WITH FUTURE CONSEQUENCES
    if selected_girl.pregnant and selected_girl.player_knows_pregnant and selected_girl.knows_pregnant and player.has_item("prenatal_vitamins"):
        menu:
            "I brought these prenatal vitamins if you need them.": 
                $ player.remove_item("prenatal_vitamins")
                
                # Check different dominant_approach types
                if selected_girl.dominant_approach == "compassionate":
                    # Genuinely grateful
                    $ selected_girl.apply_impacts({"affection": (750, 1500), "prenatal_boost": 1})
                    if is_base_mother:
                        selected_girl.character "Oh! Thank you so much, Professor! As an experienced mother, this means the world to me - you're already thinking about our baby and my other child. I feel so connected to you."
                    elif is_student:
                        selected_girl.character "Oh! Thank you so much, Professor! This means the world to me - you're already taking care of our baby! I feel so connected to you."
                    else:
                        selected_girl.character "Oh! Thank you so much, Professor! This means the world to me - you're already taking care of our baby. I feel so connected to you."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    # Turns it into something sexual
                    $ selected_girl.apply_impacts({"prenatal_boost": 1, "corruption": (250, 750), "affection": (250, 750)})
                    if is_base_mother:
                        selected_girl.character "Mmm... taking care of your baby while pregnant with your child... As an experienced woman, that's so hot. I'll take these vitamins if it means you'll keep taking care of me in other ways too."
                    elif is_student:
                        selected_girl.character "Mmm... taking care of your baby while pregnant... that's so hot! I'll take these vitamins if it means you'll keep taking care of me in other ways too!"
                    else:
                        selected_girl.character "Mmm... taking care of your baby while pregnant... That's so hot. I'll take these vitamins if it means you'll keep taking care of me in other ways too."
                        
                elif selected_girl.dominant_approach == "dominate":
                    # Accepts without question
                    $ selected_girl.apply_impacts({"prenatal_boost": 1, "affection": (750, 1500), "fear": (-750, -250)})
                    if is_base_mother:
                        selected_girl.character "If that's what you want, Master. As an experienced mother, I'll take these vitamins for our baby and stay healthy for my other child too."
                    elif is_student:
                        selected_girl.character "If that's what you want, Professor. I'll take these vitamins for our baby."
                    else:
                        selected_girl.character "If that's what you want, Master. I'll take these vitamins for our baby."
                        
                elif selected_girl.dominant_approach == "transactional":
                    # Sees this as leverage
                    if is_base_mother:
                        selected_girl.character "Prenatal vitamins? That's thoughtful, Professor. As an experienced mother, I know prenatal care and vitamins for children is expensive... What's in it for me?"
                    elif is_student:
                        selected_girl.character "Prenatal vitamins? That's nice of you! But as a student, I know vitamins cost money... what are you offering for this?"
                    else:
                        selected_girl.character "Prenatal vitamins? That's thoughtful, Professor. Of course, prenatal care and vitamins is expensive... What's in it for me?"
                    
                    menu:
                        "Grant her 500 cash for prenatal expenses?":
                            if player.cash >= 500:
                                $ player.cash -= 500
                                $ selected_girl.cash += 500
                                $ selected_girl.apply_impacts({"prenatal_boost": 1, "corruption": (250, 750), "affection": (250, 750)})
                                if is_base_mother:
                                    selected_girl.character "500 for prenatal expenses? As an experienced mother, I know that's reasonable since I'm carrying your child and already have another to care for. Fine, I'll take the vitamins... but don't think this covers everything."
                                elif is_student:
                                    selected_girl.character "500 for prenatal expenses? Oh my god, that's so much! Okay, yeah, I'll take the vitamins! Thank you!"
                                else:
                                    selected_girl.character "500 for prenatal expenses? That's reasonable since I'm carrying your child. Fine, I'll take the vitamins... but don't think this covers everything."
                            else:
                                if is_base_mother:
                                    selected_girl.character "Don't offer what you can't deliver, Professor. An experienced mother knows prenatal care costs money I don't have."
                                elif is_student:
                                    selected_girl.character "Oh... you don't have enough for that? That's okay... I'll try to get vitamins some other way, I guess."
                                else:
                                    selected_girl.character "Don't offer what you can't deliver, Professor. Prenatal care costs money I don't have."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        
                        # Only students get grade option
                        "Grant her a grade bump of 25 percent?" if is_student:
                            if hasattr(selected_girl, 'grades'):
                                # Check if already at max
                                if selected_girl.grades >= 100:
                                    selected_girl.character "But... my grades are already at maximum! A bump won't help much... can you offer something else?"
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                else:
                                    # Apply 25 point increase (not 25% of current grade)
                                    $ new_grade = min(100, selected_girl.grades + 25)
                                    $ selected_girl.grades = new_grade
                                    $ selected_girl.apply_impacts({"baby_desire": (750, 1000), "corruption": (950, 1500)})
                                    selected_girl.character "Grade bump for having your baby? As a student, that's perfect security! Fine, you can put a baby in me... but I want this in writing!"
                            else:
                                # Missing grade attributes
                                selected_girl.character "I... don't think you can change my grades? Can you? As a student, maybe just cash would help more?"
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        
                        "Promise to give her an A+ for taking care of your baby" if is_student:
                            if hasattr(selected_girl, "grades"):
                                $ selected_girl.grades = min(100, selected_girl.grades + 100)
                                $ selected_girl.apply_impacts({"prenatal_boost": 1, "corruption": (950, 1500), "discipline": (-750, -250)})
                                selected_girl.character "A+ for taking care of your baby? As a student, that's amazing! Now that's a negotiation. Fine, I'll take the vitamins... but this better not be the only support I get."
                            else:
                                selected_girl.character "I'm not even in your class. As a student, try again with something that actually benefits me."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        
                        "Promise to cover all medical expenses":
                            $ selected_girl.apply_impacts({"prenatal_boost": 1, "affection": (250, 750), "corruption": (250, 750)})
                            if is_base_mother:
                                selected_girl.character "Medical coverage? As an experienced mother, I appreciate that security for our child. Fine, I'll take the vitamins... but I expect more support later."
                            elif is_student:
                                selected_girl.character "You'll cover all the doctor stuff? Really? As a student, that's perfect! Okay, I'll take the vitamins! Thank you so much!"
                            else:
                                selected_girl.character "Medical coverage? That's security. Fine, I'll take the vitamins... but I expect more support later."
                            # Convert trust to fear
                            $ selected_girl.apply_impacts({"fear": (-750, -250)})
                        
                        "Just take the damn vitamins.":
                            if is_base_mother:
                                selected_girl.character "Fine. As an experienced mother, don't expect me to be grateful when I'm doing all the work growing your baby while caring for another child."
                            elif is_student:
                                selected_girl.character "Fine... I'll take them. As a student, I guess I should take care of myself for the baby."
                            else:
                                selected_girl.character "Fine. But don't expect me to be grateful when I'm doing all the work growing your baby."
                            $ selected_girl.apply_impacts({"prenatal_boost": 1, "affection": (-750, -250)})
                
                else:
                    # Hesitant acceptance
                    $ selected_girl.apply_impacts({"prenatal_boost": 1, "fear": (-750, -250)})
                    if is_base_mother:
                        selected_girl.character "I... I suppose I should take them. As an experienced mother, it's for the baby's health... and I need to stay strong for my other child too."
                    elif is_student:
                        selected_girl.character "I... I suppose I should take them. As a student, it's for the baby's health... I'm a little scared of taking pills though."
                    else:
                        selected_girl.character "I... I suppose I should take them. It's for the baby's health..."
                    "[selected_girl] hesitates before taking them, hands trembling slightly."


    
   

    # FINAL REACTION (BASED ON OUTCOMES) - WITH MEMORY FOR FUTURE CONVERSATIONS
    if selected_girl.pregnant and selected_girl.player_knows_pregnant and selected_girl.knows_pregnant:
        # Check what her current condom preference is
        if selected_girl.wants_vaginal_condom:
            # She wants condoms - check if player is happy about this
            if selected_girl.dominant_approach in ["compassionate", "dominate"]:
                $ selected_girl.previous_pregnancy_reaction = "positive"
                if is_base_mother:
                    selected_girl.character "Thank you for understanding, Professor. As an experienced mother, knowing you'll protect my pussy while I'm carrying our baby means everything - especially with my other child to consider."
                elif is_student:
                    selected_girl.character "Thank you for understanding, Professor. Knowing you'll protect my pussy while I'm carrying our baby means everything to me."
                else:
                    selected_girl.character "Thank you for understanding, Professor. Knowing you'll protect my pussy while I'm carrying our baby means everything."
                    
            elif selected_girl.dominant_approach == "transactional":
                $ selected_girl.previous_pregnancy_reaction = "neutral"
                if is_base_mother:
                    selected_girl.character "Fine, you'll use condoms while I'm pregnant. As an experienced mother, I expect extra compensation for carrying your child AND protecting my existing family's wellbeing."
                    menu:
                        "Grant her 1000 cash for pregnancy care?":
                            if player.cash >= 1000:
                                $ player.cash -= 1000
                                $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                                selected_girl.character "1000 for prenatal care? As an experienced mother, I know that's reasonable. I'll make sure to take good care of your baby... and your wallet."
                            else:
                                selected_girl.character "Don't insult an experienced mother. Prenatal care costs more than that."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        "Promise to cover all medical expenses":
                            $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                            selected_girl.character "Medical coverage? Now you're talking like a responsible father. As an experienced mother, I'll make sure our baby gets the best care."
                        "Leave it be.":
                            selected_girl.character "Fine. As an experienced mother, don't expect me to be happy about carrying your child for free."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                else:
                    selected_girl.character "Fine, you'll use condoms while I'm pregnant. But as a student, I expect compensation for carrying your child - this is a temporary arrangement, after all."
                    menu:
                        "Grant her 800 cash for pregnancy expenses?":
                            if player.cash >= 800:
                                $ player.cash -= 800
                                $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                                selected_girl.character "800 for pregnancy expenses? As a student, that helps a lot! I'll take good care of your investment."
                            else:
                                selected_girl.character "That's not even close to enough for carrying your child as a student."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        "Leave it be.":
                            selected_girl.character "Suit yourself. As a student, remember - nothing in life is free, especially not babies."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
            else:
                $ selected_girl.previous_pregnancy_reaction = "neutral"
                if is_base_mother:
                    selected_girl.character "Thanks for checking in about protection while I'm pregnant, Professor. As an experienced mother, I appreciate you being responsible about our baby and my existing child."
                elif is_student:
                    selected_girl.character "Thanks for checking in about protection while I'm pregnant, Professor. I appreciate you being responsible about our baby."
                else:
                    selected_girl.character "Thanks for checking in about protection while I'm pregnant, Professor. I appreciate you being responsible about our baby."
        
        else:
            # She doesn't want condoms - check her reaction
            if selected_girl.baby_desire > 70:
                $ selected_girl.previous_pregnancy_reaction = "positive"
                if is_base_mother:
                    selected_girl.character "Thank you for understanding, Professor. As an experienced mother, I love that you want to feel me completely while I'm carrying our baby - and my body already knows how to handle children."
                elif is_student:
                    selected_girl.character "Thank you for understanding, Professor. I love that you want to feel me completely while I'm carrying our baby!"
                else:
                    selected_girl.character "Thank you for understanding, Professor. I love that you want to feel me completely while I'm carrying our baby."
            elif selected_girl.dominant_approach == "transactional":
                $ selected_girl.previous_pregnancy_reaction = "neutral"
                if is_base_mother:
                    selected_girl.character "No condoms while I'm pregnant? Smart move - you get what you want and as an experienced mother, I get leverage. But carrying your child while raising my existing one? That deserves compensation."
                    menu:
                        "Grant her 1500 cash for family support?":
                            if player.cash >= 1500:
                                $ player.cash -= 1500
                                $ selected_girl.apply_impacts({"affection": (250, 750), "corruption": (750, 1000)})
                                selected_girl.character "1500 for supporting our growing family? As an experienced mother, I know that's good investment. You can fuck my bare pregnant pussy anytime."
                            else:
                                selected_girl.character "You think that's enough for two kids as an experienced mother? Try again when you're serious about being a father."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        "Promise to help with childcare expenses":
                            $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                            selected_girl.character "Childcare support? Now you're thinking like a provider. As an experienced mother, fine, you can have bare access to your pregnant pussy."
                        "Leave it be.":
                            selected_girl.character "Fine. As an experienced mother, remember - I'm doing all the work growing your family here."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
                else:
                    selected_girl.character "No condoms while I'm pregnant? Good. As a student, carrying your child deserves proper compensation - I'm essentially giving you a legacy here."
                    menu:
                        "Grant her 1200 cash for carrying your child?":
                            if player.cash >= 1200:
                                $ player.cash -= 1200
                                $ selected_girl.apply_impacts({"affection": (250, 750), "corruption": (750, 1000)})
                                selected_girl.character "1200 for carrying your heir? As a student, that's fair price. Enjoy your bare pregnant pussy while it lasts."
                            else:
                                selected_girl.character "You're seriously lowballing the price of your own child as a student? Pathetic."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        "Leave it be.":
                            selected_girl.character "Suit yourself. As a student, don't expect special treatment for free."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})
            else:
                $ selected_girl.previous_pregnancy_reaction = "neutral"
                if is_base_mother:
                    selected_girl.character "I'm glad we're on the same page about this, Professor. As an experienced mother, my body knows what it's doing, and I want to share this experience with you completely."
                elif is_student:
                    selected_girl.character "I'm glad we're on the same page about this, Professor. I want to share this experience with you completely."
                else:
                    selected_girl.character "I'm glad we're on the same page about this, Professor. I want to share this experience with you completely."
        
        # Set reaction based on baby_desire and dominant_approach
        if selected_girl.baby_desire > 70 and selected_girl.dominant_approach in ["compassionate", "sexualized"]:
            $ selected_girl.previous_pregnancy_reaction = "positive"
        elif selected_girl.baby_desire < 30 and selected_girl.dominant_approach == "transactional":
            $ selected_girl.previous_pregnancy_reaction = "negative"
        else:
            $ selected_girl.previous_pregnancy_reaction = "neutral"
    
    # APPLY FINAL IMPACTS (SCALE BASED ON DIALOGUE CHOICES)
    if selected_girl.pregnant and selected_girl.player_knows_pregnant and selected_girl.knows_pregnant:
        $ impact_amount = 50 + (selected_girl.baby_desire // 2)
        
        if is_base_mother:
            $ selected_girl.apply_impacts({
                "affection": impact_amount,
                "naturism": impact_amount * 0.7,
                "fear": -(impact_amount * 0.5)  # Convert trust to fear
            })
        elif is_student:
            $ selected_girl.apply_impacts({
                "affection": impact_amount * 0.8,
                "corruption": impact_amount * 0.5,
                "fear": -(impact_amount * 0.6)  # Convert trust to fear
            })
    
    # SET UP FOR FUTURE CONVERSATIONS
    if selected_girl.pregnant and selected_girl.player_knows_pregnant and selected_girl.knows_pregnant:
        # Schedule follow-up conversation based on pregnancy phase
        if selected_girl.pregnancy_phase == 1:
            $ selected_girl.pregnancy_followup = time_manager.total_days + 7
        elif selected_girl.pregnancy_phase == 2:
            $ selected_girl.pregnancy_followup = time_manager.total_days + 14
        else:
            $ selected_girl.pregnancy_followup = time_manager.total_days + 7
        
        # Create unique dialogue paths for next conversation
        $ current_level = getattr(selected_girl, "pregnancy_discussion_level", 0)
        $ selected_girl.pregnancy_discussion_level = 1 if current_level == 0 else min(3, current_level + 1)
        
    # Track that this conversation happened
    $ actions_already_done.setdefault(selected_girl.id, []).append("small_talk_pregnancy")
    $ time_manager.skip_time(minutes=5)
    
    return

label vt_small_talk_pregnancy_followup:
    
    # Clear identification of relationship types (matching small_talk_pregnancy)
    $ is_base_mother = False
    $ is_student = False
    $ is_other = False

    if hasattr(selected_girl, "daughter") and selected_girl.daughter:
        $ is_base_mother = True
    elif hasattr(selected_girl, "mother") and selected_girl.mother:
        $ is_student = True
    else:
        $ is_other = True
    
    # PROPER KIDS TRACKING (matching small_talk_pregnancy)
    $ total_kids = selected_girl.kids
    $ kids_with_player = selected_girl.kids_with_player
    $ kids_with_others = selected_girl.kids_with_npc
    $ is_currently_a_mother = total_kids > 0
    if is_base_mother:
        $ is_currently_a_mother = total_kids > 1  # includes original daughter
    
    # PREGNANCY PHASE (matching small_talk_pregnancy)
    $ pregnancy_phase = 0
    if selected_girl.pregnant:
        $ pregnancy_phase = selected_girl.pregnancy_phase
    
    # KNOWLEDGE MATRIX (matching small_talk_pregnancy)
    $ player_knows = hasattr(selected_girl, "player_knows_pregnant") and selected_girl.player_knows_pregnant
    $ she_knows = selected_girl.knows_pregnant

    # NORMALIZE AND CLUSTER PERSONALITY TRAITS (matching small_talk_pregnancy)
    $ norm_naturism = selected_girl.naturism / 10
    $ norm_corruption = selected_girl.corruption / 10
    $ norm_discipline = selected_girl.discipline / 10
    $ norm_fear = selected_girl.fear / 10

    $ natural_leaning = norm_naturism - norm_discipline
    $ risk_taking = norm_corruption - norm_fear

    
    # NORMALIZE PLAYER STATS TO 0-10 SCALE FOR CLUSTERING (matching small_talk_pregnancy)
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

    # Track previous baby_desire for impact calculation
    $ previous_baby_desire = selected_girl.baby_desire
    $ discussion_level = selected_girl.pregnancy_discussion_level
    
    # DYNAMIC CHILD REFERENCE (matching small_talk_pregnancy)
    $ child_reference = ""
    if is_base_mother and (total_kids - kids_with_player - kids_with_others) > 0:
        $ child_reference = "my daughter"
    elif kids_with_player > 0:
        $ child_reference = "your child" if kids_with_player == 1 else f"our {total_kids} children"
    elif kids_with_others > 0:
        $ child_reference = "that child" if kids_with_others == 1 else f"my {total_kids} children"
    else:
        $ child_reference = "my child" if is_currently_a_mother else ""

    # FOLLOW-UP DIALOGUE BASED ON DISCUSSION LEVEL AND PREGNANCY STATUS
    if discussion_level >= 2:
        if selected_girl.baby_desire > 70:
            "[selected_girl] smiles warmly, her hand instinctively moving to her stomach if she's pregnant."
            
            if pregnancy_phase > 0:
                if pregnancy_phase == 1:
                    selected_girl.character "I've been thinking about our last conversation... I took a test this morning and it was positive."
                elif pregnancy_phase == 2:
                    selected_girl.character "I've been thinking about our last conversation... I can feel the baby moving now. It's really happening."
                else:
                    selected_girl.character "I've been thinking about our last conversation... it won't be long now. I've been preparing everything for the baby."
                
                $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 8)
                
            elif is_currently_a_mother:
                if is_base_mother and child_reference:
                    selected_girl.character "I've been thinking about what we talked about... I want to experience pregnancy with [child_reference]."
                else:
                    selected_girl.character "I've been thinking about what we talked about... I want to experience pregnancy with you."
                
                $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 7)
                
            else:
                selected_girl.character "I've been researching fertility cycles since we last spoke. I want this with you."
                $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 6)
                
        elif selected_girl.baby_desire > 30:
            "[selected_girl] looks thoughtful but hesitant, clearly wrestling with her feelings."
            
            if pregnancy_phase > 0:
                if she_knows and not player_knows:
                    selected_girl.character "I need to tell you something... I'm pregnant. I wasn't sure how to bring it up."
                    $ selected_girl.player_knows_pregnant = True
                    $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 5)
                elif she_knows and player_knows:
                    selected_girl.character "I've been learning to accept this pregnancy since we last spoke."
                    $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 4)
                else:
                    selected_girl.character "I've been feeling different... I think I might be pregnant."
                    $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 3)
            else:
                if risk_taking > 2:
                    selected_girl.character "I'm not actively trying, but I'm not preventing it either since we talked."
                    $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 4)
                else:
                    selected_girl.character "I'm being more careful, but I've been thinking about what you said."
                    $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 2)
                
        else:  # baby_desire <= 30
            "[selected_girl] looks down, avoiding eye contact as she speaks."
            
            if pregnancy_phase > 0:
                if she_knows:
                    selected_girl.character "I need to tell you something... I'm pregnant. I don't know how I feel about it."
                    $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 3)
                else:
                    selected_girl.character "I've been taking extra precautions since we talked."
                    $ selected_girl.baby_desire = max(0, selected_girl.baby_desire - 3)
            else:
                if norm_fear > 7:
                    selected_girl.character "I've been thinking about what you said... but it still makes me uncomfortable."
                    $ selected_girl.baby_desire = max(0, selected_girl.baby_desire - 2)
                else:
                    selected_girl.character "I've been thinking about what you said... I need more time."
                    $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 1)

    elif discussion_level == 1:
        if selected_girl.baby_desire > 70:
            "[selected_girl] smiles softly, her eyes distant as she remembers your previous conversation."
            selected_girl.character "I wasn't sure at first, but after our talk I've been dreaming about having your child."
            $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 5)
            
        elif selected_girl.baby_desire > 30:
            "[selected_girl] seems thoughtful but hesitant, clearly weighing her options."
            selected_girl.character "I've been thinking about what you said... but I need more time to process everything."
            $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 3)
            
        else:  # baby_desire <= 30
            "[selected_girl] crosses her arms defensively, putting up emotional barriers."
            selected_girl.character "I know you're interested in this topic, but I'm not comfortable discussing it further."
            $ selected_girl.baby_desire = max(0, selected_girl.baby_desire - 1)

    else:  
        # discussion_level == 0 (shouldn't happen in follow-up)
        "[selected_girl] looks genuinely perplexed, unsure how to respond."
        selected_girl.character "I'm confused... why are you bringing this up again so soon?"
        $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 1)

    # Additional dialogue based on motherhood status (matching small_talk_pregnancy)
    if is_currently_a_mother and selected_girl.baby_desire > 50:
        if is_base_mother and child_reference:
            selected_girl.character "I think about [child_reference] when I consider having another child with you."
            $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 4)
        else:
            selected_girl.character "Being a mother has changed how I view what we discussed."
            $ selected_girl.baby_desire = min(100, selected_girl.baby_desire + 3)

    # Update tracking variables (matching small_talk_pregnancy pattern)
    $ selected_girl.pregnancy_discussion_level = min(3, discussion_level + 1)
    
    # Set reaction based on baby_desire (matching small_talk_pregnancy)
    if selected_girl.baby_desire > 70:
        $ selected_girl.previous_pregnancy_reaction = "positive"
    elif selected_girl.baby_desire > 30:
        $ selected_girl.previous_pregnancy_reaction = "neutral"
    else:
        $ selected_girl.previous_pregnancy_reaction = "negative"

    # PLAYER RESPONSE OPTIONS WITH STAT REFERENCES (matching small_talk_pregnancy structure)
    menu:
        "This aligns with my compassionate approach to relationships." if empathy > 6:
            player.character "I'm glad you've been reflecting on our previous conversation. Your well-being is important to me."
            
            if selected_girl.baby_desire > 70:
                selected_girl.character "I appreciate how understanding you are, Professor. It makes me feel safe discussing these things."
                $ selected_girl.apply_impacts({"affection": (550, 750), "fear": (-750, -250)})
            else:
                selected_girl.character "Thank you for being so understanding, Professor."
                $ selected_girl.apply_impacts({"affection": (350, 750), "fear": (-750, -250)})
            
        "This demonstrates proper discipline in our relationship." if control > 6:
            player.character "Good. I expect you to take this seriously and be responsible."
            
            if selected_girl.baby_desire > 70:
                selected_girl.character "I will, Professor. I want to do this the right way with you."
                $ selected_girl.apply_impacts({"discipline": (250, 750), "affection": (250, 750)})
            else:
                selected_girl.character "I'll try to meet your expectations, Professor..."
                $ selected_girl.apply_impacts({"fear": (250, 750), "affection": (-750, -250)})
                
        "This fits with my more adventurous perspective." if lust > 6:
            player.character "I'm glad you're embracing the more... passionate aspects of our relationship."
            
            if pregnancy_phase > 0:
                selected_girl.character "It certainly makes things more intense now, doesn't it?"
                $ selected_girl.apply_impacts({"corruption": (450, 750), "affection": (350, 750)})
            else:
                selected_girl.character "I've been thinking about how much I enjoy our intimate moments."
                $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                
        # VAGINAL CONDOM PREFERENCES - FOLLOWUP EDITION
        "What are your thoughts on condoms for vaginal sex now?":
            # Response based on initial_reaction
            if selected_girl.initial_reaction == "loving":
                if selected_girl.wants_vaginal_condom:
                    if is_currently_a_mother:
                        selected_girl.character "I feel so connected to you, but I have a child to think about. When you're inside my pussy, I need that protection - I can't risk another pregnancy right now."
                    else:
                        selected_girl.character "I feel so connected to you, but when you're inside my pussy, I need that rubber layer. It lets me relax and enjoy us without worry."
                else:
                    if is_currently_a_mother:
                        selected_girl.character "I feel so connected to you. I want to feel your bare cock sliding into my pussy - I'm already a mother, so another baby wouldn't be the end of the world."
                    else:
                        selected_girl.character "I feel so connected to you. I want to feel your bare cock sliding into my pussy, nothing between us when we make love."
                        
            elif selected_girl.initial_reaction == "submissive":
                if selected_girl.wants_vaginal_condom:
                    if is_currently_a_mother:
                        selected_girl.character "You're in charge, Master. If you want to wrap your cock before entering my pussy, I'll accept it - I must protect my existing child."
                    else:
                        selected_girl.character "You're in charge, Master. If you want to wrap your cock before entering my pussy, I'll accept it."
                else:
                    if is_currently_a_mother:
                        selected_girl.character "You're in charge, Master. If you want to fuck my bare pussy with no condom, I won't stop you - my body already knows how to handle children."
                    else:
                        selected_girl.character "You're in charge, Master. If you want to fuck my bare pussy with no condom, I won't stop you."
                        
            elif selected_girl.initial_reaction == "seductive":
                if selected_girl.wants_vaginal_condom:
                    if is_currently_a_mother:
                        selected_girl.character "The way you look at me is so hot... but as a mother, I need to be careful. Watching you roll a condom over your hard cock before fucking me shows you respect my situation."
                    else:
                        selected_girl.character "The way you look at me is so hot... but watching you roll a condom over your hard cock before fucking me can be its own kind of sexy."
                else:
                    if is_currently_a_mother:
                        selected_girl.character "The way you look at me is so hot. I want to feel your raw cock stretching my pussy open, no barriers - motherhood hasn't dulled my desires."
                    else:
                        selected_girl.character "The way you look at me is so hot. I want to feel your raw cock stretching my pussy open, no barriers."
                        
            elif selected_girl.initial_reaction == "manipulative":
                if selected_girl.wants_vaginal_condom:
                    if is_currently_a_mother:
                        selected_girl.character "What's in it for me? I'm a mother with responsibilities, Professor. Letting you fuck my pussy with a condom costs extra - I have childcare to pay for."
                    else:
                        selected_girl.character "What's in it for me? Letting you fuck my pussy with a condom costs extra... unless you make it worth my time."
                else:
                    if is_currently_a_mother:
                        selected_girl.character "What's in it for me? Bareback pussy access from a single mother? That's premium pricing, Professor - I'm supporting a household here."
                    else:
                        selected_girl.character "What's in it for me? Bareback pussy access? That's premium pricing, Professor."
                        
            elif selected_girl.initial_reaction == "devoted":
                if selected_girl.wants_vaginal_condom:
                    if is_currently_a_mother:
                        selected_girl.character "I'll do anything for you, including letting you put a condom on before you enter my pussy if it pleases you - my child's wellbeing comes first though."
                    else:
                        selected_girl.character "I'll do anything for you, including letting you put a condom on before you enter my pussy if it pleases you."
                else:
                    if is_currently_a_mother:
                        selected_girl.character "I'll do anything for you, including letting you fuck my unprotected pussy if it pleases you - my body is yours even with my maternal duties."
                    else:
                        selected_girl.character "I'll do anything for you, including letting you fuck my unprotected pussy if it pleases you."
                        
            elif selected_girl.initial_reaction == "admiring":
                if selected_girl.wants_vaginal_condom:
                    if is_currently_a_mother:
                        selected_girl.character "You're so strong. I trust your judgment about wrapping your cock before you take my pussy - a mother needs to be practical about these things."
                    else:
                        selected_girl.character "You're so strong. I trust your judgment about wrapping your cock before you take my pussy."
                else:
                    if is_currently_a_mother:
                        selected_girl.character "You're so strong. I trust your decision to claim my bare pussy without protection - even with my child at home."
                    else:
                        selected_girl.character "You're so strong. I trust your decision to claim my bare pussy without protection."
                        
            elif selected_girl.initial_reaction == "infatuated":
                if selected_girl.wants_vaginal_condom:
                    if is_currently_a_mother:
                        selected_girl.character "I can't stop thinking about you... but I need you to wear a condom when you fuck my pussy - I can't get pregnant again while raising my child."
                    else:
                        selected_girl.character "I can't stop thinking about you... but I need you to wear a condom when you fuck my pussy."
                else:
                    if is_currently_a_mother:
                        selected_girl.character "I can't stop thinking about you. I dream about feeling your bare cock pumping into my pussy - maybe giving my child a sibling someday."
                    else:
                        selected_girl.character "I can't stop thinking about you. I dream about feeling your bare cock pumping into my pussy."
                        
            elif selected_girl.initial_reaction == "generous":
                if selected_girl.wants_vaginal_condom:
                    if is_currently_a_mother:
                        selected_girl.character "I want to give you everything, but I need you to use a condom when you take my pussy - I must be responsible for my child's sake."
                    else:
                        selected_girl.character "I want to give you everything, but I need you to use a condom when you take my pussy."
                else:
                    if is_currently_a_mother:
                        selected_girl.character "I want to give you everything. My bare pussy is yours whenever you want it - motherhood hasn't made me selfish."
                    else:
                        selected_girl.character "I want to give you everything. My bare pussy is yours whenever you want it."
                        
            elif selected_girl.initial_reaction == "neutral":
                if selected_girl.wants_vaginal_condom:
                    if is_currently_a_mother:
                        selected_girl.character "As a mother, I need to be careful. Use a condom when you fuck my pussy - I can't risk another mouth to feed right now."
                    else:
                        selected_girl.character "Just another student with preferences. Use a condom when you fuck my pussy."
                else:
                    if is_currently_a_mother:
                        selected_girl.character "I'm already a mother, so what's one more risk? You can fuck my bare pussy no problem."
                    else:
                        selected_girl.character "Just another student with preferences. You can fuck my bare pussy no problem."
            
            $ selected_girl.player_knows_vaginal_condom = True
            
            menu:
                "I respect your boundaries. We'll always use condoms when fucking your pussy.":
                    $ selected_girl.wants_vaginal_condom = True
                    $ selected_girl.apply_impacts({"affection": (550, 1000), "fear": (-1000,-500)})
                    
                    # Response based on her initial_reaction
                    if selected_girl.initial_reaction == "loving":
                        if is_currently_a_mother:
                            selected_girl.character "Thank you for understanding. Knowing you'll protect my pussy and respect my responsibilities as a mother makes me feel even more connected to you."
                        else:
                            selected_girl.character "Thank you for understanding. Knowing you'll protect my pussy makes me feel even more connected to you."
                    elif selected_girl.initial_reaction == "submissive":
                        if is_currently_a_mother:
                            selected_girl.character "Thank you, Master. Your consideration for my pussy and my role as a mother means everything to me."
                        else:
                            selected_girl.character "Thank you, Master. Your consideration for my pussy means everything to me."
                    elif selected_girl.initial_reaction == "seductive":
                        if is_currently_a_mother:
                            selected_girl.character "Mmm... a gentleman who respects a mother's boundaries. That's unexpectedly hot. I like that."
                        else:
                            selected_girl.character "Mmm... a gentleman who respects pussy boundaries. That's unexpectedly hot. I like that."
                    elif selected_girl.initial_reaction == "manipulative":
                        if is_currently_a_mother:
                            selected_girl.character "Fine. I'll remember this favor next time you want something - single mothers don't forget kindness."
                        else:
                            selected_girl.character "Fine. I'll remember this favor next time you want something from me."
                    elif selected_girl.initial_reaction == "devoted":
                        if is_currently_a_mother:
                            selected_girl.character "Thank you. I'll always let you protect my pussy this way. Your will is my command - and you're showing you care about my child too."
                        else:
                            selected_girl.character "Thank you. I'll always let you protect my pussy this way. Your will is my command."
                    elif selected_girl.initial_reaction == "admiring":
                        if is_currently_a_mother:
                            selected_girl.character "You're so considerate about my pussy and my family situation. I admire you even more for respecting me as a mother."
                        else:
                            selected_girl.character "You're so considerate about my pussy. I admire you even more for respecting me."
                    elif selected_girl.initial_reaction == "infatuated":
                        if is_currently_a_mother:
                            selected_girl.character "You're perfect! Even when you're talking about fucking my pussy, you're still so respectful of my motherhood. I can't stop thinking about you."
                        else:
                            selected_girl.character "You're perfect! Even when you're talking about fucking my pussy, you're still so respectful. I can't stop thinking about you."
                    elif selected_girl.initial_reaction == "generous":
                        if is_currently_a_mother:
                            selected_girl.character "Thank you. I want to give you my pussy, but safely. Your respect for my role as a mother means everything."
                        else:
                            selected_girl.character "Thank you. I want to give you my pussy, but safely. Your respect means everything."
                    elif selected_girl.initial_reaction == "neutral":
                        if is_currently_a_mother:
                            selected_girl.character "Thank you for understanding. A mother needs to be practical, and I appreciate that you get it."
                        else:
                            selected_girl.character "Thank you for understanding. That means a lot to me."
                    else:
                        selected_girl.character "Thank you for respecting my boundaries about condoms."
                
                "But what if we wanted to make a baby? No condom when I cum in your pussy?":
                    if selected_girl.baby_desire > 50 and selected_girl.initial_reaction in ["loving", "devoted", "generous", "infatuated"]:
                        # Emotionally invested reactions want your baby
                        $ selected_girl.wants_vaginal_condom = False
                        $ selected_girl.apply_impacts({"baby_desire": (750, 1000), "affection": (750, 1000)})
                        
                        if selected_girl.initial_reaction == "loving":
                            if is_currently_a_mother:
                                selected_girl.character "A baby with you... and another child for our family? I'd love nothing more! Please cum in my bare pussy."
                            else:
                                selected_girl.character "A baby with you... I'd love nothing more! Please cum in my bare pussy and put a baby in me."
                        elif selected_girl.initial_reaction == "devoted":
                            if is_currently_a_mother:
                                selected_girl.character "Anything for you. I want to carry your baby and expand our family. Fill my pussy with your cum, please."
                            else:
                                selected_girl.character "Anything for you. I want to carry your baby. Fill my pussy with your cum, please."
                        elif selected_girl.initial_reaction == "generous":
                            if is_currently_a_mother:
                                selected_girl.character "I want to give you everything, including another baby to grow our family. Take my bare pussy and breed me."
                            else:
                                selected_girl.character "I want to give you everything, including a baby. Take my bare pussy and breed me."
                        elif selected_girl.initial_reaction == "infatuated":
                            if is_currently_a_mother:
                                selected_girl.character "A baby! I can't stop thinking about having your baby and growing our family! Please cum inside me!"
                            else:
                                selected_girl.character "A baby! I can't stop thinking about having your baby! Please cum inside me and knock me up!"
                                
                    elif selected_girl.initial_reaction == "manipulative":
                        # Check if she actually wants a baby too
                        if selected_girl.baby_desire > 60:
                            # She wants your baby, but still sees it as leverage
                            if is_currently_a_mother:
                                selected_girl.character "A baby with you? Well now... another baby to add to our family? That changes things. I DO want this, but I'm not giving it away for free. What's your offer?"
                            else:
                                selected_girl.character "A baby with you? Well now... that changes things. I DO want a baby, and you're the perfect candidate... but I'm not giving it away for free. What's your offer?"
                            
                            menu:
                                "Offer 2000 cash for baby expenses?":
                                    if player.cash >= 2000:
                                        $ player.cash -= 2000
                                        $ selected_girl.wants_vaginal_condom = False
                                        $ selected_girl.apply_impacts({"baby_desire": (750, 1000), "corruption": (450, 750)})
                                        if is_currently_a_mother:
                                            selected_girl.character "2000 upfront? That's reasonable since we both want this and our family is growing. Fine, you can breed me... but I still expect support. This works out for both of us."
                                        else:
                                            selected_girl.character "2000 upfront? That's reasonable since we both want this. Fine, you can breed me... but I still expect child support. This works out for both of us."
                                    else:
                                        if is_currently_a_mother:
                                            selected_girl.character "You think that's enough when we BOTH want this baby and our family is growing? Come back when you're serious about our future."
                                        else:
                                            selected_girl.character "You think that's enough when we BOTH want this baby? Come back when you're serious about our future."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                
                                "Promise to give her an A+..." if is_student:
                                    if selected_girl.grades >= 100:
                                        selected_girl.character "My grades are already maxed. Your offer is useless. Try something else."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    else:
                                        $ selected_girl.grades = 100
                                        $ selected_girl.wants_vaginal_condom = False
                                        $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750), "corruption": (950, 1500), "discipline": (-750, -250)})
                                        selected_girl.character "A+ and medical coverage? Now THAT's a negotiation. Fine, you can put a baby in me..."
                                
                                "Leave it be.":
                                    if is_currently_a_mother:
                                        selected_girl.character "Fine. But you're passing up on growing our family together. Don't come crying to me when you realize what you missed."
                                    else:
                                        selected_girl.character "Fine. But you're passing up on something we both want. Don't come crying to me when you realize what you missed."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                        else:
                            # She doesn't really want a baby - pure business transaction
                            if is_currently_a_mother:
                                selected_girl.character "Another baby? I already have children, Professor. We're talking significant financial commitment for our growing family. What's your offer?"
                            else:
                                selected_girl.character "A baby? That's a lifetime commitment, Professor. We're talking 18+ years of support. What's your offer?"
                            
                            menu:
                                "Offer 5000 cash for baby expenses?":
                                    if player.cash >= 5000:
                                        $ player.cash -= 5000
                                        $ selected_girl.wants_vaginal_condom = False
                                        $ selected_girl.apply_impacts({"baby_desire": (1000, 1500), "corruption": (950, 1500)})
                                        if is_currently_a_mother:
                                            selected_girl.character "5000 upfront? That's a start for another child. Fine, you can breed me... but I expect significant child support for our growing family."
                                        else:
                                            selected_girl.character "5000 upfront? That's a start. Fine, you can breed me... but I expect regular child support payments. This is strictly business."
                                    else:
                                        selected_girl.character "You think 5000 covers raising a baby? Don't insult me. Come back when you're serious."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                "Promise to cover all medical expenses(2000) and give her an A+" if is_student:
                                    if selected_girl.grades >= 100 or player.cash <=2000:
                                        if selected_girl.grades >= 100:
                                            selected_girl.character "My grades are already maxed. Your offer is useless. Try something else."
                                        if  player.cash <=2000:
                                            selected_girl.character "Come back when you actually have the cash, PRO..FESS...OR...dumbass..."
                                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                                    else:
                                        $ selected_girl.grades = 100
                                        $ selected_girl.wants_vaginal_condom = False
                                        $ selected_girl.apply_impacts({"baby_desire": (550, 1000), "affection": (250, 750), "corruption": (750, 1000), "discipline": (-750, -250)})
                                        if is_currently_a_mother:
                                            selected_girl.character "Medical coverage plus guaranteed A+? Now that's a negotiation. Fine, you can put another baby in me... deal of a lifetime!"
                                        else:
                                            selected_girl.character "Medical coverage plus guaranteed A+? Now that's a negotiation. Fine, you can put a baby in me... deal of a lifetime!"
                                "Leave it be.":
                                    if is_currently_a_mother:
                                        selected_girl.character "Smart move. Another child is expensive, and I'm not giving you one without proper compensation for our family."
                                    else:
                                        selected_girl.character "Smart move. Raising a kid is expensive, and I'm not giving you one without proper compensation."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    elif selected_girl.initial_reaction in ["seductive", "submissive"]:
                        # Sexually open but need more convincing for baby
                        if selected_girl.baby_desire > 50:
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "corruption": (250, 750)})
                            
                            if selected_girl.initial_reaction == "seductive":
                                if is_currently_a_mother:
                                    selected_girl.character "Mmm... breeding me again? That's so hot. Fine, you can cum in my bare pussy and give me another baby... but you better take responsibility."
                                else:
                                    selected_girl.character "Mmm... breeding me? That's so hot. Fine, you can cum in my bare pussy... but you better take responsibility."
                            elif selected_girl.initial_reaction == "submissive":
                                if is_currently_a_mother:
                                    selected_girl.character "If you want to put another baby in me, Master... I'll let you cum in my bare pussy."
                                else:
                                    selected_girl.character "If you want to put a baby in me, Master... I'll let you cum in my bare pussy."
                        else:
                            $ selected_girl.wants_vaginal_condom = True
                            if is_currently_a_mother:
                                selected_girl.character "Another baby? That's... a lot. I already have children to think about."
                            else:
                                selected_girl.character "A baby? That's... a lot. I'm not sure I'm ready for that."
                    else:  # admiring, neutral, or low baby desire
                        $ selected_girl.wants_vaginal_condom = True
                        if is_currently_a_mother:
                            selected_girl.character "Another baby? I'm not sure I'm ready to expand our family right now."
                        else:
                            selected_girl.character "That's not something I'm comfortable discussing right now."
                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
                
                "Would you consider letting me fuck your bare pussy sometimes?":
                    # No persuasion needed - the reaction already tells us the answer
                    # Check different reaction types
                    if selected_girl.initial_reaction in ["seductive", "infatuated", "generous"]:
                        # These are already open to it
                        $ selected_girl.wants_vaginal_condom = False
                        $ selected_girl.apply_impacts({"corruption": (550, 1000), "affection": (250, 750)})
                        
                        if selected_girl.initial_reaction == "seductive":
                            selected_girl.character "Mmm... bareback fucking my pussy? I've been wanting you to ask. Take me bare."
                        elif selected_girl.initial_reaction == "infatuated":
                            selected_girl.character "Anything for you! I want to feel your bare cock inside my pussy so badly."
                        elif selected_girl.initial_reaction == "generous":
                            selected_girl.character "I want to give you everything. My bare pussy is yours whenever you want it."
                            
                    elif selected_girl.initial_reaction == "manipulative":
                        # This is where the manipulation menu fits
                        selected_girl.character "Bare pussy access? That's a premium service, Professor. What are you offering?"
                        
                        menu:
                            "Grant her a 500 cash incentive?":
                                if player.cash >= 500:
                                    $ player.cash -= 500
                                    $ selected_girl.wants_vaginal_condom = False
                                    $ selected_girl.apply_impacts({"corruption": (650, 1000), "affection": (250, 750)})
                                    if is_currently_a_mother:
                                        selected_girl.character "Well now... 500 for bare pussy access from a single mother? Deal. Just don't get too attached - this is a business arrangement."
                                    else:
                                        selected_girl.character "Well now... 500 for bare pussy access? Deal. Just don't get too attached - this is a business arrangement."
                                else:
                                    selected_girl.character "Don't waste my time with empty promises, Professor. Come back when you can actually pay."
                                    $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            "Grant her an automatic 10 percent to her grades" if is_student:
                                if selected_girl.grades >= 100:
                                    girl.character "My grades are already perfect. Don't lie to me. Cash or get lost."
                                    $ girl.apply_impacts({"affection": (-750, -250)})
                                else:
                                    $ selected_girl.grades = min(100, selected_girl.grades + 10)
                                    $ selected_girl.wants_vaginal_condom = False
                                    $ selected_girl.apply_impacts({"corruption": (850, 1000), "affection": (250, 750), "discipline": (-750, -250)})
                                    if selected_girl.birth_control:
                                        selected_girl.character "Grade manipulation for bareback privileges? I like how you think, Professor. Fine, you can fuck my bare pussy... but if you knock me up, we are discussing new terms!"
                                    else:
                                        selected_girl.character "Grade manipulation for bareback privileges? I like how you think, Professor. Fine, you can fuck my bare pussy... but your playing with fire! If you knock me up, we are discussing new terms!"
                            "Leave it be.":
                                if is_currently_a_mother:
                                    selected_girl.character "Suit yourself. My bare pussy stays on lockdown until you learn how negotiations work - I have a child to feed."
                                else:
                                    selected_girl.character "Suit yourself. My bare pussy stays on lockdown until you learn how negotiations work."
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                    
                    elif selected_girl.initial_reaction in ["submissive", "devoted", "loving"]:
                        # These will agree to please the player
                        $ selected_girl.wants_vaginal_condom = False
                        $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                        
                        if selected_girl.initial_reaction == "submissive":
                            if is_currently_a_mother:
                                selected_girl.character "If that's what you want, Master... I'll let you fuck my bare pussy - my body is yours to command."
                            else:
                                selected_girl.character "If that's what you want, Master... I'll let you fuck my bare pussy."
                        elif selected_girl.initial_reaction == "devoted":
                            if is_currently_a_mother:
                                selected_girl.character "Anything for you. Take my bare pussy whenever you wish - even with my maternal duties."
                            else:
                                selected_girl.character "Anything for you. Take my bare pussy whenever you wish."
                        elif selected_girl.initial_reaction == "loving":
                            if is_currently_a_mother:
                                selected_girl.character "I trust you completely. Let's feel each other without anything between us - I know you'll respect me as a mother."
                            else:
                                selected_girl.character "I trust you completely. Let's feel each other without anything between us."
                    
                    else:  # admiring, neutral, or others
                        $ selected_girl.wants_vaginal_condom = True
                        if is_currently_a_mother:
                            selected_girl.character "I'm not comfortable with that. I need to be careful as a mother - let's stick to condoms for now."
                        else:
                            selected_girl.character "I'm not comfortable with that. Let's stick to condoms for now."

    
    # Calculate and log baby_desire change (matching small_talk_pregnancy tracking)
    $ baby_desire_change = selected_girl.baby_desire - previous_baby_desire
    $ renpy.log(f"Baby desire changed by {baby_desire_change} for {selected_girl.first_name}")
    
    # Set up for future interactions (matching small_talk_pregnancy pattern)
    $ actions_already_done.setdefault(selected_girl.id, []).append("pregnancy_followup")
    
    # Schedule next follow-up based on discussion level
    if selected_girl.pregnancy_discussion_level == 1:
        $ selected_girl.pregnancy_followup = time_manager.total_days + 7
    elif selected_girl.pregnancy_discussion_level == 2:
        $ selected_girl.pregnancy_followup = time_manager.total_days + 10
    else:
        # At max discussion level, no more scheduled follow-ups
        $ renpy.log(f"No further pregnancy follow-ups scheduled for {selected_girl.first_name}")
    
    # Skip time for conversation
    $ time_manager.skip_time(minutes=5)
    
    return



label vt_pregnancy_discovery:
    # NEITHER knows she's pregnant - player might discover it first
    $ pregnancy_phase = selected_girl.pregnancy_phase

    # Calculate discovery chance based on multiple factors
    $ discovery_chance = 25 + (selected_girl.intellect // 3)

    # Pregnancy phase affects visibility
    if pregnancy_phase >= 2:
        $ discovery_chance += 30  # Much more obvious in 2nd/3rd trimester
    elif pregnancy_phase == 1:
        $ discovery_chance += 10  # Slightly more obvious in 1st trimester

    # Physical changes matter
    if selected_girl.preg_body:
        $ discovery_chance += 25  # Visible baby bump

    # Previous discussions help
    if has_discussed_pregnancy_before:
        $ discovery_chance += 15

    # Existing kids with player makes him more observant
    if kids_with_player > 0:
        $ discovery_chance += 20  # He's more likely to notice pregnancy signs

    # Baby desire affects how obvious she makes it
    if selected_girl.baby_desire > 70:
        $ discovery_chance += 15  # Subconsciously wants him to know
    elif selected_girl.baby_desire < 30:
        $ discovery_chance -= 15  # Actively hiding it

    # Only attempt discovery if chance is met
    if renpy.random.randint(1, 100) < discovery_chance:
        # Player discovers BEFORE she knows
        if pregnancy_phase == 1:
            # FIRST TRIMESTER - subtle symptoms
            "[selected_girl] rubs her stomach absentmindedly, looking slightly uncomfortable."

            if selected_girl.fear > 70:
                selected_girl.character "I've been feeling strange lately... tired all the time and my clothes feel tighter. I hope I'm not sick..."
            elif selected_girl.intellect > 70:
                selected_girl.character "My cycle is [renpy.random.randint(35,45)] days late. That's statistically unusual for me."
            elif selected_girl.naturism > 80:
                selected_girl.character "My body is changing in ways that feel so natural... but different from before."
            else:
                selected_girl.character "I've been feeling different lately... it's hard to explain."

        elif pregnancy_phase >= 2:
            # SECOND OR THIRD TRIMESTER - obvious signs
            if selected_girl.preg_body:
                "[selected_girl] has a visible baby bump that's becoming harder to hide."
                "[selected_girl] notices you looking at her rounded belly and shifts uncomfortably."
            else:
                "[selected_girl] moves differently, more carefully, one hand often supporting her lower back."

            if selected_girl.fear > 70:
                selected_girl.character "My clothes have been fitting differently lately... I hope it's nothing serious."
            elif selected_girl.intellect > 70:
                selected_girl.character "I've noticed several pregnancy symptoms, but statistically it's unlikely to be that."
            elif selected_girl.naturism > 80:
                selected_girl.character "My body is embracing these changes with such grace... it's beautiful."
            else:
                selected_girl.character "I've been gaining a lot of weight lately... it's hard to explain."

        # DISCOVERY MENU - PLAYER DISCOVERIES, SHE REALIZES
        menu:
            "I think you might be pregnant.":
                # Simple check using player's compassionate approach
                $ norm_compassion = (player.compassion + 10) / 2
                $ norm_reputation = player.reputation / 10
                $ compassion_approach = (norm_compassion + norm_reputation) / 2
                
                if compassion_approach > 6 or selected_girl.intellect > 50:
                    # She realizes through conversation
                    $ selected_girl.knows_pregnant = True
                    $ selected_girl.player_knows_pregnant = True
                    $ selected_girl.apply_impacts({"intellect": (750, 1000)})

                    if selected_girl.baby_desire > 70:
                        $ selected_girl.previous_pregnancy_reaction = "positive"
                        if selected_girl.dominant_approach == "compassionate":
                            selected_girl.character "Oh... you're right. That would explain everything... and honestly, I'm thrilled! I'm having your baby!"
                        elif selected_girl.dominant_approach == "sexualized":
                            selected_girl.character "Wait... you think I'm pregnant? That would explain why I'm so horny all the time! You knocked me up!"
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "Wait... pregnant? That changes everything. My value just increased significantly."
                        elif selected_girl.dominant_approach == "dominate":
                            selected_girl.character "Pregnant? That would explain the symptoms. I accept this diagnosis."
                        else:
                            selected_girl.character "Oh... you're right. That would explain everything... and honestly, I'm thrilled!"
                    else:
                        $ selected_girl.previous_pregnancy_reaction = "neutral"
                        if selected_girl.dominant_approach == "compassionate":
                            selected_girl.character "Oh... you're right. That would explain everything... but I'm scared..."
                        elif selected_girl.dominant_approach == "sexualized":
                            selected_girl.character "Wait... pregnant? Seriously? That's... a lot to process."
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "Wait... pregnant? That complicates my plans significantly. This is not ideal."
                        elif selected_girl.dominant_approach == "dominate":
                            selected_girl.character "Pregnant? That would explain the symptoms. This presents complications."
                        else:
                            selected_girl.character "Oh... you're right. That would explain everything... but I'm scared."
                else:
                    $ selected_girl.previous_pregnancy_reaction = "negative"
                    selected_girl.character "What? No, that's ridiculous. I'd know if I was pregnant..."
                    $ selected_girl.apply_impacts({"fear": (550, 1000)})

            "Have you considered taking a pregnancy test?":
                # Simple check using player's compassionate approach
                $ norm_compassion = (player.compassion + 10) / 2
                $ norm_reputation = player.reputation / 10
                $ compassion_approach = (norm_compassion + norm_reputation) / 2
                
                if compassion_approach > 5:
                    $ selected_girl.previous_pregnancy_reaction = "neutral"
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "I... I suppose I should. Just to be sure it's nothing serious. Thank you for being so concerned about me."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "A pregnancy test? Hmm... I guess I could. Though if I am pregnant, you'll have to take responsibility for knocking me up, won't you?"
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "I'll consider it. But if I'm pregnant, we'll need to discuss compensation for my time and the test costs."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "If you believe it's necessary, I will take the test. Your judgment in this matter is noted."
                    else:
                        selected_girl.character "I... I suppose I should. Just to be sure it's nothing serious."
                    $ selected_girl.apply_impacts({"discipline": (750, 1000)})
                else:
                    $ selected_girl.previous_pregnancy_reaction = "negative"
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "I don't think that's necessary... I'm probably just not feeling well."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "Why would I need a test? I feel fine. Besides, pregnancy tests are so clinical... not sexy at all."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "I don't need a pregnancy test. Unless you're planning to pay for it and compensate me for my time?"
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "That is unnecessary. I would know if my body had changed in such a manner."
                    else:
                        selected_girl.character "I don't need a pregnancy test. I'm not pregnant."
                    $ selected_girl.apply_impacts({"fear": (550, 1000)})

            "You've been showing some pregnancy symptoms lately...":
                # Simple check - compassionate helps, controlling hurts
                $ norm_compassion = (player.compassion + 10) / 2
                $ norm_control = (player.control + 10) / 2
                
                if norm_compassion > 6 or norm_control < 7:
                    $ selected_girl.previous_pregnancy_reaction = "neutral"
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "Symptoms? What do you mean? I've just been feeling a bit off lately... but you've noticed? That's actually quite sweet of you."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "Symptoms? You mean like being horny all the time and my boobs getting bigger? Yeah, I guess I have been showing some... symptoms."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "Symptoms? If you're suggesting pregnancy, that's valuable information. My symptoms would indeed change our current arrangement."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "My physical condition is not open for debate. If there are symptoms, I am managing them appropriately."
                    else:
                        selected_girl.character "Symptoms? What do you mean? I've just been feeling a bit off lately..."
                    $ selected_girl.apply_impacts({"intellect": (550, 1000)})
                else:
                    $ selected_girl.previous_pregnancy_reaction = "negative"
                    if selected_girl.dominant_approach == "compassionate":
                        selected_girl.character "That's not very appropriate to say, Professor... I'm just not feeling well."
                    elif selected_girl.dominant_approach == "sexualized":
                        selected_girl.character "Are you calling me fat? Because that's what it sounds like. Not cool."
                    elif selected_girl.dominant_approach == "transactional":
                        selected_girl.character "My physical condition is not up for discussion unless there's financial compensation involved."
                    elif selected_girl.dominant_approach == "dominate":
                        selected_girl.character "Your observations are unwelcome. Do not comment on my physical condition again."
                    else:
                        selected_girl.character "That's inappropriate to say, Professor. I'm just not feeling well."
                    $ selected_girl.apply_impacts({"affection": (-1500, -750)})

    return


label vt_pregnancy_confession:
    # SHE knows but PLAYER doesn't - her confession
    if selected_girl.preg_father == "player":
        if kids_with_player > 0:
            # Already has kids with him
            "[selected_girl] looks nervous but determined to tell you something."

            if selected_girl.baby_desire > 70:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "I have something to tell you... I'm pregnant again! We're having another baby!"
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Guess what? You knocked me up again! I'm pregnant!"
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "I am pregnant with your second child. We need to discuss financial arrangements immediately."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "I am carrying your second child. This information is provided for planning purposes."
                else:
                    selected_girl.character "I'm pregnant again... with your baby."
            else:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "I need to tell you something... I'm pregnant again. I'm scared, but I wanted you to know."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Well... I'm pregnant again. Yeah. It's... a lot, you know?"
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "I am pregnant again. This requires immediate renegotiation of our support arrangement."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "I am pregnant again. This presents logistical challenges we must address."
                else:
                    selected_girl.character "I'm pregnant again... and it's yours."
        else:
            # First baby with him
            "[selected_girl] takes a deep breath, looking nervous."

            if selected_girl.baby_desire > 70:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "I have something wonderful to tell you... I'm pregnant! I'm carrying your baby!"
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "I took a test... and I'm pregnant! You knocked me up!"
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "I have confirmed I am pregnant. Since you are the father, we need to discuss financial arrangements immediately."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "I am pregnant. You are the father. This is a fact we must address."
                else:
                    selected_girl.character "I'm pregnant... and it's yours."
            else:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "I need to tell you something... I'm pregnant. I'm scared, but I wanted you to be the first to know."
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Well... I'm pregnant. Yeah. It's... a lot, you know?"
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "I am pregnant. This requires immediate discussion of terms and your involvement."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "I am pregnant. This presents significant complications that require your involvement."
                else:
                    selected_girl.character "I'm pregnant... and I think it's yours."
    else:
        # Pregnant by someone else
        "[selected_girl] looks uncomfortable, avoiding eye contact."

        if selected_girl.dominant_approach == "compassionate":
            selected_girl.character "Professor... I need to tell you something. I'm pregnant. It's... not yours. I'm so sorry..."
        elif selected_girl.dominant_approach == "sexualized":
            selected_girl.character "So... funny story. I'm pregnant. Yeah, not yours though. Sorry?"
        elif selected_girl.dominant_approach == "transactional":
            selected_girl.character "I am pregnant. Since you are not the father, this doesn't directly concern you, but I felt you should know."
        elif selected_girl.dominant_approach == "dominate":
            selected_girl.character "I am pregnant. The father is someone else. This information is provided for transparency."
        else:
            selected_girl.character "I... I'm pregnant. It's not yours, but I thought you should know."

    $ selected_girl.player_knows_pregnant = True
    return


#the end of file cause labels suck at collapsing :P
