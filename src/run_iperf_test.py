import subprocess
import json
import csv
from datetime import datetime
from pathlib import Path


DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "throughput_tests.csv"
INTERVAL_CSV_FILE = DATA_DIR / "throughput_intervals.csv"

TEST_DURATION = 10


def run_iperf_test(server_host: str):
    command = [
        "iperf3",
        "-c",
        server_host,
        "-t",
        str(TEST_DURATION),
        "-J"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"iperf3 test failed:\n{result.stderr}"
        )

    return result.stdout


def parse_iperf_output(output: str):
    data = json.loads(output)

    end_data = data["end"]

    sent = end_data["sum_sent"]
    received = end_data["sum_received"]

    sent_mbps = sent["bits_per_second"] / 1_000_000
    received_mbps = received["bits_per_second"] / 1_000_000

    retransmits = sent.get("retransmits", 0)

    summary_metrics = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "sent_mbps": round(sent_mbps, 2),
        "received_mbps": round(received_mbps, 2),
        "retransmits": retransmits,
    }

    interval_metrics = []

    for index, interval in enumerate(data["intervals"], start=1):
        interval_sum = interval["sum"]

        throughput_mbps = (
            interval_sum["bits_per_second"] / 1_000_000
        )

        interval_metrics.append({
            "second": index,
            "throughput_mbps": round(throughput_mbps, 2),
            "retransmits": interval_sum.get("retransmits", 0),
        })

    return summary_metrics, interval_metrics

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

def save_intervals_to_csv(
    intervals,
    timestamp,
    server_host,
    scenario,
    distance_m,
):
    DATA_DIR.mkdir(exist_ok=True)

    file_exists = INTERVAL_CSV_FILE.exists()

    fieldnames = [
        "timestamp",
        "server_host",
        "scenario",
        "distance_m",
        "second",
        "throughput_mbps",
        "retransmits",
    ]

    with INTERVAL_CSV_FILE.open("a", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        for interval in intervals:
            writer.writerow({
                "timestamp": timestamp,
                "server_host": server_host,
                "scenario": scenario,
                "distance_m": distance_m,
                "second": interval["second"],
                "throughput_mbps": interval["throughput_mbps"],
                "retransmits": interval["retransmits"],
            })

def select_scenario():
    scenarios = {
        "1": "baseline",
        "2": "distance",
        "3": "obstruction",
        "4": "network_load",
    }

    print("\nSelect test scenario:")
    print("1. baseline")
    print("2. distance")
    print("3. obstruction")
    print("4. network_load")

    choice = input("Enter choice (1-4): ").strip()

    if choice not in scenarios:
        raise ValueError("Invalid scenario selection.")

    return scenarios[choice]

def main():
    print("Wireless Network Throughput Test")
    print("--------------------------------")

    server_host = input(
        "iperf3 server IP address: "
    ).strip()

    scenario = select_scenario()

    distance_input = input(
        "Approximate distance from router in meters (optional): "
    ).strip()

    notes = input(
        "Notes (optional): "
    ).strip()

    distance_m = (
        float(distance_input)
        if distance_input
        else None
    )

    print(
        f"\nRunning {TEST_DURATION} second TCP throughput test..."
    )

    output = run_iperf_test(server_host)

    metrics, intervals = parse_iperf_output(output)

    metrics["server_host"] = server_host
    metrics["scenario"] = scenario
    metrics["distance_m"] = distance_m
    metrics["notes"] = notes

    print("\nTest results:")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    save_result_to_csv(metrics)

    save_intervals_to_csv(
    intervals,
    metrics["timestamp"],
    server_host,
    scenario,
    distance_m,
)
    print(f"\nSummary saved to {CSV_FILE}")
    print(f"Interval data saved to {INTERVAL_CSV_FILE}")


if __name__ == "__main__":
    main()
