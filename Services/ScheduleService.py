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
            t,
            %s,
            d
        FROM generate_series(%s, %s, interval '1 day') AS d
        JOIN generate_series(%s, %s - interval '15 minutes', interval '15 minutes') AS t ON TRUE
        WHERE EXTRACT(ISODOW FROM d) = %s
    """, (
        schedule_info.doctor_id,
        schedule_info.room_id,
        schedule_info.start_date,
        schedule_info.start_date + timedelta(days=300),
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
            INSERT INTO "DoctorSchedules" (doctor_id, block_start, room_id, date)
            SELECT
                %s,
                t,
                %s,
                %s
            FROM generate_series(%s, %s - interval '15 minutes', interval '15 minutes') AS t
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
            t,
            %s,
            d
        FROM generate_series(%s, %s, interval '1 day') AS d
        JOIN generate_series(%s, %s - interval '15 minutes', interval '15 minutes') AS t ON TRUE
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