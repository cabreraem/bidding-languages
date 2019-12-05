from biddinglanguage import BiddingLanguage
from orlanguage import OR
from xorlanguage import XOR

import copy

class ORofXOR(BiddingLanguage):
    """Class implementing ORofXOR bidding language."""

    def __init__(self, bids):

        # Verify that bids are represented as a list
        if type(bids) != list:
            raise TypeError("Bids must be a list.")

        total_items = []
        size = 0
        # Check that each bid is another XOR bid
        for bid in bids:
            if type(bid) != XOR:
                raise TypeError("Each bid must be of type XOR.")
            size += bid.size
            total_items.extend(bid.items)

        # instantiate fields
        self.bids = bids
        self.join = "OR"
        self.size = size
        self.items = list(set(total_items))

    def __str__(self):
        result = "(" + str(self.bids[0]) + ")"
        for i in range(1, len(self.bids)):
            result += " "+ self.join + " "
            result += "(" + str(self.bids[i]) + ")"
        return result

    def to_OR(self):
        """Translates ORofXOR bid to the OR* bidding language."""

        new_bids = []
        dummy = "d"
        i = 0
        current_items = list(self.items)

        # iterate over every XOR clause in the bid
        for xor_clause in self.bids:
            # create a unique dummy variable for each clause
            while dummy in current_items:
                dummy = "d" + str(i)
                i += 1
            current_items.append(dummy)

            # add dummy variable to each bid within the clause
            for items, value in xor_clause.bids:
                new_items = list(items)
                new_items.append(dummy)
                new_bids.append((new_items, value))
        
        # Construct new OR bid
        return OR(new_bids)  

    def WDP(self):
        """Solves winner determination problem."""
        or_bid = self.to_OR()
        return or_bid.WDP()
            


