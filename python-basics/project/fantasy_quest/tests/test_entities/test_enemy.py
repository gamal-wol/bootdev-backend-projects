"""
Tests for enemy system
"""

import pytest
from unittest.mock import patch
from src.entities.enemy import Enemy, create_enemy, get_random_enemy, ENEMY_TYPES
from src.core.character import Character


class TestEnemy:
    """Tests for Enemy class"""

    def test_enemy_initialization(self):
        """Test Enemy initialization with all attributes"""
        # Create Enemy instance
        enemy = Enemy(
            name="Test Enemy",
            health=50,
            attack=15,
            defense=5,
            xp_reward=30,
            gold_reward=20,
            loot_table=[("health_potion", 0.5)]
        )

        # Verify all attributes set correctly
        assert enemy.name == "Test Enemy"
        assert enemy.max_health == 50
        assert enemy.current_health == 50
        assert enemy.attack == 15
        assert enemy.defense == 5
        assert enemy.xp_reward == 30
        assert enemy.gold_reward == 20

        # Check loot_table is list
        assert isinstance(enemy.loot_table, list)
        assert len(enemy.loot_table) == 1

    def test_enemy_inherits_character(self, sample_enemy):
        """Test Enemy inherits from Character and has all methods"""
        # Verify Enemy is instance of Character
        assert isinstance(sample_enemy, Character)

        # Test inherited methods work (take_damage, is_alive, heal)
        assert sample_enemy.is_alive() is True

        initial_health = sample_enemy.current_health
        sample_enemy.take_damage(10)
        assert sample_enemy.current_health < initial_health

        sample_enemy.heal(5)
        assert sample_enemy.current_health > (initial_health - 10)

    @patch('random.random')
    def test_enemy_get_loot_guaranteed_drop(self, mock_random):
        """Test loot with 100% drop chance"""
        # Create enemy with 100% drop chance item
        enemy = Enemy(
            name="Test",
            health=50,
            attack=10,
            defense=5,
            xp_reward=20,
            gold_reward=10,
            loot_table=[("health_potion", 1.0)]  # 100% chance
        )

        # Mock random to return 0 (always drop)
        mock_random.return_value = 0.1

        # Call get_loot()
        loot = enemy.get_loot()

        # Verify item in returned list
        assert "health_potion" in loot
        assert len(loot) == 1

    @patch('random.random')
    def test_enemy_get_loot_no_drop(self, mock_random):
        """Test loot with 0% drop chance"""
        # Create enemy with 0% drop chance
        enemy = Enemy(
            name="Test",
            health=50,
            attack=10,
            defense=5,
            xp_reward=20,
            gold_reward=10,
            loot_table=[("health_potion", 0.0)]  # 0% chance
        )

        # Mock random to return high value (no drops)
        mock_random.return_value = 0.9

        # Call get_loot()
        loot = enemy.get_loot()

        # Verify empty list returned
        assert loot == []
        assert len(loot) == 0

    def test_enemy_get_loot_multiple_items(self):
        """Test enemy with multiple loot table entries"""
        # Enemy with multiple loot table entries
        enemy = Enemy(
            name="Test",
            health=50,
            attack=10,
            defense=5,
            xp_reward=20,
            gold_reward=10,
            loot_table=[
                ("health_potion", 0.5),
                ("iron_sword", 0.3),
                ("iron_armor", 0.2)
            ]
        )

        # Test that multiple items can drop (run multiple times)
        all_drops = []
        for _ in range(100):
            drops = enemy.get_loot()
            all_drops.extend(drops)

        # Verify randomness - should get some drops over 100 iterations
        assert len(all_drops) > 0


