import pygame
import pygame.freetype

from pygame.locals import *
from collections import deque
from algos import *

DEFUALT_BOARD = [
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 3]
]

width = 10
height = 10

# 0 is free
# 1 is obstacle
# 2 is start
# 3 is end
# 4 is visited
# 5 is path

# colors
freeColor = (237, 247, 246)
obstacleColor = (38, 96, 164)
startColor = (241, 153, 83)
endColor = (86, 53, 30)
visitedColor = (196, 115, 53)
pathColor = (255, 183, 3)
lineColor = (174, 180, 181)
colors = [["Free", "Obstacle", "Start", "End", "Visited", "Path", "Line"],
        [freeColor, obstacleColor, startColor, endColor, visitedColor, pathColor, lineColor]]

# finds the start and end nodes in the board
def find(board):
    start = None
    end = None
    for i in range(height):
        for j in range(width):
            # start is found
            if board[i][j] == 2:
                start = (i,j)
            # end is found
            elif board[i][j] == 3:
                end = (i,j)

    return (start, end)    

# defines actions when the user has clicked a tile
def userClick(board, currMarker, blocksize, startEnd):
    # gets mouse position
    x, y = pygame.mouse.get_pos()
    if x < width * blocksize:
        # converts mouse position to appropriate row/col values
        row = int(x / blocksize)
        column = int(y / blocksize)
        
        # checks if a start & end already exist in board
        if currMarker == 2 and any(2 in r for r in board):
            startEnd[0] = True
            board[row][column] = board[row][column]
        elif currMarker == 3 and any(3 in r for r in board):
            startEnd[1] = True
            board[row][column] = board[row][column]
        elif currMarker == 2:
            startEnd[0] = True
            board[row][column] = currMarker
        elif currMarker == 3:
            startEnd[1] = True
            board[row][column] = currMarker
        else:
            if board[row][column] == 2:
                startEnd[0] = False 
            elif board[row][column] == 3:
                startEnd[1] = False
            board[row][column] = currMarker


