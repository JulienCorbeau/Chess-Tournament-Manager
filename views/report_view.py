"""
Report View

Handles display of formatted reports and tables.
This is a "dumb" view - it only displays pre-formatted data.
Controllers prepare all data and formatting.
"""


class ReportView:
    """
    Console-based view for displaying reports in table format.
    
    This view receives fully formatted data from controllers
    and displays it without any data processing.
    """

    def display_table(self, title, headers, rows):
        """
        Display data in a formatted table.
        
        Args:
            title (str): Table title
            headers (list): Column headers
            rows (list): List of row data (each row is a list)
        
        Example:
            title = "All Players"
            headers = ["ID", "Name", "Score"]
            rows = [[1, "John", 5], [2, "Jane", 7]]
        """
        print(f"\n--- {title} ---")
        
        if not rows:
            print("Aucune donnée à afficher.")
            return

        # Calculate column widths based on content
        num_columns = len(headers)
        col_widths = [len(h) for h in headers]

        for row in rows:
            for i in range(num_columns):
                cell_width = len(str(row[i]))
                if cell_width > col_widths[i]:
                    col_widths[i] = cell_width

        # Build and print header
        header_line = ""
        separator_line = ""
        for i in range(num_columns):
            width = col_widths[i] + 2  # Add padding
            header_line += f"{headers[i]:<{width}}"
            separator_line += "-" * width
        
        print(header_line)
        print(separator_line)

        # Print data rows
        for row in rows:
            row_line = ""
            for i in range(num_columns):
                width = col_widths[i] + 2
                row_line += f"{str(row[i]):<{width}}"
            print(row_line)
        
        print(separator_line)
