import React from 'react';
import { Canvas } from '@react-three/fiber';
import { Html,Line,CatmullRomLine } from '@react-three/drei';
import { Satellite, SatelliteMovement, colors } from './Satellite';
import { Vector3 } from 'three';
import '../css/skyplot.css';

function sphericalToCartesian2D(r, azimuth, zenith, center) {
  // Convert to radians
  azimuth = (azimuth * Math.PI) / 180;
  zenith = (zenith * Math.PI) / 180;

  // Calculate X and Y based on 2D plane
  const x = r * Math.sin(zenith) * Math.cos(azimuth) + center[0];
  const y = r * Math.sin(zenith) * Math.sin(azimuth) + center[1];

  // Rotate the coordinates 90 degrees to the left (around Z-axis)
  const rotatedX = -y; // Swap and negate the y-coordinate to rotate 90 degrees left
  const rotatedY = x;  // Set the new y-coordinate as the original x

  return [rotatedX, rotatedY];
}

const SatelliteRoute = ({ points, color }) => (
  <Line
    points={points}  
    color={color}  // Line color
    lineWidth={2}  // Width of the line
    dashed={false}  // Optional: use dashed line if desired
  />
);
const CircleOutline = ({ radius, position }) => {
    const points = [];
    // Create points along the circumference of a circle
    for (let i = 0; i <= 100; i++) {
      const angle = (i / 100) * Math.PI * 2;
      points.push([Math.cos(angle) * radius, Math.sin(angle) * radius, 0]);
    }

    return (
    <><mesh position={position} rotation={[0, 0, 0]}>
        {/* Create the circular geometry */}
        <ringGeometry args={[radius - 0.05, radius, 64]} />

        <meshBasicMaterial color="white" side={2} />
    </mesh>
    <Line
            points={points} // Array of [x, y, z] points
            color="black"
            lineWidth={2} // Optional: Adjust line thickness
            position={position}
            rotation={[0, 0, 0]} /></>
  );
};

export const SatelliteMap = ({satellites}) => {
  const center = [0, 0];
  const radius = 4;
  const elevations = [10, 60, 90]; // Example: 30°, 60°, 90° elevations
  const radii = elevations.map(elev => radius * Math.cos((elev * Math.PI) / 180));
  let satellitesGrouped = {};
  satellites.map((satellitesBefore, index) =>
    satellitesBefore.map((satellites, innerIndex) => {
      satellites.satellitesData.map((satellite) => {
        const color = colors[satellite.satName[0]];
        const { azimuth, zenith } = satellite;
        const coords = sphericalToCartesian2D(radius, azimuth, zenith, center);
        if (!satellitesGrouped[satellite.satName]) {
          satellitesGrouped[satellite.satName] = [[coords[0], coords[1], color]];
        }else{
          satellitesGrouped[satellite.satName].push([coords[0], coords[1], color]);
        }
      });
    }))
  console.log(satellitesGrouped);
  return (
    <div className="skyplot-container">
      <Canvas className="skyplot-canvas" camera={{ position: [0, 0, 10], fov: 45 }}>
        <CircleOutline radius={radius} position={[0, 0, 0]} />
        {radii.map((radius, index) => (
          <CircleOutline key={index} radius={radius} position={[0, 0, 0]} />
        ))}
        
        {Object.keys(satellitesGrouped).map((satName) => {
          let color = "white"
          const routePoints = satellitesGrouped[satName].map((satellite) => {
            color = satellite[2]
            return new Vector3(satellite[0], satellite[1], 0);
          })

          return (
            <SatelliteRoute
              key={`2`}
              points={routePoints}
              color={color}
            />
          );
        })}
      {Object.keys(satellitesGrouped).map((satName) => {
          const sattelittes = satellitesGrouped[satName];
          const sat = sattelittes[sattelittes.length - 1];
          return <Satellite key={sat[0]} position={[sat[0], sat[1], 0]} label={satName} />;
        })}
      </Canvas>
    </div>
  );
};

