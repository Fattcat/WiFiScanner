from time import sleep, strftime
import pywifi
from pywifi import const
import os
import datetime

datum = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

# Specify the folder where the file will be saved
folder = "/home/kali/Desktop/WiFiScanResult"

if not os.path.exists(folder):
    os.makedirs(folder)

# Specify the file where the results will be saved
filename = os.path.join(folder, f"{datum}.txt")

# Mapping of numerical security types to their corresponding names
security_type_mapping = {
    const.AKM_TYPE_NONE: "None",
    const.AKM_TYPE_WPA: "WPA",
    const.AKM_TYPE_WPAPSK: "WPA-PSK",
    const.AKM_TYPE_WPA2: "WPA2",
    const.AKM_TYPE_WPA2PSK: "WPA2-PSK",
    const.AKM_TYPE_UNKNOWN: "Unknown",
}

def freq_to_channel(freq):
    # Convert frequency to channel number
    if 2412 <= freq <= 2484:
        return (freq - 2412) // 5 + 1
    elif 5180 <= freq <= 5825:
        return (freq - 5180) // 5 + 36
    else:
        return None

def get_security_type_name(security_type):
    # Get the corresponding security type name
    return security_type_mapping.get(security_type, "Unknown")

def scan_wifi():
    wifi = pywifi.PyWiFi()
    
    # Use wlan1 as the wireless interface
    iface = wifi.interfaces()[1]

    iface.scan()
    sleep(2)
    scan_results = iface.scan_results()

    with open(filename, "a") as file:
        file.write("+" + "--" * 20 + "\n")
        file.write(f"Scan Time: {strftime('%Y-%m-%d %H:%M:%S')}\n")
        for result in scan_results:
            ssid = result.ssid
            bssid = result.bssid
            freq = result.freq
            channel = freq_to_channel(freq)
            security_type = get_security_type_name(result.akm[0])
            signal_strength = result.signal

            # Write to the file
            file.write("+" + "--" * 20 + "+\n")
            file.write("Datum : " + datum + "\n")
            file.write(f"WiFi (SSID): {ssid}" + "\n")
            file.write(f"MAC Address: {bssid}" + "\n")
            file.write(f"Channel: {channel}" + "\n")
            file.write(f"Security Type: {security_type}" + "\n")
            file.write(f"WiFi Signal Strength: {signal_strength}" + "\n")
            file.write("+" + "--" * 20 + "+\n\n")

def main():
    while True:
        print("\nScanning for WiFi networks...\n")
        scan_wifi()
        sleep(8)

if __name__ == "__main__":
    main()
