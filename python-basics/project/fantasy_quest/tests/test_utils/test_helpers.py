"""
Tests for utility helper functions
"""

import pytest
from unittest.mock import patch, MagicMock
from src.utils.helpers import (
    get_user_choice, get_user_input, display_title,
    display_game_over, clear_screen
)


class TestGetUserChoice:
    """Tests for get_user_choice function"""

    @patch('builtins.input')
    def test_get_user_choice_valid_input(self, mock_input):
        """Test with valid choice"""
        # Mock input with valid choice
        mock_input.return_value = "1"
        valid_choices = ["1", "2", "3"]

        # Call function
        result = get_user_choice(valid_choices)

        # Verify returns expected value
        assert result == "1"

    @patch('builtins.input')
    def test_get_user_choice_case_insensitive(self, mock_input):
        """Test case insensitive input"""
        # Mock input with different case
        mock_input.return_value = "yes"
        valid_choices = ["YES", "NO"]

        # Call function
        result = get_user_choice(valid_choices)

        # Verify works correctly
        assert result == "YES"

    @patch('builtins.input')
    def test_get_user_choice_retry_on_invalid(self, mock_input):
        """Test that function retries on invalid input"""
        # Mock sequence: invalid, then valid
        mock_input.side_effect = ["invalid", "5", "2"]
        valid_choices = ["1", "2", "3"]

        # Call function
        result = get_user_choice(valid_choices)

        # Verify loops until valid input
        assert result == "2"
        assert mock_input.call_count == 3


class TestGetUserInput:
    """Tests for get_user_input function"""

    @patch('builtins.input')
    def test_get_user_input_valid(self, mock_input):
        """Test with valid non-empty input"""
        # Mock non-empty input
        mock_input.return_value = "  Hero Name  "

        # Call function
        result = get_user_input("Enter name: ")

        # Verify returns trimmed string
        assert result == "Hero Name"

    @patch('builtins.input')
    def test_get_user_input_rejects_empty(self, mock_input):
        """Test that empty input is rejected by default"""
        # Mock empty string then valid input
        mock_input.side_effect = ["", "  ", "Valid"]

        # Call function
        result = get_user_input("Enter name: ")

        # Verify loops for non-empty
        assert result == "Valid"
        assert mock_input.call_count == 3

    @patch('builtins.input')
    def test_get_user_input_allow_empty(self, mock_input):
        """Test with allow_empty=True"""
        # Set allow_empty = True
        mock_input.return_value = ""

        # Call function
        result = get_user_input("Enter (optional): ", allow_empty=True)

        # Verify accepts empty string
        assert result == ""


class TestClearScreen:
    """Tests for clear_screen function"""

    @patch('os.system')
    @patch('os.name', 'nt')  # Windows
    def test_clear_screen_windows(self, mock_system):
        """Test clear screen on Windows"""
        clear_screen()

        # Should call 'cls' on Windows
        mock_system.assert_called_once_with('cls')

    @patch('os.system')
    @patch('os.name', 'posix')  # Unix/Linux/Mac
    def test_clear_screen_unix(self, mock_system):
        """Test clear screen on Unix systems"""
        clear_screen()

        # Should call 'clear' on Unix
        mock_system.assert_called_once_with('clear')


class TestDisplayTitle:
    """Tests for display_title function"""

    @patch('src.utils.helpers.clear_screen')
    @patch('builtins.print')
    def test_display_title(self, mock_print, mock_clear):
        """Test that title displays correctly"""
        # Call function
        display_title()

        # Verify clear_screen called
        mock_clear.assert_called_once()

        # Verify print was called (title displayed)
        assert mock_print.called


class TestDisplayGameOver:
    """Tests for display_game_over function"""

    @patch('src.utils.helpers.clear_screen')
    @patch('builtins.print')
    def test_display_game_over(self, mock_print, mock_clear, sample_player):
        """Test game over screen display"""
        # Set some stats
        sample_player.level = 5
        sample_player.gold = 150

        # Call function
        display_game_over(sample_player)

        # Verify clear_screen called
        mock_clear.assert_called_once()

        # Verify player info displayed
        assert mock_print.called
        # Check that relevant info was in print calls
        print_calls = [str(call) for call in mock_print.call_args_list]
        full_output = " ".join(print_calls)
        assert sample_player.name in full_output or any(sample_player.name in str(call) for call in mock_print.call_args_list)


class TestPause:
    """Tests for pause function"""

    @patch('builtins.input')
    def test_pause(self, mock_input):
        """Test pause function"""
        from src.utils.helpers import pause

        # Mock input
        mock_input.return_value = ""

        # Call pause()
        pause()

        # Verify waits for Enter
        mock_input.assert_called_once()
