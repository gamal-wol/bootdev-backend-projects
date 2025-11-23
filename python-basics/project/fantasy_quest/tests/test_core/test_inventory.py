"""
Tests for inventory management system
"""

import pytest
from src.core.inventory import Inventory
from src.entities.items import Weapon, Armor, Potion, get_item


class TestInventory:
    """Tests for the Inventory class"""

    def test_inventory_initialization(self, empty_inventory):
        """Verify default capacity = 20 and empty state"""
        # Verify default capacity = 20
        assert empty_inventory.capacity == 20

        # Check items list is empty
        assert len(empty_inventory.items) == 0
        assert empty_inventory.items == []

        # Assert no equipped items
        assert empty_inventory.equipped_weapon is None
        assert empty_inventory.equipped_armor is None

    def test_add_item_success(self, empty_inventory, sample_weapon):
        """Test adding item to inventory"""
        # Call add_item()
        result = empty_inventory.add_item(sample_weapon)

        # Verify returns True
        assert result is True

        # Check item in inventory
        assert sample_weapon in empty_inventory.items
        assert len(empty_inventory.items) == 1

    def test_add_item_full_inventory(self, empty_inventory):
        """Test adding item when inventory is full"""
        # Fill inventory to capacity
        for i in range(20):
            weapon = Weapon(f"Sword {i}", "A sword", 10, 5)
            empty_inventory.add_item(weapon)

        assert len(empty_inventory.items) == 20

        # Try to add one more
        extra_weapon = Weapon("Extra", "Too many", 10, 5)
        result = empty_inventory.add_item(extra_weapon)

        # Verify returns False
        assert result is False

        # Check item not added
        assert extra_weapon not in empty_inventory.items
        assert len(empty_inventory.items) == 20

    def test_remove_item_success(self, empty_inventory, sample_weapon):
        """Test removing item from inventory"""
        # Add item
        empty_inventory.add_item(sample_weapon)
        assert sample_weapon in empty_inventory.items

        # Call remove_item()
        result = empty_inventory.remove_item(sample_weapon)

        # Verify returns True
        assert result is True

        # Check item removed
        assert sample_weapon not in empty_inventory.items
        assert len(empty_inventory.items) == 0

    def test_remove_item_not_found(self, empty_inventory, sample_weapon):
        """Test removing item that doesn't exist in inventory"""
        # Try to remove item not in inventory
        result = empty_inventory.remove_item(sample_weapon)

        # Verify returns False
        assert result is False

    def test_equip_weapon_success(self, empty_inventory, sample_player, sample_weapon):
        """Test equipping a weapon"""
        # Add weapon to inventory
        empty_inventory.add_item(sample_weapon)
        initial_attack = sample_player.attack

        # Call equip_weapon()
        result = empty_inventory.equip_weapon(sample_weapon, sample_player)

        # Verify player attack increases
        assert sample_player.attack == initial_attack + sample_weapon.attack_bonus

        # Check weapon removed from items
        assert sample_weapon not in empty_inventory.items

        # Assert weapon set as equipped
        assert empty_inventory.equipped_weapon == sample_weapon

        # Check return message
        assert "Equipped" in result
        assert sample_weapon.name in result

    def test_equip_weapon_replaces_existing(self, empty_inventory, sample_player):
        """Test equipping weapon when one is already equipped"""
        # Create two weapons
        weapon1 = Weapon("Sword1", "First", 10, 10)
        weapon2 = Weapon("Sword2", "Second", 20, 15)

        # Equip first weapon
        empty_inventory.add_item(weapon1)
        empty_inventory.equip_weapon(weapon1, sample_player)
        initial_attack = sample_player.attack

        # Equip second weapon
        empty_inventory.add_item(weapon2)
        empty_inventory.equip_weapon(weapon2, sample_player)

        # Verify first weapon returned to inventory
        assert weapon1 in empty_inventory.items

        # Check player attack updated correctly
        # Attack should lose weapon1 bonus and gain weapon2 bonus
        assert sample_player.attack == initial_attack - weapon1.attack_bonus + weapon2.attack_bonus

        # Verify weapon2 is equipped
        assert empty_inventory.equipped_weapon == weapon2

    def test_equip_weapon_not_in_inventory(self, empty_inventory, sample_player, sample_weapon):
        """Test equipping weapon not in inventory"""
        # Try to equip weapon not owned
        result = empty_inventory.equip_weapon(sample_weapon, sample_player)

        # Verify error message
        assert "don't have" in result

        # Check no changes to player stats
        assert sample_player.attack == 10  # Default starting attack

    def test_equip_armor_success(self, empty_inventory, sample_player, sample_armor):
        """Test equipping armor"""
        # Add armor to inventory
        empty_inventory.add_item(sample_armor)
        initial_defense = sample_player.defense

        # Call equip_armor()
        result = empty_inventory.equip_armor(sample_armor, sample_player)

        # Verify player defense increases
        assert sample_player.defense == initial_defense + sample_armor.defense_bonus

        # Check armor equipped
        assert empty_inventory.equipped_armor == sample_armor
        assert sample_armor not in empty_inventory.items

        # Check return message
        assert "Equipped" in result

    def test_equip_armor_replaces_existing(self, empty_inventory, sample_player):
        """Test equipping armor when one is already equipped"""
        # Create two armors
        armor1 = Armor("Armor1", "First", 10, 10)
        armor2 = Armor("Armor2", "Second", 20, 15)

        # Equip first armor
        empty_inventory.add_item(armor1)
        empty_inventory.equip_armor(armor1, sample_player)
        initial_defense = sample_player.defense

        # Equip second armor
        empty_inventory.add_item(armor2)
        empty_inventory.equip_armor(armor2, sample_player)

        # Verify first armor returned to inventory
        assert armor1 in empty_inventory.items

        # Check defense updated correctly
        assert sample_player.defense == initial_defense - armor1.defense_bonus + armor2.defense_bonus

        # Verify armor2 is equipped
        assert empty_inventory.equipped_armor == armor2

    def test_use_potion_success(self, empty_inventory, damaged_player, sample_potion):
        """Test using a potion"""
        # Add potion to inventory
        empty_inventory.add_item(sample_potion)
        initial_health = damaged_player.current_health

        # Call use_potion()
        result = empty_inventory.use_potion(sample_potion, damaged_player)

        # Verify HP restored
        expected_health = min(damaged_player.max_health, initial_health + sample_potion.heal_amount)
        assert damaged_player.current_health == expected_health

        # Check potion consumed (removed)
        assert sample_potion not in empty_inventory.items

        # Check return message
        assert damaged_player.name in result
        assert "restored" in result.lower()

    def test_use_potion_at_full_health(self, empty_inventory, sample_player):
        """Test using potion when already at max health"""
        # Player at max health
        assert sample_player.current_health == sample_player.max_health

        potion = Potion("Test", "Test", 10, 50)
        empty_inventory.add_item(potion)

        # Use potion
        result = empty_inventory.use_potion(potion, sample_player)

        # Verify no overflow
        assert sample_player.current_health == sample_player.max_health

        # Check potion still consumed
        assert potion not in empty_inventory.items

    def test_get_items_by_type(self, empty_inventory):
        """Test filtering items by type"""
        # Add multiple item types
        weapon1 = Weapon("Sword", "A sword", 10, 5)
        weapon2 = Weapon("Axe", "An axe", 15, 7)
        armor1 = Armor("Shield", "A shield", 20, 5)
        potion1 = Potion("HP Potion", "Heals", 10, 30)

        empty_inventory.add_item(weapon1)
        empty_inventory.add_item(weapon2)
        empty_inventory.add_item(armor1)
        empty_inventory.add_item(potion1)

        # Call get_items_by_type("weapon")
        weapons = empty_inventory.get_items_by_type("weapon")

        # Verify only weapons returned
        assert len(weapons) == 2
        assert weapon1 in weapons
        assert weapon2 in weapons
        assert armor1 not in weapons

        # Test for each item type
        armors = empty_inventory.get_items_by_type("armor")
        assert len(armors) == 1
        assert armor1 in armors

        potions = empty_inventory.get_items_by_type("potion")
        assert len(potions) == 1
        assert potion1 in potions

    def test_display_inventory(self, empty_inventory, sample_weapon, sample_armor, sample_potion):
        """Test inventory display formatting"""
        # Add various items
        empty_inventory.add_item(sample_weapon)
        empty_inventory.add_item(sample_armor)
        empty_inventory.add_item(sample_potion)

        player = pytest.importorskip("src.core.character").Player("Test")

        # Equip some items
        empty_inventory.equip_weapon(sample_weapon, player)
        empty_inventory.equip_armor(sample_armor, player)

        # Call display_inventory()
        display = empty_inventory.display_inventory()

        # Verify formatted string contains all items
        assert isinstance(display, str)
        assert "INVENTORY" in display
        assert sample_weapon.name in display  # Equipped weapon shown
        assert sample_armor.name in display   # Equipped armor shown
        assert sample_potion.name in display  # Item in inventory

        # Check equipped items shown separately
        assert "EQUIPPED" in display
        assert "ITEMS" in display

    def test_is_full(self, empty_inventory):
        """Test is_full() method"""
        # Empty inventory is not full
        assert empty_inventory.is_full() is False

        # Fill to capacity
        for i in range(20):
            empty_inventory.add_item(Weapon(f"Item{i}", "Filler", 1, 1))

        # Should be full now
        assert empty_inventory.is_full() is True
