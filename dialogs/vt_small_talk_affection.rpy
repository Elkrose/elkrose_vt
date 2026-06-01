init 5 python:
#making it a habit to init hijank label lower priority
    config.label_overrides["small_talk_affection"] = "vt_small_talk_affection"

label vt_small_talk_affection:
    "You bring up some topics that might interest her."

    if selected_girl.affection < 15:
        "[selected_girl] seems guarded and keeps her distance."

        if selected_girl.fear > 60:
            selected_girl.character "Please... I don't want to talk about this. Can't we just leave it alone?"
            $ selected_girl.apply_impacts({"fear": (250, 750)})
        elif selected_girl.discipline > 60:
            selected_girl.character "This conversation is inappropriate. I'd prefer if we discussed something else."
            $ selected_girl.apply_impacts({"discipline": (250, 750)})
        elif selected_girl.corruption > 60:
            selected_girl.character "If you're trying to get something from me, just say it directly. I don't have time for games."
            $ selected_girl.apply_impacts({"corruption": (250, 750)})
        elif selected_girl.intellect > 70:
            selected_girl.character "I fail to see the practical value in this conversation. Can we move on?"
            $ selected_girl.apply_impacts({"intellect": (250, 750)})
        elif selected_girl.naturism > 60:
            selected_girl.character "Human interactions feel so forced sometimes. I'd rather be in nature."
            $ selected_girl.apply_impacts({"naturism": (250, 750)})
        else:
            selected_girl.character "I'm not comfortable discussing this with you."
        
        $ selected_girl.apply_impacts({"affection": -500, "fear": (250, 750)})
    else:
        if selected_girl.affection < 30:
            "[selected_girl] seems to be warming up to you slightly."

            if selected_girl.intellect > 70 and selected_girl.discipline > 50:
                selected_girl.character "That's an interesting perspective. I'd like to explore the logical implications further."
                $ selected_girl.apply_impacts({"intellect": (250, 750), "discipline": (250, 750)})
            elif selected_girl.naturism > 70:
                selected_girl.character "This reminds me of how connected we all are to nature's cycles. Have you ever noticed...?"
                $ selected_girl.apply_impacts({"naturism": (250, 750)})
            elif selected_girl.corruption > 40 and selected_girl.fear < 40:
                selected_girl.character "I might be interested... but what's in it for me?"
                $ selected_girl.apply_impacts({"corruption": (250, 750), "fear": (-750, -250)})
            elif selected_girl.fear > 50:
                $ selected_girl.apply_impacts({"fear": 250})
                selected_girl.character "I... suppose I can listen for a little while. Please don't make this uncomfortable."
            else:
                selected_girl.character "I've never really thought about it that way before."
            
            $ selected_girl.apply_impacts({"affection": (250, 750)})
        elif selected_girl.affection < 45:
            "[selected_girl] is becoming more engaged in the conversation."
            if selected_girl.discipline > 60 and selected_girl.corruption < 30:
                selected_girl.character "I find myself wanting to open up to you, even though it goes against my usual principles."
                $ selected_girl.apply_impacts({"corruption": (250, 750), "discipline": (-750, -250)})
            elif selected_girl.fear > 40 and selected_girl.affection > 35:
                selected_girl.character "I'm scared of these feelings, but I can't deny that I'm drawn to you."
                $ selected_girl.apply_impacts({"fear": (-750, -250)})
            elif selected_girl.naturism > 50 and selected_girl.intellect < 60:
                selected_girl.character "Being with you feels as natural as breathing. I've never felt this way before."
                $ selected_girl.apply_impacts({"naturism": (250, 750), "intellect": (-750, -250)})
            elif selected_girl.corruption > 50 and selected_girl.discipline < 40:
                selected_girl.character "You know how to say all the right things. I like that in a person."
                $ selected_girl.apply_impacts({"corruption": (250, 750), "discipline": (-750, -250)})
            else:
                selected_girl.character "I'm starting to enjoy our conversations more than I expected."
                
            $ selected_girl.apply_impacts({"affection": (250, 750)})
        elif selected_girl.affection < 60:
            "[selected_girl] is leaning in, clearly interested in what you're saying."

            if selected_girl.fear > 40 and selected_girl.affection > 50:
                selected_girl.character "Even though part of me is still afraid, being with you feels right."
                $ selected_girl.apply_impacts({"fear": (-750, -250)})
            elif selected_girl.discipline > 60 and selected_girl.corruption > 30:
                selected_girl.character "You're making me question everything I thought I knew about myself."
                $ selected_girl.apply_impacts({"corruption": (250, 750), "discipline": (-750, -250)})
            elif selected_girl.naturism > 60 and selected_girl.intellect > 60:
                selected_girl.character "The natural order and intellectual pursuits converge when I'm with you. It's fascinating."
                $ selected_girl.apply_impacts({"naturism": (250, 750), "intellect": (250, 750)})
            elif selected_girl.corruption > 60 and selected_girl.fear < 30:
                selected_girl.character "I like the way you think. We should explore these ideas more... privately."
                $ selected_girl.apply_impacts({"corruption": (250, 750), "fear": (-750, -250)})
            else:
                selected_girl.character "I find myself looking forward to our conversations. What does that mean?"
            
            $ selected_girl.apply_impacts({"affection": (250, 750)})
        elif selected_girl.affection < 75:
            "[selected_girl] is completely focused on you, her eyes bright with interest."

            if selected_girl.corruption > 70:
                selected_girl.character "I've learned that what we want matters more than what others think we should want. And right now, I want you."
                $ selected_girl.apply_impacts({"corruption": (250, 750)})
            elif selected_girl.discipline > 70 and selected_girl.corruption < 40:
                selected_girl.character "I've always followed the rules, but with you... I find myself wanting to break them all."
                $ selected_girl.apply_impacts({"corruption": (250, 750), "discipline": (-750, -250)})
            elif selected_girl.fear > 50 and selected_girl.affection > 65:
                selected_girl.character "Even though part of me is terrified, I've never felt more alive than when I'm with you."
                $ selected_girl.apply_impacts({"fear": (-750, -250)})
            elif selected_girl.naturism > 60 and selected_girl.discipline < 40:
                selected_girl.character "Our bodies know what our minds try to deny. I can feel how right this is between us."
                $ selected_girl.apply_impacts({"naturism": (250, 750), "discipline": (250, 750)})
            elif selected_girl.intellect > 70 and selected_girl.corruption > 40:
                selected_girl.character "The rational choice would be to maintain distance, but my emotions override that logic with you."
                $ selected_girl.apply_impacts({"corruption": (250, 750), "intellect": (-750, -250)})
            else:
                selected_girl.character "I've never felt this connection with anyone before. I want to explore it further."
            
            $ selected_girl.apply_impacts({"affection": (250, 750)})
        else:
            "[selected_girl] looks at you with complete trust and affection."

            if selected_girl.discipline > 70 and selected_girl.corruption > 50:
                selected_girl.character "You've shown me that rules are meant to be broken, and I've never felt more free."
                $ selected_girl.apply_impacts({"corruption": (250, 750), "discipline": (-750, -250)})
            elif selected_girl.fear > 40 and selected_girl.affection > 80:
                selected_girl.character "You've helped me overcome so many fears. With you, I feel brave enough to face anything."
                $ selected_girl.apply_impacts({"fear": (-750, -250)})
            elif selected_girl.naturism > 70 and selected_girl.intellect > 70:
                selected_girl.character "With you, I've found the perfect balance between intellect and instinct, mind and nature."
                $ selected_girl.apply_impacts({"naturism": (250, 750), "intellect": (-750, -250)})
            elif selected_girl.corruption > 80:
                selected_girl.character "I used to think there were limits to what I'd do, but with you, I want to explore every dark corner of desire."
                $ selected_girl.apply_impacts({"corruption": (250, 750)})
            elif selected_girl.fear < 20 and selected_girl.discipline > 60:
                selected_girl.character "You've made me feel safe enough to let go of control, and disciplined enough to know my own boundaries."
                $ selected_girl.apply_impacts({"discipline": (250, 750), "fear": (-750, -250)})
            else:
                selected_girl.character "I never imagined I could feel this way about someone. You've changed everything for me."
            
            # Diminishing returns at highest levels
            $ selected_girl.apply_impacts({"affection": (250, 750)})

    return
