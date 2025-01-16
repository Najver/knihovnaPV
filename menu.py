from active_record import ActiveRecord
from database import Database
from report import report_books, report_users, report_loans

def display_main_menu():
    print("\n--- Hlavní menu ---")
    print("1. Aktuální výpůjčky")
    print("2. Autoři")
    print("3. Knihy")
    print("4. Knihy-Autoři")
    print("5. Nejvíce půjčované knihy")
    print("6. Uživatelé")
    print("7. Výpůjčky")
    print("8. Generovat souhrnný report")
    print("9. Ukončit")

def display_submenu(table_name):
    print(f"\n--- Menu pro tabulku {table_name} ---")
    print("1. Zobrazit všechna data")
    print("2. Vyhledat podle ID")
    print("3. Vložit nový záznam")
    print("4. Upravit záznam podle ID")
    print("5. Smazat záznam podle ID")
    if table_name == "vypujcky":
        print("6. Přidat výpůjčku (transakce)")
    print("6. Zpět" if table_name != "vypujcky" else "7. Zpět")

def display_report_menu():
    print("\n--- Reporty ---")
    print("1. Report o knihách")
    print("2. Report o uživatelích")
    print("3. Report o výpůjčkách")
    print("4. Zpět do hlavního menu")


def handle_submenu(table_name):
    table = ActiveRecord(table_name)
    db = Database()
    columns = db.get_columns(table_name)

    while True:
        display_submenu(table_name)
        choice = input("Vyberte akci (1-7): ")

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

        elif choice == "6" and table_name == "vypujcky":
            add_vypujcka_with_transaction()

        elif choice == "6" or (choice == "7" and table_name == "vypujcky"):
            break


        else:
            print("Neplatná volba, zkuste to znovu.")

def handle_report_menu():
    while True:
        display_report_menu()
        choice = input("Vyberte report (1-4): ")

        if choice == "1":
            report_books()
        elif choice == "2":
            report_users()
        elif choice == "3":
            report_loans()
        elif choice == "4":
            print("Návrat do hlavního menu.")
            break
        else:
            print("Neplatná volba, zkuste to znovu.")

def add_vypujcka_with_transaction():
    table = ActiveRecord("vypujcky")
    db = Database()

    try:
        kniha_id = int(input("Zadejte ID knihy: "))
        uzivatel_id = int(input("Zadejte ID uživatele: "))
        datum_vypujceni = input("Zadejte datum výpůjčky (YYYY-MM-DD): ")

        # Kontrola existence knihy
        db.cursor.execute("SELECT id FROM knihy WHERE id = %s", (kniha_id,))
        if not db.cursor.fetchone():
            print("Kniha neexistuje.")
            return

        # Kontrola existence uživatele
        db.cursor.execute("SELECT id FROM uzivatele WHERE id = %s", (uzivatel_id,))
        if not db.cursor.fetchone():
            print("Uživatel neexistuje.")
            return

        # Transakce: Přidání výpůjčky a případná aktualizace knihy
        queries = [
            (
                "INSERT INTO vypujcky (kniha_id, uzivatel_id, datum_vypujceni) VALUES (%s, %s, %s)",
                (kniha_id, uzivatel_id, datum_vypujceni)
            ),
            (
                "UPDATE knihy SET cena = cena - 10 WHERE id = %s",  # Například snížení ceny knihy
                (kniha_id,)
            )
        ]

        table.execute_transaction(queries)
        print("Výpůjčka byla úspěšně přidána.")

    except ValueError:
        print("Neplatný vstup, zkuste to znovu.")
    except Exception as e:
        print(f"Chyba: {e}")
