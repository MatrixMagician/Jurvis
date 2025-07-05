# Jurvis

An AI agent powered by Google Gemini that can interact with your local file system. Jurvis gives you a secure way to let AI scan directories, read files, modify content, and execute Python scripts - all from a chat interface.

## What it does

Jurvis is your local AI assistant that can:
- 📁 Scan files and directories 
- 📖 Read file contents
- ✏️ Overwrite files with new content
- 🐍 Execute Python scripts using the interpreter

Perfect for developers and AI enthusiasts who want to experiment with AI agents that can actually interact with their local environment.

## Requirements

- Python 3.10 or higher
- Unix-like shell (zsh, bash, etc.)
- Linux, Windows, or macOS
- Google Gemini API key

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/jurvis.git
cd jurvis
```

### 2. Install uv package manager
Follow the installation instructions at: https://github.com/astral-sh/uv

### 3. Set up the virtual environment
```bash
uv venv
```

### 4. Install dependencies
```bash
uv add google-genai==1.12.1
uv add python-dotenv==1.1.0
```

### 5. Get your Gemini API key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Create a `.env` file in the project root:
```
GEMINI_API_KEY="your_api_key_here"
```

## Usage

Run Jurvis from the project directory:

```bash
# Using uv (recommended)
uv run main.py

# Or using Python directly
python3 main.py
```

That's it! Start chatting with Jurvis and ask it to help with your files and code.

## Security Note

Jurvis operates within a pre-defined local directory for security. It won't have access to your entire system - just the directory you specify.

## Built With

- Python 3.10+
- Google Gemini API
- uv package manager