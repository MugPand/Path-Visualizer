from collections import deque

def dfs(board, start, end, updateNode, marker):
    boardCopy = [row[:] for row in board]
    stack = []
    stack.append(start)
    while len(stack) > 0:
        curr = stack.pop()
        if curr == end:
            return True
        else:
            if boardCopy[curr[0]][curr[1]] != 2:
                updateNode.append([curr[0], curr[1], marker])
                boardCopy[curr[0]][curr[1]] = marker
            # check north pos
            if curr[0] > 0 and boardCopy[curr[0]-1][curr[1]] != marker and boardCopy[curr[0]-1][curr[1]] != 1:
                stack.append((curr[0] - 1, curr[1]))
            # check east pos
            if curr[1] < len(board[0]) - 1 and boardCopy[curr[0]][curr[1]+1] != marker and boardCopy[curr[0]][curr[1]+1] != 1:
                stack.append((curr[0], curr[1] + 1))
            # check south pos
            if curr[0] < len(board) - 1 and boardCopy[curr[0]+1][curr[1]] != marker and boardCopy[curr[0]+1][curr[1]] != 1:
                stack.append((curr[0] + 1, curr[1]))
            # check west pos
            if curr[1] > 0 and boardCopy[curr[0]][curr[1]-1] != marker and boardCopy[curr[0]][curr[1]-1] != 1:
                stack.append((curr[0], curr[1] - 1))

    return False


def bfs(board, start, end, updateNode, parents):
    boardCopy = [row[:] for row in board]
    queue = deque()
    queue.append(start)
    while len(queue) > 0:
        curr = queue.popleft()
        if curr == end:
            return True
        else:
            if boardCopy[curr[0]][curr[1]] != 2:
                updateNode.append([curr[0], curr[1], 4])
                boardCopy[curr[0]][curr[1]] = 4
            # check north pos
            if curr[0] > 0 and boardCopy[curr[0]-1][curr[1]] != 4 and boardCopy[curr[0]-1][curr[1]] != 1:
                queue.append((curr[0] - 1, curr[1]))
                parents[curr[0]-1][curr[1]] = (curr[0], curr[1])
            # check east pos
            if curr[1] < len(board[0]) - 1 and boardCopy[curr[0]][curr[1]+1] != 4 and boardCopy[curr[0]][curr[1]+1] != 1:
                queue.append((curr[0], curr[1] + 1))
                parents[curr[0]][curr[1]+1] = (curr[0], curr[1])
            # check south pos
            if curr[0] < len(board) - 1 and boardCopy[curr[0]+1][curr[1]] != 4 and boardCopy[curr[0]+1][curr[1]] != 1:
                queue.append((curr[0] + 1, curr[1]))
                parents[curr[0]+1][curr[1]] = (curr[0], curr[1])
            # check west pos
            if curr[1] > 0 and boardCopy[curr[0]][curr[1]-1] != 4 and boardCopy[curr[0]][curr[1]-1] != 1:
                queue.append((curr[0], curr[1] - 1))
                parents[curr[0]][curr[1]-1] = (curr[0], curr[1])

    return False