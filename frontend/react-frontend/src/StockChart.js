import React, { useState, useEffect } from 'react';
import axios from 'axios';

function StockChart() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    // Fetch data from API
    axios.get('http://127.0.0.1:8000/api/stock-data/?company=AAPL')
      .then(response => {
        console.log('API Response:', response);  // Log the full response
        setData(response.data.results);
      })
      .catch(error => {
        console.error('Error fetching stock data:', error.response ? error.response.data : error.message);
      });
  }, []);
234
  return (
    <div>
      <h2>Stock Prices</h2>
      <ul>
        {data.length === 0 ? (
          <p>Loading...</p>
        ) : (
          data.map(item => (
            <li key={item.id}>
              {item.date}: ${item.close_price}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}

export default StockChart;
