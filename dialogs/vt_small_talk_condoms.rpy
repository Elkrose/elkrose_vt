#SPECIFIC CHERRY DIALOGS
# to catch mothers if not hasattr(self, "daughter"):

# Save-compat shim: redirect the old un-prefixed label name (pre-1.0.6 saves/references) instead of erroring.
label small_talk_condoms:
    jump vt_small_talk_condoms

label vt_small_talk_condoms:
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
    
    # FETISH INTEGRATION
    $ vaginal_fetish = max(selected_girl.pussy_cum_fetish or 0, selected_girl.vaginal_cum_fetish or 0)
    $ anal_fetish = max(selected_girl.ass_cum_fetish or 0, selected_girl.anal_cum_fetish or 0)
    $ body_fetish = max(selected_girl.thigh_cum_fetish or 0, selected_girl.boob_cum_fetish or 0)
    
    # PROTECTION STATE TRACKING
    $ protection_state = {
        "vaginal": selected_girl.wants_vaginal_condom,
        "anal": selected_girl.wants_anal_condom,
        "oral": selected_girl.wants_oral_condom,
        "body": selected_girl.wants_body_condom
    }

    # Calculate the original protection count
    $ protection_count = sum(1 for p in protection_state.values() if p)

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

    if not hasattr(selected_girl, "previous_condoms_reaction"):
        $ selected_girl.previous_condoms_reaction = "neutral"
    if not hasattr(selected_girl, "condoms_discussion_level"):
        $ selected_girl.condoms_discussion_level = 0
    if not hasattr(selected_girl, "condoms_followup"):
        $ selected_girl.condoms_followup = 0
    
    # TRACK CONVERSATION HISTORY
    $ has_discussed_condoms_before = getattr(selected_girl, "has_discussed_condoms_before", False)
    $ previous_condoms_reaction = getattr(selected_girl, "previous_condoms_reaction", "neutral")
    $ condoms_discussion_level = getattr(selected_girl, "condoms_discussion_level", 1)
    
    # CHECK FOR ACTIVE FOLLOW-UP 
    # If we have a scheduled follow-up that's ready to happen
    if hasattr(selected_girl, "has_condoms_followup") and selected_girl.has_condoms_followup:
        # Reset the flag so it doesn't keep appearing
        $ selected_girl.has_condoms_followup = False
        
        # Update tracking variables for the follow-up
        $ selected_girl.condoms_discussion_level = min(3, condoms_discussion_level + 1)
        
        # Show follow-up specific dialogue based on her dominant approach
        if selected_girl.dominant_approach == "compassionate":
            if previous_condoms_reaction == "positive":
                "[selected_girl]'s eyes light up with warmth as you approach her, clearly remembering your beautiful conversation about protection and intimacy."
                if is_base_mother and child_reference:
                    selected_girl.character "Professor! I've been thinking so much about our talk... even with [child_reference] to consider, I feel closer to you knowing we understand each other so well."
                elif is_student:
                    selected_girl.character "Professor! I've been thinking about our protection talk... it made me feel so connected to you. I'm glad we had that conversation."
                else:
                    selected_girl.character "Professor! I've been thinking about our protection talk... I feel so much closer to you now that we understand each other."
            elif previous_condoms_reaction == "negative":
                "[selected_girl] looks hesitant as you approach, clearly remembering your difficult discussion about protection."
                if is_base_mother:
                    selected_girl.character "Professor... I've been thinking about what we discussed... as an experienced mother, I'm still not comfortable with some of those suggestions."
                elif is_student:
                    selected_girl.character "Professor... I've been thinking about our talk... I'm still not sure about some of the protection changes we discussed."
                else:
                    selected_girl.character "Professor... I've been thinking about our talk... I'm still not comfortable with some of those suggestions."
            else:
                "[selected_girl] gives you a thoughtful smile as you approach, clearly processing your previous protection discussion."
                selected_girl.character "Professor... I've been thinking about our protection talk. Thank you for being so understanding about my preferences."
        
        elif selected_girl.dominant_approach == "sexualized":
            if previous_condoms_reaction == "positive":
                "[selected_girl] licks her lips as you approach, a hungry look in her eyes as she clearly remembers your steamy conversation about protection."
                if is_base_mother:
                    selected_girl.character "Mmm, Professor... I've been fantasizing about our protection talk all week. As an experienced woman, I can't wait to try out our new arrangements..."
                elif is_student:
                    selected_girl.character "Professor! I've been thinking about our protection talk non-stop! It was so hot discussing all those intimate details with you..."
                else:
                    selected_girl.character "Professor... I've been fantasizing about our protection talk. I can't wait to experience everything we discussed..."
            elif previous_condoms_reaction == "negative":
                "[selected_girl] rolls her eyes dramatically as you approach, clearly annoyed that you're bringing up the protection topic again."
                if is_base_mother:
                    selected_girl.character "Professor, really? As an experienced woman, I thought we were done with the boring protection logistics. Can't we talk about something more exciting?"
                elif is_student:
                    selected_girl.character "Ugh, protection again? I thought we were done with that boring stuff. Can't we talk about something actually fun?"
                else:
                    selected_girl.character "Protection again? I thought we covered everything. Can't we move on to more exciting topics?"
            else:
                "[selected_girl] gives you a curious look as you approach, clearly wondering what direction your protection talk will take this time."
                selected_girl.character "Professor... back to talk about protection? Hmm... okay, but let's make it more interesting this time, shall we?"
        
        elif selected_girl.dominant_approach == "transactional":
            if previous_condoms_reaction == "positive":
                "[selected_girl] gets a calculating gleam in her eye as you approach, already running numbers in her head about your protection arrangements."
                if is_base_mother:
                    selected_girl.character "Professor. I've been reviewing our protection agreements. As an experienced mother, I believe our current arrangement is mutually beneficial, though I'm open to renegotiations if you have new terms."
                elif is_student:
                    selected_girl.character "Professor! I've been thinking about our protection deal... is this where you offer me more money or grades for different arrangements?"
                else:
                    selected_girl.character "Professor. I've been analyzing our protection terms. Unless you have new offers to make, I believe our current arrangement stands."
            elif previous_condoms_reaction == "negative":
                "[selected_girl] looks impatient as you approach, clearly viewing your follow-up as a waste of time and resources."
                if is_base_mother:
                    selected_girl.character "Professor, unless you're planning to significantly improve your offer for protection changes, as an experienced mother, I don't see why we're discussing this again."
                elif is_student:
                    selected_girl.character "Professor... unless you're planning to pay me more or give me better grades, I don't really want to talk about protection again."
                else:
                    selected_girl.character "Professor, unless you have new financial terms to offer, I don't see the point in revisiting our protection arrangements."
            else:
                "[selected_girl] looks analytical as you approach, clearly weighing the pros and cons of your protection discussion."
                selected_girl.character "Professor. You wanted to follow up about protection terms? Very well, but make it worth my time. What new proposals do you have?"
        
        elif selected_girl.dominant_approach == "dominate":
            if previous_condoms_reaction == "positive":
                "[selected_girl] stands taller as you approach, her expression serious and determined as she remembers your discussion about protection protocols."
                if is_base_mother:
                    selected_girl.character "Professor. I have been implementing our protection agreements as discussed. As an experienced mother, I maintain proper protocols for all activities we've agreed upon."
                elif is_student:
                    selected_girl.character "Professor. I've been following our protection discussion... I'm doing what you want with protection, just like we talked about."
                else:
                    selected_girl.character "Professor. I have been adhering to our protection agreements as instructed. All protocols are being maintained."
            elif previous_condoms_reaction == "negative":
                "[selected_girl] stiffens defensively as you approach, her expression cold as she remembers your unwanted protection discussion."
                if is_base_mother:
                    selected_girl.character "Professor. As an experienced mother, I believe my position on protection was made clear. Unless you have new commands, this discussion is concluded."
                elif is_student:
                    selected_girl.character "Professor... I thought we were done talking about protection. I'm not changing my mind unless you tell me to."
                else:
                    selected_girl.character "Professor. My position on protection remains unchanged. Unless you have new directives, this matter is settled."
            else:
                "[selected_girl] nods respectfully as you approach, her expression focused as she remembers your serious discussion about protection."
                selected_girl.character "Professor. You wished to continue our protection discussion. I am prepared to receive your instructions on this matter."
        
        else:
            # Fallback for any other approaches
            "[selected_girl] arches a brow as you approach her, clearly remembering your previous conversation about protection."
            if previous_condoms_reaction == "positive":
                selected_girl.character "Professor! I've been thinking about our protection talk. It was nice figuring that out together."
            elif previous_condoms_reaction == "negative":
                selected_girl.character "Professor... back to this topic again? I thought we were done discussing protection."
            else:
                selected_girl.character "Professor... you wanted to talk more about protection? I'm listening..."
        
        # Call the actual follow-up dialogue
        call vt_small_talk_condoms_followup from _call_vt_small_talk_condoms_followup
        
        # Exit after follow-up completes
        return
    
    # INITIAL GREETING - CHARACTER-APPROPRIATE WITH MEMORY
    "You approach [selected_girl] to discuss protection preferences."
    
    if has_discussed_condoms_before:
        if previous_condoms_reaction == "positive":
            if selected_girl.dominant_approach == "compassionate":
                if is_base_mother:
                    selected_girl.character "You wanted to talk more about protection? I've been thinking about what we discussed... it's nice to feel so connected with you."
                elif is_student:
                    selected_girl.character "You wanted to talk more about protection? I've been thinking about what we discussed... I'm still a little nervous but I trust you."
                else:
                    selected_girl.character "You wanted to talk more about protection? I've been thinking about what we discussed... I feel close to you."
            elif selected_girl.dominant_approach == "sexualized":
                if is_base_mother:
                    selected_girl.character "Back to talk about protection? Mmm... I've been touching myself thinking about our last conversation... it was so hot."
                elif is_student:
                    selected_girl.character "Back to talk about protection? I've been fantasizing about what we discussed... it makes me so wet thinking about it."
                else:
                    selected_girl.character "Back to talk about protection? I've been fantasizing about what we discussed... it turns me on remembering it."
            elif selected_girl.dominant_approach == "transactional":
                if is_base_mother:
                    selected_girl.character "Back to this topic? I've already established my position as an experienced woman. Unless you have new terms to offer..."
                elif is_student:
                    selected_girl.character "Back to this topic? I've already told you what I think... are you going to make it worth my time this time?"
                else:
                    selected_girl.character "Back to this topic? I've already established my position. Unless you have new terms to offer..."
            elif selected_girl.dominant_approach == "dominate":
                if is_base_mother:
                    selected_girl.character "We've already addressed this topic. As an experienced mother, I found our previous discussion sufficient."
                elif is_student:
                    selected_girl.character "We've already addressed this topic. I found our previous discussion sufficient, Professor."
                else:
                    selected_girl.character "We've already addressed this topic. I found our previous discussion sufficient."
        elif previous_condoms_reaction == "negative":
            if selected_girl.dominant_approach == "compassionate":
                if is_base_mother:
                    selected_girl.character "Back to this topic again? I... I'm still not comfortable discussing this. Can we talk about something else?"
                elif is_student:
                    selected_girl.character "Back to this topic again? I... I'm still not comfortable discussing this. I'm scared..."
                else:
                    selected_girl.character "Back to this topic again? I... I'm still not comfortable discussing this. Can we talk about something else?"
            elif selected_girl.dominant_approach in ["sexualized", "transactional", "dominate"]:
                if is_base_mother:
                    selected_girl.character "Back to this topic again? As an experienced woman, I thought we were done with this."
                elif is_student:
                    selected_girl.character "Back to this topic again? I thought we were done with this..."
                else:
                    selected_girl.character "Back to this topic again? I thought we were done with this."
        else:
            if selected_girl.dominant_approach == "compassionate":
                if is_base_mother:
                    selected_girl.character "You wanted to talk about protection again? I'll listen... as an experienced mother, I want to understand what's important to you."
                elif is_student:
                    selected_girl.character "You wanted to talk about protection again? I'll listen... I'm still trying to understand..."
                else:
                    selected_girl.character "You wanted to talk about protection again? I'll listen... I want to understand."
            elif selected_girl.dominant_approach == "sexualized":
                if is_base_mother:
                    selected_girl.character "Protection talk again? Good... as an experienced woman, I've been wanting to discuss this more."
                elif is_student:
                    selected_girl.character "Protection talk again? Good... I've been wanting to discuss this more with you."
                else:
                    selected_girl.character "Protection talk again? Good... I've been wanting to discuss this more."
            elif selected_girl.dominant_approach == "transactional":
                if is_base_mother:
                    selected_girl.character "You wish to discuss protection again? As an experienced woman, very well, but make it worth my time."
                elif is_student:
                    selected_girl.character "You wish to discuss protection again? Very well, but make it worth my time this time."
                else:
                    selected_girl.character "You wish to discuss protection again? Very well, but make it worth my time."
            elif selected_girl.dominant_approach == "dominate":
                if is_base_mother:
                    selected_girl.character "You wish to continue our protection discussion. As an experienced mother, I am prepared to consider this seriously."
                elif is_student:
                    selected_girl.character "You wish to continue our protection discussion. I am prepared to consider this seriously, Professor."
                else:
                    selected_girl.character "You wish to continue our protection discussion. I am prepared to consider this seriously."
    else:
        $ selected_girl.has_discussed_condoms_before = True
        if selected_girl.dominant_approach == "compassionate":
            if is_base_mother:
                selected_girl.character "I'm glad you wanted to talk about this, Professor. As an experienced mother, protection is something I take seriously."
            elif is_student:
                selected_girl.character "I'm glad you wanted to talk about this, Professor. Protection is... something I've been thinking about."
            else:
                selected_girl.character "I'm glad you wanted to talk about this. Protection is something important to discuss."
        elif selected_girl.dominant_approach == "sexualized":
            if is_base_mother:
                selected_girl.character "Mmm... protection talk? As an experienced woman, I know all about making protection... interesting."
            elif is_student:
                selected_girl.character "Protection talk? I've never really talked about this stuff before but it's kind of exciting..."
            else:
                selected_girl.character "Protection talk? I find protection can be... quite exciting actually."
        elif selected_girl.dominant_approach == "transactional":
            if is_base_mother:
                selected_girl.character "Protection preferences? As an experienced woman, I know exactly what my preferences are worth. What's your offer?"
            elif is_student:
                selected_girl.character "Protection preferences? I'm not really sure what this is worth... what are you offering?"
            else:
                selected_girl.character "Protection preferences? What's in it for me? I might share if you make it worth my while."
        elif selected_girl.dominant_approach == "dominate":
            if is_base_mother:
                selected_girl.character "Protection preferences. As an experienced mother, proceed with your questions."
            elif is_student:
                selected_girl.character "Protection preferences. Proceed with your questions, Professor."
            else:
                selected_girl.character "Protection preferences. Proceed with your questions."
    
    
    # MAIN CONVERSATION - SPECIFIC PROTECTION TOPICS
    menu:
        "What are your thoughts on condoms for vaginal sex?":
            $ selected_girl.player_knows_vaginal_condom = True
            
            # Check if she's already pregnant - if so, she won't care about vaginal condoms
            if selected_girl.pregnant:
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I'm already pregnant, Professor. As an experienced mother, vaginal protection isn't really necessary anymore, is it?"
                    elif is_student:
                        selected_girl.character "I'm already pregnant, Professor. So I guess we don't need condoms for vaginal anymore?"
                    else:
                        selected_girl.character "I'm already pregnant, Professor. Vaginal protection isn't necessary anymore."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I'm pregnant! Oh my god, as an experienced woman, being bare while pregnant is so hot! No condoms needed!"
                    elif is_student:
                        selected_girl.character "I'm pregnant! Oh my god, no condoms needed! That's so hot!"
                    else:
                        selected_girl.character "I'm pregnant! No condoms needed! That's hot!"
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I'm already carrying your child. As an experienced mother, vaginal access is now included in our pregnancy arrangement."
                    elif is_student:
                        selected_girl.character "I'm already pregnant... so does bare access come free now or do I still get paid?"
                    else:
                        selected_girl.character "I'm already carrying your child. Vaginal access is included in the pregnancy arrangement."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I am pregnant. As an experienced mother, vaginal protection is unnecessary. Proceed as you wish."
                    elif is_student:
                        selected_girl.character "I'm pregnant... so if you don't want to use condoms, that's okay, Professor."
                    else:
                        selected_girl.character "I am pregnant. Vaginal protection is unnecessary. Proceed as you wish."
                
                $ selected_girl.wants_vaginal_condom = False
                $ selected_girl.previous_condoms_reaction = "positive"
            
            # Not pregnant - check her current preference
            elif selected_girl.wants_vaginal_condom:
                # She wants condoms
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "As an experienced mother, I need to be careful. When you're inside my pussy, I need that protection - I can't risk another pregnancy right now."
                    elif is_student:
                        selected_girl.character "I feel so connected to you, but I'm kind of scared... when you're inside my pussy, I think I need that protection. I'm not ready to be a mom yet."
                    else:
                        selected_girl.character "I feel so connected to you, but when you're inside my pussy, I need that rubber layer. It lets me relax and enjoy us without worry."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "The way you look at me is so hot... but as an experienced woman, I need to be careful. Watching you roll a condom over your hard cock before fucking me shows you respect my situation."
                    elif is_student:
                        selected_girl.character "The way you look at me is so hot... but I'm kind of scared of getting pregnant. Watching you put on a condom makes me feel safer... and actually kind of sexy in a responsible way?"
                    else:
                        selected_girl.character "The way you look at me is so hot... but watching you roll a condom over your hard cock before fucking me can be its own kind of sexy."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "What's in it for me? As an experienced mother with responsibilities, protected vaginal sex costs extra - I have childcare to pay for."
                    elif is_student:
                        selected_girl.character "What's in it for me? Protected vaginal sex... um, does that cost less than without? I'm not sure about the pricing here..."
                    else:
                        selected_girl.character "What's in it for me? Protected vaginal sex costs extra... unless you make it worth my time."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "You're in charge, Professor. As an experienced mother, if you want to wrap your cock before entering my pussy, I'll accept it - I must protect my existing family."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want to use a condom when we... you know... I'll do what you want."
                    else:
                        selected_girl.character "You're in charge, Professor. If you want to wrap your cock before entering my pussy, I'll accept it."
                
                # Player can try to convince her otherwise
                menu:
                    "I respect your boundaries. We'll always use condoms for vaginal.": 
                        $ selected_girl.previous_condoms_reaction = "positive"
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "Thank you for understanding. As an experienced mother, I appreciate you respecting my responsibilities. It makes me feel even more connected to you."
                            elif is_student:
                                selected_girl.character "Thank you for understanding! That makes me feel so much better about... you know. I'm glad you're being so responsible with me."
                            else:
                                selected_girl.character "Thank you for understanding. Knowing you'll protect my pussy makes me feel even more connected to you."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "Mmm... a gentleman who respects an experienced woman's boundaries. That's unexpectedly hot. I like that."
                            elif is_student:
                                selected_girl.character "Mmm... you're being so sweet and responsible! That's actually really hot. I like that a lot."
                            else:
                                selected_girl.character "Mmm... a gentleman who respects pussy boundaries. That's unexpectedly hot. I like that."
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Fine. As an experienced mother, I'll remember this favor next time you want something - responsible men are valuable."
                            elif is_student:
                                selected_girl.character "Okay! I'll remember you were so nice about this. That was really good of you, Professor."
                            else:
                                selected_girl.character "Fine. I'll remember this favor next time you want something from me."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "Thank you, Professor. As an experienced mother, your consideration for my pussy and my family means everything to me."
                            elif is_student:
                                selected_girl.character "Thank you, Professor! I'm glad you're being so thoughtful about... about me."
                            else:
                                selected_girl.character "Thank you, Professor. Your consideration for my pussy means everything to me."
                        
                        $ selected_girl.apply_impacts({"affection": 50, "fear": -50})
                    
                    "But what if we wanted to make a baby? No condom when I cum in your pussy?":
                        # Try to convince her to skip condoms
                        if selected_girl.dominant_approach == "compassionate":
                            if selected_girl.baby_desire > 50:
                                $ selected_girl.wants_vaginal_condom = False
                                $ selected_girl.previous_condoms_reaction = "positive"
                                $ selected_girl.apply_impacts({"baby_desire": 50, "affection": 50})
                                if is_base_mother:
                                    selected_girl.character "A baby with you... as an experienced mother, I'd love to give you another child. Please cum in my bare pussy."
                                elif is_student:
                                    selected_girl.character "A baby with you? Oh my god, really? I'd love that! Please cum in my bare pussy and put a baby in me!"
                                else:
                                    selected_girl.character "A baby with you... I'd love nothing more! Please cum in my bare pussy and put a baby in me."
                            else:
                                $ selected_girl.previous_condoms_reaction = "negative"
                                if is_base_mother:
                                    selected_girl.character "I'm not ready for another baby right now, Professor. As an experienced mother, I know what that entails."
                                elif is_student:
                                    selected_girl.character "I'm not ready for a baby right now, Professor. I'm still in school!"
                                else:
                                    selected_girl.character "I'm not ready for a baby right now, Professor."
                                $ selected_girl.apply_impacts({"affection": -20})
                        
                        elif selected_girl.dominant_approach == "sexualized":
                            if selected_girl.baby_desire > 40:
                                $ selected_girl.wants_vaginal_condom = False
                                $ selected_girl.previous_condoms_reaction = "positive"
                                $ selected_girl.apply_impacts({"baby_desire": 30, "corruption": 50})
                                if is_base_mother:
                                    selected_girl.character "A baby? You knocking me up again? As an experienced woman, that's so hot! Fill my pussy with your cum!"
                                elif is_student:
                                    selected_girl.character "A baby? You knocking me up? Oh wow! That's so hot! Please cum inside me and put a baby in me!"
                                else:
                                    selected_girl.character "A baby? You knocking me up? That's so hot! Please cum in my bare pussy and put a baby in me!"
                            else:
                                $ selected_girl.previous_condoms_reaction = "negative"
                                selected_girl.character "I'm not ready to ruin my figure for a baby right now, Professor."
                                $ selected_girl.apply_impacts({"affection": -20})
                        
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "A baby with you? That's a significant financial commitment, Professor. What are you offering?"
                            
                            menu:
                                "Offer 5000 cash for baby expenses?":
                                    if player.cash >= 5000:
                                        $ player.cash -= 5000
                                        $ selected_girl.cash += 5000
                                        $ selected_girl.wants_vaginal_condom = False
                                        $ selected_girl.previous_condoms_reaction = "positive"
                                        $ selected_girl.apply_impacts({"baby_desire": 60, "corruption": 60})
                                        if is_base_mother:
                                            selected_girl.character "5000 upfront? As an experienced mother, that's reasonable for expanding our family. Fine, you can breed me... but I expect ongoing support."
                                        elif is_student:
                                            selected_girl.character "5000? Oh my god, that's so much! Okay, yeah, you can put a baby in me for that! I'll be a good mom, I promise!"
                                        else:
                                            selected_girl.character "5000 upfront? That's a start. Fine, you can breed me... but I expect regular child support payments."
                                    else:
                                        $ selected_girl.previous_condoms_reaction = "negative"
                                        if is_base_mother:
                                            selected_girl.character "You think that's enough for an experienced woman to carry your child? Don't insult me. Come back when you're serious."
                                        elif is_student:
                                            selected_girl.character "That's not enough for a baby, is it? I don't think so... you need to be more serious than that."
                                        else:
                                            selected_girl.character "You think that's enough for 18+ years of commitment? Don't insult me. Come back when you're serious."
                                        $ selected_girl.apply_impacts({"affection": -30})
                                
                                "Promise to cover all medical expenses":
                                    $ selected_girl.wants_vaginal_condom = False
                                    $ selected_girl.previous_condoms_reaction = "positive"
                                    $ selected_girl.apply_impacts({"baby_desire": 50, "affection": 20, "corruption": 40})
                                    if is_base_mother:
                                        selected_girl.character "Medical coverage for your child? As an experienced mother, I appreciate that security. Fine, you can put a baby in me... but I want this commitment in writing."
                                    elif is_student:
                                        selected_girl.character "You'll cover all the doctor stuff? Really? Okay! That makes me feel so much better about having a baby! Yeah, let's do it!"
                                    else:
                                        selected_girl.character "Medical coverage? That's security. Fine, you can put a baby in me... but I want this contract in writing."
                                
                                "Leave it be.":
                                    $ selected_girl.previous_condoms_reaction = "negative"
                                    if is_base_mother:
                                        selected_girl.character "Smart move. An experienced mother isn't cheap, and I'm not giving you a child without proper compensation."
                                    elif is_student:
                                        selected_girl.character "Oh... okay. Maybe having a baby right now is... a lot. I understand."
                                    else:
                                        selected_girl.character "Smart move. I'm not giving you a baby without proper compensation."
                                    $ selected_girl.apply_impacts({"affection": -10})
                        
                        elif selected_girl.dominant_approach == "dominate":
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"baby_desire": 40, "affection": 30})
                            if is_base_mother:
                                selected_girl.character "If you wish to put a baby in me, Professor... as an experienced mother, I will accept your seed. My body knows how to serve you."
                            elif is_student:
                                selected_girl.character "If you want to put a baby in me, Professor... okay, I'll do that for you. Whatever you want."
                            else:
                                selected_girl.character "If you wish to put a baby in me, Professor... I will accept your seed. My body is yours to command."
                    
                    "Would you consider letting me fuck your bare pussy sometimes?":
                        # Try to convince her for occasional bare sex
                        if selected_girl.dominant_approach == "compassionate":
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 30, "affection": 30})
                            if is_base_mother:
                                selected_girl.character "I trust you completely, Professor. As an experienced mother, let's feel each other without anything between us."
                            elif is_student:
                                selected_girl.character "I trust you, Professor. I want to feel you without anything between us... that sounds really intimate."
                            else:
                                selected_girl.character "I trust you completely. Let's feel each other without anything between us."
                        
                        elif selected_girl.dominant_approach == "sexualized":
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 50, "affection": 25})
                            if is_base_mother:
                                selected_girl.character "Mmm... bareback fucking my pussy? As an experienced woman, I've been wanting you to ask. Take me bare, Professor."
                            elif is_student:
                                selected_girl.character "Mmm... bareback? Like... without a condom? I've never done that before! But... okay, yeah, I want to try! Take me bare!"
                            else:
                                selected_girl.character "Mmm... bareback fucking my pussy? I've been wanting you to ask. Take me bare."
                        
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "Bare pussy access? That's a premium service, Professor. What are you offering?"
                            
                            menu:
                                "Offer 500 cash for bareback vaginal?":
                                    if player.cash >= 500:
                                        $ player.cash -= 500
                                        $ selected_girl.cash += 500
                                        $ selected_girl.wants_vaginal_condom = False
                                        $ selected_girl.previous_condoms_reaction = "positive"
                                        $ selected_girl.apply_impacts({"corruption": 40, "affection": 10})
                                        if is_base_mother:
                                            selected_girl.character "500 for bareback access? As an experienced mother, I know that's fair. Deal. Just don't get too attached - this is business."
                                        elif is_student:
                                            selected_girl.character "500? Oh my god, that's so much! Okay, yeah, you can fuck me without a condom for that! Thank you!"
                                        else:
                                            selected_girl.character "500 for bareback access? Deal. Just don't get too attached - this is a business arrangement."
                                    else:
                                        $ selected_girl.previous_condoms_reaction = "negative"
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time with empty promises. Come back when you can actually pay."
                                        elif is_student:
                                            selected_girl.character "Oh... you don't have enough? That's okay... maybe some other time?"
                                        else:
                                            selected_girl.character "Don't waste my time with empty promises. Come back when you can actually pay."
                                        $ selected_girl.apply_impacts({"affection": -25})
                                
                                "Leave it be.":
                                    $ selected_girl.previous_condoms_reaction = "negative"
                                    if is_base_mother:
                                        selected_girl.character "Suit yourself. An experienced mother's bare pussy stays on lockdown until you learn how negotiations work."
                                    elif is_student:
                                        selected_girl.character "Oh... okay. Well, if you change your mind about cash, just let me know, I guess?"
                                    else:
                                        selected_girl.character "Suit yourself. My bare pussy stays on lockdown until you learn how negotiations work."
                                    $ selected_girl.apply_impacts({"affection": -10})
                        
                        elif selected_girl.dominant_approach == "dominate":
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 30, "affection": 30})
                            if is_base_mother:
                                selected_girl.character "If that's what you want, Professor... as an experienced mother, I'll let you fuck my bare pussy."
                            elif is_student:
                                selected_girl.character "If that's what you want, Professor... okay, I'll let you fuck me without a condom."
                            else:
                                selected_girl.character "If that's what you want, Professor... I'll let you fuck my bare pussy."
            
            else:
                # She doesn't want condoms
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I feel so connected to you. As an experienced mother, I want to feel your bare cock sliding into my pussy - my body already knows how to handle children."
                    elif is_student:
                        selected_girl.character "I feel so connected to you. I want to feel your bare cock inside me... it feels more intimate without anything between us, you know?"
                    else:
                        selected_girl.character "I feel so connected to you. I want to feel your bare cock sliding into my pussy, nothing between us when we make love."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "The way you look at me is so hot. As an experienced woman, I want to feel your raw cock stretching my pussy open - motherhood hasn't dulled my desires at all."
                    elif is_student:
                        selected_girl.character "The way you look at me is so hot! I want to feel your bare cock inside me... I've never done it without a condom before, that sounds so exciting!"
                    else:
                        selected_girl.character "The way you look at me is so hot. I want to feel your raw cock stretching my pussy open, no barriers."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "What's in it for me? Bareback pussy access from an experienced mother? That's premium pricing, Professor - I know exactly what I'm offering."
                    elif is_student:
                        selected_girl.character "What's in it for me? Bareback...? Is that more expensive? I don't really know what to charge for that... what do you think is fair?"
                    else:
                        selected_girl.character "What's in it for me? Bareback pussy access? That's premium pricing, Professor."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "You're in charge, Professor. As an experienced mother, if you want to fuck my bare pussy with no condom, I won't stop you - my body knows how to handle this."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want to fuck me without a condom... okay, I'll let you. Whatever you want."
                    else:
                        selected_girl.character "You're in charge, Professor. If you want to fuck my bare pussy with no condom, I won't stop you."
                
                $ selected_girl.previous_condoms_reaction = "positive"
                
                # Player can try to convince her to use condoms
                menu:
                    "I respect your choice. We'll go bare for vaginal.": 
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "Thank you for understanding, Professor. As an experienced mother, I love that you want to feel me completely."
                            elif is_student:
                                selected_girl.character "Thank you for understanding, Professor! I love that you want to feel me completely!"
                            else:
                                selected_girl.character "Thank you for understanding, Professor. I love that you want to feel me completely."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "Mmm... I love a man who appreciates bare pussy. As an experienced woman, you won't regret this."
                            elif is_student:
                                selected_girl.character "Mmm... I love a man who appreciates bare pussy! You won't regret this!"
                            else:
                                selected_girl.character "Mmm... I love a man who appreciates bare pussy. You won't regret this."
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Good choice. As an experienced mother, bare access is the premium experience - you're getting your money's worth."
                            elif is_student:
                                selected_girl.character "Good choice! Bare access is the best experience!"
                            else:
                                selected_girl.character "Good choice. Bare access is the premium experience."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "As you wish, Professor. As an experienced mother, my bare pussy is yours to command."
                            elif is_student:
                                selected_girl.character "As you wish, Professor. My bare pussy is yours to command."
                            else:
                                selected_girl.character "As you wish, Professor. My bare pussy is yours to command."
                        
                        $ selected_girl.apply_impacts({"affection": 50, "corruption": 25})
                    
                    "But shouldn't we be more careful? We should use condoms.": 
                        # Try to convince her to use condoms
                        if selected_girl.dominant_approach == "compassionate":
                            if selected_girl.baby_desire < 30:
                                $ selected_girl.wants_vaginal_condom = True
                                $ selected_girl.previous_condoms_reaction = "positive"
                                $ selected_girl.apply_impacts({"discipline": 50, "fear": -25})
                                if is_base_mother:
                                    selected_girl.character "You're right... as an experienced mother, I should be more careful. We'll use condoms for vaginal."
                                elif is_student:
                                    selected_girl.character "You're right... I should be more careful. We'll use condoms for vaginal."
                                else:
                                    selected_girl.character "You're right... I should be more careful. We'll use condoms for vaginal."
                            else:
                                $ selected_girl.previous_condoms_reaction = "negative"
                                if is_base_mother:
                                    selected_girl.character "I know you're worried, Professor, but as an experienced mother, I want to feel you completely."
                                elif is_student:
                                    selected_girl.character "I know you're worried, Professor, but I want to feel you completely."
                                else:
                                    selected_girl.character "I know you're worried, Professor, but I want to feel you completely."
                                $ selected_girl.apply_impacts({"affection": -15})
                        
                        elif selected_girl.dominant_approach == "sexualized":
                            $ selected_girl.previous_condoms_reaction = "negative"
                            if is_base_mother:
                                selected_girl.character "Why would we want that? As an experienced woman, bare sex is so much hotter!"
                            elif is_student:
                                selected_girl.character "Why would we want that? Bare sex is so much hotter!"
                            else:
                                selected_girl.character "Why would we want that? Bare sex is so much hotter!"
                            $ selected_girl.apply_impacts({"affection": -20})
                        
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "You want me to start using condoms? As an experienced woman, that would be a downgrade in service. You'll need to pay extra for that."
                            
                            menu:
                                "Offer 300 cash for me to use condoms?":
                                    if player.cash >= 300:
                                        $ player.cash -= 300
                                        $ selected_girl.cash += 300
                                        $ selected_girl.wants_vaginal_condom = True
                                        $ selected_girl.previous_condoms_reaction = "positive"
                                        $ selected_girl.apply_impacts({"discipline": 30, "corruption": 20})
                                        if is_base_mother:
                                            selected_girl.character "300 for me to use condoms? As an experienced mother, that's insulting but I'll take it. Fine, we'll use protection."
                                        elif is_student:
                                            selected_girl.character "300 for me to use condoms? That's weird but okay! We'll use condoms!"
                                        else:
                                            selected_girl.character "300 for me to use condoms? That's insulting but I'll take it. Fine, we'll use protection."
                                    else:
                                        $ selected_girl.previous_condoms_reaction = "negative"
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time. If you want me to downgrade to condoms, you'll need to pay more."
                                        elif is_student:
                                            selected_girl.character "You don't have enough? Then we're not using condoms."
                                        else:
                                            selected_girl.character "Don't waste my time. If you want me to downgrade to condoms, you'll need to pay more."
                                        $ selected_girl.apply_impacts({"affection": -25})
                                
                                "Leave it be.":
                                    $ selected_girl.previous_condoms_reaction = "negative"
                                    if is_base_mother:
                                        selected_girl.character "Smart choice. As an experienced woman, bare access is the premium experience you're paying for."
                                    elif is_student:
                                        selected_girl.character "Okay! We'll keep going bare then!"
                                    else:
                                        selected_girl.character "Smart choice. Bare access is the premium experience you're paying for."
                                    $ selected_girl.apply_impacts({"affection": -5})
                        
                        elif selected_girl.dominant_approach == "dominate":
                            $ selected_girl.previous_condoms_reaction = "negative"
                            if is_base_mother:
                                selected_girl.character "I prefer bare intimacy, Professor. As an experienced mother, my body is prepared for this."
                            elif is_student:
                                selected_girl.character "I prefer bare intimacy, Professor. I'm prepared for this."
                            else:
                                selected_girl.character "I prefer bare intimacy, Professor. I'm prepared for this."
                            $ selected_girl.apply_impacts({"affection": -15})

        "What about for anal sex?":
            $ selected_girl.player_knows_anal_condom = True
            
            # Similar structure for anal condoms
            if selected_girl.wants_anal_condom:
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
                        selected_girl.character "The way you look at me is so hot... but as an experienced woman, I need to be careful. Watching you roll a condom over your hard cock before taking my ass shows you respect my health."
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
                        selected_girl.character "You're in charge, Professor. As an experienced mother, if you want to wrap your cock before entering my ass, I'll accept it - I must protect my family."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want to use a condom for anal... I'll do what you want."
                    else:
                        selected_girl.character "You're in charge, Professor. If you want to wrap your cock before entering my ass, I'll accept it."
                
                # Player choices to convince her
                menu:
                    "I respect your boundaries. We'll always use condoms for anal.": 
                        $ selected_girl.previous_condoms_reaction = "positive"
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "Thank you for understanding. As an experienced mother, I appreciate you respecting my health concerns. It makes me feel even more connected to you."
                            elif is_student:
                                selected_girl.character "Thank you for understanding! That makes me feel so much better about... you know, anal. I'm glad you're being so responsible with me."
                            else:
                                selected_girl.character "Thank you for understanding. Knowing you'll protect my ass makes me feel even more connected to you."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "Mmm... a gentleman who respects an experienced woman's anal boundaries. That's unexpectedly hot. I like that."
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
                                selected_girl.character "Thank you, Professor. As an experienced mother, your consideration for my ass and my family means everything to me."
                            elif is_student:
                                selected_girl.character "Thank you, Professor! I'm glad you're being so thoughtful about... about my ass."
                            else:
                                selected_girl.character "Thank you, Professor. Your consideration for my ass means everything to me."
                        
                        $ selected_girl.apply_impacts({"affection": 50, "fear": -50})
                    
                    "Would you consider letting me fuck your bare ass sometimes?":
                        # Try to convince her for bare anal
                        if selected_girl.dominant_approach == "compassionate":
                            $ selected_girl.wants_anal_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 30, "affection": 30})
                            if is_base_mother:
                                selected_girl.character "I trust you completely, Professor. As an experienced mother, let's feel each other without anything between us... even there."
                            elif is_student:
                                selected_girl.character "I trust you, Professor. I want to feel you without anything between us... even in my ass. That sounds really intimate."
                            else:
                                selected_girl.character "I trust you completely. Let's feel each other without anything between us... even there."
                        
                        elif selected_girl.dominant_approach == "sexualized":
                            $ selected_girl.wants_anal_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 50, "affection": 25})
                            if is_base_mother:
                                selected_girl.character "Mmm... bareback fucking my ass? As an experienced woman, I've been wanting you to ask. Take my bare ass, Professor."
                            elif is_student:
                                selected_girl.character "Mmm... bareback anal? Like... without a condom? I've never done that before! But... okay, yeah, I want to try! Take my bare ass!"
                            else:
                                selected_girl.character "Mmm... bareback fucking my ass? I've been wanting you to ask. Take my bare ass."
                        
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "Bare ass access? That's a premium service, Professor. What are you offering?"
                            
                            menu:
                                "Offer 400 cash for bareback anal?":
                                    if player.cash >= 400:
                                        $ player.cash -= 400
                                        $ selected_girl.cash += 400
                                        $ selected_girl.wants_anal_condom = False
                                        $ selected_girl.previous_condoms_reaction = "positive"
                                        $ selected_girl.apply_impacts({"corruption": 40, "affection": 10})
                                        if is_base_mother:
                                            selected_girl.character "400 for bareback anal? As an experienced mother, I know that's fair. Deal. Just don't get too attached - this is business."
                                        elif is_student:
                                            selected_girl.character "400? Oh my god, that's so much! Okay, yeah, you can fuck my ass without a condom for that! Thank you!"
                                        else:
                                            selected_girl.character "400 for bareback anal? Deal. Just don't get too attached - this is a business arrangement."
                                    else:
                                        $ selected_girl.previous_condoms_reaction = "negative"
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time with empty promises. Come back when you can actually pay."
                                        elif is_student:
                                            selected_girl.character "Oh... you don't have enough? That's okay... maybe some other time?"
                                        else:
                                            selected_girl.character "Don't waste my time with empty promises. Come back when you can actually pay."
                                        $ selected_girl.apply_impacts({"affection": -25})
                                
                                "Leave it be.":
                                    $ selected_girl.previous_condoms_reaction = "negative"
                                    if is_base_mother:
                                        selected_girl.character "Suit yourself. An experienced mother's bare ass stays on lockdown until you learn how negotiations work."
                                    elif is_student:
                                        selected_girl.character "Oh... okay. Well, if you change your mind about cash, just let me know, I guess?"
                                    else:
                                        selected_girl.character "Suit yourself. My bare ass stays on lockdown until you learn how negotiations work."
                                    $ selected_girl.apply_impacts({"affection": -10})
                        
                        elif selected_girl.dominant_approach == "dominate":
                            $ selected_girl.wants_anal_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 30, "affection": 30})
                            if is_base_mother:
                                selected_girl.character "If that's what you want, Professor... as an experienced mother, I'll let you fuck my bare ass."
                            elif is_student:
                                selected_girl.character "If that's what you want, Professor... okay, I'll let you fuck my ass without a condom."
                            else:
                                selected_girl.character "If that's what you want, Professor... I'll let you fuck my bare ass."
            
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
                        selected_girl.character "You're in charge, Professor. As an experienced mother, if you want to fuck my bare ass with no condom, I won't stop you - my body knows how to handle this."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want to fuck my ass without a condom... okay, I'll let you. Whatever you want."
                    else:
                        selected_girl.character "You're in charge, Professor. If you want to fuck my bare ass with no condom, I won't stop you."
                $ selected_girl.previous_condoms_reaction = "positive"
                
                # Player can try to convince her to use condoms
                menu:
                    "I respect your choice. We'll go bare for anal.": 
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "Thank you for understanding, Professor. As an experienced mother, I love that you want to feel me completely, even there."
                            elif is_student:
                                selected_girl.character "Thank you for understanding, Professor! I love that you want to feel me completely, even there!"
                            else:
                                selected_girl.character "Thank you for understanding, Professor. I love that you want to feel me completely, even there."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "Mmm... I love a man who appreciates bare anal. As an experienced woman, you won't regret this."
                            elif is_student:
                                selected_girl.character "Mmm... I love a man who appreciates bare anal! You won't regret this!"
                            else:
                                selected_girl.character "Mmm... I love a man who appreciates bare anal. You won't regret this."
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Good choice. As an experienced mother, bare anal is the premium experience - you're getting your money's worth."
                            elif is_student:
                                selected_girl.character "Good choice! Bare anal is the best experience!"
                            else:
                                selected_girl.character "Good choice. Bare anal is the premium experience."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "As you wish, Professor. As an experienced mother, my bare ass is yours to command."
                            elif is_student:
                                selected_girl.character "As you wish, Professor. My bare ass is yours to command."
                            else:
                                selected_girl.character "As you wish, Professor. My bare ass is yours to command."
                        
                        $ selected_girl.apply_impacts({"affection": 50, "corruption": 25})
                    
                    "But shouldn't we be more careful? We should use condoms for anal.": 
                        # Try to convince her to use condoms
                        if selected_girl.dominant_approach == "compassionate":
                            if selected_girl.fear > 60:
                                $ selected_girl.wants_anal_condom = True
                                $ selected_girl.previous_condoms_reaction = "positive"
                                $ selected_girl.apply_impacts({"discipline": 50, "fear": -25})
                                if is_base_mother:
                                    selected_girl.character "You're right... as an experienced mother, I should be more careful about my health. We'll use condoms for anal."
                                elif is_student:
                                    selected_girl.character "You're right... I should be more careful. We'll use condoms for anal."
                                else:
                                    selected_girl.character "You're right... I should be more careful. We'll use condoms for anal."
                            else:
                                $ selected_girl.previous_condoms_reaction = "negative"
                                if is_base_mother:
                                    selected_girl.character "I know you're worried, Professor, but as an experienced mother, I want to feel you completely."
                                elif is_student:
                                    selected_girl.character "I know you're worried, Professor, but I want to feel you completely."
                                else:
                                    selected_girl.character "I know you're worried, Professor, but I want to feel you completely."
                                $ selected_girl.apply_impacts({"affection": -15})
                        
                        elif selected_girl.dominant_approach == "sexualized":
                            $ selected_girl.previous_condoms_reaction = "negative"
                            if is_base_mother:
                                selected_girl.character "Why would we want that? As an experienced woman, bare anal is so much more intense!"
                            elif is_student:
                                selected_girl.character "Why would we want that? Bare anal is so much more intense!"
                            else:
                                selected_girl.character "Why would we want that? Bare anal is so much more intense!"
                            $ selected_girl.apply_impacts({"affection": -20})
                        
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "You want me to start using condoms for anal? As an experienced woman, that would be a downgrade in service. You'll need to pay extra for that."
                            
                            menu:
                                "Offer 300 cash for me to use condoms for anal?":
                                    if player.cash >= 300:
                                        $ player.cash -= 300
                                        $ selected_girl.cash += 300
                                        $ selected_girl.wants_anal_condom = True
                                        $ selected_girl.previous_condoms_reaction = "positive"
                                        $ selected_girl.apply_impacts({"discipline": 30, "corruption": 20})
                                        if is_base_mother:
                                            selected_girl.character "300 for me to use condoms for anal? As an experienced mother, that's insulting but I'll take it. Fine, we'll use protection."
                                        elif is_student:
                                            selected_girl.character "300 for me to use condoms for anal? That's weird but okay! We'll use condoms!"
                                        else:
                                            selected_girl.character "300 for me to use condoms for anal? That's insulting but I'll take it. Fine, we'll use protection."
                                    else:
                                        $ selected_girl.previous_condoms_reaction = "negative"
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time. If you want me to downgrade to condoms, you'll need to pay more."
                                        elif is_student:
                                            selected_girl.character "You don't have enough? Then we're not using condoms."
                                        else:
                                            selected_girl.character "Don't waste my time. If you want me to downgrade to condoms, you'll need to pay more."
                                        $ selected_girl.apply_impacts({"affection": -25})
                                
                                "Leave it be.":
                                    $ selected_girl.previous_condoms_reaction = "negative"
                                    if is_base_mother:
                                        selected_girl.character "Smart choice. As an experienced woman, bare anal is the premium experience you're paying for."
                                    elif is_student:
                                        selected_girl.character "Okay! We'll keep going bare for anal then!"
                                    else:
                                        selected_girl.character "Smart choice. Bare anal is the premium experience you're paying for."
                                    $ selected_girl.apply_impacts({"affection": -5})
                        
                        elif selected_girl.dominant_approach == "dominate":
                            $ selected_girl.previous_condoms_reaction = "negative"
                            if is_base_mother:
                                selected_girl.character "I prefer bare intimacy, Professor. As an experienced mother, my body is prepared for this."
                            elif is_student:
                                selected_girl.character "I prefer bare intimacy, Professor. I'm prepared for this."
                            else:
                                selected_girl.character "I prefer bare intimacy, Professor. I'm prepared for this."
                            $ selected_girl.apply_impacts({"affection": -15})


        "And for oral sex?":
            $ selected_girl.player_knows_oral_condom = True
            
            # Similar structure for oral condoms
            if selected_girl.wants_oral_condom:
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
                        selected_girl.character "The way you look at me is so hot... but as an experienced woman, I need to be careful. Using protection when I suck your cock shows you respect my health situation."
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
                        selected_girl.character "You're in charge, Professor. As an experienced mother, if you want to use protection when I suck your cock, I'll accept it - I must stay healthy for my family."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want to use protection for oral... I'll do what you want."
                    else:
                        selected_girl.character "You're in charge, Professor. If you want to use protection when I suck your cock, I'll accept it."
                
                # Player choices to convince her
                menu:
                    "I respect your boundaries. We'll always use protection for oral.": 
                        $ selected_girl.previous_condoms_reaction = "positive"
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "Thank you for understanding. As an experienced mother, I appreciate you respecting my health concerns. It makes me feel even more connected to you."
                            elif is_student:
                                selected_girl.character "Thank you for understanding! That makes me feel so much better about... you know, oral. I'm glad you're being so responsible with me."
                            else:
                                selected_girl.character "Thank you for understanding. Knowing you'll protect my health makes me feel even more connected to you."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "Mmm... a gentleman who respects an experienced woman's oral boundaries. That's unexpectedly hot. I like that."
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
                                selected_girl.character "Thank you, Professor. As an experienced mother, your consideration for my health and my family means everything to me."
                            elif is_student:
                                selected_girl.character "Thank you, Professor! I'm glad you're being so thoughtful about... about my health."
                            else:
                                selected_girl.character "Thank you, Professor. Your consideration for my health means everything to me."
                        
                        $ selected_girl.apply_impacts({"affection": 50, "fear": -50})
                    
                    "Would you consider letting me cum in your mouth without protection sometimes?":
                        # Try to convince her for bare oral
                        if selected_girl.dominant_approach == "compassionate":
                            $ selected_girl.wants_oral_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 25, "affection": 30})
                            if is_base_mother:
                                selected_girl.character "I trust you completely, Professor. As an experienced mother, let me taste you without anything between us."
                            elif is_student:
                                selected_girl.character "I trust you, Professor. I want to taste you without anything between us... that sounds really intimate."
                            else:
                                selected_girl.character "I trust you completely. Let me taste you without anything between us."
                        
                        elif selected_girl.dominant_approach == "sexualized":
                            $ selected_girl.wants_oral_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 40, "affection": 25})
                            if is_base_mother:
                                selected_girl.character "Mmm... cumming in my bare mouth? As an experienced woman, I've been wanting you to ask. I want to taste you."
                            elif is_student:
                                selected_girl.character "Mmm... cumming in my mouth without protection? Like... bare? I've never done that before! But... okay, yeah, I want to taste you!"
                            else:
                                selected_girl.character "Mmm... cumming in my bare mouth? I've been wanting you to ask. I want to taste you."
                        
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "Bare cock in my mouth? That's a premium service, Professor. What are you offering?"
                            
                            menu:
                                "Offer 300 cash for bare oral?":
                                    if player.cash >= 300:
                                        $ player.cash -= 300
                                        $ selected_girl.cash += 300
                                        $ selected_girl.wants_oral_condom = False
                                        $ selected_girl.previous_condoms_reaction = "positive"
                                        $ selected_girl.apply_impacts({"corruption": 35, "affection": 10})
                                        if is_base_mother:
                                            selected_girl.character "300 for bare oral? As an experienced mother, I know that's fair. Deal. Just don't get too attached - this is business."
                                        elif is_student:
                                            selected_girl.character "300? Oh my god, that's so much! Okay, yeah, you can cum in my mouth without protection for that! Thank you!"
                                        else:
                                            selected_girl.character "300 for bare oral? Deal. Just don't get too attached - this is a business arrangement."
                                    else:
                                        $ selected_girl.previous_condoms_reaction = "negative"
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time with empty promises. Come back when you can actually pay."
                                        elif is_student:
                                            selected_girl.character "Oh... you don't have enough? That's okay... maybe some other time?"
                                        else:
                                            selected_girl.character "Don't waste my time with empty promises. Come back when you can actually pay."
                                        $ selected_girl.apply_impacts({"affection": -25})
                                
                                "Leave it be.":
                                    $ selected_girl.previous_condoms_reaction = "negative"
                                    if is_base_mother:
                                        selected_girl.character "Suit yourself. An experienced mother's mouth stays on lockdown until you learn how negotiations work."
                                    elif is_student:
                                        selected_girl.character "Oh... okay. Well, if you change your mind about cash, just let me know, I guess?"
                                    else:
                                        selected_girl.character "Suit yourself. My mouth stays on lockdown until you learn how negotiations work."
                                    $ selected_girl.apply_impacts({"affection": -10})
                        
                        elif selected_girl.dominant_approach == "dominate":
                            $ selected_girl.wants_oral_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 25, "affection": 30})
                            if is_base_mother:
                                selected_girl.character "If that's what you want, Professor... as an experienced mother, I'll let you cum in my bare mouth."
                            elif is_student:
                                selected_girl.character "If that's what you want, Professor... okay, I'll let you cum in my mouth without protection."
                            else:
                                selected_girl.character "If that's what you want, Professor... I'll let you cum in my bare mouth."
            
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
                        selected_girl.character "What's in it for me? Bare oral? Is that more expensive? I don't really know what to charge for that... what do you think is fair?"
                    else:
                        selected_girl.character "What's in it for me? Bare cock in my mouth? That's premium pricing, Professor."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "You're in charge, Professor. As an experienced mother, if you want me to suck your bare cock with no protection, I won't stop you - my mouth is yours to command."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want me to suck your cock without a condom... okay, I'll do it. Whatever you want."
                    else:
                        selected_girl.character "You're in charge, Professor. If you want me to suck your bare cock with no protection, I won't stop you."
                
                $ selected_girl.previous_condoms_reaction = "positive"
                
                # Player can try to convince her to use protection
                menu:
                    "I respect your choice. We'll go bare for oral.": 
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "Thank you for understanding, Professor. As an experienced mother, I love that you want to share this intimacy with me."
                            elif is_student:
                                selected_girl.character "Thank you for understanding, Professor! I love that you want to share this intimacy with me!"
                            else:
                                selected_girl.character "Thank you for understanding, Professor. I love that you want to share this intimacy with me."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "Mmm... I love a man who appreciates bare oral. As an experienced woman, you won't regret this."
                            elif is_student:
                                selected_girl.character "Mmm... I love a man who appreciates bare oral! You won't regret this!"
                            else:
                                selected_girl.character "Mmm... I love a man who appreciates bare oral. You won't regret this."
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Good choice. As an experienced mother, bare oral is the premium experience - you're getting your money's worth."
                            elif is_student:
                                selected_girl.character "Good choice! Bare oral is the best experience!"
                            else:
                                selected_girl.character "Good choice. Bare oral is the premium experience."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "As you wish, Professor. As an experienced mother, my mouth is yours to command."
                            elif is_student:
                                selected_girl.character "As you wish, Professor. My mouth is yours to command."
                            else:
                                selected_girl.character "As you wish, Professor. My mouth is yours to command."
                        
                        $ selected_girl.apply_impacts({"affection": 50, "corruption": 25})
                    
                    "But shouldn't we be more careful? We should use protection for oral.": 
                        # Try to convince her to use protection
                        if selected_girl.dominant_approach == "compassionate":
                            if selected_girl.fear > 60:
                                $ selected_girl.wants_oral_condom = True
                                $ selected_girl.previous_condoms_reaction = "positive"
                                $ selected_girl.apply_impacts({"discipline": 50, "fear": -25})
                                if is_base_mother:
                                    selected_girl.character "You're right... as an experienced mother, I should be more careful about oral health. We'll use protection."
                                elif is_student:
                                    selected_girl.character "You're right... I should be more careful. We'll use protection."
                                else:
                                    selected_girl.character "You're right... I should be more careful. We'll use protection."
                            else:
                                $ selected_girl.previous_condoms_reaction = "negative"
                                if is_base_mother:
                                    selected_girl.character "I know you're worried, Professor, but as an experienced mother, I want to share this intimacy with you."
                                elif is_student:
                                    selected_girl.character "I know you're worried, Professor, but I want to share this intimacy with you."
                                else:
                                    selected_girl.character "I know you're worried, Professor, but I want to share this intimacy with you."
                                $ selected_girl.apply_impacts({"affection": -15})
                        
                        elif selected_girl.dominant_approach == "sexualized":
                            $ selected_girl.previous_condoms_reaction = "negative"
                            if is_base_mother:
                                selected_girl.character "Why would we want that? As an experienced woman, tasting you directly is so much more intimate!"
                            elif is_student:
                                selected_girl.character "Why would we want that? Tasting you directly is so much more intimate!"
                            else:
                                selected_girl.character "Why would we want that? Tasting you directly is so much more intimate!"
                            $ selected_girl.apply_impacts({"affection": -20})
                        
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "You want me to start using protection for oral? As an experienced woman, that would be a downgrade in service. You'll need to pay extra for that."
                            
                            menu:
                                "Offer 200 cash for me to use protection for oral?":
                                    if player.cash >= 200:
                                        $ player.cash -= 200
                                        $ selected_girl.cash += 200
                                        $ selected_girl.wants_oral_condom = True
                                        $ selected_girl.previous_condoms_reaction = "positive"
                                        $ selected_girl.apply_impacts({"discipline": 30, "corruption": 20})
                                        if is_base_mother:
                                            selected_girl.character "200 for me to use protection for oral? As an experienced mother, that's insulting but I'll take it. Fine, we'll use protection."
                                        elif is_student:
                                            selected_girl.character "200 for me to use protection for oral? That's weird but okay! We'll use protection!"
                                        else:
                                            selected_girl.character "200 for me to use protection for oral? That's insulting but I'll take it. Fine, we'll use protection."
                                    else:
                                        $ selected_girl.previous_condoms_reaction = "negative"
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time. If you want me to downgrade to protection, you'll need to pay more."
                                        elif is_student:
                                            selected_girl.character "You don't have enough? Then we're not using protection."
                                        else:
                                            selected_girl.character "Don't waste my time. If you want me to downgrade to protection, you'll need to pay more."
                                        $ selected_girl.apply_impacts({"affection": -25})
                                
                                "Leave it be.":
                                    $ selected_girl.previous_condoms_reaction = "negative"
                                    if is_base_mother:
                                        selected_girl.character "Smart choice. As an experienced woman, bare oral is the premium experience you're paying for."
                                    elif is_student:
                                        selected_girl.character "Okay! We'll keep going bare for oral then!"
                                    else:
                                        selected_girl.character "Smart choice. Bare oral is the premium experience you're paying for."
                                    $ selected_girl.apply_impacts({"affection": -5})
                        
                        elif selected_girl.dominant_approach == "dominate":
                            $ selected_girl.previous_condoms_reaction = "negative"
                            if is_base_mother:
                                selected_girl.character "I prefer bare intimacy, Professor. As an experienced mother, I'm prepared for this."
                            elif is_student:
                                selected_girl.character "I prefer bare intimacy, Professor. I'm prepared for this."
                            else:
                                selected_girl.character "I prefer bare intimacy, Professor. I'm prepared for this."
                            $ selected_girl.apply_impacts({"affection": -15})


        "What about for body shots or other external ejaculation?":
            $ selected_girl.player_knows_body_condom = True
            
            # Similar structure for body condoms
            if selected_girl.wants_body_condom:
                # She wants condoms for body shots
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I feel so connected to you, but as an experienced mother, I prefer using condoms even for body shots. It keeps things cleaner and more controlled for my family life."
                    elif is_student:
                        selected_girl.character "I feel so connected to you, but I'm kind of messy... I think I prefer condoms for body shots. It keeps things cleaner and less awkward."
                    else:
                        selected_girl.character "I feel so connected to you, but I prefer using condoms even for body shots. It keeps things cleaner and more controlled."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "The way you look at me is so hot... but as an experienced woman, I need to be careful. Using condoms for body shots shows you respect my practical needs."
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
                        selected_girl.character "You're in charge, Professor. As an experienced mother, if you want to use condoms for body shots, I'll accept it - I must be careful as a mother."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want to use condoms for body shots... I'll do what you want."
                    else:
                        selected_girl.character "You're in charge, Professor. If you want to use condoms for body shots, I'll accept it."
                
                # Player choices to convince her
                menu:
                    "I respect your boundaries. We'll always use condoms for body shots.": 
                        $ selected_girl.previous_condoms_reaction = "positive"
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
                                selected_girl.character "Yes, Professor. Being clean and controlled is the right choice for an experienced mother."
                            elif is_student:
                                selected_girl.character "Yes, Professor. Being clean and controlled is what you want - I'll remember that."
                            else:
                                selected_girl.character "Yes, Professor. Being clean and controlled is what you want."
                        
                        $ selected_girl.apply_impacts({"discipline": 50, "affection": 20})
                    
                    "I love the idea of my cum on your bare skin...":
                        # Try to convince her for bare body shots
                        if selected_girl.dominant_approach == "sexualized":
                            $ selected_girl.wants_body_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 40, "affection": 20})
                            if is_base_mother:
                                selected_girl.character "Mmm... marking my body with your cum? As an experienced woman, that's so hot. Do it - even mothers need to feel desired and marked."
                            elif is_student:
                                selected_girl.character "Mmm... marking my body with your cum? That's so hot! I've never done that before! Do it - mark me with your cum!"
                            else:
                                selected_girl.character "Mmm... marking my body with your cum? That's so hot. Do it."
                        
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "Marking my bare body with your cum? That's a premium service, Professor. What are you offering?"
                            
                            menu:
                                "Offer 300 cash for body marking?":
                                    if player.cash >= 300:
                                        $ player.cash -= 300
                                        $ selected_girl.cash += 300
                                        $ selected_girl.wants_body_condom = False
                                        $ selected_girl.previous_condoms_reaction = "positive"
                                        $ selected_girl.apply_impacts({"corruption": 35, "affection": 10})
                                        if is_base_mother:
                                            selected_girl.character "300 for body marking privileges? As an experienced mother, I know that's fair. Fine, just don't get any crazy ideas - I'm still a mother."
                                        elif is_student:
                                            selected_girl.character "300? Oh my god, that's so much! Okay, yeah, you can mark my body with your cum for that! Thank you!"
                                        else:
                                            selected_girl.character "300 for body marking privileges? Deal. Just don't get too attached - this is business."
                                    else:
                                        $ selected_girl.previous_condoms_reaction = "negative"
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time with empty promises. Come back when you can actually pay."
                                        elif is_student:
                                            selected_girl.character "Oh... you don't have enough? That's okay... maybe some other time?"
                                        else:
                                            selected_girl.character "Don't waste my time with empty promises. Come back when you can actually pay."
                                        $ selected_girl.apply_impacts({"affection": -20})
                                
                                "Leave it be.":
                                    $ selected_girl.previous_condoms_reaction = "negative"
                                    if is_base_mother:
                                        selected_girl.character "Suit yourself. An experienced mother's bare skin stays off-limits until you learn how negotiations work."
                                    elif is_student:
                                        selected_girl.character "Oh... okay. Well, if you change your mind about cash, just let me know, I guess?"
                                    else:
                                        selected_girl.character "Suit yourself. My bare skin stays off-limits until you learn how negotiations work."
                                    $ selected_girl.apply_impacts({"affection": -10})
                        
                        elif selected_girl.dominant_approach in ["compassionate", "dominate"]:
                            $ selected_girl.wants_body_condom = False
                            $ selected_girl.previous_condoms_reaction = "positive"
                            $ selected_girl.apply_impacts({"corruption": 25, "affection": 25})
                            
                            if selected_girl.dominant_approach == "compassionate":
                                if is_base_mother:
                                    selected_girl.character "I trust you completely, Professor. As an experienced mother, let me give you this intimacy - mark my bare skin if it pleases you."
                                elif is_student:
                                    selected_girl.character "I trust you, Professor. I want to feel your cum on my bare skin... that sounds really intimate and special."
                                else:
                                    selected_girl.character "I trust you completely. Let me give you this intimacy - mark my bare skin if it pleases you."
                            else:
                                if is_base_mother:
                                    selected_girl.character "If that's what you want, Professor... as an experienced mother, I'll let you mark my bare body."
                                elif is_student:
                                    selected_girl.character "If that's what you want, Professor... okay, I'll let you cum on my bare body."
                                else:
                                    selected_girl.character "If that's what you want, Professor... I'll let you mark my bare body."
                        
                        else:
                            $ selected_girl.previous_condoms_reaction = "negative"
                            if is_base_mother:
                                selected_girl.character "That's inappropriate to say, Professor. As a mother, I need to maintain certain standards for my family."
                            elif is_student:
                                selected_girl.character "That's inappropriate to say, Professor... I'm not comfortable with that kind of talk."
                            else:
                                selected_girl.character "That's inappropriate to say, Professor."
                            $ selected_girl.apply_impacts({"affection": -15, "fear": 20})
            
            else:
                # She doesn't want condoms for body shots
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I feel so connected to you, but as an experienced mother, I prefer keeping things clean and controlled for my family life."
                    elif is_student:
                        selected_girl.character "I feel so connected to you, but I'm kind of messy... I think I prefer keeping things clean and controlled."
                    else:
                        selected_girl.character "I feel so connected to you, but I prefer keeping things clean and controlled."
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "The way you look at me is so hot... but as an experienced woman, I need to be careful about getting cum everywhere while caring for my family."
                    elif is_student:
                        selected_girl.character "The way you look at me is so hot... but I'm kind of worried about getting cum everywhere. That might be messy..."
                    else:
                        selected_girl.character "The way you look at me is so hot... but I'm kind of worried about getting cum everywhere."
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "What's in it for me? As an experienced mother, clean body shots cost extra - I have to maintain certain standards for my family."
                    elif is_student:
                        selected_girl.character "What's in it for me? Clean body shots... um, does that cost extra? I'm not sure about the pricing for that..."
                    else:
                        selected_girl.character "What's in it for me? Clean body shots cost extra... unless you make it worth my time."
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "You're in charge, Professor. As an experienced mother, if you want clean body shots, I'll accept it - I must be careful as a mother."
                    elif is_student:
                        selected_girl.character "You're in charge, Professor. If you want clean body shots... I'll do what you want."
                    else:
                        selected_girl.character "You're in charge, Professor. If you want clean body shots, I'll accept it."
                
                $ selected_girl.previous_condoms_reaction = "positive"
                
                # Player can try to convince her to use condoms
                menu:
                    "I respect your choice. We'll go bare for body shots.": 
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "Thank you for understanding, Professor. As an experienced mother, I love that you want to share this intimacy with me."
                            elif is_student:
                                selected_girl.character "Thank you for understanding, Professor! I love that you want to share this intimacy with me!"
                            else:
                                selected_girl.character "Thank you for understanding, Professor. I love that you want to share this intimacy with me."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "Mmm... I love a man who appreciates marking my body. As an experienced woman, you won't regret this."
                            elif is_student:
                                selected_girl.character "Mmm... I love a man who appreciates marking my body! You won't regret this!"
                            else:
                                selected_girl.character "Mmm... I love a man who appreciates marking my body. You won't regret this."
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Good choice. As an experienced mother, bare body marking is the premium experience - you're getting your money's worth."
                            elif is_student:
                                selected_girl.character "Good choice! Bare body marking is the best experience!"
                            else:
                                selected_girl.character "Good choice. Bare body marking is the premium experience."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "As you wish, Professor. As an experienced mother, my body is yours to mark."
                            elif is_student:
                                selected_girl.character "As you wish, Professor. My body is yours to mark."
                            else:
                                selected_girl.character "As you wish, Professor. My body is yours to mark."
                        
                        $ selected_girl.apply_impacts({"affection": 50, "corruption": 25})
                    
                    "But shouldn't we be more careful? We should use condoms for body shots.": 
                        # Try to convince her to use condoms
                        if selected_girl.dominant_approach == "compassionate":
                            if selected_girl.fear > 60:
                                $ selected_girl.wants_body_condom = True
                                $ selected_girl.previous_condoms_reaction = "positive"
                                $ selected_girl.apply_impacts({"discipline": 50, "fear": -25})
                                if is_base_mother:
                                    selected_girl.character "You're right... as an experienced mother, I should be more careful about cleanliness. We'll use condoms."
                                elif is_student:
                                    selected_girl.character "You're right... I should be more careful about cleanliness. We'll use condoms."
                                else:
                                    selected_girl.character "You're right... I should be more careful about cleanliness. We'll use condoms."
                            else:
                                $ selected_girl.previous_condoms_reaction = "negative"
                                if is_base_mother:
                                    selected_girl.character "I know you're worried, Professor, but as an experienced mother, I want to share this intimacy with you."
                                elif is_student:
                                    selected_girl.character "I know you're worried, Professor, but I want to share this intimacy with you."
                                else:
                                    selected_girl.character "I know you're worried, Professor, but I want to share this intimacy with you."
                                $ selected_girl.apply_impacts({"affection": -15})
                        
                        elif selected_girl.dominant_approach == "sexualized":
                            $ selected_girl.previous_condoms_reaction = "negative"
                            if is_base_mother:
                                selected_girl.character "Why would we want that? As an experienced woman, feeling your cum on my skin is so much more intimate!"
                            elif is_student:
                                selected_girl.character "Why would we want that? Feeling your cum on my skin is so much more intimate!"
                            else:
                                selected_girl.character "Why would we want that? Feeling your cum on my skin is so much more intimate!"
                            $ selected_girl.apply_impacts({"affection": -20})
                        
                        elif selected_girl.dominant_approach == "transactional":
                            selected_girl.character "You want me to start using condoms for body shots? As an experienced woman, that would be a downgrade in service. You'll need to pay extra for that."
                            
                            menu:
                                "Offer 200 cash for clean body shots?":
                                    if player.cash >= 200:
                                        $ player.cash -= 200
                                        $ selected_girl.cash += 200
                                        $ selected_girl.wants_body_condom = True
                                        $ selected_girl.previous_condoms_reaction = "positive"
                                        $ selected_girl.apply_impacts({"discipline": 30, "corruption": 20})
                                        if is_base_mother:
                                            selected_girl.character "200 for clean body shots? As an experienced mother, that's insulting but I'll take it. Fine, we'll use condoms."
                                        elif is_student:
                                            selected_girl.character "200 for clean body shots? That's weird but okay! We'll use condoms!"
                                        else:
                                            selected_girl.character "200 for clean body shots? That's insulting but I'll take it. Fine, we'll use condoms."
                                    else:
                                        $ selected_girl.previous_condoms_reaction = "negative"
                                        if is_base_mother:
                                            selected_girl.character "Don't waste an experienced mother's time. If you want me to downgrade to clean shots, you'll need to pay more."
                                        elif is_student:
                                            selected_girl.character "You don't have enough? Then we're not using condoms."
                                        else:
                                            selected_girl.character "Don't waste my time. If you want me to downgrade to clean shots, you'll need to pay more."
                                        $ selected_girl.apply_impacts({"affection": -25})
                                
                                "Leave it be.":
                                    $ selected_girl.previous_condoms_reaction = "negative"
                                    if is_base_mother:
                                        selected_girl.character "Smart choice. As an experienced woman, bare body marking is the premium experience you're paying for."
                                    elif is_student:
                                        selected_girl.character "Okay! We'll keep going bare for body shots then!"
                                    else:
                                        selected_girl.character "Smart choice. Bare body marking is the premium experience you're paying for."
                                    $ selected_girl.apply_impacts({"affection": -5})
                        
                        elif selected_girl.dominant_approach == "dominate":
                            $ selected_girl.previous_condoms_reaction = "negative"
                            if is_base_mother:
                                selected_girl.character "I prefer bare intimacy, Professor. As an experienced mother, I'm prepared for this."
                            elif is_student:
                                selected_girl.character "I prefer bare intimacy, Professor. I'm prepared for this."
                            else:
                                selected_girl.character "I prefer bare intimacy, Professor. I'm prepared for this."
                            $ selected_girl.apply_impacts({"affection": -15})








        # FALLBACK OPTION - ALWAYS AVAILABLE
        "Perhaps we should maintain appropriate professional boundaries regarding intimate topics.": 
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
    
    # PHASE 2: FINAL REACTIONS BASED ON OUTCOMES
    $ protection_changed = False
    $ protection_count_new = sum(1 for p in [selected_girl.wants_vaginal_condom, 
                                           selected_girl.wants_anal_condom,
                                           selected_girl.wants_oral_condom,
                                           selected_girl.wants_body_condom] if p)
    
    if protection_count_new != protection_count:
        $ protection_changed = True
        
        if protection_count_new > protection_count:  # More cautious
            if selected_girl.dominant_approach == "compassionate":
                selected_girl.character "Thank you for helping me see the importance of protection, Professor."
            elif selected_girl.dominant_approach == "sexualized":
                selected_girl.character "I guess being more careful isn't so bad... if it makes you happy."
            elif selected_girl.dominant_approach == "transactional":
                selected_girl.character "Fine, I'll be more careful - but this better be worth it."
            elif selected_girl.dominant_approach == "dominate":
                selected_girl.character "As you wish, Professor. I will maintain proper protection protocols."
        else:  # Less cautious
            if selected_girl.dominant_approach == "compassionate":
                selected_girl.character "I'm looking forward to experiencing more intimate connection with you, Professor."
            elif selected_girl.dominant_approach == "sexualized":
                selected_girl.character "Oh yes! I can't wait to feel you completely without anything between us!"
            elif selected_girl.dominant_approach == "transactional":
                selected_girl.character "Good choice - bare access is the premium experience you're paying for."
            elif selected_girl.dominant_approach == "dominate":
                selected_girl.character "As you wish, Professor. I will accommodate your preference for bare intimacy."
    else:
        if selected_girl.dominant_approach == "compassionate":
            selected_girl.character "Thanks for checking in about protection preferences, Professor. I feel closer to you now."
        elif selected_girl.dominant_approach == "sexualized":
            selected_girl.character "Thanks for checking in about protection... now let's test out our new arrangements!"
        elif selected_girl.dominant_approach == "transactional":
            selected_girl.character "Thanks for clarifying our protection terms. Let me know if you want to negotiate anything else."
        elif selected_girl.dominant_approach == "dominate":
            selected_girl.character "Acknowledged. Protection preferences have been confirmed."
    
    
    # PHASE 3: SET UP FOR FUTURE CONVERSATIONS
    # Track that this conversation happened
    $ actions_already_done.setdefault(selected_girl.id, []).append("small_talk_condoms")
    
    # Create unique dialogue paths for next conversation
    $ current_level = getattr(selected_girl, "condoms_discussion_level", 0)
    $ selected_girl.condoms_discussion_level = 1 if current_level == 0 else min(3, current_level + 1)

    # Schedule follow-up conversation based on discussion level
    if protection_changed:
        if condoms_discussion_level == 1:
            $ selected_girl.condoms_followup = time_manager.total_days + 5
        elif condoms_discussion_level == 2:
            $ selected_girl.condoms_followup = time_manager.total_days + 7
        else:
            $ selected_girl.condoms_followup = time_manager.total_days + 10
    
    # Apply final impacts based on discussion level and outcomes
    $ impact_amount = 25 * condoms_discussion_level
    
    if protection_count_new > protection_count:  # More cautious
        $ selected_girl.apply_impacts({
            "discipline": impact_amount,
            "fear": impact_amount * 0.5,
            "affection": impact_amount * 0.3
        })
    elif protection_count_new < protection_count:  # Less cautious
        $ selected_girl.apply_impacts({
            "corruption": impact_amount,
            "naturism": impact_amount * 0.5,
            "affection": impact_amount * 0.7
        })
    else:  # No change
        $ selected_girl.apply_impacts({
            "intellect": impact_amount * 0.5,
            "affection": impact_amount * 0.4
        })
    
    $ time_manager.skip_time(minutes=5)
    
    return

