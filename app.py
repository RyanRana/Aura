import os
import google.generativeai as genai
import snowflake.connector
from dotenv import load_dotenv
from database_connector import get_schema_for_agent

# --- Reusable Tools for the Agent ---

def execute_snowflake_query(sql_query: str):
    """A tool to execute a SQL query on Snowflake and return results."""
    # ... (code is unchanged from previous version)
    load_dotenv()
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
        cur.execute(sql_query)
        columns = [desc[0] for desc in cur.description]
        results = cur.fetchall()
        
        # Format results for easy use by the agent
        if not results:
            return "Query returned no results."
        
        formatted_results = " | ".join(columns) + "\n"
        for row in results:
            formatted_results += " | ".join(map(str, row)) + "\n"
        return formatted_results

    except Exception as e:
        print(f"Error executing query: {e}")
        return f"Error: Could not execute query. {e}"
    finally:
        if conn:
            conn.close()

def text_to_sql_tool(question: str, db_schema: str, chat_history: list):
    """A tool that takes a natural language question and returns structured data from the database."""
    print(f"\n[Tool Activated: Text-to-SQL] Answering sub-question: '{question}'")
    
    # Step 1: Generate SQL from the sub-question
    sql_query = generate_sql_query(question, db_schema, chat_history)
    if not sql_query:
        return "Error: Could not generate a valid SQL query."
    print(f"Generated SQL:\n{sql_query}\n")

    # Step 2: Execute the query
    results = execute_snowflake_query(sql_query)
    return results

# --- Core Gemini Functions (Prompts) ---

def generate_sql_query(user_question: str, db_schema: str, chat_history: list):
    """Uses Gemini to generate a SQL query from a user question."""
    # ... (code is unchanged from previous version)
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    formatted_history = format_chat_history(chat_history)

    prompt = f"""
    You are an expert Snowflake SQL data analyst. Your task is to write a single, valid Snowflake SQL query.
    Use the conversation history to understand context for follow-up questions. For example, if the user asks "what about last week?", refer to the previous question to understand what data they are asking for.

    **Database Schema:**
    ---
    {db_schema}
    ---

    **Previous Conversation:**
    ---
    {formatted_history if formatted_history else "No previous conversation."}
    ---

    **User Question:**
    "{user_question}"

    **SQL Query:**
    """
    try:
        response = model.generate_content(prompt)
        sql_query = response.text.strip()
        if sql_query.lower().startswith("```sql"):
            sql_query = sql_query[5:-3].strip()
        return sql_query
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

def format_chat_history(chat_history: list):
    """Helper to format chat history for the prompt."""
    if not chat_history:
        return ""
    return "\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in chat_history])
    
# --- The Main Agent "Brain" ---

def run_agentic_flow(user_question: str, db_schema: str, chat_history: list):
    """
    The main agentic loop that thinks, acts, and synthesizes an answer.
    """
    print("\n[Aria's Brain] Starting new investigation...")
    
    # THOUGHT: The agent thinks about how to answer the high-level question.
    # It formulates a plan and identifies the data it needs.
    print("[Aria's Brain] Step 1: Formulating an analysis plan...")
    
    plan_prompt = f"""
    You are Aria, an Autonomous Retail Intelligence Agent. Your goal is to perform a root cause analysis.
    A manager has asked: "{user_question}"
    
    Based on the database schema, create a step-by-step plan to investigate this.
    For each step, state the specific question you need to answer.
    
    Example Plan:
    1. Check the sales figures for the specified product and time frame.
    2. Analyze the inventory levels to check for stockouts.
    3. Examine the spoilage data to see if waste was a factor.
    
    Your plan should be concise and logical.

    **Database Schema:**
    ---
    {db_schema}
    ---
    
    **Analysis Plan:**
    """
    
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    plan_response = model.generate_content(plan_prompt)
    analysis_plan = plan_response.text
    print(f"Analysis Plan:\n{analysis_plan}")
    
    # ACTION & OBSERVATION: The agent executes the plan, step by step.
    print("\n[Aria's Brain] Step 2: Executing plan and gathering data...")
    
    observations = ""
    sub_questions = [line.split('. ')[1] for line in analysis_plan.strip().split('\n') if '. ' in line]
    
    for i, sub_q in enumerate(sub_questions, 1):
        # The agent uses its tool to get data for each step of the plan.
        observation = text_to_sql_tool(sub_q, db_schema, chat_history)
        observations += f"Observation {i} (from question '{sub_q}'):\n{observation}\n\n"
        
    print(f"--- All Data Gathered ---\n{observations}")

    # FINAL SYNTHESIS: The agent combines all its observations into a final answer.
    print("[Aria's Brain] Step 3: Synthesizing final recommendation...")
    
    synthesis_prompt = f"""
    You are Aria, an Autonomous Retail Intelligence Agent. You have completed your investigation into the manager's question: "{user_question}"
    
    You executed a plan and gathered the following data:
    ---
    {observations}
    ---
    
    Based on all of these observations, provide a final, comprehensive answer.
    Start with a direct answer to the question.
    Then, provide a brief summary of the key findings from your investigation.
    Finally, if applicable, suggest a recommended next step or action for the manager.
    Your tone should be professional, data-driven, and helpful.
    """
    
    final_answer_response = model.generate_content(synthesis_prompt)
    return final_answer_response.text.strip()


def main():
    """Main function to run the interactive console."""
    print("Fetching database schema once for the session...")
    db_schema = get_schema_for_agent()
    if not db_schema:
        print("Fatal: Could not retrieve database schema. Exiting.")
        return
    print("Schema loaded. Aria is ready.\n")
    
    chat_history = []

    while True:
        user_question = input("Ask Aria a high-level question (or type 'exit' to quit): ")
        if user_question.lower() in ['exit', 'quit']:
            print("Shutting down Aria. Goodbye!")
            break
        if not user_question:
            continue
            
        # The main loop now calls the new agentic flow
        final_answer = run_agentic_flow(user_question, db_schema, chat_history)
        
        print("\n💡 Aria's Final Answer:")
        print(final_answer)
        print("-" * 20 + "\n")
        
        chat_history.append({"role": "user", "content": user_question})
        chat_history.append({"role": "assistant", "content": final_answer})

if __name__ == "__main__":
    main()


