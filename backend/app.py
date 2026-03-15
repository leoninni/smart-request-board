"""Flask REST API for the Smart Request Board."""

import json
import os
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from models import Request, init_db, get_session
from parser import parse_request

app = Flask(__name__)
CORS(app)  # allow the frontend (file://) to call the API

# Load product catalog once at startup
CATALOG_PATH = os.path.join(os.path.dirname(__file__), "catalog.json")
with open(CATALOG_PATH) as f:
    CATALOG: list[dict] = json.load(f)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/requests", methods=["POST"])
def create_request():
    """Parse raw text, save to DB, return structured JSON."""
    body = request.get_json(silent=True) or {}
    raw_text = (body.get("text") or "").strip()

    if not raw_text:
        return jsonify({"error": "Field 'text' is required"}), 400

    parsed = parse_request(raw_text)

    with get_session() as session:
        req = Request(
            raw_input=parsed["raw_input"],
            item=parsed["item"],
            category=parsed["category"],
            budget_chf=parsed["budget_chf"],
            priority=parsed["priority"],
            created_at=datetime.utcnow(),
        )
        session.add(req)
        session.commit()
        result = req.to_dict()

    return jsonify(result), 201


@app.route("/requests", methods=["GET"])
def list_requests():
    """Return all saved requests as a JSON array, newest first."""
    with get_session() as session:
        rows = session.query(Request).order_by(Request.created_at.desc()).all()
        return jsonify([r.to_dict() for r in rows])


@app.route("/match", methods=["GET"])
def match_request():
    """
    Return catalog items that match a saved request.
    Query params:
      - request_id (int, required)
    Filters catalog to matching category; if budget is set, only items <= budget.
    Returns items sorted by price ascending.
    """
    request_id = request.args.get("request_id", type=int)
    if request_id is None:
        return jsonify({"error": "request_id is required"}), 400

    with get_session() as session:
        req = session.get(Request, request_id)
        if req is None:
            return jsonify({"error": "Request not found"}), 404

        category = req.category
        budget = req.budget_chf

    matches = [item for item in CATALOG if item["category"] == category]
    if budget is not None:
        matches = [item for item in matches if item["price_chf"] <= budget]
    matches.sort(key=lambda x: x["price_chf"])

    return jsonify({
        "request_id": request_id,
        "category": category,
        "budget_chf": budget,
        "matches": matches,
    })


# ---------------------------------------------------------------------------
# Seed data (only inserted once)
# ---------------------------------------------------------------------------

SEED_REQUESTS = [
    "need headphones for calls, max 80 bucks, asap",
    "wireless mouse budget 30 chf, low priority",
    "URGENT laptop charger max 50 euros",
    "printer paper a4, about 25 francs, whenever",
    "coffee machine for the kitchen",
]


def seed_db():
    with get_session() as session:
        existing = session.query(Request).count()
        if existing > 0:
            return  # already seeded
        for text in SEED_REQUESTS:
            parsed = parse_request(text)
            session.add(Request(
                raw_input=parsed["raw_input"],
                item=parsed["item"],
                category=parsed["category"],
                budget_chf=parsed["budget_chf"],
                priority=parsed["priority"],
                created_at=datetime.utcnow(),
            ))
        session.commit()
        print(f"Seeded {len(SEED_REQUESTS)} requests.")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    seed_db()
    print("Smart Request Board API running at http://localhost:5000")
    app.run(debug=True, port=5000)
