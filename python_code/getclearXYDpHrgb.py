# 1.5、getclearXYD_XYDpHrgb.py 的子集合 --> getclearXYDpHrgb.py

# XYDpHrgb（上表面点）  保存为  1、clearXYDpHrgb.txt  -->  2、clearXYDpHrgb.las  

import time
import os
import laspy
import numpy as np


def get_subdirectories(directory_path):
    subdirectories = [name for name in os.listdir(
        directory_path) if os.path.isdir(os.path.join(directory_path, name))]
    return subdirectories


def read_xyd_data(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            # 去除每行末尾的换行符并将数据转换为浮点数
            x, y, d = map(float, line.strip().split(','))
            data.append((x, y, d))
    return data


def save_XYDDpHRGB_lasdata(txt_file_path,las_file_path):
    # 读取文件数据并转换为NumPy数组
    data = np.loadtxt(txt_file_path, delimiter=',', dtype=float)

    # 创建LAS文件
    out_las = laspy.create(point_format=2) # 点格式2包含RGB数据
    # 将X、Y、Z坐标数据赋值给out_las对象
    out_las.x = data[:, 0]
    out_las.y = data[:, 1]
    out_las.z = data[:, 2]

    # 设置RGB颜色值
    out_las.red = data[:, 3].astype(np.uint16)
    out_las.green = data[:, 4].astype(np.uint16)
    out_las.blue = data[:, 5].astype(np.uint16)

    # 设置LAS文件头信息（根据需要调整）
    # 设置LAS文件头信息，包括空间参考信息
    out_las.header.min = [min(out_las.x), min(out_las.y), min(out_las.z)]
    out_las.header.max = [max(out_las.x), max(out_las.y), max(out_las.z)]

    # 设置LAS文件的坐标系为WGS 84地理坐标系（EPSG:4326）
    # out_las.header.proj4 = '+proj=longlat +datum=WGS84 +no_defs'

    # 写入并保存LAS文件
    out_las.write(las_file_path)


def generate_color_gradient(num_segments, start_color, end_color):
    # 获取颜色渐变数组
    gradient_colors = [(255,255,255)]
    for i in range(num_segments-1):
        t = i / (num_segments - 1)
        r = start_color[0] + (end_color[0] - start_color[0]) * t
        g = start_color[1] + (end_color[1] - start_color[1]) * t
        b = start_color[2] + (end_color[2] - start_color[2]) * t
        gradient_colors.append([round(r), round(g), round(b)])  # 将颜色值为0-255的范围 round()四省五入取整

    return gradient_colors


def get_interval_index(H):
    # 区间定义，第一个元素表示最小值，最后一个元素表示无穷大，其他值为各个区间的上限值
    intervals = [0,0.01, 0.25, 0.50, 1.0, 1.50, 2.0, 2.5,
                 3, 3.5, 4, 4.5, 5, 7.5, 10, float('inf')]

    # 循环遍历所有区间，找到第一个H小于等于的区间，然后返回对应的索引
    for i in range(len(intervals)):
        if H <= intervals[i+1]:
            return i

    # 如果H小于所有区间的第一个值，则属于第一个区间
    return 0


# 主函数main()
# 记录开始时间
start_time = time.time()
# 替换为你的大文件夹路径
directory_path = '../flood/30jiami'
subdirectories = get_subdirectories(directory_path)


def read_and_filter_data(XYD_list_lines, input_file, output_file, threshold, gradient_colors):
    kept_data = []
    deleted_data = 0

    # input_file是每个时刻的XYDpH.txt
    with open(input_file, 'r') as f:
        lines = f.readlines()

        for i in range(len(lines)):
            XYDpH_list = lines[i].rstrip('\n').split(',')
            XYD_list = XYD_list_lines[i].rstrip('\n').split(',')
            try:
                H = float(XYDpH_list[2])-float(XYD_list[2])
                if H >= threshold:
                    index = get_interval_index(H)
                    rgbList = gradient_colors[index]
                    # 上表面
                    upsurface_point = lines[i].rstrip(
                        '\n') + ',' + ','.join(str(element) for element in rgbList) + '\n'
                    kept_data.append(upsurface_point)
                    # 下表面
                    # subsurface_point = XYD_list_lines[i].rstrip(
                    #     '\n') + ',' + ','.join(str(element) for element in rgbList) + '\n'
                    # kept_data.append(subsurface_point)
                else:
                    deleted_data += 1
            except ValueError:
                print(f"Error: Invalid data format in line: {lines[i]}")
    kept_data[-1] = kept_data[-1].rstrip('\n')  # 移除末尾的换行符
    # print(kept_data[-1])
    with open(output_file, 'w') as f:
        f.writelines(kept_data)

    return deleted_data, len(kept_data), kept_data





# 按照数字大小排序
sorted_subdirectories = sorted(subdirectories, key=lambda x: int(x))
xyd_file_path = os.path.join(
    directory_path, sorted_subdirectories[0], 'XYD.txt')
with open(xyd_file_path, 'r') as f:
    XYD_list_lines = f.readlines()
threshold = 0.05  # 阈值
count = 1
# 生成颜色渐变数组，从浅蓝色到深蓝色
intervals = [0, 0.01,0.25, 0.50, 1.0, 1.50, 2.0, 2.5,
             3, 3.5, 4, 4.5, 5, 7.5, 10, float('inf')]
num_segments = len(intervals)-1
start_color = [149, 208, 238]
end_color = [10, 9, 145]
gradient_colors = generate_color_gradient(
    num_segments, start_color, end_color)
for directory in sorted_subdirectories[1:]:
    input_file = os.path.join(directory_path, directory, 'XYDpH.txt')
    # output_file = os.path.join(directory_path, directory, 'clearLLRHD.txt')
    output_file = os.path.join(
        directory_path, directory, 'clearXYDpHrgb_'+str(threshold)+'.txt')
    # # 如果生成文件的名字取错了，可以通过这个自动删除文件
    # file_path_to_delete = os.path.join(
    #     directory_path, directory, 'XYDDpH_'+str(threshold)+'.txt')
    # os.remove(file_path_to_delete)
    # 保存为XYDDpH.txt
    deleted_count, kept_count, kept_data = read_and_filter_data(
        XYD_list_lines, input_file, output_file, threshold, gradient_colors)  # 调用主函数
    # 保存为XYDDpH.las
    XYDpHlas_file_path = os.path.join(
        directory_path, directory, 'clearXYDpHrgb_'+str(threshold)+'.las')
    save_XYDDpHRGB_lasdata(output_file,XYDpHlas_file_path)
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