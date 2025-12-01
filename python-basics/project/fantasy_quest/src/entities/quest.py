"""
Quest system for Fantasy Quest
Manages main story and side quests
"""


class Quest:
    """Represents a quest with objectives and rewards"""
    
    def __init__(self, quest_id: str, name: str, description: str, 
                 objectives: dict, rewards: dict, required_level: int = 1):
        """
        Initialize a quest
        
        Args:
            quest_id: Unique quest identifier
            name: Quest name
            description: Quest description
            objectives: Dictionary of objective_name: target_count
            rewards: Dictionary with 'xp', 'gold', 'items' keys
            required_level: Minimum player level to start
        """
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.objectives = objectives
        self.progress = {obj: 0 for obj in objectives}
        self.rewards = rewards
        self.required_level = required_level
        self.completed = False
        self.turned_in = False
    
    def update_progress(self, objective: str, amount: int = 1):
        """
        Update quest objective progress
        
        Args:
            objective: Name of the objective to update
            amount: Amount to increment by
        """
        if objective in self.progress and not self.completed:
            self.progress[objective] = min(
                self.progress[objective] + amount,
                self.objectives[objective]
            )
            self.check_completion()
    
    def check_completion(self):
        """Check if all objectives are complete"""
        for obj, target in self.objectives.items():
            if self.progress[obj] < target:
                return
        self.completed = True
    
    def get_progress_string(self) -> str:
        """Get formatted progress display"""
        output = f"\n[{self.name}]"
        if self.completed:
            output += " ✓ COMPLETE"
        output += f"\n{self.description}\n"
        
        for obj, target in self.objectives.items():
            current = self.progress[obj]
            status = "✓" if current >= target else " "
            output += f"  [{status}] {obj}: {current}/{target}\n"
        
        output += f"\nRewards:\n"
        if self.rewards.get('xp'):
            output += f"  • {self.rewards['xp']} XP\n"
        if self.rewards.get('gold'):
            output += f"  • {self.rewards['gold']} Gold\n"
        if self.rewards.get('items'):
            for item in self.rewards['items']:
                output += f"  • {item}\n"
        
        return output
    
    def turn_in(self, player, inventory) -> str:
        """
        Complete the quest and grant rewards

        Args:
            player: Player character
            inventory: Player's inventory

        Returns:
            Result message
        """
        if not self.completed:
            return "Quest objectives not complete!"

        if self.turned_in:
            return "Quest already turned in!"

        from src.entities.items import get_item

        self.turned_in = True
        message = f"\n🎉 Quest Complete: {self.name}\n"

        # Grant XP
        if self.rewards.get('xp'):
            player.gain_xp(self.rewards['xp'])
            message += f"  Gained {self.rewards['xp']} XP!\n"

        # Grant gold
        if self.rewards.get('gold'):
            player.gain_gold(self.rewards['gold'])
            message += f"  Gained {self.rewards['gold']} gold!\n"

        # Grant items
        if self.rewards.get('items'):
            message += "  Received items:\n"
            for item_key in self.rewards['items']:
                item = get_item(item_key)
                if item and inventory.add_item(item):
                    message += f"    • {item.name}\n"

        return message

    def to_dict(self) -> dict:
        """
        Serialize quest to dictionary

        Returns:
            Dictionary containing quest state
        """
        return {
            "quest_id": self.quest_id,
            "progress": self.progress,
            "completed": self.completed,
            "turned_in": self.turned_in
        }


