import subprocess
import re

def run_command(command):
    result = subprocess.run(command, text=True, shell=True, stdout=subprocess.PIPE)
    return result.stdout

def get_device_rssi():
    # Start the Bluetooth tool
    run_command("bluetoothctl power on")
    run_command("bluetoothctl agent on")
    run_command("bluetoothctl scan on")

    # Allow some time to discover devices
    print("Scanning for devices... Please wait.")
    time.sleep(10)  # Scan for 10 seconds

    # List devices
    devices_output = run_command("bluetoothctl devices")
    
    # Extract device addresses
    devices = re.findall(r'Device (\S+) ', devices_output)

    # Get info for each device
    for device in devices:
        info_output = run_command(f"bluetoothctl info {device}")
        rssi_match = re.search(r'RSSI: ([-\d]+)', info_output)
        if rssi_match:
            print(f"Device {device} RSSI: {rssi_match.group(1)}")
        else:
            print(f"Device {device} RSSI: Not available")

    # Stop scanning and clean up
    run_command("bluetoothctl scan off")
    run_command("bluetoothctl power off")

get_device_rssi()
