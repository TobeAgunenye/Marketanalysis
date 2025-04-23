import React, { useEffect, useState } from 'react';
import '../index.css'; // <-- We'll write styles here or inject into your index.css

const About = () => {
  const [show, setShow] = useState(false);

  useEffect(() => {
    setTimeout(() => setShow(true), 300);
  }, []);

  return (
    <div className={`about-wrapper fade-card ${show ? 'show' : ''}`}>
      <div className="section-header">
        <h1>About Our Application</h1>
        <p className="tagline">
          Empowering SMEs and individual investors with smart, AI-powered financial forecasting tools.
        </p>
      </div>

      <section>
        <h2> What We Do</h2>
        <p>
          We merge <strong>LSTM-based forecasting</strong> with <strong>VADER sentiment analysis</strong> 
          to give you a dual-lens view into market trends: the numbers and the news that drive them.
        </p>
      </section>

      <section>
        <h2> Why It Matters</h2>
        <p>
          Traditional tools miss the context. Our app connects data movements with public perception and current events
          so you understand not just the trends, but the causes behind them.
        </p>
      </section>

      <section>
        <h2> Technology Stack</h2>
        <p>
          We use <strong>Django</strong> to power our backend, <strong>React</strong> for the interface, 
          <strong>LSTM</strong> for long-term market forecasting, and <strong>VADER</strong> for real-time sentiment scoring.
        </p>
      </section>

      <section>
        <h2> Our Philosophy</h2>
        <p>
          We believe in <strong>transparent, responsible AI</strong>. Every insight is understandable, every result traceable—
          no black-box magic here.
        </p>
      </section>

      <section>
        <h2>Disclaimer</h2>
        <p>
          This is not financial advice. It’s a smart assistant to guide your thinking. 
          Please consult financial experts before making investment decisions.
        </p>
      </section>
    </div>
  );
};

export default About;