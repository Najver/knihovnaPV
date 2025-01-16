from database import Database

class ActiveRecord:
    def __init__(self, table):
        self.table = table
        self.db = Database()

    def all(self):
        query = f"SELECT * FROM {self.table}"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def find(self, record_id):
        # Dynamicky načte seznam sloupců
        columns = self.db.get_columns(self.table)
        # Zjistí, který sloupec použít jako klíč (předpoklad: 'id' nebo první sloupec)
        primary_key = "id" if "id" in columns else columns[0]
        query = f"SELECT * FROM {self.table} WHERE {primary_key} = %s"
        self.db.cursor.execute(query, (record_id,))
        return self.db.cursor.fetchone()

    def insert(self, data):
        placeholders = ", ".join(["%s"] * len(data))
        columns = ", ".join(data.keys())
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        self.db.cursor.execute(query, tuple(data.values()))
        self.db.connection.commit()
        return self.db.cursor.lastrowid

    def update(self, record_id, data):
        placeholders = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {self.table} SET {placeholders} WHERE id = %s"
        self.db.cursor.execute(query, tuple(data.values()) + (record_id,))
        self.db.connection.commit()

    def delete(self, record_id):
        query = f"DELETE FROM {self.table} WHERE id = %s"
        self.db.cursor.execute(query, (record_id,))
        self.db.connection.commit()

    def execute_transaction(self, queries_with_data):
        try:
            for query, data in queries_with_data:
                self.db.cursor.execute(query, data)
            self.db.connection.commit()
            print("Transakce byla úspěšně dokončena.")
        except Exception as e:
            self.db.connection.rollback()
            print(f"Transakce selhala: {e}")
