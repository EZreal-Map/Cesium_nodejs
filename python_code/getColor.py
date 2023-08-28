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

    H = 0
    index = get_interval_index(H)
    print(index)
    print("Interval Index gradient_colors:", gradient_colors[index])