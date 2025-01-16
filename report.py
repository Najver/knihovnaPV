from database import Database

def report_books():
    db = Database()
    try:
        db.cursor.execute("SELECT COUNT(*) AS pocet_knih, MIN(cena) AS nejlevnejsi, MAX(cena) AS nejdrazsi FROM knihy")
        knihy_data = db.cursor.fetchone()

        print("\n--- Report o knihách ---")
        print(f"Počet knih: {knihy_data['pocet_knih']}")
        print(f"Nejlevnější kniha: {knihy_data['nejlevnejsi']} Kč")
        print(f"Nejdražší kniha: {knihy_data['nejdrazsi']} Kč")

    except Exception as e:
        print(f"Chyba při generování reportu o knihách: {e}")

    finally:
        db.close()

def report_users():
    db = Database()
    try:
        db.cursor.execute("SELECT COUNT(*) AS pocet_uzivatelu FROM uzivatele")
        uzivatele_data = db.cursor.fetchone()

        print("\n--- Report o uživatelích ---")
        print(f"Počet registrovaných uživatelů: {uzivatele_data['pocet_uzivatelu']}")

    except Exception as e:
        print(f"Chyba při generování reportu o uživatelích: {e}")

    finally:
        db.close()

def report_loans():
    db = Database()
    try:
        db.cursor.execute("""
            SELECT 
                COUNT(*) AS pocet_vypujcek, 
                AVG(DATEDIFF(IFNULL(datum_vraceni, CURDATE()), datum_vypujceni)) AS prumerna_doba_vypujcky
            FROM vypujcky
        """)
        vypujcky_data = db.cursor.fetchone()

        print("\n--- Report o výpůjčkách ---")
        print(f"Počet aktuálních výpůjček: {vypujcky_data['pocet_vypujcek']}")
        print(f"Průměrná doba výpůjčky: {vypujcky_data['prumerna_doba_vypujcky']:.2f} dní")

    except Exception as e:
        print(f"Chyba při generování reportu o výpůjčkách: {e}")

    finally:
        db.close()