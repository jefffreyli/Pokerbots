import eval7

class PokerRankerHelper:
    def __init__(self, filename="rank_mapping.txt"):
        self.filename = filename
        self.rank_mapping = self.load_rank_mapping()

    def all_5_card_combos(self, deck):
        """
        Generator that yields all 5-card combinations from the given deck,
        without using itertools.
        """
        def generate_combos(start_index, chosen):
            if len(chosen) == 5:
                yield chosen
                return
            if start_index >= len(deck):
                return
            for i in range(start_index, len(deck)):
                chosen.append(deck[i])
                yield from generate_combos(i + 1, chosen)
                chosen.pop()
        yield from generate_combos(0, [])

    def generate_rank_mapping(self):
        """
        Generate a dictionary that maps the raw eval7 scores to ranks (1 to 7462).
        """
        ranks = "23456789TJQKA"
        suits = "cdhs"
        deck = [eval7.Card(r + s) for r in ranks for s in suits]
        
        all_hand_scores = []
        for five_cards in self.all_5_card_combos(deck):
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

    def save_rank_mapping(self):
        """
        Save the rank mapping to a text file.
        Format: each line is "raw_score rank".
        """
        with open(self.filename, "w") as file:
            for raw_score, rank in self.rank_mapping.items():
                file.write(f"{raw_score} {rank}\n")
        # print(f"Rank mapping saved to {self.filename}.")

    def load_rank_mapping(self):
        """
        Load the rank mapping from a text file.
        If the file does not exist, generate and save the rank mapping.
        """
        try:
            rank_mapping = {}
            with open(self.filename, "r") as file:
                for line in file:
                    raw_score, rank = line.strip().split()
                    rank_mapping[int(raw_score)] = int(rank)
            # print(f"Rank mapping loaded from {self.filename}.")
            return rank_mapping
        except FileNotFoundError:
            # print("Rank mapping file not found. Generating a new one...")
            rank_mapping = self.generate_rank_mapping()
            self.rank_mapping = rank_mapping
            self.save_rank_mapping()
            return rank_mapping

    def raw_score_to_rank(self, raw_score):
        """
        Convert a raw eval7 score to its rank (1 = best, 7462 = worst).
        """
        return self.rank_mapping.get(raw_score, 8000)

    def evaluate_hand(self, hand):
        """
        Evaluate a hand and return its rank.
        """
        raw_score = eval7.evaluate(hand)
        rank = self.raw_score_to_rank(raw_score)
        return raw_score, rank

# # Example usage
# if __name__ == "__main__":
#     ranker = PokerRanker()

#     # Example hand: Royal Flush in spades
#     hand = [
#         eval7.Card("6s"),
#         eval7.Card("6s"),
#         eval7.Card("5s"),
#         eval7.Card("Ts"),
#         eval7.Card("Ac"),
#     ]

#     raw_score, rank = ranker.evaluate_hand(hand)
#     print("Hand:", hand)
#     print("Raw Score:", raw_score)
#     print("Rank (1=best, 7462=worst):", rank)
