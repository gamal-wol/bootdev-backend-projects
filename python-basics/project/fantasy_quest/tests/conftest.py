"""
Shared pytest fixtures for Fantasy Quest tests
"""

import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.character import Player, Character
from src.core.inventory import Inventory
from src.entities.enemy import Enemy, create_enemy
from src.entities.items import Weapon, Armor, Potion, get_item
from src.entities.quest import Quest, QuestLog
from src.main import Game


@pytest.fixture
def sample_player():
    """Create a sample player for testing"""
    return Player("TestHero")


@pytest.fixture
def sample_character():
    """Create a basic character for testing"""
    return Character("TestChar", health=100, attack=15, defense=10)


@pytest.fixture
def sample_enemy():
    """Create a sample enemy for testing"""
    return create_enemy("goblin", level_modifier=1)


@pytest.fixture
def sample_inventory():
    """Create an inventory with some test items"""
    inventory = Inventory()
    inventory.add_item(get_item("rusty_sword"))
    inventory.add_item(get_item("leather_armor"))
    inventory.add_item(get_item("minor_potion"))
    return inventory


@pytest.fixture
def empty_inventory():
    """Create an empty inventory"""
    return Inventory()


@pytest.fixture
def sample_weapon():
    """Create a test weapon"""
    return Weapon("Test Sword", "A test weapon", 100, 20)


@pytest.fixture
def sample_armor():
    """Create a test armor"""
    return Armor("Test Armor", "Test protective gear", 150, 15)


@pytest.fixture
def sample_potion():
    """Create a test potion"""
    return Potion("Test Potion", "Restores health", 50, 75)


@pytest.fixture
def sample_quest():
    """Create a test quest"""
    quest = Quest(
        quest_id="test_quest",
        name="Test Quest",
        description="A test quest for testing",
        objectives={"Defeat Goblins": 5, "Collect Items": 3},
        rewards={"xp": 100, "gold": 50, "items": ["health_potion"]}
    )
    return quest


@pytest.fixture
def quest_log():
    """Create a fresh quest log"""
    return QuestLog()


@pytest.fixture
def fresh_game():
    """Create a fresh Game instance"""
    return Game()


@pytest.fixture
def damaged_player():
    """Create a player with reduced health"""
    player = Player("DamagedHero")
    player.current_health = 50
    return player


@pytest.fixture
def high_level_player():
    """Create a high-level player for testing"""
    player = Player("VeteranHero")
    player.level = 10
    player.max_health = 280
    player.current_health = 280
    player.attack = 37
    player.defense = 23
    player.gold = 500
    return player
