import pygame
import random

#stałe
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 128, 255)
FPS = 35

pygame.init()

size = [300,400]
screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()

#współrzędne początkowe gracza
x_gracz = 30
y_gracz = 30

#współrzędne początkowe dolnej przeszkody
y_down = random.randint(0,120)
x_down = 390

#współrzędne początkowe górnej przeszkody
y_up = random.randint(180,300)
x_up = 390

font = pygame.font.Font(None, 36)

game_over = False

#gra
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True

    #kończy
    if y_gracz > 350 or y_gracz < 0:
        game_over = True
    #sterowanie
    if not game_over:
        y_gracz += 2.5
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]: y_gracz-= 12

    screen.fill(BLACK) #żeby się kwadrat nie zostawał

    pygame.draw.rect(screen, BLUE, [x_gracz, y_gracz, 50, 50])

    if game_over:
        # jeśli game_over jest prawidziwe skończ grę
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])
        game_over=False


    clock.tick(FPS)

    pygame.display.flip()

pygame.quit()
