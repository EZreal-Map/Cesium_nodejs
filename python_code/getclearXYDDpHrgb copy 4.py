import gltf
import json

# Function to read the mesh_1108.2dm file
def read_mesh_file(filename):
    triangle_indices = []
    vertices = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[0] == 'E3T':
                vertex_indices = [int(parts[2]) - 1, int(parts[3]) - 1, int(parts[4]) - 1]
                triangle_indices.append(vertex_indices)
            elif parts[0] == 'ND':
                x = float(parts[2])
                y = float(parts[3])
                z = float(parts[4])
                vertices.append([x, y, z])

    return triangle_indices, vertices

# Replace 'mesh_1108.2dm' with your file path
file_path = 'mesh_1108.2dm'
triangle_indices, vertices = read_mesh_file(file_path)

# Create gltf data
gltf_data = {
    "scenes": [{"nodes": [0]}],
    "nodes": [{"mesh": 0}],
    "meshes": [{"primitives": [{
        "attributes": {"POSITION": vertices},
        "indices": triangle_indices,
        "mode": 4
    }]}],
    "accessors": [
        {"bufferView": 0, "componentType": 5125, "count": len(triangle_indices), "type": "SCALAR"},
        {"bufferView": 1, "componentType": 5126, "count": len(vertices), "type": "VEC3"}
    ],
    "bufferViews": [
        {"buffer": 0, "byteOffset": 0, "byteLength": len(triangle_indices) * 4, "target": 34963},
        {"buffer": 0, "byteOffset": len(triangle_indices) * 4, "byteLength": len(vertices) * 12, "target": 34962}
    ],
    "buffers": [{"byteLength": len(triangle_indices) * 4 + len(vertices) * 12}],
}

with open('complex_topology_model.gltf', 'w') as f:
    json.dump(gltf_data, f)
