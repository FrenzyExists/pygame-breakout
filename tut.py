"""
A simple game I made with pygame while following
a tutorial on udemy, with some changes here and there
"""

import sys
from time import sleep
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
FONT_FG = pygame.Color("#e76f51")

SCORE = 0
LIVES = 3
DRAW: bool = True


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
        self.rect.centerx = int(SIZE[0] / 2)
        self.rect.centery = int(SIZE[1] * 13 / 14)
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

        # Ensure the Pallet stays within the window boundaries
        if self.rect.left < 0:
            self.rect.left = 0  # fixes bug where pallet gets stuck
            self.vel = -self.vel * self.friction
        elif self.rect.right > SIZE[0]:
            self.rect.right = SIZE[0]  # fixes bug where pallet gets stuck
            self.vel = -self.vel * self.friction

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

        pygame.draw.rect(self.image, (self.color), self.rect)


class Wall(pygame.sprite.Group):
    def __init__(
        self,
        container_width: int,
        container_height: int,
        amount_of_bricks: int,
        gap: int = 10,
        top_gap: int = None,
    ):
        pygame.sprite.Group.__init__(self)
        self.gap = gap
        rows = ceil(sqrt(amount_of_bricks + self.gap))
        cols = ceil(amount_of_bricks / rows)
        brick_width: int = ceil(
            (container_width + self.gap) / cols - self.gap - self.gap // 2
        )
        brick_height = ceil((container_height + self.gap) / rows - self.gap)
        pos_x, pos_y = self.gap, self.gap + top_gap

        for i in range(rows):
            for j in range(cols):
                brick = Brick(
                    BRICK_BG,
                    pos_x + brick_width // 2,
                    pos_y + brick_height // 2,
                    brick_width,
                    brick_height,
                )
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

    def __init__(
        self, color: pygame.Color, x=SIZE[0] // 2, y=SIZE[1] // 2, radius=12, speed=5
    ) -> None:
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
        self.rect = pygame.draw.circle(
            screen, self.color, (self.x, self.y), self.radius
        )

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


class Director:
    def __init__(self) -> None:
        pass

    def action(self, initial_scene, fps=60):
        pass


class Scene:
    def __init__(self) -> None:
        self.next_scene = False
        self.playing = True
        pass

    def event(self, e):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

    def change_scene(self, new_scene):
        pass


def display_big_text(surface: pygame.Surface, text: str, quit=True, can_sleep=True, sleep_time=3) -> None:
    big_text = pygame.font.SysFont(None, 72)
    txt: pygame.Surface = big_text.render(text, True, BALL_BG)
    txt_rect = txt.get_rect()
    txt_rect.center = [SIZE[0] // 2, SIZE[1] // 2]
    surface.blit(txt, txt_rect)
    pygame.display.update()
    if can_sleep:
        sleep(sleep_time)
    if quit:

        sys.exit(0)


# Init Display
DISPLAY_SURF = pygame.display.set_mode(SIZE)

# Set Window name
pygame.display.set_caption("Bouncing ball")

myBall = Ball(BALL_BG)
myPallet = Pallet(PALLET_BG)
# 10, SIZE[0], 300
myWall = Wall(
    container_height=SIZE[1] // 3,
    amount_of_bricks=20,
    container_width=SIZE[0],
    gap=6,
    top_gap=30,
)

font = pygame.font.SysFont(None, 32)

# Adjust event repetition
pygame.key.set_repeat(30)

start_game = False

# Event loop
while True:
    CLOCK.tick(60)  # 60 FPS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if DRAW and pygame.key.get_pressed()[pygame.K_SPACE]:
        print("BOI")
        DRAW = False

    DISPLAY_SURF.fill(BG)
    if not start_game:
        for i in ["READY?", "3", "2", "1", "GO!!! GO!!! GO!!!"]:
            display_big_text(DISPLAY_SURF, i, False, sleep_time=0.6)
            DISPLAY_SURF.fill(BG)
        start_game = True

    # Update Ball and Pallet

    myBall.draw(DISPLAY_SURF)
    myWall.draw(DISPLAY_SURF)

    if not DRAW:
        myBall.update()
    else:
        myBall.x, myBall.y = myPallet.rect.centerx, myPallet.rect.top-myPallet.rect.height

    myPallet.update(pygame.key.get_pressed())

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

    DISPLAY_SURF.blit(font.render(f"SCORE: {SCORE}", 1, FONT_FG), (20, 10))
    DISPLAY_SURF.blit(font.render(
        f"LIVES: {LIVES}", 1, FONT_FG), (SIZE[0] - 100, 10))
    DISPLAY_SURF.blit(myPallet.image, myPallet.rect)

    if len(myWall.sprites()) == 0:
        display_big_text(DISPLAY_SURF, f"YOU WON!!!  {SCORE}")

    if LIVES == 0:
        display_big_text(DISPLAY_SURF, "AWW... YOU LOST")

    # Update Display
    pygame.display.update()

    # Update lives here so when we loose we see the 0
    if myBall.rect.bottom >= SIZE[1]:
        LIVES -= 1
        DRAW = True
