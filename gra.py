import pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))
done = False
blue = True
x = 30
y = 30

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            blue = not blue
    y+=1.5
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]: y-=7

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x, y, 45, 45))

    pygame.display.flip()
    clock.tick(60)
