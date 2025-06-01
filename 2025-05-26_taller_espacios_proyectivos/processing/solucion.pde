boolean usePerspective = true; // Control para cambiar cámara

void setup() {
    size(600, 600, P3D);
    noStroke();
}

void draw() {
    background(30);

    // Cambiar cámara
    if (usePerspective) {
        perspective();
    } else {
        ortho();
    }

    // Centramos el sistema de coordenadas
    translate(width / 2, height / 2, 0);

    // Rotamos lentamente para visualizar 3D
    rotateY(frameCount * 0.01);
    rotateX(frameCount * 0.005);

    // Dibujar varios objetos con distinta profundidad (eje Z)

    // Cubo rojo
    pushMatrix();
    translate(-100, 0, -150);
    fill(200, 50, 50);
    box(80);
    popMatrix();

    // Esfera verde
    pushMatrix();
    translate(100, 0, 0);
    fill(50, 200, 50);
    sphere(50);
    popMatrix();

    // Toro azul
    pushMatrix();
    translate(0, 100, 150);
    fill(50, 50, 200);
    torus(40, 15);
    popMatrix();

    // Texto indicador
    fill(255);
    textSize(18);
    textAlign(LEFT, TOP);
    text("Cámara: " + (usePerspective ? "Perspectiva" : "Ortográfica"), -width / 2 + 10, -height / 2 + 10);
    text("Presiona ESPACIO para cambiar cámara", -width / 2 + 10, -height / 2 + 35);
}

// Función para dibujar toro, ya que Processing no la tiene nativa
void torus(float r1, float r2) {
    int sides = 30;
    int rings = 30;
    for (int i = 0; i < sides; i++) {
        float theta1 = TWO_PI * i / sides;
        float theta2 = TWO_PI * (i + 1) / sides;
        beginShape(QUAD_STRIP);
        for (int j = 0; j <= rings; j++) {
            float phi = TWO_PI * j / rings;
            float x1 = (r1 + r2 * cos(phi)) * cos(theta1);
            float y1 = (r1 + r2 * cos(phi)) * sin(theta1);
            float z1 = r2 * sin(phi);

            float x2 = (r1 + r2 * cos(phi)) * cos(theta2);
            float y2 = (r1 + r2 * cos(phi)) * sin(theta2);
            float z2 = r2 * sin(phi);

            vertex(x1, y1, z1);
            vertex(x2, y2, z2);
        }
        endShape();
    }
}

void keyPressed() {
    if (key == ' ') {
        usePerspective = !usePerspective;
    }
}