class QuestLog:
    """Manages all player quests"""
    
    def __init__(self):
        """Initialize quest log"""
        self.active_quests = {}
        self.completed_quests = []
    
    def add_quest(self, quest: Quest):
        """Add a quest to active quests"""
        self.active_quests[quest.quest_id] = quest
    
    def get_quest(self, quest_id: str) -> Quest:
        """Retrieve a quest by ID"""
        return self.active_quests.get(quest_id)
    
    def complete_quest(self, quest_id: str):
        """Move a quest to completed list"""
        if quest_id in self.active_quests:
            quest = self.active_quests.pop(quest_id)
            self.completed_quests.append(quest)
    
    def update_all(self, objective: str, amount: int = 1):
        """Update objective for all active quests"""
        for quest in self.active_quests.values():
            quest.update_progress(objective, amount)
    
    def display_quests(self) -> str:
        """Get formatted quest log display"""
        output = f"\n{'='*50}\n"
        output += "  QUEST LOG\n"
        output += f"{'='*50}\n"

        if self.active_quests:
            output += "\n[ACTIVE QUESTS]\n"
            for quest in self.active_quests.values():
                output += quest.get_progress_string()
                output += "\n"
        else:
            output += "\n[ACTIVE QUESTS]\n  No active quests\n"

        if self.completed_quests:
            output += f"\n[COMPLETED QUESTS] ({len(self.completed_quests)})\n"
            for quest in self.completed_quests:
                output += f"  ✓ {quest.name}\n"

        output += f"{'='*50}\n"
        return output

    def to_dict(self) -> dict:
        """
        Serialize quest log to dictionary

        Returns:
            Dictionary containing all quest states
        """
        return {
            "active_quests": [quest.to_dict() for quest in self.active_quests.values()],
            "completed_quests": [quest.to_dict() for quest in self.completed_quests]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'QuestLog':
        """
        Deserialize quest log from dictionary

        Args:
            data: Dictionary containing quest log state

        Returns:
            Reconstructed QuestLog instance
        """
        quest_log = cls()

        # Restore active quests
        for quest_data in data.get("active_quests", []):
            quest_id = quest_data["quest_id"]

            # Get quest template from database
            if quest_id in QUEST_DATABASE:
                # Create new quest from template
                template = QUEST_DATABASE[quest_id]
                quest = Quest(
                    quest_id=template.quest_id,
                    name=template.name,
                    description=template.description,
                    objectives=template.objectives,
                    rewards=template.rewards,
                    required_level=template.required_level
                )

                # Restore progress and state
                quest.progress = quest_data["progress"]
                quest.completed = quest_data["completed"]
                quest.turned_in = quest_data["turned_in"]

                quest_log.active_quests[quest_id] = quest

        # Restore completed quests
        for quest_data in data.get("completed_quests", []):
            quest_id = quest_data["quest_id"]

            # Get quest template from database
            if quest_id in QUEST_DATABASE:
                # Create new quest from template
                template = QUEST_DATABASE[quest_id]
                quest = Quest(
                    quest_id=template.quest_id,
                    name=template.name,
                    description=template.description,
                    objectives=template.objectives,
                    rewards=template.rewards,
                    required_level=template.required_level
                )

                # Restore progress and state
                quest.progress = quest_data["progress"]
                quest.completed = quest_data["completed"]
                quest.turned_in = quest_data["turned_in"]

                quest_log.completed_quests.append(quest)

        return quest_log


# Predefined quests
QUEST_DATABASE = {
    "goblin_slayer": Quest(
        quest_id="goblin_slayer",
        name="Goblin Slayer",
        description="The village is being terrorized by goblins. Defeat them!",
        objectives={"Defeat Goblins": 5},
        rewards={"xp": 100, "gold": 50, "items": ["health_potion"]},
        required_level=1
    ),
    "orc_hunter": Quest(
        quest_id="orc_hunter",
        name="Orc Hunter",
        description="A band of orcs threatens the kingdom. Hunt them down!",
        objectives={"Defeat Orcs": 3},
        rewards={"xp": 200, "gold": 100, "items": ["iron_sword", "health_potion"]},
        required_level=3
    ),
    "dragon_slayer": Quest(
        quest_id="dragon_slayer",
        name="Dragon Slayer",
        description="An ancient dragon has awakened. Only the bravest can face it!",
        objectives={"Defeat Dragons": 1},
        rewards={"xp": 1000, "gold": 1000, "items": ["legendary_blade", "dragon_armor"]},
        required_level=10
    ),
}
