import React from 'react';

const RustPlus = ({ goBack }) => {
  return (
    <div className="search-view">
      <button className="back-button" onClick={goBack}>← Назад</button>

      <h2>📡 Rust+ События</h2>

      <div className="profile-card" style={{
        background: 'rgba(255, 255, 255, 0.05)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        borderRadius: '16px',
        padding: '24px',
        textAlign: 'center',
        marginTop: '20px'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '16px' }}>🛠️</div>
        <h3 style={{ margin: '0 0 12px 0', color: 'var(--accent-color)' }}>В разработке</h3>
        <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '14px', lineHeight: '1.5' }}>
          Интеграция с официальным API Rust+ находится в стадии тестирования. <br/><br/>
          Скоро здесь появится возможность привязывать сервера и получать пуш-уведомления о срабатывании умных будильников и уничтожении турелей.
        </p>
      </div>
    </div>
  );
};

export default RustPlus;