init 5 python:
#making it a habit to init hijank label lower priority
    config.label_overrides["small_talk_corruption"] = "vt_small_talk_corruption"

label vt_small_talk_corruption:
    "You bring up some topics that might push her boundaries."

    if selected_girl.corruption < 15:
        "[selected_girl] looks uncomfortable with the direction of the conversation."

        if selected_girl.discipline > 70:
            selected_girl.character "This is completely inappropriate. I refuse to discuss such matters."
            $ selected_girl.apply_impacts({"discipline": (250, 750)})
        elif selected_girl.fear > 60:
            selected_girl.character "Please... don't say things like that. It scares me."
            $ selected_girl.apply_impacts({"fear": (250, 750)})
        elif selected_girl.affection > 40:
            selected_girl.character "I'm disappointed you'd talk about this. I thought you were different."
            $ selected_girl.apply_impacts({"affection": (-750, -250)})
        elif selected_girl.intellect > 70:
            selected_girl.character "This conversation lacks any intellectual merit. Let's discuss something meaningful."
            $ selected_girl.apply_impacts({"intellect": (250, 750)})
        elif selected_girl.naturism > 60:
            selected_girl.character "Such unnatural thoughts... They disturb the harmony I seek."
            $ selected_girl.apply_impacts({"naturism": (-750, -250)})
        else:
            selected_girl.character "Can we talk about something else?"

        $ selected_girl.apply_impacts({"affection": (-750, -250), "fear": (250, 750)})
    else:
        if selected_girl.corruption < 30:
            "[selected_girl] looks a little surprised but curious to hear more."

            if selected_girl.discipline > 50 and selected_girl.affection > 20:
                selected_girl.character "I shouldn't be interested in this... but I am. Why?"
                $ selected_girl.apply_impacts({"discipline": (250, 750), "affection": (250, 750)})
            elif selected_girl.intellect > 60:
                selected_girl.character "How interesting... from a purely academic perspective, of course."
                $ selected_girl.apply_impacts({"intellect": (250, 750)})
            elif selected_girl.fear > 40:
                selected_girl.character "This is wrong... but part of me wants to know more anyway."
                $ selected_girl.apply_impacts({"fear": (250, 750)})
            elif selected_girl.naturism > 50:
                selected_girl.character "Nature has its dark sides too, doesn't it? Tell me more..."
                $ selected_girl.apply_impacts({"naturism": (250, 750)})
            else:
                selected_girl.character "How interesting..."
        elif selected_girl.corruption < 45:
            "[selected_girl] looks intrigued, wanting to hear more."

            if selected_girl.discipline > 40 and selected_girl.corruption > 35:
                selected_girl.character "I'm starting to understand why people find this tempting..."
                $ selected_girl.apply_impacts({"discipline": (250, 750)})
            elif selected_girl.affection > 40 and selected_girl.fear < 30:
                selected_girl.character "With you, even these thoughts feel exciting somehow."
                $ selected_girl.apply_impacts({"affection": (250, 750), "fear": (-750, -250)})
            elif selected_girl.intellect > 60:
                selected_girl.character "The psychological implications are fascinating. Humans are such complex creatures."
                $ selected_girl.apply_impacts({"intellect": (250, 750)})
            elif selected_girl.naturism > 60:
                selected_girl.character "The wildness in nature reflects the wildness in us, doesn't it?"
                $ selected_girl.apply_impacts({"naturism": (250, 750)})
            else:
                selected_girl.character "That is {b}so{/b} interesting!"
        elif selected_girl.corruption < 60:
            "[selected_girl] looks intrigued, her curiosity clearly piqued."

            if selected_girl.discipline > 30 and selected_girl.affection > 50:
                selected_girl.character "I never thought I'd say this, but you're making me question my values."
                $ selected_girl.apply_impacts({"discipline": (250, 750), "affection": (250, 750)})
            elif selected_girl.fear > 30 and selected_girl.corruption > 50:
                selected_girl.character "This scares me, but I can't stop thinking about it. About us."
                $ selected_girl.apply_impacts({"fear": (250, 750)})
            elif selected_girl.intellect > 50 and selected_girl.corruption > 50:
                selected_girl.character "Rationality tells me this is wrong, but my curiosity overwhelms reason."
                $ selected_girl.apply_impacts({"intellect": (250, 750)})
            elif selected_girl.naturism > 50 and selected_girl.affection > 40:
                selected_girl.character "You bring out the wild side in me I've always tried to suppress."
                $ selected_girl.apply_impacts({"naturism": (250, 750), "affection": (250, 750)})
            else:
                selected_girl.character "Tell me more about this. I want to understand completely."
        elif selected_girl.corruption < 75:
            "[selected_girl] looks completely captivated by the conversation."

            if selected_girl.discipline > 20 and selected_girl.corruption > 65:
                selected_girl.character "Rules are just society's attempt to control what feels natural. With you, I feel free."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.fear < 20 and selected_girl.affection > 60:
                selected_girl.character "I used to be afraid of these thoughts, but with you, I embrace them completely."
                $ selected_girl.apply_impacts({"fear": (250, 750), "affection": (250, 750)})
            elif selected_girl.intellect > 60 and selected_girl.discipline < 30:
                selected_girl.character "My mind understands the risks, but my body only understands desire."
                $ selected_girl.apply_impacts({"intellect": (250, 750), "discipline": (-750, -250)})
            elif selected_girl.naturism > 70:
                selected_girl.character "You've helped me understand that all of nature's impulses - even the dark ones - are beautiful."
                $ selected_girl.apply_impacts({"naturism": (250, 750)})
            else:
                selected_girl.character "That is right up my alley, tell me more."
            
        else:
            "[selected_girl] looks at you with a mischievous, knowing smile."

            if selected_girl.discipline < 20 and selected_girl.corruption > 80:
                selected_girl.character "I used to care about right and wrong. Now I only care about what feels good with you."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.fear < 10 and selected_girl.affection > 70:
                selected_girl.character "There's nothing I wouldn't try with you. You've made me fearless."
                $ selected_girl.apply_impacts({"fear": (250, 750), "affection": (250, 750)})
            elif selected_girl.intellect > 60 and selected_girl.corruption > 85:
                selected_girl.character "Intelligence without corruption is boring. You've awakened my true potential."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            elif selected_girl.naturism > 70 and selected_girl.discipline < 20:
                selected_girl.character "In nature, the strongest survive and the most passionate thrive. We're both."
                $ selected_girl.apply_impacts({"naturism": (250, 750), "discipline": (-750, -250)})
            else:
                selected_girl.character "I never knew this part of me existed before you. Now I can't imagine life without it."
        # Diminishing returns at highest corruption levels
        $ selected_girl.apply_impacts({"corruption": (250, 750), "fear": (-750, -250), "discipline": (-600, -300)})

    return
