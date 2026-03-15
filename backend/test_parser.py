"""Unit tests for the rule-based request parser."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from parser import parse_request, extract_budget, extract_priority, extract_category


# ---------------------------------------------------------------------------
# Budget extraction
# ---------------------------------------------------------------------------

def test_budget_bucks():
    assert extract_budget("max 80 bucks") == 80.0

def test_budget_chf():
    assert extract_budget("budget 30 chf") == 30.0

def test_budget_euros():
    assert extract_budget("URGENT laptop charger max 50 euros") == 50.0

def test_budget_francs():
    assert extract_budget("about 25 francs") == 25.0

def test_budget_none():
    assert extract_budget("coffee machine for the kitchen") is None

def test_budget_decimal():
    assert extract_budget("max 19.99 chf") == 19.99


# ---------------------------------------------------------------------------
# Priority extraction
# ---------------------------------------------------------------------------

def test_priority_urgent_asap():
    assert extract_priority("need headphones asap") == "urgent"

def test_priority_urgent_caps():
    assert extract_priority("URGENT laptop charger") == "urgent"

def test_priority_low_whenever():
    assert extract_priority("printer paper, whenever") == "low"

def test_priority_low_no_rush():
    assert extract_priority("no rush, just some sticky notes") == "low"

def test_priority_normal():
    assert extract_priority("wireless mouse budget 30 chf") == "normal"


# ---------------------------------------------------------------------------
# Category extraction
# ---------------------------------------------------------------------------

def test_category_electronics_headphones():
    assert extract_category("headphones for video calls") == "electronics"

def test_category_electronics_charger():
    assert extract_category("laptop charger") == "electronics"

def test_category_office_paper():
    assert extract_category("printer paper a4") == "office"

def test_category_appliances_coffee():
    assert extract_category("coffee machine for the kitchen") == "appliances"

def test_category_other():
    assert extract_category("something completely unknown") == "other"


# ---------------------------------------------------------------------------
# Full parse_request integration
# ---------------------------------------------------------------------------

def test_full_parse_headphones():
    result = parse_request("need headphones for calls, max 80 bucks, asap")
    assert result["category"] == "electronics"
    assert result["budget_chf"] == 80.0
    assert result["priority"] == "urgent"
    assert result["raw_input"] == "need headphones for calls, max 80 bucks, asap"

def test_full_parse_mouse():
    result = parse_request("wireless mouse, budget 30 chf, low priority")
    assert result["category"] == "electronics"
    assert result["budget_chf"] == 30.0
    assert result["priority"] == "low"

def test_full_parse_no_budget_no_priority():
    result = parse_request("coffee machine for the kitchen")
    assert result["category"] == "appliances"
    assert result["budget_chf"] is None
    assert result["priority"] == "normal"

def test_full_parse_urgent_charger():
    result = parse_request("URGENT laptop charger max 50 euros")
    assert result["priority"] == "urgent"
    assert result["budget_chf"] == 50.0
    assert result["category"] == "electronics"


# ---------------------------------------------------------------------------
# Runner (no pytest required)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_budget_bucks, test_budget_chf, test_budget_euros,
        test_budget_francs, test_budget_none, test_budget_decimal,
        test_priority_urgent_asap, test_priority_urgent_caps,
        test_priority_low_whenever, test_priority_low_no_rush, test_priority_normal,
        test_category_electronics_headphones, test_category_electronics_charger,
        test_category_office_paper, test_category_appliances_coffee, test_category_other,
        test_full_parse_headphones, test_full_parse_mouse,
        test_full_parse_no_budget_no_priority, test_full_parse_urgent_charger,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed}/{passed+failed} tests passed")
    if failed:
        sys.exit(1)