label vt_small_talk_condoms_followup:
    
    # Clear identification of relationship types (matching small_talk_condoms)
    $ is_base_mother = False
    $ is_student = False
    $ is_other = False

    if hasattr(selected_girl, "daughter") and selected_girl.daughter:
        $ is_base_mother = True
    elif hasattr(selected_girl, "mother") and selected_girl.mother:
        $ is_student = True
    else:
        $ is_other = True
    
    # PROPER KIDS TRACKING (matching small_talk_condoms)
    $ total_kids = selected_girl.kids
    $ kids_with_player = selected_girl.kids_with_player
    $ kids_with_others = selected_girl.kids_with_npc
    
    # MOTHERHOOD STATUS (matching small_talk_condoms)
    $ is_currently_a_mother = total_kids > 0
    if is_base_mother:
        $ is_currently_a_mother = total_kids > 1  # includes original daughter
    
    # DYNAMIC CHILD REFERENCE (matching small_talk_condoms)
    $ child_reference = ""
    if is_base_mother and (total_kids - kids_with_player - kids_with_others) > 0:
        $ child_reference = "my daughter"
    elif kids_with_player > 0:
        $ child_reference = "your child" if kids_with_player == 1 else f"our {total_kids} children"
    elif kids_with_others > 0:
        $ child_reference = "that child" if kids_with_others == 1 else f"my {total_kids} children"
    else:
        $ child_reference = "my child" if is_currently_a_mother else ""
    
    # FETISH INTEGRATION (matching small_talk_condoms)
    $ vaginal_fetish = max(selected_girl.pussy_cum_fetish or 0, selected_girl.vaginal_cum_fetish or 0)
    $ anal_fetish = max(selected_girl.ass_cum_fetish or 0, selected_girl.anal_cum_fetish or 0)
    $ body_fetish = max(selected_girl.thigh_cum_fetish or 0, selected_girl.boob_cum_fetish or 0)
    
    # PROTECTION STATE TRACKING (matching small_talk_condoms)
    $ protection_state = {
        "vaginal": selected_girl.wants_vaginal_condom,
        "anal": selected_girl.wants_anal_condom,
        "oral": selected_girl.wants_oral_condom,
        "body": selected_girl.wants_body_condom
    }

    # Track previous protection states
    $ previous_vaginal = getattr(selected_girl, "previous_wants_vaginal_condom", selected_girl.wants_vaginal_condom)
    $ previous_anal = getattr(selected_girl, "previous_wants_anal_condom", selected_girl.wants_anal_condom)
    $ previous_oral = getattr(selected_girl, "previous_wants_oral_condom", selected_girl.wants_oral_condom)
    $ previous_body = getattr(selected_girl, "previous_wants_body_condom", selected_girl.wants_body_condom)
    
    # Determine what's changed
    $ vaginal_changed = (previous_vaginal != selected_girl.wants_vaginal_condom)
    $ anal_changed = (previous_anal != selected_girl.wants_anal_condom)
    $ oral_changed = (previous_oral != selected_girl.wants_oral_condom)
    $ body_changed = (previous_body != selected_girl.wants_body_condom)
    
    $ changes_count = sum([vaginal_changed, anal_changed, oral_changed, body_changed])
    
    # DETERMINE OVERALL PROTECTION ATTITUDE (matching small_talk_condoms)
    $ protection_count = sum(1 for p in protection_state.values() if p)
    $ protection_attitude = "cautious" if protection_count >= 3 else "balanced" if protection_count == 2 else "adventurous"
    
    # NORMALIZE AND CLUSTER PERSONALITY TRAITS (matching small_talk_condoms)
    $ norm_naturism = selected_girl.naturism / 10
    $ norm_corruption = selected_girl.corruption / 10
    $ norm_discipline = selected_girl.discipline / 10
    $ norm_fear = selected_girl.fear / 10

    $ natural_leaning = norm_naturism - norm_discipline
    $ risk_taking = norm_corruption - norm_fear
    
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

    # TRACK CONVERSATION HISTORY (matching small_talk_condoms)
    $ has_discussed_condoms_before = "small_talk_condoms" in actions_already_done.get(selected_girl.id, [])
    $ previous_condoms_reaction = getattr(selected_girl, "previous_condoms_reaction", "neutral")
    $ discussion_level = selected_girl.condoms_discussion_level
    
    # OPENING BASED ON CURRENT PROTECTION ATTITUDE AND CHANGES
    if changes_count > 0:
        if protection_attitude == "cautious":
            "[selected_girl] looks serious, clearly prepared to discuss the changes she's made to her protection preferences."
        elif protection_attitude == "balanced":
            "[selected_girl] seems thoughtful, ready to discuss how her protection preferences have evolved."
        else:  # adventurous
            "[selected_girl] gives you a knowing smile, clearly excited to discuss her more adventurous protection choices."
    else:
        if protection_attitude == "cautious":
            "[selected_girl] nods professionally, ready to continue our discussion about protection."
        elif protection_attitude == "balanced":
            "[selected_girl] seems thoughtful, ready to discuss protection preferences further."
        else:  # adventurous
            "[selected_girl] gives you a suggestive smile, eager to continue our discussion about protection."

    # DIFFERENT DIALOGUE BASED ON DISCUSSION LEVEL AND PROTECTION CHANGES
    if discussion_level >= 2:
        if changes_count > 0:
            if protection_attitude == "cautious":
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've been implementing the protection changes we discussed. As an experienced mother, I feel much safer now, especially with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've been implementing the protection changes we discussed. I feel much safer now... thank you for helping me be responsible."
                    else:
                        selected_girl.character "I've been implementing the protection changes we discussed. I feel much safer now."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've been more careful about protection like we talked about... but as an experienced woman, I have to admit, sometimes I miss the thrill of going bare."
                    elif is_student:
                        selected_girl.character "I've been using protection like we discussed... but sometimes I wonder what it would feel like without anything between us."
                    else:
                        selected_girl.character "I've been more careful about protection... but sometimes I miss the thrill of going bare."
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've adjusted my protection terms as discussed. As an experienced mother, these new safety protocols require additional compensation, of course."
                    elif is_student:
                        selected_girl.character "I've been following our protection deal... but if you want me to be more careful, that costs extra. Just so we're clear."
                    else:
                        selected_girl.character "I've adjusted my protection terms as discussed. These new safety protocols require additional compensation."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have implemented the protection protocols as instructed. As an experienced mother, I maintain proper safety measures for all activities."
                    elif is_student:
                        selected_girl.character "I've been using protection like you wanted... I'm following your instructions about safety."
                    else:
                        selected_girl.character "I have implemented the protection protocols as instructed. All safety measures are being maintained."
                
                # Specific changes mentioned
                if vaginal_changed and not selected_girl.wants_vaginal_condom:
                    selected_girl.character "I decided against vaginal protection after reconsidering the risks."
                    $ selected_girl.apply_impacts({"fear": -20, "discipline": 10})
                elif anal_changed and not selected_girl.wants_anal_condom:
                    selected_girl.character "I've stopped using anal protection as we discussed, but I'm monitoring the situation."
                    $ selected_girl.apply_impacts({"fear": -15, "corruption": 25})
                elif body_changed and not selected_girl.wants_body_condom:
                    selected_girl.character "Experiencing body shots without protection has been... intense, but I'm being careful."
                    $ selected_girl.apply_impacts({"corruption": 30, "affection": 15})
                else:
                    selected_girl.character "I've added protection in areas where I wasn't being careful before."
                    $ selected_girl.apply_impacts({"discipline": 25, "fear": 10})
                
            elif protection_attitude == "balanced":
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've been adjusting my protection preferences based on how I'm feeling. As an experienced mother, I'm trying to find the right balance between safety and intimacy, especially with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've been adjusting my protection preferences based on how I'm feeling. I'm trying to find the right balance between being safe and feeling close to you."
                    else:
                        selected_girl.character "I've been adjusting my protection preferences based on how I'm feeling. I'm trying to find the right balance."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've been mixing it up with protection like we talked about. As an experienced woman, sometimes I want the thrill of going bare, other times I want to play it safe... keeps things exciting!"
                    elif is_student:
                        selected_girl.character "I've been mixing it up with protection! Sometimes I want to feel you completely, other times I want to be safe... it's actually pretty hot not knowing what we'll do!"
                    else:
                        selected_girl.character "I've been mixing it up with protection. Sometimes I want the thrill of going bare, other times I want to play it safe... keeps things exciting!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've been adjusting protection terms based on the situation. As an experienced mother, different activities have different pricing structures - bare access costs more, of course."
                    elif is_student:
                        selected_girl.character "I've been changing protection based on what's happening... bare costs more, protected costs less. Just let me know what you want and I'll give you a price!"
                    else:
                        selected_girl.character "I've been adjusting protection terms based on the situation. Different activities have different pricing structures - bare access costs more."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have been adjusting protection protocols based on circumstances. As an experienced mother, I use discretion while maintaining appropriate safety measures."
                    elif is_student:
                        selected_girl.character "I've been changing protection based on the situation... I'm trying to follow your lead on what's appropriate."
                    else:
                        selected_girl.character "I have been adjusting protection protocols based on circumstances. I use discretion while maintaining appropriate safety measures."
                
                if vaginal_changed:
                    if selected_girl.wants_vaginal_condom:
                        selected_girl.character "I've started using vaginal protection when I feel less certain."
                        $ selected_girl.apply_impacts({"discipline": 15, "naturism": -10})
                    else:
                        selected_girl.character "I've stopped using vaginal protection when I feel particularly connected to you."
                        $ selected_girl.apply_impacts({"naturism": 15, "corruption": 10})
                
                if anal_changed:
                    if selected_girl.wants_anal_condom:
                        selected_girl.character "I've been using anal protection more consistently when I'm feeling cautious."
                        $ selected_girl.apply_impacts({"discipline": 15, "fear": 10})
                    else:
                        selected_girl.character "I've been skipping anal protection when I'm feeling particularly adventurous."
                        $ selected_girl.apply_impacts({"corruption": 20, "affection": 10})
                
            else:  # adventurous
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've been embracing more direct intimacy without barriers between us. As an experienced mother, I trust you completely, even with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've been embracing more direct intimacy without barriers between us. I trust you completely and want to feel everything with you."
                    else:
                        selected_girl.character "I've been embracing more direct intimacy without barriers between us. I trust you completely."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've been going completely bare like we discussed! As an experienced woman, it's so much more intense without anything between us - I can't get enough!"
                    elif is_student:
                        selected_girl.character "I've been going completely bare like we discussed! Oh my god, it's so much more intense without anything between us - I love it!"
                    else:
                        selected_girl.character "I've been going completely bare like we discussed! It's so much more intense without anything between us - I can't get enough!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've been offering premium bare access as discussed. As an experienced mother, this is our highest tier service - and priced accordingly."
                    elif is_student:
                        selected_girl.character "I've been going bare for everything like you wanted! That's the most expensive option, right? I hope you're appreciating the premium service!"
                    else:
                        selected_girl.character "I've been offering premium bare access as discussed. This is our highest tier service - and priced accordingly."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have been providing bare access as commanded. As an experienced mother, I offer myself completely without barriers for your pleasure."
                    elif is_student:
                        selected_girl.character "I've been going bare like you wanted... I'm offering myself completely without anything between us."
                    else:
                        selected_girl.character "I have been providing bare access as commanded. I offer myself completely without barriers for your pleasure."
                
                if vaginal_changed and not selected_girl.wants_vaginal_condom:
                    if vaginal_fetish > 70:
                        selected_girl.character "I've stopped vaginal protection completely. I love feeling you inside me with nothing between us."
                        $ selected_girl.apply_impacts({"vaginal_cum_fetish": 30, "corruption": 40})
                    else:
                        selected_girl.character "I've stopped vaginal protection. It feels so much more intimate this way."
                        $ selected_girl.apply_impacts({"corruption": 30, "naturism": 20})
                
                elif anal_changed and not selected_girl.wants_anal_condom:
                    if anal_fetish > 70:
                        selected_girl.character "I've stopped anal protection completely. The intensity without barriers is incredible."
                        $ selected_girl.apply_impacts({"anal_cum_fetish": 30, "corruption": 35})
                    else:
                        selected_girl.character "I've stopped anal protection. It's much more intense this way."
                        $ selected_girl.apply_impacts({"corruption": 25, "naturism": 15})
                
                elif body_changed and not selected_girl.wants_body_condom:
                    if body_fetish > 70:
                        selected_girl.character "I love feeling your cum on my bare skin. I've stopped using protection for body shots completely."
                        $ selected_girl.apply_impacts({"boob_cum_fetish": 20, "thigh_cum_fetish": 20, "corruption": 30})
                    else:
                        selected_girl.character "I've stopped using protection for body shots. It feels more authentic this way."
                        $ selected_girl.apply_impacts({"corruption": 20, "naturism": 10})
                
                else:
                    selected_girl.character "I've been selective about when I use protection, based on how I'm feeling."
                    $ selected_girl.apply_impacts({"corruption": 15, "naturism": 10})
        
        else:  # No changes since last discussion
            if protection_attitude == "cautious":
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've maintained my current protection preferences as we discussed. As an experienced mother, I feel comfortable with this level of safety, especially with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've kept my protection preferences as we discussed. I feel good about being responsible... thank you for helping me."
                    else:
                        selected_girl.character "I've maintained my current protection preferences as we discussed. I feel comfortable with this level of safety."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've kept using protection like we talked about... but as an experienced woman, I have to admit, sometimes I get tempted to go bare just for the thrill!"
                    elif is_student:
                        selected_girl.character "I've kept using protection like we talked about... but sometimes I get tempted to go bare! It sounds so exciting!"
                    else:
                        selected_girl.character "I've kept using protection like we talked about... but sometimes I get tempted to go bare just for the thrill!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've maintained our current protection terms. As an experienced mother, unless you're willing to pay for bare access, these safety measures remain in place."
                    elif is_student:
                        selected_girl.character "I've kept our protection deal the same... unless you want to pay more to go bare, I'm staying protected!"
                    else:
                        selected_girl.character "I've maintained our current protection terms. Unless you're willing to pay for bare access, these safety measures remain in place."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have maintained the protection protocols as instructed. As an experienced mother, I continue to follow all safety procedures."
                    elif is_student:
                        selected_girl.character "I've kept using protection like you wanted... I'm still following your safety instructions."
                    else:
                        selected_girl.character "I have maintained the protection protocols as instructed. I continue to follow all safety procedures."
                $ selected_girl.apply_impacts({"discipline": 10})
                
            elif protection_attitude == "balanced":
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've kept my protection preferences consistent. As an experienced mother, I feel good about this balanced approach, especially when considering [child_reference or 'my family']."
                    elif is_student:
                        selected_girl.character "I've kept my protection approach consistent. I feel good about finding this balance with you."
                    else:
                        selected_girl.character "I've kept my protection preferences consistent. I feel good about this balanced approach."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've been sticking to our protection mix. As an experienced woman, I like keeping you guessing - sometimes protected, sometimes bare!"
                    elif is_student:
                        selected_girl.character "I've been sticking to our protection mix! I like keeping you guessing - sometimes protected, sometimes bare!"
                    else:
                        selected_girl.character "I've been sticking to our protection mix. I like keeping you guessing - sometimes protected, sometimes bare!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've maintained our tiered protection pricing. As an experienced mother, different activities still have different rates - bare access remains premium."
                    elif is_student:
                        selected_girl.character "I've kept our protection deal the same - different activities still cost different amounts!"
                    else:
                        selected_girl.character "I've maintained our tiered protection pricing. Different activities still have different rates - bare access remains premium."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have maintained our balanced protection approach. As an experienced mother, I use discretion while following established protocols."
                    elif is_student:
                        selected_girl.character "I've kept our protection approach balanced... I'm trying to follow your lead on what works best."
                    else:
                        selected_girl.character "I have maintained our balanced protection approach. I use discretion while following established protocols."
                $ selected_girl.apply_impacts({"intellect": 10})
                
            else:  # adventurous
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've maintained my preference for more direct intimacy. As an experienced mother, I trust you completely, even with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've kept preferring direct intimacy without barriers. I trust you completely and love feeling close to you."
                    else:
                        selected_girl.character "I've maintained my preference for more direct intimacy. I trust you completely."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've kept going bare for everything! As an experienced woman, I can't imagine going back to using protection - it's so much better this way!"
                    elif is_student:
                        selected_girl.character "I've kept going bare for everything! I can't imagine using protection again - it feels so much better without!"
                    else:
                        selected_girl.character "I've kept going bare for everything! I can't imagine going back to using protection - it's so much better this way!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've maintained premium bare access across all services. As an experienced mother, this remains our highest tier offering - priced accordingly."
                    elif is_student:
                        selected_girl.character "I've kept going bare for everything! That's still the most expensive option, right? Good, because I'm enjoying the premium treatment!"
                    else:
                        selected_girl.character "I've maintained premium bare access across all services. This remains our highest tier offering - priced accordingly."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have maintained bare access as commanded. As an experienced mother, I continue to offer myself completely without barriers."
                    elif is_student:
                        selected_girl.character "I've kept going bare like you wanted... I'm still offering myself completely to you."
                    else:
                        selected_girl.character "I have maintained bare access as commanded. I continue to offer myself completely without barriers."
                $ selected_girl.apply_impacts({"corruption": 10, "affection": 5})
    
    elif discussion_level == 1:
        if changes_count > 0:
            if protection_attitude == "cautious":
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've been trying out the protection changes we discussed. As an experienced mother, it's helping me feel more responsible, especially with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've been trying out the protection changes we discussed. It's helping me feel more responsible... thank you for caring about my safety."
                    else:
                        selected_girl.character "I've been trying out the protection changes we discussed. It's helping me feel more responsible."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've been using protection like we talked about... but as an experienced woman, I have to admit, it's kind of killing the mood sometimes."
                    elif is_student:
                        selected_girl.character "I've been using protection like we talked about... but it's kind of killing the mood sometimes, you know?"
                    else:
                        selected_girl.character "I've been using protection like we talked about... but I have to admit, it's kind of killing the mood sometimes."
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've implemented the protection changes as discussed. As an experienced mother, these safety measures affect pricing - let me know if you want to negotiate terms."
                    elif is_student:
                        selected_girl.character "I've been using protection like we discussed... but this is the cheaper option, right? Just making sure we're clear on the pricing."
                    else:
                        selected_girl.character "I've implemented the protection changes as discussed. These safety measures affect pricing - let me know if you want to negotiate terms."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have been following the protection instructions. As an experienced mother, I maintain proper safety protocols as directed."
                    elif is_student:
                        selected_girl.character "I've been using protection like you wanted... I'm trying to follow your instructions about being safe."
                    else:
                        selected_girl.character "I have been following the protection instructions. I maintain proper safety protocols as directed."
                $ selected_girl.apply_impacts({"discipline": 20, "fear": 10})
                
            elif protection_attitude == "balanced":
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've been adjusting my protection preferences like we talked about. As an experienced mother, I feel good about finding this balance with you, even with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've been adjusting my protection like we talked about. I feel good about finding this balance with you."
                    else:
                        selected_girl.character "I've been adjusting my protection preferences like we talked about. I feel good about finding this balance."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've been mixing up protection like we discussed! As an experienced woman, sometimes bare, sometimes protected... keeps things exciting!"
                    elif is_student:
                        selected_girl.character "I've been mixing up protection like we discussed! Sometimes bare, sometimes protected... it's actually pretty fun not knowing what we'll do!"
                    else:
                        selected_girl.character "I've been mixing up protection like we discussed! Sometimes bare, sometimes protected... keeps things exciting!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've been adjusting protection based on our agreement. As an experienced mother, different activities still have different pricing - bare costs extra."
                    elif is_student:
                        selected_girl.character "I've been changing protection based on what we're doing... just remember, bare activities cost more!"
                    else:
                        selected_girl.character "I've been adjusting protection based on our agreement. Different activities still have different pricing - bare costs extra."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have been adjusting protection protocols as instructed. As an experienced mother, I use appropriate discretion for each situation."
                    elif is_student:
                        selected_girl.character "I've been changing protection based on what we're doing... I'm trying to follow your lead on what's appropriate."
                    else:
                        selected_girl.character "I have been adjusting protection protocols as instructed. I use appropriate discretion for each situation."
                $ selected_girl.apply_impacts({"intellect": 15, "affection": 10})
                
            else:  # adventurous
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've been embracing less protection like we discussed. As an experienced mother, I trust you completely, even with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've been going with less protection like we talked about. I trust you completely and love feeling close to you."
                    else:
                        selected_girl.character "I've been embracing less protection like we discussed. I trust you completely."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've been going bare more like we discussed! As an experienced woman, it's so much more intense without anything between us - I'm loving it!"
                    elif is_student:
                        selected_girl.character "I've been going bare more like we discussed! Oh my god, it's so much more intense - I'm loving it!"
                    else:
                        selected_girl.character "I've been going bare more like we discussed! It's so much more intense without anything between us - I'm loving it!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've been offering more bare access as discussed. As an experienced mother, this upgrade in service requires appropriate compensation."
                    elif is_student:
                        selected_girl.character "I've been going bare more like you wanted! This is the expensive option, right? I hope you're appreciating the upgrade!"
                    else:
                        selected_girl.character "I've been offering more bare access as discussed. This upgrade in service requires appropriate compensation."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have been providing more bare access as commanded. As an experienced mother, I offer myself increasingly without barriers."
                    elif is_student:
                        selected_girl.character "I've been going bare more like you wanted... I'm offering myself more completely to you."
                    else:
                        selected_girl.character "I have been providing more bare access as commanded. I offer myself increasingly without barriers."
                
                if vaginal_changed and not selected_girl.wants_vaginal_condom:
                    $ selected_girl.apply_impacts({"corruption": 25, "affection": 15})
                elif anal_changed and not selected_girl.wants_anal_condom:
                    $ selected_girl.apply_impacts({"corruption": 20, "affection": 10})
                else:
                    $ selected_girl.apply_impacts({"corruption": 15, "affection": 5})
        
        else:  # No changes since last discussion
            if protection_attitude == "cautious":
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've kept my protection preferences the same. As an experienced mother, I'm still thinking about being more cautious, especially with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've kept my protection the same... I'm still thinking about being more careful. Thanks for understanding."
                    else:
                        selected_girl.character "I've kept my protection preferences the same. I'm still thinking about being more cautious."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've kept using protection... but as an experienced woman, I'm still tempted to go bare just for the thrill of it!"
                    elif is_student:
                        selected_girl.character "I've kept using protection... but I'm still tempted to go bare! It sounds so exciting!"
                    else:
                        selected_girl.character "I've kept using protection... but I'm still tempted to go bare just for the thrill of it!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've maintained current protection pricing. As an experienced mother, unless you're willing to pay for bare access, these terms remain in effect."
                    elif is_student:
                        selected_girl.character "I've kept our protection deal the same... unless you want to pay more, I'm staying protected!"
                    else:
                        selected_girl.character "I've maintained current protection pricing. Unless you're willing to pay for bare access, these terms remain in effect."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have maintained current protection protocols. As an experienced mother, I continue to follow established safety procedures."
                    elif is_student:
                        selected_girl.character "I've kept using protection like you wanted... I'm still following your safety instructions."
                    else:
                        selected_girl.character "I have maintained current protection protocols. I continue to follow established safety procedures."
                $ selected_girl.apply_impacts({"discipline": 10, "fear": 5})
                
            elif protection_attitude == "balanced":
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've maintained my current protection approach. As an experienced mother, I'm still considering adjustments, especially with [child_reference or 'my family'] to think about."
                    elif is_student:
                        selected_girl.character "I've kept my protection the same... I'm still considering making some changes. Thanks for being patient with me."
                    else:
                        selected_girl.character "I've maintained my current protection approach. I'm still considering adjustments."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've been sticking to our protection mix... but as an experienced woman, I'm still thinking about going completely bare sometimes!"
                    elif is_student:
                        selected_girl.character "I've been sticking to our protection mix... but I'm still thinking about going completely bare sometimes!"
                    else:
                        selected_girl.character "I've been sticking to our protection mix... but I'm still thinking about going completely bare sometimes!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've maintained our tiered protection structure. As an experienced mother, I'm still open to negotiating different terms if you're interested."
                    elif is_student:
                        selected_girl.character "I've kept our protection deal the same... but I'm still open to negotiating if you want to change anything!"
                    else:
                        selected_girl.character "I've maintained our tiered protection structure. I'm still open to negotiating different terms if you're interested."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have maintained our balanced protection approach. As an experienced mother, I await further instructions regarding any protocol changes."
                    elif is_student:
                        selected_girl.character "I've kept our protection approach balanced... I'm waiting for you to tell me if you want any changes."
                    else:
                        selected_girl.character "I have maintained our balanced protection approach. I await further instructions regarding any protocol changes."
                $ selected_girl.apply_impacts({"intellect": 10})
                
            else:  # adventurous
                if selected_girl.dominant_approach == "compassionate":
                    if is_base_mother:
                        selected_girl.character "I've kept preferring minimal protection. As an experienced mother, I'm still thinking about embracing more direct intimacy with you, even with [child_reference or 'my family'] to consider."
                    elif is_student:
                        selected_girl.character "I've kept preferring minimal protection... I'm still thinking about being even more intimate with you."
                    else:
                        selected_girl.character "I've kept preferring minimal protection. I'm still thinking about embracing more direct intimacy with you."
                        
                elif selected_girl.dominant_approach == "sexualized":
                    if is_base_mother:
                        selected_girl.character "I've kept going bare like we talked about... but as an experienced woman, I'm thinking about going even more wild!"
                    elif is_student:
                        selected_girl.character "I've kept going bare like we talked about... but I'm thinking about being even more adventurous!"
                    else:
                        selected_girl.character "I've kept going bare like we talked about... but I'm thinking about going even more wild!"
                        
                elif selected_girl.dominant_approach == "transactional":
                    if is_base_mother:
                        selected_girl.character "I've maintained premium bare access. As an experienced mother, I'm considering offering even more exclusive services - for the right price."
                    elif is_student:
                        selected_girl.character "I've kept going bare like you wanted... but I'm thinking about offering even more special services! For extra credit, of course!"
                    else:
                        selected_girl.character "I've maintained premium bare access. I'm considering offering even more exclusive services - for the right price."
                        
                elif selected_girl.dominant_approach == "dominate":
                    if is_base_mother:
                        selected_girl.character "I have maintained bare access as instructed. As an experienced mother, I'm prepared to offer even more intimate services if commanded."
                    elif is_student:
                        selected_girl.character "I've kept going bare like you wanted... I'm ready for whatever you want to try next."
                    else:
                        selected_girl.character "I have maintained bare access as instructed. I'm prepared to offer even more intimate services if commanded."
                $ selected_girl.apply_impacts({"corruption": 10, "naturism": 5})
    
    else:  # discussion_level == 0 (shouldn't happen in follow-up)
        if selected_girl.dominant_approach == "compassionate":
            selected_girl.character "I'm confused... why are you bringing this up again so soon? I'm still processing our previous conversation."
        elif selected_girl.dominant_approach == "sexualized":
            selected_girl.character "Again with the protection talk? We just discussed this! Can't we move on to something more exciting?"
        elif selected_girl.dominant_approach == "transactional":
            selected_girl.character "We just negotiated protection terms. Unless you have new offers, this follow-up seems unnecessary."
        elif selected_girl.dominant_approach == "dominate":
            selected_girl.character "This topic was recently addressed. Unless you have new directives, this follow-up is premature."
        else:
            selected_girl.character "I'm confused... why are you bringing this up again so soon? I'm still processing our previous conversation."
        $ selected_girl.apply_impacts({"intellect": 5})

    # Additional dialogue based on motherhood status
    if is_currently_a_mother and child_reference:
        if selected_girl.dominant_approach == "compassionate":
            selected_girl.character "I think about [child_reference] when I consider my protection choices. I need to be responsible."
            $ selected_girl.apply_impacts({"discipline": 15})
        elif selected_girl.dominant_approach == "sexualized":
            selected_girl.character "Even with [child_reference] around, I can't help but get excited thinking about our protection arrangements..."
            $ selected_girl.apply_impacts({"corruption": 10})
        elif selected_girl.dominant_approach == "transactional":
            selected_girl.character "With [child_reference] to consider, my protection services require premium compensation. The stakes are higher."
            $ selected_girl.apply_impacts({"corruption": 5})
        elif selected_girl.dominant_approach == "dominate":
            selected_girl.character "With [child_reference] to protect, I maintain stricter safety protocols. My family comes first."
            $ selected_girl.apply_impacts({"discipline": 10})

    # Update tracking variables
    $ selected_girl.condoms_discussion_level = min(3, discussion_level + 1)
    
    # Store current protection states as previous for next time
    $ selected_girl.previous_wants_vaginal_condom = selected_girl.wants_vaginal_condom
    $ selected_girl.previous_wants_anal_condom = selected_girl.wants_anal_condom
    $ selected_girl.previous_wants_oral_condom = selected_girl.wants_oral_condom
    $ selected_girl.previous_wants_body_condom = selected_girl.wants_body_condom
    
    # Set reaction based on protection attitude
    if protection_attitude == "cautious":
        $ selected_girl.previous_condoms_reaction = "positive"
    elif protection_attitude == "balanced":
        $ selected_girl.previous_condoms_reaction = "neutral"
    else:  # adventurous
        $ selected_girl.previous_condoms_reaction = "positive"

    # PLAYER RESPONSE OPTIONS WITH MEANINGFUL CHOICES
    menu:
        "This aligns with my compassionate approach to relationships." if norm_compassion > 5:
            player.character "I'm glad you've been reflecting on our previous conversation. Your comfort and safety are important to me."
            
            if changes_count > 0:
                if protection_attitude == "cautious":
                    selected_girl.character "Thank you for caring about my safety, Professor. It means a lot."
                    $ selected_girl.apply_impacts({"affection": 30, "fear": -25})
                elif protection_attitude == "balanced":
                    selected_girl.character "Thank you for understanding my approach, Professor. It means a lot."
                    $ selected_girl.apply_impacts({"affection": 25, "intellect": 15})
                else:  # adventurous
                    selected_girl.character "Thank you for embracing my preferences, Professor. It means a lot."
                    $ selected_girl.apply_impacts({"affection": 35, "corruption": 20})
            else:
                selected_girl.character "Thank you for checking in, Professor. I appreciate your concern."
                $ selected_girl.apply_impacts({"affection": 20})
            
        "This demonstrates proper discipline in our relationship." if norm_control > 5:
            player.character "Good. I expect you to be responsible with protection in our relationship."
            
            if protection_attitude == "cautious":
                selected_girl.character "I am being responsible, Professor. I'm following our protection agreements consistently."
                $ selected_girl.apply_impacts({"discipline": 30, "affection": 15})
            elif protection_attitude == "balanced":
                selected_girl.character "I'm being responsible in my own way, Professor. I adjust based on the situation."
                $ selected_girl.apply_impacts({"intellect": 25, "discipline": 10})
            else:  # adventurous
                if selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "I'm being responsible in my own way, Professor. I know what I'm comfortable with!"
                    $ selected_girl.apply_impacts({"corruption": 25, "affection": 20})
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "I'm being perfectly responsible - all our bare activities are properly compensated!"
                    $ selected_girl.apply_impacts({"corruption": 15, "affection": 10})
                else:
                    selected_girl.character "I'm being responsible in my own way, Professor. I know what I'm comfortable with."
                    $ selected_girl.apply_impacts({"corruption": 15, "affection": 10})
                
        "This fits with my more adventurous perspective." if norm_lust > 5:
            player.character "I'm glad you're embracing the more... direct aspects of our relationship."
            
            if protection_attitude == "adventurous":
                if selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "I love the feeling of direct connection without protection between us!"
                    $ selected_girl.apply_impacts({"corruption": 35, "affection": 25})
                elif selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "I love feeling close to you without anything between us."
                    $ selected_girl.apply_impacts({"affection": 30, "corruption": 15})
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "You're getting the premium bare experience you're paying for - enjoy it!"
                    $ selected_girl.apply_impacts({"corruption": 20, "affection": 15})
                else:
                    selected_girl.character "I'm pleased you're satisfied with our direct intimacy."
                    $ selected_girl.apply_impacts({"affection": 20, "corruption": 10})
            else:
                selected_girl.character "I see what you mean, Professor, but I'm not ready for that level of intimacy yet."
                $ selected_girl.apply_impacts({"corruption": 15})
        
        "Let's discuss specific protection preferences.":
            player.character "Let's focus on specific aspects of our protection agreements."
            
            menu:
                "How do you feel about vaginal protection now?":
                    # Similar structure to main conversation but focused on follow-up
                    if selected_girl.wants_vaginal_condom:
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "I still prefer using vaginal protection. As an experienced mother, it makes me feel safer and more in control."
                            elif is_student:
                                selected_girl.character "I still prefer using vaginal protection. It makes me feel safer... thanks for understanding."
                            else:
                                selected_girl.character "I still prefer using vaginal protection. It makes me feel safer and more in control."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "I still prefer protection for vaginal... but as an experienced woman, sometimes I get tempted to go bare just for you!"
                            elif is_student:
                                selected_girl.character "I still prefer protection for vaginal... but sometimes I get tempted to go bare! It sounds so exciting!"
                            else:
                                selected_girl.character "I still prefer protection for vaginal... but sometimes I get tempted to go bare just for the thrill!"
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Vaginal protection remains standard pricing. As an experienced mother, bare access would require additional compensation."
                            elif is_student:
                                selected_girl.character "Vaginal protection is still the standard price! If you want bare, that costs extra!"
                            else:
                                selected_girl.character "Vaginal protection remains standard pricing. Bare access would require additional compensation."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "I maintain vaginal protection as instructed. As an experienced mother, I follow established safety protocols."
                            elif is_student:
                                selected_girl.character "I'm still using vaginal protection like you wanted... I'm following your instructions."
                            else:
                                selected_girl.character "I maintain vaginal protection as instructed. I follow established safety protocols."
                        
                        menu:
                            "That's responsible.":
                                $ selected_girl.apply_impacts({"discipline": 20, "affection": 10})
                                if selected_girl.dominant_approach == "compassionate":
                                    selected_girl.character "Thank you for understanding. I appreciate your support for my safety."
                                elif selected_girl.dominant_approach == "sexualized":
                                    selected_girl.character "Thanks... even though it's less exciting, I know you care about me."
                                elif selected_girl.dominant_approach == "transactional":
                                    selected_girl.character "Good. Responsible choices maintain proper service standards."
                                elif selected_girl.dominant_approach == "dominate":
                                    selected_girl.character "Acknowledged. Your approval of my safety protocols is noted."
                            
                            "Would you consider being more flexible?" if risk_taking > 4:
                                $ persuasion_score = 30 + (risk_taking * 3)
                                if persuasion_score > 50:
                                    $ selected_girl.wants_vaginal_condom = False
                                    $ selected_girl.apply_impacts({"corruption": 30, "naturism": 20})
                                    if selected_girl.dominant_approach == "compassionate":
                                        selected_girl.character "I... I suppose I could try it without protection sometimes. But only if you're careful."
                                    elif selected_girl.dominant_approach == "sexualized":
                                        selected_girl.character "Really? Okay... I'll try going bare sometimes! This is going to be so exciting!"
                                    elif selected_girl.dominant_approach == "transactional":
                                        selected_girl.character "For additional compensation, I could be more flexible about bare vaginal access."
                                    elif selected_girl.dominant_approach == "dominate":
                                        selected_girl.character "If you wish me to be more flexible with vaginal protection, I will comply."
                                else:
                                    if selected_girl.dominant_approach == "compassionate":
                                        selected_girl.character "I'm not comfortable with that, Professor. I need to be careful."
                                    elif selected_girl.dominant_approach == "sexualized":
                                        selected_girl.character "I don't think I'm ready for that yet... but maybe someday!"
                                    elif selected_girl.dominant_approach == "transactional":
                                        selected_girl.character "Bare vaginal access requires significant additional compensation. Current offer insufficient."
                                    elif selected_girl.dominant_approach == "dominate":
                                        selected_girl.character "I am not comfortable with that level of flexibility in vaginal protection."
                    
                    else:
                        # She doesn't want vaginal protection
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "I prefer not using vaginal protection. As an experienced mother, it feels more intimate without barriers, and I trust you completely."
                            elif is_student:
                                selected_girl.character "I prefer not using vaginal protection. It feels more intimate without barriers... I trust you."
                            else:
                                selected_girl.character "I prefer not using vaginal protection. It feels more intimate without barriers, and I trust you completely."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "I love experiencing vaginal intimacy without barriers! As an experienced woman, it's so much more intense this way!"
                            elif is_student:
                                selected_girl.character "I love going bare for vaginal! Oh my god, it's so much more intense without anything between us!"
                            else:
                                selected_girl.character "I love experiencing vaginal intimacy without barriers! It's so much more intense this way!"
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Bare vaginal access remains our premium service. As an experienced mother, you're getting exactly what you're paying for."
                            elif is_student:
                                selected_girl.character "Bare vaginal is the most expensive option! You're getting the premium service!"
                            else:
                                selected_girl.character "Bare vaginal access remains our premium service. You're getting exactly what you're paying for."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "I maintain bare vaginal access as permitted. As an experienced mother, I offer myself to you without barriers."
                            elif is_student:
                                selected_girl.character "I'm not using vaginal protection like you wanted... I'm offering myself completely to you."
                            else:
                                selected_girl.character "I maintain bare vaginal access as permitted. I offer myself to you without barriers."
                        
                        menu:
                            "I respect your boundaries.":
                                $ selected_girl.apply_impacts({"affection": 20, "trust": 30})
                                if selected_girl.dominant_approach == "compassionate":
                                    selected_girl.character "Thank you for understanding. I feel so close to you when you respect my choices."
                                elif selected_girl.dominant_approach == "sexualized":
                                    selected_girl.character "Thanks! I love that you want me bare too!"
                                elif selected_girl.dominant_approach == "transactional":
                                    selected_girl.character "Good. You're getting premium value from our bare arrangement."
                                elif selected_girl.dominant_approach == "dominate":
                                    selected_girl.character "Acknowledged. Your approval of my bare offering is appreciated."
                            
                            "Should we consider protection for health reasons?" if norm_discipline > 5:
                                $ persuasion_score = 35 + (norm_discipline * 4)
                                if persuasion_score > 55:
                                    $ selected_girl.wants_vaginal_condom = True
                                    $ selected_girl.apply_impacts({"discipline": 25, "fear": 15})
                                    if selected_girl.dominant_approach == "compassionate":
                                        selected_girl.character "You're right, Professor. Safety is important. I'll use protection."
                                    elif selected_girl.dominant_approach == "sexualized":
                                        selected_girl.character "I guess you're right... if it's for health reasons, I'll use protection."
                                    elif selected_girl.dominant_approach == "transactional":
                                        selected_girl.character "For health reasons, I'll adjust to protected vaginal access. Pricing remains standard."
                                    elif selected_girl.dominant_approach == "dominate":
                                        selected_girl.character "If health protection is required, I will comply with vaginal condoms."
                                else:
                                    if selected_girl.dominant_approach == "compassionate":
                                        selected_girl.character "I'm not comfortable with that suggestion, Professor. I trust you completely."
                                    elif selected_girl.dominant_approach == "sexualized":
                                        selected_girl.character "But going bare feels so good! Do we have to?"
                                    elif selected_girl.dominant_approach == "transactional":
                                        selected_girl.character "Health concerns would require additional compensation for the change in service."
                                    elif selected_girl.dominant_approach == "dominate":
                                        selected_girl.character "I prefer bare access as previously established. I do not wish to change."
                
                "What about anal protection?":
                    # Similar structure for anal follow-up
                    if selected_girl.wants_anal_condom:
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "I definitely prefer using protection for anal. As an experienced mother, it's much safer that way."
                            elif is_student:
                                selected_girl.character "I definitely prefer using protection for anal. It's much safer that way... thanks for looking out for me."
                            else:
                                selected_girl.character "I definitely prefer using protection for anal. It's much safer that way."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "I prefer protection for anal... but as an experienced woman, sometimes I wonder what bare would feel like!"
                            elif is_student:
                                selected_girl.character "I prefer protection for anal... but sometimes I wonder what bare would feel like! That sounds intense!"
                            else:
                                selected_girl.character "I prefer protection for anal... but sometimes I wonder what bare would feel like!"
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Anal protection remains standard pricing. As an experienced mother, bare anal would require additional compensation."
                            elif is_student:
                                selected_girl.character "Anal protection is the standard price! Bare anal costs extra!"
                            else:
                                selected_girl.character "Anal protection remains standard pricing. Bare anal would require additional compensation."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "I maintain anal protection as instructed. As an experienced mother, I follow established safety protocols."
                            elif is_student:
                                selected_girl.character "I'm still using anal protection like you wanted... I'm following your instructions."
                            else:
                                selected_girl.character "I maintain anal protection as instructed. I follow established safety protocols."
                        
                        menu:
                            "That's wise.":
                                $ selected_girl.apply_impacts({"affection": 15, "intellect": 20})
                                if selected_girl.dominant_approach == "compassionate":
                                    selected_girl.character "Thank you. Safety is important to me, and I'm glad you understand."
                                elif selected_girl.dominant_approach == "sexualized":
                                    selected_girl.character "Thanks... even though it's less exciting, I know you care about me being safe."
                                elif selected_girl.dominant_approach == "transactional":
                                    selected_girl.character "Wise choices maintain proper service standards and reduce liability."
                                elif selected_girl.dominant_approach == "dominate":
                                    selected_girl.character "Acknowledged. Your approval of my anal safety protocols is noted."
                            
                            "Would you consider being more adventurous?" if risk_taking > 5:
                                $ persuasion_score = 30 + (risk_taking * 3)
                                if persuasion_score > 50:
                                    $ selected_girl.wants_anal_condom = False
                                    $ selected_girl.apply_impacts({"corruption": 30, "affection": 20})
                                    if selected_girl.dominant_approach == "compassionate":
                                        selected_girl.character "I... I suppose I could try it without protection sometimes. But only if you're careful."
                                    elif selected_girl.dominant_approach == "sexualized":
                                        selected_girl.character "Really? Okay... I'll try bare anal sometimes! This is going to be so intense!"
                                    elif selected_girl.dominant_approach == "transactional":
                                        selected_girl.character "For additional compensation, I could be more flexible about bare anal access."
                                    elif selected_girl.dominant_approach == "dominate":
                                        selected_girl.character "If you wish me to be more adventurous with anal protection, I will comply."
                                else:
                                    if selected_girl.dominant_approach == "compassionate":
                                        selected_girl.character "I'm not comfortable with that, Professor. Anal sex is risky enough without skipping protection."
                                    elif selected_girl.dominant_approach == "sexualized":
                                        selected_girl.character "I don't think I'm ready for bare anal yet... but maybe someday!"
                                    elif selected_girl.dominant_approach == "transactional":
                                        selected_girl.character "Bare anal access requires significant additional compensation. Current offer insufficient."
                                    elif selected_girl.dominant_approach == "dominate":
                                        selected_girl.character "I am not comfortable with that level of risk in anal protection."
                    
                    else:
                        # She doesn't want anal protection
                        if selected_girl.dominant_approach == "compassionate":
                            if is_base_mother:
                                selected_girl.character "I don't usually use protection for anal. As an experienced mother, it feels more intimate without barriers, and I trust you."
                            elif is_student:
                                selected_girl.character "I don't usually use protection for anal. It feels more intimate without barriers... I trust you."
                            else:
                                selected_girl.character "I don't usually use protection for anal. It feels more intimate without barriers, and I trust you."
                        elif selected_girl.dominant_approach == "sexualized":
                            if is_base_mother:
                                selected_girl.character "I don't mind skipping protection for anal! As an experienced woman, the intensity without barriers is incredible!"
                            elif is_student:
                                selected_girl.character "I don't mind skipping protection for anal! Oh my god, the intensity without barriers is incredible!"
                            else:
                                selected_girl.character "I don't mind skipping protection for anal. The intensity without barriers is incredible!"
                        elif selected_girl.dominant_approach == "transactional":
                            if is_base_mother:
                                selected_girl.character "Bare anal access is included in our current arrangement. As an experienced mother, you're getting premium value."
                            elif is_student:
                                selected_girl.character "Bare anal is included in what we agreed on! You're getting the good stuff!"
                            else:
                                selected_girl.character "Bare anal access is included in our current arrangement. You're getting premium value."
                        elif selected_girl.dominant_approach == "dominate":
                            if is_base_mother:
                                selected_girl.character "I maintain bare anal access as permitted. As an experienced mother, I offer this intimacy to you without barriers."
                            elif is_student:
                                selected_girl.character "I'm not using anal protection like you wanted... I'm offering myself completely to you."
                            else:
                                selected_girl.character "I maintain bare anal access as permitted. I offer this intimacy to you without barriers."
                        
                        menu:
                            "I respect your choice.":
                                $ selected_girl.apply_impacts({"affection": 20})
                                if selected_girl.dominant_approach == "compassionate":
                                    selected_girl.character "Thank you for understanding. I feel so close to you when you respect my choices."
                                elif selected_girl.dominant_approach == "sexualized":
                                    selected_girl.character "Thanks! I love that you want me bare for anal too!"
                                elif selected_girl.dominant_approach == "transactional":
                                    selected_girl.character "Good. You're receiving full value from our bare anal arrangement."
                                elif selected_girl.dominant_approach == "dominate":
                                    selected_girl.character "Acknowledged. Your approval of my bare anal offering is appreciated."
                            
                            "Should we consider protection for safety?" if norm_discipline > 5:
                                $ persuasion_score = 35 + (norm_discipline * 4)
                                if persuasion_score > 55:
                                    $ selected_girl.wants_anal_condom = True
                                    $ selected_girl.apply_impacts({"discipline": 25, "fear": 15})
                                    if selected_girl.dominant_approach == "compassionate":
                                        selected_girl.character "You're right, Professor. Safety is important. I'll use protection for anal."
                                    elif selected_girl.dominant_approach == "sexualized":
                                        selected_girl.character "I guess you're right... if it's for safety, I'll use protection for anal."
                                    elif selected_girl.dominant_approach == "transactional":
                                        selected_girl.character "For safety reasons, I'll adjust to protected anal access. Pricing remains standard."
                                    elif selected_girl.dominant_approach == "dominate":
                                        selected_girl.character "If anal protection is required for safety, I will comply."
                                else:
                                    if selected_girl.dominant_approach == "compassionate":
                                        selected_girl.character "I'm not comfortable with that suggestion, Professor. I trust you completely."
                                    elif selected_girl.dominant_approach == "sexualized":
                                        selected_girl.character "But bare anal feels so good! Do we have to?"
                                    elif selected_girl.dominant_approach == "transactional":
                                        selected_girl.character "Safety concerns would require additional compensation for the change in anal service."
                                    elif selected_girl.dominant_approach == "dominate":
                                        selected_girl.character "I prefer bare anal as previously established. I do not wish to change."
    
    # Track that this follow-up conversation happened
    $ actions_already_done.setdefault(selected_girl.id, []).append("condoms_followup")
    
    # Schedule next follow-up based on discussion level
    if selected_girl.condoms_discussion_level == 1:
        $ selected_girl.condoms_followup = time_manager.total_days + 5
    elif selected_girl.condoms_discussion_level == 2:
        $ selected_girl.condoms_followup = time_manager.total_days + 7
    else:
        # At max discussion level, no more scheduled follow-ups
        $ renpy.log(f"No further condoms follow-ups scheduled for {selected_girl.first_name}")
    
    # Skip time for conversation
    $ time_manager.skip_time(minutes=5)
    
    return

#the end of file cause labels suck at collapsing :P
