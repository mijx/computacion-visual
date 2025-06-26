# -*- coding: utf-8 -*-
"""
Entrenamiento completo de un modelo de Deep Learning sobre MNIST
Incluye: carga, visualización, entrenamiento, validación, fine-tuning y guardado de resultados.
"""
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold
import seaborn as sns
import pandas as pd

# Configuración de directorios
# Obtener la ruta del directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construir rutas a las carpetas 'modelos' y 'resultados'
modelos_dir = os.path.join(script_dir, "..", "modelos")
resultados_dir = os.path.join(script_dir, "..", "resultados")
data_dir = os.path.join(script_dir, "..", "data")

# Crear directorios si no existen
os.makedirs(modelos_dir, exist_ok=True)
os.makedirs(resultados_dir, exist_ok=True)

# 1. Cargar y visualizar el dataset
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
train_data = datasets.MNIST(root=data_dir, train=True, download=True, transform=transform)
test_data = datasets.MNIST(root=data_dir, train=False, download=True, transform=transform)

# Visualización de un ejemplo
def visualizar_ejemplo(dataset):
    image, label = dataset[0]
    plt.imshow(image.squeeze(), cmap="gray")
    plt.title(f"Etiqueta: {label}")
    plt.savefig(os.path.join(resultados_dir, "ejemplo_mnist.png"))
    plt.close()
visualizar_ejemplo(train_data)

# 2. Preparar los dataloaders
train_size = int(0.8 * len(train_data))
val_size = len(train_data) - train_size
train_subset, val_subset = random_split(train_data, [train_size, val_size])
batch_size = 64
train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_subset, batch_size=batch_size)
test_loader = DataLoader(test_data, batch_size=batch_size)

# 3. Definir el modelo simple
class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 10)
        )
    def forward(self, x):
        return self.net(x)

# 4. Configurar función de pérdida y optimizador
def entrenar_modelo(model, train_loader, val_loader, epochs=10, lr=0.001, device="cpu"):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    train_losses, val_losses, val_accuracies = [], [], []
    for epoch in range(epochs):
        model.train()
        running_loss = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            output = model(images)
            loss = criterion(output, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        train_losses.append(running_loss / len(train_loader))
        # Validación
        model.eval()
        val_loss = 0
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                output = model(images)
                val_loss += criterion(output, labels).item()
                _, predicted = torch.max(output.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        val_losses.append(val_loss / len(val_loader))
        accuracy = correct / total
        val_accuracies.append(accuracy)
        print(f"Epoch {epoch+1}/{epochs}, Train Loss: {train_losses[-1]:.4f}, Val Loss: {val_losses[-1]:.4f}, Val Accuracy: {accuracy:.4f}")
    return train_losses, val_losses, val_accuracies

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNN().to(device)
train_losses, val_losses, val_accuracies = entrenar_modelo(model, train_loader, val_loader, epochs=10, device=device)

# Guardar curvas de pérdida
plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Val Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.title("Curva de pérdida")
plt.savefig(os.path.join(resultados_dir, "curva_loss.png"))
plt.close()

# 5. Evaluación en test y matriz de confusión
def evaluar_modelo(model, loader, device):
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            output = model(images)
            _, preds = torch.max(output, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())
    return np.array(all_labels), np.array(all_preds)

y_test, y_pred = evaluar_modelo(model, test_loader, device)
print(classification_report(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Matriz de confusión (modelo simple)")
plt.savefig(os.path.join(resultados_dir, "confusion_matrix.png"))
plt.close()

# 6. K-Fold Cross Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
X = torch.stack([train_data[i][0] for i in range(len(train_data))])
y = torch.tensor([train_data[i][1] for i in range(len(train_data))])
kfold_metrics = []
for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
    print(f"Fold {fold+1}")
    train_subset = torch.utils.data.Subset(train_data, train_idx)
    val_subset = torch.utils.data.Subset(train_data, val_idx)
    train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_subset, batch_size=batch_size)
    model = SimpleNN().to(device)
    _, _, val_accuracies = entrenar_modelo(model, train_loader, val_loader, epochs=5, device=device)
    kfold_metrics.append(val_accuracies[-1])
print("Accuracies por fold:", kfold_metrics)

# 7. Fine-Tuning con modelo preentrenado
model_ft = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
for param in model_ft.parameters():
    param.requires_grad = False
model_ft.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, 10)
model_ft = model_ft.to(device)
optimizer_ft = optim.Adam(model_ft.fc.parameters(), lr=1e-4)
criterion_ft = nn.CrossEntropyLoss()

# Entrenamiento solo de la capa final
ft_train_losses, ft_val_losses, ft_val_accuracies = [], [], []
for epoch in range(5):
    model_ft.train()
    running_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer_ft.zero_grad()
        output = model_ft(images)
        loss = criterion_ft(output, labels)
        loss.backward()
        optimizer_ft.step()
        running_loss += loss.item()
    ft_train_losses.append(running_loss / len(train_loader))
    # Validación
    model_ft.eval()
    val_loss = 0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            output = model_ft(images)
            val_loss += criterion_ft(output, labels).item()
            _, predicted = torch.max(output.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    ft_val_losses.append(val_loss / len(val_loader))
    accuracy = correct / total
    ft_val_accuracies.append(accuracy)
    print(f"[Fine-tuning] Epoch {epoch+1}/5, Train Loss: {ft_train_losses[-1]:.4f}, Val Loss: {ft_val_losses[-1]:.4f}, Val Accuracy: {accuracy:.4f}")

# Evaluación fine-tuning
y_test_ft, y_pred_ft = evaluar_modelo(model_ft, test_loader, device)
print("[Fine-tuning]", classification_report(y_test_ft, y_pred_ft))

# 8. Guardar modelo final y comparación de métricas
torch.save(model_ft.state_dict(), os.path.join(modelos_dir, "modelo_final.pth"))

# Comparación de métricas
metrics = {
    "Modelo": ["SimpleNN", "ResNet18 (fine-tuning)"],
    "Accuracy": [np.mean(kfold_metrics), np.mean(ft_val_accuracies)],
    "Precision": [
        classification_report(y_test, y_pred, output_dict=True)["weighted avg"]["precision"],
        classification_report(y_test_ft, y_pred_ft, output_dict=True)["weighted avg"]["precision"]
    ],
    "Recall": [
        classification_report(y_test, y_pred, output_dict=True)["weighted avg"]["recall"],
        classification_report(y_test_ft, y_pred_ft, output_dict=True)["weighted avg"]["recall"]
    ]
}
df_metrics = pd.DataFrame(metrics)
df_metrics.to_csv(os.path.join(resultados_dir, "comparacion_metrics.csv"), index=False)

print("Taller completado. Resultados y modelo guardados en la carpeta correspondiente.") 