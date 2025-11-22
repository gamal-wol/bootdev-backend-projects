"""
Enemy system for Fantasy Quest
Defines various enemy types with different stats and loot
"""

import random
from src.core.character import Character


class Enemy(Character):
    """Enemy character with loot drops"""
    
    def __init__(self, name: str, health: int, attack: int, defense: int, 
                 xp_reward: int, gold_reward: int, loot_table: list = None):
        """
        Initialize an enemy
        
        Args:
            name: Enemy name
            health: HP value
            attack: Attack power
            defense: Defense value
            xp_reward: XP given when defeated
            gold_reward: Gold dropped when defeated
            loot_table: List of (item_key, drop_chance) tuples
        """
        super().__init__(name, health, attack, defense)
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.loot_table = loot_table or []
    
    def get_loot(self) -> list:
        """
        Determine what items the enemy drops
        
        Returns:
            List of item keys that dropped
        """
        drops = []
        for item_key, chance in self.loot_table:
            if random.random() < chance:
                drops.append(item_key)
        return drops


# Enemy templates
ENEMY_TYPES = {
    "goblin": {
        "name": "Goblin",
        "health": 30,
        "attack": 5,
        "defense": 2,
        "xp_reward": 20,
        "gold_reward": 10,
        "loot_table": [("minor_potion", 0.3)]
    },
    "orc": {
        "name": "Orc Warrior",
        "health": 60,
        "attack": 12,
        "defense": 5,
        "xp_reward": 40,
        "gold_reward": 25,
        "loot_table": [("health_potion", 0.4), ("iron_sword", 0.1)]
    },
    "troll": {
        "name": "Cave Troll",
        "health": 100,
        "attack": 18,
        "defense": 8,
        "xp_reward": 70,
        "gold_reward": 50,
        "loot_table": [("greater_potion", 0.5), ("iron_armor", 0.15)]
    },
    "dark_knight": {
        "name": "Dark Knight",
        "health": 150,
        "attack": 25,
        "defense": 15,
        "xp_reward": 120,
        "gold_reward": 100,
        "loot_table": [("steel_sword", 0.3), ("steel_armor", 0.2), ("greater_potion", 0.6)]
    },
    "dragon": {
        "name": "Ancient Dragon",
        "health": 300,
        "attack": 40,
        "defense": 25,
        "xp_reward": 500,
        "gold_reward": 500,
        "loot_table": [("legendary_blade", 0.5), ("dragon_armor", 0.5), ("mega_potion", 0.8)]
    },
    "slime": {
        "name": "Slime",
        "health": 20,
        "attack": 3,
        "defense": 1,
        "xp_reward": 10,
        "gold_reward": 5,
        "loot_table": [("minor_potion", 0.2)]
    },
    "skeleton": {
        "name": "Skeleton",
        "health": 40,
        "attack": 8,
        "defense": 3,
        "xp_reward": 25,
        "gold_reward": 15,
        "loot_table": [("rusty_sword", 0.15), ("minor_potion", 0.25)]
    },
    "vampire": {
        "name": "Vampire",
        "health": 120,
        "attack": 22,
        "defense": 10,
        "xp_reward": 100,
        "gold_reward": 80,
        "loot_table": [("health_potion", 0.7), ("steel_armor", 0.15)]
    }
}


def create_enemy(enemy_type: str, level_modifier: int = 0) -> Enemy:
    """
    Create an enemy instance with optional level scaling
    
    Args:
        enemy_type: Type of enemy to create
        level_modifier: Multiplier for scaling enemy stats based on player level
        
    Returns:
        Enemy instance
    """
    if enemy_type not in ENEMY_TYPES:
        enemy_type = "goblin"  # Default
    
    template = ENEMY_TYPES[enemy_type]
    
    # Scale stats based on level modifier
    scale = 1 + (level_modifier * 0.2)
    
    enemy = Enemy(
        name=template["name"],
        health=int(template["health"] * scale),
        attack=int(template["attack"] * scale),
        defense=int(template["defense"] * scale),
        xp_reward=int(template["xp_reward"] * scale),
        gold_reward=int(template["gold_reward"] * scale),
        loot_table=template["loot_table"]
    )
    
    return enemy


def get_random_enemy(player_level: int) -> Enemy:
    """
    Generate a random enemy appropriate for the player's level
    
    Args:
        player_level: Current player level
        
    Returns:
        Random enemy instance
    """
    # Define level ranges for enemy types
    if player_level <= 2:
        enemy_pool = ["slime", "goblin"]
    elif player_level <= 4:
        enemy_pool = ["goblin", "skeleton", "orc"]
    elif player_level <= 7:
        enemy_pool = ["orc", "skeleton", "troll", "vampire"]
    elif player_level <= 10:
        enemy_pool = ["troll", "dark_knight", "vampire"]
    else:
        enemy_pool = ["dark_knight", "vampire", "dragon"]
    
    enemy_type = random.choice(enemy_pool)
    return create_enemy(enemy_type, player_level - 1)
