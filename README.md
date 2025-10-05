```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ██╗   ██╗██████╗  █████╗     ██████╗ ███████╗████████╗ █████╗ ██╗██╗   ║
║    ██╔══██╗██║   ██║██╔══██╗██╔══██╗    ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║   ║
║    ███████║██║   ██║██████╔╝███████║    ██████╔╝█████╗     ██║   ███████║██║██║   ║
║    ██╔══██║██║   ██║██╔══██╗██╔══██║    ██╔══██╗██╔══╝     ██║   ██╔══██║██║██║   ║
║    ██║  ██║╚██████╔╝██║  ██║██║  ██║    ██║  ██║███████╗   ██║   ██║  ██║██║███████╗║
║    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝║
║                                                                               ║
║              🤖 Autonomous Retail Intelligence Agent 🤖                       ║
║                                                                               ║
║         AI-Powered Analytics | Agentic RAG | Real-Time Insights              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

# 🚀 Aura: Autonomous Retail Intelligence Agent

**Aura** is an AI-powered analytics platform designed to provide retail managers with immediate, data-driven insights. It features a conversational AI that can perform multi-step investigations into business questions by querying a Snowflake data warehouse, alongside a real-time analytics dashboard.

> 💡 **What makes Aura different?** Unlike traditional BI tools, Aura doesn't just answer questions—it **investigates** them. Ask "Why are sales down?" and watch it autonomously break down the problem, query multiple data sources, and synthesize actionable insights.

***

## 📸 Screenshots

**Dashboard View**
*Displays key performance indicators and recent sales activity pulled directly from Snowflake.*
![Aura Analytics Dashboard](https://storage.googleapis.com/gemini-prod/images/2237d11f-c0c5-4384-9547-074404731818)

**Chatbox View**
*Interact with the AI agent to ask complex questions or upload CSV files for analysis and ingestion.*
![Aura Conversational AI Chatbox](https://storage.googleapis.com/gemini-prod/images/5f0f353a-cbe1-4019-b636-f0464870f7d6)

***

## ✨ Features

* **Conversational AI Agent:** Ask complex, high-level questions (e.g., "Why are avocado sales down?") and receive synthesized, actionable answers.
* **Agentic RAG Workflow:** The AI autonomously creates and executes a multi-step plan to query the database, gather observations, and analyze the results.
* **Smart CSV Upload:** Attach a CSV file, and the AI will analyze its contents, suggest the correct database table and column mapping, and upload the data upon your confirmation.
* **Live Analytics Dashboard:** View key performance indicators (KPIs) and recent sales activity pulled in real-time from Snowflake.

### 🎯 Quick Stats

```
┌─────────────────────────────────────────────────────────────────┐
│  📊 AURA BY THE NUMBERS                                         │
├─────────────────────────────────────────────────────────────────┤
│  🤖 AI Models Used:        Google Gemini 2.5 Flash Lite         │
│  ❄️  Database:              Snowflake Cloud Data Warehouse      │
│  ⚛️  Frontend Framework:    React 19 + Vite + Material-UI       │
│  🐍 Backend Framework:      Flask + Python 3.12                 │
│  🔄 Workflow Type:          Autonomous Agentic RAG              │
│  📈 Max Sub-Queries:        20 per investigation                │
│  ⚡ Avg Response Time:      10-30 seconds                       │
│  🎨 UI Components:          Modern, responsive design           │
└─────────────────────────────────────────────────────────────────┘
```

***

## 🛠️ Tech Stack

* **Backend:** **Python**, **Flask**, **Google Gemini API**, **Snowflake Connector**, **Pandas**
* **Frontend:** **React (Vite)**, **Material-UI (MUI)**, **Axios**, **React Router DOM**
* **Database:** **Snowflake**

***

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

* Python 3.10+
* Node.js 18.x+ and npm
* Access to a Snowflake instance and a Google AI Studio API Key.

### ⚙️ Configuration

1.  In the root directory of the project, create a file named `.env`.
2.  Copy and paste the following template into the `.env` file and fill in your credentials.

    ```env
    # Snowflake Credentials
    SNOWFLAKE_USER="your_snowflake_username"
    SNOWFLAKE_PASSWORD="your_snowflake_password"
    SNOWFLAKE_ACCOUNT="your_snowflake_account_identifier"
    SNOWFLAKE_WAREHOUSE="your_warehouse"
    SNOWFLAKE_DATABASE="your_database"
    SNOWFLAKE_SCHEMA="your_schema"

    # Google Gemini API Key
    GOOGLE_API_KEY="your_gemini_api_key"
    ```

### 🐍 Backend Setup

1.  **Create Virtual Environment:**
    From the root directory, create and activate a Python virtual environment.
    ```bash
    # Create the environment
    python3 -m venv venv

    # Activate it (macOS/Linux)
    source venv/bin/activate
    
    # Activate it (Windows)
    .\venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    Install all required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Flask Server:**
    Start the backend API server. It will run on `http://localhost:5001`.
    ```bash
    python api.py
    ```
    Keep this terminal window open.

