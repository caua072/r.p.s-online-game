import pygame

class Player():
    def __init__(self, x, y, WIDTH, HEIGHT, color):

        self.x = x
        self.y = y
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.color = color
        self.rect = (x, y, WIDTH, HEIGHT)
        self.vel = 3

    def draw(self, win):

        pygame.draw.rect(win, self.color, self.rect)

    def move(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.vel

        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_w]:
            self.y -= self.vel

        if keys[pygame.K_s]:
            self.y += self.vel

        self.update()

    def update(self):

        self.rect = (self.x, self.y, self.WIDTH, self.HEIGHT)