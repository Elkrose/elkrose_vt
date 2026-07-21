# VT MOD - FERTILITY ITEMS
# This file must load AFTER the core database is created but BEFORE StoreManager initializes

init -3 python:
    """This init level (-3) runs after:
       - VT mod's init -34 (Mother patching)
       - VT mod's init -14 (Girl patching)
       - Core game's init -4 (database_shop_items creation)
       
       But BEFORE StoreManager initializes (which happens around init 0)
    """
    
    # CORRECTED IMPORT - Corrupted Academy doesn't use "main_classes" directory
    try:
        # Try direct import (Corrupted Academy places Python files directly in game directory)
        from class_shop_item_ren import ConsumableItem, StoreItem
        renpy.log("VT MOD: Successfully imported ConsumableItem directly")
    except ImportError:
        try:
            # Alternative path that might work in some versions
            from game.class_shop_item_ren import ConsumableItem, StoreItem
            renpy.log("VT MOD: Successfully imported ConsumableItem from game directory")
        except ImportError:
            # Fallback - check if already available in renpy.store
            if hasattr(renpy.store, 'ConsumableItem'):
                ConsumableItem = renpy.store.ConsumableItem
                StoreItem = renpy.store.StoreItem
                renpy.log("VT MOD: Found ConsumableItem in renpy.store")
            else:
                renpy.log("VT MOD ERROR: Could not find ConsumableItem class anywhere!")
                # Don't return here - we'll let the actual error happen so it's visible
    
    # Check if database_shop_items exists before modifying it
    if "database_shop_items" in globals():
        # Make sure "misc" category exists
        if "misc" not in database_shop_items:
            database_shop_items["misc"] = {}
        
        # Add fertility pill
        if "fertility_pill" not in database_shop_items.get("gifts", {}):
            database_shop_items["gifts"]["fertility_pill"] = Gift(
                id="fertility_pill",
                name="FertiBOOST",
                icon="_mods/content/elkrose_vt/extra_images/fertilitypills.png",
                price=100,
                lewdness=5,
                accept_temporary_stat_changes={"fertility_boost": 7},
                accept_buff_duration=7,
                description="FertiBOOST! A 7-day fertility supplement that provides a reliable conception advantage.\nTake when pursuing pregnancy for optimal results.\n{color=#CCCCCC}Fertility:{/color} {color=#00FF00}++{/color}"
            )

        # Add prenatal vitamins
        if "prenatal_vitamins" not in database_shop_items.get("gifts", {}):
            database_shop_items["gifts"]["prenatal_vitamins"] = Gift(
                id="prenatal_vitamins",
                name="PregnaVITA",
                icon="_mods/content/elkrose_vt/extra_images/pregboosters.png",
                price=1000,
                lewdness=3,
                description="PregnaVITA! Essential nutrients for healthy fetal development and maternal wellness during pregnancy. Take daily for optimal results.\nPrenatal vitamins that accelerate pregnancy progression.\nSpeeds Pregnancy by 2 times\n{color=#CCCCCC}Pregnancy Speed:{/color} {color=#00FF00}+++++{/color}"
            )

        # Add Plan B pill
        if "planb_pill" not in database_shop_items.get("gifts", {}):
            database_shop_items["gifts"]["planb_pill"] = Gift(
                id="planb_pill",
                name="SafeDOCK",
                icon="_mods/content/elkrose_vt/extra_images/planb_pill.png",
                price=500,
                lewdness=3,
                accept_impacts={"planb_boost": 7},
                description="SafeDOCK! Closes the bay doors before a drunken sea man tries to dock.\nBlocks all conception attempts for a strict 7-day window.\n{color=#CCCCCC}Pregnancy Prevention:{/color} {color=#00FF00}++++{/color}"
            )

        # Add Emergency Contraceptive Pill
        if "emergency_pill" not in database_shop_items.get("gifts", {}):
            database_shop_items["gifts"]["emergency_pill"] = Gift(
                id="emergency_pill",
                name="DryDOCK",
                icon="_mods/content/elkrose_vt/extra_images/emergency_pill.png",
                price=1000,
                lewdness=3,
                accept_impacts={"emergency_pill": 14},
                description="DryDOCK! A thorough reset for when the bay gets occupied too soon.\nSafely clears early pregnancy within a 14-day window.\n{color=#CCCCCC}Pregnancy Reset:{/color} {color=#00FF00}++++{/color}"
            )

        # Add condoms
        if "condoms" not in database_shop_items.get("misc", {}):
            database_shop_items["misc"]["condoms"] = ConsumableItem(
                id="condoms",
                name="BasicShield Condoms",
                icon="_mods/content/elkrose_vt/extra_images/condom.png",
                price=20,
                item_type="misc",
                description="BasicShield! No-frills protection that gets the job done. Simple, reliable, and always in your wallet.\n Might break if you are too eager. \nComes with 10!\n{color=#CCCCCC}Pregnancy Prevention:{/color} {color=#00FF00}++{/color}",
                applied_buff={
                    "name": "Condom Inventory",
                    "stat_changes": {
                        "condom_type": "cheap",
                        "condom_cheap_count": 10
                    },
                    "duration_in_days": 0
                }
            )
        
        # Add premium condoms (never break)
        if "condoms_premium" not in database_shop_items.get("misc", {}):
            database_shop_items["misc"]["condoms_premium"] = ConsumableItem(
                id="condoms_premium",
                name="UltraProtect Condoms (10 pack)",
                icon="_mods/content/elkrose_vt/extra_images/condom_premium.png",
                price=50,
                item_type="misc",
                description="UltraProtect! Premium latex with feather-light comfort and enhanced sensation. Makes protection feel like pleasure.\nPremium condoms that never break. Comes in 10!\n{color=#CCCCCC}Pregnancy Prevention:{/color} {color=#00FF00}+++++{/color}",
                applied_buff={
                    "name": "Premium Condom Use",
                    "stat_changes": {
                        "condom_type": "premium",
                        "condom_premium_count": 10
                    },
                    "duration_in_days": 0
                }
            )

        renpy.log("VT MOD: Successfully added fertility items to shop database")
    else:
        renpy.log("VT MOD ERROR: database_shop_items not found! Could not add fertility items")


    

    def add_requirements(original, new_requirement):
        if not original or original.strip() == "True":
            return new_requirement
        else:
            return f"({original}) and {new_requirement}"

    def update_requirement_description(action, new_requirement):
        if not action.requirement_description or action.requirement_description.strip() == "":
            return f"Requires: {new_requirement}."
        else:
            # Remove trailing period if present
            desc = action.requirement_description.rstrip('.')
            return f"{desc}, {new_requirement}."

    # Check if database_sex_options exists before modifying it
    if "database_sex_options" in globals():
        # Process face category
        if "face" in database_sex_options:
            for i, action in enumerate(database_sex_options["face"]):
                if action.action_entry_name == "blowjob" or action.action_entry_name == "use_mouth":
                    # Regular oral sex: Just needs active condom if preferred
                    condom_requirement = "(not girl.wants_oral_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_oral_condom))"
                    
                    # *** CHECK: Only patch if our requirement is not already present ***
                    if condom_requirement not in action.requirements:
                        new_requirements = add_requirements(action.requirements, condom_requirement)
                        new_desc = update_requirement_description(action, "Condom if preferred for oral")
                        
                        database_sex_options["face"][i] = SexAction(
                            name=action.name,
                            display_name=action.display_name,
                            requirements=new_requirements,
                            requirement_description=new_desc,
                            action_label="sex_blowjob",
                            action_entry_name=action.action_entry_name,
                        )
                        renpy.log(f"VT MOD: Patched {action.action_entry_name} with condom requirements")
                
                elif action.action_entry_name == "facial" or action.action_entry_name == "creampie_mouth":
                    # Oral creampie: Allowed if:
                    # - Girl doesn't want condom, OR
                    # - Condom is being used (intact OR broken but unaware)
                    condom_requirement = "(not girl.wants_oral_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_oral_condom))"
                    
                    # *** CHECK: Only patch if our requirement is not already present ***
                    if condom_requirement not in action.requirements:
                        new_requirements = add_requirements(action.requirements, condom_requirement)
                        new_desc = update_requirement_description(action, "Condom in use (working or unaware of break)")
                        
                        database_sex_options["face"][i] = SexAction(
                            name=action.name,
                            display_name=action.display_name,
                            requirements=new_requirements,
                            requirement_description=new_desc,
                            action_label=action.name,
                            action_entry_name=action.action_entry_name,
                        )
                        renpy.log(f"VT MOD: Patched {action.action_entry_name} with correct creampie logic")
        
        # Process boobs category
        if "boobs" in database_sex_options:
            for i, action in enumerate(database_sex_options["boobs"]):
                if action.action_entry_name == "fuck_boobs":
                    # Cumshot on boobs: Allowed if:
                    # - Girl doesn't want condom, OR
                    # - Condom is being used (intact OR broken but unaware)
                    condom_requirement = "(not girl.wants_body_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_boob_condom))"
                    
                    # *** CHECK: Only patch if our requirement is not already present ***
                    if condom_requirement not in action.requirements:
                        new_requirements = add_requirements(action.requirements, condom_requirement)
                        new_desc = update_requirement_description(action, "Condom in use (working or unaware of break)")
                        
                        database_sex_options["boobs"][i] = SexAction(
                            name=action.name,
                            display_name=action.display_name,
                            requirements=new_requirements,
                            requirement_description=new_desc,
                            action_label=action.name,
                            action_entry_name=action.action_entry_name,
                        )
                        renpy.log(f"VT MOD: Patched {action.action_entry_name} with correct cumshot logic")
                    
                if action.action_entry_name == "cumshot_boobs":
                    # Cumshot on boobs: Allowed if:
                    # - Girl doesn't want condom, OR
                    # - Condom is being used (intact OR broken but unaware)
                    condom_requirement = "(not girl.wants_body_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_boob_condom))"
                    
                    # *** CHECK: Only patch if our requirement is not already present ***
                    if condom_requirement not in action.requirements:
                        new_requirements = add_requirements(action.requirements, condom_requirement)
                        new_desc = update_requirement_description(action, "Condom in use (working or unaware of break)")
                        
                        database_sex_options["boobs"][i] = SexAction(
                            name=action.name,
                            display_name=action.display_name,
                            requirements=new_requirements,
                            requirement_description=new_desc,
                            action_label=action.name,
                            action_entry_name=action.action_entry_name,
                        )
                        renpy.log(f"VT MOD: Patched {action.action_entry_name} with correct cumshot logic")
        
        # Process pussy category
        if "pussy" in database_sex_options:
            for i, action in enumerate(database_sex_options["pussy"]):
                if action.action_entry_name == "fuck_pussy":
                    # Regular vaginal sex: Just needs active condom if preferred
                    condom_requirement = "(not girl.wants_vaginal_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_vaginal_condom))"
                    
                    # *** CHECK: Only patch if our requirement is not already present ***
                    if condom_requirement not in action.requirements:
                        new_requirements = add_requirements(action.requirements, condom_requirement)
                        new_desc = update_requirement_description(action, "Condom if preferred for vaginal")
                        
                        database_sex_options["pussy"][i] = SexAction(
                            name=action.name,
                            display_name=action.display_name,
                            requirements=new_requirements,
                            requirement_description=new_desc,
                            action_label=action.name,
                            action_entry_name=action.action_entry_name,
                        )
                        renpy.log(f"VT MOD: Patched {action.action_entry_name} with condom requirements")
                
                elif action.action_entry_name == "cumshot_pussy" or action.action_entry_name == "creampie_pussy":
                    # Vaginal creampie: Allowed if:
                    # - Girl doesn't want condom, OR
                    # - Condom is being used (intact OR broken but unaware)
                    condom_requirement = "(not girl.wants_vaginal_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_vaginal_condom))"
                    
                    # *** CHECK: Only patch if our requirement is not already present ***
                    if condom_requirement not in action.requirements:
                        new_requirements = add_requirements(action.requirements, condom_requirement)
                        new_desc = update_requirement_description(action, "Condom in use (working or unaware of break)")
                        
                        database_sex_options["pussy"][i] = SexAction(
                            name=action.name,
                            display_name=action.display_name,
                            requirements=new_requirements,
                            requirement_description=new_desc,
                            action_label=action.name,
                            action_entry_name=action.action_entry_name,
                        )
                        renpy.log(f"VT MOD: Patched {action.action_entry_name} with correct creampie logic")
        
        # Process ass category
        if "ass" in database_sex_options:
            for i, action in enumerate(database_sex_options["ass"]):
                if action.action_entry_name == "fuck_ass":
                    # Regular anal sex: Just needs active condom if preferred
                    condom_requirement = "(not girl.wants_anal_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_anal_condom))"
                    
                    # *** CHECK: Only patch if our requirement is not already present ***
                    if condom_requirement not in action.requirements:
                        new_requirements = add_requirements(action.requirements, condom_requirement)
                        new_desc = update_requirement_description(action, "Condom if preferred for anal")
                        
                        database_sex_options["ass"][i] = SexAction(
                            name=action.name,
                            display_name=action.display_name,
                            requirements=new_requirements,
                            requirement_description=new_desc,
                            action_label=action.name,
                            action_entry_name=action.action_entry_name,
                        )
                        renpy.log(f"VT MOD: Patched {action.action_entry_name} with condom requirements")
                
                elif action.action_entry_name == "creampie_ass":
                    # Anal creampie: Allowed if:
                    # - Girl doesn't want condom, OR
                    # - Condom is being used (intact OR broken but unaware)
                    condom_requirement = "(not girl.wants_anal_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_anal_condom))"
                    
                    # *** CHECK: Only patch if our requirement is not already present ***
                    if condom_requirement not in action.requirements:
                        new_requirements = add_requirements(action.requirements, condom_requirement)
                        new_desc = update_requirement_description(action, "Condom in use (working or unaware of break)")
                        
                        database_sex_options["ass"][i] = SexAction(
                            name=action.name,
                            display_name=action.display_name,
                            requirements=new_requirements,
                            requirement_description=new_desc,
                            action_label=action.name,
                            action_entry_name=action.action_entry_name,
                        )
                        renpy.log(f"VT MOD: Patched {action.action_entry_name} with correct creampie logic")
        
        # Process legs category
        if "legs" in database_sex_options:
            for i, action in enumerate(database_sex_options["legs"]):
                if action.action_entry_name == "cumshot_thighs":
                    # Cumshot on thighs: Allowed if:
                    # - Girl doesn't want condom, OR
                    # - Condom is being used (intact OR broken but unaware)
                    condom_requirement = "(not girl.wants_body_condom) or (player.condom_active != 'raw' and (not player.condom_broke or not girl.aware_thigh_condom))"
                    
                    # *** CHECK: Only patch if our requirement is not already present ***
                    if condom_requirement not in action.requirements:
                        new_requirements = add_requirements(action.requirements, condom_requirement)
                        new_desc = update_requirement_description(action, "Condom in use (working or unaware of break)")
                        
                        database_sex_options["legs"][i] = SexAction(
                            name=action.name,
                            display_name=action.display_name,
                            requirements=new_requirements,
                            requirement_description=new_desc,
                            action_label=action.name,
                            action_entry_name=action.action_entry_name,
                        )
                        renpy.log(f"VT MOD: Patched {action.action_entry_name} with correct cumshot logic")
        
        renpy.log("VT MOD: Successfully checked and patched necessary sex actions")
    else:
        renpy.log("VT MOD ERROR: database_sex_options not found! Could not patch sex actions")


    # CORRECTED: Patch the consume_item method instead of redefining the whole class
    if "Gift" in globals():
        # *** CHECK: Only patch if it hasn't been patched before ***
        # We check for a special attribute we add to the function after patching.
        if not hasattr(Gift.give_gift, 'vt_patched'):
            # Save the original method
            original_give_gift = Gift.give_gift
            
            def vt_give_gift(self, girl, apply_impacts=True):
                # VT gift pills are "ammo": they live as a sidecar count, never as Gift objects
                # in anyone's inventory. So for our pills, apply the impacts directly (skipping
                # the base flow's player.remove_item / girl.add_item, which would stash the Gift
                # on the girl). Non-VT gifts fall through to the original behavior unchanged.
                is_vt_pill = self.id in ("fertility_pill", "prenatal_vitamins", "planb_pill", "emergency_pill")

                if is_vt_pill:
                    if apply_impacts:
                        self.apply_gift_impacts(girl, accepted_gift=True)
                else:
                    original_give_gift(self, girl, apply_impacts)

                # Now handle our special VT items
                if self.id == "fertility_pill":
                    # If she AND the player both know she's pregnant, FertiBOOST is pointless and
                    # isn't offered (excluded in vt_get_items_and_quantity). Guard here too so a
                    # stray call can't apply the boost or burn a pill.
                    if girl.pregnant and getattr(girl, "knows_pregnant", False) and getattr(girl, "player_knows_pregnant", False):
                        vt_preg_notify(f"{girl.first_name} laughs softly - you both know she's already expecting.", duration=3.0)
                        return
                    # Boost only matters before conception; an already-pregnant girl still "takes"
                    # it (and the reaction reflects her secret/obliviousness) but gains nothing.
                    if not girl.pregnant:
                        girl.fertility_boost += 7  # 7 day of fertility boost
                    renpy.log(f"{girl.first_name} was given FertiBOOST!!")
                    vt_preg_notify(vt_pill_reaction(girl, "fertility_pill"), duration=3.5)

                elif self.id == "prenatal_vitamins":
                    # Always goes into her PregnaVITA supply when accepted; she only *takes* one
                    # (on the weekly tick) once she's pregnant and knows it -- apply_prenatal_boost
                    # gates the actual dose -- so a non-pregnant girl/mother just holds onto it.
                    girl.prenatal_boost = getattr(girl, "prenatal_boost", 0) + 1
                    vt_preg_notify(vt_pill_reaction(girl, "prenatal_vitamins"), duration=3.5)

                if self.id == "planb_pill":
                    # Apply planb boost to the girl
                    girl.apply_planb_pill()
                    girl.planb_pills += 1  # 7 day of protection from pregnancy
                    renpy.log(f"{girl.first_name} was given SafeDOCK!")
                    vt_preg_notify(f"{girl.first_name} was given SafeDOCK!", duration=3.0)

                if self.id == "emergency_pill":
                    # Apply fertility boost to the girl
                    girl.apply_emergency_pill()
                    girl.emergency_pill += 1  # 14 day of fertility boost
                    renpy.log(f"{girl.first_name} was given a DryDOCK!")
                    vt_preg_notify(f"{girl.first_name} was given a DryDOCK!", duration=3.0)

                # Spend one unit of pill "ammo" now that the gift has been applied.
                if is_vt_pill:
                    try:
                        counts = vt_player_pill_counts(player)
                        if counts.get(self.id, 0) > 0:
                            counts[self.id] -= 1
                    except Exception:
                        pass

                # Condoms aren't gifts -- they're auto-converted to counts at purchase and
                # spent from the cherry HUD, so they're not handled here.

            # Replace the method
            Gift.give_gift = vt_give_gift
            
            # *** FLAG: Mark the method as patched so we don't patch it again ***
            Gift.give_gift.vt_patched = True
            
            renpy.log("VT MOD: Successfully patched Gift.give_gift method.")
        else:
            renpy.log("VT MOD: Gift.give_gift method already patched. Skipping.")
    else:
        renpy.log("VT MOD ERROR: Gift class not found! Could not patch give_gift method")
            

    # CORRECTED: Patch the consume_item method instead of redefining the whole class
    if "ConsumableItem" in globals():
        # *** CHECK: Only patch if it hasn't been patched before ***
        if not hasattr(ConsumableItem.consume_item, 'vt_patched'):
            # Save the original method
            original_consume_item = ConsumableItem.consume_item
            
            # Define our custom version
            def vt_consume_item(self) -> None:
                player.remove_item(self)
                
                if self.applied_buff:
                    # Special handling for our custom items
                    stat_changes = self.applied_buff["stat_changes"]

                    if "condom_type" in stat_changes:
                        # Apply condom
                        condom_type = stat_changes["condom_type"]
                        # Determine quantity
                        condom_quantity = 1
                        if condom_type == "cheap":
                            condom_quantity = stat_changes.get("condom_cheap_count", 1)
                        elif condom_type == "premium":
                            condom_quantity = stat_changes.get("condom_premium_count", 1)
                        
                        # CORRECT: ONLY update inventory counts (DO NOT set condom_active)
                        condom_name = "BasicShield" if condom_type == "cheap" else "UltraProtect"
                        condom_word = "condom" if condom_quantity == 1 else "condoms"
                        if condom_type == "cheap":
                            player.condom_cheap_count += condom_quantity
                        elif condom_type == "premium":
                            player.condom_premium_count += condom_quantity
                        # Show notification with proper pluralization
                        
                        queue_notification(f"{condom_quantity} {condom_name} {condom_word} added to inventory!", duration= 3.0)
                    
                        # CRITICAL: Force UI refresh after inventory change
                        renpy.restart_interaction()
                    else:
                        # Default buff handling
                        player.apply_temporary_stat_change(
                            buff_name=self.applied_buff["name"],
                            impacts=stat_changes,
                            duration_in_days=self.applied_buff["duration_in_days"],
                        )
            
            # Replace the method
            ConsumableItem.consume_item = vt_consume_item
            
            # *** FLAG: Mark the method as patched so we don't patch it again ***
            ConsumableItem.consume_item.vt_patched = True
            
            renpy.log("VT MOD: Successfully patched ConsumableItem.consume_item method.")
        else:
            renpy.log("VT MOD: ConsumableItem.consume_item method already patched. Skipping.")
    else:
        renpy.log("VT MOD ERROR: ConsumableItem class not found! Could not patch consume_item method")

    ## Check if database_fullbody_image_tags exists before modifying it
    pregnancy_tag_overrides = {
        # --- Third Trimester (Most Specific) ---
        "preg_3rd_shower": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.id == girls_in_locker_room[2]",
        "preg_3rd_bare": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.is_nude()",
        "preg_3rd_swimsuit": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_swimsuit(girl)",
        "preg_3rd_bikini": "getattr(girl, 'pregnancy_phase', 0) == 3 and (is_wearing_bikini(girl) or is_wearing_swimsuit(girl))",
        "preg_3rd_underwear": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.is_in_underwear()",
        "preg_3rd_bottomless": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.is_bottomless()",
        "preg_3rd_topless": "getattr(girl, 'pregnancy_phase', 0) == 3 and girl.is_topless()",
        "preg_3rd_maid": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_maid_outfit(girl)",
        "preg_3rd_nurse": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_nurse_outfit(girl)",
        "preg_3rd_secretary": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_working_as_secretary(girl)",
        "preg_3rd_teacher": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_working_as_teacher(girl)",
        "preg_3rd_teaching_assistant": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_working_as_teaching_assistant(girl)",
        "preg_3rd_uniform": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_uniform(girl)",
        "preg_3rd_athletic": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_athletic_outfit(girl)",
        "preg_3rd_work": "getattr(girl, 'pregnancy_phase', 0) == 3 and is_wearing_work_outfit(girl)",
        "preg_3rd_clothed": "getattr(girl, 'pregnancy_phase', 0) == 3 and not girl.is_in_underwear() and not girl.is_nude()",
        # --- Second Trimester ---
        "preg_2nd_shower": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.id == girls_in_locker_room[2]",
        "preg_2nd_bare": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.is_nude()",
        "preg_2nd_swimsuit": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_swimsuit(girl)",
        "preg_2nd_bikini": "getattr(girl, 'pregnancy_phase', 0) == 2 and (is_wearing_bikini(girl) or is_wearing_swimsuit(girl))",
        "preg_2nd_underwear": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.is_in_underwear()",
        "preg_2nd_bottomless": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.is_bottomless()",
        "preg_2nd_topless": "getattr(girl, 'pregnancy_phase', 0) == 2 and girl.is_topless()",
        "preg_2nd_maid": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_maid_outfit(girl)",
        "preg_2nd_nurse": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_nurse_outfit(girl)",
        "preg_2nd_secretary": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_working_as_secretary(girl)",
        "preg_2nd_teacher": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_working_as_teacher(girl)",
        "preg_2nd_teaching_assistant": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_working_as_teaching_assistant(girl)",
        "preg_2nd_uniform": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_uniform(girl)",
        "preg_2nd_athletic": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_athletic_outfit(girl)",
        "preg_2nd_work": "getattr(girl, 'pregnancy_phase', 0) == 2 and is_wearing_work_outfit(girl)",
        "preg_2nd_clothed": "getattr(girl, 'pregnancy_phase', 0) == 2 and not girl.is_in_underwear() and not girl.is_nude()",
        # --- First Trimester ---
        "preg_1st_shower": "getattr(girl, 'pregnancy_phase', 0) == 1 and girl.id == girls_in_locker_room[2]",
        "preg_1st_bare": "getattr(girl, 'pregnancy_phase', 0) == 1 and girl.is_nude()",
        "preg_1st_swimsuit": "getattr(girl, 'pregnancy_phase', 0) == 1 and is_wearing_swimsuit(girl)",
        "preg_1st_bikini": "getattr(girl, 'pregnancy_phase', 0) == 1 and (is_wearing_bikini(girl) or is_wearing_swimsuit(girl))",
        "preg_1st_underwear": "getattr(girl, 'pregnancy_phase', 0) == 1 and girl.is_in_underwear()",
        "preg_1st_bottomless": "getattr(girl, 'pregnancy_phase', 0) == 1 and girl.is_bottomless()",
        "preg_1st_topless": "getattr(girl, 'pregnancy_phase', 0) == 1 and girl.is_topless()",
        "preg_1st_maid": "getattr(girl, 'pregnancy_phase', 0) == 1 and is_wearing_maid_outfit(girl)",
        "preg_1st_nurse": "getattr(girl, 'pregnancy_phase', 0) == 1 and is_wearing_nurse_outfit(girl)",
        "preg_1st_secretary": "getattr(girl, 'pregnancy_phase', 0) == 1 and is_working_as_secretary(girl)",
        "preg_1st_teacher": "getattr(girl, 'pregnancy_phase', 0) == 1 and is_working_as_teacher(girl)",
        "preg_1st_teaching_assistant": "getattr(girl, 'pregnancy_phase', 0) == 1 and is_working_as_teaching_assistant(girl)",
        "preg_1st_uniform": "getattr(girl, 'pregnancy_phase', 0) == 1 and is_wearing_uniform(girl)",
        "preg_1st_athletic": "getattr(girl, 'pregnancy_phase', 0) == 1 and is_wearing_athletic_outfit(girl)",
        "preg_1st_work": "getattr(girl, 'pregnancy_phase', 0) == 1 and is_wearing_work_outfit(girl)",
        "preg_1st_clothed": "getattr(girl, 'pregnancy_phase', 0) == 1 and not girl.is_in_underwear() and not girl.is_nude()",
        # --- General Pregnancy (Fallback for any visible pregnancy) ---
        "preg_shower": "is_visibly_pregnant(girl) and girl.id == girls_in_locker_room[2]",
        "preg_bare": "is_visibly_pregnant(girl) and girl.is_nude()",
        "preg_swimsuit": "is_visibly_pregnant(girl) and is_wearing_swimsuit(girl)",
        "preg_bikini": "is_visibly_pregnant(girl) and (is_wearing_bikini(girl) or is_wearing_swimsuit(girl))",
        "preg_underwear": "is_visibly_pregnant(girl) and girl.is_in_underwear()",
        "preg_bottomless": "is_visibly_pregnant(girl) and girl.is_bottomless()",
        "preg_topless": "is_visibly_pregnant(girl) and girl.is_topless()",
        "preg_maid": "is_visibly_pregnant(girl) and is_wearing_maid_outfit(girl)",
        "preg_nurse": "is_visibly_pregnant(girl) and is_wearing_nurse_outfit(girl)",
        "preg_secretary": "is_visibly_pregnant(girl) and is_working_as_secretary(girl)",
        "preg_teacher": "is_visibly_pregnant(girl) and is_working_as_teacher(girl)",
        "preg_teaching_assistant": "is_visibly_pregnant(girl) and is_working_as_teaching_assistant(girl)",
        "preg_uniform": "is_visibly_pregnant(girl) and is_wearing_uniform(girl)",
        "preg_athletic": "is_visibly_pregnant(girl) and is_wearing_athletic_outfit(girl)",
        "preg_work": "is_visibly_pregnant(girl) and is_wearing_work_outfit(girl)",
        "preg_clothed": "is_visibly_pregnant(girl) and not girl.is_in_underwear() and not girl.is_nude()",
    }
    
    if "database_fullbody_image_tags" in globals():
        original_database = database_fullbody_image_tags
        
        marker_tag = "preg_3rd_shower"
        # Check if the marker tag is already a key in the dictionary
        if marker_tag not in database_fullbody_image_tags:
            # The marker is not found, so it's safe to add our entire block
            
            # 1. Add all your new key-value pairs to the existing dictionary
            database_fullbody_image_tags.update(pregnancy_tag_overrides)
            
            # 2. To get them at the "top", we must rebuild the dictionary.
            #    Create a new ordered dictionary with your items first.
            from collections import OrderedDict
            new_ordered_db = OrderedDict()
            
            # 3. Add your items first
            for tag in pregnancy_tag_overrides:
                new_ordered_db[tag] = database_fullbody_image_tags[tag]
                
            # 4. Add all the original items (that aren't yours) after them
            for tag, condition in database_fullbody_image_tags.items():
                if tag not in pregnancy_tag_overrides:
                    new_ordered_db[tag] = condition
            
            # 5. Replace the old database with the new, correctly ordered one.
            database_fullbody_image_tags.clear()
            database_fullbody_image_tags.update(new_ordered_db)
            
            renpy.log("VT MOD: Successfully prepended pregnancy overrides to database.")
        else:
            # The marker was found, so we do nothing to avoid duplicates
            renpy.log("VT MOD: Pregnancy overrides already found. Skipping addition.")
    else:
        renpy.log("VT MOD ERROR: database_fullbody_image_tags not found! Could not add pregnancy overrides")


