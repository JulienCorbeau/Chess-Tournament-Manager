import datetime
class Round:
    """
    Represents a single round (like "Round 1") in a tournament.
    It contains a list of matches.
    """
    def __init__(self, name, matches=None, start_date_time=None, 
                 end_date_time=None):
        """
        This is the "builder" for the Round object.

        Args:
            name (str): The name of the round (e.g., "Round 1").
            matches (list): A list of match tuples.
            start_date_time (str): The start time (ISO format string).
            end_date_time (str): The end time (ISO format string).
        """
        self.name = name
        
        # A match is a tuple: ([player_id_A, 0.0], [player_id_B, 0.0])
        self.matches = matches if matches is not None else []
        
        # If no start time is given, set it to "now"
        if start_date_time is None:
            self.start_date_time = datetime.datetime.now().isoformat()
        else:
            self.start_date_time = start_date_time
            
        self.end_date_time = end_date_time  # This is None at the beginning

    def to_dict(self):
        """
        Converts the Round object into a dictionary
        so it can be saved to the JSON file.
        """
        
        # --- Convert Player objects in matches to IDs ---
        serialized_matches = []
        for match_tuple in self.matches:
            # match_tuple = ([player_A_obj, score_A], [player_B_obj, score_B])
            player_a_data = match_tuple[0]  # This is [player_A_obj, score_A]
            player_b_data = match_tuple[1]  # This is [player_B_obj, score_B]
            
            # --- Convert Player A ---
            if hasattr(player_a_data[0], 'player_id'):
                p_a_id = player_a_data[0].player_id  # Get ID from object
            else:
                p_a_id = player_a_data[0]  # It is already an ID
            
            # --- Convert Player B ---
            if hasattr(player_b_data[0], 'player_id'):
                p_b_id = player_b_data[0].player_id  # Get ID from object
            else:
                p_b_id = player_b_data[0]  # It is already an ID

            # Build the match tuple again, but with IDs
            serialized_match = (
                [p_a_id, player_a_data[1]],    # [player_id_A, score_A]
                [p_b_id, player_b_data[1]]     # [player_id_B, score_B]
            )
            serialized_matches.append(serialized_match)

        # Return the final dictionary
        return {
            "name": self.name,
            "start_date_time": self.start_date_time,
            "end_date_time": self.end_date_time,
            "matches": serialized_matches  # Save the converted list of matches
        }