import random, itertools, string, copy

###############################################
# Functions supplied for you
###############################################

def stringProduct(L):
    # This helper function (which is extremely useful for makeSuperSetDeck)
    # is provided for students, since it uses some concepts we have not
    # yet covered.  This takes a list of strings and returns a list of
    # their product -- that is, a list of strings where the first character
    # is any letter from the first string, the second character is the any
    # letter from the second string, and so on.
    # For example:
    # stringProduct(['AB', 'CDE']) returns ['AC', 'AD', 'AE', 'BC', 'BD', 'BE']
    # Also:
    # stringProduct(['AB', 'CD', 'EFG']) returns ['ACE', 'ACF', 'ACG', 'ADE',
    #                                             'ADF', 'ADG', 'BCE', 'BCF',
    #                                             'BCG', 'BDE', 'BDF', 'BDG']   
    resultTuples = list(itertools.product(*L))
    resultStrings = [''.join(t) for t in resultTuples]
    return resultStrings

def combinations(L, n):
    # This helper function (which is extremely useful for findFirstSet)
    # is provided for students, since it uses some concepts we have not
    # yet covered.  
    # Given a list of values L and a non-negative integer n,
    # this function returns a list of all the possible lists
    # made up of any n values in L.
    # For example:
    # combinations(['A', 'B', 'C', 'D'], 2) returns:
    # [['A', 'B'], ['A', 'C'], ['A', 'D'], ['B', 'C'], ['B', 'D'], ['C', 'D']]
    # See how this is a list of all the possible lists made up of
    # any 2 values in L.
    # Also, order does not matter.  See how ['A', 'B'] is in the result
    # and so ['B', 'A'] is not.
    return [list(v) for v in itertools.combinations(L, n)]

###############################################
# Functions for you to write
###############################################

def allSame(L):
    # Returns True if all the values in the list L are equal and False
    # otherwise.  You may assume L is non-empty.
    for i in range(len(L)-1):
        if L[i] != L[i+1]:
            return False
    return True

def allDiffer(L):
    # Returns True if all the values in the list L are different and False
    # otherwise.  You may assume L is non-empty.
    for i in range(len(L)-1):
        if L[i] in L[i+1:]:
            return False
    return True

def isSet(cards):
    # Given a list of cards, return True if those cards form a set,
    # and False otherwise.
    # Here you may assume the list of cards is non-empty and that each card
    # is a string of valid options from the same list of possible features.
    # Thus, just confirm that for every feature, every card either has the
    # same option or every card has a different option.
    currFeature = []
    lengthCards = len(cards)
    lengthFeatures = len(cards[0])
    for i in range(len(cards[0])):
        for j in range((len(cards))):
            currFeature.append(cards[j][i])
        if not (allSame(currFeature) or allDiffer(currFeature)):
            return False
        currFeature = []
    return True

def makeSuperSetDeck(dims):
    # This generates all possible cards with the given dimensions
    # and returns them in a sorted list.
    # For example, consider makeSuperSetDeck([3,4]):
    # Here, there are two features:
    #     * feature0 has 3 features ('A', 'B', or 'C')
    #     * feature1 has 4 features ('A', 'B', 'C', or 'D')
    # Each card in the deck includes an option from each feature,
    # resulting in this deck:
    # ['AA', 'AB', 'AC', 'AD', 'BA', 'BB', 'BC', 'BD', 'CA', 'CB', 'CC', 'CD']
    # Thus, makeSuperSetDeck([3,4]) returns that list.
    # Hint: use stringProduct() here!
    letters = ["A", "B", "C", "D", "E"]
    temp = ""
    features = []
    for i in range(len(dims)):
        for j in range(dims[i]):
            temp += letters[j]
        features.append(temp)
        temp = ""
    resultStrings = stringProduct(features)
    return resultStrings

def boardContainsSelection(board, selection):
    # helper function for checkSelectionIsSet()
    # Return True if every card in the selection (a list of cards) is
    # also on the board (another list of cards), and False otherwise.
    for card in selection:
        if card not in board:
            return False
    return True

