import React from 'react';
import { Container, Button } from 'react-bootstrap';

const HeroSection = () => (
  <div className="hero-section mb-5">
    <Container className="text-center">
      <h1 className="display-4">📈 Stock Dashboard</h1>
      <p className="lead mt-2">
        Your go-to portal for market insights.
      </p>
      <hr className="my-4" />
      <p>
        Stay updated with real-time stock performance and trends.
      </p>
      <Button variant="outline-info" size="lg" href="/about">
        Learn More
      </Button>
    </Container>
  </div>
);

export default HeroSection;
