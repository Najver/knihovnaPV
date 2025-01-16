import mysql.connector
import configparser

class Database:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.connection = mysql.connector.connect(
            host=config["database"]["host"],
            port=int(config["database"]["port"]),
            user=config["database"]["user"],
            password=config["database"]["password"],
            database=config["database"]["database"]
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def get_columns(self, table):
        query = f"DESCRIBE {table}"
        self.cursor.execute(query)
        return [column["Field"] for column in self.cursor.fetchall()]

    def close(self):
        self.cursor.close()
        self.connection.close()