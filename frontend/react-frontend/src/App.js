import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MyNavbar from './components/MyNavbar';  // Navbar component
import HomePage from './components/HomePage';  // Home page component
import About from './components/About';  // About component
import MarketOverview from './components/MarketOverview';  // Market Overview component
import StockDetail from './components/StockDetail';  // Stock Detail component
import PredictionsPage from './components/Prediction';  // Predictions component
import SettingsPage from './components/SettingsPage';  // Settings page component


const App = () => {
  return (
    <Router>
      <MyNavbar />
      <Routes>
        <Route path="/home" element={<HomePage />} /> {/* Home Page route */}
        <Route path="/about" element={<About />} /> {/* About page route */}
        <Route path="/overview" element={<MarketOverview />} /> {/* Market overview route */}
        <Route path="/stock/:company" element={<StockDetail />} /> {/* Stock detail route */}
        <Route path="/predictions" element={<PredictionsPage />} /> {/* Predictions route */}
        <Route path="/settings" element={<SettingsPage />} /> {/* Settings route */}
      </Routes>
    </Router>
  );
};

export default App;