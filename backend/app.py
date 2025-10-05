import os
import json
import time
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
    
    sql_query = generate_sql_query(question, db_schema, chat_history)
    if not sql_query:
        return "Error: Could not generate a valid SQL query."
    print(f"Generated SQL:\n{sql_query}\n")

    results = execute_snowflake_query(sql_query)
    return results

# --- Core Gemini Functions (Prompts) ---

def generate_sql_query(user_question: str, db_schema: str, chat_history: list):
    """Uses Gemini to generate a SQL query from a user question."""
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    formatted_history = format_chat_history(chat_history)

    prompt = f"""
    You are an expert Snowflake SQL data analyst. Your task is to write a single, valid Snowflake SQL query.
    
    **CONTEXT AWARENESS:**
    Use the conversation history to understand context for follow-up questions. For example:
    - If the user asks "what about last week?" after asking about "this week", apply the same analysis to last week
    - If they ask "how about the other products?" after asking about a specific product, analyze all other products
    - If they ask "what's the trend?" after asking about sales, show the trend over time
    - Pronouns like "it", "that", "them" refer to the most recently discussed items

    **IMPORTANT DATABASE NOTES:**
    - The DIM_DATE table has duplicate DATE_KEY entries (each date appears 3 times)
    - Use DISTINCT when selecting DATE_KEY from DIM_DATE to avoid "Single-row subquery returns more than one row" errors
    - The data is from July 2025 to October 2025 (test data)
    - Use NET_SALES for revenue calculations (not GROSS_SALES)
    - Always use proper JOINs between tables

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

    Return ONLY the raw SQL query, without any markdown, explanation, or leading characters.
    **SQL Query:**
    """
    try:
        response = model.generate_content(prompt)
        sql_query = response.text.strip()
        if sql_query.lower().startswith("```sql"):
            sql_query = sql_query[5:-3].strip()
        if sql_query.startswith('l'):
            sql_query = sql_query[1:]
        return sql_query.lstrip()
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

def format_chat_history(chat_history: list):
    """Helper to format chat history for the prompt."""
    if not chat_history:
        return ""
    
    # Handle different message formats from frontend and console
    formatted_messages = []
    for msg in chat_history:
        if isinstance(msg, dict):
            # Frontend format: {'sender': 'user', 'text': '...', 'type': 'text'}
            if msg.get('type') == 'text':
                sender = 'User' if msg.get('sender') == 'user' else 'Assistant'
                text = msg.get('text', '')
                formatted_messages.append(f"{sender}: {text}")
        elif isinstance(msg, dict) and 'role' in msg:
            # Console format: {'role': 'user', 'content': '...'}
            sender = 'User' if msg.get('role') == 'user' else 'Assistant'
            text = msg.get('content', '')
            formatted_messages.append(f"{sender}: {text}")
    
    # Return last 6 messages (3 exchanges) to keep context manageable
    return "\n".join(formatted_messages[-6:])

# --- NEW: Intent Router ---

