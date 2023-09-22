import trimesh
import numpy as np
import os
from pyproj import Proj

def get_subdirectories(directory_path):
    subdirectories = [name for name in os.listdir(
        directory_path) if os.path.isdir(os.path.join(directory_path, name))]
    return subdirectories


directory_path = '../flood/30jiami'
subdirectories = get_subdirectories(directory_path)
# 按照数字大小排序
sorted_subdirectories = sorted(subdirectories, key=lambda x: int(x))

# 定义一个空列表用于存储面信息
faces = []
# 定义一个空列表用于存储顶点信息
vertices = []

# 打开并读取文件
with open(directory_path + '/mesh_1108.2dm', 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 如果行以'E3T'开头，提取第3到5个数，并将其转为整数后减1（因为索引从0开始）
        if line.startswith('E3T'):
            face_data = list(map(int, line.split()[2:5]))
            face_data = [x - 1 for x in face_data]  # 减1以符合Python的索引规则
            faces.append(face_data)
        if line.startswith('ND'):
            vertex_data = list(map(float, line.split()[2:5]))
            vertices.append(vertex_data)
# 输出faces
# print(faces)


# 定义一个UTM投影坐标系统，用做center.txt坐标（utm113）转换为经纬度坐标
utm113 = Proj("+proj=tmerc +lon_0=113.35 +y_0=0 +x_0=500000 +ellps=IAU76 \
+towgs84=-7.849095,18.661172,12.682502,0.809388,-1.667217,-56.719783,-3.30421e-007 +units=m +no_defs")

count = 1
threshold = 0.05
for directory in sorted_subdirectories[1:]:
    print(f'当前正在写入第{count}/{len(sorted_subdirectories[1:])}个文件夹----{directory}')

    Hrgb_inputfile_path = os.path.join(
        directory_path, directory, 'Hrgb.txt')
    glb_outputfile_path = os.path.join(
        directory_path, directory, 'triangle_mesh_' + str(threshold) + '.glb')
    # 从不同时刻文件读取数据并拆分成顶点坐标和颜色信息
    data = np.loadtxt(Hrgb_inputfile_path, delimiter=',')
    H = data[:, :1]  # 第一列是H
    Facecolors = data[:, 1:]    # 后三列是r, g, b颜色值
    # faces = [[0, 1, 2],[0, 1, 3]]

    rectify_vertices = np.array(vertices)
    # 定义一个空列表用于存储顶点颜色信息
    pointColors = np.zeros((len(vertices), 3), dtype=int)
    for i, value in enumerate(faces):
        # print(value)
        for index in value:
            pointColors[index] = np.array(Facecolors[i])
            # pointColors[index] = [255,0,0]
            if rectify_vertices[index,2] == vertices[index][2]:
                rectify_vertices[index,2] += H[i]
                # print(rectify_vertices[index][2])
            # print(index)

    pointColors = pointColors.tolist()
    # print(pointColors)

    # 修改vertices，纠正glb中心点
    position_file_path = os.path.join(
        directory_path, directory, 'center_point_position_'+str(threshold)+'.txt')
    # 打开文件并读取内容
    with open(position_file_path, 'r') as file:
        line = file.readline().strip()  # 读取并去除首尾空白字符
        longitude, latitude, height = map(float, line.split())
    utm_x, utm_y = utm113(longitude, latitude, inverse=False)
    
    print(f"中心点修正 ---> utm_x: {utm_x}, utm_y: {utm_y}, Height: {height}")
    # rectify_vertices = np.array(vertices)
    rectify_vertices = rectify_vertices - np.array([utm_x,utm_y,height])
    # 把下表面 + H 变为 上表面
    # rectify_vertices[:,2] =  rectify_vertices[:,2] + np.array(H)
    rectify_vertices = rectify_vertices.tolist()

    # 清除H<0.05的faces数据
    clearFaces = []
    for i, h in enumerate(H):
        if(h > threshold):
            clearFaces.append(faces[i])

    mesh = trimesh.Trimesh(vertices=rectify_vertices, faces=clearFaces, vertex_colors=pointColors)
    # 保存为glb格式
    mesh.export(glb_outputfile_path, file_type='glb')
    
    count += 1
    # 用trimesh内置的方法进行可视化
    # mesh.show()