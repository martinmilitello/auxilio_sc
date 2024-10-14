# Import the `random` module for generating random numbers
import random

# Define a dictionary to store the game state
game_state = {
    'current_room': 'hallway',
    'inventory': [],
    'health': 100
}

# Define a dictionary to store the room descriptions and exits
rooms = {
    'hallway': {
        'description': 'You are in a dark hallway.',
        'exits': ['kitchen', 'garden'],
        'items': ['key']
    },
    'kitchen': {
        'description': 'You are in a kitchen.',
        'exits': ['hallway', 'pantry'],
        'items': ['knife']
    },
    'garden': {
        'description': 'You are in a beautiful garden.',
        'exits': ['hallway', 'pond'],
        'items': []
    },
    'pantry': {
        'description': 'You are in a pantry.',
        'exits': ['kitchen'],
        'items': ['food']
    },
    'pond': {
        'description': 'You are by a peaceful pond.',
        'exits': ['garden'],
        'items': []
    }
}

# Define a function to display the current room description
def display_room():
    print(rooms[game_state['current_room']]['description'])

# Define a function to display the current room exits
def display_exits():
    print('Exits:')
    for exit in rooms[game_state['current_room']]['exits']:
        print(exit)

# Define a function to display the current room items
def display_items():
    print('Items:')
    for item in rooms[game_state['current_room']]['items']:
        print(item)

# Define a function to handle player input
def handle_input(input_str):
    if input_str == 'go north':
        game_state['current_room'] = rooms[game_state['current_room']]['exits'][0]
    elif input_str == 'go south':
        game_state['current_room'] = rooms[game_state['current_room']]['exits'][1]
    elif input_str == 'take key':
        game_state['inventory'].append('key')
        print('You took the key.')
    elif input_str == 'take knife':
        game_state['inventory'].append('knife')
        print('You took the knife.')
    elif input_str == 'take food':
        game_state['inventory'].append('food')
        print('You took the food.')
    elif input_str == 'inventory':
        print('You have:')
        for item in game_state['inventory']:
            print(item)
    elif input_str == 'health':
        print('Your health is:', game_state['health'])
    else:
        print('Invalid input.')

# Main game loop
while True:
    display_room()
    display_exits()
    display_items()
    input_str = input('> ')
    handle_input(input_str)