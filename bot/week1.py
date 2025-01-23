'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import random
import eval7


class Player(Bot):
    '''
    A pokerbot.
    '''
    HAND_RANKS = {
        "Royal Flush":      1,
        "Straight Flush":   2,
        "Four of a Kind":   3,
        "Full House":       4,
        "Flush":            5,
        "Straight":         6,
        "Three of a Kind":  7,
        "Two Pair":         8,
        "One Pair":         9,
        "High Card":       10
    }

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''

        # self.hand_ranges = {
        #     "blue": {
        #         ("Ah", "Ad"), ("Ah", "Ac"), ("Ah", "As"), ("Ad", "Ac"), ("Ad", "As"), ("Ac", "As"),  # AA
        #         ("Kh", "Kd"), ("Kh", "Kc"), ("Kh", "Ks"), ("Kd", "Kc"), ("Kd", "Ks"), ("Kc", "Ks"),  # KK
        #         ("Qh", "Qd"), ("Qh", "Qc"), ("Qh", "Qs"), ("Qd", "Qc"), ("Qd", "Qs"), ("Qc", "Qs"),  # QQ
        #         ("Jh", "Jd"), ("Jh", "Jc"), ("Jh", "Js"), ("Jd", "Jc"), ("Jd", "Js"), ("Jc", "Js"),  # JJ
        #         ("Th", "Td"), ("Th", "Tc"), ("Th", "Ts"), ("Td", "Tc"), ("Td", "Ts"), ("Tc", "Ts"),  # TT
        #         ("Ah", "Kh"), ("Kh", "Ah"), ("Ad", "Kd"), ("Kd", "Ad"), ("Ac", "Kc"), ("Kc", "Ac"),  # AK
        #         ("As", "Ks"), ("Ks", "As"), ("Ah", "Kd"), ("Ah", "Kc"), ("Ah", "Ks"), ("Kh", "Ad"), 
        #         ("Kh", "Ac"), ("Kh", "As"), ("Ad", "Kc"), ("Ad", "Ks"), ("Kd", "Ah"), ("Kd", "Ac"), 
        #         ("Kd", "As"), ("Ac", "Ks"), ("Ac", "Kh"), ("Kc", "Ah"), ("Kc", "Ad"), ("Kc", "As"),
        #         ("As", "Kh"), ("As", "Kd"), ("Ks", "Ah"), ("Ks", "Ad"), ("Ks", "Ac")
        #     },
        #     "green": {
        #         ("Ah", "Qh"), ("Ad", "Qd"), ("Ac", "Qc"), ("As", "Qs"),  # AQ suited
        #         ("Ah", "Jh"), ("Ad", "Jd"), ("Ac", "Jc"), ("As", "Js"),  # AJ suited
        #         ("Kh", "Qh"), ("Kd", "Qd"), ("Kc", "Qc"), ("Ks", "Qs"),  # KQ suited
        #         ("8h", "8d"), ("8h", "8c"), ("8h", "8s"), ("8d", "8c"), ("8d", "8s"), ("8c", "8s"),  # 88
        #         ("9h", "9d"), ("9h", "9c"), ("9h", "9s"), ("9d", "9c"), ("9d", "9s"), ("9c", "9s")   # 99
        #     },
        #     "yellow": {
        #         ("2h", "2d"), ("2h", "2c"), ("2h", "2s"), ("2d", "2c"), ("2d", "2s"), ("2c", "2s"),  # 22
        #         ("3h", "3d"), ("3h", "3c"), ("3h", "3s"), ("3d", "3c"), ("3d", "3s"), ("3c", "3s"),  # 33
        #         ("4h", "4d"), ("4h", "4c"), ("4h", "4s"), ("4d", "4c"), ("4d", "4s"), ("4c", "4s"),  # 44
        #         ("5h", "5d"), ("5h", "5c"), ("5h", "5s"), ("5d", "5c"), ("5d", "5s"), ("5c", "5s"),  # 55
        #         ("6h", "6d"), ("6h", "6c"), ("6h", "6s"), ("6d", "6c"), ("6d", "6s"), ("6c", "6s"),  # 66
        #         ("7h", "7d"), ("7h", "7c"), ("7h", "7s"), ("7d", "7c"), ("7d", "7s"), ("7c", "7s"),  # 77
        #         ("Th", "9h"), ("Td", "9d"), ("Tc", "9c"), ("Ts", "9s"),  # T9s
        #         ("Jh", "Th"), ("Jd", "Td"), ("Jc", "Tc"), ("Js", "Ts")   # JTs
        #     },
        #     "orange": {
        #         ("Ah", "5h"), ("Ad", "5d"), ("Ac", "5c"), ("As", "5s"),  # A5s
        #         ("Kh", "7h"), ("Kd", "7d"), ("Kc", "7c"), ("Ks", "7s"),  # K7s
        #         ("Qh", "Jh"), ("Qd", "Jd"), ("Qc", "Jc"), ("Qs", "Js"),  # QJs
        #         ("Th", "8h"), ("Td", "8d"), ("Tc", "8c"), ("Ts", "8s")   # T8s
        #     }
        # }

        self.hand_ranges = {
            "green": {
                "AAo", "AAs" "AKo", "AKs", "AQo", "AQs", "AJo", "AJs", "ATo", "ATs" "A9s", "A8s", "A7s", "A6s", "A5s", "A4s",
                "KKo", "KKs", "KQo", "KQs", "KJs", "KTs", "K9s",
                "QQo", "QQs", "QJs", "QTs",
                "JJo", "JJs", "JTs", "J9s"
                "TTo", "TTs", "T9s"
                "99o", "99s",
                "88o", "88s",
                "77o", "77s",
                "66o", "66s",
                "55o", "55s",
                "44o", "44s",
            },
            "yellow": {
                 "A9o", "A8o" "A3s", "A2s",
                 "KTo","KJo","K8s", "K7s", "K6s", "K5s", "K4s",
                 "QJo", "QTo", "Q8s", "Q7s",
                 "JTo","J8s", "J7s",
                 "T8s", "T7s",
                 "98s", "97s",
                 "87s", "86s",
                 "76s",
                 "65s", 
                 "54s",
                 "33s",
                 "22s"

            },
            "orange": {
                "A7o", "A6o", "A5o", "A4o",
                "K9o", "K8o", "K7o", "K6o", "K5o", "K4o", "K3o",
                "Q9o", "Q8o", "Q7o", "Q6o", "Q5o", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s"
                "J9o", "J8o", "J7o", "J6o", "J6s", "J5s", "J4s", "J3s", "J2s"
                "T9o", "T8o", "T7o", "T6o", "T6s", "T5s", "T4s", "T3s", "T2s"
                "98o", "97o", "96o", "95s", "94s", "93s", "92s",
                "87o", "86o", "85o", "84s", "83s", "82s",
                "76o", "75o", "74s", "73s"
                "65o", "63s", "62s",
                "54o", "52s"
                "43s", "42s"
            }
        }
        
        self.broadway = {'A', 'K', 'Q', 'J', 'T'}

    def is_green(self, my_cards):
        """
        Returns True if the 2-card hand belongs to the 'green' range as defined
        in self.hand_ranges['green'], based on rank only.
        
        :param cards: a list or tuple of length 2, e.g. ['2s', '5d']
        :return: bool
        """
        # extract ranks only, e.g. '2s' -> '2', '5d' -> '5'
        rank1 = my_cards[0][0]
        rank2 = my_cards[1][0]

        # form both possible (rank1, rank2) and (rank2, rank1) pairs
        pair1 = (rank1, rank2)
        pair2 = (rank2, rank1)
        
        # check if either orientation is in the 'green' set
        if pair1 in self.hand_ranges["green"] or pair2 in self.hand_ranges["green"]:
            return True
        return False
    
    

    def preflop_strength(self, my_cards):
        rank1 = my_cards[0][0]
        suit1 = my_cards[0][1]
        rank2 = my_cards[1][0]
        suit2 = my_cards[1][1]

        # Determine if the hand is suited or offsuit
        if suit1 == suit2:
            hand = f"{rank1}{rank2}s"
        else:
            hand = f"{rank1}{rank2}o"

        # Check against hand ranges
        for strength, hands in self.hand_ranges.items():
            if hand in hands or hand[::-1] in hands:  # Check both orientations
                return strength

        return "unknown"  # Return "unknown" if not found in any range

        

    def calculate_win_rate(self, my_cards, board_cards):
        MC_ITER = 100

        my_cards = [eval7.Card(card) for card in my_cards]
        board_cards = [eval7.Card(card) for card in board_cards]

        deck = eval7.Deck()

        for card in my_cards + board_cards:
            deck.cards.remove(card)
        
        score = 0
        for _ in range(MC_ITER):

            deck.shuffle()

            num_cards_needed = 2 + (5 - len(board_cards))
            draw = deck.peek(num_cards_needed)

            opp_draw = draw[:2]
            board_draw = draw[2:]

            my_hand = my_cards + board_cards + board_draw
            opp_hand = opp_draw + board_cards + board_draw

            my_value = eval7.evaluate(my_hand)
            opp_value = eval7.evaluate(opp_hand)

            if my_value > opp_value:
                score += 1
            elif my_value < opp_value:
                score += 0
            else:
                score += 0.5
        
        win_rate = score / MC_ITER

        return win_rate

    def calculate_outs(self, my_cards, board_cards):
        '''
        Calculate the number of outs (cards that improve your hand) using eval7.

        Arguments:
        my_cards: List of your hole cards (e.g., ['Ah', 'Kd']).
        board_cards: List of community cards currently on the board (e.g., ['Qs', 'Jd', '7h']).

        Returns:
        Number of outs.
        '''
        my_cards = [eval7.Card(card) for card in my_cards]
        board_cards = [eval7.Card(card) for card in board_cards]

        # Remaining deck excluding known cards
        deck = eval7.Deck()
        known_cards = my_cards + board_cards
        for card in known_cards:
            deck.cards.remove(card)

        best_hand_score = eval7.evaluate(my_cards + board_cards)
        outs = 0

        for draw_card in deck.cards:
            # Simulate the board with one more card
            simulated_board = board_cards + [draw_card]
            my_hand_score = eval7.evaluate(my_cards + simulated_board)

            if my_hand_score > best_hand_score:
                outs += 1

        return outs


    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your cards
        big_blind = bool(active)  # True if you are the big blind
        my_bounty = round_state.bounties[active]  # your current bounty rank
        

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        #street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed

        print("My delta: ", my_delta)
        print("------------------------------------------")
        
        my_bounty_hit = terminal_state.bounty_hits[active]  # True if you hit bounty
        opponent_bounty_hit = terminal_state.bounty_hits[1-active] # True if opponent hit bounty
        bounty_rank = previous_state.bounties[active]  # your bounty rank

        # The following is a demonstration of accessing illegal information (will not work)
        opponent_bounty_rank = previous_state.bounties[1-active]  # attempting to grab opponent's bounty rank

        if my_bounty_hit:
            print("I hit my bounty of " + bounty_rank + "!")
        if opponent_bounty_hit:
            print("Opponent hit their bounty of " + opponent_bounty_rank + "!")


    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_bounty = round_state.bounties[active]  # your current bounty rank
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot
        pot_total = my_contribution + opp_contribution

        win_rate = self.calculate_win_rate(my_cards, board_cards)
        pot_odds = continue_cost / (my_pip + opp_pip + 0.1)
        min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
        
        big_blind = bool(active)
        
        self.print_info(game_state, round_state, active)

        hand_strength = self.preflop_strength(my_cards)

        # Check if bounty hit
        # If bounty hit play more aggresively
        if self.bounty_in_hand(my_cards, my_bounty):
            if win_rate > pot_odds:
                if random.random() < 0.20 and max_raise is not None and RaiseAction in legal_actions:
                    return RaiseAction(max_raise)
                elif random.random() < 0.50:
                    return RaiseAction(min_raise)
                elif CallAction in legal_actions:
                    return CallAction()
                else:
                    # Fall back to call
                    if continue_cost > 0 and CallAction in legal_actions:
                        return CallAction()
                    elif CheckAction in legal_actions:
                        return CheckAction()

        # On the preflop round, only continue if the hand strength is blue or green
        if street < 3 and hand_strength not in ["green", "yellow", "orange"]:
            
            if big_blind and CheckAction in legal_actions:
                return CheckAction()
            return FoldAction()

        if win_rate > pot_odds:
            if RaiseAction in legal_actions:
                raise_amount = int(min_raise + (max_raise - min_raise) * 0.09)
                return RaiseAction(raise_amount)
            elif CallAction in legal_actions:
                return CallAction()
            elif CheckAction in legal_actions:
                return CheckAction()
        
        # bluff 10% of "bad" hands
        elif random.random() < 0.1:
            if RaiseAction in legal_actions:
                raise_amount = int(min_raise + (max_raise - min_raise) * 0.09)
                return RaiseAction(raise_amount)
            elif CallAction in legal_actions:
                return CallAction()
            elif CheckAction in legal_actions:
                return CheckAction()
            else:
                return FoldAction()
        
        return FoldAction()
    
    def hand_rank(self, my_cards, board_cards):
        """
        Evaluates the best 5-card hand from my_cards + board_cards
        and returns an integer 1..10,
        where 1 is the best category (nut flush / royal flush)
        and 10 is the worst (high card).
        """

        # 1) Convert string cards (e.g. 'As', 'Th') into eval7.Card objects
        all_cards = [eval7.Card(c) for c in my_cards + board_cards]

        # 2) Evaluate and get an integer score (lower = stronger)
        hand_value = eval7.evaluate(all_cards)

        # 3) Convert that score into a string category, e.g. 'Flush', 'Two Pair'
        hand_type_str = eval7.handtype(hand_value)

        # 4) Map that string to a 1..10 rank using HAND_RANKS
        #    (If eval7 returns "Straight Flush" for a Royal Flush,
        #     you'll need custom logic to detect if it's specifically a "Royal".)
        #    By default, eval7.handtype() does distinguish "Straight Flush"
        #    vs "Royal Flush".
        rank_num = self.HAND_RANKS.get(hand_type_str, 10)  # default to 10 if unknown

        return rank_num

    def bounty_in_hand(self, cards, bounty_rank):
            """
            Return True if your hole cards contain your bounty rank.
            cards: e.g. [('A','s'), ('T','h')] => ranks are 'A','T'
            bounty_rank: e.g. 'A'
            """
            ranks = [c[0] for c in cards]
            return (bounty_rank in ranks)

    def bounty_on_board(self, board, bounty_rank):
        """
        Return True if the board contains your bounty rank.
        board: e.g. [('K','h'), ('T','d'), ('5','c')] => ranks 'K','T','5'
        bounty_rank: e.g. '5'
        """
        ranks = [c[0] for c in board]
        return (bounty_rank in ranks)

    def print_info(self, game_state, round_state, active):
        """
        Print out information about the state of the game
        """

        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_bounty = round_state.bounties[active]  # your current bounty rank
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot

        win_rate = self.calculate_win_rate(my_cards, board_cards)
        pot_odds = continue_cost / (my_pip + opp_pip + 0.1)
        min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise

        print("My cards: ", my_cards)
        print("Board cards: ", board_cards)
        print("Win rate: ", win_rate)
        print("Outs: ", self.calculate_outs(my_cards, board_cards))
        print("Outs percent: ", self.calculate_outs(my_cards, board_cards)*2)
        print("Pot odds: ", pot_odds)
        print("My pip: ", my_pip)
        print("Opp pip: ", opp_pip)
        print("Min raise: ", min_raise)
        print("Max raise: ", max_raise)
        print("My bounty: ", my_bounty)
        print("---")


if __name__ == '__main__':
    run_bot(Player(), parse_args())