import os
import sys


# Add conda Library\bin to PATH if running on Windows
conda_base = r"C:\conda_envs\skoro9"  # Adjust if your conda root differs
os.environ["PATH"] = (
    os.path.join(conda_base, "Library", "bin") + ";" + os.environ["PATH"]
)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as m
m_small = 0.7641
m_big = 0.7645
radius = 0.04395
k = 9.8 * 0.1154 * 0.0305 / ( 4 * (np.pi)**2 * 2.179)

df = pd.read_excel('Data.xlsx')
pm_length = 0.001
pm_radius = 0.0001
sigma_k = k * m.sqrt((pm_length/0.1154)**2+(pm_length/0.0305)**2+(pm_length/2.179)**2)
names = df['Body'].values.tolist()

weights = df['Weight'].values.tolist()

amounts = df['Amount'].values.tolist()

times = df['Time'].values.tolist()
i_exp = []
i_exp_dict = {}
i_empty_theory = 0.5 * weights[0] * (0.1154**2)
i_empty = k * weights[0] * ((times[0] / amounts[0]) ** 2)
for name, weight, amount, time in zip(names, weights, amounts, times):
    if isinstance(weight, str):
        weight = float(weight.replace(',', '.'))

    i = k * weight * ((time/amount)**2)
    if name == 'Empty':
        i_exp.append(0.0)  # ИСПРАВЛЕНО: чистый момент пустого тела равен нулю
        i_exp_dict[name] = 0.0
    else:
        i_body = i - i_empty  # ИСПРАВЛЕНО: вычитаем i_empty вместо сложения
        i_exp.append(i_body)  # ИСПРАВЛЕНО: добавляем разность, а не сумму (было i + i_empty)
        i_exp_dict[name] = i_body  # ИСПР

i_circle = []
# ИСПРАВЛЕНО: диапазон изменен с 5 на 6.
# В вашей Excel-таблице строка 'Circle_whole' идет 7-й по счету, что в Python соответствует индексу 6.
for f in range(5, len(i_exp)):
    i_circle.append(i_exp[f])

r_list = [0, 0.023, 0.044, 0.06, 0.068]
i_theory = []
for r in r_list:
    i_theory.append((m_big + m_small)*(0.5 * radius**2 + r**2))
print(round(sigma_k, 6))
# # =====================================================================
# # НАСТРОЙКА ДАННЫХ ДЛЯ ОСИ X (КВАДРАТ РАССТОЯНИЯ)
# # =====================================================================
# # Переводим исхо6дный r_list в квадрат расстояния r^2
# r_squared = [r**2 for r in r_list]
#
# # =====================================================================
# # РАСЧЕТ ПРЯМОЙ МНК ЧЕРЕЗ ТЕОРЕТИЧЕСКИЕ ТОЧКИ
# # =====================================================================
# # np.polyfit(X, Y, 1) находит коэффициенты (наклон и сдвиг) для прямой Y = a*X + b
# slope, intercept = np.polyfit(r_squared, i_theory, 1)
#
# # Генерируем массив точек для гладкой линии МНК
# x_mnk = np.linspace(min(r_squared), max(r_squared), 100)
# y_mnk = slope * x_mnk + intercept
#
# # =====================================================================
# # ПОСТРОЕНИЕ ГРАФИКОВ
# # =====================================================================
# plt.figure(figsize=(10, 6))
#
# # 1. Теоретические точки и линия МНК через них
# plt.scatter(r_squared, i_theory, color='red', marker='o', s=60, label='Теория (Точки)')
# plt.plot(x_mnk, y_mnk, color='red', linestyle='--', linewidth=1.5, label=f'Теория МНК: I = {slope:.4f}·r² + {intercept:.5f}')
#
# # 2. Экспериментальные точки
# plt.scatter(r_squared, i_circle, color='blue', marker='x', s=80, linewidths=2, label='Эксперимент (Точки)')
#
# # =====================================================================
# # ОФОРМЛЕНИЕ ГРАФИКА
# # =====================================================================
# plt.xlabel('Квадрат расстояния до центра $r^2$, м²', fontsize=11)
# plt.ylabel('Момент инерции $I$, кг·м²', fontsize=11)
# plt.title('Зависимость момента инерции от квадрата расстояния $I(r^2)$', fontsize=12, fontweight='bold')
#
# plt.grid(True, linestyle=':', alpha=0.6) # Делаем сетку аккуратной
# plt.legend(fontsize=10, loc='upper left')  # Выводим легенду со всеми цветами
#
# # Отображаем график на экране
# plt.show()