class TestCreateEnemy:
    """Tests for create_enemy function"""

    def test_create_enemy_basic(self):
        """Test creating enemy without level modifier"""
        # Call create_enemy("goblin")
        goblin = create_enemy("goblin")

        # Verify correct stats from template
        assert goblin.name == "Goblin"
        assert goblin.max_health == 30
        assert goblin.attack == 5
        assert goblin.defense == 2
        assert goblin.xp_reward == 20
        assert goblin.gold_reward == 10

        # Check no level modifier (scale = 1)
        template = ENEMY_TYPES["goblin"]
        assert goblin.max_health == template["health"]

    def test_create_enemy_with_level_scaling(self):
        """Test creating enemy with level scaling"""
        # Call create_enemy("goblin", level_modifier=5)
        goblin = create_enemy("goblin", level_modifier=5)

        # Verify stats scaled up (scale = 1 + 5*0.2 = 2.0)
        template = ENEMY_TYPES["goblin"]
        expected_health = int(template["health"] * 2.0)
        expected_attack = int(template["attack"] * 2.0)

        assert goblin.max_health == expected_health
        assert goblin.attack == expected_attack

        # Check XP and gold rewards scaled
        assert goblin.xp_reward == int(template["xp_reward"] * 2.0)
        assert goblin.gold_reward == int(template["gold_reward"] * 2.0)

    def test_create_enemy_invalid_type(self):
        """Test creating enemy with non-existent type"""
        # Call with non-existent enemy type
        enemy = create_enemy("nonexistent_type")

        # Verify defaults to "goblin"
        assert enemy.name == "Goblin"
        assert enemy.max_health == 30


class TestGetRandomEnemy:
    """Tests for get_random_enemy function"""

    @patch('random.choice')
    def test_get_random_enemy_level_1_range(self, mock_choice):
        """Test enemy pool for level 1-2 players"""
        # Mock choice to verify correct pool
        mock_choice.return_value = "slime"

        # Test level 1
        enemy = get_random_enemy(1)

        # Should get slime/goblin
        called_with = mock_choice.call_args[0][0]
        assert "slime" in called_with
        assert "goblin" in called_with
        assert len(called_with) == 2

    @patch('random.choice')
    def test_get_random_enemy_level_3_range(self, mock_choice):
        """Test enemy pool for level 3-4 players"""
        mock_choice.return_value = "goblin"

        # Test level 3
        enemy = get_random_enemy(3)

        # Should get goblin/skeleton/orc
        called_with = mock_choice.call_args[0][0]
        assert "goblin" in called_with
        assert "skeleton" in called_with
        assert "orc" in called_with

    @patch('random.choice')
    def test_get_random_enemy_level_8_range(self, mock_choice):
        """Test enemy pool for level 8-10 players"""
        mock_choice.return_value = "troll"

        # Test level 8
        enemy = get_random_enemy(8)

        # Should get troll/dark_knight/vampire
        called_with = mock_choice.call_args[0][0]
        assert "troll" in called_with
        assert "dark_knight" in called_with
        assert "vampire" in called_with

    @patch('random.choice')
    def test_get_random_enemy_level_12_range(self, mock_choice):
        """Test enemy pool for level 12+ players"""
        mock_choice.return_value = "dragon"

        # Test level 12
        enemy = get_random_enemy(12)

        # Should get dark_knight/vampire/dragon
        called_with = mock_choice.call_args[0][0]
        assert "dark_knight" in called_with
        assert "vampire" in called_with
        assert "dragon" in called_with

    def test_get_random_enemy_scaling(self):
        """Test that high-level enemies have scaled stats"""
        # Generate enemy for high level player
        enemy = get_random_enemy(10)

        # Verify stats are scaled appropriately
        # Level 10 means level_modifier = 9, scale = 1 + 9*0.2 = 2.8
        # Health should be significantly higher than base
        assert enemy.max_health > 50  # Should be scaled up from base values


class TestEnemyTypes:
    """Tests for enemy type definitions"""

    def test_all_enemy_types_valid(self):
        """Verify all enemy types can be created"""
        for enemy_type in ENEMY_TYPES.keys():
            enemy = create_enemy(enemy_type)
            assert enemy is not None
            assert enemy.name is not None
            assert enemy.max_health > 0
            assert enemy.attack > 0

    def test_enemy_progression(self):
        """Verify enemies get progressively stronger"""
        slime = create_enemy("slime")
        goblin = create_enemy("goblin")
        orc = create_enemy("orc")
        troll = create_enemy("troll")
        dragon = create_enemy("dragon")

        # Check HP progression
        assert slime.max_health < goblin.max_health
        assert goblin.max_health < orc.max_health
        assert orc.max_health < troll.max_health
        assert troll.max_health < dragon.max_health

        # Check reward progression
        assert slime.xp_reward < goblin.xp_reward
        assert goblin.xp_reward < orc.xp_reward
        assert orc.xp_reward < troll.xp_reward
