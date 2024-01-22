import sys

import pygame
from pygame.locals import QUIT

SIZE = (640, 480)
pygame.init()

GRAVITY = 0.1
CLOCK = pygame.time.Clock()


class Ball(pygame.sprite.Sprite):

    def __init__(self) -> None:
        # load image
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bolita.png")

        # get rect
        self.rect = self.image.get_rect()

        # Set initial position
        self.rect.centerx = int(SIZE[0] / 2)
        self.rect.centery = int(SIZE[1] / 2)

        # Set vx and vy
        self.vx = 7
        self.vy = 7

    def update(self):
        self.rect.move_ip((self.vx, self.vy))
        if self.rect.bottom > SIZE[1] or self.rect.top <= 0:
            self.vy = -self.vy
        if self.rect.right > SIZE[0] or self.rect.left <= 0:
            self.vx = -self.vx


# Init Display
DISPLAYSURF = pygame.display.set_mode(SIZE)

# Set Window name
pygame.display.set_caption('Bouncing ball')

myBall = Ball()

# Event loop
while True:
    CLOCK.tick(60)  # 60 FPS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update Ball
    myBall.update()

    DISPLAYSURF.fill((0, 0, 64))

    # Draw Ball
    DISPLAYSURF.blit(myBall.image, myBall.rect)

    # Update Display
    pygame.display.update()
