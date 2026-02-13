from os import system, name
from typing import Callable, List, Any, Tuple

# Constants for UI formatting
BREAK_HARD = "=============================="
BREAK_SOFT = "------------------------------"
INPUT_INDICATOR = ":: "
SELECTED_INDICATOR = "* "

# Error message generator
def type_error_message(options: List[Any]) -> str:
    return f"All options must support string representation. Options passed: {options}"

# Utility function to check if a value is an integer
def is_int(value: Any) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False

# Clear the console screen
def clear_screen() -> None:
    system("cls") if name == "nt" else system("clear")

# Display a prompt and get user input
def _display_and_input(prompt: str, body_text: str) -> str:
    clear_screen()
    print(f"{BREAK_HARD}\n{prompt}\n{BREAK_SOFT}\n{body_text}\n{BREAK_HARD}")
    try:
        return input(INPUT_INDICATOR)
    except KeyboardInterrupt:
        print("\nInput interrupted by user.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

# General menu handler with validation
def menu(prompt: str, body_text: str, validate: Callable[[Any], Tuple[bool, str]]) -> Any:
    while True:
        response = _display_and_input(prompt, body_text)
        is_valid, error_message = validate(response)
        if is_valid:
            return response
        prompt = f"{prompt}\n{error_message}"

# Menu for selecting an integer within a range
def int_menu(prompt: str, min_value: int, max_value: int) -> int:
    if max_value <= min_value:
        raise ValueError(f"max_valid ({max_value}) must be greater than min_value ({min_value})!")

    def validate(response: str) -> Tuple[bool, str]:
        if is_int(response):
            value = int(response)
            if min_value <= value <= max_value:
                return True, ""
        return False, f"Response is invalid. Please type an integer between {min_value} and {max_value}."

    body_text = f"Please enter a number between {min_value} and {max_value}."
    return int(menu(prompt, body_text, validate))

# Menu for selecting an option from a list
def list_menu(prompt: str, options: List[Any]) -> int:
    if not options:
        raise ValueError("Options cannot be empty!")

    def validate(response: str) -> Tuple[bool, str]:
        if is_int(response):
            index = int(response)
            if 0 <= index < len(options):
                return True, ""
        return False, "Response is invalid. Please type a number corresponding to the option you wish to select."

    body_text = "\n".join([f"{i}: {option}" for i, option in enumerate(options)])
    return int(menu(prompt, body_text, validate))

# Menu for multiple-choice selection
def multiple_choice_menu(prompt: str, options: List[Any]) -> List[int]:
    if not options:
        raise ValueError("Options cannot be empty!")

    options = [str(option) for option in options]
    options.insert(0, "Done")
    selected_indices: List[int] = []

    while True:
        choice = list_menu(prompt, options)
        if choice == 0:
            return selected_indices
        if options[choice].startswith(SELECTED_INDICATOR):
            options[choice] = options[choice][len(SELECTED_INDICATOR):]
            selected_indices.remove(choice)
        else:
            options[choice] = f"{SELECTED_INDICATOR}{options[choice]}"
            selected_indices.append(choice)

# Menu for free-text response
def text_response_menu(prompt: str) -> str:
    def validate(response: str) -> Tuple[bool, str]:
        return True, ""

    body_text = "Please type your response below."
    return menu(prompt, body_text, validate)
