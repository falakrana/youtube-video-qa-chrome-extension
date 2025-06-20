# YouTube Video Q&A Chatbot

## Overview
This project is a YouTube Video Question Answering system that allows users to ask questions about the content of YouTube videos. The system extracts the video transcript, processes it using natural language processing techniques, and provides accurate answers to user queries based on the video content.

## Features
- Extract transcripts from YouTube videos
- Process and understand video content using Google's Gemini AI
- Answer user questions based on the video content
- Chrome extension for easy access while watching videos
- Web interface for direct interaction
- Caching system for improved performance on repeated queries

## Technical Stack:
- **Backend**: Flask (Python)
- **AI Models**: Google Gemini (Gemini-1.5-flash)
- **Vector Database**: FAISS for semantic search
- **Frontend**:
    - Chrome Extension (HTML, CSS, JavaScript)
    - Web Interface (HTML, CSS, JavaScript)
- **Transcript Extraction**: youtube-transcript-api

## installation:
### Prerequistes:
- Python 3.8+
- html, css, js (for Chrome extension development)
- Google API key (for Gemini AI)

### Setup:
1. Clone the repository:
    git clone <repository-url>
    cd youtube-qa-chatbot
2. Install Python dependencies:
    pip install -r requirements.txt
3. Create a `.env` file in the root directory and add your Google API key:
    GOOGLE_API_KEY=your_api_key_here
4. For Chrome extension:
    - Open Chrome and navigate to `chrome://extensions/`
    - Enable "Developer mode"
    - Click "Load unpacked" and select the directory containing the extension files

## Usage:
1. Nagivate to your youtube video.
2. Click the extension icon in your browser toolbar
3. Type your question in the popup
4. Click "Ask Question" to get the answer based on the current video


## Limitation:
Video should contain transcript.
