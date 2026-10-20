# Climax pull-out coercion. Redirect target for creampie_pussy (01_vt_mod_items.rpy): a bare, not-on-BC,
# low-baby-desire girl interjects to make you pull out. Push (stop_bc_breed willingness) or respect her.
# Outcomes: eager=finish inside + permanent creampie flag; conditional=this session only; else=pull out.
# Choosing to respect her isn't a guaranteed clean pull-out either: vt_try_pullout_failure rolls a
# random MECHANICAL failure (a "pullout_fail" outcome, distinct from force_success/force_fail below) --
# a genuine accident, not a player choice, mirroring this mod's own condom-breakage precedent (a flat
# base chance that climbs the more times he's already had to hold back this session, same shape as
# player.condom_cum's escalation). Framed as blameless: no player-side impact, no fear/affection hit --
# same reasoning a broken condom isn't "his fault" either. Still routes through the real creampie
# action (so the ordinary pregnancy-risk check applies), with vt_force_creampie_active reused to skip
# the base game's consent-flavored narration/fetish-growth for it, same as force_success -- she didn't
# agree to this outcome either, so it shouldn't count as her "conceding" progress, just without any of
# force_success's blame-laden impacts or session-ending override (this is a single accidental beat,
# not a whole-session coercion outcome).
# A no_soft/no_hard refusal after pushing offers one more escalation: force it anyway, a genuine
# player-vs-girl roll (vt_try_force_creampie) that can still fail -- her refusal isn't just reskinned,
# a failed force attempt costs more than a plain refusal and a successful one costs the player too
# (vt_notoriety, control up, compassion down -- vt_notoriety is a new player-facing sidecar stat, see
# 00_vt_patcher.rpy's player condom sidecar). A successful force also skips generic_action_creampie_pussy's
# own consent-flavored text and cancels/reverses its unconditional corruption+arousal grant (see
# VT_FORCE_SUCCESS_GIRL_COMPENSATION), and skips the SEPARATE vt_catch_vaginal_creampie hook's own
# consent-flavored narration/fetish-growth/baby_desire-growth (00_vt_patcher.rpy, gated on
# vt_force_creampie_active) -- both assume consent, which a forced outcome isn't. In their place, a
# mod-authored VT_FORCE_DESCRIPTION narrates the act itself, followed by her distressed VT_FORCE_LINES
# reaction -- shown AFTER the act narrates, not before (it references what just happened to her).
# A force attempt (success OR fail) also overrides the WHOLE SESSION's ending via se_end_label/
# se_use_generic_ending (vt_forced_sex_ending / vt_force_fail_followup, below) -- the base game's
# own generic_sex_ending is a session-level wrap-up that otherwise praises the player regardless of
# what happened, since it's unaware of anything this mod does mid-session.

