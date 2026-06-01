init 5 python:
#making it a habit to init hijank label lower priority
    config.label_overrides["small_talk_fear"] = "vt_small_talk_fear"
    config.label_overrides["small_talk_fear_lower"] = "vt_small_talk_fear_lower"

label vt_small_talk_fear:
    "You bring up some topics as thinly veiled threats trying to scare her."

    if selected_girl.fear < 15:
        "[selected_girl] looks confused and unbothered."

        if selected_girl.discipline > 70:
            selected_girl.character "Is this supposed to intimidate me? It's rather pathetic."
            $ selected_girl.apply_impacts({"discipline": (-750, -250)})
        elif selected_girl.corruption > 60:
            selected_girl.character "I've heard worse threats from people who actually meant them. Try harder."
            $ selected_girl.apply_impacts({"corruption": (-750, -250)})
        elif selected_girl.intellect > 70:
            selected_girl.character "Your attempts at psychological manipulation are transparent and poorly executed."
            $ selected_girl.apply_impacts({"intellect": (250, 750)})
        elif selected_girl.affection > 40:
            selected_girl.character "Why are you saying these things? I thought you cared about me."
            $ selected_girl.apply_impacts({"affection": (-750, -250)})
        elif selected_girl.naturism > 60:
            selected_girl.character "Nature's true threats are far more impressive than this. You're like a storm that's lost its power."
            $ selected_girl.apply_impacts({"naturism": (-750, -250)})
        else:
            selected_girl.character "I don't understand why you're saying this. It's not scary at all."
        
    else:
        if selected_girl.fear < 30:
            "[selected_girl] looks slightly nervous but tries to hide it."

            if selected_girl.discipline > 50:
                selected_girl.character "I won't let you see that you're getting to me. I'm stronger than that."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.corruption > 40:
                selected_girl.character "Interesting approach. Most people try bribery first."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.affection > 30:
                selected_girl.character "Why are you doing this? I thought we had something special."
                $ selected_girl.apply_impacts({"affection": (-750, -250)})
            elif selected_girl.intellect > 60:
                selected_girl.character "I recognize what you're doing, but I must admit it's... somewhat effective."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            else:
                selected_girl.character "I'm not sure what you're trying to accomplish with this conversation."
        elif selected_girl.fear < 45:
            "[selected_girl] looks uncomfortable, her composure starting to crack."

            if selected_girl.discipline > 40:
                selected_girl.character "I'm trying to remain calm, but you're making it difficult."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.corruption > 50:
                selected_girl.character "You're playing a dangerous game. I hope you know what you're doing."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.affection > 40:
                selected_girl.character "Please don't say things like that. You're scaring me, but I still care about you."
                $ selected_girl.apply_impacts({"affection": (-750, -250)})
            elif selected_girl.fear > 35 and selected_girl.intellect > 50:
                selected_girl.character "My mind knows this is manipulation, but my body is responding anyway."
                $ selected_girl.apply_impacts({"intellect": (-750, -250), "fear": (250, 750)})
            else:
                selected_girl.character "I'd rather you didn't talk about these things."
        elif selected_girl.fear < 60:
            "[selected_girl] looks visibly worried and anxious."

            if selected_girl.discipline > 30:
                selected_girl.character "I'm trying to stay strong, but you're breaking down my defenses."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.corruption > 40:
                selected_girl.character "You're awakening something dark in me. I'm not sure how I feel about that."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.affection > 50:
                selected_girl.character "I know I should run, but part of me still wants to stay with you."
                $ selected_girl.apply_impacts({"affection": (-750, -250)})
            elif selected_girl.intellect > 50:
                selected_girl.character "I understand the psychology behind what you're doing, but knowing doesn't make it less effective."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            else:
                selected_girl.character "Please... can we talk about something else?"
        elif selected_girl.fear < 75:
            "[selected_girl] looks frightened, her hands trembling slightly."

            if selected_girl.discipline > 20:
                selected_girl.character "I've always prided myself on my control, but with you... I feel powerless."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.corruption > 50:
                selected_girl.character "There's a part of me that's terrified, and another part that's terrifyingly excited."
                $ selected_girl.apply_impacts({"corruption": (250, 750)})
            elif selected_girl.affection > 60:
                selected_girl.character "I should hate you for making me feel this way, but I can't. I still need you."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            elif selected_girl.intellect < 40:
                selected_girl.character "I don't understand what's happening. I just know I'm scared."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            else:
                selected_girl.character "I'll do whatever you want. Just please don't hurt me."
        else:
            "[selected_girl] looks terrified and on edge."

            if selected_girl.discipline > 10:
                selected_girl.character "All my principles, all my training... none of it matters when I'm with you."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.corruption > 60:
                selected_girl.character "I never knew fear and desire could feel so similar. You've taught me so much."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.affection > 70:
                selected_girl.character "I'm terrified of you, but I'm more terrified of losing you. Does that make sense?"
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            elif selected_girl.naturism > 50:
                selected_girl.character "You're like a force of nature. I can't resist you any more than I can resist a storm."
                $ selected_girl.apply_impacts({"naturism": (250, 750)})
            else:
                selected_girl.character "Please... I'll do anything. Just tell me what you want."
            
        # At highest fear levels, discipline might start to crack
        $ selected_girl.apply_impacts({"fear": (250, 750), "discipline": (250, 750), "affection": (-750, -250)})

    return

