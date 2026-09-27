import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def data_export(file_path): 
    data = []
    with open(file_path, encoding='accp1251') as f:
        for line in f:
            n = line.strip()
            if n: 
                try:
                    data.append(int(n))  
                except ValueError:
                    continue 
    return data

def grouping_data(data_list, n): 

    data_list_copy = data_list.copy() 
    grouped_data = []
    
    while len(data_list_copy) >= n:
        summ = 0
        for i in range(n):
            x = data_list_copy.pop(0)
            summ += x
        grouped_data.append(summ)
    return grouped_data

def unique(n): 
    unique_set = set(n)
    unique_list = list(unique_set)
    return unique_list

path = input("Введите путь к файлу: ")
t = int(input("Введите размер группы (t): "))

nums = data_export(path)
data_e = grouping_data(nums, t)

plt.hist(data_e, edgecolor='black') 
plt.title("Гистограмма сгруппированных данных")
plt.xlabel("Сумма в группе")
plt.ylabel("Частота")
plt.show()