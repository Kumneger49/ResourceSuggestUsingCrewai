import streamlit as st
import os
import sys
from pathlib import Path
import time
from datetime import datetime
import requests
import json
import re
from youtubesearchpython import VideosSearch

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent / "src"))

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

def search_youtube_videos(topic: str):
    """
    Search YouTube for videos about the topic.
    Replicates your YouTubeSearchTool functionality.
    """
    try:
        videos = VideosSearch(topic, limit=5)
        video_list = []
        for v in videos.result()['result']:
            video_list.append({"title": v['title'], "link": v['link']})
        return video_list
    except Exception as e:
        st.warning(f"YouTube search error: {str(e)}")
        return []

def search_web_resources(topic: str):
    """
    Search the web for information about the topic.
    Replicates web search functionality without ChromaDB.
    """
    try:
        # Using DuckDuckGo API for web search
        search_url = f"https://api.duckduckgo.com/?q={topic}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            if 'AbstractURL' in data and data['AbstractURL']:
                results.append({
                    'title': data.get('Abstract', f'Information about {topic}'),
                    'url': data['AbstractURL'],
                    'snippet': data.get('Abstract', '')
                })
            if 'RelatedTopics' in data:
                for topic_item in data['RelatedTopics'][:5]:
                    if isinstance(topic_item, dict) and 'FirstURL' in topic_item:
                        results.append({
                            'title': topic_item.get('Text', f'Related to {topic}'),
                            'url': topic_item['FirstURL'],
                            'snippet': topic_item.get('Text', '')
                        })
            return results
    except Exception as e:
        st.warning(f"Web search error: {str(e)}")
    return []

def run_research_pipeline(topic: str, api_key: str):
    """
    Replicates your CrewAI pipeline functionality without using CrewAI directly.
    This mimics the researcher and writer agents workflow.
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Step 1: Research Phase (Researcher Agent)
        st.info("🔍 **Researcher Agent**: Gathering information from web and YouTube...")
        
        # Get YouTube videos
        youtube_videos = search_youtube_videos(topic)
        
        # Get web resources
        web_resources = search_web_resources(topic)
        
        # Step 2: Research Summary (Researcher Agent Output)
        research_content = f"""
## Research Findings for: {topic}

### Web Resources Found:
"""
        for i, resource in enumerate(web_resources, 1):
            research_content += f"{i}. **{resource['title']}**: {resource['url']}\n   {resource['snippet']}\n\n"
        
        research_content += "\n### YouTube Videos Found:\n"
        for i, video in enumerate(youtube_videos, 1):
            research_content += f"{i}. **{video['title']}**: {video['link']}\n\n"
        
        # Step 3: Writer Agent Phase
        st.info("📝 **Writer Agent**: Creating comprehensive summary...")
        
        writer_prompt = f"""
You are a Senior Content Writer specializing in creating clear, engaging summaries of research findings.

Based on the following research about "{topic}", create a comprehensive summary that includes:

## Executive Summary
Provide a clear overview of the topic and its key concepts.

## Key Insights
Highlight the most important findings and insights about {topic}.

## Recommended Resources

### Websites
List and describe the recommended websites with their URLs.

### YouTube Videos
List and describe the recommended YouTube videos with their URLs.

Research Content:
{research_content}

