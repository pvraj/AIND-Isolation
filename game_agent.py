"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
from math import sqrt

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def get_distance_between_2_points(current_player_location, enemy_player_location, maximize_distance):
    '''
        Description: Given as input 2 coordinates, return the distance between them. (If specified, return the distance in negative form).
        :param current_player_location: (tuple of 2 integers) Current player's location in tuple form.
        :param enemy_player_location: (tuple of 2 integers) Enemy player's location in tuple form.
        :param maximize_distance: (boolean). True if maximizing distance. False if minimizing distance. The purpose of this is in heuristics where a greater distance corresponds to a greater score, a positive value is desired. In heuristics where a smaller distance corresponds to a greater score, a negative number is desired (thus the distance is inverted with -1). For example, if maximizing the distance between 2 points, 5 > 1. If minimizing the distance between 2 points, -1 * 1 > -1 * 5.
        :return: (float) Distance between 2 pairs of coordinates as a positive or negative float.
    '''
    current_player_x, current_player_y = current_player_location
    enemy_player_x, enemy_player_y = enemy_player_location
    if maximize_distance:
        return sqrt(((enemy_player_y - current_player_y) ** 2) + ((enemy_player_x - current_player_x) ** 2))
    return -1 * sqrt(((enemy_player_y - current_player_y) ** 2) + ((enemy_player_x - current_player_x) ** 2))

def custom_score(game, player):
    """Description: Calculate the heuristic value of a game state from the point of view of the given player.

    Heuristic: Using the distance formula, maximize the distance between our agent and the center of the board while the ratio of moves to total spaces is < 30% (essentially, use the 'bad moves' first, saving the 'good moves' for last). When the ratio exceeds 30%, return a linear combination consisting of the following: number of moves available to my agent; number of moves available to the enemy agent; number of intersecting moves between the agents; distance between the 2 agents.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    moves_total_spaces_ratio = game.move_count / (game.height * game.width)
    if moves_total_spaces_ratio < 0.30:
        return get_distance_between_2_points(game.get_player_location(player), (game.height/2, game.width/2), True)
    my_moves = frozenset(game.get_legal_moves(player))
    enemy_moves = frozenset(game.get_legal_moves(game.get_opponent(player)))
    return 3*(len(my_moves) - len(enemy_moves)) + len(my_moves.intersection(enemy_moves)) + get_distance_between_2_points(game.get_player_location(player), game.get_player_location(game.get_opponent(player)), True)

def custom_score_2(game, player):
    """Description: Calculate the heuristic value of a game state from the point of view of the given player.

    Heuristic: Using the distance formula, maximize the distance between our agent and the enemy agent while the ratio of moves to total spaces is < 30% (essentially, "run away"). When the ratio exceeds 30%, return a linear combination consisting of the following: number of moves available to my agent; distance between the 2 agents.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    moves_total_spaces_ratio = game.move_count / (game.height * game.width)
    if moves_total_spaces_ratio < 0.30:
        return get_distance_between_2_points(game.get_player_location(player), game.get_player_location(game.get_opponent(player)), True)
    my_moves = frozenset(game.get_legal_moves(player))
    return 3*len(my_moves) + get_distance_between_2_points(game.get_player_location(player), game.get_player_location(game.get_opponent(player)), True)

