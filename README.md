# 🎧 Sales Call AI (Ollama Powered)

AI-powered Sales Call Assistant that transcribes customer & salesperson audio,
performs **speaker diarization**, **intent detection**, **sentiment analysis**,
**entity extraction**, and gives **real-time AI sales suggestions** like:
- Next questions to ask
- Objection handling
- Product recommendations
- Auto-replies

Built using Streamlit, NLP, and Ollama (Local LLM) to assist sales agents with real-time AI-driven conversation intelligence.


---

## 🚀 Features

- 🎙️ Audio Upload (WAV / MP3)
- 🎤 Live Browser Audio Recording
- 🧠 Speaker Diarization (Customer vs Salesperson)
- 📝 Speech-to-Text (STT)
- 📊 Intent, Sentiment & Entity Extraction
- 🤖 AI Suggestions:
  - Next Question (3 options)
  - Objection Handling
  - Product Recommendation
  - Auto Reply
- 📄 Downloadable Call Summary Report
- 🖥️ Clean, App-like Frontend UI

---

## 🧠 Tech Stack

- Python
- Streamlit
- Ollama (Local LLM)
- NLP (Rule + LLM based)
- Speech Recognition
- Speaker Diarization
- Whisper / Vosk (STT)

---




## ⚙️ Setup & Run

### 1️⃣ Clone Repository
```bash
git clone https://github.com/mitali2701/Real_time_sales_call_ai.git
cd sales_call_ai

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Install & Run Ollama

Download Ollama from: https://ollama.com

Verify installation:

ollama --version


Pull model:

ollama pull phi3:mini

5️⃣ Run Application
streamlit run app.py

## 🧪 Example Workflow

- Upload or record audio
- Generate transcript with speaker separation
- Customer dialogue analyzed using Ollama
- AI suggests:
  - Next questions
  - Objection handling
  - Product recommendations
- Continue conversation


📌 Use Cases

Sales call analysis

Customer support automation

Call center training

AI sales coaching

📜 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it.

🙌 Author

Mitali Doble
AI engineer

⭐ If you like this project, please star the repository!


