import React,{useState} from 'react';
import { useSetAtom, useAtom } from 'jotai';
import {elevationState, updateDataState,timeState, gnssState} from '../states/states';

const FilterComponent = () => {
  const [gnssNames, setGnssNames] = useAtom(gnssState);
  const [elevationAngle, setElevationAngle] = useAtom(elevationState)
  const [time, setTime] =useAtom(timeState);
  const [hours, setHours] = useState(time.getHours()-2);
  const setUpdateData = useSetAtom(updateDataState)

  const handleCheckboxChange = (e) => {
    setGnssNames({
      ...gnssNames,
      [e.target.name]: e.target.checked,
    });
  };

  const handleDateChange = (event) => {
    const selectedDate = event.target.value; // This is the selected date in 'YYYY-MM-DD' format
    const newDate = new Date(selectedDate); // Create a new Date object from the selected date

    // Update only the date part, while keeping the original time (hours, minutes, seconds)
    newDate.setHours(time.getHours(), time.getMinutes(), time.getSeconds(), time.getMilliseconds());

    setTime(newDate); // Update the state with the new date and original time
  };

  const handleElevationAngleChange = (e) => {
    setElevationAngle(e.target.value);
  };

  const handleUpdateData = () => {
    setUpdateData(true);
  }
  const handleHourChange = (event) => {
    const newHours = parseInt(event.target.value, 10); // Get the new hours value from the slider
    const updatedTime = new Date(time); // Clone the current time

    // Update the hours while keeping the date and minutes/seconds/milliseconds intact
    updatedTime.setHours(newHours);

    setHours(newHours-2); // Update the hours state
    setTime(updatedTime); // Update the full Date object
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
        <h4>Time of day</h4>
        <input
          type="date"
          value={time.toISOString().slice(0, 10)}
          onChange={handleDateChange}
        />
      </div>
      <div>
        <p>Selected Start Time: {time.toUTCString()}</p>
      </div>
      <div>
        <h4>Hours</h4>
        <input
          type="range"
          min="0"
          max="23"
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