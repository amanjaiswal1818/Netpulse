# app.py
import subprocess
from flask import Flask, render_template, jsonify, request
import psutil
import speedtest
import wakeonlan
import scapy.all as scapy
from mac_vendor_lookup import MacLookup

app = Flask(__name__)
mac_lookup = MacLookup()

# --- Frontend Route ---
@app.route('/')
def index():
    return render_template('index.html')

# --- API Routes ---
@app.route('/api/ping')
def api_ping():
    host = request.args.get('host', '8.8.8.8') # Default to Google's DNS
    try:
        # Use subprocess to run the ping command
        result = subprocess.check_output(['ping', '-n', '4', host], text=True, stderr=subprocess.STDOUT)
        return jsonify({'status': 'success', 'output': result})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'output': e.output})

@app.route('/api/nmap')
def api_nmap():
    host = request.args.get('host', '127.0.0.1') # Default to localhost
    try:
        # Run a simple nmap scan
        result = subprocess.check_output(['nmap', '-F', host], text=True, stderr=subprocess.STDOUT)
        return jsonify({'status': 'success', 'output': result})
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        output = e.output if hasattr(e, 'output') else "nmap command not found. Is it installed?"
        return jsonify({'status': 'error', 'output': output})

@app.route('/api/sysinfo')
def api_sysinfo():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    # On Pi, we can get temp. For now, we'll fake it.
    temp = "N/A" 
    try:
        # This will only work on the Raspberry Pi
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp_milli_c = int(f.read())
            temp = f"{temp_milli_c / 1000.0:.1f}°C"
    except FileNotFoundError:
        pass # Not on a Pi
        
    return jsonify(cpu=cpu, ram=ram, temp=temp)


@app.route('/api/speedtest')
def api_speedtest():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping = st.results.ping

        result = (
            f"Download: {download_speed:.2f} Mbps\n"
            f"Upload: {upload_speed:.2f} Mbps\n"
            f"Ping: {ping:.2f} ms"
        )
        return jsonify({'status': 'success', 'output': result})
    except Exception as e:
        return jsonify({'status': 'error', 'output': str(e)})


@app.route('/api/wol', methods=['POST'])
def api_wol():
    mac_address = request.json.get('mac_address')
    if not mac_address:
        return jsonify({'status': 'error', 'output': 'MAC address is required.'}), 400
    try:
        wakeonlan.send_magic_packet(mac_address)
        return jsonify({'status': 'success', 'output': f'Magic packet sent to {mac_address}'})
    except Exception as e:
        return jsonify({'status': 'error', 'output': str(e)})

@app.route('/api/discover')
def api_discover():
    try:
        # Create an ARP request packet to broadcast to the local network
        arp_request = scapy.ARP(pdst="192.168.1.0/24")
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        
        # Send the packet and receive responses
        result = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        # Parse the responses to create a list of devices
        devices = []
        for sent, received in result:
            mac = received.hwsrc
            ip = received.psrc
            vendor = "Unknown"
            try:
                vendor = mac_lookup.lookup(mac)
            except Exception:
                pass # Vendor not found in database

            devices.append({'ip': ip, 'mac': mac, 'vendor': vendor})

        return jsonify({'status': 'success', 'devices': devices})
    except Exception as e:
        return jsonify({'status': 'error', 'output': str(e)})


if __name__ == '__main__':
    # Host 0.0.0.0 makes it accessible on your network
    app.run(debug=True, host='0.0.0.0')
