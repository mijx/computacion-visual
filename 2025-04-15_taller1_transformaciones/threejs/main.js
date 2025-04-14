import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );


// Establecer escena
scene.background = new THREE.Color( 0xffffff );


// Crear cubo solo con borde
const geometry = new THREE.BoxGeometry( 1, 1, 1 );
const material = new THREE.MeshLambertMaterial	( { color: 0x006400 } );
const cube = new THREE.Mesh( geometry, material );
scene.add( cube );

// Fuente de luz
const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
dirLight.position.set(0, 3, 0); // En el centro y encima del cubo
dirLight.target = cube; // Apunta hacia el cubo
scene.add(dirLight);
scene.add(dirLight.target);

// Agregar circulo que muestra la traslación del cubo
const circleRadius = 2;
const circleSegments = 64;
const circleGeometry = new THREE.CircleGeometry(circleRadius, circleSegments);
const circleMaterial = new THREE.LineBasicMaterial({ color: 0x0000ff });
const circle = new THREE.LineLoop(circleGeometry, circleMaterial);
scene.add(circle);


// Configurar camara
camera.position.z = 5;

// function animate(){
let angle = 0;
const clock = new THREE.Clock();

function animate(){
    // Traslación
    angle += 0.02;
    cube.position.x = 2 * Math.cos(angle);
    cube.position.y = 2 * Math.sin(angle);

    // Rotación
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    // Escalado
    const scaleFactor = 0.7 + 0.4 * Math.abs(Math.sin(clock.getElapsedTime()));
    cube.scale.set(scaleFactor, scaleFactor, scaleFactor);
    
    renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);