import os
import pandas as pd

# 设置csv文件所在的文件夹路径
# folder_path = 'E:\\ColumbiaUniversity\\ELEN6889\\Project'
#folder_path = 'E:\\ColumbiaUniversity\\ELEN6889\\Project\\dataset\\name'
folder_path = 'E:\\ColumbiaUniversity\\ELEN6889\\Project\\dataset\\place+name'

# 读取文件夹中的所有csv文件
files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# 创建一个空的DataFrame对象
df = pd.DataFrame()

# 遍历每个文件并将它们合并到DataFrame中
for file in files:
    file_path = os.path.join(folder_path, file)
    temp_df = pd.read_csv(file_path, header=None)
    df = pd.concat([df, temp_df])

# 保存合并后的DataFrame到一个新的csv文件中
merged_file_path = "mergedPlaceName.csv"
df.to_csv(merged_file_path, index=False)