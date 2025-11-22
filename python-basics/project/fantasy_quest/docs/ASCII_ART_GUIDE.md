# ASCII Art Integration Guide

## Overview
ASCII art has been added throughout Fantasy Quest to enhance the visual experience of the text-based RPG.

## New Module: `src/utils/ascii_art.py`

### Enemy Sprites (8 Total)
All enemies now have unique ASCII art displayed at the start of combat:
- **Slime** - Blob-like creature
- **Goblin** - Small humanoid
- **Skeleton** - Undead warrior
- **Orc Warrior** - Large hostile humanoid
- **Cave Troll** - Giant monster
- **Vampire** - Undead noble
- **Dark Knight** - Armored antagonist
- **Ancient Dragon** - Epic boss creature

### Banner Functions
Large text banners for major game events:
- `victory_banner()` - Displayed after combat wins
- `defeat_banner()` - Shown when player loses in combat
- `level_up_banner()` - Celebration when player levels up
- `quest_complete_banner()` - Achievement display for completed quests
- `game_over_art()` - Final screen with gravestone when player dies

### Decorative Headers
Scene-setting headers for game locations:
- `shop_header()` - Merchant/shop screen
- `rest_header()` - Inn/rest area
- `get_game_title()` - Enhanced main title screen

### Utility Functions
- `get_enemy_sprite(enemy_name)` - Retrieve sprite by enemy name
- `create_border(text, width)` - Create decorative borders around text

## Modified Files

### 1. `src/core/combat.py`
**Changes:**
- Added `from src.utils.ascii_art import get_enemy_sprite, victory_banner, defeat_banner`
- Enhanced `combat_loop()`: Displays enemy sprite at combat start
- Enhanced `process_combat_rewards()`: Shows victory banner instead of plain text
- Added defeat banner when player dies in combat

**Combat Flow:**
```
1. Clear screen
2. Display "A wild [Enemy] appears!" banner
3. Show enemy ASCII sprite
4. Player presses Enter to begin battle
5. (Combat turns...)
6. Victory: Show victory banner + rewards
   OR Defeat: Show defeat banner + death message
```

### 2. `src/utils/helpers.py`
**Changes:**
- Enhanced `display_title()`: Uses large ASCII art title from ascii_art module
- Enhanced `display_game_over()`: Shows gravestone ASCII art
- Added `display_level_up(player)`: New function for level up celebrations

**New Display Functions:**
```python
display_level_up(player)  # Called from character.py when player levels up
```

### 3. `src/core/character.py`
**Changes:**
- Modified `level_up()`: Now calls `display_level_up(self)` for enhanced visuals
- Imports `from src.utils.helpers import display_level_up`

### 4. `src/main.py`
**Changes:**
- Enhanced `check_quest_completion()`: Displays quest complete banner
- Enhanced `rest()`: Shows inn/rest header
- Enhanced `visit_shop()`: Displays shop header
- Added imports for `quest_complete_banner`, `shop_header`, `rest_header`

## Visual Improvements Summary

### Before → After

**Title Screen:**
- Before: Simple box with emoji
- After: Large stylized "FANTASY QUEST" ASCII text

**Combat Start:**
- Before: Text only "⚔️ A wild Goblin appears!"
- After: Banner + Enemy ASCII sprite art

**Victory:**
- Before: "🎉 VICTORY!"
- After: Large "VICTORY!" ASCII banner

**Level Up:**
- Before: "🎉 Level Up! [Name] reached level X!"
- After: Large "LEVEL UP" banner with stars

**Quest Complete:**
- Before: "🎉 Quest Ready to Turn In: [Name]"
- After: "QUEST COMPLETE" ASCII banner

**Shop:**
- Before: "🏪 SHOP"
- After: Large "SHOP" ASCII header with welcome message

**Rest/Inn:**
- Before: "🏕️ Rest at the inn?"
- After: "REST" ASCII header with bed emoji

**Game Over:**
- Before: "💀 GAME OVER 💀"
- After: Full "GAME OVER" banner with gravestone ASCII art

**Defeat in Combat:**
- Before: Silent failure (no visual)
- After: Large "DEFEAT" banner before game over

## Testing

### Run ASCII Art Demo
```bash
cd d:\GitHub\bootdev-backend-projects\python-basics\project\fantasy_quest
python demo_ascii_art.py
```

This showcases all ASCII art elements in sequence.

### Play the Game
```bash
python run_game.py
```

Experience the enhanced visuals during normal gameplay:
1. Start game → See new title screen
2. Explore → Encounter enemy with sprite
3. Win combat → See victory banner
4. Level up → See level up banner
5. Visit shop → See shop header
6. Rest at inn → See rest header
7. Complete quest → See quest banner
8. Die in combat → See defeat + game over art

## Design Specifications

### Width Standards
- Primary content: 67 characters (for alignment with banners)
- Borders: Box-drawing characters (╔═╗║╚╝)
- Enemy sprites: 15-25 characters wide, 5-8 lines tall
- Large banners: Full width ASCII text art

### Character Set
- Box drawing: ╔═╗║╚╝
- ASCII art: Standard ASCII characters
- Emojis: Retained for inline text (⚔️💀🎉 etc.)

### Terminal Compatibility
- Works on Windows PowerShell
- Works on Unix/Linux terminals
- Requires UTF-8 support for box-drawing characters
- No color dependencies (monochrome)

## Future Enhancements (Optional)

### Potential Additions
- [ ] Color support using `colorama` library
- [ ] Animation frames for critical hits
- [ ] More enemy sprite variations
- [ ] Item/weapon ASCII art
- [ ] Character class sprites
- [ ] Location/map ASCII art
- [ ] Boss battle special frames
- [ ] Status effect visual indicators

### Color Scheme Ideas (if colorama added)
- Red: Damage, danger, defeat
- Green: Healing, success, defense
- Yellow/Gold: Rewards, gold, XP
- Cyan: Magic, special abilities
- Magenta: Rare/legendary items
- White: Normal text
- Gray: Descriptions, flavor text

## File Structure

```
fantasy_quest/
├── src/
│   ├── utils/
│   │   ├── ascii_art.py     # NEW - All ASCII art storage
│   │   └── helpers.py        # MODIFIED - Enhanced displays
│   ├── core/
│   │   ├── combat.py         # MODIFIED - Enemy sprites + banners
│   │   └── character.py      # MODIFIED - Level up banner
│   └── main.py               # MODIFIED - Shop/rest/quest banners
├── demo_ascii_art.py         # NEW - Showcase all art
└── ASCII_ART_GUIDE.md        # This file
```

## Code Examples

### Using Enemy Sprites
```python
from src.utils.ascii_art import get_enemy_sprite

enemy_name = "Goblin"
sprite = get_enemy_sprite(enemy_name)
if sprite:
    print(sprite)
```

### Using Banners
```python
from src.utils.ascii_art import victory_banner, level_up_banner

# Show victory
print(victory_banner())

# Show level up
print(level_up_banner())
```

### Creating Custom Borders
```python
from src.utils.ascii_art import create_border

text = "Welcome, Hero!"
print(create_border(text, width=67))
```

## Credits

**ASCII Art Created:** November 22, 2025  
**Integration:** Complete across all major game systems  
**Style:** Block text for banners, detailed sprites for enemies  
**Compatibility:** Cross-platform terminal support  

---

*"From simple text to epic adventures - now with more art!"*
