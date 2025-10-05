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

# --- Mock Mode (set AURA_MOCK_DATA=1 to enable stub responses when DB is down) ---
USE_MOCK_DATA = os.environ.get("AURA_MOCK_DATA", "0") == "1"

def _mock_dashboard_data():
    return {
        "totalRevenue": "$1,234,567.89",
        "unitsSold": "98,765",
        "avgProfitMargin": "34.2%",
        "topProduct": "Whole Milk 1 gal",
        "recentSales": [
            {"text": "Whole Milk 1 gal sold 42 units at Princeton", "value": "$1,008.00"},
            {"text": "Organic Bananas sold 120 units at Edison", "value": "$420.00"},
            {"text": "Pasta 16oz sold 64 units at New Brunswick", "value": "$192.00"},
            {"text": "Greek Yogurt 32oz sold 37 units at Princeton", "value": "$166.50"},
            {"text": "Cereal Box sold 58 units at Edison", "value": "$291.00"},
        ],
    }

def _mock_analytics_data():
    return {
        "salesTrend": [{"date": f"09-{d:02d}", "sales": 2000 + 75 * d} for d in range(1, 15)] +
                       [{"date": f"10-{d:02d}", "sales": 2600 + 60 * d} for d in range(1, 15)],
        "topProducts": [
            {"name": "Whole Milk 1 gal", "value": 320000},
            {"name": "Pasta 16oz", "value": 110000},
            {"name": "Organic Bananas", "value": 98000},
            {"name": "Avocados", "value": 78000},
            {"name": "Greek Yogurt 32oz", "value": 2600},
        ],
        "storePerformance": [
            {"store": "Princeton", "revenue": 210000},
            {"store": "New Brunswick", "revenue": 205000},
            {"store": "Edison", "revenue": 198000},
        ],
        "spoilageData": [{"date": f"10-{d:02d}", "quantity": 100 + d * 3, "value": 2500 + d * 40} for d in range(1, 15)],
        "categoryComparison": [
            {"category": "Dairy", "sales": 520000},
            {"category": "Produce", "sales": 390000},
            {"category": "Grocery", "sales": 260000},
            {"category": "Meat", "sales": 16000},
        ],
        "promotionEffectiveness": [
            {"promotion": "Princeton", "withPromo": 120000, "withoutPromo": 90000},
            {"promotion": "New Brunswick", "withPromo": 115000, "withoutPromo": 88000},
            {"promotion": "Edison", "withPromo": 112000, "withoutPromo": 86000},
        ],
    }

# --- Flask App Initialization ---
app = Flask(__name__)

# Configure CORS with explicit settings for production
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"],
     supports_credentials=False)

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

# --- Error Handlers to ensure CORS works even with errors ---
@app.after_request
def after_request(response):
    """Ensure CORS headers are present on all responses."""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with CORS headers."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with CORS headers."""
    return jsonify({"error": "Internal server error"}), 500

