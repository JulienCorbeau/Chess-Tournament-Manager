"""
Player Model

Represents a chess player in the tournament management system.
This is a data model (anemic pattern) - it contains only data attributes
and serialization logic. Business logic is handled by managers.
"""


class Player:
    """
    A chess player with personal information and identification.
    
    Attributes:
        player_id (int): Unique internal identifier
        last_name (str): Player's last name
        first_name (str): Player's first name
        date_of_birth (str): Birth date in YYYY-MM-DD format
        national_id (str): National chess federation ID (e.g., "AB12345")
    """

    def __init__(
        self,
        last_name,
        first_name,
        date_of_birth,
        national_id,
        player_id=None,
    ):
        """
        Initialize a new Player instance.
        
        Args:
            last_name (str): Player's last name
            first_name (str): Player's first name
            date_of_birth (str): Birth date in YYYY-MM-DD format
            national_id (str): National chess federation ID
            player_id (int, optional): Unique identifier. Auto-generated if None.
        """
        self.player_id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id

    def to_dict(self):
        """
        Convert the Player object to a dictionary for JSON serialization.
        
        Returns:
            dict: Player data as a dictionary
        """
        return {
            "player_id": self.player_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id,
        }
