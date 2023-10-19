# 1.3、statisticsLLRHD.py
# 分别统计 
# H > 0.01 
# H > 0.05
# H > 0.1
# H > 0.15
# 尝试统计每个点被使用的情况，输出保存在初始目录文件下的count_array_0.05.txt  threshold_0.05.png

import time
import os
import numpy as np
import matplotlib.pyplot as plt


def get_subdirectories(directory_path):
    subdirectories = [name for name in os.listdir(
        directory_path) if os.path.isdir(os.path.join(directory_path, name))]
    return subdirectories


def read_and_statistics_data(input_file, threshold, count_array):
    kept_data = []
    deleted_data = []
    count_index = 0
    with open(input_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            data = line.strip().split(',')
            if len(data) == 5:
                try:
                    value = float(data[3])
                    if value > threshold:
                        count_array[count_index] += 1  # 计数
                        kept_data.append(line)
                    else:
                        deleted_data.append(line)
                except ValueError:
                    print(f"Error: Invalid data format in line: {line}")
            count_index += 1

    # kept_data[-1] = kept_data[-1].rstrip('\n') # 移除末尾的换行符
    # print(kept_data[-1])
    # with open(output_file, 'w') as f:
    #     f.writelines(kept_data)

    return len(deleted_data), len(kept_data), count_array


# 主函数main()
# 记录开始时间
start_time = time.time()
# 替换为你的大文件夹路径
directory_path = '../flood/30jiami'
subdirectories = get_subdirectories(directory_path)
# 按照数字大小排序
sorted_subdirectories = sorted(subdirectories, key=lambda x: int(x))

center_file_path = os.path.join(
    directory_path, sorted_subdirectories[0], 'center.txt')

# 打开文件并读取数据
with open(center_file_path, "r") as file:
    line_count = sum(1 for line in file)

threshold = 0.0001
# 阈值

count = 1
count_array = np.zeros(line_count, dtype=int)
deleted_count_array = np.zeros(len(sorted_subdirectories[1:]), dtype=int)
kept_count_array = np.zeros(len(sorted_subdirectories[1:]), dtype=int)
output_file = os.path.join(
    directory_path, sorted_subdirectories[0], 'count_array_'+str(threshold)+'.txt')
for directory in sorted_subdirectories[1:]:
    input_file = os.path.join(directory_path, directory, 'LLRHD.txt')
    # 如果生成文件的名字取错了，可以通过这个自动删除文件
    # file_path_to_delete = os.path.join(directory_path, directory, 'afterClear_LLRHD.txt')
    # os.remove(file_path_to_delete)

    deleted_count, kept_count, count_array = read_and_statistics_data(
        input_file, threshold, count_array)  # 调用主函数
    deleted_count_array[count-1] = deleted_count
    kept_count_array[count-1] = kept_count

    # 打印结果
    deleted_percentage = deleted_count / (deleted_count + kept_count) * 100
    kept_percentage = kept_count / (deleted_count + kept_count) * 100
    print(f'当前正在写入第{count}/{len(sorted_subdirectories[1:])}个文件夹')
    print(f"Deleted rows: {deleted_count:<5}   {deleted_percentage:.2f}%")
    print(f"Kept rows:    {kept_count:<5}   {kept_percentage:.2f}%")
    count += 1

print(f"\n共有{count-1}个时刻(文件夹),每个时刻(文件夹)有{line_count}个网格中心点")
print(f"当筛选条件为 H > {threshold:.2f} 时")
print(f"网格平均点数：{round(np.mean(kept_count_array))}")
print(f"网格最大点数：{np.max(kept_count_array)}")

with open(output_file, 'w') as file:
    for item in count_array[:-1]:
        file.write(str(item) + '\n')
    file.write(str(count_array[-1]))  # 末位不用 + '\n'

# 创建柱形图
# plt.bar(sorted_subdirectories[1:], kept_count_array)
print(kept_count_array)
plt.bar(range(1, len(kept_count_array) + 1), kept_count_array)
# 设置图表标题和标签
plt.title('threshold = '+str(threshold))
plt.xlabel('time')
plt.ylabel('kept_count')
output_png = os.path.join(
    directory_path, sorted_subdirectories[0], 'threshold_'+str(threshold)+'.png')
# 保存图表为图片
plt.savefig(output_png)
# 显示图表
plt.show()
# 记录结束时间
end_time = time.time()
# 计算运行时间
execution_time = end_time - start_time
print("代码运行时间为：", execution_time, "秒")
# 代码运行时间为： 94.0535569190979 秒