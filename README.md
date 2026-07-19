# AI-News-Agent

An intelligent news automation system powered by Large Language Models (LLM).

AI-News-Agent automatically crawls news articles, analyzes content with AI models, and generates structured news reports.

---

# Features

## Automated News Crawling

Supported sources:

- BBC Chinese
- AIBase

Technologies:

- Requests
- BeautifulSoup
- Playwright


The system can automatically:

- Collect news titles
- Extract article URLs
- Crawl article content
- Store news data


---

## AI-Powered News Analysis

Supports:

- DeepSeek API
- Qwen API
- OpenAI Compatible API


AI automatically generates:

- News summaries
- Importance scores
- Categories
- Keywords extraction


Output formats:

- SQLite database storage
- Markdown news reports


---

## Database

Using:

- SQLite


Stored information:

- News title
- URL
- Source
- Publication time
- Article content
- AI summary
- Keywords
- Category


---

## Web Dashboard

Provides:

- News browsing interface
- AI analysis results
- News API service


Technologies:

- FastAPI
- SQLite


---

# Project Structure


```text
AI-News-Agent

├── crawler              News crawling module
│
├── summary              AI summarization module
│
├── web                  Web interface and API
│
├── data                 Data storage
│
├── scheduler.py         Automated task scheduler
│
├── requirements.txt     Python dependencies
│
└── README.md
```

# Installation
1. Clone Repository
git clone https://github.com/jeams11/AI-News-Agent.git

cd AI-News-Agent
2. Create Virtual Environment

Create an isolated Python environment:

python3 -m venv venv

Activate virtual environment:

source venv/bin/activate
3. Install Dependencies

Install required Python packages:

pip install -r requirements.txt

Install Playwright browser:

playwright install chromium
Usage
1. News Crawling

Enter crawler directory:

cd crawler

Run BBC crawler:

python bbc.py

Run AIBase crawler:

python aibase.py
2. AI News Summarization

Enter summary directory:

cd summary

Run AI summarization:

python summarize.py

Generated output:

news_report.md
3. Web Service

Start web server:

python web/app.py

Open browser:

http://127.0.0.1:8000
Automated Tasks

AI-News-Agent includes an automated scheduler.

The scheduler automatically performs:

News crawling every hour
AI news summarization every 12 hours

Run scheduler:

python scheduler.py
| Technology      | Purpose                   |
| --------------- | ------------------------- |
| Python          | Core programming language |
| Playwright      | Browser automation        |
| BeautifulSoup   | HTML parsing              |
| SQLite          | Database storage          |
| FastAPI         | Web API framework         |
| OpenAI SDK      | LLM integration           |
| Qwen / DeepSeek | AI news analysis          |
