import numpy as np
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go
from scipy.stats import poisson, norm

# =====================================================================
# 1. ЗАГРУЗКА ДАННЫХ
# =====================================================================
file_path = 'data.xlsx'

try:
    df = pd.read_excel(file_path)
    columns_to_process = df.columns.tolist()
    print(f"Успешно загружено столбцов: {len(columns_to_process)}")
except Exception as e:
    print(f"Ошибка при чтении файла {file_path}: {e}")
    exit()

# Исправленная строка: интервалы группировки согласно методичке
tau_values = [1, 10, 20, 80]
print("\nГенерация интерактивных графиков в HTML файлы (без matplotlib)...")

# =====================================================================
# 2. ПОСТРОЕНИЕ ГИСТОГРАММ ДЛЯ ВСЕХ 10 СТОЛБЦОВ
# =====================================================================
for col in columns_to_process:
    data_raw = df[col].dropna().to_numpy().astype(int)
    t_total = len(data_raw)

    # Создаем сетку из 4 подграфиков (2 ряда по 2 колонки)
    fig = sp.make_subplots(
        rows=2, cols=2,
        subplot_titles=[f'Интервал tau = {t} с' for t in tau_values],
        horizontal_spacing=0.08, vertical_spacing=0.12
    )

    for idx, tau in enumerate(tau_values):
        row = (idx // 2) + 1
        col_idx = (idx % 2) + 1

        N_blocks = t_total // tau
        if tau == 1:
            g_data = data_raw
        else:
            g_data = data_raw[:N_blocks * tau].reshape(N_blocks, tau).sum(axis=1)

        m_n = np.mean(g_data)
        s_n = np.std(g_data, ddof=1) if len(g_data) > 1 else 1.0

        # 1. Экспериментальная гистограмма (Относительные частоты)
        fig.add_trace(
            go.Histogram(
                x=g_data, histnorm='probability density',
                name='Эксперимент', marker_color='teal', opacity=0.6,
                xbins=dict(start=g_data.min() - 0.5, end=g_data.max() + 1.5, size=1),
                showlegend=(idx == 0)
            ),
            row=row, col=col_idx
        )

        # Отрезок значений для теоретических кривых
        x_theory = np.arange(g_data.min(), g_data.max() + 1)

        # 2. Теория: Распределение Пуассона
        y_poisson = poisson.pmf(x_theory, mu=m_n)
        fig.add_trace(
            go.Scatter(
                x=x_theory, y=y_poisson, mode='lines+markers',
                name='Пуассон', line=dict(color='crimson', dash='dash', width=2),
                marker=dict(size=4), showlegend=(idx == 0)
            ),
            row=row, col=col_idx
        )

        # 3. Теория: Распределение Гаусса
        x_gauss = np.linspace(g_data.min(), g_data.max(), 200)
        y_gauss = norm.pdf(x_gauss, loc=m_n, scale=s_n)
        fig.add_trace(
            go.Scatter(
                x=x_gauss, y=y_gauss, mode='lines',
                name='Гаусс', line=dict(color='darkblue', width=2),
                showlegend=(idx == 0)
            ),
            row=row, col=col_idx
        )

        # Настройка осей для каждого подграфика
        fig.update_xaxes(title_text="Число отсчетов, n", row=row, col=col_idx)
        fig.update_yaxes(title_text="Доля, w_n", row=row, col=col_idx)

    # Настройки внешнего вида всего коллажа
    fig.update_layout(
        title=f"Распределения для серии данных: {col}",
        title_font=dict(size=18),
        barmode='overlay',
        height=900, width=1300,
        template='plotly_white'
    )

    # Сохраняем в интерактивный HTML-файл
    html_name = f"plots_{col}.html"
    fig.write_html(html_name)
    print(f"  ✔ Создан веб-файл с графиками: {html_name}")

print("\n=== ВСЕ ПРОЦЕССЫ УСПЕШНО ЗАВЕРШЕНЫ БЕЗ ОШИБОК ===")
