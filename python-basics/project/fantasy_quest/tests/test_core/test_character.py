"""
Tests for character system (Character and Player classes)
"""

import pytest
from unittest.mock import patch
from src.core.character import Character, Player


class TestCharacter:
    """Tests for the base Character class"""

    def test_character_initialization(self, sample_character):
        """Verify Character initializes with correct name, health, attack, defense"""
        assert sample_character.name == "TestChar"
        assert sample_character.max_health == 100
        assert sample_character.current_health == 100
        assert sample_character.attack == 15
        assert sample_character.defense == 10
        # Assert max_health equals current_health on creation
        assert sample_character.max_health == sample_character.current_health

    def test_character_is_alive(self):
        """Test is_alive() returns correct values based on health"""
        char = Character("Test", health=50, attack=10, defense=5)

        # Test is_alive() returns True when health > 0
        assert char.is_alive() is True

        # Test is_alive() returns False when health = 0
        char.current_health = 0
        assert char.is_alive() is False

        # Test is_alive() returns False when health < 0
        char.current_health = -10
        assert char.is_alive() is False

    def test_character_take_damage_basic(self, sample_character):
        """Test damage calculation with normal attack"""
        initial_health = sample_character.current_health

        # Test damage calculation (20 attack - 10 defense = 10 damage minimum)
        damage_dealt = sample_character.take_damage(20)

        # Verify defense reduces damage
        assert damage_dealt == max(1, 20 - sample_character.defense)
        assert sample_character.current_health == initial_health - damage_dealt

        # Assert minimum 1 damage is dealt
        low_damage = sample_character.take_damage(5)  # 5 - 10 def = negative, should be 1
        assert low_damage >= 1

    def test_character_take_damage_edge_cases(self):
        """Test take_damage with edge cases"""
        char = Character("Test", health=50, attack=10, defense=5)

        # Test take_damage with 0 damage input
        char.take_damage(0)
        assert char.current_health >= 50 - 1  # Minimum 1 damage

        # Reset character
        char = Character("Test", health=50, attack=10, defense=5)

        # Test health cannot go below 0
        char.take_damage(1000)
        assert char.current_health == 0
        assert char.current_health >= 0

    def test_character_heal_basic(self, sample_character):
        """Test heal() restores correct HP amount"""
        # Damage the character first
        sample_character.current_health = 50

        # Test heal() restores correct HP amount
        healed = sample_character.heal(30)

        # Verify returned value matches actual HP gained
        assert healed == 30
        assert sample_character.current_health == 80

    def test_character_heal_overflow(self, sample_character):
        """Test healing cannot exceed max_health"""
        sample_character.current_health = 90

        # Try to heal beyond max
        healed = sample_character.heal(50)

        # Test healing cannot exceed max_health
        assert sample_character.current_health == sample_character.max_health

        # Verify correct value returned when capped
        assert healed == 10  # Only 10 HP was actually restored


