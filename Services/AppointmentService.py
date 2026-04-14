from DTOs.AppointmentDTOs import AppointmentDTO

def get_appointment_by_id(conn, app_id: int):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, doctor_id, patient_id, treatment_id, "time", status, room_id
        FROM "Appointments"
        WHERE id = %s
    """, (app_id,))

    data = cur.fetchone()

    if not data:
        return None

    return {
        "id": data[0],
        "doctor_id": data[1],
        "patient_id": data[2],
        "treatment_id": data[3],
        "time": data[4],
        "status": data[5],
        "room_id": data[6],
    }

def get_appointments_by_patient_id(conn, patient_id: int):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, doctor_id, patient_id, treatment_id, "time", status, room_id
        FROM "Appointments"
        WHERE patient_id = %s
    """, (patient_id,))

    data = cur.fetchall()

    if not data:
        return None

    return [
        {
            "id": row[0],
            "doctor_id": row[1],
            "patient_id": row[2],
            "treatment_id": row[3],
            "time": row[4],
            "status": row[5],
            "room_id": row[6],
        }
        for row in data
    ]


def create_appointment(conn, app_data: AppointmentDTO):
    cur = conn.cursor()

    cur.execute("""
        SELECT 1 FROM "Appointments"
        WHERE doctor_id = %s AND "time" = %s
    """, (app_data.doctor_id, app_data.time))

    if cur.fetchone():
        return False

    cur.execute("""
        INSERT INTO "Appointments"
        (doctor_id, patient_id, treatment_id, "time", status, room_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, app_data.map())

    appointment_id = cur.fetchone()[0]
    conn.commit()

    return {"id": appointment_id}


def update_appointment_status(conn, app_id: int, status: str):
    cur = conn.cursor()

    cur.execute("""
        UPDATE "Appointments"
        SET status = %s 
        WHERE id = %s
    """, (status, app_id))

    if cur.rowcount == 0:
        return False

    conn.commit()

    return True