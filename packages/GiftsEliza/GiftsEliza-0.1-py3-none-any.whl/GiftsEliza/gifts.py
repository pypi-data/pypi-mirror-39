"""
This is a Gift module that has three methods:
    i) is_mel - checks whether the guests' name matches with 'Mel Melitpolski' or email matches with keyword 'mel',
    ii) most_and_least_common_type - given list of gits, finds the most and the least common gift types
    iii) get_gifts - return the gifts brought in the event 

This module shows various types of documentation available for use with pydoc. 
To generate HTML documentation for this module issue the command:
    pydoc -w gifts
"""

def is_mel(name, email):
    """Is this user Mel?
    >>> is_mel('Mel Melitpolski', 'mel@ubermelon.com')
    True
    >>> is_mel('Judith Butler', 'judith@awesome.com')
    False
    >>> is_mel('Norman Bates', 'mel@ubermelon.com')
    True
    >>> is_mel('Mel Melitpolski', 'norman@batesmotel.com')
    True"""

    return name == "Mel Melitpolski" or email == "mel@ubermelon.com"


def most_and_least_common_type(gifts):
    """Given list of gifts, return most and least common gift types.
    Return most and least common gift types in tuple of format (most, least).
    >>> gifts = [
    ...     {'type': 'dessert'},
    ...     {'type': 'dessert'},
    ...     {'type': 'appetizer'},
    ...     {'type': 'dessert'},
    ...     {'type': 'appetizer'},
    ...     {'type': 'drink'},
    ... ]
    >>> most_and_least_common_type(gifts)
    ('dessert', 'drink')
    >>> gifts = [
    ...     {'type': 'dessert'},
    ...     {'type': 'dessert'},
    ...     {'type': 'dessert'},
    ... ]
    >>> most_and_least_common_type(gifts)
    ('dessert', 'dessert')
    >>> gifts = [
    ...     {'type': 'dessert'},
    ...     {'type': 'appetizer'},
    ...     {'type': 'dessert'},
    ...     {'type': 'appetizer'},
    ...     {'type': 'drink'},
    ... ]
    >>> most_and_least_common_type(gifts)
    ('dessert', 'drink')
    >>> gifts = []
    >>> most_and_least_common_type(gifts)
    (None, None)"""

    types = {}

    # Count number of each type
    for gift in gifts:
        types[gift['type']] = types.get(gift['type'], 0) + 1

    most_count = most_type = None
    least_count = least_type = None

    # Find most, least common
    for gift_type, count in types.items():
        if most_count is None or count > most_count:
            most_count = count
            most_type = gift_type

        if least_count is None or count < least_count:
            least_count = count
            least_type = gift_type

    return (most_type, least_type)


def get_gifts():
    """Return gifts being brought to this event.
    """

    return [
        {'type': 'dessert',
         'description': 'Chocolate mousse',
         'who': 'Leslie'},
        {'type': 'dessert',
         'description': 'Cardamom-Pear pie',
         'who': 'Joel'},
        {'type': 'appetizer',
         'description': 'Humboldt Fog cheese',
         'who': 'Meggie'},
        {'type': 'dessert',
         'description': 'Lemon bars',
         'who': 'Bonnie'},
        {'type': 'appetizer',
         'description': 'Mini-enchiladas',
         'who': 'Katie'},
        {'type': 'drink',
         'description': 'Sangria',
         'who': 'Anges'},
        {'type': 'dessert',
         'description': 'Chocolate-raisin cookies',
         'who': 'Henry'},
        {'type': 'dessert',
         'description': 'Brownies',
         'who': 'Sarah'}
    ]