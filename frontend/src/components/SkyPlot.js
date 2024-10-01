import React from 'react';
import { Html,Line } from '@react-three/drei';
import { Satellite } from './Satellite';

function sphericalToCartesian2D(r, azimuth, zenith, center) {
  // Convert to radians
  azimuth = (azimuth * Math.PI) / 180;
  zenith = (zenith * Math.PI) / 180;
  
  // Calculate X and Y based on 2D plane
  const x = r * Math.sin(zenith) * Math.cos(azimuth) + center[0];
  const y = r * Math.sin(zenith) * Math.sin(azimuth) + center[1];
  
  return [x, y];
}
const CircleOutline = ({ radius, position }) => {
    const points = [];
    // Create points along the circumference of a circle
    for (let i = 0; i <= 64; i++) {
      const angle = (i / 64) * Math.PI * 2;
      points.push([Math.cos(angle) * radius, Math.sin(angle) * radius, 0]);
    }

    return (
    <><mesh position={position} rotation={[-Math.PI / 2, 0, 0]}>
        {/* Create the circular geometry */}
        <ringGeometry args={[radius - 0.05, radius, 64]} />

        <meshBasicMaterial color="white" side={2} />
    </mesh>
    <Line
            points={points} // Array of [x, y, z] points
            color="black"
            lineWidth={2} // Optional: Adjust line thickness
            position={position}
            rotation={[-Math.PI / 2, 0, 0]} /></>
  );
};

export const SatelliteMap = ({satellites}) => {
  const center = [0, 0];
  const radius = 3;

  return (
    <>
      {/* Render 2D Circle */}
        <CircleOutline radius={radius} position={[0, 0, 0]} />

      {/* Render Satellites */}
      {satellites.map((satellite, index) => {
        const satNumbers = Object.keys(satellite.Satelitenumber);
        return satNumbers.map((key) => {
            const satName = satellite.Satelitenumber[key];
            const azimuth = satellite.azimuth[key];
            const zenith = satellite.zenith[key];
            const [x, y] = sphericalToCartesian2D(radius, azimuth, zenith, center);
            return <Satellite key={index} position={[x, y, 0]} label={satName} />;
        });
      })}

      {/* Render Your Position */}
      <mesh position={[0, 0, 0]}>
        <circleGeometry args={[0.2, 32]} />
        <meshBasicMaterial color="black" />
        <Html distanceFactor={10}>
          <div style={{ color: 'white', background: 'black', padding: '2px' }}>Your position</div>
        </Html>
      </mesh>
    </>
  );
};

