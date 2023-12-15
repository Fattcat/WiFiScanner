from time import sleep, strftime
import pywifi
from pywifi import const
import os
import datetime
from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE

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

def get_gps_interface():
    try:
        gpsd_socket = gps(host="localhost", port="2947")
        return gpsd_socket
    except Exception as e:
        print(f"Error connecting to GPS: {e}")
        return None

def get_gps_location(session, timeout=5):
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            report = session.next()
            if 'lat' in report and 'lon' in report and 'alt' in report:
                return report['lat'], report['lon'], report['alt']
        except StopIteration:
            pass
        except Exception as e:
            print(f"Error in get_gps_location: {e}")

    print("Timeout reached for GPS data. Proceeding without GPS.")
    return None, None, None

def write_gps_info(file, lat, lon, alt):
    file.write(f"GPS Lat: {lat}\n")
    file.write(f"GPS Lon: {lon}\n")
    file.write(f"GPS Alt: {alt}\n")

def scan_wifi(interface):
    interface.scan()
    sleep(2)
    scan_results = interface.scan_results()

    with open(filename, "a") as file:
        file.write("\n" + "=" * 40 + "\n")
        file.write(f"Scan Time: {strftime('%Y-%m-%d %H:%M:%S')}\n")

        gps_session = get_gps_interface()
        if gps_session:
            lat, lon, alt = get_gps_location(gps_session)
            if lat is not None and lon is not None and alt is not None:
                write_gps_info(file, lat, lon, alt)
            else:
                print("No GPS data available.")

        for result in scan_results:
            ssid = result.ssid
            bssid = result.bssid
            freq = result.freq
            channel = freq_to_channel(freq)
            security_type = get_security_type_name(result.akm[0])
            signal_strength = result.signal

            print("\n" + "=" * 40)
            print(f"SSID: {ssid}")
            print(f"MAC Address: {bssid}")
            print(f"CH: {channel} Freq: {freq}")
            print(f"Security Type: {security_type}")
            print(f"Signal Strength: {signal_strength} dB")

            lat, lon, alt = get_gps_location(gps_session)
            if lat is not None and lon is not None and alt is not None:
                print(f"GPS Lat: {lat}")
                print(f"GPS Lon: {lon}")
                print(f"GPS Alt: {alt}")
            
            print("=" * 40 + "\n")

            file.write("=" * 40 + "\n")
            file.write(f"SSID: {ssid}\n")
            file.write(f"MAC Address: {bssid}\n")
            file.write(f"CH: {channel} Freq: {freq}\n")
            file.write(f"Security Type: {security_type}\n")
            file.write(f"Signal Strength: {signal_strength} dB\n")
            file.write(f"GPS Lat: {lat}\n")
            file.write(f"GPS Lon: {lon}\n")
            file.write(f"GPS Alt: {alt}\n")

def main():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()

    # Use wlan1 as the wireless interface
    for iface in interfaces:
        if "wlan1" in iface.name():
            selected_interface = iface
            break
    else:
        print("WiFi interface 'wlan1' not found.")