### 🖥️ Frontend Setup

1.  **Navigate to Frontend Directory:**
    Open a **new terminal window** and navigate into the frontend project.
    ```bash
    cd aria-frontend
    ```

2.  **Install Dependencies:**
    Install all required Node.js packages.
    ```bash
    npm install
    ```

3.  **Run the React Server:**
    Start the frontend development server. It will run on `http://localhost:5173` and should open automatically in your browser.
    ```bash
    npm run dev
    ```

You should now have both servers running and be able to access the application in your browser!

***

## 📊 Data Flow Architecture

### 🎯 System Architecture Overview

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                            🌐 AURA INTELLIGENCE SYSTEM                            ║
╚═══════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              👤 USER INTERFACE LAYER                             │
│                                                                                   │
│  ┌──────────────┐        ┌──────────────┐        ┌──────────────┐              │
│  │  💬 Chatbox  │        │ 📊 Dashboard │        │ 📁 CSV Upload│              │
│  │   Interface  │        │     View     │        │   Interface  │              │
│  └──────┬───────┘        └──────┬───────┘        └──────┬───────┘              │
│         │                       │                       │                        │
│         └───────────────────────┴───────────────────────┘                        │
│                                 │                                                 │
│                    ⚛️  React Frontend (Vite + MUI)                               │
│                         Port: 5173 | Axios HTTP Client                           │
└─────────────────────────────────┼───────────────────────────────────────────────┘
                                  │
                                  │ 🔄 REST API (JSON)
                                  │ CORS Enabled
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🐍 BACKEND API LAYER (Flask)                           │
│                                  Port: 5001                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  API ENDPOINTS                                                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐│   │
│  │  │ /api/chat    │  │/api/dashboard│  │/api/upload-  │  │/api/execute-││   │
│  │  │              │  │    -data     │  │    plan      │  │   upload    ││   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘│   │
│  └─────────┼──────────────────┼──────────────────┼──────────────────┼──────┘   │
│            │                  │                  │                  │            │
│  ┌─────────▼──────────────────▼──────────────────▼──────────────────▼──────┐   │
│  │                    🧠 AGENTIC AI WORKFLOW ENGINE                         │   │
│  │                                                                           │   │
│  │  ┌────────────────────────────────────────────────────────────────┐     │   │
│  │  │  1️⃣  INTENT ROUTER (route_user_question)                       │     │   │
│  │  │      • Greeting  • Data Query  • Off-Topic                     │     │   │
│  │  └────────────────────────┬───────────────────────────────────────┘     │   │
│  │                           │                                              │   │
│  │  ┌────────────────────────▼───────────────────────────────────────┐     │   │
│  │  │  2️⃣  ANALYSIS PLANNER (run_agentic_flow)                       │     │   │
│  │  │      Generates 5-20 investigation sub-questions                │     │   │
│  │  └────────────────────────┬───────────────────────────────────────┘     │   │
│  │                           │                                              │   │
│  │  ┌────────────────────────▼───────────────────────────────────────┐     │   │
│  │  │  3️⃣  TEXT-TO-SQL ENGINE (text_to_sql_tool)                     │     │   │
│  │  │      Converts natural language → Snowflake SQL                 │     │   │
│  │  └────────────────────────┬───────────────────────────────────────┘     │   │
│  │                           │                                              │   │
│  │  ┌────────────────────────▼───────────────────────────────────────┐     │   │
│  │  │  4️⃣  QUERY EXECUTOR (execute_snowflake_query)                  │     │   │
│  │  │      Runs queries & collects observations                      │     │   │
│  │  └────────────────────────┬───────────────────────────────────────┘     │   │
│  │                           │                                              │   │
│  │  ┌────────────────────────▼───────────────────────────────────────┐     │   │
│  │  │  5️⃣  ANSWER SYNTHESIZER                                        │     │   │
│  │  │      Combines all data → actionable insights                   │     │   │
│  │  └────────────────────────────────────────────────────────────────┘     │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
└─────────────────────┬─────────────────────────────┬─────────────────────────────┘
                      │                             │
        ┌─────────────▼──────────────┐   ┌──────────▼─────────────┐
        │   🤖 GOOGLE GEMINI API     │   │  ❄️  SNOWFLAKE DB      │
        │                            │   │                        │
        │  • gemini-2.5-flash-lite   │   │  📋 Tables:            │
        │  • Intent Classification   │   │  • FACT_SALES_DAILY    │
        │  • SQL Generation          │   │  • DIM_PRODUCT         │
        │  • Answer Synthesis        │   │  • DIM_STORE           │
        │  • CSV Mapping             │   │  • DIM_DATE            │
        │                            │   │  • DIM_PROMOTION       │
        │  ⚠️  Rate Limit:           │   │                        │
        │     15 requests/min        │   │  🔐 Secure Connection  │
        │     (Free Tier)            │   │     via Connector      │
        └────────────────────────────┘   └────────────────────────┘
