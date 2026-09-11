# Wireless Network Test Analyzer

A Python based network testing project for collecting, logging, and analyzing wireless performance metrics across repeatable test scenarios.

The project is designed to practice test engineering workflows including controlled test execution, structured data collection, performance analysis, and anomaly investigation.

## Current Features

### Stage 1: Ping Testing
- Automated ping execution
- Latency measurement
- Packet loss measurement
- Scenario and distance metadata
- CSV result logging

### Stage 2: TCP Throughput Testing
- iperf3 client automation
- JSON result parsing
- TCP throughput measurement
- Retransmission tracking
- Summary CSV logging
- Per second throughput interval logging

### Stage 3: UDP Testing
- UDP throughput measurement
- Jitter measurement
- UDP packet loss measurement
- Datagram loss tracking
- Structured CSV logging

### Stage 4: Test Scenario Analysis
- Controlled baseline testing
- Controlled distance testing
- Controlled obstruction testing
- Three repeated runs per test type and scenario

Planned:
- Network load testing
- Automated repeated-run comparison

### Stage 5: Analysis and Visualization
Planned:
- Automated performance comparison
- Anomaly detection
- Charts and trend visualization
- Streamlit dashboard

## Test Setup

Current local throughput testing uses:

- MacBook as the iperf3 client
- iPhone 14 Pro as the iperf3 server
- Both devices connected to the same WiFi network

The iPhone server application is kept awake and in the foreground during testing to prevent the iperf3 server from stopping.

## Controlled Test Methodology

The controlled dataset collected on September 10, 2026 uses the following rules:

- The iPhone iperf3 server remains fixed near the router on the second floor.
- `distance_m` means the approximate distance from the Mac client to the router, not the distance between the Mac and iPhone.
- Each scenario contains three ping runs, three 10-second TCP runs, and three 10-second UDP runs at a target rate of 50 Mbps.
- Ping uses `8.8.8.8`, so its latency includes WiFi, router, ISP, WAN, and remote-host effects. It is an end-to-end observation, not an isolated WiFi latency measurement.
- TCP and UDP use the iPhone server at `192.168.1.133` on the same WiFi network.

Controlled scenarios:

| Scenario | Mac position | Obstructions |
|---|---|---|
| Baseline | About 2 m from router, same room | None noted |
| Distance | About 8 m from router | Two interior walls |
| Obstruction | About 10 m from router, one floor below | One floor between Mac and router |

The distance scenario is not a pure distance-only test because two interior walls were present. Results from that scenario reflect both increased distance and wall attenuation. Rows whose notes begin with `Controlled` make up the controlled dataset; earlier rows are retained as development data.

## Data Output

### Ping Results

`data/network_tests.csv`

Stores:
- timestamp
- target
- packets sent and received
- packet loss
- minimum, average, and maximum latency
- latency standard deviation
- scenario
- distance
- notes

### TCP Throughput Summary

`data/throughput_tests.csv`

Stores:
- timestamp
- sent throughput
- received throughput
- retransmissions
- server address
- scenario
- distance
- notes

### TCP Interval Results

`data/throughput_intervals.csv`

Stores per second:
- timestamp
- scenario
- distance
- throughput
- retransmissions

### UDP Results

`data/udp_tests.csv`

Stores:
- timestamp
- throughput
- jitter
- lost and total datagrams
- packet loss percentage
- server address
- scenario
- distance
- notes

## Project Structure

```text
wireless-network-test-analyzer/
├── data/
│   ├── network_tests.csv
│   ├── throughput_tests.csv
│   ├── throughput_intervals.csv
│   └── udp_tests.csv
├── src/
│   ├── run_ping_test.py
│   ├── run_iperf_test.py
│   └── run_udp_test.py
├── README.md
├── requirements.txt
└── .gitignore
