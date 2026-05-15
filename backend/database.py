import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# ==========================================
# HOUR 2: MOCK EHR DATABASE
# ==========================================
MOCK_EHR = {
    "patient_123": {
        "appointments": [],
        "medications": ["Lisinopril 10mg"]
    }
}

def check_slots(date: str):
    return ["09:00 AM", "10:00 AM", "02:00 PM"]

def book_slot(patient_id: str, date: str, time: str):
    MOCK_EHR.setdefault(patient_id, {"appointments": []})
    MOCK_EHR[patient_id]["appointments"].append({"date": date, "time": time})
    return f"Appointment successfully booked for {date} at {time}."

# ==========================================
# HOUR 3: CHROMA DB RAG (Lab Terminology)
# ==========================================
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

lab_docs = [
    Document(page_content="HDL: High-density lipoprotein, often called 'good' cholesterol. Normal range is >40 mg/dL for men, >50 mg/dL for women.", metadata={"source_doc_id": "doc1"}),
    Document(page_content="LDL: Low-density lipoprotein, 'bad' cholesterol. Normal range <100 mg/dL.", metadata={"source_doc_id": "doc2"}),
    Document(page_content="A1C: Hemoglobin A1C test measures average blood sugar over 3 months. Normal <5.7%.", metadata={"source_doc_id": "doc3"}),
    Document(page_content="WBC: White Blood Cell count. Normal range 4,500 to 11,000 WBCs per microliter.", metadata={"source_doc_id": "doc4"}),
    Document(page_content="RBC: Red Blood Cell count. Normal range 4.7-6.1 million cells/mcL for men, 4.2-5.4 for women.", metadata={"source_doc_id": "doc5"}),
    Document(page_content="Platelets: Cell fragments for clotting. Normal range 150,000 to 450,000/mcL.", metadata={"source_doc_id": "doc6"}),
    Document(page_content="Hemoglobin: Protein in RBCs that carries oxygen. Normal 13.8-17.2 g/dL (men), 12.1-15.1 g/dL (women).", metadata={"source_doc_id": "doc7"}),
    Document(page_content="Hematocrit: Proportion of red blood cells. Normal 40.7-50.3% (men), 36.1-44.3% (women).", metadata={"source_doc_id": "doc8"}),
    Document(page_content="BUN: Blood Urea Nitrogen, measures kidney function. Normal range 7 to 20 mg/dL.", metadata={"source_doc_id": "doc9"}),
    Document(page_content="Creatinine: Waste product from muscles, measures kidney function. Normal 0.84 to 1.21 mg/dL.", metadata={"source_doc_id": "doc10"}),
]

vectorstore = Chroma.from_documents(documents=lab_docs, embedding=embeddings, collection_name="lab_kb")
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

def query_lab_kb(query: str):
    docs = retriever.invoke(query)
    return "\n".join([d.page_content for d in docs])

# ==========================================
# HOUR 5: MOCK SUPABASE ESCALATION QUEUE
# ==========================================
ESCALATION_QUEUE = []

def add_to_escalation_queue(patient_id: str, session_id: str, reason: str, risk_score: float, messages: list):
    ESCALATION_QUEUE.append({
        "patient_id": patient_id,
        "session_id": session_id,
        "reason": reason,
        "risk_score": risk_score,
        "status": "PENDING",
        "last_message": messages[-1].content if messages else ""
    })
