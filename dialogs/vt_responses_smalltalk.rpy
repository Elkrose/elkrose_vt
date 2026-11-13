# VT SMALL-TALK RESPONSE DATA
#
# Data for the dialog response engine (00_vt_dialog_engine.rpy / VT-Dialog-Response-System.md).
# DATA ONLY -- no control flow. Each entry: optional `when` conditions, optional `priority`,
# and a `lines` dict in vt_voice's register->variants shape. Omitted axes = "don't care";
# approach-specific entries out-specify the bare fallback, reproducing the old elif chain.
#
# Migration is behaviour-preserving: lines are lifted verbatim from the live trees in
# vt_small_talk_pregnancy.rpy. The live trees are NOT yet wired to call this -- that's a later phase.
#
# SEEDED SO FAR:
#   vaginal_condom_pref -- COMPLETE (68 entries): by_player, by_other, wants-condom, prefers-bare.
#   anal_condom_pref    -- COMPLETE (78 entries): general 39 [by_player(13, register-rich) +
#                          wants(13) + prefers-bare(13)] + anal-virgin overlay 39 [same shape,
#                          anal_virgin:True]. No parent/desire/pill (vaginal) axes -- anal = no preg
#                          risk. wants/prefers gated pregnancy in {none, by_other} (no anal by-other
#                          case). Virgin entries out-specify their general sibling by 1 condition ->
#                          win for anal virgins; general 39 are the experienced path, untouched.
#                          Virgin tone = RELUCTANCE ("gross/weird at first"), carried by the register
#                          ladder (demure/shy squeamish -> direct/crude reluctant-but-curious).
#   oral_condom_pref    -- COMPLETE (39 entries): by_player(13, register-rich) + wants(13) +
#                          prefers-bare(13). Same shape as anal; NO oral-virgin overlay (a first
#                          blowjob lacks anal's trepidation charge). Gated as anal.
#   bc_methods          -- COMPLETE (16 entries, register-rich): how she frames her CURRENT bc status.
#                          Branches birth_control x desire_tier x parent_broad x virgin x
#                          wants_vaginal_condom -- NO approach/role/pregnancy (the live `_bc_line`
#                          reads none of those). 2x3 grid: HIGH splits parent->virgin; ON-pill MID/LOW
#                          no sub-split; NOT-pill MID/LOW split virgin x wants (2x2). desire_tier per
#                          the engine fact (mid=30-70), matching the vaginal prefers-bare convention.
#   body_condom_pref    -- COMPLETE (13 entries, neutral-only): the 4th protection-menu sibling.
#                          approach x role (12) + one empty-when role-agnostic fallback for approaches
#                          outside the four known ones. External ejaculation = no preg risk, so no
#                          pregnancy/desire/virgin axes. Single-line source -> neutral-only.
#   pregnancy_feelings_supportive -- item 1 of the pregnancy-feelings menu ("This is a beautiful time
#                          in your life...", live ~3747-3885). PURE-LINE branches migrated (27 entries,
#                          neutral-only): compassionate/sexualized/dominate x desire_tier x role. The
#                          `transactional` approach embeds cash sub-menus -> stays in the label for now.
#                          pregnancy in {by_player, by_other} (the label's knows-pregnant gate).
#   pregnancy_feelings_fetish -- item 2 ("I love the idea of you carrying my child...", live ~3888-3959).
#                          PURE-LINE branches migrated (9 entries, neutral-only): compassionate/
#                          sexualized/dominate x role (no desire_tier -- only transactional splits, >50).
#                          transactional (cash sub-menu + role-split disgust else) AND the trailing else
#                          (unknown approach disgust line) stay in the label; no empty-when fallback here
#                          (it would misroute transactional's role-split disgust text).
# TODO (next): pregnancy-feelings items 3-5 (practical/nurturing[mother]/school[student]) +
#   the prenatal-vitamins beat; each leaves its transactional cash sub-menus in the label.
# REWORDED (2026-07-09) to fit the EXPERIENCED path -- the general (non-virgin) entries baked in
#   first-timer language that only the anal-virgin overlay should carry: general sexualized/student/
#   prefers-bare in BOTH anal (:852) and oral (:1437) said "I've never..." (now "nothing between us,
#   that sounds so exciting!"); anal compassionate/student/wants (:792) said "I'm nervous about anal...
#   I've heard it can be risky" (now "I'm always careful about anal... I know it can be risky without it").
#   These 3 table lines now DIVERGE (intentionally) from their live counterparts (live 2520/2861/2480,
#   still un-reworded) -- the fix lands for players when Phase-2 rewiring points the live tree at vt_say.
#
# VALIDATED: exec + matcher sweep over 720 not-pregnant states -> exactly 1 winner each (no ties);
# cross-state isolation holds (pregnant+wants_condom routes to by_player, not wants-condom).

