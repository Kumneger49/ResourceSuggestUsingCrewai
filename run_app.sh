#!/bin/bash

# ResourceSuggester AI - Streamlit App Launcher
echo "🔍 Starting ResourceSuggester AI..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 Installing Streamlit..."
    pip install streamlit
fi

# Start the Streamlit app
echo "🚀 Launching ResourceSuggester AI..."
echo "🌐 The app will open in your browser at http://localhost:8501"
echo "📝 Press Ctrl+C to stop the server"
echo ""

streamlit run streamlit_app.py
