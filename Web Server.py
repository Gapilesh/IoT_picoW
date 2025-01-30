import network
import socket
import time
from machine import Pin

ssid = "Gapzzz"  # Replace with your Wi-Fi name
password = "********"  # Replace with your Wi-Fi password

led = Pin("LED", Pin.OUT)  # Onboard LED on Pico W

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
while not wlan.isconnected():
    time.sleep(1)

print("Connected to Wi-Fi:", wlan.ifconfig()[0])

# Create Web Server
def webpage():
    return """<!DOCTYPE html>
<html>
<head>
    <title>Pico W LED Control</title>
</head>
<body>
    <h2>Control Onboard LED</h2>
    <a href="/?led=on"><button style="padding:10px;font-size:20px;">Turn ON</button></a>
    <a href="/?led=off"><button style="padding:10px;font-size:20px;">Turn OFF</button></a>
</body>
</html>"""

# Start Web Server
addr = ("0.0.0.0", 80)
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Web Server Running...")

while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()
    print("Request:", request)

    if "/?led=on" in request:
        led.on()
    elif "/?led=off" in request:
        led.off()

    response = webpage()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + response)
    conn.close()

