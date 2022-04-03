from constant import *
from game import Poptile
from collections import deque
from typing import Tuple, List, Iterator
from itertools import product
from copy import deepcopy
from statistics import stdev
import random

DEBUG = False

def debug_print(msg):
    if DEBUG:
        print(msg)

class PoptileAI(Poptile):
    def __init__(self, w, h, c, nc):
        super().__init__(w, h, c, nc)
    
    def evaluate(self, board) -> int:
        score = 0
        for x in range(self.width):
            height = 0
            for y in reversed(range(self.height)):
                if board[y][x] != EMPTY:
                    height = y
                    break
            score += height ** 3
        return -score

    def getClickableList(self, board) -> Iterator[Tuple[int, int]]:
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        d = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for y in range(self.height):
            for x in range(self.width):
                if not visited[y][x] and board[y][x] != EMPTY:
                    q = deque()
                    q.append((y, x))
                    yield (y, x)
                    visited[y][x] = True
                    clicked_color = board[y][x]
                    
                    while q:
                        cy, cx = q.popleft()
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
                            visited[ny][nx] = True

    def getBestMove(self, depth) -> Tuple[int, int]:
        max_score = INF * 2
        best_move = (-1, -1)
        for y, x in self.getClickableList(self.board):
            debug_print(f'coord {y}, {x}')
            clicked_board = deepcopy(self.board)
            self.deleteTiles(clicked_board, y, x)
            self.dropTiles(clicked_board)
            if not self.checkNotGameOver(clicked_board):
                debug_print('gameover')
                cur_score = INF
            else:
                cur_score = self.dfs(clicked_board, depth)
            if cur_score > max_score:
                max_score = cur_score
                best_move = (y, x)
        
        return best_move
    
    def dfs(self, board, depth) -> float:
        if depth == 0:
            return self.evaluate(board)
        ret = 0
        cnt = 0
        for y, x in self.getClickableList(board):
            clicked_board = deepcopy(board)
            cnt += 1
            self.deleteTiles(clicked_board, y, x)
            self.dropTiles(clicked_board)
            if not self.checkNotGameOver(clicked_board):
                ret += INF
                continue
            ret += self.dfs(clicked_board, depth-1)
        return (ret / cnt)

    def simulate(self, width, depth):
        cnt = 0
        while self.isAlive():
            y, x = self.getBestMove(depth)
            self.click(y, x)
            cnt += 1
        return self.score, cnt

def main():
    f = open(LOGFILE, 'a')
    score_log = []
    for i in range(1, 101):
        game = PoptileAI(WIDTH, HEIGHT, COLOR, NUMCOLOR)
        score, cnt = game.simulate(DFSWIDTH, DFSDEPTH)
        score_log.append(score)
        msg = f'game {i:3d}: {score:7d} pts, {cnt:5d} clk\n'
        print(msg, end='')
        f.write(msg)

    score_log.sort()
    print(f'max score: {max(score_log)}')
    print(f'avg score: {sum(score_log) / 100}')
    print(f'std score: {stdev(score_log)}')

if __name__ == '__main__':
    main()
