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

        self.hand_ranges = {
            "green": {
                "AAo", "AAs", "AKo", "AKs", "AQo", "AQs", "AJo", "AJs", "ATo", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s",
                "KKo", "KKs", "KQo", "KQs", "KJs", "KTs", "K9s",
                "QQo", "QQs", "QJs", "QTs", "Q9s",
                "JJo", "JJs", "JTs", "J9s",
                "TTo", "TTs", "T9s",
                "99o", "99s",
                "88o", "88s",
                "77o", "77s",
                "66o", "66s",
                "55o", "55s",
                "44o", "44s",
            },
            "yellow": {
                 "A9o", "A8o", "A3s", "A2s",
                 "KTo","KJo","K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                 "QJo", "QTo", "Q8s", "Q7s",
                 "JTo","J8s", "J7s",
                 "T8s", "T7s",
                 "98s", "97s",
                 "87s", "86s",
                 "76s",
                 "65s", 
                 "54s", "57s",
                 "33s", "33o",
                 "22s", "22o"
            },
            "orange": {
                "A7o", "A6o", "A5o", "A4o", "A3o", "A2o",
                "K9o", "K8o", "K7o", "K6o", "K5o", "K4o", "K3o",
                "Q9o", "Q8o", "Q7o", "Q6o", "Q5o", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                "J9o", "J8o", "J7o", "J6o", "J6s", "J5s", "J4s", "J3s", "J2s",
                "T9o", "T8o", "T7o", "T6o", "T6s", "T5s", "T4s", "T3s", "T2s",
                "98o", "97o", "96o", "95s", "94s", "93s", "92s",
                "87o", "86o", "85o", "84s", "83s", "82s",
                "76o", "75o", "74s", "73s",
                "65o", "63s", "62s",
                "54o", "52s",
                "43s", "42s"
            }
        }
        
    def hole_strength(self, my_cards):
        rank1 = my_cards[0][0]
        suit1 = my_cards[0][1]
        rank2 = my_cards[1][0]
        suit2 = my_cards[1][1]
        hand_rank = f"{rank1}{rank2}"

        # Determine if the hand is suited or offsuit
        suit = "s"
        if suit1 == suit2:
            suit = "s"
        else:
            suit = "o"

        # Check against hand ranges
        for strength, hands in self.hand_ranges.items():
            if hand_rank+suit in hands or hand_rank[::-1]+suit in hands:  # Check both orientations
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
        print("------------------------------------------\n")
        
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
        self.print_info(game_state, round_state, active)

        # VARIABLESVARIABLESVARIABLESVARIABLESVARIABLESVARIABLES
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
        min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
        
        big_blind = bool(active)
        small_blind = not big_blind
        win_rate = self.calculate_win_rate(my_cards, board_cards)
        pot_odds = continue_cost / (pot_total + continue_cost + 0.1)
        bounty_bonus_ev = 0.405 * (0.5 * opp_pip + 10)
        effective_pot_odds = continue_cost / (pot_total + continue_cost + bounty_bonus_ev)
        hole_strength = self.hole_strength(my_cards)
        has_raised = my_pip > 1
        hand_rank = self.hand_rank(my_cards, board_cards)
        has_hit_bounty = self.bounty_hit(my_cards, board_cards, my_bounty)

        # STRATEGYSTRATEGYSTRATEGYSTRATEGYSTRATEGYSTRATEGY
        # On the preflop round, check fold some percentage of the time on "weak" hands
        if street < 3 and hole_strength == "green":
            if not has_raised and RaiseAction in legal_actions:
                raise_amount = int(min_raise + (max_raise - min_raise) * 0.015)
                return RaiseAction(raise_amount)
            elif CallAction in legal_actions:
                return CallAction()
            elif CheckAction in legal_actions:
                return CheckAction()

        if street < 3 and hole_strength == "yellow":
            if random.random() < 0.1 and not has_hit_bounty:
                if small_blind and continue_cost < 5 and CallAction in legal_actions: # call to see the flop
                    return CallAction()
                else:
                    return CheckAction() if CheckAction in legal_actions else FoldAction()
            else:
                if not has_raised and RaiseAction in legal_actions:
                    raise_amount = int(min_raise + (max_raise - min_raise) * 0.0135)
                    return RaiseAction(raise_amount)
                return CallAction() if CallAction in legal_actions else CheckAction()
        
        if street < 3 and hole_strength == "orange":
            if continue_cost/(pot_total + 0.1) > 5:
                return CheckAction() if CheckAction in legal_actions else FoldAction()
            elif random.random() < 0.05 and not has_hit_bounty:
                if small_blind and continue_cost < 5 and CallAction in legal_actions: # call to see the flop
                    return CallAction()
                else:
                    return CheckAction() if CheckAction in legal_actions else FoldAction()
            else:
                if not has_raised and RaiseAction in legal_actions:
                    raise_amount = int(min_raise + (max_raise - min_raise) * 0.012)
                    return RaiseAction(raise_amount)
                return CallAction() if CallAction in legal_actions else CheckAction()

        if street == 3:
            if win_rate > effective_pot_odds:
                if RaiseAction in legal_actions and hand_rank <= 9:
                    raise_amount = int(min_raise + (max_raise - min_raise) * 0.03)
                    return RaiseAction(raise_amount)

            # # Check fold if the hand is weak and the continue_cost is greater than equal 1/4 of the pot
            # elif continue_cost/(pot_total + 0.1) >= 0.5:
            #     return CheckAction() if CheckAction in legal_actions else FoldAction()
            else:
                return CallAction() if CallAction in legal_actions else CheckAction() if CheckAction in legal_actions else FoldAction()
        
        if street == 4:
            if win_rate > effective_pot_odds: # good chance of winning
                if RaiseAction in legal_actions and hand_rank <= 9:
                    raise_amount = int(min_raise + (max_raise - min_raise) * 0.15)
                    return RaiseAction(raise_amount)
                elif CallAction in legal_actions:
                    return CallAction()
                elif CheckAction in legal_actions:
                    return CheckAction()
            else: # bad chance of winning
                return CallAction() if CallAction in legal_actions else CheckAction()
        
        if street == 5:
            if win_rate > effective_pot_odds:
                if RaiseAction in legal_actions:
                    raise_amount = int(min_raise + (max_raise - min_raise) * 0.3)
                    return RaiseAction(raise_amount)
                # only call if continue_cost is less than 1/4 of the pot
                elif continue_cost/pot_total < 0.25 and CallAction in legal_actions:
                    return CallAction()
                elif CheckAction in legal_actions:
                    return CheckAction()
                return CallAction() if CallAction in legal_actions else CheckAction()
            return CallAction() if CallAction in legal_actions else CheckAction()
        
        # Default action
        return CheckAction() if CheckAction in legal_actions else FoldAction()


    
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

    def bounty_hit(self, cards, board, bounty_rank):
        """
        Return True if your hole cards or the board contains your bounty rank.
        
        Arguments:
        cards: List of your hole cards (e.g., [('A', 's'), ('T', 'h')] => ranks are 'A', 'T').
        board: List of board cards (e.g., [('K', 'h'), ('T', 'd'), ('5', 'c')] => ranks are 'K', 'T', '5').
        bounty_rank: The rank to check for (e.g., 'A').

        Returns:
        True if bounty rank is in hole cards or board cards, False otherwise.
        """
        # Combine the ranks from hole cards and board cards
        ranks = [c[0] for c in cards + board]
        
        # Check if bounty rank exists in the combined ranks
        return bounty_rank in ranks

    def determine_board_texture(self, board_cards):
        suits = [card[1] for card in board_cards]
        ranks = [card[0] for card in board_cards]

        # Check for flush draws
        suit_counts = {suit: suits.count(suit) for suit in set(suits)}
        flush_draw = any(count >= 3 for count in suit_counts.values())

        # Check for straight draws
        rank_values = sorted([eval7.Card(card).rank for card in board_cards])
        straight_draw = any(
            rank_values[i] + 1 == rank_values[i + 1] for i in range(len(rank_values) - 1)
        )

        # Determine texture
        if flush_draw and straight_draw:
            return "very wet"
        elif flush_draw or straight_draw:
            return "wet"
        else:
            return "dry"

    def hand_strength(self, my_cards, board_cards):
        '''
        Evaluate the strength of the player's hand relative to the board.

        Arguments:
        my_cards: List of the player's hole cards (e.g., ['Ah', 'Kd']).
        board_cards: List of community cards currently on the board (e.g., ['Qs', 'Jd', '7h']).

        Returns:
        An integer from 1 to 5 representing the relative strength of the hand.
        '''
        my_cards = [eval7.Card(card) for card in my_cards]
        board_cards = [eval7.Card(card) for card in board_cards]

        # Evaluate the player's hand combined with the board
        my_hand = my_cards + board_cards
        my_hand_value = eval7.evaluate(my_hand)

        # Evaluate the board alone
        board_value = eval7.evaluate(board_cards)

        # Determine the relative strength
        difference = my_hand_value - board_value
        if difference > 1000:
            return 1  # Very Strong
        elif difference > 500:
            return 2  # Strong
        elif difference > 0:
            return 3  # Neutral
        elif difference > -500:
            return 4  # Weak
        else:
            return 5  # Very Weak

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
        pot_total = my_contribution + opp_contribution

        win_rate = self.calculate_win_rate(my_cards, board_cards)
        pot_odds = continue_cost / (my_pip + opp_pip + 0.1)
        min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise

        board_texture = self.determine_board_texture(board_cards)
        hole_strength = self.hole_strength(my_cards)
        hand_strength = self.hand_strength(my_cards, board_cards)
        hand_rank = self.hand_rank(my_cards, board_cards)
        has_raised = my_pip > 1

        print("My cards: ", my_cards)
        print("Continue cost: ", continue_cost)
        print("Pot total:", pot_total)
        print("Call amount decimal: ", continue_cost/pot_total)
        print("hand_strength: ", hand_strength)
        print("Hand rank:", hand_rank)
        print("Hole strength: ", hole_strength)
        print("Board cards: ", board_cards)
        print("Board texture: ", board_texture)
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