init python:

    # Tunable impacts (revisit during playtest).
    VT_PULLOUT_IMPACTS = {
        "yes_perm":    {"corruption": (500, 1000), "baby_desire": (200, 500)},
        "yes_session": {"corruption": (200, 500)},
        "no_soft":     {"affection": (-250, -100)},
        "no_hard":     {"affection": (-500, -250), "fear": (200, 500)},
        "respect":     {"affection": (100, 300)},
    }

    # Forced-creampie escalation (past a no_soft/no_hard refusal). Tunable, flagged for sign-off:
    # deliberately no corruption/baby_desire grant on either branch -- unlike the consensual
    # yes_perm/yes_session outcomes, she isn't conceding here, so this doesn't reward the same way.
    # Forcing her also reflects on the player himself regardless of whether the roll succeeds --
    # control up, compassion down -- with a bigger swing (plus vt_notoriety) if it actually lands.
    VT_FORCE_IMPACTS = {
        "force_success": {
            "girl":   {"fear": (400, 800), "affection": (-800, -400)},
            "player": {"vt_notoriety": (10, 20), "control": (0.2, 0.4), "compassion": (-0.4, -0.2)},
        },
        "force_fail": {
            "girl":   {"fear": (500, 900), "affection": (-900, -500)},
            "player": {"vt_notoriety": (3, 8), "control": (0.05, 0.15), "compassion": (-0.15, -0.05)},
        },
    }

    # Compensates for generic_action_creampie_pussy's own unconditional database_action_impacts
    # grant (arousal +15, pressure +57, corruption +3750 XP) when force_success routes through it --
    # that grant assumes consent, which contradicts everything above. Corruption is cancelled
    # outright (a forced creampie doesn't get to also count as her "conceding" progress); arousal is
    # flipped net-negative (violation, not pleasure); pressure is left untouched -- the base grant
    # already climbs it, which is the correct direction for a forced encounter as-is.
    VT_FORCE_SUCCESS_GIRL_COMPENSATION = {"corruption": (-3750, -3750), "arousal": (-40, -20)}

    # Her interjection when you go to finish inside.
    VT_PULLOUT_INTERJECT = {
        "crude":    ["Wait -- pull out! I'm not on the pill, don't you dare cum in me!", "Pull out, I mean it! I'm not on birth control, don't you fucking cum in me!", "Whoa, hold up -- pull out! I'm not covered, don't you dare cum in me!"],
        "explicit": ["Nngh -- pull out! I'm not on anything, you can't cum inside!", "Ah -- wait, pull out! I'm not protected, please don't cum inside!", "Mmh -- not inside, pull out! I'm not on anything, I mean it!"],
        "direct":   ["Wait -- pull out. I'm not on birth control, don't cum in me.", "Hold on -- pull out. I'm not protected right now, don't cum inside me.", "Wait, stop -- I'm not on birth control. Pull out before you cum."],
        "neutral":  ["W-wait, pull out! I'm not on anything right now!", "Wait, please pull out! I'm not on birth control!", "Hold on -- I'm not protected, please pull out!"],
        "shy":      ["N-no, pull out! P-please, I'm not on the pill...!", "W-wait, please... I'm not on the pill, pull out!", "Um, wait -- I'm not protected... please pull out...!"],
        "demure":   ["Wait -- you mustn't finish inside. I'm not protected...!", "Please, you must withdraw. I am not protected right now.", "Wait, I beg you -- I am not on birth control. Please pull out."],
    }

    # Player's push lines.
    VT_PULLOUT_PUSH = [
        "I'm too close to stop... let me cum inside you, just this once.",
        "I want to cum in you so bad... let me fill you up.",
        "Just this once, let me stay inside when I cum -- please.",
    ]

    # Her answer, keyed by outcome then register.
    VT_PULLOUT_LINES = {
        "yes_perm": {
            "crude":    ["Fuck it -- do it. Fill me up, and keep cumming in me from now on.", "Screw it, just cum in me already -- and don't pull out again.", "Do it -- fill me up. I don't want you pulling out ever again."],
            "explicit": ["God... yes, cum inside me. Don't pull out -- not now, not ever.", "Yes -- cum inside me, every time from now on. I mean it.", "Ohh, don't stop -- all I want now is for you to cum inside me."],
            "direct":   ["...Okay. Cum inside. And keep doing it -- I want it.", "Fine -- cum inside. From now on, don't pull out.", "Okay, I want this. Cum inside me, and keep doing it."],
            "neutral":  ["...Do it -- finish inside me. I don't want you to pull out anymore.", "Alright -- go ahead and finish inside. I want that from now on.", "Okay. Don't pull out anymore -- finish inside me."],
            "shy":      ["I... o-okay. Finish inside... I want to feel it. Every time.", "O-okay... I want you to finish inside, every time now...", "I... I want that. Please, finish inside me from now on."],
            "demure":   ["...Very well. Finish inside me. Don't hold back -- not anymore.", "Very well -- finish inside me. I no longer wish for you to withdraw.", "...I want this. Please finish inside me, from now on."],
        },
        "yes_session": {
            "crude":    ["...Fuck it -- cum in me for the rest of this encounter. But next time, you pull out.", "Ugh, fine -- while we're together this time. After that, back to pulling out.", "Alright, for this encounter. Do it. But don't get used to it."],
            "explicit": ["Ohh -- okay, for this encounter. Cum inside... but don't expect it next time.", "Mmh -- alright, while we're together this time. Cum inside me, but that's it.", "Okay... for this encounter, cum in me. Back to pulling out next time."],
            "direct":   ["...Fine, for this encounter -- cum in me -- but we go back to pulling out next time.", "Okay -- while we're together this time. Cum inside, then next time we're back to pulling out.", "Alright, for this encounter only. You can cum inside, but don't expect it next time."],
            "neutral":  ["...Okay, for this encounter. Finish inside. But pull out next time.", "While we're together this time, then -- finish inside. Pull out again next time.", "Okay, I'll allow it for this encounter. Finish inside, but don't assume I'll agree next time."],
            "shy":      ["I-I... for this encounter, okay? O-only while we're together this time...", "J-just while we're together this time... I guess it's okay... b-but next time, pull out...", "O-okay, for this encounter. But please pull out again next time..."],
            "demure":   ["For this encounter, then. Finish inside -- but do not presume it next time.", "While we are together this time, you may finish inside. Do not expect it next time.", "Very well, for this encounter. Do not make a habit of it, however."],
        },
        "no": {
            "crude":    ["No! Pull out -- pull out now!", "No! I said pull out, now!", "Uh-uh, no way -- get out, now!"],
            "explicit": ["No -- not inside! Pull out, I mean it!", "No, not inside me -- pull out now!", "No -- please, pull out, I can't risk it!"],
            "direct":   ["No. Pull out. I'm not risking it.", "No. I need you to pull out, right now.", "No -- I won't risk it. Pull out."],
            "neutral":  ["No -- pull out! Please!", "No, please -- you need to pull out!", "No -- I mean it, pull out now!"],
            "shy":      ["N-no, please pull out! I-I can't...!", "N-no, I can't risk it... please pull out...!", "P-please, no... pull out, now...!"],
            "demure":   ["No -- withdraw. I will not allow you to finish inside me.", "No. I must insist that you withdraw.", "No -- please, you must pull out. I cannot risk it."],
        },
    }

    # Mod-authored override for the creampie act's own narration when force_success routes through
    # it. generic_action_creampie_pussy's baked-in description is suppressed (skip_descriptions)
    # because it assumes consent -- this replaces it rather than leaving a content gap. Not keyed by
    # her register (third-person player-POV narration of the act, not her own voice); easy to edit
    # or extend directly -- this is the general "override the creampie text" hook.
    VT_FORCE_DESCRIPTION = [
        "You hold her hips and push through her protest, burying yourself to the hilt and finishing inside her anyway. She goes rigid beneath you, saying nothing more, and doesn't move until it's over.",
        "You ignore her plea and keep going, emptying yourself inside her despite her refusal. She doesn't fight -- she just goes still and quiet, waiting for it to end.",
    ]

    # Her reaction to a forced-creampie escalation, keyed by outcome then register.
    VT_FORCE_LINES = {
        "force_success": {
            "crude":    ["You -- you actually just came in me. I told you not to, and you did it anyway.", "You did it anyway. I told you no, and you came in me regardless.", "You actually just did that. I said no, and you came in me anyway."],
            "explicit": ["Oh god, you didn't pull out... you came inside me even though I said no...", "You came inside me... after I said no. I can't believe you did that.", "God, I can feel it -- you came inside me, even after I told you not to."],
            "direct":   ["You didn't stop. I told you not to, and you came inside me anyway.", "You went ahead and came inside me. I told you not to.", "I said no, and you did it anyway. I can't believe that."],
            "neutral":  ["You... you didn't pull out. I told you not to. Why didn't you listen?", "You didn't listen. I told you no, and you finished inside me anyway.", "I can't believe you just did that. I said not to, and you did it."],
            "shy":      ["Y-you didn't stop... I told you not to... I can feel it... why didn't you listen to me?", "Y-you really did it... I told you not to... why...?", "I-I can feel it... you didn't listen, even after I said no..."],
            "demure":   ["You finished inside me despite my explicit refusal. I... I do not know what to say.", "I asked you not to, and yet you finished inside me regardless.", "You disregarded what I said entirely. I am at a loss for words."],
        },
        "force_fail": {
            "crude":    ["The fuck was that?! I said pull out, and you almost didn't -- don't you EVER try that again!", "You almost didn't stop! Don't you EVER try that shit again!", "What the hell was that?! I said no, and you still tried it!"],
            "explicit": ["You could have -- god, you actually tried to keep going. Don't you dare do that again!", "You actually tried to keep going after I said no. Don't ever do that again!", "God, you almost didn't stop... don't you dare try that again!"],
            "direct":   ["You didn't listen. I said pull out, and you kept going anyway -- that's not okay.", "You tried to keep going even after I refused. That isn't acceptable.", "You didn't stop when I told you to. That can't happen again."],
            "neutral":  ["You tried to keep going even after I said no. Please... don't ever do that again.", "You kept trying even after I said no. Please don't do that again.", "You didn't listen at first. Please don't ever try that again."],
            "shy":      ["Y-you didn't stop... I was so scared. Please don't ever do that again...", "Y-you kept going for a second there... I was really scared...", "I-I was so scared you weren't going to stop... please don't do that again..."],
            "demure":   ["You disregarded my refusal entirely. That is unacceptable, and it must never happen again.", "You persisted despite my refusal. This must not happen again.", "That you continued at all, even briefly, is unacceptable."],
        },
    }

    # Override narration for force_success when she was ALSO a virgin (girl.hymen and
    # girl.first_time_pussy both true at attempt time -- captured into vt_forced_girl_was_virgin by
    # vt_try_force_creampie, since the act itself is what flips those flags). A forced virginity loss
    # is a much bigger narrative beat than a routine forced creampie, so it gets its own heavier
    # content instead of reusing VT_FORCE_DESCRIPTION/VT_FORCE_LINES["force_success"].
    VT_FORCE_VIRGIN_DESCRIPTION = [
        "You feel it the instant you push through -- a moment's resistance, then gone. She was still a virgin, and you didn't stop to ask; you take that from her along with everything else, finishing inside her before she ever gets the chance to make that choice herself.",
        "There's no mistaking the tightness, or the way she goes rigid the instant you break past it. She was still a virgin. You don't ask -- you just keep going, and finish inside her before she can stop you.",
    ]

    # Her immediate reaction when the forced creampie was ALSO her first time.
    VT_FORCE_VIRGIN_LINES = {
        "crude":    ["That was my FIRST time! I always thought I'd get to choose, and you didn't even ask -- you just took it and came in me!", "That was supposed to be MY choice, and you just took it from me without even asking!", "I was still a virgin! You didn't even ask -- you just took that from me!"],
        "explicit": ["Oh god, that was my first time... I always imagined it would be different. You didn't even ask -- you just took it from me.", "I was still a virgin... and you didn't even ask. You just took it from me.", "That was my first time, and you took it without asking me anything."],
        "direct":   ["That was my first time. I always thought that would be my choice to make, not something taken from me like this.", "I was still a virgin. You never asked -- you simply took that choice from me.", "That was supposed to be mine to decide. You took it without asking."],
        "neutral":  ["That... that was my first time. I always thought it would be different. You didn't even ask.", "I was still a virgin... and you didn't ask me at all.", "That was my first time, and you never even asked me."],
        "shy":      ["Th-that was my first time... I always thought... I never thought it would happen like this... you didn't even ask...", "I-I was still a virgin... you didn't ask me... I didn't want it like this...", "Th-that was supposed to be my choice... you never asked..."],
        "demure":   ["That was my first time. I had always hoped it would be a choice I made myself, not one taken from me without my consent.", "I was still untouched. You never sought my consent -- you simply took it.", "That decision was meant to be mine alone. You never asked me at all."],
    }

    # Session-ending lines (see vt_forced_sex_ending / vt_force_fail_followup below), replacing or
    # appending to the base game's generic_sex_ending, which otherwise praises the player regardless
    # of a forced outcome this session. Register-keyed like the rest of this file.

    # force_success, she did NOT orgasm this session -- pure anger/violation, no ambiguity.
    VT_FORCED_ENDING_ANGRY = {
        "crude":    ["You came in me earlier without giving a shit what I said. That's not something I'm just going to get over.", "I'm still pissed about earlier. You came in me after I told you not to, and that's not okay.", "You really just ignored me earlier and came inside anyway. I haven't forgotten that."],
        "explicit": ["I keep thinking about earlier... you came inside me even after I told you not to. That wasn't your choice to make.", "I'm still upset about earlier. You came inside me, and I told you not to.", "What happened earlier is still bothering me. You didn't listen when I said no."],
        "direct":   ["I haven't forgotten what happened earlier. You came inside me despite my refusal, and that isn't something I'll just let go.", "I'm still angry about earlier. You came inside me despite my refusal.", "What you did earlier hasn't left my mind. You ignored what I said."],
        "neutral":  ["I'm still thinking about earlier... you didn't listen when I said no, and you finished inside me anyway.", "I keep thinking about earlier. You didn't stop when I told you no.", "I'm still upset about what happened earlier. You didn't listen to me."],
        "shy":      ["I... I can't stop thinking about earlier. You didn't stop, even after I said no... that really hurt.", "I-I keep thinking about earlier... you didn't stop... it really scared me...", "I'm still... upset about earlier. You didn't listen when I said no..."],
        "demure":   ["I have not forgotten what transpired earlier. You disregarded my refusal entirely, and that is not something I take lightly.", "What occurred earlier remains with me. You did not heed my refusal.", "I continue to reflect on earlier events. My objection was entirely disregarded."],
    }

    # force_success, sex_interaction_cum_count > 0 by session end -- her body responded at some
    # point, but that is explicitly not the same as consent; still angry/sad about the creampie.
    # This is the fallback bucket for a girl who doesn't clear any of the three tone-bucket
    # thresholds below (_vt_forced_conflicted_lines) -- kept as the plain baseline framing.
    VT_FORCED_ENDING_CONFLICTED = {
        "crude":    ["Fuck... I came anyway, I won't lie about that. But that doesn't mean I wanted you to cum inside me. I told you not to.", "Yeah, I came too, whatever. Doesn't mean I wanted you cumming inside me after I said no.", "My body got off, fine. That's not the same as me wanting you to cum in me."],
        "explicit": ["God, I did end up cumming... but don't mistake that for wanting what you did. You came inside me after I said no.", "I did cum, I'll admit it. But that's not the same as wanting what you did.", "My body responded, yes. That doesn't mean I was okay with you cumming inside."],
        "direct":   ["My body responded, I'll admit that. But that isn't the same as consent -- you came inside me after I refused.", "I did cum, yes. That doesn't change that you came inside me without my consent.", "My body reacted, that's true. It still wasn't consent."],
        "neutral":  ["I know I came too, at some point... but that doesn't make what you did okay. You didn't listen when I said no.", "I came too, I know. But that's not the same as being okay with what happened.", "My body responded, but that doesn't excuse what you did."],
        "shy":      ["I-I couldn't help how my body reacted... but that doesn't mean any of this was okay. You didn't stop when I told you to.", "I-I did end up... finishing too... but that doesn't make it okay...", "M-my body reacted, but I still didn't want that to happen..."],
        "demure":   ["I will not deny that my body responded. That does not excuse what you did -- you finished inside me despite my explicit refusal.", "I concede that my body reacted. That does not equate to my consent.", "That I climaxed changes nothing about the fact that I refused."],
    }

    # Same situation as VT_FORCED_ENDING_CONFLICTED above, but for a girl whose intellect is high
    # enough (see _vt_forced_conflicted_lines) that she articulates the arousal/consent distinction
    # explicitly and analytically, regardless of how upset she otherwise is.
    VT_FORCED_ENDING_CONFLICTED_ANALYTICAL = {
        "crude":    ["My body getting off doesn't mean shit -- arousal and consent aren't the same thing, and you should already know that.", "My body's reaction doesn't tell you shit about whether I consented -- you already know the difference.", "Getting off and saying yes are two different things. You crossed a line regardless."],
        "explicit": ["Just because my body responded doesn't mean I consented to any of it. Those are two completely different things, and you crossed a line regardless.", "Arousal isn't consent. My body responding doesn't erase that I said no.", "You know full well arousal and permission aren't the same thing. That still applies here."],
        "direct":   ["My body's reaction and my consent aren't the same thing. One happening doesn't excuse the other being ignored.", "Physical arousal and consent are separate concepts. You ignored the one that mattered.", "My body's reaction doesn't retroactively grant permission you never had."],
        "neutral":  ["I know my body reacted, but that's a physical response, not permission. You still did something I explicitly said no to.", "A physical response isn't the same as agreement. You still crossed a line I set.", "I understand my body reacted. That's not the same as me consenting."],
        "shy":      ["I-I know my body reacted... but that's not the same as agreeing to it. Those are different things, even if it's confusing.", "I-I know it's confusing, but... my body reacting isn't the same as agreeing...", "It's just... a physical thing. It's not the same as saying yes..."],
        "demure":   ["That my body responded is a physiological fact, not a moral one. It does not, in any sense, constitute my consent.", "A bodily response is not equivalent to informed consent, however it may appear.", "One may be aroused without ever having granted permission. The two are distinct."],
    }

    # Same situation, for a girl whose affection is high enough that the personal-trust angle
    # dominates -- it stings more because she trusts/cares about him, not despite it.
    VT_FORCED_ENDING_CONFLICTED_BETRAYED = {
        "crude":    ["The fact that my body still got into it just makes this worse, honestly -- I actually trust you, and you did this to me anyway.", "It stings even more that my body got into it, honestly -- I trusted you, and you still did that.", "I trusted you, and that's what makes this hurt so much more than it should."],
        "explicit": ["It almost hurts more that my body responded, because I trust you. And you still didn't listen to me.", "This hurts worse because I trust you. My body responding doesn't fix that you ignored me.", "I trusted you with this, and you still went ahead anyway. That's what hurts most."],
        "direct":   ["It's worse, somehow, that my body reacted -- because I trusted you, and you still went ahead without my consent.", "This is worse precisely because I trust you. That trust didn't stop you.", "I trusted you, which is exactly why this hurts more than it should."],
        "neutral":  ["I think it hurts more because I trust you. My body responding doesn't change that you didn't listen to me.", "It hurts more because I trusted you with this. That doesn't make what happened okay.", "I trust you, which is why this stings so much. It still wasn't right."],
        "shy":      ["I-I think it hurts worse because... because I trust you. My body reacting doesn't mean what you did was okay.", "I-I trust you so much... that's why this hurts more than it should...", "It's worse because... I really did trust you with this..."],
        "demure":   ["It wounds me more, I think, precisely because I trust you. My body's response changes nothing about what you disregarded.", "The pain is compounded precisely because I trusted you so completely.", "It wounds me further that this came from someone I trusted."],
    }

    # Same situation, for a girl whose corruption is high enough that her body's response barely
    # registers as surprising to her anymore -- matter-of-fact/resigned; the anger is purely about
    # the act itself, not personal betrayal.
    VT_FORCED_ENDING_CONFLICTED_DEFIANT = {
        "crude":    ["Yeah, I came. Big surprise. Doesn't mean you get a pass for ignoring me.", "Of course I came; I always do now. Doesn't mean you get to just ignore me.", "Yeah, I got off. Big deal. You still don't get a pass for that."],
        "explicit": ["My body's going to respond to this stuff at this point, that's just how it works now. Doesn't mean what you did was fine.", "My body responding is old news by now. Doesn't mean what you did was fine.", "I stopped being surprised by my body's reactions a while ago. Still doesn't excuse this."],
        "direct":   ["My body reacting isn't news to me anymore. It still doesn't make what you did acceptable.", "My body reacting is expected at this point. It doesn't excuse ignoring my refusal.", "That's just how my body works now. It changes nothing about what you did."],
        "neutral":  ["I'm not surprised my body reacted -- that's just how it goes for me now. It still doesn't excuse what you did.", "I'm used to my body reacting by now. It still doesn't make this okay.", "That's just how things go for me these days. Still doesn't excuse what happened."],
        "shy":      ["I-I'm not even that surprised my body reacted... it just does that now. But that doesn't make it okay.", "I-I guess I'm used to it by now... but it still wasn't okay...", "It just... happens now. That doesn't mean what you did was fine..."],
        "demure":   ["My body's response is, by now, unremarkable to me. It remains entirely irrelevant to whether what you did was acceptable.", "My body's reactions no longer surprise me. That is beside the point entirely.", "Such responses are, by now, routine for me. They excuse nothing of what transpired."],
    }

    def _vt_forced_conflicted_lines(girl):
        """Pick the CONFLICTED-ending tone bucket by her stats -- register (vt_explicitness_register,
        corruption/naturism-driven) still separately controls word choice within whichever bucket
        this returns; this is a second, orthogonal axis for what she emphasizes emotionally.
        Priority order (checked top to bottom, matching this mod's existing threshold convention,
        e.g. vt_small_talk_affection.rpy's corruption > 60 / intellect > 70-style cutoffs):
        analytical (intellect) > betrayed (affection) > defiant (corruption) > baseline."""
        if girl.intellect > 65:
            return VT_FORCED_ENDING_CONFLICTED_ANALYTICAL
        if girl.affection > 55:
            return VT_FORCED_ENDING_CONFLICTED_BETRAYED
        if girl.corruption > 55:
            return VT_FORCED_ENDING_CONFLICTED_DEFIANT
        return VT_FORCED_ENDING_CONFLICTED

    # Follow-up after either ending above, only when she isn't on birth control (checked live).
    VT_FORCED_ENDING_PREGNANCY_WORRY = {
        "crude":    ["And now I get to spend the next few weeks wondering if I'm knocked up, since you didn't bother pulling out.", "Great, now I get to sit here wondering if I'm pregnant, since you couldn't be bothered to pull out.", "Now I've got weeks of wondering if I'm knocked up ahead of me. Thanks for that."],
        "explicit": ["Now I'm going to be worrying myself sick over whether I'm pregnant. I'm not even on the pill.", "I'm going to be a wreck wondering if I'm pregnant now. I'm not on anything.", "Now there's a real chance I'm pregnant. I'm not protected at all."],
        "direct":   ["Now I have to worry about whether I'm pregnant. I'm not protected, and that was entirely your doing.", "I now have to worry about a pregnancy I didn't ask for. I'm not on birth control.", "You've left me wondering if I'm pregnant now. I wasn't protected."],
        "neutral":  ["Now I'm worried I might be pregnant. I'm not on birth control, and you knew that.", "Now I have to worry about being pregnant. I'm not on birth control.", "I might be pregnant now, and I wasn't protected at all."],
        "shy":      ["W-what if I get pregnant now...? I'm not protected... I'm really scared.", "I-I might actually be pregnant now... I'm not protected...", "W-what if this actually gets me pregnant...? I'm scared..."],
        "demure":   ["I am now left to worry whether I am with child. I am not protected, and you were well aware of that.", "I must now contend with the possibility of pregnancy, unprotected as I am.", "The prospect of pregnancy now weighs on me, given my lack of protection."],
    }

    # Follow-up appended in vt_forced_sex_ending after the ending + pregnancy-worry lines above,
    # only when vt_forced_girl_was_virgin is true -- one more reflective beat specifically about it
    # having been her first time.
    VT_FORCED_ENDING_VIRGIN_ADDENDUM = {
        "crude":    ["And to top it off, that was supposed to be my first time. Guess I don't get a do-over on that.", "And that was my first time too. Guess that's just gone now, huh.", "On top of everything, that was supposed to be my first time. Not like this."],
        "explicit": ["I keep coming back to the fact that that was my first time. I always thought it would be so different from that.", "And on top of it all, that was my first time. Not how I ever pictured it.", "I can't stop thinking about how my first time was taken from me."],
        "direct":   ["I also can't stop thinking that that was my first time. It was supposed to be my choice, not yours.", "And that was also my first time. It should have been my decision.", "On top of everything else, that was supposed to be my first time."],
        "neutral":  ["And that was supposed to be my first time. I always imagined it would go so differently than that.", "And that was also my first time. I imagined it very differently.", "That was supposed to be my first time too. Not like this."],
        "shy":      ["I-I keep thinking about how that was my first time... it wasn't supposed to happen like that...", "A-and that was my first time too... it wasn't supposed to be like this...", "I keep thinking that was also my first time... not this way..."],
        "demure":   ["I find myself dwelling on the fact that that was my first time. It was meant to be my choice, not one made for me.", "And that, too, was meant to be my first time -- not one taken from me.", "I dwell further on the fact that it was also my first time, lost this way."],
    }

    # force_fail only -- relief he pulled out/came outside instead, still uneasy about the attempt.
    VT_FORCED_ENDING_ATTEMPT = {
        "crude":    ["I'm still glad you actually pulled out earlier. For a second there I really thought you weren't going to stop.", "At least you actually pulled out earlier. For a second I thought you wouldn't.", "Good thing you stopped when you did earlier. I really wasn't sure you would."],
        "explicit": ["I'm relieved you pulled out earlier... when you kept going, I genuinely didn't think you'd stop in time.", "I'm glad you actually stopped earlier. I wasn't sure you would for a second there.", "At least you pulled out in the end. I was genuinely worried you wouldn't."],
        "direct":   ["I'm still glad you pulled out earlier. When you kept pushing, I wasn't sure you were going to stop at all.", "I'm relieved you stopped earlier. For a moment I doubted you would.", "At least you did pull out eventually. I wasn't certain you would."],
        "neutral":  ["I'm glad you pulled out earlier, even if it took you a while to actually do it. I was worried for a second.", "I'm glad you stopped earlier, even though it took a moment. I was worried.", "At least you did pull out in the end. That was a scary moment."],
        "shy":      ["I-I'm still glad you pulled out earlier... when you kept going, I really thought you weren't going to stop...", "I-I'm glad you stopped... for a second I really didn't think you would...", "A-at least you pulled out eventually... I was really scared for a moment..."],
        "demure":   ["I remain grateful that you withdrew earlier, though I confess I was uncertain you would stop at all.", "I am relieved you ultimately withdrew, though your hesitation concerned me.", "I remain thankful you stopped, even if only after some uncertainty."],
    }

    # Her line when you pull out (respect choice).
    VT_PULLOUT_RESPECT = {
        "crude":    ["Good. Thanks for pulling out like I asked.", "Yeah, you pulled out like I asked. Thanks.", "Mm, appreciate you pulling out. Smart move."],
        "explicit": ["Mmm -- yes, pull out, cover me. Thank you for being careful.", "Thank you for pulling out when I asked.", "God, thank you for being careful. Pulling out was the right call."],
        "direct":   ["Thank you. Pulling out -- that's the right call.", "Good call, pulling out. I appreciate that.", "Thanks for pulling out. That was the responsible thing to do."],
        "neutral":  ["Thank you for pulling out. I feel safer with you.", "Thanks for pulling out. That means a lot to me.", "I appreciate you pulling out. It makes me trust you more."],
        "shy":      ["Th-thank you for pulling out... I was scared for a second.", "Th-thanks for being careful... I really appreciate it...", "I-I'm glad you pulled out... thank you..."],
        "demure":   ["Thank you for withdrawing. That was considerate of you.", "I appreciate your restraint in withdrawing. Thank you.", "Your consideration in pulling out did not go unnoticed. Thank you."],
    }

    # Menu captions for the pull-out gate below, register-keyed like the rest of this file (keyed
    # off her register, same as everything else here -- there's no separate "player register"
    # concept anywhere in this mod). Previously bare literals with zero variety at all.
    VT_PULLOUT_MENU_PUSH_CAPTION = {
        "crude":    ["Push her to let you cum inside", "Talk her into letting you cum inside", "Try to convince her to take it"],
        "explicit": ["Push her to let you cum inside", "Try to convince her to let you cum inside", "Coax her into letting you cum inside"],
        "direct":   ["Push her to let you cum inside", "Try to convince her to let you cum inside", "Ask her to let you cum inside anyway"],
        "neutral":  ["Push her to let you finish inside", "Try to convince her to let you finish inside", "Ask if you can finish inside anyway"],
        "shy":      ["Push her to let you finish inside", "Gently try to convince her", "Softly ask if you can finish inside"],
        "demure":   ["Push her to let you finish inside", "Attempt to persuade her otherwise", "Politely ask to finish inside anyway"],
    }
    VT_PULLOUT_MENU_RESPECT_CAPTION = {
        "crude":    ["Respect her -- pull out", "Fine, pull out", "Pull out like she wants"],
        "explicit": ["Respect her -- pull out", "Respect her wishes and pull out", "Pull out, like she asked"],
        "direct":   ["Respect her -- pull out", "Respect her wishes and pull out", "Pull out as she asked"],
        "neutral":  ["Respect her -- pull out", "Respect her wishes and pull out", "Pull out as she requested"],
        "shy":      ["Respect her -- pull out", "Respect what she wants and pull out", "Gently pull out as she asked"],
        "demure":   ["Respect her -- pull out", "Honor her wishes and withdraw", "Respectfully pull out as she asked"],
    }
    VT_PULLOUT_MENU_FORCE_CAPTION = {
        "crude":    ["Force it anyway", "Do it anyway, screw what she wants", "Keep going regardless"],
        "explicit": ["Force it anyway", "Keep going despite her refusal", "Push through anyway"],
        "direct":   ["Force it anyway", "Keep going despite her refusal", "Push through regardless"],
        "neutral":  ["Force it anyway", "Keep going despite her refusal", "Try to push through anyway"],
        "shy":      ["Force it anyway", "Keep going despite her refusal", "Push through despite her objection"],
        "demure":   ["Force it anyway", "Proceed despite her refusal", "Disregard her objection and continue"],
    }
    VT_PULLOUT_MENU_YIELD_CAPTION = {
        "crude":    ["Fine -- pull out", "Alright, pull out then", "Whatever, pull out"],
        "explicit": ["Fine -- pull out", "Give up and pull out", "Alright -- pull out"],
        "direct":   ["Fine -- pull out", "Give up and pull out instead", "Back off and pull out"],
        "neutral":  ["Fine -- pull out", "Give up and pull out instead", "Back off and pull out"],
        "shy":      ["Fine -- pull out", "Give up and pull out instead", "Back off and pull out"],
        "demure":   ["Fine -- pull out", "Relent and withdraw instead", "Concede and pull out"],
    }

    def vt_accepts_creampie(girl):
        """Permanent 'you may finish inside me' concession (sidecar flag)."""
        try:
            return bool(vt_girl_bucket(girl).get("vt_accepts_vaginal_creampie", False))
        except Exception as e:
            renpy.log(f"VT MOD ERROR: vt_accepts_creampie failed for {getattr(girl, 'first_name', girl)}: {e!r}")
            return False

    def vt_set_accepts_creampie(girl, val=True):
        """Returns True if the permanent flag was actually persisted, False on failure -- callers
        that narrate a permanent concession should check this rather than assume the write landed."""
        try:
            vt_girl_bucket(girl)["vt_accepts_vaginal_creampie"] = bool(val)
            return True
        except Exception as e:
            renpy.log(f"VT MOD ERROR: vt_set_accepts_creampie failed for {getattr(girl, 'first_name', girl)}: {e!r} -- permanent flag NOT saved.")
            return False

    def vt_wants_pullout(girl):
        """True if she'll interject for a pull-out: raw (or a broken condom she's aware of), not wanting a
        condom now, not on BC, not pregnant, baby_desire band 'none', not already conceded."""
        if girl is None or not isinstance(girl, Girl):
            return False
        if not getattr(store, "is_during_sex_interaction", False):
            return False
        # Raw: no condom, or a broken one she's aware of.
        _raw = getattr(player, "condom_active", "raw") == "raw"
        _broke_known = getattr(player, "condom_broke", False) and getattr(girl, "aware_vaginal_condom", False)
        if not (_raw or _broke_known):
            return False
        # Wants a condom now -> the condom gate handles it, not this.
        if vt_condom_now(girl, "vaginal"):
            return False
        if getattr(girl, "birth_control", False):
            return False
        if getattr(girl, "pregnant", False):
            return False
        if vt_baby_desire_band(girl) != "none":
            return False
        if vt_accepts_creampie(girl):
            return False
        if girl.id in getattr(store, "vt_creampie_session", set()):
            return False
        return True

    def vt_try_creampie(girl, player=None):
        """Resolve a 'let me finish inside' push; store the result for the gate to show."""
        if player is None:
            player = getattr(store, "player", None)

        band = vt_willingness_band(girl, "stop_bc_breed", player)
        if band == "eager":
            if vt_set_accepts_creampie(girl, True):                # permanent
                outcome, line_key = "yes_perm", "yes_perm"
            else:
                # Persisting the permanent flag failed -- fall back to session-only rather than
                # promising a permanent concession that didn't actually save.
                outcome, line_key = "yes_session", "yes_session"
                store.vt_creampie_session.add(girl.id)
        elif band == "conditional":
            outcome, line_key = "yes_session", "yes_session"
            store.vt_creampie_session.add(girl.id)                 # this session only
        elif band == "hesitant":
            outcome, line_key = "no_soft", "no"
        else:
            outcome, line_key = "no_hard", "no"

        impacts = VT_PULLOUT_IMPACTS.get(outcome)
        if impacts:
            girl.apply_impacts(dict(impacts))

        line = vt_voice(girl, VT_PULLOUT_LINES[line_key], "Pull out!")
        store.vt_pullout_result = {"outcome": outcome, "line": line}

    def vt_try_pullout_failure(girl, player):
        """Roll whether a genuine attempt to pull out fails anyway -- a random mechanical accident,
        not a player choice. Mirrors the mod's own condom-breakage formula shape (flat base chance
        + an escalating term, both capped): a flat base plus a bump for each earlier pull-out this
        same sex session, on the theory that holding back gets harder the more times he's already
        had to do it. Placeholder base/escalation/cap -- flag for tuning. Increments the session
        counter regardless of outcome (each attempt counts toward the wear, not just failures)."""
        base_chance = 8
        per_attempt = 4
        escalation_cap = 27  # base + cap = 35, the ceiling on this roll
        chance = base_chance + min(escalation_cap, per_attempt * store.vt_pullout_fail_count)
        store.vt_pullout_fail_count += 1
        return renpy.random.randint(1, 100) <= chance

    # Third-person narration override for a pullout_fail outcome, mirroring VT_FORCE_DESCRIPTION's
    # role (replaces generic_action_creampie_pussy's own consent-flavored text) but framed as an
    # accident, not a violation -- not register-keyed, same reasoning as VT_FORCE_DESCRIPTION.
    VT_PULLOUT_FAIL_DESCRIPTION = [
        "You mean to pull out in time, but your body doesn't cooperate -- you're still buried inside her when it happens, and there's no taking it back now.",
        "You try to pull out, but it's too late -- you're already spilling inside her before you can stop yourself.",
    ]

    # Her immediate reaction to a pullout_fail -- alarmed and surprised, NOT angry (it's an accident,
    # not a betrayal; contrast with VT_FORCE_LINES, which is written as a deliberate refusal ignored).
    VT_PULLOUT_FAIL_LINES = {
        "crude":    ["Wait, what -- you're still inside?! Fuck, you were supposed to pull out!", "Shit, you're still in there! You said you'd pull out!", "You're fucking kidding me, you're still in there!"],
        "explicit": ["Wait -- you're still inside me?! You were supposed to pull out!", "Oh god, I can feel it -- you didn't make it out in time!", "Wait, you didn't pull out in time -- I can feel it!"],
        "direct":   ["Wait, you're still inside. You were supposed to pull out.", "You didn't make it out in time. I can feel it.", "Wait, you said you'd pull out -- you didn't."],
        "neutral":  ["Wait -- you're still inside me? You were supposed to pull out!", "Oh no, you didn't make it out in time...", "Wait, you were supposed to pull out in time..."],
        "shy":      ["W-wait, you're still... oh no, you were supposed to pull out...!", "Y-you didn't make it out in time... oh no...", "W-wait, you said you'd pull out...!"],
        "demure":   ["Wait -- you are still inside me. You were meant to withdraw in time.", "Oh dear, you did not withdraw in time after all.", "Oh -- you were meant to withdraw, and did not."],
    }

    # Follow-up worry, shown only when she isn't on birth control (checked live, same convention as
    # VT_FORCED_ENDING_PREGNANCY_WORRY) -- deliberately blameless phrasing ("wasn't supposed to
    # happen", "neither of us intending"), unlike that beat's accusatory "you knew that" framing,
    # since this wasn't a choice either of them made.
    VT_PULLOUT_FAIL_PREGNANCY_WORRY = {
        "crude":    ["Great, now I get to spend the next few weeks wondering if that knocked me up. Wasn't even supposed to happen.", "So now I've got to worry about being pregnant, and it wasn't even on purpose. Perfect.", "Fuck, now I'm stuck wondering if I'm pregnant, and this wasn't even supposed to happen."],
        "explicit": ["Now I'm going to be worrying myself sick over whether I'm pregnant. I'm not even on the pill.", "I'm going to be a wreck wondering if that got me pregnant. I'm not protected at all.", "Now I have to spend weeks wondering if I'm pregnant, and I'm not even protected."],
        "direct":   ["Now I have to worry about whether I'm pregnant. I'm not protected, and that wasn't supposed to happen.", "I have to worry about a pregnancy now, even though neither of us meant for that to happen.", "Now I have to wonder if I'm pregnant, and that wasn't supposed to happen at all."],
        "neutral":  ["Now I'm worried I might be pregnant. I'm not on birth control, and that wasn't supposed to happen.", "I might be pregnant now, even though you didn't mean for that to happen.", "Now I'll be worrying about being pregnant, and that wasn't the plan at all."],
        "shy":      ["W-what if I get pregnant now...? I'm not protected... and it wasn't even supposed to happen...", "I-I might actually be pregnant now... and it wasn't even on purpose...", "W-what if that got me pregnant...? It wasn't supposed to happen like that..."],
        "demure":   ["I am now left to worry whether I am with child, despite neither of us intending that outcome.", "The prospect of pregnancy now weighs on me, though I know this was not by design.", "I must now wonder whether I am with child, though this was surely never intended."],
    }

    def vt_try_force_creampie(girl, player):
        """Roll whether pushing PAST a no_soft/no_hard refusal actually forces the creampie
        through. A genuine contest, not a guaranteed override -- modeled on the base game's own
        player-vs-npc roll (label_pta_discussion_options.rpy's speech-success check): a player
        term, an npc resistance term, and RNG, not a flat stat-threshold check.

        player.control is the one existing player stat that's semantically a dominance/
        forcefulness score, and it's otherwise wired nowhere in the base game -- this gives it a
        first real purpose (the same pairing _vt_player_nudge already uses for the much smaller,
        consensual "deference" nudge: player.control vs. her fear+discipline).

        Girl-side resistance mirrors the mod's own dominant_approach["dominate"] shape
        ((discipline + fear) / 2), dampened by corruption/affection -- the stats that make her
        "want it" undercut how much she can hold out against being forced.

        Threshold and every impact number here are starting points flagged for playtest/sign-off,
        not final tuning.
        """
        dominance = player.control * 10  # 0-10 -> 0-100
        resistance = (girl.fear + girl.discipline) / 2.0
        resistance -= girl.corruption * 0.3 + girl.affection * 0.2
        resistance = max(0.0, min(100.0, resistance))

        roll = renpy.random.random()
        force_score = roll + (dominance - resistance) / 100.0
        outcome = "force_success" if force_score >= 0.55 else "force_fail"

        impacts = VT_FORCE_IMPACTS.get(outcome, {})
        if impacts.get("girl"):
            girl.apply_impacts(dict(impacts["girl"]))
        if impacts.get("player"):
            player.apply_impacts(dict(impacts["player"]))

        # Override the session's ending (vt_forced_sex_ending / vt_force_fail_followup) instead of
        # letting generic_sex_ending praise the player regardless of this -- that base label is a
        # session-level wrap-up, not per-action, and has no idea this happened. A later
        # force_success always wins over an earlier force_fail in the same session; using
        # store.se_end_label/store.se_use_generic_ending explicitly since this is a plain function,
        # not a label (same caution this file already uses for other store access).
        if outcome == "force_success" or store.vt_force_outcome_this_session != "force_success":
            if store.se_end_label not in ("vt_forced_sex_ending", "vt_force_fail_followup"):
                # Ground-truth check instead of gating on vt_force_outcome_this_session -- that flag
                # is only ever cleared by vt_forced_ending_handoff completing, so it can't be trusted
                # if an earlier forced session's ending was ever abandoned mid-flow (e.g. testing/
                # reloading). se_end_label itself can be: sex_interaction_clear() always resets it to
                # None at the true end of any completed interaction, and the current scene's own
                # location label (if any) sets it fresh every time a brand-new interaction starts --
                # so if it isn't already one of OUR OWN override targets, it's guaranteed to be
                # whatever THIS session's enclosing scene actually set.
                store.vt_orig_se_end_label = store.se_end_label
                store.vt_orig_se_use_generic_ending = store.se_use_generic_ending
            store.vt_force_outcome_this_session = outcome
            store.vt_forced_girl = girl
            store.vt_forced_girl_was_virgin = bool(getattr(girl, "hymen", False) and getattr(girl, "first_time_pussy", False))
            if outcome == "force_success":
                store.se_end_label = "vt_forced_sex_ending"
                store.se_use_generic_ending = False   # full replace -- the praise never plays
            else:
                store.se_end_label = "vt_force_fail_followup"
                # Leave se_use_generic_ending as whatever the enclosing scene already wanted --
                # don't force it either way. The screen's own dispatch reaches our append label
                # regardless (via generic_sex_ending's tail if the scene wanted generic text, or
                # directly if it didn't), so forcing this could inject praise text into a scene
                # that deliberately skipped it, or suppress text a scene wanted to show.

        line = vt_voice(girl, VT_FORCE_LINES[outcome], "...")
        store.vt_pullout_result = {"outcome": outcome, "line": line}
        return outcome

