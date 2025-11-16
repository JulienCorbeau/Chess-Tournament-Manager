"""
Tournament Controller

Manages tournament creation, player enrollment, and Swiss system pairing.

Swiss System Pairing Algorithm:
    1. Sort players by score (highest first)
    2. Pair players of similar rank who haven't played each other
    3. Avoid rematches using opponent history
    4. Handle odd players with "bye" (1 point, no match)
    5. Prioritize players who haven't received a bye
"""

import re
import random
from datetime import datetime
from models.tournament import Tournament
from models.round import Round
from managers.tournament_manager import TournamentManager
from managers.player_manager import PlayerManager
from views.main_view import MainView


class TournamentController:
    """
    Controller for tournament operations.
    
    Responsibilities:
    - Tournament creation and validation
    - Player enrollment
    - Round generation (random for Round 1, Swiss for others)
    - Match result recording
    - Swiss system pairing logic
    
    Following Principle #1: Manipulates objects, not IDs
    Following Principle #2: Autonomous components
    Following Principle #4: Single responsibility
    Following Principle #5: Business logic in controller, not view
    """

    def __init__(self):
        """Initialize controller with its dependencies."""
        self.tournament_manager = TournamentManager()
        self.player_manager = PlayerManager()
        self.view = MainView()
        self.report_controller = None

    def set_report_controller(self, report_controller):
        """
        Set reference to report controller for cross-controller communication.
        
        Args:
            report_controller (ReportController): The report controller instance
        """
        self.report_controller = report_controller

    # ========================================
    # TOURNAMENT CREATION
    # ========================================

    def create_new_tournament(self):
        """
        Orchestrate tournament creation workflow.
        
        Workflow:
        1. Prompt user for tournament data
        2. Validate data
        3. Generate new ID
        4. Create Tournament object
        5. Save to storage
        6. Display success message
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

    def _validate_tournament_data(self, tournament_data):
        """
        Validate tournament data before creation.
        
        Validation rules:
        - Name and location cannot be empty
        - Dates must be in YYYY-MM-DD format
        - End date cannot be before start date
        - Number of rounds must be positive integer
        
        Args:
            tournament_data (dict): Tournament data to validate
        
        Returns:
            str: Error message if invalid, None if valid
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
        if rounds_str:
            try:
                num_rounds = int(rounds_str)
                if num_rounds <= 0:
                    return "Le nombre de tours doit être un entier positif."
            except ValueError:
                return "Le nombre de tours doit être un nombre valide."
        
        return None

    # ========================================
    # TOURNAMENT MANAGEMENT
    # ========================================

    def manage_tournament(self):
        """
        Display and handle the tournament management menu.
        
        Menu adapts based on tournament state:
        - Before start: Can add players and start
        - In progress: Can enter results
        - Finished: Read-only mode
        """
        tournaments = self.tournament_manager.load_items()
        
        selected_tournament = self._prompt_user_for_tournament(tournaments)
        if selected_tournament is None:
            self.view.display_selection_cancelled()
            return

        while True:
            current_round_name = None
            is_tournament_finished = False
            
            if selected_tournament.rounds:
                current_round = selected_tournament.rounds[-1]
                current_round_name = current_round.name
                
                if (len(selected_tournament.rounds) >= selected_tournament.number_of_rounds
                    and current_round.end_date_time is not None):
                    is_tournament_finished = True
            
            choice = self.view.display_tournament_management_menu(
                selected_tournament,
                current_round_name,
                is_tournament_finished
            )
            
            if choice == "1":
                if not selected_tournament.rounds:
                    self.add_player_to_tournament(selected_tournament)
                else:
                    self.view.display_validation_error(
                        "Les inscriptions sont fermées car le tournoi a commencé."
                    )
            
            elif choice == "2":
                if not selected_tournament.rounds:
                    self._start_new_round(selected_tournament)
                elif is_tournament_finished:
                    self.view.display_validation_error("Le tournoi est terminé.")
                else:
                    self._enter_round_results(selected_tournament)
            
            elif choice == "3":
                print("\nAffichage des résultats du tournoi... (Pas encore implémenté)")
            elif choice == "4":
                break
            else:
                self.view.display_validation_error("Choix invalide. Veuillez réessayer.")

    def add_player_to_tournament(self, tournament):
        """
        Add a player to a tournament.
        
        Workflow:
        1. Load all players
        2. Filter out already enrolled players
        3. Let user select from available players
        4. Add Player OBJECT to tournament (not ID)
        5. Initialize score data via manager
        6. Save tournament
        
        Args:
            tournament (Tournament): Tournament to add player to
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
        
        self.tournament_manager.get_player_score(tournament, selected_player.player_id)
        
        all_tournaments = self.tournament_manager.load_items()
        for i, t in enumerate(all_tournaments):
            if t.tournament_id == tournament.tournament_id:
                all_tournaments[i] = tournament
                break
        self.tournament_manager.save_items(all_tournaments)
        
        player_name = f"{selected_player.first_name} {selected_player.last_name}"
        self.view.display_player_added_to_tournament(player_name, tournament.name)

    # ========================================
    # ROUND MANAGEMENT: START
    # ========================================

    def _start_new_round(self, tournament):
        """
        Start the tournament by creating Round 1 with random pairing.
        
        Workflow:
        1. Validate (tournament not started, minimum 2 players)
        2. Shuffle players randomly
        3. Create pairs (handle bye if odd number)
        4. Create Round object
        5. Save tournament
        
        Args:
            tournament (Tournament): Tournament to start
        """
        if tournament.rounds:
            self.view.display_validation_error("Le tournoi a déjà commencé.")
            return
        
        if len(tournament.players) < 2:
            self.view.display_validation_error(
                "Il faut au moins 2 joueurs inscrits pour démarrer."
            )
            return

        players_list = list(tournament.players)
        random.shuffle(players_list)

        matches = []
        for i in range(0, len(players_list), 2):
            if i + 1 == len(players_list):
                # Odd number: give bye to last player
                player = players_list[i]
                self.tournament_manager.add_points_to_player(
                    tournament, player.player_id, 1.0
                )
                self.tournament_manager.add_opponent_to_player(
                    tournament, player.player_id, -1
                )
                break
    
            player1 = players_list[i]
            player2 = players_list[i+1]
            
            matches.append((
                [player1, 0.0],
                [player2, 0.0]
            ))

        new_round_id = self._get_next_round_id()
        round_name = f"Round {len(tournament.rounds) + 1}"
        
        new_round = Round(
            name=round_name,
            matches=matches,
            round_id=new_round_id
        )

        tournament.rounds.append(new_round)
        
        all_tournaments = self.tournament_manager.load_items()
        for i, t in enumerate(all_tournaments):
            if t.tournament_id == tournament.tournament_id:
                all_tournaments[i] = tournament
                break
        
        self.tournament_manager.save_items(all_tournaments)
        self.view.display_round_started(new_round.name, len(matches))

    # ========================================
    # ROUND MANAGEMENT: ENTER RESULTS
    # ========================================

    def _enter_round_results(self, tournament):
        """
        Record match results for the current round.
        
        Workflow:
        1. Validate round exists and not yet completed
        2. For each match, prompt for result
        3. Update player scores via manager
        4. Update opponent history via manager
        5. Mark round as complete
        6. Save tournament
        7. Generate next round OR display tournament finished
        
        Args:
            tournament (Tournament): Tournament with matches to record
        """
        if not tournament.rounds:
            self.view.display_validation_error("Erreur : Aucun round n'a été lancé.")
            return
        
        current_round = tournament.rounds[-1]

        if current_round.end_date_time is not None:
            self.view.display_validation_error(
                f"Les résultats pour le {current_round.name} ont déjà été saisis."
            )
            return

        updated_matches = []
        
        for match_tuple in current_round.matches:
            player_a = match_tuple[0][0]
            player_b = match_tuple[1][0]
                
            while True:
                result_str = self.view.prompt_for_match_result(player_a, player_b)
                if result_str not in ["1", "2", "3"]:
                    self.view.display_validation_error("Veuillez entrer 1, 2, ou 3.")
                else:
                    break
            
            if result_str == "1":
                score_a, score_b = 1.0, 0.0
            elif result_str == "2":
                score_a, score_b = 0.0, 1.0
            else:
                score_a, score_b = 0.5, 0.5

            self.tournament_manager.add_points_to_player(
                tournament, player_a.player_id, score_a
            )
            self.tournament_manager.add_points_to_player(
                tournament, player_b.player_id, score_b
            )
            
            self.tournament_manager.add_opponent_to_player(
                tournament, player_a.player_id, player_b.player_id
            )
            self.tournament_manager.add_opponent_to_player(
                tournament, player_b.player_id, player_a.player_id
            )
            
            updated_matches.append(([player_a, score_a], [player_b, score_b]))

        current_round.matches = updated_matches
        current_round.end_date_time = datetime.now().isoformat()
        tournament.current_round += 1

        all_tournaments = self.tournament_manager.load_items()
        for i, t in enumerate(all_tournaments):
            if t.tournament_id == tournament.tournament_id:
                all_tournaments[i] = tournament
                break
        self.tournament_manager.save_items(all_tournaments)

        self.view.display_results_saved(current_round.name)
        
        if len(tournament.rounds) < tournament.number_of_rounds:
            self._generate_next_round(tournament)
        else:
            self.view.display_tournament_finished()

    # ========================================
    # SWISS PAIRING ALGORITHM
    # ========================================

    def _generate_next_round(self, tournament):
        """
        Generate the next round using Swiss system pairing.
        
        Swiss System Algorithm:
        1. Get all players with their scores and opponent history
        2. Sort players by score (highest first)
        3. Pair players from top to bottom:
           - Try to pair with next unpaired player
           - Skip if they've already played each other
           - Force pairing if no valid opponent (rematch as last resort)
        4. Handle odd player with bye:
           - Prioritize players who haven't had a bye (-1 in history)
           - Give 1 point and mark -1 in opponent history
        5. Create Round object and save
        
        Args:
            tournament (Tournament): Tournament to generate round for
        """
        # Step 1: Get player data
        players_with_scores = []
        for player in tournament.players:
            score_data = self.tournament_manager.get_player_score(
                tournament, player.player_id
            )
            players_with_scores.append({
                'player': player,
                'score': score_data['total_points'],
                'opponents': score_data['opponents_history']
            })
        
        # Step 2: Sort by score (highest first)
        players_with_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Step 3: Create pairings
        matches = []
        paired_player_ids = set()
        
        for i, player_data in enumerate(players_with_scores):
            if player_data['player'].player_id in paired_player_ids:
                continue
            
            player_a = player_data['player']
            opponent_found = False
            
            # Try to find valid opponent (haven't played before)
            for j in range(i + 1, len(players_with_scores)):
                candidate_data = players_with_scores[j]
                
                if candidate_data['player'].player_id in paired_player_ids:
                    continue
                
                player_b = candidate_data['player']
                
                if player_b.player_id not in player_data['opponents']:
                    matches.append(([player_a, 0.0], [player_b, 0.0]))
                    paired_player_ids.add(player_a.player_id)
                    paired_player_ids.add(player_b.player_id)
                    opponent_found = True
                    break
            
            # Force pairing if no valid opponent found
            if not opponent_found:
                for j in range(i + 1, len(players_with_scores)):
                    candidate_data = players_with_scores[j]
                    
                    if candidate_data['player'].player_id in paired_player_ids:
                        continue
                    
                    player_b = candidate_data['player']
                    matches.append(([player_a, 0.0], [player_b, 0.0]))
                    paired_player_ids.add(player_a.player_id)
                    paired_player_ids.add(player_b.player_id)
                    break
        
        # Step 4: Handle bye if odd number of players
        if len(paired_player_ids) < len(tournament.players):
            self._assign_bye(
                tournament, players_with_scores, paired_player_ids
            )
        
        # Step 5: Create and save round
        new_round_id = self._get_next_round_id()
        round_name = f"Round {len(tournament.rounds) + 1}"
        
        new_round = Round(
            name=round_name,
            matches=matches,
            round_id=new_round_id
        )
        
        tournament.rounds.append(new_round)
        
        all_tournaments = self.tournament_manager.load_items()
        for i, t in enumerate(all_tournaments):
            if t.tournament_id == tournament.tournament_id:
                all_tournaments[i] = tournament
                break
        
        self.tournament_manager.save_items(all_tournaments)
        self.view.display_round_started(new_round.name, len(matches))

    def _assign_bye(self, tournament, players_with_scores, paired_player_ids):
        """
        Assign a bye to an unpaired player.
        
        Priority: Players who haven't had a bye yet (-1 not in opponent history)
        
        Args:
            tournament (Tournament): The tournament
            players_with_scores (list): List of player data dicts
            paired_player_ids (set): Set of already paired player IDs
        """
        # Try to find player without previous bye
        for player_data in players_with_scores:
            if player_data['player'].player_id not in paired_player_ids:
                if -1 not in player_data['opponents']:
                    bye_player = player_data['player']
                    self.tournament_manager.add_points_to_player(
                        tournament, bye_player.player_id, 1.0
                    )
                    self.tournament_manager.add_opponent_to_player(
                        tournament, bye_player.player_id, -1
                    )
                    paired_player_ids.add(bye_player.player_id)
                    return
        
        # If all have had bye, give to first unpaired
        for player_data in players_with_scores:
            if player_data['player'].player_id not in paired_player_ids:
                bye_player = player_data['player']
                self.tournament_manager.add_points_to_player(
                    tournament, bye_player.player_id, 1.0
                )
                self.tournament_manager.add_opponent_to_player(
                    tournament, bye_player.player_id, -1
                )
                break

    # ========================================
    # HELPER METHODS
    # ========================================

    def _get_next_round_id(self):
        """
        Generate the next available round ID across all tournaments.
        
        Returns:
            int: Next available round ID
        """
        all_tournaments = self.tournament_manager.load_items()
        all_round_ids = []
        
        for t in all_tournaments:
            for r in t.rounds:
                if r.round_id:
                    all_round_ids.append(r.round_id)
        
        max_id = max(all_round_ids) if all_round_ids else 0
        return max_id + 1

    def _prompt_user_for_tournament(self, tournaments):
        """
        Display tournament selection menu and get user choice.
        
        Args:
            tournaments (list): List of Tournament objects
        
        Returns:
            Tournament: Selected tournament, or None if cancelled
        """
        items_as_strings = [
            f"{i}. {t.name} (ID: {t.tournament_id})"
            for i, t in enumerate(tournaments, 1)
        ]
            
        if not self.view.display_selection_list(
            "Sélectionner un Tournoi", items_as_strings
        ):
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
        Display player selection menu and get user choice.
        
        Args:
            players (list): List of Player objects
        
        Returns:
            Player: Selected player, or None if cancelled
        """
        items_as_strings = [
            f"{i}. {p.last_name} {p.first_name} (ID: {p.player_id})"
            for i, p in enumerate(players, 1)
        ]

        if not self.view.display_selection_list(
            "Sélectionner un Joueur", items_as_strings
        ):
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
