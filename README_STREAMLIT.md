# 🔍 ResourceSuggester AI - Streamlit Web Interface

A beautiful, user-friendly web interface for the ResourceSuggester AI multi-agent research system. This application allows users to research any topic using AI agents that search the web, find YouTube videos, and create comprehensive summaries.

## 🚀 Features

- **🎯 Easy Topic Input**: Simple interface to enter research topics
- **🤖 AI-Powered Research**: Uses CrewAI agents for comprehensive research
- **🌐 Web Search**: Finds relevant websites and online resources
- **📺 YouTube Integration**: Discovers educational videos on your topic
- **📝 Smart Summaries**: Creates well-organized research summaries
- **💾 Download Results**: Export findings as Markdown or JSON
- **⚙️ Customizable Settings**: Adjust research depth and video count
- **🎨 Modern UI**: Beautiful, responsive design with progress tracking

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup Instructions

1. **Navigate to the project directory**
   ```bash
   cd /path/to/ResourceSuggester/resourcesuggest
   ```

2. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```

3. **Install Streamlit dependencies**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

4. **Set up your OpenAI API key**
   - Get an API key from [OpenAI](https://platform.openai.com/api-keys)
   - You'll enter it in the web interface

## 🚀 Running the Application

### Start the Streamlit App
```bash
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Alternative: Run with specific port
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 📖 How to Use

### 1. **Configure API Key**
   - In the sidebar, enter your OpenAI API key
   - The key is stored securely in the session

### 2. **Enter Research Topic**
   - Type your research topic in the main input field
   - Be specific for better results
   - Use example topics for inspiration

### 3. **Customize Settings** (Optional)
   - **Research Depth**: Choose from Quick Overview, Detailed Analysis, or Comprehensive Research
   - **Number of Videos**: Set how many YouTube videos to find (3-10)

### 4. **Start Research**
   - Click "🚀 Start Research" button
   - Watch the progress bar as AI agents work
   - Results will appear in organized tabs

### 5. **Review Results**
   - **📝 Summary**: Executive summary of findings
   - **🌐 Web Resources**: Recommended websites
   - **📺 Video Resources**: Educational YouTube videos

### 6. **Download Results**
   - Export as Markdown (.md) for documentation
   - Export as JSON for data processing

## 🎯 Example Topics

Try these example topics to get started:
- Machine Learning Fundamentals
- Climate Change Solutions
- Blockchain Technology
- Artificial Intelligence Ethics
- Sustainable Energy
- Data Science Career Path
- Cybersecurity Best Practices
- Digital Marketing Strategies

## 🔧 Configuration

### Environment Variables
You can also set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Customization
- Modify `streamlit_app.py` to change the UI design
- Adjust agent configurations in `src/resourcesuggest/crew.py`
- Update research parameters in the sidebar settings

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Make sure you're in the correct directory
   - Verify the virtual environment is activated
   - Check that all dependencies are installed

2. **API Key errors**
   - Ensure your OpenAI API key is valid
   - Check that you have sufficient credits
   - Verify the key is entered correctly in the sidebar

3. **YouTube scraper errors**
   - The app uses compatible versions of `youtube-search-python` and `httpx`
   - If issues persist, check the package versions

4. **Slow performance**
   - Research time depends on topic complexity
   - Check your internet connection
   - Verify OpenAI API response times

### Getting Help
- Check the console output for detailed error messages
- Verify all dependencies are correctly installed
- Ensure you're using the correct Python environment

## 📁 Project Structure

```
resourcesuggest/
├── streamlit_app.py              # Main Streamlit application
├── requirements_streamlit.txt    # Python dependencies for Streamlit
├── README_STREAMLIT.md          # This file
├── src/
│   └── resourcesuggest/
│       ├── crew.py              # CrewAI configuration
│       ├── main.py              # CLI version
│       └── tools/
│           └── custom_tool.py
└── .venv/                       # Virtual environment
```

## 🔒 Security Notes

- API keys are stored in session state (not saved to disk)
- Clear your browser cache when switching between different API keys
- Never commit API keys to version control

## 🚀 Deployment

### Local Development
```bash
streamlit run streamlit_app.py
```

### Production Deployment
For production deployment, consider:
- Using Streamlit Cloud
- Setting up proper environment variables
- Implementing user authentication
- Adding rate limiting

## 📄 License

This project is part of the ResourceSuggester AI system.

## 🤝 Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting new features
- Improving the UI/UX
- Adding new research capabilities

---

**Happy Researching! 🔍✨**
