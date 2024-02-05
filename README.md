# FPL API

This is a simple API for the Fantasy Premier League game. It scrapes the official FPL site to retrieve data and present it in JSON format.

## Documentation

The API design is inspired by the [Fantasy Premier League API Endpoints: A Detailed Guide](https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19) by [Frenzel Timothy](https://medium.com/@frenzelts?source=post_page-----acbd5598eb19--------------------------------).
The guide shows all endpoint that are implemented in this API wrapper.

## Installation

Run the following command to download the most recent release:

```bash
pip install git+https://github.com/C-Roensholt/fpl-api.git 
```

To install a specific version:

```bash
pip install git+https://github.com/C-Roensholt/fpl-api.git@v0.0.1
```

## Usage

A basic example of how to use the API could be:

```python

from fplapi import fplAPI

# Initialize API connection
client = fplAPI()

# Extract metadata
fpl_data = client.get_fpl_data()
fixtures = client.get_fixtures()

# Get player data
player_detailed_data_list = []
for player in fpl_data["elements"]:
    player_detailed_data = client.get_player_detailed_data(element_id=player["id"])
    player_detailed_data_list.append(player_detailed_data)

# Get gameweek player data and gameweek dream team
player_gameweek_data_list = []
gameweek_dream_team_list = []
for fixture in fixtures:
    if fixture["finished"] == True:
        player_gameweek_data = client.get_player_gameweek_data(event_id=fixture["id"])
        gameweek_dream_team = client.get_team_dream_gameweek(event_id=fixture["id"])
        # add gameweek id to data
        player_gameweek_data["event_id"] = fixture["id"]
        gameweek_dream_team["event_id"] = fixture["id"]
        player_gameweek_data_list.append(player_gameweek_data)
        gameweek_dream_team_list.append(gameweek_dream_team)

```
