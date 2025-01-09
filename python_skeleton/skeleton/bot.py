'''
This file contains the base class that you should implement for your pokerbot.
'''

from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import random


class Bot():
    '''
    The base class for a pokerbot.
    '''

    def __init__(self):
        '''
        Initialize the bot with hand ranges.
        '''
        self.hand_ranges = {
            "fantastic": {"AA", "KK", "QQ", "JJ", "TT", "AK"},
            "great": {"AQ", "AJ", "KQ", "88", "99"},
            "decent": {"22", "33", "44", "55", "66", "77", "T9s", "JTs"},
            "speculative": {"A5s", "K7s", "QJs", "T8s"}
        }

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
        pass

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
        pass

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
        legal_actions = round_state.legal_actions()
        if RaiseAction in legal_actions:
            _, max_raise = round_state.raise_bounds()  # Raise
            return RaiseAction(max_raise)  # All-in
        elif CallAction in legal_actions:
            return CallAction()  # Call
        elif CheckAction in legal_actions:
            return CheckAction()  # Check
        return FoldAction()  # Fold
