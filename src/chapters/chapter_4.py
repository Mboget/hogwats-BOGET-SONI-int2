#Guided scenario: Quidditch match



from src.universe.character import Character
from src.universe.house import House


def create_team(house, team_data, is_player=False, player=None): #

    # Initialize the team
    team = {
        'name': house,
        'score': 0,
        'goals_scored': 0,
        'goals_blocked': 0,
        'caught_snitch': False,
        'players': []
    }

    your_team=[]
    # 2. Load players from JSON data
    if house in team_data:
        # Copy the list to avoid modifying the original JSON data in memory
        your_team = list(team_data[house]['players'])

    # 3. If it's the player's team, insert the player as Seeker
    if is_player and player:
        # Create player: First name Last name (Seeker)
        player_str = f"{player.first_name} {player.last_name} (Seeker)"

        # Index 0 is always Seeker
        if len(team['players']) > 0:
            team['players'][0] = player_str
        else:
            team['players'].append(player_str)

    return team

