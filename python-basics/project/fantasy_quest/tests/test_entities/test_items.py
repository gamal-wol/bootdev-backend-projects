"""
Tests for item system (Item, Weapon, Armor, Potion classes)
"""

import pytest
from src.entities.items import Item, Weapon, Armor, Potion, get_item, ITEMS_DATABASE
from src.core.character import Character


class TestItem:
    """Tests for base Item class"""

    def test_item_initialization(self):
        """Test Item initialization with all attributes"""
        # Create base Item
        item = Item("Test Item", "A test description", 100)

        # Verify name, description, value set
        assert item.name == "Test Item"
        assert item.description == "A test description"
        assert item.value == 100

    def test_item_str_representation(self):
        """Test __str__() format for Item"""
        item = Item("Magic Ring", "Grants power", 500)

        # Check __str__() format
        item_str = str(item)
        assert "Magic Ring" in item_str
        assert "Grants power" in item_str


class TestWeapon:
    """Tests for Weapon class"""

    def test_weapon_initialization(self, sample_weapon):
        """Test Weapon initialization and inheritance"""
        # Verify inherits Item properties
        assert sample_weapon.name == "Test Sword"
        assert sample_weapon.description == "A test weapon"
        assert sample_weapon.value == 100

        # Check attack_bonus set
        assert sample_weapon.attack_bonus == 20

        # Assert item_type = "weapon"
        assert sample_weapon.item_type == "weapon"

    def test_weapon_str_representation(self, sample_weapon):
        """Test weapon string representation includes attack bonus"""
        weapon_str = str(sample_weapon)

        # Verify includes attack bonus in string
        assert "Test Sword" in weapon_str
        assert "+20" in weapon_str or "20" in weapon_str
        assert "ATK" in weapon_str


class TestArmor:
    """Tests for Armor class"""

    def test_armor_initialization(self, sample_armor):
        """Test Armor initialization"""
        # Create Armor
        assert sample_armor.name == "Test Armor"
        assert sample_armor.value == 150

        # Check defense_bonus set
        assert sample_armor.defense_bonus == 15

        # Assert item_type = "armor"
        assert sample_armor.item_type == "armor"

    def test_armor_str_representation(self, sample_armor):
        """Test armor string shows defense bonus"""
        armor_str = str(sample_armor)

        # Verify defense bonus shown in string
        assert "Test Armor" in armor_str
        assert "+15" in armor_str or "15" in armor_str
        assert "DEF" in armor_str


class TestPotion:
    """Tests for Potion class"""

    def test_potion_initialization(self, sample_potion):
        """Test Potion initialization"""
        # Create Potion
        assert sample_potion.name == "Test Potion"
        assert sample_potion.value == 50

        # Check heal_amount set
        assert sample_potion.heal_amount == 75

        # Assert consumable = True
        assert sample_potion.consumable is True

        # Verify item_type = "potion"
        assert sample_potion.item_type == "potion"

    def test_potion_use(self, sample_potion):
        """Test using a potion on a character"""
        # Create character with reduced health
        char = Character("TestChar", health=100, attack=10, defense=5)
        char.current_health = 30

        # Use potion
        result = sample_potion.use(char)

        # Verify correct HP restored
        assert char.current_health == 30 + sample_potion.heal_amount

        # Check return message format
        assert isinstance(result, str)
        assert char.name in result
        assert sample_potion.name in result

    def test_potion_str_representation(self, sample_potion):
        """Test potion string shows heal amount"""
        potion_str = str(sample_potion)

        # Verify shows heal amount in string
        assert "Test Potion" in potion_str
        assert "75" in potion_str
        assert "HP" in potion_str or "Heals" in potion_str


class TestItemDatabase:
    """Tests for item database and get_item function"""

    def test_get_item_valid_keys(self):
        """Test get_item() returns correct items for all database keys"""
        # Test weapons
        rusty_sword = get_item("rusty_sword")
        assert isinstance(rusty_sword, Weapon)
        assert rusty_sword.name == "Rusty Sword"
        assert rusty_sword.attack_bonus == 5

        iron_sword = get_item("iron_sword")
        assert isinstance(iron_sword, Weapon)
        assert iron_sword.attack_bonus == 10

        steel_sword = get_item("steel_sword")
        assert isinstance(steel_sword, Weapon)
        assert steel_sword.attack_bonus == 15

        legendary_blade = get_item("legendary_blade")
        assert isinstance(legendary_blade, Weapon)
        assert legendary_blade.attack_bonus == 30

        # Test armors
        leather_armor = get_item("leather_armor")
        assert isinstance(leather_armor, Armor)
        assert leather_armor.defense_bonus == 5

        iron_armor = get_item("iron_armor")
        assert isinstance(iron_armor, Armor)
        assert iron_armor.defense_bonus == 10

        steel_armor = get_item("steel_armor")
        assert isinstance(steel_armor, Armor)
        assert steel_armor.defense_bonus == 15

        dragon_armor = get_item("dragon_armor")
        assert isinstance(dragon_armor, Armor)
        assert dragon_armor.defense_bonus == 35

        # Test potions
        minor_potion = get_item("minor_potion")
        assert isinstance(minor_potion, Potion)
        assert minor_potion.heal_amount == 30

        health_potion = get_item("health_potion")
        assert isinstance(health_potion, Potion)
        assert health_potion.heal_amount == 50

        greater_potion = get_item("greater_potion")
        assert isinstance(greater_potion, Potion)
        assert greater_potion.heal_amount == 100

        mega_potion = get_item("mega_potion")
        assert isinstance(mega_potion, Potion)
        assert mega_potion.heal_amount == 999

    def test_get_item_invalid_key(self):
        """Test get_item() with non-existent item"""
        # Call get_item("nonexistent")
        result = get_item("nonexistent_item_key")

        # Verify returns None
        assert result is None

    def test_items_database_completeness(self):
        """Verify all expected items exist in database"""
        # Check that key items exist
        expected_weapons = ["rusty_sword", "iron_sword", "steel_sword", "legendary_blade"]
        expected_armors = ["leather_armor", "iron_armor", "steel_armor", "dragon_armor"]
        expected_potions = ["minor_potion", "health_potion", "greater_potion", "mega_potion"]

        for weapon_key in expected_weapons:
            assert weapon_key in ITEMS_DATABASE
            assert isinstance(ITEMS_DATABASE[weapon_key], Weapon)

        for armor_key in expected_armors:
            assert armor_key in ITEMS_DATABASE
            assert isinstance(ITEMS_DATABASE[armor_key], Armor)

        for potion_key in expected_potions:
            assert potion_key in ITEMS_DATABASE
            assert isinstance(ITEMS_DATABASE[potion_key], Potion)
