"""
Location system for Fantasy Quest
Manages game locations, navigation, and spatial awareness
"""

from typing import Dict, List, Optional, Callable


class Location:
    """Base class for all game locations"""

    def __init__(
        self,
        name: str,
        description: str,
        location_type: str = "general"
    ):
        """
        Initialize a location

        Args:
            name: Display name of the location
            description: Detailed description shown when entering
            location_type: Type of location (village, shop, guild, combat, etc.)
        """
        self.name = name
        self.description = description
        self.location_type = location_type
        self.npcs: Dict[str, 'NPC'] = {}  # NPCs present at this location
        self.connections: Dict[str, 'Location'] = {}  # Connected locations
        self.visited = False
        self.actions: Dict[str, Callable] = {}  # Custom actions for this location

    def add_npc(self, npc_id: str, npc: 'NPC'):
        """Add an NPC to this location"""
        self.npcs[npc_id] = npc

    def remove_npc(self, npc_id: str):
        """Remove an NPC from this location"""
        if npc_id in self.npcs:
            del self.npcs[npc_id]

    def add_connection(self, direction: str, location: 'Location'):
        """Add a connection to another location"""
        self.connections[direction] = location

    def get_display(self) -> str:
        """Get formatted location display"""
        output = "\n" + "=" * 50 + "\n"
        output += f"  {self.name}\n"
        output += "=" * 50 + "\n"
        output += f"{self.description}\n"

        if self.npcs:
            output += "\n" + "Present:".ljust(12)
            npc_names = [npc.get_display_name() for npc in self.npcs.values()]
            output += ", ".join(npc_names) + "\n"

        if self.connections:
            output += "\n" + "Exits:".ljust(12)
            exits = [f"{direction} ({loc.name})"
                    for direction, loc in self.connections.items()]
            output += ", ".join(exits) + "\n"

        output += "=" * 50 + "\n"
        return output

    def get_actions(self) -> List[tuple]:
        """
        Get available actions at this location

        Returns:
            List of (display_text, action_key) tuples
        """
        actions = []

        # NPC interactions
        for npc_id, npc in self.npcs.items():
            actions.append((f"Talk to {npc.name}", f"talk_{npc_id}"))

        # Navigation
        for direction, location in self.connections.items():
            actions.append((f"Go {direction} ({location.name})", f"go_{direction}"))

        # Custom location actions
        for action_name in self.actions.keys():
            actions.append((action_name, action_name))

        return actions

    def mark_visited(self):
        """Mark this location as visited"""
        self.visited = True


class LocationManager:
    """Manages game locations and player navigation"""

    def __init__(self):
        """Initialize location manager"""
        self.locations: Dict[str, Location] = {}
        self.current_location: Optional[Location] = None

    def add_location(self, location_id: str, location: Location):
        """Add a location to the game world"""
        self.locations[location_id] = location

    def get_location(self, location_id: str) -> Optional[Location]:
        """Get a location by ID"""
        return self.locations.get(location_id)

    def set_current_location(self, location_id: str):
        """Set the player's current location"""
        if location_id in self.locations:
            self.current_location = self.locations[location_id]
            self.current_location.mark_visited()
            return True
        return False

    def navigate_to(self, direction: str) -> bool:
        """
        Navigate to a connected location

        Args:
            direction: Direction to travel

        Returns:
            True if navigation successful, False otherwise
        """
        if not self.current_location:
            return False

        if direction in self.current_location.connections:
            self.current_location = self.current_location.connections[direction]
            self.current_location.mark_visited()
            return True

        return False

    def get_current_display(self) -> str:
        """Get display for current location"""
        if self.current_location:
            return self.current_location.get_display()
        return "\nYou are nowhere...\n"

    def get_current_actions(self) -> List[tuple]:
        """Get available actions at current location"""
        if self.current_location:
            return self.current_location.get_actions()
        return []
