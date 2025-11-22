# Fantasy Quest

A text-based RPG adventure game built as part of Boot.dev's Python Basics course.

**Current Version:** 1.1.0 | [View Changelog](CHANGELOG.md)

## Overview

Fantasy Quest is a terminal-based role-playing game where you create a character, battle monsters, complete quests, and level up your hero. The game features a complete RPG experience with character progression, equipment management, and an engaging quest system.

## Features

### 🎮 Core Gameplay
- **Character System**: Create and customize your hero with dynamic stats
- **Turn-Based Combat**: Strategic battles against various enemies
- **Level Progression**: Gain XP, level up, and increase your power
- **Inventory Management**: Collect and use items, weapons, and armor
- **Quest System**: Complete objectives for rewards
- **Shop System**: Buy potions and equipment with earned gold

### ⚔️ Combat System
- Attack enemies with your equipped weapon
- Use healing potions during battle
- Attempt to flee from dangerous encounters
- Damage calculation based on ATK and DEF stats
- Enemy loot drops including gold, XP, and items

### 📦 Items & Equipment
- **Weapons**: Rusty Sword, Iron Sword, Steel Sword, Legendary Blade
- **Armor**: Leather Armor, Iron Armor, Steel Armor, Dragon Armor
- **Potions**: Minor, Health, Greater, and Mega healing potions
- Equip items to boost your stats

### 🗡️ Enemies
- **Slime** - Weak beginner enemy
- **Goblin** - Common forest dweller
- **Skeleton** - Undead warrior
- **Orc Warrior** - Tough fighter
- **Cave Troll** - Powerful brute
- **Vampire** - Cunning predator
- **Dark Knight** - Elite enemy
- **Ancient Dragon** - Legendary boss

### 📜 Quest System
- Track multiple active quests
- Complete objectives to earn rewards
- Unlock new quests as you level up
- Turn in completed quests for XP, gold, and items

## How to Play

### Installation & Setup

1. Navigate to the game directory:
```bash
cd bootdev-backend-projects/python-basics/project/fantasy_quest
```

2. Run the game:
```bash
python run_game.py
```

### Game Controls

The game is menu-driven. Simply enter the number corresponding to your choice when prompted.

#### Main Menu Options:
1. **Explore** - Venture into the wilderness to find enemies
2. **View Inventory** - Check your collected items
3. **Manage Equipment** - Equip weapons, armor, or use potions
4. **View Quests** - Check your quest log and progress
5. **Rest** - Pay gold to restore HP at the inn
6. **Visit Shop** - Purchase items and equipment
7. **Quit Game** - Exit the game

#### Combat Options:
1. **Attack** - Deal damage to the enemy
2. **Use Potion** - Heal yourself during battle
3. **Try to Flee** - Attempt to escape (50% chance)

## Game Mechanics

### Character Stats
- **HP (Health Points)**: When this reaches 0, game over
- **ATK (Attack)**: Determines damage dealt in combat
- **DEF (Defense)**: Reduces incoming damage
- **Level**: Increases through gaining XP
- **Gold**: Currency for buying items and resting

### Leveling System
- Defeat enemies to gain XP
- Level up to increase all stats
- HP is fully restored on level up
- Higher levels unlock tougher enemies and better quests

### Inventory System
- Capacity: 20 items
- Equipped items are separate from inventory
- Potions are consumed when used
- Equipment can be swapped at any time

## Project Structure

```
fantasy_quest/
├── src/                     # Source code
│   ├── core/               # Core game systems
│   │   ├── character.py    # Character and Player classes
│   │   ├── combat.py       # Turn-based combat system
│   │   └── inventory.py    # Inventory management
│   ├── entities/           # Game entities
│   │   ├── enemy.py        # Enemy types and generation
│   │   ├── items.py        # Item definitions and database
│   │   └── quest.py        # Quest system and quest log
│   ├── utils/              # Utility functions
│   │   └── helpers.py      # Helper functions
│   └── main.py             # Main game loop and menu system
├── docs/                    # Documentation
│   ├── DEVELOPMENT.md      # Development documentation
│   ├── PLAYER_GUIDE.md     # Player guide and strategies
│   └── API_REFERENCE.md    # Technical API reference
├── README.md                # This file
└── run_game.py              # Game launcher
```

## Python Concepts Demonstrated

This project showcases various Python programming concepts:
- **Object-Oriented Programming**: Classes, inheritance, encapsulation
- **Data Structures**: Lists, dictionaries, tuples
- **Control Flow**: Loops, conditionals, function calls
- **Error Handling**: Input validation and edge cases
- **Modules**: Code organization across multiple files
- **Type Hints**: Function annotations for clarity
- **Docstrings**: Comprehensive documentation

## Tips for Success

1. **Equip your starting items** before exploring
2. **Stock up on potions** before difficult battles
3. **Level up** by fighting enemies appropriate to your level
4. **Complete quests** for bonus rewards
5. **Save gold** for better equipment in the shop
6. **Rest when needed** to maintain full HP

## Version History

See [CHANGELOG.md](CHANGELOG.md) for a complete history of changes and updates.

**Latest Version:** 1.1.0 (November 22, 2025)
- Project restructuring with professional folder organization
- Comprehensive documentation suite
- Improved code organization and maintainability

## Future Enhancements

Possible features to add:
- Save/load game functionality
- More enemy types and boss battles
- Skill system with special abilities
- Multiple character classes
- World map with different zones
- Crafting system
- Multiplayer or co-op mode

See [CHANGELOG.md](CHANGELOG.md) → Unreleased section for planned features.

## Credits

Created as part of Boot.dev's Python Basics course.
Developed: November 22, 2025

---

**Enjoy your adventure in Fantasy Quest!** ⚔️🐉🏰
