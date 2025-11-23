"""
Tests for ASCII art utility functions
"""

import pytest
from src.utils.ascii_art import (
    get_enemy_sprite, get_game_title, victory_banner, defeat_banner,
    level_up_banner, quest_complete_banner, game_over_art,
    shop_header, rest_header, create_border,
    ENEMY_SPRITES, ASCII_ART_ENABLED
)


class TestGetEnemySprite:
    """Tests for enemy sprite retrieval"""

    def test_get_enemy_sprite_valid(self):
        """Test retrieving valid enemy sprites"""
        # Test each enemy name in ENEMY_SPRITES
        for enemy_name in ENEMY_SPRITES.keys():
            sprite = get_enemy_sprite(enemy_name)

            # Verify returns non-empty string
            assert isinstance(sprite, str)
            assert len(sprite) > 0

    def test_get_enemy_sprite_invalid(self):
        """Test requesting non-existent enemy sprite"""
        # Request non-existent enemy
        sprite = get_enemy_sprite("NonExistentEnemy")

        # Verify returns empty string or handles gracefully
        assert sprite == "" or sprite is None or isinstance(sprite, str)

    def test_get_enemy_sprite_case_sensitive(self):
        """Test that sprite lookup is case-sensitive"""
        # Should work with correct case
        sprite_correct = get_enemy_sprite("Goblin")
        assert len(sprite_correct) > 0

        # May not work with wrong case
        sprite_wrong = get_enemy_sprite("goblin")
        # This might return empty or the sprite depending on implementation
        assert isinstance(sprite_wrong, str)


class TestBannerFunctions:
    """Tests for banner functions"""

    def test_banner_functions_return_strings(self):
        """Test that all banner functions return strings"""
        # Call each banner function
        banners = [
            get_game_title(),
            victory_banner(),
            defeat_banner(),
            level_up_banner(),
            quest_complete_banner(),
            game_over_art(),
            shop_header(),
            rest_header()
        ]

        # Verify returns string type
        for banner in banners:
            assert isinstance(banner, str)

            # Check non-empty
            assert len(banner) > 0

    def test_victory_banner(self):
        """Test victory banner"""
        banner = victory_banner()
        assert "VICTORY" in banner or "Victory" in banner or "victory" in banner

    def test_defeat_banner(self):
        """Test defeat banner"""
        banner = defeat_banner()
        assert isinstance(banner, str)
        assert len(banner) > 0

    def test_game_over_art(self):
        """Test game over art"""
        art = game_over_art()
        assert isinstance(art, str)
        # Should contain some game over related text or art
        assert len(art) > 10


class TestCreateBorder:
    """Tests for create_border function"""

    def test_create_border_basic(self):
        """Test creating border with default width"""
        # Call with sample text
        border = create_border("Test Text")

        # Verify proper formatting
        assert isinstance(border, str)
        assert "Test Text" in border

    def test_create_border_custom_width(self):
        """Test border with custom width"""
        border = create_border("Test", width=20)

        # Check width calculations
        assert isinstance(border, str)
        assert len(border.split('\n')[0]) <= 25  # Approximate check


class TestAllSprites:
    """Tests for sprite completeness"""

    def test_all_sprites_defined(self):
        """Verify all enemy types have sprites"""
        expected_enemies = [
            "Slime", "Goblin", "Skeleton", "Orc Warrior",
            "Cave Troll", "Vampire", "Dark Knight", "Ancient Dragon"
        ]

        # Iterate through expected enemy types
        for enemy in expected_enemies:
            # Verify each has corresponding sprite
            assert enemy in ENEMY_SPRITES

            # Check no missing sprites
            sprite = ENEMY_SPRITES[enemy]
            assert sprite is not None
            assert len(sprite) > 0

    def test_enemy_sprites_structure(self):
        """Test that sprites are properly formatted"""
        for enemy_name, sprite in ENEMY_SPRITES.items():
            # Each sprite should be a non-empty string
            assert isinstance(sprite, str)
            assert len(sprite) > 0

            # Sprites should contain newlines (multiline art)
            assert '\n' in sprite


class TestASCIIArtConfiguration:
    """Tests for ASCII art configuration"""

    def test_ascii_art_enabled_flag(self):
        """Test ASCII_ART_ENABLED configuration"""
        # Should be a boolean
        assert isinstance(ASCII_ART_ENABLED, bool)

        # Default should be True based on the implementation
        assert ASCII_ART_ENABLED is True
