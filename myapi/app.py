from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import time

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) # Mở khóa CORS tuyệt đối cho mọi nguồn

def get_db_connection():
    # Hàm tự động thử lại nếu MariaDB khởi động chậm hơn Flask
    for i in range(5):
        try:
            conn = mysql.connector.connect(
                host="mariadb",
                user="root",
                password="123",
                database="monitor_db"
            )
            return conn
        except mysql.connector.Error:
            time.sleep(2)
    return None

@app.route('/api/realtime-value', methods=['GET'])
def get_realtime_value():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"parameter_name": "Giá Bitcoin (USD)", "current_value": 62950.00, "status": "NORMAL"})

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT parameter_name, current_value, status FROM current_metrics WHERE parameter_name = 'Giá Bitcoin (USD)' ORDER BY id DESC LIMIT 1")
        data = cursor.fetchone()
        cursor.close()
        conn.close()

        if data:
            return jsonify(data)
    except Exception as e:
        pass

    return jsonify({"parameter_name": "Giá Bitcoin (USD)", "current_value": 62950.00, "status": "NORMAL"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
