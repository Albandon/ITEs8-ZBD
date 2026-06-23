import subprocess
import csv
import re
import sys

import db
from db import get_write_conn

# python write_benchmark.py "C:\sciezka\do\ab.exe" http://127.0.0.1:8000/clinics/no_unique

if len(sys.argv) < 3:
    print("Usage:")
    print(r'python write_benchmark.py "C:\path\to\ab.exe" <URL>')
    sys.exit(1)

AB_PATH = sys.argv[1]
URL = sys.argv[2]

REQUESTS = [100, 100, 100, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
CONCURRENCY_LEVELS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]

CSV_FILE = "../write_benchmark_results.csv"

results = []

for i in range(0, len(CONCURRENCY_LEVELS)):
    print(f"running test for concurrency = {CONCURRENCY_LEVELS[i]}, requests = {REQUESTS[i]}")

    command = [
        AB_PATH,
        "-n", str(REQUESTS[i]),
        "-c", str(CONCURRENCY_LEVELS[i]),
        "-p", "jsons/clinic.json",
        "-T", "application/json",
        URL
    ]

    process = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    output = process.stdout

    # debug
    if process.returncode != 0:
        print(f"Benchmark failed for concurrency={CONCURRENCY_LEVELS[i]}")
        print(process.stderr)

    tpr_match = re.search(
        r"Time per request:\s*([\d.]+)\s*\[ms\]",
        output
    )

    rps_match = re.search(
        r"Requests per second:\s+([\d\.]+)",
        output
    )

    failed_match = re.search(
        r"Failed requests:\s+(\d+)",
        output
    )

    tpr = float(tpr_match.group(1)) if tpr_match else None
    rps = float(rps_match.group(1)) if rps_match else None
    failed = int(failed_match.group(1)) if failed_match else None

    results.append([
        CONCURRENCY_LEVELS[i],
        REQUESTS[i],
        tpr,
        rps,
        failed
    ])

    # remove added records
    con, pool = get_write_conn()
    cur = con.cursor()

    cur.execute("""
            DELETE FROM "Clinics"
            WHERE city = 'Testowo'
        """)

    con.commit()
    pool.putconn(con)

with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Concurrency",
        "Requests",
        "Time per Request (ms)",
        "Requests per Second",
        "Failed Requests"
    ])

    writer.writerows(results)

print(f"Results saved to {CSV_FILE}")