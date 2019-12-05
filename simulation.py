import logging
import random
import sys
from optparse import OptionParser
from orlanguage import OR
from orofxorlanguage import ORofXOR
from xorlanguage import XOR
from xoroforlanguage import XORofOR
import time

def configure_logging(loglevel):
    """Configure logging, as seen in pset 5."""
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    root_logger = logging.getLogger('')
    strm_out = logging.StreamHandler(sys.__stdout__)
    strm_out.setFormatter(logging.Formatter('%(message)s'))
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(strm_out)

def create_items(num_items):
    """Given a number of items, creates a list of unique strings naming each item."""
    items = []
    x = 0
    for i in range(num_items):
        if i < 26:
            items.append(chr(ord('A') + i))
        elif i < 52:
            items.append(chr(ord('a') + (i%26)))
        else:
            items.append(chr(ord('A') + (i%26))+ str(x))
            x += 1
    return items

def make_or_bid(total_items, num_bids, max_items, max_val):
    """Generates a random OR bid from parameters."""
    bids = []
    for i in range(num_bids):
        num_items = random.randint(1, max_items)
        items = random.sample(total_items, num_items)
        val = random.randint(1, max_val)
        bids.append((items, val))
    return OR(bids)

def make_xor_bid(total_items, num_bids, max_items, max_val):
    """Generates a random XOR bid from parameters."""
    bids = []
    for i in range(num_bids):
        num_items = random.randint(1, max_items)
        items = random.sample(total_items, num_items)
        val = random.randint(1, max_val)
        bids.append((items, val))
    return XOR(bids)

