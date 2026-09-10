import subprocess
import re
import csv
from datetime import datetime
from pathlib import Path


TARGET = "8.8.8.8"
PING_COUNT = 10

DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "network_tests.csv"


def run_ping_test(target: str, count: int):
    command = ["ping", "-c", str(count), target]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout


def parse_ping_output(output: str):
    packet_pattern = (
        r"(\d+) packets transmitted, "
        r"(\d+) packets received, "
        r"([\d.]+)% packet loss"
    )

    latency_pattern = (
        r"round-trip min/avg/max/stddev = "
        r"([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms"
    )

    packet_match = re.search(packet_pattern, output)
    latency_match = re.search(latency_pattern, output)

    if not packet_match:
        raise ValueError("Could not parse packet statistics.")

    packets_sent = int(packet_match.group(1))
    packets_received = int(packet_match.group(2))
    packet_loss = float(packet_match.group(3))

    min_latency = None
    avg_latency = None
    max_latency = None
    stddev_latency = None

    if latency_match:
        min_latency = float(latency_match.group(1))
        avg_latency = float(latency_match.group(2))
        max_latency = float(latency_match.group(3))
        stddev_latency = float(latency_match.group(4))

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "target": TARGET,
        "packets_sent": packets_sent,
        "packets_received": packets_received,
        "packet_loss_percent": packet_loss,
        "min_latency_ms": min_latency,
        "avg_latency_ms": avg_latency,
        "max_latency_ms": max_latency,
        "stddev_latency_ms": stddev_latency,
    }


def save_result_to_csv(metrics):
    DATA_DIR.mkdir(exist_ok=True)

    file_exists = CSV_FILE.exists()

    with CSV_FILE.open("a", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=metrics.keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(metrics)


def main():
    print("Wireless Network Ping Test")
    print("--------------------------")

    scenario = input(
        "Scenario (baseline/distance/obstruction/network_load): "
    ).strip()

    distance_input = input(
        "Approximate distance from router in meters (optional): "
    ).strip()

    notes = input(
        "Notes (optional): "
    ).strip()

    distance_m = float(distance_input) if distance_input else None

    print(f"\nRunning ping test against {TARGET}...")

    output = run_ping_test(TARGET, PING_COUNT)

    metrics = parse_ping_output(output)

    metrics["scenario"] = scenario
    metrics["distance_m"] = distance_m
    metrics["notes"] = notes

    print("\nParsed results:")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    save_result_to_csv(metrics)

    print(f"\nResult saved to {CSV_FILE}")

if __name__ == "__main__":
    main()