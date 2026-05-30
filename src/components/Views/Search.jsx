import React, { useState, useEffect } from 'react';
import { showMainButton, hideMainButton, sendDataToBot } from '../../utils/telegram';

const Search = ({ goBack }) => {
  const [nickname, setNickname] = useState('');

  // Управляем главной кнопкой Telegram при вводе текста
  useEffect(() => {
    if (nickname.trim().length > 0) {
      showMainButton('Найти игрока', handleSearch);
    } else {
      hideMainButton();
    }

    return () => hideMainButton(); // Очистка при размонтировании
  }, [nickname]);

  const handleSearch = () => {
    // Отправляем данные в бота и закрываем Web App
    sendDataToBot('SEARCH_NICK', { nickname });
  };

  return (
    <div className="search-view">
      <button className="back-button" onClick={goBack}>← Назад</button>

      <h2>Поиск по нику</h2>
      <p className="description">
        Обратите внимание, ник должен в точности соответствовать нику игрока,
        иначе бот его не найдет. А так же бот ищет игроков, которые были
        в онлайне за последние две недели.
      </p>

      <input
        type="text"
        className="tg-input"
        placeholder="Введите Ник игрока..."
        value={nickname}
        onChange={(e) => setNickname(e.target.value)}
        autoFocus
      />
    </div>
  );
};

export default Search;