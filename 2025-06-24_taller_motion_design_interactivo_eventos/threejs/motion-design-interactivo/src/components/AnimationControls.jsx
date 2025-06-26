import React from 'react';

const AnimationControls = ({ changeAnimation }) => {
  return (
    <div style={{ position: 'absolute', top: '10px', left: '10px', zIndex: 10 }}>
      <button onClick={() => changeAnimation('Saludo')}>Saludo</button>
      <button onClick={() => changeAnimation('Idle')}>Idle</button>
      <button onClick={() => changeAnimation('Run')}>Run</button>
      <button onClick={() => changeAnimation('Jump')}>Jump</button>
    </div>
  );
};

export default AnimationControls;
