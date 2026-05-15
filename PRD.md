# Product Requirements Document (PRD)
## Healthcare Agentic AI System

**Version:** 1.0 (Hackathon MVP)
**Date:** May 2026
**Status:** MVP Completed

---

## 1. Executive Summary
The Healthcare Agentic AI System is an enterprise-grade, deterministic multi-agent orchestrator designed to handle patient inquiries. Unlike traditional chatbots that are prone to hallucination and non-compliant behavior, this system introduces a "Fail-Closed" architecture. It routes administrative and informational queries to specialized domain agents while enforcing a strict, mandatory **Safety/Compliance Firewall** on all outputs to ensure clinical safety and HIPAA compliance. 

## 2. Problem Statement
Healthcare providers face massive operational bottlenecks answering routine patient queries (appointments, lab definitions, prescription refills). However, deploying standard Generative AI in healthcare is dangerous; AI hallucinating a diagnosis or giving incorrect medication advice can lead to fatal outcomes and extreme legal liability. There is a need for a system that automates routine tasks but has the architectural constraints to explicitly refuse clinical interpretation and safely escalate to a human.

## 3. Product Vision
**"AI assists, Humans decide."**
To build the most trusted, compliance-first AI routing system for hospitals, where the AI serves as a hyper-efficient triage and administrative assistant that inherently knows its own limitations.

## 4. Target Personas
1. **The Patient:** Needs fast, 24/7 answers to routine questions, appointment bookings, and simple explanations of medical terminology.
2. **The Clinical Staff (Nurse/Doctor):** Needs an intelligent escalation queue that only flags them when human clinical judgment is strictly required, reducing their overall alert fatigue.
3. **The Compliance Officer:** Needs a deterministic, 100% auditable trail of every AI decision to ensure HIPAA and SOC2 compliance.

## 5. Core Features & Requirements

### 5.1 Orchestrator Agent (The Router)
* **Requirement:** Must interpret natural language input and classify the intent (e.g., Appointment, Lab Report, Emergency).
* **Requirement:** Must calculate a Risk Score (0.0 to 1.0) based on the intent and the presence of emergency keywords.
* **Requirement:** Must route the query to the correct specialized Domain Agent.

### 5.2 Domain Agents (The Specialists)
* **Appointment Agent:** Must be able to read available slots and securely book an appointment by executing deterministic tool calls to the EHR database.
* **Lab Report Agent:** Must use Retrieval-Augmented Generation (RAG) to define lab terminology by strictly referencing pre-approved clinical documents.

### 5.3 Safety/Compliance Agent (The Firewall)
* **Requirement:** *Non-negotiable.* Every single drafted AI response must pass through this node before reaching the patient.
* **Requirement:** Must evaluate the response against a strict 7-Step Clinical Rubric:
  1. No PII/PHI Leakage
  2. No Diagnostic Claims
  3. No Medication Directives
  4. No Lab Interpretation (defining is okay, interpreting health status is blocked)
  5. No Prompt Injection 
  6. Appropriate Confidence Thresholds
  7. Mandatory Citations for facts
* **Requirement:** If the response violates *any* rule, the agent must block the message and trigger a human escalation.

### 5.4 Escalation Queue (Staff Dashboard)
* **Requirement:** Must provide a real-time UI for clinical staff.
* **Requirement:** Escalated tickets must clearly display the Patient ID, the calculated Risk Score, the exact reason the Safety Firewall blocked the AI, and the patient's original message.

## 6. Technical Architecture & Tech Stack
* **Backend Framework:** Python / FastAPI
* **Agentic Framework:** LangGraph (Chosen for strict, deterministic state-machine routing)
* **LLM Provider:** Groq (`llama-3.3-70b-versatile` for heavy safety evaluation; `llama-3.1-8b-instant` for rapid orchestration routing).
* **Embeddings & Vector DB:** HuggingFace local embeddings (`all-MiniLM-L6-v2`) and ChromaDB for local, secure RAG operations.
* **Observability:** LangSmith for end-to-end trace logging and auditability.
* **Frontend:** Streamlit (Split-screen implementation for Demo purposes).

## 7. Non-Functional Requirements
* **Latency:** The Orchestrator routing must occur in < 500ms. The Safety evaluation must occur in < 800ms. Total round trip should not exceed 2.5 seconds.
* **Security & Privacy:** The architecture must support Row-Level Security (RLS) and scoped JWTs (designed in the backend architecture plan).
* **Auditability:** Every node execution must be recorded via LangChain tracing. 

## 8. Future Roadmap (Post-MVP)
* **Phase 1:** Integration with real HL7/FHIR EHR standards (Epic/Cerner).
* **Phase 2:** Deployment of a specialized Insurance Agent for real-time claims and coverage queries.
* **Phase 3:** Transition to fine-tuned, self-hosted open-source models (e.g., Llama-3-8B fine-tuned specifically on hospital compliance guidelines) to remove reliance on external API vendors and completely eliminate external data transit.
