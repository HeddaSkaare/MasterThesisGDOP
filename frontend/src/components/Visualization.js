import { Canvas } from '@react-three/fiber';
import { Html, OrbitControls } from '@react-three/drei';
import React, { useEffect, useState } from 'react';
import { useAtom, useAtomValue } from 'jotai'
import {elevationState, updateDataState,timeState, gnssState} from '../states/states';


// Satellite component rendering a satellite sphere with label
const Satellite = ({ name, position }) => (
  <mesh position={position}>
    <sphereGeometry args={[0.1, 32, 32]} />
    <meshStandardMaterial color="red" />
    <Html distanceFactor={10}>
      <div style={{ color: 'white', background: 'black', padding: '2px' }}>{name}</div>
    </Html>
  </mesh>
);

function sphericalToCartesian(r, azimuth, zenith, center) {
    azimuth = azimuth * Math.PI / 180;
    zenith = zenith * Math.PI / 180;
    const x = r * Math.sin(zenith) * Math.cos(azimuth) + center[0];
    const y = r * Math.sin(zenith) * Math.sin(azimuth) + center[1];
    const z = r * Math.cos(zenith) + center[2];

    const theta = -Math.PI / 2;  // Rotation angle (-π/2 radians)
    const yRotated = y * Math.cos(theta) - z * Math.sin(theta);
    const zRotated = y * Math.sin(theta) + z * Math.cos(theta);
    return [x, yRotated, zRotated];
}


// HalfSphere component to render the half sphere in 3D space
const HalfSphere = () => (
    <>
    
        <mesh position={[0, -3.33, 0]} rotation={[-Math.PI/2, 0, 0]}> 
            <sphereGeometry args={[6, 32, 32, 0, Math.PI]} />
            <meshStandardMaterial color="blue" wireframe />
        </mesh>
        <mesh position={[0, -Math.PI-0.4,0 ]}>
            <sphereGeometry args={[0.2, 32, 32]} />
            <meshStandardMaterial color="black" />
            <Html distanceFactor={10}>
            <div style={{ color: 'white', background: 'black', padding: '2px' }}>Your position</div>
            </Html>
        </mesh>
</>
);

// Main visualization component
const Visualization = ({ }) => {
    const [satellites,setSatellites] = useState([])
    const [loading,setLoading] = useState(true)
    const [error, setError] = useState('')
    const [updateData,setUpdateData] = useAtom(updateDataState);
    const gnssNames = useAtomValue(gnssState);
    const elevationAngle = useAtomValue(elevationState);
    const time =useAtomValue(timeState);
    // const [GDOP, setGDOP] = useState(0);
    // const [subset, setSubset] = useState([]);
    
    useEffect(() => {
      setLoading(true);
    
      const filteredGNSS = Object.keys(gnssNames).filter((key) => gnssNames[key]);
      const endTime = new Date(time.getTime() + (2 * 60 * 60 * 1000));//sets the end time to 2 hours after the start time
    
      fetch('http://127.0.0.1:5000/satellites', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({
          startTime: time.toISOString(),
          endTime: endTime.toISOString(),
          elevationAngle: elevationAngle.toString(),
          GNSS: filteredGNSS,
        })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); 
      })
      .then(data => {
        console.log(data)
        setSatellites(data.satellites);
        setUpdateData(false);  
        setLoading(false);  
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        setLoading(false);
      });
    }, [updateData]);
    
  if (loading) {
    return <p>Loading data...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <><div style={{ width: '1500px', height: '500px' }}>
      <Canvas camera={{ position: [0, 0, 10], fov: 75 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <HalfSphere />
        {/* Iterate over the satellites */}
        {satellites.map((satellite, idx) => {
          // Convert dictionary-like structure to arrays using Object.keys
          const satNumbers = Object.keys(satellite.Satelitenumber);
          console.log(satNumbers);
          return satNumbers.map((key) => {
            //console.log(satellite.Satelitenumber[key])
            const satName = satellite.Satelitenumber[key];
            const azimuth = satellite.azimuth[key];
            const zenith = satellite.zenith[key];

            // Assuming sphericalToCartesian is a function to convert azimuth and elevation
            const coordinates = sphericalToCartesian(6, azimuth, zenith, [0, 0, -Math.PI]);

            return <Satellite key={`${idx}-${key}`} name={satName} position={coordinates} />;
          });
        })}
        <OrbitControls />
      </Canvas>
    </div>
    {/* <div>
      <p>GDOP: {GDOP}</p>
      <p>Subset: {subset}</p>
    </div> */}
      </>
  );
};

export default Visualization;
