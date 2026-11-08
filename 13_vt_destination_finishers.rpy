# VT-owned destination finish presentation. Permission and routing remain in script 12.
# Keep the existing public helpers/label names for saved and external callers.
# Impacts, callbacks, exposure, media and return order are unchanged by extraction.

init -3 python:
    VT_FINISH_ACTIONS = {"face": "facial", "mouth": "creampie_mouth", "boobs": "cumshot_boobs",
                         "thighs": "cumshot_thighs", "ass": "cumshot_ass", "creampie_ass": "creampie_ass"}

    def vt_apply_destination_finish(destination):
        previous = store.vt_oral_narration
        narration = []
        store.vt_oral_narration = narration
        try:
            apply_action_impacts(VT_FINISH_ACTIONS[destination])
        finally:
            store.vt_oral_narration = previous
        exposed = player.condom_active == "raw" or player.condom_broke
        if exposed:
            part = {"creampie_ass": "in_ass", "thighs": "legs"}.get(destination, destination)
            player.cum_splatter_girl(part, selected_girl)
            player.cum_splatter_clothes(part, selected_girl)
        # Replace the inherited duplicate action description, retaining first-time,
        # awareness and progression notifications after the complete callback loop.
        return [entry for entry in narration if entry[0] != "dialog"], exposed

init -3 python:
    VT_DESTINATION_AFTERMATH = {
     "contained": [
      "You cum hard into the condom. It holds, and you pull back carefully to keep it that way.",
      "Your release fills the tip of the condom, and it holds. You ease back, breathing hard.",
      "You finish with a groan, the condom catching all of it. You take a second before drawing back."],
     "unnoticed": [
      "As you pull back you see the tear in the condom. She hasn't noticed.",
      "Only afterward do you see the condom has split. Nothing in her face says she knows.",
      "The condom comes away torn. She is still catching her breath, unaware."],
     "noticed": [
      "The condom comes away torn, and she sees it the same moment you do.",
      "Her eyes go straight to the split condom. For a moment, she just looks at it.",
      "There's no missing the tear now. She stares at it, then at you."],
     # Exposed finishes are keyed by destination so each can name what happened.
     # "pussy" is absent: 11_vt_vaginal_finishers.rpy owns that finish and its narration.
     "mouth": [
      "You hold deep in her mouth and cum, emptying yourself until you're spent, then slowly pull out.",
      "You finish on her tongue, pulse after pulse, and she takes all of it before you draw back.",
      "You cum in her mouth with a groan. When you finally pull out, she swallows and lets out a long breath."],
     "creampie_ass": [
      "You bury yourself deep in her ass and cum, dumping your thick load until you're spent, then slowly pull out.",
      "You finish in her tight ass, pulse after pulse, and she takes all of it before you finally draw back.",
      "You cum inside her ass with a groan. When you do finally pull out, she lets out a long breath."],
     "face": [
      "You blast your cum across her face, leaving her marked and both of you breathing hard.",
      "You cum with a groan, painting her face with thick ropes. She blinks up at you through the mess.",
      "You finish right where she let you. It's messy, and she takes a second to wipe her eyes before looking at you."],
     "boobs": [
      "You blast your cum across her chest, leaving her marked and both of you breathing hard.",
      "You cum with a groan, painting her chest with thick ropes. You smile, admiring how good she looks covered in your seed.",
      "You finish right where she let you. It's messy, and she looks down at her chest, then up at you."],
     "thighs": [
      "You blast your cum across her thighs, leaving her marked and both of you breathing hard.",
      "You cum with a groan, striping her thighs with thick ropes. You smile, admiring the mess you've left on her.",
      "You finish right where she let you. It runs down her thighs, and she glances at it, then at you."],
     "ass": [
      "You blast your cum across her ass, leaving her marked and both of you breathing hard.",
      "You cum with a groan, painting her ass with thick ropes. You smile, admiring how good she looks covered in your seed.",
      "You finish right where she let you. It's messy, and she looks back over her shoulder at you."]}

    VT_DESTINATION_SETTLE = {
     "crude": ["Fuck... okay. Give me a second.", "Damn. That was something. Hang on.", "Shit, I need a minute after that."],
     "explicit": ["Mmm... don't move yet. Let me enjoy that.", "That's more like it. Give me a second to catch up.", "God. Okay... I need a breath."],
     "direct": ["Okay. Give me a sec.", "That works. Hold on a moment.", "Whew. Let me catch my breath."],
     "neutral": ["Wow... okay. Just a moment.", "Let me catch my breath.", "That was... yeah. Give me a second."],
     "shy": ["Um... c-can we stay like this a second?", "I... that was a lot. Just a moment.", "S-sorry, I just need a second..."],
     "demure": ["Goodness. Allow me a moment.", "That was... rather a lot. A moment, please.", "Let me collect myself, please."]}

    VT_DESTINATION_UNEASY = {
     "crude": ["Shit -- it broke? Fuck. Back off a second.", "Are you kidding me? The damn thing tore.", "Fuck. Back up. I need to see how bad that is."],
     "explicit": ["It broke? ...Shit. That wasn't the plan.", "Wait. Stop. That condom's done -- give me a second.", "Well, that's not what I agreed to. Let me think."],
     "direct": ["The condom broke. Stop. Let me deal with this.", "That tore. Give me a minute.", "Hold on. That's not what we agreed."],
     "neutral": ["Wait... it broke? Oh no.", "That's... not good. I need a moment.", "Please, just give me a minute. I wasn't ready for that."],
     "shy": ["I-it broke...? I... I need a second.", "Oh no... oh no. Please give me a moment.", "That... wasn't supposed to happen, was it?"],
     "demure": ["Oh dear. The condom has failed.", "That is not what I agreed to. Please give me a moment.", "I need a moment, please. This is... unexpected."]}

    def vt_destination_aftermath(girl, destination, exposed):
        if not exposed:
            key = "contained"
        elif player.condom_active != "raw":
            key = "unnoticed" if vt_finish_perceived_contained(girl, destination) else "noticed"
        else:
            key = destination
        return vt_booth_choice(girl, VT_DESTINATION_AFTERMATH[key])

