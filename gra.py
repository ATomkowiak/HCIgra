import pygame
import random

#stałe
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 400
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 128, 255)
FPS = 30

x = 30
y = 30

pygame.init()

score=0
size = [SCREEN_WIDTH,SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()


#współrzędne początkowe gracza
x_gracz = 30
y_gracz = 30

#współrzędne początkowe dolnej przeszkody
y_down = random.randint(30,300)
x_down = 290

#długość dolnej
h_down = 400 - y_down

#współrzędne początkowe górnej przeszkody
y_up = y_down+80
x_up = 290

#długosć górnej
h_up=400 - y_up

font = pygame.font.Font(None, 36)

game_over = False
done = False

#gra
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True

    #kończy
    if y_gracz > 375 or y_gracz < 0:
        game_over = True
    if x_up < 45 and x_down < 45:
        if y_gracz >= y_down-25 :
            game_over = True
    #sterowanie
    if not game_over:
        y_gracz += 2.5
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]: y_gracz-= 12

    #ruch przeszkód
    if not game_over:
        x_up-=2.5
        x_down-=2.5

    screen.fill(BLACK) #żeby się kwadrat nie zostawał

    pygame.draw.rect(screen, BLUE, [x_gracz, y_gracz, 25, 25])
    pygame.draw.rect(screen, GREEN, [x_down, y_down, 30, h_down])
    pygame.draw.rect(screen, GREEN, [x_up, y_up, 30, h_up])

    if x_up == 20  and x_down == 20:
        score+=1
        #współrzędne początkowe dolnej przeszkody
        y_down = random.randint(30,300)
        x_down = 290

        #długość dolnej
        h_down = 400 - y_down

        #współrzędne początkowe górnej przeszkody
        y_up = y_down+80
        x_up = 290

        #długosć górnej
        h_up=400 - y_up

        pygame.draw.rect(screen, GREEN, [x_down, y_down, 30, h_down])
        pygame.draw.rect(screen, GREEN, [x_up, y_up, 30, h_up])

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
