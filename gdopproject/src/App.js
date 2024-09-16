import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
    const [value, setValue] = useState(null);

    useEffect(() => {
        axios.get('/api/get_value')
            .then(response => {
                setValue(response.data.value);
            })
            .catch(error => {
                console.error("There was an error fetching the data!", error);
            });
    }, []);

    return (
        <div>
            <h1>Model Output: {value}</h1>
        </div>
    );
}

export default App;