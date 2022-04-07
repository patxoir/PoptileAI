
from ai import PoptileAI
from constant import *
from statistics import stdev, mean
import pygame
pygame.init()


FRAME_RATE = 10
TILESIZE = 30
SCREENRECT = pygame.Rect(100, 100, TILESIZE * 8, 100 + TILESIZE * 15)
bestdepth = pygame.display.mode_ok(SCREENRECT.size, 0, 32)

# FIXME: pygame.display.set_mode를 두번 불러야 윈도우가 나타남
pygame.display.set_mode(SCREENRECT.size, 0, bestdepth)
screen = pygame.display.set_mode(SCREENRECT.size, 0, bestdepth)
clock = pygame.time.Clock()

class PygamePoptileAI(PoptileAI):
    def __init__(self, w, h, c, nc):
        
        self.colors = [
            pygame.color.Color(0xff, 0xff, 0xff),
            pygame.color.Color(0x00, 0xaa, 0xff),
            pygame.color.Color(0xff, 0xaa, 0x00),
            pygame.color.Color(0xaa, 0xff, 0x00),
        ]

        super().__init__(w, h, c, nc)
    
    def draw(self):
        
        pygame.draw.rect(screen, pygame.color.Color((0, 0, 0)), [0, 0, TILESIZE * 8, 100])
        sf = pygame.font.SysFont(pygame.font.get_default_font(), 20, bold=True)
        textStr = "score: " + str(self.score)
        text = sf.render(textStr, True, (0, 0xaa, 0xff))
        screen.blit(text, (50,40))

        for row, line in enumerate(reversed(self.board)):
            for col, tile in enumerate(line):
                sy, sx = 100 + row * TILESIZE, col * TILESIZE
                pygame.draw.rect(screen, self.colors[tile], [sx, sy, TILESIZE, TILESIZE])
        pygame.display.flip()
        
        # frame interval
        clock.tick(FRAME_RATE)

def main():
    
    f = open(LOGFILE, 'a')
    score_log = []
    for i in range(1, 101):
        game = PygamePoptileAI(WIDTH, HEIGHT, COLOR, NUMCOLOR)
        score, cnt = game.simulate(DFSWIDTH, DFSDEPTH, game.draw)
        score_log.append(score)
        msg = f'game {i:3d}: {score:7d} pts, {cnt:5d} clk\n'
        print(msg, end='')
        f.write(msg)

    score_log.sort()
    print(f'max score: {max(score_log)}')
    print(f'avg score: {mean(score_log)}')
    print(f'std score: {stdev(score_log)}')

if __name__ == '__main__':
    main()
