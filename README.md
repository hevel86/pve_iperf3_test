# Python Iperf3 Test Script

This script is designed to perform Iperf3 tests between multiple Proxmox Virtual Environment (PVE) servers. It uses SSH to connect to each PVE server and run Iperf3 tests from one server to another. The results are then displayed in a tabular format.

## Prerequisites

Before using this script, make sure you have the following:

- Python 3.x installed on your local machine.
- Paramiko library installed (can be installed using `pip install paramiko`).
- SSH access to the PVE servers with SSH key authentication.
- PVE servers running Iperf3 in server mode (`iperf3 -s`).

## Configuration

1. Update the `hosts_full` list with the full DNS names of your PVE servers.
2. Modify the `ssh_username` variable with your SSH username.
3. Update the `ssh_key_filepath` variable with the path to your private SSH key.

## Usage

1. Run the script using Python: `python main.py`
2. The script will connect to each PVE server and perform Iperf3 tests between them.
3. Results are displayed in a tabular format, showing Gbps speed and retries for each test.

## Sample Output

```plaintext
      pve2_retries  pve3_retries pve1_retries
pve1  (5.07, 4758)  (6.22, 1199)          N/A
pve2           N/A   (9.32, 122)   (9.40, 54)
pve3  (4.70, 3494)           N/A   (9.38, 68)
