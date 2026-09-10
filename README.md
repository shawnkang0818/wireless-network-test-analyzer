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
Planned:
- UDP throughput
- Jitter
- UDP packet loss

### Stage 4: Test Scenario Analysis
Planned:
- Baseline testing
- Distance testing
- Obstruction testing
- Network load testing
- Repeated run comparison

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

## Project Structure

```text
wireless-network-test-analyzer/
├── data/
│   ├── network_tests.csv
│   ├── throughput_tests.csv
│   └── throughput_intervals.csv
├── src/
│   ├── run_ping_test.py
│   └── run_iperf_test.py
├── README.md
├── requirements.txt
└── .gitignore