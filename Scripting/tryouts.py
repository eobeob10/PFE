import pandas as pd
df = pd.read_csv("Host Discovery/interface.txt")
print(df.iloc[0][0])
print(type(df))
