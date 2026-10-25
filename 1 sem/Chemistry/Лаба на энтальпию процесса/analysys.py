import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Загрузка данных из файла Excel по полному пути
file_path = (
    r'C:\Users\User\Lab_work\Lab_Work\1 sem\Chemistry\Лаба на энтальпию процесса\лента_A.xlsx'
)
df = pd.read_excel(file_path, skiprows=1)
df.columns = ['t', 'L', 'step']

# Извлекаем время (t) и сигнал/значение (L)
time = df['t'].values
signal = df['L'].values

# 2. Калибровка: перевод сигнала L в температуру T (°C)
L_min, L_max = np.min(signal), np.max(signal)
T_min, T_max = 16.0, 28.0  # Диапазон температур по шкале на фотографии
temperature = T_min + (signal - L_min) / (L_max - L_min) * (T_max - T_min)

# 3. Настройка холста и сетки под миллиметровку
fig, ax = plt.subplots(figsize=(12, 8), dpi=300)

ax.set_xlim(0, 300)  # Время от 0 до 300 сек
ax.set_ylim(15, 28)  # Температура от 15°C до 28°C

# 4. Настройка сетки (миллиметровка)
ax.set_xticks(
    np.arange(0, 301, 20)
)  # Каждые 20 сек (по 0.5 см на 10 сек -> 1 см = 20 сек)
ax.set_yticks(np.arange(15, 29, 1))  # Каждые 1°C (1 см = 1°C)

ax.set_xticks(np.arange(0, 301, 2), minor=True)  # Мелкие деления по X (каждые 2 сек)
ax.set_yticks(
    np.arange(15, 29, 0.1), minor=True
)  # Мелкие деления по Y (каждые 0.1°C)

ax.grid(which='major', color='red', linestyle='-', linewidth=0.8, alpha=0.6)
ax.grid(which='minor', color='red', linestyle=':', linewidth=0.4, alpha=0.3)

# 5. Построение графика
ax.plot(
    time[::5],
    temperature[::5],
    color='blue',
    marker='o',
    markersize=2,
    linestyle='-',
    linewidth=1.5,
    label='Экспериментальные точки $T(\\tau)$',
)

ax.set_xlabel('Время $\\tau$, сек', fontsize=12, fontweight='bold')
ax.set_ylabel('Температура $t, ^\\circ\\text{C}$', fontsize=12, fontweight='bold')
ax.set_title(
    'Зависимость температуры раствора от времени $T(\\tau)$',
    fontsize=14,
    fontweight='bold',
    pad=15,
)

ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

ax.legend(loc='upper right', frameon=True)
plt.tight_layout()

# Сохранение графика в файл
folder_path = (
    r'C:\Users\User\Lab_work\Lab_Work\1 sem\Chemistry\Лаба на энтальпию процесса'
)
plt.savefig(os.path.join(folder_path, 'millimeter_graph.png'), dpi=300)

# ==========================================================
# 6. ГЕНЕРАЦИЯ И СОХРАНЕНИЕ ТАБЛИЦЫ С ШАГОМ 2 СЕКУНДЫ
# ==========================================================
times_target = np.arange(0, 301, 2)
table_rows = []

for t_val in times_target:
  idx = np.abs(time - t_val).argmin()
  table_rows.append(
      {
          'Время τ (сек)': round(time[idx], 1),
          'Температура T (°C)': round(temperature[idx], 2),
      }
  )

table_df = pd.DataFrame(table_rows)

# Вывод первых строк в консоль
print('\n' + '=' * 45)
print('    ТАБЛИЦА ЗНАЧЕНИЙ (ШАГ 2 СЕКУНДЫ)')
print('=' * 45)
print(table_df.head(15).to_string(index=False))
print(f'... (всего точек: {len(table_df)})')
print('=' * 45)

# Сохранение в текстовый файл
file_out_path = os.path.join(folder_path, 'table_points_2s.txt')
table_df.to_csv(file_out_path, sep='\t', index=False, encoding='utf-8')
print(f'Файл с таблицей успешно сохранен: {file_out_path}')

# Показать графическое окно
plt.show()