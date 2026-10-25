import math as mt
from scipy import integrate as it
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


# Задаем полу-оси эллипсоида по направлениям X, Y и Z
rx, ry, rz = 1, 1, 1

# Создаем сетку сферических/полярных углов
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

# Вычисляем декартовы координаты точек эллипсоида
x = rx * np.outer(np.cos(u), np.sin(v))
y = ry * np.outer(np.sin(u), np.sin(v))
z = rz * np.outer(np.ones_like(u), np.cos(v))

# Создаем 3D-график
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

# Рисуем поверхность эллипсоида
ax.plot_surface(x, y, z, color="b", alpha=0.6, edgecolor="k", lw=0.3)

# Выравниваем масштабы осей, чтобы эллипсоид не выглядел сплюснутым
max_radius = max(rx, ry, rz)
ax.set_xlim([-max_radius, max_radius])
ax.set_ylim([-max_radius, max_radius])
ax.set_zlim([-max_radius, max_radius])

ax.set_xlabel("Ось X")
ax.set_ylabel("Ось Y")
ax.set_zlabel("Ось З")
ax.set_title("График эллипсоида в Python")

plt.show()