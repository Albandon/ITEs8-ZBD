from DTOs.DoctorDTOs import CreateDoctorDTO, CreateDoctorLoginInfoDTO, CreateDoctorWithLoginDTO
from Utils import PasswordEncrypter as pe

def search_doctors_by_name(conn, query: str):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, first_name || ' ' || last_name AS name
        FROM "Doctors"
        WHERE (first_name || ' ' || last_name) ILIKE %s
    """, (f'%{query}%',))

    data = cur.fetchall()

    if not data:
        return []

    return [{
        "id": row[0],
        "name": row[1]
    } for row in data]

def search_doctors_by_speciality_id(conn, speciality_id: int):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, first_name || ' ' || last_name AS name
        FROM "Doctors" d
        JOIN "DoctorsSpecialities" ds ON ds.doctor_id = d.id
        WHERE ds.speciality_id = %s
    """, (speciality_id,))

    data = cur.fetchall()

    if not data:
        return []

    return [{
        "id": row[0],
        "name": row[1]
    } for row in data]

def get_doctor_by_id(conn, doctor_id: int):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, first_name, last_name, sex
        FROM "Doctors"
        WHERE id = %s
    """, (doctor_id,))

    data = cur.fetchone()

    if not data:
        return None

    return {
        "id": data[0],
        "first_name": data[1],
        "last_name": data[2],
        "sex": data[3]
    }

def create_doctor(conn, doctor_info: CreateDoctorDTO):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO "Doctors" (first_name, last_name, sex)
        VALUES (%s, %s, %s)
        RETURNING id
    """, doctor_info.map())

    doctor_id = cur.fetchone()[0]
    conn.commit()

    return doctor_id

def create_doctor_login_info(conn, doctor_info: CreateDoctorLoginInfoDTO):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO "DoctorLoginInfo" (doctor_id, email, phone, hash_password, created_at)
        VALUES (%s, %s, %s, %s, current_timestamp)
    """, doctor_info.map(pe.hash_password(doctor_info.password)))

    conn.commit()

def update_doctor(conn, doctor_info: CreateDoctorDTO):
    cur = conn.cursor()

    cur.execute("""
        UPDATE "Doctors"
        SET first_name = %s, last_name = %s, sex = %s
        WHERE id = %s
    """, (doctor_info.map(),))

    conn.commit()

def update_doctor_password(conn, password: str, doctor_id: int) -> bool:
    cur = conn.cursor()

    cur.execute("""
        SELECT hash_password
        FROM "DoctorLoginInfo"
        WHERE doctor_id = %s
    """, (doctor_id,))

    old_hash_password = cur.fetchone()[0]

    if pe.verify_password(password, old_hash_password):
        return False  # return false when new password is the same as old one

    cur.execute("""
        UPDATE "DoctorLoginInfo"
        SET hash_password = %s
        WHERE doctor_id = %s
    """, (pe.hash_password(password), doctor_id))

    conn.commit()

    return True

def get_doctor_login_info_by_doctor_id(conn, doctor_id: int):
    cur = conn.cursor()

    cur.execute("""
        SELECT doctor_id, email, phone, hash_password, created_at
        FROM "DoctorLoginInfo"
        WHERE doctor_id = %s
    """, (doctor_id,))

    data = cur.fetchone()

    if not data:
        return None

    return {
        "doctor_id": data[0],
        "email": data[1],
        "phone": data[2],
        "hash_password": data[3],
        "created_at": data[4]
    }

def create_doctor_with_login(conn, dto: CreateDoctorWithLoginDTO):
    doctor_id = create_doctor(conn, CreateDoctorDTO(
        first_name=dto.first_name,
        last_name=dto.last_name,
        sex=dto.sex
    ))

    create_doctor_login_info(conn, CreateDoctorLoginInfoDTO(
        doctor_id=doctor_id,
        email=dto.email,
        phone=dto.phone,
        password=dto.password
    ))
    return doctor_id