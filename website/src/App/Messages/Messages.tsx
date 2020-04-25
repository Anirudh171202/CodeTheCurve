import React, { useState } from "react";

interface MessagesProps {
  history: message[];
}

function Messages({ history }: MessagesProps) {
  return (
    <div className="messages">
      {history.map((message, index) => (
        <div className="message" key={index} style={{ justifyContent: message.sender === "bot" ? "flex-start" : "flex-end" }}>
          <p className={`bubble ${message.sender}`}>{message.text}</p>
        </div>
      ))}
    </div>
  );
}

export default Messages;
