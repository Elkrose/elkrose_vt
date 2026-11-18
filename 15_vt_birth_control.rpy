# Birth-control presentation reads the decision captured before its owning impacts.
# No new saved preferences, relationship scores or permission grants live here.
init -3 python:
    def vt_bc_general_available(girl):
        return girl.affection >= 25

    def vt_bc_personal_available(girl, accepted_invite=False):
        return accepted_invite or vt_history_level(girl) > 0

    VT_BC_GENERAL_REPLIES = {
        "neutral": [
            "I think it's a conversation worth having before you need an answer.",
            "I'd want to know where we both stood before making any plans.",
            "It depends on what someone wants for their life. I can see why people make different choices.",
        ],
        "shy": [
            "I'd rather talk things through first. It would make me feel a little more at ease.",
            "I don't bring it up often, but I do think it's worth talking about.",
        ],
        "direct": [
            "It's worth talking about early. Nobody should have to guess what the other person wants.",
            "People make their own choices. I'd want us to be clear about where we both stand.",
        ],
    }

    def vt_bc_general_reply(girl):
        if girl.has_trait("secretive"):
            return renpy.random.choice((
                "I think it's sensible to talk about it. I tend to keep my own choices private.",
                "I'm happy to talk in general. The details are something I keep to myself.",
            ))
        return vt_voice(girl, VT_BC_GENERAL_REPLIES)

    VT_BC_REPLIES = {
        "stop": {
            "warm": {
                "neutral": ["I've been thinking about a baby with you too. Yes, I'll stop taking them.", "You didn't have to make a grand speech. I want this with you. I'll stop my birth control.", "That future has been on my mind. Yes. Let's give ourselves that chance."],
                "reserved": ["I've imagined it more often than I've admitted. Yes, I'll stop taking them.", "I needed a moment to say it aloud... but I do want a baby with you. I'll stop.", "This matters to me. If you're asking seriously, my answer is yes. I'll stop taking them."],
                "direct": ["Yes. I want a baby with you, and I'm done pretending I haven't thought about it. I'll stop.", "You could have just asked. I want that future with you too. The pills can go.", "You caught me hoping you'd bring this up. Yes, I'll stop taking them."],
            },
            "settled": {
                "neutral": ["Yes. I've thought about what this means, and I'm ready to stop taking them.", "I do want a baby. I'll stop my birth control and see where this takes us.", "I'm comfortable making that change. I'll stop taking them."],
                "reserved": ["It's a big decision, but I have thought about it. Yes, I'll stop.", "I wouldn't say yes lightly. I am ready to stop taking them.", "I've given this some thought. I'll stop my birth control."],
                "direct": ["Yes. I've made up my mind. I'll stop taking them.", "I know what I'm agreeing to. Let's give it a chance; I'll stop the pills.", "I'm ready for that possibility. I'll stop my birth control."],
            },
            "pressure": {
                "neutral": ["All right. I'll stop taking them. I'm still nervous about this, even if I've agreed.", "Okay... I'll do what you're asking and stop. I need you to understand that I'm uneasy.", "I'll stop my birth control. Please don't mistake that for me having no doubts."],
                "reserved": ["If that's what you want... I'll stop. I'm frightened of what comes next.", "All right. I'll stop taking them. Please give me a little room to get used to this.", "I hear you. I'll stop... but I can't pretend I'm completely at ease."],
                "direct": ["Fine. I'll stop the pills. That doesn't mean the worry has disappeared.", "I'll do it. Just don't expect me to sound thrilled while I'm still this nervous.", "Yes, I'll stop. I need you to hear the uncertainty in that answer too."],
            },
            "pressure_wait": {
                "neutral": ["I hear what you want. I'm not ready to stop taking them, though. We need to talk this through.", "I'm feeling pushed toward an answer. My birth control stays as it is for now.", "I can consider it, but I haven't agreed to stop. Give me time to think."],
                "reserved": ["Please give me a moment. I can't make that change just because I'm afraid to disappoint you.", "I understand what you're asking... but I haven't said yes. I'll keep taking them for now.", "I'm too unsettled to decide this now. Nothing changes today."],
                "direct": ["I heard the request. I haven't agreed to it. I'm staying on birth control for now.", "Don't turn my hesitation into a yes. We still need to talk.", "I might consider it. Pushing harder won't make me ready today."],
            },
            "considering": {
                "neutral": ["Part of me likes the idea, but I'm not ready to stop taking them. I'd like us to talk about what we both want.", "I've thought about it. I still need time before I change my birth control.", "Maybe. I'm considering it, but my answer today is to keep taking them."],
                "reserved": ["I can imagine that future... I'm just not ready to choose it yet. I'll stay on birth control for now.", "It's something I could think about with you. I haven't agreed to stop, though.", "Could we talk about this without deciding everything today? I'll keep taking them for now."],
                "direct": ["I'm interested, but I'm not there yet. The pills stay for now.", "That's a conversation we can have. It isn't a yes to stopping today.", "Maybe later. I'd like to think it through before changing anything."],
            },
            "hesitant": {
                "neutral": ["I'm not ready for that possibility. I'll keep taking my birth control.", "I understand why you're asking, but I don't want to stop right now.", "I need more certainty than I have today. Nothing changes for now."],
                "reserved": ["I don't think I could be comfortable with that right now. I'll keep taking them.", "I'm sorry... I'm not ready to stop my birth control.", "That's more than I can agree to today. I'd rather leave things as they are."],
                "direct": ["Not right now. I'm staying on birth control.", "I don't want to take that step yet. Let's leave it there.", "I heard you, but I'm not ready. I'll keep taking them."],
            },
            "refuse": {
                "neutral": ["No. I don't want to stop my birth control.", "I've made my choice. I'm keeping my birth control as it is.", "That isn't something I want. Please respect my answer."],
                "reserved": ["No... I'm keeping my birth control. I need you to accept that.", "I don't want this. Please don't ask me to pretend otherwise.", "My answer is no. I'd rather we moved on."],
                "direct": ["No. The birth control stays.", "I'm not agreeing to that. Let's change the subject.", "I don't want to stop. That's my answer."],
            },
        },
        "start": {
            "warm": {
                "neutral": ["I want us to enjoy what we have without rushing into parenthood. Yes, I'll start taking it.", "That makes sense for us right now. I'll start birth control.", "I'm glad we can talk about this together. Yes, I'll start taking it."],
                "reserved": ["I was hoping we could talk about this. Yes, I'll start birth control.", "I care about our future, and I'm happy to take things at this pace. I'll start taking it.", "Yes... that feels right for us just now. I'll start birth control."],
                "direct": ["Yes. I like what we have, and I'm in no rush for a baby. I'll start taking it.", "That's one decision we can agree on. I'll start birth control.", "I'm glad we're on the same page. I'll start taking it."],
            },
            "settled": {
                "neutral": ["Yes. I don't want to plan for a baby right now, so I'll start birth control.", "I've considered it, and I'm comfortable starting birth control.", "That fits what I want at the moment. I'll start taking it."],
                "reserved": ["I've thought about it. Yes, I'd like to start birth control.", "I don't feel ready for a baby. I'll start taking it.", "Yes. I've taken a little time to think, and I'm ready to make that choice."],
                "direct": ["Yes. A baby isn't what I want right now. I'll start birth control.", "That works for me. I'll start taking it.", "I've made up my mind: I'll start birth control."],
            },
            "pressure": {
                "neutral": ["All right. I'll start taking it. I'm still uneasy about this conversation.", "Okay... I'll do what you're asking and start birth control. I need a little time to settle.", "I'll start taking it. Please don't read that as me having no reservations."],
                "reserved": ["If that's what you want... I'll start taking it. I'm still nervous.", "All right. I'll start birth control. Please give me some room after this.", "I'll do it... but I'm not completely at ease with how we got here."],
                "direct": ["Fine. I'll start taking it. That doesn't make this an easy conversation.", "I'll do it. Just don't mistake a nervous yes for enthusiasm.", "Yes, I'll start birth control. I still have mixed feelings."],
            },
            "pressure_wait": {
                "neutral": ["I understand what you're asking. I'm not ready to start taking it, though.", "I'm feeling pushed into deciding. I haven't agreed to start birth control.", "I can consider it, but nothing changes today. I need time to think."],
                "reserved": ["Please give me a little time. I can't decide this because I'm afraid of disappointing you.", "I hear you... but I haven't said yes to starting birth control.", "I'm too unsettled to make that choice right now."],
                "direct": ["I heard you. I haven't agreed to start taking it.", "Don't make the decision for me. We still need to talk.", "I might consider it. I haven't agreed to change anything today."],
            },
            "considering": {
                "neutral": ["I can see why you're suggesting it. I'd like to think before I start taking it.", "Maybe. We should talk about what we each want before I change anything.", "I'm considering it, but I'm not ready to start birth control today."],
                "reserved": ["Could I have some time to think? I'm not saying yes just yet.", "I can talk about it with you. I haven't decided to start taking it, though.", "It's a lot to consider. I'd rather not make the choice today."],
                "direct": ["Maybe, but not today. I want to think it through.", "It's an option. I haven't decided to start taking it yet.", "Let's talk first. Nothing changes until I've made up my mind."],
            },
            "hesitant": {
                "neutral": ["I'm not comfortable starting birth control right now.", "I understand your point, but I don't want to start taking it yet.", "I still have too many doubts to make that change today."],
                "reserved": ["I don't think I'm ready to start taking it. Please give me time.", "I hear you... but it doesn't feel right for me at the moment.", "I'd rather leave things as they are for now."],
                "direct": ["Not right now. I'm not ready to start taking it.", "I get why you're asking, but my answer is no for now.", "I'm not comfortable with that change yet. Let's leave it there."],
            },
            "refuse": {
                "neutral": ["No. I don't want to start birth control.", "That isn't the choice I want to make. Please respect that.", "I've thought about it, and my answer is no."],
                "reserved": ["No... I don't want to start taking it. I need you to accept my answer.", "I don't want to make that change. Please don't press me.", "My answer is no. I'd like to move on."],
                "direct": ["No. I'm not starting birth control.", "I don't want to take it. That's my answer.", "I'm not agreeing to that. Let's talk about something else."],
            },
        },
    }

    def vt_bc_reply_tone(girl, band, details):
        """A score gained through fear is not an enthusiastic preference."""
        threshold = 75.0 if band == "eager" else 50.0
        pressured = details["fear_help"] > 0.0 and details["without_fear"] < threshold <= details["score"]
        if band == "eager":
            if pressured:
                return "pressure"
            return "warm" if getattr(girl, "affection", 0) >= 70 else "settled"
        if band == "conditional":
            return "pressure_wait" if pressured else "considering"
        return "hesitant" if band == "hesitant" else "refuse"

    def vt_bc_reply_pool(girl, ask, band, details, pitch="request"):
        direction = "start" if ask == "start_bc" else "stop"
        tone = vt_bc_reply_tone(girl, band, details)
        source = {key: list(lines) for key, lines in VT_BC_REPLIES[direction][tone].items()}
        if tone == "warm" and getattr(girl, "kids_with_player", 0) > 0:
            if direction == "stop":
                source["neutral"][0] = "Another baby with you... yes. I'll stop taking them."
                source["reserved"][0] = "I've caught myself imagining another baby with you. Yes, I'll stop."
                source["direct"][0] = "Yes. I want to add to the family we've started. I'll stop taking them."
            else:
                source["neutral"][0] = "I love the family we've started, and I'm not ready to add to it yet. I'll start birth control."
                source["reserved"][0] = "I'd like some time with the family we have. Yes, I'll start taking it."
                source["direct"][0] = "I love our family. I'm also ready for a pause before another baby. I'll start taking it."
        if band == "eager" and tone != "pressure":
            if pitch == "natural":
                source["neutral"][2] = "I've thought about more than just changing my routine. I'm ready for that possibility; I'll stop taking them."
            elif pitch == "thrill":
                source["direct"][2] = "I can enjoy the thought and still take it seriously. Yes, I'll stop taking them."
            elif pitch == "health":
                source["neutral"][2] = "I'm comfortable making that choice for myself. Yes, I'll start birth control."
        # Register shapes voice; role does not invent a family relationship or an opinion.
        return {"neutral": list(source["neutral"]), "demure": list(source["reserved"]),
                "shy": list(source["reserved"]), "direct": list(source["direct"]),
                "explicit": list(source["direct"]), "crude": list(source["direct"])}

    def vt_bc_reply(girl, ask, band, player=None, pitch="request", on_bc=True, details=None):
        if details is None:
            details = vt_bc_decision_details(girl, ask, player)
        # Already off BC: a discussion about trying must not claim a second pill change
        # or grant condom/finish permission. Keep the caller's existing impacts alone.
        if not on_bc and ask != "start_bc":
            if band == "eager":
                pool = {"neutral": ["I'm already off birth control. Yes, I'm willing to give that possibility a chance.",
                                    "There's no pill for me to stop. I am ready to talk seriously about a baby.",
                                    "I'm not taking birth control already. Yes, we can talk about trying."]}
                if vt_bc_reply_tone(girl, band, details) == "pressure":
                    pool = {"neutral": ["I'm already off birth control. All right... but I still feel uneasy about this.",
                                        "There's nothing for me to stop taking. I'll go along with what you're asking, though I'm nervous.",
                                        "I'm not on birth control. I hear what you want; please don't mistake my agreement for certainty."]}
            else:
                pool = {"neutral": ["I'm already off birth control, but that doesn't mean I've decided to try for a baby.",
                                    "Not taking the pill isn't the same as being ready for parenthood. I haven't agreed to that.",
                                    "My birth control hasn't changed. Neither has my answer about trying: I'm not ready."]}
            return vt_voice(girl, pool, "", player)
        return vt_voice(girl, vt_bc_reply_pool(girl, ask, band, details, pitch), "", player)
