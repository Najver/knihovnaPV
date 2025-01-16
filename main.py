from menu import display_main_menu, handle_submenu
from menu import handle_report_menu
from menu import handle_import_menu

def main():
    tables = ["aktualnivypujcky", "autori", "knihy", "knihy_autori", "nejvicepujcovaneknihy", "uzivatele", "vypujcky"]

    while True:
        display_main_menu()
        choice = input("Vyberte tabulku nebo akci (1-10): ")

        if choice in [str(i) for i in range(1, len(tables) + 1)]:
            handle_submenu(tables[int(choice) - 1])

        elif choice == "8":
            handle_report_menu()

        elif choice == "9":
            handle_import_menu()

        elif choice == "10":
            print("Ukončuji aplikaci.")
            break

        else:
            print("Neplatná volba, zkuste to znovu.")


if __name__ == "__main__":
    main()