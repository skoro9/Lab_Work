import pandas as pd


df = pd.read_excel('data.xlsx')

pareto  = df['Sim_Pareto_alpha_2'].values.tolist()

num_amount = {}
unique = set(pareto)
unique = list(unique)
unique.sort()
for i in unique:
    x = pareto.count(i)
    num_amount.update({i:x})    

print(num_amount)