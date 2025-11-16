"""
Base Manager

Generic data persistence manager for model objects.
Handles JSON file operations, ID generation, and basic CRUD operations.
This class uses the Template Method pattern - child managers specify
the file path, model class, and ID attribute name.

Data Flow:
    Load:  JSON file -> Python dict -> Model object (hydration)
    Save:  Model object -> Python dict -> JSON file (dehydration)
"""

import json
import os


class BaseManager:
    """
    Abstract base manager for data persistence.
    
    Provides generic methods for loading, saving, and managing model instances
    in JSON files with auto-incrementing IDs.
    
    Attributes:
        file_path (str): Path to the JSON storage file
        model_class (class): The model class to instantiate (e.g., Player, Tournament)
        id_attribute_name (str): Name of the ID field (e.g., "player_id")
    """

    def __init__(self, file_path, model_class, id_attribute_name):
        """
        Initialize the base manager.
        
        Args:
            file_path (str): Path to JSON file (e.g., "data/players.json")
            model_class (class): Model class to create instances from
            id_attribute_name (str): Name of the ID attribute
        """
        self.file_path = file_path
        self.model_class = model_class
        self.id_attribute_name = id_attribute_name
        self._ensure_file_exists()

    # ========================================
    # FILE SYSTEM OPERATIONS
    # ========================================

    def _ensure_file_exists(self):
        """
        Create the storage file and its directory if they don't exist.
        Initializes the file with an empty JSON array.
        """
        dir_name = os.path.dirname(self.file_path)
        
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def _load_data(self):
        """
        Load raw data from the JSON file.
        
        Returns:
            list: List of dictionaries from JSON file, or empty list if error
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data):
        """
        Save raw data to the JSON file.
        
        Args:
            data (list): List of dictionaries to save
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ========================================
    # CRUD OPERATIONS
    # ========================================

    def load_items(self):
        """
        Load all items from JSON and convert them to model objects.
        
        This performs "hydration": raw dict data -> model instances
        
        Returns:
            list: List of model instances (e.g., [Player, Player, ...])
        """
        raw_data = self._load_data()
        return [self.model_class(**data) for data in raw_data]

    def save_items(self, items):
        """
        Convert model objects to dictionaries and save to JSON.
        
        This performs "dehydration": model instances -> raw dict data
        
        Args:
            items (list): List of model instances to save
        """
        data_to_save = [item.to_dict() for item in items]
        self._save_data(data_to_save)

    def add_item(self, item):
        """
        Add a new item to the storage.
        
        Args:
            item: Model instance to add (must have to_dict() method)
        """
        items = self.load_items()
        items.append(item)
        self.save_items(items)

    # ========================================
    # ID MANAGEMENT
    # ========================================

    def get_next_id(self):
        """
        Generate the next available ID using auto-increment logic.
        
        Finds the maximum existing ID and returns max + 1.
        
        Returns:
            int: Next available ID (starts at 1 if no items exist)
        """
        items = self.load_items()
        
        if not items:
            return 1

        ids = [
            getattr(item, self.id_attribute_name)
            for item in items
            if getattr(item, self.id_attribute_name, None) is not None
        ]
        
        max_id = max(ids) if ids else 0
        return max_id + 1

    # ========================================
    # QUERY OPERATIONS
    # ========================================

    def get_item_by_id(self, item_id):
        """
        Find and return a single item by its ID.
        
        Args:
            item_id (int): ID to search for
            
        Returns:
            Model instance if found, None otherwise
        """
        all_items = self.load_items()
        
        for item in all_items:
            if getattr(item, self.id_attribute_name) == item_id:
                return item
        
        return None

    def get_items_by_ids(self, ids):
        """
        Find and return multiple items by their IDs.
        
        Args:
            ids (list): List of IDs to search for
            
        Returns:
            list: List of found model instances
        """
        all_items = self.load_items()
        id_set = set(ids)
        
        found_items = [
            item for item in all_items
            if getattr(item, self.id_attribute_name) in id_set
        ]
        
        return found_items
