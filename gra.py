import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 128, 255)

pygame.init()

size = [300,400]
screen = pygame.display.set_mode(size)

done = False
#blue = True

clock = pygame.time.Clock()

x = 30
y = 30

font = pygame.font.Font(None, 36)

game_over = False

while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True


    if y > 350 or y < 0:
        game_over = True

    if not game_over:
        y += 2.5
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]: y-= 12

    screen.fill(BLACK)

    pygame.draw.rect(screen, BLUE, [x, y, 50, 50])

    if game_over:
        # If game over is true, draw game over
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])

    clock.tick(60)

    pygame.display.flip()

pygame.quit()
