import React, { useState, useEffect } from 'react';
import { initApp } from './utils/telegram';
import Home from './components/Views/Home';
import Search from './components/Views/Search';
import './styles/App.css';
import Faq from './components/Views/Faq';
import Profile from './components/Views/Profile';
import RaidCalc from './components/Views/RaidCalc';
import SearchSteam from './components/Views/SearchSteam';
import Trackings from './components/Views/Trackings';
import RustPlus from './components/Views/RustPlus';

// 🛠️ Универсальная заглушка для экранов, которые еще не готовы
const Placeholder = ({ title, goBack }) => {
  return (
    <div className="search-view" style={{ textAlign: 'center', paddingTop: '10vh' }}>
      <button className="back-button" onClick={goBack} style={{ display: 'inline-block', marginBottom: '20px' }}>
        ← В меню
      </button>
      <h2>{title}</h2>
      <p className="description" style={{ marginTop: '20px', display: 'inline-block' }}>
        Этот раздел находится в разработке 🛠️
      </p>
    </div>
  );
};

const App = () => {
  const [currentView, setCurrentView] = useState('home');

  useEffect(() => {
    initApp();
  }, []);

  // Наш мини-роутер
  const renderView = () => {
    switch (currentView) {
      case 'searchNick':
        return <Search goBack={() => setCurrentView('home')} />;

      // Добавляем обработку остальных кнопок
      case 'searchSteam':
        return <SearchSteam goBack={() => setCurrentView('home')} />;
      case 'tracking':
        return <Trackings goBack={() => setCurrentView('home')} />;
      case 'faq':
        return <Faq goBack={() => setCurrentView('home')} />;
      case 'raidCalc':
        return <RaidCalc goBack={() => setCurrentView('home')} />;
      case 'profile':
        return <Profile goBack={() => setCurrentView('home')} />;
      case 'rustPlus':
        return <RustPlus goBack={() => setCurrentView('home')} />;

      case 'home':
      default:
        return <Home navigateTo={setCurrentView} />;
    }
  };

  return (
    <div className="app-container">
      {renderView()}
    </div>
  );
};

export default App;