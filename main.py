import pygame
from network import Network
from player import Player
pygame.font.init()

WIDTH = 700
HEIGHT = 700

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Client')

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('arial', 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):

    win.fill((112, 109, 109))
    
    if not (game.connected()):
        font = pygame.font.SysFont('arial', 80)
        text = font.render('Wainting another connection', 1, (80, 110, 122), True)
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))


btns = [Button('R', 50, 500, (255, 0, 0)), Button('S', 250, 500, (0, 255, 0)), Button('P', 450, 500, (0, 0, 255))]

def main():

    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP)
    print('Player: ', player)

    while run:
        clock.tick(60)
        try:
            game = n.send('get')
        except:
            run = False
            print('No game founded1')
            break

        if game.bothWent():
            redrawWindow()
            pygame.time.delay(500)
            try:
                game = n.send('reset')
            except:
                run = False
                print('No game founded2')
                break
            font = pygame.font.SysFont('arial', 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render('You won!', 1, (0, 255, 0))
            elif (game.winner() == 1 and player == 0) or (game.winner() == 0 and player == 1):
                text = font.render('You lost', 1, (255, 0, 0))
            else:
                text = font.render('Tied game', 1, (0, 0, 255))

            win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        
        redrawWindow(win, game, player)



main()