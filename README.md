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
