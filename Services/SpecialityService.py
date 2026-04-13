def create_speciality(conn, speciality_name: str) -> int:
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO "Specialities" (name)
        VALUES (%s)
        ON CONFLICT DO NOTHING
        RETURNING id
    """, (speciality_name,))

    row = cur.fetchone()
    conn.commit()

    if not row:
        return -1

    return row[0]

def get_speciality_by_id(conn, speciality_id: int):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name
        FROM "Specialities"
        WHERE id = %s
    """, (speciality_id,))

    data = cur.fetchone()

    if not data:
        return None

    return {
        'id': data[0],
        'name': data[1]
    }

def assign_speciality_to_doctor(conn, speciality_id, doctor_id):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO "DoctorsSpecialities" (speciality_id, doctor_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (speciality_id, doctor_id))

    conn.commit()
    return cur.rowcount > 0