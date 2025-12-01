"""
NPC system for Fantasy Quest
Manages non-player characters with dialogue and relationships
"""

from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum


class NPCRole(Enum):
    """NPC role types"""
    QUEST_GIVER = "quest_giver"
    MERCHANT = "merchant"
    HEALER = "healer"
    TRAINER = "trainer"
    VILLAGER = "villager"


class NPC:
    """Base class for all NPCs"""

    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        role: NPCRole = NPCRole.VILLAGER
    ):
        """
        Initialize an NPC

        Args:
            name: NPC's name
            title: NPC's title/job
            description: Physical description or personality
            role: NPC's primary role
        """
        self.name = name
        self.title = title
        self.description = description
        self.role = role
        self.relationship = 50  # 0-100 scale, starts neutral at 50
        self.dialogue_tree: Dict[str, Dict] = {}
        self.first_meeting = True
        self.conversation_count = 0
        self.services: List[str] = []

    def get_display_name(self) -> str:
        """Get formatted display name"""
        return f"{self.name} ({self.title})"

    def adjust_relationship(self, amount: int):
        """
        Adjust relationship level

        Args:
            amount: Amount to adjust (positive or negative)
        """
        self.relationship = max(0, min(100, self.relationship + amount))

    def get_relationship_tier(self) -> str:
        """Get relationship tier name"""
        if self.relationship < 20:
            return "Hostile"
        elif self.relationship < 40:
            return "Unfriendly"
        elif self.relationship < 60:
            return "Neutral"
        elif self.relationship < 80:
            return "Friendly"
        else:
            return "Trusted"

    def add_dialogue(self, dialogue_key: str, dialogue_data: Dict):
        """
        Add dialogue option

        Args:
            dialogue_key: Unique identifier for this dialogue
            dialogue_data: Dict with 'text', 'options', 'conditions', etc.
        """
        self.dialogue_tree[dialogue_key] = dialogue_data

    def get_greeting(self) -> str:
        """Get appropriate greeting based on relationship and history"""
        if self.first_meeting:
            return self._get_first_greeting()
        else:
            return self._get_regular_greeting()

    def _get_first_greeting(self) -> str:
        """Get greeting for first meeting"""
        return f"{self.name}: \"Greetings, traveler. I haven't seen you around before.\""

    def _get_regular_greeting(self) -> str:
        """Get greeting for returning visitor"""
        tier = self.get_relationship_tier()
        if tier == "Hostile":
            return f"{self.name}: \"You again...\""
        elif tier == "Unfriendly":
            return f"{self.name}: \"Oh. It's you.\""
        elif tier == "Neutral":
            return f"{self.name}: \"Hello again.\""
        elif tier == "Friendly":
            return f"{self.name}: \"Good to see you!\""
        else:  # Trusted
            return f"{self.name}: \"Ah, my friend! Welcome back!\""

    def get_dialogue_options(self, context: Dict = None) -> List[Tuple[str, str]]:
        """
        Get available dialogue options

        Args:
            context: Game context (player, quests, etc.)

        Returns:
            List of (display_text, dialogue_key) tuples
        """
        options = []

        # Base dialogue options available to all NPCs
        options.append(("Ask about themselves", "about"))
        options.append(("Small talk", "chat"))

        # Role-specific options
        if self.role == NPCRole.QUEST_GIVER:
            options.append(("Ask about quests", "quests"))
        elif self.role == NPCRole.MERCHANT:
            options.append(("Browse wares", "shop"))
            options.append(("Sell items", "sell"))
        elif self.role == NPCRole.HEALER:
            options.append(("Request healing", "heal"))

        # Add custom dialogue from dialogue tree
        for key, data in self.dialogue_tree.items():
            if self._check_dialogue_conditions(data, context):
                display = data.get("display", key)
                options.append((display, key))

        options.append(("Goodbye", "leave"))

        return options

    def _check_dialogue_conditions(self, dialogue_data: Dict, context: Dict = None) -> bool:
        """
        Check if dialogue option should be available

        Args:
            dialogue_data: Dialogue data with potential conditions
            context: Game context

        Returns:
            True if conditions met, False otherwise
        """
        if "conditions" not in dialogue_data:
            return True

        conditions = dialogue_data["conditions"]

        # Check relationship requirement
        if "min_relationship" in conditions:
            if self.relationship < conditions["min_relationship"]:
                return False

        # Check if first meeting only
        if conditions.get("first_meeting_only", False):
            if not self.first_meeting:
                return False

        # Context-based conditions would go here
        # (e.g., quest status, player level, items owned)

        return True

    def process_dialogue(self, dialogue_key: str, context: Dict = None) -> str:
        """
        Process dialogue selection and return response

        Args:
            dialogue_key: Selected dialogue option
            context: Game context

        Returns:
            NPC's response text
        """
        # Mark no longer first meeting
        if self.first_meeting:
            self.first_meeting = False
            self.adjust_relationship(5)  # Small boost for talking first time

        self.conversation_count += 1

        # Handle standard dialogue
        if dialogue_key == "about":
            return self._dialogue_about()
        elif dialogue_key == "chat":
            return self._dialogue_chat()
        elif dialogue_key == "leave":
            return self._dialogue_leave()

        # Handle custom dialogue from tree
        if dialogue_key in self.dialogue_tree:
            dialogue_data = self.dialogue_tree[dialogue_key]
            return dialogue_data.get("text", "...")

        return f"{self.name}: \"I don't understand.\""

    def _dialogue_about(self) -> str:
        """Response when asked about themselves"""
        return f"{self.name}: \"{self.description}\""

    def _dialogue_chat(self) -> str:
        """Response for small talk"""
        self.adjust_relationship(1)  # Small relationship boost
        tier = self.get_relationship_tier()

        if tier in ["Hostile", "Unfriendly"]:
            return f"{self.name}: \"I don't have time for idle chatter.\""
        elif tier == "Neutral":
            return f"{self.name}: \"The weather's been decent lately.\""
        elif tier == "Friendly":
            return f"{self.name}: \"Things have been going well, thank you for asking!\""
        else:  # Trusted
            return f"{self.name}: \"You know, I really appreciate our talks. It's nice to have a friend like you.\""

    def _dialogue_leave(self) -> str:
        """Response when saying goodbye"""
        tier = self.get_relationship_tier()

        if tier in ["Hostile", "Unfriendly"]:
            return f"{self.name}: \"Fine.\""
        elif tier == "Neutral":
            return f"{self.name}: \"Farewell.\""
        elif tier == "Friendly":
            return f"{self.name}: \"Take care!\""
        else:  # Trusted
            return f"{self.name}: \"Safe travels, my friend!\""

    def to_dict(self) -> dict:
        """
        Serialize NPC relationship state to dictionary

        Returns:
            Dictionary containing NPC state
        """
        return {
            "relationship": self.relationship,
            "first_meeting": self.first_meeting,
            "conversation_count": self.conversation_count
        }

    def from_dict(self, data: dict):
        """
        Load NPC relationship state from dictionary

        Args:
            data: Dictionary containing NPC state
        """
        self.relationship = data.get("relationship", 50)
        self.first_meeting = data.get("first_meeting", True)
        self.conversation_count = data.get("conversation_count", 0)


