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

print(f"Modelo cargado:")
print(f"Número de vértices: {num_vertices}")
print(f"Número de caras: {num_faces}")
print(f"Número de aristas: {num_edges}")

# Crear malla Open3D
mesh_o3d = o3d.geometry.TriangleMesh(
    o3d.utility.Vector3dVector(vertices),
    o3d.utility.Vector3iVector(faces)
)

# Asignar color por defecto a las caras (rojo)
mesh_o3d.paint_uniform_color([1.0, 0.0, 0.0])  # Color rojo para todas las caras

# Si el modelo tiene colores de vértices, asignarlos
if hasattr(tmesh.visual, 'vertex_colors') and tmesh.visual.vertex_colors is not None:
    vertex_colors = np.asarray(tmesh.visual.vertex_colors)[:, :3] / 255.0  # Normalizar a [0, 1]
else:
    # Si no tiene colores de vértices, asignar un color por defecto (blanco)
    vertex_colors = np.ones_like(vertices)  # Asignar color blanco

# Asignar colores de vértices a la malla
mesh_o3d.vertex_colors = o3d.utility.Vector3dVector(vertex_colors)

# Colores de aristas: crear y asignar color azul
edges = tmesh.edges  # Obtenemos las aristas
edge_lines = []
for edge in edges:
    # Dibujamos aristas como líneas
    p1 = vertices[edge[0]]
    p2 = vertices[edge[1]]
    edge_lines.append([p1, p2])
edge_lines = np.array(edge_lines)

# Crear un objeto de líneas con los colores de las aristas
line_set = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(edge_lines.reshape(-1, 3)),
    lines=o3d.utility.Vector2iVector([[i, i + 1] for i in range(0, len(edge_lines)*2, 2)]), 
)
line_set.colors = o3d.utility.Vector3dVector([[0, 0, 1] for _ in range(len(edge_lines))])  # Azul para las aristas

# Visualizar la malla 3D con vértices, caras y aristas
o3d.visualization.draw_geometries([mesh_o3d, line_set])
