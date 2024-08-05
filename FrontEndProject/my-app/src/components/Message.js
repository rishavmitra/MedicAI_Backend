
import React from 'react';
import './Message.css'; 

const Message = ({ text, fromUser }) => {
  return (
    <div className={`message ${fromUser ? 'user' : 'other'}`}>
      <p>{text}</p>
    </div>
  );
};

export default Message;
