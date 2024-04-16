import ampule
import socketpool
import wifi
import time

@ampule.route("/hello/world")
def light_set(request):
    return (200, {}, 'Hi There!')

# Connect to WiFi & get date/time
print("Connecting to WiFi...")


wifi.radio.connect("Fab Lab IUB", "fabbers@iub")  # Replace with your WiFi SSID and PSK
time.sleep(1)  # Wait for the connection to be established

print("Connected to WiFi!")


pool = socketpool.SocketPool(wifi.radio)
socket = pool.socket()
socket.bind(('0.0.0.0', 1234))
socket.listen(1)
socket.setblocking(True)
print("Listening on %s, IPv4 Addr: %s" % (socket, wifi.radio.ipv4_address))

while True:
    ampule.listen(socket)