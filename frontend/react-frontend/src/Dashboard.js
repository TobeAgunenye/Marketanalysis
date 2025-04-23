import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';  // For linking to the stock detail page
import { Card, Row, Col } from 'react-bootstrap';  // For layout
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';  // For charting
import axios from 'axios';

const Dashboard = () => {
  const [data, setData] = useState({
    AAPL: [],
    AMZN: [],
    TSLA: [],
    GOOG: []
  });

  // Fetch stock data when the component mounts

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-5">Stock Dashboard</h1>
      <Row className="justify-content-center">
        {['AAPL', 'AMZN', 'TSLA', 'GOOG'].map(company => (
          <Col md={3} key={company} className="mb-4">
            <Link to={`/stock/${company}`} className="text-decoration-none">
              <Card>
                <Card.Body>
                  <Card.Title className="text-center">{company}</Card.Title>
                  <ResponsiveContainer width="100%" height={200}>
                    <LineChart data={data[company]}>
                      <CartesianGrid stroke="#ccc" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="close_price" stroke="#1e90ff" />
                    </LineChart>
                  </ResponsiveContainer>
                </Card.Body>
              </Card>
            </Link>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default Dashboard;
