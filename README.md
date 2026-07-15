# Network Health Checker

A Python CLI tool to check the health of multiple network hosts: ping +
common TCP port scanning, with a terminal report and CSV export.

## Features

- Reads hosts from a file (`hosts.txt`), supports comments (`#`).
- Cross-platform ping (Windows/Linux/Mac) via `subprocess`.
- TCP port scanning with `socket` (default: 22, 80, 443, 3389).
- Terminal report (rich table if `rich` is installed, plain text otherwise).
- CSV export with timestamp.

## Installation

```bash
git clone https://github.com/bryanvargasmadrigal/network-health-checker.git
cd network-health-checker
pip install -r requirements.txt   # optional, only for the rich table
```

## Usage

```bash
python3 checker.py
```

Options:

```bash
python3 checker.py -f hosts.txt -o report.csv -p 22,80,443,3389
```

| Flag | Description | Default |
|------|-------------|---------|
| `-f` | Hosts file | `hosts.txt` |
| `-o` | CSV output file | `report.csv` |
| `-p` | Ports to check (comma-separated) | `22,80,443,3389` |

## Example output

```
Host             Status    22   80   443
----------------------------------------
8.8.8.8          UP        X    X    OK
1.1.1.1          UP        X    X    OK
google.com       UP        X    OK   OK
192.168.1.1      DOWN
```

## "UP/DOWN" logic

A host is marked **UP** if it responds to ping **or** if at least one port
is open (useful when ICMP is blocked by a firewall but the service is
still running).

## Project structure

```
network-health-checker/
├── checker.py
├── hosts.txt
├── report.csv
├── requirements.txt
├── README.md
└── screenshots/
```

## Technologies

- Python 3.10+ (uses `list[str]`, generic `dict` types)
- `socket`, `subprocess`, `csv`, `argparse`
- `rich` (optional, improves terminal output)

## Possible future improvements

- Concurrent execution (`concurrent.futures`) to scan hosts in parallel.
- Explicit DNS resolution and resolved IP in the report.
- Email/webhook alerts when a host changes status.
- `--watch` mode for continuous monitoring with a configurable interval.
