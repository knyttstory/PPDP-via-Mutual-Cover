import pandas as pd
import random


random.seed(42)
preserve_ratio = 0.05
data_path = "./original_data.csv"           # 原始文件的路径

original_data = pd.read_csv(data_path)       # 读取原始文件
print(original_data.info())

columns_name = list(original_data.columns)
drop_colomns = ["RELATED", "RACED", "EDUCD", "INCTOT"]         # 去掉的属性
add_columns = list(set(columns_name) ^ set(drop_colomns))      # 保留的属性
print(add_columns)
filter_tuples = original_data[add_columns].copy()         # 筛选保留属性的数据
print(filter_tuples.head())

temp_flag = None
for key_column in filter_tuples:
    if temp_flag is None:
        temp_flag = filter_tuples[key_column] > 0          # 去掉值为0的数据
    else:
        temp_flag &= filter_tuples[key_column] > 0
temp_flag &= filter_tuples["AGE"] >= 16
temp_flag &= filter_tuples["AGE"] <= 70
filter_tuples = filter_tuples[temp_flag]
print(filter_tuples.head())
print(filter_tuples.info())

preserve_rows = []          # 随机保留一些数据
for rindex, _ in filter_tuples.iterrows():
    if random.random() < preserve_ratio:
        preserve_rows.append(rindex)
filter_tuples = filter_tuples.loc[preserve_rows, add_columns]
print(filter_tuples.info())

duplicate_columns = add_columns.copy()
duplicate_columns.remove("INCWAGE")
duplicate_columns.remove("OCC")
filter_tuples = filter_tuples.drop_duplicates(subset=duplicate_columns)     # 删除重复数据
print(filter_tuples.info())
for key_column in filter_tuples:
    print(filter_tuples[key_column].value_counts())
filter_tuples.to_csv("./filter_data.csv", sep=",", header=True, index=False)
