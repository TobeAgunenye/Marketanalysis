import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Button } from 'react-bootstrap';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';
import axios from 'axios';

import HeroSection from '../components/HeroSection';
import SkeletonLoader from '../components/skeletonloader';

const HomePage = () => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const companies = ['AAPL', 'AMZN', 'TSLA', 'GOOG'];
        const stockData = {};

        for (const company of companies) {
          const response = await axios.get(`http://127.0.0.1:8000/api/stock-data/?company=${company}`);
          stockData[company] = response.data.results;
        }

        setData(stockData);
        setLoading(false);
      } catch (err) {
        setError('Failed to load stock data. Please try again.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="container mt-5">
      <HeroSection />

      {error && (
        <div className="alert alert-danger text-center">
          {error}
        </div>
      )}

      <Row>
        {['AAPL', 'AMZN', 'TSLA', 'GOOG'].map(company => (
          <Col md={4} key={company} className="mb-4">
            <Card className="h-100 shadow">
              <div style={{ width: '100%', height: '150px' }}>
                {loading ? (
                  <SkeletonLoader />
                ) : (
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data[company]}>
                      <CartesianGrid stroke="#eee" strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="close_price" stroke="#1e90ff" />
                    </LineChart>
                  </ResponsiveContainer>
                )}
              </div>
              <Card.Body>
                <h5 className="card-title">{company}</h5>
                <p className="card-text">
                  Latest data on {company} stock.
                </p>
                <Button href={`/stock/${company}`} variant="primary">
                  See More
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default HomePage;
