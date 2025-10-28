from managers.base_manager import BaseManager

class AutoIncrementManager(BaseManager):
    """
    Inherits from BaseManager and adds functionality
    to automatically generate incrementing integer IDs.
    """
    def __init__(self, file_path, model_class, id_attribute_name):
        """
        Initializes the manager.

        Args:
            file_path (str): Path to the JSON file.
            model_class (class): The model to manage (e.g., Tournament).
            id_attribute_name (str): The name of the ID attribute 
                                     on the model (e.g., "tournament_id").
        """
        super().__init__(file_path, model_class)
        self.id_attribute_name = id_attribute_name

    def get_next_id(self):
        """
        Loads all items, finds the maximum ID, and returns the next ID.
        """
        items = self.load_all()
        if not items:
            return 1

        ids = []
        for item in items:
            item_id = getattr(item, self.id_attribute_name, None)
            if item_id is not None:
                ids.append(item_id)
        
        max_id = max(ids) if ids else 0
        return max_id + 1