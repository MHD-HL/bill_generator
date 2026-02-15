import sqlite3


class DataBaseManager:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name: str, columns: dict):
        try:
            columns_with_types = ", ".join(
                [f"{col_name} {attributes}" for col_name, attributes in columns.items()]
            )
            create_table_query = (
                f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
            )
            self.cursor.execute(create_table_query)
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"An error occurred while creating the table: {e}")

    def insert_data(self, table_name: str, data: list[dict]):
        try:
            for entry in data:
                columns = ", ".join(entry.keys())
                placeholders = ", ".join(["?" for _ in entry])
                insert_query = (
                    f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                )
                self.cursor.execute(insert_query, tuple(entry.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"An error occurred while inserting data: {e}")

    def update_data(self, table_name: str, updates: dict, condition: str):
        try:
            set_clause = ", ".join([f"{col} = ?" for col in updates.keys()])
            update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            self.cursor.execute(update_query, tuple(updates.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            return [f"An error occurred while updating data: {e}"]

    def delete_data(self, table_name: str, condition: str):
        try:
            delete_query = f"DELETE FROM {table_name} WHERE {condition}"
            self.cursor.execute(delete_query)
            self.conn.commit()
        except sqlite3.Error as e:
            return [f"An error occurred while deleting data: {e}"]

    def get_data(
        self, table_name: str, columns: str | list[str] = None, condition: str = None
    ):
        try:
            if columns is None and condition is None:
                self.cursor.execute(f"SELECT * FROM {table_name}")
            elif condition is None:
                columns_str = (
                    ", ".join(columns) if isinstance(columns, list) else columns
                )
                self.cursor.execute(f"SELECT {columns_str} FROM {table_name}")
            else:
                columns_str = (
                    ", ".join(columns) if isinstance(columns, list) else columns
                )
                self.cursor.execute(
                    f"SELECT {columns_str} FROM {table_name} WHERE {condition}"
                )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return [f"An error occurred while retrieving data: {e}"]

    def execute_query(self, query: str, params: tuple = ()): 
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return [f"An error occurred while executing query: {e}"]

    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            return [f"An error occurred while closing the connection: {e}"]
