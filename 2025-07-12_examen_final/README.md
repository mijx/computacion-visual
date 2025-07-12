pasos para crear entorno:
Entrar a carpeta raiz del proyecto
py -3.10 -m venv mediapipe_env
.\mediapipe_env\Scripts\activate

Luego instalar las librerías:
pip install numpy==1.26.4
pip install mediapipe
pip install opencv-python (creo que este ponía problemas...)

Ejecutar no con botn de vs code sino con:
python main.py estando dentro del venv
