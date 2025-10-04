import snowflake.connector

# Replace with your actual credentials
conn = snowflake.connector.connect(
    user="MATTDSPECHT",
    password="Chrwx2007#extra",
    account="IROUKNG-OG97168",
    warehouse="SNOWFLAKE_LEARNING_WH",
    database="SNOWFLAKE_LEARNING_DB",
    schema="MATTDSPECHT_LOAD_SAMPLE_DATA_FROM_S3"
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