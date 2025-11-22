"""
Item system for Fantasy Quest
Defines various item types: weapons, armor, consumables
"""


class Item:
    """Base item class"""
    
    def __init__(self, name: str, description: str, value: int):
        """
        Initialize an item
        
        Args:
            name: Item name
            description: Item description
            value: Gold value of the item
        """
        self.name = name
        self.description = description
        self.value = value
    
    def __str__(self) -> str:
        return f"{self.name} - {self.description}"


class Weapon(Item):
    """Weapon item that increases attack power"""
    
    def __init__(self, name: str, description: str, value: int, attack_bonus: int):
        """
        Initialize a weapon
        
        Args:
            name: Weapon name
            description: Weapon description
            value: Gold value
            attack_bonus: Attack power bonus
        """
        super().__init__(name, description, value)
        self.attack_bonus = attack_bonus
        self.item_type = "weapon"
    
    def __str__(self) -> str:
        return f"{self.name} (+{self.attack_bonus} ATK) - {self.description}"


class Armor(Item):
    """Armor item that increases defense"""
    
    def __init__(self, name: str, description: str, value: int, defense_bonus: int):
        """
        Initialize armor
        
        Args:
            name: Armor name
            description: Armor description
            value: Gold value
            defense_bonus: Defense bonus
        """
        super().__init__(name, description, value)
        self.defense_bonus = defense_bonus
        self.item_type = "armor"
    
    def __str__(self) -> str:
        return f"{self.name} (+{self.defense_bonus} DEF) - {self.description}"


class Potion(Item):
    """Consumable potion that restores health"""
    
    def __init__(self, name: str, description: str, value: int, heal_amount: int):
        """
        Initialize a potion
        
        Args:
            name: Potion name
            description: Potion description
            value: Gold value
            heal_amount: HP restored when used
        """
        super().__init__(name, description, value)
        self.heal_amount = heal_amount
        self.item_type = "potion"
        self.consumable = True
    
    def use(self, character) -> str:
        """
        Use the potion on a character
        
        Args:
            character: Character to heal
            
        Returns:
            Message describing the effect
        """
        healed = character.heal(self.heal_amount)
        return f"{character.name} used {self.name} and restored {healed} HP!"
    
    def __str__(self) -> str:
        return f"{self.name} (Heals {self.heal_amount} HP) - {self.description}"


# Predefined items
ITEMS_DATABASE = {
    # Weapons
    "rusty_sword": Weapon("Rusty Sword", "An old, weathered blade", 20, 5),
    "iron_sword": Weapon("Iron Sword", "A sturdy iron blade", 50, 10),
    "steel_sword": Weapon("Steel Sword", "A well-crafted steel sword", 100, 15),
    "legendary_blade": Weapon("Legendary Blade", "A sword of ancient power", 500, 30),
    
    # Armor
    "leather_armor": Armor("Leather Armor", "Basic leather protection", 30, 5),
    "iron_armor": Armor("Iron Armor", "Heavy iron plating", 75, 10),
    "steel_armor": Armor("Steel Armor", "Reinforced steel armor", 150, 15),
    "dragon_armor": Armor("Dragon Armor", "Armor forged from dragon scales", 600, 35),
    
    # Potions
    "minor_potion": Potion("Minor Health Potion", "Restores a small amount of HP", 15, 30),
    "health_potion": Potion("Health Potion", "Restores moderate HP", 30, 50),
    "greater_potion": Potion("Greater Health Potion", "Restores significant HP", 60, 100),
    "mega_potion": Potion("Mega Health Potion", "Fully restores HP", 120, 999),
}


def get_item(item_key: str) -> Item:
    """
    Retrieve an item from the database
    
    Args:
        item_key: Item identifier
        
    Returns:
        Item instance
    """
    return ITEMS_DATABASE.get(item_key)
