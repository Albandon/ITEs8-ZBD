import db

# --- HELPERS ---
def confirm(prompt="Czy na pewno? (t/n): "):
    return input(prompt).lower() == 't'

# --- PATIENTS ---
def show_patients():
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM "Patients";')
    for row in cur.fetchall():
        print(row)

    conn.close()


def add_patient():
    conn = db.get_connection()
    cur = conn.cursor()

    print("\n--- Dodawanie pacjenta ---")

    new_id = input("ID (tymczasowo)")
    first = input("Imię: ")
    last = input("Nazwisko: ")
    sex = input("Płeć (M/F): ")
    birthdate = input("Data urodzenia (YYYY-MM-DD): ")
    pesel = input("PESEL: ")
    address = input("Adres: ")
    city = input("Miasto: ")
    postal = input("Kod pocztowy: ")
    country = input("Kod kraju: ")

    print("\n--- PODSUMOWANIE ---")
    print(first, last, sex, birthdate, pesel, address, city, postal, country)

    if not confirm():
        print("Anulowano.")
        return


    cur.execute("""
            INSERT INTO "Patients"
            ("id","first_name","last_name","sex","birthdate","pesel","address","city","postal_code","country_code")
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (new_id, first, last, sex, birthdate, pesel, address, city, postal, country))


    conn.commit()
    conn.close()

    print(f"Dodano! ID: {new_id}")


# --- APPOINTMENTS ---
def show_appointments():
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT a."id", a."time", a."status",
               d."first_name", d."last_name"
        FROM "Appointments" a
        JOIN "Doctors" d ON d."id" = a."doctor_id";
    """)

    for row in cur.fetchall():
        print(row)

    conn.close()


def cancel_appointment():
    conn = db.get_connection()
    cur = conn.cursor()

    id = input("ID wizyty do anulowania: ")

    print(f"Anulujesz wizytę ID={id}")
    if not confirm():
        print("Anulowano operację.")
        return

    cur.execute("""
        UPDATE "Appointments"
        SET "status" = 'CAN'
        WHERE "id" = %s
    """, (id,))

    conn.commit()
    conn.close()
    print("Anulowano!")


# --- MAIN ---
def main():
    while True:
        print("\n--- MENU ---")
        print("1. Pokaż pacjentów")
        print("2. Dodaj pacjenta")
        print("3. Pokaż wizyty")
        print("4. Anuluj wizytę")
        print("0. Wyjście")

        choice = input("Wybór: ")

        if choice == "1":
            show_patients()
        elif choice == "2":
            add_patient()
        elif choice == "3":
            show_appointments()
        elif choice == "4":
            cancel_appointment()
        elif choice == "0":
            break
        else:
            print("Zły wybór")


if __name__ == "__main__":
    main()
