import streamlit as st
import time

# --- Page Configuration ---
# The st.set_page_config() command must be the first Streamlit command in your script.
st.set_page_config(
    page_title="Aria: Retail Intelligence Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Mock Agent Function ---
# This function simulates the behavior of your actual LangChain agent.
# It includes a "thinking" spinner and streams the response word by word.
def mock_agent_response(prompt):
    """
    A placeholder function to simulate the agent's response generation.
    Replace this with your actual agent.run(prompt) call.
    """
    response_text = (
        "Based on my analysis, organic banana sales in New Brunswick are down 40% this week "
        "compared to the last 4-week average. My investigation indicates this is due to a "
        "stockout that began on Tuesday morning. Inventory levels dropped to zero and were not "
        "replenished.\n\n**Recommendation:** I recommend placing an emergency order for organic "
        "bananas and investigating the restocking delay from the distribution center to prevent "
        "future lost sales."
    )
    # Simulate a "thinking" delay
    with st.spinner("Aria is investigating..."):
        time.sleep(2)

    # Stream the response to the UI
    def stream_response():
        for word in response_text.split(" "):
            yield word + " "
            time.sleep(0.05)
    return stream_response

# --- Application Title and Introduction ---
st.title("🤖 Aria: The Autonomous Retail Intelligence Agent")
st.markdown("""
Welcome! I am Aria, your AI-powered assistant for analyzing store performance.
Ask me a high-level question, and I will autonomously investigate the issue by querying Snowflake to find the root cause.
\n*For example: 'Why are we losing money on avocados this week at the Edison store?'*
""")


# --- Chat History Management ---
# Initialize chat history in session state if it doesn't exist.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages on each rerun.
for message in st.session_state.messages:
    # Use custom icons for user and assistant
    avatar = '🧑‍💻' if message["role"] == "user" else '🤖'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# --- User Input and Agent Response ---
# The st.chat_input widget displays a text input field at the bottom of the page.
if prompt := st.chat_input("Ask Aria a question..."):
    # Add the user's message to the chat history and display it.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar='🧑‍💻'):
        st.markdown(prompt)

    # Generate and display the agent's response.
    with st.chat_message("assistant", avatar='🤖'):
        # The st.write_stream function is used to display the streamed response.
        response_generator = mock_agent_response(prompt)
        full_response = st.write_stream(response_generator)

    # Add the full response from the agent to the chat history.
    st.session_state.messages.append({"role": "assistant", "content": full_response})

