import os
import streamlit as st
from dotenv import load_dotenv
from chat_handler import ChatHandler
from templates import get_available_templates, render_template_html
from exporters import export_pdf_from_html, export_docx_from_data

load_dotenv()
st.set_page_config(page_title="AI Resume Builder", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

def normalize_resume(d):
    """Ensure all keys exist and types are what templates expect."""
    d = dict(d or {})
    d.setdefault("name", "")
    d.setdefault("title", "")
    d.setdefault("summary", "")
    d.setdefault("contact", {})
    d.setdefault("experience", [])
    d.setdefault("education", [])
    d.setdefault("skills", {})

    # contact defaults
    c = d["contact"] = dict(d["contact"] or {})
    for k in ("email","phone","location","linkedin","github"):
        c.setdefault(k, "")

    # experience list sanity
    fixed_exp = []
    for e in d["experience"]:
        e = dict(e or {})
        e.setdefault("title","")
        e.setdefault("company","")
        e.setdefault("location","")
        e["start_date"] = (e.get("start_date") or "").strip()
        e["end_date"]   = (e.get("end_date") or "").strip() or "Present"
        # bullets/technologies lists
        b = e.get("bullets")
        if b is None and e.get("description"):
            b = [e["description"]]
        if not isinstance(b, list): b = [str(b)] if b else []
        e["bullets"] = b
        t = e.get("technologies")
        if not isinstance(t, list): t = [str(t)] if t else []
        e["technologies"] = t
        fixed_exp.append(e)
    d["experience"] = fixed_exp

    # education list sanity
    fixed_edu = []
    for e in d["education"]:
        e = dict(e or {})
        for k in ("school","degree","location","start_date","end_date"):
            e.setdefault(k,"")
        det = e.get("details")
        if not isinstance(det, list): det = [str(det)] if det else []
        e["details"] = det
        fixed_edu.append(e)
    d["education"] = fixed_edu

    # skills dict sanity
    sk = d["skills"] = dict(d["skills"] or {})
    for k in ("design","frontend","backend","data_ai","tools","other"):
        v = sk.get(k)
        if not isinstance(v, list): sk[k] = [str(v)] if v else []
    return d

# ---------- TITLE ----------

# ---------- CSS ----------
st.markdown("""
<style>
/* Page background */
html, body, .stApp, .main { background: #87CEEB !important; }

/* Make top split full-height */
[data-testid="stHorizontalBlock"] { height: 100vh !important; }
[data-testid="column"] > div { height: 100vh !important; display:flex; flex-direction:column; }

/* ===== LEFT COLUMN STYLING (applied to the real column div that has .left-anchor) ===== */
[data-testid="column"] > div:has(> .left-anchor) {
  position: relative;
  background:#f3f4f7;                 /* lane color */
  border-right:2px solid #dcdfe3;
  padding-left:40px;
  padding-top:70px;                    /* space for title bar if you use it */
}

/* Chat window inside left column */
.chat-window {
  flex:1;
  margin-top:20px;
  width:85%;
  border-radius:20px;
  background:#fff;
  border:1px solid #d9dee2;           /* thin outline */
  box-shadow:0 4px 8px rgba(0,0,0,0.05);
  overflow:hidden;
  display:flex; flex-direction:column;
  max-height: calc(100vh - 200px);    /* Fixed max height: screen height minus space for input */
}
.chat-scroll { 
  flex:1; 
  overflow-y:auto; 
  padding:24px 28px; 
  max-height: calc(100vh - 280px);    /* Scrollable area with fixed max height */
}

/* Pinned input: style the real Streamlit container that holds the form using an anchor */
[data-testid="stElementContainer"]:has(> .chat-input-anchor) {
  position: fixed;                     /* truly fixed to viewport bottom-left */
  bottom: 24px;
  left: 60px;
  width: 36vw;
  background: #fff;
  border: 1px solid #d9dee2;
  border-radius: 24px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  padding: 6px 10px;
  display: flex; align-items: center; gap: 10px;
  z-index: 1000;
}
[data-testid="stElementContainer"]:has(> .chat-input-anchor) input[type="text"]{
  border:none !important; outline:none !important; background:#f3f5f7; border-radius:18px;
  padding:10px 12px; font-size:14px; flex:1; color:#333;
}
[data-testid="stElementContainer"]:has(> .chat-input-anchor) .stButton > button{
  background:#007AFF; color:#fff; border:none; border-radius:50%; width:36px; height:36px;
  font-size:16px; font-weight:700; padding:0; box-shadow:0 2px 6px rgba(0,0,0,0.18); cursor:pointer;
}

/* Chat bubbles */
.msg{ max-width:75%; padding:10px 14px; border-radius:18px; margin:6px 0; font-size:14px; line-height:1.4; word-wrap:break-word;}
.user{ margin-left:auto; background:#007AFF; color:#fff; border-bottom-right-radius:4px;}
.bot { margin-right:auto; background:#E5E5EA; color:#000; border-bottom-left-radius:4px;}

/* Auto-scroll to bottom for new messages */
.chat-scroll {
  scroll-behavior: smooth;
}

/* Typing animation */
.typing-indicator {
    margin-right: auto;
    background: #E5E5EA;
    color: #000;
    border-bottom-left-radius: 4px;
    padding: 10px 14px;
    max-width: 75%;
    border-radius: 18px;
    margin: 6px 0;
}

.typing-dots {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.typing-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #999;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }
.typing-dot:nth-child(3) { animation-delay: 0s; }

@keyframes typing {
    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

/* ===== RIGHT COLUMN: RESUME PAGE ===== */
/* Style the column that has the right anchor */
[data-testid="column"] > div:has(> .right-anchor) {
  display:flex; flex-direction:column; padding-top:70px;
}

/* Style the container that holds the doc anchor + the iframe (st.components) */
[data-testid="stElementContainer"]:has(> .doc-anchor) {
    flex:1; display:flex; justify-content:center; align-items:flex-start;
    overflow:auto; background:#fff; padding:24px;
}

        /* Style the inner component container (the one st.components creates) - PDF-like document */
        [data-testid="stElementContainer"]:has(> .doc-anchor) > div:nth-child(2) {
          width:816px !important;                          /* letter width at ~96dpi (8.5 inches) */
          height:1056px !important;                       /* letter height at ~96dpi (11 inches) */
          background:#fff !important;
          border:2px solid #333 !important;                /* thick black border like a document */
          border-radius:8px !important;
          box-shadow:0 8px 32px rgba(0,0,0,0.15) !important;
          overflow:hidden !important;
          position: relative !important;
        }
        
        /* Force iframe content to have white background */
        [data-testid="stElementContainer"]:has(> .doc-anchor) iframe {
          background:#fff !important;
        }

/* Add document-like styling */
[data-testid="stElementContainer"]:has(> .doc-anchor) > div:nth-child(2)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #e74c3c 0%, #f39c12 25%, #f1c40f 50%, #2ecc71 75%, #3498db 100%);
  z-index: 1;
}

        /* Ensure the iframe fills that "page" */
        [data-testid="stElementContainer"]:has(> .doc-anchor) iframe {
          width:100% !important;
          height:1056px !important;             /* exactly 11 inches at 96dpi */
          background:#fff !important;
          border: none !important;
        }

        /* Alternative selector for the resume container */
        .stIFrame {
          border: 2px solid #333 !important;
          border-radius: 8px !important;
          box-shadow: 0 8px 32px rgba(0,0,0,0.15) !important;
        }

        /* Target the iframe container more directly */
        [data-testid="stIFrame"] {
          border: 2px solid #333 !important;
          border-radius: 8px !important;
          box-shadow: 0 8px 32px rgba(0,0,0,0.15) !important;
        }

/* Fixed site title */
.title-bar{
  position:fixed; top:0; left:0; width:100%;
  padding:16px 40px; background:#fff; border-bottom:1px solid #d9dee2;
  font-size:22px; font-weight:700; z-index:9999; box-shadow:0 1px 4px rgba(0,0,0,0.06);
  color: #333;
}
</style>
""", unsafe_allow_html=True)


# ---------- INIT STATE FIRST ----------
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
             "content": "Hi! I’m your AI resume assistant. Tell me about your background, work experience, and skills. I’ll build your resume and ask for any missing pieces."}
        ]
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = {
            "name": "",
            "title": "",
            "contact": {"email": "", "phone": "", "location": "", "linkedin": "", "github": ""},
            "summary": "",
            "experience": [],
            "education": [],
            "skills": {"design": [], "frontend": [], "backend": [], "data_ai": [], "tools": [], "other": []}
        }
    if "selected_template" not in st.session_state:
        st.session_state.selected_template = "Modern Clean"
    if "chat_handler" not in st.session_state:
        st.session_state.chat_handler = ChatHandler()

