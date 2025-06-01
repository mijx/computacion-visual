import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

def proyectar_perspectiva(puntos, d=1.0):
    P = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1/d, 0]
    ])
    puntos_hom = np.vstack((puntos, np.ones((1, puntos.shape[1]))))
    proy = P @ puntos_hom
    proy /= proy[-1, :]
    return proy[:-1]

def proyectar_ortogonal(puntos):
    P = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
    ])
    puntos_hom = np.vstack((puntos, np.ones((1, puntos.shape[1]))))
    proy = P @ puntos_hom
    return proy

# Generar puntos 3D - cubo unitario
puntos = np.array([
    [0, 1, 1, 0, 0, 1, 1, 0],  # x
    [0, 0, 1, 1, 0, 0, 1, 1],  # y
    [0, 0, 0, 0, 1, 1, 1, 1]   # z
])

proy_ort = proyectar_ortogonal(puntos)

# Preparar figura
fig, axs = plt.subplots(1, 3, figsize=(18,6))
plt.subplots_adjust(bottom=0.25)

# Gráfico 3D original
ax1 = axs[0]
ax1 = plt.subplot(131, projection='3d')
ax1.scatter(puntos[0], puntos[1], puntos[2], c='r')
for i in range(puntos.shape[1]):
    ax1.text(puntos[0,i], puntos[1,i], puntos[2,i], f'{i}')
ax1.set_title('Puntos 3D originales')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_box_aspect([1,1,1])

# Gráfico ortogonal
ax2 = axs[1]
ax2.scatter(proy_ort[0], proy_ort[1], c='b')
for i in range(proy_ort.shape[1]):
    ax2.text(proy_ort[0,i], proy_ort[1,i], f'{i}')
ax2.set_title('Proyección Ortogonal (XY)')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.axis('equal')

# Gráfico perspectiva (vacío inicialmente)
ax3 = axs[2]
ax3.set_title('Proyección Perspectiva')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.axis('equal')
scat = ax3.scatter([], [], c='g')
texts = [ax3.text(0,0,"") for _ in range(puntos.shape[1])]

# Slider para distancia focal
axcolor = 'lightgoldenrodyellow'
ax_d = plt.axes([0.25, 0.1, 0.5, 0.03], facecolor=axcolor)
slider_d = Slider(ax_d, 'Distancia focal', 0.1, 5.0, valinit=1.0)

def update(val):
    d = slider_d.val
    proy_persp = proyectar_perspectiva(puntos, d)
    
    ax3.clear()  # limpiar gráfico
    
    ax3.set_title('Proyección Perspectiva')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.axis('equal')
    
    ax3.scatter(proy_persp[0], proy_persp[1], c='g')
    for i in range(proy_persp.shape[1]):
        ax3.text(proy_persp[0,i], proy_persp[1,i], str(i))
    
    fig.canvas.draw_idle()

# Inicializar gráfico perspectiva
update(1.0)

slider_d.on_changed(update)

plt.show()
