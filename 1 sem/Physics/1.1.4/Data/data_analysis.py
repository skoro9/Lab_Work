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

def grouping_data(data_list, n): # Функция группировки данных
    result = []
    for k in range(0, len(data_list), n):
        chunk = data_list[k : k + n]
        result.append(sum(chunk))
    return result

# Data extraction
df = pd.read_excel("data.xlsx")
tau_values = [1, 10, 20, 40, 80]
columns = df.columns.tolist()

for f, column in enumerate(columns):
    data = df[column].values.tolist()
    # <--- ИЗМЕНЕНИЕ: чуть увеличили ширину фигуры для лучшего размещения правой оси
    fig, axs = plt.subplots(3, 2, figsize=(14, 12))
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
            p_poisson = poisson.pmf(x_poisson, mu) * n_total
            axs[i].plot(x_poisson, p_poisson, "g--", marker="o", linewidth=2, label="Пуассон")

        axs[i].set_title(f"tau = {tau}")
        axs[i].set_ylabel("Абсолютная частота")  # <--- ИЗМЕНЕНИЕ: уточнили название левой оси
        axs[i].legend(loc="upper right")
        
        # <--- ИЗМЕНЕНИЕ: блок создания и настройки второй (правой) оси для относительной частоты
        ax_right = axs[i].twinx()
        ymin, ymax = axs[i].get_ylim()
        ax_right.set_ylim(ymin / n_total, ymax / n_total)
        ax_right.set_ylabel("Относительная частота", color="darkblue")
        ax_right.tick_params(axis='y', labelcolor="darkblue")
        ax_right.grid(False) # Отключаем сетку для правой оси, чтобы не дублировать линии

    if len(tau_values) < len(axs):
        axs[-1].axis("off")
        
    plt.tight_layout()
    filename = f"graph_{column}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')