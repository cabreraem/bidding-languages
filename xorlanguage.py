from biddinglanguage import BiddingLanguage
from orlanguage import OR

class XOR(BiddingLanguage):
    """Class implementing XOR bidding language."""

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
        self.join = "XOR"
        self.size = len(bids)
        self.items = list(set(total_items))

    def __str__(self):
        result = str(self.bids[0])
        for i in range(1, self.size):
            result += " "+ self.join + " "
            result += str(self.bids[i])
        return result
    
    def to_OR(self):
        """Translates XOR bid to the OR* bidding language."""
        
        # Create valid dummy variable
        dummy = "d"
        i = 0
        while dummy in self.items:
            dummy = "d" + str(i)
            i += 1
        new_bids = []

        # Add dummy variable to each bid
        for items, value in self.bids:
            new_items = list(items)
            new_items.append(dummy)
            new_bids.append((new_items, value))

        # Construct new OR bid
        return OR(new_bids)

    def WDP(self):
        """Solves winner determination problem."""
        or_bid = self.to_OR()
        return or_bid.WDP()

            


