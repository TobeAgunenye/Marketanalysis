import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Legend, Brush } from 'recharts';
import { Row, Col, Card, Spinner } from 'react-bootstrap';
import SentimentCard from './Sentimentcard';  // Import SentimentCard to display sentiment data

const StockDetail = () => {
  const { company } = useParams();
  const [stockDetail, setStockDetail] = useState([]);
  const [predictions, setPredictions] = useState([]);  // Define state for predictions
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);



  const allDataRef = useRef([]);
  const currentIndexRef = useRef(0);

  useEffect(() => {
    let interval;
  
    const fetchAllData = async () => {
      try {
        const stockResponse = await axios.get(`http://127.0.0.1:8000/api/stock-simulation/?company=${company}&start_date=2019-01-02&limit=9999`);
        allDataRef.current = stockResponse.data.results;
        console.log("Total days received:", allDataRef.current.length);
  
        if (allDataRef.current.length > 0) {
          setStockDetail([allDataRef.current[0]]);
        }
  
        const predictionResponse = await axios.get(`http://127.0.0.1:8000/api/market-predictions/${company}/`);
        const formattedPredictions = predictionResponse.data.results.map(prediction => ({
          ...prediction,
          prediction_date: new Date(prediction.prediction_date).toISOString().split('T')[0]
        }));
        setPredictions(formattedPredictions);
  
        setLoading(false);
  
        interval = setInterval(() => {
          const index = currentIndexRef.current;
          const data = allDataRef.current;
        
          if (index < data.length) {
            const nextDay = data[index];
            setStockDetail(prev => {
              const updated = [...prev, nextDay];
              return updated.slice(-10);
            });
        
            currentIndexRef.current += 1; // ✅ move outside setStockDetail
          } else {
            clearInterval(interval);
          }
        }, 5000);


      } catch (err) {
        setError('Failed to fetch data. Please try again later.');
        setLoading(false);
      }
    };
  
    fetchAllData();
  
    return () => clearInterval(interval);
  }, [company]);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const color = payload[0].dataKey === 'predicted_price' ? '#82ca9d' : '#1e90ff'; // Green for predicted price
      return (
        <div className="custom-tooltip" style={{ borderColor: color }}>
          <p className="label">{`${new Date(label).toISOString().split('T')[0]}`}</p>
          <p className="intro" style={{ color: color }}>{`Price: ${payload[0].value}`}</p>
        </div>
      );
    }
  
    return null;
  };

  
  // ✅ Handle loading state
  if (loading) {
    return (
      <div className="text-center my-5">
        <Spinner animation="border" variant="primary" />
        <p>Loading {company} stock data...</p>
      </div>
    );
  }

  // ✅ Handle error state
  if (error) {
    return <div className="alert alert-danger text-center">{error}</div>;
  }

  return (
    <div className="container mt-5 pt-5">
      <h1 className="mb-4 text-center text-primary">
        {company} Stock Details
      </h1>

      {/* Sentiment Analysis Section - placed on top */}
      <SentimentCard company={company} />  {/* Sentiment analysis displayed on top */}

<Row className="mb-4">
  {/* 🌟 Full-width Close Price */}
  <Col xs={12}>
    <Card className="shadow border-0 mb-4">
      <Card.Body>
        <h5 className="text-center mb-3">📈 Close Price</h5>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={stockDetail}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis dataKey="date" stroke="#555" />
            <YAxis stroke="#555" />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="close_price"
              stroke="#1e90ff"
              strokeWidth={2}
              dot={{ r: 3 }}
              activeDot={{ r: 6 }}
            />
            <Brush dataKey="date" height={30} stroke="#1e90ff" />
          </LineChart>
        </ResponsiveContainer>
      </Card.Body>
    </Card>
  </Col>

  {/* 🔮 Predictions + 4 mini charts side by side */}
  <Col xs={12}>
    <Row>
      {/* Predictions */}
      <Col md={6}>
        <Card className="shadow border-0 mb-4 h-100">
          <Card.Body>
            <h5 className="text-center mb-3">📉 Next Years Predictions</h5>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={predictions}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="prediction_date"
                  tickFormatter={(value) => new Date(value).toISOString().split('T')[0]}
                />
                <YAxis />
                <Tooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="predicted_price" stroke="#82ca9d" />
                <Brush dataKey="prediction_date" height={30} stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </Card.Body>
        </Card>
      </Col>

      {/* Mini Charts */}
      <Col md={6}>
        <h6 className="text-center text-uppercase mt-2 mb-3" style={{ fontWeight: '600', color: '#2c3e50' }}>
          📊 Today's Prices
        </h6>
        <Row>
          {[
            { title: '🔵 Open', key: 'open_price', color: '#ff6f61' },
            { title: '🟢 High', key: 'high_price', color: '#32a852' },
            { title: '🟠 Low', key: 'low_price', color: '#f39c12' },
            { title: '🔴 Volume', key: 'volume', color: '#c0392b' },
          ].map(({ title, key, color }) => (
            <Col md={6} key={key}>
              <Card className="shadow border-0 mb-4">
                <Card.Body>
                  <h6 className="text-center mb-2">{title}</h6>
                  <ResponsiveContainer width="100%" height={120}>
                    <LineChart data={stockDetail}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" hide />
                      <YAxis hide />
                      <Tooltip />
                      <Line
                        type="monotone"
                        dataKey={key}
                        stroke={color}
                        strokeWidth={2}
                        dot={{ r: 1 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Col>
    </Row>
  </Col>
</Row>
    </div>
  );
};

export default StockDetail;