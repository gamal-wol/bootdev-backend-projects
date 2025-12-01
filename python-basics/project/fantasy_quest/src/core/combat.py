"""
Combat system for Fantasy Quest
Handles turn-based battles between player and enemies
"""

import random
from src.utils.helpers import get_user_choice, clear_screen
from src.utils.ascii_art import get_enemy_sprite, get_hero_sprite, victory_banner, defeat_banner


def calculate_damage(attacker, defender) -> int:
    """
    Calculate damage dealt in an attack
    
    Args:
        attacker: Character performing the attack
        defender: Character being attacked
        
    Returns:
        Damage amount
    """
    # Base damage with some randomness (80-120% of attack stat)
    base_damage = attacker.attack * random.uniform(0.8, 1.2)
    # Apply defender's defense
    damage = max(1, int(base_damage - defender.defense))
    return damage


def player_turn(player, enemy, inventory) -> tuple[bool, str]:
    """
    Handle player's turn in combat
    
    Args:
        player: Player character
        enemy: Enemy being fought
        inventory: Player's inventory
        
    Returns:
        Tuple of (combat_continues, action_message)
    """
    print(f"\n{player.name}: {player.current_health}/{player.max_health} HP")
    print(f"{enemy.name}: {enemy.current_health}/{enemy.max_health} HP")
    print("\nWhat will you do?")
    print("1. Attack")
    print("2. Use Potion")
    print("3. Try to Flee")
    
    choice = get_user_choice(["1", "2", "3"])
    
    if choice == "1":
        # Attack
        damage = calculate_damage(player, enemy)
        enemy.take_damage(damage)
        message = f"\n⚔️  {player.name} attacks {enemy.name} for {damage} damage!"
        
        if not enemy.is_alive():
            message += f"\n💀 {enemy.name} has been defeated!"
            return False, message
        
        return True, message
    
    elif choice == "2":
        # Use potion
        potions = inventory.get_items_by_type("potion")
        
        if not potions:
            return True, "\n❌ You don't have any potions!"
        
        print("\nAvailable Potions:")
        for i, potion in enumerate(potions, 1):
            print(f"{i}. {potion}")
        print(f"{len(potions) + 1}. Cancel")
        
        choices = [str(i) for i in range(1, len(potions) + 2)]
        potion_choice = get_user_choice(choices)
        
        if potion_choice == str(len(potions) + 1):
            return True, "\n↩️  Cancelled"
        
        potion = potions[int(potion_choice) - 1]
        message = f"\n🧪 {inventory.use_potion(potion, player)}"
        return True, message
    
    else:  # choice == "3"
        # Try to flee (50% chance)
        if random.random() < 0.5:
            return False, f"\n🏃 {player.name} fled from battle!"
        else:
            return True, f"\n❌ Couldn't escape!"


def enemy_turn(enemy, player) -> str:
    """
    Handle enemy's turn in combat
    
    Args:
        enemy: Enemy character
        player: Player being attacked
        
    Returns:
        Action message
    """
    damage = calculate_damage(enemy, player)
    player.take_damage(damage)
    return f"\n🗡️  {enemy.name} attacks {player.name} for {damage} damage!"


def combat_loop(player, enemy, inventory) -> tuple[bool, dict]:
    """
    Main combat loop
    
    Args:
        player: Player character
        enemy: Enemy to fight
        inventory: Player's inventory
        
    Returns:
        Tuple of (player_won, rewards_dict)
    """
    clear_screen()
    print(f"\n{'='*67}")
    print(f"                  ⚔️  A wild {enemy.name} appears!  ⚔️")
    print(f"{'='*67}")
    
    # Display hero and enemy sprites side by side
    hero_sprite = get_hero_sprite()
    enemy_sprite = get_enemy_sprite(enemy.name)
    
    if hero_sprite and enemy_sprite:
        # Split sprites into lines for side-by-side display
        hero_lines = hero_sprite.strip().split('\n')
        enemy_lines = enemy_sprite.strip().split('\n')
        
        # Pad to same height
        max_height = max(len(hero_lines), len(enemy_lines))
        hero_lines += [''] * (max_height - len(hero_lines))
        enemy_lines += [''] * (max_height - len(enemy_lines))
        
        # Display side by side with spacing
        print()
        for hero_line, enemy_line in zip(hero_lines, enemy_lines):
            print(f"  {hero_line:25}     {enemy_line}")
        print()
    elif enemy_sprite:
        # Fallback: just show enemy sprite if hero sprite not available
        print(enemy_sprite)
    
    input("\nPress Enter to begin battle...")
    
    fled = False
    
    while player.is_alive() and enemy.is_alive():
        # Player turn
        continue_combat, message = player_turn(player, enemy, inventory)
        print(message)
        
        if not continue_combat:
            if not enemy.is_alive():
                # Victory!
                break
            else:
                # Player fled
                fled = True
                break
        
        if not enemy.is_alive():
            break
        
        # Enemy turn
        enemy_message = enemy_turn(enemy, player)
        print(enemy_message)
        
        if not player.is_alive():
            break
        
        input("\nPress Enter to continue...")
    
    # Determine outcome
    if fled:
        return False, {}
    elif player.is_alive():
        # Player won - show victory with hero sprite
        clear_screen()
        print(victory_banner())
        
        hero_sprite = get_hero_sprite()
        if hero_sprite:
            print(hero_sprite)
        
        print(f"\n🎉 {player.name} defeated the {enemy.name}! 🎉")
        
        rewards = {
            "xp": enemy.xp_reward,
            "gold": enemy.gold_reward,
            "loot": enemy.get_loot()
        }
        return True, rewards
    else:
        # Player died - show defeat banner
        clear_screen()
        print(defeat_banner())
        print(f"\n{player.name} was defeated by the {enemy.name}...")
        input("\nPress Enter to continue...")
        return False, {}


def process_combat_rewards(player, inventory, rewards):
    """
    Apply combat rewards to player
    
    Args:
        player: Player character
        inventory: Player's inventory
        rewards: Dictionary with xp, gold, and loot
    """
    from src.entities.items import get_item
    
    clear_screen()
    print(victory_banner())
    
    # XP
    print(f"Gained {rewards['xp']} XP!")
    leveled_up = player.gain_xp(rewards['xp'])
    
    # Gold
    print(f"Gained {rewards['gold']} gold!")
    player.gain_gold(rewards['gold'])
    
    # Loot
    if rewards['loot']:
        print("\nItems dropped:")
        for item_key in rewards['loot']:
            item = get_item(item_key)
            if item:
                if inventory.add_item(item):
                    print(f"  📦 {item.name}")
                else:
                    print(f"  ❌ {item.name} (Inventory full!)")

    # Display updated character stats
    print(player.get_stats())

    input("\nPress Enter to continue...")
