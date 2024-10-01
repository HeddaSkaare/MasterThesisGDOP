import React,{useState} from 'react';
import { useSetAtom, useAtom } from 'jotai';
import {elevationState, updateDataState,timeState, gnssState, epochState} from '../states/states';

const FilterComponent = () => {
  const [gnssNames, setGnssNames] = useAtom(gnssState);
  const [elevationAngle, setElevationAngle] = useAtom(elevationState)
  const [time, setTime] =useAtom(timeState);
  const [hours, setHours] = useAtom(epochState);
  const setUpdateData = useSetAtom(updateDataState)

  const handleCheckboxChange = (e) => {
    setGnssNames({
      ...gnssNames,
      [e.target.name]: e.target.checked,
    });
  };

  const handleDateChange = (event) => {
    const localTime = event.target.value; // Get the selected local time string
    const utcTime = new Date(localTime + ":00.000Z"); // Append UTC format and create Date object
    setTime(utcTime); // Update state with UTC date
  };

  const handleElevationAngleChange = (e) => {
    setElevationAngle(e.target.value);
  };

  const handleUpdateData = () => {
    setUpdateData(true);
  }
  const handleHourChange = (event) => {
    setHours(event.target.value);
  };


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
        <h4>Time of Day (UTC)</h4>
        <input
          type="datetime-local"
          value={time.toISOString().slice(0, 16)} // Format to yyyy-MM-ddTHH:mm in UTC
          onChange={handleDateChange}
        />
      </div>
      <div>
        <p>Selected Start Time: {time.toUTCString()}</p>
      </div>
      <div>
        <h4>Time Epoch</h4>
        <input
          type="range"
          min="0"
          max="24"
          value={hours}
          onChange={handleHourChange}
        />
        <span>{hours}</span>
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