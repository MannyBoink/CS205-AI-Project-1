import heapq as queue
import copy
import time

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
            return
        
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


generalSearch(board_size = 3, initialState = sample, heuristic = None)
generalSearch(board_size = 3, initialState = sample, heuristic = "Misplaced Tile")
generalSearch(board_size = 3, initialState = sample, heuristic = "Manhattan Distance")