def checkSelectionIsSet(board, selection, cardsPerSet):
    # Given a board (a list of cards from the deck), a selection
    # (a non-empty list of cards on the board), and the cardsPerSet
    # (a positive number of cards required to make a set), return True
    # if the selection is legal and in fact forms a set.
    # Instead of returning False, return a string with a
    # description of why the selection is not a set, as such:
    # 1. If the board is empty, return 'Empty board!'
    # 2. If the number of cards in the selection does not match the
    #    required number of cards in a set, return 'Wrong number of cards!'
    # 3. If any of the cards in the selection are not actually on the board,
    #    return 'Some of those cards are not on the board!'
    # 4. If any of the cards in the selection are duplicates,
    #    return 'Some of those cards are duplicates!'
    # 5. If the cards in the selection do not form a legal set,
    #    return 'Those cards do not form a set!'
    if board == []:
        return "Empty board!"
    elif len(selection) != cardsPerSet:
        return "Wrong number of cards!"
    elif not boardContainsSelection(board, selection):
        return "Some of those cards are not on the board!"
    for i in range(len(selection)):
        if selection[i] in selection[i+1:]:
            return "Some of those cards are duplicates!"
    if not isSet(selection):
        return "Those cards do not form a set!"
    return True

def findFirstSet(board, cardsPerSet):
    # helper function for dealUntilSetExists()
    # Given a possibly-empty board, and a positive number of cards per set,
    # loop over combinations(board, cardsPerSet) and return the
    # first list of cards that are on the board and form a set.  Return None
    # if there are no sets on the board.
    # Note that this function will be tested when we test dealUntilSetExists.
    # Hint: you will want to use the combinations() helper function
    # that we provided above.
    if board == []:
        return None
    combos = combinations(board, cardsPerSet)
    for combo in combos:
        if checkSelectionIsSet(board, combo, cardsPerSet) == True:
            return combo
    return None

def dealUntilSetExists(deck, cardsPerSet):
    # Start with an empty board.
    # Keep adding cards from the top of the deck (that is, "dealing")
    # (without modifying the deck) to the board until
    # there is a set among the cards in the board.
    # Return a sorted list of just the cards that form that set.
    # Notes:
    #  1. This function does not deal a fixed number of cards.  It keeps
    #     dealing until it finds a set, no matter how many cards that requires.
    #  2. You can ignore the error case where the deck runs out
    #     of cards before a set is found -- that is, you should never return None.
    # Hint: findFirstSet will be useful here.
    board = []
    i = 0
    while findFirstSet(board, cardsPerSet) == None:
        board.append(deck[i])
        i += 1
    result = findFirstSet(board, cardsPerSet)
    return sorted(result)

def getRandomBoardWithSet(dims, targetBoardSize):
    # Make a new SuperSet deck with the given dimensions,
    # then shuffle the deck, deal cards until a set is dealt.
    # Call that the foundSet.
    # Then, form a board starting with that set, and adding
    # more cards from the deck (that are not already in the set)
    # until the board is the given size.  Then sort and return it
    # in a tuple along with the foundSet.
    # Hint: to randomly shuffle a list L, do this:  random.shuffle(L),
    # which mutatingly shuffles (randomizes the order) of the list L.
    cardsPerSet = min(dims)
    deck = makeSuperSetDeck(dims)
    random.shuffle(deck)
    foundSet = dealUntilSetExists(deck, cardsPerSet)
    for card in foundSet:
       deck.remove(card) 
    board = copy.copy(foundSet)
    i = 0
    while len(board) < targetBoardSize:
       board.append(deck[i])
       i += 1
    board.sort()
    return(board, foundSet)
   

###############################################
# End of Functions for you to write
# (You do not need to edit below here)
###############################################

###############################################
# Console-Based playSuperSet (for debugging)
###############################################

# We are providing these functions to you so that once you write
# the helper functions above, you can play a simplified version of
# SuperSet in the console.  Of course, it's more fun and engaging
# to make a nice animated version of the game, which is your next step.
# But it's also nice to get something running at this point.  :-)

def playSuperSetGame(dims, targetBoardSize, rounds):
    print(f'''\
-------
New game: rounds={rounds}, dims={dims}, targetBoardSize={targetBoardSize}
Enter h for a debugging hint.
Enter a to autoplay.
-------''')
    cardsPerSet = min(dims)
    for roundNumber in range(rounds):
        print(f'Round {roundNumber+1} of {rounds}:')
        board, foundSet = getRandomBoardWithSet(dims, targetBoardSize)
        if foundSet == None:
            print('Could not generate random board. Giving up (sorry).')
            return
        hint = ' '.join(foundSet)
        playSuperSetRound(board, hint, cardsPerSet)
    print('Game over!')

