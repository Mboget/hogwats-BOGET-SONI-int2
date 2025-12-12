# journey to hogwarts: chapter 2
# tasks:
# import modules: no
# meeting friends: yes
# welcome message: yes
# Sorting ceremony in the Great Hall: no
# Player's installation in their common room according to their house : yes
# Display of complete information about the player's character to summarize the end of the chapter: yes
# Display of a message confirming the end of the chapter and announcing the start of classes at Hogwarts: yes

from universe.character import display_character

from src.utils.input_utils import load_file,ask_choice

print("journey to hogwarts: chapter 2")

def meet_friends(character):
    print()
    print("you board the train which is slowly departing northward...")

    print("\n A red-haired boy enters your compartment, looking friendly.")
    print("how do you respond? \n 1.Sure have a seat /n 2. Sorry I prefer to travel alone.")
    choice=int(input("Your choice: "))
    if choice == 1:
        character['attributes']['loyalty'] +=1
        print("Ron smiles: Awesome! You'll see, Hogwarts is amazing!")
    else:
        character['attributes']['ambition'] += 1
        print("Ron shrugs and moves on")

    print("A girl enters next, already carrying a stack of books.")
    print("— Hello, I'm Hermione Granger. Have you ever read 'A History of Magic'?")
    print("How do you respond(write the corresponding integer? \n 1.Yes, I love learning new things! \n Uh... no, I prefer adventures over books.")
    choice=int(input("Your choice: "))
    if choice == 1:
        print("Hermione smiles, impressed: — Oh, that's rare! You must be very clever!")
        character['attributes']['intelligence'] +=1
    else:
        print("Hermione looks disappointed and leaves")
        character['attributes']['courage'] += 1

    print("\n Then a blonde boy enters, looking arrogant.")
    print("I'm Draco Malfoy. It's best to choose your friends carefully from the start, don't you think?")
    print("How do you respond? /n 1. Shake his hand politely. /n 2. Ignore him completely. /n 3. Respond with arrogance.")
    choice=int(input("Your choice: "))
    if choice == 1:
        print("You are a good judge of character")
        character['attributes']['ambition'] += 1
    elif choice == 2:
        print("HOW DARE YOU IGNORE ME ! Father will be hearing about this")
        character['attributes']['loyalty'] +=1
    else:
        character['attributes']['courage'] += 1
        print("You will regret this!")


    print("\n Your updated attributes are:")
    for attr, value in character['Attributes'].items():
        print(f" - {attr}: {value}")


# Sorting ceremony:
def sorting(character, questions):
    questions = [
        (
            "You see a friend in danger. What do you do?",
            ["Rush to help", "Think of a plan", "Seek help", "Stay calm and observe"],
             ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"]
        ),
        (
            "Which trait describes you best?",
            ["Brave and loyal", "Cunning and ambitious", "Patient and hardworking", "Intelligent and curious"],
             ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"]
        ),
        (
            "When faced with a difficult challenge, you...",
            ["Charge in without hesitation", "Look for the best strategy", "Rely on your friends","Analyze the problem"],
            ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"]
        )
    ]
    print("\nThe sorting ceremony begins in the Great Hall...")
    print("The Sorting Hat observes you for a long time before asking its questions:")


    house_scores = {
        "Gryffindor": 0,
        "Slytherin": 0,
        "Hufflepuff": 0,
        "Ravenclaw": 0
    }

    #  ATTRIBUTE INFLUENCE: Add points based on character attributes (x2)

    attributes = character.attributes

    house_scores["Gryffindor"] += attributes.get('courage', 0) * 2
    house_scores["Slytherin"] += attributes.get('ambition', 0) * 2
    house_scores["Hufflepuff"] += attributes.get('loyalty', 0) * 2
    house_scores["Ravenclaw"] += attributes.get('intelligence', 0) * 2

    for question_text, options, house_assignments in questions:

        chosen_option = ask_choice(question_text, options)

        chosen_index = options.index(chosen_option)
        assigned_house = house_assignments[chosen_index]
        house_scores[assigned_house] += 3

        print("\nSummary of scores:")
    for house, score in house_scores.items():
        print(f"{house}: {score} points")

    max_score = max(house_scores.values())
    winning_houses = [house for house, score in house_scores.items() if score == max_score]
    final_house_name = winning_houses[0]
    character.house.nom = final_house_name
    print(f"\nThe Sorting Hat exclaims: **{final_house_name.upper()}!!!**")
    print(f"You join the {final_house_name} students to loud cheers!")


def enter_common_room(character):
    print("\nYou follow the prefects through the castle corridors...")
    houses_data = load_file("../data/houses.json")

    player_house = character.get('House')

    if player_house and player_house in houses_data:
        house_info = houses_data[player_house]

        # Display description
        print(f"\nDescription of the {player_house} Common Room:")
        print(house_info.get('description', 'A majestic common room.'))

        # Display welcome message
        print(house_info.get('welcome_message', f"Welcome to the noble House of {player_house}."))

        # Display house colors
        colors = ", ".join(house_info.get('colors', ['unknown']))
        print(f"Your house colors: {colors}")
    else:
        print("\nCould not find information for your house. Something is wrong!")


def welcome_message():
    print("Welcome, new students! Before the feast, I must say a few words.")
    print("Nitwit! Blubber! Oddment! Tweak!")
    print("Now, let the feast begin and the Sorting Ceremony commence!")
    input()

#end of ch 2
print(f"End of ch 2 {character['House']} student")
print("="*50)
display_character(character)
print("\nEnd of Chapter 2! Classes begin tomorrow. Your adventure continues...")