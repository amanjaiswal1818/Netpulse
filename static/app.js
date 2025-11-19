document.addEventListener('DOMContentLoaded', () => {
    const hostInput = document.getElementById('host-input');
    const pingBtn = document.getElementById('ping-btn');
    const nmapBtn = document.getElementById('nmap-btn');
    const outputBox = document.getElementById('output-box');
    const sysInfoBox = document.getElementById('sys-info');

    async function runCommand(url) {
        outputBox.textContent = 'Running...';
        try {
            const response = await fetch(url);
            const data = await response.json();
            outputBox.textContent = data.output;
        } catch (error) {
            outputBox.textContent = `Error: ${error.message}`;
        }
    }

    pingBtn.addEventListener('click', () => {
        const host = hostInput.value || '8.8.8.8';
        runCommand(`/api/ping?host=${host}`);
    });

    nmapBtn.addEventListener('click', () => {
        const host = hostInput.value || '127.0.0.1';
        runCommand(`/api/nmap?host=${host}`);
    });

    const speedtestBtn = document.getElementById('speedtest-btn');
    speedtestBtn.addEventListener('click', () => {
        runCommand('/api/speedtest');
    });

    const macInput = document.getElementById('mac-input');
    const wolBtn = document.getElementById('wol-btn');

    wolBtn.addEventListener('click', async () => {
        const mac_address = macInput.value;
        if (!mac_address) {
            outputBox.textContent = 'Please enter a MAC address.';
            return;
        }

        outputBox.textContent = 'Sending Magic Packet...';
        try {
            const response = await fetch('/api/wol', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ mac_address })
            });
            const data = await response.json();
            outputBox.textContent = data.output;
        } catch (error) {
            outputBox.textContent = `Error: ${error.message}`;
        }
    });
    
    // Update system info every 3 seconds
    setInterval(async () => {
        const response = await fetch('/api/sysinfo');
        const data = await response.json();
        sysInfoBox.textContent = `CPU: ${data.cpu}% | RAM: ${data.ram}% | Temp: ${data.temp}`;
    }, 3000);
});