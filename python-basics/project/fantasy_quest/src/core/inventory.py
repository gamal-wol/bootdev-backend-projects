"""
Inventory management system for Fantasy Quest
Handles item storage, equipment, and usage
"""

from src.entities.items import Weapon, Armor, Potion


class Inventory:
    """Manages player's items and equipment"""
    
    def __init__(self, capacity: int = 20):
        """
        Initialize inventory
        
        Args:
            capacity: Maximum number of items that can be carried
        """
        self.capacity = capacity
        self.items = []
        self.equipped_weapon = None
        self.equipped_armor = None
    
    def add_item(self, item) -> bool:
        """
        Add an item to inventory
        
        Args:
            item: Item to add
            
        Returns:
            True if item added successfully, False if inventory full
        """
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True
    
    def remove_item(self, item) -> bool:
        """
        Remove an item from inventory
        
        Args:
            item: Item to remove
            
        Returns:
            True if item removed, False if not found
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def equip_weapon(self, weapon, player) -> str:
        """
        Equip a weapon
        
        Args:
            weapon: Weapon to equip
            player: Player character to modify stats
            
        Returns:
            Status message
        """
        if not isinstance(weapon, Weapon):
            return "That's not a weapon!"
        
        if weapon not in self.items:
            return "You don't have that weapon!"
        
        # Unequip current weapon
        if self.equipped_weapon:
            player.attack -= self.equipped_weapon.attack_bonus
            self.items.append(self.equipped_weapon)
        
        # Equip new weapon
        self.equipped_weapon = weapon
        player.attack += weapon.attack_bonus
        self.items.remove(weapon)
        
        return f"Equipped {weapon.name}! ATK +{weapon.attack_bonus}"
    
    def equip_armor(self, armor, player) -> str:
        """
        Equip armor
        
        Args:
            armor: Armor to equip
            player: Player character to modify stats
            
        Returns:
            Status message
        """
        if not isinstance(armor, Armor):
            return "That's not armor!"
        
        if armor not in self.items:
            return "You don't have that armor!"
        
        # Unequip current armor
        if self.equipped_armor:
            player.defense -= self.equipped_armor.defense_bonus
            self.items.append(self.equipped_armor)
        
        # Equip new armor
        self.equipped_armor = armor
        player.defense += armor.defense_bonus
        self.items.remove(armor)
        
        return f"Equipped {armor.name}! DEF +{armor.defense_bonus}"
    
    def use_potion(self, potion, player) -> str:
        """
        Use a consumable potion
        
        Args:
            potion: Potion to use
            player: Player to apply effect to
            
        Returns:
            Result message
        """
        if not isinstance(potion, Potion):
            return "That's not a potion!"
        
        if potion not in self.items:
            return "You don't have that potion!"
        
        # Use the potion
        result = potion.use(player)
        self.items.remove(potion)
        
        return result
    
    def get_items_by_type(self, item_type: str) -> list:
        """
        Get all items of a specific type
        
        Args:
            item_type: Type of items to retrieve ('weapon', 'armor', 'potion')
            
        Returns:
            List of items matching the type
        """
        return [item for item in self.items if hasattr(item, 'item_type') and item.item_type == item_type]
    
    def display_inventory(self) -> str:
        """
        Get formatted inventory display
        
        Returns:
            Formatted string showing all items
        """
        output = f"\n{'='*50}\n"
        output += f"  INVENTORY ({len(self.items)}/{self.capacity})\n"
        output += f"{'='*50}\n"
        
        # Equipped items
        output += "\n[EQUIPPED]\n"
        if self.equipped_weapon:
            output += f"  Weapon: {self.equipped_weapon}\n"
        else:
            output += "  Weapon: None\n"
            
        if self.equipped_armor:
            output += f"  Armor: {self.equipped_armor}\n"
        else:
            output += "  Armor: None\n"
        
        # Inventory items
        if self.items:
            output += "\n[ITEMS]\n"
            for i, item in enumerate(self.items, 1):
                output += f"  {i}. {item}\n"
        else:
            output += "\n[ITEMS]\n  (Empty)\n"
        
        output += f"{'='*50}\n"
        return output
    
    def is_full(self) -> bool:
        """Check if inventory is at capacity"""
        return len(self.items) >= self.capacity
