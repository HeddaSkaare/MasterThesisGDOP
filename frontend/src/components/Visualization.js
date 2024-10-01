import { Canvas } from '@react-three/fiber';
import { Html, OrbitControls } from '@react-three/drei';
import React, { useEffect, useState } from 'react';
import { useAtom, useAtomValue } from 'jotai'
import {elevationState, updateDataState,timeState, gnssState, epochState} from '../states/states';
import { SatelliteMap } from './SkyPlot';
import '../css/visualization.css';
import { BarChartGraph } from './BoxPlot';
import { LineGraph } from './LinePlot';

const gps = {
  G: 'GPS',
  R: 'GLONASS',
  E: 'Galileo',
  C: 'BeiDou',
  J: 'QZSS',
  I: 'IRNSS',
  S: 'SBAS',
};


// Main visualization component
const Visualization = ({ }) => {
    const [satellites,setSatellites] = useState([])
    const [loading,setLoading] = useState(true)
    const [error, setError] = useState('')
    const [updateData,setUpdateData] = useAtom(updateDataState);
    const gnssNames = useAtomValue(gnssState);
    const elevationAngle = useAtomValue(elevationState);
    const time =useAtomValue(timeState);
    const epoch = useAtomValue(epochState);
    const labels = [];

    //const [initialLoad,setInitialLoad] = useState(true);
    const [DOP, setDOP] = useState([[0,0,0]]);

    // const [subset, setSubset] = useState([]);
    // useEffect(() => {
    //   setLoading(true);
    //   if(initialLoad){
    //     fetch('http://127.0.0.1:5000/initialize', {
    //       headers: {
    //         'Accept': 'application/json',
    //         'Content-Type': 'application/json'
    //       },
    //       method: "GET",
    //     })
    //     .then(response => {
    //       if (!response.ok) {
    //         throw new Error('Network response was not ok');
    //       }
    //       return response.json(); 
    //     })
    //     .then(data => {
    //       console.log("initial",data)
    //       setSatellites(data.data);
    //       setInitialLoad(false); 
    //       setLoading(false);  
    //     })
    //     .catch(error => {
    //       console.error('There was a problem with the fetch operation:', error);
    //       setLoading(false);
    //     });
    //   }
    // },[initialLoad]);
    useEffect(() => {
      setLoading(true);
    
      const filteredGNSS = Object.keys(gnssNames).filter((key) => gnssNames[key]);
      //const endTime = new Date(time.getTime() - (1 * 60 * 60 * 1000));//sets the end time to 2 hours after the start time
    
      fetch('http://127.0.0.1:5000/satellites', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({
          time: time.toISOString(),
          elevationAngle: elevationAngle.toString(),
          epoch: epoch.toString(),
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
        console.log("updated",data)
        setSatellites(data.satellites);
        setDOP(data.DOP);
        setUpdateData(false);  
        setLoading(false);  
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        setLoading(false);
      });

      for (let i = 0; i < 2*4; i++) {
        const currentTime = new Date(time.getTime() + i* 30 * 60 * 1000); 
        labels.push(currentTime.toISOString().slice(11, 16)); 
      }
    }, [updateData]);
    
  if (loading) {
    return <p>Loading data...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <>
    <div style={{ width: '1200px', height: '700px' }}>
      <Canvas camera={{ position: [0, 0, 10], fov: 45 }}>
        <SatelliteMap satellites={satellites} />
      </Canvas>
    </div>
    <div className="satellite-table">
      {satellites.map((satellite, index) => {
        const satNumbers = Object.keys(satellite.Satelitenumber);
        const label = satellite.Satelitenumber[0][0];
        return (
          <div key={index} className="satellite-column">
            <div className="satellite-name">{gps[label]}</div>
            {satNumbers.map((key) => {
              const satName = satellite.Satelitenumber[key];
              return (
                <div key={key} className="satellite-number">
                  <p>{satName}</p>
                </div>)
            })}
          </div>
        )
      })}
    </div>
    <BarChartGraph data={satellites} labels={labels}/>
    <LineGraph data={satellites} labels={labels}/>
    </>
  );
};

export default Visualization;
