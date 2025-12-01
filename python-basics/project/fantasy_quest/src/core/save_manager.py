"""
Save/Load system for Fantasy Quest
Handles game state persistence to JSON files
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, List, Tuple


class SaveManager:
    """Manages game save/load operations with JSON files"""

    SAVE_VERSION = "1.0"
    SAVES_DIR = "saves"
    MAX_SLOTS = 3

    def __init__(self):
        """Initialize SaveManager and ensure saves directory exists"""
        self.saves_path = Path(__file__).parent.parent.parent / self.SAVES_DIR
        self._ensure_saves_directory()

    def _ensure_saves_directory(self):
        """Create saves directory if it doesn't exist"""
        if not self.saves_path.exists():
            self.saves_path.mkdir(parents=True, exist_ok=True)

    def _get_save_path(self, slot: int) -> Path:
        """
        Get the file path for a save slot

        Args:
            slot: Save slot number (1-3)

        Returns:
            Path object for the save file

        Raises:
            ValueError: If slot is not between 1 and 3
        """
        if not 1 <= slot <= self.MAX_SLOTS:
            raise ValueError(f"Invalid save slot. Must be between 1 and {self.MAX_SLOTS}.")

        return self.saves_path / f"save_slot_{slot}.json"

    def save_exists(self, slot: int) -> bool:
        """
        Check if a save file exists in the given slot

        Args:
            slot: Save slot number (1-3)

        Returns:
            True if save file exists, False otherwise
        """
        try:
            save_path = self._get_save_path(slot)
            return save_path.exists() and save_path.is_file()
        except ValueError:
            return False

    def save_game(self, game, slot: int) -> Tuple[bool, str]:
        """
        Save complete game state to a slot

        Args:
            game: Game instance containing all game state
            slot: Save slot number (1-3)

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            save_path = self._get_save_path(slot)

            # Build save data structure
            save_data = {
                "version": self.SAVE_VERSION,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "player": self._serialize_player(game.player),
                "inventory": self._serialize_inventory(game.inventory),
                "quests": self._serialize_quests(game.quest_log),
                "npcs": self._serialize_npcs(game.npcs),
                "world_state": {
                    "current_location": game.location_manager.current_location.location_id
                                       if game.location_manager.current_location else "village",
                    "registered": game.registered
                }
            }

            # Write to file with pretty formatting
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            return True, f"Game saved successfully to slot {slot}!"

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Failed to save game: {str(e)}"

    def load_game(self, slot: int) -> Tuple[bool, Optional[Dict], str]:
        """
        Load game state from a slot

        Args:
            slot: Save slot number (1-3)

        Returns:
            Tuple of (success: bool, save_data: dict or None, message: str)
        """
        try:
            save_path = self._get_save_path(slot)

            if not save_path.exists():
                return False, None, f"No save file found in slot {slot}."

            # Read save file
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Validate save version
            if save_data.get("version") != self.SAVE_VERSION:
                return False, None, f"Incompatible save version. Expected {self.SAVE_VERSION}, got {save_data.get('version')}."

            # Validate required fields
            required_fields = ["player", "inventory", "quests", "npcs", "world_state"]
            missing_fields = [field for field in required_fields if field not in save_data]

            if missing_fields:
                return False, None, f"Corrupted save file: missing fields {', '.join(missing_fields)}."

            return True, save_data, f"Game loaded successfully from slot {slot}!"

        except ValueError as e:
            return False, None, str(e)
        except json.JSONDecodeError:
            return False, None, f"Corrupted save file in slot {slot}: invalid JSON format."
        except Exception as e:
            return False, None, f"Failed to load game: {str(e)}"

    def list_saves(self) -> List[Dict]:
        """
        List all available saves with metadata

        Returns:
            List of dictionaries containing save metadata for each slot
            Each dict contains: slot, exists, player_name, level, timestamp, formatted_time
        """
        saves_info = []

        for slot in range(1, self.MAX_SLOTS + 1):
            save_info = {
                "slot": slot,
                "exists": False,
                "player_name": None,
                "level": None,
                "gold": None,
                "location": None,
                "timestamp": None,
                "formatted_time": None
            }

            try:
                save_path = self._get_save_path(slot)

                if save_path.exists():
                    with open(save_path, 'r', encoding='utf-8') as f:
                        save_data = json.load(f)

                    save_info["exists"] = True
                    save_info["player_name"] = save_data.get("player", {}).get("name", "Unknown")
                    save_info["level"] = save_data.get("player", {}).get("level", 1)
                    save_info["gold"] = save_data.get("player", {}).get("gold", 0)
                    save_info["location"] = save_data.get("world_state", {}).get("current_location", "Unknown")
                    save_info["timestamp"] = save_data.get("timestamp")

                    if save_info["timestamp"]:
                        save_info["formatted_time"] = self._format_timestamp(save_info["timestamp"])

            except Exception:
                # If there's an error reading the save, mark it as corrupted
                save_info["exists"] = True
                save_info["player_name"] = "Corrupted Save"
                save_info["formatted_time"] = "Unknown"

            saves_info.append(save_info)

        return saves_info

    def delete_save(self, slot: int) -> Tuple[bool, str]:
        """
        Delete a save slot

        Args:
            slot: Save slot number (1-3)

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            save_path = self._get_save_path(slot)

            if not save_path.exists():
                return False, f"No save file found in slot {slot}."

            save_path.unlink()
            return True, f"Save slot {slot} deleted successfully."

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Failed to delete save: {str(e)}"

    def _format_timestamp(self, timestamp: str) -> str:
        """
        Format ISO timestamp as human-readable relative time

        Args:
            timestamp: ISO format timestamp string

        Returns:
            Formatted string like "2 hours ago", "3 days ago"
        """
        try:
            save_time = datetime.fromisoformat(timestamp)
            now = datetime.now(timezone.utc)

            # Calculate time difference
            delta = now - save_time

            # Format based on time difference
            seconds = delta.total_seconds()

            if seconds < 60:
                return "Just now"
            elif seconds < 3600:
                minutes = int(seconds / 60)
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            elif seconds < 86400:
                hours = int(seconds / 3600)
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif seconds < 604800:
                days = int(seconds / 86400)
                return f"{days} day{'s' if days != 1 else ''} ago"
            elif seconds < 2592000:
                weeks = int(seconds / 604800)
                return f"{weeks} week{'s' if weeks != 1 else ''} ago"
            else:
                months = int(seconds / 2592000)
                return f"{months} month{'s' if months != 1 else ''} ago"

        except Exception:
            return "Unknown"

    # Serialization methods

    def _serialize_player(self, player) -> Dict:
        """
        Serialize player to dictionary

        Args:
            player: Player instance

        Returns:
            Dictionary containing player data
        """
        if hasattr(player, 'to_dict'):
            return player.to_dict()

        # Fallback manual serialization
        return {
            "name": player.name,
            "level": player.level,
            "xp": player.xp,
            "xp_to_level": player.xp_to_level,
            "current_health": player.current_health,
            "max_health": player.max_health,
            "attack": player.attack,
            "defense": player.defense,
            "gold": player.gold
        }

    def _serialize_inventory(self, inventory) -> Dict:
        """
        Serialize inventory to dictionary

        Args:
            inventory: Inventory instance

        Returns:
            Dictionary containing inventory data
        """
        from src.entities.items import Weapon, Armor, Potion, ITEMS_DATABASE

        # Find item keys in database
        def get_item_key(item):
            """Get the database key for an item"""
            for key, db_item in ITEMS_DATABASE.items():
                if (db_item.name == item.name and
                    db_item.item_type == item.item_type):
                    return key
            return None

        # Serialize items list
        items_keys = []
        for item in inventory.items:
            item_key = get_item_key(item)
            if item_key:
                items_keys.append(item_key)

        # Serialize equipped items
        equipped_weapon_key = None
        if inventory.equipped_weapon:
            equipped_weapon_key = get_item_key(inventory.equipped_weapon)

        equipped_armor_key = None
        if inventory.equipped_armor:
            equipped_armor_key = get_item_key(inventory.equipped_armor)

        return {
            "capacity": inventory.capacity,
            "items": items_keys,
            "equipped_weapon": equipped_weapon_key,
            "equipped_armor": equipped_armor_key
        }

    def _serialize_quests(self, quest_log) -> Dict:
        """
        Serialize quest log to dictionary

        Args:
            quest_log: QuestLog instance

        Returns:
            Dictionary containing quest data
        """
        if hasattr(quest_log, 'to_dict'):
            return quest_log.to_dict()

        # Fallback manual serialization
        return {
            "active_quests": [
                {
                    "quest_id": quest.quest_id,
                    "progress": quest.progress,
                    "completed": quest.completed,
                    "turned_in": quest.turned_in
                }
                for quest in quest_log.active_quests.values()
            ],
            "completed_quests": [
                {
                    "quest_id": quest.quest_id,
                    "progress": quest.progress,
                    "completed": quest.completed,
                    "turned_in": quest.turned_in
                }
                for quest in quest_log.completed_quests
            ]
        }

    def _serialize_npcs(self, npcs: Dict) -> Dict:
        """
        Serialize NPC states to dictionary

        Args:
            npcs: Dictionary of NPC instances

        Returns:
            Dictionary containing NPC state data
        """
        npcs_data = {}

        for npc_id, npc in npcs.items():
            npcs_data[npc_id] = {
                "relationship": npc.relationship,
                "first_meeting": npc.first_meeting,
                "conversation_count": npc.conversation_count
            }

            # Save quest-giver specific data
            if hasattr(npc, 'available_quests'):
                npcs_data[npc_id]["available_quests"] = list(npc.available_quests)

            # Save merchant specific data
            if hasattr(npc, 'shop_inventory'):
                npcs_data[npc_id]["shop_inventory"] = dict(npc.shop_inventory)

        return npcs_data

    # Deserialization helper (to be used by Game class)

    @staticmethod
    def deserialize_inventory(inventory_data: Dict, inventory_instance):
        """
        Restore inventory state from serialized data

        Args:
            inventory_data: Dictionary containing inventory data
            inventory_instance: Inventory instance to populate
        """
        from src.entities.items import get_item

        # Clear current inventory
        inventory_instance.items = []
        inventory_instance.equipped_weapon = None
        inventory_instance.equipped_armor = None

        # Restore capacity
        inventory_instance.capacity = inventory_data.get("capacity", 20)

        # Restore items
        for item_key in inventory_data.get("items", []):
            item = get_item(item_key)
            if item:
                inventory_instance.items.append(item)

        # Restore equipped weapon
        equipped_weapon_key = inventory_data.get("equipped_weapon")
        if equipped_weapon_key:
            inventory_instance.equipped_weapon = get_item(equipped_weapon_key)

        # Restore equipped armor
        equipped_armor_key = inventory_data.get("equipped_armor")
        if equipped_armor_key:
            inventory_instance.equipped_armor = get_item(equipped_armor_key)

    @staticmethod
    def deserialize_npcs(npcs_data: Dict, npcs_instances: Dict):
        """
        Restore NPC states from serialized data

        Args:
            npcs_data: Dictionary containing NPC state data
            npcs_instances: Dictionary of NPC instances to update
        """
        for npc_id, npc_state in npcs_data.items():
            if npc_id in npcs_instances:
                npc = npcs_instances[npc_id]

                # Restore common NPC data
                npc.relationship = npc_state.get("relationship", 50)
                npc.first_meeting = npc_state.get("first_meeting", True)
                npc.conversation_count = npc_state.get("conversation_count", 0)

                # Restore quest-giver specific data
                if "available_quests" in npc_state and hasattr(npc, 'available_quests'):
                    npc.available_quests = set(npc_state["available_quests"])

                # Restore merchant specific data
                if "shop_inventory" in npc_state and hasattr(npc, 'shop_inventory'):
                    npc.shop_inventory = dict(npc_state["shop_inventory"])
