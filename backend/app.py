from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = psycopg2.connect(
        host="db",
        database="mydb",
        user="user",
        password="password"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_table;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
