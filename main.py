# A unified input system
'''
# About
Uses buttons to navigate menus

These are designed for the command line and do not as of *yet* account for the final UI.

# Types of menus 
- Lists: list_menu(prompt, options)
- Number selections: int_menu(prompt, start_value) 
- Wait for input: wait_for_button_press()
'''

scrolling_options_user_instructions = "<<: 1; enter: 2; >>: 3" # unused

print("""==============================
Thank you for using the easy-TTUI module.
In this current state, the module uses number keys to simulate button presses, as detailed here:
- Left: 1
- Right: 3
- Enter: 2
==============================
""")

def push_to_display(line_one, line_two = ""): 
    '''
    Depricating. I don't want to use this style of display.

    Updates the display. As of right now this just prints a message.

    Keep in mind that the final UI will be a two line display.
    '''

    print(f"{line_one}\n{line_two}")

def wait_for_button_press():
    '''
    Waits for a button press
    '''
    push_to_display("Press any key to continue")
    input()

def list_menu(prompt = "", options = []):
    '''
    Takes a list

    Returns an item from a list provided
    '''

    # insert visual end-of-arrays
    options.insert(0, "<|") # low boundary
    options.append("|>") # high boundary
    option_selected = 0
    while True:
        push_to_display(prompt, f"<< {options[option_selected]} >>")
        button_pressed = int(input())
        if button_pressed == 2:
            if option_selected != 0 and option_selected != len(options) - 1: 
                return options[option_selected]
        if button_pressed == 1:
            if option_selected > 0:
                option_selected -= 1
        elif button_pressed == 3:
            if option_selected < len(options) - 1:
                option_selected += 1

def int_menu(prompt = "", start_value = 0):
    '''
    Takes an unused starting value

    Returns an integer value
    '''

    number_selected = start_value
    while True:
        push_to_display(prompt, f"<< {number_selected} >>")
        button_pressed = int(input())
        if button_pressed == 1:
            number_selected -= 1
        elif button_pressed == 3:
            number_selected += 1
        elif button_pressed == 2:
            return number_selected