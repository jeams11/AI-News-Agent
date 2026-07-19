# AI-News-Agent

An intelligent news automation system powered by Large Language Models (LLM).

AI-News-Agent automatically crawls news articles, analyzes content with AI models, and generates structured news reports.


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


## Web Dashboard

Provides:

- News browsing interface
- AI analysis results
- News API service


Technologies:

- FastAPI
- SQLite


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


## 1. Clone Repository

```bash
git clone https://github.com/jeams11/AI-News-Agent.git

cd AI-News-Agent
```


## 2. Create Virtual Environment

Create an isolated Python environment:

```bash
python3 -m venv venv
```


Activate virtual environment:

```bash
source venv/bin/activate
```


## 3. Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```


Install Playwright browser:

```bash
playwright install chromium
```


# Usage


## 1. News Crawling

Enter crawler directory:

```bash
cd crawler
```


Run BBC crawler:

```bash
python bbc.py
```


Run AIBase crawler:

```bash
python aibase.py
```


## 2. AI News Summarization

Enter summary directory:

```bash
cd summary
```


Run AI summarization:

```bash
python summarize.py
```


Generated output:

```text
news_report.md
```


## 3. Web Service

Start web server:

```bash
python web/app.py
```


Open browser:

```text
http://127.0.0.1:8000
```


# Automated Tasks

AI-News-Agent includes an automated scheduler.

The scheduler automatically performs:

- News crawling every hour
- AI news summarization every 12 hours


Run scheduler:

```bash
python scheduler.py
```


# Technology Stack


| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Playwright | Browser automation |
| BeautifulSoup | HTML parsing |
| SQLite | Database storage |
| FastAPI | Web API framework |
| OpenAI SDK | LLM integration |
| Qwen / DeepSeek | AI news analysis |


# Requirements

Main dependencies:

- Python 3.10+
- Playwright
- FastAPI
- SQLite
- OpenAI Compatible API


# License

MIT License