def make_orofxor_bid(total_items, num_bids, max_items, max_val, num_clauses):
    """Generates a random ORofXOR bid from parameters."""

    bids = []
    for i in range(num_clauses):
        xor_clause = make_xor_bid(total_items, num_bids // num_clauses, max_items, max_val, num_clauses)
        bids.append(xor_clause)
    return ORofXOR(bids)

def make_xorofor_bid(total_items, num_bids, max_items, max_val, num_clauses):
    """Generates a random XORofOR bid from parameters."""

    bids = []
    for i in range(num_clauses):
        or_clause = make_or_bid(total_items, num_bids // num_clauses, max_items, max_val, num_clauses)
        bids.append(or_clause)
    return XORofOR(bids)

def run_WDP_sim(options, language):
    """Run simulation for the winner determination problem given options."""

    sum_time = 0

    for i in range(1, options.iters + 1):
        logging.info("==== Iteration %d / %d. ====" % (i, options.iters))
        items = create_items(options.num_items)

        # Create bid based on language
        if language == 'OR':
            bid = make_or_bid(items, options.num_bids, options.max_items, options.max_value)
        elif language == 'XOR':
            bid = make_xor_bid(items, options.num_bids, options.max_items, options.max_value)
        elif language == 'XORofOR':
            bid = make_xorofor_bid(items, options.num_bids, options.max_items, options.max_value, options.num_clauses)
        else:
            bid = make_orofxor_bid(items, options.num_bids, options.max_items, options.max_value, options.num_clauses)
        
        # Log each atom in the bid
        logging.info("Number of atoms: %d" % bid.size)
        logging.debug("List of all bids:")
        if language == 'OR' or language == 'XOR':
            for atom in bid.bids:
                logging.debug("\t %s bid on items %s for value %d" % (bid.join, atom[0], atom[1]))
        else:
            for clause in bid.bids:
                logging.debug("\t %s clause:" % bid.join)
                for atom in clause.bids:
                    logging.debug("\t \t %s bid on items %s for value %d" % (clause.join, atom[0], atom[1]))

        # Solve WDP and time its duration
        start_time = time.time()
        winners = bid.WDP()
        duration = time.time() - start_time

        # Log the allocated winners
        logging.debug("List of allocated winners:")
        for winner in winners:
            logging.debug("\t Bidder %d is allocated items %s with value %d." % winner)
        logging.info("\t WDP took %s seconds." % duration)
        sum_time += duration
    
    # Log the average duration of WDP
    avg_time = sum_time / float(options.iters)
    logging.info("\t ==== Summary ====")
    logging.info("\t Average WDP time: %f" % avg_time)

def run_translate_sim(options, language):
    """Run simulation for the translation problem given options."""

    for i in range(1, options.iters + 1):
            logging.info("==== Iteration %d / %d. ====" % (i, options.iters))

            # Create bids given the language
            items = create_items(options.num_items)
            if language == 'XOR':
                bid = make_xor_bid(items, options.num_bids, options.max_items, options.max_value)
            elif language == 'XORofOR':
                bid = make_xorofor_bid(items, options.num_bids, options.max_items, options.max_value, options.num_clauses)
            else:
                bid = make_orofxor_bid(items, options.num_bids, options.max_items, options.max_value, options.num_clauses) 

            # Log original bids and some summary numbers               
            logging.info("\t Current number of atoms: %d" % bid.size)
            logging.info("\t Current number of items: %d" % len(bid.items))
            logging.debug("List of all bids:")
            if language == 'OR' or language == 'XOR':
                for atom in bid.bids:
                    logging.debug("\t %s bid on items %s for value %d" % (bid.join, atom[0], atom[1]))
            else:
                for clause in bid.bids:
                    logging.debug("\t %s clause:" % bid.join)
                    for atom in clause.bids:
                        logging.debug("\t \t %s bid on items %s for value %d" % (clause.join, atom[0], atom[1]))
            
            translated = bid.to_OR()

            # Log translated bids and some summary numbers
            logging.info("\t Translated number of atoms: %d" % translated.size)
            logging.info("\t Translated number of items: %d" % len(translated.items))
            logging.info("\t Dummy items: %d" % (len(translated.items)-len(bid.items)))
            logging.debug("List of all bids:")
            for atom in translated.bids:
                logging.debug("\t OR bid on items %s for value %d" % atom)

def main(args):

    usage_msg = "Usage:  %prog [options] BiddingLanguage"
    parser = OptionParser(usage=usage_msg)

    def usage(msg):
        print("Error: %s\n" % msg)
        parser.print_help()
        sys.exit()
    
    # Add flags to parser as in pset 5
    parser.add_option("--loglevel",
                      dest="loglevel", default="info",
                      help="Set the logging level: 'debug' or 'info'")

    parser.add_option("--num-items",
                      dest="num_items", default=5, type="int",
                      help="Set number of items")

    parser.add_option("--num-bids",
                      dest="num_bids", default=10, type="int",
                      help="Set number of bids")

    parser.add_option("--num-clauses",
                      dest="num_clauses", default=5, type="int",
                      help="Set number of bids in each clause.")

    parser.add_option("--max-items",
                      dest="max_items", default=5, type="int",
                      help="Set max number of items allowed in an atom")

    parser.add_option("--max-value",
                      dest="max_value", default=20, type="int",
                      help="Set max value allowed for a bid")
    
    parser.add_option("--action",
                      dest="action", default='WDP',
                    help="Set action to 'WDP' or 'translate'")

    parser.add_option("--iters",
                      dest="iters", default=1, type="int",
                      help="Number of different runs.")
    
    (options, args) = parser.parse_args()

    # Validate action parameter
    if options.action not in ['WDP', 'translate']:
        raise ValueError("Action flag is invalid, must be 'WDP' or 'translate'")
    
    # Validate language parameter
    if len(args) == 0:
        # default
        language = 'OR'
    elif len(args) == 1:
        c = args[0]
        if c in ['OR', 'XORofOR', 'ORofXOR', 'XOR']:
            language = c
        else:
            raise ValueError("Bad argument, must be one of 'OR', 'XORofOR', 'ORofXOR', 'XOR'")
    else:
        raise ValueError("Only one argument allowed.")

    # Begin logging
    configure_logging(options.loglevel)
    logging.info("Starting simulation...")

    # Run the WDP simulation if selected
    if options.action == 'WDP':
        run_WDP_sim(options, language)

    # Run the translation simulation if selected, and language isn't OR
    elif options.action == 'translate':
        if language == 'OR':
            logging.info("OR bid in final form, can't be translated.")
        else:
            run_translate_sim(options, language)

if __name__ == "__main__":
    main(sys.argv)
