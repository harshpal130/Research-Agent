# 🔍 Research-Agent

An AI-powered Multi-Agent Research Assistant built using **LangChain**, **Mistral AI**, **Tavily Search**, and **Streamlit**.

🌐 Live Demo: https://research-agent0.streamlit.app/

---

## Features

### Search Agent
- Searches the web for recent and reliable information.
- Uses Tavily Search API for high-quality results.

### Reader Agent
- Identifies relevant sources from search results.
- Scrapes webpages for detailed content extraction.

### Writer Agent
- Generates structured research reports.
- Produces:
  - Introduction
  - Key Findings
  - Conclusion
  - Sources

### Critic Agent
- Reviews generated reports.
- Provides:
  - Quality Score
  - Strengths
  - Areas for Improvement
  - Final Verdict

---

## Tech Stack

- Python
- LangChain
- LangGraph / LCEL
- Mistral AI
- Tavily Search
- BeautifulSoup4
- Streamlit
- Pydantic

---

## Project Structure

```text
Research-Agent/
│
├── agent.py
├── pipeline.py
├── tools.py
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/<your-username>/Research-Agent.git
cd Research-Agent
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## Running Locally

### Streamlit App

```bash
streamlit run app.py
```

### Pipeline Script

```bash
python pipeline.py
```

---

## Workflow

```text
User Query
     │
     ▼
Search Agent
     │
     ▼
Reader Agent
     │
     ▼
Writer Agent
     │
     ▼
Critic Agent
     │
     ▼
Final Research Report
```

---

## Example Use Cases

- Market Research
- Technology Trends Analysis
- Academic Research Assistance
- Industry Reports
- Competitor Analysis
- News Summarization

---

## Future Improvements

- PDF Export
- Multi-source Content Aggregation
- Citation Generation
- Research Memory
- Agent Collaboration using LangGraph
- Report Versioning

---

## Live Demo

🔗 https://research-agent0.streamlit.app/

---

## Author

**Harsh**

Built with LangChain, Mistral AI, Tavily Search, and Streamlit.
