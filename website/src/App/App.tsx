import React, { useState } from "react";
import SendButton from "./SendButton";
import Messages from "./Messages";

function App() {
  const [text, setText] = useState("");
  const [history, setHistory] = useState<message[]>([]);

  const sendMessage = async () => {
    if (text.trim().length === 0) return;
    setHistory((history) => [...history, { sender: "user", text }]);
    setText("");
    console.log(JSON.stringify({ text }));
    try {
      const res = await fetch("/chatbot", {
        method: "POST",
        body: JSON.stringify({ text }),
        headers: { "Content-Type": "application/json" },
      });

      const { text: botMessage } = await res.json();

      setHistory((history) => [...history, { sender: "bot", text: botMessage }]);
    } catch (err) {
      console.error(err);
    }
  };

  const handleKeydown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.keyCode === 13) {
      sendMessage();
    }
  };

  return (
    <div className="chat">
      <div className="header">
        <h3>Coronabot</h3>
      </div>
      <Messages history={history} />
      <div className="input">
        <input type="text" onChange={(e) => setText(e.target.value)} value={text} placeholder="Ask a question" onKeyDown={handleKeydown} />
        <button
          className="send"
          onClick={sendMessage}
          style={{ backgroundColor: text.trim().length ? "rgb(23, 99, 212)" : "rgb(75, 74, 74)" }}
        >
          <SendButton />
        </button>
      </div>
    </div>
  );
}

export default App;
