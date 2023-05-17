import os
import pandas as pd

path = "./result/"
files = os.listdir(path)
# print(files)

eva_df = pd.read_csv(os.path.join(path, files[0]))

for i in range(1, len(files)-1):

    df = pd.read_csv(os.path.join(path, files[i]))
    eva_df = pd.concat([eva_df, df], axis=0)

# print(eva_df)
eva_df.to_csv(os.path.join(path, "results.csv"), index=False)
