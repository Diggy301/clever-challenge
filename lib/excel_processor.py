import pandas
import pathlib
import sqlite3


class ExcelProcessor:
    """
    A class to process Excel files and store the data in a SQLite database.
    """
    def __init__(self, db_path: pathlib.Path, table_name: str) -> None:
        """
        Initializes the ExcelProcessor with the database path and table name.

        :param db_path: The path to the SQLite database file.
        :param table_name: The name of the table where data will be inserted.
        """
        self.db_path = db_path
        self.table_name = table_name

    def create_table(self) -> None:
        """
        Creates a table in the SQLite database if it doesn't already exist.

        The table schema is based on a 2-column structure for Excel data.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Adjust table schema based on the 2-column Excel structure
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            column1 TEXT,
            column2 TEXT
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        connection.close()

    def insert_data(self, data: list[tuple[str]]) -> None:
        """
        Inserts data into the SQLite table.

        :param data: A list of tuples representing the rows to be inserted.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Insert data (tuple for each row)
        insert_query = f"INSERT INTO {self.table_name} (column1, column2) VALUES (?, ?)"
        cursor.executemany(insert_query, data)
        connection.commit()
        connection.close()

    def process_excel_file(self, file_path: pathlib.Path) -> None:
        """
        Processes Excel file to read data from the 'Plan1' sheet and inserts it into the SQLite database.

        :param file_path: The path to the Excel file to be processed.
        """
        try:
            # Read Excel file and the specific sheet 'Plan1'
            df = pandas.read_excel(file_path, sheet_name="Plan1")

            # Drop the first row
            df = df.iloc[1:]

            # Convert the DataFrame to a list of tuples
            data = df.to_records(index=False)

            # Create the table and insert data into SQLite
            self.create_table()
            self.insert_data(data)
            print(f"Processed {file_path} and inserted data into {self.table_name}.")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")