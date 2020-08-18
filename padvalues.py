atts = {
    -1: None,
    0: 'Fire',
    1: 'Water',
    2: 'Wood',
    3: 'Light',
    4: 'Dark',
    5: 'Heart',
    6: 'Jammer',
    7: 'Poison',
    8: 'Mortal Poison',  # Speculated.
    9: 'Bomb',
}



types = {
    -1: None,
    0: 'Evo Material',
    1: 'Balanced',
    2: 'Physical',
    3: 'Healer',
    4: 'Dragon',
    5: 'God',
    6: 'Attacker',
    7: 'Devil',
    8: 'Machine',
    
    12: 'Awaken Material',
    
    14: 'Enhance Material',
    15: 'Redeemable Material',
    #? Protected?
}

awakensDict = {
    # 0: None,  # No need.
    1: 'Enhanced HP',
    2: 'Enhanced Attack',
    3: 'Enhanced Heal',
    4: 'Reduced Fire Damage',
    5: 'Reduced Water Damage',
    6: 'Reduced Wood Damage',
    7: 'Reduced Light Damage',
    8: 'Reduced Dark Damage',
    9: 'Auto-Recover',
    10: 'Resistance-Bind',
    11: 'Resistance-Dark',
    12: 'Resistance-Jammers',
    13: 'Resistance-Poison',
    14: 'Enhanced Fire Orbs',
    15: 'Enhanced Water Orbs',
    16: 'Enhanced Wood Orbs',
    17: 'Enhanced Light Orbs',
    18: 'Enhanced Dark Orbs',
    19: 'Extended Move Time',
    20: 'Recover Bind',
    21: 'Skill Boost',
    22: 'Enhanced Fire Att.',
    23: 'Enhanced Water Att.',
    24: 'Enhanced Wood Att.',
    25: 'Enhanced Light Att.',
    26: 'Enhanced Dark Att.',
    27: 'Two-Pronged Attack',
    28: 'Resistance-Skill Bind',
    29: 'Enhanced Heart Orbs',
    30: 'Multi Boost',
    31: 'Dragon Killer',
    32: 'God Killer',
    33: 'Devil Killer',
    34: 'Machine Killer',
    35: 'Balanced Killer',
    36: 'Attacker Killer',
    37: 'Physical Killer',
    38: 'Healer Killer',
    # 39: 'Evo Material Killer',
    # 40: 'Awaken Material Killer',
    # 41: 'Enhance Material Killer',
    # 42: 'Redeemable Material Killer',
    39: 'Evo Killer',
    40: 'Awaken Killer',
    41: 'Enhance Killer',
    42: 'Redeemable Killer',
    43: 'Enhanced Combos',
    44: 'Guard Break',
    45: 'Bonus Attack',
    46: 'Enhanced Team HP',
    47: 'Enhanced Team Recovery',
    48: 'Damage Void Piercer',
    49: 'Awoken Assist',
    50: 'Super Bonus Attack',
    51: 'Skill Charge',
    52: 'Resistance-Bind+',
    53: 'Extended Move Time+',
    54: 'Resistance-Clouds',
    55: 'Resistance-Immobility',
    56: 'Skill Boost+',
    57: '80% or more HP Enhanced',
    58: '50% or less HP Enhanced',
    59: '[L] Heal Matching',
    60: '[L] Increased Attack',
    61: 'Super Enhanced Combos',
    62: 'Combo Orbs',
    63: 'Skill Voice',
    64: 'Dungeon Bonus',
    65: 'Reduced HP',
    66: 'Reduced Attack',
    67: 'Reduced Recovery',
    68: 'Resistance-Blind+',
    69: 'Resistance-Jammers+',
    70: 'Resistance-Poison+',
    71: 'Blessing of Jammers',
    72: 'Blessing of Poison Orbs',
}

