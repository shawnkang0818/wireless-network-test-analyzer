import subprocess
import json
import csv
from datetime import datetime
from pathlib import Path


DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "udp_tests.csv"

TEST_DURATION = 10
UDP_BANDWIDTH = "50M"


def run_udp_test(server_host: str):
    command = [
        "iperf3",
        "-c",
        server_host,
        "-u",
        "-b",
        UDP_BANDWIDTH,
        "-t",
        str(TEST_DURATION),
        "-J",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "iperf3 UDP test failed.\n"
            f"Return code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    return result.stdout


def parse_udp_output(output: str):
    data = json.loads(output)

    end_data = data["end"]

    udp_summary = end_data["sum"]

    throughput_mbps = (
        udp_summary["bits_per_second"] / 1_000_000
    )

    jitter_ms = udp_summary.get("jitter_ms", 0)

    lost_packets = udp_summary.get("lost_packets", 0)
    packets = udp_summary.get("packets", 0)
    lost_percent = udp_summary.get("lost_percent", 0)

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "throughput_mbps": round(throughput_mbps, 2),
        "jitter_ms": round(jitter_ms, 3),
        "lost_packets": lost_packets,
        "packets": packets,
        "packet_loss_percent": round(lost_percent, 3),
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
    print("Wireless Network UDP Test")
    print("-------------------------")

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
        f"\nRunning {TEST_DURATION} second UDP test "
        f"at {UDP_BANDWIDTH}..."
    )

    output = run_udp_test(server_host)

    metrics = parse_udp_output(output)

    metrics["server_host"] = server_host
    metrics["scenario"] = scenario
    metrics["distance_m"] = distance_m
    metrics["notes"] = notes

    print("\nUDP test results:")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    save_result_to_csv(metrics)

    print(f"\nResult saved to {CSV_FILE}")


if __name__ == "__main__":
    main()