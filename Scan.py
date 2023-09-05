import time
import pywifi
from pywifi import const

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()
    time.sleep(2)
    scan_results = iface.scan_results()

    for result in scan_results:
        ssid = result.ssid
        bssid = result.bssid
        channel = result.channel
        security_type = result.akm[0]
        signal_strength = result.signal

        print("WiFi (SSID):", ssid)
        print("Mac Address:", bssid)
        print("Channel:", channel)
        print("Security Type:", security_type)
        print("WiFi Signal Strength:", signal_strength)
        print()

def main():
    while True:
        print("\nScanning for WiFi networks...\n")
        scan_wifi()
        time.sleep(8)

if __name__ == "__main__":
    main()
