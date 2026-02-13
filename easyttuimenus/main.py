from os import system, name
from typing import Callable, List, Any

BREAK_HARD = "=============================="
BREAK_SOFT = "------------------------------"
INPUT_INDICATOR = ":: "
SELECTED_INDICATOR = "* "
TYPE_ERROR_MESSEGE: Callable[[List[Any]], str] = lambda options: f"All options must support string representation. Options passed: {options}"

def _is_int(x: Any) -> bool:
    try:
        int(x)
        return True
    except:
        return False

def clear():
    system("cls") if name == "nt" else system("clear")

def _display(prompt: str, body_text: str) -> int | ValueError:
    clear()
    print(f"{BREAK_HARD}\n{prompt}\n{BREAK_SOFT}\n{body_text}\n{BREAK_HARD}")
    try:
        return int(input(INPUT_INDICATOR))
    except ValueError as e:
        return e

def _display_and_input(prompt: str, body_text: str) -> Any:
    clear()
    print(f"{BREAK_HARD}\n{prompt}\n{BREAK_SOFT}\n{body_text}\n{BREAK_HARD}")
    try:
        return input(INPUT_INDICATOR)
    except Exception as e:
        print("An unexpected error has occured:\n{e}")

def _menu(prompt: str, body_text: str, validate: Callable[[Any], tuple[bool, str]]) -> Any:
    while True:
        response = _display_and_input(prompt, body_text)
        is_valid, err_mseg = validate(response)
        if is_valid:
            return response
        prompt = f"{prompt}\n{err_mseg}"


def int_menu(prompt: str, min: int, max: int) -> int:
    if max <= min:
        raise ValueError(f"Max ({max}) cannot be smaller than min ({min})!")
    validate: Callable[[int], tuple[bool, str]] = lambda x: (
        min <= int(x) <= max if _is_int(x) else False,
        f"Response is invalid. Please type an integer number between {min} and {max}."
    )
    body_text = f"Please enter a number between {min} and {max}."
    return int(_menu(prompt, body_text, validate))

def list_menu(prompt: str, options: List[Any]) -> int:
    if len(options) == 0:
        raise ValueError("Options cannot be empty!")
    validate: Callable[[int], tuple[bool, str]] = lambda x: (
        0 <= int(x) < len(options) if _is_int(x) else False,
        f"Response is invalid. Please type a number corresponding to the option you wish to select."
    )
    body_text = "\n".join([f"{i}: {options[i]}" for i in range(len(options))])
    return int(_menu(prompt, body_text, validate))

def multiple_choice_menu(prompt: str, options: List[Any]) -> list[int]:
    """A wrapper for `list_menu()` that adds multiple-choice support."""
    options = [str(o) for o in options]
    options.insert(0, "Done")
    selected: list[int] = []
    while True:
        choice = list_menu(prompt, options)
        if choice == 0:
            return selected
        if options[choice].startswith(SELECTED_INDICATOR):
            options[choice] = options[choice][2:]
            selected.remove(choice)
        else:
            options[choice] = f"{SELECTED_INDICATOR}{options[choice]}"
            selected.append(choice)
