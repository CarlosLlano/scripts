import subprocess
import re
import time


def ping(host, count=4):
    try:
        # Run the ping command and capture the output
        ping_result = subprocess.run(['ping', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True, timeout=10)

        # Check if the ping was successful
        if ping_result.returncode == 0:
            # Extract the round-trip time values from the output using regular expressions
            ping_times = re.findall(r"time=(\d+\.\d+)", ping_result.stdout)

            if ping_times:
                # Calculate the average round-trip time
                avg_ping_time = sum(float(time) for time in ping_times) / len(ping_times)
                return avg_ping_time, None
            else:
                return None, "No ping times found in the output."
        else:
            return None, f"Ping failed with return code {ping_result.returncode}: {ping_result.stderr}"
    except subprocess.TimeoutExpired:
        return None, "Ping command timed out."


if __name__ == "__main__":
    host_to_ping = "192.168.10.178"
    ping_count = 4  # Number of ping requests to send

    while True:
        avg_time, error = ping(host_to_ping, ping_count)

        if error:
            print(f"Error: {error}")
        else:
            print(f"Average Ping Time: {avg_time} ms")

        time.sleep(60)  # Wait for 60 seconds before pinging again