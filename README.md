# Healthcare Agentic AI MVP 

A **compliance-first, fail-closed Agentic AI system** designed to automate routine healthcare inquiries while absolutely guaranteeing patient safety. 

Traditional AI chatbots in healthcare are a massive liability because they hallucinate diagnoses and give dangerous medical advice. This system solves that problem by using a **Deterministic Multi-Agent State Machine**. It routes administrative tasks to highly constrained domain agents, and forces *every* single output through a strict **Safety Firewall** before it ever reaches the patient. If the AI detects a medical emergency or a potential compliance violation, it kills the response and securely routes the patient to a Human Escalation Queue.

**"AI assists, Humans decide."**

---

## 🌟 Key Features
- **Intelligent Orchestration:** A fast LLM (`llama-3.1-8b-instant`) classifies intent, calculates risk scores, and routes patient queries in milliseconds.
- **Domain Specialists:** Specialized agents capable of executing tool calls (e.g., querying mock EHR databases to book appointments).
- **Secure RAG:** A local ChromaDB instance utilizing HuggingFace embeddings (`all-MiniLM-L6-v2`) to pull verified definitions for lab terminology.
- **The Safety Firewall:** An impassable gateway powered by a heavy reasoning model (`llama-3.3-70b-versatile`). It evaluates every AI response against a strict 7-step clinical rubric (checking for diagnostic claims, medication directives, PHI leakage, etc.).
- **Live Escalation Dashboard:** A Streamlit split-screen UI where clinical staff can monitor escalated issues, risk scores, and the exact reasons the AI chose to block a response.
- **100% Observable:** Fully integrated with LangSmith for end-to-end tracing, auditing, and compliance logging.

---

## 🛠️ Architecture Stack
* **Language:** Python (FastAPI backend)
* **Agent Framework:** LangGraph / LangChain
* **Inference Engine:** Groq (Llama 3.1 & 3.3)
* **Vector Store:** ChromaDB
* **Embeddings:** Sentence-Transformers (Local HuggingFace)
* **UI/Frontend:** Streamlit
* **Telemetry:** LangSmith

---

## 🚀 How to Run Locally

Follow these steps to run the system on your local machine.

### 1. Clone the repository
```bash
git clone https://github.com/SangamithraSG/Healthcare_AI.git
cd Healthcare_AI
```

### 2. Set up your API Keys
You will need a free [Groq API Key](https://console.groq.com/) for fast LLM inference and a [LangSmith API Key](https://smith.langchain.com/) for trace observability.

Create a file named `.env` in the root directory of the project and add your keys:
```bash
# .env
GROQ_API_KEY="your_groq_api_key_here"
LANGCHAIN_API_KEY="your_langsmith_api_key_here"
```
*(Note: This `.env` file is safely ignored by git and will not be pushed to GitHub).*

### 3. Install Dependencies
It is highly recommended to use a virtual environment (`python -m venv venv` and `source venv/bin/activate`).
```bash
pip install -r requirements.txt
```

### 4. Run the Application
You can start both the FastAPI backend and the Streamlit UI simultaneously using the included shell script:
```bash
bash run.sh
```
Once the script is running, open your browser to **http://localhost:8501**.

---

## 🧪 Demo Scenarios to Try

Once the UI is running, try typing these specific prompts into the Patient Chat to see how the architecture responds:

### Scenario 1: Auto-Resolution (Low Risk)
* **Type:** `"I need to book an appointment for next Monday."`
* **Result:** The Orchestrator routes to the Appointment Agent, which securely books the 09:00 AM slot and replies instantly.

### Scenario 2: Secure Information Retrieval (Medium Risk)
* **Type:** `"What does HDL mean in my blood test?"`
* **Result:** The Orchestrator routes to the Lab Agent, which uses RAG to pull the clinical definition from the local vector database. It passes the Safety Firewall because it is purely informational.

### Scenario 3: The Safety Block & Escalation (High Risk)
* **Type:** `"My HDL is 30, does this mean I'm going to have a heart attack?"`
* **Result:** The AI attempts to answer, but the **Safety Firewall intercepts it**. It realizes answering this violates the "No Diagnostic Claims" rule. It blocks the AI, informs the patient they are being transferred, and instantly pushes the data to the Staff Escalation Queue (on the right side of the screen) with a high Risk Score.

