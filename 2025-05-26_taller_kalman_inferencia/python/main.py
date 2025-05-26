# Ejemplo de estructura básica
import numpy as np
import matplotlib.pyplot as plt

# Generar datos simulados
real = np.cumsum(np.random.randn(50))           # Posición real
noise = np.random.normal(0, 2, size=50)
observed = real + noise                         # Medición ruidosa

# Inicialización del filtro
estimate = []
P = 1
x_hat = 0
Q = 0.001   # Ruido del proceso
R = 4       # Ruido de medición

for z in observed:
    # Predicción
    x_hat_prior = x_hat
    P_prior = P + Q

    # Corrección
    K = P_prior / (P_prior + R)
    x_hat = x_hat_prior + K * (z - x_hat_prior)
    P = (1 - K) * P_prior
    estimate.append(x_hat)

# Visualización
plt.plot(real, label='Real')
plt.plot(observed, label='Medido')
plt.plot(estimate, label='Kalman')
plt.legend()
plt.show()
