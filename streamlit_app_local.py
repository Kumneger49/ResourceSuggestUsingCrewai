import streamlit as st
import os
import sys
from pathlib import Path
import time
from datetime import datetime

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent / "src"))

from resourcesuggest.crew import ResourceSuggester

# Page configuration
st.set_page_config(
    page_title="ResourceSuggester AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .result-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    
    .agent-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .agent-working {
        background: #e3f2fd;
        border-left: 3px solid #2196f3;
    }
    
    .agent-complete {
        background: #e8f5e8;
        border-left: 3px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 ResourceSuggester AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your AI-powered research assistant that finds the best resources for any topic</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to enable AI-powered research"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your OpenAI API key")
        
        st.divider()
        
        # Additional settings
        st.subheader("🔧 Advanced Options")
        
        # Research depth
        research_depth = st.selectbox(
            "Research Depth",
            ["Quick Overview", "Detailed Analysis", "Comprehensive Research"],
            help="Choose how thorough you want the research to be"
        )
        
        # Number of videos
        num_videos = st.slider(
            "Number of YouTube Videos",
            min_value=3,
            max_value=10,
            value=5,
            help="How many YouTube videos to find"
        )
        
        st.divider()
        
        # About section
        st.subheader("ℹ️ About")
        st.markdown("""
        **ResourceSuggester AI** uses advanced AI agents to:
        - 🔍 Search the web for relevant information
        - 📺 Find educational YouTube videos
        - 📝 Create comprehensive summaries
        - 📚 Organize resources for easy access
        """)
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Topic input
        st.subheader("🎯 What would you like to research?")
        
        topic = st.text_input(
            "Enter your research topic",
            placeholder="e.g., machine learning, climate change, blockchain technology...",
            help="Be specific for better results"
        )
        
        # Research button
        col_button1, col_button2, col_button3 = st.columns([1, 2, 1])
        with col_button2:
            start_research = st.button(
                "🚀 Start Research",
                use_container_width=True,
                disabled=not (topic and api_key)
            )
        
        # Display results
        if start_research and topic and api_key:
            with st.spinner("🤖 AI agents are researching your topic..."):
                try:
                    # Initialize the crew
                    crew = ResourceSuggester().crew()
                    
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulate progress updates
                    for i in range(100):
                        time.sleep(0.05)
                        progress_bar.progress(i + 1)
                        if i < 30:
                            status_text.text("🔍 Researcher agent is gathering information...")
                        elif i < 70:
                            status_text.text("📝 Writer agent is creating summary...")
                        else:
                            status_text.text("✨ Finalizing results...")
                    
                    # Run the crew
                    result = crew.kickoff(inputs={"topic": topic})
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Research complete!")
                    
                    # Display results
                    st.success("🎉 Research completed successfully!")
                    
                    # Results section
                    st.subheader("📊 Research Results")
                    
                    # Create tabs for different result types
                    tab1, tab2, tab3 = st.tabs(["📝 Summary", "🌐 Web Resources", "📺 Video Resources"])
                    
                    with tab1:
                        st.markdown("### Executive Summary")
                        if hasattr(result, 'raw') and result.raw:
                            st.markdown(result.raw)
                        else:
                            st.markdown(str(result))
                    
                    with tab2:
                        st.markdown("### 🌐 Recommended Websites")
                        # This would be populated from the actual results
                        st.info("Web resources will be displayed here based on the research results")
                    
                    with tab3:
                        st.markdown("### 📺 Recommended YouTube Videos")
                        # This would be populated from the actual results
                        st.info("YouTube videos will be displayed here based on the research results")
                    
                    # Download results
                    st.subheader("💾 Download Results")
                    col_dl1, col_dl2 = st.columns(2)
                    
                    with col_dl1:
                        if st.button("📄 Download as Markdown"):
                            # Create markdown content
                            markdown_content = f"""
# Research Results: {topic}

## Summary
{str(result)}

## Generated on
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                            """
                            
                            st.download_button(
                                label="📥 Download Markdown",
                                data=markdown_content,
                                file_name=f"research_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
                                mime="text/markdown"
                            )
                    
                    with col_dl2:
                        if st.button("📊 Download as JSON"):
                            import json
                            json_content = {
                                "topic": topic,
                                "timestamp": datetime.now().isoformat(),
                                "results": str(result)
                            }
                            
                            st.download_button(
                                label="📥 Download JSON",
                                data=json.dumps(json_content, indent=2),
                                file_name=f"research_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                                mime="application/json"
                            )
                
                except Exception as e:
                    st.error(f"❌ An error occurred during research: {str(e)}")
                    st.info("💡 Make sure your OpenAI API key is valid and you have sufficient credits")
        
        # Show example topics if no research has been started
        elif not start_research:
            st.markdown("### 💡 Example Topics")
            
            example_topics = [
                "Machine Learning Fundamentals",
                "Climate Change Solutions",
                "Blockchain Technology",
                "Artificial Intelligence Ethics",
                "Sustainable Energy",
                "Data Science Career Path",
                "Cybersecurity Best Practices",
                "Digital Marketing Strategies"
            ]
            
            cols = st.columns(3)
            for i, topic_example in enumerate(example_topics):
                with cols[i % 3]:
                    if st.button(topic_example, key=f"example_{i}"):
                        st.session_state.suggested_topic = topic_example
                        st.rerun()
            
            # Display suggested topic if selected
            if 'suggested_topic' in st.session_state:
                st.info(f"💡 Try researching: **{st.session_state.suggested_topic}**")

if __name__ == "__main__":
    main()
