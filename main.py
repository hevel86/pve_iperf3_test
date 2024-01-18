import paramiko
import pandas as pd
import re
import os

# Define the hosts with full DNS names
hosts_full = ['pve1.machinebuilders.local', 'pve2.machinebuilders.local', 'pve3.machinebuilders.local']
ssh_username = 'root'
ssh_key_filepath = os.path.expanduser('~/.ssh/id_rsa')  # Update with the path to your private key

# Create a dictionary with the short names as keys for storing results
hosts_short = [host.split('.')[0] for host in hosts_full]
results = {host: {} for host in hosts_short}


# Function to run iperf3 test and parse the output for Gbps and retries
def run_iperf3_test(ssh_client, server):
    command = f'iperf3 -c {server} -t 10'
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    errors = stderr.read().decode('utf-8')

    # Parse the output to extract Gbps and retries from the summary line
    speed_search = re.search(r'(\d+\.\d+) Gbits/sec\s+(\d+)\s+sender', output)

    if speed_search:
        speed = speed_search.group(1)
        retries = speed_search.group(2)
    else:
        speed = 'N/A'
        retries = 'N/A'

    return (speed, retries), errors


# Function to create SSH client and connect to the server
def create_ssh_client(hostname, username, key_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file(key_path)
    client.connect(hostname, username=username, pkey=private_key)
    return client


# Iterate over the hosts and perform the iperf3 tests
for client_full in hosts_full:
    client_short = client_full.split('.')[0]  # Extract the short name for display purposes
    ssh_client = create_ssh_client(client_full, ssh_username, ssh_key_filepath)
    for server_full in hosts_full:
        if server_full != client_full:
            server_short = server_full.split('.')[0]
            print(f"Testing from {client_short} to {server_short}")
            result_tuple, errors = run_iperf3_test(ssh_client, server_full)
            results[client_short][f'{server_short}_retries'] = result_tuple  # Storing the tuple (speed, retries)
            if errors:
                print(f"Errors from {client_short} to {server_short}: {errors}")
    ssh_client.close()


# Convert the results dictionary to a pandas DataFrame
df_results = pd.DataFrame(results).T  # Transpose the DataFrame to match the desired format

# Replace empty cells with 'N/A'
df_results.fillna('N/A', inplace=True)

# Display the DataFrame
print(df_results)
