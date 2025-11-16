"""
Round Model

Represents a single round in a chess tournament.
Each round contains a list of matches and timing information.
"""

import datetime


class Round:
    """
    A tournament round containing multiple matches.
    
    Attributes:
        round_id (int): Unique identifier for the round
        name (str): Round name (e.g., "Round 1", "Round 2")
        matches (list): List of match tuples in format:
                       [([player_obj, score], [player_obj, score]), ...]
        start_date_time (str): Round start time in ISO format
        end_date_time (str): Round end time in ISO format (None if ongoing)
    
    Match tuple structure:
        ([Player_A, score_A], [Player_B, score_B])
        Example: ([<Player obj>, 1.0], [<Player obj>, 0.0])
    """

    def __init__(
        self,
        name,
        matches=None,
        start_date_time=None,
        end_date_time=None,
        round_id=None,
    ):
        """
        Initialize a new Round instance.
        
        Args:
            name (str): Round name (e.g., "Round 1")
            matches (list, optional): List of match tuples. Defaults to empty list.
            start_date_time (str, optional): Start time in ISO format. Defaults to now.
            end_date_time (str, optional): End time in ISO format. None if ongoing.
            round_id (int, optional): Unique identifier. Auto-generated if None.
        """
        self.round_id = round_id
        self.name = name
        self.matches = matches if matches is not None else []
        self.start_date_time = (
            start_date_time if start_date_time else datetime.datetime.now().isoformat()
        )
        self.end_date_time = end_date_time

    def to_dict(self):
        """
        Convert the Round object to a dictionary for JSON serialization.
        
        This method "dehydrates" the round:
        - Converts Player objects in matches to player IDs
        - Preserves scores as-is
        
        Returns:
            dict: Round data with matches containing player IDs instead of objects
        """
        serialized_matches = []
        
        for match_tuple in self.matches:
            # Extract player and score data
            player_a_data = match_tuple[0]  # [player_obj/id, score]
            player_b_data = match_tuple[1]  # [player_obj/id, score]
            
            # Convert Player objects to IDs if needed
            player_a_id = (
                player_a_data[0].player_id
                if hasattr(player_a_data[0], 'player_id')
                else player_a_data[0]
            )
            player_b_id = (
                player_b_data[0].player_id
                if hasattr(player_b_data[0], 'player_id')
                else player_b_data[0]
            )
            
            # Rebuild match tuple with IDs
            serialized_match = (
                [player_a_id, player_a_data[1]],
                [player_b_id, player_b_data[1]]
            )
            serialized_matches.append(serialized_match)

        return {
            "round_id": self.round_id,
            "name": self.name,
            "start_date_time": self.start_date_time,
            "end_date_time": self.end_date_time,
            "matches": serialized_matches,
        }
