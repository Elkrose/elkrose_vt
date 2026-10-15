#SPECIFIC CHERRY DIALOGS
# to catch mothers if not hasattr(self, "daughter"):

# Per-girl day of her last "How's the baby doing?" free check-in (girl.id -> total_days). Keyed off a
# store dict (not a girl attribute) so it leaves nothing on the girl objects if the mod is removed.
default vt_baby_checkin_days = {}
# Menu-`set` of pregnancy sub-menu captions already chosen this entry -- the menu hides items whose
# caption is in it (they disappear, unlike an `if`-gate which greys under menu_include_disabled=True).
default vt_preg_menu_seen = set()

init python:
    def vt_bc_pitch_hint(girl, leaning_ok, bc_need=None):
        # The greyed-tooltip text for a birth-control persuasion pitch: report the FIRST unmet gate
        # condition so the disabled option explains itself. The pitches are now ASKABLE once she's in
        # the conversation (no relationship/history wall on the ASK -- her willingness drives the answer),
        # so the only gates left are birth-control state, personality (transactional), and thematic fit.
        # bc_need: True = must be ON birth control, False = must be OFF, None = either.
        on_bc = bool(getattr(girl, "birth_control", False))
        if bc_need is True and not on_bc:
            return "Only when she's already on birth control."
        if bc_need is False and on_bc:
            return "Only when she's not already on birth control."
        if getattr(girl, "dominant_approach", None) == "transactional":
            return "She treats this as a transaction -- use the cash offers above instead."
        if not leaning_ok:
            return "It doesn't fit her -- she isn't inclined this way right now."
        return "Available."   # not greyed; this text is never shown

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

    # INITIAL GREETING - fire the scene-opener up front so it precedes any discovery /
    # confession beat. It used to print AFTER them, which read as restarting the conversation.
    # Skipped on the scheduled-follow-up path (it narrates its own approach) and when a
    # not-pregnant stranger is about to be refused at the CLOSED gate below.
    $ _preg_followup_pending = hasattr(selected_girl, "has_pregnancy_followup") and selected_girl.has_pregnancy_followup and has_discussed_pregnancy_before
    $ _preg_topic_refused = (not selected_girl.pregnant) and vt_topic_tier(selected_girl, player) == "closed"
    if not _preg_followup_pending and not _preg_topic_refused:
        "You approach [selected_girl] to discuss pregnancy and family matters."

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

    # Layer 1 hard CLOSED gate (VT-Pregnancy-System.md section 7): a girl who is effectively a
    # stranger -- low affection, low corruption and no sexual history, so her openness score
    # sits below the CLOSED cut -- refuses the reproductive subject out of hand, however corrupt
    # she is. The player has to build the relationship up first. Skipped while she is pregnant so
    # a discovery / confession / follow-up is never blocked.
    if not selected_girl.pregnant and vt_topic_tier(selected_girl, player) == "closed":
        if is_base_mother:
            selected_girl.character "That's a very personal subject, Professor, and I hardly know you. I'd rather not discuss my body or birth control with you."
        elif is_student:
            selected_girl.character "Um... that's really personal, Professor. I-I don't know you well enough to talk about... pregnancy and things like that."
        else:
            selected_girl.character "That's an awfully personal thing to ask, Professor. I'm not comfortable discussing it with someone I barely know."
        return
  
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

    # The pregnancy-discussion beat below is no longer forced at the landing -- it is reached
    # from the menu's "What are your thoughts on pregnancy?" item, so the opening no longer
    # presumes the topic. Jump past the extracted beat label straight to the menu.
    jump vt_preg_main_menu

label vt_preg_general_beat:
    # Two lines per visit: an OPENER, then she EXPOUNDS. The opener differs by visit -- a repeat
    # non-pregnant visit gets the "again?" greeting; a first visit (and any pregnant girl) gets the
    # role/pregnancy-aware opening. Then the Q&A expound runs, self-gated to non-pregnant, so a pregnant
    # girl stops after her pregnancy-aware opener. (Replaces the old three-line stack.)
    $ _pg_mode = "preg" if (selected_girl.pregnant and selected_girl.player_knows_pregnant and selected_girl.knows_pregnant) else ("reentry" if has_discussed_pregnancy_before else "first")
    $ selected_girl.has_discussed_pregnancy_before = True

    # The player raises the topic first (the menu caption isn't spoken aloud), so she reacts + expounds
    # AFTER being asked. Non-pregnant only -- a pregnant girl's opener answers a different, implicit ask.
    if _pg_mode != "preg":
        player.character "What are your thoughts on pregnancy in general?"

    # --- reentry: repeat-visit greeting (non-pregnant) ---
    if _pg_mode == "reentry":
        if previous_pregnancy_reaction == "positive":
            if selected_girl.baby_desire > 70:
                if selected_girl.dominant_approach == "compassionate":
                    selected_girl.character "You wanted to talk more about pregnancy? I've been dreaming about nothing but having your babies!"
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "Back to talk about making babies? I've been touching myself thinking about you breeding me..."
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "You want to discuss pregnancy again? I've been calculating the financial benefits of having your children..."
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "You wish to continue our pregnancy discussion. I have been preparing my body to bear your children."
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
        jump vt_preg_gb_qa

    # --- opener for a first visit + any pregnant girl: the role / pregnancy-aware opening. Then it
    #     falls straight into the expound below (the reentry greeting jumps past this to the expound). ---
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
                    selected_girl.character "As a mother, I understand pregnancy is a beautiful journey... I'd love to have a baby with you!"
                elif selected_girl.dominant_approach == "sexualized":
                    selected_girl.character "As a mother, I know how amazing pregnancy can be... my body changing, growing new life... I want that with you!"
                elif selected_girl.dominant_approach == "transactional":
                    selected_girl.character "As a mother, I understand the benefits of a bigger family. What are you offering to father a child with me?"
                elif selected_girl.dominant_approach == "dominate":
                    selected_girl.character "As a mother, I have experience with pregnancy. I am prepared to bear your children."
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
            # VOICE REWORK (VT-Pregnancy-System.md section 6 axis 2): word-crudeness now keys on
            # her corruption register (vt_voice), not the dominant_approach argmax that made a
            # barely-corrupt girl talk "sexualized". baby_desire still sets her stance (wants a
            # baby / neutral / not interested); vt_voice random-picks a register-appropriate line.
            python:
                if selected_girl.baby_desire > 70:
                    _preg_intro = vt_voice(selected_girl, {
                        "demure":   ["Pregnancy? I... think about it more than I'd admit. Starting a family someday is something I quietly hope for."],
                        "shy":      ["Pregnancy? Oh... um. I'd be lying if I said I hadn't thought about having that, someday."],
                        "neutral":  ["Pregnancy? Honestly, the idea has been on my mind. Starting a family doesn't scare me the way it used to."],
                        "direct":   ["Pregnancy? Mmm... I'll admit it, the thought of getting knocked up has been living in my head lately."],
                        "explicit": ["Pregnancy? God, yes. I've been thinking about what it'd feel like to actually get bred."],
                        "crude":    ["Pregnancy? Fuck, don't get me started. I've been aching to get knocked up and you know it."],
                    })
                elif selected_girl.baby_desire > 30:
                    _preg_intro = vt_voice(selected_girl, {
                        "demure":   ["Pregnancy? That's... a lot to think about. Someday, maybe, if everything were right."],
                        "shy":      ["Pregnancy? Um... it's not something I've really decided about. It's a big thing to imagine."],
                        "neutral":  ["Pregnancy? It's a serious topic. I'm not against the idea, but I'm in no rush."],
                        "direct":   ["Pregnancy? A someday-maybe, for me. Right now I'm just enjoying myself.", "Pregnancy? The risk of it is kind of thrilling, but settling down? Not yet."],
                        "explicit": ["Pregnancy? Hah, the risk is kind of hot... but actually getting knocked up? Not yet."],
                        "crude":    ["Pregnancy? I love playing with fire, but a baby's a whole other thing. Ask me when I'm hornier."],
                    })
                else:
                    _preg_intro = vt_voice(selected_girl, {
                        "demure":   ["Pregnancy? Oh... that's not something I'm ready for at all. I'd rather not, honestly."],
                        "shy":      ["Pregnancy? Um... no. That's a really big thing, and I'm just... not there."],
                        "neutral":  ["Pregnancy? No, thank you. That's about the last thing I want right now."],
                        "direct":   ["Pregnancy? Mmm, hard pass. I like the fun without the consequences.", "Pregnancy? No way, I'm having way too much fun to slow down for that."],
                        "explicit": ["Pregnancy? Ha, no. I'll fool around all you like, but I'm not trying to get knocked up."],
                        "crude":    ["Pregnancy? Fuck no. You can use me however you want, but keep the babies out of it."],
                    })
            selected_girl.character "[_preg_intro]"

