import React, { useEffect, useRef } from 'react';
import { useLoader } from '@react-three/fiber';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader';
import { TextureLoader } from 'three';  // Cargar la textura

const ModeloOBJ = (props) => {
  // Cargar el archivo .mtl que contiene los materiales
  const mtl = useLoader(MTLLoader, '/modelo.mtl');
  
  // Cargar la textura Diffuse_baseColor.png
  const texture = useLoader(TextureLoader, '/Diffuse_baseColor.png');

  const obj = useLoader(OBJLoader, '/modelo.obj', (loader) => {
    mtl.preload(); // Pre-cargar los materiales
    loader.setMaterials(mtl); // Aplicar materiales desde el archivo .mtl
  });

  const groupRef = useRef();

  useEffect(() => {
    obj.traverse((child) => {
      if (child.isMesh) {
        // Aseguramos de centrar la geometría para que se ajuste a la escena
        child.geometry.center(); 

        // Aplicar la textura al material del modelo
        child.material.map = texture; // Asignamos la textura cargada
        child.material.needsUpdate = true; // Necesario para actualizar el material
        
        // Asegurarnos de que el material esté utilizando una textura y no sea blanco
        child.material.color.set(0xffffff); // Establecer el color base como blanco
        child.material.shininess = 30; // Ajustar brillo si es necesario
        child.material.specular.set(0x111111); // Ajustar el reflejo especular
      }
    });
  }, [obj, texture]);

  return (
    <group ref={groupRef} {...props}>
      <primitive object={obj} />
    </group>
  );
};

export default ModeloOBJ;
