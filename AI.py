# -*- coding: utf8 -*-
import random
import numpy as np

#  размерность нейросети
inp_lay_food = 1
inp_lay_bact_h = 1
inp_lay_bact_o = 1
hidden_lay = 2
out_lay = 1
# параметры изменение весов - обучения нейросети
mutation = 0.5
power_weight_mutation = 0.1
a = {}


# создание массива рандомных весов от -1 до 1
def init_weight():
    weight = []
    for _ in range((inp_lay_food + inp_lay_bact_h + inp_lay_bact_o) * hidden_lay + hidden_lay * out_lay):
        weight.append(random.random() * (1 + 1) - 1)
    return weight


# изменение рандомных весов лучшей бактерии поколения
def change_best_weight(weight):
    new_weight = weight
    ran = []
    for i in range(len(weight)):
        ran.append(i)
    for i in range(round(len(weight) * mutation)):
        new_weight[ran.pop(random.randint(0, len(ran) - 1))] += random.random() * (
                    power_weight_mutation + power_weight_mutation) - power_weight_mutation  # изменение веса на +- n
    return new_weight


# мутация
def mutation_two(first_weight, second_weight):
    second_weight = second_weight
    ran = []
    for i in range(len(first_weight)):
        ran.append(i)
    for i in range(round(len(second_weight) * 0.5)):
        a = ran.pop(random.randint(0, len(ran) - 1))
        second_weight[a] = first_weight[a]
    return second_weight


# функция активации - гиперболический тангенс
def tanh(x):
    return np.tanh(x)


# получение входных данных
def get_input(r_food, r_bact_h, r_bact_o):
    input_layers = []
    # заполнение входных данных нулями
    for _ in range(inp_lay_food + inp_lay_bact_h + inp_lay_bact_o):
        input_layers.append([0, 0])

    # заполнение входных данных значениями
    a = 0
    for i in range(inp_lay_food):
        try:
            input_layers[a] = r_food[i]
        except IndexError:
            break
        a += 1
    for i in range(inp_lay_bact_h):
        try:
            input_layers[a] = r_bact_h[i]
        except IndexError:
            break
        a += 1
    for i in range(inp_lay_bact_o):
        try:
            input_layers[a] = r_bact_o[i]
        except IndexError:
            break
        a += 1

    return input_layers

# вычисление выходных данных
def get_output(input_layers, weight):
    input_layers = input_layers
    weight = weight
    hidden_layers = []
    # заполнение скрытого слоя нулями
    for _ in range(hidden_lay):
        hidden_layers.append([0, 0])

    # перемножение входных данных и весов
    counter = 0
    for i in input_layers:
        for j in range(hidden_lay):
            hidden_layers[j][0] += i[0] * weight[counter]
            hidden_layers[j][1] += i[1] * weight[counter]
            counter += 1

    # активация преобразованных входных данных в скрытом слое
    for i in hidden_layers:
        i[0] = tanh(i[0])
        i[1] = tanh(i[1])

    # заполнение выходных данных нулями
    output_layers = []
    for _ in range(out_lay):
        output_layers.append([0, 0])

    # перемножение скрытого слоя и весов
    for i in hidden_layers:
        for j in range(out_lay):
            output_layers[j][0] += i[0] * weight[counter]
            output_layers[j][1] += i[1] * weight[counter]
            counter += 1

    # активация и домножение выходных данных
    for i in output_layers:
        i[0] = tanh(i[0]) * 2.5
        i[1] = tanh(i[1]) * 2.5

    return output_layers
