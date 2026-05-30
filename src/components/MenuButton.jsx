import React from 'react';

const MenuButton = ({ icon, text, onClick, fullWidth = false }) => {
  return (
    <button
      className={`menu-button ${fullWidth ? 'full-width' : ''}`}
      onClick={onClick}
    >
      <span className="icon">{icon}</span>
      <span className="text">{text}</span>
    </button>
  );
};

export default MenuButton;