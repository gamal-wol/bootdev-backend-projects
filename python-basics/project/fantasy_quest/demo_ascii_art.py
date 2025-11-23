"""
ASCII Art Demo for Fantasy Quest
Displays all the new ASCII art elements
"""

from src.utils.ascii_art import (
    get_game_title, victory_banner, defeat_banner, level_up_banner,
    quest_complete_banner, shop_header, rest_header, game_over_art,
    get_enemy_sprite, get_hero_sprite, ENEMY_SPRITES
)

def main():
    print("=" * 70)
    print("FANTASY QUEST - ASCII ART SHOWCASE")
    print("=" * 70)
    
    # Title Screen
    input("\nPress Enter to see: TITLE SCREEN...")
    print(get_game_title())
    
    # Hero Sprite
    input("\nPress Enter to see: HERO SPRITE...")
    print(f"\n{'='*70}")
    print(f"{'Hero Character':^70}")
    print('='*70)
    print(get_hero_sprite())
    
    # Enemy Sprites
    input("\nPress Enter to see: ENEMY SPRITES...")
    for enemy_name in ENEMY_SPRITES.keys():
        print(f"\n{'='*70}")
        print(f"{enemy_name:^70}")
        print('='*70)
        print(get_enemy_sprite(enemy_name))
    
    # Victory Banner
    input("\nPress Enter to see: VICTORY BANNER...")
    print(victory_banner())
    
    # Defeat Banner
    input("\nPress Enter to see: DEFEAT BANNER...")
    print(defeat_banner())
    
    # Level Up Banner
    input("\nPress Enter to see: LEVEL UP BANNER...")
    print(level_up_banner())
    
    # Quest Complete Banner
    input("\nPress Enter to see: QUEST COMPLETE BANNER...")
    print(quest_complete_banner())
    
    # Shop Header
    input("\nPress Enter to see: SHOP HEADER...")
    print(shop_header())
    
    # Rest Header
    input("\nPress Enter to see: REST/INN HEADER...")
    print(rest_header())
    
    # Game Over Art
    input("\nPress Enter to see: GAME OVER SCREEN...")
    print(game_over_art())
    
    print("\n" + "="*70)
    print("ASCII ART SHOWCASE COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    main()
