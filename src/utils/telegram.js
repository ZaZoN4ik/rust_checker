const tg = window.Telegram.WebApp;

export const initApp = () => {
  tg.expand(); // Разворачиваем на весь экран
  tg.ready();  // Сообщаем телеграму, что приложение готово
};

// Функция для отправки данных обратно в бота
export const sendDataToBot = (action, payload = {}) => {
  const data = JSON.stringify({ action, ...payload });
  tg.sendData(data);
};

export const getThemeColors = () => ({
  bgColor: tg.themeParams.bg_color || '#1c1c1d',
  textColor: tg.themeParams.text_color || '#ffffff',
  buttonColor: tg.themeParams.button_color || '#2c2c2e',
  buttonTextColor: tg.themeParams.button_text_color || '#ffffff'
});

export const showMainButton = (text, onClick) => {
    tg.MainButton.setText(text);
    tg.MainButton.show();
    tg.MainButton.onClick(onClick);
};

export const hideMainButton = () => {
    tg.MainButton.hide();
};