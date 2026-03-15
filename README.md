# Smart Request Board

A local full-stack web app where you type a messy purchase request in plain English and the app automatically structures it, stores it, and lets you browse, compare, and filter requests.

## Problem Statement

Procurement teams receive purchase requests as unstructured free text — emails, chat messages, incomplete forms. Manually categorizing and matching these to a product catalog wastes time and introduces errors.

## Solution

A rule-based parser extracts key fields (item, category, budget, priority) from plain-English input. Parsed requests are stored in a local database and matched against a product catalog, giving instant structured comparisons without any AI API dependencies.

## Tech Stack

| Layer | Tool |
|---|---|
| Backend | Python + Flask |
| Database | SQLite via SQLAlchemy |
| Frontend | HTML + CSS + vanilla JS |
| Version control | Git + GitHub |

## Requirements

- Python **3.10 or newer** (uses `X | Y` union type syntax)

## How to Run

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Start the backend
cd backend
python3 app.py

# 3. Open the frontend
# Open frontend/index.html in your browser (or visit http://localhost:5000)
```

The app runs entirely locally — no API keys, no internet connection required.

## Example Inputs

- `"need headphones for calls, max 80 bucks, asap"` → category: electronics, budget: 80, priority: urgent
- `"URGENT laptop charger max 50 euros"` → category: electronics, budget: 50, priority: urgent
- `"wireless mouse, budget 30 chf, low priority"` → category: electronics, budget: 30, priority: low

## Project Structure

```
smart-request-board/
├── README.md
├── DEMO.md
├── requirements.txt
├── backend/
│   ├── app.py          # Flask routes
│   ├── models.py       # SQLAlchemy models
│   ├── parser.py       # Rule-based text parser
│   ├── test_parser.py  # Unit tests
│   └── catalog.json    # Fake product catalog
├── frontend/
│   ├── index.html      # Submit form
│   ├── requests.html   # Request list
│   └── style.css       # Basic styling
└── .gitignore
```
