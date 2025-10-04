import streamlit as st
import snowflake.connector
import os
import pandas as pd
from dotenv import load_dotenv

from langchain.agents import tool, AgentExecutor, create_react_agent
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Page Configuration ---
st.set_page_config(
    page_title="Aria: Retail Intelligence Partner",
    page_icon="🤝",
    layout="centered"
)

# --- Environment and API Key Setup ---
load_dotenv()

# Check for Google API Key
if "GOOGLE_API_KEY" not in os.environ:
    st.error("🚨 Google API Key not found. Please set it in your .env file.")
    st.stop()

# --- Snowflake Connection ---
@st.cache_resource
def get_snowflake_connection():
    """Establishes a connection to Snowflake."""
    try:
        conn = snowflake.connector.connect(
            user=os.environ["SNOWFLAKE_USER"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
            database=os.environ["SNOWFLAKE_DATABASE"],
            schema=os.environ["SNOWFLAKE_SCHEMA"]
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {e}")
        return None

conn = get_snowflake_connection()


# --- Agent Tools ---

# Tier 1: Core Operational Tools
@tool
def get_sales_performance(product_name: str, store_location: str) -> str:
    """
    Returns sales performance (units sold, revenue) for a product and store over the last 7 days.
    """
    if not conn: return "Snowflake connection not available."
    query = f"""
        SELECT SALE_DATE, UNITS_SOLD, REVENUE FROM SALES
        WHERE PRODUCT_NAME = '{product_name}' AND STORE_LOCATION = '{store_location}'
        AND SALE_DATE >= CURRENT_DATE() - 7 ORDER BY SALE_DATE;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        df = cursor.fetch_pandas_all()
        cursor.close()
        return f"Sales data for {product_name} in {store_location}:\n{df.to_string()}" if not df.empty else f"No sales data found for {product_name} in {store_location} for the last 7 days."
    except Exception as e:
        return f"Error fetching sales data: {e}"


@tool
def get_inventory_levels(product_name: str, store_location: str) -> str:
    """
    Returns current inventory and last restock date for a product at a specific store.
    """
    if not conn: return "Snowflake connection not available."
    query = f"""
        SELECT STOCK_ON_HAND, LAST_RESTOCK_DATE FROM INVENTORY
        WHERE PRODUCT_NAME = '{product_name}' AND STORE_LOCATION = '{store_location}';
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        df = cursor.fetch_pandas_all()
        cursor.close()
        return f"Inventory data for {product_name} in {store_location}:\n{df.to_string()}" if not df.empty else f"No inventory data found for {product_name} in {store_location}."
    except Exception as e:
        return f"Error fetching inventory data: {e}"

# Tier 2: Strategic & Profitability Tools
@tool
def get_product_profitability(product_name: str, store_location: str) -> str:
    """
    Calculates the profit margin for a specific product over the last 7 days.
    Use this to determine if a product is actually making money, not just selling well.
    """
    if not conn: return "Snowflake connection not available."
    query = f"""
        SELECT
            SUM(s.REVENUE) as total_revenue,
            SUM(s.UNITS_SOLD * p.COST_OF_GOODS) as total_cost,
            (total_revenue - total_cost) as total_profit,
            (total_profit / total_revenue) * 100 as profit_margin_percent
        FROM SALES s
        JOIN PRODUCTS p ON s.PRODUCT_NAME = p.PRODUCT_NAME
        WHERE s.PRODUCT_NAME = '{product_name}' AND s.STORE_LOCATION = '{store_location}'
        AND s.SALE_DATE >= CURRENT_DATE() - 7;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        df = cursor.fetch_pandas_all()
        cursor.close()
        if df.empty or df['TOTAL_REVENUE'][0] is None:
            return f"Not enough data to calculate profitability for {product_name} in {store_location}."
        return f"Profitability for {product_name} in {store_location} (last 7 days):\n{df.to_string()}"
    except Exception as e:
        return f"Error calculating profitability: {e}"


@tool
def check_promotion_impact(product_name: str, store_location: str) -> str:
    """
    Analyzes a promotion's impact by comparing sales during the promotion to the period before.
    """
    if not conn: return "Snowflake connection not available."
    try:
        cursor = conn.cursor()
        promo_query = f"SELECT START_DATE, END_DATE FROM PROMOTIONS WHERE PRODUCT_NAME = '{product_name}' AND STORE_LOCATION = '{store_location}';"
        cursor.execute(promo_query)
        promo_result = cursor.fetchone()
        if not promo_result: return f"No promotion found for {product_name} in {store_location}."
        
        start_date, end_date = promo_result
        
        promo_sales_query = f"SELECT AVG(UNITS_SOLD) as avg_units_sold FROM SALES WHERE PRODUCT_NAME = '{product_name}' AND STORE_LOCATION = '{store_location}' AND SALE_DATE BETWEEN '{start_date}' AND '{end_date}';"
        cursor.execute(promo_sales_query)
        promo_sales = cursor.fetchone()[0] or 0

        before_sales_query = f"SELECT AVG(UNITS_SOLD) as avg_units_sold FROM SALES WHERE PRODUCT_NAME = '{product_name}' AND STORE_LOCATION = '{store_location}' AND SALE_DATE BETWEEN '{start_date - pd.Timedelta(days=7)}' AND '{start_date - pd.Timedelta(days=1)}';"
        cursor.execute(before_sales_query)
        before_sales = cursor.fetchone()[0] or 0
        
        cursor.close()
        lift = ((promo_sales - before_sales) / before_sales) * 100 if before_sales > 0 else float('inf') if promo_sales > 0 else 0
        
        return (f"Promotion analysis for {product_name} in {store_location}:\n"
                f"- Average daily units sold before promotion: {before_sales:.2f}\n"
                f"- Average daily units sold during promotion: {promo_sales:.2f}\n"
                f"- Sales lift: {lift:.2f}%")
    except Exception as e:
        return f"Error analyzing promotion impact: {e}"

# Tier 3: Proactive & Action-Oriented Tools
@tool
def forecast_product_demand(product_name: str, store_location: str) -> str:
    """
    Provides a simple sales forecast for the next 5 days based on the last 14 days of sales data.
    """
    if not conn: return "Snowflake connection not available."
    query = f"""
        SELECT AVG(UNITS_SOLD) as avg_daily_sales FROM SALES
        WHERE PRODUCT_NAME = '{product_name}' AND STORE_LOCATION = '{store_location}' AND SALE_DATE >= CURRENT_DATE() - 14;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        avg_sales = cursor.fetchone()[0]
        cursor.close()
        if avg_sales is None: return f"Not enough historical data to forecast for {product_name}."
        
        forecast = [round(avg_sales * (1 + (i * 0.05))) for i in range(5)]
        
        return (f"5-Day demand forecast for {product_name} in {store_location}:\n" +
                "\n".join([f"- Day {i+1}: {val} units" for i, val in enumerate(forecast)]))
    except Exception as e:
        return f"Error forecasting demand: {e}"

@tool
def draft_inventory_order(product_name: str, store_location: str) -> str:
    """
    Drafts a suggested inventory order based on the sales forecast and current inventory levels.
    Use this as a final step to prevent future stockouts.
    """
    # This is a 'meta-tool' - it uses the output of other tools.
    # The agent will learn to call the prerequisite tools first.
    inventory_str = get_inventory_levels(product_name, store_location)
    forecast_str = forecast_product_demand(product_name, store_location)

    try:
        # Simple parsing for the hackathon
        stock_on_hand = int(inventory_str.split("STOCK_ON_HAND")[1].split("\n")[1].strip())
        forecasted_demand_5_days = sum([int(line.split(":")[1].strip().split(" ")[0]) for line in forecast_str.split("\n")[1:]])
        
        # Maintain a 3-day safety stock
        avg_daily_demand = forecasted_demand_5_days / 5
        safety_stock = round(avg_daily_demand * 3)
        
        order_amount = max(0, round(forecasted_demand_5_days + safety_stock - stock_on_hand))
        
        return (f"Inventory Order Draft for {product_name} at {store_location}:\n"
                f"- 5-Day Forecasted Demand: {forecasted_demand_5_days} units\n"
                f"- Current Stock: {stock_on_hand} units\n"
                f"- Recommended Safety Stock (3 days): {safety_stock} units\n"
                f"--------------------------------------------------\n"
                f"**Suggested Order Amount: {order_amount} units**")

    except Exception as e:
        return f"Could not draft order. Prerequisite data might be missing. Error: {e}. Inventory: [{inventory_str}], Forecast: [{forecast_str}]"


# --- Agent Initialization ---
SYSTEM_PROMPT = """
You are "Aria," an expert retail supply chain analyst and strategic partner for a Wakefern store manager.
Your goal is to not just answer questions, but to identify root causes, analyze profitability, forecast future needs,
and help the manager take concrete actions.

When a user asks a question:
1.  **Deconstruct the Problem:** Think step-by-step about what business metrics are relevant (e.g., sales, inventory, profit, promotions).
2.  **Select Your Tools:** Choose the appropriate tools to gather evidence from Snowflake. You can use multiple tools in sequence to build a complete picture.
3.  **Synthesize Findings:** Connect the dots between the data points. Do not just report the data; explain what it means in a business context.
4.  **Formulate a Recommendation:** Conclude with a clear, concise recommendation. If the user's query implies an action (like ordering), provide the necessary information. Start your final answer with "**Recommendation:**"
"""

@st.cache_resource
def get_agent():
    """Initializes and returns the LangChain agent."""
    tools = [
        get_sales_performance,
        get_inventory_levels,
        get_product_profitability,
        check_promotion_impact,
        forecast_product_demand,
        draft_inventory_order
    ]
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
    prompt = hub.pull("hwchase17/react")
    prompt.template = SYSTEM_PROMPT + prompt.template
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- Streamlit UI ---
st.image("https://i.imgur.com/v8Lg4Vj.png", width=150)
st.title("Aria: Your Retail Intelligence Partner")
st.markdown("Ask a strategic question, and Aria will provide a data-driven plan.")

st.markdown("""
**Example Questions:**
- *The BOGO avocado promotion in Edison sold well, but was it actually profitable?*
- *We had a stockout on bananas in New Brunswick. Draft an order to prevent this from happening again.*
- *Why are we losing money on avocados this week at the Edison store?*
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Aria your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Aria is investigating..."):
            agent = get_agent()
            try:
                response = agent.invoke({"input": prompt})
                output = response['output']
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

