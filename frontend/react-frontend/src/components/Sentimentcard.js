import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SentimentCard = ({ company }) => {
  const [sentimentData, setSentimentData] = useState(null);
  const [currentArticleIndex, setCurrentArticleIndex] = useState(0); // Track current article index
  const [isDataLoaded, setIsDataLoaded] = useState(false); // Track if data is loaded
  const [fadeClass, setFadeClass] = useState(''); // Track fade class for transition

  useEffect(() => {
    const fetchSentimentData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/sentiment/${company}/`);
        setSentimentData(response.data.results);  // Assuming your data is in the 'results' key
        setIsDataLoaded(true); // Set data as loaded
      } catch (err) {
        console.error('Error fetching sentiment data:', err);
      }
    };

    fetchSentimentData();
  }, [company]); // Fetch sentiment data when company changes

  useEffect(() => {
    if (isDataLoaded && sentimentData && sentimentData.length > 0) {
      // Set an interval to change the current article every 5 seconds
      const interval = setInterval(() => {
        setFadeClass(''); // Reset the fade class
        setCurrentArticleIndex((prevIndex) => (prevIndex + 1) % sentimentData.length);  // Cycle through articles

        // After the article changes, apply the fade class again after a brief delay to trigger transition
        setTimeout(() => {
          setFadeClass('show');
        }, 50); // Delay to allow the opacity reset to take effect
      }, 5000); // Change article every 5 seconds

      // Clean up the interval on unmount
      return () => clearInterval(interval);
    }
  }, [isDataLoaded, sentimentData]); // Only run interval when data is loaded and available

  if (!sentimentData) {
    return <p>Loading sentiment data...</p>;
  }

  const currentArticle = sentimentData[currentArticleIndex];

  return (
    <div className="card mb-4">
      <div className="card-body">
        <h5 className="card-title">Sentiment Analysis for {company}</h5>
        <div className={`fade-card ${fadeClass}`} style={{ transition: 'opacity 1s' }}>
          {currentArticle && (
            <>
              <h6>{currentArticle.article_title}</h6>
              <p>{currentArticle.sentiment_label} - Score: {currentArticle.sentiment_score}</p>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default SentimentCard;