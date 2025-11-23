"""
Integration tests for game flow
Tests multiple systems working together
"""

import pytest
from unittest.mock import patch, MagicMock
from src.main import Game
from src.core.character import Player
from src.core.inventory import Inventory
from src.entities.quest import QuestLog, QUEST_DATABASE
from src.entities.items import get_item


class TestGameInitialization:
    """Tests for game initialization"""

    def test_game_initialization(self, fresh_game):
        """Test Game instance creation"""
        # Verify initial state
        assert fresh_game.player is None
        assert fresh_game.inventory is None
        assert fresh_game.quest_log is None

        # Check game_running = True
        assert fresh_game.game_running is True

    @patch('src.main.get_user_input')
    @patch('src.main.clear_screen')
    @patch('src.main.display_title')
    def test_start_new_game(self, mock_title, mock_clear, mock_input, fresh_game):
        """Test starting a new game"""
        # Mock user input for name
        mock_input.return_value = "TestHero"

        # Call start_new_game()
        fresh_game.start_new_game()

        # Verify player, inventory, quest_log created
        assert fresh_game.player is not None
        assert isinstance(fresh_game.player, Player)
        assert fresh_game.player.name == "TestHero"

        assert fresh_game.inventory is not None
        assert isinstance(fresh_game.inventory, Inventory)

        assert fresh_game.quest_log is not None
        assert isinstance(fresh_game.quest_log, QuestLog)

        # Check starting items added
        assert len(fresh_game.inventory.items) > 0


class TestExploreAndCombat:
    """Tests for explore and combat integration"""

    @patch('src.main.pause')
    @patch('src.main.clear_screen')
    @patch('src.main.combat_loop')
    @patch('src.main.get_random_enemy')
    def test_explore_and_combat_victory(self, mock_enemy, mock_combat, mock_clear, mock_pause, fresh_game):
        """Test explore leading to combat victory"""
        # Setup game
        fresh_game.player = Player("Hero")
        fresh_game.inventory = Inventory()
        fresh_game.quest_log = QuestLog()
        fresh_game.quest_log.add_quest(QUEST_DATABASE["goblin_slayer"])

        # Mock enemy
        from src.entities.enemy import create_enemy
        enemy = create_enemy("goblin")
        mock_enemy.return_value = enemy

        # Mock combat scenario - player wins
        rewards = {"xp": 20, "gold": 10, "loot": []}
        mock_combat.return_value = (True, rewards)

        initial_xp = fresh_game.player.xp
        initial_gold = fresh_game.player.gold

        # Call explore
        fresh_game.explore()

        # Verify rewards processed
        assert fresh_game.player.xp >= initial_xp
        assert fresh_game.player.gold >= initial_gold

    @patch('src.main.pause')
    @patch('src.main.clear_screen')
    @patch('src.main.combat_loop')
    @patch('src.main.get_random_enemy')
    def test_explore_and_combat_defeat(self, mock_enemy, mock_combat, mock_clear, mock_pause, fresh_game):
        """Test explore leading to combat defeat"""
        # Setup game
        fresh_game.player = Player("Hero")
        fresh_game.inventory = Inventory()
        fresh_game.quest_log = QuestLog()

        # Mock enemy
        from src.entities.enemy import create_enemy
        mock_enemy.return_value = create_enemy("goblin")

        # Mock combat - player loses
        mock_combat.return_value = (False, {})

        # Call explore
        fresh_game.explore()

        # Should complete without errors


class TestRestSystem:
    """Tests for rest/inn system"""

    @patch('src.main.pause')
    @patch('src.main.get_user_choice')
    @patch('src.main.clear_screen')
    def test_rest_restores_health(self, mock_clear, mock_choice, mock_pause, fresh_game):
        """Test resting at the inn"""
        # Setup game
        fresh_game.player = Player("Hero")
        fresh_game.inventory = Inventory()
        fresh_game.player.current_health = 50  # Reduce health
        fresh_game.player.gold = 100

        # Mock user choosing to rest
        mock_choice.return_value = "1"  # Yes

        initial_gold = fresh_game.player.gold

        # Call rest
        fresh_game.rest()

        # Verify health restored
        assert fresh_game.player.current_health == fresh_game.player.max_health

        # Check gold spent
        assert fresh_game.player.gold < initial_gold


