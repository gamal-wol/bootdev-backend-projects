"""
Tests for quest system
"""

import pytest
from src.entities.quest import Quest, QuestLog, QUEST_DATABASE
from src.core.character import Player
from src.core.inventory import Inventory


class TestQuest:
    """Tests for Quest class"""

    def test_quest_initialization(self, sample_quest):
        """Test Quest initialization with all attributes"""
        # Verify all attributes set
        assert sample_quest.quest_id == "test_quest"
        assert sample_quest.name == "Test Quest"
        assert sample_quest.description == "A test quest for testing"
        assert sample_quest.objectives == {"Defeat Goblins": 5, "Collect Items": 3}

        # Check progress dict initialized to 0s
        assert sample_quest.progress == {"Defeat Goblins": 0, "Collect Items": 0}

        # Assert completed = False, turned_in = False
        assert sample_quest.completed is False
        assert sample_quest.turned_in is False

    def test_quest_update_progress_single_objective(self, sample_quest):
        """Test updating progress for a single objective"""
        # Call update_progress()
        sample_quest.update_progress("Defeat Goblins", 1)

        # Verify progress increments
        assert sample_quest.progress["Defeat Goblins"] == 1
        assert sample_quest.completed is False  # Not complete yet

    def test_quest_update_progress_multiple_increments(self, sample_quest):
        """Test multiple progress updates"""
        # Update same objective multiple times
        sample_quest.update_progress("Defeat Goblins", 2)
        sample_quest.update_progress("Defeat Goblins", 1)

        # Verify cumulative increase
        assert sample_quest.progress["Defeat Goblins"] == 3

    def test_quest_update_progress_capped_at_target(self, sample_quest):
        """Test that progress doesn't exceed objective target"""
        # Update progress beyond target
        sample_quest.update_progress("Defeat Goblins", 10)

        # Verify doesn't exceed objective target
        assert sample_quest.progress["Defeat Goblins"] == 5  # Capped at objective
        assert sample_quest.progress["Defeat Goblins"] <= sample_quest.objectives["Defeat Goblins"]

    def test_quest_check_completion_incomplete(self, sample_quest):
        """Test completion check when quest is incomplete"""
        # Complete only some objectives
        sample_quest.update_progress("Defeat Goblins", 5)  # Complete this one
        sample_quest.update_progress("Collect Items", 1)   # Not complete

        # Verify completed = False
        assert sample_quest.completed is False

    def test_quest_check_completion_complete(self, sample_quest):
        """Test completion check when all objectives met"""
        # Complete all objectives
        sample_quest.update_progress("Defeat Goblins", 5)
        sample_quest.update_progress("Collect Items", 3)

        # Verify completed = True
        assert sample_quest.completed is True

    def test_quest_get_progress_string_incomplete(self, sample_quest):
        """Test progress string display for incomplete quest"""
        sample_quest.update_progress("Defeat Goblins", 2)

        # Call get_progress_string()
        progress_str = sample_quest.get_progress_string()

        # Verify shows progress for each objective
        assert "Test Quest" in progress_str
        assert "Defeat Goblins" in progress_str
        assert "2/5" in progress_str
        assert "Collect Items" in progress_str
        assert "0/3" in progress_str

        # Check reward section included
        assert "Rewards" in progress_str or "rewards" in progress_str

    def test_quest_get_progress_string_complete(self, sample_quest):
        """Test progress string for completed quest"""
        # Complete quest
        sample_quest.update_progress("Defeat Goblins", 5)
        sample_quest.update_progress("Collect Items", 3)

        progress_str = sample_quest.get_progress_string()

        # Verify "COMPLETE" marker shown
        assert "COMPLETE" in progress_str

    def test_quest_turn_in_success(self, sample_quest, sample_player, empty_inventory):
        """Test successful quest turn-in"""
        # Complete quest
        sample_quest.update_progress("Defeat Goblins", 5)
        sample_quest.update_progress("Collect Items", 3)

        initial_xp = sample_player.xp
        initial_gold = sample_player.gold
        initial_items = len(empty_inventory.items)

        # Call turn_in() with player and inventory
        result = sample_quest.turn_in(sample_player, empty_inventory)

        # Verify player gains XP and gold
        assert sample_player.xp == initial_xp + sample_quest.rewards["xp"]
        assert sample_player.gold == initial_gold + sample_quest.rewards["gold"]

        # Check items added to inventory
        assert len(empty_inventory.items) > initial_items

        # Assert turned_in = True
        assert sample_quest.turned_in is True

        # Check return message
        assert isinstance(result, str)
        assert "Complete" in result or "complete" in result

    def test_quest_turn_in_incomplete(self, sample_quest, sample_player, empty_inventory):
        """Test turning in incomplete quest"""
        # Quest not completed
        sample_quest.update_progress("Defeat Goblins", 2)  # Only partial

        # Call turn_in()
        result = sample_quest.turn_in(sample_player, empty_inventory)

        # Verify error message
        assert "not complete" in result.lower()

        # Check turned_in remains False
        assert sample_quest.turned_in is False

    def test_quest_turn_in_already_turned_in(self, sample_quest, sample_player, empty_inventory):
        """Test turning in quest twice"""
        # Complete and turn in quest
        sample_quest.update_progress("Defeat Goblins", 5)
        sample_quest.update_progress("Collect Items", 3)
        sample_quest.turn_in(sample_player, empty_inventory)

        initial_xp = sample_player.xp

        # Try to turn in again
        result = sample_quest.turn_in(sample_player, empty_inventory)

        # Verify error message
        assert "already" in result.lower()

        # Check no additional XP granted
        assert sample_player.xp == initial_xp


