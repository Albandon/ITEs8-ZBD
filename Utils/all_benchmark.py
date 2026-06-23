import subprocess
import csv
import re
import sys
import os
import db

# Użycie:
# python benchmark_all.py "C:\sciezka\do\ab.exe" <bazowy URL>

if len(sys.argv) < 2:
    print("Usage:")
    print(r'python benchmark_all.py "C:\path\to\ab.exe" <bazowy URL>')
    sys.exit(1)

AB_PATH = sys.argv[1]
BASE = sys.argv[2]

CONCURRENCY_LEVELS = [1, 100]
REQUESTS = [100, 1000]

CSV_FILE = "../benchmark_all_results.csv"
SLOW_QUERIES_FILE = "../benchmark_all_slow_queries.csv"

# Wszystkie endpointy
# method: GET / POST / PUT / PATCH / DELETE
# body_file: nazwa pliku .json (None jeśli brak)
ENDPOINTS = [
    # --- Appointments ---
    {"url": f"{BASE}/appointments/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/appointments/patient/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/appointments/", "method": "POST", "body_file": "jsons/appointment.json"},
    {"url": f"{BASE}/appointments/1/SCH", "method": "PATCH", "body_file": None},

    # --- Doctors ---
    {"url": f"{BASE}/doctors/search?query=Jan", "method": "GET", "body_file": None},
    {"url": f"{BASE}/doctors/speciality/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/doctors/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/doctors/1", "method": "PUT", "body_file": "jsons/doctor_update.json"},
    {"url": f"{BASE}/doctors/", "method": "POST", "body_file": "jsons/doctor_create.json"},
    {"url": f"{BASE}/doctors/1/password?password=Test123", "method": "PATCH", "body_file": None},
    {"url": f"{BASE}/doctors/1/login-info", "method": "GET", "body_file": None},

    # --- Specialities ---
    {"url": f"{BASE}/specialities/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/specialities/?name=Testowa", "method": "POST", "body_file": None},
    {"url": f"{BASE}/specialities/1/doctors/1", "method": "POST", "body_file": None},

    # --- Rooms ---
    {"url": f"{BASE}/rooms/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/rooms/speciality/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/rooms/clinic/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/rooms/clinic/1/speciality/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/rooms/", "method": "POST", "body_file": "jsons/room.json"},

    # --- Clinics ---
    {"url": f"{BASE}/clinics/1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/clinics/", "method": "GET", "body_file": None},
    {"url": f"{BASE}/clinics/", "method": "POST", "body_file": "jsons/clinic.json"},
    {"url": f"{BASE}/clinics/no_unique", "method": "POST", "body_file": "jsons/clinic.json"},

    # --- Treatments ---
    {"url": f"{BASE}/treatments/1?t_id=1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/treatments/1/time?t_id=1", "method": "GET", "body_file": None},
    {"url": f"{BASE}/treatments/", "method": "POST", "body_file": "jsons/treatment.json"},
    {"url": f"{BASE}/treatments/1/time/2", "method": "PATCH", "body_file": None},

    # --- Schedules ---
    {"url": f"{BASE}/schedules/regular", "method": "PUT", "body_file": "jsons/schedule_regular.json"},
    {"url": f"{BASE}/schedules/regular", "method": "POST", "body_file": "jsons/schedule_regular.json"},
    {"url": f"{BASE}/schedules/modify-day", "method": "PUT", "body_file": "jsons/schedule_modify.json"},
    {"url": f"{BASE}/schedules/available?doctor_id=1&treatment_id=1", "method": "GET", "body_file": None},
]

results = []
slow_queries = []


def run_ab(ab_path, n, c, method, url, body_file):
    command = [ab_path, "-n", str(n), "-c", str(c)]

    if method in ("POST", "PUT") and body_file:
        command += ["-p", body_file, "-T", "application/json"]
    elif method == "PATCH":
        command += ["-m", "PATCH"]
        if body_file:
            command += ["-p", body_file, "-T", "application/json"]
    elif method == "DELETE":
        command += ["-m", "DELETE"]

    command.append(url)
    return subprocess.run(command, capture_output=True, text=True)


def parse_ab(output):
    time_match = re.search(r"Time per request:\s+([\d\.]+)\s+\[ms\]\s+\(mean\)", output)
    rps_match = re.search(r"Requests per second:\s+([\d\.]+)", output)
    failed_match = re.search(r"Failed requests:\s+(\d+)", output)
    return (
        float(time_match.group(1)) if time_match else None,
        float(rps_match.group(1)) if rps_match else None,
        int(failed_match.group(1)) if failed_match else None,
    )


for endpoint in ENDPOINTS:
    url = endpoint["url"]
    method = endpoint["method"]
    body_file = endpoint["body_file"]

    print(f"\n{'=' * 55}")
    print(f"Testing: {method} {url}")

    for i, c in enumerate(CONCURRENCY_LEVELS):
        n = REQUESTS[i]
        print(f"  c={c}, n={n} ...", end=" ", flush=True)

        # Reset statystyk pg przed testem
        con = db.get_connection()
        cur = con.cursor()
        cur.execute("SELECT pg_stat_statements_reset();")
        con.commit()

        # Uruchom ab
        process = run_ab(AB_PATH, n, c, method, url, body_file)

        if process.returncode != 0:
            print(f"FAILED")
            print(f"  stderr: {process.stderr[:200]}")
            con.close()
            continue

        avg_time, rps, failed = parse_ab(process.stdout)
        print(f"avg={avg_time}ms, rps={rps}, failed={failed}")

        results.append([method, url, c, n, avg_time, rps, failed])

        # Pobierz top 3 najwolniejsze zapytania po teście
        cur.execute("""
            SELECT
                query,
                calls,
                round(mean_exec_time::numeric, 2) AS avg_ms,
                round(total_exec_time::numeric, 2) AS total_ms
            FROM pg_stat_statements
            WHERE query NOT LIKE '%pg_stat%'
            ORDER BY mean_exec_time DESC
            LIMIT 3;
        """)

        for row in cur.fetchall():
            slow_queries.append([method, url, c, row[0], row[1], row[2], row[3]])

        con.close()

# Zapis wyników ab
with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Method", "URL", "Concurrency", "Requests",
                     "Avg Time (ms)", "RPS", "Failed Requests"])
    writer.writerows(results)

# Zapis wolnych zapytań
with open(SLOW_QUERIES_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Method", "URL", "Concurrency", "Query",
                     "Calls", "Avg Time (ms)", "Total Time (ms)"])
    writer.writerows(slow_queries)

print(f"\nResults saved to {CSV_FILE}")
print(f"Slow queries saved to {SLOW_QUERIES_FILE}")