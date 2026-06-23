from DTOs.ClinicDTOs import Clinic as ClinicDTO

def get_all_clinics(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, address, city 
        FROM "Clinics"
        ORDER BY city ASC
    """)

    clinics = cur.fetchall()

    return [
        {
        "id": clinic[0],
        "address": clinic[1],
        "city": clinic[2],
        }
        for clinic in clinics
    ]
def get_clinic_by_id(conn, clinic_id: int):
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, address, city
            FROM "Clinics"
            WHERE id = %s
        """, (clinic_id,))

        data = cur.fetchone()
        if not data:
            return None

        return {
            "id": data[0],
            "address": data[1],
            "city": data[2],
        }
    except:
        conn.rollback()
        raise

def create_clinic(conn, clinic: ClinicDTO, unique=True):
    cur = conn.cursor()

    if unique:
        cur.execute("""
            SELECT 1 
            FROM "Clinics"
            WHERE city = %s AND address = %s
        """, (clinic.city, clinic.address))

        if cur.fetchone():
            return False

    cur.execute("""
        INSERT INTO "Clinics"
        (address, city)
        VALUES (%s, %s)
        RETURNING id
    """, clinic.map())

    clinic_id = cur.fetchone()[0]
    conn.commit()

    return {"id": clinic_id}