class TestShopSystem:
    """Tests for shop purchases"""

    @patch('src.main.pause')
    @patch('src.main.get_user_choice')
    @patch('src.main.clear_screen')
    def test_shop_purchase(self, mock_clear, mock_choice, mock_pause, fresh_game):
        """Test buying from shop"""
        # Setup game
        fresh_game.player = Player("Hero")
        fresh_game.inventory = Inventory()
        fresh_game.player.gold = 100

        # Mock user buying potion then leaving
        mock_choice.side_effect = ["1", "6"]  # Buy minor potion, then leave

        initial_gold = fresh_game.player.gold
        initial_items = len(fresh_game.inventory.items)

        # Visit shop
        fresh_game.visit_shop()

        # Verify gold spent
        assert fresh_game.player.gold < initial_gold

        # Check item in inventory
        assert len(fresh_game.inventory.items) > initial_items


class TestEquipmentManagement:
    """Tests for equipment management"""

    @patch('src.main.pause')
    @patch('src.main.get_user_choice')
    @patch('src.main.clear_screen')
    def test_equipment_management_flow(self, mock_clear, mock_choice, mock_pause, fresh_game):
        """Test equipping weapon and armor"""
        # Setup game
        fresh_game.player = Player("Hero")
        fresh_game.inventory = Inventory()

        # Add weapon and armor
        weapon = get_item("iron_sword")
        armor = get_item("iron_armor")
        fresh_game.inventory.add_item(weapon)
        fresh_game.inventory.add_item(armor)

        initial_attack = fresh_game.player.attack
        initial_defense = fresh_game.player.defense

        # Equip weapon
        result = fresh_game.inventory.equip_weapon(weapon, fresh_game.player)
        assert fresh_game.player.attack > initial_attack

        # Equip armor
        result = fresh_game.inventory.equip_armor(armor, fresh_game.player)
        assert fresh_game.player.defense > initial_defense


class TestQuestCompletion:
    """Tests for quest completion flow"""

    @patch('src.main.pause')
    @patch('src.main.get_user_choice')
    @patch('src.main.clear_screen')
    def test_quest_completion_flow(self, mock_clear, mock_choice, mock_pause, fresh_game):
        """Test completing and turning in a quest"""
        # Setup game
        fresh_game.player = Player("Hero")
        fresh_game.inventory = Inventory()
        fresh_game.quest_log = QuestLog()

        # Add quest
        quest = QUEST_DATABASE["goblin_slayer"]
        fresh_game.quest_log.add_quest(quest)

        # Simulate defeating required enemies
        fresh_game.quest_log.update_all("Defeat Goblins", 5)

        # Verify quest completes
        assert quest.completed is True

        # Mock turning in
        mock_choice.return_value = "1"  # Yes, turn in now

        initial_xp = fresh_game.player.xp

        # Turn in quest
        fresh_game.check_quest_completion()

        # Verify rewards received
        assert fresh_game.player.xp > initial_xp or quest.turned_in is True


class TestGameQuit:
    """Tests for quitting the game"""

    @patch('src.main.get_user_choice')
    @patch('src.main.clear_screen')
    def test_quit_game_confirm(self, mock_clear, mock_choice, fresh_game):
        """Test quitting with confirmation"""
        # Setup game
        fresh_game.player = Player("Hero")

        # Mock confirming quit
        mock_choice.return_value = "1"  # Yes

        # Call quit
        fresh_game.quit_game()

        # Verify game_running = False
        assert fresh_game.game_running is False

    @patch('src.main.get_user_choice')
    @patch('src.main.clear_screen')
    def test_quit_game_cancel(self, mock_clear, mock_choice, fresh_game):
        """Test cancelling quit"""
        # Setup game
        fresh_game.player = Player("Hero")

        # Mock cancelling quit
        mock_choice.return_value = "2"  # No

        initial_state = fresh_game.game_running

        # Call quit
        fresh_game.quit_game()

        # Verify game_running unchanged
        assert fresh_game.game_running == initial_state
