from __future__ import print_function, unicode_literals
from docopt import docopt
from PyInquirer import style_from_dict, Token, prompt, Separator
from orlanguage import OR
from orofxorlanguage import ORofXOR
from xorlanguage import XOR
from xoroforlanguage import XORofOR
import time

# Global style setup for PyInquirer
style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

def create_bid(current_bids):
    """Prompts user for the creation of a bid."""
    var_name = [
            {
                'type': 'input',
                'message': 'Input a variable name:',
                'name': 'var'
            } ]

    language_question = [
            {
                'type': 'list',
                'message': 'Select a bidding language',
                'name': 'language',
                'choices': [
                    {
                        'name': 'OR'
                    },
                    {
                        'name': 'XOR'
                    },
                    {
                        'name': 'XOR of OR'
                    },
                    {
                        'name': 'OR of XOR'
                    }
                ]
            }
    ]

    # Keep prompting for a variable name until it is valid (alphanumeric and not already in use)
    while True:
        response = prompt(var_name, style=style)
        var = response['var']
        # validate variable
        if not var.isalnum():
            print("Variable name must only contain of alphanumeric characters.")
        elif var in current_bids.keys():
            print("That variable name is already taken")
        else:
            break
    
    language = prompt(language_question, style=style)['language']

    # Create bid based on given language
    if language == 'OR' or language == 'XOR':
        atoms = make_simple_bid()
        if language == 'OR':
            bid = OR(atoms)
        else:
            bid = XOR(atoms)
    elif language == 'OR of XOR':
        bid = make_orofxor_bid()
    else:
        bid = make_xorofor_bid()
    
    # Add bid to current bids and print the final bid form
    current_bids[var] = bid
    print("%s = %s" % (var, bid))
    return current_bids

def make_simple_bid():
    """Creates bid list for OR or XOR bids."""

    bids = []
    while True:
        val_question = [
        {
            'type': 'input',
            'message': 'Input value of bid:',
            'name': 'value'
        } ]
        question = [
            {
                'type': 'input',
                'message': 'Input items separated by a comma:',
                'name': 'items'
            }
        ]
        response = prompt(question, style=style)
        items = [x.strip() for x in response['items'].split(',')]

        # Keep prompting for a value until it is valid
        while True:
            response = prompt(val_question, style=style)
            value = response['value']
            try:
                value = float(value)
                break
            except ValueError:
                print("Value must be a number")
       
        # Create new atom
        atom = (items, value)
        print("Adding atom %s to new bid." % str(atom))
        bids.append(atom)

        # Ask to create another atom, if not exit loop
        question = [
            {
                'type': 'confirm',
                'message': 'Add another atom?',
                'name': 'confirm'
            },
        ]
        response = prompt(question, style=style)
        if not response['confirm']:
            break
    return bids

def make_orofxor_bid():
    """Create ORofXOR bid through user prompt."""

    num_clauses = 1
    clauses = []
    while True:
        # For each clause make a simple XOR bid
        print("Create XOR clause %d:" % num_clauses)
        atoms = make_simple_bid()
        clause = XOR(atoms)
        clauses.append(clause)
        num_clauses += 1

        # Prompt user if they want another clause
        question = [
            {
                'type': 'confirm',
                'message': 'Add another clause?',
                'name': 'confirm'
            },
        ]
        response = prompt(question, style=style)
        if not response['confirm']:
            break
    return ORofXOR(clauses)

def make_xorofor_bid():
    """Create XORofOR bid through user prompt."""

    num_clauses = 1
    clauses = []
    while True:
        # For each clause make a simple OR bid
        print("Create OR clause %d:" % num_clauses)
        atoms = make_simple_bid()
        clause = OR(atoms)
        clauses.append(clause)
        num_clauses += 1
    
        # Prompt user if they want another clause
        question = [
            {
                'type': 'confirm',
                'message': 'Add another clause?',
                'name': 'confirm'
            },
        ]
        response = prompt(question, style=style)
        if not response['confirm']:
            break
    return XORofOR(clauses)

def solve_bid(current_bids):
    """Solve winner determination problem for a selected bid."""

    # Create bid choices out of current_bids
    choices = [{'name': bid} for bid in current_bids]
    question = [
            {
                'type': 'list',
                'message': 'Select a bid to solve',
                'name': 'bid',
                'choices': choices,
                'validate': lambda answer: 'You must choose a bid to solve.' \
                    if len(answer) == 0 else True
            },
            
    ]
    bid_name = prompt(question, style=style)['bid']

    # Retrieve bid by variable name and solve
    bid = current_bids[bid_name]
    bid = bid.to_OR()
    start_time = time.time()
    winners = bid.WDP()
    duration = time.time() - start_time

    # Print winners and time
    print("The winners are:")
    for winner in winners:
        print("\t Bidder %d, who is allocated items %s with value %d." % winner)
    print("WDP took %s seconds." % duration)
    
def translate_bid(current_bids):
    """Translate a selected bid to OR."""

    # Create bid choices out of current_bids
    choices = [{'name': bid} for bid in current_bids]
    question = [
            {
                'type': 'list',
                'message': 'Select a bid to solve',
                'name': 'bid',
                'choices': choices,
                'validate': lambda answer: 'You must choose a bid to solve.' \
                    if len(answer) == 0 else True
            },      
    ]
    bid_name = prompt(question, style=style)['bid']
    new_name = bid_name + "_as_OR"
    bid = current_bids[bid_name]
    new_bid = bid.to_OR()

    # Add new translated bid to bids list
    current_bids[new_name] = new_bid
    print("%s = %s" % (new_name, new_bid))
    return current_bids

def main():
    print("Welcome to the Bidding Languages Interpreter.")

    current_bids = {}
    while True:
        question = [
        {
            'type': 'list',
            'message': 'Select an action',
            'name': 'operation',
            'choices': [
                {
                    'name': 'See bids'
                },
                {
                    'name': 'Create bid'
                },
                {
                    'name': 'Solve bid'
                },
                {
                    'name': 'Translate bid to OR'
                },
                {
                    'name': 'Exit'
                }
            ],
            'validate': lambda answer: 'You must choose one action.' \
                if len(answer) == 0 else True}]
        
        operation = prompt(question, style=style)['operation']
        if operation == 'See bids':
            if not current_bids:
                print("There are no bids.")
            else:
                for bid in current_bids:
                    print("%s = %s" % (bid, current_bids[bid]))
        elif operation == 'Create bid':
            current_bids = create_bid(current_bids)
        elif operation == 'Solve bid':
            solve_bid(current_bids)
        elif operation == 'Translate bid':
            current_bids = translate_bid(current_bids)
        else:
            return

if __name__ == "__main__":
    main()