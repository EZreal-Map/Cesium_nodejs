import numpy as np
import open3d as o3d

# 读取包含点云数据的txt文件
file_path = "../flood/30jiami/17520/XYDDpHrgb_0.01.txt"  # 替换为你的txt文件路径
# 指定逗号为分隔符
data = np.loadtxt(file_path, delimiter=',')

# 提取XYZ和RGB信息
points = data[:, :3]
colors = data[:, 3:] / 255.0  # 将RGB值范围转换为[0, 1]

# 创建Open3D的PointCloud对象
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)

# 可视化点云数据
o3d.visualization.draw_geometries([pcd])
