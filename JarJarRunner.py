#!/usr/bin/env python3
import pygame
import os
import random

# Settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
GRAVITY = 1
JUMP_VELOCITY = -20
DINO_SPRITE = pygame.image.load(os.path.join("assets", "player.png"))
OBSTACLE_SPRITE = pygame.image.load(os.path.join("assets", "obstacle2.png"))

# Game States
HOME_SCREEN = 0
RUNNING_SCREEN = 1
GAMEOVER_SCREEN = 2

# text
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(os.path.join("fonts", "starjedi.ttf"), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = DINO_SPRITE
        self.rect = self.image.get_rect()
        self.rect.center = (100, WINDOW_HEIGHT - 17)
        self.velocity = 0
        self.jumping = False

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.velocity = 0
            self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity += JUMP_VELOCITY
            self.jumping = True

# obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = OBSTACLE_SPRITE
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH, WINDOW_HEIGHT - 18)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Game init
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("JAM#2 - Jar Jar Binks Runner")
clock = pygame.time.Clock()

# Create sprites
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
jarjar = Player()
all_sprites.add(jarjar)

# Game variables
game_state = HOME_SCREEN
score = 0

# Music
homemusic = pygame.mixer.Sound(os.path.join("music", "home.ogg"))
runningmusic = pygame.mixer.Sound(os.path.join("music", "running.ogg"))
gameovermusic = pygame.mixer.Sound(os.path.join("music", "gameover.ogg"))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == HOME_SCREEN:
                    game_state = RUNNING_SCREEN
                elif game_state == RUNNING_SCREEN:
                    jarjar.jump()
                elif game_state == GAMEOVER_SCREEN:
                    game_state = HOME_SCREEN
                    score = 0
                    obstacles.empty()

    if game_state == RUNNING_SCREEN:
        homemusic.stop()
        runningmusic.play(-1)
        if random.randrange(200) < 2:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

        hits = pygame.sprite.spritecollide(jarjar, obstacles, False)
        if hits:
            game_state = GAMEOVER_SCREEN

        all_sprites.update()

        score += 1

        FPS += 0.01

    # Display
    screen.fill(BACKGROUND_COLOR)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WINDOW_WIDTH // 2, 50, (255, 255, 255))

    if game_state == HOME_SCREEN:
        all_sprites.add(jarjar)
        draw_text(screen, "Jar Jar Binks Runner", 64, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4, (255, 255, 255))
        draw_text(screen, "Press SPACE to o.p.e.n the game", 22, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, (255, 255, 255))
        gameovermusic.stop()
        homemusic.play(-1)
    elif game_state == GAMEOVER_SCREEN:
        FPS = 60
        runningmusic.stop()
        gameovermusic.play(-1)
        all_sprites.empty()
        draw_text(screen, "Game over", 64, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4, (255, 0, 0))
        draw_text(screen, f"Score: {score}", 30, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, (255, 255, 255))
        draw_text(screen, "Press SPACE to r.e.s.t.a.r.t the game", 22, WINDOW_WIDTH // 2, WINDOW_HEIGHT * 3 // 4, (255, 255, 255))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