class TestPlayer:
    """Tests for the Player class"""

    def test_player_initialization(self, sample_player):
        """Verify Player starts at level 1 with correct starting stats"""
        # Verify Player starts at level 1
        assert sample_player.level == 1

        # Check starting stats (100 HP, 10 ATK, 5 DEF)
        assert sample_player.max_health == 100
        assert sample_player.current_health == 100
        assert sample_player.attack == 10
        assert sample_player.defense == 5

        # Verify starting gold = 50
        assert sample_player.gold == 50

        # Check XP = 0, xp_to_level = 100
        assert sample_player.xp == 0
        assert sample_player.xp_to_level == 100

    def test_player_gain_xp_no_level_up(self, sample_player):
        """Test gaining XP without reaching level threshold"""
        # Add XP below threshold
        leveled_up = sample_player.gain_xp(50)

        # Verify XP increases correctly
        assert sample_player.xp == 50

        # Assert level remains unchanged
        assert sample_player.level == 1
        assert leveled_up is False

    @patch('builtins.input')
    def test_player_gain_xp_with_level_up(self, mock_input, sample_player):
        """Test gaining XP that triggers level up"""
        mock_input.return_value = ""  # Mock the pause in level_up display

        initial_level = sample_player.level
        initial_xp_to_level = sample_player.xp_to_level

        # Add XP to trigger level up
        leveled_up = sample_player.gain_xp(120)

        # Verify level increases
        assert sample_player.level == initial_level + 1
        assert leveled_up is True

        # Check overflow XP carries over
        assert sample_player.xp == 20  # 120 - 100 = 20 overflow

        # Verify xp_to_level increases (exponential curve)
        assert sample_player.xp_to_level == int(initial_xp_to_level * 1.5)

    @patch('builtins.input')
    def test_player_level_up_stat_increases(self, mock_input, sample_player):
        """Test that leveling up increases stats correctly"""
        mock_input.return_value = ""  # Mock the pause in level_up display

        # Record initial stats
        initial_max_hp = sample_player.max_health
        initial_attack = sample_player.attack
        initial_defense = sample_player.defense

        # Damage player to test full heal
        sample_player.current_health = 50

        # Trigger level_up()
        sample_player.level_up()

        # Assert max_health increases by 20
        assert sample_player.max_health == initial_max_hp + 20

        # Assert attack increases by 3
        assert sample_player.attack == initial_attack + 3

        # Assert defense increases by 2
        assert sample_player.defense == initial_defense + 2

        # Verify current_health = max_health (full heal)
        assert sample_player.current_health == sample_player.max_health

    def test_player_gain_gold(self, sample_player):
        """Test gain_gold() with positive amount"""
        initial_gold = sample_player.gold

        sample_player.gain_gold(100)

        # Verify gold increases correctly
        assert sample_player.gold == initial_gold + 100

    def test_player_spend_gold_success(self, sample_player):
        """Test spend_gold() with sufficient funds"""
        initial_gold = sample_player.gold

        # Test spend_gold() with sufficient funds
        result = sample_player.spend_gold(30)

        # Verify gold decreases
        assert sample_player.gold == initial_gold - 30

        # Assert returns True
        assert result is True

    def test_player_spend_gold_failure(self, sample_player):
        """Test spend_gold() with insufficient funds"""
        initial_gold = sample_player.gold

        # Test spend_gold() with insufficient funds
        result = sample_player.spend_gold(1000)

        # Verify gold unchanged
        assert sample_player.gold == initial_gold

        # Assert returns False
        assert result is False

    def test_player_get_stats(self, sample_player):
        """Test get_stats() returns formatted string"""
        stats = sample_player.get_stats()

        # Test get_stats() returns formatted string
        assert isinstance(stats, str)

        # Verify contains name, level, HP, ATK, DEF, XP, Gold
        assert sample_player.name in stats
        assert f"Level {sample_player.level}" in stats
        assert f"HP: {sample_player.current_health}/{sample_player.max_health}" in stats
        assert f"ATK: {sample_player.attack}" in stats
        assert f"DEF: {sample_player.defense}" in stats
        assert f"XP: {sample_player.xp}/{sample_player.xp_to_level}" in stats
        assert f"Gold: {sample_player.gold}" in stats

    @patch('builtins.input')
    def test_player_multiple_level_ups(self, mock_input, sample_player):
        """Test gaining enough XP for multiple levels"""
        mock_input.return_value = ""  # Mock the pause in level_up display

        # Give enough XP for 3 level ups (100 + 150 + 225 = 475)
        sample_player.gain_xp(500)

        # Verify stats compound correctly
        assert sample_player.level == 4  # Started at 1, gained 3 levels

        # Check XP threshold scaling
        # Level 1->2: 100 * 1.5 = 150
        # Level 2->3: 150 * 1.5 = 225
        # Level 3->4: 225 * 1.5 = 337.5 = 337
        assert sample_player.xp_to_level == 337

        # Verify HP, ATK, DEF increased correctly
        assert sample_player.max_health == 100 + (20 * 3)  # 160
        assert sample_player.attack == 10 + (3 * 3)  # 19
        assert sample_player.defense == 5 + (2 * 3)  # 11