label vt_preg_gb_qa:
    # EXPOUND -- her substantive answer, following the opener. Self-gated to non-pregnant, so a pregnant
    # girl stops after her pregnancy-aware opener (the "thoughts in general" Q&A doesn't fit her).
    # Phase 1: General talk about pregnancy (the player's question was asked up front, before the opener)
    if not selected_girl.pregnant or not (selected_girl.player_knows_pregnant and selected_girl.knows_pregnant):
        # VOICE REWORK (VT-Pregnancy-System.md section 6 axis 2): stance comes from baby_desire
        # (kept coherent with the intro -- a "hard pass" girl stays a hard pass here), words come
        # from her corruption register via vt_voice. Parents speak from experience; everyone else
        # speaks aspirationally, so a vaginal virgin never claims sex she has not had.
        python:
            # THREE tiers of experience, so a mother never claims she carried HIS child when she hasn't:
            #   player-parent (kids_with_player>0) -> "your baby / again"; a mother NOT by him -> speaks from
            #   her own past pregnancy but wants HIS baby next; never-pregnant -> purely aspirational.
            _preg_player_parent = selected_girl.kids_with_player > 0
            _preg_mother = is_base_mother or is_currently_a_mother
            if selected_girl.baby_desire > 70:
                if _preg_player_parent:
                    _preg_thoughts = vt_voice(selected_girl, {
                        "demure":   ["My thoughts? Carrying a child was the most profound thing I've ever done. I'd happily do it again, with you."],
                        "shy":      ["My thoughts? Oh... becoming a mother changed me. I think I'd love to feel that again."],
                        "neutral":  ["My thoughts? Honestly, it's been the most meaningful part of my life. I wouldn't mind growing our family."],
                        "direct":   ["My thoughts? I'd do it again in a heartbeat. Carrying your baby felt incredible."],
                        "explicit": ["My thoughts? God, I loved being bred. The idea of you putting another one in me is intoxicating."],
                        "crude":    ["My thoughts? Knock me up again? Fuck yes. I loved every second of being bred and I want more."],
                    })
                elif _preg_mother:
                    _preg_thoughts = vt_voice(selected_girl, {
                        "demure":   ["My thoughts? Carrying my little one was the most profound thing I've ever done. I'd cherish the chance to do it again -- with you, this time."],
                        "shy":      ["My thoughts? Oh... becoming a mother changed me. The thought of feeling that again, with you... it gives me butterflies."],
                        "neutral":  ["My thoughts? Honestly, motherhood has been the most meaningful part of my life. I'd love to grow my family with you."],
                        "direct":   ["My thoughts? I've done it before and I'd do it again in a heartbeat -- and the idea of it being yours this time? Incredible."],
                        "explicit": ["My thoughts? God, I loved being pregnant. The thought of you being the one to put a baby in me is intoxicating."],
                        "crude":    ["My thoughts? I loved every second of being bred. Put one in me yourself and I'd be in absolute heaven."],
                    })
                else:
                    _preg_thoughts = vt_voice(selected_girl, {
                        "demure":   ["My thoughts? I think about it more than I let on. The idea of a family makes my chest ache, in a good way."],
                        "shy":      ["My thoughts? Oh... I think it might be the most wonderful thing. I get butterflies just imagining it."],
                        "neutral":  ["My thoughts? Honestly, I find the idea beautiful. Starting a family feels like something I really want."],
                        "direct":   ["My thoughts? I want it, plain and simple. The idea of getting knocked up someday does something to me."],
                        "explicit": ["My thoughts? God, I think about getting bred way too much. A baby in me is the hottest thing I can imagine."],
                        "crude":    ["My thoughts? Fuck, I want to get knocked up so bad it's embarrassing. Breed me and I'd be in heaven."],
                    })
            elif selected_girl.baby_desire > 30:
                _preg_thoughts = vt_voice(selected_girl, {
                    "demure":   ["My thoughts? It's a beautiful thing... someday, with the right person. I'm just not in any hurry."],
                    "shy":      ["My thoughts? It's... a big thing to imagine. Part of me is curious, part of me is scared. Someday, maybe."],
                    "neutral":  ["My thoughts? It's a serious decision. I'm open to it eventually, but it would have to be the right time."],
                    "direct":   ["My thoughts? I could see it down the road. The idea isn't unsexy... but not yet.", "My thoughts? Maybe someday. Right now I'm enjoying myself too much to think hard about it."],
                    "explicit": ["My thoughts? The risk of it is kind of a turn-on, I'll admit. Actually doing it, though? Someday."],
                    "crude":    ["My thoughts? Playing with the risk is hot as hell. Whether I'd actually go through with it... ask me later."],
                })
            else:
                _preg_thoughts = vt_voice(selected_girl, {
                    "demure":   ["My thoughts? Honestly... it's just not something I want for myself right now. Maybe one day, but not now."],
                    "shy":      ["My thoughts? Um... I don't really see it for me, not for a long while. It's a lot to take on."],
                    "neutral":  ["My thoughts? It's a huge commitment, and frankly not one I want anytime soon. I have other plans."],
                    "direct":   ["My thoughts? Not for me, thanks. I like my life the way it is, fun and uncomplicated.", "My thoughts? Hard no. A kid would cramp everything I enjoy right now."],
                    "explicit": ["My thoughts? I'll have all the fun I want, but actually getting knocked up? No thanks.", "My thoughts? Sex is great. Babies? That's a hard no from me."],
                    "crude":    ["My thoughts? I'll fuck like it's going out of style, but a baby wrecking my body? Absolutely not."],
                })
        selected_girl.character "[_preg_thoughts]"

label vt_preg_gb_end:
    return

label vt_preg_main_menu:
    # Merge the two mutually-exclusive pregnancy entries into one item -- this game sets
    # config.menu_include_disabled = True, so a plain `if`-gated twin would render greyed-out
    # rather than hidden. One dynamic label sidesteps that. The "About your pregnancy..." feelings
    # conversation is entirely "our baby" content, so it only opens when the PLAYER is the father -- a
    # girl carrying someone else's child (preg_father != "player") gets the general item instead, and
    # never wrongly calls the baby yours.
    $ _preg_is_players = selected_girl.pregnant and selected_girl.player_knows_pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player"
    $ _preg_topic_label = "About your pregnancy..." if _preg_is_players else "What are your thoughts on pregnancy?"
    menu:
        # BIRTH CONTROL OPTIONS
        "What are your thoughts on birth control methods?":
            player.character "What are your thoughts on birth control methods?"
            # Reveal birth control status if player doesn't know yet
            if not selected_girl.bc_status_known:
                $ selected_girl.bc_status_known = True

            # If she KNOWS she's pregnant, birth control is moot -- she says so, and the whole start/stop/
            # breeding sub-menu is SKIPPED (no oblivious "let's prevent/risk pregnancy" questions). Pregnancy
            # talk lives under "About your pregnancy...". A secret pregnancy (she doesn't know) frames it normally.
            if selected_girl.pregnant and selected_girl.knows_pregnant:
                $ _line = vt_say(selected_girl, "bc_already_pregnant", player)
                selected_girl.character "[_line]"
                jump vt_preg_wrapup
            $ _line = vt_say(selected_girl, "bc_methods", player)
            selected_girl.character "[_line]"

            # The salvaged family pitch (below) uses a caption aware of whether she's a mother and how many
            # children she has -- a sibling vs another sibling -- so it reads right for base mothers and others.
            # Also compute each pitch's "leaning" bool ONCE (reused by both the menu gate and its hint, so
            # they can't drift) and the dynamic greyed-tooltip text that reports the actual blocking reason.
            python:
                if is_base_mother and total_kids == 1:
                    _bc_family_pitch = "Do you think your daughter would like a sibling?"
                elif total_kids >= 2:
                    _bc_family_pitch = "Do you think your children would like another sibling?"
                elif total_kids == 1:
                    _bc_family_pitch = "Do you think your child would like a sibling?"
                else:
                    _bc_family_pitch = "Have you ever thought about starting a family together?"

                _lean_natural = selected_girl.naturism > 50
                _lean_family = (vt_baby_desire_band(selected_girl) in ("thinking", "obsessed", "fixation", "obsession")) or is_base_mother
                _lean_thrill = vt_explicitness_register(selected_girl) in ("direct", "explicit", "crude")
                _lean_health = selected_girl.discipline > 50
                _bc_hint_natural = vt_bc_pitch_hint(selected_girl, _lean_natural, bc_need=True)
                _bc_hint_family  = vt_bc_pitch_hint(selected_girl, _lean_family)
                _bc_hint_thrill  = vt_bc_pitch_hint(selected_girl, _lean_thrill)
                _bc_hint_health  = vt_bc_pitch_hint(selected_girl, _lean_health, bc_need=False)

            menu:
                "Have you considered starting birth control?|Only if she's not already on birth control" if not selected_girl.birth_control:
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
                            "Grant her a grade bump of 15 percent?|Only available for students" if is_student:
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
                    
                "Would you consider stopping birth control?|Only if she's on birth control" if selected_girl.birth_control:
                    # Askable whenever she's on birth control and you're in this conversation -- no
                    # relationship/history wall on the ASK, matching the persuasion pitches (the mod is
                    # moving away from assuming these questions are player-directed; her corruption drives
                    # it). Her WILLINGNESS band alone decides how readily; dominant_approach is VOICE/framing
                    # only and no longer flips birth_control on its own (that no-floor flip was the old bug).
                    $ _breed_band = vt_willingness_band(selected_girl, "stop_bc_breed")
                    $ _breed_voice = selected_girl.dominant_approach
                    if _breed_band == "eager" and _breed_voice != "transactional":
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
                    elif _breed_voice == "transactional" and _breed_band in ("conditional", "eager"):
                        # A transactional girl monetizes even a willing yes -- price beat (band-gated).
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
                            "Grant her a grade bump of 50 percent?|Only available for students" if is_student:
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
                    elif _breed_band == "conditional":
                        # Open to it, but wants reassurance/commitment first -- BC stays on for now.
                        $ _breed_reg = vt_explicitness_register(selected_girl)
                        if _breed_reg in ("crude", "explicit", "direct"):
                            selected_girl.character "Mmm, maybe... but going bare to make a baby is a big step. Show me you really mean it, and I'm yours."
                        else:
                            selected_girl.character "I've thought about it... but I'd need to know we're truly committed before I'd ever stop. Can you give me that?"
                    else:
                        # Hesitant or refusing -- birth control stays on (was: low baby desire).
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

                # ---- Salvaged persuasion pitches (vt_small_talk_birth_control.rpy retired). Each is a
                #      themed entry point, askable once she's in this conversation (no relationship/history
                #      wall); her vt_willingness_band alone decides, consistent with the generic stop/start-BC
                #      options above. Transactional girls are excluded -- they use the cash beats above.
                #      She changes BC only on an "eager" band. ----
                "I think your body would feel better functioning naturally without artificial hormones.|[_bc_hint_natural]" if selected_girl.birth_control and _lean_natural and selected_girl.dominant_approach != "transactional":
                    player.character "I think your body would feel better functioning naturally without artificial hormones."
                    $ _bc_band = vt_willingness_band(selected_girl, "natural_cycle")
                    if _bc_band == "eager":
                        $ selected_girl.birth_control = False
                        $ selected_girl.apply_impacts({"naturism": (250, 750), "affection": (250, 750)})
                        $ _line = vt_say(selected_girl, "bc_pitch_natural_yes", player)
                    else:
                        $ _line = vt_say(selected_girl, "bc_pitch_natural_no", player)
                    selected_girl.character "[_line]"

                # Family pitch -- askable on OR off BC (on: pitch to stop; off: already off, pitch to try).
                "[_bc_family_pitch]|[_bc_hint_family]" if _lean_family and selected_girl.dominant_approach != "transactional":
                    player.character "[_bc_family_pitch]"
                    $ _bc_band = vt_willingness_band(selected_girl, "stop_bc_breed")
                    if selected_girl.birth_control:
                        if _bc_band == "eager":
                            $ selected_girl.birth_control = False
                            $ selected_girl.apply_impacts({"baby_desire": (750, 1500), "affection": (250, 750)})
                            $ _line = vt_say(selected_girl, "bc_pitch_family_yes", player)
                        else:
                            $ _line = vt_say(selected_girl, "bc_pitch_family_no", player)
                    else:
                        if _bc_band == "eager":
                            $ selected_girl.apply_impacts({"baby_desire": (750, 1500), "affection": (250, 750)})
                            $ _line = vt_say(selected_girl, "bc_pitch_family_yes_offbc", player)
                        else:
                            $ _line = vt_say(selected_girl, "bc_pitch_family_no_offbc", player)
                    selected_girl.character "[_line]"

                # Thrill pitch -- askable on OR off BC (on: pitch to stop; off: already off, savoring the risk).
                "Isn't there something exciting about the possibility of pregnancy without birth control?|[_bc_hint_thrill]" if _lean_thrill and selected_girl.dominant_approach != "transactional":
                    player.character "Isn't there something exciting about the possibility of pregnancy without birth control?"
                    $ _bc_band = vt_willingness_band(selected_girl, "stop_bc_breed")
                    if selected_girl.birth_control:
                        if _bc_band == "eager":
                            $ selected_girl.birth_control = False
                            $ selected_girl.apply_impacts({"corruption": (750, 1500), "affection": (250, 750)})
                            $ _line = vt_say(selected_girl, "bc_pitch_thrill_yes", player)
                        else:
                            $ _line = vt_say(selected_girl, "bc_pitch_thrill_no", player)
                    else:
                        if _bc_band == "eager":
                            $ selected_girl.apply_impacts({"corruption": (750, 1500), "affection": (250, 750)})
                            $ _line = vt_say(selected_girl, "bc_pitch_thrill_yes_offbc", player)
                        else:
                            $ _line = vt_say(selected_girl, "bc_pitch_thrill_no_offbc", player)
                    selected_girl.character "[_line]"

                "I'm concerned about your health and responsible reproductive choices.|[_bc_hint_health]" if not selected_girl.birth_control and _lean_health and selected_girl.dominant_approach != "transactional":
                    player.character "I'm concerned about your health and responsible reproductive choices."
                    $ _bc_band = vt_willingness_band(selected_girl, "start_bc")
                    if _bc_band == "eager":
                        $ selected_girl.birth_control = True
                        $ selected_girl.apply_impacts({"discipline": (250, 750)})
                        $ _line = vt_say(selected_girl, "bc_pitch_health_yes", player)
                    else:
                        $ _line = vt_say(selected_girl, "bc_pitch_health_no", player)
                    selected_girl.character "[_line]"

                "Never mind.":
                    selected_girl.character "Oh... okay. Well, let me know if you want to talk about anything else."
                    $ selected_girl.apply_impacts({"affection": (250, 750)})
                    return
                

        # Condoms and (when she's pregnant) pregnancy questions live behind sub-menus so the
        # top level stays short; each still asks one beat per visit.
        "About condoms...":
            jump vt_preg_condom_submenu
        "[_preg_topic_label]":
            if _preg_is_players:
                jump vt_preg_pregnancy_submenu
            else:
                call vt_preg_general_beat

        # Back out to the small-talk topic list. make_small_talk (the base dispatcher) counts a topic as
        # used the instant it returns and charges 10 minutes, which would wrongly burn a small-talk action
        # and can trip the daily "enough small talk" cap. So instead of a plain return we use the base's
        # own sanctioned hook -- a topic that returns a string gets `jump expression`'d there -- to route
        # through vt_preg_smalltalk_reenter, which undoes the accounting for this aborted visit first.
        "Go back...":
            return "vt_preg_smalltalk_reenter"

    # Reached by birth control (a protection topic) and the non-pregnant general beat; the reaction
    # guards on pregnant+known so it only speaks after a pregnant girl's protection question.
    call vt_preg_protection_reaction
    jump vt_preg_wrapup

