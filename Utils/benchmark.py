import subprocess
import csv
import re
import sys

if len(sys.argv) < 3:
    print('Usage: python benchmark.py "C:\\path\\to\\ab.exe" <URL>')
    sys.exit(1)

AB_PATH = sys.argv[1]
URL = sys.argv[2]

REQUESTS = [100, 100, 100, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]

CONCURRENCY_LEVELS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]

CSV_FILE = "benchmark_results.csv"

results = []

for c in range(len(CONCURRENCY_LEVELS)):
    print(f"Running benchmark: concurrency={CONCURRENCY_LEVELS[c]}, requests={REQUESTS[c]}")

    command = [
        AB_PATH,
        "-n", str(REQUESTS[c]),
        "-c", str(CONCURRENCY_LEVELS[c]),
        URL
    ]

    process = subprocess.run(command, capture_output=True, text=True)
    output = process.stdout

    if process.returncode != 0:
        print(f"Benchmark failed for c={CONCURRENCY_LEVELS[c]}")
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
        CONCURRENCY_LEVELS[c],
        REQUESTS[c],
        tpr,
        rps,
        failed
    ])

with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Concurrency",
        "Requests",
        "Time per Request (ms)",
        "Requests per Second",
        "Failed Requests"
    ])
    writer.writerows(results)

print(f"Saved to {CSV_FILE}")