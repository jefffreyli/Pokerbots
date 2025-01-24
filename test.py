import eval7
import json
import os

def all_5_card_combos(deck):
    """
    Generator that yields all 5-card combinations from the given deck,
    without using itertools.
    """
    def generate_combos(start_index, chosen):
        # If we have 5 cards, yield the combination
        if len(chosen) == 5:
            yield chosen
            return
        
        # If not enough cards left to complete a 5-card hand, stop
        if start_index >= len(deck):
            return
        
        # For each position from start_index to the end of the deck
        for i in range(start_index, len(deck)):
            # Choose deck[i]
            chosen.append(deck[i])
            # Recurse with next index
            yield from generate_combos(i + 1, chosen)
            # Backtrack
            chosen.pop()
    
    # Start recursion with an empty chosen list
    yield from generate_combos(0, [])

def generate_rank_mapping():
    """
    Generate a dictionary that maps the raw eval7 scores to ranks (1 to 7462).
    """
    ranks = "23456789TJQKA"
    suits = "cdhs"
    deck = [eval7.Card(r + s) for r in ranks for s in suits]
    
    all_hand_scores = []
    for five_cards in all_5_card_combos(deck):
        score = eval7.evaluate(five_cards)
        all_hand_scores.append(score)
    
    all_hand_scores.sort(reverse=True)
    
    rank_mapping = {}
    rank = 1
    last_score = None
    
    for score in all_hand_scores:
        if score != last_score:
            rank_mapping[score] = rank
            rank += 1
            last_score = score
    
    return rank_mapping

def save_rank_mapping_to_file(rank_mapping, filename="rank_mapping.json"):
    """
    Save the rank mapping to a JSON file.
    """
    with open(filename, "w") as file:
        json.dump(rank_mapping, file)
    print(f"Rank mapping saved to {filename}.")

def load_rank_mapping_from_file(filename="rank_mapping.json"):
    """
    Load the rank mapping from a JSON file.
    """
    if os.path.exists(filename):
        with open(filename, "r") as file:
            rank_mapping = json.load(file)
        print(f"Rank mapping loaded from {filename}.")
        return rank_mapping
    else:
        return None

def raw_score_to_rank(raw_score, rank_map):
    """
    Convert a raw eval7 score to its rank (1 = best, 7462 = worst).
    """
    return rank_map.get(raw_score, None)

# Main script
if __name__ == "__main__":
    # Check if the rank mapping file exists
    rank_mapping = load_rank_mapping_from_file()
    
    if rank_mapping is None:
        print("Generating rank mapping; this may take some time...")
        rank_mapping = generate_rank_mapping()
        save_rank_mapping_to_file(rank_mapping)
    
    # Example usage
    def example_usage():
        hand = [
            eval7.Card("6s"),
            eval7.Card("6s"),
            eval7.Card("5s"),
            eval7.Card("Ts"),
            eval7.Card("Ac"),
        ]
        raw_score = eval7.evaluate(hand)
        rank = raw_score_to_rank(raw_score, rank_mapping)
        print("Hand:", hand)
        print("Raw Score:", raw_score)
        print("Rank (1=best, 7462=worst):", rank)

    example_usage()
