"""
agent.py

The FitFindr planning loop. Orchestrates the three tools in response to a
natural language user query, passing state between them via a session dict.

Complete tools.py and test each tool in isolation before implementing this file.
"""

from tools import search_listings, suggest_outfit, create_fit_card


def _new_session(query: str, wardrobe: dict) -> dict:
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


def run_agent(query: str, wardrobe: dict) -> dict:
    session = _new_session(query, wardrobe)

    query_lower = query.lower()

    max_price = None
    size = None

    words = query_lower.replace(",", "").split()

    for i, word in enumerate(words):
        if word.startswith("$"):
            price_text = word.replace("$", "")
            if price_text.replace(".", "").isdigit():
                max_price = float(price_text)

        if word == "under" and i + 1 < len(words):
            next_word = words[i + 1].replace("$", "")
            if next_word.replace(".", "").isdigit():
                max_price = float(next_word)

        if word == "size" and i + 1 < len(words):
            size = words[i + 1].upper()

    description = query_lower

    if max_price is not None:
        description = description.replace(f"under ${int(max_price)}", "")
        description = description.replace(f"under {int(max_price)}", "")
        description = description.replace(f"${int(max_price)}", "")

    if size is not None:
        description = description.replace(f"size {size.lower()}", "")

    description = description.replace("looking for", "").replace("i'm", "").strip()

    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

    search_results = search_listings(
        description=description,
        size=size,
        max_price=max_price,
    )

    session["search_results"] = search_results

    if not search_results:
        session["error"] = (
            "Sorry, I could not find a listing that matches your request. "
            "Try changing the item description, size, or price range."
        )
        return session

    selected_item = search_results[0]
    session["selected_item"] = selected_item

    outfit_suggestion = suggest_outfit(selected_item, wardrobe)
    session["outfit_suggestion"] = outfit_suggestion

    fit_card = create_fit_card(outfit_suggestion, selected_item)
    session["fit_card"] = fit_card

    return session


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== Happy path: graphic tee ===\n")
    session = run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    )

    if session["error"]:
        print(f"Error: {session['error']}")
    else:
        print(f"Parsed: {session['parsed']}")
        print(f"Found: {session['selected_item']['title']}")
        print(f"\nOutfit: {session['outfit_suggestion']}")
        print(f"\nFit card: {session['fit_card']}")

    print("\n\n=== No-results path ===\n")
    session2 = run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    )

    print(f"Parsed: {session2['parsed']}")
    print(f"Error message: {session2['error']}")
    print(f"Fit card should be None: {session2['fit_card']}")