import streamlit as st
from movie_agent import MovieAgent

# Initialize the movie recommendation agent
movie_agent = MovieAgent()

# Set up the main title and description
st.title("🎬 Movie Recommendator 🍿")
st.subheader("Get personalized movie recommendations just by asking!")

# Initialize the conversation history in Streamlit session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Input field for the user to ask for recommendations
user_input = st.text_input("Ask for movie recommendations:")

# Process user input and get response from the agent
if user_input:
    response = movie_agent.run(user_input=user_input)
    st.session_state.conversation.append({"user": user_input, "bot": response["output"]})

# Display the conversation history
st.write("### Chat History")
for chat in st.session_state.conversation:
    st.write(f"**You:** {chat['user']}")
    st.write(f"**Movie Recommendator:** {chat['bot']}")

# Add a sidebar with additional options or information
st.sidebar.title("About")
st.sidebar.info("""
This app uses a sophisticated movie recommendation engine to suggest films based on your preferences.
Simply type in your preferences or ask for specific types of movies, and the agent will provide personalized suggestions!
""")


# Optional: Add theming or style improvements (e.g., background color, font style)
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f5f5f5;
        color: #333333;
    }
    .sidebar .sidebar-content {
        background: #e0e0e0;
        color: #333333;
    }
    </style>
    """, unsafe_allow_html=True
)

# Optional: Add movie posters if URLs are provided by the agent
if user_input:
    if "posters" in response:
        st.write("### Recommended Movies")
        cols = st.columns(3)
        for i, poster in enumerate(response["posters"]):
            with cols[i % 3]:
                st.image(poster["url"], caption=poster["title"])

# Optional: Implement a reset button to clear the conversation history
if st.sidebar.button("Reset Conversation"):
    st.session_state.conversation = []
    st.experimental_rerun()


# Add a footer
st.markdown(
    """
    <hr>
    <footer>
    <p style="text-align: center;">© 2024 Movie Recommendator. All rights reserved.</p>
    <p style="text-align: center;">Developed with ❤️ by Tibis.</p>
    </footer>
    """, unsafe_allow_html=True
)