import sys

import pygame
from pygame.locals import QUIT

SIZE = (640, 480)
pygame.init()

GRAVITY = 0.1
CLOCK = pygame.time.Clock()
BG = pygame.Color("#264653")
BALL_BG = pygame.Color("#e9c46a")
PALLET_BG = pygame.Color("#2a9d8f")


class Pallet(pygame.sprite.Sprite):
    def __init__(self, color) -> None:
        self.width: int = 70
        self.height: int = 12
        self.image = pygame.Surface((self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.centerx = int(SIZE[0]/2)
        self.rect.centery = int(SIZE[1]*4/5)
        self.image.fill(BG)
        self.max_speed = 10
        self.acceleration = 0.5
        self.friction = 0.95
        self.vel = 0

        pygame.draw.rect(self.image, color,
                         self.image.get_rect(), border_radius=4)

    def update(self, keys) -> None:
        if keys[pygame.K_LEFT]:
            self.vel -= self.acceleration
        elif keys[pygame.K_RIGHT]:
            self.vel += self.acceleration
        else:
            self.vel *= self.friction

        if self.vel > self.max_speed:
            self.vel = self.max_speed
        elif self.vel < -self.max_speed:
            self.vel = -self.max_speed
        self.rect.x += self.vel

        self.rect.move(self.rect.x, self.rect.y)


class Ball(pygame.sprite.Sprite):

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.radius = 12
        self.x = SIZE[0] // 2
        self.y = SIZE[1] // 2

        self.vx = 5
        self.vy = 5

    def draw(self, screen):
        pygame.draw.circle(screen, BALL_BG, (self.x, self.y), self.radius)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if (self.x + self.radius) > SIZE[0] or (self.x - self.radius) <= 0:
            self.vx = -self.vx
        if (self.y + self.radius) > SIZE[1] or (self.y - self.radius) <= 0:
            self.vy = -self.vy


# Init Display
DISPLAYSURF = pygame.display.set_mode(SIZE)

# Set Window name
pygame.display.set_caption('Bouncing ball')

myBall = Ball()
myPallet = Pallet(PALLET_BG)

# Event loop
while True:
    CLOCK.tick(60)  # 60 FPS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update Ball
    myBall.update()
    myPallet.update(pygame.key.get_pressed())

    DISPLAYSURF.fill(BG)
    myBall.draw(DISPLAYSURF)
    DISPLAYSURF.blit(myPallet.image, myPallet.rect)

    # Update Display
    pygame.display.update()
