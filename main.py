import pygame
from network import Network
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
        font = pygame.font.SysFont('comicsans', 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p, pts0, pts1):
    win.fill((112, 109, 109))
    
    if not(game.connected()):
        font = pygame.font.SysFont('comicsans', 50)
        text = font.render('Wainting another connection', 1, (0, 0, 0))
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont('comicsans', 45)
        fontpts = pygame.font.SysFont('comicsans', 25)
        text = font.render('Your move', 1, (0, 255, 255))
        textpts0 = fontpts.render('Player1: %s' % pts0, 1, (0, 0, 0))
        textpts1 = fontpts.render('Player2: %s' % pts1, 1, (0, 0, 0))
        win.blit(text, (80, 200))

        text = font.render('Opponent move', 1, (0, 255, 255))
        win.blit(text, (350, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render('Locked In', 1, (0, 0, 0))
            else:
                text1 = font.render('Wainting', 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render('Locked In', 1, (0, 0, 0))
            else:
                text2 = font.render('Wainting', 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
            win.blit(textpts1, (20, 30))
            win.blit(textpts0, (20, 60))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))
            win.blit(textpts0, (20, 30))
            win.blit(textpts1, (20, 60))
        
        for btn in btns:
            btn.draw(win)

    pygame.display.update()

btns = [Button('R', 50, 500, (255, 0, 0)), Button('S', 250, 500, (0, 255, 0)), Button('P', 450, 500, (0, 0, 255))]

def main():

    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print('Player: ', player)
    pts0 = 0
    pts1 = 0

    while run:
        clock.tick(60)
        try:
            game = n.send('get')
        except:
            run = False
            print('No game founded1')
            break

        if game.bothWent():
            redrawWindow(win, game, player, pts0, pts1)
            pygame.time.delay(500)
            try:
                game = n.send('reset')
            except:
                run = False
                print('No game founded2')
                break
            font = pygame.font.SysFont('comicsans', 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render('You won!', 1, (0, 255, 0))
            elif (game.winner() == 1 and player == 0) or (game.winner() == 0 and player == 1):
                text = font.render('You lost', 1, (255, 0, 0))
            else:
                text = font.render('Tied game', 1, (0, 0, 255))

            if game.winner() == 0:
                pts0 += 1
            elif game.winner() == 1:
                pts1 += 1

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
        
        redrawWindow(win, game, player, pts0, pts1)

def menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((112, 109, 109))
        font = pygame.font.SysFont('comicsans', 40)
        text = font.render('Click to queue with someone else', 1, (0, 0, 0))
        win.blit(text, (100, 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()


while True:
    menu()