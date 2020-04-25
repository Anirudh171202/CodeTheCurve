import React, { useState } from "react";
import yandex from "ya-translate";
import SendButton from "./SendButton";
import Messages from "./Messages";

const translate = yandex("trnsl.1.1.20200328T211017Z.ab2eb594adaba721.7c008849ce33008b5aa263bd3053e3604d886c64");

function App() {
  const [text, setText] = useState("");
  const [history, setHistory] = useState<message[]>([
    { sender: "user", text: "ani has alzheimers" },
    { sender: "bot", text: "Yes that is fax" },
  ]);

  const sendMessage = async () => {
    if (text.trim().length === 0) return;
    setHistory((history) => [...history, { sender: "user", text }]);
    setText("");

    const {
      detected: { lang },
      transArr,
    } = await translate.translate(text.trim());
    const translatedText = transArr[0];

    // Dialogflow
    let botMessage = "dialogflow_stuff";

    if (lang !== "en") {
      botMessage = await translate.translate(botMessage, lang);
    }

    setHistory((history) => [...history, { sender: "bot", text: botMessage }]);
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
