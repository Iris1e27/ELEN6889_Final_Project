import os
import pandas as pd

# 输入目录和输出文件名
input_dir = 'dataset'
output_file = 'fileRowNums.txt'
dir_list = ['name', 'place+name']

# 遍历name和place+name两个文件夹
for folder in dir_list:
    # 获取文件夹的路径
    folder_path = os.path.join(input_dir, folder)
    # 遍历文件夹中的CSV文件
    for file in os.listdir(folder_path):
        # 获取CSV文件的路径
        file_path = os.path.join(folder_path, file)
        # 使用pandas读取CSV文件并计算行数
        df = pd.read_csv(file_path)
        num_rows = len(df.index)
        # 将文件名和行数写入输出文件中
        with open(output_file, 'a') as f:
            f.write(f'{file},{num_rows}\n')
