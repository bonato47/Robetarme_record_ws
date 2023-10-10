from plot_verification import *
import pandas as pd

data = pd.read_csv("../data/csv_transform/tes2t_shot_target1_transform.csv", index_col=False)
print(data)
#plot_path(data,"tes2t_shot_target1_transform")