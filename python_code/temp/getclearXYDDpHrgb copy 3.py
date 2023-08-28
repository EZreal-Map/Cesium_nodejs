import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 定义三角形拓扑关系
triangles = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]])

# 定义顶点坐标和颜色属性
vertices = np.array([
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.5, 0.5, 1.0]
])

colors = np.array([
    [1.0, 0.0, 0.0, 1.0],  # Red
    [0.0, 1.0, 0.0, 1.0],  # Green
    [0.0, 0.0, 1.0, 1.0],  # Blue
    [1.0, 1.0, 0.0, 1.0],  # Yellow
    [0.5, 0.5, 0.5, 1.0],  # Gray
])

# 为每个面片重复顶点，并设置颜色
triangles_faces = [np.repeat(vertices[triangle_idx][np.newaxis, :], 4, axis=0) for triangle_idx in triangles]
face_colors = np.repeat(colors, 4, axis=0)

# 创建一个3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制三角面片
collection = Poly3DCollection(triangles_faces, facecolors=face_colors)
ax.add_collection3d(collection)

# 设置坐标轴范围
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.set_zlim([0, 1])

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 显示图形
plt.show()