label vt_destination_finisher(destination, action_name=None, additional_subtags=None, skip_descriptions=False, skip_responses=False, _vt_exposure_agreed=False):
    $ _vt_destination_notifications, _vt_destination_exposed = vt_apply_destination_finish(destination)
    $ vt_note_finish_closing(selected_girl, known_break=(_vt_destination_exposed and player.condom_active != "raw" and not vt_finish_perceived_contained(selected_girl, destination) and not _vt_exposure_agreed))
    $ renpy.retain_after_load()
    if _vt_destination_notifications:
        call vt_oral_action_continuation(_vt_destination_notifications)
    if _vt_destination_exposed:
        $ _vt_destination_action = VT_FINISH_ACTIONS[destination]
        if action_name:
            $ media_helper.show_video(_vt_destination_action + "_" + action_name, selected_girl, sub_tags=additional_subtags, default_to=_vt_destination_action)
        else:
            $ media_helper.show_video(_vt_destination_action, selected_girl, sub_tags=additional_subtags)
    if skip_descriptions and skip_responses and currently_playing_video:
        pause
    if not skip_descriptions:
        $ _vt_destination_line = vt_destination_aftermath(selected_girl, destination, _vt_destination_exposed)
        "[_vt_destination_line]"
    if not skip_responses:
        $ _vt_destination_pool = VT_DESTINATION_UNEASY if _vt_destination_exposed and not vt_finish_perceived_contained(selected_girl, destination) and not _vt_exposure_agreed else VT_DESTINATION_SETTLE
        $ _vt_destination_line = vt_booth_voice(selected_girl, _vt_destination_pool, "Give me a moment.")
        selected_girl.character "[_vt_destination_line]"
    $ media_helper.hide_video()
    return
