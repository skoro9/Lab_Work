import os
import sys


# Add conda Library\bin to PATH if running on Windows
conda_base = r"C:\conda_envs\skoro9"  # Adjust if your conda root differs
os.environ["PATH"] = (
    os.path.join(conda_base, "Library", "bin") + ";" + os.environ["PATH"]
)
# Сверху находится блок, который я взял у Gemini, чтобы исправить ошибку Pycharm

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm, poisson
import math as m

def grouping_data(data_list, n): # Функция группировки данных
    result = []
    for k in range(0, len(data_list), n):
        chunk = data_list[k : k + n]
        result.append(sum(chunk))
    return result

# Data extraction
df = pd.read_excel("data.xlsx")
tau_values = [10, 20, 40, 80]
columns = df.columns.tolist()

for f, column in enumerate(columns):
    data = df[column].values.tolist()
    # <--- ИЗМЕНЕНИЕ: чуть увеличили ширину фигуры для лучшего размещения правой оси
    fig, axs = plt.subplots(2, 2, figsize=(14, 12))
    axs = axs.flatten()

    fig.suptitle(f"График для колонки: {column}", fontsize=16, fontweight="bold")
    for i, tau in enumerate(tau_values):
        grouped = grouping_data(data, tau)
        
        # <--- ИЗМЕНЕНИЕ: сохранили общее количество элементов (размерность) для расчета долей
        n_total = len(grouped) 

        count, bins, ignored = axs[i].hist(
            grouped, bins=15, density=False, alpha=0.8, color="skyblue", edgecolor="black", label="Данные"
        )

        # Параметры для распределений
        mu = np.mean(grouped)
        std = np.std(grouped)

        bin_width = bins[1] - bins[0]

        x_min, x_max = axs[i].get_xlim()
        x = np.linspace(x_min, x_max, 200)

        p_norm = norm.pdf(x, mu, std) * n_total * bin_width
        axs[i].plot(x, p_norm, "r-", linewidth=2, label="Гаусс")

        if mu > 0:
            x_poisson = np.arange(int(max(0, x_min)), int(x_max) + 1)
            p_poisson = poisson.pmf(x_poisson, mu) * n_total * bin_width
            axs[i].plot(x_poisson, p_poisson, "g--", marker="o", linewidth=2, label="Пуассон")

        axs[i].set_title(f"tau = {tau}")
        axs[i].set_ylabel("Абсолютная частота")  # <--- ИЗМЕНЕНИЕ: уточнили название левой оси
        axs[i].legend(loc="upper right")
        
        # <--- ИЗМЕНЕНИЕ: блок создания и настройки второй (правой) оси для относительной частоты
        ax_right = axs[i].twinx()
        y_min, y_max = axs[i].get_ylim()
        ax_right.set_ylim(y_min / n_total, y_max / n_total)
        ax_right.set_ylabel("Относительная частота", color="darkblue")
        ax_right.tick_params(axis='y', labelcolor="darkblue")
        ax_right.grid(False) # Отключаем сетку для правой оси, чтобы не дублировать линии

    if len(tau_values) < len(axs):
        axs[-1].axis("off")
        
    plt.tight_layout()
    filename = f"graph_{column}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')

# ==========================================
# ДОПОЛНИТЕЛЬНЫЙ БЛОК ОБРАБОТКИ ПО ПУНКТАМ 16-19
# ==========================================
experimental_data = df['Experimental'].values.tolist()
with open('calc_results.txt', 'w', encoding='utf-8') as f:
    for tau in tau_values:
        grouped = grouping_data(experimental_data, tau)

        arr = np.array(grouped)
        mean_val = np.mean(arr)
        std_dev = np.std(arr)
        pogr_mean = std_dev / m.sqrt(len(arr))
        j_low = mean_val / tau
        sigma_j = pogr_mean / tau
        epsilon = pogr_mean * 100 / mean_val
        epsilon_sqrt = 100/(m.sqrt(mean_val * len(arr)))
        # 1. Сначала инициализируем все счетчики нулями
        amount_1 = 0
        amount_2 = 0
        amount_3 = 0

        # 2. Считаем количество попаданий в каждый коридор (независимые if)
        for val in grouped:
            if abs(val - mean_val) <= std_dev:
                amount_1 += 1

            if abs(val - mean_val) <= 2 * std_dev:
                amount_2 += 1

            if abs(val - mean_val) <= 3 * std_dev:
                amount_3 += 1

        # 3. Находим общее число точек в эксперименте
        total_points = len(grouped)

        # 4. Вычисляем доли (значения от 0 до 1)
        share_1 = amount_1 / total_points
        share_2 = amount_2 / total_points
        share_3 = amount_3 / total_points

        data_lines = [f'Данные для группировки данных по {tau} штук\n','\n',f'Среднее число регистируемых частиц:{mean_val}\n', f'Среднеквадратичное отклонение:{std_dev}\n', f'Погрешность среднего значения:{pogr_mean}, sqrt {m.sqrt(pogr_mean)}\n',f'Средняя интенсивность регистрируемых частиц в секунду и её погрешность: {j_low} и {sigma_j}\n', f'Сравнение распределения Пуассона {m.sqrt(mean_val)} and {std_dev}\n', f"Доля для 1 сигмы: {amount_1}, {share_1:.4f}\n", f"Доля для 2 сигм:{amount_2},  {share_2:.4f} \n", f"Доля для 3 сигм:{amount_3},  {share_3:.4f} \n", f'{epsilon}, {epsilon_sqrt}','\n']
        f.writelines(data_lines)
print(grouping_data(experimental_data, 10))
print(grouping_data(experimental_data, 20))
print(grouping_data(experimental_data, 40))
print(grouping_data(experimental_data, 80))