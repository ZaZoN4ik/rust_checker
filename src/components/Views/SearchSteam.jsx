import React, { useState, useEffect } from 'react';
import { showMainButton, hideMainButton, sendDataToBot } from '../../utils/telegram';

const SearchSteam = ({ goBack }) => {
  const [steamId, setSteamId] = useState('');

  useEffect(() => {
    if (steamId.trim().length > 0) {
      showMainButton('Найти профиль', () => {
        sendDataToBot('SEARCH_STEAM', { steamId });
      });
    } else {
      hideMainButton();
    }

    return () => hideMainButton();
  }, [steamId]);

  return (
    <div className="search-view">
      <button className="back-button" onClick={goBack}>← Назад</button>

      <h2>Поиск по Steam ID</h2>
      <p className="description">
        Введите Steam ID (17 цифр), прямую ссылку на профиль или кастомную ссылку (vanity url).
        Например: <code>7656119...</code> или <code>/id/nickname</code>.
      </p>

      <input
        type="text"
        className="tg-input"
        placeholder="Введите Steam ID или ссылку..."
        value={steamId}
        onChange={(e) => setSteamId(e.target.value)}
        autoFocus
      />
    </div>
  );
};

export default SearchSteam;