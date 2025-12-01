"""
Specific game locations for Fantasy Quest
All locations in the game world
"""

from src.world.location import Location


def create_game_locations() -> dict:
    """
    Create and connect all game locations

    Returns:
        Dictionary of location_id: Location objects
    """
    locations = {}

    # ===== MILLHAVEN VILLAGE (Hub) =====
    village = Location(
        name="Millhaven Village",
        description=(
            "A peaceful hamlet nestled at the edge of the Dark Forest.\n"
            "Thatched-roof cottages line the cobblestone paths, and smoke\n"
            "rises from chimneys. Villagers go about their daily business,\n"
            "though worry lingers in their eyes.\n\n"
            "The village square lies before you."
        ),
        location_type="village"
    )
    locations["village"] = village

    # ===== ADVENTURE GUILD =====
    guild = Location(
        name="Adventure Guild",
        description=(
            "The Adventure Guild stands as a sturdy stone building.\n"
            "Inside, the walls are covered with notices, maps, and trophies\n"
            "from past adventures. A large quest board dominates one wall.\n\n"
            "The air smells of parchment and determination."
        ),
        location_type="guild"
    )
    locations["guild"] = guild

    # ===== GENERAL SHOP =====
    shop = Location(
        name="General Shop",
        description=(
            "The shop is a cozy establishment filled with supplies.\n"
            "Shelves line the walls, stocked with potions, weapons, and armor.\n"
            "Sunlight streams through the windows, illuminating motes of dust.\n\n"
            "The shopkeeper stands behind a worn wooden counter."
        ),
        location_type="shop"
    )
    locations["shop"] = shop

    # ===== COZY TAVERN =====
    tavern = Location(
        name="The Cozy Tavern",
        description=(
            "Warm light and the smell of hearty stew greet you.\n"
            "Wooden tables and chairs are scattered about, and a fire\n"
            "crackles in the hearth. A few patrons sit quietly, nursing drinks.\n\n"
            "The tavern keeper polishes mugs behind the bar."
        ),
        location_type="tavern"
    )
    locations["tavern"] = tavern

    # ===== DARK FOREST =====
    forest = Location(
        name="Dark Forest",
        description=(
            "Ancient trees loom overhead, their branches blocking out the sun.\n"
            "Twisted roots snake across the forest floor, and strange sounds\n"
            "echo through the shadows. This is a dangerous place.\n\n"
            "You sense movement in the undergrowth..."
        ),
        location_type="combat"
    )
    locations["forest"] = forest

    # ===== VILLAGE INN (Rest Location) =====
    inn = Location(
        name="Village Inn",
        description=(
            "A modest inn with clean, simple rooms.\n"
            "The common room has a few tables and a small fireplace.\n"
            "Travelers and locals alike find rest here.\n\n"
            "A sign advertises rooms for the night."
        ),
        location_type="inn"
    )
    locations["inn"] = inn

    # ===== Connect locations =====
    # From Village to other locations
    village.add_connection("guild", guild)
    village.add_connection("shop", shop)
    village.add_connection("tavern", tavern)
    village.add_connection("inn", inn)
    village.add_connection("forest", forest)

    # Back to village from each location
    guild.add_connection("village", village)
    shop.add_connection("village", village)
    tavern.add_connection("village", village)
    inn.add_connection("village", village)
    forest.add_connection("village", village)

    return locations


def get_starting_location() -> str:
    """Get the ID of the starting location"""
    return "village"