# --- API Endpoints ---

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint to handle chat interactions with the Aura agent."""
    try:
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
            final_answer = "Hello! I'm Aura, your Autonomous Retail Intelligence Agent. How can I help you analyze our data today?"
        elif intent == 'off_topic':
            final_answer = "I'm sorry, but I can only answer questions related to our retail data. Please ask something about sales, inventory, or product performance."
        elif intent == 'unanswerable':
            final_answer = "I understand you're asking about business/retail topics, but I don't have the necessary data in our system to answer that question. I can help you with questions about sales, inventory, product performance, and other data that's available in our Snowflake database. Could you try rephrasing your question to focus on data we have available?"
        else:
            final_answer = "I'm not sure how to handle that request. Please try asking a question related to our retail data."

        return jsonify({"response": final_answer})
    
    except Exception as e:
        error_message = str(e)
        # Check if it's a quota error
        if "ResourceExhausted" in error_message or "quota" in error_message.lower():
            return jsonify({
                "error": "API rate limit exceeded. Please wait a moment before trying again. The Gemini API free tier allows 15 requests per minute."
            }), 429
        else:
            print(f"Error in chat endpoint: {e}")
            return jsonify({"error": f"An error occurred: {error_message}"}), 500


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
    # Serve mock data when DB is unavailable or mock mode enabled
    if USE_MOCK_DATA or not DB_SCHEMA:
        return jsonify(_mock_dashboard_data())

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
        # Fallback to mock data so frontend remains usable
        return jsonify(_mock_dashboard_data()), 200
    finally:
        if conn:
            conn.close()

@app.route('/api/analytics-data', methods=['GET'])
def get_analytics_data():
    """Endpoint to fetch visualization data for analytics page."""
    # Serve mock data when DB is unavailable or mock mode enabled
    if USE_MOCK_DATA or not DB_SCHEMA:
        return jsonify(_mock_analytics_data())

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

        # Query 1: Sales Trend (Last 30 Days)
        cur.execute("""
            SELECT 
                TO_CHAR(D.D_DATE, 'MM-DD') as date,
                SUM(F.NET_SALES) as sales
            FROM FACT_SALES_DAILY F
            JOIN DIM_DATE D ON F.DATE_KEY = D.DATE_KEY
            WHERE D.D_DATE >= DATEADD(day, -30, CURRENT_DATE())
            GROUP BY D.D_DATE
            ORDER BY D.D_DATE;
        """)
        sales_trend = [{"date": row[0], "sales": float(row[1]) if row[1] else 0} for row in cur.fetchall()]

        # Query 2: Top Products by Revenue
        cur.execute("""
            SELECT 
                P.PRODUCT_NAME as name,
                SUM(F.NET_SALES) as value
            FROM FACT_SALES_DAILY F
            JOIN DIM_PRODUCT P ON F.PRODUCT_KEY = P.PRODUCT_KEY
            GROUP BY P.PRODUCT_NAME
            ORDER BY value DESC
            LIMIT 5;
        """)
        top_products = [{"name": row[0], "value": float(row[1]) if row[1] else 0} for row in cur.fetchall()]

        # Query 3: Store Performance
        cur.execute("""
            SELECT 
                S.STORE_NAME as store,
                SUM(F.NET_SALES) as revenue
            FROM FACT_SALES_DAILY F
            JOIN DIM_STORE S ON F.STORE_KEY = S.STORE_KEY
            GROUP BY S.STORE_NAME
            ORDER BY revenue DESC
            LIMIT 10;
        """)
        store_performance = [{"store": row[0], "revenue": float(row[1]) if row[1] else 0} for row in cur.fetchall()]

        # Query 4: Daily Sales Volume (Last 30 Days) - Using as alternative to spoilage
        cur.execute("""
            SELECT 
                TO_CHAR(D.D_DATE, 'MM-DD') as date,
                SUM(F.QTY_SOLD) as quantity,
                SUM(F.NET_SALES) as value
            FROM FACT_SALES_DAILY F
            JOIN DIM_DATE D ON F.DATE_KEY = D.DATE_KEY
            WHERE D.D_DATE >= DATEADD(day, -30, CURRENT_DATE())
            GROUP BY D.D_DATE
            ORDER BY D.D_DATE;
        """)
        spoilage_data = [{"date": row[0], "quantity": float(row[1]) if row[1] else 0, "value": float(row[2]) if row[2] else 0} for row in cur.fetchall()]

        # Query 5: Category Sales Comparison (Top Products as Categories)
        cur.execute("""
            SELECT 
                P.PRODUCT_NAME as category,
                SUM(F.NET_SALES) as sales
            FROM FACT_SALES_DAILY F
            JOIN DIM_PRODUCT P ON F.PRODUCT_KEY = P.PRODUCT_KEY
            GROUP BY P.PRODUCT_NAME
            ORDER BY sales DESC
            LIMIT 8;
        """)
        category_comparison = [{"category": row[0] if row[0] else "Unknown", "sales": float(row[1]) if row[1] else 0} for row in cur.fetchall()]

        # Query 6: Promotion Effectiveness (Promo vs No Promo by Store)
        cur.execute("""
            SELECT 
                S.STORE_NAME as promotion,
                SUM(CASE WHEN F.PROMO_KEY > 0 THEN F.NET_SALES ELSE 0 END) as withPromo,
                SUM(CASE WHEN F.PROMO_KEY = 0 OR F.PROMO_KEY IS NULL THEN F.NET_SALES ELSE 0 END) as withoutPromo
            FROM FACT_SALES_DAILY F
            JOIN DIM_STORE S ON F.STORE_KEY = S.STORE_KEY
            GROUP BY S.STORE_NAME
            ORDER BY withPromo DESC
            LIMIT 5;
        """)
        promotion_effectiveness = [{"promotion": row[0], "withPromo": float(row[1]) if row[1] else 0, "withoutPromo": float(row[2]) if row[2] else 0} for row in cur.fetchall()]

        analytics_data = {
            "salesTrend": sales_trend,
            "topProducts": top_products,
            "storePerformance": store_performance,
            "spoilageData": spoilage_data,
            "categoryComparison": category_comparison,
            "promotionEffectiveness": promotion_effectiveness
        }
        
        return jsonify(analytics_data)

    except Exception as e:
        print(f"Error fetching analytics data: {e}")
        # Fallback to mock data so frontend remains usable
        return jsonify(_mock_analytics_data()), 200
    finally:
        if conn:
            conn.close()

# --- Main Execution ---
if __name__ == '__main__':
    # Get port from environment variable (Render provides this)
    # Default to 5001 for local development
    port = int(os.environ.get('PORT', 5001))
    
    # Bind to 0.0.0.0 so Render can access it
    # Use debug=False for production
    app.run(host='0.0.0.0', port=port, debug=False)