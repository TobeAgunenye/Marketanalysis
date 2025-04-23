import 'bootstrap/dist/css/bootstrap.min.css';  // Import Bootstrap CSS globally
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';  // Ensure App is imported correctly

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />  {/* App is the root component */}
  </React.StrictMode>
);