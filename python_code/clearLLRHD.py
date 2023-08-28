# 1.2、clearLLRHD.py

# 输入：读取上一步在每一时刻文件夹里面生成的LLRHD.txt文件。

# 输出：清除H(水深)小于阈值的数据，比如threshold = 0.05  #阈值，生成精简后的洪水数据文件clearLLRHD.py。

import time
import os


def get_subdirectories(directory_path):
    subdirectories = [name for name in os.listdir(
        directory_path) if os.path.isdir(os.path.join(directory_path, name))]
    return subdirectories


def read_and_filter_data(input_file, output_file, threshold):
    kept_data = []
    deleted_data = []

    with open(input_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            data = line.strip().split(',')
            if len(data) == 5:
                try:
                    value = float(data[3])
                    if value > threshold:
                        kept_data.append(line)
                    else:
                        deleted_data.append(line)
                except ValueError:
                    print(f"Error: Invalid data format in line: {line}")
    kept_data[-1] = kept_data[-1].rstrip('\n')  # 移除末尾的换行符
    # print(kept_data[-1])
    with open(output_file, 'w') as f:
        f.writelines(kept_data)

    return len(deleted_data), len(kept_data), kept_data


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

threshold = 0.05  # 阈值
count = 1
for directory in sorted_subdirectories[1:]:
    input_file = os.path.join(directory_path, directory, 'LLRHD.txt')
    # output_file = os.path.join(directory_path, directory, 'clearLLRHD.txt')
    output_file = os.path.join(
        directory_path, directory, 'clearLLRHD_'+str(threshold)+'.txt')
    # 如果生成文件的名字取错了，可以通过这个自动删除文件
    file_path_to_delete = os.path.join(
        directory_path, directory, 'clearLLRHD.txt')
    os.remove(file_path_to_delete)
    deleted_count, kept_count, kept_data = read_and_filter_data(
        input_file, output_file, threshold)  # 调用主函数

    # 打印结果
    deleted_percentage = deleted_count / (deleted_count + kept_count) * 100
    kept_percentage = kept_count / (deleted_count + kept_count) * 100
    print(f'当前正在写入第{count}/{len(sorted_subdirectories[1:])}个文件夹')
    print(f"Deleted rows: {deleted_count:<5}   {deleted_percentage:.2f}%")
    print(f"Kept rows:    {kept_count:<5}   {kept_percentage:.2f}%")
    count += 1

# 记录结束时间
end_time = time.time()
# 计算运行时间
execution_time = end_time - start_time
print("代码运行时间为：", execution_time, "秒")
# 代码运行时间为： 94.0535569190979 秒
