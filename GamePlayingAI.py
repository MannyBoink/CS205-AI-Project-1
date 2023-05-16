import heapq as queue
import copy
import time
import matplotlib.pyplot as plt

def printBoard(state): 
    grid_0 = f" _______________"
    grid_1 = f"|| {state[0][0]} | {state[0][1]} | {state[0][2]} ||\n"
    grid_2 = f"|| {state[1][0]} | {state[1][1]} | {state[1][2]} ||\n"
    grid_3 = f"|| {state[2][0]} | {state[2][1]} | {state[2][2]} || "
    print(grid_0, "\n", grid_1, grid_2, grid_3)

def generalSearch(board_size = 3, initialState=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], heuristic = None, verbose = False):
    goal = None
    if board_size == 3:
        goal = goal8
    if board_size == 4:
        goal = goal15

    def h(state, heuristic):
        # Check for Uniform Cost Search
        if heuristic == None:
            return 0
        # Create the goal state hashmap to get the number of misplaced Tiles and Manhattan Distance
        goalStateMap = {}
        for i in range(board_size):
            for j in range(board_size):
                goalStateMap[goal[i][j]] = [i, j]
        
        misplacedTileSum = 0
        manhattanDistance = 0
        for row in range(board_size):
            for col in range(board_size):
                if state[row][col] != 0 and goalStateMap[state[row][col]] != [row, col]:
                    misplacedTileSum += 1
                    manhattanDistance += abs(goalStateMap[state[row][col]][0] - row) + abs(goalStateMap[state[row][col]][1] - col)

        if heuristic == "Misplaced Tile":
            return misplacedTileSum
        else:
            return manhattanDistance

    def isValid(i, j):
        return i >= 0 and i < board_size and j >= 0 and j < board_size
    
    def isGoalState(state):
        if state == goal:
            return True
        return False

    def makeString(state):
        stringChars = ""
        for row in state:
            for col in row:
                stringChars += str(col)
        return stringChars

    def locateBlankTile(state):
        for row in range(board_size):
            for col in range(board_size):
                if state[row][col] == 0:
                    return (row, col)
    
    def swapBlankOperator(state, blankX, blankY, neighborX, neighborY):
        state[blankX][blankY], state[neighborX][neighborY] = state[neighborX][neighborY], state[blankX][blankY]
        return state
        
    start = time.time()
    distanceMap, depthMap = {}, {}
    visitedNodes = set()

    initState = makeString(initialState)
    depthMap[initState] = 0
    distanceMap[initState] = h(initialState, heuristic) #g(n) = 0 for any search and h(n) = 0 for Uniform Cost Search
    nodes = [(distanceMap[initState], initialState)]    
    maxQueue = 0
    exploredCount = 0

    while nodes:
        if heuristic is None:
            node = nodes.pop(0)
        else: 
            node = queue.heappop(nodes) # node[0] is the distance of node[1] from initialState
        nodeVisited = makeString(node[1]) # Switching to String for hashing
        #Printing the Exploration
        if verbose:
            print("Exploring State for g(n) =", distanceMap[nodeVisited], "and h(n)=", h(node[1], heuristic))
            for row in node[1]:
                print(row)

        #Check for Goal State
        if isGoalState(node[1]):
            end = time.time()
            print("Goal State Reached!")
            print("Solution Depth:", distanceMap[makeString(goal)])
            print("Nodes Explored:", exploredCount)
            print("Max Queue Size:", maxQueue)
            print("Time Taken: %.3f" %(end - start), "seconds")
            return exploredCount, maxQueue, (end - start)
        
        # Add to Visited and increase count of explored nodes. The algorithm later explores the node to its completeness.

        visitedNodes.add(nodeVisited)
        exploredCount += 1

        #Locating the Blank Tile to Create neighbors
        locateBlank = locateBlankTile(node[1])
        
        for x in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Operator List: [Move Blank Left, Move Blank Right, Move Blank Up, Move Blank Down]
            neighborX = locateBlank[0] + x[0]
            neighborY = locateBlank[1] + x[1]
            
            if not isValid(neighborX, neighborY): # Neighbor is an illegal state
                continue

            neighborState = copy.deepcopy(node[1])
            neighborState = swapBlankOperator(neighborState, locateBlank[0], 
                                              locateBlank[1], neighborX, neighborY) # Applying Operator to state
            
            neighborHashableState = makeString(neighborState) # For Hashing
            
            if neighborHashableState not in visitedNodes: # New Node that hasn't been explored before
                distanceMap[neighborHashableState] = depthMap[nodeVisited] + 1 + h(neighborState, heuristic) # h in Uniform Cost = 0
                depthMap[neighborHashableState] = depthMap[nodeVisited] + 1 # g(n)
                if heuristic is None: # FIFO Queue for Uniform Cost Search
                    nodes.append((depthMap[neighborHashableState], neighborState))
                    visitedNodes.add(neighborHashableState)
                else: # Priority Queue for A* based on heuristic input by the user
                    queue.heappush(nodes, (distanceMap[neighborHashableState], neighborState))
                maxQueue = max(maxQueue, len(nodes)) # Compute the maximum Queue Length

    print("FAILURE!")
    return 0, 0, 0

