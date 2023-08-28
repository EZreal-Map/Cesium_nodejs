import os
import time
# from pyproj import Proj
import laspy
import numpy as np


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
            longitude, latitude, _, _ = line.strip().split(',')
            if (transform):
                longitude, latitude = transform(
                    longitude, latitude, inverse=True)
            center_data.append((longitude, latitude))
    return center_data


def save_XYDH_data(XYDH_file_path, center_data, S_data, H_data=None):
    with open(XYDH_file_path, 'w') as XYDH_file:
        if H_data is None:  # 返回下表面的点云txt
            for i, (S_line, (X, Y)) in enumerate(zip(S_data, center_data)):
                XYDH_data = f"{X},{Y},{S_line}"
                if i > 0:
                    XYDH_file.write('\n')  # 跳过第一个行，输入换行符
                XYDH_file.write(XYDH_data)
        else:  # 返回上表面的点云txt
            for i, (H_line, S_line, (X, Y)) in enumerate(zip(H_data, S_data, center_data)):
                XYDH_data = f"{X},{Y},{H_line+S_line}"
                if i > 0:
                    XYDH_file.write('\n')  # 跳过第一个行，输入换行符
                XYDH_file.write(XYDH_data)


def save_XYDH_lasdata(las_file_path, X, Y, Z):
    # 创建LAS文件
    out_las = laspy.create(point_format=1)
    # 将X、Y、Z坐标数据赋值给out_las对象
    out_las.x = X
    out_las.y = Y
    out_las.z = Z

    # 设置LAS文件头信息（根据需要调整）
    # 设置LAS文件头信息，包括空间参考信息
    out_las.header.min = [min(out_las.x), min(out_las.y), min(out_las.z)]
    out_las.header.max = [max(out_las.x), max(out_las.y), max(out_las.z)]

    # 设置LAS文件的坐标系为WGS 84地理坐标系（EPSG:4326）
    # out_las.header.proj4 = '+proj=longlat +datum=WGS84 +no_defs'

    # 写入并保存LAS文件
    out_las.write(las_file_path)


# 主函数main()
# 记录开始时间
start_time = time.time()
# 替换为你的大文件夹路径
directory_path = '../flood/30jiami'
subdirectories = get_subdirectories(directory_path)

# 按照数字大小排序
sorted_subdirectories = sorted(subdirectories, key=lambda x: int(x))
# 保存子目录为directory_path = '../flood/30jiami'下的第一个文件夹 [0] 里面的subcontent.txt文件
subcontent_file_path = os.path.join(
    directory_path, sorted_subdirectories[0], 'subcontent.txt')
# 调用函数，将子目录名称写入 subcontent.txt 文件
write_subdirectories_to_file(sorted_subdirectories[1:], subcontent_file_path)

# 定义一个UTM投影坐标系统，用做center.txt坐标（utm113）转换为经纬度坐标 (点云数据需要的是投影坐标)
# utm113 = Proj("+proj=tmerc +lon_0=113.35 +y_0=0 +x_0=500000 +ellps=IAU76 \
# +towgs84=-7.849095,18.661172,12.682502,0.809388,-1.667217,-56.719783,-3.30421e-007 +units=m +no_defs")
# 读取directory_path = '../flood/30jiami'下的第一个文件夹 [0] 里面的center.txt文件，读取中心点经纬度X Y(50坐标)
center_file_path = os.path.join(
    directory_path, sorted_subdirectories[0], 'center.txt')
center_data = read_center_data(center_file_path)  # 关键数据 经纬度
# 因为每个文件夹里面的DEM数据都是不变的，读取一份就行
S_file_path = os.path.join(directory_path, sorted_subdirectories[1], 'S')
S_data = read_data_between_brackets(S_file_path)  # 关键数据 DEM
# 保存上表面点云txt x,y,DEM
XYD_file_path = os.path.join(
    directory_path, sorted_subdirectories[0], 'XYD.txt')
save_XYDH_data(XYD_file_path, center_data, S_data)
# 拆分center_data = [(X1, Y1), (X2, Y2), (X3, Y3), ...]
# 初始化空列表，用于存储X和Y坐标
X_data = []
Y_data = []

for i, (X, Y) in enumerate(center_data):
    # 将X和Y坐标分别添加到它们对应的列表中
    X_data.append(float(X))
    Y_data.append(float(Y))

XYDlas_file_path = os.path.join(
    directory_path, sorted_subdirectories[0], 'XYD.las')
save_XYDH_lasdata(XYDlas_file_path, X_data, Y_data, S_data)
# 计数:写入第count个文件
count = 1
for directory in sorted_subdirectories[1:]:
    H_file_path = os.path.join(directory_path,  directory, 'H')
    XYDpH_file_path = os.path.join(directory_path, directory, 'XYDpH.txt')
    # 保存为XYDpH.txt
    H_data = read_data_between_brackets(H_file_path)  # 关键数据 水深
    save_XYDH_data(XYDpH_file_path, center_data, S_data, H_data)
    # 保存为XYDpH.las
    XYDpHlas_file_path = os.path.join(
        directory_path, directory, 'XYDpH.las')
    save_XYDH_lasdata(XYDpHlas_file_path, X_data, Y_data, H_data)
    print(f'当前正在写入第{count}/{len(sorted_subdirectories[1:])}个文件夹')
    count += 1


# 记录结束时间
end_time = time.time()
# 计算运行时间
execution_time = end_time - start_time
print(
    f"运行完成：一共写入{count}个文件夹,在初始文件夹里生成一个XYD.txt/.las\
    \n在每一文件夹内生成一个XYDpH.txt/.las,每个文件包含{len(H_data)}个数据")
print("代码运行时间为：", execution_time, "秒")

# 运行完成：一共写入175个文件夹,在每一文件夹内生成一个LLRHD.txt,每个文件包含526318个数据
# 代码运行时间为： 309.91260170936584 秒