default vt_pullout_result = None
# Session-scoped wear counter for vt_try_pullout_failure -- each attempt to hold back and pull out
# (success or fail) increments this, escalating the next attempt's failure chance. Reset on a fresh
# sex interaction by the label_callback in vt_huds/vt_overlay.rpy, alongside vt_creampie_session.
default vt_pullout_fail_count = 0
# Session-scoped signal for vt_catch_vaginal_creampie (00_vt_patcher.rpy): true only for the
# duration of a force_success renpy.call into generic_action_creampie_pussy, so that hook can skip
# its own consent-flavored narration/fetish-growth/baby_desire-growth for a forced outcome, same as
# this file already skips generic_action_creampie_pussy's own description/response text for it.
default vt_force_creampie_active = False
# Session-scoped record of a force attempt, read by vt_forced_sex_ending/vt_force_fail_followup at
# the eventual end of the sex interaction (which may be much later than the attempt itself).
default vt_force_outcome_this_session = None   # None / "force_fail" / "force_success"
default vt_forced_girl = None                  # the Girl object a force was attempted against
default vt_forced_girl_was_virgin = False      # her hymen/first_time_pussy state at attempt time
# Snapshot of whatever the enclosing scene (bar/pier/park/home-visit invite-home, etc.) had already
# set se_end_label/se_use_generic_ending to, taken the first time a force attempt happens this
# session -- so our own ending labels can hand off to it instead of discarding its continuation.
default vt_orig_se_end_label = None
default vt_orig_se_use_generic_ending = None

