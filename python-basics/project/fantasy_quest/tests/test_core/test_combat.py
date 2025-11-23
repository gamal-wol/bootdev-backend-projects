"""
Tests for combat system
"""

import pytest
from unittest.mock import patch, MagicMock
from src.core.combat import calculate_damage, player_turn, enemy_turn, combat_loop, process_combat_rewards
from src.core.character import Player
from src.entities.enemy import create_enemy
from src.core.inventory import Inventory
from src.entities.items import get_item


class TestCalculateDamage:
    """Tests for damage calculation"""

    def test_calculate_damage_basic(self):
        """Test basic damage calculation"""
        # Create mock attacker and defender
        attacker = MagicMock()
        attacker.attack = 20
        defender = MagicMock()
        defender.defense = 5

        # Verify damage within expected range (0.8-1.2x attack)
        damage = calculate_damage(attacker, defender)

        # Assert defense is subtracted
        assert damage >= 1  # Minimum damage
        assert damage <= 20  # Max would be around attack - defense + variance

        # Verify minimum 1 damage
        defender.defense = 100  # High defense
        damage = calculate_damage(attacker, defender)
        assert damage >= 1

    def test_calculate_damage_randomness(self):
        """Test that damage has randomness"""
        attacker = MagicMock()
        attacker.attack = 50
        defender = MagicMock()
        defender.defense = 10

        # Run calculate_damage 100 times
        damages = [calculate_damage(attacker, defender) for _ in range(100)]

        # Verify results vary (not always same)
        assert len(set(damages)) > 1  # Should have multiple different values

        # Check all values within expected bounds (50*0.8 - 10 = 30 to 50*1.2 - 10 = 50)
        for damage in damages:
            assert damage >= 1
            assert damage <= 60  # Reasonable upper bound


class TestPlayerTurn:
    """Tests for player turn in combat"""

    @patch('src.core.combat.get_user_choice')
    def test_player_turn_attack(self, mock_input, sample_player, sample_enemy, empty_inventory):
        """Test player choosing to attack"""
        # Mock user input to select attack (choice "1")
        mock_input.return_value = "1"

        enemy_initial_health = sample_enemy.current_health

        # Execute player turn
        combat_continues, message = player_turn(sample_player, sample_enemy, empty_inventory)

        # Verify enemy takes damage
        assert sample_enemy.current_health < enemy_initial_health

        # Check combat continues (returns True) if enemy still alive
        if sample_enemy.is_alive():
            assert combat_continues is True

        # Verify action message returned
        assert isinstance(message, str)
        assert "attack" in message.lower()

    @patch('src.core.combat.get_user_choice')
    def test_player_turn_attack_kills_enemy(self, mock_input, sample_player, empty_inventory):
        """Test player attack that defeats enemy"""
        # Set enemy health very low
        enemy = create_enemy("slime")
        enemy.current_health = 1

        # Mock attack input
        mock_input.return_value = "1"

        # Execute player turn
        combat_continues, message = player_turn(sample_player, enemy, empty_inventory)

        # Verify combat ends (returns False)
        assert combat_continues is False

        # Check defeat message in output
        assert "defeated" in message.lower() or "defeat" in message.lower()

    @patch('src.core.combat.get_user_choice')
    def test_player_turn_use_potion_success(self, mock_input, damaged_player, sample_enemy, empty_inventory):
        """Test player using a potion during combat"""
        # Add potion to inventory
        potion = get_item("health_potion")
        empty_inventory.add_item(potion)

        # Reduce player health
        initial_health = damaged_player.current_health

        # Mock user input to select potion (choice "2", then "1" to select potion)
        mock_input.side_effect = ["2", "1"]

        # Execute player turn
        combat_continues, message = player_turn(damaged_player, sample_enemy, empty_inventory)

        # Verify HP restored
        assert damaged_player.current_health > initial_health

        # Check potion removed from inventory
        assert potion not in empty_inventory.items

        # Combat should continue
        assert combat_continues is True

    @patch('src.core.combat.get_user_choice')
    def test_player_turn_use_potion_none_available(self, mock_input, sample_player, sample_enemy, empty_inventory):
        """Test player trying to use potion when none available"""
        # Mock potion selection when inventory empty
        mock_input.return_value = "2"

        # Execute player turn
        combat_continues, message = player_turn(sample_player, sample_enemy, empty_inventory)

        # Verify appropriate error message
        assert "don't have" in message.lower() or "no" in message.lower()

        # Check combat continues
        assert combat_continues is True

    @patch('src.core.combat.get_user_choice')
    @patch('random.random')
    def test_player_turn_flee_success(self, mock_random, mock_input, sample_player, sample_enemy, empty_inventory):
        """Test successful flee attempt"""
        # Mock flee choice (choice "3")
        mock_input.return_value = "3"

        # Mock random to guarantee success
        mock_random.return_value = 0.3  # Less than 0.5 = success

        # Execute player turn
        combat_continues, message = player_turn(sample_player, sample_enemy, empty_inventory)

        # Verify combat ends (returns False)
        assert combat_continues is False

        # Check flee message
        assert "fled" in message.lower() or "escape" in message.lower()

    @patch('src.core.combat.get_user_choice')
    @patch('random.random')
    def test_player_turn_flee_failure(self, mock_random, mock_input, sample_player, sample_enemy, empty_inventory):
        """Test failed flee attempt"""
        # Mock flee choice
        mock_input.return_value = "3"

        # Mock random to guarantee failure
        mock_random.return_value = 0.7  # Greater than 0.5 = failure

        # Execute player turn
        combat_continues, message = player_turn(sample_player, sample_enemy, empty_inventory)

        # Verify combat continues (returns True)
        assert combat_continues is True

        # Check failure message
        assert "could" in message.lower() or "escape" in message.lower()


