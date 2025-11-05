class ReportView:
    """
    Handles the display of all reports in a generic way.
    This view is "dumb" and only prints what it is given.
    """
    
    def display_table(self, title, headers, rows):
        """
        Displays a formatted table based on provided data.

        Args:
            title (str): The title to print above the table.
            headers (list): A list of strings for the column headers.
            rows (list): A list of lists, where each inner list
                         represents a row's data.
        """
        print(f"\n--- {title} ---")
        
        if not rows:
            print("Aucune donnée à afficher.")
            return

        # 1. Calculate column widths based on headers and data
        num_columns = len(headers)
        # Initialize widths with header lengths
        col_widths = [len(h) for h in headers]

        # Check data for wider content
        for row in rows:
            for i in range(num_columns):
                cell_width = len(str(row[i]))
                if cell_width > col_widths[i]:
                    col_widths[i] = cell_width

        # 2. Print Headers
        header_line = ""
        separator_line = ""
        for i in range(num_columns):
            # Add 2 spaces for padding
            width = col_widths[i] + 2
            header_line += f"{headers[i]:<{width}}"
            separator_line += "-" * width
        
        print(header_line)
        print(separator_line)

        # 3. Print Rows
        for row in rows:
            row_line = ""
            for i in range(num_columns):
                width = col_widths[i] + 2
                row_line += f"{str(row[i]):<{width}}"
            print(row_line)
        
        print(separator_line)