"""
Character system for Fantasy Quest
Defines Player and base Character classes with stats and leveling mechanics
"""


class Character:
    """Base character class with core attributes and methods"""
    
    def __init__(self, name: str, health: int, attack: int, defense: int):
        """
        Initialize a character with basic stats
        
        Args:
            name: Character's name
            health: Maximum and current health points
            attack: Base attack power
            defense: Defense/armor value
        """
        self.name = name
        self.max_health = health
        self.current_health = health
        self.attack = attack
        self.defense = defense
        
    def is_alive(self) -> bool:
        """Check if character is still alive"""
        return self.current_health > 0
    
    def take_damage(self, damage: int) -> int:
        """
        Apply damage to character, accounting for defense
        
        Args:
            damage: Raw damage amount
            
        Returns:
            Actual damage taken after defense
        """
        actual_damage = max(1, damage - self.defense)  # Minimum 1 damage
        self.current_health = max(0, self.current_health - actual_damage)
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """
        Heal the character
        
        Args:
            amount: HP to restore
            
        Returns:
            Actual HP restored
        """
        old_health = self.current_health
        self.current_health = min(self.max_health, self.current_health + amount)
        return self.current_health - old_health
    
    def __str__(self) -> str:
        """String representation of character"""
        return f"{self.name} (HP: {self.current_health}/{self.max_health})"


class Player(Character):
    """Player character with additional RPG mechanics"""
    
    def __init__(self, name: str):
        """
        Initialize player with starting stats
        
        Args:
            name: Player's chosen name
        """
        super().__init__(name=name, health=100, attack=10, defense=5)
        self.level = 1
        self.xp = 0
        self.xp_to_level = 100
        self.gold = 50
        self.inventory = []
        
    def gain_xp(self, amount: int) -> bool:
        """
        Add experience points and check for level up
        
        Args:
            amount: XP to gain
            
        Returns:
            True if player leveled up, False otherwise
        """
        self.xp += amount
        
        if self.xp >= self.xp_to_level:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """Increase player level and improve stats"""
        from src.utils.helpers import display_level_up
        
        self.level += 1
        self.xp -= self.xp_to_level
        self.xp_to_level = int(self.xp_to_level * 1.5)  # Exponential XP curve
        
        # Stat increases
        self.max_health += 20
        self.current_health = self.max_health  # Full heal on level up
        self.attack += 3
        self.defense += 2
        
        display_level_up(self)
        print(f"Stats increased: HP +20, ATK +3, DEF +2")
        print(f"HP fully restored!")
        print()
    
    def gain_gold(self, amount: int):
        """Add gold to player's purse"""
        self.gold += amount
    
    def spend_gold(self, amount: int) -> bool:
        """
        Attempt to spend gold
        
        Args:
            amount: Gold to spend
            
        Returns:
            True if purchase successful, False if not enough gold
        """
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def get_stats(self) -> str:
        """Return formatted player statistics"""
        stats = f"\n{'='*40}\n"
        stats += f"  {self.name} - Level {self.level}\n"
        stats += f"{'='*40}\n"
        stats += f"  HP: {self.current_health}/{self.max_health}\n"
        stats += f"  ATK: {self.attack}  |  DEF: {self.defense}\n"
        stats += f"  XP: {self.xp}/{self.xp_to_level}\n"
        stats += f"  Gold: {self.gold}\n"
        stats += f"{'='*40}\n"
        return stats