```

### 🔄 Agentic RAG Workflow (Detailed)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     🎯 AUTONOMOUS INVESTIGATION PIPELINE                     │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  💭 USER     │  "Why are avocado sales down during the BOGO promotion?"
    │   QUESTION   │
    └──────┬───────┘
           │
           ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  🎯 STEP 1: GENERATE SUB-QUESTIONS (Gemini)                      │
    │                                                                   │
    │  AI breaks down complex question into investigation steps:       │
    │  1. What are total sales during BOGO period?                     │
    │  2. What are sales before BOGO?                                  │
    │  3. What are sales after BOGO?                                   │
    │  4. What is the spoilage rate during BOGO?                       │
    │  5. What is the average unit price?                              │
    │  ... (up to 20 sub-questions)                                    │
    └──────────────────────────┬───────────────────────────────────────┘
                               │
           ┌───────────────────┴───────────────────┐
           │   FOR EACH SUB-QUESTION (Loop)        │
           └───────────────────┬───────────────────┘
                               ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  🔧 STEP 2: PROCESS SUB-QUESTION                                 │
    │                                                                   │
    │  Sub-Q: "What are total sales during BOGO period?"               │
    └──────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  🔄 STEP 3: GENERATE SQL QUERY (Gemini Text-to-SQL)             │
    │                                                                   │
    │  Input: Natural language question + DB schema                    │
    │  Output:                                                          │
    │  ┌────────────────────────────────────────────────────────────┐ │
    │  │ SELECT SUM(NET_SALES)                                      │ │
    │  │ FROM FACT_SALES_DAILY FSD                                  │ │
    │  │ JOIN DIM_PRODUCT P ON FSD.PRODUCT_KEY = P.PRODUCT_KEY      │ │
    │  │ JOIN DIM_PROMOTION PR ON FSD.PROMO_KEY = PR.PROMO_KEY      │ │
    │  │ WHERE P.PRODUCT_NAME = 'Avocado'                           │ │
    │  │   AND PR.PROMO_TYPE = 'BOGO'                               │ │
    │  └────────────────────────────────────────────────────────────┘ │
    └──────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  ❄️  STEP 4: EXECUTE QUERY ON SNOWFLAKE                         │
    │                                                                   │
    │  ┌────────────────────────────────────────────────────────────┐ │
    │  │  Snowflake Connector                                       │ │
    │  │  ├─ Connect to warehouse                                   │ │
    │  │  ├─ Execute SQL query                                      │ │
    │  │  ├─ Fetch results                                          │ │
    │  │  └─ Return data                                            │ │
    │  └────────────────────────────────────────────────────────────┘ │
    │                                                                   │
    │  Result: $12,345.67                                              │
    └──────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  📝 STEP 5: STORE OBSERVATION                                    │
    │                                                                   │
    │  Observation 1: Total sales during BOGO = $12,345.67             │
    │  Observation 2: Total sales before BOGO = $18,234.22             │
    │  Observation 3: Total sales after BOGO = $15,678.90              │
    │  Observation 4: Spoilage rate during BOGO = 15%                  │
    │  ... (all observations collected)                                │
    └──────────────────────────┬───────────────────────────────────────┘
                               │
           ┌───────────────────┴───────────────────┐
           │   REPEAT FOR ALL SUB-QUESTIONS        │
           └───────────────────┬───────────────────┘
                               │
                               ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  🧠 STEP 6: SYNTHESIZE FINAL ANSWER (Gemini)                     │
    │                                                                   │
    │  Input: All observations + original question                     │
    │  AI analyzes patterns and generates comprehensive answer:        │
    │                                                                   │
    │  ┌────────────────────────────────────────────────────────────┐ │
    │  │ "Avocado sales decreased by 32% during the BOGO promotion │ │
    │  │  compared to the previous period. Key findings:            │ │
    │  │                                                             │ │
    │  │  1. Sales dropped from $18,234 to $12,345                  │ │
    │  │  2. Spoilage increased to 15% (up from 8%)                 │ │
    │  │  3. Unit price decreased but volume didn't compensate      │ │
    │  │                                                             │ │
    │  │  Root Cause: The promotion attracted customers but         │ │
    │  │  increased spoilage ate into profits. Consider shorter     │ │
    │  │  promotion periods or better inventory management."        │ │
    │  └────────────────────────────────────────────────────────────┘ │
    └──────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  ✅ RETURN TO USER                                               │
    │                                                                   │
    │  Display actionable insights in chat interface                   │
    └──────────────────────────────────────────────────────────────────┘

    ⏱️  Average Processing Time: 10-30 seconds (depends on complexity)
    🔄  API Calls per Query: 3-25 (1 router + 1 planner + N sub-queries + 1 synthesis)
```