# Ugh I didn't update this with new strings.
awakensList = """
None
Enhanced HP
Enhanced Attack
Enhanced Heal
Reduce Fire Damage
Reduce Water Damage
Reduce Wood Damage
Reduce Light Damage
Reduce Dark Damage
Auto-Recover
Resistance-Bind
Resistance-Dark
Resistance-Jammers
Resistance-Poison
Enhanced Fire Orbs
Enhanced Water Orbs
Enhanced Wood Orbs
Enhanced Light Orbs
Enhanced Dark Orbs
Extend Time
Recover Bind
Skill Boost
Enhanced Fire Att.
Enhanced Water Att.
Enhanced Wood Att.
Enhanced Light Att.
Enhanced Dark Att.
Two-Pronged Attack
Resistance-Skill Bind
Enhanced Heal Orbs
Multi Boost
Dragon Killer
God Killer
Devil Killer
Machine Killer
Balanced Killer
Attacker Killer
Physical Killer
Healer Killer
Evo Killer
Awaken Killer
Enhance Killer
Redeemable Killer
Enhanced Combos
Guard Break
Bonus Attack
Enhanced Team HP
Enhanced Team RCV
Damage Void Piercer
Awoken Assist
Super Bonus Attack
Skill Charge
Resistance-Bind+
Extended Move Time+
Resistance-Clouds
Resistance-Immobility
Skill Boost+
80% or more HP Enhanced
50% or less HP Enhanced
[L] Damage Reduction
[L] Increased Attack
""".strip().splitlines()

awskills = awkns = awakeningskills = awakenings = awokenskills = awakensDict


latents = [
    None,
    'Imp. HP',
    'Imp. ATK',
    'Imp. RCV',
    'Ext. Move Time',
    'Auto-Heal',
    'Fire Dmg. Red.',
    'Water Dmg. Red.',
    'Wood Dmg. Red.',
    'Light Dmg. Red.',
    'Dark Dmg. Red.',
    'Skill Delay Resist.',
]






latent_names_official = [
    None,
    'Improved HP',
    'Improved Attack',
    'Improved Healing',
    'Extended Move Time',
    'Auto-Heal',
    'Fire Damage Reduction',
    'Water Damage Reduction',
    'Wood Damage Reduction',
    'Light Damage Reduction',
    'Dark Damage Reduction',
    'Skill Delay Resistance',
    'All Stats Enhanced',  #12: first double-slot.
    None,  #13
    None,  #14
    None,  #15
    'Evo Killer',
    'Awaken Killer',
    'Enhance Killer',
    'Redeemable Killer',
    'God Killer',
    'Dragon Killer',
    'Devil Killer',
    'Machine Killer',
    'Balanced Killer',
    'Attacker Killer',
    'Physical Killer',
    'Healer Killer',
    'Improved HP+',
    'Improved ATK+',
    'Improved RCV+',  #30
    'Extended Move Time+', #31
]
latent_descs_official = [
    None,
    'Slightly improves HP',
    'Slightly improves ATK',
    'Slightly improves RCV',
    'Slightly extends time to move Orbs',
    'Recovers a little HP when matching Orbs\n(No effect when RCV is 0 or lower)',
    'Slightly reduces damage received\nfrom Fire Att. enemies',
    'Slightly reduces damage received\nfrom Water Att. enemies',
    'Slightly reduces damage received\nfrom Wood Att. enemies',
    'Slightly reduces damage received\nfrom Light Att. enemies',
    'Slightly reduces damage received\nfrom Dark Att. enemies',
    'Reduces skill delay by 1 turn for each\nAwoken Latent Skill added',
    'Increases all Stats',
    None,  #13
    None,  #14
    None,  #15
    'Increases ATK against Evo\nMaterial enemies',
    'Increases ATK against Awaken\nMaterial enemies',
    'Increases ATK against Enhance\nMaterial enemies',
    'Increases ATK against Redeemable\nMaterial enemies',
    'Increases ATK against God Types',
    'Increases ATK against Dragon Types',
    'Increases ATK against Devil Types',
    'Increases ATK against Machine Types',
    'Increases ATK against Balanced Types',
    'Increases ATK against Attacker Types',
    'Increases ATK against Physical Types',
    'Increases ATK against Healer Types',
    'Improves HP a little',
    'Improves ATK a little',
    'Improves RCV a little',
    'Extends time to move Orbs a little',
]



