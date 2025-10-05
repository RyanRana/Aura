import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import snowflake.connector
# --- Import Your Existing Logic ---
# We assume these functions are in the files as described
from app import run_agentic_flow, route_user_question
from csv_parser import get_ai_upload_plan, smart_upload_csv, get_all_table_schemas
from database_connector import get_schema_for_agent
import pandas as pd

# --- Flask App Initialization ---
app = Flask(__name__)
CORS(app) # This enables Cross-Origin Resource Sharing

# Define a folder to store temporary uploads
UPLOAD_FOLDER = 'temp_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Load Schema Once on Startup ---
print("Loading database schema for the API...")
DB_SCHEMA = get_schema_for_agent()
if not DB_SCHEMA:
    print("FATAL: Could not load database schema. The API may not function correctly.")

# --- API Endpoints ---

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint to handle chat interactions with the Aria agent."""
    data = request.json
    user_question = data.get('message')
    chat_history = data.get('history', [])

    if not user_question:
        return jsonify({"error": "No message provided."}), 400

    # Use the router to check intent
    intent = route_user_question(user_question, DB_SCHEMA)
    
    final_answer = ""
    if intent == 'data_query':
        # If it's a data query, run the full agentic flow
        final_answer = run_agentic_flow(user_question, DB_SCHEMA, chat_history)
    elif intent == 'greeting':
        final_answer = "Hello! I'm Aria, your Autonomous Retail Intelligence Agent. How can I help you analyze our data today?"
    elif intent == 'off_topic':
        final_answer = "I'm sorry, but I can only answer questions related to our retail data. Please ask something about sales, inventory, or product performance."
    elif intent == 'unanswerable':
        final_answer = "I understand you're asking about business/retail topics, but I don't have the necessary data in our system to answer that question. I can help you with questions about sales, inventory, product performance, and other data that's available in our Snowflake database. Could you try rephrasing your question to focus on data we have available?"
    else:
        final_answer = "I'm not sure how to handle that request. Please try asking a question related to our retail data."

    return jsonify({"response": final_answer})


@app.route('/api/execute-upload', methods=['POST'])
def execute_upload():
    """
    Endpoint to execute the CSV upload after the user has confirmed the AI's plan.
    """
    data = request.json
    filename = data.get('filename')
    table_name = data.get('suggested_table')
    column_mapping = data.get('column_mapping')
    schema_name = os.getenv("SNOWFLAKE_SCHEMA")

    if not all([filename, table_name, column_mapping, schema_name]):
        return jsonify({"error": "Missing data for upload execution."}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({"error": f"File {filename} not found on server."}), 404

    try:
        success, message = smart_upload_csv(
            file_path=filepath,
            table_name=table_name,
            schema_name=schema_name,
            column_mapping=column_mapping
        )

        if success:
            # Clean up the temp file after successful upload
            os.remove(filepath)
            return jsonify({"message": f"Successfully uploaded data to {table_name}."})
        else:
            return jsonify({"error": message}), 500

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred during upload: {str(e)}"}), 500

# We will add another endpoint here later for executing the upload after user confirmation.
# We will also add endpoints for the dashboard later.

@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """Endpoint to fetch all data needed for the main dashboard."""
    conn = None
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        cur = conn.cursor()

        # Query 1: Total Revenue (7D)
        cur.execute("""
            SELECT SUM(NET_SALES) 
            FROM FACT_SALES_DAILY
            WHERE DATE_KEY IN (SELECT DATE_KEY FROM DIM_DATE WHERE D_DATE >= DATEADD(day, -7, CURRENT_DATE()));
        """)
        total_revenue = cur.fetchone()[0]

        # Query 2: Units Sold (7D)
        cur.execute("""
            SELECT SUM(QTY_SOLD)
            FROM FACT_SALES_DAILY
            WHERE DATE_KEY IN (SELECT DATE_KEY FROM DIM_DATE WHERE D_DATE >= DATEADD(day, -7, CURRENT_DATE()));
        """)
        units_sold = cur.fetchone()[0]

        # Query 3: Top Product (All Time by units sold)
        cur.execute("""
            SELECT P.PRODUCT_NAME
            FROM FACT_SALES_DAILY S
            JOIN DIM_PRODUCT P ON S.PRODUCT_KEY = P.PRODUCT_KEY
            GROUP BY P.PRODUCT_NAME
            ORDER BY SUM(S.QTY_SOLD) DESC
            LIMIT 1;
        """)
        top_product = cur.fetchone()[0]

        # Query 4: Recent Sales Activity (Last 5 transactions)
        cur.execute("""
            SELECT P.PRODUCT_NAME, S.QTY_SOLD, ST.STORE_NAME, S.NET_SALES
            FROM FACT_SALES_DAILY S
            JOIN DIM_PRODUCT P ON S.PRODUCT_KEY = P.PRODUCT_KEY
            JOIN DIM_STORE ST ON S.STORE_KEY = ST.STORE_KEY
            ORDER BY S.LOAD_TS DESC
            LIMIT 5;
        """)
        recent_sales_raw = cur.fetchall()
        recent_sales = [
            {
                "text": f"{row[0]} sold {int(row[1])} units at {row[2]}",
                "value": f"${row[3]:.2f}"
            } for row in recent_sales_raw
        ]

        # NOTE: Avg Profit Margin is complex without cost data. We'll use a placeholder.
        avg_profit_margin = "96.7%"

        dashboard_data = {
            "totalRevenue": f"${total_revenue:,.2f}",
            "unitsSold": f"{int(units_sold):,}",
            "avgProfitMargin": avg_profit_margin,
            "topProduct": top_product,
            "recentSales": recent_sales
        }
        
        return jsonify(dashboard_data)

    except Exception as e:
        print(f"Error fetching dashboard data: {e}")
        return jsonify({"error": "Failed to fetch dashboard data."}), 500
    finally:
        if conn:
            conn.close()
# --- Main Execution ---
if __name__ == '__main__':
    # Runs the Flask app on localhost, port 5001
    app.run(debug=True, port=5001)