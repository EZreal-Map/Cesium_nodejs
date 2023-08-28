import gltflib

def create_gltf_triangle():
    vertices = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.5, 1.0, 0.0]
    ]

    colors = [
        [1.0, 0.0, 0.0, 1.0],  # 红色
        [0.0, 1.0, 0.0, 1.0],  # 绿色
        [0.0, 0.0, 1.0, 1.0]   # 蓝色
    ]

    indices = [
        0, 1, 2
    ]

    model = gltflib.GLTF(
        asset=gltflib.Asset(version='2.0'),
        scenes=[
            gltflib.Scene(nodes=[0])
        ],
        nodes=[
            gltflib.Node(mesh=0)
        ],
        meshes=[
            gltflib.Mesh(
                primitives=[
                    gltflib.Primitive(
                        attributes={
                            'POSITION': 0,
                            'COLOR_0': 1
                        },
                        indices=2,
                        mode=4  # mode=4 表示绘制三角形
                    )
                ]
            )
        ]
    )

    # 创建buffer和buffer views
    buffer = gltflib.Buffer(byteLength=84)
    position_buffer_view = gltflib.BufferView(buffer=0, byteOffset=0, byteLength=36, target=34962)  # 34962 对应 gltf.POSITION (VEC3)
    color_buffer_view = gltflib.BufferView(buffer=0, byteOffset=36, byteLength=48, target=34962)  # 34962 对应 gltf.COLOR_0 (VEC4)
    index_buffer_view = gltflib.BufferView(buffer=0, byteOffset=84, byteLength=12, target=34963)  # 34963 对应 gltf.indices (SCALAR)

    # 将顶点数据写入buffer views
    for i, vertex in enumerate(vertices):
        position_buffer_view.set_float32(i * 12, vertex[0])
        position_buffer_view.set_float32(i * 12 + 4, vertex[1])
        position_buffer_view.set_float32(i * 12 + 8, vertex[2])

    # 将颜色数据写入buffer views
    for i, color in enumerate(colors):
        color_buffer_view.set_float32(i * 16, color[0])
        color_buffer_view.set_float32(i * 16 + 4, color[1])
        color_buffer_view.set_float32(i * 16 + 8, color[2])
        color_buffer_view.set_float32(i * 16 + 12, color[3])

    # 将三角形的索引写入buffer views
    for i, index in enumerate(indices):
        index_buffer_view.set_uint32(i * 4, index)

    model.add_buffer(buffer)
    model.add_buffer_view(position_buffer_view)
    model.add_buffer_view(color_buffer_view)
    model.add_buffer_view(index_buffer_view)

    return model

def save_gltf_file(gltf_model, file_path):
    with open(file_path, 'wb') as f:
        gltf_model.write_binary(f)

if __name__ == "__main__":
    gltf_triangle = create_gltf_triangle()
    save_gltf_file(gltf_triangle, 'triangle.glb')
