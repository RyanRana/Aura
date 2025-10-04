import snowflake.connector

# Replace with your actual credentials
conn = snowflake.connector.connect(
    user="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    account="YOUR_ACCOUNT_IDENTIFIER",
    warehouse="YOUR_WAREHOUSE_NAME",
    database="YOUR_DATABASE_NAME",
    schema="YOUR_SCHEMA_NAME"
)

# You are now connected!
# Create a cursor object to execute queries.
cur = conn.cursor()

try:
    # Example: Execute a query
    cur.execute("SELECT CURRENT_VERSION()")
    one_row = cur.fetchone()
    print(f"Snowflake version: {one_row[0]}")
finally:
    # Close the cursor and connection
    cur.close()
    conn.close()