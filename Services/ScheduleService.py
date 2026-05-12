from DTOs.ScheduleDTOs import CreateScheduleRegularDTO, CreateScheduleModificationDTO
from datetime import date, datetime, timedelta

def create_regular_schedule(conn, schedule_info: CreateScheduleRegularDTO):
    cur = conn.cursor()

    # only remove if day off - shouldn't happen here but just in case
    if schedule_info.time_from is None or schedule_info.time_to is None:
        cur.execute("""
            DELETE FROM "DoctorSchedules"
            WHERE doctor_id = %s
                AND date >= %s
                AND date <= %s
                AND EXTRACT(ISODOW FROM date) = %s
        """, (
            schedule_info.doctor_id,
            schedule_info.start_date,
            schedule_info.start_date + timedelta(days=300),
            schedule_info.weekday
        ))

        conn.commit()
        return

    cur.execute("""
        INSERT INTO "DoctorSchedules" (doctor_id, block_start, room_id, date)
        SELECT
            %s,
            t::time,
            %s,
            d::date
        FROM generate_series(%s::date, (%s::date + interval '300 days'), interval '1 day') AS d
        JOIN generate_series(timestamp '2000-01-01' + %s, (timestamp '2000-01-01' + %s) - interval '15 minutes', interval '15 minutes') AS t ON TRUE
        WHERE EXTRACT(ISODOW FROM d) = %s
    """, (
        schedule_info.doctor_id,
        schedule_info.room_id,
        schedule_info.start_date,
        schedule_info.start_date,
        schedule_info.time_from,
        schedule_info.time_to,
        schedule_info.weekday
    ))

    conn.commit()

def modify_schedule_single_day(conn, schedule_mod: CreateScheduleModificationDTO):
    cur = conn.cursor()

    # day validation
    if schedule_mod.date < date.today() + timedelta(days=7):
        raise ValueError("Modification must be at least 7 days in advance")

    # delete old blocks
    cur.execute("""
        DELETE FROM "DoctorSchedules"
        WHERE doctor_id = %s
            AND date = %s
    """, (
        schedule_mod.doctor_id,
        schedule_mod.date
    ))

    # end if day off
    if schedule_mod.time_from is None or schedule_mod.time_to is None:
        conn.commit()
        return

    # add new blocks
    cur.execute("""
            INSERT INTO "DoctorSchedules" (doctor_id, block_start, room_id, date, modified)
            SELECT
                %s,
                t::time,
                %s,
                %s::date,
                TRUE
            FROM generate_series(%s::timestamp, (%s::timestamp - interval '15 minutes'), interval '15 minutes') AS t
        """, (
        schedule_mod.doctor_id,
        schedule_mod.room_id,
        schedule_mod.date,
        schedule_mod.time_from,
        schedule_mod.time_to
    ))

    conn.commit()

def update_regular_schedule(conn, schedule_info: CreateScheduleRegularDTO):
    cur = conn.cursor()

    # day validation
    if schedule_info.start_date < date.today() + timedelta(days=30):
        raise ValueError("Schedule change must be at least 30 days in advance")

    end_date = schedule_info.start_date + timedelta(days=300)

    # delete old blocks
    cur.execute("""
        DELETE FROM "DoctorSchedules"
        WHERE doctor_id = %s
            AND date >= %s
            AND date <= %s
            AND EXTRACT(ISODOW FROM date) = %s
    """, (
        schedule_info.doctor_id,
        schedule_info.start_date,
        end_date,
        schedule_info.weekday
    ))

    # end if day off
    if schedule_info.time_from is None or schedule_info.time_to is None:
        conn.commit()
        return

    # add new blocks
    cur.execute("""
        INSERT INTO "DoctorSchedules" (doctor_id, block_start, room_id, date)
        SELECT
            %s,
            t::time,
            %s,
            d::date
        FROM generate_series(%s::date, %s::date, interval '1 day') AS d
        JOIN generate_series(%s::timestamp, (%s::timestamp - interval '15 minutes'), interval '15 minutes') AS t ON TRUE
        WHERE EXTRACT(ISODOW FROM d) = %s
    """, (
        schedule_info.doctor_id,
        schedule_info.room_id,
        schedule_info.start_date,
        end_date,
        schedule_info.time_from,
        schedule_info.time_to,
        schedule_info.weekday
    ))

    conn.commit()

def get_available_slots(conn, doctor_id: int, treatment_id: int, date_from: date = date.today(), date_to: date = date.today() + timedelta(days=300)):
    cur = conn.cursor()

    # extract estimated blocks number for the treatment
    cur.execute("""
        SELECT estimated_blocks
        FROM "Treatments"
        WHERE id = %s
    """, (treatment_id,))

    row = cur.fetchone()
    if not row:
        return None

    estimated_blocks = row[0]

    # find starting blocks for which the next (estimated_blocks - 1) blocks exist and are also free
    cur.execute("""
        SELECT ds.id, ds.date, ds.block_start, ds.room_id
        FROM "DoctorSchedules" ds
        JOIN "Rooms" r ON r.id = ds.room_id
        JOIN "Treatments" t on t.id = %s AND t.speciality_id = r.speciality_id
        WHERE ds.doctor_id = %s
            AND ds.date BETWEEN %s AND %s
            AND ds.booked = FALSE
            -- all required blocks must exist and be available
            AND (
                SELECT COUNT(*)
                FROM "DoctorSchedules" ds2
                WHERE ds2.doctor_id = ds.doctor_id
                    AND ds2.date = ds.date
                    AND ds2.room_id = ds.room_id
                    AND ds2.block_start >= ds.block_start
                    AND ds2.block_start < ds.block_start + (%s * interval '15 minutes')
                    AND ds2.booked = FALSE
            ) = %s
        ORDER BY ds.date, ds.block_start
    """, (treatment_id, doctor_id, date_from, date_to, estimated_blocks, estimated_blocks))

    data = cur.fetchall()

    return [{
        "id": row[0],
        "date": row[1],
        "block_start": row[2],
        "room_id": row[3]
    } for row in data]