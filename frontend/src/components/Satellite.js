
import { Html } from '@react-three/drei';
import React from 'react';



export const colors = {
  G: '#1E90FF',  // Dodger Blue
  R: '#32CD32',  // Lime Green
  E: '#FF6347',  // Tomato Red
  C: '#FFD700',  // Gold
  J: '#6A5ACD',  // Slate Blue
  I: '#FF8C00',  // Dark Orange
  S: '#FF1493',  // Deep Pink
};

export const Satellite = ({ position, label }) => (
    <mesh position={position}>
      <circleGeometry args={[0.07, 32]} />
      <meshBasicMaterial color={colors[label[0]]} />
      <Html distanceFactor={5}>
        <div style={{ color: 'black', background: 'white', padding: '2px' }}>{label}</div>
      </Html>
    </mesh>
);

// Component for the interpolated satellite route


export const SatelliteMovement = ({ position, label }) => (
  <mesh position={position}>
    <circleGeometry args={[0.07, 32]} />
    <meshBasicMaterial color={colors[label[0]]} />
  </mesh>
);