def playSuperSetRound(board, hint, cardsPerSet):
    while True:
        print(f'board: {board}')
        response = input(f'Enter set of {cardsPerSet} cards--> ')
        if response == '':
            continue
        elif response == 'h':
            print(f'hint (for debugging): {hint}')
            continue
        elif response == 'a':
            print(f'autoplaying: {hint}')
            response = hint
        selection = response.split()
        result = checkSelectionIsSet(board, selection, cardsPerSet)
        if result == True:
            print('Yes!\n')
            return
        else:
            print(result) # this is the error message

def playSuperSet():
    while True:
        print('\nSuperSet!')
        print('Levels: 0 (easy) - 6 (hard)')
        response = input('Enter level [or q to quit] --> ')
        if response == 'q':
            break
        level = int(response)
        if level == 0:   dims, targetBoardSize = [3, 3], 4
        elif level == 1: dims, targetBoardSize = [3, 4], 4
        elif level == 2: dims, targetBoardSize = [4, 5], 4
        elif level == 3: dims, targetBoardSize = [3, 3, 3], 5
        elif level == 4: dims, targetBoardSize = [3, 3, 3, 3], 5
        elif level == 5: dims, targetBoardSize = [3, 3, 3, 3, 3], 6
        elif level == 6: dims, targetBoardSize = [4, 4, 4], 6
        else: print('Invalid level'); return
        rounds = 3
        playSuperSetGame(dims, targetBoardSize, rounds)
    print('Goodbye!')

###############################################
# Test Functions
###############################################

def testAllSame():
    print('Testing allSame()...', end='')
    assert(allSame(['A', 'A', 'A']) == True)
    assert(allSame(['A', 'A', 'B']) == False)
    assert(allSame(['A', 'B', 'A']) == False)
    assert(allSame(['B', 'A', 'A']) == False)
    assert(allSame(['A', 'B', 'C']) == False)
    assert(allSame(['A', 'A']) == True)
    assert(allSame(['A', 'A', 'A', 'A', 'A']) == True)
    assert(allSame(['A', 'B']) == False)
    assert(allSame(['A', 'A', 'A', 'B', 'A']) == False)
    print('Passed!')

def testAllDiffer():
    print('Testing allDiffer()...', end='')
    assert(allDiffer(['A', 'A', 'A']) == False)
    assert(allDiffer(['A', 'A', 'B']) == False)
    assert(allDiffer(['A', 'B', 'A']) == False)
    assert(allDiffer(['B', 'A', 'A']) == False)
    assert(allDiffer(['A', 'B', 'C']) == True)
    assert(allDiffer(['A', 'A']) == False)
    assert(allDiffer(['A', 'B', 'C', 'D', 'A']) == False)
    assert(allDiffer(['A', 'B']) == True)
    assert(allDiffer(['A', 'B', 'C', 'D', 'E']) == True)
    print('Passed!')

def testIsSet():
    print('Testing isSet()...', end='')
    assert(isSet(['AAA', 'BBB', 'CCC']) == True)
    assert(isSet(['AAA', 'AAB', 'AAC']) == True)
    assert(isSet(['AAA', 'AAB', 'ABA']) == False)
    assert(isSet(['AAA', 'AAB', 'AAC', 'BBB']) == False)
    assert(isSet(['DAA', 'CAB', 'BAC', 'AAD']) == True)
    print('Passed!')

def testMakeSuperSetDeck():
    print('Testing makeSuperSetDeck()...', end='')
    assert(makeSuperSetDeck([2,2]) == ['AA', 'AB', 'BA', 'BB'])
    assert(makeSuperSetDeck([2,3]) == ['AA', 'AB', 'AC', 'BA', 'BB', 'BC'])
    assert(makeSuperSetDeck([3,2]) == ['AA', 'AB', 'BA', 'BB', 'CA', 'CB'])
    assert(makeSuperSetDeck([4,3]) == ['AA', 'AB', 'AC',
                                       'BA', 'BB', 'BC',
                                       'CA', 'CB', 'CC',
                                       'DA', 'DB', 'DC'])
    assert(makeSuperSetDeck([3,2,2]) == ['AAA', 'AAB', 'ABA', 'ABB',
                                         'BAA', 'BAB', 'BBA', 'BBB',
                                         'CAA', 'CAB', 'CBA', 'CBB'])
    print('Passed!')

