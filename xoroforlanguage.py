from biddinglanguage import BiddingLanguage
from orlanguage import OR
from xorlanguage import XOR

import copy

class XORofOR(BiddingLanguage):
    """Class implementing XORofOR bidding language."""

    def __init__(self, bids):

        # Verify that bids are represented as a list
        if type(bids) != list:
            raise TypeError("Bids must be a list.")

        total_items = []
        size = 0
        # Check that each bid is another OR bid
        for bid in bids:
            if type(bid) != OR:
                raise TypeError("Each bid must be of type OR.")
            size += bid.size
            total_items.extend(bid.items)

        # instantiate fields
        self.bids = bids
        self.join = "XOR"
        self.size = size
        self.items = list(set(total_items))

    def __str__(self):
        result = "(" + str(self.bids[0]) + ")"
        for i in range(1, len(self.bids)):
            result += " "+ self.join + " "
            result += "(" + str(self.bids[i]) + ")"
        return result

    def to_OR(self):
        """Translates XORofOR bid to the OR* bidding language."""

        new_bids = []
        current_items = list(self.items)
        dummy = "d"
        i = 0
        clause_index = 0
        curr_index = 0
        dummies_per_bid = [[] for k in range(self.size)]
        
        # iterate through every OR clause in the bid
        for i in range(len(self.bids)):
            or_clause = self.bids[i]
            clause_index += len(or_clause.bids)

            # iterate through every bid in the clause
            for items, value in or_clause.bids:
                bid_dummies = []
                # create a dummy variable for every other bid not in the current clause
                for x in range(clause_index, self.size):
                    while dummy in current_items:
                        dummy = "d" + str(i)
                        i += 1
                    bid_dummies.append(dummy)
                    current_items.append(dummy)
                    dummies_per_bid[x].append(dummy)

                # create new clause with previous dummies and it's newly created ones 
                new_items = list(items)
                new_items.extend(dummies_per_bid[curr_index])
                new_items.extend(bid_dummies)
                new_bids.append((new_items, value))
                curr_index += 1
        return OR(new_bids)  

    def WDP(self):
        """Solves winner determination problem."""
        or_bid = self.to_OR()
        return or_bid.WDP()


