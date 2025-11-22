"""
Utility functions for Fantasy Quest
Helper functions for input validation, display, etc.
"""

import os


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_user_choice(valid_choices: list) -> str:
    """
    Get validated user input from a list of choices
    
    Args:
        valid_choices: List of valid input strings
        
    Returns:
        User's choice (guaranteed to be in valid_choices)
    """
    while True:
        choice = input("\nEnter your choice: ").strip().lower()
        if choice in [c.lower() for c in valid_choices]:
            # Return the original case version
            for valid in valid_choices:
                if valid.lower() == choice:
                    return valid
        print(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}")


def get_user_input(prompt: str, allow_empty: bool = False) -> str:
    """
    Get user text input with validation
    
    Args:
        prompt: Prompt to display
        allow_empty: Whether to allow empty input
        
    Returns:
        User's input string
    """
    while True:
        user_input = input(prompt).strip()
        if user_input or allow_empty:
            return user_input
        print("Input cannot be empty. Please try again.")


def display_title():
    """Display the game title screen"""
    from src import __version__
    from src.utils.ascii_art import get_game_title
    
    clear_screen()
    print(get_game_title())
    print(f"{'':^67}")
    print(f"{'v' + __version__:^67}")
    print()


def display_game_over(player):
    """
    Display game over screen
    
    Args:
        player: Player character for final stats
    """
    from src.utils.ascii_art import game_over_art
    
    clear_screen()
    print(game_over_art())
    print(f"\n{player.name} has fallen in battle...")
    print(f"\nFinal Stats:")
    print(f"  Level: {player.level}")
    print(f"  Gold Earned: {player.gold}")
    print(f"\n{'='*67}\n")


def format_separator(char: str = "=", length: int = 50) -> str:
    """
    Create a separator line
    
    Args:
        char: Character to use for separator
        length: Length of separator
        
    Returns:
        Separator string
    """
    return char * length


def display_level_up(player):
    """
    Display level up celebration screen
    
    Args:
        player: Player character who leveled up
    """
    from src.utils.ascii_art import level_up_banner
    
    print("\n" + level_up_banner())
    print(f"\n{'Congratulations!':^67}")
    print(f"{f'{player.name} reached Level {player.level}!':^67}")
    print(f"\n{'='*67}\n")
    input("Press Enter to continue...")


def pause(message: str = "\nPress Enter to continue..."):
    """
    Pause execution until user presses Enter
    
    Args:
        message: Message to display
    """
    input(message)
