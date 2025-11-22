"""
Fantasy Quest - Main Game Loop
Boot.dev Python Basics Course Project
Created: November 22, 2025

A text-based RPG adventure game featuring:
- Character progression with leveling system
- Turn-based combat against various enemies
- Inventory management with equipment
- Quest system with objectives and rewards
"""

from src.core.character import Player
from src.core.inventory import Inventory
from src.entities.enemy import get_random_enemy
from src.core.combat import combat_loop, process_combat_rewards
from src.entities.quest import QuestLog, QUEST_DATABASE
from src.entities.items import get_item
from src.utils.helpers import (
    clear_screen, display_title, display_game_over,
    get_user_choice, get_user_input, pause
)


class Game:
    """Main game controller"""
    
    def __init__(self):
        """Initialize game state"""
        self.player = None
        self.inventory = None
        self.quest_log = None
        self.game_running = True
    
    def start_new_game(self):
        """Initialize a new game"""
        display_title()
        print("Welcome, brave adventurer!")
        name = get_user_input("\nWhat is your name? ")
        
        self.player = Player(name)
        self.inventory = Inventory()
        self.quest_log = QuestLog()
        
        # Give starting items
        self.inventory.add_item(get_item("rusty_sword"))
        self.inventory.add_item(get_item("leather_armor"))
        self.inventory.add_item(get_item("minor_potion"))
        self.inventory.add_item(get_item("minor_potion"))
        
        # Add starting quest
        self.quest_log.add_quest(QUEST_DATABASE["goblin_slayer"])
        
        clear_screen()
        print(f"\nWelcome to Fantasy Quest, {self.player.name}!")
        print("\nYou awaken in a small village on the edge of a dark forest.")
        print("The villagers speak of monsters threatening the land...")
        print("Your adventure begins now!\n")
        pause()
    
    def main_menu(self):
        """Display and handle main menu"""
        while self.game_running and self.player.is_alive():
            clear_screen()
            print(self.player.get_stats())
            print("\n=== MAIN MENU ===")
            print("1. Explore (Find Enemies)")
            print("2. View Inventory")
            print("3. Manage Equipment")
            print("4. View Quests")
            print("5. Rest (Restore HP)")
            print("6. Visit Shop")
            print("7. Quit Game")
            
            choice = get_user_choice(["1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "1":
                self.explore()
            elif choice == "2":
                self.view_inventory()
            elif choice == "3":
                self.manage_equipment()
            elif choice == "4":
                self.view_quests()
            elif choice == "5":
                self.rest()
            elif choice == "6":
                self.visit_shop()
            elif choice == "7":
                self.quit_game()
        
        if not self.player.is_alive():
            display_game_over(self.player)
    
    def explore(self):
        """Explore and encounter enemies"""
        clear_screen()
        print("\n🗺️  You venture into the wilderness...\n")
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
            self.check_quest_completion()
    
    def view_inventory(self):
        """Display inventory"""
        clear_screen()
        print(self.inventory.display_inventory())
        pause()
    
    def manage_equipment(self):
        """Equipment management menu"""
        while True:
            clear_screen()
            print(self.inventory.display_inventory())
            print("\n=== EQUIPMENT MANAGEMENT ===")
            print("1. Equip Weapon")
            print("2. Equip Armor")
            print("3. Use Potion")
            print("4. Back to Main Menu")
            
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
            result = self.inventory.equip_weapon(weapon, self.player)
            print(f"\n{result}")
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
            result = self.inventory.equip_armor(armor, self.player)
            print(f"\n{result}")
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
    
    def view_quests(self):
        """Display quest log"""
        clear_screen()
        print(self.quest_log.display_quests())
        pause()
    
    def check_quest_completion(self):
        """Check and handle completed quests"""
        for quest_id, quest in list(self.quest_log.active_quests.items()):
            if quest.completed and not quest.turned_in:
                print(f"\n🎉 Quest Ready to Turn In: {quest.name}")
                print("Turn in this quest now?")
                print("1. Yes")
                print("2. Later")
                
                choice = get_user_choice(["1", "2"])
                
                if choice == "1":
                    result = quest.turn_in(self.player, self.inventory)
                    print(result)
                    self.quest_log.complete_quest(quest_id)
                    
                    # Add new quests based on level
                    if self.player.level >= 3 and "orc_hunter" not in self.quest_log.active_quests:
                        self.quest_log.add_quest(QUEST_DATABASE["orc_hunter"])
                        print("\n📜 New Quest Available: Orc Hunter")
                    
                    if self.player.level >= 10 and "dragon_slayer" not in self.quest_log.active_quests:
                        self.quest_log.add_quest(QUEST_DATABASE["dragon_slayer"])
                        print("\n📜 New Quest Available: Dragon Slayer")
                    
                    pause()
    
    def rest(self):
        """Rest to restore HP"""
        clear_screen()
        cost = 20
        
        if self.player.current_health == self.player.max_health:
            print("\n❌ You're already at full health!")
            pause()
            return
        
        print(f"\n🏕️  Rest at the inn? (Cost: {cost} gold)")
        print(f"Current HP: {self.player.current_health}/{self.player.max_health}")
        print(f"Your Gold: {self.player.gold}")
        print("\n1. Yes")
        print("2. No")
        
        choice = get_user_choice(["1", "2"])
        
        if choice == "1":
            if self.player.spend_gold(cost):
                self.player.current_health = self.player.max_health
                print(f"\n✅ You rest and recover to full health!")
            else:
                print(f"\n❌ Not enough gold! (Need {cost}, have {self.player.gold})")
        
        pause()
    
    def visit_shop(self):
        """Visit the shop to buy items"""
        shop_items = {
            "1": ("minor_potion", "Minor Health Potion", 15),
            "2": ("health_potion", "Health Potion", 30),
            "3": ("greater_potion", "Greater Health Potion", 60),
            "4": ("iron_sword", "Iron Sword", 50),
            "5": ("iron_armor", "Iron Armor", 75),
        }
        
        while True:
            clear_screen()
            print(f"\n{'='*50}")
            print("🏪 SHOP")
            print(f"{'='*50}")
            print(f"Your Gold: {self.player.gold}")
            print(f"Inventory: {len(self.inventory.items)}/{self.inventory.capacity}")
            print("\nAvailable Items:")
            
            for key, (item_key, name, price) in shop_items.items():
                print(f"{key}. {name} - {price} gold")
            print(f"{len(shop_items) + 1}. Leave Shop")
            
            choices = [str(i) for i in range(1, len(shop_items) + 2)]
            choice = get_user_choice(choices)
            
            if choice == str(len(shop_items) + 1):
                break
            
            item_key, name, price = shop_items[choice]
            
            if self.inventory.is_full():
                print("\n❌ Your inventory is full!")
                pause()
                continue
            
            if self.player.spend_gold(price):
                item = get_item(item_key)
                self.inventory.add_item(item)
                print(f"\n✅ Purchased {name}!")
            else:
                print(f"\n❌ Not enough gold! (Need {price}, have {self.player.gold})")
            
            pause()
    
    def quit_game(self):
        """Quit the game"""
        clear_screen()
        print("\nAre you sure you want to quit?")
        print("1. Yes")
        print("2. No")
        
        choice = get_user_choice(["1", "2"])
        
        if choice == "1":
            print(f"\nThanks for playing, {self.player.name}!")
            print(f"Final Level: {self.player.level}")
            print(f"Final Gold: {self.player.gold}")
            self.game_running = False


def main():
    """Main entry point"""
    game = Game()
    game.start_new_game()
    game.main_menu()
    print("\nGoodbye! ⚔️")


if __name__ == "__main__":
    main()
