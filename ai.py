from constant import *
from game import Poptile
from collections import deque
from typing import Tuple, Iterator
from copy import deepcopy
from statistics import stdev, mean
from timeit import default_timer as timer

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
            score += height ** height
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
            if self.isGameOver(clicked_board):
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
            if self.isGameOver(clicked_board):
                ret += INF
                continue
            ret += self.dfs(clicked_board, depth-1)
        return (ret / cnt)

    def simulate(self, width, depth, callback=None):
        cnt = 0
        while self.isAlive():
            y, x = self.getBestMove(depth)
            self.click(y, x)
            cnt += 1
            if callback:
                callback()
        return self.score, cnt

class Statistics:
    def __init__(self):
        self.n = 0
        self.score_list = []
        self.click_count_list = []
        self.runtime_list = []
        self.cps_list = []

    def append(self, score, click, runtime):
        self.n += 1
        self.score_list.append(score)
        self.click_count_list.append(click)
        self.runtime_list.append(runtime)
        self.cps_list.append(click / runtime)
    
    def getLastGameInfo(self) -> str:
        msg = (f'Game {self.n:3d}:'
               f' {self.score_list[-1]:7d} pts |'
               f' {self.click_count_list[-1]:6d} clk |'
               f' {self.runtime_list[-1]:8.2f} s |'
               f' {self.cps_list[-1]:8.2f} cps')
        return msg

    def printStat(self):
        print(f'Total games played: {self.n}')
        print(f'Elapsed time: {sum(self.runtime_list):.2f} s\n')

        print(f'Max score: {max(self.score_list)}')
        print(f'Avg score: {mean(self.score_list):.2f}')
        print(f'Std score: {stdev(self.score_list):.2f}\n')

        print(f'Avg time per game: {mean(self.runtime_list):.2f} s')
        print(f'Avg cps: {mean(self.cps_list):.2f}')
        print(f'Std cps: {stdev(self.cps_list):.2f}') 

def main():
    f = open(LOGFILE, 'a')
    stat = Statistics()
    num_games = 1000
    print(f'Start simulation for {num_games} games...')
    for i in range(1, num_games + 1):
        start = timer()
        # Measure time
        game = PoptileAI(WIDTH, HEIGHT, COLOR, NUMCOLOR)
        score, cnt = game.simulate(DFSWIDTH, DFSDEPTH)
        # ... until here
        end = timer()
        runtime = end - start
        stat.append(score, cnt, runtime)
        msg = stat.getLastGameInfo()
        print(msg)
        f.write(msg + '\n')

    stat.printStat()

if __name__ == '__main__':
    main()
