
import { Html } from '@react-three/drei';
import React from 'react';

const colors = {
  G: 'blue',
  R: 'green',
  E: 'red',
  C: 'yellow',
  J: 'purple',
  I: 'orange',
    S: 'pink',
};

export const Satellite = ({ position, label }) => (
    <mesh position={position}>
      <circleGeometry args={[0.1, 32]} />
      <meshBasicMaterial color={colors[label[0]]} />
      <Html distanceFactor={5}>
        <div style={{ color: 'black', background: 'white', padding: '2px' }}>{label}</div>
      </Html>
    </mesh>
);