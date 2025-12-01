"""
Specific NPCs for Fantasy Quest
All non-player characters in the game world
"""

from src.entities.npc import QuestGiverNPC, MerchantNPC, HealerNPC, NPC, NPCRole


def create_game_npcs() -> dict:
    """
    Create all NPCs in the game

    Returns:
        Dictionary of npc_id: NPC objects
    """
    npcs = {}

    # ===== ELENA - Guild Receptionist (Quest Giver) =====
    elena = QuestGiverNPC(
        name="Elena",
        title="Guild Receptionist",
        description=(
            "I manage the Adventure Guild here in Millhaven. "
            "We coordinate efforts to protect the village from the monsters "
            "that have been emerging from the Dark Forest. "
            "If you're looking for work, I can help you get registered."
        )
    )

    # Elena's custom dialogue
    elena.add_dialogue("registration", {
        "display": "Register as an adventurer",
        "text": (
            "Elena: \"Wonderful! We always need brave souls willing to help.\n"
            "Let me get you registered in our system.\n"
            "The guild provides quests, tracks your progress, and ensures\n"
            "you're compensated for your efforts.\n\n"
            "Welcome to the Adventure Guild!\""
        ),
        "conditions": {"first_meeting_only": True}
    })

    elena.add_dialogue("monsters", {
        "display": "Ask about the monsters",
        "text": (
            "Elena: \"The situation has grown worse in recent weeks.\n"
            "Goblins, wolves, even orcs have been spotted near the village.\n"
            "Elder Marcus believes something is stirring them up,\n"
            "but we don't know what yet. We need adventurers like you\n"
            "to help us investigate and keep the villagers safe.\""
        )
    })

    elena.add_dialogue("advice", {
        "display": "Ask for advice",
        "text": (
            "Elena: \"Start with the basics - take on some goblin-hunting quests\n"
            "to build your skills and earn some coin. Visit Sarah at the shop\n"
            "for better equipment when you can afford it. And don't forget to\n"
            "rest at the tavern when you need healing. Stay safe out there!\""
        )
    })

    npcs["elena"] = elena

    # ===== SARAH - Shopkeeper (Merchant) =====
    sarah = MerchantNPC(
        name="Sarah",
        title="Shopkeeper",
        description=(
            "I run the general shop here in Millhaven. "
            "Been in my family for three generations! "
            "I sell weapons, armor, and potions to help keep our adventurers safe. "
            "I also buy items if you have anything to sell."
        )
    )

    # Sarah's shop inventory (item_id: base_price)
    sarah.set_inventory({
        "minor_potion": 15,
        "health_potion": 30,
        "greater_potion": 60,
        "iron_sword": 50,
        "iron_armor": 75,
    })

    # Sarah's custom dialogue
    sarah.add_dialogue("gossip", {
        "display": "Ask for local gossip",
        "text": (
            "Sarah: \"Oh, you want to hear the latest?\n"
            "Well, Garak at the tavern has been complaining about supply shortages.\n"
            "The merchant caravans are too afraid to travel through the forest!\n"
            "Elder Marcus has been meeting with Elena a lot lately - seems serious.\n"
            "And between you and me, I think young Tommy has a crush on Elena,\n"
            "but he's too shy to talk to her!\" *giggles*"
        )
    })

    sarah.add_dialogue("business", {
        "display": "Ask about business",
        "text": (
            "Sarah: \"Business has been... interesting.\n"
            "Lots of adventurers stocking up on potions and equipment.\n"
            "Good for sales, but it worries me. The more prepared they are,\n"
            "the more dangerous things must be getting out there.\n"
            "I do my best to keep everyone well-supplied!\""
        )
    })

    npcs["sarah"] = sarah

    # ===== GARAK - Tavern Keeper (Healer) =====
    garak = HealerNPC(
        name="Garak",
        title="Tavern Keeper",
        description=(
            "I run The Cozy Tavern. Been keeping this place for twenty years. "
            "I serve food, drink, and provide rooms for weary travelers. "
            "If you need to rest and recover, this is the place."
        ),
        heal_cost=20
    )

    # Garak's custom dialogue
    garak.add_dialogue("rumors", {
        "display": "Listen to rumors",
        "text": (
            "Garak: *leans in and lowers his voice*\n"
            "\"I've heard things from travelers passing through.\n"
            "They speak of unusual activity deep in the forest.\n"
            "Strange lights. Unnatural sounds. Some say there's an old ruin\n"
            "out there, and something has awakened within it.\n"
            "Could just be tavern talk, but... I'd be careful if I were you.\""
        )
    })

    garak.add_dialogue("village", {
        "display": "Ask about the village",
        "text": (
            "Garak: \"Millhaven's a good place. Quiet, usually.\n"
            "Folk here are honest and hardworking. We've had our share of troubles\n"
            "with monsters over the years, but we always pull through.\n"
            "The Adventure Guild has been a blessing - keeps us protected.\n"
            "Elder Marcus leads us well, and Elena runs a tight ship at the guild.\""
        )
    })

    garak.add_dialogue("forest", {
        "display": "Ask about the Dark Forest",
        "text": (
            "Garak: \"That forest has always been dangerous, but lately?\n"
            "It's gotten worse. Much worse. We used to hunt in the outer edges,\n"
            "gather herbs and mushrooms. Now? Nobody goes in unless they have to.\n"
            "The monsters are more aggressive, more organized somehow.\n"
            "Something's changed out there, and not for the better.\""
        )
    })

    npcs["garak"] = garak

    # ===== ELDER MARCUS - Village Leader (Quest Giver) =====
    marcus = QuestGiverNPC(
        name="Elder Marcus",
        title="Village Elder",
        description=(
            "I am the elder of Millhaven Village. "
            "I've lived here my entire life and seen many challenges come and go. "
            "These are dark times, but I have faith in our adventurers. "
            "I try to guide our community and keep everyone safe."
        )
    )

    # Marcus's custom dialogue
    marcus.add_dialogue("history", {
        "display": "Ask about village history",
        "text": (
            "Marcus: \"Millhaven was founded over a century ago by settlers\n"
            "seeking a peaceful life away from the big cities.\n"
            "The forest provided game, timber, and herbs. We thrived here.\n"
            "But the forest has always had its dangers - goblins, wolves, worse things.\n"
            "Thirty years ago, we established the Adventure Guild to protect ourselves.\n"
            "It's served us well, though these recent troubles test us greatly.\""
        )
    })

    marcus.add_dialogue("threat", {
        "display": "Ask about the current threat",
        "text": (
            "Marcus: \"I fear something ancient has stirred in the forest depths.\n"
            "The old stories speak of a dragon that once laired in the mountains\n"
            "beyond the forest. Could it be awakening?\n"
            "Or perhaps something else entirely has disturbed the natural order.\n"
            "Whatever it is, we must face it together, or Millhaven will fall.\""
        )
    })

    marcus.add_dialogue("blessing", {
        "display": "Request a blessing",
        "text": (
            "Marcus: *places a hand on your shoulder*\n"
            "\"May the light guide your path and steel your courage.\n"
            "Return safely to us, young hero. Millhaven needs you.\""
        )
    })

    npcs["marcus"] = marcus

    # ===== TOMMY - Blacksmith's Apprentice (Minor NPC) =====
    tommy = NPC(
        name="Tommy",
        title="Apprentice Smith",
        description=(
            "I'm learning the smithing trade from Master Brennan. "
            "Someday I hope to craft legendary weapons! "
            "For now, I mostly work the bellows and fix horseshoes."
        ),
        role=NPCRole.VILLAGER
    )

    tommy.add_dialogue("dream", {
        "display": "Ask about his dreams",
        "text": (
            "Tommy: *eyes light up*\n"
            "\"I want to be the greatest smith in the land!\n"
            "Imagine crafting a sword so fine that heroes would travel from afar to wield it!\n"
            "Master Brennan says I have potential, but I need to focus on the basics first.\n"
            "Oh, and... maybe work up the courage to talk to Elena one day.\""
        )
    })

    npcs["tommy"] = tommy

    return npcs


def assign_npcs_to_locations(npcs: dict, locations: dict):
    """
    Assign NPCs to their respective locations

    Args:
        npcs: Dictionary of NPC objects
        locations: Dictionary of Location objects
    """
    # Elena at the Guild
    if "elena" in npcs and "guild" in locations:
        locations["guild"].add_npc("elena", npcs["elena"])

    # Sarah at the Shop
    if "sarah" in npcs and "shop" in locations:
        locations["shop"].add_npc("sarah", npcs["sarah"])

    # Garak at the Tavern
    if "garak" in npcs and "tavern" in locations:
        locations["tavern"].add_npc("garak", npcs["garak"])

    # Marcus in the Village
    if "marcus" in npcs and "village" in locations:
        locations["village"].add_npc("marcus", npcs["marcus"])

    # Tommy in the Village (near the smithy)
    if "tommy" in npcs and "village" in locations:
        locations["village"].add_npc("tommy", npcs["tommy"])
