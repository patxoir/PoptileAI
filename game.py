from XORShift import XORShift
from constant import *
from collections import deque
from typing import Tuple, List
import os, sys

class Poptile:
    def __init__(self, w, h, c, nc):
        self.width = w
        self.height = h
        self.color = c.copy()
        self.numcolor = nc
        self.board = [[EMPTY for _ in range(w)] for _ in range(h)]
        self.random = XORShift()
        self.board = self.insertNewLine(self.board, self.newLine())
        self.alive = True
        self.score = 0

    def printBoard(self):
        os.system('clear')
        print('-' * self.width)
        for line in reversed(self.board):
            for v in line:
                print(self.color[v], end='')
            print()
        print('-' * self.width)
        print(f'Score: {self.score}\n')

    def insertNewLine(self, board, line) -> List[List[int]]:
        newBoard = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
        for y in reversed(range(1, self.height)):
            newBoard[y] = board[y-1].copy()
        newBoard[0] = line.copy()
        return newBoard

    def newLine(self) -> List[int]:
        return list((self.random.next() % self.numcolor)+1 for _ in range(self.width))

    def deleteTiles(self, board, y, x) -> int:
        q = deque()
        q.append((y, x))
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        visited[y][x] = True
        clicked_color = board[y][x]
        board[y][x] = EMPTY
        count = 0

        d = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        while q:
            cy, cx = q.popleft()
            count += 1
            for dy, dx in d:
                ny = cy + dy
                nx = cx + dx
                if not (0 <= ny < self.height and 0 <= nx < self.width):
                    continue
                if board[ny][nx] != clicked_color:
                    continue
                if visited[ny][nx]:
                    continue
                q.append((ny, nx))
                board[ny][nx] = EMPTY
                visited[ny][nx] = True

        return count

    def updateScore(self, count):
        self.score += count ** 2

    def dropTiles(self, board):
        for x in range(self.width):
            bottom = 0
            for y in range(self.height):
                if board[y][x] != EMPTY and y != bottom:
                    board[bottom][x] = board[y][x]
                    board[y][x] = EMPTY
                    bottom += 1
                elif board[y][x] != EMPTY:
                    bottom += 1

    def checkNotGameOver(self, board) -> bool:
        for x in range(self.width):
            if board[self.height-1][x] != EMPTY:
                return False
        return True

    def getScore(self) -> int:
        return self.score

    def isAlive(self) -> bool:
        return self.alive

    def isClickable(self, board, y, x) -> bool:
        if not (0 <= y < self.height and 0 <= x < self.width):
            return False
        if board[y][x] == EMPTY:
            return False
        return True

    def click(self, y, x):
        if not self.isClickable(self.board, y, x):
            return
        pop_count = self.deleteTiles(self.board, y, x)
        self.updateScore(pop_count)
        self.dropTiles(self.board)
        self.alive = self.checkNotGameOver(self.board)
        if self.isAlive():
            self.board = self.insertNewLine(self.board, self.newLine())

    def prompt(self) -> Tuple[int, int]:
        while True:
            try:
                y, x = map(int, input('Enter coord (y, x): ').split())
                if self.isClickable(self.board, y, x):
                    return (y, x)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass

def main():
    game = Poptile(WIDTH, HEIGHT, COLOR, NUMCOLOR)
    while game.isAlive():
        game.printBoard()
        y, x = game.prompt()
        game.click(y, x)
    
    game.printBoard()
    print('Game over!')

if __name__ == '__main__':
    main()
