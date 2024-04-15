from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# ESP32 IP Address and Port
ESP32_IP = "192.168.31.29"
ESP32_PORT = 80

@app.route('/')
def index():
    try:
        # Fetch TOTP Value from ESP32
        response = requests.get(f"http://{ESP32_IP}/totp_value_endpoint")
        
        if response.status_code == 200:
            totp_value = response.text
        else:
            totp_value = f"Error fetching TOTP: {response.status_code}"
    except Exception as e:
        totp_value = f"Connection Error: {e}"
    
    return render_template('index.html', esp_ip_address=ESP32_IP, esp_port=ESP32_PORT, totp_value=totp_value)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