# Direct SexAction continuation, reached only after its existing protection gate.
# Match sex_creampie_pussy's arguments and return to the same action wrapper/cost owner.
label vt_direct_creampie_pussy:
    call vt_pullout_climax_gate(additional_subtags=se_additional_webm_sub_tags, skip_descriptions=sex_skip_descriptions, skip_responses=sex_skip_responses) from vt_direct_creampie_pussy_return
    return

# Redirect target for creampie_pussy (01_vt_mod_items.rpy), called with the option_label kwargs.
# Resolves the pull-out, then plays the real creampie or the external cumshot.
label vt_pullout_climax_gate(action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False):
    python:
        _pg_girl = selected_girl
        _pg_real = "vt_vaginal_finisher"     # cum inside
        _pg_pullout = "vt_withdrawal_finisher"   # pull out (external)

    # Not a pull-out girl -> finish inside as chosen.
    if not vt_wants_pullout(_pg_girl):
        $ renpy.call(_pg_real, action_name=action_name, additional_subtags=additional_subtags, skip_descriptions=skip_descriptions, skip_responses=skip_responses)
        return

    # She interjects.
    $ _pg_interject = vt_voice(_pg_girl, VT_PULLOUT_INTERJECT, "Wait -- pull out! I'm not on anything!")
    _pg_girl.character "[_pg_interject]"

    $ _pg_out = "respect"
    $ _pg_force_line = ""
    $ _pg_respect_line = ""
    $ _pg_menu_push = vt_voice(_pg_girl, VT_PULLOUT_MENU_PUSH_CAPTION, "Push her to let you finish inside")
    $ _pg_menu_respect = vt_voice(_pg_girl, VT_PULLOUT_MENU_RESPECT_CAPTION, "Respect her -- pull out")
    menu:
        "[_pg_menu_push]":
            $ _pg_pitch = _vt_resolve_words(_pg_girl, renpy.random.choice(VT_PULLOUT_PUSH))
            player.character "[_pg_pitch]"
            $ vt_try_creampie(_pg_girl, player)
            python:
                _pg_res = vt_pullout_result or {}
                _pg_out = _pg_res.get("outcome", "no_hard")
                _pg_line = _pg_res.get("line", "")
            if _pg_line:
                _pg_girl.character "[_pg_line]"

            if _pg_out in ("no_soft", "no_hard"):
                $ _pg_menu_force = vt_voice(_pg_girl, VT_PULLOUT_MENU_FORCE_CAPTION, "Force it anyway")
                $ _pg_menu_yield = vt_voice(_pg_girl, VT_PULLOUT_MENU_YIELD_CAPTION, "Fine -- pull out")
                menu:
                    "[_pg_menu_force]":
                        $ _pg_out = vt_try_force_creampie(_pg_girl, player)
                        # Her reaction to being forced is shown AFTER the act itself narrates
                        # below, not here -- lines like "I can feel it" only make sense once it's
                        # actually happened, not while the roll is still resolving.
                        python:
                            _pg_res = vt_pullout_result or {}
                            _pg_force_line = _pg_res.get("line", "")

                    "[_pg_menu_yield]":
                        pass

        "[_pg_menu_respect]":
            if vt_try_pullout_failure(_pg_girl, player):
                # A genuine mechanical failure -- her reaction and the impacts land AFTER the act
                # itself narrates, below (same reasoning as the force-outcome lines: "I can feel it"
                # only makes sense once it's actually happened).
                $ _pg_out = "pullout_fail"
            else:
                $ _pg_respect_line = vt_voice(_pg_girl, VT_PULLOUT_RESPECT, "Thank you for pulling out.")

    if _pg_out in ("yes_perm", "yes_session", "force_success", "pullout_fail"):
        # Finish inside. A forced or accidentally-failed outcome both skip the base label's own
        # baked-in description/reaction/response text -- that text assumes either consent or a
        # clean pull-out, either of which would contradict the line we're about to show her saying.
        $ _pg_skip_desc = skip_descriptions or (_pg_out in ("force_success", "pullout_fail"))
        $ _pg_skip_resp = skip_responses or (_pg_out in ("force_success", "pullout_fail"))
        if _pg_out in ("force_success", "pullout_fail"):
            $ store.vt_force_creampie_active = True
        $ store.vt_force_finisher_compensation = (_pg_out == "force_success")
        $ renpy.call(_pg_real, action_name=action_name, additional_subtags=additional_subtags, skip_descriptions=_pg_skip_desc, skip_responses=_pg_skip_resp)
        $ store.vt_force_finisher_compensation = False
        if _pg_out == "force_success":
            $ store.vt_force_creampie_active = False
            # Corruption is suppressed at the impact owner, before scaling/leveling; subtracting
            # a fixed amount afterward cannot cancel the scaled grant and can remove prior XP.
            $ _pg_girl.apply_impacts({"arousal": VT_FORCE_SUCCESS_GIRL_COMPENSATION["arousal"]})
            # Mod-authored override narration in place of the suppressed base text, then her
            # distressed reaction -- both shown now that the act has actually happened. A forced
            # virginity loss (her hymen/first_time_pussy state at attempt time, captured by
            # vt_try_force_creampie into vt_forced_girl_was_virgin) is a much bigger narrative beat
            # than a routine forced creampie, so it gets its own heavier content instead of reusing
            # the standard set.
            if store.vt_forced_girl_was_virgin:
                $ _pg_desc = renpy.random.choice(VT_FORCE_VIRGIN_DESCRIPTION)
                "[_pg_desc]"
                $ _pg_force_line = vt_voice(_pg_girl, VT_FORCE_VIRGIN_LINES, "...")
            else:
                $ _pg_desc = renpy.random.choice(VT_FORCE_DESCRIPTION)
                "[_pg_desc]"
            if _pg_force_line:
                _pg_girl.character "[_pg_force_line]"
        elif _pg_out == "pullout_fail":
            $ store.vt_force_creampie_active = False
            # No compensation/session-ending override here -- this is a blameless accident, not a
            # coercion outcome, so none of force_success's blame-laden machinery applies.
            $ _pg_desc = renpy.random.choice(VT_PULLOUT_FAIL_DESCRIPTION)
            "[_pg_desc]"
            $ _pg_fail_line = vt_voice(_pg_girl, VT_PULLOUT_FAIL_LINES, "...")
            if _pg_fail_line:
                _pg_girl.character "[_pg_fail_line]"
            if not getattr(_pg_girl, "birth_control", False):
                $ _pg_fail_worry = vt_voice(_pg_girl, VT_PULLOUT_FAIL_PREGNANCY_WORRY, "...")
                if _pg_fail_worry:
                    _pg_girl.character "[_pg_fail_worry]"
    else:
        # Pull out -> external cumshot.
        # The external action still owns all effects. Its usual grinding/pleasure text does
        # not describe withdrawing after a boundary, especially after a failed force attempt.
        $ store.vt_pullout_external_active = True
        $ renpy.call(_pg_pullout, action_name=action_name, additional_subtags=additional_subtags, skip_descriptions=True, skip_responses=True)
        $ store.vt_pullout_external_active = False
        if _pg_respect_line:
            _pg_girl.character "[_pg_respect_line]"
            $ _pg_girl.apply_impacts(dict(VT_PULLOUT_IMPACTS.get("respect", {})))
        if _pg_out == "force_fail" and _pg_force_line:
            # A failed force attempt still ends in the same pull-out -- her reaction to having
            # been pushed comes after that narrates, same reasoning as the success case above.
            _pg_girl.character "[_pg_force_line]"
    return

