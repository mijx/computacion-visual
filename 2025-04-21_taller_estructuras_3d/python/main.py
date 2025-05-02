import trimesh
import open3d as o3d
import numpy as np
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(base_dir, "models", "burger.glb")

# Cargar .glb con trimesh
tmesh = trimesh.load(ruta)

# Si es una escena con múltiples geometrías, unirlas
if isinstance(tmesh, trimesh.Scene):
    tmesh = trimesh.util.concatenate(tuple(tmesh.geometry.values()))

# Convertir a open3d
vertices = np.asarray(tmesh.vertices)
faces = np.asarray(tmesh.faces)

# Información estructural
num_vertices = len(vertices)
num_faces = len(faces)
num_edges = len(tmesh.edges)

# Mostrar la información en la terminal
print(f"Modelo cargado:")
print(f"Número de vértices: {num_vertices}")
print(f"Número de caras: {num_faces}")
print(f"Número de aristas: {num_edges}")

# Crear malla Open3D
mesh_o3d = o3d.geometry.TriangleMesh(
    o3d.utility.Vector3dVector(vertices),
    o3d.utility.Vector3iVector(faces)
)

# Calcular normales para mejor visualización
mesh_o3d.compute_vertex_normals()

# Visualizar
o3d.visualization.draw_geometries([mesh_o3d])
