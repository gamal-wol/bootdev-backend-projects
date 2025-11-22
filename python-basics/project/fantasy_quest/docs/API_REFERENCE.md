# Fantasy Quest - API Reference

**Technical documentation for developers**

---

## Module Structure

### character.py
- `Character` class - Base character with HP, ATK, DEF
- `Player` class - Extends Character with level, XP, gold
  - `gain_xp(amount)` - Add XP, returns True if leveled
  - `level_up()` - Increase stats: +20 HP, +3 ATK, +2 DEF
  - `spend_gold(amount)` - Returns True if successful

### enemy.py
- `Enemy` class - Extends Character with rewards and loot
- `create_enemy(type, level_modifier)` - Create scaled enemy
- `get_random_enemy(player_level)` - Random appropriate enemy

### items.py
- `Item` base class
- `Weapon`, `Armor`, `Potion` subclasses
- `ITEMS_DATABASE` - Dictionary of all items
- `get_item(key)` - Retrieve item by key

### inventory.py
- `Inventory` class - 20-item capacity
  - `add_item(item)` - Returns True if space available
  - `equip_weapon(weapon, player)` - Updates player ATK
  - `equip_armor(armor, player)` - Updates player DEF
  - `use_potion(potion, player)` - Consumes and heals

### combat.py
- `calculate_damage(attacker, defender)` - Returns damage amount
- `combat_loop(player, enemy, inventory)` - Returns (won, rewards)
- `process_combat_rewards(player, inventory, rewards)` - Apply rewards

### quest.py
- `Quest` class - Objectives and rewards
  - `update_progress(objective, amount)` - Track progress
  - `turn_in(player, inventory)` - Grant rewards
- `QuestLog` class - Manages all quests
- `QUEST_DATABASE` - Predefined quests

### utils.py
- `get_user_choice(valid_choices)` - Validated input
- `get_user_input(prompt, allow_empty)` - Text input
- `clear_screen()` - Cross-platform screen clear
- `display_title()` - ASCII title
- `pause(message)` - Wait for Enter

---

## Key Formulas

**Damage:** `(ATK × random(0.8, 1.2) - DEF)` minimum 1

**XP to Next Level:** `current × 1.5` (exponential)

**Enemy Scaling:** `base_stat × (1 + (player_level - 1) × 0.2)`

---

## Extension Examples

### Add Custom Enemy
```python
from enemy import Enemy

boss = Enemy("Mega Boss", 500, 50, 30, 1000, 1000,
             [("legendary_blade", 1.0)])
```

### Add Custom Item
```python
from items import Weapon, ITEMS_DATABASE

epic_sword = Weapon("Epic Sword", "Very powerful", 1000, 50)
ITEMS_DATABASE["epic_sword"] = epic_sword
```

---

*API Reference created: November 22, 2025*
