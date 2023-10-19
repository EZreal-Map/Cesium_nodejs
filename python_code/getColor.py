import matplotlib.pyplot as plt

def generate_color_gradient(num_segments, start_color, end_color):
    # 获取颜色渐变数组
    gradient_colors = [[255,255,255]]
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

def plot_color_gradient(gradient_colors):
    r_values = [color[0] for color in gradient_colors]
    g_values = [color[1] for color in gradient_colors]
    b_values = [color[2] for color in gradient_colors]

    plt.plot(r_values, color='red', label='Red')
    plt.plot(g_values, color='green', label='Green')
    plt.plot(b_values, color='blue', label='Blue')

    plt.xlabel('Segment')
    plt.ylabel('Color Value')
    plt.title('Color Gradient')
    plt.legend()
    plt.show()

def find_color_indices(rgb_color, gradient_colors):
    r, g, b = rgb_color

    r_indices, g_indices, b_indices = [], [], []

    for color in gradient_colors:
        r_indices.append(color[0])
        g_indices.append(color[1])
        b_indices.append(color[2])

    r_range = 0
    g_range = 0
    b_range = 0

    for i in range(1, len(r_indices)):
        if r <= r_indices[-1]:
            r_range = len(r_indices)
            break

        if r_indices[i - 1] > r >= r_indices[i]:
            r_range = i
            break

    for i in range(1, len(g_indices)):
        if g <= g_indices[-1]:
            g_range = len(g_indices)
            break

        if g_indices[i - 1] > g >= g_indices[i]:
            g_range =  i
            break

    for i in range(1, len(b_indices)):
        if b <= b_indices[-1]:
            b_range = len(b_indices)
            break

        if b_indices[i - 1] > b >= b_indices[i]:
            b_range =  i
            break

    return r_range, g_range, b_range

if __name__ == "__main__":
    # 生成颜色渐变数组，从浅蓝色到深蓝色
    intervals = [0,0.01, 0.25, 0.50, 1.0, 1.50, 2.0, 2.5,
                3, 3.5, 4, 4.5, 5, 7.5, 10, float('inf')]
    num_segments = len(intervals)-1
    start_color = [149, 208, 238]
    end_color = [10, 9, 145]
    gradient_colors = generate_color_gradient(
        num_segments, start_color, end_color)

    print(len(gradient_colors))
    print(gradient_colors)

    H = 0
    index = get_interval_index(H)
    print(index)
    print("Interval Index gradient_colors:", gradient_colors[index])

 
    
    target_rgb = [0,0,0]
    r_range, g_range, b_range = find_color_indices(target_rgb, gradient_colors)

    print(f"Red Range: {r_range} --->H: {intervals[r_range]}")
    print(f"Green Range: {g_range} --->H: {intervals[b_range]}")
    print(f"Blue Range: {b_range} --->H: {intervals[g_range]}")

    plot_color_gradient(gradient_colors)