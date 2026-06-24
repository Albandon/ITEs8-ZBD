from psycopg2.extras import execute_values
from db import get_write_conn
from datetime import date, time

from DTOs.ScheduleDTOs import CreateScheduleRegularDTO
from Services.ScheduleService import create_regular_schedule
from DTOs.TreatmentDTOs import Treatment
from Services.TreatmentService import create_treatment
from Services.SpecialityService import create_speciality

def generate_mock_data():
    conn, pool = get_write_conn()
    conn.rollback()

    try:
        print("initializing")
        init(conn)
        print("generating doctors")
        generate_doctors(conn)

        # check right before commit
        cur = conn.cursor()
        cur.execute("SELECT inet_server_addr(), inet_server_port();")
        print(f"Connected to: {cur.fetchone()}")

        cur.execute('SELECT COUNT(*) FROM "Doctors"')
        print(f"Doctors in transaction: {cur.fetchone()[0]}")
        cur.execute('SELECT COUNT(*) FROM "Clinics"')
        print(f"Clinics in transaction: {cur.fetchone()[0]}")

        print("generating clinics")
        generate_clinics(conn)
        print("generating rooms")
        generate_rooms(conn)
        print("generating schedules")
        generate_schedules(conn)

        conn.commit()
        print("committed!")

        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM "Doctors";')
        print(f"Doctors after commit: {cur.fetchone()[0]}")
        cur.execute("SELECT inet_server_addr(), inet_server_port();")
        print(f"Connected to: {cur.fetchone()}")

    except Exception as e:
        print(f"Exception: {e}")
        conn.rollback()
        raise e

    finally:
        pool.putconn(conn)
        print("Data generated!")

def init(conn):
    treatment = Treatment (
        name="test",
        spec_id="1",
        time_blocks="3"
    )
    create_speciality(conn, "test")
    create_treatment(conn, treatment)

def generate_doctors(conn):
    fname = ["Krzysztof", "Eryk", "Mariusz", "Marek", "Ireneusz", "Piotr", "Arek", "Aleksander", "Karol", "Kacper"]
    lname_p = ["Kowal", "Szew", "Zimor", "Berdziń", "Bednar", "Mikoł", "Sokoł", "Dobrzań", "Mazur", "Jank", "Szymań", "Pior",
               "Paw", "Jakub", "Swat", "Brzydal", "Kule", "Kra", "Paster", "Wyj"]
    lname_s = ["ski", "czyk", "ak", "owski", "ewicz"]

    for first_name in fname:
        values = []

        for last_name_prefix in lname_p:
            for last_name_suffix in lname_s:
                values.append((first_name, last_name_prefix + last_name_suffix, "M"))
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO "Doctors" (first_name, last_name, sex)
        VALUES %s
        ON CONFLICT DO NOTHING
    """, values)

    cur.execute('SELECT id FROM "Doctors"')
    doctor_ids = [row[0] for row in cur.fetchall()]
    values = []

    for d_id in doctor_ids:
        values.append((d_id, 1))

    execute_values(cur, """
        INSERT INTO "DoctorsSpecialities" (doctor_id, speciality_id)
        VALUES %s
        ON CONFLICT DO NOTHING
    """, values)

def generate_clinics(conn):
    adress = ["Strzegomska", "Świdnicka", "Świebodzka", "Wrocławska", "Wałbrzyska",
             "Senatorska", "Armi Krajowej", "Kupiecka", "Polna", "Leśna"]

    city = ["Wałbrzych", "Wrocław", "Kąty Wrocławskie", "Świdnica",
            "Jaworzyna Śląska", "Żarów", "Świebodzice",
            "Długołęka", "Żary", "Poznań"]

    values = []

    for i in range(10):
        for j in range(10):
            values.append((adress[i] + f" {i+1}/{j+1}", city[j]))

    cur = conn.cursor()

    execute_values(cur, """
        INSERT INTO "Clinics" (address, city)
        VALUES %s
        ON CONFLICT DO NOTHING
    """, values)

def generate_rooms(conn):
    cur = conn.cursor()
    cur.execute('SELECT id FROM "Clinics"')
    clinics = [row[0] for row in cur.fetchall()]

    values = []

    for r_no in range(1, 5):
        for c_id in clinics:
            values.append((1, c_id, f"Gabinet {c_id}-{r_no}"))

        execute_values(cur, """
            INSERT INTO "Rooms" (speciality_id, clinic_id, room_name)
            VALUES %s
            ON CONFLICT DO NOTHING
        """, values)

def generate_schedules(conn):
    cur = conn.cursor()

    cur.execute('SELECT id FROM "Doctors"')
    doctors = [row[0] for row in cur.fetchall()]

    start_date = date.today()

    cur.execute('SELECT id FROM "Rooms"')
    rooms = [row[0] for row in cur.fetchall()]

    if not rooms:
        raise Exception("No rooms found!")

    room_count = len(rooms)

    for idx, doctor_id in enumerate(doctors):
        for weekday in range(1, 6):

            dto = CreateScheduleRegularDTO(
                doctor_id=doctor_id,
                weekday=weekday,
                start_date=start_date,
                time_from=time(8, 0),
                time_to=time(16, 0),
                room_id=rooms[idx % room_count]
            )

            create_regular_schedule(conn, dto)


generate_mock_data()