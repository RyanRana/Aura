import snowflake.connector

# Replace with your actual credentials
conn = snowflake.connector.connect(
    user="MATTDSPECHT",
    password="Chrwx2007#extra",
    account="IROUKNG-OG97168",
    warehouse="ARIA_WH",
    database="ARIA",
    schema="MART"
)

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