def route_user_question(user_question: str, db_schema: str):
    """
    Classifies the user's question to determine the correct action (intent).
    """
    print("\n[Aria's Router] Classifying user intent...")
    
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    router_prompt = f"""
    You are an intent classification agent. Your job is to determine the user's intent.
    The user is talking to Aria, an Autonomous Retail Intelligence Agent that answers questions by querying a Snowflake database.

    **Database Schema Context:**
    ---
    {db_schema}
    ---

    **User Question:**
    "{user_question}"

    **Instructions:**
    Analyze the user's question and classify it into one of the following categories:
    1. `greeting`: The user is saying hello, thank you, or other conversational pleasantries.
    2. `data_query`: The user is asking a question that can be answered using the provided database schema. This includes:
       - Direct questions about sales, products, inventory, revenue, transactions
       - Analytical questions like growth rates, trends, comparisons, performance metrics
       - Questions about underperforming products, best sellers, seasonal patterns
       - Any business question that can be derived from sales data, product data, or date information
    3. `off_topic`: The user is asking a question that is not a greeting and cannot be answered by the database schema (e.g., "what is the capital of France?", "tell me a joke", "what's the weather?", "how do I cook pasta?").
    4. `unanswerable`: The user is asking a question that requires external data not in the schema (e.g., questions about competitors, market trends, external benchmarks, future predictions, or data not available in the system).

    **IMPORTANT:** Be optimistic. If the question is about business/retail and could potentially be answered with sales data, product data, or date analysis, classify it as `data_query`. Only use `unanswerable` for questions that clearly require external data sources.

    Your response MUST be a JSON object with a single key "intent".

    **JSON Response:**
    """
    
    try:
        response = model.generate_content(router_prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        intent_data = json.loads(json_text)
        intent = intent_data.get("intent")
        print(f"Detected Intent: {intent}")
        return intent
    except Exception as e:
        print(f"Error routing intent: {e}. Defaulting to 'unanswerable'.")
        return "unanswerable"

# --- The Main Agent "Brain" ---

def run_agentic_flow(user_question: str, db_schema: str, chat_history: list):
    """
    The main agentic loop that thinks, acts, and synthesizes an answer.
    """
    print("\n[Aria's Brain] Starting new investigation...")
    start_time = time.time()
    MAX_EXECUTION_TIME = 60  # 60 seconds timeout
    
    print("[Aria's Brain] Step 1: Formulating an analysis plan...")
    
    formatted_history = format_chat_history(chat_history)
    
    plan_prompt = f"""
    You are Aria, an Autonomous Retail Intelligence Agent. Your goal is to perform a comprehensive analysis.
    A manager has asked: "{user_question}"
    
    **CONTEXT AWARENESS:**
    Consider the conversation history when creating your analysis plan. If this is a follow-up question, build upon previous analysis:
    - If they previously asked about a specific product, and now ask "what about the others?", plan to analyze all other products
    - If they asked about "this week" and now ask "last week", adapt the same analysis for last week
    - If they ask "what's the trend?" after sales questions, plan to show time-based trends
    
    Based on the database schema, create a step-by-step plan to investigate this.
    The plan should be a simple numbered list. Each item must be a single, clear question to be answered by querying the database.
    Do NOT include any markdown, rationale, or other descriptive text.

    **IMPORTANT DATABASE NOTES:**
    - The DIM_DATE table has duplicate DATE_KEY entries (each date appears 3 times)
    - Use DISTINCT when selecting DATE_KEY from DIM_DATE to avoid errors
    - The data is from July 2025 to October 2025 (test data)
    - Use NET_SALES for revenue calculations (not GROSS_SALES)
    - Keep queries simple and focused on one question at a time
    - For analytical questions (growth rates, trends, comparisons), break them into multiple steps
    - For performance questions, compare products/dates/periods systematically

    **Database Schema:**
    ---
    {db_schema}
    ---
    
    **Previous Conversation:**
    ---
    {formatted_history if formatted_history else "No previous conversation."}
    ---
    
    **Analysis Plan:**
    """
    
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    plan_response = model.generate_content(plan_prompt)
    analysis_plan = plan_response.text
    print(f"Analysis Plan:\n{analysis_plan}")
    
    print("\n[Aria's Brain] Step 2: Executing plan and gathering data...")
    
    observations = ""
    sub_questions = []
    failed_queries = 0
    max_failed_queries = 5  # Stop if too many queries fail
    
    for line in analysis_plan.strip().split('\n'):
        line = line.strip()
        parts = line.split('.', 1)
        if len(parts) == 2 and parts[0].isdigit():
            sub_questions.append(parts[1].strip())
    
    for i, sub_q in enumerate(sub_questions, 1):
        # Check timeout
        if time.time() - start_time > MAX_EXECUTION_TIME:
            print(f"[Aria's Brain] Timeout reached ({MAX_EXECUTION_TIME}s). Stopping execution.")
            break
            
        # Check if too many queries have failed
        if failed_queries >= max_failed_queries:
            print(f"[Aria's Brain] Too many failed queries ({failed_queries}). Stopping execution.")
            break
            
        observation = text_to_sql_tool(sub_q, db_schema, chat_history)
        
        # Check if query failed (be more lenient with "no results")
        if "Error:" in observation:
            failed_queries += 1
            print(f"[Aria's Brain] Query {i} failed with error. Failed count: {failed_queries}")
        elif "Query returned no results." in observation:
            # Don't count "no results" as a failure - it might be expected for some queries
            print(f"[Aria's Brain] Query {i} returned no results (not counted as failure)")
        else:
            failed_queries = 0  # Reset counter on successful query
            
        observations += f"Observation {i} (from question '{sub_q}'):\n{observation}\n\n"
        
    print(f"--- All Data Gathered ---\n{observations}")

    # Check if we have any meaningful data (be more lenient)
    if not observations.strip():
        return "I apologize, but I'm unable to find relevant data to answer your question. The question may be outside the scope of our available data, or there might be an issue with the data connection. Please try rephrasing your question or ask about sales, inventory, or product data that should be available in our system."
    elif failed_queries >= max_failed_queries:
        # Even if some queries failed, try to synthesize what we have
        print(f"[Aria's Brain] Some queries failed ({failed_queries}), but proceeding with available data...")

    print("[Aria's Brain] Step 3: Synthesizing final answer...")
    
    # --- MODIFIED PROMPT: User-friendly, concise responses with context ---
    synthesis_prompt = f"""
    You are Aria, an Autonomous Retail Intelligence Agent. You have completed your investigation into the manager's question: "{user_question}"
    
    **CONVERSATION CONTEXT:**
    Consider the conversation history to provide contextually appropriate responses:
    - If this is a follow-up question, acknowledge the connection to previous questions
    - If they're asking about "the others" or "other products", reference what was previously discussed
    - If they're asking for trends or comparisons, relate it to previous data points mentioned
    
    You executed a plan and gathered the following data:
    ---
    {observations}
    ---
    
    **Previous Conversation:**
    ---
    {formatted_history if formatted_history else "No previous conversation."}
    ---
    
    Provide a clear, direct answer to the user's question. Be concise and user-friendly.
    
    **IMPORTANT GUIDELINES:**
    - Start with a direct answer to their question
    - Keep it simple and conversational - avoid technical jargon
    - Don't explain your methodology, database queries, or technical process
    - Don't mention table names, column names, or SQL details
    - Don't explain how you calculated dates or found the data
    - Focus on the business insights, not the technical process
    - If there are interesting additional insights, mention them briefly
    - Maximum 2-3 sentences unless the question specifically asks for detailed analysis
    - If this is a follow-up question, briefly acknowledge the connection to previous discussion
    
    **Example of GOOD response:** "Your total revenue for last week was $1,402,427.01."
    **Example of BAD response:** "To determine this, I first identified the latest date in our date dimension as October 4, 2025. I then calculated the date one week prior..."
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
        user_question = input("Ask Aria a question (or type 'exit' to quit): ")
        if user_question.lower() in ['exit', 'quit']:
            print("Shutting down Aria. Goodbye!")
            break
        if not user_question:
            continue
            
        intent = route_user_question(user_question, db_schema)
        
        final_answer = ""
        
        if intent == 'data_query':
            final_answer = run_agentic_flow(user_question, db_schema, chat_history)
        elif intent == 'greeting':
            final_answer = "Hello! I'm Aria, your Autonomous Retail Intelligence Agent. How can I help you analyze our data today?"
        elif intent == 'off_topic':
            final_answer = "I'm sorry, but I can only answer questions related to our retail data in Snowflake, such as sales, inventory, and product performance."
        elif intent == 'unanswerable':
            final_answer = "I understand you're asking about business/retail topics, but I don't have the necessary data in our system to answer that question. I can help you with questions about sales, inventory, product performance, and other data that's available in our Snowflake database. Could you try rephrasing your question to focus on data we have available?"
        else:
            final_answer = "I'm not sure how to handle that request. Please try asking a question related to our retail data."

        print("\n💡 Aria's Final Answer:")
        print(final_answer)
        print("-" * 20 + "\n")
        
        chat_history.append({"role": "user", "content": user_question})
        chat_history.append({"role": "assistant", "content": final_answer})

if __name__ == "__main__":
    main()