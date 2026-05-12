from DTOs.TreatmentDTOs import Treatment as TDto

def get_treatment_by_id (con, t_id: int):
    cur = con.cursor()
    cur.execute("""
        SELECT id, name, speciality_id, estimated_blocks
        FROM "Treatments"
        WHERE id = %s
    """, (t_id,))
    
    data = cur.fetchone()
    
    if not data:
        return None
    
    return {
        "id": data[0],
        "name": data[1],
        "speciality_id": data[2],
        "time_blocks": data[3]
    }

# TODO: ocenić czy potrzebny
def get_treatments_by_doctor_id (con, d_id : int):
    pass

def get_treatment_time_by_id (con, t_id: int):
    cur = con.cursor()
    cur.execute("""
        SELECT estimated_blocks
        FROM "Treatments"
        WHERE id = %s
    """, (t_id,))
    
    data = cur.fetchone()
    
    if not data:
        return None
    
    return {
        "time_blocks": data[0]
    }

def create_treatment (con, data: TDto):
    cur = con.cursor()

    cur.execute("""
        INSERT INTO "Treatments" (name, speciality_id, estimated_blocks)
        VALUES (%s, %s, %s)
        RETURNING id
    """, data.map())

    t_id = cur.fetchone()[0]
    con.commit()

    return t_id

def update_treatment_time (con, t_id: int, time_blocks: int):
    cur = con.cursor()
    cur.execute("""
        UPDATE "Treatments"
        SET estimated_blocks = %s
        WHERE id = %s
    """, (time_blocks, t_id))
    
    if cur.rowcount == 0:
        return False

    con.commit()

    return True