class TestQuestLog:
    """Tests for QuestLog class"""

    def test_quest_log_initialization(self, quest_log):
        """Test QuestLog initialization"""
        # Verify empty state
        assert len(quest_log.active_quests) == 0
        assert len(quest_log.completed_quests) == 0

    def test_quest_log_add_quest(self, quest_log, sample_quest):
        """Test adding quest to quest log"""
        # Add quest
        quest_log.add_quest(sample_quest)

        # Verify in active_quests
        assert sample_quest.quest_id in quest_log.active_quests
        assert quest_log.active_quests[sample_quest.quest_id] == sample_quest

    def test_quest_log_get_quest(self, quest_log, sample_quest):
        """Test retrieving quest by ID"""
        quest_log.add_quest(sample_quest)

        # Retrieve quest
        retrieved = quest_log.get_quest("test_quest")

        # Verify correct quest returned
        assert retrieved == sample_quest

    def test_quest_log_complete_quest(self, quest_log, sample_quest):
        """Test moving quest to completed"""
        # Add quest to log
        quest_log.add_quest(sample_quest)

        # Complete and turn in
        sample_quest.update_progress("Defeat Goblins", 5)
        sample_quest.update_progress("Collect Items", 3)
        sample_quest.turned_in = True

        # Call complete_quest()
        quest_log.complete_quest(sample_quest.quest_id)

        # Verify moved to completed_quests
        assert sample_quest in quest_log.completed_quests

        # Check removed from active_quests
        assert sample_quest.quest_id not in quest_log.active_quests

    def test_quest_log_update_all(self, quest_log):
        """Test updating all quests with matching objective"""
        # Add multiple quests
        quest1 = Quest(
            quest_id="q1",
            name="Quest 1",
            description="Test",
            objectives={"Defeat Goblins": 3},
            rewards={"xp": 50}
        )
        quest2 = Quest(
            quest_id="q2",
            name="Quest 2",
            description="Test",
            objectives={"Defeat Goblins": 5, "Collect Items": 2},
            rewards={"xp": 100}
        )

        quest_log.add_quest(quest1)
        quest_log.add_quest(quest2)

        # Call update_all() with objective name
        quest_log.update_all("Defeat Goblins", 1)

        # Verify all matching objectives updated
        assert quest1.progress["Defeat Goblins"] == 1
        assert quest2.progress["Defeat Goblins"] == 1
        assert quest2.progress["Collect Items"] == 0  # Not updated

    def test_quest_log_display_quests_empty(self, quest_log):
        """Test display with no quests"""
        # Call display_quests()
        display = quest_log.display_quests()

        # Verify contains "No active quests"
        assert "No active quests" in display or "no active" in display.lower()

    def test_quest_log_display_quests(self, quest_log, sample_quest):
        """Test quest log display"""
        # Add active and completed quests
        quest_log.add_quest(sample_quest)

        completed_quest = Quest(
            quest_id="completed",
            name="Completed Quest",
            description="Done",
            objectives={"Test": 1},
            rewards={"xp": 10}
        )
        completed_quest.update_progress("Test", 1)
        completed_quest.turned_in = True
        quest_log.completed_quests.append(completed_quest)

        # Call display_quests()
        display = quest_log.display_quests()

        # Verify formatted output includes both sections
        assert "QUEST LOG" in display
        assert "ACTIVE QUESTS" in display
        assert sample_quest.name in display
        assert "COMPLETED QUESTS" in display
        assert completed_quest.name in display


class TestQuestDatabase:
    """Tests for predefined quests"""

    def test_quest_database_contains_main_quests(self):
        """Verify quest database has expected quests"""
        # Check main quests exist
        assert "goblin_slayer" in QUEST_DATABASE
        assert "orc_hunter" in QUEST_DATABASE
        assert "dragon_slayer" in QUEST_DATABASE

    def test_quest_database_quests_valid(self):
        """Verify all quests in database are properly configured"""
        for quest_id, quest in QUEST_DATABASE.items():
            assert quest.quest_id == quest_id
            assert quest.name is not None
            assert quest.description is not None
            assert len(quest.objectives) > 0
            assert "xp" in quest.rewards or "gold" in quest.rewards
