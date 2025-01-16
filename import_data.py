import csv
import json
import xml.etree.ElementTree as ET
from database import Database

def import_csv(table_name, file_path):
    db = Database()
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                placeholders = ", ".join(["%s"] * len(row))
                columns = ", ".join(row.keys())
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                db.cursor.execute(query, tuple(row.values()))
            db.connection.commit()
            print(f"Data z CSV byla úspěšně importována do tabulky '{table_name}'.")
    except Exception as e:
        print(f"Chyba při importu CSV: {e}")
    finally:
        db.close()

def import_json(table_name, file_path):
    db = Database()
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            data = json.load(file)
            for row in data:
                placeholders = ", ".join(["%s"] * len(row))
                columns = ", ".join(row.keys())
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                db.cursor.execute(query, tuple(row.values()))
            db.connection.commit()
            print(f"Data z JSON byla úspěšně importována do tabulky '{table_name}'.")
    except Exception as e:
        print(f"Chyba při importu JSON: {e}")
    finally:
        db.close()

def import_xml(table_name, file_path):
    db = Database()
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for record in root.findall("record"):
            data = {child.tag: child.text for child in record}
            placeholders = ", ".join(["%s"] * len(data))
            columns = ", ".join(data.keys())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            db.cursor.execute(query, tuple(data.values()))
        db.connection.commit()
        print(f"Data z XML byla úspěšně importována do tabulky '{table_name}'.")
    except Exception as e:
        print(f"Chyba při importu XML: {e}")
    finally:
        db.close()
