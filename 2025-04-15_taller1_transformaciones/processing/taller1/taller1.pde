float angle = 0;
float scaleFactor = 1;

void setup() {
  size(800, 600, P3D);
  noFill();
  stroke(0); // Color de borde del cubo
  strokeWeight(2);
}

void draw() {
  background(255); // Fondo blanco

  // Configurar la cámara
  perspective(PI/3.0, float(width) / float(height), 0.1, 1000);

  // Luz direccional
  directionalLight(255, 255, 255, 0, -1, 1); // Luz blanca desde arriba

  // Dibujar el círculo de la traslación del cubo
  pushMatrix(); // Guardar la matriz de transformación actual
  stroke(0, 0, 255); // Color del círculo (azul)
  noFill();
  ellipse(width/2, height/2, 400, 400);
  popMatrix(); // Restaurar la matriz de transformación

  // Movimiento del cubo en círculo
  float x = 200 * cos(angle);
  float y = 200 * sin(angle);
  angle += 0.02;

  // Traslación
  pushMatrix();
  translate(width/2 + x, height/2 + y, 0);

  // Escalado
  scaleFactor = 0.7 + 0.4 * abs(sin(millis() / 1000.0));
  scale(scaleFactor);  // Escalar el cubo

  // Dibujar el cubo
  box(50);

  popMatrix(); // Restaurar la matriz de transformación
}
