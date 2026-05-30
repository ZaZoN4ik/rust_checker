import React, { useState } from 'react';

const Faq = ({ goBack }) => {
  // Состояние для открытого вопроса (аккордеон)
  const [openIndex, setOpenIndex] = useState(null);

  const questions = [
    {
      q: "Могут ли меня забанить?",
      a: "Нет, вас не могут забанить. Наш сервис использует исключительно общедоступную информацию."
    },
    {
      q: "Почему иногда не показывается информация?",
      a: "Скорее всего, профиль является приватным и некоторые данные скрыты. В таком случае можете попробовать найти игрока по нику."
    },
    {
      q: "Что значит статус 'Спит'?",
      a: "После длительного отсутствия, статус 'Нет на месте' автоматически изменяется на 'Спит'."
    },
    {
      q: "Что такое баллы?",
      a: "Баллы — это внутренняя валюта бота. Поиск информации стоит 1 балл. Каждый день в 00:00 баллы восполняются (20 для обычных, 1000 для VIP)."
    }
  ];

  const toggleQuestion = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="search-view">
      <button className="back-button" onClick={goBack}>← В меню</button>
      <h2>Ответы на вопросы</h2>

      <div className="faq-list">
        {questions.map((item, index) => (
          <div
            key={index}
            className={`faq-item ${openIndex === index ? 'open' : ''}`}
            onClick={() => toggleQuestion(index)}
            style={{
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '12px',
              padding: '16px',
              marginBottom: '12px',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            <div style={{ fontWeight: '600', display: 'flex', justifyContent: 'space-between' }}>
              <span>{item.q}</span>
              <span>{openIndex === index ? '−' : '+'}</span>
            </div>
            {openIndex === index && (
              <div style={{ marginTop: '12px', fontSize: '14px', color: 'rgba(255, 255, 255, 0.8)', lineHeight: '1.4' }}>
                {item.a}
              </div>
            )}
          </div>
        ))}
      </div>

      <div style={{ marginTop: '24px', textAlign: 'center', fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>
        Остались вопросы? Напиши администратору.
      </div>
    </div>
  );
};

export default Faq;