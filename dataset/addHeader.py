import pandas as pd

# 读取CSV文件，并跳过前两行
df = pd.read_csv('mergedAll.csv', skiprows=2, header=None)

# 给DataFrame添加header
df.columns = ["team", "timestamp", "text", "location", "likes", "sentiment"]

# 将处理后的DataFrame写入CSV文件
df.to_csv('mergedAllWithHeader.csv', index=False)
