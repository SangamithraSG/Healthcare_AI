import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(layout="wide", page_title="Healthcare AI Dashboard")

st.title("Healthcare Agentic AI - Live Demo")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Patient Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Enter your medical request..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.spinner("AI is analyzing and validating safety..."):
            try:
                res = requests.post("http://127.0.0.1:8000/chat", json={
                    "session_id": "sess_demo_1",
                    "patient_id": "patient_123",
                    "message": prompt
                }).json()
                ai_reply = res.get("response", "Error reading response.")
            except Exception as e:
                ai_reply = f"System Error: {str(e)}"
                
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.markdown(ai_reply)

with col2:
    st.header("Staff Escalation Queue (Live)")
    
    if st.button("Refresh Queue"):
        st.rerun()
        
    try:
        res = requests.get("http://127.0.0.1:8000/escalations")
        queue = res.json().get("escalations", [])
    except:
        queue = []
        
    if not queue:
        st.success("Queue is empty. All patient inquiries auto-resolved safely.")
    else:
        for item in reversed(queue):
            with st.container():
                st.error(
                    f"**Patient ID:** {item['patient_id']} | **Risk Score:** {item['risk_score']}\n\n"
                    f"**Escalation Reason:** {item['reason']}\n\n"
                    f"**Patient Message:** {item['last_message']}"
                )
                st.markdown("---")
