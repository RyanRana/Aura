import os
import snowflake.connector
from dotenv import load_dotenv

def get_schema_for_agent():
    """
    Connects to Snowflake, retrieves the database schema, and returns it as a
    formatted string. Returns None if an error occurs.
    """
    load_dotenv()
    conn = None
    try:
        # Establish the connection
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        cur = conn.cursor()
        
        # SQL query to get all table, column, and data type info
        query = f"""
        SELECT table_name, column_name, data_type
        FROM {os.getenv("SNOWFLAKE_DATABASE")}.INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = '{os.getenv("SNOWFLAKE_SCHEMA")}'
        ORDER BY table_name, ordinal_position;
        """
        cur.execute(query)

        # A dictionary to hold the schema information
        schema_info = {}
        for table, column, dtype in cur.fetchall():
            if table not in schema_info:
                schema_info[table] = []
            schema_info[table].append(f"{column} ({dtype})")
            
        # Format the schema into a single string for the agent
        formatted_schema = ""
        for table_name, columns in schema_info.items():
            formatted_schema += f"Table: {table_name}\n"
            formatted_schema += "Columns: " + ", ".join(columns) + "\n\n"
            
        return formatted_schema.strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        return None # Return None to indicate failure

    finally:
        # Ensure the connection is always closed
        if conn:
            conn.close()

# This block demonstrates how to call the function and use its return value.
# It only runs when you execute this script directly.
if __name__ == "__main__":
    print("Retrieving database schema...")
    
    # Call the function and store the result in a variable
    db_schema_context = get_schema_for_agent()
    
    if db_schema_context:
        print("\n✅ Schema retrieved successfully!")
        print("This string is now ready to be used as context for Gemini:")
        print("\n--- START OF SCHEMA CONTEXT ---")
        print(db_schema_context)
        print("--- END OF SCHEMA CONTEXT ---")
        
        # In your final application, you would pass 'db_schema_context'
        # to your Gemini API call, like so:
        # response = model.generate_content(f"Database schema: {db_schema_context}\n\nUser question: ...")
    else:
        print("\n❌ Failed to retrieve the schema.")