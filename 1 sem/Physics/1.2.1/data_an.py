import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl as op
import math as mt


# Блок инерциального маятника
def speed_calculation_1(m, x): # Вычисление скорости пули, выпущенной в инерциальный маятник, и погрешности вычисления
    u = round((2.925 / m) * mt.sqrt(9.8 / 2.082) * x, 3)
    error = round(100 * mt.sqrt((0.005/2.925)**2 + (0.00001/m)**2 + (0.002/2.082*2)**2 + (0.0002/x)**2 ), 3)
    return u, error

# Массы пуль, выпущенных в первый маятник
weights_1 = [0.000506, 0.000511, 0.000505, 0.000517, 0.000505]
# Амплитуда колебаний инерциального маятника
amp_list_1 = [0.012, 0.012, 0.0115, 0.012, 0.0114]


numbers_1 = range(1, 6)

bullets_1 = list(zip(numbers_1, amp_list_1, weights_1))
speed_1 = []
for i in range(5):
    speed_1.append((numbers_1[i], speed_calculation_1(bullets_1[i][2], bullets_1[i][1])))

# Блок крутильного маятника

def speed_calculation_2 (x, m): # Вычисление скорости пули, выпущенной в крутильный маятник, и погрешности вычисления
    T_1 = 6.56
    T_2 = 4.85
    amplifier = (4 * (np.pi) * 1.4687 * 0.1156 * T_1) / ((T_1 ** 2 - T_2 ** 2) * 0.19 * 1.35 * 2)
    u = round((x / m) * amplifier, 3)
    error = round(100 * mt.sqrt((0.002 / 1.4687)**2 + (2 * 0.001 / 0.34 )**2 + (0.001 / x)**2 + (0.00001/m)**2 + (0.001 / 0.19)**2 + (0.001 / 1.35 )**2 + ((T_1 ** 2 + T_2 ** 2) * 0.1 / (T_1 * (T_1 ** 2 - T_2 ** 2)))**2 + (2 * T_2 * 0.1 / (T_1 ** 2 - T_2 ** 2))**2), 3)
    return u, error

weights_2 = [0.000508, 0.000512, 0.000502, 0.000509, 0.000511]
amp_list_2 = [0.039, 0.04, 0.041, 0.04, 0.04]
numbers_2 = range(6, 11)

bullets_2 = list(zip(numbers_2, amp_list_2, weights_2))

speed_2 = []
for i in range(5):
    speed_2.append((numbers_2[i], speed_calculation_2(bullets_2[i][1], bullets_2[i][2])))

# print(speed_1)
print(speed_2)
# print(bullets_1)
print(bullets_2)