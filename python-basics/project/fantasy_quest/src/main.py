"""
Fantasy Quest - Main Game Loop
Boot.dev Python Basics Course Project
Created: November 22, 2025
Updated: November 23, 2025 - Location-based RPG transformation

A text-based RPG adventure game featuring:
- Location-based exploration with NPCs
- Character progression with leveling system
- Turn-based combat against various enemies
- Inventory management with equipment
- Quest system with objectives and rewards
- Dynamic NPC relationships and dialogue
"""

from src.core.character import Player
from src.core.inventory import Inventory
from src.core.save_manager import SaveManager
from src.entities.enemy import get_random_enemy
from src.core.combat import combat_loop, process_combat_rewards
from src.entities.quest import QuestLog, QUEST_DATABASE
from src.entities.items import get_item
from src.entities.npc import QuestGiverNPC, MerchantNPC, HealerNPC
from src.world.location import LocationManager
from src.world.locations import create_game_locations, get_starting_location
from src.world.npcs import create_game_npcs, assign_npcs_to_locations
from src.utils.helpers import (
    clear_screen, display_title, display_game_over,
    get_user_choice, get_user_input, pause
)
from src.utils.ascii_art import get_hero_sprite


class Game:
    """Main game controller"""

    def __init__(self):
        """Initialize game state"""
        self.player = None
        self.inventory = None
        self.quest_log = None
        self.location_manager = None
        self.npcs = {}
        self.game_running = True
        self.registered = False
        self.save_manager = SaveManager()

    def start_new_game(self):
        """Initialize a new game with improved intro sequence"""
        display_title()

        # Intro narrative
        print("\nYou awaken in a small village...")
        pause("\nPress Enter to continue...")

        clear_screen()
        print("\n" + "=" * 50)
        print("  THE VILLAGE OF MILLHAVEN")
        print("=" * 50)
        print("\nYour eyes slowly open. You find yourself lying on a")
        print("simple cot in a modest room. Sunlight streams through")
        print("a small window. Your head aches slightly.")
        print("\nYou sit up, trying to remember how you got here.")
        print("The last thing you recall is traveling on the road")
        print("when... something attacked. Everything went dark.")
        print("\nA voice calls from outside:")
        print("'You're finally awake! Come out when you're ready.'")

        pause("\nPress Enter to continue...")

        # Initialize game objects (but no name yet)
        self.player = Player("Traveler")  # Temporary name
        self.inventory = Inventory()
        self.quest_log = QuestLog()

        # Give basic starting items
        self.inventory.add_item(get_item("rusty_sword"))
        self.inventory.add_item(get_item("leather_armor"))
        self.inventory.add_item(get_item("minor_potion"))

        # Initialize world
        self._initialize_world()

        # Start in the village
        self.location_manager.set_current_location("village")

        # First village exploration
        self._first_village_visit()

    def _initialize_world(self):
        """Set up the game world with locations and NPCs"""
        # Create locations
        locations = create_game_locations()

        # Create location manager
        self.location_manager = LocationManager()
        for loc_id, location in locations.items():
            self.location_manager.add_location(loc_id, location)

        # Create NPCs
        self.npcs = create_game_npcs()

        # Assign NPCs to locations
        assign_npcs_to_locations(self.npcs, locations)

    def _first_village_visit(self):
        """Handle the first time entering the village"""
        clear_screen()
        print("\n" + "=" * 50)
        print("  MILLHAVEN VILLAGE")
        print("=" * 50)
        print("\nYou step outside into the village square.")
        print("A peaceful hamlet spreads before you - thatched-roof")
        print("cottages, cobblestone paths, and friendly faces.")
        print("\nBut you notice worry in the villagers' eyes.")
        print("They speak in hushed tones about monsters in the forest.")
        print("\nAn elderly man approaches you with a kind smile.")

        pause("\nPress Enter to continue...")

        # Elder Marcus greets the player
        clear_screen()
        marcus = self.npcs.get("marcus")
        if marcus:
            print(f"\n{marcus.name}: \"Ah, you're the traveler we found")
            print("on the road yesterday! A merchant's cart was attacked")
            print("by goblins. We managed to drive them off and bring")
            print("you here to recover.\"")
            print("\n\"Welcome to Millhaven. I am Elder Marcus, leader of")
            print("this village. I hope you're feeling better?\"")

        pause("\nPress Enter to continue...")

        clear_screen()
        print("\nElder Marcus: \"These are troubled times, I'm afraid.")
        print("Monsters from the Dark Forest have grown bold.")
        print("They attack travelers, threaten our homes...\"")
        print("\n\"But perhaps this is fate! You look capable.")
        print("Have you considered joining the Adventure Guild?")
        print("They coordinate our defense against the monsters.\"")
        print("\n\"The guild hall is just across the square to the west.")
        print("Elena, the receptionist, can get you registered.")
        print("What do you say?\"")

        pause("\nPress Enter to continue...")

        # Now player explores and can register at guild
        print("\nYou are free to explore Millhaven Village.")
        print("Visit the Adventure Guild to register and begin your journey!")

        pause("\nPress Enter to continue...")

    def main_loop(self):
        """Main game loop - location-based exploration"""
        while self.game_running and self.player.is_alive():
            clear_screen()

            # Display current location
            print(self.location_manager.get_current_display())

            # Build menu based on location and state
            menu_options = self._build_location_menu()

            # Always available options
            menu_options.append(("View Character", "character"))
            menu_options.append(("Save Game", "save"))
            menu_options.append(("Quit Game", "quit"))

            # Display menu
            print("\nWhat would you like to do?")
            for i, (display, _) in enumerate(menu_options, 1):
                print(f"{i}. {display}")

            # Get choice
            choice_idx = get_user_choice([str(i) for i in range(1, len(menu_options) + 1)])
            _, action = menu_options[int(choice_idx) - 1]

            # Handle action
            self._handle_action(action)

        if not self.player.is_alive():
            display_game_over(self.player)

    def _build_location_menu(self) -> list:
        """Build menu options based on current location"""
        options = []
        current_loc = self.location_manager.current_location

        if not current_loc:
            return options

        # Location-specific options
        if current_loc.location_type == "guild":
            # Adventure Guild options
            for npc_id in current_loc.npcs:
                options.append((f"Talk to {current_loc.npcs[npc_id].name}", f"talk_{npc_id}"))
            if self.registered:
                options.append(("View Quest Board", "quest_board"))

        elif current_loc.location_type == "shop":
            # Shop options
            for npc_id in current_loc.npcs:
                options.append((f"Talk to {current_loc.npcs[npc_id].name}", f"talk_{npc_id}"))
            options.append(("Browse Wares", "browse_shop"))
            options.append(("Sell Items", "sell_items"))

        elif current_loc.location_type == "tavern":
            # Tavern options
            for npc_id in current_loc.npcs:
                options.append((f"Talk to {current_loc.npcs[npc_id].name}", f"talk_{npc_id}"))
            options.append(("Rest and Heal", "rest"))

        elif current_loc.location_type == "combat":
            # Combat area (forest)
            options.append(("Explore and Hunt", "explore"))
            options.append(("Return to Village", "go_village"))
            return options  # Early return, don't add navigation

        elif current_loc.location_type == "village":
            # Village square
            for npc_id in current_loc.npcs:
                options.append((f"Talk to {current_loc.npcs[npc_id].name}", f"talk_{npc_id}"))

        # Navigation options (for non-combat areas)
        if current_loc.location_type != "combat":
            for direction, dest in current_loc.connections.items():
                options.append((f"Go to {dest.name}", f"go_{direction}"))

        return options

    def _handle_action(self, action: str):
        """Handle player action"""
        if action == "character":
            self.view_character_screen()
        elif action == "save":
            self.prompt_save_game()
        elif action == "quit":
            self.quit_game()
        elif action.startswith("talk_"):
            npc_id = action[5:]
            self.talk_to_npc(npc_id)
        elif action.startswith("go_"):
            direction = action[3:]
            self.navigate(direction)
        elif action == "quest_board":
            self.view_quests()
        elif action == "browse_shop":
            self.browse_shop()
        elif action == "sell_items":
            self.sell_to_merchant()
        elif action == "rest":
            self.rest_at_tavern()
        elif action == "explore":
            self.explore_forest()

    def view_character_screen(self):
        """Unified character, inventory, and equipment screen"""
        while True:
            clear_screen()
            print("\n" + "=" * 50)
            print("  CHARACTER SCREEN")
            print("=" * 50)

            # Character stats
            print(self.player.get_stats())

            # Equipment
            print("\n[EQUIPMENT]")
            if self.inventory.equipped_weapon:
                print(f"  Weapon: {self.inventory.equipped_weapon}")
            else:
                print("  Weapon: None")

            if self.inventory.equipped_armor:
                print(f"  Armor: {self.inventory.equipped_armor}")
            else:
                print("  Armor: None")

            # Inventory
            print(f"\n[INVENTORY] ({len(self.inventory.items)}/{self.inventory.capacity})")
            if self.inventory.items:
                weapons = self.inventory.get_items_by_type("weapon")
                armors = self.inventory.get_items_by_type("armor")
                potions = self.inventory.get_items_by_type("potion")

                if weapons:
                    print("\n  Weapons:")
                    for weapon in weapons:
                        print(f"    - {weapon}")

                if armors:
                    print("\n  Armor:")
                    for armor in armors:
                        print(f"    - {armor}")

                if potions:
                    print("\n  Potions:")
                    for potion in potions:
                        print(f"    - {potion}")
            else:
                print("  (Empty)")

            # Active quests summary
            if self.quest_log.active_quests:
                print(f"\n[ACTIVE QUESTS] ({len(self.quest_log.active_quests)})")
                for quest in self.quest_log.active_quests.values():
                    status = "✓ Ready" if quest.completed else "In Progress"
                    print(f"  - {quest.name} ({status})")

            # Actions
            print("\n" + "=" * 50)
            print("1. Equip Weapon")
            print("2. Equip Armor")
            print("3. Use Potion")
            print("4. Back")

            choice = get_user_choice(["1", "2", "3", "4"])

            if choice == "1":
                self.equip_weapon()
            elif choice == "2":
                self.equip_armor()
            elif choice == "3":
                self.use_potion()
            elif choice == "4":
                break

    def equip_weapon(self):
        """Equip a weapon from inventory"""
        weapons = self.inventory.get_items_by_type("weapon")

        if not weapons:
            print("\n❌ You don't have any weapons to equip!")
            pause()
            return

        print("\nAvailable Weapons:")
        for i, weapon in enumerate(weapons, 1):
            print(f"{i}. {weapon}")
        print(f"{len(weapons) + 1}. Cancel")

        choices = [str(i) for i in range(1, len(weapons) + 2)]
        choice = get_user_choice(choices)

        if choice != str(len(weapons) + 1):
            weapon = weapons[int(choice) - 1]
            old_atk = self.player.attack
            result = self.inventory.equip_weapon(weapon, self.player)
            print(f"\n{result}")
            new_atk = self.player.attack
            if new_atk != old_atk:
                diff = new_atk - old_atk
                sign = "+" if diff > 0 else ""
                print(f"  ATK: {old_atk} -> {new_atk} ({sign}{diff})")
            pause()

    def equip_armor(self):
        """Equip armor from inventory"""
        armors = self.inventory.get_items_by_type("armor")

        if not armors:
            print("\n❌ You don't have any armor to equip!")
            pause()
            return

        print("\nAvailable Armor:")
        for i, armor in enumerate(armors, 1):
            print(f"{i}. {armor}")
        print(f"{len(armors) + 1}. Cancel")

        choices = [str(i) for i in range(1, len(armors) + 2)]
        choice = get_user_choice(choices)

        if choice != str(len(armors) + 1):
            armor = armors[int(choice) - 1]
            old_def = self.player.defense
            result = self.inventory.equip_armor(armor, self.player)
            print(f"\n{result}")
            new_def = self.player.defense
            if new_def != old_def:
                diff = new_def - old_def
                sign = "+" if diff > 0 else ""
                print(f"  DEF: {old_def} -> {new_def} ({sign}{diff})")
            pause()

    def use_potion(self):
        """Use a potion from inventory"""
        potions = self.inventory.get_items_by_type("potion")

        if not potions:
            print("\n❌ You don't have any potions!")
            pause()
            return

        print("\nAvailable Potions:")
        for i, potion in enumerate(potions, 1):
            print(f"{i}. {potion}")
        print(f"{len(potions) + 1}. Cancel")

        choices = [str(i) for i in range(1, len(potions) + 2)]
        choice = get_user_choice(choices)

        if choice != str(len(potions) + 1):
            potion = potions[int(choice) - 1]
            result = self.inventory.use_potion(potion, self.player)
            print(f"\n{result}")
            pause()

    def talk_to_npc(self, npc_id: str):
        """Interact with an NPC"""
        npc = self.npcs.get(npc_id)
        if not npc:
            print(f"\nCouldn't find that person...")
            pause()
            return

        # Special case: Registration with Elena
        if npc_id == "elena" and not self.registered:
            self._register_with_guild(npc)
            return

        # Normal NPC interaction
        while True:
            clear_screen()
            print("\n" + "=" * 50)
            print(f"  Talking to {npc.get_display_name()}")
            print("=" * 50)

            # Greeting
            print(f"\n{npc.get_greeting()}\n")

            # Get dialogue options
            options = npc.get_dialogue_options()

            # Display options
            for i, (display, _) in enumerate(options, 1):
                print(f"{i}. {display}")

            choice_idx = get_user_choice([str(i) for i in range(1, len(options) + 1)])
            _, dialogue_key = options[int(choice_idx) - 1]

            # Special handling for certain dialogue
            if dialogue_key == "leave":
                response = npc.process_dialogue(dialogue_key)
                print(f"\n{response}")
                pause()
                break
            elif dialogue_key == "quests" and isinstance(npc, QuestGiverNPC):
                self._handle_npc_quests(npc)
            elif dialogue_key == "shop" and isinstance(npc, MerchantNPC):
                self.browse_shop()
                break
            elif dialogue_key == "sell" and isinstance(npc, MerchantNPC):
                self.sell_to_merchant()
                break
            elif dialogue_key == "heal" and isinstance(npc, HealerNPC):
                self._handle_npc_healing(npc)
            else:
                # Regular dialogue
                response = npc.process_dialogue(dialogue_key)
                print(f"\n{response}")
                pause()

    def _register_with_guild(self, elena):
        """Handle guild registration with Elena"""
        clear_screen()
        print("\n" + "=" * 50)
        print("  ADVENTURE GUILD REGISTRATION")
        print("=" * 50)

        print(f"\n{elena.get_greeting()}\n")
        print("Elena: \"Welcome to the Millhaven Adventure Guild!\"")
        print("\"Are you here to register as an adventurer?\"")
        print("\n1. Yes, I want to register")
        print("2. Not right now")

        choice = get_user_choice(["1", "2"])

        if choice == "1":
            clear_screen()
            response = elena.process_dialogue("registration")
            print(f"\n{response}\n")

            # Display hero sprite
            hero_sprite = get_hero_sprite()
            if hero_sprite:
                print(hero_sprite)

            pause("\nPress Enter to continue...")

            # Get player name
            clear_screen()
            print("\nElena: \"Let me get some information for our records.\"")
            name = get_user_input("\nWhat is your name? ")

            self.player.name = name
            self.registered = True

            # Give starting quest
            self.quest_log.add_quest(QUEST_DATABASE["goblin_slayer"])

            clear_screen()
            print(f"\nElena: \"Excellent! Welcome aboard, {name}!\"")
            print("\"I've added your first quest to the board.\"")
            print("\"Check the Quest Board here anytime to see your objectives.\"")
            print("\n📜 Quest Added: Goblin Slayer")

            # Relationship boost
            elena.adjust_relationship(10)

            pause("\nPress Enter to continue...")
        else:
            print("\nElena: \"No problem! Come back when you're ready.\"")
            pause()

    def _handle_npc_quests(self, npc: QuestGiverNPC):
        """Handle quest interactions with quest-giver NPC"""
        clear_screen()
        print(f"\n{npc.name}: \"Let me see what quests are available...\"")

        # Check for completable quests
        completed_any = False
        for quest_id, quest in list(self.quest_log.active_quests.items()):
            if quest.completed and not quest.turned_in and quest_id in npc.available_quests:
                print(f"\n✓ {quest.name} - Ready to turn in!")
                print("Turn in this quest?")
                print("1. Yes")
                print("2. No")

                choice = get_user_choice(["1", "2"])
                if choice == "1":
                    result = quest.turn_in(self.player, self.inventory)
                    print(result)
                    self.quest_log.complete_quest(quest_id)
                    npc.complete_quest(quest_id)
                    completed_any = True

                    # Add higher level quests
                    if self.player.level >= 3 and "orc_hunter" not in self.quest_log.active_quests:
                        self.quest_log.add_quest(QUEST_DATABASE["orc_hunter"])
                        npc.add_quest("orc_hunter")
                        print("\n📜 New Quest Available: Orc Hunter")

                    if self.player.level >= 10 and "dragon_slayer" not in self.quest_log.active_quests:
                        self.quest_log.add_quest(QUEST_DATABASE["dragon_slayer"])
                        npc.add_quest("dragon_slayer")
                        print("\n📜 New Quest Available: Dragon Slayer")

                    pause()

        if not completed_any:
            print(f"\n{npc.name}: \"You don't have any completed quests to turn in right now.\"")
            print("\"Keep working on your active objectives!\"")

        pause()

    def _handle_npc_healing(self, npc: HealerNPC):
        """Handle healing interaction with healer NPC"""
        if self.player.current_health == self.player.max_health:
            print(f"\n{npc.name}: \"You're already at full health!\"")
            pause()
            return

        cost = npc.get_heal_cost()
        print(f"\n{npc.name}: \"I can restore your health for {cost} gold.\"")
        print(f"\nCurrent HP: {self.player.current_health}/{self.player.max_health}")
        print(f"Your Gold: {self.player.gold}")
        print("\n1. Yes, please heal me")
        print("2. No thanks")

        choice = get_user_choice(["1", "2"])

        if choice == "1":
            if self.player.spend_gold(cost):
                self.player.current_health = self.player.max_health
                print(f"\n{npc.name}: \"There you go! You should be feeling much better now.\"")
                npc.adjust_relationship(5)
            else:
                print(f"\n{npc.name}: \"You don't have enough gold, I'm afraid.\"")

        pause()

    def navigate(self, direction: str):
        """Navigate to a connected location"""
        if self.location_manager.navigate_to(direction):
            # Successfully moved
            pass
        else:
            print("\nYou can't go that way.")
            pause()

    def browse_shop(self):
        """Browse and buy from shop"""
        sarah = self.npcs.get("sarah")
        if not sarah or not isinstance(sarah, MerchantNPC):
            print("\nNo merchant available here.")
            pause()
            return

        while True:
            clear_screen()
            from src.utils.ascii_art import shop_header
            print(shop_header())

            print(f"\nSarah: \"Welcome! Take a look at what I have in stock.\"")
            print(f"\nYour Gold: {self.player.gold}")
            print(f"Inventory: {len(self.inventory.items)}/{self.inventory.capacity}")

            # Build shop menu
            shop_items = {}
            idx = 1
            print("\nAvailable Items:")
            for item_key, base_price in sarah.shop_inventory.items():
                item = get_item(item_key)
                actual_price = sarah.get_buy_price(base_price)
                print(f"{idx}. {item} - {actual_price} gold")
                shop_items[str(idx)] = (item_key, base_price)
                idx += 1

            print(f"{idx}. Leave Shop")

            choices = [str(i) for i in range(1, idx + 1)]
            choice = get_user_choice(choices)

            if choice == str(idx):
                print("\nSarah: \"Come back anytime!\"")
                pause()
                break

            item_key, base_price = shop_items[choice]

            if self.inventory.is_full():
                print("\n❌ Your inventory is full!")
                pause()
                continue

            actual_price = sarah.get_buy_price(base_price)
            if self.player.spend_gold(actual_price):
                item = get_item(item_key)
                self.inventory.add_item(item)
                print(f"\n✅ Purchased {item.name}!")
                sarah.adjust_relationship(2)
            else:
                print(f"\n❌ Not enough gold! (Need {actual_price}, have {self.player.gold})")

            pause()

    def sell_to_merchant(self):
        """Sell items to merchant"""
        sarah = self.npcs.get("sarah")
        if not sarah or not isinstance(sarah, MerchantNPC):
            print("\nNo merchant available here.")
            pause()
            return

        while True:
            clear_screen()
            print("\n" + "=" * 50)
            print("  SELL ITEMS")
            print("=" * 50)

            sellable = self.inventory.get_sellable_items()

            if not sellable:
                print("\nSarah: \"You don't have anything to sell!\"")
                pause()
                break

            print(f"\nSarah: \"I'll buy items at fair prices.\"")
            print(f"Your Gold: {self.player.gold}\n")

            print("Your Items:")
            for i, item in enumerate(sellable, 1):
                sell_price = sarah.get_sell_price(item.value)
                print(f"{i}. {item.name} - {sell_price} gold")

            print(f"{len(sellable) + 1}. Done selling")

            choices = [str(i) for i in range(1, len(sellable) + 2)]
            choice = get_user_choice(choices)

            if choice == str(len(sellable) + 1):
                break

            item = sellable[int(choice) - 1]
            sell_price = sarah.get_sell_price(item.value)

            if self.inventory.sell_item(item):
                self.player.gain_gold(sell_price)
                print(f"\n✅ Sold {item.name} for {sell_price} gold!")
                sarah.adjust_relationship(1)
                pause()
            else:
                print(f"\n❌ Can't sell that item!")
                pause()

    def rest_at_tavern(self):
        """Rest and heal at tavern"""
        garak = self.npcs.get("garak")
        if garak and isinstance(garak, HealerNPC):
            self._handle_npc_healing(garak)
        else:
            print("\nNo one here can help you rest.")
            pause()

    def explore_forest(self):
        """Explore the Dark Forest and encounter enemies"""
        clear_screen()
        print("\n🗺️  You venture deeper into the Dark Forest...\n")
        pause("Press Enter to continue...")

        # Generate random enemy
        enemy = get_random_enemy(self.player.level)

        # Combat
        victory, rewards = combat_loop(self.player, enemy, self.inventory)

        if victory:
            # Update quest progress
            quest_update_name = f"Defeat {enemy.name}s"
            self.quest_log.update_all(quest_update_name)

            # Process rewards
            process_combat_rewards(self.player, self.inventory, rewards)

            # Check for completed quests
            self._check_quest_completion()

    def _check_quest_completion(self):
        """Check and notify about completed quests"""
        from src.utils.ascii_art import quest_complete_banner

        for quest_id, quest in list(self.quest_log.active_quests.items()):
            if quest.completed and not quest.turned_in:
                clear_screen()
                print(quest_complete_banner())
                print(f"\n{'Quest Completed!':^67}")
                print(f"{quest.name:^67}\n")
                print("Return to the Adventure Guild to turn in this quest!")
                pause()
                break  # Only show one at a time

    def view_quests(self):
        """Display quest log"""
        clear_screen()
        print(self.quest_log.display_quests())
        pause()

    def prompt_save_game(self):
        """Prompt player to save game to a slot"""
        clear_screen()
        print(self.save_manager.format_save_list())
        print("\nChoose a save slot (1-3), or 4 to cancel:")
        choice = get_user_choice(["1", "2", "3", "4"])

        if choice in ["1", "2", "3"]:
            slot = int(choice)
            if self.save_game(slot):
                print(f"\nGame saved to slot {slot}!")
            else:
                print("\nFailed to save game.")
            pause()

    def quit_game(self):
        """Quit the game with save prompt"""
        clear_screen()
        print("\nWould you like to save before quitting?")
        print("1. Save and Quit")
        print("2. Quit without Saving")
        print("3. Cancel")

        choice = get_user_choice(["1", "2", "3"])

        if choice == "1":
            # Prompt for save slot
            clear_screen()
            print(self.save_manager.format_save_list())
            print("\nChoose a save slot (1-3):")
            slot_choice = get_user_choice(["1", "2", "3"])

            if self.save_game(int(slot_choice)):
                print(f"\nGame saved to slot {slot_choice}!")
            else:
                print("\nFailed to save game.")

            pause()
            print(f"\nThanks for playing, {self.player.name}!")
            print(f"Final Level: {self.player.level}")
            print(f"Final Gold: {self.player.gold}")
            self.game_running = False

        elif choice == "2":
            print(f"\nThanks for playing, {self.player.name}!")
            print(f"Final Level: {self.player.level}")
            print(f"Final Gold: {self.player.gold}")
            self.game_running = False

    def save_game(self, slot: int) -> bool:
        """
        Save current game state to a slot

        Args:
            slot: Save slot number (1-3)

        Returns:
            True if save successful, False otherwise
        """
        try:
            # Get current location ID
            current_location_id = None
            for loc_id, location in self.location_manager.locations.items():
                if location == self.location_manager.current_location:
                    current_location_id = loc_id
                    break

            # Serialize NPC states
            npc_states = {}
            for npc_id, npc in self.npcs.items():
                npc_states[npc_id] = npc.to_dict()

            # Build game state dictionary
            game_state = {
                "player": self.player.to_dict(),
                "inventory": self.inventory.to_dict(),
                "quest_log": self.quest_log.to_dict(),
                "current_location_id": current_location_id,
                "registered": self.registered,
                "npc_states": npc_states
            }

            # Save using save manager
            return self.save_manager.save_game(slot, game_state)

        except Exception as e:
            print(f"\nError saving game: {e}")
            return False

    def load_game_state(self, save_data: dict) -> bool:
        """
        Load game state from save data

        Args:
            save_data: Dictionary containing saved game state

        Returns:
            True if load successful, False otherwise
        """
        try:
            # Restore player
            self.player = Player.from_dict(save_data["player"])

            # Restore inventory
            self.inventory = Inventory.from_dict(save_data["inventory"])

            # Apply equipped items to player stats
            if self.inventory.equipped_weapon:
                self.player.attack += self.inventory.equipped_weapon.attack_bonus
            if self.inventory.equipped_armor:
                self.player.defense += self.inventory.equipped_armor.defense_bonus

            # Restore quest log
            self.quest_log = QuestLog.from_dict(save_data["quest_log"])

            # Initialize world
            self._initialize_world()

            # Restore current location
            current_location_id = save_data.get("current_location_id", "village")
            self.location_manager.set_current_location(current_location_id)

            # Restore registered status
            self.registered = save_data.get("registered", False)

            # Restore NPC states
            npc_states = save_data.get("npc_states", {})
            for npc_id, npc_state in npc_states.items():
                if npc_id in self.npcs:
                    self.npcs[npc_id].from_dict(npc_state)

            return True

        except Exception as e:
            print(f"\nError loading game: {e}")
            return False


