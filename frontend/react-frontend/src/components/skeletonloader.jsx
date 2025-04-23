import React from 'react';

const SkeletonLoader = () => (
  <div 
    className="skeleton" 
    style={{
      width: '100%',
      height: '150px',
      borderRadius: '8px',
      backgroundColor: '#e0e0e0',
      animation: 'pulse 1.5s infinite ease-in-out'
    }}
  ></div>
);

export default SkeletonLoader;