def testTime():
    depth = [0, 1, 2, 4, 7, 24, 31]
    UCSearchTime = []
    UCSearchNodesExplored = []
    UCSearchMaxQueue = []
    MTHeuristicTime = []
    MTSearchNodesExplored = []
    MTSearchMaxQueue = []
    MDHeuristicTime = []
    MDSearchNodesExplored = []
    MDSearchMaxQueue = []
    for state in [trivial, veryEasy, easy, doable, sample, depth24, oh_boy]:
        
        EC, MQ, T = generalSearch(board_size=3, initialState=state, heuristic=None)
        UCSearchTime.append(T)
        UCSearchNodesExplored.append(EC)
        UCSearchMaxQueue.append(MQ)

        EC, MQ, T = generalSearch(board_size=3, initialState=state, heuristic="Misplaced Tile")
        MTHeuristicTime.append(T)
        MTSearchNodesExplored.append(EC)
        MTSearchMaxQueue.append(MQ)

        EC, MQ, T = generalSearch(board_size=3, initialState=state, heuristic="Manhattan Distance")
        MDHeuristicTime.append(T)
        MDSearchNodesExplored.append(EC)
        MDSearchMaxQueue.append(MQ)
    
    plt.plot(depth, UCSearchTime, label = 'Uniform Cost Search')
    plt.plot(depth, MTHeuristicTime, label = 'A* with Misplaced Tile Heuristic')
    plt.plot(depth, MDHeuristicTime, label = 'A* with Manhattan Distance Heuristic')
    plt.show()

trivial = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 0]]

veryEasy = [[1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]]

easy = [[1, 2, 0],
        [4, 5, 3],
        [7, 8, 6]]

doable = [[0, 1, 2],
          [4, 5, 3],
          [7, 8, 6]]

oh_boy = [[6, 4, 7],
          [8, 5, 0],
          [3, 2, 1]]

depth24 = [[0, 7, 2],
           [4, 6, 1],
           [3, 5, 8]]

sample = [[4, 1, 2],
          [5, 3, 0],
          [7, 8, 6]]

goal8 = [[1, 2, 3], 
         [4, 5, 6], 
         [7, 8, 0]]

goal15 = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12],
          [13, 14, 15, 0]]

if __name__ == "__main__":
    #testTime() # Optional Call to plot graphs.
    print("Welcome to the 8-Puzzle. The sample initial States are:")
    print()
    print("Trivial")
    printBoard(veryEasy)
    print()
    print("Easy")
    printBoard(easy)
    print()
    print("Manageable")
    printBoard(doable)
    print()
    print("Slides Example")
    printBoard(sample)
    print()
    print("Here We Go")
    printBoard(oh_boy)
    print()
    print("The Goal State is:")
    printBoard(goal8)
    print()
    while True:
        print("You can keep playing this. If you want to exit, press 8, to play, press 1.")
        playQuestionMark = int(input())
        if playQuestionMark == 8:
            print("Thank You for Playing. Have a Good Day ahead!")
            break
        elif playQuestionMark != 1:
            continue
        print("Enter the Initial State or Use one of the samples available. Press 1 if you would like to enter your own initial state" 
              ", else Press 2")
        initialQuestionMark = int(input())
        newInitialState = None
        if initialQuestionMark == 1:
            print("Please enter the initial state as a 9 character string with no spaces and only numbers from 0-8 in each character.")
            print("The first 3 characters represent the first row, the next 3 the second row and the final 3 characters represent" 
                  " the final row")
            initialString = input()
            while len(initialString != 9):
                print("Your input was wrong, try again")
                initialString = input()
            flag = False
            for char in initialString:
                if int(char) > 8 or int(char) < 0:
                    print("Incorrect String, exiting")
                    flag = True
            
            if flag:
                break

            newInitialState = [[-1 for _ in range(3)] for _ in range(3)]
            i = 0
            j = 0
            for char in initialString:
                newInitialState[i][j] = int(char)
                if j == 2:
                    i += 1
                    j = 0
                else:
                    j += 1
        elif initialQuestionMark == 2:
            print("Enter the title of the sample state you would like to use")
            initialSample = input()
            if initialSample == "Trivial":
                newInitialState = trivial
            elif initialSample == "Very Easy":
                newInitialState = veryEasy
            elif initialSample == "Easy":
                newInitialState = easy
            elif initialSample == "Manageable":
                newInitialState = doable
            elif initialSample == "Slides Example":
                newInitialState = sample
            elif initialSample == "Here We Go":
                newInitialState = oh_boy
            else:
                print("Sorry, could not initialize a sample state, check your casing and spelling and try again!")
                break

        if not newInitialState:
            print("Sorry, unable to initialize state, try again next time!")
            break
        
        print("If you would like to print the states being explored (basically setting the verbosity here), press 1")
        verbosity = int(input())
        if verbosity == 1:
            verbosity = True
        else:
            verbosity = False
        print("Algorithm Choice: 1: Uniform Cost Search, 2: A* with Misplaced Tile Heuristic, 3: A* with Manhattan Distance Heuristic")
        algorithm = int(input())
        if algorithm == 1:
            generalSearch(board_size = 3, initialState = newInitialState, heuristic = None, verbose = verbosity)
        elif algorithm == 2:
            generalSearch(board_size = 3, initialState = newInitialState, heuristic = "Misplaced Tile", verbose = verbosity)
        elif algorithm == 3:
            generalSearch(board_size = 3, initialState = newInitialState, heuristic = "Manhattan Distance", verbose = verbosity)
        else:
            break
        print()