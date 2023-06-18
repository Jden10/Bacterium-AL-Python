# -*- coding: utf8 -*-
import json
import os.path
import AI as ai
import matplotlib.pyplot as plt
from options import *

# изначальный запуск программы
def start_json(name_file):
    data = []
    if os.path.isfile(name_file):
        with open(name_file) as file:
            text = json.load(file)
            text = [i for i in text.values()]
            gen = text[0][0]
            time = round(text[0][1], 3)
            weight = text[0][2]
    else:
        with open(name_file, "w") as file:
            a = {0: [0, 0, []]}
            json.dump(a, file, indent=4, ensure_ascii=False)
            gen = 0
            time = 0
            weight = ai.init_weight()
    data.append(gen)
    data.append(time)
    data.append(weight)
    return data

# изменение начальных данных
def change_json(old_time, data, name_file):
    t = [i for i in data.values()]
    max_time = t[0][1]
    if old_time <= max_time:
        with open(name_file, "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def create_graf(x, first, second, strx, strfirst):
    plt.plot(x, first, color = color_bact_herb)
    plt.plot(x, second, color = color_bact_omn)
    plt.title('обучение бактерии')
    plt.xlabel(strx, fontsize=12)
    plt.ylabel(strfirst, fontsize=12)
    plt.show()