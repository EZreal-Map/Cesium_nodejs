import numpy as np
from scipy.optimize import minimize

# 提供的(x, y)坐标对
x = [255, 250, 240, 230, 220, 210, 200, 195, 190, 185, 180, 175, 170, 165, 160, 155, 150, 145, 140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 15, 10, 5, 4, 3, 2, 1, 0.0000000001]
y = [255, 253, 248, 243, 238, 233, 228, 226, 223, 220, 218, 215, 212, 209, 206, 203, 200, 197, 194, 188, 181, 174, 167, 159, 151, 142, 132, 122, 110, 96, 80, 70, 58, 43, 39, 34, 28, 20, 0.0000000001]

# 还原x和y的原始值（乘以255）
x_original = np.array([val / 255 for val in x])
y_original = np.array([val / 255 for val in y])

# 定义目标函数
def objective(gamma):
    return np.sum((y_original - x_original**(1/gamma))**2)

# 使用优化器找到最优gamma值
initial_guess = 2.2  # 初始猜测值
result = minimize(objective, initial_guess, bounds=[(0, None)])

# 输出最优gamma值
gamma = result.x[0]
print(f"最优的gamma值为: {gamma}")