class QuestGiverNPC(NPC):
    """NPC specialized in giving quests"""

    def __init__(self, name: str, title: str, description: str):
        super().__init__(name, title, description, NPCRole.QUEST_GIVER)
        self.available_quests: List[str] = []  # Quest IDs
        self.completed_quests: List[str] = []

    def add_quest(self, quest_id: str):
        """Add quest to this NPC's available quests"""
        if quest_id not in self.available_quests:
            self.available_quests.append(quest_id)

    def complete_quest(self, quest_id: str):
        """Mark quest as completed"""
        if quest_id in self.available_quests:
            self.available_quests.remove(quest_id)
        if quest_id not in self.completed_quests:
            self.completed_quests.append(quest_id)
            self.adjust_relationship(10)  # Significant boost for quest completion

    def to_dict(self) -> dict:
        """
        Serialize QuestGiverNPC state to dictionary

        Returns:
            Dictionary containing QuestGiverNPC state
        """
        data = super().to_dict()
        data["completed_quests"] = self.completed_quests
        return data

    def from_dict(self, data: dict):
        """
        Load QuestGiverNPC state from dictionary

        Args:
            data: Dictionary containing QuestGiverNPC state
        """
        super().from_dict(data)
        self.completed_quests = data.get("completed_quests", [])


class MerchantNPC(NPC):
    """NPC specialized in trading"""

    def __init__(self, name: str, title: str, description: str):
        super().__init__(name, title, description, NPCRole.MERCHANT)
        self.shop_inventory: Dict[str, int] = {}  # item_id: price
        self.buy_back_rate = 0.5  # Buy items at 50% of value

    def set_inventory(self, inventory: Dict[str, int]):
        """Set merchant's shop inventory"""
        self.shop_inventory = inventory

    def get_sell_price(self, item_value: int) -> int:
        """Get price merchant will pay for an item"""
        base_price = int(item_value * self.buy_back_rate)

        # Relationship affects sell price
        tier = self.get_relationship_tier()
        if tier == "Trusted":
            return int(base_price * 1.2)  # 20% bonus
        elif tier == "Friendly":
            return int(base_price * 1.1)  # 10% bonus
        elif tier in ["Hostile", "Unfriendly"]:
            return int(base_price * 0.8)  # 20% penalty

        return base_price

    def get_buy_price(self, base_price: int) -> int:
        """Get price player pays to buy an item"""
        # Relationship affects buy price
        tier = self.get_relationship_tier()
        if tier == "Trusted":
            return int(base_price * 0.9)  # 10% discount
        elif tier == "Friendly":
            return int(base_price * 0.95)  # 5% discount
        elif tier in ["Hostile", "Unfriendly"]:
            return int(base_price * 1.2)  # 20% markup

        return base_price


class HealerNPC(NPC):
    """NPC specialized in healing"""

    def __init__(self, name: str, title: str, description: str, heal_cost: int = 20):
        super().__init__(name, title, description, NPCRole.HEALER)
        self.heal_cost = heal_cost

    def get_heal_cost(self) -> int:
        """Get cost for healing service"""
        # Relationship affects healing cost
        tier = self.get_relationship_tier()
        if tier == "Trusted":
            return int(self.heal_cost * 0.5)  # 50% discount
        elif tier == "Friendly":
            return int(self.heal_cost * 0.75)  # 25% discount
        elif tier in ["Hostile", "Unfriendly"]:
            return int(self.heal_cost * 1.5)  # 50% markup

        return self.heal_cost
