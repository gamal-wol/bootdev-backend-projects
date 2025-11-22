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
    clear_screen()
    print("""
╔═══════════════════════════════════════════════════╗
║                                                   ║
║           ⚔️  FANTASY QUEST  ⚔️                  ║
║                                                   ║
║         A Text-Based RPG Adventure                ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
    """)
    print(f"                    v{__version__}\n")


def display_game_over(player):
    """
    Display game over screen
    
    Args:
        player: Player character for final stats
    """
    print(f"\n{'='*50}")
    print("💀 GAME OVER 💀")
    print(f"{'='*50}")
    print(f"\n{player.name} has fallen in battle...")
    print(f"\nFinal Stats:")
    print(f"  Level: {player.level}")
    print(f"  Gold Earned: {player.gold}")
    print(f"{'='*50}\n")


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


def pause(message: str = "\nPress Enter to continue..."):
    """
    Pause execution until user presses Enter
    
    Args:
        message: Message to display
    """
    input(message)
