import React, { useState } from 'react';

// Данные о стоимости рейда (на 1 предмет)
const RAID_ITEMS = [
  { id: 'wood_door', name: 'Деревянная дверь', icon: '🚪', costs: { c4: 1, rocket: 2, satchel: 2, ammo: 18 } },
  { id: 'sheet_door', name: 'Железная дверь', icon: '🚪', costs: { c4: 1, rocket: 2, satchel: 4, ammo: 63 } },
  { id: 'garage_door', name: 'Гаражная дверь', icon: '🪟', costs: { c4: 2, rocket: 3, satchel: 9, ammo: 150 } },
  { id: 'armored_door', name: 'МВК дверь', icon: '🛡️', costs: { c4: 2, rocket: 4, satchel: 15, ammo: 200 } },
  { id: 'stone_wall', name: 'Каменная стена', icon: '🧱', costs: { c4: 2, rocket: 4, satchel: 10, ammo: 185 } },
  { id: 'metal_wall', name: 'Железная стена', icon: '🏗️', costs: { c4: 4, rocket: 8, satchel: 23, ammo: 400 } },
  { id: 'armored_wall', name: 'МВК стена', icon: '🏰', costs: { c4: 8, rocket: 15, satchel: 46, ammo: 799 } },
];

const RaidCalc = ({ goBack }) => {
  const [selectedItem, setSelectedItem] = useState(RAID_ITEMS[2]); // По умолчанию Гаражка
  const [quantity, setQuantity] = useState(1);

  const changeQuantity = (amount) => {
    const newQuantity = quantity + amount;
    if (newQuantity >= 1 && newQuantity <= 100) {
      setQuantity(newQuantity);
    }
  };

  return (
    <div className="search-view">
      <button className="back-button" onClick={goBack}>← В меню</button>
      <h2>Калькулятор рейда</h2>

      {/* Сетка выбора предметов */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))',
        gap: '8px',
        marginBottom: '20px'
      }}>
        {RAID_ITEMS.map((item) => (
          <button
            key={item.id}
            onClick={() => { setSelectedItem(item); setQuantity(1); }}
            style={{
              background: selectedItem.id === item.id ? 'var(--accent-color)' : 'rgba(255, 255, 255, 0.05)',
              border: `1px solid ${selectedItem.id === item.id ? 'var(--accent-color)' : 'rgba(255, 255, 255, 0.1)'}`,
              borderRadius: '12px',
              padding: '12px 8px',
              color: '#fff',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '4px'
            }}
          >
            <span style={{ fontSize: '24px' }}>{item.icon}</span>
            <span style={{ fontSize: '11px', textAlign: 'center' }}>{item.name}</span>
          </button>
        ))}
      </div>

      {/* Панель подсчета */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.05)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(12px)',
        borderRadius: '16px',
        padding: '20px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
      }}>

        {/* Выбор количества */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <div style={{ fontWeight: '600', fontSize: '16px' }}>
            Количество:
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', padding: '4px' }}>
            <button onClick={() => changeQuantity(-1)} style={{ background: 'none', border: 'none', color: '#fff', fontSize: '20px', width: '32px', height: '32px', cursor: 'pointer' }}>-</button>
            <span style={{ fontSize: '18px', fontWeight: 'bold', width: '24px', textAlign: 'center' }}>{quantity}</span>
            <button onClick={() => changeQuantity(1)} style={{ background: 'none', border: 'none', color: '#fff', fontSize: '20px', width: '32px', height: '32px', cursor: 'pointer' }}>+</button>
          </div>
        </div>

        {/* Результаты (стоимость) */}
        <div style={{ fontSize: '15px', color: 'rgba(255,255,255,0.9)' }}>
          <div style={{ marginBottom: '16px', textAlign: 'center', color: 'var(--accent-color)', fontWeight: 'bold' }}>
            Для уничтожения: {selectedItem.name} (x{quantity})
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', marginBottom: '8px' }}>
            <span>🧨 C4 (Взрывчатка):</span>
            <span style={{ fontWeight: 'bold' }}>{selectedItem.costs.c4 * quantity} шт.</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', marginBottom: '8px' }}>
            <span>🚀 Ракеты:</span>
            <span style={{ fontWeight: 'bold' }}>{selectedItem.costs.rocket * quantity} шт.</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', marginBottom: '8px' }}>
            <span>🎒 Сачели:</span>
            <span style={{ fontWeight: 'bold' }}>{selectedItem.costs.satchel * quantity} шт.</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px' }}>
            <span>💥 Разрывные пули:</span>
            <span style={{ fontWeight: 'bold' }}>{selectedItem.costs.ammo * quantity} шт.</span>
          </div>
        </div>

      </div>
    </div>
  );
};

export default RaidCalc;