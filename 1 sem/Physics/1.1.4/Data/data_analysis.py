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
    fig, axs = plt.subplots(3, 2, figsize=(12, 12))
    axs = axs.flatten()

    fig.suptitle(f"График для колонки: {column}", fontsize=16, fontweight="bold")
    for i, tau in enumerate(tau_values):
        grouped = grouping_data(data, tau)

        # ИЗМЕНЕНО: density=True нормирует гистограмму, чтобы высота соответствовала кривым вероятностей
        count, bins, ignored = axs[i].hist(
            grouped, bins=15, density=True, alpha=1, color="skyblue", edgecolor="black", label="Данные"
        )

        # Параметры для распределений
        mu = np.mean(grouped)
        std = np.std(grouped)

        x_min, x_max = axs[i].get_xlim()
        x = np.linspace(x_min, x_max, 200)

        # 1. ИЗМЕНЕНО: Распределение Гаусса (нормальное)
        p_norm = norm.pdf(x, mu, std)
        axs[i].plot(x, p_norm, "r-", linewidth=2, label="Гаусс")

        # 2. ИЗМЕНЕНО: Распределение Пуассона (параметр лямбда = mu)
        if mu > 0:
            x_poisson = np.arange(int(max(0, x_min)), int(x_max) + 1)
            p_poisson = poisson.pmf(x_poisson, mu)
            axs[i].plot(x_poisson, p_poisson, "g--", marker="o", linewidth=2, label="Пуассон")

        axs[i].set_title(f"tau = {tau}")
        axs[i].legend(loc="upper right")

        # ИЗМЕНЕНО: скрываем 6-й пустой график в сетке 3х2, так как tau всего 5
    if len(tau_values) < len(axs):
        axs[-1].axis("off")

    plt.tight_layout()
    plt.show()