### 📊 Key Innovation: Multi-Step Autonomous Analysis

Unlike traditional chatbots that answer questions directly, Aura uses an **agentic workflow**:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    🆚 TRADITIONAL vs AGENTIC APPROACH                       │
└────────────────────────────────────────────────────────────────────────────┘

   TRADITIONAL BI CHATBOT                    🚀 AURA (AGENTIC)
   ═══════════════════════                   ════════════════════

   User: "Why are sales down?"               User: "Why are sales down?"
          ↓                                          ↓
   ┌──────────────────┐                     ┌──────────────────────────┐
   │ Single SQL Query │                     │ AI Plans Investigation   │
   │ "SELECT sales    │                     │ • Check current sales    │
   │  FROM table"     │                     │ • Compare to last period │
   └────────┬─────────┘                     │ • Analyze promotions     │
            │                                │ • Check inventory        │
            ↓                                │ • Review competition     │
   ┌──────────────────┐                     │ • Examine seasonality    │
   │ Raw Data Result  │                     └────────┬─────────────────┘
   │ "$50,000"        │                              │
   └────────┬─────────┘                              ↓
            │                                ┌──────────────────────────┐
            ↓                                │ Executes 10-20 Queries   │
   ❌ No Context                             │ Gathers All Evidence     │
   ❌ No Analysis                            └────────┬─────────────────┘
   ❌ No Recommendations                              │
                                                      ↓
                                            ┌──────────────────────────┐
                                            │ AI Synthesizes Insights  │
                                            │ • Root cause identified  │
                                            │ • Patterns discovered    │
                                            │ • Actions recommended    │
                                            └────────┬─────────────────┘
                                                     │
                                                     ↓
                                            ✅ Full Context
                                            ✅ Deep Analysis
                                            ✅ Actionable Insights

   ⏱️  Response Time: 2-3 seconds            ⏱️  Response Time: 10-30 seconds
   📊 Queries: 1                             📊 Queries: 3-25
   🎯 Value: Low                             🎯 Value: High
