import streamlit as st
from agent import process_user_prompt

st.set_page_config(page_title="Product Assistant", page_icon="🤖", layout="wide")

st.title("💻 Product Assistant")
st.write("Ask me about laptops, tablets, or touch devices — I’ll scrape and filter results for you!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "quit" not in st.session_state:
    st.session_state["quit"] = False

# Display previous chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box (only if user hasn't quit yet)
if not st.session_state["quit"]:
    if prompt := st.chat_input("Enter your query..."):
        # Handle quit/exit command
        if prompt.lower() in ["quit", "exit"]:
            st.session_state["quit"] = True
            st.session_state["messages"].append(
                {"role": "assistant", "content": "👋 Exiting session. Goodbye!"}
            )
            st.experimental_rerun()

        # Normal processing
        else:
            # Save user message
            st.session_state["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Call agent logic
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = process_user_prompt(prompt)

                    if response is None:
                        st.markdown("⚠️ No response.")
                        st.session_state["messages"].append({"role": "assistant", "content": "⚠️ No response."})
                    elif isinstance(response, str):
                        st.markdown(response)
                        st.session_state["messages"].append({"role": "assistant", "content": response})
                    else:
                        st.write("Here are the results:")
                        st.dataframe(response.head(20))
                        st.session_state["messages"].append(
                            {"role": "assistant", "content": "📊 Displaying scraped results."}
                        )
else:
    st.info("Session ended. Refresh the page to start again.")