label vt_small_talk_fear_lower:
    "You bring up some topics in an attempt to appear less intimidating."

    if selected_girl.fear > 85:
        "[selected_girl] looks terrified and on edge."

        if selected_girl.discipline > 50:
            selected_girl.character "I don't understand why you're saying this. Is this another trick?"
            $ selected_girl.apply_impacts({"discipline": (-750, -250)})
        elif selected_girl.corruption > 60:
            selected_girl.character "I don't believe you're being sincere. What's your real angle?"
            $ selected_girl.apply_impacts({"corruption": (-750, -250)})
        elif selected_girl.affection < 30:
            selected_girl.character "Please don't hurt me. I'll do whatever you want."
            $ selected_girl.apply_impacts({"affection": (-750, -250), "fear": (-750, -250)})
        elif selected_girl.intellect > 60:
            selected_girl.character "This sudden change in approach seems strategically motivated rather than genuine."
            $ selected_girl.apply_impacts({"intellect": (-750, -250)})
        elif selected_girl.fear > 90:
            selected_girl.character "I don't understand why you're saying this. Please don't hurt me."
            $ selected_girl.apply_impacts({"fear": (250, 750)})
        else:
            selected_girl.character "I want to believe you, but I'm still scared."

        $ selected_girl.apply_impacts({"fear": (-750, -250), "affection": (250, 750), "discipline": (-750, -250)}) 
    else:
        if selected_girl.fear > 70:
            "[selected_girl] looks slightly less nervous."

            if selected_girl.discipline > 40:
                selected_girl.character "I appreciate your effort to be less intimidating, but trust takes time."
                $ selected_girl.apply_impacts({"discipline": (250, 750)})
            elif selected_girl.corruption > 50:
                selected_girl.character "This softer approach doesn't suit you. I liked the other you better."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.affection > 40:
                selected_girl.character "Thank you. It means a lot that you're trying to make me more comfortable."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            elif selected_girl.intellect > 50:
                selected_girl.character "I recognize this as a de-escalation technique, but I appreciate it nonetheless."
                $ selected_girl.apply_impacts({"intellect": (250, 750)})
            else:
                selected_girl.character "I'm still a little nervous, but this helps."
            
        elif selected_girl.fear > 55:
            "[selected_girl] looks visibly less worried and anxious."

            if selected_girl.discipline > 30:
                selected_girl.character "Your gentler side is unexpected. I'm curious to see more of it."
                $ selected_girl.apply_impacts({"discipline": (250, 750)})
            elif selected_girl.corruption > 40:
                selected_girl.character "Don't think this makes me weak. I'm just allowing you this small victory."
                $ selected_girl.apply_impacts({"corruption": (250, 750)})
            elif selected_girl.affection > 50:
                selected_girl.character "This is the person I hoped was inside you all along."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            elif selected_girl.intellect < 50:
                selected_girl.character "You're not as scary when you talk like this. I like it."
                $ selected_girl.apply_impacts({"intellect": (250, 750)})
            else:
                selected_girl.character "I feel like I can breathe a little easier now."
            
        elif selected_girl.fear > 40:
            "[selected_girl] looks more relaxed around you."

            if selected_girl.discipline > 20:
                selected_girl.character "I'm beginning to see different sides of you. It's... intriguing."
                $ selected_girl.apply_impacts({"discipline": (250, 750)})
            elif selected_girl.corruption > 30:
                selected_girl.character "I wonder which version of you is real - the terrifying one or this gentle one."
                $ selected_girl.apply_impacts({"corruption": (250, 750)})
            elif selected_girl.affection > 60:
                selected_girl.character "When you're like this, I can forget all the times you scared me."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            elif selected_girl.intellect > 50:
                selected_girl.character "Your adaptability is impressive. You switch between intimidation and reassurance effortlessly."
                $ selected_girl.apply_impacts({"intellect": (250, 750)})
            else:
                selected_girl.character "I feel safer with you now."
            
        elif selected_girl.fear > 25:
            "[selected_girl] looks considerably more comfortable in your presence."

            if selected_girl.discipline > 10:
                selected_girl.character "I'm letting my guard down with you. I hope you won't make me regret it."
                $ selected_girl.apply_impacts({"discipline": (250, 750)})
            elif selected_girl.corruption > 20:
                selected_girl.character "I almost miss the dangerous edge you had before. Almost."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.affection > 70:
                selected_girl.character "This is the person I knew was there. I'm so glad to finally meet you."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            elif selected_girl.naturism > 50:
                selected_girl.character "Like a storm passing, you've left behind calm and new growth. I like this version of you."
                $ selected_girl.apply_impacts({"naturism": (250, 750)})
            else:
                selected_girl.character "I'm starting to feel like I can trust you."
            
        else:
            "[selected_girl] looks relaxed and comfortable around you."

            if selected_girl.discipline > 0:
                selected_girl.character "I never thought I'd feel this comfortable with you. It's a pleasant surprise."
                $ selected_girl.apply_impacts({"discipline": (250, 750)})
            elif selected_girl.corruption > 10:
                selected_girl.character "Don't get too comfortable. I like you better when you're a little dangerous."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.affection > 80:
                selected_girl.character "This is the person I fell for. I'm so glad you're letting me see them more often."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            elif selected_girl.intellect > 50:
                selected_girl.character "Your emotional intelligence is surprising. You know exactly when to switch approaches."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            else:
                selected_girl.character "I feel safe with you. It's a nice feeling."
            
        # At lowest fear levels, discipline decreases as she feels more secure
        $ selected_girl.apply_impacts({"fear": (-750, -250), "affection": (250, 750), "discipline": (-750, -250)})
       

    return