def app(board):
    # initialize variables
    global fps
    running = True
    currMarker = 1
    startEnd = [False, False]
    updateNode = deque()
    message = None
    pygame.init()

    fps = 30
    CLOCK = pygame.time.Clock()
    
    # initialize font and screen
    FONT = pygame.freetype.Font(None, 20)
    screen = pygame.display.set_mode((1130,790), RESIZABLE)
    pygame.display.set_caption('Path Visualizer App')
    logo = pygame.image.load('logo.jpg')
    pygame.display.set_icon(logo)

    # main loop
    while running:
        screen.fill(lineColor)
        screenW, screenH = screen.get_size()
        blocksize = (screenW * 0.7) / width

        # defines main FPS & marks nodes in queue appropriately
        if len(updateNode) > 0:
            r, c, marker = updateNode.popleft()
            board[r][c] = marker
        else:
            fps = 30
        
        # event loop
        for event in pygame.event.get():
            # handles quit
            if event.type == pygame.QUIT:
                running = False
            # handles key strokes
            elif event.type == pygame.KEYDOWN:
                # marks cell as empty
                if event.key == K_0:
                    currMarker = 0
                # marks cell as obstacle
                elif event.key == K_1:
                    currMarker = 1
                # marks cell as start
                elif event.key == K_2:
                    currMarker = 2
                # marks cell as end
                elif event.key == K_3:
                    currMarker = 3
                # clears board
                elif event.key == K_c:
                    board = [[0] * width for x in range(height)]
                    startEnd = [False, False]
                    updateNode.clear()
                    message = None
                # reset board to DEFAULT_BOARD
                elif event.key == K_r:
                    board = [row[:] for row in DEFUALT_BOARD]
                    updateNode.clear()
                    message = None
                # runs BFS
                elif event.key == K_b:
                    start, end = find(board)
                    updateNode = deque()
                    fps = 120
                    parents = [[0]*width for i in range(height)]
                    if bfs(board, start, end, updateNode, parents):
                        message = "*BFS Found Path!*"
                        curr = end
                        pathList = []
                        while curr != start:
                            if curr != end:
                                pathList.append([curr[0], curr[1], 5])
                            curr = parents[curr[0]][curr[1]]

                        while len(pathList) > 0:
                            updateNode.append(pathList.pop())

                    else:
                        message = "*BFS Did Not Find Path!*"
                # runs DFS
                elif event.key == K_d:
                    start, end = find(board)
                    updateNode = deque()
                    fps = 60
                    if dfs(board, start, end, updateNode, 4):
                        message = "*DFS Found Path!*"
                        fps = 30
                        dfs(board, start, end, updateNode, 5)
                    else:
                        message = "*DFS Did Not Find Path!*"
            # handles mouse press
            if pygame.mouse.get_pressed()[0]:
                userClick(board, currMarker, blocksize, startEnd)
        
        # prints board
        for x in range(height):
            for y in range(width):
                if board[x][y] == 1: 
                    col = obstacleColor
                elif board[x][y] == 2:
                    col = startColor
                elif board[x][y] == 3:
                    col = endColor
                elif board[x][y] == 4:
                    col = visitedColor
                elif board[x][y] == 5:
                    col = pathColor
                else:
                    col = freeColor
                
                screen.fill(col, (x * blocksize, y * blocksize, blocksize, blocksize))
                rect = pygame.Rect(x * blocksize, y * blocksize, blocksize, blocksize)
                pygame.draw.rect(screen, lineColor, rect, 1)

        # scans for start and end tiles
        if any(2 in r for r in board):
            startEnd[0] = True
        if any(3 in r for r in board):
            startEnd[1] = True

        # prints appropriate alerts
        if not startEnd[0] and not startEnd[1]:
            FONT.render_to(screen, ((width * (width/9.89)) * blocksize, blocksize), "*Start and End Marker Not Placed*", (0,0,0))
        elif not startEnd[0]:
            FONT.render_to(screen, (width * (width / 9.5) * blocksize , blocksize), "*Start Marker Not Placed*", (0,0,0))
        elif not startEnd[1]:
            FONT.render_to(screen, (width * (width / 9.4) * blocksize, blocksize), "*End Marker Not Placed*", (0,0,0))
        elif message is not None and len(updateNode) == 0:
            FONT.render_to(screen, ((width + 1) * blocksize, blocksize), message, (0,0,0))
        else:
            screen.fill(lineColor, (width * blocksize, blocksize, width * blocksize, blocksize))

        # prints color legend
        FONT.render_to(screen, ((width + (width / 8)) * blocksize, (height / 3.25) * blocksize), "Colors Legend: ", (0,0,0))
        for i in range(6):
            screen.fill(colors[1][i], ((width + 0.5) * blocksize, (height - i - 1.5) * blocksize, blocksize, blocksize))
            rect = pygame.Rect((width + 0.5) * blocksize, (height - i - 1.5) * blocksize, blocksize, blocksize)
            pygame.draw.rect(screen, lineColor, rect, 1)
            if i is not 5 and i is not 4:
                FONT.render_to(screen, ((width + (width / 5.71)) * blocksize, (height - i - 1.1) * blocksize), colors[0][i] + "(" + str(i) + ")", (0,0,0))
            else:
                FONT.render_to(screen, ((width + (width / 5.71)) * blocksize, (height - i - 1.1) * blocksize), colors[0][i], (0,0,0))
        
        # prints instructions
        FONT.render_to(screen, ((width + (width / 25)) * blocksize, (height / 30) * blocksize), "Path Visualizer", obstacleColor, size=40)
        FONT.render_to(screen, ((width + (width / 30)) * blocksize, (height / 5) * blocksize), "Press associated key & click cells to place ", (0,0,0), size=15)
        FONT.render_to(screen, ((width + (width / 20)) * blocksize, (height / 4.5) * blocksize), "the appropriate marker on the board. ", (0,0,0), size=15)
        FONT.render_to(screen, ((width + (width / 9.7)) * blocksize, (height / 3.9) * blocksize), "Press C to clear, R to reset!", (0,0,0), size=15)
        FONT.render_to(screen, ((width + (width / 14)) * blocksize, (height / 3.6) * blocksize), "Press B to run BFS, D to run DFS!", (0,0,0), size=15)


        # updates display
        pygame.display.update()
        CLOCK.tick(fps)
    pygame.quit()
    quit()


# uncomment below line for app to start with empty with board
# board = [[0]*width for i in range(height)]
board = DEFUALT_BOARD

# runs app
app(board)
