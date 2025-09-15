import React, { useEffect, useRef, useState } from "react";
// import FlatEarthSocietyLogo from '/flat_earth_society.png';
import FlatopiaLogo from '/flatopia-logo.png';
import { Plus, Globe, Mic, Send } from "lucide-react";
import { langOptions, langData } from './constants';

export default function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [currentLang, setCurrentLang] = useState("en");
  const [recommendations, setRecommendations] = useState(langData[currentLang].recommendations);
  const canvasRef = useRef(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    setRecommendations(langData[currentLang].recommendations);
  }, [currentLang]);

  const handleSend = () => {
    if (!message.trim()) return;
    setChatHistory(prev => [...prev, { role: "user", text: message }]);
    const userMessage = message;
    setMessage("");

    setTimeout(() => {
      const aiReply = currentLang === "en"
        ? `🤖 Flatopia says: Here's a fun response to: ${userMessage}`
        : `🤖 Flatopia说: 这是对你的消息的有趣回复: ${userMessage}`;
      setChatHistory(prev => [...prev, { role: "bot", text: aiReply }]);
    }, 1200);
  };

  const hasMessages = chatHistory.length > 0;

  // Auto-scroll whenever messages change or when the layout switches to chat view
  // Floating bubbles canvas (no text)
  useEffect(() => {
    // Use rAF so it runs after DOM paints
    requestAnimationFrame(() => {
      bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
    });
  }, [chatHistory, hasMessages]);

  // (Optional) keep bottom on window resize (e.g., when devtools open/close)
  useEffect(() => {
    const onResize = () =>
      bottomRef.current?.scrollIntoView({ behavior: "instant", block: "end" });
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div
        className={`bg-white shadow-lg flex flex-col transition-all duration-500 ${
          hasMessages
            ? "w-full h-screen max-w-none rounded-none" // full-screen chat
            : "w-full max-w-lg rounded-xl p-6 space-y-6" // small centered card
        }`}
      >
        {!hasMessages ? (
          // ---------------- Onboarding View ----------------
          <>
            {/* Logo */}
            <div className="flex flex-col items-center space-y-3">
              <img src={FlatopiaLogo} alt="Flatopia Logo" className="w-30 h-20" />
              <h2 className="text-lg font-semibold text-center">Find better opportunities overseas</h2>
              <p className="text-sm text-gray-500">By flatopia.co</p>
              <select
                value={currentLang}
                onChange={(e)=>setCurrentLang(e.target.value)}
                className="border rounded px-2 py-1 text-sm"
              >
                {Object.keys(langOptions).map((key) => (
                  <option key={key} value={key}>{langOptions[key]}</option>
                ))}
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
          </>
        ) : (
          // ---------------- Chat View ----------------
          <>
            {/* Chat thread */}
            <div className="flex-1 overflow-y-auto p-6 space-y-3">
              {chatHistory.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`px-4 py-2 rounded-2xl text-sm break-words max-w-[75%] ${
                      msg.role === "user"
                        ? "bg-blue-500 text-white rounded-br-none"
                        : "bg-gray-200 text-gray-800 rounded-bl-none"
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
              {/* Auto-scroll anchor */}
              <div ref={bottomRef} />
            </div>
          </>
        )}

        {/* Input bar (always visible) */}
        <div className="flex items-center border-t px-3 py-3 space-x-3">
          {/* <button className="text-gray-600 hover:text-gray-800">
            <Plus size={20} />
          </button>
          <button className="text-gray-600 hover:text-gray-800">
            <Globe size={20} />
          </button> */}
          <input
            type="text"
            placeholder={langData[currentLang].placeholder || "Message Flatopia"}
            className="flex-1 border-none focus:ring-0 text-sm bg-white rounded-lg px-3 py-2"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          {/* <button className="text-gray-600 hover:text-gray-800">
            <Mic size={20} />
          </button> */}
          <button
            className="text-gray-600 hover:text-gray-800"
            onClick={handleSend}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
