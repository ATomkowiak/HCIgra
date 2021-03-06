# -*- coding: utf-8 -*-


import multiprocessing as mp
import pygame as pg
import pandas as pd
import filterlib as flt
import blink as blk
import pygame
import random
from pyOpenBCI import OpenBCIGanglion


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()


####################################################
    SYMULACJA_SYGNALU = False
####################################################
    mac_adress = 'd2:b4:11:81:48:ad'
####################################################

    clock = pg.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":

    global mac_adress, SYMULACJA_SYGNALU

    #######################
    SYMULACJA_SYGNALU = True
    #######################
    if not SYMULACJA_SYGNALU:
        from pyOpenBCI import OpenBCIGanglion

    mac_adress = 'd2:b4:11:81:48:ad'


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    #stałe
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 400
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 128, 255)
    FPS = 30

    pygame.init()

    score = 0
    size = [SCREEN_WIDTH,SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    done = False

    clock = pygame.time.Clock()


    #współrzędne początkowe gracza
    x_gracz = 30
    y_gracz = 30

    #wielkość górnej przeszkody
    h_up = random.randint(30,300)
    x_up = 290

    #wielkość dolnej przeszkody
    h_down = h_up + 80
    x_down = 290

    font_name = pygame.font.match_font('arial')
    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)
    game_over = False
    done = False

    #gra
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done = True

        #sterowanie stare (tylko spacja)
        #if not game_over:
            #y_gracz += 2.5
            #pressed = pygame.key.get_pressed()
            #if pressed[pygame.K_SPACE]: y_gracz-= 12


        if not game_over:
            y_gracz += 1
            pressed = pygame.key.get_pressed()
            if blink.value == 1:
                y_gracz -= 25
                blink.value = 0
            if pressed[pygame.K_SPACE]:
                y_gracz -= 12

        #kończy
        if y_gracz > 375 or y_gracz < 0:
            game_over = True

        if x_down <= 45 and x_up <= 45:
            if y_gracz >= h_down and y_gracz <= h_up:
                game_over = True


        #ruch przeszkód
        if not game_over:
            x_up-=2.5
            x_down -=2.5

        screen.fill(BLACK) #żeby się kwadrat nie zostawał

        pygame.draw.rect(screen, BLUE, [x_gracz, y_gracz, 25, 25])
        pygame.draw.rect(screen, GREEN, [x_up , 0, 30, h_up])
        pygame.draw.rect(screen, GREEN, [x_down , h_up + 80 , 30, 400])

        if x_up == 20 and x_down == 20:
            score+=1

            #współrzędne górnej
            x_up = 290

            #wielkość górnej przeszkody
            h_up = random.randint(30,300)


            #współrzędne początkowe dolnej przeszkody
            y_down = h_up + 80
            x_down = 290

            #wielkość dolnej przeszkody
            h_down = h_up + 80

            pygame.draw.rect(screen, GREEN, [x_up , 0, 30, h_up])
            pygame.draw.rect(screen, GREEN, [x_down , h_down , 30, 400])
            screen.fill(BLACK)
            draw_text(screen, str(score), 18, 150, 10)
            #wyświetlanie punktów

            if x_down <= 45 and x_up <= 45:
                if y_gracz >= h_down and y_gracz <= h_up:
                    game_over = True

        if game_over:
            # jeśli game_over jest prawidziwe skończ grę
            draw_text(screen, "Game over", 18, 150, 200)
            draw_text(screen, str(score), 18, 150, 10)
            game_over = True


        clock.tick(FPS)

        pygame.display.flip()

    pygame.quit()


# Zakończenie podprocesów
    proc_blink_det.join()
