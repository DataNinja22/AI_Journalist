import streamlit as st
import os
import time
from backend import generate_article

# Streamlit App setup
st.set_page_config(page_title="AI Journalist Agent", page_icon="🗞️", layout="wide")
st.title("🗞️ AI Journalist Agent")
st.caption("Automatically research, analyze, summarize, and write high-quality articles using GPT-4o or GPT-3.5-turbo.")

# Session state initialization for tracking progress
if "current_step" not in st.session_state:
    st.session_state.current_step = "Not Started"
if "research_results" not in st.session_state:
    st.session_state.research_results = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# User inputs
with st.sidebar:
    st.header("Settings")
    openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
    serper_api_key = st.text_input("Enter your Serper API Key", type="password")
    
    model_choice = st.selectbox(
        "Select AI Model", 
        ["gpt-3.5-turbo (Fast)", "gpt-4o (High Quality)"],
        help="GPT-3.5-turbo is faster but GPT-4o produces higher quality articles"
    )
    
    article_length = st.slider(
        "Article Length (words)", 
        min_value=300, 
        max_value=1000, 
        value=500, 
        step=100,
        help="Longer articles require more processing time"
    )
    
    num_sources = st.slider(
        "Number of Sources",
        min_value=2,
        max_value=5,
        value=3,
        help="More sources mean more comprehensive research but slower processing"
    )
    
    show_intermediates = st.checkbox("Show Intermediate Results", value=False)
    
    st.subheader("Optional")
    article_style = st.selectbox(
        "Article Style",
        ["Informative", "Persuasive", "Narrative", "Analytical", "Conversational"],
        index=0
    )
    
    target_audience = st.text_input("Target Audience (Optional)", 
                                   placeholder="e.g., General public, Students, Professionals")

# Set up the main content area
topic = st.text_input("Enter the topic you want an article on:")

# Create placeholder for detailed progress updates
progress_placeholder = st.empty()
message_placeholder = st.empty()
research_placeholder = st.empty()
analysis_placeholder = st.empty()
final_article_placeholder = st.empty()

def update_progress_message(step_name, message, progress_value):
    """Update progress bar and message"""
    progress_bar = progress_placeholder.progress(progress_value)
    message_placeholder.info(f"**Current Step:** {step_name} - {message}")
    st.session_state.current_step = step_name
    # Simulate some processing time to show progress
    time.sleep(0.5)
    return progress_bar

if openai_api_key and serper_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["SERPER_API_KEY"] = serper_api_key
    
    # Extract the model name from selection
    chosen_model = "gpt-3.5-turbo" if "3.5" in model_choice else "gpt-4o"
    
    if topic and st.button("Generate Article"):
        try:
            # Initialize progress tracking
            update_progress_message("Starting", "Initializing article generation process...", 0)
            
            # Call the backend function to generate the article
            research_text, analysis_text, article_text = generate_article(
                topic=topic,
                model=chosen_model,
                article_length=article_length,
                num_sources=num_sources,
                article_style=article_style,
                target_audience=target_audience,
                progress_callback=update_progress_message
            )
            
            # Store results in session state
            st.session_state.research_results = research_text
            st.session_state.analysis_results = analysis_text
            
            # Display intermediate results if requested
            if show_intermediates:
                research_placeholder.success("Research Results:")
                research_placeholder.markdown(research_text)
                
                analysis_placeholder.success("Analysis Results:")
                analysis_placeholder.markdown(analysis_text)
            
            # Display final article
            final_article_placeholder.subheader("📰 Final Article")
            final_article_placeholder.markdown(article_text)
            
            # Add download button
            st.download_button(
                label="Download Article",
                data=article_text,
                file_name=f"{topic.replace(' ', '_')}_article.md",
                mime="text/markdown"
            )
            
            # Add feedback options
            st.subheader("Article Feedback")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👍 Great Article!"):
                    st.success("Thanks for your positive feedback!")
            with col2:
                if st.button("👌 Good but could be better"):
                    st.info("Thanks for your feedback! What could be improved?")
                    st.text_area("Suggestions for improvement:")
            with col3:
                if st.button("👎 Needs improvement"):
                    st.warning("We appreciate your honest feedback!")
                    st.text_area("What could be improved?")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.warning("Please enter your OpenAI API key and Serper API key in the sidebar to continue.")

# Add footer with app info
st.markdown("---")
st.caption("AI Journalist- Powered by CrewAI and OpenAI")