```

| Feature | Traditional Chatbot | 🚀 Aura (Agentic) |
|---------|-------------------|------------------|
| **Query Approach** | Single query → Single answer | Complex question → Multiple investigations → Synthesized insight |
| **Analysis Depth** | Surface-level responses | Root cause analysis with context |
| **Context Awareness** | None | Considers historical trends, patterns, correlations |
| **SQL Generation** | Static, predefined queries | Dynamic query generation based on data schema |
| **Question Handling** | Limited to predefined questions | Handles any business question autonomously |
| **Insight Quality** | Raw data dump | Actionable recommendations with reasoning |

### Detailed Data Flow by Feature

#### 🔹 **Feature 1: Chat Query Flow**

```
Step 1: User Input
├─ User types question in chatbox
└─ Frontend: Chatbox.jsx captures input

Step 2: API Request
├─ Frontend sends POST to /api/chat
│  ├─ Payload: { message: "user question", history: [...] }
│  └─ Uses Axios for HTTP request
└─ CORS headers allow cross-origin communication

Step 3: Intent Classification (Backend)
├─ Backend: api.py receives request
├─ Calls: route_user_question()
│  ├─ Sends question to Gemini API
│  └─ Returns intent: "greeting" | "data_query" | "off_topic"
└─ Determines next action based on intent

Step 4a: If Greeting/Off-Topic
└─ Returns pre-defined response immediately

Step 4b: If Data Query - Agentic Flow Begins
├─ Backend: run_agentic_flow() is called
│
├─ Sub-Step 1: Create Analysis Plan
│  ├─ Gemini API generates numbered investigation steps
│  └─ Example: "1. Check sales trends, 2. Analyze promotions, 3. Review spoilage"
│
├─ Sub-Step 2: Execute Each Step
│  ├─ For each sub-question:
│  │  ├─ Call: text_to_sql_tool()
│  │  ├─ Gemini converts question → SQL query
│  │  ├─ Call: execute_snowflake_query()
│  │  ├─ Snowflake returns data
│  │  └─ Store as "Observation N"
│  └─ Repeat for all steps in plan
│
└─ Sub-Step 3: Synthesize Answer
   ├─ Gemini receives all observations
   ├─ Generates comprehensive final answer
   └─ Returns synthesized response

Step 5: Response to Frontend
├─ Backend sends JSON: { response: "final answer" }
└─ Frontend displays in chat interface

Step 6: Error Handling
├─ Rate Limit (429): "API quota exceeded, wait 1 minute"
├─ SQL Error: Shows error message from Snowflake
└─ General Error (500): Displays error to user
```

#### 🔹 **Feature 2: Dashboard Data Flow**

```
Step 1: Page Load
├─ User navigates to Dashboard
└─ Frontend: dashboard.jsx mounts

Step 2: Data Request
├─ Frontend sends GET to /api/dashboard-data
└─ No payload needed

Step 3: Backend Processing
├─ Backend: api.py receives request
├─ Establishes Snowflake connection
├─ Executes multiple SQL queries in parallel:
│  ├─ Query 1: Total Revenue (7 days)
│  ├─ Query 2: Units Sold (7 days)
│  ├─ Query 3: Top Product (all time)
│  └─ Query 4: Recent 5 transactions
└─ Formats data into JSON

Step 4: Response
├─ Backend returns:
│  {
│    totalRevenue: "$X,XXX.XX",
│    unitsSold: "X,XXX",
│    avgProfitMargin: "96.7%",
│    topProduct: "Product Name",
│    recentSales: [{text: "...", value: "$XX"}]
│  }
└─ Frontend displays in MUI cards

Step 5: Real-Time Updates
└─ Dashboard refreshes on navigation
```

#### 🔹 **Feature 3: CSV Upload Flow**

```
Step 1: File Selection
├─ User drags/drops CSV or clicks to upload
└─ Frontend: react-dropzone captures file

