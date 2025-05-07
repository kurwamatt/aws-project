from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import traceback


app = Flask(__name__)
# Enable CORS for all routes with specific configuration
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type"]}})


# Database configuration - replace with your actual RDS credentials
DB_CONFIG = {
    'host': 'db-noila.clyucs4e44b4.ap-northeast-2.rds.amazonaws.com',
    'database': 'db_noila',
    'user': 'postgres',
    'password': 'postgres2',
    'port': '5432'
}

# Table name following the required format
TABLE_NAME = 'tbl_noila_supermarket_sales'

def get_db_connection():
    """Establish a connection to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Backend is running"})

@app.route('/api/data', methods=['GET'])
def get_data():
    """Retrieve data from the database"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 100")

        rows = cursor.fetchall()
        result = [dict(row) for row in rows]

        cursor.close()
        conn.close()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['POST'])
def add_data():
    """Add new data to the database"""
    conn = None
    try:
        # Print request data for debugging
        print("Received POST request to /api/data")
        print(f"Content-Type: {request.headers.get('Content-Type')}")

        # Get JSON data from request
        data = request.get_json(force=True, silent=True)
        if not data:
            print("No JSON data found in request")
            return jsonify({"error": "No data provided or invalid JSON format"}), 400

        # Log the received data for debugging
        print(f"Received data: {data}")

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # These are the expected columns based on the table schema
        expected_columns = [
            "Invoice ID", "Date", "Customer Type", "gender",
            "Product Category", "Unit Price", "quantity",
            "Total Sales", "Payment Method"
        ]

        # Validate required fields
        missing_fields = [col for col in expected_columns if col not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Prepare the values in the correct order
        values = []
        for column in expected_columns:
            values.append(data[column])

        # Create the SQL query with proper column quoting
        columns_str = ", ".join([f'"{col}"' for col in expected_columns])
        placeholders = ", ".join(["%s"] * len(expected_columns))

        insert_query = f'INSERT INTO {TABLE_NAME} ({columns_str}) VALUES ({placeholders}) RETURNING *'

        # Log the query and values for debugging
        print(f"Executing query: {insert_query}")
        print(f"With values: {values}")

        cursor.execute(insert_query, values)
        new_row = cursor.fetchone()

        conn.commit()

        # Convert the result to a dictionary
        result = dict(new_row)
        print(f"Successfully added record: {result}")

        return jsonify({"message": "Data added successfully", "data": result})

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error in add_data: {str(e)}")
        print(f"Traceback: {error_details}")

        if conn:
            conn.rollback()  # Rollback transaction on error

        return jsonify({
            "error": str(e),
            "details": error_details
        }), 500
    finally:
        if conn:
            conn.close()  # Ensure connection is closed

@app.route('/api/data/<string:record_id>', methods=['DELETE'])
def delete_data(record_id):
    """Delete data from the database"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        # Primary key column is "Invoice ID"
        pk_column_name = "Invoice ID"
        cursor.execute(f'DELETE FROM {TABLE_NAME} WHERE "{pk_column_name}" = %s RETURNING "{pk_column_name}"', (record_id,))
        deleted = cursor.fetchone()

        conn.commit()
        cursor.close()

        if deleted:
            return jsonify({"message": f"Record {record_id} deleted successfully"})
        else:
            return jsonify({"error": f"Record {record_id} not found"}), 404

    except Exception as e:
        if conn:
            conn.rollback()  # Rollback transaction on error
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()  # Ensure connection is closed

@app.route('/api/schema', methods=['GET'])
def get_schema():
    """Get the database schema information"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = '{TABLE_NAME}'
            ORDER BY ordinal_position
        """)

        columns = cursor.fetchall()
        schema = [{"column": col[0], "type": col[1]} for col in columns]

        cursor.close()
        conn.close()

        return jsonify(schema)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
