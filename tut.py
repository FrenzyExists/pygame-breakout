"""
A simple game I made with pygame while following
a tutorial on udemy, with some changes here and there
"""

import sys

import pygame
from pygame.locals import QUIT
from math import sqrt, ceil

SIZE = (640, 480)
pygame.init()

GRAVITY = 0.1
CLOCK = pygame.time.Clock()
BG = pygame.Color("#264653")
BALL_BG = pygame.Color("#e9c46a")
PALLET_BG = pygame.Color("#2a9d8f")
BRICK_BG = pygame.Color("#f4a261")

SCORE = 0


class Pallet(pygame.sprite.Sprite):
    """
    # Pallet
    Creates a pallet object
    Takes a color as param. Pretty self-explanatory
    """

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
        self.friction = 0.85
        self.vel = 0

        pygame.draw.rect(self.image, color,
                         self.image.get_rect(), border_radius=0)

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


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x: int, y: int, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        pygame.draw.rect(self.image, (self.color),
                         self.rect)


class Wall(pygame.sprite.Group):
    def __init__(self, container_width: int, container_height: int,
                 amount_of_bricks: int, gap: int = 10, top_gap: int = None):
        pygame.sprite.Group.__init__(self)
        self.gap = gap
        rows = ceil(sqrt(amount_of_bricks+self.gap))
        cols = ceil(amount_of_bricks / rows)
        brick_width: int = ceil(
            (container_width + self.gap) / cols - self.gap-self.gap//2)
        brick_height = ceil((container_height + self.gap) / rows - self.gap)
        pos_x, pos_y = self.gap, self.gap+top_gap

        for i in range(rows):
            for j in range(cols):
                brick = Brick(BRICK_BG, pos_x + brick_width // 2,
                              pos_y + brick_height // 2, brick_width,
                              brick_height)
                self.add(brick)
                pos_x += brick_width + self.gap
            pos_y += brick_height + self.gap
            pos_x = self.gap


def collide_ball_pallet(ball: pygame.Surface, pallet: pygame.Rect):
    # Check if the ball and the pallet are overlapping
    if not pygame.sprite.collide_rect(ball, pallet):
        return False
    if ball.vy > 0 and ball.rect.left <= (pallet.rect.right):
        return True
    return False


class Ball(pygame.sprite.Sprite):
    """
    # Ball
    A ball that bounces everywhere that's it

    Params:
        color: pygame.Color object, specifies color of the ball

    Attributes:
        x: int, x-coordinate of the center of the ball
        y: int, y-coordinate of the center of the ball
        vx: horizontal velocity
        vy: vertical velocity
    """

    def __init__(self, color: pygame.Color, x=SIZE[0] // 2,
                 y=SIZE[1] // 2, radius=12, speed=5) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.rect = None
        self.vx = speed
        self.vy = speed

    def draw(self, screen):
        """
        Draws the ball on the given screen.

        Args:
            screen: A pygame.Surface object that represents the display
            surface.
        """
        # self.rect = pygame.draw.rect(screen, self.color, (self.x, self.y, self.x, self.y))
        # self.rect = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        self.rect = pygame.draw.circle(
            screen, self.color, (self.x, self.y), self.radius)

    def update(self):
        """
        Updates the position and velocity of the ball according to the
        boundaries of the screen.

        - If the ball hits the left or right edge of the screen, it reverses
        its horizontal velocity.
        - If the ball hits the top or bottom edge of the screen, it reverses
        its vertical velocity.
        """
        self.x += self.vx
        self.y += self.vy
        if (self.x + self.radius) > SIZE[0] or (self.x - self.radius) <= 0:
            self.vx = -self.vx
        if (self.y + self.radius) > SIZE[1] or (self.y - self.radius) <= 0:
            self.vy = -self.vy


# Init Display
DISPLAY_SURF = pygame.display.set_mode(SIZE)

# Set Window name
pygame.display.set_caption('Bouncing ball')

myBall = Ball(BALL_BG)
myPallet = Pallet(PALLET_BG)
# 10, SIZE[0], 300
myWall = Wall(container_height=SIZE[1]//3,
              amount_of_bricks=20, container_width=SIZE[0], gap=6, top_gap=30)

font = pygame.font.SysFont(None, 32)

# Adjust event repetition
pygame.key.set_repeat(30)

# Event loop
while True:
    CLOCK.tick(60)  # 60 FPS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update Ball and Pallet
    myBall.update()
    myPallet.update(pygame.key.get_pressed())

    DISPLAY_SURF.fill(BG)

    myBall.draw(DISPLAY_SURF)
    myWall.draw(DISPLAY_SURF)

    if collide_ball_pallet(myBall, myPallet):
        myBall.vy = -myBall.vy

    collision_list = pygame.sprite.spritecollide(myBall, myWall, True)
    if collision_list:
        cx = myBall.rect.centerx
        if cx < collision_list[0].rect.left or cx > collision_list[0].rect.right:
            myBall.vx = -myBall.vx
        else:
            myBall.vy = -myBall.vy
        SCORE += 10

    if len(myWall.sprites()) == 0:
        print("YOU WON!")
        exit(0)
    DISPLAY_SURF.blit(font.render(f"SCORE: {SCORE}", 0, PALLET_BG), (20, 10))
    DISPLAY_SURF.blit(myPallet.image, myPallet.rect)

    # Update Display
    pygame.display.update()
