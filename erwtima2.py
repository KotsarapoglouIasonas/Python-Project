import pandas as pd
import matplotlib.pyplot as plt

#diavasma tou excel apo to arxeio
df = pd.read_excel (r'pandasexcel.xlsx')

#upologismos kai emfanisi twn keliwn pou einai kena kai upologismos mean gia kathe stili
empty_percent = df.isnull().sum() / df.shape[0] * 100.00
print(empty_percent)

#gia kathe stili sumplirwnei ta kena kelia me to meso oro tis stilis
df=df.fillna(df.mean())
print (df['no_reviews'])

plot = df.plot(kind='scatter',x='no_reviews',y='times_dl',color='red')
fig = plot.get_figure()
fig.savefig('output.png')