label vt_preg_smalltalk_reenter:
    # Reached only via the "Go back..." string-return above. The base make_small_talk appends the topic
    # label (before the call) and then "small_talk" (after it) to actions_already_done; get_action_count
    # counts the latter toward the 2/day cap. Backing out isn't a real conversation, so pop this visit's
    # two trailing entries (guarded by equality so we never touch anything else) and re-show the topic
    # list. Jumping straight to make_small_talk also skips its 10-minute charge -- a free back-out.
    python:
        _st_log = actions_already_done.get(selected_girl.id)
        if _st_log:
            if _st_log[-1] == "small_talk":
                _st_log.pop()
            if _st_log and _st_log[-1] == "small_talk_pregnancy":
                _st_log.pop()
    jump make_small_talk

label vt_preg_condom_submenu:
    menu:
        # VAGINAL CONDOM PREFERENCES
        "What are your thoughts on condoms for vaginal sex?": 
            player.character "What are your thoughts on condoms for vaginal sex?"
            # Response based on dominant_approach, role, and pregnancy context
            $ selected_girl.player_knows_vaginal_condom = True
            if selected_girl.pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player": # Already pregnant with player's baby
                $ selected_girl.wants_vaginal_condom = False
            $ _line = vt_say(selected_girl, "vaginal_condom_pref", player)
            selected_girl.character "[_line]"
            
            # Skip the coercion menu only when she KNOWINGLY carries his baby -- same condition as the
            # by_player response above. A secret early pregnancy still reads as "none" (she doesn't know),
            # so she gets the normal response AND the coercion menu, consistently.
            if not (selected_girl.pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player"):
                # Stance-aware "accept" caption: don't offer "we'll always use condoms" to a girl who
                # wants BARE -- that contradicts her. (Dynamic caption avoids the greyed-option look that
                # an inline `if` would give under config.menu_include_disabled.)
                if selected_girl.wants_vaginal_condom:
                    $ _vag_accept_cap = "I respect your boundaries. We'll always use condoms when fucking your pussy."
                    $ _vag_third_cap = "Would you consider letting me fuck your bare pussy sometimes?"
                else:
                    $ _vag_accept_cap = "I respect that -- bare it is. Your call on how we stay careful."
                    $ _vag_third_cap = "Would you let me finish inside sometimes, instead of pulling out?"
                menu:
                    "[_vag_accept_cap]":
                        player.character "[_vag_accept_cap]"
                        # Respect whatever she actually wants -> don't mutate her preference: a bare-preferring
                        # girl KEEPS bare, a condom-wanting girl keeps her condom. Either way it's respect ->
                        # the same reward. Her spoken line is corrected below for the bare case.
                        $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                        # Response based on her dominant_approach, role, and family context
                        python:
                            # VOICE REWORK: dominant_approach stays the outer stance layer; role bucket
                            # (base_mother / student->"Professor" / other) and parent context fold into
                            # the pool choice; register (vt_voice) drives the words. No virgin concern --
                            # this is gratitude for future protection, not a claim of past experience.
                            _rb_parent = selected_girl.kids_with_player > 0
                            if selected_girl.dominant_approach == "compassionate":
                                if is_base_mother:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you for understanding. As the mother of your child, having you respect my boundaries for our family's future... it means the world to me."],
                                            "shy":      ["Oh... thank you. As the mother of your child, knowing you respect my boundaries like this... it means so much."],
                                            "neutral":  ["Thank you for understanding. As the mother of your child, I appreciate you respecting my boundaries for our family's future. It means the world to me."],
                                            "direct":   ["Thank you. As the mother of your child, you respecting this for our family's sake means everything."],
                                            "explicit": ["Thank you for respecting that. Knowing you'll keep me safe -- for our family -- honestly makes me want you more, not less."],
                                            "crude":    ["Thanks for getting it. We've got a kid; knowing you'll keep it wrapped when you fuck me means a lot."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you for understanding. As a mother, having you respect my responsibilities makes me feel even closer to you."],
                                            "shy":      ["Oh... thank you. Knowing you respect my responsibilities like this... it makes me feel so close to you."],
                                            "neutral":  ["Thank you for understanding. As an experienced mother, I appreciate you respecting my responsibilities. It makes me feel even more connected to you."],
                                            "direct":   ["Thank you. You respecting my responsibilities like this means a lot -- I feel closer to you for it."],
                                            "explicit": ["Thank you for respecting that. A man who honors my responsibilities... it actually makes me want you more."],
                                            "crude":    ["Thanks for getting it. Knowing you'll wrap it when you fuck me -- respecting my situation -- means a lot."],
                                        })
                                elif is_student:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you, Professor... that makes me feel so much better about us. I'm glad you're being so responsible for our family."],
                                            "shy":      ["Oh, thank you, Professor! That... that makes me feel so much better about us. I'm glad you're being responsible for our family."],
                                            "neutral":  ["Thank you, Professor! That makes me feel so much better about... us. I'm glad you're being so responsible for our family."],
                                            "direct":   ["Thank you, Professor. That makes me feel so much better about us -- I'm glad you're looking out for our family."],
                                            "explicit": ["Thank you, Professor. Knowing you'll keep me safe for our family's sake actually makes me want you even more."],
                                            "crude":    ["Thanks, Professor. We've got a kid -- knowing you'll keep it wrapped when you fuck me means a lot."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you for understanding... that makes me feel so much better about, you know. I'm glad you're being responsible with me."],
                                            "shy":      ["Oh... thank you! That makes me feel so much better about... you know. I'm glad you're being so responsible with me."],
                                            "neutral":  ["Thank you for understanding! That makes me feel so much better about... you know. I'm glad you're being so responsible with me."],
                                            "direct":   ["Thank you, Professor. That makes me feel so much better about... us. I'm glad you're being responsible with me."],
                                            "explicit": ["Thank you, Professor. Knowing you'll keep me safe actually makes me want you more, not less."],
                                            "crude":    ["Thanks, Professor. Knowing you'll keep it wrapped when you fuck me just makes me trust you more."],
                                        })
                                else:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you for understanding. Since we have a child, knowing you'll protect me like this makes me feel safe and so much closer to you."],
                                            "shy":      ["Oh... thank you. We have a little one, and knowing you'll protect me like this... it makes me feel so safe."],
                                            "neutral":  ["Thank you for understanding. Since we have a child, knowing you'll protect me like this makes me feel safe and even more connected to you."],
                                            "direct":   ["Thank you. We've got a child -- knowing you'll keep me protected like this means a lot. I feel closer to you."],
                                            "explicit": ["Thank you for respecting that. We've got our baby; knowing you'll keep me safe just makes me want you more."],
                                            "crude":    ["Thanks for getting it. We've got a kid -- knowing you'll wrap it when you fuck me means a lot."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you for understanding. Knowing you'll protect me like this makes me feel even closer to you."],
                                            "shy":      ["Oh... thank you. Knowing you'll protect me like this... it makes me feel so close to you."],
                                            "neutral":  ["Thank you for understanding. Knowing you'll protect me makes me feel even more connected to you."],
                                            "direct":   ["Thank you. Knowing you'll keep me protected like this means a lot -- I feel closer to you for it."],
                                            "explicit": ["Thank you for respecting that. Knowing you'll keep me safe actually makes me want you more, not less."],
                                            "crude":    ["Thanks for getting it. Knowing you'll keep it wrapped when you fuck me just makes me trust you more."],
                                        })
                            elif selected_girl.dominant_approach == "sexualized":
                                if is_base_mother:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Mmm... a man who respects the mother of his child. That's unexpectedly lovely. Knowing you'll be careful for our family... I like that."],
                                            "shy":      ["O-oh... a man who respects the mother of his child? That's... kind of hot, honestly. I like that you'll be careful for our family."],
                                            "neutral":  ["Mmm... a man who respects the mother of his child. That's unexpectedly hot. Knowing you'll be careful for our family... I like that a lot."],
                                            "direct":   ["Mmm... you respect the mother of your child enough to be careful for our family? That's hotter than you'd think."],
                                            "explicit": ["God, a man who'll keep the mother of his child safe... that's unexpectedly hot. Careful and confident -- I like that a lot."],
                                            "crude":    ["Fuck, a man who respects the mother of his kid enough to wrap it for our family? Hotter than it has any right to be. I like it."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Mmm... a gentleman who respects an experienced mother's boundaries. That's unexpectedly lovely. I like that."],
                                            "shy":      ["O-oh... a man who respects a mother's boundaries? That's... kind of hot, honestly. I like that."],
                                            "neutral":  ["Mmm... a gentleman who respects an experienced mother's boundaries. That's unexpectedly hot. I like that."],
                                            "direct":   ["Mmm... you respect a mother's boundaries like that? Hotter than you'd think. I like it."],
                                            "explicit": ["God, a man who honors an experienced mother's boundaries... that's unexpectedly hot. I like that a lot."],
                                            "crude":    ["Fuck, a man who respects a mother's limits enough to wrap it? Hotter than it should be. I like it."],
                                        })
                                elif is_student:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Mmm... you're being so sweet and responsible for our family. That's actually kind of hot, Professor. I like it a lot."],
                                            "shy":      ["O-oh... you're being so responsible for our family? That's... actually really hot, Professor. I like that a lot."],
                                            "neutral":  ["Mmm... you're being so sweet and responsible for our family! That's actually really hot. I like that a lot, Professor."],
                                            "direct":   ["Mmm... you, being responsible for our family? That's hotter than you'd think, Professor. I like it."],
                                            "explicit": ["God, you being careful and responsible for our family is doing things to me, Professor. That's really hot. I like it a lot."],
                                            "crude":    ["Fuck, you being all responsible for our kid is weirdly hot, Professor. Wrap it up and I still want you bad."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Mmm... you're being so sweet and responsible. That's actually kind of hot. I like it a lot."],
                                            "shy":      ["O-oh... you're being so responsible? That's... actually really hot. I like that a lot."],
                                            "neutral":  ["Mmm... you're being so sweet and responsible! That's actually really hot. I like that a lot."],
                                            "direct":   ["Mmm... you, being this responsible? That's hotter than you'd think. I like it."],
                                            "explicit": ["God, you being careful and responsible is doing things to me. That's really hot. I like it a lot, Professor."],
                                            "crude":    ["Fuck, you being all responsible is weirdly hot, Professor. Wrap it up and I still want you bad."],
                                        })
                                else:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Mmm... a man who respects the mother of his child. That's a new kind of lovely. I like it."],
                                            "shy":      ["O-oh... a man who respects the mother of his child? That's... a new kind of hot, honestly. I like it."],
                                            "neutral":  ["Mmm... a man who respects the mother of his child's pussy. That's a new kind of hot. I like it."],
                                            "direct":   ["Mmm... respecting the mother of your child like that? That's a new kind of hot. I like it."],
                                            "explicit": ["God, a man who'll keep the mother of his child safe and still take her... that's a new kind of hot. I like it."],
                                            "crude":    ["Fuck, respecting the mother of your kid enough to wrap it -- and still wreck her? New kind of hot. I like it."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Mmm... a gentleman who respects a woman's boundaries. That's unexpectedly lovely. I like it."],
                                            "shy":      ["O-oh... a man who respects my boundaries? That's... unexpectedly hot, honestly. I like it."],
                                            "neutral":  ["Mmm... a gentleman who respects pussy boundaries. That's unexpectedly hot. I like that."],
                                            "direct":   ["Mmm... you respect my boundaries like that? Hotter than you'd think. I like it."],
                                            "explicit": ["God, a man who honors my boundaries and still wants me... that's unexpectedly hot. I like it a lot."],
                                            "crude":    ["Fuck, a man who respects my limits enough to wrap it -- and still take me? Hotter than it should be. I like it."],
                                        })
                            elif selected_girl.dominant_approach == "transactional":
                                if is_base_mother:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Noted. As the mother of your child, I'll remember this consideration. A responsible father is a valuable thing -- you've raised your standing."],
                                            "shy":      ["Oh... okay. As the mother of your child, I'll remember you did this. A responsible father is... valuable. You've gone up in my estimation."],
                                            "neutral":  ["Fine. As the mother of your child, I'll remember this favor. A responsible father is a valuable asset, and you just increased your worth."],
                                            "direct":   ["Fine. I'm the mother of your child -- I'll remember this favor. Responsible fathers are valuable; your worth just went up."],
                                            "explicit": ["Noted. As the mother of your child, that consideration earns you credit -- responsible men who still fuck me well are an asset."],
                                            "crude":    ["Fine, I'll bank that one. You're the father of my kid and you'll still wrap it -- that's worth something. Your stock just went up."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Noted. As an experienced mother, I'll remember this consideration next time you want something. Responsible men are valuable."],
                                            "shy":      ["Oh... okay. As a mother already, I'll remember you did this. Responsible men are... valuable, you know."],
                                            "neutral":  ["Fine. As an experienced mother, I'll remember this favor next time you want something -- responsible men are valuable."],
                                            "direct":   ["Fine. I'm a mother already -- I'll remember this favor. Responsible men are valuable; keep that up."],
                                            "explicit": ["Noted. A responsible man who still takes me how he likes is worth more -- I'll remember the favor."],
                                            "crude":    ["Fine, I'll bank it. A man who'll still wrap it is worth keeping around -- I'll remember you did me this one."],
                                        })
                                elif is_student:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Okay. I'll remember you were so good about this for our family. That was smart of you, Professor."],
                                            "shy":      ["Oh... okay! I'll remember you were so good about this... for our family. That was really smart of you, Professor."],
                                            "neutral":  ["Okay! I'll remember you were so good about this for our family. That was really smart of you, Professor."],
                                            "direct":   ["Okay, noted. I'll remember you did right by our family here. Smart move, Professor."],
                                            "explicit": ["Okay, that earns you points, Professor. A man who looks after our family and still gets to enjoy me -- smart."],
                                            "crude":    ["Okay, I'll remember that one, Professor. Looking after our kid and still getting to fuck me -- smart play."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Okay. I'll remember you were so nice about this. That was good of you, Professor."],
                                            "shy":      ["Oh... okay! I'll remember you were so nice about this. That was really good of you, Professor."],
                                            "neutral":  ["Okay! I'll remember you were so nice about this. That was really good of you, Professor."],
                                            "direct":   ["Okay, noted. I'll remember you were good about this, Professor. That counts for something."],
                                            "explicit": ["Okay, that earns you points, Professor. A man who's considerate and still gets to enjoy me -- I'll remember."],
                                            "crude":    ["Okay, I'll bank that, Professor. Being decent about it and still getting to fuck me -- smart."],
                                        })
                                else:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Noted. I'll remember this consideration next time you want something. A man who takes care of his family is a good investment."],
                                            "shy":      ["Oh... okay. I'll remember you did this. A man who takes care of his family is... a good investment, you know."],
                                            "neutral":  ["Fine. I'll remember this favor next time you want something from me. A man who takes care of his family is a good investment."],
                                            "direct":   ["Fine, noted. I'll remember this favor. A man who takes care of his family is a good investment."],
                                            "explicit": ["Noted. A man who provides for his family and still gets to fuck me how he likes -- that's a good investment. I'll remember."],
                                            "crude":    ["Fine, I'll bank it. You look after the kid and still wrap it to fuck me -- good investment. I'll remember."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Noted. I'll remember this consideration next time you want something from me."],
                                            "shy":      ["Oh... okay. I'll remember you did this next time you want something from me."],
                                            "neutral":  ["Fine. I'll remember this favor next time you want something from me."],
                                            "direct":   ["Fine, noted. I'll remember this favor next time you want something from me."],
                                            "explicit": ["Noted. Considerate and you still get to enjoy me -- I'll remember the favor next time you want something."],
                                            "crude":    ["Fine, I'll bank it. You'll still wrap it to fuck me -- I'll remember that next time you want something."],
                                        })
                            elif selected_girl.dominant_approach == "dominate":
                                if is_base_mother:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you, Master. As the mother of your child, your care for my body and our family's future shows your wisdom. You have chosen well."],
                                            "shy":      ["Th-thank you, Master. As the mother of your child... your consideration for our family shows your wisdom. You've chosen well."],
                                            "neutral":  ["Thank you, Master. As the mother of your child, your consideration for my body and our family's future confirms your wisdom. You have made the right choice."],
                                            "direct":   ["Thank you, Master. Caring for the mother of your child and our family's future -- that confirms your wisdom. The right choice."],
                                            "explicit": ["Thank you, Master. A wise man guards the mother of his child even as he takes her. You have pleased me."],
                                            "crude":    ["Thank you, Master. You'll still wrap it and use me -- and protect our kid's future. Wise. You've pleased me."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you, Master. As a mother already, your care for my body and my family means everything to me."],
                                            "shy":      ["Th-thank you, Master. As a mother already... your consideration for my body and my family means so much."],
                                            "neutral":  ["Thank you, Master. As an experienced mother, your consideration for my pussy and my family means everything to me."],
                                            "direct":   ["Thank you, Master. Your care for my body and my family means everything -- a wise choice."],
                                            "explicit": ["Thank you, Master. A wise man protects what's his even as he uses it. That pleases me."],
                                            "crude":    ["Thank you, Master. You'll still wrap it and use me -- and protect mine. Wise. That pleases me."],
                                        })
                                elif is_student:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you, Professor. I'm glad you're being so thoughtful about our family. It shows you know what's best for us."],
                                            "shy":      ["Th-thank you, Professor! I'm glad you're being so thoughtful about our family. It shows you know what's best for us."],
                                            "neutral":  ["Thank you, Professor! I'm glad you're being so thoughtful about our family. It shows you know what's best for us."],
                                            "direct":   ["Thank you, Professor. You being this thoughtful about our family shows you know what's best for us."],
                                            "explicit": ["Thank you, Professor. A man who guards our family even as he takes me -- you know exactly what's best for us."],
                                            "crude":    ["Thank you, Professor. You'll still wrap it and use me, and look after our kid. You know what's best for us."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you, Professor. I'm glad you're being so thoughtful about... about me. It shows you know best."],
                                            "shy":      ["Th-thank you, Professor! I'm glad you're being so thoughtful about... about me."],
                                            "neutral":  ["Thank you, Professor! I'm glad you're being so thoughtful about... about me."],
                                            "direct":   ["Thank you, Professor. You being this thoughtful about me shows you know what's best."],
                                            "explicit": ["Thank you, Professor. A man who's careful with me even as he takes me -- you know what's best."],
                                            "crude":    ["Thank you, Professor. You'll still wrap it and use me right. You know what's best for me."],
                                        })
                                else:
                                    if _rb_parent:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you, Master. Your care for the mother of your child means everything to me. You have pleased me."],
                                            "shy":      ["Th-thank you, Master. Your consideration for the mother of your child means everything... you've pleased me."],
                                            "neutral":  ["Thank you, Master. Your consideration for the mother of your child means everything to me. You have pleased me."],
                                            "direct":   ["Thank you, Master. Your care for the mother of your child means everything -- you have pleased me."],
                                            "explicit": ["Thank you, Master. A wise man protects the mother of his child even as he takes her. You have pleased me."],
                                            "crude":    ["Thank you, Master. You'll still wrap it and use me -- and guard our kid. You've pleased me."],
                                        })
                                    else:
                                        _line = vt_voice(selected_girl, {
                                            "demure":   ["Thank you, Master. Your care for my body means everything to me. You have chosen wisely."],
                                            "shy":      ["Th-thank you, Master. Your consideration for my body means everything... you've chosen well."],
                                            "neutral":  ["Thank you, Master. Your consideration for my pussy means everything to me. You have pleased me."],
                                            "direct":   ["Thank you, Master. Your care for my body means everything -- you have chosen wisely."],
                                            "explicit": ["Thank you, Master. A wise man guards what's his even as he uses it. You have pleased me."],
                                            "crude":    ["Thank you, Master. You'll still wrap it and use me right. Wise. You've pleased me."],
                                        })
                            else:
                                if _rb_parent:
                                    _line = vt_voice(selected_girl, {
                                        "demure":   ["Thank you for respecting my boundaries about condoms, especially now that we have a child."],
                                        "shy":      ["Um... thank you for respecting my boundaries about condoms, especially now that we have a little one."],
                                        "neutral":  ["Thank you for respecting my boundaries about condoms, especially now that we have a child."],
                                        "direct":   ["Thanks for respecting my boundaries on condoms -- it matters more now that we've got a child."],
                                        "explicit": ["Thanks for respecting that. With a kid already, knowing you'll keep it wrapped means a lot."],
                                        "crude":    ["Thanks for getting it. We've got a kid -- keeping it wrapped when you fuck me is the right call."],
                                    })
                                else:
                                    _line = vt_voice(selected_girl, {
                                        "demure":   ["Thank you for respecting my boundaries about condoms."],
                                        "shy":      ["Um... thank you for respecting my boundaries about condoms."],
                                        "neutral":  ["Thank you for respecting my boundaries about condoms."],
                                        "direct":   ["Thanks for respecting my boundaries on condoms -- it means a lot."],
                                        "explicit": ["Thanks for respecting that. Knowing you'll keep it wrapped means a lot."],
                                        "crude":    ["Thanks for getting it. Keeping it wrapped when you fuck me is the right call."],
                                    })
                        # Bare-preferring girl: the gratitude-for-protection line above doesn't fit her, so
                        # speak a "thank you for respecting my bare preference" line instead.
                        if not selected_girl.wants_vaginal_condom:
                            $ _line = vt_voice(selected_girl, {
                                "demure":   ["Thank you for understanding. Bare it is, then -- I'll rely on you for the rest."],
                                "shy":      ["O-okay... thank you. I-I do like it bare... I'll trust you."],
                                "neutral":  ["Thank you. Bare's how I like it -- I'll trust you on the rest."],
                                "direct":   ["Good. Bare it is. I'll manage the risk -- you just don't wrap it up."],
                                "explicit": ["Mmm, good -- bare, the way I like it. I trust you to handle the rest."],
                                "crude":    ["Fuck yeah -- bare it is. Glad you're not gonna wrap it up on me."],
                            }, "Thank you -- bare it is.")
                        selected_girl.character "[_line]"

                    "But what if we wanted to make a baby? No condom when I cum in your pussy?":
                        # Check if she wants a baby and her approach
                        player.character "But what if we wanted to make a baby? No condom when I cum in my pussy?"
                        if selected_girl.baby_desire > 50 and selected_girl.dominant_approach in ["compassionate", "sexualized"]: # Emotionally invested reactions
                            $ selected_girl.wants_vaginal_condom = False
                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750)})
                            python:
                                # VOICE REWORK: only compassionate & sexualized reach here (gated by the
                                # baby_desire>50 + approach check above), and she is eager either way --
                                # stance is "yes, breed me". dominant_approach stays the outer voice layer;
                                # role bucket (base_mother / student->"Professor" / other) and the 3-way kids
                                # tier (another / sibling / first) fold into pool choice; register drives the
                                # words. No virgin split -- this is forward desire to be bred, not recollection.
                                if selected_girl.dominant_approach == "compassionate":
                                    if is_base_mother:
                                        if selected_girl.kids_with_player > 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["Another baby, to keep growing our family? As a mother already, I'd love nothing more. Please... finish inside me, bare."],
                                                "shy":      ["A-another baby? To grow our family? As a mother, I'd love that more than anything. Please... cum in me bare."],
                                                "neutral":  ["Another baby? To keep growing our family? As an experienced mother, I'd love nothing more. Please cum in my bare pussy."],
                                                "direct":   ["Another baby to grow our family? As a mother, I'd love nothing more. Cum in me bare -- put another one in me."],
                                                "explicit": ["Another baby for our family? God, yes -- as a mother I know how good this is. Cum in my bare pussy and breed me again."],
                                                "crude":    ["Another baby? Fuck yes, grow our family. I've done this before -- pump my bare pussy full and knock me up again."],
                                            })
                                        elif selected_girl.kids_with_player == 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A sibling for our little one? As a mother already, I'd love to give them one. Please... finish inside me, bare."],
                                                "shy":      ["A-a sibling for our child? As a mother, I'd love to give them one. Please... cum in me bare."],
                                                "neutral":  ["A sibling for our child? As an experienced mother, I'd love to give them one. Please cum in my bare pussy."],
                                                "direct":   ["A sibling for our child? As a mother, I'd love that. Cum in me bare and give them a brother or sister."],
                                                "explicit": ["A sibling for our baby? God, yes -- cum in my bare pussy. I want to feel you breed me again."],
                                                "crude":    ["A sibling? Fuck yes -- pump my bare pussy full and give our kid a brother or sister."],
                                            })
                                        else:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A baby with you... as a mother already, I'd love to give you a child. Please... finish inside me, bare."],
                                                "shy":      ["A-a baby with you? As a mother, I'd love to give you a child. Please... cum in me bare."],
                                                "neutral":  ["A baby with you... as an experienced mother, I'd love to give you a child. Please cum in my bare pussy."],
                                                "direct":   ["A baby with you? As a mother, I'd love to give you a child. Cum in me bare and put one in me."],
                                                "explicit": ["A baby with you? God, yes -- cum in my bare pussy. I know exactly how to carry your child, and I want to."],
                                                "crude":    ["A baby with you? Fuck yes -- pump my bare pussy full and put one in me. I've done this; breed me."],
                                            })
                                    elif is_student:
                                        if selected_girl.kids_with_player > 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["Another baby, Professor? To make our family even bigger? I'd love that. Please... cum in me, bare."],
                                                "shy":      ["A-another baby, Professor? To make our family bigger? I'd love that! Please cum in me bare!"],
                                                "neutral":  ["Another baby? Wow, Professor! To make our family even bigger? I'd love that! Please cum in my bare pussy!"],
                                                "direct":   ["Another baby, Professor? To grow our family? Yes! Cum in my bare pussy and put another one in me!"],
                                                "explicit": ["Another baby, Professor?! Our family even bigger? God yes -- cum in my bare pussy and breed me again!"],
                                                "crude":    ["Another one, Professor?! Fuck yes -- pump my bare pussy full and make our family huge!"],
                                            })
                                        elif selected_girl.kids_with_player == 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A sibling for our child, Professor? Really? I'd love that. Please... cum in me, bare."],
                                                "shy":      ["A-a sibling for our child? Oh my gosh, really? I'd love that! Please cum in me bare!"],
                                                "neutral":  ["A sibling for our child? Oh my god, really? I'd love that! Please cum in my bare pussy and give them a brother or sister!"],
                                                "direct":   ["A sibling for our child, Professor? Yes! Cum in my bare pussy and give them a brother or sister!"],
                                                "explicit": ["A sibling, Professor?! God yes -- cum in my bare pussy and put another baby in me for our little one!"],
                                                "crude":    ["A sibling?! Fuck yes, Professor -- pump my bare pussy full and give our kid a brother or sister!"],
                                            })
                                        else:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A baby with you, Professor? Really? I'd love that. Please... cum in me, bare."],
                                                "shy":      ["A-a baby with you? Oh my gosh, really? I'd love that! Please cum in me bare and put a baby in me!"],
                                                "neutral":  ["A baby with you? Oh my god, really? I'd love that! Please cum in my bare pussy and put a baby in me!"],
                                                "direct":   ["A baby with you, Professor? Yes! Cum in my bare pussy and put a baby in me!"],
                                                "explicit": ["A baby with you, Professor?! God yes -- cum in my bare pussy and breed me!"],
                                                "crude":    ["A baby?! Fuck yes, Professor -- pump my bare pussy full and put one in me!"],
                                            })
                                    else:
                                        if selected_girl.kids_with_player > 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["Another baby? I love the sound of that. Let's make our family even bigger. Please... cum in me, bare."],
                                                "shy":      ["A-another baby? To grow our family? I'd love that. Please cum in me bare."],
                                                "neutral":  ["Another baby? I love the sound of that. Let's make our beautiful family even bigger. Please cum in my bare pussy."],
                                                "direct":   ["Another baby to grow our family? I love that. Cum in my bare pussy and put another one in me."],
                                                "explicit": ["Another baby for our family? God yes -- cum in my bare pussy and breed me again."],
                                                "crude":    ["Another one? Fuck yes -- pump my bare pussy full and make our family bigger."],
                                            })
                                        elif selected_girl.kids_with_player == 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A baby with you... I'd love to give our child a sibling. Please... cum in me, bare."],
                                                "shy":      ["A-a sibling for our child? I'd love that. Please cum in me bare and put another baby in me."],
                                                "neutral":  ["A baby with you... I'd love to give our child a sibling. Please cum in my bare pussy and put another baby in me."],
                                                "direct":   ["A sibling for our child? I'd love that. Cum in my bare pussy and put another baby in me."],
                                                "explicit": ["A sibling? God yes -- cum in my bare pussy and give our little one a brother or sister."],
                                                "crude":    ["A sibling? Fuck yes -- pump my bare pussy full and give our kid a sibling."],
                                            })
                                        else:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A baby with you... I'd love nothing more. Please... cum in me, bare."],
                                                "shy":      ["A-a baby with you? I'd love nothing more! Please cum in me bare and put a baby in me."],
                                                "neutral":  ["A baby with you... I'd love nothing more! Please cum in my bare pussy and put a baby in me."],
                                                "direct":   ["A baby with you? I'd love that. Cum in my bare pussy and put a baby in me."],
                                                "explicit": ["A baby with you? God yes -- cum in my bare pussy and breed me."],
                                                "crude":    ["A baby? Fuck yes -- pump my bare pussy full and put one in me."],
                                            })
                                else:
                                    if is_base_mother:
                                        if selected_girl.kids_with_player > 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["Another baby? Knocking me up again? My body remembers this... fill me, bare, and make our family bigger."],
                                                "shy":      ["A-another baby? Getting me pregnant again? My body remembers... fill my pussy with your cum!"],
                                                "neutral":  ["Another baby? Knocking me up again? My body remembers this. Fill my pussy with your cum and make our family bigger!"],
                                                "direct":   ["Another baby? Knock me up again -- my body knows this dance. Fill my bare pussy and make our family bigger."],
                                                "explicit": ["Another baby? God, breed me again -- my body remembers being knocked up by you. Fill my bare pussy and make our family huge."],
                                                "crude":    ["Another one? Fuck yes, knock me up again -- I know exactly how good your cum feels. Breed my bare pussy and make our family huge."],
                                            })
                                        elif selected_girl.kids_with_player == 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A sibling? You'd knock me up again? As a mother already, I know how good it feels... fill me, bare."],
                                                "shy":      ["A-a sibling? Getting me pregnant again? I know how hot that is... fill my pussy with your cum!"],
                                                "neutral":  ["A sibling? You knocking me up again? As an experienced mother, I know exactly how hot that is. Fill my pussy with your cum!"],
                                                "direct":   ["A sibling? Knock me up again -- I know exactly how hot it is. Fill my bare pussy with your cum."],
                                                "explicit": ["A sibling? God, breed me again -- I remember how hot being knocked up by you is. Fill my bare pussy."],
                                                "crude":    ["A sibling? Fuck yes, breed me again -- I know how good your cum feels. Pump my bare pussy full."],
                                            })
                                        else:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A baby? You'd knock me up? As a mother already, I know how good it feels... fill me, bare."],
                                                "shy":      ["A-a baby? Getting me pregnant? I know how hot that is... fill my pussy with your cum!"],
                                                "neutral":  ["A baby? You knocking me up? As an experienced mother, I know exactly how hot that is. Fill my pussy with your cum!"],
                                                "direct":   ["A baby? Knock me up -- I know exactly how hot it is. Fill my bare pussy with your cum."],
                                                "explicit": ["A baby? God, breed me -- I remember how hot being knocked up is. Fill my bare pussy and put one in me."],
                                                "crude":    ["A baby? Fuck yes, breed me -- I know how good your cum feels. Pump my bare pussy full and knock me up."],
                                            })
                                    elif is_student:
                                        if selected_girl.kids_with_player > 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["Another baby? You're trying to get me pregnant again? That's... so hot. Cum inside me, make our family huge."],
                                                "shy":      ["A-another baby? Trying to get me pregnant again? Oh wow, that's so hot! Please cum inside me!"],
                                                "neutral":  ["Another baby? You're trying to get me pregnant again? Oh wow! That's so hot! Please cum inside me and make our family huge!"],
                                                "direct":   ["Another baby? Getting me pregnant again? So hot. Cum inside my bare pussy and make our family huge!"],
                                                "explicit": ["Another baby?! Knocking me up again is so fucking hot -- cum in my bare pussy and breed me, Professor!"],
                                                "crude":    ["Another one?! Fuck, knocking me up again is so hot -- pump my bare pussy full and make our family huge!"],
                                            })
                                        elif selected_girl.kids_with_player == 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A baby? You'd knock me up again? That's... so hot. Cum inside me and give our child a sibling."],
                                                "shy":      ["A-a baby? Getting me pregnant again? Oh wow, so hot! Please cum inside me and give our child a sibling!"],
                                                "neutral":  ["A baby? You knocking me up again? Oh wow! That's so hot! Please cum inside me and give our child a sibling!"],
                                                "direct":   ["A baby? Knocking me up again? So hot. Cum inside my bare pussy and give our child a sibling!"],
                                                "explicit": ["A sibling?! Knocking me up again is so fucking hot -- cum in my bare pussy, Professor!"],
                                                "crude":    ["A sibling?! Fuck, breed me again -- pump my bare pussy full and give our kid a sibling!"],
                                            })
                                        else:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A baby? You'd knock me up? That's... so hot. Cum inside me and put a baby in me."],
                                                "shy":      ["A-a baby? Getting me pregnant? Oh wow, so hot! Please cum inside me and put a baby in me!"],
                                                "neutral":  ["A baby? You knocking me up? Oh wow! That's so hot! Please cum inside me and put a baby in me!"],
                                                "direct":   ["A baby? Knocking me up? So hot. Cum inside my bare pussy and put a baby in me!"],
                                                "explicit": ["A baby?! Knocking me up is so fucking hot -- cum in my bare pussy and breed me, Professor!"],
                                                "crude":    ["A baby?! Fuck, knock me up -- pump my bare pussy full and put one in me!"],
                                            })
                                    else:
                                        if selected_girl.kids_with_player > 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["Another baby? Knocking me up again? That's... so hot. Cum in me, bare, and put another in me."],
                                                "shy":      ["A-another baby? Getting me pregnant again? So hot! Please cum in my bare pussy!"],
                                                "neutral":  ["Another baby? You knocking me up again? That's so hot! Please cum in my bare pussy and put another baby in me!"],
                                                "direct":   ["Another baby? Knock me up again -- so hot. Cum in my bare pussy and put another one in me!"],
                                                "explicit": ["Another baby? God, breed me again -- cum in my bare pussy and put another one in me!"],
                                                "crude":    ["Another one? Fuck yes -- knock me up again. Pump my bare pussy full and breed me!"],
                                            })
                                        elif selected_girl.kids_with_player == 1:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A baby? Knocking me up again? That's... so hot. Cum in me, bare, and give our child a sibling."],
                                                "shy":      ["A-a baby? Getting me pregnant again? So hot! Please cum in my bare pussy!"],
                                                "neutral":  ["A baby? You knocking me up again? That's so hot! Please cum in my bare pussy and put another baby in me!"],
                                                "direct":   ["A baby? Knock me up again -- so hot. Cum in my bare pussy and put another one in me!"],
                                                "explicit": ["A sibling? God, breed me again -- cum in my bare pussy and put another one in me!"],
                                                "crude":    ["A sibling? Fuck yes -- knock me up again. Pump my bare pussy full and breed me!"],
                                            })
                                        else:
                                            _line = vt_voice(selected_girl, {
                                                "demure":   ["A baby? You'd knock me up? That's... so hot. Cum in me, bare, and put one in me."],
                                                "shy":      ["A-a baby? Getting me pregnant? So hot! Please cum in my bare pussy and put a baby in me!"],
                                                "neutral":  ["A baby? You knocking me up? That's so hot! Please cum in my bare pussy and put a baby in me!"],
                                                "direct":   ["A baby? Knock me up -- so hot. Cum in my bare pussy and put one in me!"],
                                                "explicit": ["A baby? God, breed me -- cum in my bare pussy and put one in me!"],
                                                "crude":    ["A baby? Fuck yes -- knock me up. Pump my bare pussy full and breed me!"],
                                            })
                            selected_girl.character "[_line]"

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
                    
                    "[_vag_third_cap]":
                        player.character "[_vag_third_cap]"
                        if selected_girl.wants_vaginal_condom:
                            # She wants a condom -> the original "go bare sometimes?" pitch.
                            call vt_preg_vag_gobare_pitch
                        else:
                            # She already prefers bare -> the next escalation: finish inside instead
                            # of pulling out. Shares vt_accepts_vaginal_creampie with the in-sex coercion.
                            $ _fi_band = vt_willingness_band(selected_girl, "stop_bc_breed", player)
                            if _fi_band == "eager":
                                $ vt_set_accepts_creampie(selected_girl, True)
                                $ selected_girl.apply_impacts({"corruption": (250, 750), "baby_desire": (250, 500)})
                                $ _line = vt_voice(selected_girl, {
                                    "demure":   ["...Very well. You needn't pull out any longer. Finish inside me."],
                                    "shy":      ["I... o-okay. You can finish inside... I want to feel it. From now on."],
                                    "neutral":  ["...Okay. You don't have to pull out anymore. Finish inside me."],
                                    "direct":   ["You know what -- yes. Stop pulling out. Finish inside from now on."],
                                    "explicit": ["God, yes... don't pull out anymore. I want you to finish inside me."],
                                    "crude":    ["Fuck yeah... stop pulling out. Finish inside me, every time. I want to feel it."],
                                }, "...yes. Finish inside me from now on.")
                                selected_girl.character "[_line]"
                            elif _fi_band == "conditional":
                                $ selected_girl.apply_impacts({"corruption": (100, 300)})
                                $ _line = vt_voice(selected_girl, {
                                    "demure":   ["Perhaps, on occasion. If the moment moves me. But do not assume it."],
                                    "shy":      ["I-I... maybe? If it feels really good... I might let you. Sometimes."],
                                    "neutral":  ["...Maybe sometimes. If the moment's right. But usually you pull out."],
                                    "direct":   ["Maybe. In the moment, if it feels right -- but no promises."],
                                    "explicit": ["Ohh... maybe sometimes. If the moment's right, you can finish inside."],
                                    "crude":    ["Mmm... maybe. If you're deep enough and I'm into it, don't pull out. We'll see."],
                                }, "...maybe, if the moment's right.")
                                selected_girl.character "[_line]"
                            else:
                                $ _line = vt_voice(selected_girl, {
                                    "demure":   ["No. You will withdraw. I'll not be finished inside."],
                                    "shy":      ["N-no... please, you have to pull out. I-I can't risk it."],
                                    "neutral":  ["No -- you pull out. I mean it."],
                                    "direct":   ["No. You pull out. That's the deal."],
                                    "explicit": ["No way -- you pull out. I'm not risking a baby."],
                                    "crude":    ["No. You pull out. I'm not getting knocked up for your nut."],
                                }, "No -- you pull out. That's the deal.")
                                selected_girl.character "[_line]"

        # ANAL CONDOM PREFERENCES
        "What about for anal sex?":
            player.character "What about for anal sex?"
            $ _line = vt_say(selected_girl, "anal_condom_pref", player)
            selected_girl.character "[_line]"
            
            $ selected_girl.player_knows_anal_condom = True
            
            # Skip the coercion menu only when she KNOWINGLY carries his baby -- same condition as the
            # by_player response above. A secret early pregnancy still reads as "none" (she doesn't know),
            # so she gets the normal response AND the coercion menu, consistently.
            if not (selected_girl.pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player"):
                # Stance-aware accept caption: never promise "always condoms" to a girl who wants bare.
                if selected_girl.wants_anal_condom:
                    $ _anal_accept_cap = "I respect your boundaries. We'll always use condoms when fucking your ass."
                else:
                    $ _anal_accept_cap = "I respect that -- bare it is for your ass. Your call on staying careful."
                menu:
                    "[_anal_accept_cap]":
                        if selected_girl.wants_anal_condom:
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
                        else:
                            # She prefers bare -> respect THAT, don't promise condoms.
                            $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                            $ _line = vt_voice(selected_girl, {
                                "demure":  ["Thank you for understanding. Bare it is, then -- back there, your way."],
                                "shy":  ["O-okay... thank you. I-I do like it bare... back there."],
                                "neutral":  ["Thank you. I like it bare in my ass -- I trust you."],
                                "direct":  ["Good. Bare it is for my ass -- no wrapping up."],
                                "explicit":  ["Mmm, good -- bare in my ass is how I like it. I trust you."],
                                "crude":  ["Fuck yeah -- bare in my ass, no rubber. Glad you're not gonna wrap it."],
                            }, "Thank you -- bare it is.")
                            selected_girl.character "[_line]"
                    
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
                                "Grant her a grade bump of 25 percent?|Only available for students" if is_student:
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
            player.character "And for oral sex?"
            $ _line = vt_say(selected_girl, "oral_condom_pref", player)
            selected_girl.character "[_line]"
            
            $ selected_girl.player_knows_oral_condom = True
            
            # Skip the coercion menu only when she KNOWINGLY carries his baby -- same condition as the
            # by_player response above. A secret early pregnancy still reads as "none" (she doesn't know),
            # so she gets the normal response AND the coercion menu, consistently.
            if not (selected_girl.pregnant and selected_girl.knows_pregnant and selected_girl.preg_father == "player"):
                # Stance-aware accept caption: never promise "always condoms" to a girl who wants bare.
                if selected_girl.wants_oral_condom:
                    $ _oral_accept_cap = "I respect your boundaries. We'll always use protection for oral."
                else:
                    $ _oral_accept_cap = "I respect that -- no rubber for oral, then. Your call."
                menu:
                    "[_oral_accept_cap]":
                        if selected_girl.wants_oral_condom:
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
                        else:
                            # She prefers bare -> respect THAT, don't promise condoms.
                            $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
                            $ _line = vt_voice(selected_girl, {
                                "demure":  ["Thank you for understanding. Bare it is -- I do prefer the taste of you."],
                                "shy":  ["O-okay... thank you. I-I like it better without one, honestly."],
                                "neutral":  ["Thank you. I like it bare in my mouth -- I trust you."],
                                "direct":  ["Good. No rubber for oral -- that's how I like it."],
                                "explicit":  ["Mmm, good -- I want to taste you, not latex. Bare it is."],
                                "crude":  ["Fuck yeah -- no rubber. I want your bare cock in my mouth."],
                            }, "Thank you -- bare it is.")
                            selected_girl.character "[_line]"
                    
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
                                "Grant her a grade bump of 25 percent?|Only available for students" if is_student:
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
            player.character "What about for body shots or other external ejaculation?"
            $ _line = vt_say(selected_girl, "body_condom_pref", player)
            selected_girl.character "[_line]"
            
            $ selected_girl.player_knows_body_condom = True
            
            # Stance-aware accept caption: never promise "always clean" to a girl who wants your cum on her skin.
            if selected_girl.wants_body_condom:
                $ _body_accept_cap = "I like keeping things clean and controlled."
            else:
                $ _body_accept_cap = "Bare skin it is, then -- I'll mark you your way."
            menu:
                "[_body_accept_cap]":
                    if selected_girl.wants_body_condom:
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
                    else:
                        # She wants your cum on her bare skin -> respect THAT, don't flip her to a condom.
                        $ selected_girl.apply_impacts({"affection": (250, 750)})
                        $ _line = vt_voice(selected_girl, {
                            "demure":  ["Thank you. My bare skin is yours to mark, then."],
                            "shy":  ["O-okay... thank you. I-I do like it on my skin..."],
                            "neutral":  ["Thank you. I like it on my bare skin -- I trust you."],
                            "direct":  ["Good. Bare skin it is -- mark me, no fuss."],
                            "explicit":  ["Mmm, good -- your cum on my bare skin is how I like it."],
                            "crude":  ["Fuck yeah -- all over my bare skin, no wrapping up. Glad you're into it."],
                        }, "Thank you -- bare skin it is.")
                        selected_girl.character "[_line]"

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
                            "Grant her a grade bump of 25 percent?|Only available for students" if is_student:
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


        "Go back...":
            jump vt_preg_main_menu

    # A condom question was answered ("Go back" jumps away above) -- run the protection closing.
    call vt_preg_protection_reaction
    jump vt_preg_wrapup

label vt_preg_pregnancy_submenu:
    # The menu `set` below hides items already CHOSEN this entry (they disappear -- unlike an `if`-gate,
    # which greys under the game's menu_include_disabled=True). Reset it on each fresh entry so the free
    # actions return next visit. (Non-underscore store var: survives a mid-menu save/load.)
    $ vt_preg_menu_seen = set()

label vt_preg_pregnancy_submenu_loop:
    menu:
        set vt_preg_menu_seen
        # FREE ACTIONS -- ask once per visit; picking one re-fires this menu and the `set` hides it (gone,
        # not greyed), without ending the conversation. Reordered: baby first, then general thoughts.
        "How's the baby doing?":
            # Free check-in costs no turn, so grant its warmth/baby_desire at most ONCE PER IN-GAME DAY.
            python:
                _today = getattr(time_manager, "total_days", 0)
                if vt_baby_checkin_days.get(selected_girl.id) != _today:
                    vt_baby_checkin_days[selected_girl.id] = _today
                    selected_girl.apply_impacts({"affection": (950, 1500), "baby_desire": (750, 1500)})

            $ _line = vt_say(selected_girl, "pregnancy_feelings_nurturing", player)
            if _line:
                selected_girl.character "[_line]"
            elif selected_girl.dominant_approach == "transactional":
                selected_girl.character "The baby's fine, but carrying your child isn't cheap. What are you contributing to keep us both healthy?"

                menu:
                    "Offer 1000 for baby supplies":
                        if player.cash >= 1000:
                            $ player.cash -= 1000
                            $ selected_girl.cash += 1000
                            $ selected_girl.apply_impacts({"baby_desire": (250, 750), "affection": (250, 750)})
                            selected_girl.character "1000 for baby supplies? That really helps. The baby's doing great, by the way."
                        else:
                            selected_girl.character "Don't ask about the baby if you're not willing to help support them. This isn't free."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})

                    "Leave it be.":
                        selected_girl.character "Fine. The baby's fine. But don't expect updates without contributions."
                        $ selected_girl.apply_impacts({"affection": (-750, -250)})
            else:
                selected_girl.character "It's... progressing normally. I'm trying not to get too attached yet, honestly."
            jump vt_preg_pregnancy_submenu_loop

        # PRENATAL VITAMINS -- contextual beat, shown when pregnant and you carry the item.
        "I brought these prenatal vitamins if you need them.|Requires prenatal vitamins in your inventory" if player.get_item_quantity("prenatal_vitamins") > 0:
            # VT pills live in the sidecar pill_counts (Player.get_item_quantity is patched to read them);
            # has_item/remove_item hit the empty BASE inventory, so we spend via the pill-count helpers.
            # B1 fix: don't spend the item up front -- a transactional girl can still DECLINE below (can't
            # pay / no grades), and a rejected offer shouldn't cost the vitamins. Default to "she takes them"
            # and flip false only on the explicit refusals; spend once at the end if she actually took them.
            $ _took_vitamins = True

            # Check different dominant_approach types
            if selected_girl.dominant_approach == "compassionate":
                # Genuinely grateful
                $ selected_girl.apply_impacts({"affection": (750, 1500), "prenatal_boost": 1})
                $ _line = vt_say(selected_girl, "pregnancy_feelings_prenatal_vitamins", player)
                selected_girl.character "[_line]"

            elif selected_girl.dominant_approach == "sexualized":
                # Turns it into something sexual
                $ selected_girl.apply_impacts({"prenatal_boost": 1, "corruption": (250, 750), "affection": (250, 750)})
                $ _line = vt_say(selected_girl, "pregnancy_feelings_prenatal_vitamins", player)
                selected_girl.character "[_line]"

            elif selected_girl.dominant_approach == "dominate":
                # Accepts without question
                $ selected_girl.apply_impacts({"prenatal_boost": 1, "affection": (750, 1500), "fear": (-750, -250)})
                $ _line = vt_say(selected_girl, "pregnancy_feelings_prenatal_vitamins", player)
                selected_girl.character "[_line]"

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
                            $ _took_vitamins = False   # can't pay -> she doesn't take them
                            if is_base_mother:
                                selected_girl.character "Don't offer what you can't deliver, Professor. An experienced mother knows prenatal care costs money I don't have."
                            elif is_student:
                                selected_girl.character "Oh... you don't have enough for that? That's okay... I'll try to get vitamins some other way, I guess."
                            else:
                                selected_girl.character "Don't offer what you can't deliver, Professor. Prenatal care costs money I don't have."
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})

                    # Only students get grade option
                    "Grant her a grade bump of 25 percent?|Only available for students" if is_student:
                        if hasattr(selected_girl, 'grades'):
                            # Check if already at max
                            if selected_girl.grades >= 100:
                                $ _took_vitamins = False   # she balks and offers nothing -> no vitamins taken
                                selected_girl.character "But... my grades are already at maximum! A bump won't help much... can you offer something else?"
                                $ selected_girl.apply_impacts({"affection": (-750, -250)})
                            else:
                                # Apply 25 point increase (not 25% of current grade)
                                $ new_grade = min(100, selected_girl.grades + 25)
                                $ selected_girl.grades = new_grade
                                $ selected_girl.apply_impacts({"prenatal_boost": 1, "baby_desire": (750, 1000), "corruption": (950, 1500)})
                                selected_girl.character "A grade bump for taking the prenatal vitamins? That works for me. Fine, I will take them... but I want the grade agreement in writing!"
                        else:
                            # Missing grade attributes
                            $ _took_vitamins = False
                            selected_girl.character "I... don't think you can change my grades? Can you? As a student, maybe just cash would help more?"
                            $ selected_girl.apply_impacts({"affection": (-750, -250)})

                    "Promise to give her an A+ for taking care of your baby|Only available for students" if is_student:
                        if hasattr(selected_girl, "grades"):
                            $ selected_girl.grades = min(100, selected_girl.grades + 100)
                            $ selected_girl.apply_impacts({"prenatal_boost": 1, "corruption": (950, 1500), "discipline": (-750, -250)})
                            selected_girl.character "A+ for taking care of your baby? As a student, that's amazing! Now that's a negotiation. Fine, I'll take the vitamins... but this better not be the only support I get."
                        else:
                            $ _took_vitamins = False
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
            # B1: spend the vitamin only if she actually took it (declines above set _took_vitamins False).
            python:
                if _took_vitamins:
                    _pc = vt_player_pill_counts(player)
                    if _pc.get("prenatal_vitamins", 0) > 0:
                        _pc["prenatal_vitamins"] -= 1
            jump vt_preg_pregnancy_submenu_loop

        "What are your thoughts on pregnancy?":
            call vt_preg_general_beat
            jump vt_preg_pregnancy_submenu_loop

        # These beats end the visit -- they fall through to the wrap-up below.

        # SUPPORTIVE APPROACH (INCREASES BABY_DESIRE)
        "This is a beautiful time in your life. How are you feeling about it?":
            $ selected_girl.apply_impacts({"affection": (750, 1500), "baby_desire": (750, 1500)})

            $ _line = vt_say(selected_girl, "pregnancy_feelings_supportive", player)
            if _line:
                selected_girl.character "[_line]"
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

        # FETISH APPROACH (RISKY BUT POTENTIALLY HIGH BABY_DESIRE GAIN)
        "I love the idea of you carrying my child inside you...":
            if selected_girl.dominant_approach == "sexualized":
                $ selected_girl.apply_impacts({"corruption": (950, 1500), "baby_desire": (950, 1500)})
                $ _line = vt_say(selected_girl, "pregnancy_feelings_fetish", player)
                selected_girl.character "[_line]"

            elif selected_girl.dominant_approach == "compassionate":
                $ selected_girl.apply_impacts({"baby_desire": (750, 1000), "affection": (750, 1500)})
                $ _line = vt_say(selected_girl, "pregnancy_feelings_fetish", player)
                selected_girl.character "[_line]"

            elif selected_girl.dominant_approach == "dominate":
                $ selected_girl.apply_impacts({"baby_desire": (550, 900), "affection": (550, 900)})
                $ _line = vt_say(selected_girl, "pregnancy_feelings_fetish", player)
                selected_girl.character "[_line]"

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

            $ _line = vt_say(selected_girl, "pregnancy_feelings_practical", player)
            if _line:
                selected_girl.character "[_line]"
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
            else:
                selected_girl.character "You're right. I need to be more responsible about this. Maybe we should reconsider."

        # STUDENT-SPECIFIC CONCERNS
        "What about school? How will you manage?|Only available when she's a student" if is_student:
            if selected_girl.dominant_approach == "dominate":
                $ selected_girl.apply_impacts({"affection": (950, 1500), "baby_desire": (750, 1500)})
                $ _line = vt_say(selected_girl, "pregnancy_feelings_school", player)
                selected_girl.character "[_line]"

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

                    "Grant her a grade bump of 25 percent?|Only available for students" if is_student:
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
                $ _line = vt_say(selected_girl, "pregnancy_feelings_school", player)
                selected_girl.character "[_line]"

            else:
                $ selected_girl.apply_impacts({"affection": (750, 1500)})
                selected_girl.character "I'm terrified about what this means for my future as a student... but I don't know what to do."

        "Go back...":
            jump vt_preg_main_menu

    jump vt_preg_wrapup

