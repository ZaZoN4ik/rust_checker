import React, { useEffect } from 'react';
import { showMainButton, hideMainButton, sendDataToBot } from '../../utils/telegram';

const Trackings = ({ goBack }) => {

  useEffect(() => {
    showMainButton('Вывести список в чат', () => {
      sendDataToBot('GET_TRACKINGS');
    });

    return () => hideMainButton();
  }, []);

  return (
    <div className="search-view">
      <button className="back-button" onClick={goBack}>← Назад</button>

      <h2>👁 Мои отслеживания</h2>

      <div className="profile-card" style={{
        background: 'rgba(255, 255, 255, 0.05)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(12px)',
        borderRadius: '16px',
        padding: '24px',
        textAlign: 'center',
        marginTop: '20px'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '16px' }}>📡</div>
        <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '15px', lineHeight: '1.5' }}>
          Бот круглосуточно следит за игроками из вашего списка. <br/><br/>
          Нажмите на кнопку внизу, чтобы получить актуальный список ваших отслеживаний прямо в чат Telegram, где вы сможете удалить их или обновить информацию.
        </p>
      </div>
    </div>
  );
};

export default Trackings;