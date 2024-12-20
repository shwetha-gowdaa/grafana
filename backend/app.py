from flask import Flask, jsonify, Response, make_response
from prometheus_client import start_http_server, Summary, generate_latest, CONTENT_TYPE_LATEST
import psycopg2

app = Flask(__name__)

# Create a metric to track the request processing time
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Database connection parameters
DB_HOST = "db"
DB_NAME = "mydb"
DB_USER = "user"
DB_PASSWORD = "password"

# Database query
def get_data_from_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_table;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Endpoint for Prometheus metrics
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/api/data', methods=['GET'])
@REQUEST_TIME.time()
def get_data():
    try:
        data = get_data_from_db()
        response = make_response(jsonify({
            "source": "backend",
            "data": data
        }))
        response.headers['X-Source'] = 'Backend'
        return response
    except Exception as e:
        response = make_response(jsonify({"error": str(e)}), 500)
        response.headers['X-Source'] = 'Backend'
        return response

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5000)