# ADD THIS AFTER THE CONSUMABLEITEM PATCH
#
# Condom selector. Modal screen shown in the current context. Was a
# `label vt_select_condom` menu opened via ShowMenu; because the target was a
# label it routed through the game menu (suppress_overlay on) with no modal
# backdrop, leaving location buttons live under the picker -- clicking one
# jumped away mid-menu and orphaned the screen. Selection logic below is a
# verbatim port of the old menu branches.
init python:
    def vt_equip_cheap_condom():
        player.condom_cheap_count -= 1
        player.condom_active = "cheap"
        player.condom_cum = 0
        player.condom_dirty = False
        player.condom_broke = False
        queue_notification("Equipped BasicShield condom", duration=2.0)
        renpy.log(f"VT MOD: Consumed 1 cheap condom. Remaining: {player.condom_cheap_count}")

        # If we ran out of condoms, automatically switch to raw
        if player.condom_cheap_count <= 0 and player.condom_active == "cheap":
            player.condom_active = "raw"
            queue_notification("Out of BasicShield condoms!", duration=3.0)

    def vt_equip_premium_condom():
        player.condom_premium_count -= 1
        player.condom_active = "premium"
        player.condom_cum = 0
        player.condom_dirty = False
        player.condom_broke = False
        queue_notification("Equipped UltraProtect condom", duration=2.0)
        renpy.log(f"VT MOD: Consumed 1 premium condom. Remaining: {player.condom_premium_count}")

        # If we ran out of condoms, automatically switch to raw
        if player.condom_premium_count <= 0 and player.condom_active == "premium":
            player.condom_active = "raw"
            queue_notification("Out of UltraProtect condoms!", duration=3.0)

    def vt_go_bareback():
        player.condom_active = "raw"
        player.condom_cum = 0
        player.condom_dirty = False
        player.condom_broke = False
        queue_notification("Removed condom - going bareback", duration=2.0)

    def vt_clean_up_condom():
        player.condom_cum = 0
        player.condom_dirty = False
        player.condom_broke = False
        player.condom_active = "raw"
        queue_notification("Cleaned up", duration=2.0)
        renpy.log("VT MOD: Cleaned up after creampie")

screen vt_select_condom():
    modal True
    zorder 200
    style_prefix "choice"

    # Left, vertically centered -- matches the base choice menu. modal True
    # blocks the map underneath; no dimming overlay needed.
    frame:
        xpos 10
        yalign 0.5
        background None

        vbox:
            spacing 5
            xalign 0.0

            if player.condom_cheap_count > 0:
                textbutton "Use BasicShield condom ([player.condom_cheap_count])":
                    action [Function(vt_equip_cheap_condom), Hide("vt_select_condom")]

            if player.condom_premium_count > 0:
                textbutton "Use UltraProtect condom ([player.condom_premium_count])":
                    action [Function(vt_equip_premium_condom), Hide("vt_select_condom")]

            textbutton "Go bareback (no protection)":
                action [Function(vt_go_bareback), Hide("vt_select_condom")]

            if player.condom_dirty or player.condom_active == "raw":
                textbutton "Clean up (wash your berries/Remove condom)":
                    action [Function(vt_clean_up_condom), Hide("vt_select_condom")]

            textbutton "Close Condom Selection":
                action Hide("vt_select_condom")