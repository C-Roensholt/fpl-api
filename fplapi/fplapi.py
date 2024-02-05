# Shoutout to Fenzel (https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19)
import json

import requests


class fplAPI:
    def __init__(self) -> None:
        self.BASE_URL = "https://fantasy.premierleague.com/api/"

    # Loaders

    def _url(self, *route, **params) -> str:
        return "{base}/{route}".format(
            base=self.BASE_URL,
            route="/".join(str(r) for r in route),
        )

    def _parse_response(self, response):
        content = response.json()
        try:
            error = content.get("error", None)
        except AttributeError:
            # API call returned a list
            return content
        return content

    def _get_json(self, *route, **params):
        for param, val in params.items():
            if isinstance(param, bool):
                params[param] = json.dumps(val)

        r = requests.get(self._url(*route), params=params)
        return self._parse_response(r)

    def get_status(self) -> json:
        """Get the status of updates, e.g. bonus points and league standings for the active gameweek

        Returns:
            json: status of updates
        """
        return self._get_json("event-status")

    # Base FPL data

    def get_fpl_data(self) -> json:
        """Get general information about the FPL game divided into 7 sections
            events: basic information of every gameweek, e.g. average score, highest score etc.
            game_settings; game settings and rules
            phases: phases of the FPL season
            teams: information of every PL team in FPL
            total_players: total PL players in FPL
            elements: information of every PL players in FPL, e.g. values, goals, assists, xg etc.
            element_types: information about playing positions (GK, DEF, MID, FWD)

        Returns:
            json: General information about FPL in 7 sections
        """
        return self._get_json("bootstrap-static")

    # Fixture

    def get_fixtures(self, event: int = None, future: bool = 0) -> json:
        """Get fixtures from the FPL season
            stats: match facts that affect points of a player by id

        Args:
            event (int, optional): Get specific gameweek by id. Defaults to None.
            future (bool, optional): Get only future gameweeks (1) or all gameweeks (0). Defaults to 0.

        Returns:
            json: _description_
        """
        return self._get_json("fixtures", event=event, future=future)

    # Manager

    def get_manager_data(self, manager_id: int) -> json:
        """Get basic information a FPL manager

        Args:
            manager_id (int): id of the mananger (can be found in the url of "Pick Team" -> "View Gameweek history")

        Returns:
            json: basic FPL manager information
        """
        return self._get_json("entry", manager_id)

    def get_manager_gameweek_data(self, manager_id: int, event_id: int) -> json:
        """Get information about a FPL manager for a specific gameweek in 4 sections
            active_chip: name of active chip, if empty no actve chip
            automatic_subs: players that were automatic subbed in for the gameweek
            entry_history: information about the gameweek for the manager, overall rank, gw rank etc.
            picks: players the manager had for the specific gameweek
        Args:
            manager_id (int): id of the manager
            event_id (int): id of the gameweek

        Returns:
            json: information about a FPL manager for a specific gameweek in 4 sections
        """
        return self._get_json("entry", manager_id, "event", event_id, "picks")

    def get_manager_history_data(self, manager_id: int) -> json:
        """Get information about a managers previous performance from current season (current) and previous seasons (past)
            current: information from current FPL season
            past: information from previous FPL season(s)
            chips: chips used this season

        Args:
            manager_id (int): id of the manager

        Returns:
            json: historic information from a specific manager
        """
        return self._get_json("entry", manager_id, "history")

    def get_manager_my_team(self, manager_id: int) -> json:
        """Get information about your FPL team, requires authentication
            picks: players you have picked in your team
            chips: current status of your chip usage
            transfers: information of your last transfer

        Args:
            manager_id (int): id of a FPL manager

        Returns:
            json: information about your FPL team
        """
        return self._get_json("my-team", manager_id)

    # Team

    def get_team_dream_gameweek(self, event_id: int) -> json:
        """Get information of each gameweek's best performer

        Args:
            event_id (int): id of the gameweek

        Returns:
            json: information of each gameweek's best performer
        """
        return self._get_json("dream-team", event_id)

    # Player

    def get_player_gameweek_data(self, event_id: int) -> json:
        """Get information about all players' in a specific gameweek in 3 sections
            id: id of the player (element_id)
            stats: player stats, e.g. goals, assists, xg
            explain: detail about players' gameweek points, e.g. goals, assists, bonus points

        Args:
            event_id (int): id of the gameweek

        Returns:
            json: information about all players' in a specific gameweek in 3 sections
        """
        return self._get_json("event", event_id, "live")

    def get_player_detailed_data(self, element_id: int) -> json:
        """Get detailed PL player information in 3 sections
            fixtures: list of remaining fixtures for the season
            history: list of previous fixture and match stats in the season
            history_past: list of previous seasons and seasonal stats

        Args:
            element_id (int): PL player id

        Returns:
            json: detailed PL player information in 3 sections
        """
        return self._get_json("element-summary", element_id)

    # League

    def get_league_standing_classic(
        self, league_id: int, page_standing: int = None
    ) -> json:
        """Get classic league standing from a specific FPL league

        Args:
            league_id (int): id of a FPL league
            page_standing (int, optional): choose page if multiple pages. Defaults to None.

        Returns:
            json: classic league standing from a specific FPL league
        """
        return self._get_json(
            "leagues-classic", league_id, "standings", page_standing=page_standing
        )

    def get_league_standing_h2h(
        self, league_id: int, page_standing: int = None
    ) -> json:
        """Get H2H standing from a specific FPL league

        Args:
            league_id (int): id of a FPL league
            page_standing (int, optional): choose page if multiple pages. Defaults to None.

        Returns:
            json: H2H standing from a specific FPL league
        """
        return self._get_json(
            "leagues-h2h", league_id, "standings", page_standing=page_standing
        )

    # Misc

    def get_set_piece_notes(self) -> json:
        """Get information of each team's set piece takers, updates or confirmation

        Returns:
            json: information of each team's set piece taker
        """
        return self._get_json("team", "set-piece-notes")
