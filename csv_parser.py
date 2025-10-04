import os
import json
import pandas as pd
import google.generativeai as genai
import snowflake.connector
from dotenv import load_dotenv

# --- Database Functions (Self-contained) ---

def get_all_table_schemas(schema_name: str):
    """
    Connects to Snowflake and retrieves the schema for ALL tables in a given schema.
    This is used by the AI to determine the best destination table.
    """
    load_dotenv()
    conn = None
    all_schemas = {}
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"), password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"), warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"), schema=schema_name
        )
        cur = conn.cursor()
        query = f"""
        SELECT table_name, column_name, data_type
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{schema_name.upper()}'
        ORDER BY table_name, ORDINAL_POSITION;
        """
        cur.execute(query)
        for table, column, dtype in cur.fetchall():
            if table not in all_schemas:
                all_schemas[table] = {}
            all_schemas[table][column] = dtype
        
        if not all_schemas:
            return None, f"Could not find any tables in schema '{schema_name}'."
        return all_schemas, None
    except Exception as e:
        return None, f"Error fetching all Snowflake schemas: {e}"
    finally:
        if conn:
            conn.close()

# --- AI-Powered Mapping Function ---

def get_ai_upload_plan(csv_cols: list, all_db_schemas: dict):
    """
    Uses Gemini to suggest the best target table and create a column mapping.
    """
    print("   - Asking AI to analyze CSV and suggest an upload plan...")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    schemas_str = ""
    for table, cols in all_db_schemas.items():
        schemas_str += f"Table `{table}`:\n"
        for col, dtype in cols.items():
            schemas_str += f"- {col} ({dtype})\n"
        schemas_str += "\n"

    prompt = f"""
    You are an intelligent data pipeline expert. A user wants to upload a CSV.
    Based on the CSV's column names, determine the most logical destination table from the available Snowflake schemas and create a column mapping.

    **Instructions:**
    1.  **Suggest Table:** Identify the single best Snowflake table for this data.
    2.  **Map Columns:** Map each CSV column to the most logical column in the suggested table. If a CSV column has no logical match, map it to `null`.
    3.  **Return JSON:** Your output MUST be a JSON object with two keys: "suggested_table" and "column_mapping".

    **Available Snowflake Schemas:**
    ---
    {schemas_str}
    ---

    **CSV Columns:**
    ---
    {', '.join(csv_cols)}
    ---

    **JSON Response:**
    """
    try:
        response = model.generate_content(prompt)
        json_response_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_response_text), None
    except Exception as e:
        return None, f"Failed to get a valid plan from the AI model: {e}"

# --- Smart Upload Function ---

def smart_upload_csv(file_path: str, table_name: str, schema_name: str, column_mapping: dict):
    """
    Uploads a CSV to a Snowflake table using a provided column map.
    """
    print(f"\nAttempting smart upload for '{file_path}' to table '{table_name}'...")
    load_dotenv()
    conn = None
    try:
        csv_cols = pd.read_csv(file_path, nrows=0).columns.tolist()
        
        # Filter map for only valid, non-null mappings
        valid_mapping = {
            csv_col: snow_col for csv_col, snow_col in column_mapping.items()
            if csv_col in csv_cols and snow_col is not None
        }

        if not valid_mapping:
            return False, "AI mapping resulted in no common columns. Cannot upload."

        print(f"   - Applying AI-generated mapping for columns: {', '.join(valid_mapping.keys())}")

        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"), password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"), warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"), schema=schema_name
        )
        cur = conn.cursor()

        stage_name = "temp_csv_stage"
        cur.execute(f"CREATE OR REPLACE TEMPORARY STAGE {stage_name}")
        put_command = f"PUT file://{os.path.abspath(file_path)} @{stage_name}"
        cur.execute(put_command)

        # Dynamically build the COPY INTO command from the AI map
        target_cols_str = ", ".join(f'"{col}"' for col in valid_mapping.values())
        source_cols_str = ", ".join(f't.${csv_cols.index(col) + 1}' for col in valid_mapping.keys())
        
        copy_command = f"""
        COPY INTO {table_name} ({target_cols_str})
        FROM (SELECT {source_cols_str} FROM @{stage_name} t)
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 EMPTY_FIELD_AS_NULL = TRUE)
        ON_ERROR = 'CONTINUE';
        """
        
        print("   - Executing smart COPY INTO command...")
        cur.execute(copy_command)
        
        print(f"✅ Successfully loaded matching data into '{table_name}'.")
        return True, None

    except Exception as e:
        error_message = f"❌ Failed to upload data to Snowflake: {e}"
        print(error_message)
        return False, error_message
    finally:
        if conn:
            conn.close()


# --- Tester Block ---
if __name__ == "__main__":
    # --- CONFIGURATION ---
    test_csv_file = "tester.csv"
    target_schema_name = "MART_2"
    
    # --- EXECUTION ---
    print("="*50)
    print("RUNNING AI-POWERED CSV UPLOADER IN TEST MODE")
    print("="*50)

    if not os.path.exists(test_csv_file):
        print(f"FATAL: Test file '{test_csv_file}' not found. Exiting.")
    else:
        # Step 1: Get all table schemas for context
        all_schemas, err = get_all_table_schemas(target_schema_name)
        if err:
            print(f"FATAL: {err}")
        else:
            # Step 2: Get AI suggestion for table and mapping
            csv_columns = pd.read_csv(test_csv_file, nrows=0).columns.tolist()
            upload_plan, err = get_ai_upload_plan(csv_columns, all_schemas)

            if err:
                print(f"FATAL: {err}")
            else:
                # Step 3: Present the plan to the user for confirmation
                print("\n--- AI Upload Plan ---")
                print(f"Suggested Table: {upload_plan.get('suggested_table')}")
                print("Column Mapping:")
                print(json.dumps(upload_plan.get('column_mapping'), indent=2))
                print("----------------------\n")

                confirm = input("Do you want to proceed with this upload plan? (y/n): ")
                if confirm.lower() == 'y':
                    # Step 4: Execute the smart upload with the AI's plan
                    suggested_table = upload_plan.get('suggested_table')
                    mapping = upload_plan.get('column_mapping')
                    
                    if suggested_table and mapping:
                        success, message = smart_upload_csv(
                            test_csv_file, 
                            suggested_table, 
                            target_schema_name, 
                            mapping
                        )
                        if not success:
                            print(f"Upload failed. Reason: {message}")
                    else:
                        print("Upload aborted: AI plan was incomplete.")
                else:
                    print("Upload aborted by user.")

