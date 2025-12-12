def int_menu(prompt: str, min: int, max: int) -> int:
    """
    Display a menu prompting the user to select an integer within a specified range.

    Args:
        prompt (str): The message to display to the user.
        min (int): The minimum value in the range.
        max (int): The maximum value in the range.

    Returns:
        int: The integer selected by the user.
    """
    ...

def list_menu(prompt: str, options: list[str]) -> int:
    """
    Display a menu prompting the user to select an option from a list.

    Args:
        prompt (str): The message to display to the user.
        options (list[str]): The list of options to choose from.

    Returns:
        int: The index of the selected option.
    """
    ...

def multiple_choice_menu(prompt: str, options: list[str]) -> list[int]:
    """
    Display a menu prompting the user to select multiple options from a list.

    Args:
        prompt (str): The message to display to the user.
        options (list[str]): The list of options to choose from.

    Returns:
        list[int]: A list of indices representing the selected options.
    """
    ...
