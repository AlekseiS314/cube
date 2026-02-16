import pygame
from random import randint
from datetime import datetime, timedelta
import numpy as np
import math
pygame.init()

def smaller(small: int, ogr: int):
    global x
    global y
    global player_x
    global player_y
    mouse1 = pygame.mouse.get_pressed()
    if mouse1[0]:
        if player_x >= ogr:
            player_x -= small
            player_y -= small
            x += small / 2
            y += small / 2


def move(x_velocity, y_velocity):
    global x
    global y
    key_1 = pygame.key.get_pressed()
    if key_1[pygame.K_LEFT]:
        if x + WIDTH / 2 > 0:
            x -= x_velocity
    if key_1[pygame.K_RIGHT]:
        if x + WIDTH / 2 + player_x < WIDTH:
            x += x_velocity
    if key_1[pygame.K_UP]:
        if y + HEIGHT / 2 > 0:
            y -= y_velocity
    if key_1[pygame.K_DOWN]:
        if y + HEIGHT / 2 + player_y < HEIGHT:
            y += y_velocity


def create_apple():
    global start_time
    if current_time - start_time > time_create_apple:
        apple_list.append((randint(1, WIDTH), randint(1, HEIGHT)))
        start_time = datetime.now()


def eat_draw_apple():
    global player_y
    global player_x
    global TIMER_0
    global COUNT_GRIND_APPLE
    global ADD_SECOND_FOR_APPLE
    l = 4
    for apple_coordinate in apple_list:
        if x0 - l <= apple_coordinate[0] <= x1 + l:
            if y0 - l <= apple_coordinate[1] <= y1 + l:
                apple_list.remove(apple_coordinate)
                TIMER_0 += ADD_SECOND_FOR_APPLE
                COUNT_GRIND_APPLE += 1
        pygame.draw.circle(sc, (255, 0, 0), apple_coordinate, 7, 5)


def create_spike():
    global start_time_spike
    if current_time_spike - start_time_spike >= time_create_spike:
        pol = randint(1, 4)
        if pol == 1:
            y_cor = 0
            x_cor = randint(1, WIDTH)
        elif pol == 2:
            y_cor = HEIGHT
            x_cor = randint(1, WIDTH)
        elif pol == 3:
            y_cor = randint(1, HEIGHT)
            x_cor = 0
        else:
            y_cor = randint(1, HEIGHT)
            x_cor = WIDTH
        coordinate = [x_cor, y_cor]

        spike_list.append([coordinate,pol])
        start_time_spike = datetime.now()


def damage_move_spike():
    def damage_spike():
        global player_x
        global player_y
        if x0 <= spike[0][0] <= x1:
            if y0 <= spike[0][1] <= y1:
                spike_list.remove(spike)
                end_game()

    def move_spike(i):
        match spike_list[i][1]:
            case 1:
                spike_list[i][0][1] += 5
            case 2:
                spike_list[i][0][1] -= 5
            case 3:
                spike_list[i][0][0] += 5
            case 4:
                spike_list[i][0][0] -= 5
        pygame.draw.circle(sc, (0, 0, 255), spike_list[i][0], 4, 5)

    def delete_spike(s):
        x_s = s[0][0]
        y_s = s[0][1]
        if x_s < 0 or x_s > WIDTH:
            spike_list.remove(s)
        elif y_s < 0 or y_s > HEIGHT:
            spike_list.remove(s)

    global x_real
    global y_real
    for spike_index in range(len(spike_list)):
        spike = spike_list[spike_index]
        move_spike(spike_index)
    for spike in spike_list:
        delete_spike(spike)
        damage_spike()

def create_line():
    global start_time_line
    global x_real
    global y_real
    global line_list
    if current_time_line - start_time_line > time_create_line:
        mn = randint(1,4)
        ran = 50
        if mn == 1:
            s1 = randint(1,ran)
            s2 = randint(1,ran)
        elif mn == 2:
            s1 = -randint(1, ran)
            s2 = randint(1, ran)
        elif mn == 3:
            s1 = randint(1, ran)
            s2 = -randint(1, ran)
        elif mn == 4:
            s1 = -randint(1, ran)
            s2 = -randint(1, ran)
        x_line = x_real + s1
        y_line = y_real + s2
        alpha = randint(0, 179)


        line_list.append([x_line,y_line,alpha,datetime.now()])
        start_time_line = datetime.now()

