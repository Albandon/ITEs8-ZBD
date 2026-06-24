from DTOs.RoomDTOs import CreateRoomDTO

def get_room_by_id(conn, room_id: int):
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM "Rooms"
        WHERE id = %s  
    """, (room_id,))

    data = cur.fetchone()

    if not data:
        return None

    return {
        'id': data[0],
        'speciality_id': data[1],
        'clinic_id': data[2],
        'room_name': data[3]
    }

def get_rooms_by_speciality_id(conn, speciality_id: int):
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM "Rooms"
        WHERE speciality_id = %s
    """, (speciality_id,))

    data = cur.fetchall()

    if not data:
        return []

    return [{
        'id': row[0],
        'speciality_id': row[1],
        'clinic_id': row[2],
        'room_name': row[3]
    } for row in data]

def get_rooms_by_clinic_id(conn, clinic_id: int):
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM "Rooms"
        WHERE clinic_id = %s
    """, (clinic_id,))

    data = cur.fetchall()

    if not data:
        return []

    return [{
        'id': row[0],
        'speciality_id': row[1],
        'clinic_id': row[2],
        'room_name': row[3]
    } for row in data]


def get_rooms_by_clinic_and_speciality_id(conn, clinic_id: int, speciality_id: int):
    cur = conn.cursor()

    cur.execute("""
        SELECT r.id, r.room_name, c.address || ', ' || c.city, s.name FROM "Rooms" r
        LEFT JOIN "Clinics" c ON r.clinic_id = c.id
        LEFT JOIN "Specialities" s ON r.speciality_id = s.id
        WHERE r.clinic_id = %s
            AND r.speciality_id = %s
    """, (clinic_id, speciality_id))

    data = cur.fetchall()

    if not data:
        return []

    return [{
        'id': row[0],
        'room_name': row[1],
        'clinic_address': row[2],
        'speciality_name': row[3]
    } for row in data]

def create_room(conn, room_info: CreateRoomDTO):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO "Rooms" (speciality_id, clinic_id, room_name)
        VALUES (%s, %s, %s)
        RETURNING id
    """, room_info.map())

    room_id = cur.fetchone()[0]
    conn.commit()

    return room_id