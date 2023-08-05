#!python3
# -*- coding: utf-8 -*-

from random import choice
from sys import exit
import pygame

FOUR_NEIGH = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}
DIRE = {(0, -1): "left", (0, 1): "right", (-1, 0): "up", (1, 0): "down"}
ROWS = 50


def mht_dis(d1, d2):
    return abs(d1[0]-d2[0])+abs(d1[1]-d2[1])


def min_dis(body, d):
    mind = 200
    mini = 0
    for i in body:
        d1 = mht_dis(i, d)
        if d1 < mind:
            mind = d1
            mini = i
    return mini


def max_dis(body, d):
    maxd = -1
    maxi = 0
    for i in body:
        d1 = mht_dis(body[i], d)
        if d1 > maxd:
            maxd = d1
            maxi = i
    return maxi


def max_min(dic, food, last, dire, opt):
    dis = 200 if opt == "min" else -1
    key = 0
    for item in dic:
        d = mht_dis(item, food)
        if (opt == "min" and d < dis) or (opt == "max" and d > dis):
            dis = d
            key = item
            # print(food, item)
        elif d == dis and dire == (item[0]-last[0], item[1]-last[1]):
            key = item
    return key


def draw_snake(screen, color, x, y):
    rect = pygame.Rect(y*10, x*10, 10, 10)
    screen.fill(color, rect)
    pygame.display.update(rect)


def test(screen):
    head = (10, 10)
    n = head
    food = (35, 15)
    draw_snake(screen, 0x00ff00, *food)
    walk = {}
    for i in range(1, 25):
        draw_snake(screen, 0xff00ff, 18, i)
        draw_snake(screen, 0xff00ff, i, 18)
        walk[(18, i)] = (-1, -1)
        walk[(i, 18)] = (1, 1)

    dic = {head: (-1, -1)}
    timer = pygame.time.Clock()

    while dic != {}:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        timer.tick(500)

        n = min_dis(dic, food)

        walk[n] = dic.pop(n)
        draw_snake(screen, 0xff0000, n[0], n[1])
        if n == food:
            break
        for d in list(FOUR_NEIGH.values()):
            to = (n[0]+d[0], n[1]+d[1])
            if to[0] < 0 or to[1] < 0 or to[0] >= 50 or to[1] >= 50 or to in walk or to in dic:
                continue
            dic[to] = n
    # if n == food:
    while n != (-1, -1):
        draw_snake(screen, 0x00ff00, *n)
        n = walk[n]
        timer.tick(300)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def connect(screen, opt="min"):
    head = head = (10, 10)
    food = (35, 15)
    now = head
    last = now
    walk = {}

    for i in range(1, 25):
        draw_snake(screen, 0xff00ff, 18, i)
        draw_snake(screen, 0xff00ff, i, 18)
        walk[(18, i)] = (-1, -1)
        walk[(i, 18)] = (1, 1)

    wait = {head: (-1, -1)}
    d = choice(list(DIRE.values()))
    timer = pygame.time.Clock()
    while wait != {}:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        last = now
        now = max_min(wait, food, now, d, opt)
        d = (now[0]-last[0], now[1]-last[1])
        # print("now: ", last, now, d)
        if d not in DIRE:
            d = choice(list(DIRE.values()))
        walk[now] = wait.pop(now)
        draw_snake(screen, 0xff0000, *now)
        if now == food:
            break
        for d in list(FOUR_NEIGH.values()):
            to = (now[0]+d[0], now[1]+d[1])
            if to[0] < 0 or to[1] < 0 or to[0] >= ROWS or to[1] >= ROWS or to in walk or to in wait:
                continue
            wait[to] = now
        timer.tick(80)

    dire = []
    last = now
    result = now == food
    draw_snake(screen, 0x00ff00, *now)
    while now != head:
        now = walk[now]
        # draw_snake(screen, 0x00ff00, *now)
        d = (last[0]-now[0], last[1]-now[1])
        dire.append(DIRE[d])
        last = now
    dire.reverse()

    return result, dire


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500), 0, 32)
    pygame.display.set_caption('test')
    # test(screen)
    connect(screen, "max")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    # print(mht_dis((10,8), (10, 8)))