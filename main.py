from menu import display_main_menu, handle_submenu

def main():
    tables = ["aktualnivypujcky", "autori", "knihy", "knihy_autori", "nejvicepujcovaneknihy", "uzivatele", "vypujcky"]

    while True:
        display_main_menu()
        choice = input("Vyberte tabulku (1-8): ")

        if choice in [str(i) for i in range(1, len(tables) + 1)]:
            handle_submenu(tables[int(choice) - 1])

        elif choice == "8":
            print("Ukončuji aplikaci.")
            break

        else:
            print("Neplatná volba, zkuste to znovu.")

if __name__ == "__main__":
    main()