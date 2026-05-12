import subprocess
import csv
import re
import sys

# użycie:
# python benchmark.py "C:\sciezka\do\ab.exe" http://127.0.0.1:8000/clinics/1

if len(sys.argv) < 3:
    print("Usage:")
    print(r'python benchmark.py "C:\path\to\ab.exe" <URL>')
    sys.exit(1)

AB_PATH = sys.argv[1]
URL = sys.argv[2]

REQUESTS = 5000

# CONCURRENCY_LEVELS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]

CSV_FILE = "benchmark_results.csv"

results = []

for concurrency in range(25,500,25):
    print(f"Running test for concurrency = {concurrency}")

    command = [
        AB_PATH,
        "-n", str(REQUESTS),
        "-c", str(concurrency),
        URL
    ]

    process = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    output = process.stdout

    # debug gdy benchmark padnie
    if process.returncode != 0:
        print(f"Benchmark failed for concurrency={concurrency}")
        print(process.stderr)

    time_match = re.search(
        r"Time per request:\s+([\d\.]+)\s+\[ms\]\s+\(mean\)",
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

    avg_time = float(time_match.group(1)) if time_match else None
    rps = float(rps_match.group(1)) if rps_match else None
    failed = int(failed_match.group(1)) if failed_match else None

    results.append([
        concurrency,
        REQUESTS,
        avg_time,
        rps,
        failed
    ])

with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Concurrency",
        "Requests",
        "Average Time per Request (ms)",
        "Requests per Second",
        "Failed Requests"
    ])

    writer.writerows(results)

print(f"Results saved to {CSV_FILE}")