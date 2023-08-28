import laspy

# 读取文本文件数据
input_file = "../flood/30jiami/0/center.txt"
data = []
with open(input_file, "r") as f:
    for line in f:
        x, y, z, _ = map(float, line.strip().split(','))
        data.append((x, y, z))

# 创建LAS文件
out_las_file = "laspy.las"
out_las = laspy.create(point_format=0)
out_las.x = [point[0] for point in data]
out_las.y = [point[1] for point in data]
out_las.z = [point[2] for point in data]

# 设置LAS文件头信息（根据需要调整）
# 设置LAS文件头信息，包括空间参考信息
out_las.header.min = [min(out_las.x), min(out_las.y), min(out_las.z)]
out_las.header.max = [max(out_las.x), max(out_las.y), max(out_las.z)]

# 设置LAS文件的坐标系为WGS 84地理坐标系（EPSG:4326）
# out_las.header.proj4 = '+proj=longlat +datum=WGS84 +no_defs'

# 写入并保存LAS文件
out_las.write(out_las_file)

print("转换完成！")
