from Fortuna import CumulativeWeightedChoice, FlexCat, dice, d


note = """
Typical treasure table from a massively popular roll playing game.

Dynamic Treasure Table
     1-50   1d4 Potion(s) of healing
    51-60   Spell scroll (cantrip) - one of several cantrips
    61-70   Potion of climbing
    71-90   Spell scroll (level 1) - one of several level 1 spells
    91-94   Spell scroll (level 2) - one of several level 2 spells
    95-98   Potion of greater healing
       99   Bag of holding
      100   Driftglobe
"""


random_spell = FlexCat({
    "cantrip": (
        "Acid Splash", "Blade Ward", "Chill Touch", "Dancing Lights", "Fire Bolt", "Friends", "Guidance",
        "Light", "Mage Hand", "Mending", "Message", "Minor Illusion", "Poison Spray", "Prestidigitation",
        "Ray of Frost", "Resistance", "Sacred Flame", "Shocking Grasp", "Spare the Dying", "Thaumaturgy",
        "True Strike", "Vicious Mockery",
    ),
    "level_1": (
        "Alarm", "Animal Friendship", "Bane", "Bless", "Burning Hands", "Charm Person", "Chromatic Orb",
        "Color Spray", "Command", "Comprehend Languages", "Create or Destroy Water", "Cure Wounds",
        "Detect Evil and Good", "Detect Magic", "Detect Poison and Disease", "Disguise Self",
        "Dissonant Whispers", "Expeditious Retreat", "Faerie Fire", "False Life", "Feather Fall",
        "Find Familiar", "Fog Cloud", "Grease", "Guiding Bolt", "Healing Word", "Heroism", "Identify",
        "Illusory Script", "Inflict Wounds", "Jump", "Longstrider", "Mage Armor", "Magic Missile",
        "Protection from Evil and Good", "Purify Food and Drink", "Ray of Sickness", "Sanctuary",
        "Shield", "Shield of Faith", "Silent Image", "Sleep", "Speak with Animals", "Tasha's Hideous Laughter",
        "Tenser's Floating Disk", "Thunderwave", "Unseen Servant", "Witch Bolt",
    ),
    "level_2": (
        "Aid", "Alter Self", "Animal Messenger", "Arcane Lock", "Augury", "Blindness/Deafness", "Blur",
        "Calm Emotions", "Cloud of Daggers", "Continual Flame", "Crown of Madness", "Darkness", "Darkvision",
        "Detect Thoughts", "Enhance Ability", "Enlarge/Reduce", "Enthrall", "Find Traps", "Flaming Sphere",
        "Gentle Repose", "Gust of Wind", "Heat Metal", "Hold Person", "Invisibility", "Knock",
        "Lesser Restoration", "Levitate", "Locate Animals or Plants", "Locate Object", "Magic Mouth",
        "Magic Weapon", "Melf's Acid Arrow", "Mirror Image", "Misty Step", "Nystul's Magic Aura",
        "Phantasmal Force", "Prayer of Healing", "Protection from Poison", "Ray of Enfeeblement",
        "Rope Trick", "Scorching Ray", "See Invisibility", "Shatter", "Silence", "Spider Climb",
        "Spiritual Weapon", "Suggestion", "Warding Bond", "Web", "Zone of Truth",
    ),
    # ToDo: spell levels 3-9
}, y_bias="front", x_bias="cycle")


treasure_table = CumulativeWeightedChoice((
    (50, lambda: f"{d(4)} Potion(s) of healing"),
    (60, lambda: f"Spell scroll (cantrip) {random_spell('cantrip')}"),
    (70, "Potion of climbing"),
    (90, lambda: f"Spell scroll (level 1) {random_spell('level_1')}"),
    (94, lambda: f"Spell scroll (level 2) {random_spell('level_2')}"),
    (98, "Potion of greater healing"),
    (99, "Bag of holding"),
    (100, "Driftglobe"),
))


if __name__ == "__main__":
    print(note)
    print(f"Random Spell: {random_spell()}")
    print(f"Random Spell List: {random_spell(n_samples=dice(2, 4))}")
    print(f"Random Treasure: {treasure_table()}")
    print(f"Random Treasure List: {treasure_table(n_samples=dice(2, 4))}")
