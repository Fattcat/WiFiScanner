from time import sleep, strftime
import pywifi
from pywifi import const
import os
import datetime

datum = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

# [-----------FARBY------------]
reset = '\033[0m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
orange = '\033[33m\033[31m'
blue = '\033[34m'
magenta = '\033[35m'
# [-----------FARBY------------]

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

def get_security_type_name(result):
    # Get the corresponding security type name
    return security_type_mapping.get(result.akm[0], "Unknown") if result.akm else "Unknown"

def scan_wifi():
    wifi = pywifi.PyWiFi()

    # Check if there are any interfaces
    interfaces = wifi.interfaces()
    if not interfaces:
        print("Error: No wireless interfaces available.")
        return

    # Select wlan1 or the first available interface
    iface = next((i for i in interfaces if "wlan1" in i.name()), interfaces[0])

    iface.scan()
    sleep(2)
    scan_results = iface.scan_results()

    with open(filename, "a") as file:
        file.write("\n\n+" + "--" * 20 + "+\n")
        file.write(f"      Scan Time: {strftime('%Y-%m-%d %H:%M:%S')}\n")
        for result in scan_results:
            ssid = result.ssid
            bssid = result.bssid
            freq = result.freq
            channel = freq_to_channel(freq)
            security_type = get_security_type_name(result)
            signal_strength = result.signal

            # Print colored results to the terminal
            print(f"\n\n[{magenta}+{reset}]" + "--" * 20 + f"[{magenta}+{reset}]")
            print(f"    [+] Scan Time: {strftime('%Y-%m-%d %H:%M:%S')} [+]\n")
            print(f"{yellow}SSID{reset}: {green}{ssid}{reset}")
            print(f"{yellow}MAC{reset} : {green}{bssid}{reset}")
            print(f"{yellow}CH{reset}  : {green}{channel}{reset}, {yellow}Freq: {reset}{green}{freq}{reset}")
            print(f"{yellow}SecType{reset}: {green}{security_type}{reset}")
            print(f"{yellow}Signal{reset} : {green}{signal_strength}{reset} {yellow}dB{reset}")
            print(f"[{magenta}+{reset}]" + "--" * 20 + f"[{magenta}+{reset}]\n")

            # Write to the file without colored text
            file.write("+" + "--" * 20 + "+\n")
            file.write(f"      Scan Time: {strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"SSID: {ssid}\n")
            file.write(f"MAC Address: {bssid}\n")
            file.write(f"CH: {channel} Freq: {freq}\n")
            file.write(f"Security Type: {security_type}\n")
            file.write(f"Signal Strength: {signal_strength} dB\n")

def main():
    while True:
        print(f"[{magenta}+{reset}]" + "--" * 20 + f"[{magenta}+{reset}]\n")
        print(f"[{magenta}+{reset}] Starting Donk - WiFi Scanner [{magenta}+{reset}]")
        print(f"\nSkenovanie sieti v okoli ...\n")
        sleep(2)
        print(f"   : -------- {red}Vysledky skenu{reset} --------:")
        scan_wifi()
        sleep(3)

if __name__ == "__main__":
    main()