init python:

    vt_register_responses("vaginal_condom_pref", [

        # ---- pregnancy == by_player : she's carrying his child, so virginity is moot. -------------
        # compassionate
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "mother", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next baby now, and we already have our little one. After all my body has given you, I don't want anything between us -- just you."],
            "shy":      ["I-I'm pregnant with your next... and we have our child already. After everything, we... we don't really need that barrier anymore, do we?"],
            "neutral":  ["I'm already carrying your next baby, and we have our child. As the mother of your children, I don't need a condom between us -- I just want to feel you."],
            "direct":   ["I'm carrying your next and we've already got one. No barrier needed now -- I want to feel all of you."],
            "explicit": ["I'm pregnant with your next baby and we made a child before. There's nothing left to guard against -- I want you bare inside me, nothing in the way."],
            "crude":    ["I'm knocked up with your next and we've already got a kid -- a condom's pointless now. Just take me bare, I want to feel you."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "mother", "parent": False}, "lines": {
            "demure":   ["I'm already carrying your baby. As a mother, I know my body can handle this -- and I'd rather have nothing between us now."],
            "shy":      ["I-I'm pregnant with your baby already... so we don't really need that barrier between us anymore, do we?"],
            "neutral":  ["I'm already carrying your baby. As an experienced mother, I know there's nothing to protect against now -- I just want to feel you."],
            "direct":   ["I'm carrying your baby already. No need for a barrier now -- I want to feel you completely."],
            "explicit": ["I'm pregnant with your baby. The risk is already behind us -- so take me bare, I want to feel every inch with nothing in the way."],
            "crude":    ["I'm already knocked up -- what's a condom for now? Just fuck me bare, I want to feel you."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "student", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next baby, Professor... and we have our other one. So... we don't need condoms anymore, do we? That's kind of wonderful."],
            "shy":      ["I-I'm pregnant with your next baby, Professor! And we already have our little one... so I guess we don't need condoms now, right? That's... amazing."],
            "neutral":  ["I'm carrying your next baby, Professor, and we have our other one. So we really don't need condoms anymore -- and honestly, I love that."],
            "direct":   ["I'm pregnant with your next, Professor, and we've already got one. No more condoms needed -- I want to feel you."],
            "explicit": ["I'm carrying your next baby, Professor! We've already made one, so there's nothing to stop now -- I want to feel you bare inside me."],
            "crude":    ["I'm knocked up with your next, Professor, and we've got a kid already -- so screw the condoms, I just want to feel you raw."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "student", "parent": False}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... so I guess we don't need condoms anymore, do we? That's... kind of wonderful."],
            "shy":      ["I-I'm pregnant with your baby, Professor! Wow... so we don't need condoms now, right? That's... kind of amazing."],
            "neutral":  ["I'm carrying your baby, Professor. So we don't really need condoms anymore -- and I kind of love how close that makes us."],
            "direct":   ["I'm pregnant with your baby, Professor. No more condoms needed now -- I want to feel you."],
            "explicit": ["I'm carrying your baby, Professor! There's nothing left to protect against, so... I want to feel you bare inside me."],
            "crude":    ["I'm knocked up already, Professor -- so screw the condoms, I just want to feel you raw."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "other", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next baby, and we have our child. I want to feel you completely now, with nothing between us. We're closer than ever."],
            "shy":      ["I-I'm pregnant with your next... and we already have our little one. So we don't need that barrier anymore, do we?"],
            "neutral":  ["I'm carrying your next baby, and we have our child. I want to feel you completely, with nothing between us."],
            "direct":   ["I'm pregnant with your next and we've got one already. No barrier now -- I want to feel all of you."],
            "explicit": ["I'm carrying your next baby; we've already made one. Nothing to guard against now -- I want you bare, filling me with nothing in the way."],
            "crude":    ["I'm knocked up with your next and we've got a kid -- the condom's pointless. Take me bare, I want to feel you."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "other", "parent": False}, "lines": {
            "demure":   ["I'm already carrying your baby. I want to feel you completely now, with nothing between us. It's a special kind of closeness."],
            "shy":      ["I-I'm pregnant with your baby already... so we don't really need that barrier between us anymore, do we?"],
            "neutral":  ["I'm already carrying your baby. I want to feel you completely, with nothing between us -- it's its own kind of intimacy now."],
            "direct":   ["I'm carrying your baby already. No barrier needed now -- I want to feel all of you."],
            "explicit": ["I'm pregnant with your baby. The risk is behind us -- so take me bare, I want to feel you with nothing in the way."],
            "crude":    ["I'm already knocked up -- a condom's pointless now. Just fuck me bare, I want to feel you."],
        }},

        # sexualized
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "mother", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next baby already... and we've made a child before. There's something thrilling about being bare with you now -- no need to hold back."],
            "shy":      ["I-I'm pregnant with your next... we already have one, and the thought of you bare again makes me blush. No condoms now, right?"],
            "neutral":  ["I'm pregnant with your next baby, and we've already made one. An experienced mother going bare again, feeling you finish inside me -- it's the hottest thing I know."],
            "direct":   ["I'm carrying your next and we've got one already. No condom -- I want to feel you cum inside me, nothing in the way."],
            "explicit": ["I'm pregnant with your next baby! Being bare again, knowing you already bred me once... feeling you fill me while I'm carrying is unbelievably hot."],
            "crude":    ["I'm already knocked up with your next, and we've got a kid -- so fuck the condom and breed me bare again. Feeling you cum in me is the hottest thing there is."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "mother", "parent": False}, "lines": {
            "demure":   ["I'm carrying your baby... and being bare with you now, knowing it already happened, feels deliciously freeing."],
            "shy":      ["I-I'm pregnant already... the thought of you finishing inside me with nothing between us makes me so flustered. No condom now, hm?"],
            "neutral":  ["I'm pregnant with your baby. An experienced woman like me being bare, feeling you cum inside while I carry your child -- it's the hottest thing I've felt."],
            "direct":   ["I'm carrying your baby. No condom -- I want to feel you cum inside me bare."],
            "explicit": ["I'm pregnant with your baby! Being bare, feeling you fill me while I'm already carrying you... it's the ultimate thrill."],
            "crude":    ["I'm already knocked up -- so fuck the condom and cum in me bare. Feeling you breed me while I'm carrying is unreal."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "student", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next baby, Professor... and we have our other one. The idea of you bare again is so exciting -- no condoms now, right?"],
            "shy":      ["I-I'm pregnant with your next, Professor! And we have our little one... oh my god, you can cum in me bare again! It feels so naughty."],
            "neutral":  ["I'm pregnant with your next baby, Professor, and we already have one. You can finish inside me bare again -- and honestly it's so hot."],
            "direct":   ["I'm carrying your next, Professor, and we've got one already. No condom -- cum inside me, I want to feel it."],
            "explicit": ["I'm pregnant with your next baby, Professor! You can fill me bare again -- we've already made one, so there's nothing stopping you. So hot!"],
            "crude":    ["I'm knocked up with your next, Professor, and we've got a kid -- so cum in me raw again. God, feeling you breed me is so fucking hot."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "student", "parent": False}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... so you can be bare with me now, can't you? The thought of it makes me tingle."],
            "shy":      ["I-I'm pregnant with your baby, Professor! Oh my god, you can cum inside me with no condom now! That's so... wow, it feels naughty."],
            "neutral":  ["I'm pregnant with your baby, Professor. You can finish inside me bare now -- and I didn't expect how hot that would feel."],
            "direct":   ["I'm carrying your baby, Professor. No condom needed -- cum inside me, I want to feel it."],
            "explicit": ["I'm pregnant with your baby, Professor! You can fill me bare now -- there's nothing to stop you anymore. It's so hot."],
            "crude":    ["I'm already knocked up, Professor -- so cum in me raw. God, feeling you breed me with nothing in the way is so fucking hot."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "other", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next baby, and we have our child. Being bare with you now feels thrilling -- there's nothing left to hold back."],
            "shy":      ["I-I'm pregnant with your next... we have our little one already, and the thought of you bare again makes me shiver."],
            "neutral":  ["I'm carrying your next baby, and we made one before. Feeling you cum inside me bare again, while I carry your child, is the ultimate thrill."],
            "direct":   ["I'm pregnant with your next and we've got one. No condom -- I want to feel you cum in me bare."],
            "explicit": ["I'm carrying your next baby! Being bare again, knowing we already made a child... feeling you fill me is the ultimate thrill."],
            "crude":    ["I'm knocked up with your next and we've got a kid -- so breed me bare again. Feeling you cum in me is the hottest thing there is."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "other", "parent": False}, "lines": {
            "demure":   ["I'm carrying your baby... so being bare with you now feels exciting and free. No need to hold back."],
            "shy":      ["I-I'm pregnant with your baby already... the thought of you finishing inside me with nothing between us makes me so flustered."],
            "neutral":  ["I'm pregnant with your baby. Of course I want you bare -- feeling you cum inside me while I carry your child is the ultimate thrill."],
            "direct":   ["I'm carrying your baby. No condom -- I want to feel you cum inside me bare."],
            "explicit": ["I'm pregnant with your baby! Of course I want you bare -- feeling you fill me while I'm carrying is the ultimate thrill."],
            "crude":    ["I'm already knocked up -- so fuck the condom and cum in me bare. Feeling you breed me is unreal."],
        }},

        # transactional
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "mother", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next child, and we have one already. As the mother of your children, bare access is simply part of our arrangement now -- no extra charge, provided you keep supporting them."],
            "shy":      ["I-I'm pregnant with your next... and we have our child. So I suppose bare is just... part of the deal now? No extra charge, as long as you provide for them."],
            "neutral":  ["I'm carrying your next child. As an experienced mother to both, bare access is part of our established family arrangement -- no additional charge, but I expect you to uphold your end for both children."],
            "direct":   ["I'm carrying your next, and we've got one. Bare's included in the family arrangement now -- no charge, but keep up your support."],
            "explicit": ["I'm pregnant with your next. Bare access is part of our family package now -- you finish in me at no extra cost, so long as you provide for our children."],
            "crude":    ["I'm knocked up with your next and we've got a kid -- so bare's just part of the deal now. No charge to cum in me, long as you pay for them."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "mother", "parent": False}, "lines": {
            "demure":   ["I'm carrying your child now. As a mother, bare access is part of our arrangement -- no extra charge, as long as you uphold the support."],
            "shy":      ["I-I'm pregnant with your baby... so bare is just part of the deal now, isn't it? No extra charge, if you provide for us."],
            "neutral":  ["I'm carrying your child. As an experienced mother, bare access is now part of our family arrangement -- no additional charge, though I expect you to uphold your end of the support."],
            "direct":   ["I'm carrying your child. Bare's included in the arrangement now -- no charge, but keep up your support."],
            "explicit": ["I'm pregnant with your child. Bare access comes with the package now -- you finish in me at no extra cost, provided you provide."],
            "crude":    ["I'm knocked up -- so bare's part of the deal now. No charge to cum in me, long as you pay your share."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "student", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next baby, Professor... and we have our other one. So bare's just included now, isn't it? Part of the family deal."],
            "shy":      ["I-I'm carrying your next, Professor... we already have one, so this is just... part of the arrangement now, right? Bare's free?"],
            "neutral":  ["I'm carrying your next baby, Professor, and we have one already. So bare access is just part of our deal now -- included, right?"],
            "direct":   ["I'm pregnant with your next, Professor, and we've got one. So bare's part of the package now -- no extra charge, yeah?"],
            "explicit": ["I'm carrying your next, Professor. We've already got one, so bare access is just part of the family deal now -- you finish in me, no charge."],
            "crude":    ["I'm knocked up with your next, Professor, and we've got a kid -- so cumming in me bare is just part of the deal now, right? No charge."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "student", "parent": False}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... so does that mean bare is just free now? Part of the deal?"],
            "shy":      ["I-I'm carrying your baby, Professor... so does bare cost the same now, or is it just... included? I'm not sure how it works for this."],
            "neutral":  ["I'm carrying your baby, Professor... so does that mean bare access is free now? Or do I still get paid for it? I'm not sure on the pricing here."],
            "direct":   ["I'm pregnant with your baby, Professor. So bare's just included now, right? No charge?"],
            "explicit": ["I'm carrying your baby, Professor. So you finishing in me bare is just part of the deal now -- no extra charge, since it's already done?"],
            "crude":    ["I'm knocked up, Professor -- so cumming in me bare is free now, yeah? Nothing left to charge for."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "other", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next child, and we have one already. As the father of both, bare access is part of our ongoing arrangement -- no extra charge."],
            "shy":      ["I-I'm pregnant with your next... we already have a child, so bare is just part of the family deal now, isn't it?"],
            "neutral":  ["I'm carrying your next child. Since you're the father to both, bare access is included in our ongoing family package -- no additional charge."],
            "direct":   ["I'm carrying your next, and you father both -- so bare's included in the arrangement now. No charge."],
            "explicit": ["I'm pregnant with your next. You father both children, so bare access is part of the package -- you finish in me at no extra cost."],
            "crude":    ["I'm knocked up with your next and you've got a kid with me -- so bare's just part of the deal. No charge to cum in me."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "other", "parent": False}, "lines": {
            "demure":   ["I'm carrying your child now. Since you're the father, bare access is part of the arrangement -- no extra charge."],
            "shy":      ["I-I'm pregnant with your baby... so bare is just included now, isn't it? Since you're the father."],
            "neutral":  ["I'm carrying your child. Since you're the father, bare access is included in the pregnancy package -- no additional charge."],
            "direct":   ["I'm carrying your child. You're the father, so bare's included now -- no charge."],
            "explicit": ["I'm pregnant with your child. You father it, so bare access comes with the package -- you finish in me at no extra cost."],
            "crude":    ["I'm knocked up and you're the father -- so bare's part of the deal now. No charge to cum in me."],
        }},

        # dominate
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "mother", "parent": True}, "lines": {
            "demure":   ["I am carrying your next child, Master, and we have one already. Protection is needless now -- you may take me as you wish, the mother of your children."],
            "shy":      ["I-I'm carrying your next, Master... and we have our child. There's no need for protection now... you may do as you please with me."],
            "neutral":  ["I am carrying your next child, Master. As the mother of your children, I know protection is unnecessary now. You may proceed as you wish."],
            "direct":   ["I'm carrying your next, Master, and we've got one. Protection's pointless now -- take me however you want."],
            "explicit": ["I am carrying your next child, Master. There is nothing left to guard against -- use the mother of your children bare, as you please."],
            "crude":    ["I'm knocked up with your next, Master, and we've got a kid -- so no condom. Use me bare, however you fucking want."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "mother", "parent": False}, "lines": {
            "demure":   ["I am carrying your child, Master. Protection is needless now -- you may take me as you wish."],
            "shy":      ["I-I'm carrying your baby, Master... so there's no need for protection now. You may do as you please."],
            "neutral":  ["I am carrying your child, Master. As an experienced mother, I know protection is unnecessary. You may proceed as you wish."],
            "direct":   ["I'm carrying your child, Master. Protection's pointless now -- take me however you want."],
            "explicit": ["I am carrying your child, Master. Nothing left to guard against -- use me bare, as you please."],
            "crude":    ["I'm knocked up, Master -- so no condom. Use me bare, however you fucking want."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "student", "parent": True}, "lines": {
            "demure":   ["I'm carrying your next baby, Professor... and we have our other one. So if you don't want a condom, that's okay. Whatever you want, for our family."],
            "shy":      ["I-I'm carrying your next, Professor... we have our child already... so if you'd rather go without, I'll do whatever you want."],
            "neutral":  ["I'm carrying your next baby, Professor, and we have one already -- so if you don't want a condom, that's okay. Whatever you want is what I'll do for our family."],
            "direct":   ["I'm pregnant with your next, Professor, and we've got one. If you don't want a condom, I'll do whatever you want."],
            "explicit": ["I'm carrying your next, Professor. If you want me bare, take me bare -- whatever you want, I'm yours."],
            "crude":    ["I'm knocked up with your next, Professor -- so if you want to fuck me bare, do it. Whatever you want."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "student", "parent": False}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... so if you don't want to use a condom, that's okay. Whatever you want."],
            "shy":      ["I-I'm carrying your baby, Professor... so if you'd rather go without a condom now, I'll do whatever you want."],
            "neutral":  ["I'm carrying your baby, Professor... so if you don't want to use a condom, that's okay. Whatever you want is what I'll do."],
            "direct":   ["I'm pregnant with your baby, Professor. If you don't want a condom, I'll do whatever you want."],
            "explicit": ["I'm carrying your baby, Professor. If you want me bare, take me bare -- whatever you want, I'm yours."],
            "crude":    ["I'm knocked up, Professor -- so if you want to fuck me bare, do it. Whatever you want."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "other", "parent": True}, "lines": {
            "demure":   ["I am carrying your next child, Master, and we have one already. Protection is unnecessary now -- proceed as you wish with the mother of your child."],
            "shy":      ["I-I'm carrying your next, Master... we have our little one... so there's no need for protection. Do as you please."],
            "neutral":  ["I am carrying your next child, Master. Protection is unnecessary now. Proceed as you wish with the mother of your child."],
            "direct":   ["I'm carrying your next, Master, and we've got one. Protection's pointless -- take me however you wish."],
            "explicit": ["I am carrying your next child, Master. Nothing to guard against now -- use me bare, as you please."],
            "crude":    ["I'm knocked up with your next, Master, and we've got a kid -- no condom. Use me bare, however you want."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "other", "parent": False}, "lines": {
            "demure":   ["I am carrying your child, Master. Protection is unnecessary now -- proceed as you wish."],
            "shy":      ["I-I'm carrying your baby, Master... so there's no need for protection now. Do as you please."],
            "neutral":  ["I am carrying your child, Master. Protection is unnecessary for vaginal sex now. Proceed as you wish."],
            "direct":   ["I'm carrying your child, Master. Protection's pointless -- take me however you wish."],
            "explicit": ["I am carrying your child, Master. Nothing to guard against -- use me bare, as you please."],
            "crude":    ["I'm knocked up, Master -- so no condom. Use me bare, however you want."],
        }},

        # fallback approach (unknown / other initial_reaction) -- lower specificity, no `approach` key
        {"when": {"pregnancy": "by_player", "parent": True}, "lines": {
            "demure":   ["I'm pregnant with your next baby... and we already have one. So condoms aren't really needed anymore, are they?"],
            "shy":      ["I-I'm carrying your next... and we have our little one. So we don't really need condoms now, do we?"],
            "neutral":  ["I'm pregnant with your next baby, and we already have one. So condoms aren't really necessary anymore, are they?"],
            "direct":   ["I'm carrying your next and we've got one already -- so condoms aren't really needed now, right?"],
            "explicit": ["I'm pregnant with your next baby and we've made one before -- so there's no real point to condoms now, is there?"],
            "crude":    ["I'm knocked up with your next and we've got a kid -- condoms are pointless now, yeah?"],
        }},
        {"when": {"pregnancy": "by_player", "parent": False}, "lines": {
            "demure":   ["I'm pregnant with your baby... so condoms aren't really needed anymore, are they?"],
            "shy":      ["I-I'm carrying your baby... so we don't really need condoms now, do we?"],
            "neutral":  ["I'm pregnant with your baby... so condoms aren't really necessary anymore, are they?"],
            "direct":   ["I'm carrying your baby -- so condoms aren't really needed now, right?"],
            "explicit": ["I'm pregnant with your baby -- so there's no real point to condoms now, is there?"],
            "crude":    ["I'm knocked up already -- condoms are pointless now, yeah?"],
        }},

        # ---- pregnancy == by_other : awkward honesty; standing condom preference still governs. ----
        {"when": {"pregnancy": "by_other", "wants_vaginal_condom": True}, "lines": {
            "demure":   ["This is... awkward, but you should know -- I'm already pregnant. It isn't yours, and I'm sorry. It doesn't change what I want with you, though: I'd still rather we used a condom. That matters to me regardless."],
            "shy":      ["Um... I-I have to be honest. I'm already pregnant... and it's not yours. I'm so sorry. But it doesn't change anything between us -- I'd still want a condom. Please."],
            "neutral":  ["I'll be straight with you, even if it's awkward -- I'm already pregnant, and it isn't yours. That said, it doesn't change what I want from you: I still want us using condoms."],
            "direct":   ["Awkward truth -- I'm already pregnant, and no, not yours. Doesn't change what I want with you, though. The condom stays on. That's just me."],
            "explicit": ["I'll be blunt, even if it's weird -- I'm knocked up already, and it's not yours. Doesn't change a thing between us: I still want you wrapped when you fuck me."],
            "crude":    ["Real talk, even if it's fucked -- I'm already pregnant, not by you. Doesn't change what I want, though. Condom stays on when you fuck me."],
        }},
        {"when": {"pregnancy": "by_other", "wants_vaginal_condom": False}, "lines": {
            "demure":   ["This is awkward, but you deserve honesty -- I'm already pregnant. It isn't yours, and I'm sorry. It doesn't change what I want with you, though... and there's nothing left to risk now, so I'd still rather have nothing between us."],
            "shy":      ["Um... I-I should be honest. I'm already pregnant, and... it's not yours. I'm sorry. It doesn't change us, though -- and, well, there's nothing to risk now, so I-I'd still prefer bare."],
            "neutral":  ["Honest truth, awkward as it is -- I'm already pregnant, and it's not yours. It doesn't change what I want from you. And since the risk's already moot, I'd still rather skip the condom."],
            "direct":   ["Awkward but fair -- I'm already pregnant, not yours. Doesn't change what I want with you. Can't exactly get more pregnant, so no condom -- I want to feel you."],
            "explicit": ["Blunt version -- I'm already knocked up, and it's not yours. Doesn't change a thing between us. Nothing left to risk, so skip the condom and let me feel you bare."],
            "crude":    ["Real talk -- I'm already pregnant, not by you. Doesn't change what I want. Can't knock me up twice, so fuck the condom and give it to me bare."],
        }},

    ])

    # ---- not pregnant, WANTS A CONDOM : approach x role x parent(kids_with_player>0). --------------
    # Gated on pregnancy=="none" so a pregnant girl who also wants a condom can't tie the by_player set.
    vt_register_responses("vaginal_condom_pref", [

        # compassionate
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "compassionate", "role": "mother", "parent": True}, "lines": {
            "demure":   ["As a mother already, I have to be careful for the little one we have. When we're close, I need that protection -- I couldn't bear another pregnancy just yet."],
            "shy":      ["I-I have our child to think of... so when you're with me, I really do need that protection. I'm not ready for another so soon."],
            "neutral":  ["As an experienced mother, I have to be careful for the child we already have. When you're inside me, I need that protection. I can't risk another pregnancy right now."],
            "direct":   ["We've got a child already, so I have to be careful. When you're inside me, keep it covered -- I can't risk another pregnancy yet."],
            "explicit": ["I love feeling close to you, but we've got a baby already -- so wrap it when you fuck me. I can't get knocked up again this soon."],
            "crude":    ["I've already got your kid -- so keep it wrapped when you fuck me. Much as I'd love your cum, I'm not getting knocked up again right now."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "compassionate", "role": "mother", "parent": False}, "lines": {
            "demure":   ["As a mother with responsibilities, I have to be careful. When we're close, I need that protection -- I couldn't risk a pregnancy right now."],
            "shy":      ["I-I have responsibilities... so when you're with me, I really do need that protection. I can't risk it right now."],
            "neutral":  ["As an experienced mother with responsibilities, I have to be careful. When you're inside me, I need that protection. I can't risk another pregnancy right now."],
            "direct":   ["I've got responsibilities, so I have to be careful. When you're inside me, keep it covered -- I can't risk a pregnancy now."],
            "explicit": ["I love being close to you, but I have to be smart -- so wrap it when you fuck me. I can't afford to get knocked up right now."],
            "crude":    ["Much as I'd love your cum, I can't get knocked up right now -- so keep it wrapped when you fuck me."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "compassionate", "role": "student", "parent": True}, "lines": {
            "demure":   ["I feel so close to you, Professor... but we have our little one, and I couldn't manage another so soon. When we're together, I need that protection."],
            "shy":      ["I-I feel so close to you... but we have our child, and I'm scared of another so soon. When we're together, I need that protection, Professor."],
            "neutral":  ["I feel so close to you, but I'm also really scared... we have our child, and I can't handle another one so soon. When we're together, I need that protection, Professor."],
            "direct":   ["I'm close to you, Professor, but we've got a kid already -- I can't handle another yet. Keep it covered when we're together."],
            "explicit": ["You make me want you so bad, Professor... but we've got a baby already. Wrap it when you take me -- I can't get knocked up again this soon."],
            "crude":    ["God, I want you, Professor -- but we've already got a kid. Keep it wrapped when you fuck me, I can't get knocked up again yet."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "compassionate", "role": "student", "parent": False}, "lines": {
            "demure":   ["I feel so close to you, Professor... but I'm not ready to be a mother yet. When we're together, I think I need that protection."],
            "shy":      ["I-I feel so close to you... but I'm scared. When we're together, I think I need that protection. I'm not ready to be a mom yet, Professor."],
            "neutral":  ["I feel so close to you, but I'm also really scared... when we're together, I think I need that protection. I'm not ready to be a mom yet, Professor."],
            "direct":   ["I'm close to you, Professor, but I'm not ready to be a mom. Keep it covered when we're together, okay?"],
            "explicit": ["You make me want you so much, Professor... but I'm not ready for a baby. Wrap it when you take me -- I can't risk getting knocked up."],
            "crude":    ["God, I want you, Professor -- but I'm not trying to be a mom yet. Keep it wrapped when you fuck me."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "compassionate", "role": "other", "parent": True}, "lines": {
            "demure":   ["I feel connected to you... but we have a child to think of. When we're intimate, I need that protection -- it lets me relax and enjoy you."],
            "shy":      ["I-I feel so connected to you... but we have a little one. When we're intimate, I need that protection, so I can relax."],
            "neutral":  ["I feel connected to you, but we have a child to think about. When we're intimate, I need that layer of protection. It lets me relax and enjoy the moment without worrying about another."],
            "direct":   ["I'm connected to you, but we've got a child. When we're intimate, keep it covered -- then I can actually relax and enjoy you."],
            "explicit": ["I love how connected we are, but we've got a baby already. Wrap it when you fuck me -- then I can let go and enjoy every second."],
            "crude":    ["I'm crazy about you, but we've got a kid -- so keep it wrapped when you fuck me. Then I can stop worrying and just enjoy your cock."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "compassionate", "role": "other", "parent": False}, "lines": {
            "demure":   ["I feel connected to you... but when we're intimate, I need that protection. It lets me relax and truly enjoy the moment."],
            "shy":      ["I-I feel so connected to you... but when we're intimate, I need that protection, so I can relax and enjoy it."],
            "neutral":  ["I feel connected to you, but when we're intimate, I need that layer of protection. It lets me relax and enjoy the moment without worrying."],
            "direct":   ["I'm connected to you, but when we're intimate, keep it covered -- then I can actually relax and enjoy you."],
            "explicit": ["I love how connected we are, but wrap it when you fuck me -- then I can let go and enjoy every second without worrying."],
            "crude":    ["I'm crazy about you -- but keep it wrapped when you fuck me. Then I can stop worrying and just enjoy your cock."],
        }},

        # sexualized
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "sexualized", "role": "mother", "parent": True}, "lines": {
            "demure":   ["The way you look at me makes me melt... but we have our child, and I must be sensible. Honestly, watching you put one on -- caring for our family -- is its own quiet thrill."],
            "shy":      ["Y-you make me feel so hot... but we have our little one, so I have to be smart. Watching you roll one on... it's kind of sexy that you respect our family."],
            "neutral":  ["The way you look at me is so hot... but we have a child, and I have to be smart. Watching you roll a condom on before you take me shows you respect our family, and that's a turn-on."],
            "direct":   ["You make me so hot... but we've got a kid, so play it smart. Honestly, watching you glove up before you take me is its own kind of sexy."],
            "explicit": ["God, you make me wet... but we've got a baby already, so wrap it. Watching you roll it on before you fuck me? Weirdly hot."],
            "crude":    ["Fuck, you get me dripping... but we've got a kid, so keep it wrapped. Watching you snap that condom on before you ruin me is hotter than it should be."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "sexualized", "role": "mother", "parent": False}, "lines": {
            "demure":   ["The way you look at me makes me melt... but as a mother I must be sensible. Watching you put one on, respecting my situation, is its own quiet thrill."],
            "shy":      ["Y-you make me feel so hot... but I have to be smart. Watching you roll one on... honestly it's kind of sexy that you respect my situation."],
            "neutral":  ["The way you look at me is so hot... but as an experienced mother, I need to be smart. Watching you roll a condom on before you take me shows you respect my situation, and that's a turn-on."],
            "direct":   ["You make me so hot... but I've got to be smart. Watching you glove up before you take me is its own kind of sexy."],
            "explicit": ["God, you make me wet... but I have to be responsible, so wrap it. Watching you roll it on before you fuck me? Weirdly hot."],
            "crude":    ["Fuck, you get me dripping... but I've got to be smart, so keep it wrapped. Watching you snap that condom on before you ruin me is hotter than it should be."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "sexualized", "role": "student", "parent": True}, "lines": {
            "demure":   ["You make me feel so warm... but we have our little one, and I'm nervous about another. Watching you put one on makes me feel safe -- and a bit sexy, oddly."],
            "shy":      ["You make me feel so hot... but we have our child, and I'm scared of getting pregnant again. Watching you put a condom on makes me feel safer... and kind of sexy in a responsible way?"],
            "neutral":  ["You make me feel so hot... but we have our child, and I'm so nervous about getting pregnant again. Watching you put on a condom makes me feel safer... and actually kind of sexy in a responsible way?"],
            "direct":   ["You make me so hot, Professor... but we've got a kid, and I'm nervous about another. Honestly, watching you glove up is kind of sexy."],
            "explicit": ["God, you get me going, Professor... but we've got a baby and I can't risk another. Watching you wrap it before you take me is hotter than I'd admit."],
            "crude":    ["Fuck, you make me wet, Professor... but we've got a kid, so keep it wrapped. Watching you snap that condom on is weirdly hot."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "sexualized", "role": "student", "parent": False}, "lines": {
            "demure":   ["You make me feel so warm... but I'm nervous about getting pregnant. Watching you put one on makes me feel safe -- and a bit sexy, oddly."],
            "shy":      ["You make me feel so hot... but I'm so scared of getting pregnant. Watching you put a condom on makes me feel safer... and kind of sexy in a responsible way?"],
            "neutral":  ["You make me feel so hot... but I'm so nervous about getting pregnant. Watching you put on a condom makes me feel safer... and actually kind of sexy in a responsible way?"],
            "direct":   ["You make me so hot, Professor... but I'm nervous about getting pregnant. Honestly, watching you glove up is kind of sexy."],
            "explicit": ["God, you get me going, Professor... but I can't risk getting knocked up. Watching you wrap it before you take me is hotter than I'd admit."],
            "crude":    ["Fuck, you make me wet, Professor... but I'm not getting knocked up. Watching you snap that condom on is weirdly hot."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "sexualized", "role": "other", "parent": True}, "lines": {
            "demure":   ["The way you look at me makes me melt... but we have a child now. Watching you put one on, thinking of our family, is its own quiet kind of sexy."],
            "shy":      ["Y-you make me so hot... but we have a little one. Watching you roll one on, thinking about our family... it's kind of sexy, honestly."],
            "neutral":  ["The way you look at me is so hot... but we have a child now. Watching you roll a condom on before you fuck me shows you're thinking about our family, which is its own kind of sexy."],
            "direct":   ["You make me so hot... but we've got a kid now. Watching you glove up before you fuck me -- thinking of our family -- is its own kind of sexy."],
            "explicit": ["God, you make me wet... but we've got a baby, so wrap it. Watching you roll it on before you fuck me is hotter than it has any right to be."],
            "crude":    ["Fuck, you get me dripping... but we've got a kid, so keep it wrapped. Watching you snap it on before you wreck me is stupidly hot."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "sexualized", "role": "other", "parent": False}, "lines": {
            "demure":   ["The way you look at me makes me melt... but watching you put one on can be its own quiet kind of sexy. It's like teasing what's coming."],
            "shy":      ["Y-you make me so hot... but honestly, watching you roll one on is kind of sexy too. It's like a little tease before."],
            "neutral":  ["The way you look at me is so hot... but watching you roll a condom on before you fuck me can be its own kind of sexy. It's like teasing what's to come."],
            "direct":   ["You make me so hot... but watching you glove up before you fuck me is its own kind of sexy. Call it a tease."],
            "explicit": ["God, you make me wet... but watching you roll it on before you fuck me is hotter than it should be. The anticipation does it for me."],
            "crude":    ["Fuck, you get me dripping... but watching you snap that condom on before you ruin me is its own kind of hot. Tease me with it."],
        }},

        # transactional
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "transactional", "role": "mother", "parent": True}, "lines": {
            "demure":   ["Let's be clear about terms. As the mother of your child, allowing you inside me with protection comes at a price -- my safety and our child's wellbeing are worth it."],
            "shy":      ["Um... to be clear... as the mother of your child, letting you... with a condom... that costs a little extra. My safety has a price."],
            "neutral":  ["Let's be clear. As the mother of your child, letting you fuck my pussy with a condom costs extra. My safety and our child's wellbeing have a price."],
            "direct":   ["Terms first. I'm the mother of your child -- so condom access to my pussy carries a premium. My safety isn't free."],
            "explicit": ["Let's be clear. You want to fuck my pussy wrapped? As the mother of your child, that's a premium service -- my safety and our kid's future cost extra."],
            "crude":    ["Get it straight. You want to fuck this pussy with a rubber on? That costs you -- I'm the mother of your kid, my safety's not cheap."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "transactional", "role": "mother", "parent": False}, "lines": {
            "demure":   ["Let's be clear about terms. As an experienced mother, allowing you inside me with protection comes at a price -- my safety and my child's wellbeing are worth it."],
            "shy":      ["Um... to be clear... as a mother already, letting you... with a condom... that costs a little extra. My safety has a price."],
            "neutral":  ["Let's be clear. As an experienced mother, letting you fuck my pussy with a condom costs extra. My safety and my existing child's wellbeing have a price."],
            "direct":   ["Terms first. I'm already a mother -- so condom access to my pussy carries a premium. My safety isn't free."],
            "explicit": ["Let's be clear. You want to fuck my pussy wrapped? As a mother already, that's a premium -- my safety and my kid's future cost extra."],
            "crude":    ["Get it straight. You want this pussy with a rubber on? That costs you -- I've got a kid to protect, my safety's not cheap."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "transactional", "role": "student", "parent": True}, "lines": {
            "demure":   ["What's in it for me? We have a child, so letting you... with protection... is about keeping our family safe. That carries a cost, Professor."],
            "shy":      ["Um... what do I get? We have our child, so letting you... you know... with a condom is about protecting our family. That's going to cost extra, Professor."],
            "neutral":  ["What's in it for me? We have a child, so letting you... you know... with a condom is about protecting our family. That's going to cost you extra, Professor."],
            "direct":   ["What do I get out of it? We've got a kid, Professor -- so condom access is about protecting our family. That's a premium."],
            "explicit": ["What's in it for me, Professor? We've got a baby, so you fucking me wrapped is the safe option -- and the safe option costs extra."],
            "crude":    ["What's it worth to you, Professor? We've got a kid -- so you want this pussy wrapped, that's a premium. Safety ain't free."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "transactional", "role": "student", "parent": False}, "lines": {
            "demure":   ["What's in it for me? Letting you... with protection... um, does that cost less than without? I'm honestly not sure how to price this, Professor."],
            "shy":      ["Um... what do I get? Letting you... you know... with a condom... does that cost less than without? I'm not sure about the pricing here, Professor."],
            "neutral":  ["What's in it for me? Letting you... you know... with a condom... um, does that cost less than without? I'm not sure about the pricing here, Professor."],
            "direct":   ["What do I get? Letting you in with a condom -- does that cost more or less than bare? I'm not sure how to price it, Professor."],
            "explicit": ["What's in it for me, Professor? You fucking me wrapped -- is that cheaper than bare, or more? I genuinely don't know the rate for this."],
            "crude":    ["What's it worth, Professor? You want this pussy with a rubber -- does that cost more or less than raw? I haven't figured the pricing."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "transactional", "role": "other", "parent": True}, "lines": {
            "demure":   ["What's in it for me? We have a child. Allowing you inside me with protection is the safer choice for our family -- so it carries a premium."],
            "shy":      ["Um... what do I get? We have a little one, so letting you... with a condom is the safer option for our family. That costs a bit extra."],
            "neutral":  ["What's in it for me? We have a child. Letting you fuck my pussy with a condom costs extra. It's the safer option for our family, so you pay a premium."],
            "direct":   ["What do I get? We've got a kid -- condom access to my pussy is the safe choice for the family, so it's a premium."],
            "explicit": ["What's in it for me? We've got a baby, so you fucking me wrapped is the safe play -- and safe costs extra."],
            "crude":    ["What's it worth? We've got a kid -- you want this pussy wrapped, that's the safe option, so you pay more for it."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "transactional", "role": "other", "parent": False}, "lines": {
            "demure":   ["What's in it for me? Allowing you inside me with protection is the safer choice -- so naturally it carries a premium."],
            "shy":      ["Um... what do I get? Letting you... with a condom is the safer option, so it costs a little extra."],
            "neutral":  ["What's in it for me? Letting you fuck my pussy with a condom costs extra. It's the safer option, so you pay a premium for the reduced risk."],
            "direct":   ["What do I get? Condom access to my pussy is the safe choice, so it's a premium. Reduced risk, higher rate."],
            "explicit": ["What's in it for me? You fucking me wrapped is the low-risk option -- and low-risk costs extra."],
            "crude":    ["What's it worth? You want this pussy wrapped, that's the safe play -- so you pay more for it. Simple."],
        }},

        # dominate
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "dominate", "role": "mother", "parent": True}, "lines": {
            "demure":   ["You are in command, Master. As the mother of your child, if you wish to use a condom, I will accept it -- I must keep our little one safe."],
            "shy":      ["Y-you decide, Master. As the mother of your child... if you wish protection, I'll accept it. I must keep our child safe."],
            "neutral":  ["You are in charge, Master. As the mother of your child, if you wish to use a condom, I will accept it. I must prioritize the safety of the child we already have."],
            "direct":   ["Your call, Master. I'm the mother of your child -- if you want a condom, I'll take it. Our child's safety comes first."],
            "explicit": ["You command me, Master. If you wish to fuck me wrapped, I submit to it -- I must protect the child we already made."],
            "crude":    ["I'm yours to use, Master -- if you want to fuck me with a rubber on, I'll take it. I've got to keep our kid safe."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "dominate", "role": "mother", "parent": False}, "lines": {
            "demure":   ["You are in command, Master. As a mother already, if you wish to use a condom, I will accept it -- I must keep my child safe."],
            "shy":      ["Y-you decide, Master. As a mother already... if you wish protection, I'll accept it. I must keep my child safe."],
            "neutral":  ["You are in charge, Master. As an experienced mother, if you wish to use a condom, I will accept it. I must prioritize the safety of the child I already have."],
            "direct":   ["Your call, Master. I'm already a mother -- if you want a condom, I'll take it. My child's safety comes first."],
            "explicit": ["You command me, Master. If you wish to fuck me wrapped, I submit to it -- I must protect the child I already have."],
            "crude":    ["I'm yours to use, Master -- if you want to fuck me with a rubber on, I'll take it. I've got a kid to keep safe."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "dominate", "role": "student", "parent": True}, "lines": {
            "demure":   ["You're in command, Professor... but we have our little one. If you wish to use protection when we're together, I'll do as you say. It's for the best."],
            "shy":      ["Y-you're in charge, Professor. But we have a child. If you want to use a condom when we... do it... I'll do what you want. It's probably best."],
            "neutral":  ["You're in charge, Professor. But we have a child. If you want to use a condom when we... do it... I'll do what you want. It's probably for the best."],
            "direct":   ["Your call, Professor. But we've got a kid -- if you want a condom when we do it, I'll do what you want."],
            "explicit": ["You decide, Professor. We've got a baby, so if you want to fuck me wrapped, I'll obey. Whatever you say."],
            "crude":    ["I do as you say, Professor -- we've got a kid, so if you want to fuck me with a rubber, I'll take it. Your call."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "dominate", "role": "student", "parent": False}, "lines": {
            "demure":   ["You're in command, Professor. If you wish to use protection when we're together, I'll do exactly as you say. Your choice is what matters."],
            "shy":      ["Y-you're in charge, Professor. If you want to use a condom when we... do it... I'll do what you want. Your choice is what matters."],
            "neutral":  ["You're in charge, Professor. If you want to use a condom when we... do it... I'll do what you want. Your choice is what matters."],
            "direct":   ["Your call, Professor. If you want a condom when we do it, I'll do exactly what you say."],
            "explicit": ["You decide, Professor. If you want to fuck me wrapped, I'll obey -- whatever you want from me."],
            "crude":    ["I do as you say, Professor -- if you want to fuck me with a rubber, I'll take it. Your call, always."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "dominate", "role": "other", "parent": True}, "lines": {
            "demure":   ["You are in command. As the mother of your child, if you wish to use a condom before taking me, I will accept it -- for our family's sake."],
            "shy":      ["Y-you decide. As the mother of your child... if you wish protection before entering me, I'll accept it, for our family."],
            "neutral":  ["You are in charge. As the mother of your child, if you wish to use a condom before entering my pussy, I will accept it for the sake of our family."],
            "direct":   ["Your call. I'm the mother of your child -- if you want a condom before you enter me, I'll accept it. For the family."],
            "explicit": ["You command me. If you wish to fuck me wrapped, I submit -- for the sake of the child we made."],
            "crude":    ["I'm yours to use -- if you want to fuck me with a rubber on, I'll take it. We've got a kid; I'll do what keeps them safe."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "approach": "dominate", "role": "other", "parent": False}, "lines": {
            "demure":   ["You are in command. If you wish to use a condom before taking me, I will accept it without question."],
            "shy":      ["Y-you decide. If you wish to use protection before entering me, I'll accept it."],
            "neutral":  ["You are in charge. If you wish to use a condom before entering my pussy, I will accept it."],
            "direct":   ["Your call. If you want a condom before you enter me, I'll accept it without question."],
            "explicit": ["You command me. If you wish to fuck me wrapped, I submit to it -- whatever you want."],
            "crude":    ["I'm yours to use -- if you want to fuck me with a rubber on, I'll take it. However you want me."],
        }},

        # fallback approach (unknown / other initial_reaction)
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "parent": True}, "lines": {
            "demure":   ["I'd prefer we use condoms... we have a child, and it simply feels safer for me right now."],
            "shy":      ["Um... I'd rather use condoms. We have a little one, and it just feels safer for me right now."],
            "neutral":  ["I prefer using condoms for vaginal sex... we have a child, and it's just safer that way for me right now."],
            "direct":   ["I'd rather use condoms for this. We've got a kid -- it's just safer for me right now."],
            "explicit": ["Let's use condoms for this. We've got a baby already, so I'd rather play it safe right now."],
            "crude":    ["Keep it wrapped for this -- we've already got a kid, and I'm not risking another right now."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": True, "parent": False}, "lines": {
            "demure":   ["I'd prefer we use condoms... it simply feels safer for me right now."],
            "shy":      ["Um... I'd rather use condoms. It just feels safer for me right now."],
            "neutral":  ["I prefer using condoms for vaginal sex... it's just safer that way for me right now."],
            "direct":   ["I'd rather use condoms for this. It's just safer for me right now."],
            "explicit": ["Let's use condoms for this. I'd rather play it safe right now."],
            "crude":    ["Keep it wrapped for this -- I'm not risking it right now."],
        }},

    ])

    # ---- not pregnant, PREFERS BARE : keyed on baby_desire tier x pill x virgin (+ broad parent). --
    # Structural note: only the >70 tier has a parent branch, and it takes precedence over virgin
    # (so the virgin entry carries parent_broad:False). Mid/low tiers split on virgin only.
    vt_register_responses("vaginal_condom_pref", [

        # desire HIGH (>70), on the pill -- aching to be bred, tempted to throw the pills out
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "high", "birth_control": True, "parent_broad": True}, "lines": {
            "demure":   ["I'm on the pill... but after carrying your child once, I keep looking at that little packet and thinking how easy it'd be to just stop. No condom either way -- I want to feel you."],
            "shy":      ["Um... I-I'm on the pill, but... having already had your baby, part of me wants to quietly stop taking it. No condom, please -- I want all of you."],
            "neutral":  ["I'm on the pill -- though honestly, after carrying your child, I keep thinking about throwing them out. Skip the condom regardless; I want to feel you bare again."],
            "direct":   ["I'm on the pill, for now. But I've had your baby once, and I keep eyeing those pills like I should toss them. No condom -- I want you bare."],
            "explicit": ["I'm on the pill, but after you bred me once I can't stop thinking about flushing them and letting you fill me raw again. Definitely no condom -- I want every drop."],
            "crude":    ["I'm on the pill, but fuck it, I keep wanting to chuck the things so you can knock me up again. No condom -- breed me bare like before."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "high", "birth_control": True, "virgin": True, "parent_broad": False}, "lines": {
            "demure":   ["I'm on the pill... but I confess I daydream about stopping. I've never even done it, yet I picture my first time leading somewhere more. No condom, please -- I want to feel you."],
            "shy":      ["Um... I-I'm on the pill, but part of me wants to stop. I've never done it, so it's all in my head, but I imagine you bare, no condom... maybe more than that."],
            "neutral":  ["I'm on the pill, though I keep thinking I'd toss it. I've never done it, so it's only imagination -- but I want my first time bare, no condom, nothing held back."],
            "direct":   ["I'm on the pill, but honestly I want to quit it. I've never done it yet, so it's fantasy -- but when it happens I want you raw, no condom, come what may."],
            "explicit": ["I'm on the pill, but I keep imagining throwing it out. I'm still a virgin, so it's pure fantasy -- but I want my first time to be your bare cock filling me, nothing stopping a baby."],
            "crude":    ["I'm on the pill but I want to ditch it. Haven't even been fucked yet, but when you take me I want it raw, no condom -- breed me on my first if it happens."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "high", "birth_control": True}, "lines": {
            "demure":   ["I'm on the pill... but having felt you bare, I keep thinking how easy it'd be to simply stop. No condom regardless -- I want all of you."],
            "shy":      ["Um... I-I'm on the pill, but I... I keep wanting to stop taking it. No condom either way -- I want to feel you like before."],
            "neutral":  ["I'm on the pill, though I keep eyeing them and thinking I should quit. Skip the condom -- I've had you bare and I want it again."],
            "direct":   ["I'm on the pill, for now. I've had you raw and I keep wanting to toss the pills. No condom -- I want all of you."],
            "explicit": ["I'm on the pill, but I crave going raw with you again so badly I keep thinking of flushing them. No condom -- fill me bare like you used to."],
            "crude":    ["I'm on the pill, but I keep wanting to chuck them so you can breed me bare again. No condom -- fuck a baby into me like before."],
        }},

        # desire HIGH (>70), NOT on the pill -- breed me, don't pull out
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "high", "birth_control": False, "parent_broad": True}, "lines": {
            "demure":   ["I'd rather we went without... after carrying your child, having nothing between us feels like where we're meant to be. I want to feel all of you."],
            "shy":      ["Um... I-I don't really want a condom. After our baby, going bare just feels... right. I want to feel you, all of you."],
            "neutral":  ["Honestly, I'd skip it. After carrying your child, bare is what feels natural to me now -- I want to feel you completely."],
            "direct":   ["No condom for me. I've already had your baby -- I want to feel you bare inside me again, nothing in the way."],
            "explicit": ["Skip the condom. After you bred me once, I crave your raw cock filling me again -- I want to feel every inch with nothing between us."],
            "crude":    ["Fuck the condom. You already knocked me up once -- put that bare cock back in me and breed me again."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "high", "birth_control": False, "virgin": True, "parent_broad": False}, "lines": {
            "demure":   ["I'd rather go without... I know I've never done it, but when I imagine my first time, it's just you and me, nothing in between. That's how I want it."],
            "shy":      ["Um... no condom. I-I've never done it, so this is all in my head, but... I picture my first time bare. It feels more real that way."],
            "neutral":  ["I think I'd want to go bare. I've never actually done it, so it's only imagination -- but I want my first time to be just us, nothing between us."],
            "direct":   ["No condom. I've never done it yet, so it's all fantasy -- but I want my first time raw, feeling you with nothing in the way."],
            "explicit": ["Skip the condom. I'm still a virgin, so it's pure fantasy -- but I want my first time to be your bare cock filling me, no barriers."],
            "crude":    ["No condom. Haven't even been fucked yet, but when you take my virginity I want it raw -- I want you to breed me bare for my first."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "high", "birth_control": False}, "lines": {
            "demure":   ["I'd rather not... having felt you bare, anything between us just feels wrong now. I want all of you."],
            "shy":      ["Um... no condom. Once I felt you without one, I... I couldn't go back. I want to feel you, properly."],
            "neutral":  ["I'd skip it. I've felt you bare before, and honestly nothing else compares -- I want to feel you completely."],
            "direct":   ["No condom. I've had you bare and I'm not going back -- I want to feel every inch of you, nothing in the way."],
            "explicit": ["Skip it. I know exactly how your raw cock feels, and I crave it -- I want you bare, filling me with nothing between us."],
            "crude":    ["Fuck the condom. I've had your bare cock and I want it again -- stretch me out raw and don't hold back."],
        }},

        # desire MID (30-70), on the pill -- prefers bare for the feel
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "mid", "birth_control": True, "virgin": True}, "lines": {
            "demure":   ["I think I'd like to go without... I've never actually done it, so I'd be a little nervous, but I want my first time to feel close and real."],
            "shy":      ["Um... I-I'd rather not use one. I've never done it, so it's a bit scary, but... bare just feels more like how I imagine it."],
            "neutral":  ["I'd lean toward bare. I've never done it, so I can't really compare -- but I want my first time to be just us, no barrier."],
            "direct":   ["No condom, I think. I've never done it yet, so it's all imagination -- but I want my first time to feel like just us."],
            "explicit": ["I'd go bare. I'm still a virgin, so it's fantasy for now -- but when it happens, I want to feel you raw, not through latex."],
            "crude":    ["Skip the rubber. Haven't been fucked yet, but when I am, I want to actually feel the cock, not a condom."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "mid", "birth_control": True}, "lines": {
            "demure":   ["I'd rather go without... it just feels closer that way. I'll be sensible about it, but I do prefer bare."],
            "shy":      ["Um... I-I like it better without one. I know I should be careful, but bare just feels nicer."],
            "neutral":  ["I prefer bare, honestly. It feels better -- I just stay on top of the careful part myself."],
            "direct":   ["No condom for me. I like the real thing -- I keep myself covered with the pill, so we're fine."],
            "explicit": ["I'd skip it. I love feeling a bare cock -- I'm on the pill, so you can enjoy me raw without the worry."],
            "crude":    ["Lose the condom. I want to feel that bare cock -- I'm on the pill, so just fuck me raw."],
        }},

        # desire MID (30-70), NOT on the pill -- ambivalent, pull out or don't, your call
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "mid", "birth_control": False, "virgin": True}, "lines": {
            "demure":   ["I'd want to go without... I've never done it, so I'm only imagining. I'm not on anything, so maybe you'd pull out -- or maybe not. I think I'd leave that up to you."],
            "shy":      ["Um... no condom. I-I've never done it, and I'm not on the pill, so... you'd have to decide whether to pull out. I-I kind of like leaving it to you."],
            "neutral":  ["I'd lean bare. I've never done it, so it's all imagination -- and I'm not on anything, so pulling out would be your call. Honestly, I'd let you choose."],
            "direct":   ["No condom, I think. I've not done it yet, and I'm not on the pill -- so pull out or don't, your call. I like the idea of leaving it to you."],
            "explicit": ["Skip the condom. I'm a virgin and not on anything, so whether you pull out or finish in me is up to you. The not-knowing is half the thrill."],
            "crude":    ["No rubber. Haven't been fucked yet and I'm not on the pill, so pull out or breed me -- your choice. I kinda want it out of my hands."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "mid", "birth_control": False}, "lines": {
            "demure":   ["I'd rather go bare... I'm not on anything right now, so you'd have to pull out -- or not. I think I'd leave that decision to you."],
            "shy":      ["Um... I-I like it without. I'm not on the pill, so... pull out, maybe? Or don't. I-I kind of want it to be your call."],
            "neutral":  ["I prefer bare. I'm not on anything at the moment, so pulling out's on you -- and honestly, I like leaving that choice in your hands."],
            "direct":   ["No condom for me. I'm not on the pill, so pull out or don't -- your call. There's something hot about not deciding it myself."],
            "explicit": ["Skip it, I want you bare. I'm not on anything, so whether you pull out or fill me is up to you. Leaving that risk to you is half the fun."],
            "crude":    ["Lose the condom. I'm not on the pill, so pull out or cum in me -- your choice. I kinda love not being the one who decides."],
        }},

        # desire LOW (<30), on the pill -- careful, prefers bare for the feel
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "low", "birth_control": True, "virgin": True}, "lines": {
            "demure":   ["I think I'd like to go without... I've never done it, so I'm only imagining, but bare sounds like the nicer way. And I'm on the pill, so a baby isn't a worry -- it could just be you and me."],
            "shy":      ["Um... I-I haven't done it yet, so this is all in my head, but bare sounds better. I'm on the pill, though, so I don't have to be scared of getting pregnant."],
            "neutral":  ["I've never actually done it, so I'm guessing -- but bare sounds better to me. I'm on the pill, so the worry's handled; a baby is genuinely the last thing I want."],
            "direct":   ["I've not done it yet, so it's all imagination -- but bare sounds like the better part. I'm on the pill, so we're covered. I want the fun, not a kid."],
            "explicit": ["I'm still a virgin, so it's pure imagination -- but going bare sounds like how it ought to feel. I'm on the pill, though; getting knocked up is a hard no. So you could enjoy me raw."],
            "crude":    ["Haven't been fucked yet, so I'm just guessing -- but I bet a bare cock beats a condom. I'm on the pill, though, 'cause no fucking way I'm getting pregnant."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "low", "birth_control": True}, "lines": {
            "demure":   ["I'd rather go without... but carefully. I love the feel, yet a baby would be a real problem for me -- so the pill it is."],
            "shy":      ["Um... I-I do prefer bare, but I'm careful about it. I stay on the pill, because I really can't be pregnant right now."],
            "neutral":  ["I prefer bare, but I'm responsible -- I stay on the pill, because a pregnancy is the last thing I want."],
            "direct":   ["No condom, I like it raw -- but I'm on the pill and I stay on it. Fun, yes; a baby, no."],
            "explicit": ["I love it bare, so skip the condom -- but I'm on the pill. Cum in me all you want, just don't expect a kid out of it."],
            "crude":    ["Ditch the condom, I want it raw -- but I'm on the pill, so breed all you want, you're not actually knocking me up."],
        }},

        # desire LOW (<30), NOT on the pill -- doesn't want a baby, pull out, it's on you
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "low", "birth_control": False, "virgin": True}, "lines": {
            "demure":   ["I'd like to go without... I've never done it, so it's only imagining. But I'm not on anything, so you'd have to promise to pull out. A baby would be too much for me right now -- I'm trusting you with that."],
            "shy":      ["Um... I-I'd prefer bare, but I'm not on the pill, so... you'd have to pull out. Please? I-I really can't be pregnant -- I'm leaving that in your hands."],
            "neutral":  ["I'd want it bare -- I've never done it, so I can only imagine. But I'm not on anything, so you'd need to pull out. I really don't want a baby, so that part's on you."],
            "direct":   ["Bare, I think -- but I'm not on the pill, so you pull out, no exceptions. I've never done it, but I know I don't want a kid. I'm leaving that to you to handle."],
            "explicit": ["I want it raw -- I'm a virgin, so it's fantasy for now. But I'm not on anything, so you have to pull out before you finish. A baby's a hard no; I'm trusting you to make the call."],
            "crude":    ["Fuck the condom, I want to feel it -- but I'm not on the pill, so you'd better pull out. Haven't been bred and I'm not starting now. That's on you to get right."],
        }},
        {"when": {"pregnancy": "none", "wants_vaginal_condom": False, "desire_tier": "low", "birth_control": False}, "lines": {
            "demure":   ["I'd rather go without... but I'm not on anything right now, so you'd have to pull out. A baby would be a real problem for me -- I'm trusting you with that."],
            "shy":      ["Um... I-I do like it bare, but I'm not on the pill, so... you'd need to pull out. I really can't be pregnant right now -- I'm leaving it to you."],
            "neutral":  ["I prefer bare, but I'm not on anything at the moment, so you'd have to pull out. A pregnancy is the last thing I want -- so I'm putting that in your hands."],
            "direct":   ["No condom, I like it raw -- but I'm not on the pill, so you pull out, every time. Fun, yes; a baby, no. I'm trusting you to handle it."],
            "explicit": ["I love it bare, so skip the condom -- but I'm not on anything, so you pull out before you cum. I'm not getting knocked up; that part's on you to get right."],
            "crude":    ["Ditch the condom, I want it raw -- but I'm not on the pill, so you'd better pull out in time. I'm not getting bred -- that's on you."],
        }},

    ])

    # =============================================================================================
    # ANAL CONDOM PREFERENCE  (live tree: vt_small_talk_pregnancy.rpy ~2341-2540)
    # Anal has no pregnancy risk, so this beat branches on approach x role ONLY -- no parent /
    # desire_tier / birth_control / virgin axes. The pill is vaginal-only; the pregnant-by-player
    # "bare" wish here is PURE DESIRE / surrender, never a risk-removal claim.
    #
    # PARTITION: by_player entries carry pregnancy=="by_player"; the standing-preference (wants /
    # prefers-bare) entries carry pregnancy in {none, by_other} -- the anal tree has NO by-other
    # special case, so a pregnant-by-other girl falls through to her standing anal preference,
    # exactly as the live `elif wants_anal_condom / else` does. The two sets never co-match.
    # =============================================================================================

    # ---- pregnancy == by_player : lifted verbatim from the already-vt_voice'd block (2344-2472). --
    vt_register_responses("anal_condom_pref", [

        # compassionate
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "mother"}, "lines": {
            "demure":   ["I'm already carrying your child... so feeling you with nothing between us, even there, is just about how close I want to be to you. Nothing held back."],
            "shy":      ["I-I'm already pregnant with your baby... so the thought of feeling you bare, even in my ass, it... it would mean being so close to you. I'd want that."],
            "neutral":  ["I'm already carrying your baby, Professor. As an experienced mother, wanting you bare in my ass isn't about anything but feeling all of you -- it would be incredibly intimate."],
            "direct":   ["I'm carrying your child. I want to feel you bare in my ass -- not for any other reason than wanting all of you, nothing between us."],
            "explicit": ["I'm pregnant with your baby. I want your bare cock in my ass, skin to skin -- feeling you that deep with nothing in the way is what I crave."],
            "crude":    ["I'm already knocked up -- so I want you raw in my ass. Nothing between us, just feeling you fill me completely."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "student"}, "lines": {
            "demure":   ["Since I'm carrying your baby, Professor... could we be bare even for that? It feels like it would be so close and special."],
            "shy":      ["I-I'm already pregnant with your baby, Professor... so feeling you bare, even in my ass? That sounds intense, but... really intimate. I think I'd want it."],
            "neutral":  ["I'm carrying your baby, Professor. So feeling you bare in my ass would be such an intimate thing to share with you -- I want that closeness."],
            "direct":   ["I'm pregnant with your baby, Professor. I want to feel you bare in my ass too -- nothing between us, just you."],
            "explicit": ["I'm carrying your baby, Professor! So I want to feel your bare cock in my ass -- skin on skin, nothing in the way. It would feel so close."],
            "crude":    ["I'm already knocked up, Professor -- so I want you raw in my ass too. I want to feel all of you, nothing between us."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "other"}, "lines": {
            "demure":   ["I'm already carrying your child... so feeling you bare, even there, is just about how close I want to be. Nothing held back between us."],
            "shy":      ["I-I'm already pregnant with your baby... so the thought of you bare in my ass, it... it would be such a close, intimate thing."],
            "neutral":  ["I'm already carrying your baby. Feeling you bare in my ass would just be another way to feel all of you -- I want that intimacy with you."],
            "direct":   ["I'm carrying your child. I want to feel you bare in my ass -- nothing between us, just feeling all of you."],
            "explicit": ["I'm pregnant with your baby. I want your bare cock in my ass too -- skin to skin, feeling you that deep with nothing in the way."],
            "crude":    ["I'm already knocked up -- so I want you raw in my ass. Nothing between us, just you filling me."],
        }},

        # sexualized
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "mother"}, "lines": {
            "demure":   ["I'm carrying your baby already... and there's something so thrilling about being completely bare with you now, even there. I can't help wanting it."],
            "shy":      ["I-I'm pregnant with your baby... and the thought of you bare in my ass, while I'm carrying you, makes me blush so hard. It's so naughty -- I want it."],
            "neutral":  ["I'm pregnant with your baby! As an experienced woman, taking your bare cock in my ass while I'm carrying your child is unbelievably hot. I want it!"],
            "direct":   ["I'm carrying your baby. I want your raw cock in my ass -- being this full of you, bare, is exactly what I crave."],
            "explicit": ["I'm pregnant with your baby! Bareback in my ass while I'm carrying your child -- god, it's the filthiest, hottest thing I can imagine. Take it."],
            "crude":    ["I'm already knocked up with your kid -- so shove your bare cock in my ass. Feeling you raw while I'm carrying you is so fucking hot."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... and the idea of you bare, even there, makes me tingle. It feels so naughty -- I think I want it."],
            "shy":      ["I-I'm pregnant with your baby, Professor! Oh my god, bareback anal while I'm carrying? That's so naughty... but it sounds so hot. Yes!"],
            "neutral":  ["I'm pregnant with your baby, Professor! Feeling your bare cock in my ass while I'm carrying your child -- that's so hot and taboo. I want it!"],
            "direct":   ["I'm carrying your baby, Professor. I want your bare cock in my ass -- nothing between us, it's so hot."],
            "explicit": ["I'm pregnant with your baby, Professor! Bareback in my ass while carrying you -- god, that's so filthy and hot. Do it!"],
            "crude":    ["I'm already knocked up, Professor -- so fuck my ass raw. Feeling you bare while I'm carrying you is so fucking hot!"],
        }},
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "other"}, "lines": {
            "demure":   ["I'm carrying your baby already... and being completely bare with you, even there, is so thrilling now. I can't help wanting it."],
            "shy":      ["I-I'm pregnant with your baby... and the thought of you bare in my ass makes me shiver. It's so naughty -- I want it."],
            "neutral":  ["I'm pregnant with your baby! Bareback anal while I'm carrying your child? That's so hot and taboo. I want it."],
            "direct":   ["I'm carrying your baby. I want your raw cock in my ass -- being this full of you, bare, is what I crave."],
            "explicit": ["I'm pregnant with your baby! Bareback in my ass while carrying your child -- it's the filthiest, hottest thing. Take it."],
            "crude":    ["I'm already knocked up -- so shove your bare cock in my ass. Feeling you raw while I'm carrying you is unreal."],
        }},

        # transactional
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "mother"}, "lines": {
            "demure":   ["I'm carrying your child now, so I'm fully invested in you. I want you bare in my ass too -- not as a charge, just because I crave you. Keep providing, and I'm yours however you like."],
            "shy":      ["I-I'm carrying your baby, so I'm committed to you now... I want you bare, even there. Not for a price -- I just want it. Take care of us, and I'm yours."],
            "neutral":  ["I'm carrying your child -- I'm fully invested in you now. As an experienced mother, I want you bare in my ass, nothing between us. Keep supporting me well, and you can have me however you like."],
            "direct":   ["I'm carrying your child, so I'm all in. I want you bare in my ass -- not part of any deal, I just crave you. Keep providing and I'm yours."],
            "explicit": ["I'm carrying your child -- fully yours now. I want your bare cock in my ass, nothing between us, because I crave you. Keep me well kept and take me however you want."],
            "crude":    ["I'm knocked up with your kid, so I'm all yours -- I want your raw cock in my ass because I fucking want it, not for a price. Pay your way and use me however."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, so I'm all yours now... does bare even cost anything for that? I don't want it for a price -- I just want to feel you."],
            "shy":      ["I-I'm carrying your baby, so I'm yours now... I want you bare even there. Does that, um, cost extra? I don't really care -- I just want it."],
            "neutral":  ["I'm carrying your baby, so I'm all yours now... does bareback anal cost anything? Because I want it -- I just want to feel you, no barrier."],
            "direct":   ["I'm carrying your baby, so I'm yours. I want you bare in my ass -- forget the price, I just want to feel you."],
            "explicit": ["I'm carrying your baby, Professor, so I'm all yours -- I want your bare cock in my ass, no charge, I just crave feeling you."],
            "crude":    ["I'm knocked up, so I'm yours -- I want your raw cock in my ass, no price, I just fucking want it."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "other"}, "lines": {
            "demure":   ["I'm carrying your child, so I'm committed to you completely now. I want you bare even there -- not part of a deal, just because I crave you."],
            "shy":      ["I-I'm carrying your baby, so I'm all in now... I want you bare in my ass too. Not for a price -- I just want it."],
            "neutral":  ["I'm carrying your child, so I'm committed to you completely. I want bareback anal now -- not part of any deal, just because I crave you bare."],
            "direct":   ["I'm carrying your child, so I'm yours. I want you bare in my ass -- not a transaction, I just crave you."],
            "explicit": ["I'm carrying your child -- fully yours. I want your bare cock in my ass, no charge, because I crave feeling you with nothing between us."],
            "crude":    ["I'm knocked up with your kid, so I'm all yours -- I want your raw cock in my ass because I want it, not for a price."],
        }},

        # dominate
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "mother"}, "lines": {
            "demure":   ["I am carrying your child, Master. I want nothing between us now -- you may take my ass bare, as you wish."],
            "shy":      ["I-I'm carrying your baby, Master... I want nothing between your cock and me, even there. Take my ass bare, however you please."],
            "neutral":  ["I am carrying your child, Master. As an experienced mother, I want nothing between your cock and me now -- take my ass bare, as you wish."],
            "direct":   ["I'm carrying your child, Master. I want you bare in my ass now -- use me however you wish."],
            "explicit": ["I am carrying your child, Master. I want your bare cock in my ass, nothing between us -- take it as you please."],
            "crude":    ["I'm knocked up with your kid, Master -- so take my ass raw. Nothing between us, use me however you fucking want."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... I want to feel you bare, even there. Take my ass however you like."],
            "shy":      ["I-I'm carrying your baby, Professor... I want to feel you bare in me now. You can take my ass however you like."],
            "neutral":  ["I'm carrying your baby, Professor... I want to feel you bare in me now. Take my ass however you like."],
            "direct":   ["I'm carrying your baby, Professor. I want you bare in my ass -- use me however you want."],
            "explicit": ["I'm carrying your baby, Professor. I want your bare cock in my ass now -- take me however you like."],
            "crude":    ["I'm knocked up, Professor -- so take my ass raw. Use me however you want."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "other"}, "lines": {
            "demure":   ["I am carrying your child, Master. I want nothing in the way now -- use my ass bare, as you wish."],
            "shy":      ["I-I'm carrying your baby, Master... I want you bare, even there. Use my ass as you please."],
            "neutral":  ["I am carrying your child, Master. I want you bare now, nothing in the way -- use my ass as you wish."],
            "direct":   ["I'm carrying your child, Master. I want you bare in my ass -- use me as you wish."],
            "explicit": ["I am carrying your child, Master. I want your bare cock in my ass, nothing between us -- use me as you please."],
            "crude":    ["I'm knocked up with your kid, Master -- so use my ass raw, however you fucking want."],
        }},

        # fallback approach (unknown / other initial_reaction) -- no `approach` key, no role branch
        {"when": {"pregnancy": "by_player"}, "lines": {
            "demure":   ["I'm carrying your baby now... I don't want anything between us anymore. I'd love to feel you bare, even there."],
            "shy":      ["I-I'm carrying your baby now... I don't want anything between us. I want to feel you bare in my ass."],
            "neutral":  ["I'm carrying your baby now... I don't want anything between us anymore. I want to feel you bare in my ass."],
            "direct":   ["I'm carrying your baby now -- I don't want anything between us. I want you bare in my ass."],
            "explicit": ["I'm carrying your baby now -- nothing between us anymore. I want to feel your bare cock in my ass."],
            "crude":    ["I'm knocked up now -- so nothing between us. I want you raw in my ass."],
        }},

    ])

    # ---- standing preference, WANTS A CONDOM for anal (live `elif wants_anal_condom`, 2474-2505). --
    # Single line per branch in the source -> migrated as neutral-only (resolves for every register).
    # Gated pregnancy in {none, by_other} so it fires for by-other too but never ties the by_player set.
    vt_register_responses("anal_condom_pref", [

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["As an experienced mother, I need to be careful about my health. When you're in my ass, I need that protection - I can't risk getting sick while caring for my family."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "compassionate", "role": "student"}, "lines": {
            "neutral": ["I feel so connected to you, but I'm always careful about anal... when you're in my ass, I think I need that protection. I know it can be risky without it."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "compassionate", "role": "other"}, "lines": {
            "neutral": ["I feel so connected to you, but when you're in my ass, I need that rubber layer. It lets me relax and enjoy us without worry."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["The way you look at me is so hot... but as an experienced mother, I need to be careful. Watching you roll a condom over your hard cock before taking my ass shows you respect my health."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "sexualized", "role": "student"}, "lines": {
            "neutral": ["The way you look at me is so hot... but I'm kind of scared of anal without protection. Watching you put on a condom makes me feel safer... and actually kind of sexy!"],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "sexualized", "role": "other"}, "lines": {
            "neutral": ["The way you look at me is so hot... but watching you roll a condom over your hard cock before taking my ass can be its own kind of sexy."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "transactional", "role": "mother"}, "lines": {
            "neutral": ["What's in it for me? As an experienced mother with responsibilities, protected anal costs extra - I have to maintain my health for my family."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "transactional", "role": "student"}, "lines": {
            "neutral": ["What's in it for me? Protected anal... um, does that cost less than without? I'm not sure about the pricing for anal stuff..."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "transactional", "role": "other"}, "lines": {
            "neutral": ["What's in it for me? Protected anal costs extra... unless you make it worth my time."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["You're in charge, Master. As an experienced mother, if you want to wrap your cock before entering my ass, I'll accept it - I must protect my family."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "dominate", "role": "student"}, "lines": {
            "neutral": ["You're in charge, Professor. If you want to use a condom for anal... I'll do what you want."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "approach": "dominate", "role": "other"}, "lines": {
            "neutral": ["You're in charge, Master. If you want to wrap your cock before entering my ass, I'll accept it."],
        }},

        # fallback approach
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True}, "lines": {
            "neutral": ["I prefer using condoms for anal sex... it's safer that way."],
        }},

    ])

    # ---- standing preference, PREFERS BARE for anal (live `else`, 2507-2538). Same shape. ----------
    vt_register_responses("anal_condom_pref", [

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["I feel so connected to you. As an experienced mother, I want to feel your bare cock in my ass - it's a different kind of intimacy that I trust you with."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "compassionate", "role": "student"}, "lines": {
            "neutral": ["I feel so connected to you. I want to feel your bare cock in my ass... it feels more intimate without anything between us, you know?"],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "compassionate", "role": "other"}, "lines": {
            "neutral": ["I feel so connected to you. I want to feel your bare cock in my ass, nothing between us when we're intimate like that."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["The way you look at me is so hot. As an experienced woman, I want to feel your raw cock stretching my ass open - motherhood hasn't dulled my desires for that intensity."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "sexualized", "role": "student"}, "lines": {
            "neutral": ["The way you look at me is so hot! I want to feel your bare cock in my ass... nothing between us, that sounds so exciting!"],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "sexualized", "role": "other"}, "lines": {
            "neutral": ["The way you look at me is so hot. I want to feel your raw cock stretching my ass open, no barriers."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "transactional", "role": "mother"}, "lines": {
            "neutral": ["What's in it for me? Bareback anal from an experienced mother? That's premium pricing, Professor - I know exactly what I'm offering."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "transactional", "role": "student"}, "lines": {
            "neutral": ["What's in it for me? Bareback anal? Is that more expensive? I don't really know what to charge for that... what do you think is fair?"],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "transactional", "role": "other"}, "lines": {
            "neutral": ["What's in it for me? Bareback anal access? That's premium pricing, Professor."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["You're in charge, Master. As an experienced mother, if you want to fuck my bare ass with no condom, I won't stop you - my body knows how to handle this."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "dominate", "role": "student"}, "lines": {
            "neutral": ["You're in charge, Professor. If you want to fuck my ass without a condom... okay, I'll let you. Whatever you want."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "approach": "dominate", "role": "other"}, "lines": {
            "neutral": ["You're in charge, Master. If you want to fuck my bare ass with no condom, I won't stop you."],
        }},

        # fallback approach
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False}, "lines": {
            "neutral": ["I don't really like condoms for anal... I prefer it bare."],
        }},

    ])

    # =============================================================================================
    # ANAL VIRGIN OVERLAY  (design change, not migration -- signed off 2026-07-01)
    # First anal is its own reluctance beat: most girls find it "gross and weird at first", so the
    # register ladder carries distaste-warming-to-willingness (demure/shy = squeamish, needs
    # reassurance; direct/crude = reluctant-but-curious, "sounds gross, but..."). Fact: anal_virgin
    # (anal_sex_count<=0). These carry anal_virgin:True, so they out-specify their general sibling
    # by one condition and win for virgins; the general 39 stay the experienced path untouched.
    # Role note: a base-mother anal-virgin is experienced as a mother but NOT back there -- never
    # claim "experienced" at anal here. One virgin variant per approach/role/sub-block + fallbacks.
    # =============================================================================================

    # ---- by_player + anal virgin : carrying his child, reluctant-but-surrendering first-timer. -----
    vt_register_responses("anal_condom_pref", [

        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "compassionate", "role": "mother"}, "lines": {
            "demure":   ["I'm carrying your child... and I'd give you anything now, even that. I'll be honest, though -- it frightens me a little, and part of me thinks it must be improper. But for you, if you're gentle, I'd try."],
            "shy":      ["I-I'm carrying your baby... so I want to give you everything. But I've never done... that. It seems kind of dirty, and I'm nervous. You'd have to be so gentle with me."],
            "neutral":  ["I'm carrying your baby, and I want to be everything for you. I've never done anal, though -- honestly it always seemed strange to me. But if you want it, I'll try, for you."],
            "direct":   ["I'm carrying your child, so I'm yours completely. I've never done anal -- it always seemed a bit weird to me, I won't lie -- but I'll give you that too. Just take it slow."],
            "explicit": ["I'm pregnant with your baby, so I'll give you anything -- even my ass, though I've never done it. It seems kind of nasty, honestly, but I want to give you all of me. Be gentle, and it's yours."],
            "crude":    ["I'm knocked up with your kid, so you can have all of me -- even my ass. Never had a cock back there, and yeah, it sounds gross... but I'll take it for you. Just go easy at first."],
        }},
        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "compassionate", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... so I want to give you everything. But I've never done that, and it scares me a little. It seems improper. If you were gentle... I'd try, for you."],
            "shy":      ["I-I'm carrying your baby, Professor... I want to be all yours. But anal? I've never... isn't it kind of dirty? I'm really nervous. You'd have to be so careful with me."],
            "neutral":  ["I'm carrying your baby, Professor. I want to give you everything -- but I've never done anal, and honestly it seems weird to me. Still, for you, I'd be willing to try it slowly."],
            "direct":   ["I'm carrying your baby, Professor, so I'm all yours. I've never done anal though -- it seems a little weird, I'll admit -- but I'll try it for you. Just be patient with me."],
            "explicit": ["I'm pregnant with your baby, Professor! I want to give you all of me -- even back there, though I've never done it. It sounds kind of nasty, but that almost makes it exciting. Go slow and it's yours."],
            "crude":    ["I'm knocked up with your kid, Professor -- so you can have everything, even my ass. Never had it back there, and it sounds pretty gross... but I'll try it for you. Just ease into it, okay?"],
        }},
        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "compassionate", "role": "other"}, "lines": {
            "demure":   ["I'm carrying your child... I'd give you anything now, even that. It frightens me, though, and it seems somehow wrong. But if you're gentle, I'd try it for you."],
            "shy":      ["I-I'm carrying your baby... I want to give you everything. But I've never done that -- isn't it kind of dirty? I'm nervous. You'd have to be gentle with me."],
            "neutral":  ["I'm carrying your baby, and I want to be everything for you. I've never done anal, though, and it always seemed strange to me. But for you, I'd try, slowly."],
            "direct":   ["I'm carrying your child, so I'm yours completely. Never done anal -- it seemed weird to me, honestly -- but I'll give you that too. Just take it slow."],
            "explicit": ["I'm pregnant with your baby, so you can have anything -- even my ass, though I've never done it. It seems kind of nasty, but I want all of me to be yours. Be gentle, and it's yours."],
            "crude":    ["I'm knocked up, so you can have all of me -- even my ass. Never had a cock back there, and yeah, sounds gross... but I'll take it for you. Go easy at first."],
        }},

        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "sexualized", "role": "mother"}, "lines": {
            "demure":   ["I'm carrying your baby already... and being this bold feels new. I've never done that -- it seems so wicked, almost dirty -- but the thought of it, now that I'm yours, makes me flush. Maybe... maybe I'd try."],
            "shy":      ["I-I'm pregnant with your baby... and I've never done anal. It seems so naughty and gross... but the way that makes me feel is confusing. M-maybe, if you're gentle, I'd want to try it."],
            "neutral":  ["I'm pregnant with your baby! I've never done anal -- honestly it always seemed dirty to me. But being this deep in you has me curious... the taboo of it is kind of thrilling. I might want to try."],
            "direct":   ["I'm carrying your baby. I've never done anal -- it always seemed nasty to me -- but I won't lie, the filthiness of it is getting me a little hot now. I think I want you to be my first."],
            "explicit": ["I'm pregnant with your baby! I've never had it in my ass -- it seemed so dirty -- but god, imagining you being the one to take it there, while I'm carrying you, is filthier and hotter than I expected. Take my first."],
            "crude":    ["I'm knocked up with your kid -- and I've never had a cock in my ass. Sounds nasty as hell... but fuck, thinking about you being the one to ruin it makes me wet. Be my first, just ease it in."],
        }},
        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "sexualized", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... and I've never done that. It seems so wicked -- but somehow that makes me tingle. Maybe I'd let you be the one, if you were gentle."],
            "shy":      ["I-I'm pregnant with your baby, Professor! I've never done anal... it seems really dirty and weird. But the naughtiness of it kind of excites me? M-maybe you could be my first..."],
            "neutral":  ["I'm pregnant with your baby, Professor! I've never done anal -- it always seemed gross to me. But the taboo of it is weirdly exciting now that I'm yours. I think I'd want to try it with you."],
            "direct":   ["I'm carrying your baby, Professor. Never done anal -- it seemed nasty to me -- but honestly the filth of it is turning me on a little. I want you to be my first back there."],
            "explicit": ["I'm pregnant with your baby, Professor! I've never had it in my ass -- it seemed so filthy -- but imagining you taking my anal virginity while I'm carrying you is so nasty and hot. Do it, be my first!"],
            "crude":    ["I'm knocked up, Professor -- and I've never had a cock in my ass. Sounds gross... but fuck it, the dirtiness has me dripping. Take my ass-virginity, just go slow at first!"],
        }},
        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "sexualized", "role": "other"}, "lines": {
            "demure":   ["I'm carrying your baby already... and I've never done that. It seems so wicked -- but now that I'm yours, the thought of it makes me flush. Maybe I'd try, for the thrill."],
            "shy":      ["I-I'm pregnant with your baby... and I've never done anal. It seems dirty and strange... but the naughtiness confuses me in a good way. M-maybe I'd let you be my first."],
            "neutral":  ["I'm pregnant with your baby! I've never done anal -- it always seemed dirty. But the taboo is thrilling now that I'm yours; I'm curious to try it with you."],
            "direct":   ["I'm carrying your baby. Never done anal -- seemed nasty to me -- but the filthiness of it is getting me hot. I want you to be my first there."],
            "explicit": ["I'm pregnant with your baby! Never had it in my ass -- it seemed so dirty -- but imagining you taking it there while I carry you is filthier and hotter than I thought. Take my first."],
            "crude":    ["I'm knocked up -- and I've never had a cock in my ass. Sounds nasty... but fuck, it's got me wet. Be the one to ruin my ass, just ease it in."],
        }},

        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "transactional", "role": "mother"}, "lines": {
            "demure":   ["I'm carrying your child now, so I'm devoted to you. But my ass? I've never done that -- it seems improper, and it would be a first for me. If you want it, that's a special arrangement... though for you, perhaps I'd give it freely."],
            "shy":      ["I-I'm carrying your baby, so I'm yours... but I've never done anal. It seems kind of dirty, and it's my first -- so that's, um, worth extra, isn't it? Th-though for you I might not charge."],
            "neutral":  ["I'm carrying your child, so I'm committed to you. But I've never done anal -- honestly it seemed gross to me. A first like that is premium... though since it's you, maybe I'd just give it."],
            "direct":   ["I'm carrying your child, so I'm all in. Never done anal though -- seemed weird to me -- and a first back there is worth a premium. But for you? Keep providing and it's yours."],
            "explicit": ["I'm pregnant with your child, so I'm yours -- but I've never had it in my ass. It seemed nasty, and my anal virginity is premium... though for the father of my baby, I might hand it over for nothing but you taking care of us."],
            "crude":    ["I'm knocked up with your kid, so I'm yours -- but I've never had a cock in my ass. Sounds gross, and a first like that costs. Still... for you? Pay your way and you can pop my ass-cherry."],
        }},
        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "transactional", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, Professor, so I'm yours... but I've never done that. It seems improper, and it's my first -- would that cost more? I don't really know how to price something I've never given."],
            "shy":      ["I-I'm carrying your baby, Professor... but I've never done anal. It seems dirty, and it'd be my first, so... is that extra? I'm not sure what a first is worth."],
            "neutral":  ["I'm carrying your baby, Professor, so I'm all yours -- but I've never done anal. It seemed gross to me. My first back there... does that cost more? I honestly don't know the rate for a first."],
            "direct":   ["I'm carrying your baby, Professor, so I'm yours. Never done anal though -- seemed weird -- and it'd be my first. That's got to be worth something extra, right? I don't know how to price it."],
            "explicit": ["I'm pregnant with your baby, Professor -- I'm yours, but I've never had it in my ass. It seemed nasty, and taking my anal virginity is a premium thing... isn't it? I've never sold a first before."],
            "crude":    ["I'm knocked up, Professor -- I'm yours, but nobody's ever had my ass. Sounds gross... but a virgin ass has to be worth a premium, yeah? I dunno what to charge for popping that cherry."],
        }},
        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "transactional", "role": "other"}, "lines": {
            "demure":   ["I'm carrying your child, so I'm devoted -- but I've never done that. It seems improper, and a first would be a special arrangement. Though for you, perhaps I'd simply give it."],
            "shy":      ["I-I'm carrying your baby, so I'm yours... but I've never done anal. It seems dirty, and it's my first, so that's worth extra... isn't it? Th-though maybe not, for you."],
            "neutral":  ["I'm carrying your child, so I'm committed. But I've never done anal -- it seemed gross. A first like that is premium... though since it's you, maybe I'd just give it."],
            "direct":   ["I'm carrying your child, so I'm all in. Never done anal -- seemed weird -- and a first back there is a premium. For you, though? Keep me kept and it's yours."],
            "explicit": ["I'm pregnant with your child, so I'm yours -- but I've never had it in my ass. It seemed nasty, and my anal virginity is premium... though for you I might hand it over for nothing but being provided for."],
            "crude":    ["I'm knocked up, so I'm yours -- but nobody's had my ass. Sounds gross, and a virgin ass costs. Still, for you? Pay your way and you can pop that cherry."],
        }},

        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "dominate", "role": "mother"}, "lines": {
            "demure":   ["I am carrying your child, Master. I've never done that -- it frightens me, and it seems improper -- but I am yours. If you command it, I will yield my ass to you, though I beg you to be gentle with my first."],
            "shy":      ["I-I'm carrying your baby, Master... I've never done anal. It seems dirty, and I'm frightened. But if you wish it... I'll obey. Please be gentle -- it's my first."],
            "neutral":  ["I am carrying your child, Master. I've never done anal -- it always seemed strange and frightening to me -- but I submit to you. If you will it, my ass is yours, though I ask for patience my first time."],
            "direct":   ["I'm carrying your child, Master. Never done anal -- it scares me, seemed wrong -- but I'm yours. If you command it, take my ass. Just go slow, it's my first."],
            "explicit": ["I am carrying your child, Master. I've never had it in my ass -- it seemed nasty and it frightens me -- but I belong to you. If you wish to take my anal virginity, it is yours to take. Be firm but patient."],
            "crude":    ["I'm knocked up with your kid, Master -- and nobody's had my ass. It scares me, sounds gross... but I'm yours. If you want to pop my ass-cherry, do it. Just ease in the first time."],
        }},
        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "dominate", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... I've never done that. It frightens me and seems improper -- but I'm yours. If you wish it, I'll give you my ass, though please be gentle my first time."],
            "shy":      ["I-I'm carrying your baby, Professor... I've never done anal. It seems dirty and scary. But if you want it... I'll do it. Please be gentle -- it's my first."],
            "neutral":  ["I'm carrying your baby, Professor. I've never done anal -- it seemed strange and frightening -- but I'll do what you want. If you wish it, my ass is yours, just be patient my first time."],
            "direct":   ["I'm carrying your baby, Professor. Never done anal -- it scares me a bit -- but I'll do what you say. If you want my ass, take it. Just go slow, it's my first."],
            "explicit": ["I'm carrying your baby, Professor. I've never had it in my ass -- it frightened me -- but I'm yours. If you want to take my anal virginity, do it. Just be patient with my first."],
            "crude":    ["I'm knocked up, Professor -- nobody's had my ass. It scares me, sounds gross... but I'll do what you want. Wanna pop my ass-cherry? Do it, just ease in the first time."],
        }},
        {"when": {"pregnancy": "by_player", "anal_virgin": True, "approach": "dominate", "role": "other"}, "lines": {
            "demure":   ["I am carrying your child, Master. I've never done that -- it frightens me and seems wrong -- but I am yours. If you command it, my ass is yours, though I beg gentleness my first time."],
            "shy":      ["I-I'm carrying your baby, Master... I've never done anal. It seems dirty and scary. But if you wish it, I'll obey. Please be gentle -- it's my first."],
            "neutral":  ["I am carrying your child, Master. I've never done anal -- it seemed strange and frightening -- but I submit. If you will it, take my ass, just be patient my first time."],
            "direct":   ["I'm carrying your child, Master. Never done anal -- it scares me -- but I'm yours. If you command it, take my ass. Go slow, it's my first."],
            "explicit": ["I am carrying your child, Master. I've never had it in my ass -- it frightened me -- but I belong to you. If you wish to take my anal virginity, it's yours. Be firm but patient."],
            "crude":    ["I'm knocked up, Master -- nobody's had my ass. Scares me, sounds gross... but I'm yours. Want to pop my ass-cherry? Do it, ease in the first time."],
        }},

        # fallback approach
        {"when": {"pregnancy": "by_player", "anal_virgin": True}, "lines": {
            "demure":   ["I'm carrying your baby now... I'd give you anything, even that. But I've never done it, and it frightens me a little. If you're gentle, I'd try."],
            "shy":      ["I-I'm carrying your baby now... I want to give you everything. But I've never done anal -- isn't it kind of dirty? I'm nervous, but... I'd try for you."],
            "neutral":  ["I'm carrying your baby now... I want to give you all of me. I've never done anal, though, and it always seemed strange. But for you, I'd try it slowly."],
            "direct":   ["I'm carrying your baby now -- I'm yours. Never done anal, and it seemed weird to me, but I'll give you that too. Just take it slow."],
            "explicit": ["I'm carrying your baby now -- I'll give you anything, even my ass, though I've never done it. It seems kind of nasty, but I want all of me to be yours. Be gentle."],
            "crude":    ["I'm knocked up now -- so you can have all of me, even my ass. Never had it back there, sounds gross... but I'll take it for you. Go easy at first."],
        }},

    ])

    # ---- standing pref WANTS A CONDOM + anal virgin : the condom is a safety blanket for the first. -
    vt_register_responses("anal_condom_pref", [

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "compassionate", "role": "mother"}, "lines": {
            "demure":   ["I've never done... that. Honestly it seems improper, and the idea makes me nervous. If we ever did, I'd need a condom -- and you to be very gentle. I've children to think of, too."],
            "shy":      ["I-I've never done anal... it seems kind of dirty, and I'm scared of it. If we ever tried, I'd really need a condom. And you'd have to be so gentle with me."],
            "neutral":  ["I've never done anal -- honestly it always seemed strange and a little gross to me. If we ever tried, I'd need a condom, and I'd need you to go slow. I have my family to be careful for, too."],
            "direct":   ["I've never done anal, and I'll be honest -- it seems weird to me. If we ever do, it's with a condom, and slowly. I've got a child to stay healthy for."],
            "explicit": ["I've never had it in my ass -- it seems kind of nasty, to be blunt. If you ever want to, wrap it and be gentle -- a first like that scares me, and I've a family to protect."],
            "crude":    ["Never had a cock in my ass -- and yeah, it sounds gross. If you ever want to try, keep it wrapped and go slow. It's my first back there and I've got kids to keep safe."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "compassionate", "role": "student"}, "lines": {
            "demure":   ["I've never done that, Professor... it seems improper, and it frightens me a little. If we ever did, I'd need a condom, and you to be gentle. Please."],
            "shy":      ["I-I've never done anal... isn't it kind of dirty? It scares me. If we ever tried, I'd really need a condom, Professor. And you'd have to be careful."],
            "neutral":  ["I've never done anal, Professor -- it always seemed strange to me, honestly. If we ever tried, I'd need a condom, and I'd need you to go slow with me."],
            "direct":   ["I've never done anal, Professor -- it seems weird to me, I'll admit. If we ever do, it's with a condom, and slowly. It's my first."],
            "explicit": ["I've never had it in my ass, Professor -- it seems kind of nasty. If you ever want to, wrap it and be gentle -- a first like that really scares me."],
            "crude":    ["Never had a cock in my ass, Professor -- sounds gross. If you ever want to try, keep it wrapped and ease in. It'd be my first."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "compassionate", "role": "other"}, "lines": {
            "demure":   ["I've never done that... it seems improper, and it makes me nervous. If we ever did, I'd need a condom -- and you to be very gentle with me."],
            "shy":      ["I-I've never done anal... it seems dirty, and I'm scared. If we ever tried, I'd need a condom. And you'd have to be so gentle."],
            "neutral":  ["I've never done anal -- it always seemed strange and a bit gross to me. If we ever tried, I'd need a condom, and you to go slow."],
            "direct":   ["I've never done anal, and honestly it seems weird to me. If we ever do, it's with a condom, and slowly."],
            "explicit": ["I've never had it in my ass -- it seems kind of nasty. If you ever want to, wrap it and be gentle -- a first like that scares me."],
            "crude":    ["Never had a cock in my ass -- sounds gross. If you ever want to try, keep it wrapped and go slow. It'd be my first."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "sexualized", "role": "mother"}, "lines": {
            "demure":   ["I've never done that... it seems so wicked. The thought makes me nervous and a little flushed at once. If we tried, I'd want a condom -- and you gentle."],
            "shy":      ["I-I've never done anal... it seems dirty, but the naughtiness kind of gets to me. If we tried, though, I'd need a condom -- and you to be gentle with my first."],
            "neutral":  ["I've never done anal -- it always seemed nasty to me, though I'll admit the taboo is a little exciting. If we tried, I'd want a condom, and you to go slow. It'd be my first."],
            "direct":   ["I've never done anal -- seemed filthy to me, but the idea's got a certain heat. If we do, wrap it and take it slow. It's my first back there."],
            "explicit": ["I've never had it in my ass -- it seemed so dirty, though picturing it is hotter than I'd admit. If you take my anal virginity, do it wrapped and gentle. The nerves are half the thrill."],
            "crude":    ["Never had a cock in my ass -- sounds nasty, but fuck, thinking about it does something to me. If you pop that cherry, keep it wrapped and ease in. First time back there."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "sexualized", "role": "student"}, "lines": {
            "demure":   ["I've never done that, Professor... it seems so wicked. It makes me nervous, but also a bit warm. If we tried, I'd want a condom, and you gentle."],
            "shy":      ["I-I've never done anal, Professor... it seems dirty, but somehow that excites me? If we tried, I'd need a condom, and you to be gentle with my first."],
            "neutral":  ["I've never done anal, Professor -- it seemed nasty to me, though the taboo is kind of thrilling. If we tried, I'd want a condom and you to go slow. It'd be my first."],
            "direct":   ["I've never done anal, Professor -- seemed filthy, but the idea's got a heat to it. If we do, wrap it and take it slow. It's my first."],
            "explicit": ["I've never had it in my ass, Professor -- it seemed so dirty, but picturing you taking my anal virginity is nasty-hot. Do it wrapped and gentle -- the nerves are part of it."],
            "crude":    ["Never had a cock in my ass, Professor -- sounds gross, but fuck, it gets me going. If you pop that cherry, keep it wrapped and ease in. First time."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "sexualized", "role": "other"}, "lines": {
            "demure":   ["I've never done that... it seems so wicked, and the thought leaves me nervous and flushed at once. If we tried, I'd want a condom -- and you gentle."],
            "shy":      ["I-I've never done anal... it seems dirty, but the naughtiness gets to me. If we tried, I'd need a condom, and you to be gentle with my first."],
            "neutral":  ["I've never done anal -- it seemed nasty to me, though the taboo is a little exciting. If we tried, I'd want a condom and you to go slow. It'd be my first."],
            "direct":   ["I've never done anal -- seemed filthy, but the idea's got a heat. If we do, wrap it and take it slow. It's my first back there."],
            "explicit": ["I've never had it in my ass -- it seemed so dirty, though picturing it is hotter than I'd admit. If you take my anal virginity, wrapped and gentle. The nerves are half the thrill."],
            "crude":    ["Never had a cock in my ass -- sounds nasty, but it does something to me. If you pop that cherry, keep it wrapped and ease in. First time back there."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "transactional", "role": "mother"}, "lines": {
            "demure":   ["I've never done that -- it seems improper, and it would be my first. If you want it, that's a premium, and I'd insist on a condom. I've a family's health to guard."],
            "shy":      ["I-I've never done anal... it seems dirty, and it'd be my first, so that's extra. And I'd need a condom -- I have my family to think of."],
            "neutral":  ["I've never done anal -- it seemed gross to me. A first like that costs extra, and I'd require a condom. My health matters to my family."],
            "direct":   ["Never done anal -- seemed weird to me -- and a first is a premium. Wrapped only. I've got a family's health to protect."],
            "explicit": ["I've never had it in my ass -- it seemed nasty, and my anal virginity is a premium. You want it? Wrapped, and you pay for the first. I've a family to stay healthy for."],
            "crude":    ["Nobody's had my ass -- sounds gross, and a virgin ass costs. You want to pop it? Wrapped only, and it's premium. I've got kids to stay clean for."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "transactional", "role": "student"}, "lines": {
            "demure":   ["I've never done that -- it seems improper, and it'd be my first. Would that cost more? And I'd want a condom. I'm not sure how to price something I've never given."],
            "shy":      ["I-I've never done anal... it seems dirty, and it's my first, so... is that extra? And with a condom. I don't know what a first is worth, Professor."],
            "neutral":  ["I've never done anal -- it seemed gross to me. My first back there... does that cost more? And I'd want a condom. I honestly don't know the rate for a first."],
            "direct":   ["Never done anal -- seemed weird -- and it'd be my first. That's worth extra, right, Professor? Wrapped, though. I don't know how to price a first."],
            "explicit": ["I've never had it in my ass -- it seemed nasty, and taking my anal virginity is a premium... isn't it? Wrapped only. I've never sold a first, so name a fair price."],
            "crude":    ["Nobody's had my ass, Professor -- sounds gross, but a virgin ass has to be worth a premium, right? Wrapped only. I dunno what to charge to pop that cherry."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "transactional", "role": "other"}, "lines": {
            "demure":   ["I've never done that -- it seems improper, and a first would be a premium. And I'd insist on a condom, naturally."],
            "shy":      ["I-I've never done anal... it seems dirty, and it's my first, so that's extra. With a condom, of course."],
            "neutral":  ["I've never done anal -- it seemed gross to me. A first like that costs extra, and I'd require a condom."],
            "direct":   ["Never done anal -- seemed weird -- and a first is a premium. Wrapped only."],
            "explicit": ["I've never had it in my ass -- it seemed nasty, and my anal virginity is a premium. Wrapped, and you pay for the first."],
            "crude":    ["Nobody's had my ass -- sounds gross, and a virgin ass costs. Wrapped only, and it's premium."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "dominate", "role": "mother"}, "lines": {
            "demure":   ["I've never done that, Master -- it frightens me and seems improper. But if you command it, I'll yield. Use a condom, I beg you, and be gentle with my first. I've a family to keep well."],
            "shy":      ["I-I've never done anal, Master... it seems dirty and it scares me. But if you wish it, I'll obey -- with a condom, please, and gently. It's my first."],
            "neutral":  ["I've never done anal, Master -- it seemed strange and frightening. But if you will it, I submit -- with a condom, and patience my first time. I must stay healthy for my family."],
            "direct":   ["Never done anal, Master -- it scares me -- but if you command it, I'll take it. Wrapped, and slow. It's my first, and I've a family to protect."],
            "explicit": ["I've never had it in my ass, Master -- it frightened me -- but I'm yours to command. Take my anal virginity if you wish, but wrapped, and be patient. I've a family to stay healthy for."],
            "crude":    ["Nobody's had my ass, Master -- it scares me, sounds gross -- but I'm yours. Want to pop it? Do it wrapped and ease in. It's my first, and I've got kids to keep clean for."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "dominate", "role": "student"}, "lines": {
            "demure":   ["I've never done that, Professor... it frightens me and seems improper. But if you wish it, I'll yield -- with a condom, please, and gently. It's my first."],
            "shy":      ["I-I've never done anal, Professor... it seems dirty and scary. But if you want it, I'll obey -- with a condom, and gently. Please, it's my first."],
            "neutral":  ["I've never done anal, Professor -- it seemed strange and frightening. But if you will it, I'll do it -- with a condom, and patience my first time."],
            "direct":   ["Never done anal, Professor -- it scares me -- but if you command it, I'll take it. Wrapped, and slow. It's my first."],
            "explicit": ["I've never had it in my ass, Professor -- it frightened me -- but I'm yours. Take my anal virginity if you wish, wrapped, and be patient with my first."],
            "crude":    ["Nobody's had my ass, Professor -- scares me, sounds gross -- but I'm yours. Want to pop it? Wrapped, and ease in. My first."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True, "approach": "dominate", "role": "other"}, "lines": {
            "demure":   ["I've never done that, Master -- it frightens me and seems wrong. But if you command it, I'll yield -- with a condom, and gently. It's my first."],
            "shy":      ["I-I've never done anal, Master... it seems dirty and it scares me. But if you wish it, I'll obey -- with a condom, please. It's my first."],
            "neutral":  ["I've never done anal, Master -- it seemed strange and frightening. But if you will it, I submit -- with a condom, and patience my first time."],
            "direct":   ["Never done anal, Master -- it scares me -- but if you command it, I'll take it. Wrapped, and slow. My first."],
            "explicit": ["I've never had it in my ass, Master -- it frightened me -- but I'm yours to command. Wrapped, and be patient with my first."],
            "crude":    ["Nobody's had my ass, Master -- scares me, sounds gross -- but I'm yours. Want to pop it? Wrapped, ease in. My first."],
        }},

        # fallback approach
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": True, "anal_virgin": True}, "lines": {
            "demure":   ["I've never done that... it seems improper, and it makes me nervous. If we ever did, I'd want a condom -- and you gentle."],
            "shy":      ["I-I've never done anal... it seems kind of dirty, and it scares me. If we ever tried, I'd really want a condom."],
            "neutral":  ["I've never done anal -- it always seemed strange to me. If we ever tried, I'd want a condom, and to go slow."],
            "direct":   ["I've never done anal -- seemed weird to me. If we ever do, it's with a condom, and slowly. It's my first."],
            "explicit": ["I've never had it in my ass -- it seemed kind of nasty. If you ever want to, wrap it and be gentle. A first like that scares me."],
            "crude":    ["Never had a cock in my ass -- sounds gross. If you ever try, keep it wrapped and ease in. It'd be my first."],
        }},

    ])

    # ---- standing pref PREFERS BARE + anal virgin : reluctant/never-done-it, but would give it bare. -
    vt_register_responses("anal_condom_pref", [

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "compassionate", "role": "mother"}, "lines": {
            "demure":   ["I've never done that... it seems improper, and I'd be nervous. But if I gave you that part of me, I wouldn't want anything between us -- it should be skin to skin. Just be gentle with my first."],
            "shy":      ["I-I've never done anal... it seems kind of dirty, and I'm scared. But if I let you, I-I wouldn't want a condom -- I'd want to feel it's really you. Please be gentle."],
            "neutral":  ["I've never done anal -- honestly it always seemed strange to me. But if I gave you that, I wouldn't want a barrier; it'd feel more like trust that way. Just go slow with my first."],
            "direct":   ["I've never done anal, and it seemed weird to me, I'll admit. But if I let you have it, I'd want it bare -- no barrier, just you. Take my first slow."],
            "explicit": ["I've never had it in my ass -- it seemed kind of nasty, honestly. But if I give you that, I'd want you bare -- skin to skin, feeling it's really you taking my first. Be gentle."],
            "crude":    ["Never had a cock in my ass -- sounds gross, not gonna lie. But if I let you pop it, I want it bare, no rubber -- I want to feel it's really you. Just ease into my first."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "compassionate", "role": "student"}, "lines": {
            "demure":   ["I've never done that, Professor... it seems improper, and it scares me a little. But if I gave you that, I wouldn't want anything between us. Just be gentle with my first."],
            "shy":      ["I-I've never done anal... isn't it kind of dirty? It scares me. But if I let you, I-I wouldn't want a condom, Professor -- I'd want to feel it's you. Please be gentle."],
            "neutral":  ["I've never done anal, Professor -- it seemed strange to me. But if I gave you that, I wouldn't want a barrier; it'd feel more real that way. Go slow with my first."],
            "direct":   ["I've never done anal, Professor -- seemed weird, I'll admit. But if I let you have it, I'd want it bare, just you. Take my first slow."],
            "explicit": ["I've never had it in my ass, Professor -- it seemed nasty. But if I give you that, I'd want you bare -- feeling it's really you taking my first. Be gentle."],
            "crude":    ["Never had a cock in my ass, Professor -- sounds gross. But if I let you pop it, I want it bare, no rubber -- feel it's really you. Ease into my first."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "compassionate", "role": "other"}, "lines": {
            "demure":   ["I've never done that... it seems improper, and I'd be nervous. But if I gave you that part of me, I wouldn't want anything between us. Be gentle with my first."],
            "shy":      ["I-I've never done anal... it seems dirty, and I'm scared. But if I let you, I-I wouldn't want a condom -- I'd want to feel it's you. Please be gentle."],
            "neutral":  ["I've never done anal -- it always seemed strange. But if I gave you that, I wouldn't want a barrier; it'd feel more like trust. Go slow with my first."],
            "direct":   ["I've never done anal, and it seemed weird to me. But if I let you have it, I'd want it bare -- no barrier, just you. My first slow."],
            "explicit": ["I've never had it in my ass -- it seemed nasty. But if I give you that, I'd want you bare -- skin to skin, my first. Be gentle."],
            "crude":    ["Never had a cock in my ass -- sounds gross. But if I let you pop it, I want it bare, no rubber -- feel it's really you. Ease into my first."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "sexualized", "role": "mother"}, "lines": {
            "demure":   ["I've never done that... it seems so wicked. But if I let you, I wouldn't want a barrier -- if I'm going to be that bold, I want to feel all of it. Just be gentle with my first."],
            "shy":      ["I-I've never done anal... it seems dirty, but the naughtiness gets to me. If I let you take it, I-I'd want it bare -- I'd want to feel everything. Gently, though, it's my first."],
            "neutral":  ["I've never done anal -- it seemed nasty to me, but the taboo's exciting. If I give you my first, I'd want it bare -- no barrier, I want to feel all of it. Just go slow."],
            "direct":   ["I've never done anal -- seemed filthy, but the idea's hot. If you take my first, take it bare -- I want to feel every bit of it. Slow, at least to start."],
            "explicit": ["I've never had it in my ass -- it seemed so dirty, but that's half the thrill. If you take my anal virginity, take it raw -- I want to feel your bare cock claim my first. Be gentle at first."],
            "crude":    ["Never had a cock in my ass -- sounds nasty, but fuck it turns me on. Pop my ass-cherry bare -- no rubber, I want to feel it. Just ease that bare cock in for my first."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "sexualized", "role": "student"}, "lines": {
            "demure":   ["I've never done that, Professor... it seems so wicked. But if I let you, I wouldn't want a barrier -- if I'm being this bold, I want to feel it all. Gently, my first."],
            "shy":      ["I-I've never done anal, Professor... it seems dirty, but it excites me somehow. If I let you take it, I-I'd want it bare. Gently though -- it's my first."],
            "neutral":  ["I've never done anal, Professor -- it seemed nasty, but the taboo's exciting. If I give you my first, I'd want it bare -- I want to feel all of it. Go slow."],
            "direct":   ["I've never done anal, Professor -- seemed filthy, but it's hot. If you take my first, bare -- I want to feel every bit. Slow to start."],
            "explicit": ["I've never had it in my ass, Professor -- it seemed so dirty, but that's the thrill. Take my anal virginity raw -- I want your bare cock to claim my first. Gentle at first."],
            "crude":    ["Never had a cock in my ass, Professor -- sounds nasty, but fuck it's hot. Pop my ass-cherry bare -- no rubber. Just ease that bare cock in for my first."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "sexualized", "role": "other"}, "lines": {
            "demure":   ["I've never done that... it seems so wicked. But if I let you, I wouldn't want a barrier -- if I'm being bold, I want to feel it all. Gently, my first."],
            "shy":      ["I-I've never done anal... it seems dirty, but the naughtiness gets to me. If I let you, I-I'd want it bare. Gently -- it's my first."],
            "neutral":  ["I've never done anal -- it seemed nasty, but the taboo's exciting. If I give you my first, I'd want it bare -- feel all of it. Go slow."],
            "direct":   ["I've never done anal -- seemed filthy, but it's hot. If you take my first, bare -- I want to feel every bit. Slow to start."],
            "explicit": ["I've never had it in my ass -- it seemed so dirty, but that's the thrill. Take my anal virginity raw -- bare cock to claim my first. Gentle at first."],
            "crude":    ["Never had a cock in my ass -- sounds nasty, but it's hot. Pop my ass-cherry bare -- no rubber. Ease that bare cock in for my first."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "transactional", "role": "mother"}, "lines": {
            "demure":   ["I've never done that -- it seems improper, and it'd be my first. If you want it bare, that's the highest premium... though I'd want to feel it truly, with nothing between us."],
            "shy":      ["I-I've never done anal... it seems dirty, and it's my first. Bare would be extra-special -- and honestly, if I do it, I-I'd rather feel it, no condom."],
            "neutral":  ["I've never done anal -- it seemed gross to me. A first, and bare? That's premium on premium. But if I'm giving my first, I'd want to actually feel it -- no barrier."],
            "direct":   ["Never done anal -- seemed weird -- and a bare first is top dollar. But I'll admit, if I give it up, I'd want it raw, no rubber. Worth every cent."],
            "explicit": ["I've never had it in my ass -- my anal virginity is premium, and bare is the ultimate. If you pay for it, take it raw -- I want to feel your bare cock take my first."],
            "crude":    ["Nobody's had my ass -- a virgin ass raw is top price. But if you're paying, take it bare -- I wanna feel that first with no rubber. Costs, but it's worth it."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "transactional", "role": "student"}, "lines": {
            "demure":   ["I've never done that -- it's my first, and bare would be... more, wouldn't it? I don't know how to price it. But if I gave it, I think I'd want to feel it, no condom."],
            "shy":      ["I-I've never done anal... it's my first, and bare is extra, right? I'm not sure. But if I do it, I-I'd kind of want it raw, to feel it."],
            "neutral":  ["I've never done anal -- my first, and bare on top of that? I don't know the rate. But honestly, if I give my first, I'd want to feel it -- no barrier."],
            "direct":   ["Never done anal -- it's my first, and a bare first has to be a premium, right, Professor? I don't know how to price it. But I'd want it raw if I do it."],
            "explicit": ["I've never had it in my ass -- taking my anal virginity bare is the ultimate premium... isn't it? I've never sold a first. But if you take it, I'd want it raw."],
            "crude":    ["Nobody's had my ass, Professor -- a virgin ass bare has to be top price, right? Dunno what to charge. But if you pop it, I want it raw."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "transactional", "role": "other"}, "lines": {
            "demure":   ["I've never done that -- it'd be my first, and bare would be the highest premium. Though I'd want to feel it, truly, with nothing between us."],
            "shy":      ["I-I've never done anal... it's my first, and bare is extra-special. If I do it, I-I'd rather feel it, no condom."],
            "neutral":  ["I've never done anal -- a first, and bare? Premium on premium. But if I give my first, I'd want to actually feel it -- no barrier."],
            "direct":   ["Never done anal -- a bare first is top dollar. But if I give it up, I'd want it raw, no rubber."],
            "explicit": ["I've never had it in my ass -- my anal virginity is premium, bare is the ultimate. Pay for it and take it raw -- I want to feel your bare cock take my first."],
            "crude":    ["Nobody's had my ass -- a virgin ass raw is top price. If you're paying, take it bare -- I wanna feel that first with no rubber."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "dominate", "role": "mother"}, "lines": {
            "demure":   ["I've never done that, Master -- it frightens me and seems improper. But if you command it, take it bare; I would keep nothing between us. Be gentle with my first, I beg you."],
            "shy":      ["I-I've never done anal, Master... it scares me, it seems dirty. But if you wish it, take it bare -- I-I wouldn't want a barrier from you. Please, gently, my first."],
            "neutral":  ["I've never done anal, Master -- it seemed strange and frightening. But if you will it, take it bare; I keep nothing between us. Only be patient with my first."],
            "direct":   ["Never done anal, Master -- it scares me -- but if you command it, take it raw. Nothing between us. Just go slow, it's my first."],
            "explicit": ["I've never had it in my ass, Master -- it frightened me -- but I'm yours. Take my anal virginity bare if you wish; I'd keep no barrier from you. Be firm but patient with my first."],
            "crude":    ["Nobody's had my ass, Master -- it scares me, sounds gross -- but I'm yours. Want it? Take it bare, no rubber. Just ease that raw cock into my first."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "dominate", "role": "student"}, "lines": {
            "demure":   ["I've never done that, Professor... it frightens me. But if you wish it, take it bare -- I'd keep nothing between us. Gently, my first, please."],
            "shy":      ["I-I've never done anal, Professor... it scares me, it seems dirty. But if you want it, take it bare -- I-I wouldn't want a barrier from you. Gently, my first."],
            "neutral":  ["I've never done anal, Professor -- it seemed frightening. But if you will it, take it bare; I keep nothing between us. Be patient with my first."],
            "direct":   ["Never done anal, Professor -- it scares me -- but if you command it, take it raw. Nothing between us. Go slow, my first."],
            "explicit": ["I've never had it in my ass, Professor -- it frightened me -- but I'm yours. Take my anal virginity bare if you wish; no barrier from you. Be patient with my first."],
            "crude":    ["Nobody's had my ass, Professor -- scares me, sounds gross -- but I'm yours. Want it? Bare, no rubber. Ease that raw cock into my first."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True, "approach": "dominate", "role": "other"}, "lines": {
            "demure":   ["I've never done that, Master -- it frightens me and seems wrong. But if you command it, take it bare; nothing between us. Gently with my first, I beg."],
            "shy":      ["I-I've never done anal, Master... it scares me. But if you wish it, take it bare -- I-I wouldn't want a barrier from you. Gently, my first."],
            "neutral":  ["I've never done anal, Master -- it seemed frightening. But if you will it, take it bare; I keep nothing between us. Patience with my first."],
            "direct":   ["Never done anal, Master -- it scares me -- but if you command it, take it raw. Nothing between us. Slow, my first."],
            "explicit": ["I've never had it in my ass, Master -- it frightened me -- but I'm yours. Take my anal virginity bare; no barrier from you. Be patient with my first."],
            "crude":    ["Nobody's had my ass, Master -- scares me, sounds gross -- but I'm yours. Want it? Bare, no rubber. Ease that raw cock into my first."],
        }},

        # fallback approach
        {"when": {"pregnancy": ["none", "by_other"], "wants_anal_condom": False, "anal_virgin": True}, "lines": {
            "demure":   ["I've never done that... it seems improper, and it makes me nervous. But if I gave you that, I don't think I'd want a barrier -- just you, gently, my first."],
            "shy":      ["I-I've never done anal... it seems kind of dirty, and it scares me. But if I let you, I-I wouldn't want a condom -- I'd want to feel it's you. Gently."],
            "neutral":  ["I've never done anal -- it always seemed strange. But if I gave you that, I wouldn't want a barrier -- I'd want to feel it's really you taking my first. Go slow."],
            "direct":   ["I've never done anal -- seemed weird to me. But if I let you have it, I'd want it bare, just you. Take my first slow."],
            "explicit": ["I've never had it in my ass -- it seemed kind of nasty. But if I give you that, I'd want you bare -- feeling it's really you taking my first. Gently."],
            "crude":    ["Never had a cock in my ass -- sounds gross. But if I let you pop it, I want it bare, no rubber. Just ease into my first."],
        }},

    ])

    # =============================================================================================
    # ORAL CONDOM PREFERENCE  (live tree: vt_small_talk_pregnancy.rpy ~2682-2879)
    # Same shape as anal: approach x role only (no preg risk). NO oral-virgin overlay -- a first
    # blowjob doesn't carry the "gross/weird/trepidation" charge anal virginity does. by_player
    # carries pregnancy=="by_player"; wants/prefers gated pregnancy in {none, by_other} (no oral
    # by-other special case). Single-line wants/prefers -> neutral-only lines dict.
    # REWORDED 2026-07-09 (with the two anal ones): the general sexualized/student/prefers-bare line
    # dropped "I've never given oral without protection before" (first-timer language belongs only to a
    # virgin overlay, which oral doesn't have) -> now "nothing between us, that sounds so exciting!".
    # This table line intentionally diverges from live :2861 until Phase-2 rewiring.
    # =============================================================================================

    # ---- pregnancy == by_player : lifted verbatim from the already-vt_voice'd block (2685-2813). --
    vt_register_responses("oral_condom_pref", [

        # compassionate
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "mother"}, "lines": {
            "demure":   ["I'm already carrying your child... so tasting you with nothing between us is just about how close I want to be. I want all of you, nothing held back."],
            "shy":      ["I-I'm already pregnant with your baby... so the thought of tasting you bare, with nothing in the way, it... it would feel so intimate. I'd want that."],
            "neutral":  ["I'm already carrying your baby, Professor. As an experienced mother, wanting to taste you bare isn't about anything but feeling close to you -- it would be incredibly intimate."],
            "direct":   ["I'm carrying your child. I want to taste you bare -- not for any reason but wanting all of you, nothing between us."],
            "explicit": ["I'm pregnant with your baby. I want your bare cock on my tongue -- tasting you with nothing in the way is what I crave."],
            "crude":    ["I'm already knocked up -- so I want you raw in my mouth. Nothing between us, just the taste of you."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "student"}, "lines": {
            "demure":   ["Since I'm carrying your baby, Professor... could I taste you bare? It feels like it would be so close and special."],
            "shy":      ["I-I'm already pregnant with your baby, Professor... so I can suck you without a condom? That sounds... really intimate and special. I think I'd want it."],
            "neutral":  ["I'm carrying your baby, Professor. So tasting you bare would be such an intimate thing to share -- I want that closeness."],
            "direct":   ["I'm pregnant with your baby, Professor. I want to taste you bare too -- nothing between us, just you."],
            "explicit": ["I'm carrying your baby, Professor! So I want your bare cock on my tongue -- nothing in the way, just the taste of you."],
            "crude":    ["I'm already knocked up, Professor -- so I want you raw in my mouth too. I want to taste all of you, nothing between us."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "compassionate", "role": "other"}, "lines": {
            "demure":   ["I'm already carrying your child... so tasting you bare is just about how close I want to be. Nothing held back between us."],
            "shy":      ["I-I'm already pregnant with your baby... so the thought of tasting you with nothing in the way, it... it would be such a close, intimate thing."],
            "neutral":  ["I'm already carrying your baby. Tasting you bare would just be another way to feel all of you -- I want that intimacy."],
            "direct":   ["I'm carrying your child. I want to taste you bare -- nothing between us, just feeling all of you."],
            "explicit": ["I'm pregnant with your baby. I want your bare cock on my tongue too -- tasting you with nothing in the way."],
            "crude":    ["I'm already knocked up -- so I want you raw in my mouth. Nothing between us, just the taste of you."],
        }},

        # sexualized
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "mother"}, "lines": {
            "demure":   ["I'm carrying your baby already... and there's something so thrilling about tasting you completely bare now. I can't help wanting it."],
            "shy":      ["I-I'm pregnant with your baby... and the thought of tasting you bare, while I'm carrying you, makes me blush so hard. It's so naughty -- I want it."],
            "neutral":  ["I'm pregnant with your baby! As an experienced woman, tasting your bare cock while carrying your child is unbelievably hot. I want to swallow every drop!"],
            "direct":   ["I'm carrying your baby. I want your raw cock on my tongue -- tasting you bare is exactly what I crave."],
            "explicit": ["I'm pregnant with your baby! Sucking you bare while I'm carrying your child -- god, it's so filthy and hot. I want you to cum in my mouth."],
            "crude":    ["I'm already knocked up with your kid -- so give me your bare cock to suck. I want to taste your cum while I'm carrying you."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... and the idea of tasting you bare makes me tingle. It feels so naughty -- I think I want it."],
            "shy":      ["I-I'm pregnant with your baby, Professor! Oh my god, I can suck your bare cock and taste you? That's so naughty... but so hot. Yes!"],
            "neutral":  ["I'm pregnant with your baby, Professor! Tasting your bare cock while I'm carrying your child -- that's so hot. I want to feel you cum in my mouth!"],
            "direct":   ["I'm carrying your baby, Professor. I want your bare cock on my tongue -- nothing between us, it's so hot."],
            "explicit": ["I'm pregnant with your baby, Professor! Sucking you bare while carrying you -- god, that's so filthy and hot. Cum in my mouth!"],
            "crude":    ["I'm already knocked up, Professor -- so give me your raw cock. I want to taste your cum while I'm carrying you!"],
        }},
        {"when": {"pregnancy": "by_player", "approach": "sexualized", "role": "other"}, "lines": {
            "demure":   ["I'm carrying your baby already... and tasting you completely bare is so thrilling now. I can't help wanting it."],
            "shy":      ["I-I'm pregnant with your baby... and the thought of tasting you bare makes me shiver. It's so naughty -- I want it."],
            "neutral":  ["I'm pregnant with your baby! Tasting your bare cock while carrying your child? That's so hot. I want it!"],
            "direct":   ["I'm carrying your baby. I want your raw cock on my tongue -- tasting you bare is what I crave."],
            "explicit": ["I'm pregnant with your baby! Sucking you bare while carrying your child -- it's so filthy and hot. I want to swallow every drop."],
            "crude":    ["I'm already knocked up -- so give me your bare cock to suck. I want to taste your cum while I'm carrying you."],
        }},

        # transactional
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "mother"}, "lines": {
            "demure":   ["I'm carrying your child now, so I'm fully invested in you. I want to taste you bare too -- not as a charge, just because I crave you. Keep providing, and my mouth is yours."],
            "shy":      ["I-I'm carrying your baby, so I'm committed to you now... I want to taste you bare. Not for a price -- I just want it. Take care of us, and I'm yours."],
            "neutral":  ["I'm carrying your child -- I'm fully invested in you now. As an experienced mother, I want to taste you bare, nothing between us. Keep supporting me well, and my mouth is yours however you want it."],
            "direct":   ["I'm carrying your child, so I'm all in. I want to suck you bare -- not part of any deal, I just crave you. Keep providing and I'm yours."],
            "explicit": ["I'm carrying your child -- fully yours now. I want your bare cock in my mouth, nothing between us, because I crave the taste of you. Keep me well kept and use my mouth however you want."],
            "crude":    ["I'm knocked up with your kid, so I'm all yours -- I want to suck your raw cock because I fucking want to taste you, not for a price. Pay your way and use my mouth however."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, so I'm all yours now... does bare oral even cost anything? I don't want it for a price -- I just want to taste you."],
            "shy":      ["I-I'm carrying your baby, so I'm yours now... I want to taste you bare. Does that, um, cost extra? I don't really care -- I just want it."],
            "neutral":  ["I'm carrying your baby, so I'm all yours now... does bare oral cost anything? Because I want it -- I just want to taste you, nothing in the way."],
            "direct":   ["I'm carrying your baby, so I'm yours. I want to suck you bare -- forget the price, I just want to taste you."],
            "explicit": ["I'm carrying your baby, Professor, so I'm all yours -- I want your bare cock in my mouth, no charge, I just crave the taste of you."],
            "crude":    ["I'm knocked up, so I'm yours -- I want to suck your raw cock, no price, I just fucking want to taste you."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "transactional", "role": "other"}, "lines": {
            "demure":   ["I'm carrying your child, so I'm committed to you completely now. I want to taste you bare -- not part of a deal, just because I crave you."],
            "shy":      ["I-I'm carrying your baby, so I'm all in now... I want to taste you bare too. Not for a price -- I just want it."],
            "neutral":  ["I'm carrying your child, so I'm committed to you completely. I want to suck you bare now -- not part of any deal, just because I crave the taste of you."],
            "direct":   ["I'm carrying your child, so I'm yours. I want to suck you bare -- not a transaction, I just crave you."],
            "explicit": ["I'm carrying your child -- fully yours. I want your bare cock in my mouth, no charge, because I crave the taste of you."],
            "crude":    ["I'm knocked up with your kid, so I'm all yours -- I want to suck your raw cock because I want to taste you, not for a price."],
        }},

        # dominate
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "mother"}, "lines": {
            "demure":   ["I am carrying your child, Master. I want nothing between us now -- you may use my mouth bare, as you wish."],
            "shy":      ["I-I'm carrying your baby, Master... I want to taste you with nothing in the way. Use my mouth bare, however you please."],
            "neutral":  ["I am carrying your child, Master. As an experienced mother, I want to taste you bare now -- use my mouth as you wish."],
            "direct":   ["I'm carrying your child, Master. I want you bare on my tongue now -- use my mouth however you wish."],
            "explicit": ["I am carrying your child, Master. I want your bare cock in my mouth, nothing between us -- use it as you please."],
            "crude":    ["I'm knocked up with your kid, Master -- so use my mouth raw. Nothing between us, fuck my throat however you want."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "student"}, "lines": {
            "demure":   ["I'm carrying your baby, Professor... I want to taste you bare. Use my mouth however you like."],
            "shy":      ["I-I'm carrying your baby, Professor... I want to taste you bare now. You can use my mouth however you like."],
            "neutral":  ["I'm carrying your baby, Professor... I want to taste you bare now. Use my mouth however you like."],
            "direct":   ["I'm carrying your baby, Professor. I want you bare on my tongue -- use my mouth however you want."],
            "explicit": ["I'm carrying your baby, Professor. I want your bare cock in my mouth now -- use it however you like."],
            "crude":    ["I'm knocked up, Professor -- so use my mouth raw. Fuck my throat however you want."],
        }},
        {"when": {"pregnancy": "by_player", "approach": "dominate", "role": "other"}, "lines": {
            "demure":   ["I am carrying your child, Master. I want nothing in the way now -- use my mouth bare, as you wish."],
            "shy":      ["I-I'm carrying your baby, Master... I want to taste you bare. Use my mouth as you please."],
            "neutral":  ["I am carrying your child, Master. I want you bare on my tongue now -- use my mouth as you wish."],
            "direct":   ["I'm carrying your child, Master. I want you bare in my mouth -- use it as you wish."],
            "explicit": ["I am carrying your child, Master. I want your bare cock in my mouth, nothing between us -- use it as you please."],
            "crude":    ["I'm knocked up with your kid, Master -- so use my mouth raw, however you fucking want."],
        }},

        # fallback approach (unknown / other initial_reaction) -- no `approach` key, no role branch
        {"when": {"pregnancy": "by_player"}, "lines": {
            "demure":   ["I'm carrying your baby now... I don't want anything between us anymore. I'd love to taste you bare."],
            "shy":      ["I-I'm carrying your baby now... I don't want anything between us. I want to taste you bare."],
            "neutral":  ["I'm carrying your baby now... I don't want anything between us anymore. I want to taste you bare."],
            "direct":   ["I'm carrying your baby now -- I don't want anything between us. I want you bare on my tongue."],
            "explicit": ["I'm carrying your baby now -- nothing between us anymore. I want your bare cock on my tongue."],
            "crude":    ["I'm knocked up now -- so nothing between us. I want you raw in my mouth."],
        }},

    ])

    # ---- standing preference, WANTS PROTECTION for oral (live `elif wants_oral_condom`, 2815-2846). -
    vt_register_responses("oral_condom_pref", [

        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["As an experienced mother, I need to be careful about my health. When I'm sucking your cock, I prefer using protection - I can't risk getting sick while caring for my family."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "compassionate", "role": "student"}, "lines": {
            "neutral": ["I feel so connected to you, but I'm kind of nervous about oral... when I'm sucking your cock, I think I need that protection. I want to be safe."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "compassionate", "role": "other"}, "lines": {
            "neutral": ["I feel so connected to you, but when I'm sucking your cock, I need that protection. It lets me relax and enjoy pleasuring you without worry."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["The way you look at me is so hot... but as an experienced mother, I need to be careful. Using protection when I suck your cock shows you respect my health situation."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "sexualized", "role": "student"}, "lines": {
            "neutral": ["The way you look at me is so hot... but I'm kind of scared of oral without protection. Using something makes me feel safer... and actually kind of kinky!"],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "sexualized", "role": "other"}, "lines": {
            "neutral": ["The way you look at me is so hot... but using protection when I suck your cock can be its own kind of kinky."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "transactional", "role": "mother"}, "lines": {
            "neutral": ["What's in it for me? As an experienced mother with responsibilities, protected oral costs extra - I have to buy dental dams and stay healthy for my family."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "transactional", "role": "student"}, "lines": {
            "neutral": ["What's in it for me? Protected oral... um, does that cost less than without? I'm not sure about the pricing for blowjobs..."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "transactional", "role": "other"}, "lines": {
            "neutral": ["What's in it for me? Sucking your cock with protection costs extra... unless you make it worth my time."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["You're in charge, Master. As an experienced mother, if you want to use protection when I suck your cock, I'll accept it - I must stay healthy for my family."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "dominate", "role": "student"}, "lines": {
            "neutral": ["You're in charge, Professor. If you want to use protection for oral... I'll do what you want."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True, "approach": "dominate", "role": "other"}, "lines": {
            "neutral": ["You're in charge, Master. If you want to use protection when I suck your cock, I'll accept it."],
        }},

        # fallback approach
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": True}, "lines": {
            "neutral": ["I prefer using protection for oral sex... it's safer that way."],
        }},

    ])

    # ---- standing preference, PREFERS BARE for oral (live `else`, 2848-2879). Same shape. ----------
    vt_register_responses("oral_condom_pref", [

        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["I feel so connected to you. As an experienced mother, I want to taste your bare cock in my mouth - it's a different kind of intimacy that I trust you with."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "compassionate", "role": "student"}, "lines": {
            "neutral": ["I feel so connected to you. I want to taste your bare cock in my mouth... it feels more intimate without anything between us, you know?"],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "compassionate", "role": "other"}, "lines": {
            "neutral": ["I feel so connected to you. I want to taste your bare cock in my mouth, nothing between us when I'm pleasuring you."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["The way you look at me is so hot. As an experienced woman, I want to feel your bare cock sliding between my lips - motherhood hasn't dulled my desire to please you completely."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "sexualized", "role": "student"}, "lines": {
            "neutral": ["The way you look at me is so hot! I want to taste your bare cock in my mouth... nothing between us, that sounds so exciting!"],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "sexualized", "role": "other"}, "lines": {
            "neutral": ["The way you look at me is so hot. I want to feel your bare cock sliding between my lips, no barriers."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "transactional", "role": "mother"}, "lines": {
            "neutral": ["What's in it for me? Bare cock in my mouth from an experienced mother? That's premium pricing, Professor - I know exactly what I'm offering."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "transactional", "role": "student"}, "lines": {
            "neutral": ["What's in it for me? Bare oral? Is that more expensive? I don't really know what to charge for blowjobs... what do you think is fair?"],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "transactional", "role": "other"}, "lines": {
            "neutral": ["What's in it for me? Bare cock in my mouth? That's premium pricing, Professor."],
        }},

        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["You're in charge, Master. As an experienced mother, if you want me to suck your bare cock with no protection, I won't stop you - my mouth is yours to command."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "dominate", "role": "student"}, "lines": {
            "neutral": ["You're in charge, Professor. If you want me to suck your cock without a condom... okay, I'll do it. Whatever you want."],
        }},
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False, "approach": "dominate", "role": "other"}, "lines": {
            "neutral": ["You're in charge, Master. If you want me to suck your bare cock with no protection, I won't stop you."],
        }},

        # fallback approach
        {"when": {"pregnancy": ["none", "by_other"], "wants_oral_condom": False}, "lines": {
            "neutral": ["I don't really like protection for oral... I prefer to taste you directly."],
        }},

    ])

    # =============================================================================================
    # BIRTH CONTROL METHODS  (live tree: vt_small_talk_pregnancy.rpy ~3221-3384, the `_bc_line` block)
    # This is how she FRAMES her current birth-control status when asked. It branches ONLY on
    # birth_control x desire_tier x parent_broad x virgin x wants_vaginal_condom -- NOT on approach,
    # role, or pregnancy (the live `_bc_line` computation reads none of those; approach/role only
    # appear in the menu responses, which stay in the label). desire_tier uses the engine's fact
    # (mid = 30-70), matching the vaginal prefers-bare convention above.
    #
    # PARTITION: 2 (birth_control) x 3 (desire_tier) = 6 cells, each fully covered and disjoint:
    #   * HIGH tier splits: parent (player-parent, kids_with_player>0) -> parent_broad&!parent (a mother by
    #     experience but NOT by the player) -> !parent_broad&virgin -> !parent_broad&!virgin. So a base mother
    #     who never carried HIS child no longer claims "your baby again" (2026-07-29 conflation fix).
    #   * ON-pill MID/LOW have NO sub-split (one line each), matching the live tree.
    #   * NOT-pill MID/LOW split virgin x wants_vaginal_condom (2x2), as the live nested ifs.
    # No parent branch in MID/LOW (the live tree only checks _bc_parent in the HIGH tier), so a
    # parent there is non-virgin and falls to the `virgin: False` entries -- behaviour-preserving.
    # =============================================================================================

    # ---- ON birth control ------------------------------------------------------------------------
    vt_register_responses("bc_methods", [

        # desire HIGH (>70), on the pill -- PLAYER-PARENT (has carried HIS child; kids_with_player>0)
        {"when": {"birth_control": True, "desire_tier": "high", "parent": True}, "lines": {
            "demure":   ["I'm on the pill for now... though I'll confess, after carrying your child, a part of me resents the little thing."],
            "shy":      ["I'm on the pill... but, um... having already been a mother, there are days I wish I weren't taking it."],
            "neutral":  ["I'm on birth control at the moment. Honestly, after having your child, I take it more out of habit than conviction."],
            "direct":   ["I'm on the pill -- for now. But I've already carried your baby once, and that pull doesn't really go away."],
            "explicit": ["I'm on the pill, but after being bred by you once, I keep thinking about throwing it out and feeling you fill me again."],
            "crude":    ["I'm on the fucking pill, but you already knocked me up once -- half of me wants to flush them and let you breed me again."],
        }},
        # desire HIGH, on the pill -- a MOTHER by experience but NOT by the player (carried someone
        # else's child): speaks from her own past pregnancy, wants HIS to be next -- never "your baby again".
        {"when": {"birth_control": True, "desire_tier": "high", "parent_broad": True, "parent": False}, "lines": {
            "demure":   ["I'm on the pill for now... though having been a mother once, a part of me aches to feel that again -- with you, this time."],
            "shy":      ["I'm on the pill... but, um... I've carried a child before, and there are days I wish I weren't taking it when I think of you."],
            "neutral":  ["I'm on birth control at the moment. Honestly, I've been a mother already -- I take it out of habit more than conviction. I'd carry yours in a heartbeat."],
            "direct":   ["I'm on the pill -- for now. I've done this before, and that pull doesn't go away. The thought of the next one being yours is... a lot."],
            "explicit": ["I'm on the pill, but I've been pregnant before, and I keep thinking about tossing it and letting you be the one to fill me."],
            "crude":    ["I'm on the fucking pill, but I've been bred before -- half of me wants to flush them and let you be the one to knock me up."],
        }},
        {"when": {"birth_control": True, "desire_tier": "high", "parent_broad": False, "virgin": True}, "lines": {
            "demure":   ["I'm on the pill... even though I've never... you know. I suppose I just like imagining a someday."],
            "shy":      ["I'm on birth control... not that I've ever needed it yet. I just... think about the future, is all."],
            "neutral":  ["I'm on birth control, though honestly I've never even been with anyone. I just like the idea of being ready for it someday."],
            "direct":   ["I'm on the pill -- which is funny, since I've never actually done it. I just catch myself wondering what it'd be like."],
            "explicit": ["I'm on the pill even though I'm still a virgin. I can't help wondering what it'd feel like raw... even with nothing to compare it to."],
            "crude":    ["I'm on the pill and I haven't even been fucked yet. Doesn't stop me picturing you breeding me raw, though."],
        }},
        {"when": {"birth_control": True, "desire_tier": "high", "parent_broad": False, "virgin": False}, "lines": {
            "demure":   ["I'm on the pill... though, if I'm honest, the thought of one day not needing it makes my heart flutter."],
            "shy":      ["I'm on birth control... b-but I'd be lying if I said I never daydream about not being."],
            "neutral":  ["I'm on birth control. I'm responsible about it... even if some quiet part of me wishes I didn't have to be."],
            "direct":   ["I'm on the pill. Sensible, I know -- but the idea of going without it has been creeping into my head lately."],
            "explicit": ["I'm on the pill, but I keep imagining what it'd feel like raw, with nothing stopping you from putting a baby in me."],
            "crude":    ["I'm on the pill, but fuck, I fantasize about ditching it and letting you breed me bare."],
        }},

        # desire MID (30-70), on the pill -- no sub-split
        {"when": {"birth_control": True, "desire_tier": "mid"}, "lines": {
            "demure":   ["I'm on the pill. It's the sensible thing for now. Maybe that changes someday, but I'm in no hurry."],
            "shy":      ["I'm on birth control... it just feels like the responsible choice right now. I'm not really ready to think past that."],
            "neutral":  ["I'm on birth control. It keeps things simple for me -- I'd rather decide if and when, not leave it to chance."],
            "direct":   ["I'm on the pill. I like a bit of risk in the moment, sure, but actually rolling the dice? No, I stay covered."],
            "explicit": ["I'm on the pill. The idea of going raw is a fun thing to tease about... but I'm not actually careless enough to do it."],
            "crude":    ["I'm on the pill. Talking dirty about going bare is hot, but I'm not stupid enough to actually risk it."],
        }},

        # desire LOW (<30), on the pill -- no sub-split
        {"when": {"birth_control": True, "desire_tier": "low"}, "lines": {
            "demure":   ["I'm on the pill, and I stay on it. I'd never want to leave something that important to chance."],
            "shy":      ["I'm on birth control... yes. That part isn't up for debate. The thought of a surprise terrifies me."],
            "neutral":  ["I'm on birth control, and I'm careful about it. A pregnancy is the last thing I want right now."],
            "direct":   ["I'm on the pill, and I stay on it. I'm here for the fun, not for a baby -- that's the whole point.", "On the pill, yeah, and careful about it. The last thing I want is a little surprise."],
            "explicit": ["I'm on the pill and it stays that way. Fuck all you want, but I'm not getting knocked up over it."],
            "crude":    ["I'm on the pill and it's not coming off. You can rail me however you like, but a kid? Hard no."],
        }},

    ])

    # ---- NOT on birth control --------------------------------------------------------------------
    vt_register_responses("bc_methods", [

        # desire HIGH (>70), not on the pill -- breed me, don't pull out -- PLAYER-PARENT (kids_with_player>0)
        {"when": {"birth_control": False, "desire_tier": "high", "parent": True}, "lines": {
            "demure":   ["I'm not on anything right now... and after carrying your child, I find I don't really mind that."],
            "shy":      ["I'm... not on birth control. Having been a mother already, the thought of it happening again doesn't scare me like it should."],
            "neutral":  ["I'm not on any birth control. Honestly, after having your child, leaving it to nature feels right to me."],
            "direct":   ["I'm not on anything. I've already carried your baby once -- I'm not in a hurry to put a stop to that happening again."],
            "explicit": ["I'm not on birth control. After you bred me once, the idea of you doing it again with nothing in the way drives me wild."],
            "crude":    ["I'm not on shit. You already knocked me up once -- leave me bare and breed me again, I dare you."],
        }},
        # desire HIGH, not on the pill -- a MOTHER by experience but NOT by the player: past pregnancy, wants HIS next.
        {"when": {"birth_control": False, "desire_tier": "high", "parent_broad": True, "parent": False}, "lines": {
            "demure":   ["I'm not on anything right now... and having been a mother once, I find I don't mind that at all -- especially with you."],
            "shy":      ["I'm... not on birth control. I've carried a child before, so the thought of it happening again doesn't scare me the way it should -- not with you."],
            "neutral":  ["I'm not on any birth control. Honestly, I've been a mother before, and leaving it to nature with you feels right."],
            "direct":   ["I'm not on anything. I've carried a child before and I'd do it again in a heartbeat -- the idea of the next one being yours is thrilling."],
            "explicit": ["I'm not on birth control. I've been pregnant before, and the thought of you being the one to breed me next drives me wild."],
            "crude":    ["I'm not on shit. I've been knocked up before -- leave me bare and be the one to breed me next, I dare you."],
        }},
        {"when": {"birth_control": False, "desire_tier": "high", "parent_broad": False, "virgin": True}, "lines": {
            "demure":   ["I'm not on anything... not that I've had reason to be yet. But I do think about it, more than I admit."],
            "shy":      ["I'm not on birth control... I've never even been with anyone, so... I just haven't. The idea of it someday makes me flush."],
            "neutral":  ["I'm not on birth control. I've never needed it -- but I'd be lying if I said the idea of someday didn't appeal to me."],
            "direct":   ["I'm not on anything. I've never done it, so it's all just imagination -- but the thought of nothing in the way does something to me."],
            "explicit": ["I'm not on birth control. I'm still a virgin, so it's pure fantasy -- but I picture you taking me bare and filling me up far too often."],
            "crude":    ["I'm not on anything and I'm still a virgin. Doesn't stop me dreaming about you breeding me raw for my first time."],
        }},
        {"when": {"birth_control": False, "desire_tier": "high", "parent_broad": False, "virgin": False}, "lines": {
            "demure":   ["I'm not on anything right now... and the thought of leaving it that way makes my heart race, if I'm honest."],
            "shy":      ["I'm... not on birth control. I know I should be, but a part of me likes the idea of not being."],
            "neutral":  ["I'm not on any birth control. I keep telling myself I should start -- and keep not doing it, because some part of me wants this."],
            "direct":   ["I'm not on anything. I should be, I know -- but the idea of you bare with nothing stopping you is hard to give up."],
            "explicit": ["I'm not on birth control. The thought of you raw, with a real chance of putting a baby in me, is too good to give up."],
            "crude":    ["I'm not on shit. Take me bare and breed me -- that's exactly the risk I want."],
        }},

        # desire MID (30-70), not on the pill -- virgin x wants_vaginal_condom
        {"when": {"birth_control": False, "desire_tier": "mid", "virgin": True, "wants_vaginal_condom": True}, "lines": {
            "demure":   ["I'm not on anything... but I've never needed it, either. I'd want to sort that out before anything ever happened."],
            "shy":      ["I'm... not on birth control. I've never been with anyone, so it never came up. I'd want to be careful, though, if it did."],
            "neutral":  ["I'm not on birth control -- I've never had reason to be. But I'd definitely want to before taking any real risk."],
            "direct":   ["I'm not on anything. Never done it, so it never mattered -- but I wouldn't go in unprotected, that's for sure."],
            "explicit": ["I'm not on the pill -- I'm a virgin, so what would be the point yet? Whoever's my first had better wrap it, though."],
            "crude":    ["I'm not on anything 'cause I've never fucked anyone. But trust me, my first time, it's staying wrapped."],
        }},
        {"when": {"birth_control": False, "desire_tier": "mid", "virgin": True, "wants_vaginal_condom": False}, "lines": {
            "demure":   ["I'm not on anything -- I've never needed it. If it happened, I think I'd want it bare and just trust you to pull out... or not."],
            "shy":      ["I'm... not on birth control. I've never been with anyone. But I don't think I'd want a condom -- you'd pull out, maybe? I-I'd leave that to you."],
            "neutral":  ["I'm not on birth control -- never had reason to be. When it happens I'd lean bare, though, and leave the pulling-out to you."],
            "direct":   ["I'm not on anything; never done it. But I wouldn't want a condom -- you'd just pull out, or take the chance. Your call."],
            "explicit": ["I'm not on the pill -- I'm a virgin, so why would I be? When it happens I want it bare, though. You pull out... or you don't. Up to you."],
            "crude":    ["I'm not on anything 'cause I've never fucked. But when I do, no rubber -- pull out or breed me, I'd leave that to you."],
        }},
        {"when": {"birth_control": False, "desire_tier": "mid", "virgin": False, "wants_vaginal_condom": True}, "lines": {
            "demure":   ["I'm not on anything at the moment... which I know I should fix. I'd want us being careful in the meantime."],
            "shy":      ["I'm... not on birth control right now. It makes me a little nervous, honestly. I'd want to be safe until I sort it out."],
            "neutral":  ["I'm not on birth control currently. It's something I mean to handle -- until then I'd rather we didn't take chances."],
            "direct":   ["I'm not on anything right now. I should be, and I'd want us covered until I am -- I'm not looking for surprises."],
            "explicit": ["I'm not on the pill at the moment. The risk is a fun thing to flirt with, but I'd keep it wrapped until I am."],
            "crude":    ["I'm not on anything right now. Flirt with the risk all you want, but keep it wrapped till I'm sorted."],
        }},
        {"when": {"birth_control": False, "desire_tier": "mid", "virgin": False, "wants_vaginal_condom": False}, "lines": {
            "demure":   ["I'm not on anything at the moment... and honestly I prefer bare. So for now you'd pull out -- or not. I'd half leave that to you."],
            "shy":      ["I'm... not on birth control right now. I like it without, though, so... you'd just pull out, I suppose. Or not. I-I don't mind leaving it to you."],
            "neutral":  ["I'm not on birth control currently. I prefer bare, so until I sort the pill, it's pull-out -- and honestly I don't mind leaving that call to you."],
            "direct":   ["I'm not on anything right now. I like it raw, so no condom -- you just pull out. Or don't; I kind of like leaving that up to you."],
            "explicit": ["I'm not on the pill at the moment. I love it bare, so skip the rubber -- you pull out, or you don't. The risk is half the fun."],
            "crude":    ["I'm not on anything right now. I want it bare, so no condom -- pull out or cum in me, your call. I kinda like not deciding."],
        }},

        # desire LOW (<30), not on the pill -- virgin x wants_vaginal_condom
        {"when": {"birth_control": False, "desire_tier": "low", "virgin": True, "wants_vaginal_condom": True}, "lines": {
            "demure":   ["I'm not on anything -- but I've never been with anyone either, so it's never come up. If it ever did, I'd want to be very careful."],
            "shy":      ["I'm... not on birth control. I've never needed it. And honestly, the idea of a baby frightens me, so I'd want every precaution."],
            "neutral":  ["I'm not on birth control. I've never had reason to be -- but a pregnancy is the last thing I'd want, so I'd insist on protection."],
            "direct":   ["I'm not on anything, never have been -- never needed it. But a baby? No thanks. It'd be wrapped, every time."],
            "explicit": ["I'm not on the pill -- still a virgin, so why would I be? But I'm not trying to get knocked up, so it'd stay wrapped."],
            "crude":    ["I'm not on anything 'cause I've never been fucked. And when I am, no way I'm risking a kid -- it stays wrapped."],
        }},
        {"when": {"birth_control": False, "desire_tier": "low", "virgin": True, "wants_vaginal_condom": False}, "lines": {
            "demure":   ["I'm not on anything -- I've never been with anyone. But I think I'd want it bare, so you'd have to promise to pull out. A baby frightens me; I'd be trusting you."],
            "shy":      ["I'm... not on birth control. I've never needed it. If it happened I'd want bare, but... you'd have to pull out. I really couldn't handle being pregnant."],
            "neutral":  ["I'm not on birth control -- never had reason. But a pregnancy is the last thing I'd want, so if I went bare, you'd have to pull out, no exceptions."],
            "direct":   ["I'm not on anything, never have been. Never done it -- but I wouldn't want a condom either. You'd pull out, every time. A baby's a hard no."],
            "explicit": ["I'm not on the pill -- still a virgin, so why would I be? When it happens I want it bare, though, so you pull out before you finish. Getting knocked up is a hard no."],
            "crude":    ["I'm not on anything 'cause I've never been fucked. But when I am, no rubber -- you pull out, period. No fucking way I'm getting bred."],
        }},
        {"when": {"birth_control": False, "desire_tier": "low", "virgin": False, "wants_vaginal_condom": True}, "lines": {
            "demure":   ["I'm not on anything right now, which honestly worries me. I'd want us being very careful until I start."],
            "shy":      ["I'm... not on birth control, and it makes me anxious. A baby is the last thing I want -- please, let's be safe."],
            "neutral":  ["I'm not on birth control currently, and I don't like that. I want to start soon -- until then I'd insist we stay protected."],
            "direct":   ["I'm not on anything, and I need to fix that. A pregnancy is the last thing I want -- keep it wrapped until I'm covered."],
            "explicit": ["I'm not on the pill right now, and it makes me twitchy. Fuck me all you like, but it stays wrapped until I'm covered."],
            "crude":    ["I'm not on anything yet and it freaks me out. Use me however, but the condom stays on -- I'm not getting knocked up."],
        }},
        {"when": {"birth_control": False, "desire_tier": "low", "virgin": False, "wants_vaginal_condom": False}, "lines": {
            "demure":   ["I'm not on anything right now, which worries me -- but I do prefer bare. So you'd have to pull out, every time. A baby would be a real problem; I'm trusting you with that."],
            "shy":      ["I'm... not on birth control, and it makes me anxious. I like it bare, though, so... you'd need to pull out. Please be careful -- I really can't be pregnant."],
            "neutral":  ["I'm not on birth control currently, and I don't like that. I prefer bare, so until I start, you pull out -- a pregnancy is the last thing I want, so that's on you."],
            "direct":   ["I'm not on anything, and I need to fix that. I like it raw, though -- so no condom, you just pull out, every time. A baby? No. I'm trusting you to handle it."],
            "explicit": ["I'm not on the pill right now, and it makes me twitchy. I love it bare, so skip the rubber -- but you pull out before you cum. I'm not getting knocked up; that's on you."],
            "crude":    ["I'm not on anything yet and it freaks me out. I want it bare, though -- so no condom, just pull out in time. I'm not getting bred -- that's on you to get right."],
        }},

    ])

    # =============================================================================================
    # BODY-SHOT / EXTERNAL EJACULATION PREFERENCE  (live tree: vt_small_talk_pregnancy.rpy ~3026-3055,
    # the opening `_bc_line`-equivalent statement). The 4th sibling of the protection menu.
    # Branches approach x role ONLY -- no pregnancy/desire/virgin axes (external ejaculation carries
    # no pregnancy risk, and the live opening reads only dominant_approach + role). Single-line in the
    # source, so migrated neutral-only (vt_voice falls every register back to neutral).
    #
    # PARTITION: 4 known approaches x 3 roles = 12 entries (spec 2). The live `else` (any approach
    # outside those four) is a single role-agnostic line -> one empty-`when` fallback that loses on
    # specificity to the 12, exactly as the live if/elif/else routes.
    # =============================================================================================
    vt_register_responses("body_condom_pref", [

        # compassionate
        {"when": {"approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["I feel so connected to you, but as an experienced mother, I prefer using condoms even for body shots. It keeps things cleaner and more controlled for my family life."],
        }},
        {"when": {"approach": "compassionate", "role": "student"}, "lines": {
            "neutral": ["I feel so connected to you, but I'm kind of messy... I think I prefer condoms for body shots. It keeps things cleaner and less awkward."],
        }},
        {"when": {"approach": "compassionate", "role": "other"}, "lines": {
            "neutral": ["I feel so connected to you, but I prefer using condoms even for body shots. It keeps things cleaner and more controlled."],
        }},

        # sexualized
        {"when": {"approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["The way you look at me is so hot... but as an experienced mother, I need to be careful. Using condoms for body shots shows you respect my practical needs."],
        }},
        {"when": {"approach": "sexualized", "role": "student"}, "lines": {
            "neutral": ["The way you look at me is so hot... but I'm kind of worried about getting cum everywhere. Using condoms for body shots can be its own kind of sexy, right?"],
        }},
        {"when": {"approach": "sexualized", "role": "other"}, "lines": {
            "neutral": ["The way you look at me is so hot... but using condoms for body shots can be its own kind of sexy."],
        }},

        # transactional
        {"when": {"approach": "transactional", "role": "mother"}, "lines": {
            "neutral": ["What's in it for me? As an experienced mother with responsibilities, clean body shots cost extra - I have to maintain certain standards for my family."],
        }},
        {"when": {"approach": "transactional", "role": "student"}, "lines": {
            "neutral": ["What's in it for me? Body shots... um, does that cost extra if you want it clean? I'm not sure about the pricing for that..."],
        }},
        {"when": {"approach": "transactional", "role": "other"}, "lines": {
            "neutral": ["What's in it for me? Using condoms for body shots costs extra... unless you make it worth my time."],
        }},

        # dominate
        {"when": {"approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["You're in charge, Master. As an experienced mother, if you want to use condoms for body shots, I'll accept it - I must be careful as a mother."],
        }},
        {"when": {"approach": "dominate", "role": "student"}, "lines": {
            "neutral": ["You're in charge, Professor. If you want to use condoms for body shots... I'll do what you want."],
        }},
        {"when": {"approach": "dominate", "role": "other"}, "lines": {
            "neutral": ["You're in charge, Master. If you want to use condoms for body shots, I'll accept it."],
        }},

        # fallback approach (unknown / other initial_reaction) -- role-agnostic, lowest specificity
        {"when": {}, "lines": {
            "neutral": ["I'm not sure about body shots... I prefer to keep things clean."],
        }},

    ])

    # =============================================================================================
    # PREGNANCY-FEELINGS MENU -- item 1: SUPPORTIVE  ("This is a beautiful time in your life. How are
    # you feeling about it?")   Live tree: vt_small_talk_pregnancy.rpy ~3747-3885.
    # Gated in the label by `pregnant and player_knows_pregnant and knows_pregnant`, so the girl always
    # KNOWS she's pregnant here -> pregnancy in {by_player, by_other}. Branches approach x desire_tier
    # x role. Lines lifted verbatim; single-line source -> neutral-only (vt_voice falls back to neutral).
    #
    # SCOPE (pure-line branches first): compassionate / sexualized / dominate migrated here. The
    # `transactional` approach embeds its own cash sub-menus (player.cash checks + apply_impacts), which
    # are control flow -- it stays in the label untouched for now (both the >60 menu paths AND the <=60
    # else lines). apply_impacts({"affection", "baby_desire"}) also stays in the label.
    #
    # desire_tier uses the engine fact (>70 high, 30-70 mid, <30 low) -- the live compassionate/
    # sexualized/dominate branches all read `>70 / >30 / else`, the same 1-value edge diff at
    # baby_desire==30 already adopted table-wide (not a new divergence).
    # =============================================================================================
    vt_register_responses("pregnancy_feelings_supportive", [

        # ---- compassionate --------------------------------------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "desire_tier": "high", "role": "mother"}, "lines": {
            "neutral": ["It's wonderful! As an experienced mother, I feel so connected to you and our growing family. My body was made for this purpose, and I love that you're here with me through it all."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "desire_tier": "high", "role": "student"}, "lines": {
            "neutral": ["It's wonderful! I feel so connected to you. I've always dreamed about being pregnant with you, and now it's really happening!"],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "desire_tier": "high", "role": "other"}, "lines": {
            "neutral": ["It's wonderful! I feel so connected to you. I've always wanted to experience this with you."],
        }},

        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "desire_tier": "mid", "role": "mother"}, "lines": {
            "neutral": ["It's... unexpected but as an experienced mother, I'm trying to be positive about expanding our family, though I'm nervous about managing another child."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "desire_tier": "mid", "role": "student"}, "lines": {
            "neutral": ["It's... unexpected but I'm trying to be positive about it, though I'm scared about being pregnant and in school."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "desire_tier": "mid", "role": "other"}, "lines": {
            "neutral": ["It's... unexpected but I'm trying to be positive about it, though I'm scared."],
        }},

        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "desire_tier": "low", "role": "mother"}, "lines": {
            "neutral": ["I'm scared... as an experienced mother, I know how much work this is, and I wasn't planning another pregnancy right now."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "desire_tier": "low", "role": "student"}, "lines": {
            "neutral": ["I'm scared... I didn't plan for this to happen while I'm still in school. I don't know what to do."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "desire_tier": "low", "role": "other"}, "lines": {
            "neutral": ["I'm scared... I didn't plan for this to happen."],
        }},

        # ---- sexualized -----------------------------------------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "desire_tier": "high", "role": "mother"}, "lines": {
            "neutral": ["The way you look at me while I'm pregnant is so hot... knowing I'm carrying your child makes me want you even more. As an experienced woman, pregnancy makes me feel incredibly sexy!"],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "desire_tier": "high", "role": "student"}, "lines": {
            "neutral": ["The way you look at me while I'm pregnant is so hot... knowing I'm carrying your baby makes me so horny! I can't stop thinking about you!"],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "desire_tier": "high", "role": "other"}, "lines": {
            "neutral": ["The way you look at me while I'm pregnant is so hot... knowing I'm carrying your child makes me want you even more."],
        }},

        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "desire_tier": "mid", "role": "mother"}, "lines": {
            "neutral": ["Being pregnant is... different. As an experienced mother, I know my body is changing, but sometimes I still feel sexy knowing I'm carrying your baby."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "desire_tier": "mid", "role": "student"}, "lines": {
            "neutral": ["Being pregnant is... weird. Sometimes I feel sexy knowing I'm carrying your baby, but sometimes I just feel fat and awkward."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "desire_tier": "mid", "role": "other"}, "lines": {
            "neutral": ["Being pregnant is... different. Sometimes I feel sexy knowing I'm carrying your child."],
        }},

        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "desire_tier": "low", "role": "mother"}, "lines": {
            "neutral": ["Pregnancy isn't as sexy as I thought it would be... as an experienced mother, I know the reality is a lot of work and discomfort."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "desire_tier": "low", "role": "student"}, "lines": {
            "neutral": ["I don't feel very sexy right now... being pregnant is kind of gross actually. My body feels all weird."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "desire_tier": "low", "role": "other"}, "lines": {
            "neutral": ["I don't feel very sexy right now... pregnancy is a lot of work."],
        }},

        # ---- dominate -------------------------------------------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "desire_tier": "high", "role": "mother"}, "lines": {
            "neutral": ["I am carrying your child. As an experienced mother, I am prepared for this responsibility and will fulfill my duty to expand our family."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "desire_tier": "high", "role": "student"}, "lines": {
            "neutral": ["I'm carrying your baby! I'll do my best to be a good mother and take care of your child properly."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "desire_tier": "high", "role": "other"}, "lines": {
            "neutral": ["I am carrying your child. I am prepared for this responsibility."],
        }},

        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "desire_tier": "mid", "role": "mother"}, "lines": {
            "neutral": ["I am carrying your child. As an experienced mother, I will manage this situation efficiently and effectively."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "desire_tier": "mid", "role": "student"}, "lines": {
            "neutral": ["I'm carrying your baby... I'll try to handle this the best I can. I'm scared but I'll do what needs to be done."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "desire_tier": "mid", "role": "other"}, "lines": {
            "neutral": ["I am carrying your child. I will manage this situation."],
        }},

        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "desire_tier": "low", "role": "mother"}, "lines": {
            "neutral": ["I am carrying your child. As an experienced mother, this presents significant logistical challenges that must be addressed."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "desire_tier": "low", "role": "student"}, "lines": {
            "neutral": ["I'm carrying your baby... this is really complicated. I don't know how I'm supposed to handle this."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "desire_tier": "low", "role": "other"}, "lines": {
            "neutral": ["I am carrying your child. This presents significant challenges."],
        }},

    ])

    # =============================================================================================
    # PREGNANCY-FEELINGS MENU -- item 2: FETISH  ("I love the idea of you carrying my child inside
    # you...")   Live tree: vt_small_talk_pregnancy.rpy ~3888-3959.
    # Same knows-pregnant gate -> pregnancy in {by_player, by_other}. Here the 3 migrated approaches
    # branch approach x role ONLY (no desire_tier split -- only `transactional` splits, on baby_desire
    # >50). apply_impacts differs per approach and stays in the label.
    #
    # SCOPE (pure-line branches first): compassionate / sexualized / dominate migrated (9 entries,
    # neutral-only). LEFT IN LABEL: (a) the `transactional` approach -- >50 embeds a cash sub-menu,
    # <=50 is a role-split disgust reaction with its own affection/fear impacts; (b) the trailing `else`
    # (any approach outside the four) -- a disgust line + impacts. No empty-`when` fallback here on
    # purpose: a fallback would wrongly capture transactional states (whose live disgust text is
    # role-split and differs), so transactional + unknown both fall through to "" and the label's
    # existing if/elif/else keeps speaking them, behaviour-preserving.
    # =============================================================================================
    vt_register_responses("pregnancy_feelings_fetish", [

        # ---- sexualized -----------------------------------------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["That's... incredibly inappropriate, but as an experienced woman, I find it strangely exciting. I feel myself wanting it more, especially when you cum inside my pregnant pussy..."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "role": "student"}, "lines": {
            "neutral": ["That's... so dirty but so hot! Oh my god, saying that while I'm pregnant with your baby... I can't stop thinking about it! I want you so bad!"],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "role": "other"}, "lines": {
            "neutral": ["That's... incredibly inappropriate, but strangely exciting. I feel myself wanting it more, especially when you cum inside me..."],
        }},

        # ---- compassionate --------------------------------------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["Oh... you saying that while I'm already carrying your child... as an experienced mother, it makes me want to give you more babies."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "role": "student"}, "lines": {
            "neutral": ["Oh... you saying that while I'm pregnant with your baby... that's so romantic! I want to have more of your babies!"],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "role": "other"}, "lines": {
            "neutral": ["Oh... you saying that... it makes me want to carry your child even more."],
        }},

        # ---- dominate -------------------------------------------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["If you wish me to carry more of your children, Professor. As an experienced mother, my body is prepared to serve this purpose."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "student"}, "lines": {
            "neutral": ["If you want me to have more babies... okay, I will. Whatever you want, Professor."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "other"}, "lines": {
            "neutral": ["If you wish me to carry more of your children, I will obey your command."],
        }},

    ])

    # =============================================================================================
    # PREGNANCY-FEELINGS MENU -- item 3: PRACTICAL  ("We need to be responsible about this situation.")
    # Live tree: vt_small_talk_pregnancy.rpy ~3962-4027. This is the DECREASES-baby_desire path.
    # Same knows-pregnant gate -> pregnancy in {by_player, by_other}. Migrated approaches branch
    # approach x role ONLY (no desire_tier split). The top-level apply_impacts
    # ({"discipline": (750,1000), "baby_desire": (-750,-250)}) stays in the label.
    #
    # SCOPE (pure-line branches first): dominate (3) + compassionate/sexualized grouped (3) migrated
    # (6 entries, neutral-only). The grouped pair uses one entry per role with approach as a list
    # (["compassionate","sexualized"]), mirroring the live `in [...]` group -- both approaches speak
    # the same line. LEFT IN LABEL: (a) the `transactional` approach -- it embeds cash sub-menus
    # (player.cash checks + apply_impacts), no single spoken line; (b) the trailing `else` (any
    # approach outside the four) -- a single pure line, but migrating it would need an empty-`when`
    # fallback that would wrongly capture transactional states, so it stays in the label. transactional
    # + unknown both fall through to "" and the label's if/elif/else keeps speaking them.
    # =============================================================================================
    vt_register_responses("pregnancy_feelings_practical", [

        # ---- dominate -------------------------------------------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["You're absolutely right. As an experienced mother, I need to be more responsible for my existing family and this new child."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "student"}, "lines": {
            "neutral": ["You're right. I need to be more responsible about this... even though I'm scared about being a pregnant student."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "other"}, "lines": {
            "neutral": ["You're absolutely right. I need to be more responsible about this."],
        }},

        # ---- compassionate / sexualized (grouped in the live tree) ----------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": ["compassionate", "sexualized"], "role": "mother"}, "lines": {
            "neutral": ["I understand your concern, but as an experienced mother, I've made my decision. This baby is meant to be, and I'll handle my responsibilities to all my children."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": ["compassionate", "sexualized"], "role": "student"}, "lines": {
            "neutral": ["I understand you're worried, but I've made my decision. This baby happened and I'll handle it... even if it's scary."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": ["compassionate", "sexualized"], "role": "other"}, "lines": {
            "neutral": ["I understand your concern, but I've made my decision. This baby is meant to be."],
        }},

    ])

    # =============================================================================================
    # PREGNANCY-FEELINGS MENU -- item 4: NURTURING  ("How's the baby doing?")
    # Live tree: vt_small_talk_pregnancy.rpy. Asks how the baby IN HER WOMB is doing -- available to ANY
    # pregnant + known girl (the `is_base_mother` gate was removed 2026-07-26). Branches are approach-only.
    # The top-level apply_impacts ({"affection": (950,1500), "baby_desire": (750,1500)}) stays in the label.
    #
    # compassionate / sexualized / dominate each have a GENERAL entry (no role -- any pregnant girl) plus a
    # more-specific `role: mother` variant that out-specifies it, so a mother-character frames the same
    # unborn-baby question from experience. LEFT IN LABEL: (a) the `transactional` approach -- cash sub-menu
    # (player.cash checks + impacts), no single spoken line; (b) the trailing `else` (any approach outside
    # the four, provably-dead) -- a single pure line. Both fall through to "" and the label speaks them.
    # =============================================================================================
    # Varies by TRIMESTER (the `trimester` fact = first/second/third from pregnancy_phase). For each
    # trimester + approach there is a GENERAL line (any pregnant girl) and a more-specific `role: mother`
    # variant that out-specifies it (experienced-mother framing). Neutral-only for now.
    vt_register_responses("pregnancy_feelings_nurturing", [

        # ---- FIRST TRIMESTER (early; not showing yet) ----
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "first", "approach": "compassionate"}, "lines": {
            "neutral": ["It's so early still, but knowing there's a little life just starting inside me takes my breath away. I'm being so careful with everything I do."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "first", "approach": "sexualized"}, "lines": {
            "neutral": ["It's early, but just knowing your baby is already growing in me has me feeling some kind of way... honestly it's a total turn-on."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "first", "approach": "dominate"}, "lines": {
            "neutral": ["It's early days -- nothing to see yet. But I'm tracking everything carefully and taking all the right precautions."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "first", "approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["So early still, but as an experienced mother I know these first quiet weeks well. It brings back everything from when I was carrying my daughter."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "first", "approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["It's early, but I've done this before -- and being pregnant with your baby has me feeling as alive and needy as ever."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "first", "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["Early days. As an experienced mother I recognize the signs already, and I'm managing the prenatal care precisely."],
        }},

        # ---- SECOND TRIMESTER (showing; feeling movement) ----
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "second", "approach": "compassionate"}, "lines": {
            "neutral": ["It's wonderful now -- I can feel the little flutters, and my bump is really starting to show. It finally feels real. I've been reading everything I can about how the baby's growing."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "second", "approach": "sexualized"}, "lines": {
            "neutral": ["The bump's showing and I can feel them move now! Being pregnant with your child makes me feel so alive... I can't wait until you can feel them too."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "second", "approach": "dominate"}, "lines": {
            "neutral": ["The baby is developing as expected. The bump is here, the movements are regular -- I'm managing all of the prenatal care properly."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "second", "approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["Wonderful! As an experienced mother, I can feel the kicks now. It's bringing back such beautiful memories with my daughter. I've been researching fetal development extensively for our growing family."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "second", "approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["Amazing! As an experienced woman, pregnancy makes me feel so alive and sexy! I can't wait until you can feel them move too!"],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "second", "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["The baby is developing as expected. As an experienced mother, I am managing all prenatal care appropriately."],
        }},

        # ---- THIRD TRIMESTER (heavily pregnant; near due) ----
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "third", "approach": "compassionate"}, "lines": {
            "neutral": ["Getting close now! They kick so much these days. I'm tired and huge, but I can't wait to meet them... not long to go."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "third", "approach": "sexualized"}, "lines": {
            "neutral": ["God, I'm huge and they will not stop kicking -- but there's something so hot about being this full with your baby. Almost there!"],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "third", "approach": "dominate"}, "lines": {
            "neutral": ["Third trimester. Large and uncomfortable, but on schedule. The baby is strong and the due date is close."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "third", "approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["Almost there! They're so active now. As an experienced mother I know just how close we are -- and I still get emotional every time, exactly like I did with my daughter."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "third", "approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["So big, and they kick constantly! I've carried before, but being this full with your baby is its own kind of thrilling. Nearly time!"],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "trimester": "third", "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["Third trimester, near term. As an experienced mother I have every preparation in order. The baby is strong and delivery is close."],
        }},

    ])

    # =============================================================================================
    # PREGNANCY-FEELINGS MENU -- item 5: SCHOOL  ("What about school? How will you manage?")
    # Live tree: vt_small_talk_pregnancy.rpy ~4060-4104. This menu item is STUDENT-ONLY -- the live
    # option is gated `if is_student`, so there is NO role split inside; every line is student-flavored.
    # Branches are approach-only.
    #
    # NOTE (Phase-2 wiring): unlike items 1/3/4 there is NO top-level apply_impacts -- each branch runs
    # its OWN apply_impacts before speaking, and they DIFFER: dominate (:4062) and the
    # [compassionate,sexualized] group (:4100) both apply {"affection":(950,1500),"baby_desire":(750,1500)};
    # the `else` (:4103) applies {"affection":(750,1500)} only; transactional's impacts live inside its
    # menu results. So the impacts cannot be hoisted -- they stay per-branch in the label. Only the
    # spoken line migrates.
    #
    # SCOPE (pure-line branches first): dominate + [compassionate,sexualized] group migrated (2 entries,
    # neutral-only). Each carries `"role": "student"` (redundant with the live menu gate but makes the
    # beat self-protecting -- returns "" for a non-student). LEFT IN LABEL: (a) the `transactional`
    # approach -- a cash sub-menu AND a grade-bump sub-menu (player.cash / girl.grades mutations); (b) the
    # trailing `else` (any approach outside the four) -- a single pure line + its own impacts, not
    # migrated because a fallback would misroute transactional states. transactional + unknown fall
    # through to "" and the label keeps speaking them.
    # =============================================================================================
    vt_register_responses("pregnancy_feelings_school", [

        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "student"}, "lines": {
            "neutral": ["I've been thinking about it... as a student mother, I want this baby more than anything, even if it means taking time off school. I've already researched online degree programs that work with pregnancy."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": ["compassionate", "sexualized"], "role": "student"}, "lines": {
            "neutral": ["I've been thinking about it... as a student, I want this baby more than anything, even if it means taking time off school. Your support means everything."],
        }},

    ])

    # =============================================================================================
    # PREGNANCY-FEELINGS FAMILY -- PHASE-5 PRENATAL-VITAMINS beat ("I brought these prenatal vitamins...")
    # Live tree: vt_small_talk_pregnancy.rpy. This is a CONTEXTUAL menu item, gated on the player
    # actually carrying PregnaVITA -- `player.get_item_quantity("prenatal_vitamins") > 0` (VT pills live
    # in the sidecar pill_counts, NOT base inventory, so has_item/remove_item must NOT be used). The
    # menu-item body spends one via `vt_player_pill_counts(player)`, THEN branches on dominant_approach.
    # Every migratable branch is ROLE-SPLIT (is_base_mother / is_student / else).
    #
    # NOTE (Phase-2 wiring): there is NO top-level apply_impacts, and the pill is spent at the
    # menu-item level BEFORE the approach check. Each approach branch runs its OWN apply_impacts and they
    # DIFFER: compassionate {"affection":(750,1500),"prenatal_boost":1}; sexualized
    # {"prenatal_boost":1,"corruption":(250,750),"affection":(250,750)}; dominate
    # {"prenatal_boost":1,"affection":(750,1500),"fear":(-750,-250)}; the `else` (hesitant)
    # {"prenatal_boost":1,"fear":(-750,-250)}. So the item-removal and per-branch impacts stay in the
    # label -- only the spoken line migrates.
    #
    # SCOPE (pure-line branches): compassionate / sexualized / dominate migrated, each role-split
    # (mother/student/other) = 9 entries, neutral-only. Role encodes the live is_base_mother/is_student/
    # else split (role "other" = the live `else`). `pregnancy:[by_player,by_other]` follows the label gate.
    # LEFT IN LABEL: (a) the `transactional` approach -- a line then a cash sub-menu AND a student-only
    # grade-bump / A+ / medical-coverage / "just take them" sub-menu (player.cash / girl.grades mutations);
    # (b) the trailing `else` (hesitant acceptance) -- role-split lines + its own impacts + a trailing
    # narrator beat ("[selected_girl] hesitates before taking them..."), not migrated because a fallback
    # would misroute transactional states. transactional + unknown fall through to "" and the label keeps
    # speaking them.
    # =============================================================================================
    vt_register_responses("pregnancy_feelings_prenatal_vitamins", [

        # ---- compassionate (genuinely grateful) -----------------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "role": "mother"}, "lines": {
            "neutral": ["Oh! Thank you so much, Professor! As an experienced mother, this means the world to me - you're already thinking about our baby and my other child. I feel so connected to you."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "role": "student"}, "lines": {
            "neutral": ["Oh! Thank you so much, Professor! This means the world to me - you're already taking care of our baby! I feel so connected to you."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "compassionate", "role": "other"}, "lines": {
            "neutral": ["Oh! Thank you so much, Professor! This means the world to me - you're already taking care of our baby. I feel so connected to you."],
        }},

        # ---- sexualized (turns it into something sexual) --------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "role": "mother"}, "lines": {
            "neutral": ["Mmm... taking care of your baby while pregnant with your child... As an experienced woman, that's so hot. I'll take these vitamins if it means you'll keep taking care of me in other ways too."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "role": "student"}, "lines": {
            "neutral": ["Mmm... taking care of your baby while pregnant... that's so hot! I'll take these vitamins if it means you'll keep taking care of me in other ways too!"],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "sexualized", "role": "other"}, "lines": {
            "neutral": ["Mmm... taking care of your baby while pregnant... That's so hot. I'll take these vitamins if it means you'll keep taking care of me in other ways too."],
        }},

        # ---- dominate (accepts without question) ----------------------------------------------------
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "mother"}, "lines": {
            "neutral": ["If that's what you want, Master. As an experienced mother, I'll take these vitamins for our baby and stay healthy for my other child too."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "student"}, "lines": {
            "neutral": ["If that's what you want, Professor. I'll take these vitamins for our baby."],
        }},
        {"when": {"pregnancy": ["by_player", "by_other"], "approach": "dominate", "role": "other"}, "lines": {
            "neutral": ["If that's what you want, Master. I'll take these vitamins for our baby."],
        }},

    ])

    # =============================================================================================
    # BIRTH-CONTROL PERSUASION PITCHES  (salvaged from the retired vt_small_talk_birth_control.rpy)
    # Four themed player pitches added to the live bc_methods sub-menu. The LABEL computes her consent
    # band (vt_willingness_band on the pitch's intent) and calls the matching _yes / _no beat here; these
    # beats vary ONLY by register (vt_voice), so they carry no `when`. Lines seed the old file's best
    # flavor. natural -> natural_cycle intent; family + thrill -> stop_bc_breed; health -> start_bc.
    # =============================================================================================

    # ---- NATURAL CYCLE ("your body would feel better functioning naturally") -> stop BC ----
    vt_register_responses("bc_pitch_natural_yes", [
        {"lines": {
            "neutral": ["You make a compelling argument... I've always felt our bodies work best naturally. I'll stop taking them and let my cycle run its course."],
            "demure":  ["That's a thoughtful way to see it. I'll set the pills aside and trust my body to do what it's meant to."],
            "shy":     ["I... I suppose our bodies are meant to work on their own. Okay... I'll stop taking them."],
            "direct":  ["Honestly? Going off the hormones sounds good to me. I'll stop -- let's see how my body does on its own."],
            "explicit":["Nothing artificial between us? That idea does something to me. I'll come off the pills."],
            "crude":   ["Mmm... natural means more chances for you to fill my bare pussy. Pills are gone."],
        }},
    ])
    vt_register_responses("bc_pitch_natural_no", [
        {"lines": {
            "neutral": ["I see your point about natural living, Professor, but I'd rather stay on my birth control for now."],
            "demure":  ["I appreciate the philosophy, truly, but I prefer the certainty my birth control gives me."],
            "shy":     ["I... I understand, but going off them frightens me. I'd rather keep taking them."],
            "crude":   ["Cute pitch, but the pill stays. I'm not gambling my body on 'natural.'"],
        }},
    ])

    # ---- FAMILY PLANNING -> stop BC. Splits on parent_broad so the answer matches the caption: a mother
    #      (has a child) answers about giving her little one a SIBLING; a childless girl about STARTING one. ----
    vt_register_responses("bc_pitch_family_yes", [
        {"when": {"parent_broad": True}, "lines": {
            "neutral": ["A little brother or sister for my little one... you know, I'd love that. I'll stop taking them."],
            "demure":  ["A sibling for my child... I've quietly hoped for exactly that. I'll set my birth control aside."],
            "shy":     ["I... I think they'd adore a sibling. And so would I. O-okay... I'll stop."],
            "direct":  ["Honestly? They deserve a sibling, and I want another. I'll stop taking them."],
            "explicit":["Give my little one a sibling and fill me up doing it? God, yes. I'll stop taking them."],
            "crude":   ["Fuck yes -- knock me up and give them a sibling. I'm done with the pills."],
        }},
        {"when": {"parent_broad": False}, "lines": {
            "neutral": ["You know... I've always pictured starting a family with you. Maybe it's time. I'll stop taking them."],
            "demure":  ["I've long dreamed of a family with you. Perhaps you're right... I'll set my birth control aside."],
            "shy":     ["I... I've dreamed about giving you a family. O-okay... I'll stop."],
            "direct":  ["Honestly, I've wanted this -- a family with you. I'll stop taking them."],
            "explicit":["Starting a family with you? The thought makes me ache. I'll stop taking them."],
            "crude":   ["God, yes -- put a baby in me. I'm done with the pills."],
        }},
    ])
    vt_register_responses("bc_pitch_family_no", [
        {"when": {"parent_broad": True}, "lines": {
            "neutral": ["Maybe one day they'd like a little sibling... but I'm not ready to come off my birth control for that yet."],
            "shy":     ["They might love a sibling someday... but I'm not ready for another just now. I'll keep taking them."],
            "crude":   ["A sibling eventually, sure -- not today. The pill stays on."],
        }},
        {"when": {"parent_broad": False}, "lines": {
            "neutral": ["I'd love a family with you someday, Professor, but I'm not ready to stop just yet."],
            "shy":     ["Someday I want that with you... but not yet. I'll keep taking them for now."],
            "crude":   ["Slow down -- I want kids eventually, not today. Pill stays."],
        }},
    ])

    # ---- THRILL / RISK ("something exciting about the possibility") -> stop BC ----
    vt_register_responses("bc_pitch_thrill_yes", [
        {"lines": {
            "neutral": ["God, that's a wicked thing to say... but you're right, the risk is exciting. I'll stop taking them."],
            "demure":  ["That's a shocking thing to propose, Professor... though I can't pretend I feel no thrill. I'll stop taking them."],
            "shy":     ["That's... that's a scandalous thing to suggest. B-but the thrill of it... okay. I'll stop."],
            "direct":  ["You're terrible for saying that -- and you're right, it's a rush. I'll stop taking them."],
            "explicit":["That's so inappropriate... and so hot. The danger of it. I'll stop taking them."],
            "crude":   ["Fuck, the risk makes me wet. Breed me and let's see what happens -- pills are gone."],
        }},
    ])
    vt_register_responses("bc_pitch_thrill_no", [
        {"lines": {
            "neutral": ["That's a reckless thrill, Professor. Exciting to imagine, but I'll keep my birth control."],
            "shy":     ["That's... a lot to even think about. It scares me more than it excites me. I'll keep taking them."],
            "crude":   ["Hot fantasy, but I'm not actually rolling those dice. Pill stays."],
        }},
    ])

    # ---- HEALTH / RESPONSIBLE ("be responsible") -> start BC ----
    vt_register_responses("bc_pitch_health_yes", [
        {"lines": {
            "neutral": ["You're right, Professor. I should be more responsible about this. I'll start taking birth control."],
            "demure":  ["That's a responsible concern, and I appreciate it. I'll begin taking birth control."],
            "shy":     ["I... I suppose you're right. I'll start birth control, to be safe."],
            "direct":  ["Fair point. No surprises unless we mean it. I'll get on birth control."],
            "crude":   ["Fair enough -- no accidents unless we actually want one. I'll get on the pill."],
        }},
    ])
    vt_register_responses("bc_pitch_health_no", [
        {"lines": {
            "neutral": ["I hear your concern, Professor, but I'm not going to start birth control right now."],
            "shy":     ["I... I know you mean well, but I don't think I'm ready to start them."],
            "crude":   ["Appreciate the concern, but I'll take my chances without the pill for now."],
        }},
    ])

    # ---- OFF-BC variants of the family + thrill pitches (she's already off birth control, so the pitch
    #      is about actually TRYING, not stopping) -- used when those pitches are asked to an off-BC girl. ----
    vt_register_responses("bc_pitch_family_yes_offbc", [
        {"when": {"parent_broad": True}, "lines": {
            "neutral": ["You know... they really would love a sibling. And I'm not on anything to stop it. Let's give them one."],
            "demure":  ["A sibling for my little one... and I'm doing nothing to prevent it. Perhaps we should simply let it happen."],
            "shy":     ["I... I'm not even on the pill. So if we wanted to give them a sibling... we already could, couldn't we?"],
            "direct":  ["Honestly? I'm already off the pill. If you want to give them a sibling, we don't have to wait."],
            "explicit":["They need a sibling and I'm not on anything -- so every time you finish in me, we're already trying. Let's make it count."],
            "crude":   ["They need a sibling and I'm off the pill already, so quit talking and put another baby in me."],
        }},
        {"when": {"parent_broad": False}, "lines": {
            "neutral": ["You know... I'm not on anything as it is. Maybe we should just start that family and see."],
            "demure":  ["I've hoped for a family with you... and I'm doing nothing to prevent it. Perhaps we should simply let nature decide."],
            "shy":     ["I... I'm not even on the pill. So if we wanted to start a family... we sort of already could, couldn't we?"],
            "direct":  ["Honestly? I'm already off the pill. If you want to start a family, we don't have to wait."],
            "explicit":["I'm not on anything -- so every time you finish inside me, we're already playing that game. Let's make it count."],
            "crude":   ["I'm off the pill already, so quit talking and put a baby in me."],
        }},
    ])
    vt_register_responses("bc_pitch_family_no_offbc", [
        {"when": {"parent_broad": True}, "lines": {
            "neutral": ["They might love a little brother or sister someday... but I'm not ready to make that happen just yet."],
            "shy":     ["I... I'm off the pill, but that doesn't mean I'm ready to give them a sibling right this moment."],
            "crude":   ["Off the pill, sure, but I'm not begging you to give them a sibling today. Ease off."],
        }},
        {"when": {"parent_broad": False}, "lines": {
            "neutral": ["I'm not on anything, it's true... but I'm not in a rush to start a family just yet."],
            "shy":     ["I... I'm off the pill, but that doesn't mean I'm ready to actually try. Not this second."],
            "crude":   ["Off the pill, sure, but I'm not begging you to knock me up today. Ease off."],
        }},
    ])
    vt_register_responses("bc_pitch_thrill_yes_offbc", [
        {"lines": {
            "neutral": ["You don't have to tell me -- every time you go bare, that little risk is electric. I love it."],
            "demure":  ["I know... and I'll admit, being off the pill with you, there's a thrill to it I don't want to give up."],
            "shy":     ["I... I already feel it. Being off the pill, every time... it's frightening and exciting all at once."],
            "direct":  ["Trust me, I feel it. I'm already off the pill -- every time you finish in me is a roll of the dice, and I love it."],
            "explicit":["God, I know. I'm not on anything, so every time you breed me it's real. That danger gets me so wet."],
            "crude":   ["Fuck yes I feel it. No pill -- every load you dump in me could take. That's the whole thrill."],
        }},
    ])
    vt_register_responses("bc_pitch_thrill_no_offbc", [
        {"lines": {
            "neutral": ["It's a thrill to imagine, sure... but I'm already off the pill, so let's not get too reckless."],
            "shy":     ["I... I'm off the pill as it is, and honestly that already scares me a little. Let's be careful."],
            "crude":   ["I'm already playing with fire without the pill. Don't push it, or I'll go back on them."],
        }},
    ])

    # ---- Already KNOWINGLY pregnant: birth control / breeding / risk are all moot, so the bc_methods
    #      answer AND every pitch deflect to this. Father-NEUTRAL wording (works for by_player and by_other;
    #      never claims the player did it). Only used when she KNOWS she's pregnant -- a secret pregnancy
    #      still gets the normal not-pregnant lines (in-world consistent; nobody knows yet). ----
    vt_register_responses("bc_already_pregnant", [
        {"lines": {
            "demure":  ["Oh, Professor... I'm already expecting. All this talk of preventing it or risking it is rather moot now, isn't it?"],
            "shy":     ["Um... Professor? I'm already pregnant. So... that whole question is kind of behind us now."],
            "neutral": ["Professor, I'm already pregnant -- so birth control's rather beside the point at this stage, don't you think?"],
            "direct":  ["Bit late for that, Professor -- I'm already knocked up. That whole conversation's behind us."],
            "explicit":["Professor, I'm already carrying -- so all this pregnancy talk? We're well past that now."],
            "crude":   ["I'm already fucking pregnant, Professor. Prevent it, risk it -- too late now, it's done."],
        }},
    ])

    # The family topic resolves what the player knows before choosing from these replies.
    VT_FAMILY_PREGNANCY_REPLIES = {
        ("daughter", "both_by_player"): {
            "compassionate": (
                "It's a lot to take in... my mom and I, both carrying your children at the same time. Strange as it is, I'm glad we'll have each other to go through it with.",
                "Seeing Mom go through this too makes me feel less alone. We're both having your children, and she's the one person I can talk to without explaining why it's complicated.",
                "Mom's carrying your baby too. I keep getting stuck on that part. Then I remember she's probably just as overwhelmed as I am. I want to be there for her.",
            ),
            "sexualized": (
                "Both of us, round with your babies at the same time? God, that's messed up... and it turns me on more than it should.",
                "Mom and I are both having your babies. Even saying that feels like I've told you a secret we all already know. I can't stop smiling at how strange it sounds.",
                "Mom and I, both having your children. Try saying that with a straight face, Professor. I can barely do it myself.",
            ),
            "dominate": (
                "I want to ask Mom how she's holding up, Professor. She's having your baby, and so am I. I don't know what I'd say if she asked me first.",
                "Mom and I are both having your children, Professor. I want to talk to her about it. I keep practicing the first sentence and stopping before I get to the second.",
                "I want to be honest with you, Professor. Knowing Mom's carrying your baby too makes me want to ask for help, even if I haven't quite worked out what I'd ask for.",
            ),
            "transactional": (
                "My mom and I, pregnant with your kids at the same time... I don't really know how I'm supposed to feel about that.",
                "Mom and I are both having your kids. That's a lot to take on at once, and I need a minute before I can tell you how I feel about it.",
                "I know Mom's carrying your baby too. I'm trying to take in what this means for me before I start guessing what it means for the three of us.",
            ),
        },
        ("daughter", "both_expecting"): {
            "compassionate": (
                "It's strange, both of us expecting at once. At least neither of us has to go through it alone.",
                "Mom and I are both expecting, so at least I can talk to her about the weird little things that make no sense to anyone else.",
                "I thought I'd be asking Mom about what she remembered. Now we're both expecting, so we can compare notes as we go.",
            ),
            "sexualized": (
                "My mom and I, both pregnant at the same time? That's... a lot to sit with, honestly.",
                "Mom and I, both expecting at once. That sounds like gossip I'd laugh at if it were about anyone else. Living it is a lot more interesting.",
                "My mom and I both pregnant? Go ahead, you can look surprised. I did, and I'm one of the people it happened to.",
            ),
            "dominate": (
                "I hadn't thought about it that way, Professor. Both of us expecting at once -- it's just a coincidence, that's all.",
                "I'm still getting used to it, Professor. With Mom and me both expecting, I think I'd rather let her decide when we talk about it together.",
                "When you say it out loud like that, it does feel strange, Professor. Mom and I are both expecting. I'm trying to give her the same space I'd want.",
            ),
            "transactional": (
                "It's weird, both of us being pregnant at the same time. It's a lot for one house.",
                "Mom and I are both pregnant. I'm still thinking about what that changes for each of us. It might take me a while to have much to say.",
                "We both have our own decisions to make. I'm fine talking about Mom, but I'd rather keep the details of the two pregnancies separate.",
            ),
        },
        ("daughter", "relative_by_player"): {
            "compassionate": (
                "My mom, carrying your child... it's a lot to process. But I don't hate the idea of our families being tied together like that.",
                "Mom's carrying your child. I worry about her sometimes, and I hope she feels she can talk to both of us when things get hard.",
                "It'll take me a while to get used to Mom having your baby. She's still my mom, though. If she needs me, I want her to know she can ask.",
            ),
            "sexualized": (
                "You got my mom pregnant? God, that's filthy... and I can't stop thinking about it.",
                "So Mom's having your baby. I was going to play it cool when you brought it up, but that plan lasted about two seconds.",
                "My mom, carrying your child. I had a very clever remark ready for this, Professor, and somehow all I've got left is a grin.",
            ),
            "dominate": (
                "So my mother is carrying your child, Professor. I suppose that's simply how it is now.",
                "Yes, Professor, I know Mom's carrying your child. I think I'll follow her lead on what she's comfortable talking about.",
                "I did wonder how to bring up the fact that Mom's having your baby, Professor. I wanted to give her a chance to tell me how she feels first.",
            ),
            "transactional": (
                "I still don't really know what to think about my mom carrying your baby. It's a lot to wrap my head around.",
                "My mom's having your baby. I still have questions, but I think most of them are ones I need to ask her.",
                "Mom's carrying your child. I'm trying to work out how that changes things in our family. Give me a little time with it.",
            ),
        },
        ("daughter", "relative_expecting"): {
            "compassionate": (
                "I know about my mom. It's strange to think about, but I'm glad she's not going through it alone.",
                "I'm still getting used to Mom being pregnant. I hope she knows she can call me, even if all she wants is someone to listen.",
                "When I think about Mom expecting, mostly I want to make sure she has someone to lean on. I'd like to be that person if she wants.",
            ),
            "sexualized": (
                "My mom, pregnant? That's... a weirdly hot thing to think about, honestly.",
                "Mom's pregnant. There are about six jokes I could make, and I'd get a look for every single one of them. I'll behave. Mostly.",
                "I didn't expect news about Mom to make me blush, but here we are. Give me a second and I'll think of something clever to say.",
            ),
            "dominate": (
                "Yes, I know about my mother. It changes things around the house, but it's really none of my business, Professor.",
                "I know Mom's expecting, Professor. I think she'll talk about it when she wants to. I'd rather leave that up to her.",
                "I know about her pregnancy, Professor. I've thought about asking whether she needs anything. I think I'd be better at helping than talking about how I feel.",
            ),
            "transactional": (
                "It's strange, knowing my mom is pregnant. I'm still getting used to the idea.",
                "I'm still sorting out what Mom's pregnancy means for us. I don't have a tidy answer for you yet.",
                "I know she's expecting. I don't really want to speak for Mom, especially on something this personal.",
            ),
        },
        ("mother", "both_by_player"): {
            "compassionate": (
                "My daughter and I, both carrying your children at the same time... it's not how I imagined motherhood again, but I'm grateful we'll have each other.",
                "I never pictured sharing this part of my life with my daughter. We're both having your children, and I hope she knows she can lean on me. I may need to lean on her too.",
                "My daughter is carrying your child too. When she asks me what it's like, I'll have an answer from this morning for a change.",
            ),
            "sexualized": (
                "Both of us round with your children at once -- mother and daughter. It's obscene... and I love every second of it.",
                "My daughter and I are both carrying your children. I had every intention of being very serious about this, Professor. Then I caught the look on your face.",
                "The two of us are having your children, and I still catch myself smiling at how much that sentence surprises me. I suspect I'll enjoy watching you get used to it.",
            ),
            "dominate": (
                "I want to tell my daughter we'll be all right, Professor. We're both carrying your children, and right now I wish I could believe that myself.",
                "I'm trying to stay composed, Professor. My daughter and I are both carrying your children, and there are times when I feel I ought to have an answer for her. I don't always have one.",
                "I appreciate you asking, Professor. My daughter and I are both carrying your children, and I've been so busy thinking about her that I haven't let myself wonder what I want from all of this.",
            ),
            "transactional": (
                "My daughter and I, pregnant with your children at the same time. I'm still working out how I feel about all of it.",
                "My daughter and I are both having your children. I've started thinking about what each of us will need. My feelings are taking a little longer to catch up.",
                "Knowing we're both carrying your children is a lot to take in. I need some time with my daughter before I know what I'm comfortable saying to anyone else.",
            ),
        },
        ("mother", "both_expecting"): {
            "compassionate": (
                "It's strange, the two of us expecting at once. At least we can lean on each other through it.",
                "We're both expecting. I want my daughter to know she can tell me when she's had a hard day, and I hope I can do the same with her.",
                "My daughter and I are both pregnant, and I find myself relieved that we can talk about things neither of us would usually bring up. If we're both awake worrying, at least we'll know who to call.",
            ),
            "sexualized": (
                "My daughter and I, both pregnant at the same time. That's a lot to sit with.",
                "My daughter and I, expecting at the same time. I'd give you the respectable version of how I feel about it, Professor, but I'd have trouble keeping a straight face.",
                "I keep catching myself grinning at the timing. Both of us pregnant at once. That would have sounded absurd even to me before it happened.",
            ),
            "dominate": (
                "It's simply a coincidence, Professor -- the two of us expecting at once. Nothing more than that.",
                "I appreciate you asking, Professor. With both of us expecting, I think it's best to give my daughter room to talk about her own pregnancy in her own time.",
                "Yes, Professor, I know how unusual it is. My daughter and I are both expecting, and for now I'm trying to take each day as it comes.",
            ),
            "transactional": (
                "It's odd, both of us pregnant under the same roof at once. It's a lot to manage.",
                "My daughter and I are both pregnant. I'm thinking about how to be available when she needs me and still make time for my own appointments.",
                "The two of us are expecting at the same time. I think we need a little room to decide what we want to share and what we'd rather keep to ourselves.",
            ),
        },
        ("mother", "relative_by_player"): {
            "compassionate": (
                "My daughter, carrying your child... I won't pretend that's easy to sit with, but I don't regret our families being tied together this way.",
                "I know my daughter's having your baby. More than anything, I want her to feel she has people around her she can count on.",
                "My daughter is carrying your child. I'm still taking it in, but I love her, and I want her to know she's welcome to come to me even on the hard days.",
            ),
            "sexualized": (
                "You got my daughter pregnant? As depraved as that is, I can't say the thought doesn't excite me.",
                "My daughter is having your baby. I thought I had a composed answer ready, Professor. Then you asked me straight out, and I found myself smiling.",
                "My daughter's carrying your child. You chose your words very carefully just now, Professor. I almost wish you hadn't.",
            ),
            "dominate": (
                "So my daughter is carrying your child, Professor. I suppose that is simply the way of things.",
                "Yes, Professor, I know my daughter is carrying your child. I'd like to hear from her how much she wants me to be involved before I make any assumptions.",
                "I have some worries about my daughter having your baby, Professor. I'd rather talk them through with her first. I hope you'll understand.",
            ),
            "transactional": (
                "I'm still adjusting to the idea of my daughter carrying your child. It's a lot for one family.",
                "My daughter is carrying your child. I need to know what she wants for herself before I decide how I feel about the rest of it.",
                "I know my daughter's having your baby. It's a conversation I want to have with her when we have time to sit down properly.",
            ),
        },
        ("mother", "relative_expecting"): {
            "compassionate": (
                "I know about my daughter. It's not the easiest thing to sit with, but I'm glad she isn't going through it alone.",
                "I'm glad my daughter has people she can talk to. I want her to know she can lean on me as much or as little as she needs.",
                "I'm still getting used to the news. I keep thinking about what would have helped me back then, and I hope I can offer my daughter some of that.",
            ),
            "sexualized": (
                "My daughter, pregnant? I really shouldn't find that as interesting as I do.",
                "My daughter is pregnant. I know I'm expected to be very solemn about it, but sometimes a little humor is exactly what gets us through a conversation like this.",
                "I still find myself smiling at how thoroughly my daughter's news caught me off guard. I thought I had a better poker face than that.",
            ),
            "dominate": (
                "Yes, I'm aware of my daughter's condition. It's a family matter, Professor, nothing you need concern yourself with.",
                "I know my daughter's expecting, Professor. I'd like to leave it to her to decide what she wants to tell people.",
                "Yes, I'm aware, Professor. I plan to listen to my daughter first and give her time to tell me what she needs.",
            ),
            "transactional": (
                "It's strange, knowing my daughter is pregnant. I'm still getting used to the idea.",
                "My daughter is expecting. It raises a lot of practical questions, but I think she deserves time to answer those for herself.",
                "I'm still taking in the news about my daughter. For now I'd like to keep our conversations about it in the family.",
            ),
        },
    }