def custom_score_3(game, player):
    """Description: Calculate the heuristic value of a game state from the point of view of the given player.

    Heuristic: Using the distance formula, minimize the distance between our agent and the enemy agent while the ratio of moves to total spaces is < 30% (essentially, aggressively follow the opponent to attempt to mimic their path and avoid being boxed in). When the ratio exceeds 30%, return a linear combination consisting of the following: number of moves available to my agent; distance between the 2 agents.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    moves_total_spaces_ratio = game.move_count / (game.height * game.width)
    if moves_total_spaces_ratio < 0.30:
        return get_distance_between_2_points(game.get_player_location(player), game.get_player_location(game.get_opponent(player)), False)
    my_moves = frozenset(game.get_legal_moves(player))
    return 2*len(my_moves) + get_distance_between_2_points(game.get_player_location(player), game.get_player_location(game.get_opponent(player)), True)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return (-1, -1) # no valid moves (lose game)

        legal_move_to_score_map = {} # get the score of each legal move {legal_move1: score1, legal_move2: score2, etc...}
        for legal_move in legal_moves:
            legal_move_to_score_map[legal_move] = MinimaxPlayer.minimax_recursion_helper(self, game.forecast_move(legal_move), depth-1, False)
        best_move = max(legal_move_to_score_map, key=lambda k: legal_move_to_score_map[k])
        return best_move # return the move with the highest score

    def minimax_recursion_helper(self, game, depth, is_maximizing_player):
        """
        Description: This helper function implements the recursive portion of the minimax algorithm from the text. When called from the minimax function, minimax_recursion_helper will return the score associated with the best_move to take from the root.

        :param self: (MinimaxPlayer) Minimax player object.
        :param game: (isolation.Board) Isolation game object.
        :param depth: (int) num levels to traverse.
        :param is_maximizing_player: (boolean) True if maximizer node; False if minimizer node.
        :return: score value (float): Score associated with game state.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout() # Raise if time is exceeded.

        if depth == 0:  # Get the score once the depth has reached the limit.
            return self.score(game, self)

        legal_moves = game.get_legal_moves()

        if not legal_moves:  # Get the score if no legal moves (i.e., leaf or dead end).
            return self.score(game, self)

        if is_maximizing_player:  # based on Wikipedia example code. Recursive Minimax.
            best_move_score = float("-inf")
            for child_node_move in legal_moves:  # for each child node, call minimizer.
                child_node_move_score = MinimaxPlayer.minimax_recursion_helper(self, game.forecast_move(child_node_move), depth - 1, False)
                best_move_score = max(best_move_score, child_node_move_score)
            return best_move_score

        else:  # minimizer
            best_move_score = float("inf")
            for child_node_move in legal_moves: # for each child node, call maximizer.
                child_node_move_score = MinimaxPlayer.minimax_recursion_helper(self, game.forecast_move(child_node_move), depth - 1, True)
                best_move_score = min(best_move_score, child_node_move_score)
            return best_move_score


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = (-1, -1) # Initialize with losing move.
        try: # The try/except block will automatically catch the exception raised when the timer is about to expire.
            current_depth = 1
            while True:
                best_move = self.alphabeta(game, current_depth)
                current_depth += 1 # Run alphabeta with increasing depth.
        except SearchTimeout:
            return best_move  # Return the best move from the last completed search iteration.

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return (-1, -1) # No valid moves (lose).

        legal_move_to_score_map = {} # Get the score of each legal move {legal_move1: score1, legal_move2: score2, etc...}
        for legal_move in legal_moves:
            legal_move_to_score_map[legal_move] = AlphaBetaPlayer.alphabeta_recursion_helper(self, game.forecast_move(legal_move), depth - 1, False, alpha, beta) # We start with the root, which is a maximizer (so we pass False).
            alpha = max(alpha, legal_move_to_score_map[legal_move])
        best_move = max(legal_move_to_score_map, key=lambda k: legal_move_to_score_map[k])
        return best_move

    def alphabeta_recursion_helper(self, game, depth, is_maximizing_player, alpha, beta):
        '''
        Description: This helper function implements the recursive portion of the alpha beta algorithm from the text. When called from the alphabeta function, alphabeta_recursion_helper will return the score associated with the best_move to take from the root.

        :param self: (AlphaBetaPlayer) AlphaBetaPlayer object.
        :param game: (isolation.Board) Isolation game object.
        :param depth: (int) Number of levels to traverse.
        :param is_maximizing_player: (boolean) True if maximizer node; False if minimizer node.
        :param alpha: (float) Maximum score on path to the maximizer node.
        :param beta: (float) Minimum score on path to the minimizer node.
        :return: Score value (float): Score associated with the game state.
        '''
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:  # Depth limit reached; return the score.
            return self.score(game, self)

        legal_moves = game.get_legal_moves()

        if not legal_moves:  # Leaf or dead end. Return Score.
            return self.score(game, self)

        if is_maximizing_player: # Recursive alpha beta.
            best_child_node_move_score = float("-inf")
            for child_node_move in legal_moves:  # for each possible child node
                best_child_node_move_score = max(best_child_node_move_score, AlphaBetaPlayer.alphabeta_recursion_helper(self, game.forecast_move(child_node_move), depth - 1, False, alpha, beta))
                if best_child_node_move_score >= beta:
                    return best_child_node_move_score # prune (terminate early)
                alpha = max(alpha, best_child_node_move_score)
            return best_child_node_move_score # return best path to maximizer

        else:  # minimizer
            best_child_node_move_score = float("inf")
            for child_node_move in legal_moves:
                best_child_node_move_score = min(best_child_node_move_score, AlphaBetaPlayer.alphabeta_recursion_helper(self, game.forecast_move(child_node_move), depth - 1, True, alpha, beta))
                if best_child_node_move_score <= alpha:
                    return best_child_node_move_score # prune (terminate early)
                beta = min(beta, best_child_node_move_score)
            return best_child_node_move_score # return best path to minimizer