init_state()

# ---------- SPLIT LAYOUT ----------
# Title - using st.title instead of custom HTML
st.title("🤖 AI Resume Builder")

col_left, col_right = st.columns([1,1], gap="small")

# ===== LEFT COLUMN =====
with col_left:
    # Anchor the column so CSS can style this real container
    st.markdown('<span class="left-anchor"></span>', unsafe_allow_html=True)

    # Build chat window as ONE markdown block so messages are truly nested
    from html import escape
    chat_html = '<div class="chat-window"><div class="chat-scroll">'
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "bot"
        content = escape(m["content"]).replace("\n", "<br>")
        chat_html += f'<div class="msg {role}">{content}</div>'
    
    # No typing indicator for now - using immediate responses
    
    chat_html += '</div></div>'
    
    # Add JavaScript to auto-scroll to bottom and handle Enter key
    chat_html += '''
    <script>
    // Auto-scroll to bottom when new messages are added
    function scrollToBottom() {
        const chatScroll = document.querySelector('.chat-scroll');
        if (chatScroll) {
            chatScroll.scrollTop = chatScroll.scrollHeight;
        }
    }
    
    // Scroll to bottom on page load and when messages change
    window.addEventListener('load', scrollToBottom);
    setTimeout(scrollToBottom, 100); // Small delay to ensure content is rendered
    
    // Handle Enter key to submit form
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            // Find the text area and submit button
            const textArea = document.querySelector('textarea[placeholder*="product designer"]');
            const submitButton = document.querySelector('button[type="submit"]');
            
            if (textArea && submitButton && textArea.value.trim()) {
                event.preventDefault();
                submitButton.click();
            }
        }
    });
    </script>
    '''
    
    st.markdown(chat_html, unsafe_allow_html=True)

    # Pinned input: container + hidden anchor so CSS grabs this parent
    input_box = st.container()
    with input_box:
        st.markdown('<span class="chat-input-anchor"></span>', unsafe_allow_html=True)
        with st.form("chat_form", clear_on_submit=True):
            c_text, c_btn = st.columns([6, 1])
            with c_text:
                user_text = st.text_area("Type your message…", label_visibility="collapsed",
                                        placeholder="I'm a product designer who led a mobile redesign at…",
                                        key="user_input_text", height=40, 
                                        help="Press Enter to send (Shift+Enter for new line)")
            with c_btn:
                send = st.form_submit_button("➤")
            if send and user_text.strip():
                # Add user message immediately
                st.session_state.messages.append({"role":"user","content":user_text.strip()})
                
                # Process AI response (no intermediate rerun)
                assistant_text, delta = st.session_state.chat_handler.process_message(user_text, st.session_state.resume_data)
                if delta:
                    # Simple update: replace the fields that changed
                    for k, v in delta.items():
                        st.session_state.resume_data[k] = v
                
                # Add AI response immediately
                st.session_state.messages.append({"role":"assistant","content":assistant_text or "Got it—what dates for that role?"})
                st.rerun()

