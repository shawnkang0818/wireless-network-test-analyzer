import subprocess
import re
from datetime import datetime


TARGET = "8.8.8.8"
PING_COUNT = 10


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


def main():
    print(f"Running ping test against {TARGET}...")

    output = run_ping_test(TARGET, PING_COUNT)

    print("\nRaw output:")
    print(output)

    metrics = parse_ping_output(output)

    print("\nParsed results:")

    for key, value in metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()