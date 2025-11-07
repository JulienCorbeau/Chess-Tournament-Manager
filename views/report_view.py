class ReportView:
    """
    Handles the display of all reports.
    This view is "dumb" and only prints a table.
    The controller prepares all the data.
    """
    
    def display_table(self, title, headers, rows):
        """
        Displays a formatted table based on provided data.

        Args:
            title (str): The title to print above the table.
            headers (list): A list of strings for the column headers.
            rows (list): A list of lists, where each inner list
                         is a row (e.g., [1, "John", "Doe"]).
        """
        print(f"\n--- {title} ---")
        
        if not rows:
            print("Aucune donnée à afficher.")
            return

        # 1. Calculate the width needed for each column
        num_columns = len(headers)
        # Start with the width of the headers
        col_widths = [len(h) for h in headers]

        # Check all data rows to find the widest cell in each column
        for row in rows:
            for i in range(num_columns):
                cell_width = len(str(row[i]))
                if cell_width > col_widths[i]:
                    col_widths[i] = cell_width

        # 2. Print Headers
        header_line = ""
        separator_line = ""
        for i in range(num_columns):
            width = col_widths[i] + 2  # Add 2 spaces for padding
            header_line += f"{headers[i]:<{width}}"
            separator_line += "-" * width
        
        print(header_line)
        print(separator_line)

        # 3. Print Data Rows
        for row in rows:
            row_line = ""
            for i in range(num_columns):
                width = col_widths[i] + 2  # Add 2 spaces
                row_line += f"{str(row[i]):<{width}}"
            print(row_line)
        
        print(separator_line)