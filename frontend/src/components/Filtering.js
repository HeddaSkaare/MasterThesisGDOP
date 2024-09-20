import React from 'react';
import { useSetAtom, useAtom } from 'jotai';
import {elevationState, updateDataState,timeState, gnssState} from '../states/states';

const FilterComponent = () => {
  const [gnssNames, setGnssNames] = useAtom(gnssState);
  const [elevationAngle, setElevationAngle] = useAtom(elevationState)
  const [time, setTime] =useAtom(timeState)
  const setUpdateData = useSetAtom(updateDataState)

  const handleCheckboxChange = (e) => {
    setGnssNames({
      ...gnssNames,
      [e.target.name]: e.target.checked,
    });
  };

  const handleTimeChange = (e) => {
    setTime(new Date(e.target.value));
  };

  const handleElevationAngleChange = (e) => {
    setElevationAngle(e.target.value);
  };

  const handleUpdateData = () => {
    setUpdateData(true);
  }


  return (
    <div>
      <h3>Filter Options</h3>
      <div>
        <h4>GNSS Names</h4>
        {Object.keys(gnssNames).map((name) => (
          <label key={name}>
            <input
              type="checkbox"
              name={name}
              checked={gnssNames[name]}
              onChange={handleCheckboxChange}
            />
            {name}
          </label>
        ))}
      </div>
      <div>
        <h4>Time of day</h4>
        <input
          type="datetime-local"
          value={time.toISOString().slice(0, 16)}
          onChange={handleTimeChange}
        />
      </div>
      <div>
        <p>Selected Start Time: {time.toLocaleString()}</p>
      </div>
      <div>
        <h4>Elevation Angle</h4>
        <input
          type="range"
          min="10"
          max="90"
          value={elevationAngle}
          onChange={handleElevationAngleChange}
        />
        <span>{elevationAngle}°</span>
      </div>
      <div>
        <button onClick={handleUpdateData}>Update Data</button>
      </div>
    </div>
  );
};

export default FilterComponent;