def show_main_menu():
    """Display main menu and handle selection"""
    game = Game()

    while True:
        clear_screen()
        display_title()
        print("\n" + "=" * 50)
        print("  FANTASY QUEST")
        print("=" * 50)
        print("\n1. New Game")
        print("2. Load Game")
        print("3. Quit")
        print("\n" + "=" * 50)

        choice = get_user_choice(["1", "2", "3"])

        if choice == "1":
            # Start new game
            game.start_new_game()
            game.main_loop()
            break

        elif choice == "2":
            # Load game
            clear_screen()
            print(game.save_manager.format_save_list())
            print("\nChoose a save slot to load (1-3), or 4 to cancel:")
            slot_choice = get_user_choice(["1", "2", "3", "4"])

            if slot_choice in ["1", "2", "3"]:
                slot = int(slot_choice)
                save_data = game.save_manager.load_game(slot)

                if save_data:
                    if game.load_game_state(save_data):
                        print(f"\nGame loaded from slot {slot}!")
                        print(f"Welcome back, {game.player.name}!")
                        pause()
                        game.main_loop()
                        break
                    else:
                        print("\nFailed to load game state.")
                        pause()
                else:
                    print(f"\nNo save found in slot {slot}.")
                    pause()

        elif choice == "3":
            # Quit
            print("\nThanks for playing!")
            break

    print("\nGoodbye!")


def main():
    """Main entry point"""
    show_main_menu()


if __name__ == "__main__":
    main()
