from time import sleep, strftime
import pywifi
from pywifi import const
import os

# Specify the folder where the files will be saved
Folder = r"D:\PY-WiFiScan"

if not os.path.exists(Folder):
    os.makedirs(Folder)

def freq_to_channel(freq):
    # Convert frequency to channel number
    if 2412 <= freq <= 2484:
        return (freq - 2412) // 5 + 1
    elif 5180 <= freq <= 5825:
        return (freq - 5180) // 5 + 36
    else:
        return None


def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()
    sleep(2)
    scan_results = iface.scan_results()

    for result in scan_results:
        ssid = result.ssid
        bssid = result.bssid
        freq = result.freq
        channel = freq_to_channel(freq)
        security_type = result.akm[0]
        signal_strength = result.signal
        print("+" + "--" * (len(bssid) - 3) + "+")
        print("WiFi (SSID):", ssid)
        print("Mac Address:", bssid)
        print("Channel:", channel)
        print("Security Type:", security_type)
        print("WiFi Signal Strength:", signal_strength)
        print("+" + "--" * (len(bssid) - 3)  + "+")
        print("\n")

        # Save to USB with a timestamp in the file name
        timestamp = strftime("%Y-%m-%d %H-%M-%S")
        filename = os.path.join(Folder, f"wifi_results_{timestamp}.txt")
        save_to_usb(filename, ssid, channel, security_type, signal_strength)

def save_to_usb(filename, ssid, channel, security_type, signal_strength):
    with open(filename, "a") as file:
        file.write("+" + "--" * 20 + "+\n")
        file.write(f"WiFi (SSID): {ssid}\n")
        file.write(f"Channel: {channel}\n")
        file.write(f"Security Type: {security_type}\n")
        file.write(f"WiFi Signal Strength: {signal_strength}\n")
        file.write("+" + "--" * 20 + "+\n")

def main():
    while True:
        print("\nScanning for WiFi networks...\n")
        scan_wifi()
        sleep(8)

if __name__ == "__main__":
    main()
