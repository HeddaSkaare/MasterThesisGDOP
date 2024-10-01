import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2'; // Use 'Bar' instead of 'BoxPlot'
import { useAtomValue } from 'jotai';

// Register the components needed for the Bar Chart
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export const BarChartGraph = ({ data, labels }) => {
  const newLabels = ['10', '9', '11', '8', '7', '6', '6', '7']; // X-axis labels
  const barChartData = {
    labels: newLabels, // X-axis categories
    datasets: [
      {
        label: 'Number of Satellites in View',
        backgroundColor: 'rgba(255, 99, 132, 0.5)', // Bar color
        borderColor: 'rgba(255, 99, 132, 1)', // Bar border color
        borderWidth: 1,
        data: [10, 9, 11, 8, 7, 6, 6, 7], // Y-axis values
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      x: {
        beginAtZero: true,
      },
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div>
      <h4>Bar Chart</h4>
      <Bar data={barChartData} options={options} /> {/* Use the 'Bar' component here */}
    </div>
  );
};