def testCheckSelectionIsSet():
    print('Testing checkSelectionIsSet()...', end='')
    assert(checkSelectionIsSet([ ], ['AB'], 2) ==
                               'Empty board!')
    assert(checkSelectionIsSet(['AB'], ['AB'], 2) ==
                               'Wrong number of cards!')
    assert(checkSelectionIsSet([ 'AB' ], ['AB', 'BA'], 2) ==
                               'Some of those cards are not on the board!')
    assert(checkSelectionIsSet([ 'AB' ], ['AB', 'AB'], 2) ==
                               'Some of those cards are duplicates!')
    assert(checkSelectionIsSet(['AAA','BBB','CCC','ABC'],
                               ['AAA','BBB','ABC'], 3) ==
                               'Those cards do not form a set!')
    assert(checkSelectionIsSet(['AAA','BBB','CCC','ABC'],
                               ['AAA','BBB','CCC'], 3) ==
                               True)
    print('Passed!')

def testDealUntilSetExists():
    print('Testing dealUntilSetExists()...', end='')
    deck = ['AAA','ABC','BBB','CCC','CBA']
    foundSet = dealUntilSetExists(deck, 3)
    assert(foundSet == ['AAA', 'BBB', 'CCC'])
    assert(deck == ['AAA','ABC','BBB','CCC','CBA'])

    deck = ['ABC','BBB','CCC','CBA','AAA']
    foundSet = dealUntilSetExists(deck, 3)
    assert(foundSet == ['ABC', 'BBB', 'CBA'])
    assert(deck == ['ABC','BBB','CCC','CBA','AAA'])

    deck = ['ABCD','BBBB','CCCC', 'BCDA', 'AAAA', 'DDDD', 'CDAB', 'DABC']
    foundSet = dealUntilSetExists(deck, 4)
    assert(foundSet == ['AAAA', 'BBBB', 'CCCC', 'DDDD'])
    assert(deck==['ABCD','BBBB','CCCC', 'BCDA', 'AAAA', 'DDDD', 'CDAB', 'DABC'])
    print('Passed!')

def testGetRandomBoardWithSet():
    print('Testing getRandomBoardWithSet()...', end='')
    deck = ['AAA', 'AAB', 'AAC', 'ABA', 'ABB', 'ABC', 'ACA', 'ACB', 'ACC',
            'BAA', 'BAB', 'BAC', 'BBA', 'BBB', 'BBC', 'BCA', 'BCB', 'BCC',
            'CAA', 'CAB', 'CAC', 'CBA', 'CBB', 'CBC', 'CCA', 'CCB', 'CCC']
    boards = [ ]
    duplicateBoardsCount = 0
    totalBoards = 100
    for _ in range(totalBoards):
        dims = [3,3,3]
        targetBoardSize = 4
        board, foundSet = getRandomBoardWithSet(dims, targetBoardSize)
        # check board size
        assert(len(board) == targetBoardSize)
        # check if this is a duplicate board:
        if board in boards:
            duplicateBoardsCount += 1
        boards.append(board)
        # verify the board is legal: all different values, all from the deck:
        assert(allDiffer(board))
        for card in board:
            assert(card in deck)
        # verify the foundSet is in fact a legal set on the board:
        selection = foundSet
        cardsPerSet = min(dims)
        assert(checkSelectionIsSet(board, selection, cardsPerSet) == True)
    # Verify boards are unique.  Except... Since boards are
    # shuffled randomly, there is some tiny chance of duplicate
    # boards, so we will only print a warning if there are just a
    # few duplicates, and actually outright fail if there are more than a few.
    # Our sample solution had 0-4 duplicate boards per 100, so we'll be
    # more liberal here and allow up to 25 duplicate boards per 100.
    assert(duplicateBoardsCount < totalBoards/4)
    print('Passed!')

def testAll():
    testAllSame()
    testAllDiffer()
    testIsSet()
    testMakeSuperSetDeck()
    testCheckSelectionIsSet()
    testDealUntilSetExists()
    testGetRandomBoardWithSet()

###############################################
# main
###############################################

def main():
    testAll()
    playSuperSet()

main()
