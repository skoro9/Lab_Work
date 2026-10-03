import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Calculation functions

def grouping_data(data_list, n): # Группировка и суммирование соседних данных по n штук
    result = []
    while data_list:
        summ = 0
        for i in range(n):
            x = data_list.pop(0)
            summ += x
        result.append(summ)
    return result


def unique(data_list): # Поиск уникальных элементов
    return list(set(data_list))


def frequency(unique_list, data_list): # Нахождение частоты появления элемента в списке
    amount = len(unique_list)
    amount_list = []
    while unique_list:
        x = unique_list.pop(0)
        amount_list.append(data_list.count(x))
    return amount_list


# Data extraction
data = pd.read_excel('data.xlsx')

# Experimental data
experimental_data = data['Experimental'].values.tolist()

# Simulation data

regular = data['Sim_Reg'].values.tolist()

intens_20 = data['Sim_Intens_20'].values.tolist()
intens_40 = data['Sim_Intens_40'].values.tolist()
intens_80 = data['Sim_Intens_80'].values.tolist()

Pareto_alpha_1 = data['Sim_Pareto_alpha_1'].values.tolist()
Pareto_alpha_2 = data['Sim_Pareto_alpha_2'].values.tolist()

exp_1 = data['Sim_exp_1'].values.tolist()
exp_2 = data['Sim_exp_2'].values.tolist()
exp_3 = data['Sim_exp_3'].values.tolist()

# Переменные

# Переменные для экспериментальных данных

# Списки для данных
grouped_experimental_10 = grouping_data(experimental_data, 10)
grouped_experimental_20 = grouping_data(experimental_data, 20)
grouped_experimental_40 = grouping_data(experimental_data, 40)
grouped_experimental_80 = grouping_data(experimental_data, 80)
unique_experimental_1 = unique(experimental_data)
unique_experimental_10 = unique(grouped_experimental_10)
unique_experimental_20 = unique(grouped_experimental_20)
unique_experimental_40 = unique(grouped_experimental_40)
unique_experimental_80 = unique(grouped_experimental_80)
frequency_experimental_1 = frequency(unique_experimental_1, experimental_data)
frequency_experimental_10 = frequency(unique_experimental_10, grouped_experimental_10)
frequency_experimental_20 = frequency(unique_experimental_20, grouped_experimental_20)
frequency_experimental_40 = frequency(unique_experimental_40, grouped_experimental_40)
frequency_experimental_80 = frequency(unique_experimental_80, grouped_experimental_80)
# Вычисления конкретных величин

# Среднее число регистрируемых частиц
average_experimental_1 = np.mean(experimental_data)
average_experimental_10 = np.mean(grouped_experimental_10)
average_experimental_20 = np.mean(grouped_experimental_20)
average_experimental_40 = np.mean(grouped_experimental_40)
average_experimental_80 = np.mean(grouped_experimental_80)

sigma_experimental_1 = np.std(experimental_data, ddof=0)
sigma_experimental_10 = np.std(grouped_experimental_10, ddof=0)
sigma_experimental_20 = np.std(grouped_experimental_20, ddof=0)
sigma_experimental_40 = np.std(grouped_experimental_40, ddof=0)
sigma_experimental_80 = np.std(grouped_experimental_80, ddof=0)

sigma_n_mean_experimental_1 = sigma_experimental_1 / np.sqrt(len(experimental_data))
sigma_n_mean_experimental_10 = sigma_experimental_10 / np.sqrt(len(grouped_experimental_10))
sigma_n_mean_experimental_20 = sigma_experimental_20 / np.sqrt(len(grouped_experimental_20))
sigma_n_mean_experimental_40 = sigma_experimental_40 / np.sqrt(len(grouped_experimental_40))
sigma_n_mean_experimental_80 = sigma_experimental_80 / np.sqrt(len(grouped_experimental_80))

# г) Средняя интенсивность в секунду j и её погрешность sigma_j

j_experimental_1 = average_experimental_1 / 1
j_experimental_10 = average_experimental_10 / 10
j_experimental_20 = average_experimental_20 / 20
j_experimental_40 = average_experimental_40 / 40
j_experimental_80 = average_experimental_80 / 80

sigma_j_experimental_1 =