collabs = NotImplemented
'''Collab notes:

? Need to decide canonical names for the collabs?

- Collabs:
    0. <None>
    1. RO
    2. Taiko
    3. ECO
    4. (Plan and Brood)
    5. Gunma
    6. FFCD
            US only has the Chocobo (& Carbuncle & Knight) cards grouped.
    7. Famitsu (Necky)
            Japan has the Nekkis (235 485 1177 1508 2715).
    8. Punt (incl. Zell)
    9. Puzzdroid
    10. Shinra
    11. Kapybara
    12. Cathy. (Only has Cathy and her evo.)
    13. (Ukai Magoroku and its evo.)
    14. Eva.
    15. 7-11 Collab
        (not translated)
    16. Clash of Clans
    17. Groove Coaster.
    18. RO ACE.
    19. Dragon's Dogma Quest
    20. Takaoka
    21. Monster Hunter
    22. Batman
    23. Baskin Robbins
    24. Angry Birds.
    25. PAD Z
    26. HxH
    27. Hello Kitty.
    28. PAD BT
    29. BEAMS
    30. Dragon Ball
    31. Saint Seiya
            - US only has #2126.
                - Rest haven't been grouped.
    32. GungHo Collab (only #32 Spirit?)
    33. GungHo Collab (King's Gate?)
    34. GungHo Collab (unknown game)
    35. GungHo Collab (unknown game)
    36. Bikkuriman
    37. Angry Birds E-something
    38. DC
    39. Sangoku Tenka Trigger. (Mini 3K.)
    40. FotNS. (We didn't get 1703?)
    41. chibis (christmas?)
    42. {Diagoldos}
    43. {#1924 Magic Kaito Kid}
            US: Empty.
    44. more chibis (hera, plan, heroes, etc.)
    45. FF
    46. GitS
    47. Duel Masters
    48. Attack on Titan
    49. (#2426 Ninja Hattori)
    50. Shonen Sunday.
            US: Empty.
    51. Crows X Worst
    52. Bleach
    53. Superman vs Batman.
    54. PAD X
    55. Ace Attorney.
'''

# Crap. I mixed up res codes and error codes.
res_codes = {
    0: 'Okay',
    2: 'relogin',  # Need to log in again.
    8: 'dungeon not open',  # Expired.
}
# "Error Code: %d"
error_codes = {
    3: 'Unregistered',
        #= https://www.reddit.com/r/PuzzleAndDragons/comments/4siy66/questionjp_looking_for_someone_that_speaks/d59ntvt
    
    12: 'That person has too many friends.',
        # Also res:40
    
    25: 'Too many friend invites.',
        # This user has reached their max
        # number of Friends. They cannot
        # register any more Friends.
    40: 'Cannot enter dungeon due to corrupted data',
        # HT: 'ゲームデータに不整合が発生したため、\nダンジョンに潜入できません。\n\nタイトル画面に戻り、再度お試しください。'
        # Also res:40
    44: "No score to rank",
        # Seen in KO when trying to view Current Rank without a score.
        # /api.php?action=rregist&pid={PID}&sid={SID}&did=1169&t=0&g=1&r=1801&m=0&key={KEY}
    46: "Room creation failed.",
        # Seen when res=2.
        # Also seen as res=46 from action=mp_rmake_comp??

    48: 'room not found?',

    99: 'Maintenance',
    
    101: 'No connection',  # Could not detect an internet connection?
    
    104: "Can't connect to server?",
    
    108: "???",
    
    602: "Room not found.", # Entering a room after it's closed.
}

# Drop types.
drops = {
    0: '', #none
    9900: 'coins',
    9901: 'stones',
    9902: 'palpts',
    
    9911: 'dung', #gift dungeon?
    9912: 'monpts',
    
    9916: 'dungperm', #permanent dungeon
    9917: 'badge', #awoken badge
    
    9999: 'annc', #announcement again
}

badges = {
    
}

hexcolors = {
    #- Dungeon colors.
        #- Looks like this is what's used to color the dungeons?
    '#G#',       # Urgent G?
    '$00e0c6$',  # Bright Green.
        #- Score Attack
    '$47ae64$',  # Technical Green.
        #- Forbidden Tower
        #- CD Collab
        #- FF Collab
        #- FF Collab
        #- PAD Academy
        #- Ultimate Rushes
        #- Super Ultimate Dragon Rush
        #- Ancient Pair Dragons
        #- Star Dragons
        #- X Collab
        #- Other collabs and biweeklies
        #- Mythical Endless Corridors
        #- 
        #- 
    '$5677a9$',  # Conditional Blue.
        #- Alt techs from CoS to Talos's Abyss.
        #- Descended Challenge-No Continues
        #- More alt techs.
    '$b86028$',  # Normal Brown.
        #- First two floors of Punt.
        #- Breakers
        #- Lightless Devils' Nest
        #- Poring Tower
    '$be7fbc$',  # Roguelike Magenta.
    '$d3423e$',  # Annihilation Red.
        #- Machine Zeus/Hera
        #- Ult Arena
        #- Ult Descended Rush
        #- Radar dragons.
    '$ffeb66$',  # Tournament Yellow.
        #- Satan Tournament
        #- Yamatsumi Tournament
    #- Message colors.
        #- Needs to change color back after use.
    '^FFFF00^',
    '^FFFFFF^',
}

