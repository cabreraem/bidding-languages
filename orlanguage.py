from biddinglanguage import BiddingLanguage
from pulp import *


class OR(BiddingLanguage):
    """Class implementing OR/OR* bidding language."""

    def __init__(self, bids):

        # Verify that bids are represented as a list
        if type(bids) != list:
            raise TypeError("Bids must be a list.")

        total_items = []
        # Check that each bid is a tuple of an items list and a corresponding numeric value
        for bid in bids:
            if type(bid) != tuple:
                raise TypeError("Each bid must be a tuple.")
            if len(bid) != 2:
                raise TypeError("Each bid must be made of two items: an item list and a value.")
            items, value = bid
            if type(value) != float and type(value) != int:
                raise TypeError("Value must be of a numeric type.")
            if type(items) != list:
                raise TypeError("Items must be in a list.")
            total_items.extend(items)

        # instantiate fields
        self.bids = bids
        self.join = "OR"
        self.size = len(bids)
        self.items = list(set(total_items))


    def __str__(self):
        result = str(self.bids[0])
        for i in range(1, self.size):
            result += " "+ self.join + " "
            result += str(self.bids[i])
        return result

    def to_OR(self):
        return self

    def WDP(self):
        """Solve the winner determination problem using the pulp linear programming package."""

        # set up our problem, variables, and constraints
        problem = LpProblem('winner_determination', LpMaximize)
        variables = []
        values = []
        constraints = {k: [] for k in self.items}

        # Create decision variable and value for each atom
        for i,atom in enumerate(self.bids):
            z = LpVariable('z{}'.format(i + 1), 0, 1, LpBinary)
            items, value = atom
            variables.append(z)
            values.append(value)
            # add variable to it's item
            for item in items:
                constraints[item].append(z)
        
        # create objective function value*variable
        problem += lpDot(values, variables)

        # add constraints
        for item, var in constraints.items():
            if len(var) > 1:
                problem += lpSum(var) <= 1

        # Solve the integer program
        winners = []
        status = problem.solve()
        for i in range(len(variables)):
            if variables[i].value() >= 1:
                winners.append((i, self.bids[i][0], self.bids[i][1]))

        # return winners: list of tuples (winner index, winner items, winner value)
        return winners
