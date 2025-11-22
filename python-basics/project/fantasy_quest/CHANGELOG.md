# Changelog

All notable changes to Fantasy Quest will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Planned
- Save/load game functionality
- Player skills and special abilities
- Additional enemy types with unique behaviors
- Multiple locations and world map

---

## [1.1.0] - 2025-11-22

### Added
- **Project Restructuring**: Reorganized codebase into professional folder structure
  - Created `src/` directory for all source code
  - Created `src/core/` for core game systems (character, combat, inventory)
  - Created `src/entities/` for game entities (enemy, items, quest)
  - Created `src/utils/` for utility functions
- **Documentation Suite**: Comprehensive documentation in `docs/` folder
  - `DEVELOPMENT.md`: Development documentation with technical details
  - `PLAYER_GUIDE.md`: Complete player guide with strategies
  - `API_REFERENCE.md`: Technical API reference for developers
- **Game Launcher**: New `run_game.py` at project root for easy game execution
- **Version Tracking**: Added CHANGELOG.md and VERSION file

### Changed
- Reorganized all Python modules into logical subfolder structure
- Updated all import statements to use new path structure (e.g., `from src.core.character import Player`)
- Renamed `utils.py` to `helpers.py` for clarity
- Updated README.md with new project structure and run instructions

### Technical
- All modules now properly organized by responsibility
- Cleaner separation of concerns (core systems vs entities vs utilities)
- Improved scalability for future features
- Better maintainability with logical grouping

---

## [1.0.0] - 2025-11-22

### Added - Core Game Systems
- **Character System**
  - Base `Character` class with HP, ATK, DEF stats
  - `Player` class with leveling, XP, and gold management
  - Exponential XP curve (×1.5 per level)
  - Stat increases on level up: +20 HP, +3 ATK, +2 DEF
  - Starting stats: 100 HP, 10 ATK, 5 DEF, 50 Gold

- **Combat System**
  - Turn-based combat mechanics
  - Player actions: Attack, Use Potion, Flee (50% chance)
  - Damage formula with randomness: `(ATK × 0.8-1.2) - DEF`, minimum 1
  - Enemy AI with automatic attacks
  - Victory rewards: XP, gold, and loot drops

- **Inventory System**
  - 20-item capacity
  - Separate equipment slots for weapon and armor
  - Equipment management (add, remove, equip, use)
  - Stat bonuses applied when equipment is equipped

- **Item System**
  - 4 weapon tiers (Rusty Sword → Legendary Blade)
  - 4 armor tiers (Leather Armor → Dragon Armor)
  - 4 potion types (Minor → Mega Health Potions)
  - Item database with 12 unique items
  - Loot drop system with probability-based drops

- **Enemy System**
  - 8 unique enemy types (Slime → Ancient Dragon)
  - Level-based enemy scaling: `base_stat × (1 + (player_level - 1) × 0.2)`
  - Enemy-specific loot tables
  - Dynamic enemy selection based on player level

- **Quest System**
  - 3 main quests: Goblin Slayer, Orc Hunter, Dragon Slayer
  - Quest objective tracking
  - Level-gated quest unlocks
  - Turn-in system with rewards (XP, gold, items)
  - Automatic progress tracking during combat

- **Shop System**
  - Purchase potions (Minor, Health, Greater)
  - Purchase mid-tier equipment (Iron Sword, Iron Armor)
  - Gold-based economy

- **Game Features**
  - Menu-driven interface with 7 main options
  - Rest system at inn (20 gold for full HP)
  - Input validation for all user choices
  - Cross-platform screen clearing
  - ASCII title screen
  - Game over screen with final stats

### Game Balance
- **Level Progression**
  - Levels 1-2: Slimes and Goblins
  - Levels 3-4: Skeletons and Orcs
  - Levels 5-7: Trolls and Vampires
  - Levels 8-10: Dark Knights
  - Level 10+: Dragon encounters

- **Economy**
  - Starting gold: 50
  - Shop prices: 15-75 gold for consumables and equipment
  - Combat rewards: 5-500 gold per victory
  - Rest cost: 20 gold

### Technical Implementation
- **Object-Oriented Design**
  - Class inheritance (Character → Player/Enemy, Item → Weapon/Armor/Potion)
  - Composition pattern (Player has-a Inventory, Game has-a Player/QuestLog)
  - Encapsulation with private state management

- **Python Features**
  - Type hints for all function parameters and returns
  - Google-style docstrings for all classes and functions
  - Modular file organization (9 Python files)
  - Error handling with input validation

- **Data Structures**
  - Lists for inventory and quest objectives
  - Dictionaries for item/enemy/quest databases
  - Tuples for loot table entries

### Files Created
- `__init__.py`: Package initialization
- `main.py`: Game controller and menu system (346 lines)
- `character.py`: Character and Player classes (127 lines)
- `enemy.py`: Enemy system with 8 types (179 lines)
- `combat.py`: Turn-based combat mechanics (202 lines)
- `inventory.py`: Inventory management (184 lines)
- `items.py`: Item definitions and database (156 lines)
- `quest.py`: Quest tracking system (198 lines)
- `utils.py`: Helper functions (105 lines)
- `README.md`: Project documentation

### Statistics
- **Total Lines of Code**: ~1,400+
- **Classes**: 11
- **Functions**: 45+
- **Items**: 12
- **Enemies**: 8
- **Quests**: 3

---

## Version Format

Fantasy Quest follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Incompatible API changes or major gameplay overhauls
- **MINOR** version: New features, backward compatible
- **PATCH** version: Bug fixes, backward compatible

---

*Maintained by: Boot.dev Student*  
*Project Start Date: November 22, 2025*
