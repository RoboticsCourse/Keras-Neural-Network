import pandas as pd
import matplotlib.pyplot as plt

dataframe = pd.read_csv("features_test.csv")
df = pd.DataFrame(dataframe)
print(df.groupby(['Forward']).count())
print(df.groupby(['Speed']).count())
print(df.groupby(['Forward', 'Speed']).size())

dataframe = pd.read_csv("original_data.csv")
df = pd.DataFrame(dataframe)
df.plot(x='Forward', y='Speed', style='o')
plt.show()


