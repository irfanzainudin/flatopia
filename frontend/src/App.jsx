import { useState, useEffect } from 'react';
import FlatEarthSocietyLogo from '/flat_earth_society.png';
import { Plus, Globe, Mic, Send } from "lucide-react";
import { langOptions, langData } from './constants';

function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [currentLang, setCurrentLang] = useState("en");
  const [recommendations, setRecommendations] = useState(langData[currentLang].recommendations);

  useEffect(() => {
    resetRecommendations();
  }, [currentLang]);

  function resetRecommendations() {
    setRecommendations([]);
    setRecommendations(langData[currentLang].recommendations);
  }

  function resetCurrentLang() {
    setCurrentLang(`${keyName}`);
  }

  const handleSend = () => {
    if (!message.trim()) return; // ignore empty
    setChatHistory([...chatHistory, { role: "user", text: message }]);
    setMessage("");
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="w-full max-w-lg bg-white rounded-xl shadow-lg p-6 flex flex-col space-y-6">
        {/* Logo */}
        <div className="flex flex-col items-center space-y-3">
          <img src={FlatEarthSocietyLogo} alt="Twilio Logo" className="w-20 h-20" />
          <h2 className="text-lg font-semibold text-center">
            Find better opportunities overseas
          </h2>
          <p className="text-sm text-gray-500">By flatopia.co</p>
          <select id="lang-select" className="border rounded px-2 py-1 text-sm">
            {
              Object.keys(langOptions).map((keyName, keyIndex) => {
                return <option value={keyName} onClick={resetCurrentLang}>{langOptions[keyName]}</option>;
              })
            }
          </select>
        </div>

        {/* Quick action buttons */}
        <div className="grid grid-cols-2 gap-3">
          {recommendations.map((text, idx) => (
            <button
              key={idx}
              className="border rounded-lg px-3 py-2 text-sm text-left hover:bg-gray-100"
              onClick={() => setMessage(text)}
            >
              {text}
            </button>
          ))}
        </div>

        {/* Chat history */}
        <div className="flex flex-col space-y-3 max-h-64 overflow-y-auto border-t pt-3">
          {chatHistory.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`px-4 py-2 rounded-2xl text-sm ${
                  msg.role === "user"
                    ? "bg-blue-500 text-white rounded-br-none"
                    : "bg-gray-200 text-gray-800 rounded-bl-none"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        {/* Input bar */}
        <div className="flex items-center border rounded-lg px-3 py-2 space-x-3">
          <button>
            <Plus size={20} />
          </button>
          <button>
            <Globe size={20} />
          </button>
          <input
            type="text"
            placeholder="Message Flatopia"
            className="flex-1 border-none focus:ring-0 text-sm"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button>
            <Mic size={20} />
          </button>
          <button>
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}

export default App
