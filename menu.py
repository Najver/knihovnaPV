from active_record import ActiveRecord
from database import Database

def display_main_menu():
    print("\n--- Hlavní menu ---")
    print("1. Aktuální výpůjčky")
    print("2. Autoři")
    print("3. Knihy")
    print("4. Knihy-Autoři")
    print("5. Nejvíce půjčované knihy")
    print("6. Uživatelé")
    print("7. Výpůjčky")
    print("8. Ukončit")

def display_submenu(table_name):
    print(f"\n--- Menu pro tabulku {table_name} ---")
    print("1. Zobrazit všechna data")
    print("2. Vyhledat podle ID")
    print("3. Vložit nový záznam")
    print("4. Upravit záznam podle ID")
    print("5. Smazat záznam podle ID")
    print("6. Zpět")

def handle_submenu(table_name):
    table = ActiveRecord(table_name)
    db = Database()
    columns = db.get_columns(table_name)

    while True:
        display_submenu(table_name)
        choice = input("Vyberte akci (1-6): ")

        if choice == "1":
            records = table.all()
            for record in records:
                print(record)

        elif choice == "2":
            try:
                record_id = int(input("Zadejte ID: "))
                record = table.find(record_id)
                if record:
                    print(record)
                else:
                    print("Záznam nebyl nalezen.")
            except ValueError:
                print("Neplatné ID, zkuste to znovu.")

        elif choice == "3":
            data = {}
            for column in columns:
                if column != "id":
                    data[column] = input(f"Zadejte hodnotu pro {column}: ")
            try:
                record_id = table.insert(data)
                print(f"Nový záznam byl vložen s ID {record_id}.")
            except Exception as e:
                print(f"Chyba při vkládání: {e}")

        elif choice == "4":
            try:
                record_id = int(input("Zadejte ID záznamu k úprave: "))
                data = {}
                for column in columns:
                    if column != "id":
                        data[column] = input(f"Zadejte novou hodnotu pro {column}: ")
                table.update(record_id, data)
                print("Záznam byl úspěšně upraven.")
            except ValueError:
                print("Neplatné ID, zkuste to znovu.")
            except Exception as e:
                print(f"Chyba při úprave: {e}")

        elif choice == "5":
            try:
                record_id = int(input("Zadejte ID záznamu k odstranění: "))
                table.delete(record_id)
                print("Záznam byl úspěšně smazán.")
            except ValueError:
                print("Neplatné ID, zkuste to znovu.")
            except Exception as e:
                print(f"Chyba při mazání: {e}")

        elif choice == "6":
            break

        else:
            print("Neplatná volba, zkuste to znovu.")