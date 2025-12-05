################################# responsible for checking user input and reading files #################################

import os
import json
import time
import sys 

def affichage_lettre_par_lettre(texte,speed=0.01,end='\n'):
    for letter in texte:
        print(letter, end='', flush=True)
        time.sleep(speed)
    print(end)

def affichage_lettre_par_lettre_avec_input(texte,speed=0.01):
    for lettre in texte:
        print(lettre,end='',flush=True)
        time.sleep(speed)
    user_input = input()

    return user_input

def changer_statut_fichier_sauvegarde(file_path,nom_fonction):
    
    try : 
        with open(file_path,'r',encoding='utf-8'):
            content= json.load(file_path)

        content[nom_fonction] = True

        with open(file_path,'w',encoding='utf-8'):
            json.dump(content,file_path,ensure_ascii=False,indent=4)
    except FileNotFoundError:
        return('Error : file not found')

def wait_for_enter():
    """
    Attend la touche Enter sans afficher ce que tape l'utilisateur.
    Compatible Windows / Linux / macOS.
    """

    if os.name == "nt":  
        # -----------------------
        #   WINDOWS VERSION
        # -----------------------
        import msvcrt
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key == '\r':  # Enter
                    print()
                    return
                # On ignore toutes les autres touches
    else:
        # -----------------------
        #  UNIX (Linux / macOS)
        # -----------------------
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)  # mode brut, rien n'est affiché
            while True:
                ch = sys.stdin.read(1)
                if ch == '\r' or ch == '\n':  # Enter sur Unix
                    print()
                    return
                # On ignore toutes les autres touches
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def ask_text(message:str)->str:
    """
    Ask the user for a text input with optional validation.

    Args:
        message (str): The message to display to the user.

    Returns:
        str: The input text 
    """

    text = affichage_lettre_par_lettre_avec_input(message)
    # Check if the user entered an empty string or a string of whitespace characters
    if  text == '' or text == ' '*len(text):
        return ask_text(f"{message}")
    # Remove leading and trailing whitespace characters
    res = text.strip()
    return res

#print(ask_text('test'))

def convertisseur_str_to_integer(s: str) -> int:
    """
    Convertit une chaîne de caractères en entier sans utiliser int().
    
    Parameters:
        s (str): La chaîne à convertir (ex: "123" ou "-456")
    
    Returns:
        int: L'entier correspondant
    """
    s = s.strip()  # Enlève les espaces
    
    # Gère le signe négatif
    negative = False
    if s[0] == '-':
        negative = True
        s = s[1:]
    elif s[0] == '+':   
        s = s[1:]
    
    # Convertit chaque caractère en chiffre
    result = 0
    for char in s:
        if not char in '1234567890':
            raise ValueError(f"'{char}' n'est pas un chiffre valide")
        # Chaque chiffre vaut son rang * 10 + la valeur du caractère
        result = result * 10 + (ord(char) - ord('0'))
    
    return -result if negative else result

#print(convertisseur_str_to_integer("13")) 

def ask_number(message:str,min_val:int,max_val:int)->int:
    """
    Ask the user for a number with optional bounds.

    Args:
        message (str): The message to display to the user.
        min_val (int, optional): The minimum value for the number. Defaults to None.
        max_val (int, optional): The maximum value for the number. Defaults to None.

    Returns:
        int: The input number
    """

    # Ask the user for a number
    number_str = affichage_lettre_par_lettre_avec_input(message)
    
    if number_str == '' or number_str == " "*len(number_str):
        affichage_lettre_par_lettre(f'Enter an integer')
        return ask_number(message,min_val,max_val)

    try:
        # Try to convert the input to an integer
        number = convertisseur_str_to_integer(number_str)
    except ValueError:
        # If the input is not an integer, print an error message and ask again
        affichage_lettre_par_lettre(f"Please enter a integer")
        return ask_number(message,min_val,max_val)

    # Check if the number is within the bounds
    if min_val is None and max_val is None:
        # If there are no bounds, return the number
        return number

    elif min_val is None:
        # If there is no minimum bound, check if the number is lower than the maximum bound
        if number > max_val:
            # If the number is greater than the maximum bound, print an error message and ask again
            affichage_lettre_par_lettre(f"Please enter a number lower than {max_val}.")
            return ask_number(message,min_val,max_val)
        # If the number is within the bounds, return it
        return number

    elif max_val is None:
        # If there is no maximum bound, check if the number is greater than the minimum bound
        if number < min_val:
            # If the number is lower than the minimum bound, print an error message and ask again
            affichage_lettre_par_lettre(f"Please enter a number greater than {min_val}.")
            return ask_number(message,min_val,max_val)
        # If the number is within the bounds, return it
        return number

    else:
        # If there are both minimum and maximum bounds, check if the number is within them
        if number < min_val or number > max_val:
            # If the number is not within the bounds, print an error message and ask again
            affichage_lettre_par_lettre(f"Please enter a number between {min_val} and {max_val}.")
            return ask_number(message,min_val,max_val)
        # If the number is within the bounds, return it
        return number

#print(ask_number("Enter a number between 1 and 10: ",1,10))

def ask_choice(message: str, options: list) -> str:
    """
    Ask the user to make a choice from a list of options.

    Args:
        message (str): The message to display to the user.
        options (list): The list of options to choose from.

    Returns:
        str: The chosen option.
    """

    affichage_lettre_par_lettre(message)

    for i in range(len(options)):
        affichage_lettre_par_lettre(f"{i+1}. {options[i]}")

    choice_str = affichage_lettre_par_lettre_avec_input("Your choice: ")

    try:
        # Try to convert the input to an integer
        choice = convertisseur_str_to_integer(choice_str)
    except ValueError:
        # If the input is not an integer, print an error message and ask again
        affichage_lettre_par_lettre(f"Please enter the number and not the text")
        return ask_choice(message, options)

    # Check if the number is within the bounds
    if choice < 1 or choice > len(options):
        affichage_lettre_par_lettre(f"Please enter a choice between 1 and {len(options)}")
        return ask_choice(message, options)

    # If the number is within the bounds, return the chosen option
    return choice - 1 # type: ignore

"""
choices = ["Yes","No","JSPA"]
message = "Quelle est la capitale de la France" 
print(ask_choice(message,choices))"""



def load_file(file_path:str)->dict:
    """
    Load a JSON file from a given path.

    Args:
        file_path (str): The path to the JSON file to load.

    Returns:
        dict: The loaded JSON data, or an error message if the file does not exist.
    """

    # Check if the file exists at the given path.
    if not os.path.isfile(file_path): 
        return {"error": "Chemin n'existe pas"}

    # Open the file and load the JSON data.
    with open(file_path,'r') as f1:
        return json.load(f1)
    

#print(load_file("src/data/inventory.json"))

def bold(text):
    return f"\033[1m{text}\033[0m"

def charger_personnage(file_path= "src/chapters/sauvegardes/sauvegarde_donnees_personnage.json"):

    from src.universe.character import Character
    from src.universe.house import House

    content= load_file(file_path) 

    last_name = content['Last name']
    first_name = content['First name']
    attributes = {
        'cougage':content['Courage level'],
        'intelligence' : content['Intelligence level'],
        'loyality' : content['Loyalty level'],
        'ambition' : content['Ambition level']
                  }
    money = content['Money']
    inventory = content['Inventory']
    spells = content['Spells']
    house = content['House']

    return Character(last_name,first_name,attributes,money,inventory,spells,House(house))
