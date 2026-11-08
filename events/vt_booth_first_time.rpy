# Bar-only first-time presentation; ordinary action routing remains independent.
init python:
    def vt_booth_first_time_tier(girl):
        """Tone tier for a first-time vaginal/anal beat, checked in priority order (same priority
        style already used for the forced-creampie CONFLICTED-ending buckets in
        03_vt_pullout_coercion.rpy): reluctant (impaired/genuinely unwilling) overrides everything
        else, since alcohol-compliance or low overall willingness is the strongest, most concrete
        signal available; then devoted (affection) vs eager (corruption) as two alternate reasons
        she might actively want this; else an ordinary nervous-but-willing baseline."""
        if girl.has_trait("drunk") or girl.has_trait("tipsy") or girl.get_acceptance_by_name("sex_interaction") < 40:
            return "reluctant"
        if girl.affection > 55:
            return "devoted"
        if girl.corruption > 55:
            return "eager"
        return "baseline"

    # Her anticipatory line, shown right before the act plays -- by the time this gate runs, any
    # condom question has already resolved and the act is guaranteed to happen this attempt (we're
    # only reached via vt_condom_attempt_gate's own call-through), so this always pays off rather
    # than risking a "here we go" line followed by nothing happening. Same tier selector as the
    # post-beat below, so pre- and post-beat tone always agree within the same encounter.
    VT_BOOTH_FIRST_TIME_VAGINAL_PRE_LINES = {
        "reluctant": {
            "crude":    ["Wait... this is actually gonna be my first time. J-just... don't stop once you start, okay?", "H-hold on, I've actually never done this before. Just... don't stop halfway, alright?", "Okay, this is my first time, for real. Wasn't planning on tonight being it, but just go."],
            "explicit": ["Oh god, this is really it... this is going to be my first time. I'm nervous, but go ahead.", "Oh god, I've never actually done this before... I'm nervous, but don't stop now.", "This is really happening, isn't it -- my first time. I didn't plan for tonight, but go ahead."],
            "direct":   ["This is going to be my first time. I'm nervous about it, but I want you to go ahead.", "I should tell you -- this is my first time. I'm nervous, but I still want you to go ahead.", "This wasn't really the plan, but this is going to be my first time. Go ahead anyway."],
            "neutral":  ["This is... this is going to be my first time. I'm a little nervous, but go ahead.", "I haven't done this before... this is my first time. I'm nervous, but go on.", "This wasn't exactly the plan, but this is going to be my first time. Go ahead, I'm okay."],
            "shy":      ["Th-this is going to be my first time... I'm really nervous, but... go ahead...", "I-I've never done this before... this is my first time... just go slow, okay...?", "Th-this wasn't the plan, but... this is my first time... go ahead..."],
            "demure":   ["This is going to be my first time. I confess I am nervous, but please, proceed.", "I must confess I have never done this before. I am nervous, but please, continue.", "This was not quite what I had planned for tonight, but it is to be my first time nonetheless. Please, proceed."],
        },
        "devoted": {
            "crude":    ["This is gonna be my first time... and I want it to be you, for real.", "Never done this before, but I'm glad it's finally happening with you.", "This is my first time, and honestly? I wouldn't want it to be anyone but you."],
            "explicit": ["This is really about to be my first time... and I'm glad it's you. I mean that.", "I've never done this before, and I'm so glad it's you I get to share it with.", "This is really my first time, and there's no one else I'd rather it be."],
            "direct":   ["This is going to be my first time. I'm glad it's you -- I've wanted that for a while.", "I've never done this before, but I'm glad it's you. That matters to me.", "This is my first time, and I've hoped it would be you for a while now."],
            "neutral":  ["This is going to be my first time... I'm glad it's you.", "I haven't done this before... but I'm glad it's finally you.", "This is going to be my first time, and I couldn't be happier that it's with you."],
            "shy":      ["Th-this is going to be my first time... I wanted it to be you...", "I-I've never done this before... but I'm glad it's you...", "Th-this is my first time... I've wanted it to be you for a while now..."],
            "demure":   ["This is to be my first time. I am glad it is you -- I have hoped for this.", "I have never done this before. I am glad, truly, that it is you.", "This is to be my first time, and I confess I have long hoped it would be you."],
        },
        "eager": {
            "crude":    ["Finally, this is gonna be my first time. I've wanted this for so long, just go.", "Finally -- my first time. I've been waiting for this way too long, don't hold back.", "This is finally happening. I've wanted this forever, just fucking go already."],
            "explicit": ["Oh my god, this is really happening... my first time, finally. Don't hold back.", "Finally, my first time is actually happening. I've wanted this so bad, don't hold back.", "Oh my god, I can't believe this is finally it. I've wanted this for so long."],
            "direct":   ["This is going to be my first time. I've wanted this for a while -- go ahead.", "Finally, this is my first time. I've wanted this for way too long -- go ahead.", "This is really happening. I've been wanting this for a while now, so go ahead."],
            "neutral":  ["This is going to be my first time... and honestly, I've been wanting this.", "This is finally going to be my first time... I've wanted this for a while.", "This is going to be my first time, at last. I've honestly been hoping for this."],
            "shy":      ["Th-this is going to be my first time... I've wanted this for a while...", "F-finally, this is my first time... I've wanted this for so long...", "Th-this is really happening... my first time, finally..."],
            "demure":   ["This is to be my first time. I confess I have wanted this for some time now.", "This is, at last, to be my first time. I confess I have longed for this.", "This is to be my first time, and I must admit I have anticipated this for quite some time."],
        },
        "baseline": {
            "crude":    ["Okay, wow... this is actually gonna be my first time. Go easy on me?", "Okay, wow, I've actually never done this before. Take it easy on me, yeah?", "So this is my first time, for real. Just don't go too rough on me."],
            "explicit": ["Oh wow, this is really it... my first time. I'm nervous, but go ahead.", "Oh wow, I've never actually done this before... this is my first time. I'm nervous, go ahead.", "This is really happening -- my first time. I'm nervous, but I want to."],
            "direct":   ["This is going to be my first time. I'm a little nervous, but go ahead.", "I haven't done this before. This is my first time -- I'm nervous, but go ahead.", "This is my first time. A little nervous about it, but go ahead."],
            "neutral":  ["This is... going to be my first time. I'm a little nervous, but go ahead.", "I've never done this before... this is my first time. I'm a little nervous, but go on.", "This is going to be my first time. Nervous, but I want to go ahead."],
            "shy":      ["Th-this is going to be my first time... I'm nervous, but... go ahead...", "I-I've never done this before... this is my first time... I'm nervous...", "Th-this is really my first time... please go easy...?"],
            "demure":   ["This is to be my first time. I am somewhat nervous, but please, proceed.", "I have never done this before. This is to be my first time, and I am somewhat nervous.", "This is to be my first time. I confess to some nervousness, but please, continue."],
        },
    }

    # Her first-time reaction line, vaginal. Consensual-but-impaired/reluctant is a different beat
    # from VT_FORCE_VIRGIN_LINES (03_vt_pullout_coercion.rpy) -- she went along with this, she just
    # wasn't fully sober/eager about it; "reluctant" here must never read as non-consensual.
    VT_BOOTH_FIRST_TIME_VAGINAL_LINES = {
        "reluctant": {
            "crude":    ["Shit... that actually happened, huh? I wasn't planning on losing it like this, but I guess I'm glad it was you.", "Shit, guess that's my first time gone now. Wasn't the plan, but I'm not mad it was you.", "Huh, actually happened... didn't think tonight would be the night, but okay, I'm glad it was you at least."],
            "explicit": ["Oh my god, that was it... my first time. I wasn't really planning on tonight, but I don't hate that it was you.", "Oh my god, that's my first time gone... wasn't planning on tonight, but I'm glad it was you.", "That actually just happened -- my first time. Didn't expect tonight, but I don't regret it being you."],
            "direct":   ["That was my first time. I hadn't planned on tonight being the night, but I don't regret that it was you.", "That's my first time gone now. Wasn't planning on that tonight, but I'm glad it was you.", "So that happened -- my first time. Didn't plan on tonight, but I don't regret it."],
            "neutral":  ["That was... my first time. I wasn't planning on it happening like this, but I'm glad it was you at least.", "That's my first time, gone now. I didn't plan on tonight, but I'm glad it was you.", "So that just happened... my first time. Wasn't the plan, but I don't mind that it was you."],
            "shy":      ["Th-that was my first time... I wasn't planning on tonight... b-but I'm glad it was you, I think.", "Th-that's my first time, gone now... wasn't planning on tonight... but I'm glad it was you...", "I-I didn't think tonight would be it... but that was my first time... I'm glad, I think..."],
            "demure":   ["That was my first time. I confess I had not intended for tonight to be the night, but I am glad it was you.", "That was, in fact, my first time. I confess this was not my intention for tonight, yet I am glad it was you.", "I find that was my first time. Tonight was not what I had planned, but I am not sorry it was you."],
        },
        "devoted": {
            "crude":    ["That's it, I gave you my first time... I wanted it to be you, you know that?", "That's my first time, gone, and I gave it to you. That's exactly what I wanted.", "So that's my first time, done. Glad as hell it was you."],
            "explicit": ["That was my first time... and I wanted it to be you. I mean that.", "That's my first time, gone now, and I'm so glad it was you. I really mean that.", "That was my first time -- and I wouldn't have wanted it to be anyone else."],
            "direct":   ["That was my first time. I wanted it to be you -- I've wanted that for a while, actually.", "That's my first time, gone now. I'm glad it was you -- I've hoped for that for a while.", "That was my first time, and I wanted it to be you. That's been true for a while now."],
            "neutral":  ["That was my first time... I'm glad it was you. I've wanted this for a while.", "That's my first time, now. I'm really glad it was you -- I've wanted this for a while.", "That was my first time... and I wanted it to be you. I've felt that way for a while."],
            "shy":      ["Th-that was my first time... I wanted it to be you, I really did...", "Th-that's my first time, gone now... I'm so glad it was you...", "I-I gave you my first time... that's what I wanted, really..."],
            "demure":   ["That was my first time. I wanted it to be you, truly -- I have hoped for this for some time.", "That was, indeed, my first time, and I am glad it was you. I have hoped for this for quite some time.", "I find that was my first time, and I wanted it to be you -- truly, I have longed for this."],
        },
        "eager": {
            "crude":    ["Fuck, that's my first time gone and I loved every second of it. Can't believe I waited this long.", "Fuck, my first time's finally gone, and it was so worth the wait.", "Holy shit, that's my first time done, and I loved every bit of it."],
            "explicit": ["Oh my god, that was my first time and it was so much better than I imagined. I can't believe I waited.", "Oh my god, my first time is finally gone, and it was even better than I imagined.", "That was my first time, and it was incredible. I can't believe I waited this long for that."],
            "direct":   ["That was my first time. It was better than I expected -- I don't know why I waited so long.", "That's my first time, gone now, and it was better than I expected. Worth the wait.", "That was my first time, and I loved it. I don't know why I waited this long."],
            "neutral":  ["That was my first time... and honestly, it was better than I thought it'd be.", "That's my first time, finally gone... and it was better than I expected.", "That was my first time... and I can't believe I waited this long to feel that."],
            "shy":      ["Th-that was my first time... it was so much better than I thought it'd be...", "Th-that's my first time, finally... it was so good...", "I-I can't believe that was my first time... it was better than I imagined..."],
            "demure":   ["That was my first time. It exceeded my expectations considerably -- I confess I am somewhat surprised at myself.", "That was, at last, my first time, and it far exceeded what I had imagined.", "I find that was my first time, and I confess I have no notion why I waited so long for it."],
        },
        "baseline": {
            "crude":    ["Okay, wow... that's my first time, officially. That was a lot, but a good kind of a lot.", "Okay, wow, so that's my first time out of the way. That was a lot, but good.", "Huh, so that's my first time, officially done. Wasn't expecting that much, honestly."],
            "explicit": ["Wow... that was my first time. I'm a little overwhelmed, but in a good way, I think.", "Wow, that's my first time, gone now. I'm a little overwhelmed, but a good kind of overwhelmed.", "That was my first time... a lot to take in, but in a good way, I think."],
            "direct":   ["That was my first time. I'm a little overwhelmed, but I think that's normal.", "That's my first time, done. A little overwhelmed, but I think that's normal.", "That was my first time. I'm still catching my breath, but I think it's supposed to feel like that."],
            "neutral":  ["That was my first time... I'm a little nervous, but I think that's normal.", "So that's my first time, gone now... a little nervous still, but I think that's normal.", "That was my first time... still processing it a little, but I think it's normal."],
            "shy":      ["Th-that was my first time... I'm still kind of processing it, but... I think it was good?", "Th-that's my first time, done now... I'm still processing it...", "I-I think that was my first time... it's a lot, but... I think it was good?"],
            "demure":   ["That was my first time. I find myself somewhat overwhelmed, though I believe that is to be expected.", "That was, in fact, my first time. I confess to feeling somewhat overwhelmed by it.", "I find that was my first time, and I am somewhat overwhelmed, though I suspect that is only natural."],
        },
    }

    # Extra line if she orgasms on this exact same tick -- explicitly NOT the enthusiastic/"slut"-
    # tiered framing generic_action_orgasm's own acceptance-tiered content could otherwise land on;
    # each tier reacts to her own orgasm consistently with the tone of the line above it.
    VT_BOOTH_FIRST_TIME_VAGINAL_ORGASM_ADDENDUM = {
        "reluctant": {
            "crude":    ["Fuck, I can't believe I actually came from that... guess my body had other plans tonight.", "Fuck, I actually %verb_climax_ed% from that... my body clearly had other plans tonight.", "Didn't expect to actually finish tonight, but I guess my body wanted it more than I did."],
            "explicit": ["God, I actually came... I wasn't expecting my body to react like that, especially not tonight.", "God, I actually %verb_climax_ed%... wasn't expecting my body to react like that tonight.", "I didn't expect to finish, but I did. My body clearly had its own plans tonight."],
            "direct":   ["I didn't expect to actually finish. My body had other ideas tonight, apparently.", "I actually %verb_climax_ed%, which surprised me. My body had other plans tonight, I guess.", "Didn't think I'd finish tonight, but I did. Guess my body wanted this more than I expected."],
            "neutral":  ["I didn't think I'd actually finish tonight... guess my body had other plans.", "I actually %verb_climax_ed%... wasn't expecting that, but I guess my body had other plans.", "I didn't expect to finish tonight, but I did. My body clearly disagreed with me."],
            "shy":      ["I-I can't believe I actually came... I wasn't expecting that, not tonight of all nights.", "I-I actually %verb_climax_ed%... I really wasn't expecting that, not tonight...", "I didn't think I'd finish... but I did... my body had other ideas, I guess..."],
            "demure":   ["I confess I did not anticipate reaching my own release tonight. My body, it seems, had other intentions.", "I confess I %verb_climax_ed% as well, which I had not anticipated tonight of all nights.", "I did not expect to reach my own release tonight, and yet I did. My body, it would seem, had its own designs."],
        },
        "devoted": {
            "crude":    ["God, I actually came too... guess that's what happens when it's someone I actually care about.", "God, I actually %verb_climax_ed% too... guess that's what happens when it's someone I really care about.", "Didn't expect to finish too, but I did. Must be a you thing."],
            "explicit": ["I came too... I didn't expect that, but I guess it makes sense, given how much I care about you.", "I %verb_climax_ed% too... didn't expect that, but it makes sense, given how much I care about you.", "I actually finished too. Guess that's what happens when I care about someone this much."],
            "direct":   ["I came too, which surprised me a little -- but I suppose it makes sense, feeling the way I do about you.", "I %verb_climax_ed% too, which surprised me -- but it makes sense, given how I feel about you.", "I finished too, actually. Guess that's what happens when it's someone I care about."],
            "neutral":  ["I came too... I didn't expect that, but maybe it makes sense, given how I feel about you.", "I %verb_climax_ed% too... wasn't expecting that, but maybe it's because of how I feel about you.", "I finished too... didn't expect that, but it makes sense, given how much you mean to me."],
            "shy":      ["I-I came too... I wasn't expecting that, but... maybe it's because it's you.", "I-I %verb_climax_ed% too... wasn't expecting that... maybe it's because it's you...", "I finished too... I really wasn't expecting that... but maybe that's just because of you..."],
            "demure":   ["I found my own release as well, which I had not anticipated -- though perhaps it is only natural, given my feelings for you.", "I %verb_climax_ed% as well, which I had not anticipated -- though it is perhaps only natural, given my feelings for you.", "I confess I found my own release, unexpectedly so. Perhaps that is simply what comes of caring for you as I do."],
        },
        "eager": {
            "crude":    ["And I came too, holy shit. Guess I've been missing out this whole time.", "And I %verb_climax_ed% too, holy shit. Can't believe what I've been missing out on.", "Fuck, I finished too. Didn't know I had that in me."],
            "explicit": ["And I came too... god, I can't believe how good that felt. I've been missing out.", "And I %verb_climax_ed% too... god, that felt incredible. I've been missing out this whole time.", "And I finished too, holy shit. Can't believe how good that was."],
            "direct":   ["And I came too. I can't believe what I've been missing out on.", "And I %verb_climax_ed% too. Can't believe I've been missing out on that.", "And I finished too. That was so much better than I expected."],
            "neutral":  ["And I came too... I can't believe I waited this long to feel that.", "And I %verb_climax_ed% too... can't believe I waited this long to feel that.", "And I finished too... I didn't know it could feel like that."],
            "shy":      ["A-and I came too... I can't believe how good that felt...", "A-and I %verb_climax_ed% too... I didn't know it could feel like that...", "A-and I finished too... that was so much better than I thought..."],
            "demure":   ["And I reached my own release as well -- I confess I had no notion it could feel quite so extraordinary.", "And I %verb_climax_ed% as well -- I confess I had no notion it could feel so extraordinary.", "I too reached my own release, and I confess I had no idea I had been missing something so remarkable."],
        },
        "baseline": {
            "crude":    ["And yeah, I came too. Didn't expect that on the first try, honestly.", "And yeah, I %verb_climax_ed% too. Wasn't expecting that on the first go, honestly.", "And I finished too, actually. Didn't think that'd happen my first time."],
            "explicit": ["And I came too... I honestly didn't expect that to happen my first time.", "And I %verb_climax_ed% too... honestly didn't expect that my first time.", "And I finished too. Wasn't expecting that to happen so soon."],
            "direct":   ["And I came too, which I wasn't expecting for a first time.", "And I %verb_climax_ed% too, which I wasn't expecting for a first time.", "And I finished too, actually. Didn't think that would happen tonight."],
            "neutral":  ["And I came too... I wasn't expecting that to happen, not my first time.", "And I %verb_climax_ed% too... wasn't expecting that, not my first time.", "And I finished too... I really didn't think that would happen tonight."],
            "shy":      ["A-and I came too... I really wasn't expecting that, not my first time...", "A-and I %verb_climax_ed% too... I wasn't expecting that at all...", "A-and I finished too... I didn't think that would happen my first time..."],
            "demure":   ["And I reached my own release as well, which I confess I did not expect on a first occasion.", "And I %verb_climax_ed% as well, which I confess I did not anticipate on a first occasion.", "I too found my own release, though I confess I did not expect as much on my first time."],
        },
    }
