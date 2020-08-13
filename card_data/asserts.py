ATT_RANGE = range(-1,5)
STAT_EXPONENTS = {0.7, 1, 1.5, }
    # Atk can also be 100.
        # Only Cloud's Buster Sword.

def check_assumptions(card):
    #0
    
    assert card.att in ATT_RANGE
    assert card.subatt in ATT_RANGE
    assert card.isult in (0,1)
    
    #8
    assert card._UNK09 in range(5)
    assert card.lvmax in range(1,100)
    
    
    #16
        # Guess I should check the exponents are only in a certain set.
        # Only check if lvmax > 1.
    if card.lvmax > 1:
        ...
    ...
    #24
    ...
    #32
    ...
    
    
    #...
    assert card.f_inherits in {0,2,3,6,7}

