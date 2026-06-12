import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_empty_wardrobe


def test_search_returns_results():
    results = search_listings(
        "vintage graphic tee",
        size=None,
        max_price=50
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_search_empty_results():
    results = search_listings(
        "designer ballgown",
        size="XXS",
        max_price=5
    )

    assert results == []


def test_search_price_filter():
    results = search_listings(
        "jacket",
        size=None,
        max_price=10
    )

    assert all(item["price"] <= 10 for item in results)


def test_suggest_outfit_empty_wardrobe():
    item = {
        "title": "Test Shirt",
        "description": "Blue graphic tee",
        "style_tags": ["casual"],
        "colors": ["blue"]
    }

    result = suggest_outfit(item, get_empty_wardrobe())

    assert isinstance(result, str)
    assert len(result) > 0


def test_create_fit_card_missing_outfit():
    item = {
        "title": "Test Shirt"
    }

    result = create_fit_card("", item)

    assert "missing" in result.lower()