#!/usr/bin/env python3
import json
import requests
import os
import datetime
import sys


def fetch_cards_from_anki(deck_name="Italiano"):
    """Fetch all cards from Anki deck using AnkiConnect API"""
    # First get all card IDs
    payload = {
        "action": "findCards",
        "version": 6,
        "params": {"query": f"deck:{deck_name}"},
    }

    try:
        response = requests.post("http://localhost:8765", json=payload)
        response.raise_for_status()
        data = response.json()

        if "error" in data and data["error"] is not None:
            print(f"Error fetching card IDs: {data['error']}")
            return []

        if "result" not in data:
            print(f"Response missing 'result' field")
            return []

        card_ids = data["result"]

        if not card_ids:
            print(f"No cards found in deck: {deck_name}")
            return []

        print(f"Found {len(card_ids)} cards in deck: {deck_name}")

        # Now get card info
        payload = {"action": "cardsInfo", "version": 6, "params": {"cards": card_ids}}

        response = requests.post("http://localhost:8765", json=payload)
        response.raise_for_status()
        data = response.json()

        if "error" in data and data["error"] is not None:
            print(f"Error fetching card details: {data['error']}")
            return []

        if "result" not in data:
            print(f"Response missing 'result' field")
            return []

        return data["result"]

    except requests.exceptions.ConnectionError:
        print(
            "Error: Could not connect to Anki. Make sure Anki is running and AnkiConnect is installed."
        )
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def format_cards(cards):
    """Extract only front and back values from cards"""
    formatted_cards = []

    for card in cards:
        try:
            front = card["fields"]["Front"]["value"]
            back = card["fields"]["Back"]["value"]

            formatted_cards.append({"front": front, "back": back})
        except KeyError:
            print(
                f"Warning: Card {card.get('cardId', 'unknown')} has unexpected format. Skipping."
            )

    return formatted_cards


def save_to_json(cards, output_dir="docs"):
    """Save cards to JSON file in the output directory"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the data structure
    data = {
        "vocabulary": cards,
        "updated_at": datetime.datetime.now().isoformat(),
        "count": len(cards),
    }

    # Save to file with fixed name
    filename = f"{output_dir}/vocabulary.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Also create a simple index.html page
    index_content = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=vocabulary.json">
    <title>Ragazzo Vocabulary</title>
</head>
<body>
    <p>Redirecting to vocabulary data...</p>
</body>
</html>
"""
    with open(f"{output_dir}/index.html", "w") as f:
        f.write(index_content)

    return filename


def push_to_github():
    """Commit and push changes to GitHub"""
    try:
        # Add all files in docs directory
        os.system("git add docs/")

        # Commit with timestamp
        commit_message = f"Update vocabulary data - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        os.system(f'git commit -m "{commit_message}"')

        # Push to origin
        os.system("git push origin main")

        return True
    except Exception as e:
        print(f"Error pushing to GitHub: {e}")
        return False


def main():
    print("Fetching cards from Anki...")
    cards = fetch_cards_from_anki("Italiano")

    if not cards:
        sys.exit(1)

    print("Formatting cards...")
    formatted_cards = format_cards(cards)

    print("Saving to JSON...")
    output_file = save_to_json(formatted_cards)
    print(f"Saved {len(formatted_cards)} cards to {output_file}")

    print("Pushing to GitHub...")
    success = push_to_github()
    if success:
        print("Successfully pushed to GitHub!")
        print("Your vocabulary is available at:")
        print("https://moritzmoeller.github.io/ragazzo-vocabulary/vocabulary.json")
    else:
        print("Failed to push to GitHub.")


if __name__ == "__main__":
    main()
