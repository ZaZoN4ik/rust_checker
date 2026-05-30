import React, { useEffect, useState } from 'react';

const Profile = ({ goBack }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Пытаемся получить данные из объекта Telegram
    const tg = window.Telegram?.WebApp;

    if (tg?.initDataUnsafe?.user) {
      setUser(tg.initDataUnsafe.user);
    } else {
      // Заглушка, если ты открыл приложение просто в браузере на компе (вне ТГ)
      setUser({
        first_name: "Выживший",
        last_name: "",
        username: "rust_player",
        id: 123456789,
        photo_url: ""
      });
    }
  }, []);

  return (
    <div className="search-view">
      <button className="back-button" onClick={goBack}>← В меню</button>
      <h2>Мой профиль</h2>

      {user && (
        <div className="profile-card" style={{
          background: 'rgba(255, 255, 255, 0.05)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(12px)',
          borderRadius: '16px',
          padding: '24px',
          textAlign: 'center',
          marginTop: '20px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
        }}>

          {/* Аватарка */}
          {user.photo_url ? (
            <img
              src={user.photo_url}
              alt="avatar"
              style={{ width: '84px', height: '84px', borderRadius: '50%', marginBottom: '16px', border: '2px solid var(--accent-color)' }}
            />
          ) : (
            <div style={{
              width: '84px', height: '84px', borderRadius: '50%',
              background: 'rgba(255,255,255,0.1)', border: '2px solid var(--accent-color)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '32px', margin: '0 auto 16px'
            }}>
              👤
            </div>
          )}

          {/* Имя и Ник */}
          <h3 style={{ margin: '0 0 8px 0', fontSize: '20px' }}>
            {user.first_name} {user.last_name}
          </h3>
          {user.username && (
            <div style={{ color: 'var(--accent-color)', marginBottom: '20px', fontSize: '15px' }}>
              @{user.username}
            </div>
          )}

          {/* Плашка со статистикой */}
          <div style={{
            background: 'rgba(0, 0, 0, 0.2)',
            padding: '16px',
            borderRadius: '12px',
            fontSize: '14px',
            color: 'rgba(255,255,255,0.8)',
            textAlign: 'left'
          }}>
            <p style={{ margin: '0 0 12px 0', display: 'flex', justifyContent: 'space-between' }}>
              <span>ID:</span>
              <span style={{color: '#fff'}}>{user.id}</span>
            </p>
            <p style={{ margin: '0 0 12px 0', display: 'flex', justifyContent: 'space-between' }}>
              <span>Баллы:</span>
              <span style={{color: '#fff'}}>⏳ Загрузка...</span>
            </p>
            <p style={{ margin: '0', display: 'flex', justifyContent: 'space-between' }}>
              <span>VIP Статус:</span>
              <span style={{color: '#fff'}}>⏳ Загрузка...</span>
            </p>
          </div>

        </div>
      )}
    </div>
  );
};

export default Profile;