🧠 Smart Companion
AI-Powered Task Management for Neurodivergent Minds

Smart Companion is an AI-assisted productivity app designed to help neurodivergent individuals (ADHD, Autism, Executive Dysfunction, etc.) break overwhelming tasks into tiny, manageable action steps.

It combines:

🎯 AI task breakdown using Ollama

🎤 Offline voice input using Vosk

🎨 Beautiful UI built with Streamlit

💾 Local persistence using SQLite

🚀 Features
🧠 Mood-Based AI Planning

Users select their current mood:

Calm 🙂

Low Energy 😴

Overwhelmed 😣

Motivated 🔥

The AI adapts the task breakdown accordingly:

Low energy → ultra tiny steps

Overwhelmed → calming starter steps

Motivated → efficient & productive steps

✨ AI Task Breakdown

Uses a local LLM (default: qwen2.5:7b)

Generates 10–12 short, physical action steps

Each step under 10 words

No fluff, only actionable instructions

🎤 Voice Input (Offline)

5-second voice recording

Speech-to-text using Vosk

No internet required

📊 Gamified Productivity

Points system

Streak tracking

Completed tasks counter

Progress bar

Celebration animation 🎉

💾 Data Export

View raw session data

Download progress as JSON

Local SQLite database support

⚙️ Tech Stack
Layer	Technology
Frontend	Streamlit
AI Engine	Ollama (Local LLM)
Default Model	qwen2.5:7b
Voice Recognition	Vosk + PyAudio
Database	SQLite
Backend Logic	Python
Styling	Custom CSS


🖥️ Installation Guide
1️⃣ Clone Repository
git clone https://github.com/your-username/smart-companion.git
cd smart-companion
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3️⃣ Install Requirements
pip install -r requirements.txt
4️⃣ Install & Run Ollama



Install Ollama:

ollama pull qwen2.5:7b
ollama serve

Make sure it runs at:

http://localhost:11434



5️⃣ Setup Vosk Model

Download an English model from the official Vosk site and:

Extract it

Rename folder to model

Place it in project root

6️⃣ Run the App
streamlit run app.py




🧩 How It Works
1️⃣ Mood Selection

User selects current emotional state.

2️⃣ Task Input

Type a task

Or record voice

3️⃣ AI Processing

llm_helper.py:

Builds a mood-adjusted prompt

Sends request to Ollama

Parses numbered response into list

4️⃣ Step Execution

Displays one step at a time

Updates progress

Awards points

5️⃣ Data Handling

Session state tracks live progress

SQLite optionally stores persistent data

JSON export available




🧠 Prompt Design Strategy

The system dynamically modifies prompts:

Example:

User Mood: Overwhelmed
Make steps calming, very simple, and non-demanding.

Rules enforced:

10–12 steps

Under 10 words each

Physical actions only

No conversational filler

🔐 Offline-First Design

Smart Companion works completely offline:

Local LLM via Ollama

Local speech recognition

Local database

No cloud APIs required

Perfect for:

Privacy-focused users

Hackathons

College projects

Personal productivity tools

🛠️ Future Improvements

🔔 Daily AI challenges

📅 Calendar integration

📱 Mobile version

🧠 Adaptive learning from user history

☁️ Optional cloud sync

🎯 XP leveling system improvements

🎓 Ideal For

Neurodivergent individuals

Students

Hackathon projects

AI + UX research

Executive function support tools

❤️ Credits

Built with 💗 by Team NeuralNodes

