from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        board = {}
        domains = init_domains()
        restrict_domain(domains, problem)
        decision_stack = []
        for spot in sd_spots:
            board[spot] = None
        while True:
            (board, domains, conflict) = self.propogate(board, domains)
            if not conflict:
                filled = True
                for spot in board:
                    if spot is None:
                        filled = False
                if filled:
                    return domains
                else:
                    (board, x) = self.make_decision(board, domains)
                    decision_stack.append((copy.deepcopy(board), x, copy.deepcopy(domains)))
            else:
                if not decision_stack:
                    return None
                else:
                    (board, domains) = self.backtrack(decision_stack)

        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignment function 
        #   and turn the value into a single element list and return them as a domain map. 

    def propogate(self, board, domains):
        while True:
            for spot in sd_spots:
                if not domains[spot]:
                    return board, domains, True
                if len(domains[spot]) is 1:
                    board[spot] = domains[spot][0]
                if board[spot] is not None and len(domains[spot]) > 1:
                    domains[spot].empty()
                    domains[spot].append(board[spot])
            consistent = True
            for spot in sd_spots:
                if len(domains[spot]) > 1:
                    continue
                else:
                    number = domains[spot][0]
                    for spot_peer in sd_peers[spot]:
                        if number in domains[spot_peer]:
                            consistent = False
                            domains[spot_peer].remove(number)
            if consistent:
                return (board, domains, False)


    def make_decision(self, board, domains):
        for spot in sd_spots:
            if board[spot] is None:
                board[spot] = domains[spot][0]
                return (board, spot)

    def backtrack(self, decision_stack):
        (board, x, domains) = decision_stack.pop()
        a = board[x]
        board[x] = None
        domains[x] = domains[x].remove(a)
        return (board, domains)

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
