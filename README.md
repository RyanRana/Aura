# Aura: Autonomous Retail Intelligence Agent

Aura is an AI-powered analytics platform designed to provide retail managers with immediate, data-driven insights. It features a conversational AI that can perform multi-step investigations into business questions by querying a Snowflake data warehouse, alongside a real-time analytics dashboard.

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