label vt_preg_protection_reaction:
    # FINAL REACTION (BASED ON OUTCOMES) -- her closing reaction to the PROTECTION discussion. Reached
    # only from the protection paths (birth control + the condom sub-menu), so it never tacks a
    # condom-stance line onto a pregnancy-feelings or "thoughts on pregnancy" beat. Guarded pregnant+known.
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
    return

label vt_preg_wrapup:
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
    if kids_with_player > 0:
        # "Ours" counts only the player's children -- not total_kids, which would fold in a
        # base mother's NPC-fathered daughter.
        $ child_reference = "your child" if kids_with_player == 1 else f"our {kids_with_player} children"
    elif is_base_mother:
        # Her own daughter -- read the identity flag directly, not an "unaccounted child"
        # count (the daughter now reliably lives in kids_with_npc).
        $ child_reference = "my daughter"
    elif kids_with_others > 0:
        $ child_reference = "that child" if kids_with_others == 1 else f"my {kids_with_others} children"
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
        "This aligns with my compassionate approach to relationships.|Requires your compassion above 6" if empathy > 6:
            player.character "I'm glad you've been reflecting on our previous conversation. Your well-being is important to me."
            
            if selected_girl.baby_desire > 70:
                selected_girl.character "I appreciate how understanding you are, Professor. It makes me feel safe discussing these things."
                $ selected_girl.apply_impacts({"affection": (550, 750), "fear": (-750, -250)})
            else:
                selected_girl.character "Thank you for being so understanding, Professor."
                $ selected_girl.apply_impacts({"affection": (350, 750), "fear": (-750, -250)})
            
        "This demonstrates proper discipline in our relationship.|Requires your control above 6" if control > 6:
            player.character "Good. I expect you to take this seriously and be responsible."
            
            if selected_girl.baby_desire > 70:
                selected_girl.character "I will, Professor. I want to do this the right way with you."
                $ selected_girl.apply_impacts({"discipline": (250, 750), "affection": (250, 750)})
            else:
                selected_girl.character "I'll try to meet your expectations, Professor..."
                $ selected_girl.apply_impacts({"fear": (250, 750), "affection": (-750, -250)})
                
        "This fits with my more adventurous perspective.|Requires your lust above 6" if lust > 6:
            player.character "I'm glad you're embracing the more... passionate aspects of our relationship."
            
            if pregnancy_phase > 0:
                selected_girl.character "It certainly makes things more intense now, doesn't it?"
                $ selected_girl.apply_impacts({"corruption": (450, 750), "affection": (350, 750)})
            else:
                selected_girl.character "I've been thinking about how much I enjoy our intimate moments."
                $ selected_girl.apply_impacts({"corruption": (250, 750), "affection": (250, 750)})
                
        # VAGINAL CONDOM PREFERENCES - FOLLOWUP EDITION
        "What are your thoughts on condoms for vaginal sex now?":
            player.character "What are your thoughts on condoms for vaginal sex now?"
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
            
            # Stance-aware accept caption: never promise "always condoms" to a girl who wants bare.
            if selected_girl.wants_vaginal_condom:
                $ _fuvag_accept_cap = "I respect your boundaries. We'll always use condoms when fucking your pussy."
                $ _fuvag_third_cap = "Would you consider letting me fuck your bare pussy sometimes?"
            else:
                $ _fuvag_accept_cap = "I respect that -- bare it is. Your call on how we stay careful."
                $ _fuvag_third_cap = "Would you let me finish inside sometimes, instead of pulling out?"
            menu:
                "[_fuvag_accept_cap]":
                    if selected_girl.wants_vaginal_condom:
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
                    else:
                        # She prefers bare -> respect THAT, don't promise condoms.
                        $ selected_girl.apply_impacts({"affection": (550, 1000), "fear": (-1000, -500)})
                        $ _line = vt_voice(selected_girl, {
                            "demure":  ["Thank you for understanding. Bare it is, then -- I'll rely on you for the rest."],
                            "shy":  ["O-okay... thank you. I-I do like it bare... I'll trust you."],
                            "neutral":  ["Thank you. Bare's how I like it -- I'll trust you on the rest."],
                            "direct":  ["Good. Bare it is. I'll manage the risk -- you just don't wrap it up."],
                            "explicit":  ["Mmm, good -- bare, the way I like it. I trust you to handle the rest."],
                            "crude":  ["Fuck yeah -- bare it is. Glad you're not gonna wrap it up on me."],
                        }, "Thank you -- bare it is.")
                        selected_girl.character "[_line]"
                
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
                                
                                "Promise to give her an A+...|Only available for students" if is_student:
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
                                "Promise to cover all medical expenses(2000) and give her an A+|Only available for students" if is_student:
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
                
                "[_fuvag_third_cap]":
                    player.character "[_fuvag_third_cap]"
                    if selected_girl.wants_vaginal_condom:
                        call vt_preg_fuvag_gobare_pitch
                    else:
                        $ _fi_band = vt_willingness_band(selected_girl, "stop_bc_breed", player)
                        if _fi_band == "eager":
                            $ vt_set_accepts_creampie(selected_girl, True)
                            $ selected_girl.apply_impacts({"corruption": (250, 750), "baby_desire": (250, 500)})
                            $ _line = vt_voice(selected_girl, {
                                "demure":   ["...Very well. You needn't pull out any longer. Finish inside me."],
                                "shy":      ["I... o-okay. You can finish inside... I want to feel it. From now on."],
                                "neutral":  ["...Okay. You don't have to pull out anymore. Finish inside me."],
                                "direct":   ["You know what -- yes. Stop pulling out. Finish inside from now on."],
                                "explicit": ["God, yes... don't pull out anymore. I want you to finish inside me."],
                                "crude":    ["Fuck yeah... stop pulling out. Finish inside me, every time."],
                            }, "...yes. Finish inside me from now on.")
                            selected_girl.character "[_line]"
                        elif _fi_band == "conditional":
                            $ selected_girl.apply_impacts({"corruption": (100, 300)})
                            $ _line = vt_voice(selected_girl, {
                                "demure":   ["Perhaps, on occasion. If the moment moves me. But do not assume it."],
                                "shy":      ["I-I... maybe? If it feels really good... I might let you. Sometimes."],
                                "neutral":  ["...Maybe sometimes. If the moment's right. But usually you pull out."],
                                "direct":   ["Maybe. In the moment, if it feels right -- but no promises."],
                                "explicit": ["Ohh... maybe sometimes. If the moment's right, you can finish inside."],
                                "crude":    ["Mmm... maybe. If you're deep enough and I'm into it, don't pull out."],
                            }, "...maybe, if the moment's right.")
                            selected_girl.character "[_line]"
                        else:
                            $ _line = vt_voice(selected_girl, {
                                "demure":   ["No. You will withdraw. I'll not be finished inside."],
                                "shy":      ["N-no... please, you have to pull out. I-I can't risk it."],
                                "neutral":  ["No -- you pull out. I mean it."],
                                "direct":   ["No. You pull out. That's the deal."],
                                "explicit": ["No way -- you pull out. I'm not risking a baby."],
                                "crude":    ["No. You pull out. I'm not getting knocked up for your nut."],
                            }, "No -- you pull out. That's the deal.")
                            selected_girl.character "[_line]"

    
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

label vt_preg_vag_gobare_pitch:
    # Verbatim go-bare pitch for a condom-wanting girl (extracted from the vaginal condom beat
    # so option 3 can branch cleanly). Runs in the vt_small_talk_pregnancy call context, so
    # is_base_mother / is_student / selected_girl / player are all in scope.
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

    return

label vt_preg_fuvag_gobare_pitch:
    # Verbatim follow-up-convo go-bare pitch for a condom-wanting girl (extracted so option 3
    # can branch). Runs in the vt_small_talk_pregnancy_followup call context.
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
            "Grant her an automatic 10 percent to her grades|Only available for students" if is_student:
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

    return