# ===== RIGHT COLUMN =====
with col_right:
    # Anchor so CSS styles this real column container
    st.markdown('<span class="right-anchor"></span>', unsafe_allow_html=True)

    # Toolbar (normal Streamlit)
    c1, c2, c3, c4 = st.columns([2,2,1,1])
    with c1:
        templates = get_available_templates()
        st.session_state.selected_template = st.selectbox(
            "Template",
            options=list(templates.keys()),
            index=list(templates.keys()).index(st.session_state.get("selected_template","Modern Clean"))
        )
    with c2:
        st.caption("Download when you’re happy. The preview matches the export.")
    with c3:
        export_pdf = st.button("📄 PDF")
    with c4:
        export_docx = st.button("📝 DOCX")

    # Single-page "doc"
    safe_data = normalize_resume(st.session_state.resume_data)
    html = render_template_html(safe_data, st.session_state.selected_template)
    
    # Safety: if HTML is empty, show a tiny diagnostic
    if not html or not html.strip():
        st.warning("Template returned empty HTML. Showing raw data for debugging:")
        st.json(safe_data)
    else:
        doc_box = st.container()
        with doc_box:
            st.markdown('<span class="doc-anchor"></span>', unsafe_allow_html=True)
            st.components.v1.html(html, height=1056, scrolling=False)

    # Download buttons with proper formatting
    if export_pdf:
        # Get name for filename
        name = st.session_state.resume_data.get("name", "Resume")
        if name:
            # Format name for filename: "FirstName_LastName"
            name_parts = name.split()
            if len(name_parts) >= 2:
                filename = f"Resume_{name_parts[0]}_{name_parts[-1]}.pdf"
            else:
                filename = f"Resume_{name_parts[0]}.pdf"
        else:
            filename = "Resume.pdf"
        
        pdf_data = export_pdf_from_html(html)
        st.download_button("Download PDF", pdf_data, file_name=filename, mime="application/pdf")
    
    if export_docx:
        # Get name for filename
        name = st.session_state.resume_data.get("name", "Resume")
        if name:
            # Format name for filename: "FirstName_LastName"
            name_parts = name.split()
            if len(name_parts) >= 2:
                filename = f"Resume_{name_parts[0]}_{name_parts[-1]}.docx"
            else:
                filename = f"Resume_{name_parts[0]}.docx"
        else:
            filename = "Resume.docx"
        
        docx_data = export_docx_from_data(st.session_state.resume_data, st.session_state.selected_template)
        st.download_button("Download DOCX", docx_data, file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
