import os
import pandas as pd

# 用于保存每个CSV文件的第二列的最早时间和最晚时间
file_times = []

# 指定文件夹路径
folder_paths = [
    r"E:\ColumbiaUniversity\ELEN6889\Project\dataset\name",
    r"E:\ColumbiaUniversity\ELEN6889\Project\dataset\place+name"
]

# 遍历文件夹
for folder_path in folder_paths:
    for file_name in os.listdir(folder_path):
        # 只处理CSV文件
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            # 读取CSV文件
            df = pd.read_csv(file_path)
            # 获取第二列的最早时间和最晚时间
            col_name = df.columns[1]
            min_time = df[col_name].min()
            max_time = df[col_name].max()
            # 将结果保存到列表中
            file_times.append([file_name, min_time, max_time])

# 将结果保存到CSV文件中
result_df = pd.DataFrame(file_times, columns=["File Name", "Earliest Time", "Latest Time"])
result_df.to_csv("fileTime.csv", index=False)