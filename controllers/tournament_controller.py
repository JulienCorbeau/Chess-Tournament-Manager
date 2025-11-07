import re
import random
from datetime import datetime
from models.tournament import Tournament
from models.round import Round

class TournamentController:
    """
    Manages all logic for tournaments:
    - Creation and validation
    - Managing a specific tournament (adding players, starting rounds)
    """
    def __init__(self, tournament_manager, player_manager, view):
        """
        Initializes the TournamentController.
        """
        self.tournament_manager = tournament_manager
        self.player_manager = player_manager
        self.view = view

    def _validate_tournament_data(self, tournament_data):
        """
        Internal helper. Checks if tournament data is valid.
        Returns an error message or None.
        """
        if not tournament_data["name"] or not tournament_data["location"]:
            return "Le nom et le lieu ne peuvent pas être vides."
        try:
            start = datetime.strptime(tournament_data["start_date"], "%Y-%m-%d")
            end = datetime.strptime(tournament_data["end_date"], "%Y-%m-%d")
        except ValueError:
            return "Format de date invalide. Veuillez utiliser YYYY-MM-DD."
        
        if end < start:
            return "La date de fin ne peut pas être antérieure à la date de début."
        
        rounds_str = tournament_data["number_of_rounds_str"]
        if rounds_str:  # Only validate if user typed something in the field
            try:
                num_rounds = int(rounds_str)
                if num_rounds <= 0:
                    return "Le nombre de tours doit être un entier positif."
            except ValueError:
                return "Le nombre de tours doit être un nombre valide."
        return None

    def create_new_tournament(self):
        """
        Orchestrates the process of creating a new tournament.
        """
        while True:
            # 1. Get data from view
            tournament_data = self.view.prompt_for_new_tournament()
            
            # 2. Validate
            error = self._validate_tournament_data(tournament_data)
            if error:
                self.view.display_validation_error(error)
                continue

            # 3. Process data
            rounds_str = tournament_data["number_of_rounds_str"]
            number_of_rounds = int(rounds_str) if rounds_str else 4
            new_id = self.tournament_manager.get_next_id()

            # 4. Create model object
            tournament = Tournament(
                name=tournament_data["name"],
                location=tournament_data["location"],
                start_date=tournament_data["start_date"],
                end_date=tournament_data["end_date"],
                description=tournament_data["description"],
                number_of_rounds=number_of_rounds,
                tournament_id=new_id
            )

            # 5. Save
            self.tournament_manager.add_item(tournament)
            self.view.create_tournament_message(tournament.name)
            break

    def manage_tournament(self):
        """
        Orchestrates the sub-menu for managing one tournament.
        """
        # 1. Load all tournaments
        tournaments = self.tournament_manager.load_items()
        
        # 2. Ask user to pick one
        selected_tournament = self._prompt_user_for_tournament(tournaments)
        if selected_tournament is None:
            self.view.display_selection_cancelled()
            return

        # 3. Load the full objects for players and rounds
        self._hydrate_tournament_players(selected_tournament)
        self._hydrate_tournament_rounds(selected_tournament)

        # 4. Show the specific sub-menu
        while True:
            choice = self.view.display_tournament_management_menu(
                selected_tournament
            )
            if choice == "1":
                self.add_player_to_tournament(selected_tournament)
            elif choice == "2":
                self._start_new_round(selected_tournament)
            elif choice == "3":
                print("\nAffichage des résultats du tournoi... (Pas encore implémenté)")
            elif choice == "4":
                break  # Exit to main menu
            else:
                self.view.display_validation_error("Choix invalide. Veuillez réessayer.")

    def add_player_to_tournament(self, tournament):
        """
        Adds one existing player to the selected tournament.
        """
        # 1. Load all available players
        all_players = self.player_manager.load_items()
        
        # 2. Get IDs of players already in the tournament
        enrolled_player_ids = {
            player.player_id for player in tournament.players
        }
        
        # 3. Create a new list of players who are NOT enrolled
        available_players = [
            player for player in all_players 
            if player.player_id not in enrolled_player_ids
        ]
        
        if not available_players:
            self.view.display_all_players_already_enrolled()
            return

        # 4. Ask user to pick from the available list
        selected_player = self._prompt_user_for_player(available_players)
        if selected_player is None:
            self.view.display_selection_cancelled()
            return

        # 5. Add the player object to the tournament's list
        tournament.players.append(selected_player)
        
        # 6. Save the *entire* list of tournaments
        all_tournaments = self.tournament_manager.load_items()
        for i, tournament_choice in enumerate(all_tournaments):
            if tournament_choice.tournament_id == tournament.tournament_id:
                all_tournaments[i] = tournament  # Replace with the modified one
                break
        self.tournament_manager.save_items(all_tournaments)
        
        # 7. Show success message
        player_name = f"{selected_player.first_name} {selected_player.last_name}"
        self.view.display_player_added_to_tournament(player_name, tournament.name)
    
    def _hydrate_tournament_players(self, tournament):
            """
            Internal helper.
            Converts a list of player IDs (like [1, 2])
            into a list of full Player Objects ([<Player 1>, <Player 2>]).
            """
            # If list is empty or already has objects, do nothing
            if not tournament.players or hasattr(tournament.players[0], 'player_id'):
                return

            all_players = self.player_manager.load_items()
            hydrated_players = []
            player_id_map = {
                player.player_id: player for player in all_players
            }
            
            for player_id in tournament.players:
                if player_id in player_id_map:
                    hydrated_players.append(player_id_map[player_id])
                else:
                    print(f"Attention: Joueur ID {player_id} non trouvé.")
            
            tournament.players = hydrated_players

    def _hydrate_tournament_rounds(self, tournament):
        """
        Internal helper.
        Converts a list of round dicts (from JSON)
        into a list of full Round Objects.
        """
        hydrated_rounds = []
        for round_data in tournament.rounds:
            if isinstance(round_data, Round):
                hydrated_rounds.append(round_data)  # Already an object
            else:
                hydrated_rounds.append(Round(**round_data))  # Convert from dict
        tournament.rounds = hydrated_rounds

    def _start_new_round(self, tournament):
        """
        Generates the first round of the tournament.
        """
        # 1. Check if it's possible to start
        if tournament.rounds:
            self.view.display_validation_error("Le tournoi a déjà commencé.")
            return

        if len(tournament.players) < 2:
            self.view.display_validation_error("Il faut au moins 2 joueurs inscrits pour démarrer.")
            return

        # 2. Get the list of players and shuffle them
        players_list = list(tournament.players) 
        random.shuffle(players_list)

        # 3. Create match pairs
        matches = []
        for i in range(0, len(players_list), 2):
            # If there is an odd number of players, the last one is left out
            if i + 1 == len(players_list):
                break 
    
            player1 = players_list[i]
            player2 = players_list[i+1]
            
            # Create the match tuple: ([PlayerA, 0.0], [PlayerB, 0.0])
            match_tuple = (
                [player1, 0.0],  # Player 1 and their score
                [player2, 0.0]   # Player 2 and their score
            )
            matches.append(match_tuple)

        # 4. Create the new Round object
        round_name = f"Round {len(tournament.rounds) + 1}"
        new_round = Round(name=round_name, matches=matches)

        # 5. Add the round to the tournament and save
        tournament.rounds.append(new_round)
        
        all_tournaments = self.tournament_manager.load_items()
        for i, t in enumerate(all_tournaments):
            if t.tournament_id == tournament.tournament_id:
                all_tournaments[i] = tournament
                break
        self.tournament_manager.save_items(all_tournaments)

        # 6. Show success message
        self.view.display_round_started(new_round.name, len(matches))
    
    def _prompt_user_for_tournament(self, tournaments):
        """
        Internal helper. Manages the tournament selection menu.
        """
        # 1. Format the list of strings for the view
        items_as_strings = []
        for i, item in enumerate(tournaments, 1):
            line = f"{i}. {item.name} (ID: {item.tournament_id})"
            items_as_strings.append(line)
            
        # 2. Ask the view to display the list
        if not self.view.display_selection_list("Sélectionner un Tournoi", items_as_strings):
            return None  # List was empty

        # 3. Loop until user gives a valid choice
        while True:
            choice_str = self.view.prompt_for_choice()
            
            if not choice_str.isdigit():
                self.view.display_validation_error("Veuillez entrer un numéro valide.")
                continue

            choice_int = int(choice_str)
            
            if choice_int == 0:
                return None  # User cancelled
            if 1 <= choice_int <= len(tournaments):
                return tournaments[choice_int - 1]  # Return the chosen object
            else:
                self.view.display_validation_error("Ce numéro n'est pas dans la liste.")

    def _prompt_user_for_player(self, players):
        """
        Internal helper. Manages the player selection menu.
        """
        # 1. Format the list of strings
        items_as_strings = []
        for i, item in enumerate(players, 1):
            line = f"{i}. {item.last_name} {item.first_name} (ID: {item.player_id})"
            items_as_strings.append(line)

        # 2. Ask view to display
        if not self.view.display_selection_list("Sélectionner un Joueur", items_as_strings):
            return None

        # 3. Loop for valid choice
        while True:
            choice_str = self.view.prompt_for_choice()
            if not choice_str.isdigit():
                self.view.display_validation_error("Veuillez entrer un numéro valide.")
                continue

            choice_int = int(choice_str)
            
            if choice_int == 0:
                return None  # User cancelled
            if 1 <= choice_int <= len(players):
                return players[choice_int - 1]  # Return the chosen object
            else:
                self.view.display_validation_error("Ce numéro n'est pas dans la liste.")