def draw_line():
    def damage_line(l : list):
        def check_hitbox(xf,yf,u):
            kp = np.tan(u * np.pi / 180)
            bp = yf - kp * xf
            if 45 < u < 90:
                return ((y1 <= kp * x1 + bp) and (y0 >= kp * x0 + bp))
            else:
                return ((y1 >= kp * x1 + bp) and (y0 <= kp * x0 + bp))
        global x0
        global y0
        global x1
        global y1
        global player_y
        global player_x
        if check_hitbox(l[0],l[1],l[2]):
            end_game()

    def calc_coordinate(x_dot : int,y_dot : int,ugol : int) -> tuple[tuple[int]]:
        if ugol == 90:
            rezx1 = x_dot
            rezx2 = x_dot
        else:
            k_r = np.tan(ugol * np.pi / 180)
            b_r = y_dot - k_r * x_dot
            rezx1 = -(b_r/k_r)
            rezx2 = (HEIGHT - b_r) / k_r
        rezy1 = 0
        rezy2 = HEIGHT
        return ((rezx1,rezy1), (rezx2,rezy2))

    global line_list
    for line in line_list:
        c = datetime.now()
        xa = line[0]
        ya = line[1]
        a = line[2]
        dot1, dot2 = calc_coordinate(xa, ya, a)
        delta = c - line[3]
        if delta <= time_bigger_line:
            pygame.draw.line(sc,(0,162,232),dot1,dot2,math.ceil(6 * (delta.microseconds // 1000)/1000))
        elif time_bigger_line < delta < time_live_line:
            pygame.draw.line(sc, (0, 100, 232), dot1, dot2, 6)
            damage_line(line)

def create_sieve():
    global time_create_sieve
    global line_list
    global start_time_sieve
    if current_time_sieve - start_time_sieve > time_create_sieve:
        for i in range(-WIDTH * 2,WIDTH * 2,200):
            line_list.append([i, 0, 45,  datetime.now()])
            line_list.append([i, 0, -45, datetime.now()])
            print(i)
        start_time_sieve = datetime.now()



def player_color_f():
    global player_x
    if player_x > 255:
        return 255
    else:
        return player_x

def okno():
    global COUNT_GRIND_APPLE
    global TIMER_0
    global text_sc
    global text_dest
    global font_win
    qp = str(60 - TIMER_0 + COUNT_GRIND_APPLE * ADD_SECOND_FOR_APPLE)
    result = qp[:qp.index('.') + 3]
    text_sc = font_win.render(f"{result}", False, (0, 255, 0), None)
    text_dest = text_sc.get_rect(midtop=(WIDTH / 2, HEIGHT / 2))
    sc.blit(text_sc, text_dest)

def end_game():
    global flag
    flag = False

WIDTH = 1920
HEIGHT = 1080
FPS = 60
COUNT_APPLE = 0
APPLE_TIMER = 0
player_x = 20
player_y = 20
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
color = (255, 255, 255)
flag = True
x = 0
y = 0
ADD_SECOND_FOR_APPLE = 5
start_time = datetime.now()
start_time_spike = datetime.now()
start_time_line = datetime.now()
start_time_sieve = datetime.now()

apple_list = []
time_create_apple = timedelta(seconds=3)

spike_list = []
time_create_spike = timedelta(seconds=0.2)

line_list = []
const_time_create_line = 1
time_create_line = timedelta(seconds=const_time_create_line)

time_bigger_line = timedelta(seconds=1)

const_time_live_line = 1.5
time_live_line = timedelta(seconds=const_time_live_line)

const_time_create_sieve = 4
time_create_sieve = timedelta(seconds=const_time_create_sieve)

font = pygame.font.Font(None,30)
font_win = pygame.font.Font(None,300)
TIMER_0 = 60
COUNT_GRIND_APPLE = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()
    if flag:
        current_time = datetime.now()
        current_time_spike = datetime.now()
        current_time_line = datetime.now()
        current_time_sieve = datetime.now()

        smaller(4,20)

        move(5,5)

        sc.fill((255, 255, 255))
        pygame.draw.rect(sc,(20,player_color_f(),20),(WIDTH/2 + x,HEIGHT/2 + y,player_x,player_y))
        x_real = WIDTH/2 + x + player_x/2
        y_real = HEIGHT/2 + y + player_y/2
        x0 = WIDTH / 2 + x
        y0 = HEIGHT / 2 + y # левый верхинй
        x1 = x0 + player_x
        y1 = y0 + player_y  # правый нижний

        create_apple()
        eat_draw_apple()

        create_spike()
        damage_move_spike()

        create_line()
        create_sieve()
        draw_line()

        TIMER_0 -= 1/60
        qwer = str(TIMER_0)[:str(TIMER_0).index('.') + 3]
        text_sc = font.render(qwer,False,(0,0,0),None)
        text_dest = text_sc.get_rect(midtop=(WIDTH/2,0))
        sc.blit(text_sc,text_dest)
    else:
       okno()

    pygame.display.update()
    clock.tick(FPS)