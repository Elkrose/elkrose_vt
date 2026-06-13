label vt_small_talk_naturism:
    "You bring up some topics related to nature and natural living."

    if selected_girl.naturism < 15:
        "[selected_girl] looks uncomfortable and hesitant."

        if selected_girl.discipline > 70:
            selected_girl.character "This seems impractical and unhygienic. I prefer modern comforts."
            $ selected_girl.apply_impacts({"naturism": (-750, -250)})
        elif selected_girl.corruption > 60:
            selected_girl.character "Why would anyone want to live like that? It sounds boring."
            $ selected_girl.apply_impacts({"naturism": (-750, -250)})
        elif selected_girl.intellect > 70:
            selected_girl.character "There's no scientific evidence supporting these lifestyle choices. It's sentimental nonsense."
            $ selected_girl.apply_impacts({"naturism": (-750, -250)})
        elif selected_girl.fear > 60:
            selected_girl.character "Being exposed to nature like that seems dangerous. What about animals and weather?"
            $ selected_girl.apply_impacts({"naturism": (-750, -250)})
        elif selected_girl.affection > 40:
            selected_girl.character "I know this is important to you, but I'm not sure about it."
            $ selected_girl.apply_impacts({"naturism": (-750, -250)})
        else:
            selected_girl.character "I'm not sure about this. Can we talk about something else?"
        
        $ selected_girl.apply_impacts({"naturism": (250, 750), "discipline": (250, 750)})
    else:
        if selected_girl.naturism < 30:
            "[selected_girl] looks a little surprised but curious to hear more."

            if selected_girl.discipline > 50:
                selected_girl.character "I don't normally consider such things, but there might be some merit to it."
                $ selected_girl.apply_impacts({"discipline": (250, 750)})
            elif selected_girl.corruption > 40:
                selected_girl.character "I suppose there's a certain freedom in it, but it seems limiting in other ways."
                $ selected_girl.apply_impacts({"corruption": (250, 750)})
            elif selected_girl.intellect > 60:
                selected_girl.character "From an evolutionary perspective, I can see the logic, but modern life has advantages."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            elif selected_girl.fear > 40:
                selected_girl.character "It sounds... interesting, but I'm not sure I could handle the wilderness."
                $ selected_girl.apply_impacts({"fear": (250, 750)})
            elif selected_girl.affection > 30:
                selected_girl.character "If it's important to you, I'd like to understand it better."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            else:
                selected_girl.character "This is unexpected, but I'm open to learning more."
            
        elif selected_girl.naturism < 45:
            "[selected_girl] looks intrigued, considering your words carefully."

            if selected_girl.discipline > 40:
                selected_girl.character "I'm finding myself drawn to these ideas, even though they conflict with my usual values."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.corruption > 30:
                selected_girl.character "There's something primal about it that appeals to me. I never expected that."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.intellect > 50:
                selected_girl.character "The more I learn, the more I realize how disconnected we've become from our roots."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            elif selected_girl.fear > 30:
                selected_girl.character "I'm still a bit nervous about it, but I'm starting to see the appeal."
                $ selected_girl.apply_impacts({"fear": (250, 750)})
            elif selected_girl.affection > 40:
                selected_girl.character "When you explain it like that, I can feel how important it is to you."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            else:
                selected_girl.character "I'm really enjoying this conversation. Tell me more!"
            
        elif selected_girl.naturism < 60:
            "[selected_girl] looks intrigued and interested, leaning forward."

            if selected_girl.discipline > 30:
                selected_girl.character "I'm starting to question the artificial boundaries we've created for ourselves."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.corruption > 20:
                selected_girl.character "There's a raw honesty to natural living that I find refreshing."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.intellect > 40:
                selected_girl.character "The ecological and psychological benefits are becoming clearer to me now."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            elif selected_girl.fear > 20:
                selected_girl.character "I used to be afraid of nature, but now I feel like I'm part of it."
                $ selected_girl.apply_impacts({"fear": (-750, -250)})
            elif selected_girl.affection > 50:
                selected_girl.character "Being with you in nature feels so right, like we're meant to be this way."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            else:
                selected_girl.character "I'm really enjoying this conversation. Tell me more!"
            
        elif selected_girl.naturism < 75:
            "[selected_girl] looks completely at ease and engaged."

            if selected_girl.discipline > 20:
                selected_girl.character "I used to think control and order were everything, but nature has taught me the beauty of chaos."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.corruption > 10:
                selected_girl.character "I used to think power came from dominance, but now I see it comes from harmony with nature."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.intellect > 30:
                selected_girl.character "My mind once rejected these ideas, but my body and soul have embraced them."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            elif selected_girl.fear > 10:
                selected_girl.character "The wilderness no longer frightens me. It feels like home."
                $ selected_girl.apply_impacts({"fear": (-750, -250)})
            elif selected_girl.affection > 60:
                selected_girl.character "Being natural with you feels more real than anything I've experienced before."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            else:
                selected_girl.character "This is exactly what I love to talk about. Let's dive deeper."
            
        else:
            "[selected_girl] looks completely at ease, her movements natural and fluid."

            if selected_girl.discipline > 10:
                selected_girl.character "I've learned that true discipline comes from listening to nature, not fighting against it."
                $ selected_girl.apply_impacts({"discipline": (-750, -250)})
            elif selected_girl.corruption > 0:
                selected_girl.character "The artificial pleasures I once sought seem hollow compared to the joy of natural living."
                $ selected_girl.apply_impacts({"corruption": (-750, -250)})
            elif selected_girl.intellect > 20:
                selected_girl.character "I used to think humanity was above nature, but now I know we are nature."
                $ selected_girl.apply_impacts({"intellect": (-750, -250)})
            elif selected_girl.fear > 0:
                selected_girl.character "I once feared the wild, but now I fear a life without it more."
                $ selected_girl.apply_impacts({"fear": (-750, -250)})
            elif selected_girl.affection > 70:
                selected_girl.character "With you, I've discovered my true nature. We're like two animals finding their mate in the wild."
                $ selected_girl.apply_impacts({"affection": (250, 750)})
            else:
                selected_girl.character "This is who I am now. I could never go back to living the way I did before."
            
        # Diminishing returns at highest naturism levels
        $ selected_girl.apply_impacts({"naturism": (250, 750), "discipline": (-750, -250), "fear": (-750, -250), "corruption": (-750, -250)})

    return

