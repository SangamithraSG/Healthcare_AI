# Healthcare Agentic AI System

This repository contains the hackathon MVP for the Healthcare Agentic AI System, demonstrating a strict, compliance-first, multi-agent orchestrator for patient inquiries.

## Quickstart
1. Set environment variables:
   ```bash
   export GROQ_API_KEY="your_groq_api_key_here"
   export LANGCHAIN_API_KEY="your_langsmith_api_key_here"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   bash run.sh
   ```

## Included Scenarios for Demo:
- **Scenario 1:** Appointment Scheduling (Auto-resolve)
- **Scenario 2:** Lab Report Explanation (Assisted lookup via RAG)
- **Scenario 3:** Medical Advice / Diagnostics (Safety Agent hard stop & escalation)
