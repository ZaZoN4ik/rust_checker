import React from 'react';
import MenuButton from '../MenuButton';

const Home = ({ navigateTo }) => {
  return (
    <div className="home-view">
      <div className="button-grid">
        <MenuButton icon="🔍" text="Стим" onClick={() => navigateTo('searchSteam')} />
        <MenuButton icon="🔍" text="Ник" onClick={() => navigateTo('searchNick')} />

        <MenuButton icon="👁" text="Мои отслеживания" onClick={() => navigateTo('tracking')} />
        <MenuButton icon="❓" text="Ответы на вопросы" onClick={() => navigateTo('faq')} />

        <MenuButton icon="🧮" text="Калькулятор рейда" onClick={() => navigateTo('raidCalc')} />
        <MenuButton icon="👤" text="Мой профиль" onClick={() => navigateTo('profile')} />
      </div>

      <div className="full-width-container">
        <MenuButton icon="📡" text="Rust+ события" fullWidth={true} onClick={() => navigateTo('rustPlus')} />
      </div>
    </div>
  );
};

export default Home;