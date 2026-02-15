from os import system, name, get_terminal_size
from typing import List, Any

def _get_terminal_columns():
    try:
        return get_terminal_size().columns
    except OSError:
        return 80 # nasty little fallback

# Utility function to check if a value is an integer
def _is_int(value: Any) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False 

# Clear the console screen
def clear_screen() -> None:
    system("cls") if name == "nt" else system("clear")

class Config:
    BREAK_HARD_CHAR = "="
    BREAK_SOFT_CHAR = "-"
    INPUT_INDICATOR = ":: "
    CHECKBOX_EMPTY = "[ ] "
    CHECKBOX_FULL = "[x] "

class _Menu():
    # ///////////////////////////////
    # dynamic components
    break_hard: str
    break_soft: str
    # ///////////////////////////////
    # other vars 
    err_str: str
    body_text: str
    # ///////////////////////////////

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        pass

    @classmethod
    def validate(cls, response: Any) -> bool:
        """Generic validator that always returns True"""
        return True
    
    @classmethod
    def refresh_dynamic_components(cls):
        cls.break_hard = Config.BREAK_HARD_CHAR * _get_terminal_columns()
        cls.break_soft = Config.BREAK_SOFT_CHAR * _get_terminal_columns()

    @classmethod
    def display_and_input(cls, prompt: str, body_text: str) -> str:
        clear_screen()
        cls.refresh_dynamic_components()
        print(f"{cls.break_hard}\n{prompt}\n{cls.break_soft}\n{body_text}\n{cls.break_hard}")
        try:
            return input(Config.INPUT_INDICATOR)
        except KeyboardInterrupt:
            print("\nInput interrupted by user.")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    @classmethod
    def get_response(cls, prompt: str):
        while True:
            response = _Menu.display_and_input(prompt, cls.body_text)
            valid = cls.validate(response)
            if valid:
                return response
            prompt = f"{prompt}\n{cls.err_str}"

class IntMenu(_Menu):

    # ///////////////////////////////
    # validation variables
    min_value: int = 0 # on the fence about keeping this default value
    max_value: int 
    err_str: str = "Response is invalid."
    # ///////////////////////////////

    def __new__(cls, prompt: str, min_value: int, max_value: int) -> int:
        if max_value <= min_value:
            raise ValueError(f"max_valid ({max_value}) must be greater than min_value ({min_value})!")

        cls.min_value = min_value
        cls.max_value = max_value
        cls.body_text = f"Please enter a number between {min_value} and {max_value}."

        return int(IntMenu.get_response(prompt))

    # used by get_response
    @classmethod
    def validate(cls, response: str) -> bool:
        return cls.min_value <= int(response) <= cls.max_value if _is_int(response) else False

class MultipleChoiceMenu(IntMenu):
    err_str = "Response is invalid. Please type a number corresponding to the option you wish to select."

    def __new__(cls, prompt: str, options: List[Any]) -> int:
        if not options:
            raise ValueError("Options cannot be empty!")

        cls.body_text = "\n".join([f"{i}: {option}" for i, option in enumerate(options)])
        cls.max_value = len(options) + 1 #validate uses <=

        return int(MultipleChoiceMenu.get_response(prompt))

class CheckboxMenu(MultipleChoiceMenu):
    # ill need to revisit this with my dynamic assets thingie 
    def __new__(cls, prompt: str, options: List[Any]) -> List[int]:
        if not options:
            raise ValueError("Options cannot be empty!")

        options = [Config.CHECKBOX_EMPTY + str(option) for option in options]
        options.insert(0, "Done")
        selected_indices: List[int] = []

        while True:
            choice = MultipleChoiceMenu(prompt, options)
            if choice == 0: # "Done" 
                return selected_indices # gross behavior here: the "done" item offsets the value of all the selecte items... is this a bad feature? IDK. fixing it would mean that the actual returned value does not match what is displayed, so im on the fence about fixing this one
            if options[choice].startswith(Config.CHECKBOX_EMPTY): # then select it
                options[choice] = options[choice][len(Config.CHECKBOX_EMPTY):]
                options[choice] = f"{Config.CHECKBOX_FULL}{options[choice]}"
                selected_indices.append(choice)
            elif options[choice].startswith(Config.CHECKBOX_FULL): # then de-select it
                options[choice] = options[choice][len(Config.CHECKBOX_FULL):]
                options[choice] = f"{Config.CHECKBOX_EMPTY}{options[choice]}"
                selected_indices.remove(choice)

class FreeformMenu(_Menu):
    body_text = "Please type your response below."

    def __new__(cls, prompt: str) -> str:
        return FreeformMenu.get_response(prompt)


# Now, wait a second. This is turning into form software. Obviously, it's more versatile than that. But this REALLY resembles a form.