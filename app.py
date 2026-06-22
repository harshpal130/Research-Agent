import streamlit as st
import sys
import os
import time
from io import StringIO

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    border: 1px solid #2a2a4a;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.hero p {
    color: #94a3b8;
    font-size: 1.05rem;
    margin: 0;
    font-weight: 300;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Pipeline steps ── */
.pipeline-bar {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
    align-items: center;
}
.step-pill {
    flex: 1;
    background: #1e1e2e;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    text-align: center;
    font-size: 0.78rem;
    font-weight: 500;
    color: #64748b;
    position: relative;
    transition: all 0.3s;
}
.step-pill.active {
    background: rgba(99,102,241,0.15);
    border-color: #6366f1;
    color: #a5b4fc;
}
.step-pill.done {
    background: rgba(34,197,94,0.1);
    border-color: rgba(34,197,94,0.4);
    color: #86efac;
}
.step-pill .icon { font-size: 1rem; display: block; margin-bottom: 0.2rem; }
.arrow { color: #2a2a4a; font-size: 1.2rem; }

/* ── Result cards ── */
.result-card {
    background: #0f0f1a;
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
}
.result-card.search  { border-left: 3px solid #6366f1; }
.result-card.scrape  { border-left: 3px solid #f59e0b; }
.result-card.report  { border-left: 3px solid #10b981; }
.result-card.critic  { border-left: 3px solid #f43f5e; }

.card-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.label-search { color: #818cf8; }
.label-scrape  { color: #fbbf24; }
.label-report  { color: #34d399; }
.label-critic  { color: #fb7185; }

.card-content {
    font-size: 0.88rem;
    line-height: 1.7;
    color: #cbd5e1;
    font-family: 'Inter', sans-serif;
    white-space: pre-wrap;
    max-height: 320px;
    overflow-y: auto;
}
.card-content::-webkit-scrollbar { width: 4px; }
.card-content::-webkit-scrollbar-track { background: transparent; }
.card-content::-webkit-scrollbar-thumb { background: #2a2a4a; border-radius: 4px; }

/* ── Input area ── */
.stTextInput > div > div > input {
    background: #1e1e2e !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-size: 1rem !important;
    padding: 0.9rem 1.2rem !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: #475569 !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ── Status log ── */
.log-box {
    background: #0a0a12;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #64748b;
    max-height: 160px;
    overflow-y: auto;
    margin-bottom: 1.5rem;
}
.log-line { margin: 0.15rem 0; }
.log-line.info  { color: #64748b; }
.log-line.ok    { color: #34d399; }
.log-line.warn  { color: #fbbf24; }
.log-line.active { color: #a5b4fc; }

/* ── Report export ── */
.stDownloadButton > button {
    background: #1e1e2e !important;
    border: 1px solid #2a2a4a !important;
    color: #94a3b8 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
.stDownloadButton > button:hover {
    border-color: #6366f1 !important;
    color: #a5b4fc !important;
}

/* Error box */
.err-box {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #fca5a5;
    font-size: 0.88rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render pipeline bar ───────────────────────────────────────────────
def render_pipeline(active_step: int, done_steps: list):
    steps = [
        ("🔍", "Search"),
        ("📄", "Scrape"),
        ("✍️", "Write"),
        ("🧐", "Critique"),
    ]
    pills = ""
    for i, (icon, label) in enumerate(steps, start=1):
        if i in done_steps:
            cls = "done"
        elif i == active_step:
            cls = "active"
        else:
            cls = ""
        pills += f'<div class="step-pill {cls}"><span class="icon">{icon}</span>{label}</div>'
        if i < len(steps):
            pills += '<span class="arrow">›</span>'

    st.markdown(f'<div class="pipeline-bar">{pills}</div>', unsafe_allow_html=True)


# ── Helper: result card ───────────────────────────────────────────────────────
def result_card(kind: str, label: str, content: str):
    st.markdown(f"""
    <div class="result-card {kind}">
        <div class="card-label label-{kind}">{label}</div>
        <div class="card-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">Multi-Agent System</div>
    <h1>🔬 Research Pipeline</h1>
    <p>Autonomous search → scrape → write → critique — powered by your agent network.</p>
</div>
""", unsafe_allow_html=True)


# ── Input row ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        label="topic",
        label_visibility="collapsed",
        placeholder="Enter a research topic  e.g.  'Quantum computing breakthroughs 2025'",
    )
with col2:
    run_btn = st.button("▶  Run Pipeline")


# ── Session state ─────────────────────────────────────────────────────────────
if "state" not in st.session_state:
    st.session_state.state = {}
if "logs" not in st.session_state:
    st.session_state.logs = []
if "running" not in st.session_state:
    st.session_state.running = False


# ── Pipeline execution ────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.session_state.state = {}
    st.session_state.logs = []
    st.session_state.running = True

    # Add pipeline directory to path so imports resolve
    pipeline_dir = os.path.dirname(os.path.abspath(__file__))
    if pipeline_dir not in sys.path:
        sys.path.insert(0, pipeline_dir)

    try:
        from agent import build_reader_agent, build_search_agent, critic_chain, writer_chain
    except ImportError as e:
        st.markdown(f'<div class="err-box">❌ <b>Import error:</b> {e}<br>Make sure <code>app.py</code> is in the same folder as <code>agent.py</code>.</div>', unsafe_allow_html=True)
        st.stop()

    # ── Step indicators ───────────────────────────────────────────────────────
    pipeline_placeholder = st.empty()
    log_placeholder      = st.empty()

    def add_log(msg: str, kind: str = "info"):
        ts = time.strftime("%H:%M:%S")
        st.session_state.logs.append((ts, msg, kind))
        lines = "".join(
            f'<div class="log-line {k}">[{t}]  {m}</div>'
            for t, m, k in st.session_state.logs
        )
        log_placeholder.markdown(f'<div class="log-box">{lines}</div>', unsafe_allow_html=True)

    done = []

    # ── STEP 1 · Search ───────────────────────────────────────────────────────
    pipeline_placeholder.empty()
    with pipeline_placeholder:
        render_pipeline(active_step=1, done_steps=done)

    add_log("Initialising search agent…", "active")
    with st.spinner("🔍 Search agent working…"):
        try:
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            st.session_state.state["search_result"] = search_result["messages"][-1].content
            add_log("Search agent finished.", "ok")
        except Exception as e:
            add_log(f"Search failed: {e}", "warn")
            st.markdown(f'<div class="err-box">❌ <b>Step 1 failed:</b> {e}</div>', unsafe_allow_html=True)
            st.stop()

    done.append(1)

    # ── STEP 2 · Scrape ───────────────────────────────────────────────────────
    pipeline_placeholder.empty()
    with pipeline_placeholder:
        render_pipeline(active_step=2, done_steps=done)

    add_log("Reader agent picking best URL…", "active")
    with st.spinner("📄 Reader agent scraping…"):
        try:
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [(
                    "user",
                    f"Based on the following search result about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search result:\n{st.session_state.state['search_result'][:800]}"
                )]
            })
            st.session_state.state["scraped_content"] = reader_result["messages"][-1].content
            add_log("Scraping complete.", "ok")
        except Exception as e:
            add_log(f"Scraping failed: {e}", "warn")
            st.markdown(f'<div class="err-box">❌ <b>Step 2 failed:</b> {e}</div>', unsafe_allow_html=True)
            st.stop()

    done.append(2)

    # ── STEP 3 · Write ────────────────────────────────────────────────────────
    pipeline_placeholder.empty()
    with pipeline_placeholder:
        render_pipeline(active_step=3, done_steps=done)

    add_log("Writer drafting report…", "active")
    with st.spinner("✍️ Writer composing report…"):
        try:
            research_combined = (
                f"SEARCH RESULT:\n{st.session_state.state['search_result']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{st.session_state.state['scraped_content']}"
            )
            st.session_state.state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined,
            })
            add_log("Report drafted.", "ok")
        except Exception as e:
            add_log(f"Writer failed: {e}", "warn")
            st.markdown(f'<div class="err-box">❌ <b>Step 3 failed:</b> {e}</div>', unsafe_allow_html=True)
            st.stop()

    done.append(3)

    # ── STEP 4 · Critique ─────────────────────────────────────────────────────
    pipeline_placeholder.empty()
    with pipeline_placeholder:
        render_pipeline(active_step=4, done_steps=done)

    add_log("Critic reviewing report…", "active")
    with st.spinner("🧐 Critic reviewing…"):
        try:
            st.session_state.state["feedback"] = critic_chain.invoke({
                "report": st.session_state.state["report"]
            })
            add_log("Critique done. Pipeline complete ✓", "ok")
        except Exception as e:
            add_log(f"Critic failed: {e}", "warn")
            st.markdown(f'<div class="err-box">❌ <b>Step 4 failed:</b> {e}</div>', unsafe_allow_html=True)
            st.stop()

    done.append(4)

    pipeline_placeholder.empty()
    with pipeline_placeholder:
        render_pipeline(active_step=0, done_steps=done)

    st.session_state.running = False

elif run_btn and not topic.strip():
    st.warning("Please enter a research topic first.")


# ── Results display ───────────────────────────────────────────────────────────
state = st.session_state.state

if state:
    st.markdown("---")
    st.markdown("### 📊 Pipeline Results")

    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📄 Scraped", "✍️ Report", "🧐 Critique"])

    with tab1:
        if "search_result" in state:
            result_card("search", "Search Agent Output", state["search_result"])

    with tab2:
        if "scraped_content" in state:
            result_card("scrape", "Reader Agent — Scraped Content", state["scraped_content"])

    with tab3:
        if "report" in state:
            result_card("report", "Writer Chain — Final Report", state["report"])
            st.download_button(
                label="⬇  Download Report (.txt)",
                data=state["report"],
                file_name="research_report.txt",
                mime="text/plain",
            )

    with tab4:
        if "feedback" in state:
            result_card("critic", "Critic Chain — Review & Feedback", state["feedback"])