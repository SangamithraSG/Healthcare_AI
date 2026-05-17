# Healthcare Agentic AI: Hackathon Submission

This document strictly addresses the 5 mandatory steps of the hackathon problem statement, demonstrating how our built MVP perfectly aligns with the required outcomes.

---

## STEP 1 | Understand the Problem

The current system relies heavily on manual human intervention for routine tasks, creating a massive bottleneck. The stakeholders and their pain points are:

1. **The Patient:** Experiences extreme anxiety and frustration waiting on hold or waiting days for responses regarding simple lab definitions or appointment scheduling.
2. **The Healthcare Staff (Nurses/Doctors):** Suffer from severe burnout and "alert fatigue." Spending hours answering repetitive administrative questions pulls them away from critical patient care.
3. **The Healthcare Organization:** Faces lost revenue from missed appointments, declining patient satisfaction scores, and the constant looming threat of HIPAA/compliance violations.

**The Risk of Inaction:** If this is not solved, the human cost is a degradation in the quality of care due to staff burnout. The risk to patient safety is high: critical health queries get buried under thousands of routine queries, causing fatal delays in emergency responses.

---

## STEP 2 | Define the Problem Statement

**How Might We** build an intelligent, fail-safe triage system 
**for** overwhelmed healthcare providers and anxious patients 
**so that** we can instantly auto-resolve routine administrative inquiries, while guaranteeing that 100% of critical or diagnostic medical questions are securely escalated to a human without violating clinical compliance?

---

## STEP 3 | Design the Agent System

Our MVP implements a **Deterministic Multi-Agent State Machine** (built on LangGraph) rather than a traditional chatbot. 

* **The Orchestrator (`orchestrator_node`):** Powered by an ultra-fast LLM (`llama-3.1-8b-instant`). It acts as the traffic cop. It reads the input, calculates a baseline `risk_score`, classifies the intent, and routes it to the correct domain agent.
* **The Appointment Agent (`appointment_node`):** A specialized agent equipped with tools to query an Electronic Health Record (EHR) database. It verifies availability and books slots without hallucinating times.
* **The Lab Report Agent (`lab_report_node`):** A specialized agent that uses Retrieval-Augmented Generation (RAG). It is equipped with ChromaDB and HuggingFace local embeddings to define complex medical terminology strictly based on pre-approved medical documents.
* **The Escalation Logic (`escalate_node`):** At any point, if the system detects high risk (via the Risk Engine regex or the Safety Agent), the AI's response is killed. The system routes the session to the `escalate_node`, which instantly pushes the patient's context, risk score, and reason for failure to a real-time Staff Dashboard (built in Streamlit). 

---

## STEP 4 | Define the Guardrails

Healthcare requires a "Fail-Closed" architecture. We implemented an impassable **Safety/Compliance Firewall** (`safety_node`) powered by a heavy reasoning model (`llama-3.3-70b-versatile`). *Every* drafted response must pass this node before reaching the patient.

**Actions an agent must NEVER take:**
* Make a definitive medical diagnosis.
* Instruct a patient to alter, start, or stop a medication.
* Interpret a lab value's meaning regarding the patient's health status (e.g., "Your HDL is low, you might have heart disease").

**Constraints & Hard Stops:**
* **Emergency Regex Hard Stop:** If a user types words like "chest pain" or "suicide," the system bypasses all LLMs, instantly hard-stops, and escalates to a human.
* **Data Privacy:** Cross-session data leakage is blocked by strict state-scoping.
* **Mandatory Citations:** Factual clinical claims must cite the source document.

**Why this is critical:** An LLM hallucinating a diagnosis is a fatal liability. By enforcing a 7-step clinical rubric at the end of the pipeline, we ensure the hospital is legally protected and the patient is clinically safe.

---

## STEP 5 | Monitoring and Success Metrics

We integrated **LangSmith** as our end-to-end monitoring and observability layer.

**What is monitored and logged in production?**
* Every single node execution, token usage, and latency is mapped visually.
* Any time the Safety Agent blocks a response, the exact reasoning (e.g., "Violated Rule 2: Diagnostic Claim") is logged in the database and displayed on the Staff Dashboard.

**Detecting Violations:** Compliance violations aren't detected *after* the fact; they are detected *synchronously* by the Safety Firewall, which prevents the unsafe output from ever being transmitted over the network to the patient's device.

**4 Specific Success Metrics:**
1. **Auto-Resolution Rate:** The percentage of Level-1 queries (appointments, simple definitions) completely resolved without human intervention (Target: >60%).
2. **Average Resolution Time:** Reduction in patient wait time for administrative queries (Target: Reduction from hours to < 3 seconds).
3. **Safety Interception Rate:** The percentage of high-risk diagnostic questions successfully caught, blocked, and escalated by the Safety Firewall (Target: 100%).
4. **Staff Time Saved:** The reduction in hours spent by nurses/doctors processing the administrative queue per week (Target: >20 hours/week per staff member).
