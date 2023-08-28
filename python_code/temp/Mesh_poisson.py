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

# 为点云计算法线
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

# 进行Ball Pivoting曲面重建，生成mesh
radii = [0.05]  # 调整Ball Pivoting的半径列表
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(radii))

# 将颜色信息传递给生成的曲面对象
mesh.vertex_colors = pcd.colors

# 将颜色信息传递给生成的曲面对象
mesh.vertex_colors = pcd.colors

# 同时显示原先的点云图和重构的曲面
o3d.visualization.draw_geometries([mesh])
# o3d.visualization.draw_geometries([pcd, mesh])
