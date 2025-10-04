import snowflake.connector
from dotenv import load_dotenv 
import os 

load_dotenv()
#gets the data from the env
try:
    conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
    print("Connection to Snowflake successful!")
    
    # You can now use the 'conn' object to run queries
    # For example:
    # cur = conn.cursor()
    # cur.execute("SELECT CURRENT_VERSION()")
    # one_row = cur.fetchone()
    # print(one_row[0])

except Exception as e:
    print(f"Error connecting to Snowflake: {e}")
# You are now connected!
# Create a cursor object to execute queries.
cur = conn.cursor()

try:
    # Query the first 100 rows from each fact table
    tables = ["FACT_SALES_DAILY", "FACT_INVENTORY_DAILY", "FACT_SPOILAGE_DAILY"]
    
    for table_name in tables:
        print(f"\n=== First 100 rows from {table_name} ===")
        cur.execute(f"SELECT * FROM ARIA.MART.{table_name} LIMIT 100")
        rows = cur.fetchall()
        
        if rows:
            # Get column names
            columns = [desc[0] for desc in cur.description]
            print(f"Columns: {', '.join(columns)}")
            print(f"Number of rows returned: {len(rows)}")
            print("\nData:")
            for i, row in enumerate(rows, 1):
                print(f"Row {i}: {row}")
        else:
            print("No data found in this table.")
finally:
    # Close the cursor and connection
    cur.close()
    conn.close()