class TestEnemyTurn:
    """Tests for enemy turn in combat"""

    def test_enemy_turn(self, sample_player, sample_enemy):
        """Test enemy attack on player"""
        player_initial_health = sample_player.current_health

        # Call enemy_turn()
        message = enemy_turn(sample_enemy, sample_player)

        # Verify player takes damage
        assert sample_player.current_health < player_initial_health

        # Check damage message format
        assert isinstance(message, str)
        assert sample_enemy.name in message
        assert sample_player.name in message
        assert "attack" in message.lower()


class TestCombatLoop:
    """Tests for complete combat scenarios"""

    @patch('src.core.combat.input')
    @patch('src.core.combat.get_user_choice')
    @patch('src.core.combat.clear_screen')
    def test_combat_loop_player_victory(self, mock_clear, mock_input, mock_enter, sample_player, empty_inventory):
        """Test complete combat where player wins"""
        # Create weak enemy
        enemy = create_enemy("slime")
        enemy.current_health = 10  # Make it easy to defeat

        # Mock all inputs (attack repeatedly, press enter)
        mock_input.return_value = "1"  # Always attack
        mock_enter.return_value = ""

        # Execute combat
        victory, rewards = combat_loop(sample_player, enemy, empty_inventory)

        # Verify returns (True, rewards_dict)
        assert victory is True
        assert isinstance(rewards, dict)

        # Check rewards contain xp, gold, loot
        assert "xp" in rewards
        assert "gold" in rewards
        assert "loot" in rewards
        assert rewards["xp"] > 0
        assert rewards["gold"] > 0

    @patch('src.core.combat.input')
    @patch('src.core.combat.get_user_choice')
    @patch('src.core.combat.clear_screen')
    def test_combat_loop_player_defeat(self, mock_clear, mock_input, mock_enter, empty_inventory):
        """Test combat where player is defeated"""
        # Create weak player
        weak_player = Player("WeakHero")
        weak_player.current_health = 5
        weak_player.attack = 1

        # Create strong enemy
        strong_enemy = create_enemy("orc_warrior")

        # Mock inputs
        mock_input.return_value = "1"
        mock_enter.return_value = ""

        # Execute combat
        victory, rewards = combat_loop(weak_player, strong_enemy, empty_inventory)

        # Verify returns (False, {})
        assert victory is False
        assert rewards == {}


class TestProcessCombatRewards:
    """Tests for processing combat rewards"""

    @patch('src.core.combat.input')
    @patch('src.core.combat.clear_screen')
    def test_process_combat_rewards(self, mock_clear, mock_input, sample_player, empty_inventory):
        """Test applying combat rewards to player"""
        initial_xp = sample_player.xp
        initial_gold = sample_player.gold

        # Create rewards dict
        rewards = {
            "xp": 50,
            "gold": 30,
            "loot": ["minor_potion"]
        }

        mock_input.return_value = ""

        # Call process_combat_rewards()
        process_combat_rewards(sample_player, empty_inventory, rewards)

        # Verify player gains XP and gold
        assert sample_player.xp == initial_xp + 50
        assert sample_player.gold == initial_gold + 30

        # Check items added to inventory
        potions = empty_inventory.get_items_by_type("potion")
        assert len(potions) == 1

    @patch('src.core.combat.input')
    @patch('src.core.combat.clear_screen')
    def test_process_combat_rewards_inventory_full(self, mock_clear, mock_input, sample_player):
        """Test rewards when inventory is full"""
        # Fill inventory
        full_inventory = Inventory()
        for i in range(20):
            item = get_item("minor_potion")
            full_inventory.add_item(item)

        rewards = {
            "xp": 25,
            "gold": 15,
            "loot": ["health_potion"]
        }

        mock_input.return_value = ""

        # This should not crash even if inventory is full
        process_combat_rewards(sample_player, full_inventory, rewards)

        # Player still gets XP and gold
        assert sample_player.xp == 25
        assert sample_player.gold == 65  # 50 starting + 15
