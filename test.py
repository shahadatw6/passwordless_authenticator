
# Import required modules
import time
import board
import busio
import digitalio
import adafruit_ssd1306
import adafruit_framebuf
import adafruit_hashlib as hashlib
import struct
import wifi
import adafruit_ntp
import rtc
import socketpool

# WiFi configuration
WIFI_SSID = "Mehedi bhai 10"
WIFI_PASSWORD = "SAMMY7890"

# ESP32 IP address and port (replace with your Flask server's IP address and port)
ESP_IP_ADDRESS = "192.168.31.29"
ESP_PORT = 5000

# Initialize I2C communication
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize OLED display
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize socket pool and NTP client
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0)

# Connect to WiFi
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)

# Get current time from NTP server
try:
    rtc.RTC().datetime = ntp.datetime
except Exception as e:
    print("Error setting time:", e)

# Main function to fetch and display TOTP tokens
def display_totp():
    # Fetch TOTP tokens from Flask server
    try:
        with wifi.radio.socket() as socket:
            addr_info = socket.getaddrinfo(ESP_IP_ADDRESS, ESP_PORT)
            addr = addr_info[0][-1]
            socket.connect(addr)
            socket.send(b"GET / HTTP/1.0\r\n\r\n")
            response = socket.readline()
            print("Response:", response)
            if response.startswith(b"HTTP/1.0 200"):
                data = socket.read()
                print("Data:", data)
                tokens = data.split(b"\n")
                print("Tokens:", tokens)
    except Exception as e:
        print("Error fetching tokens:", e)

    # Display tokens on OLED
    oled.fill(0)
    oled.text("ESP32 TOTP Tokens:", 0, 0, 1)
    y = 10
    for token in tokens:
        oled.text(token.strip().decode("utf-8"), 0, y, 1)
        y += 10
    oled.show()

# Main loop to continuously display TOTP tokens
while True:
    display_totp()
    time.sleep(30)  # Refresh tokens every 30 seconds