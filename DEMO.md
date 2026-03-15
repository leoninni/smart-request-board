# Demo Script

## How to Run Locally (3 commands)

```bash
pip install -r requirements.txt
cd backend && python app.py
# Open frontend/index.html in your browser
```

## What to Click

1. **Submit Form** (`index.html`)
   - Type a messy request in the textarea
   - Click "Parse & Submit"
   - See the structured result appear below the form instantly

2. **Request List** (`requests.html`)
   - See all submitted requests in a table
   - Click any row to see matched products from the catalog

## "Wow" Demo Examples

### Example 1 — Budget extraction
```
Input:  "need headphones for calls, max 80 bucks, asap"
Output: item=headphones, category=electronics, budget=80, priority=urgent
```

### Example 2 — Priority detection with caps
```
Input:  "URGENT laptop charger max 50 euros"
Output: item=laptop charger, category=electronics, budget=50, priority=urgent
```

### Example 3 — Low priority + CHF
```
Input:  "wireless mouse, budget 30 chf, low priority"
Output: item=mouse, category=electronics, budget=30, priority=low
```

### Example 4 — Office supplies
```
Input:  "need printer paper a4, about 25 francs, whenever"
Output: item=printer paper, category=office, budget=25, priority=low
```

### Example 5 — Tricky: no budget, no priority
```
Input:  "coffee machine for the kitchen"
Output: item=coffee machine, category=appliances, budget=null, priority=normal
```

## What to Explain (60-second pitch)

> "Our app takes messy free-text purchase requests — the kind you'd get in an email — and automatically extracts the key fields: what's being requested, what category it falls into, the budget, and how urgent it is.
>
> We store every parsed request in a local database, then match it against a product catalog filtered by category and budget.
>
> The parser uses regex for budget extraction and keyword lists for category and priority — no AI API needed, fully local, runs in 3 commands."