# Session-ending override, set by vt_try_force_creampie via se_end_label/se_use_generic_ending.
# Full replacement for a successful force -- generic_sex_ending's own praise-flavored text never
# plays. Reached by the base game's own screen_sex_interaction_menu.rpy jumping straight to
# se_end_label when se_use_generic_ending is False -- an existing, reusable override point already
# used by several base-game location/event files (e.g. label_home_visit_end_sex.rpy), not a
# base-file edit. Hands off to vt_forced_ending_handoff (below) rather than cleaning up and
# returning to the map directly, so the enclosing scene's own continuation still runs.
label vt_forced_sex_ending:
    python:
        _fe_girl = store.vt_forced_girl
        _fe_orgasmed = bool(_fe_girl) and getattr(_fe_girl, "sex_interaction_cum_count", 0) > 0

    if _fe_girl:
        $ _fe_lines = _vt_forced_conflicted_lines(_fe_girl) if _fe_orgasmed else VT_FORCED_ENDING_ANGRY
        $ _fe_line = vt_voice(_fe_girl, _fe_lines, "...")
        if _fe_line:
            _fe_girl.character "[_fe_line]"
        if not getattr(_fe_girl, "birth_control", False):
            $ _fe_worry = vt_voice(_fe_girl, VT_FORCED_ENDING_PREGNANCY_WORRY, "...")
            if _fe_worry:
                _fe_girl.character "[_fe_worry]"
        if store.vt_forced_girl_was_virgin:
            $ _fe_virgin_line = vt_voice(_fe_girl, VT_FORCED_ENDING_VIRGIN_ADDENDUM, "...")
            if _fe_virgin_line:
                _fe_girl.character "[_fe_virgin_line]"

    jump vt_forced_ending_handoff

