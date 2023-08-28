# 1.1、getLLRHD.py
# 输入：读取初始时刻文件夹里面的center.txt文件、和每个时刻对应的文件夹里面的H、S文件。

# 输出：

# 1. 在初始时刻文件夹里面生成一个subcontent.txt文件，便于JavaScript获取子目录。（PS:JavaScript不容易获取正在运行子目录）。
# 2. 在每一时刻文件夹里面生成一个LLRHD.txt文件，这些文件是程序主要目的，用于Cesium渲染不同时刻的洪水数据。

# LLRHD.txt每行有5列，从左到右依次是LLRHD（Longitude,Latitude,Radius,Height,DEM）。

import os
import time
from pyproj import Proj


def get_subdirectories(directory_path):
    subdirectories = [name for name in os.listdir(
        directory_path) if os.path.isdir(os.path.join(directory_path, name))]
    return subdirectories


def write_subdirectories_to_file(sorted_subdirectories, file_path):
    with open(file_path, 'w') as f:
        # 将每个子目录名称写入文件，每个名称占一行
        for directory in sorted_subdirectories[:-1]:
            f.write(directory + "\n")
        # 最后一行领出来for循环写，避免文件末尾多出一行空行
        f.write(sorted_subdirectories[-1])


def read_data_between_brackets(file_path):
    data = []
    inside_brackets = False

    with open(file_path, 'r') as file:
        for line in file:
            if ')\n' == line:
                inside_brackets = False
                break
            if inside_brackets:
                line = float(line.rstrip('\n'))  # 移除行末的换行符
                data.append(line)
            if '(\n' == line:
                inside_brackets = True
    return data


def read_center_data(center_file_path, transform=None):
    with open(center_file_path, 'r') as center_file:
        center_data = []
        for line in center_file:
            longitude, latitude, _, radius = line.strip().split(',')
            if (transform):
                longitude, latitude = transform(
                    longitude, latitude, inverse=True)
            center_data.append((longitude, latitude, radius))
    return center_data


def save_LLHRD_data(LLRHD_file_path, H_data, S_data, center_data):
    with open(LLRHD_file_path, 'w') as LLRHD_file:
        for i, (H_line, S_line, (longitude, latitude, radius)) in enumerate(zip(H_data, S_data, center_data)):
            LLRHD_data = f"{longitude},{latitude},{radius},{H_line},{S_line}"
            if i > 0:
                LLRHD_file.write('\n')  # 跳过第一个行，输入换行符
            LLRHD_file.write(LLRHD_data)


# 主函数main()
# 记录开始时间
start_time = time.time()
# 替换为你的大文件夹路径
directory_path = '../flood/30jiami'
subdirectories = get_subdirectories(directory_path)

# 按照数字大小排序
sorted_subdirectories = sorted(subdirectories, key=lambda x: int(x))
# 读取directory_path = '../flood/30jiami'下的第一个文件夹 [0] 里面的center.txt文件，读取中心点经纬度+半径数据
center_file_path = os.path.join(
    directory_path, sorted_subdirectories[0], 'center.txt')
# 保存子目录为directory_path = '../flood/30jiami'下的第一个文件夹 [0] 里面的subcontent.txt文件
subcontent_file_path = os.path.join(
    directory_path, sorted_subdirectories[0], 'subcontent.txt')
# 调用函数，将子目录名称写入 subcontent.txt 文件
write_subdirectories_to_file(sorted_subdirectories[1:], subcontent_file_path)

# 定义一个UTM投影坐标系统，用做center.txt坐标（utm113）转换为经纬度坐标
utm113 = Proj("+proj=tmerc +lon_0=113.35 +y_0=0 +x_0=500000 +ellps=IAU76 \
+towgs84=-7.849095,18.661172,12.682502,0.809388,-1.667217,-56.719783,-3.30421e-007 +units=m +no_defs")

center_data = read_center_data(center_file_path, utm113)  # 关键数据 经纬度+半径
# 因为每个文件夹里面的DEM数据都是不变的，读取一份就行
S_file_path = os.path.join(directory_path, sorted_subdirectories[1], 'S')
S_data = read_data_between_brackets(S_file_path)  # 关键数据 DEM
# 计数:写入第count个文件
count = 1
for directory in sorted_subdirectories[1:]:
    H_file_path = os.path.join(directory_path,  directory, 'H')
    # S_file_path = os.path.join(directory_path, directory, 'S')
    LLRHD_file_path = os.path.join(directory_path, directory, 'LLRHD.txt')

    H_data = read_data_between_brackets(H_file_path)  # 关键数据 水深
    # S_data = read_data_between_brackets(S_file_path)  # 关键数据 DEM

    save_LLHRD_data(LLRHD_file_path, H_data, S_data, center_data)
    print(f'当前正在写入第{count}/{len(sorted_subdirectories[1:])}个文件夹')
    count += 1


# 记录结束时间
end_time = time.time()
# 计算运行时间
execution_time = end_time - start_time
print(f"运行完成：一共写入{count-1}个文件夹,在每一文件夹内生成一个LLRHD.txt,每个文件包含{len(H_data)}个数据")
print("代码运行时间为：", execution_time, "秒")

# 运行完成：一共写入175个文件夹,在每一文件夹内生成一个LLRHD.txt,每个文件包含526318个数据
# 代码运行时间为： 309.91260170936584 秒