Step 2: File Analysis Request
├─ Frontend sends POST to /api/upload-plan
│  ├─ FormData with CSV file
│  └─ Multipart form data
└─ File stored in temp_uploads/

Step 3: AI Analysis (Backend)
├─ Backend: get_ai_upload_plan() is called
├─ Reads CSV with Pandas
├─ Gets all Snowflake table schemas
├─ Sends to Gemini API:
│  ├─ CSV columns + sample data
│  ├─ Available database tables
│  └─ Asks: "Which table? How to map columns?"
└─ Gemini returns JSON plan

Step 4: Display Confirmation
├─ Backend returns:
│  {
│    suggested_table: "TABLE_NAME",
│    column_mapping: {csv_col: db_col},
│    preview: "explanation"
│  }
└─ Frontend shows plan to user for approval

Step 5: User Confirms
├─ User clicks "Confirm Upload"
└─ Frontend sends POST to /api/execute-upload

Step 6: Data Insertion
├─ Backend: smart_upload_csv() is called
├─ Reads CSV with Pandas
├─ Maps columns according to plan
├─ Inserts data into Snowflake table
├─ Deletes temp file
└─ Returns success/error message

Step 7: Completion
└─ Frontend displays success message in chat
```

### 🔄 Key Components Interaction Map

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
├─────────────────────────────────────────────────────────────┤
│  Navbar.jsx          → Navigation between pages             │
│  dashboard.jsx       → Displays KPIs from Snowflake         │
│  Chatbox.jsx         → Chat interface + file upload         │
│  App.jsx             → Routes and layout                     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS (Axios)
                         │ Port 5173 → Port 5001
┌────────────────────────▼────────────────────────────────────┐
│                   BACKEND (Flask API)                        │
├─────────────────────────────────────────────────────────────┤
│  api.py              → API endpoints + CORS                  │
│  ├─ /api/chat        → Chat queries                          │
│  ├─ /api/dashboard-data → KPI data                           │
│  ├─ /api/upload-plan → CSV analysis                          │
│  └─ /api/execute-upload → CSV insertion                      │
│                                                               │
│  app.py              → Agentic flow logic                    │
│  ├─ route_user_question()    → Intent classification         │
│  ├─ run_agentic_flow()       → Multi-step investigation      │
│  ├─ generate_sql_query()     → Text-to-SQL conversion        │
│  └─ execute_snowflake_query() → Database queries             │
│                                                               │
│  csv_parser.py       → CSV upload intelligence               │
│  database_connector.py → Schema retrieval                    │
└────────────┬─────────────────────────┬──────────────────────┘
             │                         │
             │                         │
┌────────────▼─────────────┐  ┌───────▼──────────────────────┐
│   Google Gemini API      │  │   Snowflake Database         │
├──────────────────────────┤  ├──────────────────────────────┤
│ • Intent classification  │  │ • FACT_SALES_DAILY           │
│ • SQL query generation   │  │ • DIM_PRODUCT                │
│ • Analysis synthesis     │  │ • DIM_STORE                  │
│ • CSV mapping            │  │ • DIM_DATE                   │
│ • Rate Limit: 15 req/min │  │ • DIM_PROMOTION              │
└──────────────────────────┘  └──────────────────────────────┘
```

### 🔐 Environment Variables Flow

```
.env file (backend/)
├─ SNOWFLAKE_USER        → database_connector.py
├─ SNOWFLAKE_PASSWORD    → database_connector.py
├─ SNOWFLAKE_ACCOUNT     → database_connector.py
├─ SNOWFLAKE_WAREHOUSE   → database_connector.py
├─ SNOWFLAKE_DATABASE    → database_connector.py
├─ SNOWFLAKE_SCHEMA      → database_connector.py
└─ GOOGLE_API_KEY        → app.py (Gemini API calls)
```

### ⚡ Performance Considerations

- **Rate Limiting**: Gemini free tier = 15 requests/minute
- **Agentic Flow**: Each query may use 3-20+ API calls
- **Caching**: DB schema loaded once at startup
- **Error Recovery**: Automatic retry with exponential backoff
- **CORS**: Configured for localhost development