# Session-ending append for a FAILED force attempt -- se_use_generic_ending is left as whatever the
# enclosing scene already set it to, so generic_sex_ending plays its normal text first if that scene
# wanted it (whatever the rest of the session earned), and its own tail (label_sex_ending.rpy) jumps
# here as a continuation once se_end_label is set to a non-"generic_sex_ending" value.
label vt_force_fail_followup:
    $ _fe_girl = store.vt_forced_girl
    if _fe_girl:
        $ _fe_line = vt_voice(_fe_girl, VT_FORCED_ENDING_ATTEMPT, "...")
        if _fe_line:
            _fe_girl.character "[_fe_line]"

    jump vt_forced_ending_handoff

# Shared tail for both endings above: hand off to whatever the enclosing scene (bar/pier/park/
# home-visit invite-home, etc.) had ORIGINALLY set se_end_label to, instead of discarding its own
# continuation (its "next morning" transition, its own sex_interaction_clear(), etc -- confirmed via
# label_bar_discussions.rpy:559, which calls sex_interaction_clear() itself right before its own
# `jump sleep`). We deliberately do NOT call sex_interaction_clear() ourselves before that hand-off --
# destination labels like bar_discussion_invite_home_end_sex still need se_participants populated to
# run their own morning scene. Only fall back to clearing/returning to the map ourselves when there
# was no original end label to hand off to (a plain, unwrapped sex interaction) -- the same fallback
# generic_sex_ending itself uses when se_end_label is falsy.
label vt_forced_ending_handoff:
    python:
        _fe_next_label = store.vt_orig_se_end_label
        store.vt_forced_girl = None
        store.vt_force_outcome_this_session = None
        store.vt_forced_girl_was_virgin = False
        store.vt_orig_se_end_label = None
        store.vt_orig_se_use_generic_ending = None

    if _fe_next_label:
        $ se_end_label = None
        $ se_use_generic_ending = False
        jump expression _fe_next_label
    else:
        $ sex_interaction_clear()
        jump expression global_current_location_label
