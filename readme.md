# NetPulse 🌐

A powerful web-based network monitoring and diagnostic tool built with Flask. NetPulse provides real-time network analysis, device discovery, system monitoring, and remote wake capabilities through an intuitive web interface.

## Features

- 🔍 **Network Discovery**: Scan and discover all devices on your local network
- 📡 **Ping Tool**: Test connectivity to any host with detailed output
- 🛡️ **Port Scanner**: Nmap integration for quick port scanning
- ⚡ **Speed Test**: Measure your internet download/upload speeds and ping
- 💻 **System Monitoring**: Real-time CPU, RAM, and temperature monitoring
- 🔌 **Wake-on-LAN**: Remotely wake devices using magic packets
- 🏷️ **Vendor Identification**: Automatically identify device manufacturers from MAC addresses

## Prerequisites

- Python 3.7 or higher
- Nmap (for port scanning functionality)
- Administrator/Root privileges (for network discovery and packet sending)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/amanjaiswal1818/Netpulse.git
cd Netpulse
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Python dependencies
```bash
pip install Flask psutil speedtest-cli wakeonlan scapy mac-vendor-lookup
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 4. Install Nmap

**Windows:**
- Download from [nmap.org](https://nmap.org/download.html)
- Run the installer and ensure nmap is added to PATH

**Linux:**
```bash
sudo apt-get update
sudo apt-get install nmap
```

**macOS:**
```bash
brew install nmap
```

## Usage

### Starting the Server

**Run with standard privileges:**
```bash
python app.py
```

**Run with administrator privileges (required for network discovery):**

**Windows:**
```bash
# Run Command Prompt as Administrator
python app.py
```

**Linux/Mac:**
```bash
sudo python app.py
```

The application will be accessible at:
- Local: `http://localhost:5000`
- Network: `http://your-ip-address:5000`

## Features Guide

### 🔍 Network Discovery
Scans your local network (192.168.1.0/24) and displays:
- IP addresses of all connected devices
- MAC addresses
- Device manufacturer/vendor information

**API Endpoint:** `GET /api/sysinfo`

### 🔌 Wake-on-LAN
Remotely wake computers on your network using magic packets.

**API Endpoint:** `POST /api/wol`

**Request Body:**
```json
{
  "mac_address": "AA:BB:CC:DD:EE:FF"
}
```

## API Reference

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/api/ping` | GET | `host` | Ping a host |
| `/api/nmap` | GET | `host` | Scan ports on a host |
| `/api/sysinfo` | GET | None | Get system information |
| `/api/speedtest` | GET | None | Run internet speed test |
| `/api/discover` | GET | None | Discover network devices |
| `/api/wol` | POST | `mac_address` | Send Wake-on-LAN packet |

## Configuration

### Changing Network Range for Discovery

Edit the network range in `app.py`:

```python
# Default: 192.168.1.0/24
arp_request = scapy.ARP(pdst="192.168.1.0/24")

# Change to your network, e.g., 10.0.0.0/24
arp_request = scapy.ARP(pdst="10.0.0.0/24")
```

### Customizing Server Port

```python
# Change port from default 5000
app.run(debug=True, host='0.0.0.0', port=8080)
```

## Project Structure

```
netpulse/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend interface
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── README.md
```

## Requirements

Create a `requirements.txt` file with:

```
Flask
psutil
speedtest-cli
wakeonlan
scapy
mac-vendor-lookup
```

## Troubleshooting

### Permission Errors
**Problem:** Network discovery or packet sending fails

**Solution:** Run the application with administrator/sudo privileges
```bash
# Windows (Run as Administrator)
python app.py

# Linux/Mac
sudo python app.py
```

### Nmap Not Found
**Problem:** Port scanning returns "nmap command not found"

**Solution:** Install nmap and ensure it's in your system PATH

### Scapy Issues on Windows
**Problem:** Scapy doesn't work on Windows

**Solution:** Install Npcap from [npcap.com](https://npcap.com/)
- Download and install with "WinPcap API-compatible mode" enabled

### Temperature Reading Not Available
**Problem:** Temperature shows "N/A"

**Solution:** Temperature monitoring currently only works on Raspberry Pi. For other systems, you can integrate platform-specific temperature monitoring libraries.

## Security Considerations

- **Run on trusted networks only** - This tool performs network scanning
- **Firewall configuration** - Ensure port 5000 (or custom port) is allowed
- **Use HTTPS in production** - Consider using a reverse proxy like nginx
- **Authentication** - Add authentication for production deployments
- **Rate limiting** - Implement rate limiting for API endpoints

## Use Cases

- 🏠 **Home Network Management**: Monitor all devices on your home network
- 🏢 **IT Administration**: Quick network diagnostics and device inventory
- 🎓 **Educational**: Learn about networking protocols and tools
- 🔧 **Troubleshooting**: Diagnose network connectivity issues
- 📊 **Monitoring**: Track system performance over time

## Future Enhancements

- [ ] Add authentication and user management
- [ ] Historical data logging and charts
- [ ] Email/SMS alerts for network events
- [ ] Support for multiple network interfaces
- [ ] Advanced filtering and search for discovered devices
- [ ] Export data to CSV/JSON
- [ ] Dark mode UI
- [ ] Mobile-responsive design improvements
- [ ] Scheduled speed tests
- [ ] Custom ping intervals

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Scapy](https://scapy.net/) - Network packet manipulation
- [Nmap](https://nmap.org/) - Network scanner
- [psutil](https://github.com/giampaolo/psutil) - System monitoring
- [speedtest-cli](https://github.com/sivel/speedtest-cli) - Internet speed testing

## Disclaimer

This tool is intended for authorized network administration and educational purposes only. Always ensure you have permission before scanning networks or devices that you do not own.

---

**⚠️ Important**: Running network scans on networks you don't own or without permission may be illegal in your jurisdiction. Use responsibly!

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Contribute to the project

---

Made with ❤️ for network administrators and enthusiastsGET /api/discover`

### 📡 Ping Tool
Test connectivity to any host with detailed ping statistics.

**API Endpoint:** `GET /api/ping?host=8.8.8.8`

**Parameters:**
- `host`: Target IP address or domain (default: 8.8.8.8)

### 🛡️ Port Scanner (Nmap)
Perform fast port scans on target hosts to identify open services.

**API Endpoint:** `GET /api/nmap?host=192.168.1.1`

**Parameters:**
- `host`: Target IP address (default: 127.0.0.1)

### ⚡ Speed Test
Measure your internet connection performance:
- Download speed (Mbps)
- Upload speed (Mbps)
- Ping latency (ms)

**API Endpoint:** `GET /api/speedtest`

### 💻 System Monitoring
Monitor your system's health in real-time:
- CPU usage percentage
- RAM usage percentage
- System temperature (Raspberry Pi supported)


**API Endpoint:** `

