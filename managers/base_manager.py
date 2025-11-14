import json
import os

class BaseManager:
    """
    Provides generic (all-purpose) methods for loading, saving,
    and managing model instances (like Player or Tournament)
    to a JSON file.
    It also handles creating new auto-incrementing IDs.
    """
    def __init__(self, file_path, model_class, id_attribute_name):
        """
        Initializes the manager.
        This is called by the "child" managers (PlayerManager, etc.).

        Args:
            file_path (str): The path to the JSON file (e.g., "data/players.json").
            model_class (class): The object type to create (e.g., Player).
            id_attribute_name (str): The name of the ID field (e.g., "player_id").
        """
        self.file_path = file_path
        self.model_class = model_class  # The "mold" to create objects (e.g., Player)
        self.id_attribute_name = id_attribute_name 
        self._ensure_file_exists()  # Check if the file exists

    def _ensure_file_exists(self):
        """
        Internal helper. Checks if the file and its directory exist.
        If not, it creates them.
        """
        dir_name = os.path.dirname(self.file_path)  # Get the folder part
        if dir_name:  # If there is a folder 
            os.makedirs(dir_name, exist_ok=True)  # Create it (don't crash if it exists)
            
        # If the file itself does not exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)  # Create an empty file with an empty list

    def _load_data(self):
        """Internal helper. Loads raw data from the JSON file."""
        try:
            # Open the file with UTF-8 (for accents)
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)  # Read the data
        except (json.JSONDecodeError, FileNotFoundError):
            return []  # Return empty list if file is broken or missing

    def _save_data(self, data):
        """Internal helper. Saves raw data to the JSON file."""
        # Open the file with UTF-8 (for accents)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            # Save formatted (indent=4) and keep accents (ensure_ascii=False)
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_items(self):
        """
        Loads all items from the JSON file and converts
        them into model instances (objects).
        """
        raw_data = self._load_data()  # Get the raw list of dicts
        
        # Use the "mold" (self.model_class) to turn each dict into an object
        # e.g., [Player(**data), Player(**data), ...]
        return [self.model_class(**data) for data in raw_data]

    def save_items(self, items):
        """
        Takes a list of model instances (objects), serializes them
        (turns them into dicts), and saves them to the JSON file.
        """
        # Call the .to_dict() method on each object
        data_to_save = [item.to_dict() for item in items]
        self._save_data(data_to_save)

    def get_next_id(self):
        """
        Loads all items, finds the maximum ID, and returns the next ID.
        This is our auto-increment logic.
        """
        items = self.load_items()  # Load all objects
        if not items:
            return 1  # If no items, start at 1

        ids = []
        for item in items:
            # Get the ID value (e.g., item.player_id)
            item_id = getattr(item, self.id_attribute_name, None)
            if item_id is not None:
                ids.append(item_id)
        
        # Find the biggest ID, or 0 if the list is empty
        max_id = max(ids) if ids else 0
        return max_id + 1

    def add_item(self, item):
        """
        Adds a new item to the storage file.
        """
        items = self.load_items()  # 1. Load all items
        items.append(item)        # 2. Add the new one
        self.save_items(items)    # 3. Save the full list

    def get_item_by_id(self, item_id):
        """
        Finds and returns a single item by its ID.
        Returns None if not found.
        """
        all_items = self.load_items()
        for item in all_items:
            if getattr(item, self.id_attribute_name) == item_id:
                return item
        return None

    def get_items_by_ids(self, ids):
        """
        Finds and returns a list of items from a list of IDs.
        """
        all_items = self.load_items()
        id_set = set(ids) 
        found_items = []
        for item in all_items:
            if getattr(item, self.id_attribute_name) in id_set:
                found_items.append(item)
        return found_items