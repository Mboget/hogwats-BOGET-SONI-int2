################################# manages the main menu #################################

from src.utils.input_utils import ask_choice

def display_menu():

    c1 = "Start chapter 1 - Arrival in the magical world"
    c2 = "Start chapter 2 - Meeting of new Friends"
    c3 = "Start chapter 3 - Descovering of the spells and Magical Quiz"
    c4 = "Start chapter 4 - ... "
    c5 = "Start chapter 5 - ... "

    return(c1,c2,c3,c4,c5)

def launch_menu_choice(): 
    