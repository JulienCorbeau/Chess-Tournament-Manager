import json
import os

class BaseManager:
    """
    Provides generic methods for loading and saving model instances
    to a JSON file.
    """
    def __init__(self, file_path, model_class):
        """
        Initializes the manager, sets the file path, and
        stores the model class it will manage.

        Args:
            file_path (str): The path to the JSON file.
            model_class (class): The class (e.g., Player, Tournament)
                                 to use for deserialization.
        """
        self.file_path = file_path
        self.model_class = model_class
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        dir_name = os.path.dirname(self.file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def _load_data(self):
        """Loads raw data from the JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data):
        """Saves raw data to the JSON file."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_all(self):
        """
        Loads all items from the JSON file and converts
        them into model instances.
        """
        raw_data = self._load_data()
        # Use the stored model_class to deserialize
        return [self.model_class(**data) for data in raw_data]

    def save_all(self, items):
        """
        Takes a list of model instances, serializes them
        to dictionaries, and saves them to the JSON file.
        """
        data_to_save = [item.to_dict() for item in items]
        self._save_data(data_to_save)