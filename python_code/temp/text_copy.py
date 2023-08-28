import pdal
import json

# 构建 PDAL Pipeline
pipeline = {
    "pipeline": [
        {
            "type": "readers.text",
            "filename": "../flood/center1.txt",  # 替换为您的包含真实颜色信息的点云数据文件路径
            "header": "X Y Z",  # 替换为您的点云数据文件中的列名，包括颜色信息
            "separator": ","  # 替换为您的点云数据文件中的分隔符，例如空格或逗号
        },
        {
            "type": "writers.las",
            "filename": "output_point_cloud.las",  # 指定输出的 .LAS 文件路径和名称
            "minor_version": 2,  # 可选，指定 .LAS 文件的版本号
            "a_srs": "EPSG:4326"  # 可选，指定点云数据的坐标系
        }
    ]
}

# 执行 PDAL 转换
pipeline_str = pdal.pipeline.Pipeline(json.dumps(pipeline))
pipeline_str.execute()

print("Conversion to LAS format completed.")
