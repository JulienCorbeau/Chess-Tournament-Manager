import re
from datetime import datetime
from models.tournament import Tournament

class TournamentController:
    """
    Manages all logic related to tournaments.
    """
    def __init__(self, tournament_manager, player_manager, view):
        """
        Initializes the TournamentController.

        Args:
            tournament_manager (TournamentManager): Manager for tournament data.
            player_manager (PlayerManager): Manager for player data.
            view (MainView): The main view for user interaction.
        """
        self.tournament_manager = tournament_manager
        self.player_manager = player_manager
        self.view = view

    def _validate_tournament_data(self, tournament_data):
        """
        Validates the data collected for a new tournament.
        """
        if not tournament_data["name"] or not tournament_data["location"]:
            return "Le nom et le lieu ne peuvent pas être vides."
        try:
            start = datetime.strptime(tournament_data["start_date"], "%Y-%m-%d")
            end = datetime.strptime(tournament_data["end_date"], "%Y-%m-%d")
        except ValueError:
            return "Format de date invalide. Veuillez utiliser YYYY-MM-DD."
        if end < start:
            return (
                "La date de fin ne peut pas être antérieure à la date de "
                "début."
            )
        rounds_str = tournament_data["number_of_rounds_str"]
        if rounds_str:
            try:
                num_rounds = int(rounds_str)
                if num_rounds <= 0:
                    return (
                        "Le nombre de tours doit être un entier positif."
                    )
            except ValueError:
                return "Le nombre de tours doit être un nombre valide."
        return None

    def create_new_tournament(self):
        """
        Orchestrates the process of creating a new tournament.
        """
        while True:
            tournament_data = self.view.prompt_for_new_tournament()
            error = self._validate_tournament_data(tournament_data)
            if error:
                self.view.display_validation_error(error)
                continue
            rounds_str = tournament_data["number_of_rounds_str"]
            number_of_rounds = int(rounds_str) if rounds_str else 4
            
            new_id = self.tournament_manager.get_next_id()

            tournament = Tournament(
                name=tournament_data["name"],
                location=tournament_data["location"],
                start_date=tournament_data["start_date"],
                end_date=tournament_data["end_date"],
                description=tournament_data["description"],
                number_of_rounds=number_of_rounds,
                tournament_id=new_id
            )

            self.tournament_manager.add_item(tournament)
            self.view.create_tournament_message(tournament.name)
            break

    def manage_tournament(self):
        """
        Orchestrates the process of managing an existing tournament.
        """
        tournaments = self.tournament_manager.load_items()
        
        selected_tournament = self._prompt_user_for_tournament(tournaments)

        if selected_tournament is None:
            self.view.display_selection_cancelled()
            return

        self._hydrate_tournament_players(selected_tournament)

        while True:
            choice = self.view.display_tournament_management_menu(
                selected_tournament.name
            )
            if choice == "1":
                self.add_player_to_tournament(selected_tournament)
            elif choice == "2":
                print("\nDémarrage du tournoi... (Pas encore implémenté)")
            elif choice == "3":
                print("\nAffichage des résultats du tournoi... (Pas encore implémenté)")
            elif choice == "4":
                break
            else:
                self.view.display_validation_error("Choix invalide. Veuillez réessayer.")

    def add_player_to_tournament(self, tournament):
        """
        Adds an existing player to the selected tournament.
        """
        all_players = self.player_manager.load_items()
        enrolled_player_ids = {
            player.player_id for player in tournament.players
        }
        available_players = [
            player for player in all_players 
            if player.player_id not in enrolled_player_ids
        ]
        if not available_players:
            self.view.display_all_players_already_enrolled()
            return

        selected_player = self._prompt_user_for_player(available_players)

        if selected_player is None:
            self.view.display_selection_cancelled()
            return

        tournament.players.append(selected_player)
        all_tournaments = self.tournament_manager.load_items()
        for i, tournament_choice in enumerate(all_tournaments):
            if tournament_choice.tournament_id == tournament.tournament_id:
                all_tournaments[i] = tournament
                break
        self.tournament_manager.save_items(all_tournaments)
        
        self.view.display_message(
            f"Le joueur {selected_player.first_name} {selected_player.last_name} "
            f"a été inscrit au tournoi {tournament.name}."
        )
    
    def _hydrate_tournament_players(self, tournament):
            """
            Helper method to convert a list of player IDs in a tournament
            into a list of full Player objects.
            """
            
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

    def _prompt_user_for_tournament(self, tournaments):
        """
        Gère le processus de sélection d'un tournoi.
        """
        items_as_strings = []
        for i, item in enumerate(tournaments, 1):
            line = f"{i}. {item.name} (ID: {item.tournament_id})"
            items_as_strings.append(line)
            
        if not self.view.display_selection_list("Sélectionner un Tournoi", items_as_strings):
            return None 

        while True:
            choice_str = self.view.prompt_for_choice()
            
            if not choice_str.isdigit():
                self.view.display_validation_error("Veuillez entrer un numéro valide.")
                continue

            choice_int = int(choice_str)
            
            if choice_int == 0:
                return None
            if 1 <= choice_int <= len(tournaments):
                return tournaments[choice_int - 1] 
            else:
                self.view.display_validation_error("Ce numéro n'est pas dans la liste.")

    def _prompt_user_for_player(self, players):
        """
        Gère le processus de sélection d'un joueur.
        """
        items_as_strings = []
        for i, item in enumerate(players, 1):
            line = f"{i}. {item.last_name} {item.first_name} (ID: {item.player_id})"
            items_as_strings.append(line)

        if not self.view.display_selection_list("Sélectionner un Joueur", items_as_strings):
            return None

        while True:
            choice_str = self.view.prompt_for_choice()
            if not choice_str.isdigit():
                self.view.display_validation_error("Veuillez entrer un numéro valide.")
                continue

            choice_int = int(choice_str)
            
            if choice_int == 0:
                return None
            if 1 <= choice_int <= len(players):
                return players[choice_int - 1]
            else:
                self.view.display_validation_error("Ce numéro n'est pas dans la liste.")