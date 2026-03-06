# vectra - AI Prompt Refiner

Vectra is a Streamlit application that helps users transform simple ideas into powerful, well-structured prompts for various AI tools. It leverages Google's Gemini generative AI to refine user input and provide explanations for why the generated prompt works.

## 🚀 Features

- Converts plain English descriptions into detailed prompts for:
  - General AI assistants (ChatGPT, etc.)
  - Image generation tools (Midjourney, DALL·E, etc.)
  - Code generation tools (GitHub Copilot, CodeLlama, etc.)
  - Marketing content and copywriting
- Supports multiple tones/styles (Professional, Creative, Minimal, Cinematic, Friendly)
- Explanation generator that describes why the prompt structure is effective
- Secure API key handling using environment variables or Streamlit secrets

## 🛠️ Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Keshav1605/Vectra.git
   cd Vectra
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   . .venv/Scripts/Activate.ps1  # Windows PowerShell
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key:**
   - Local development: create a `.env` file in the project root with:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - Deployment: set `GEMINI_API_KEY` in your hosting environment or in Streamlit
     secrets (see below).

## 📦 Deployment

Vectra can be deployed on any platform that supports Python and Streamlit. For
Streamlit Cloud:

1. Push your code to GitHub (already done).
2. Create a new app on [streamlit.io/cloud](https://streamlit.io/cloud).
3. Connect the `Keshav1605/Vectra` repo and point to `app.py`.
4. Add the API key to **Secrets**:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
5. Deploy — the app will be available at a public URL.

## 🗂️ File Structure

```
Vectra/
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
├── app.py                # Main Streamlit application
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── .vscode/              # VSCode settings
```

## 🔐 Security Tips

- Never commit real API keys or `.env` files to Git.
- Use environment variables or secret management provided by your host.
- Rotate your API key if it ever becomes exposed.

## 🤝 Contributions

Feel free to open issues or submit pull requests! This is a small project meant
for learning and experimentation.

## 📄 License

This repository is provided as-is for demonstration purposes. No specific
license is attached; feel free to adapt the code for your own use.