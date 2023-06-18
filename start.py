# -*- coding: utf8 -*-
import pygame as pg
import random
import AI as ai
import date_writer as dw
from options import *
import bact_herbivorous as bh
import bact_omnivorous as bo
import foods as fd

pg.init()

sc = pg.display.set_mode((width, height))  # pg.RESIZABLE - расширение окна
pg.display.set_caption(title)  # название в окне
# pg.display.set_icon(pg.image.load(r"C:\Users\Admin\Desktop\.idea\free-icon-bacteria-1097327.png"))  # иконка

clock = pg.time.Clock()  # контроль частоты кадров

foods = pg.sprite.Group()  # все объекты - еды
bacts = pg.sprite.Group()  # все объекты - бактерии
bacts_herb = pg.sprite.Group() # все объекты - травоядные
bacts_omn = pg.sprite.Group() # все объекты - всеядные
pg.time.set_timer(pg.USEREVENT, spawn_food)  # общий таймер

# данные(перенести в бд)
generation = 1
data_bact_h = {}
data_bact_o = {}
mid_timer_list_bact_h = []
qua_bact_h_list = []
qua_bact_h_counter = 0
mid_timer_list_bact_o = []
qua_bact_o_list = []
qua_bact_o_counter = 0
generation_list = []
gen_herb = 0
gen_omn = 0


# старт программы
def start():
    global time_start_herb
    global time_start_omn
    global gen_start_herb
    global gen_start_omn
    # получение данных с предыдущих запусков программы, только для одной
    data_start_herb = dw.start_json("data_gen_herb.json")
    gen_start_herb = data_start_herb[0]
    time_start_herb = data_start_herb[1]
    weight_start_herb = data_start_herb[2]
    data_start_omn = dw.start_json("data_gen_omn.json")
    gen_start_omn = data_start_omn[0]
    time_start_omn = data_start_omn[1]
    weight_start_omn = data_start_omn[2]

    # спавн первоначальной еды
    for i in range(qu_food):
        foods.add(fd.Food())

    # выбор обученного запуска или с нуля
    print(f"Выберите запуск обучения с нуля(0) или с лучшей обученной травоядной бактерии(1)")
    print(f"Обученная бактерия:\n\tПоколение: {gen_start_herb}\n\tВремя жизни: {time_start_herb}")
    choose = int(input())
    if choose:
        # создание объектов
        inf = bh.create_bact(weight_start_herb, 10)
        bacts.add(inf)
        bacts_herb.add(inf)
    else:
        # создание объектов
        inf = (bh.create_bact(ai.init_weight(), 10))
        bacts.add(inf)
        bacts_herb.add(inf)
        gen_start_herb = 0

    # выбор обученного запуска или с нуля
    print(f"Выберите запуск обучения с нуля(0) или с лучшей обученной всеядной бактерии(1)")
    print("сейчас измененение по идее")
    print(f"Обученная бактерия:\n\tПоколение: {gen_start_omn}\n\tВремя жизни: {time_start_omn}")
    choose = int(input())
    if choose:
        inf = bo.create_bact(weight_start_omn, 10)
        bacts.add(inf)
        bacts_omn.add(inf)

    else:
        inf = bo.create_bact(ai.init_weight(), 10)
        bacts.add(inf)
        bacts_omn.add(inf)
        gen_start_omn = 0







# получение данных поколения, для одного
def data_gen(data, mid_list, bact):
    coin_data = [i for i in data.keys()]
    timer_data = [i[0] for i in data.values()]
    weight_data = [i[1] for i in data.values()]
    try:
        max_coin = max(coin_data)  # лучший coin поколения
    except ValueError:
        max_coin = 0

    max_timer = max(timer_data)  # максимальное время поколения
    mid_time = sum(timer_data) / len(timer_data)  # среднее время поколения
    mid_list.append(mid_time)
    # передача веса, поколения и coin в словарь для json файла
    return {max_coin: [generation + bact, max_timer, data[max_coin][1]]}




start()
qua_bact_h_counter += len(bacts_herb)
qua_bact_o_counter += len(bacts_omn)


# основной цикл игры
run = True
while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False

            # запись в json
            dw.change_json(time_start_herb, js_bact_h, "data_gen_herb.json")  # для травоядных
            dw.change_json(time_start_omn, js_bact_o, "data_gen_omn.json")

            #графики программы
            dw.create_graf(generation_list, mid_timer_list_bact_h, mid_timer_list_bact_o, "Поколение", "Среднее время")  # отрисовка графика среднего времени
            dw.create_graf(generation_list, qua_bact_h_list, qua_bact_o_list, "Поколение", "Количество бактерий") # отрисовка графика количества бактерий
            exit()
        # спавн n еды раз в n секунд
        if event.type == pg.USEREVENT and len(foods) <= qu_food:
            for _ in range((qu_food - len(foods)) // 2):
                foods.add(fd.Food())

    # обновление поколений
    if len(bacts) == 0:
        js_bact_h = data_gen(data_bact_h, mid_timer_list_bact_h, gen_start_herb)
        js_bact_o = data_gen(data_bact_o, mid_timer_list_bact_o, gen_start_omn)

        qua_bact_h_list.append(qua_bact_h_counter)
        qua_bact_o_list.append(qua_bact_o_counter)
        generation_list.append(generation)
        qua_bact_h = 0
        qua_bact_o = 0


        # создание объектов
        inf = bh.create_gen_bact(10, data_bact_h,1)
        bacts.add(inf)
        bacts_herb.add(inf)
        qua_bact_h += len(inf)
        inf = bo.create_gen_bact(10, data_bact_o, 1)
        bacts.add(inf)
        bacts_omn.add(inf)
        qua_bact_o += len(inf)
        data_bact_h = {}  # сброс для отслеживания поколения
        data_bact_o = {}

        generation += 1
        print(f"Поколение {generation}")

    # отрисовка и рендеринг
    for bact in bacts:
        if bact in bacts_herb:
            inf = bact.seed()
            if inf != None:
                bacts.add(inf)
                bacts_herb.add(inf)
                qua_bact_h_counter += len(inf)
            inf = bact.death()
            if inf != None:
                data_bact_h.setdefault(inf[0], inf[1])
        if bact in bacts_omn:
            inf = bact.seed()
            if inf != None:
                bacts.add(inf)
                bacts_omn.add(inf)
                qua_bact_o_counter += len(inf)
            inf = bact.death()
            if inf != None:
                data_bact_o.setdefault(inf[0], inf[1])



    foods.draw(sc)
    bacts.draw(sc)
    bacts.update(bacts_herb, bacts_omn, foods)
    pg.display.update()
    sc.fill('white')