Make sure to include all the URLs provided and create a well-structured, reader-friendly summary.
"""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an experienced content writer who excels at turning complex research into compelling narratives. You specialize in creating articles, reports, and summaries that balance accuracy with readability."},
                {"role": "user", "content": writer_prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Research pipeline error: {str(e)}")
        return f"Error during research: {str(e)}"

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
        **ResourceSuggester AI** uses advanced AI to:
        - 🔍 Search the web for relevant information
        - 📺 Find educational YouTube videos
        - 📝 Create comprehensive summaries
        - 📚 Organize resources for easy access
        """)
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Check if API key is provided
        if not api_key:
            st.error("⚠️ **Please enter your OpenAI API key in the sidebar to start researching!**")
            st.info("💡 The API key is required to enable AI-powered research functionality.")
        else:
            st.success("✅ **API Key configured! You can now start researching.**")
        
        # Topic input
        st.subheader("🎯 What would you like to research?")
        
        # Initialize topic from session state if available
        if 'suggested_topic' in st.session_state:
            default_topic = st.session_state.suggested_topic
            # Clear the session state after using it
            del st.session_state.suggested_topic
        else:
            default_topic = ""
        
        topic = st.text_input(
            "Enter your research topic",
            value=default_topic,
            placeholder="e.g., machine learning, climate change, blockchain technology...",
            help="Be specific for better results"
        )
        
        # Check if we should auto-start research (from example topic click)
        auto_start_research = False
        if 'auto_start_research' in st.session_state and st.session_state.auto_start_research:
            auto_start_research = True
            # Clear the flag after using it
            del st.session_state.auto_start_research
        
        # Research button
        col_button1, col_button2, col_button3 = st.columns([1, 2, 1])
        with col_button2:
            start_research = st.button(
                "🚀 Start Research",
                use_container_width=True,
                disabled=not (topic and api_key)
            )
        
        # Display results
        if (start_research or auto_start_research) and topic and api_key:
            # Show auto-research indicator if triggered by example topic
            if auto_start_research:
                st.info(f"🔍 **Auto-researching:** {topic}")
            
            with st.spinner("🤖 AI agents are researching your topic..."):
                try:
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Initialize Research
                    status_text.text("🤖 Initializing AI research agents...")
                    progress_bar.progress(25)
                    
                    # Step 2: Run Research Pipeline
                    status_text.text("🔍 AI agents are researching your topic...")
                    progress_bar.progress(50)
                    result = run_research_pipeline(topic, api_key)
                    
                    # Step 3: Process Results
                    status_text.text("📝 Processing research results...")
                    progress_bar.progress(75)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Research complete!")
                    
                    # Display results
                    st.success("🎉 Research completed successfully!")
                    
                    # Parse the result to extract resources
                    result_text = str(result)
                    
                    # Extract websites and videos from the result
                    websites = []
                    videos = []
                    
                    # Extract all URLs first
                    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
                    all_urls = re.findall(url_pattern, result_text)
                    
                    # Separate YouTube URLs from other websites
                    for url in all_urls:
                        if 'youtube.com' in url or 'youtu.be' in url:
                            # Extract video ID and create full URL
                            if 'youtube.com/watch?v=' in url:
                                video_id = url.split('watch?v=')[1].split('&')[0]
                                video_url = f"https://www.youtube.com/watch?v={video_id}"
                            elif 'youtu.be/' in url:
                                video_id = url.split('youtu.be/')[1].split('?')[0]
                                video_url = f"https://www.youtube.com/watch?v={video_id}"
                            else:
                                video_url = url
                            
                            # Try to find a title for this video
                            title = f"YouTube Video - {topic}"
                            videos.append({"title": title, "url": video_url})
                        else:
                            # Clean up the URL and add to websites
                            clean_url = url.rstrip('.,;:!?')
                            if clean_url not in websites:
                                websites.append(clean_url)
                    
                    # Also look for video titles in the text
                    video_section_pattern = r'(?:YouTube Videos?|Videos?|Video Resources?)[:\s]*\n(.*?)(?=\n\n|\n[A-Z]|$)'
                    video_section_match = re.search(video_section_pattern, result_text, re.DOTALL | re.IGNORECASE)
                    if video_section_match:
                        video_section = video_section_match.group(1)
                        # Extract video titles and URLs from the section
                        video_lines = video_section.split('\n')
                        for line in video_lines:
                            if 'http' in line:
                                # Extract URL and title from the line
                                url_match = re.search(url_pattern, line)
                                if url_match:
                                    url = url_match.group(0)
                                    title = line.replace(url, '').strip(' -:').strip()
                                    if not title:
                                        title = f"Video - {topic}"
                                    videos.append({"title": title, "url": url})
                    
                    # Look for website section
                    website_section_pattern = r'(?:Websites?|Web Resources?|Recommended Sites?)[:\s]*\n(.*?)(?=\n\n|\n[A-Z]|$)'
                    website_section_match = re.search(website_section_pattern, result_text, re.DOTALL | re.IGNORECASE)
                    if website_section_match:
                        website_section = website_section_match.group(1)
                        # Extract website URLs from the section
                        website_lines = website_section.split('\n')
                        for line in website_lines:
                            if 'http' in line:
                                url_match = re.search(url_pattern, line)
                                if url_match:
                                    url = url_match.group(0)
                                    clean_url = url.rstrip('.,;:!?')
                                    if clean_url not in websites:
                                        websites.append(clean_url)
                    
                    # Results section
                    st.subheader("📊 Research Results")
                    
                    # Create tabs for different result types
                    tab1, tab2, tab3 = st.tabs(["📝 Summary", "🌐 Web Resources", "📺 Video Resources"])
                    
                    with tab1:
                        st.markdown("### Executive Summary")
                        st.markdown(result_text)
                    
                    with tab2:
                        st.markdown("### 🌐 Recommended Websites")
                        if websites:
                            for i, website in enumerate(websites, 1):
                                st.markdown(f"**{i}.** [{website}]({website})")
                        else:
                            st.info("No specific websites were found in the research results. The summary may contain general information about the topic.")
                    
                    with tab3:
                        st.markdown("### 📺 Recommended YouTube Videos")
                        if videos:
                            for i, video in enumerate(videos, 1):
                                st.markdown(f"**{i}.** [{video['title']}]({video['url']})")
                        else:
                            st.info("No specific YouTube videos were found in the research results. The summary may contain general information about the topic.")
                    
                    # Download results
                    st.subheader("💾 Download Results")
                    col_dl1, col_dl2 = st.columns(2)
                    
                    with col_dl1:
                        if st.button("📄 Download as Markdown"):
                            # Create markdown content
                            markdown_content = f"""
# Research Results: {topic}

## Summary
{result_text}

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
                            json_content = {
                                "topic": topic,
                                "timestamp": datetime.now().isoformat(),
                                "results": result_text,
                                "websites": websites,
                                "videos": videos
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
            
            # Check if API key is provided for example topics
            if not api_key:
                st.warning("🔒 **Example topics are disabled. Please enter your OpenAI API key in the sidebar to enable them.**")
                # Show disabled example topics
                cols = st.columns(3)
                for i, topic_example in enumerate(example_topics):
                    with cols[i % 3]:
                        st.button(
                            topic_example, 
                            key=f"example_{i}",
                            disabled=True,
                            help="Enter your OpenAI API key to enable this feature"
                        )
            else:
                # Show active example topics
                cols = st.columns(3)
                for i, topic_example in enumerate(example_topics):
                    with cols[i % 3]:
                        if st.button(topic_example, key=f"example_{i}"):
                            # Set the topic and trigger research immediately
                            st.session_state.suggested_topic = topic_example
                            st.session_state.auto_start_research = True
                            st.rerun()

if __name__ == "__main__":
    main()

